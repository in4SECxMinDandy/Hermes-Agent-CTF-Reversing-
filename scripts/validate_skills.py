#!/usr/bin/env python3
"""Validate bundled SKILL.md files and report content-quality warnings."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from agent.skill_utils import parse_frontmatter
from tools.skill_manager_tool import _validate_content_size, _validate_frontmatter


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ROOTS = (REPO_ROOT / "skills", REPO_ROOT / "optional-skills")


@dataclass(frozen=True)
class Finding:
    path: Path
    message: str
    severity: str


def iter_skill_files(roots: tuple[Path, ...] = DEFAULT_ROOTS) -> list[Path]:
    """Return deterministic SKILL.md files from the shipped skill trees."""
    return sorted(
        path
        for root in roots
        if root.exists()
        for path in root.rglob("SKILL.md")
        if path.is_file()
    )


def validate_skill_file(path: Path) -> list[Finding]:
    content = path.read_text(encoding="utf-8")
    findings: list[Finding] = []

    for error in (_validate_frontmatter(content), _validate_content_size(content)):
        if error:
            findings.append(Finding(path, error, "error"))

    frontmatter, body = parse_frontmatter(content)
    if not frontmatter:
        return findings

    if not any(marker in body.lower() for marker in ("when to use", "use when")):
        findings.append(Finding(path, "missing a clear 'When to Use' trigger section", "warning"))
    if not any(marker in body.lower() for marker in ("verification", "validation", "verify", "tests")):
        findings.append(Finding(path, "missing an explicit verification or validation step", "warning"))

    metadata = frontmatter.get("metadata")
    hermes_metadata = metadata.get("hermes", {}) if isinstance(metadata, dict) else {}
    if not isinstance(hermes_metadata, dict) or not hermes_metadata.get("tags"):
        findings.append(Finding(path, "missing metadata.hermes.tags", "warning"))

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="fail on errors (warnings remain advisory)")
    args = parser.parse_args(argv)

    files = iter_skill_files()
    findings = [finding for path in files for finding in validate_skill_file(path)]
    errors = [finding for finding in findings if finding.severity == "error"]
    warnings = [finding for finding in findings if finding.severity == "warning"]

    for finding in findings:
        relative = finding.path.relative_to(REPO_ROOT).as_posix()
        print(f"{finding.severity.upper()}: {relative}: {finding.message}")

    print(f"Validated {len(files)} skills: {len(errors)} errors, {len(warnings)} warnings")
    return 1 if args.strict and errors else 0


if __name__ == "__main__":
    sys.exit(main())
