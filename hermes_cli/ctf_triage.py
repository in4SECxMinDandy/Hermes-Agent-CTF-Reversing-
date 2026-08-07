"""Deterministic category triage for authorized CTF challenge workspaces."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

import yaml

from hermes_cli.ctf import CTFError
from hermes_cli.ctf_benchmark import _slug_category

_TRIAGE_SCRIPTS = {
    "web": (
        "find distfiles -maxdepth 2 -type f -print -exec file {} \\; 2>&1 || true\n"
        "find distfiles -maxdepth 2 -type f -print -exec head -c 4096 {} \\; 2>&1 || true"
    ),
    "crypto": (
        "find distfiles -maxdepth 2 -type f -print -exec file {} \\; 2>&1 || true\n"
        "python3 - <<'PY'\n"
        "try:\n from Crypto.Util.number import long_to_bytes\n print('pycryptodome: ready')\n"
        "except Exception as exc:\n print(f'pycryptodome: unavailable ({exc})')\n"
        "PY\n"
        "find distfiles -maxdepth 2 -type f -exec strings -a {} \\; 2>/dev/null | head -200 || true"
    ),
    "reverse": (
        "find distfiles -maxdepth 2 -type f -print -exec file {} \\; 2>&1 || true\n"
        "r2 -v 2>&1 | head -5 || true\n"
        "find distfiles -maxdepth 2 -type f -exec strings -a {} \\; 2>/dev/null | head -300 || true"
    ),
    "forensics": (
        "find distfiles -maxdepth 2 -type f -print -exec file {} \\; 2>&1 || true\n"
        "find distfiles -maxdepth 2 -type f -exec exiftool {} \\; 2>/dev/null | head -300 || true\n"
        "find distfiles -maxdepth 2 -type f -exec binwalk {} \\; 2>/dev/null | head -200 || true"
    ),
    "binary": (
        "find distfiles -maxdepth 2 -type f -print -exec file {} \\; 2>&1 || true\n"
        "find distfiles -maxdepth 2 -type f -exec checksec --file={} \\; 2>/dev/null || true\n"
        "find distfiles -maxdepth 2 -type f -exec readelf -h {} \\; 2>/dev/null | head -200 || true\n"
        "find distfiles -maxdepth 2 -type f -exec strings -a {} \\; 2>/dev/null | head -300 || true"
    ),
}
_UNIVERSAL_SCRIPT = (
    "find distfiles -maxdepth 2 -type f -print -exec file {} \\; 2>&1 || true\n"
    "find distfiles -maxdepth 2 -type f -exec sha256sum {} \\; 2>/dev/null || true"
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _short_output(value: str, limit: int = 12000) -> str:
    if len(value) <= limit:
        return value
    return value[:limit] + f"\n...[truncated {len(value) - limit} chars]"


def _load_metadata(challenge_dir: Path) -> dict[str, Any]:
    metadata_path = challenge_dir / "metadata.yml"
    if not metadata_path.is_file():
        raise CTFError(f"Challenge metadata does not exist: {metadata_path}")
    try:
        raw = yaml.safe_load(metadata_path.read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        raise CTFError(f"Could not read challenge metadata: {exc}") from exc
    if not isinstance(raw, Mapping):
        raise CTFError("Challenge metadata root must be a mapping")
    return dict(raw)


def _run(command: list[str], *, cwd: Path, timeout: float) -> dict[str, Any]:
    started = time.perf_counter()
    try:
        result = subprocess.run(
            command,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=max(1.0, timeout),
        )
        return {
            "command": command,
            "returncode": result.returncode,
            "stdout": _short_output(result.stdout or ""),
            "stderr": _short_output(result.stderr or ""),
            "timed_out": False,
            "seconds": round(time.perf_counter() - started, 4),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command,
            "returncode": -1,
            "stdout": _short_output(str(exc.stdout or "")),
            "stderr": _short_output(str(exc.stderr or "")),
            "timed_out": True,
            "seconds": round(time.perf_counter() - started, 4),
        }
    except OSError as exc:
        return {
            "command": command,
            "returncode": -1,
            "stdout": "",
            "stderr": str(exc),
            "timed_out": False,
            "seconds": round(time.perf_counter() - started, 4),
        }


def _append_findings(challenge_dir: Path, report_path: Path, category: str, engine: str) -> None:
    findings = challenge_dir / "findings.md"
    if not findings.exists():
        findings.write_text(f"# {challenge_dir.name} findings\n", encoding="utf-8")
    with findings.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n## Automated {category} triage ({_now()})\n\n"
            f"- Engine: `{engine}`\n"
            f"- Report: `{report_path.relative_to(challenge_dir)}`\n"
            "- Fixed probes ran against distfiles; review the report before escalating.\n"
        )


def run_triage(
    challenge_dir: Path,
    *,
    image: str = "ctf-sandbox",
    engine: str = "auto",
    network: str = "none",
    timeout: float = 90.0,
) -> dict[str, Any]:
    """Run fixed category probes and persist evidence under ``workspace/triage``."""
    challenge_dir = challenge_dir.expanduser().resolve()
    if not challenge_dir.is_dir():
        raise CTFError(f"Challenge directory does not exist: {challenge_dir}")
    metadata = _load_metadata(challenge_dir)
    category = _slug_category(metadata.get("category"))
    if category not in _TRIAGE_SCRIPTS:
        raise CTFError(
            f"Unsupported triage category {metadata.get('category')!r}; use web, crypto, reverse, forensics, or binary"
        )
    if network not in {"none", "host"}:
        raise CTFError("Triage network must be 'none' or 'host'")
    if engine not in {"auto", "docker", "local"}:
        raise CTFError("Triage engine must be 'auto', 'docker', or 'local'")
    for name in ("distfiles", "workspace", "traces"):
        (challenge_dir / name).mkdir(exist_ok=True)
    docker = shutil.which("docker")
    use_docker = engine == "docker" or (engine == "auto" and docker is not None)
    if use_docker and not docker:
        raise CTFError("Docker triage was requested but docker is unavailable")
    script = _UNIVERSAL_SCRIPT + "\n\n" + _TRIAGE_SCRIPTS[category]
    if use_docker:
        command = [
            docker,
            "run",
            "--rm",
            "--network",
            network,
            "-v",
            f"{challenge_dir / 'distfiles'}:/challenge/distfiles:ro",
            "-v",
            f"{challenge_dir / 'workspace'}:/challenge/workspace:rw",
            "-v",
            f"{challenge_dir / 'metadata.yml'}:/challenge/metadata.yml:ro",
            "-w",
            "/challenge",
            image,
            "sh",
            "-lc",
            script,
        ]
        result = _run(command, cwd=challenge_dir, timeout=timeout)
        selected_engine = "docker"
    else:
        shell = shutil.which("bash") or shutil.which("sh")
        if not shell:
            raise CTFError("Local triage needs a POSIX shell; use --engine docker")
        result = _run([shell, "-lc", script], cwd=challenge_dir, timeout=timeout)
        selected_engine = "local"
    triage_dir = challenge_dir / "workspace" / "triage"
    triage_dir.mkdir(parents=True, exist_ok=True)
    report_path = triage_dir / f"{category}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    report = {
        "generated_at": _now(),
        "challenge": str(challenge_dir),
        "name": str(metadata.get("name") or challenge_dir.name),
        "category": category,
        "engine": selected_engine,
        "network": network,
        "result": result,
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _append_findings(challenge_dir, report_path, category, selected_engine)
    report["report_path"] = str(report_path)
    return report
