from pathlib import Path

ROOT = Path(__file__).parents[1]
H1 = "TripAdvisor Hotel Review Data Scraper｜猫途鹰酒店评论爬虫与数据获取"


def test_tripadvisor_has_complete_bilingual_entrypoints() -> None:
    english = (ROOT / "README.md").read_text(encoding="utf-8")
    chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    assert english.splitlines()[0] == f"# {H1}"
    assert "README.zh-CN.md" in english
    assert "README.md" in chinese
    assert "猫途鹰" in english + chinese
    assert "travel-data-connectors" not in english + chinese
    assert all(term in english for term in ("Architecture", "Technical route", "Problems", "Validation", "Responsible use", "Contact"))
    assert all(term in chinese for term in ("架构", "技术路线", "问题", "验证", "负责任使用", "联系"))


def test_tripadvisor_support_boundary_is_explicit() -> None:
    text = "\n".join((ROOT / name).read_text(encoding="utf-8") for name in ("README.md", "README.zh-CN.md", "CONTRIBUTING.md", "SECURITY.md"))
    assert "GitHub Issues" in text
    assert "wwk990630@gmail.com" in text
    assert "cookies" in text.lower()
