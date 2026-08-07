from pathlib import Path

from scripts.validate_skills import validate_skill_file


def _write_skill(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "SKILL.md"
    path.write_text(
        "---\nname: demo\ndescription: Use when testing skill validation.\n"
        "metadata:\n  hermes:\n    tags: [testing]\n---\n"
        + body,
        encoding="utf-8",
    )
    return path


def test_valid_skill_has_no_findings(tmp_path):
    assert validate_skill_file(
        _write_skill(tmp_path, "## When to Use\nUse for tests.\n\n## Verification\nRun the test.\n")
    ) == []


def test_quality_warnings_do_not_block_valid_frontmatter(tmp_path):
    findings = validate_skill_file(_write_skill(tmp_path, "General instructions.\n"))
    assert not [finding for finding in findings if finding.severity == "error"]
    assert {finding.message for finding in findings} == {
        "missing a clear 'When to Use' trigger section",
        "missing an explicit verification or validation step",
    }


def test_oversized_skill_is_an_error(tmp_path):
    path = _write_skill(tmp_path, "x" * 100_001)
    findings = validate_skill_file(path)
    assert any(finding.severity == "error" for finding in findings)
