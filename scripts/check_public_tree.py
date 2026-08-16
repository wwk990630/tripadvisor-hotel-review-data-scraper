from __future__ import annotations

import argparse
import re
from dataclasses import asdict, dataclass
from pathlib import Path


TEXT_SUFFIXES = {".ini", ".json", ".md", ".py", ".toml", ".txt", ".yaml", ".yml"}
COLLECTED_DATA_SUFFIXES = {".csv", ".har", ".jsonl"}
IGNORED_PARTS = {".git", ".pytest_cache", "__pycache__"}
ALLOWED_RULES = {
    ("scripts/check_public_tree.py", "credential-assignment"),
    ("scripts/check_public_tree.py", "secret-prefix"),
    ("scripts/check_public_tree.py", "absolute-user-path"),
    ("scripts/check_public_tree.py", "reviewer-identity-fixture"),
    ("tests/test_public_tree.py", "credential-assignment"),
}

CONTENT_RULES = {
    "credential-assignment": re.compile(
        r"(?i)\b(cookie|authorization|session(?:id)?|token|proxy_password|secret_id|signature)\b\s*[:=]\s*[\"'][^\"']+"
    ),
    "secret-prefix": re.compile(r"(?i)\b(gho_|ghp_|github_pat_|bearer\s+[a-z0-9])"),
    "absolute-user-path": re.compile(r"(?i)\b[a-z]:\\users\\"),
}
IDENTITY_FIXTURE_RULE = re.compile(
    r'(?i)[\"\'](userProfile|userId|username|displayName|profileUrl)[\"\']\s*:'
)


@dataclass(frozen=True, slots=True)
class Finding:
    path: str
    rule_id: str
    line: int | None

    def to_dict(self) -> dict[str, str | int | None]:
        return asdict(self)


def _allowed(path: str, rule_id: str) -> bool:
    return (path, rule_id) in ALLOWED_RULES


def scan_tree(root: Path) -> list[Finding]:
    root = root.resolve()
    findings: list[Finding] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        relative_text = relative.as_posix()
        if any(part in IGNORED_PARTS for part in relative.parts):
            continue
        if not path.is_file():
            continue
        if path.suffix.lower() in COLLECTED_DATA_SUFFIXES:
            findings.append(Finding(relative_text, "collected-data-file", None))
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for rule_id, pattern in CONTENT_RULES.items():
                if pattern.search(line) and not _allowed(relative_text, rule_id):
                    findings.append(Finding(relative_text, rule_id, line_number))
            if (
                path.suffix.lower() == ".json"
                and IDENTITY_FIXTURE_RULE.search(line)
                and not _allowed(relative_text, "reviewer-identity-fixture")
            ):
                findings.append(
                    Finding(relative_text, "reviewer-identity-fixture", line_number)
                )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan the public repository tree.")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    findings = scan_tree(Path(args.root))
    for finding in findings:
        location = finding.path if finding.line is None else f"{finding.path}:{finding.line}"
        print(f"{finding.rule_id}: {location}")
    if findings:
        print(f"Public-tree scan failed with {len(findings)} finding(s).")
        return 1
    print("Public-tree scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
