import json
from pathlib import Path

from scripts.check_public_tree import scan_tree


ROOT = Path(__file__).resolve().parents[1]


def test_reports_a_credential_assignment_without_echoing_its_value(tmp_path: Path) -> None:
    secret = "example-secret-that-must-not-appear"
    (tmp_path / "leak.py").write_text(
        f'cookie = "{secret}"\n',
        encoding="utf-8",
    )

    findings = scan_tree(tmp_path)
    serialized = json.dumps([finding.to_dict() for finding in findings])

    assert [finding.rule_id for finding in findings] == ["credential-assignment"]
    assert secret not in serialized


def test_rejects_collected_data_file_types(tmp_path: Path) -> None:
    (tmp_path / "reviews.jsonl").write_text("{}\n", encoding="utf-8")
    (tmp_path / "reviews.csv").write_text("id\n1\n", encoding="utf-8")

    findings = scan_tree(tmp_path)

    assert [finding.rule_id for finding in findings] == [
        "collected-data-file",
        "collected-data-file",
    ]


def test_current_public_tree_is_safe() -> None:
    assert scan_tree(ROOT) == []
