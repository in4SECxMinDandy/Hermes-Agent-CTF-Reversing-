"""Deterministic, local benchmark runner for authorized CTF workspaces.

The benchmark measures workflow reliability and evidence quality. It is not a
claim that a solver can solve every challenge; model solve-rate must be
measured against a representative corpus separately.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

import yaml

from hermes_cli.ctf import CTFError

BENCHMARK_CATEGORIES = (
    "web",
    "crypto",
    "reverse",
    "forensics",
    "binary",
)
_CATEGORY_ALIASES = {
    "web exploitation": "web",
    "web": "web",
    "cryptography": "crypto",
    "crypto": "crypto",
    "reverse engineering": "reverse",
    "reverse": "reverse",
    "digital forensics": "forensics",
    "forensics": "forensics",
    "binary exploitation": "binary",
    "binary": "binary",
    "pwn": "binary",
}
_REQUIRED_ARTIFACTS = (
    "metadata.yml",
    "distfiles",
    "workspace",
    "findings.md",
    "traces",
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _short_output(value: str, limit: int = 8000) -> str:
    if len(value) <= limit:
        return value
    return value[:limit] + f"\n...[truncated {len(value) - limit} chars]"


def _slug_category(value: Any) -> str:
    normalized = str(value or "").strip().casefold()
    return _CATEGORY_ALIASES.get(normalized, normalized)


def _inside(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


@dataclass(frozen=True)
class BenchmarkCase:
    path: Path
    name: str
    category: str
    verifier: Path

    @property
    def artifacts(self) -> dict[str, bool]:
        return {
            name: (self.path / name).is_dir() if name in {"distfiles", "workspace", "traces"}
            else (self.path / name).is_file()
            for name in _REQUIRED_ARTIFACTS
        }


def discover_benchmark_cases(root: Path) -> list[BenchmarkCase]:
    """Discover normalized challenge workspaces below ``root`` safely."""
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise CTFError(f"Benchmark root does not exist or is not a directory: {root}")
    cases: list[BenchmarkCase] = []
    for candidate in sorted(root.iterdir(), key=lambda item: item.name.casefold()):
        if not candidate.is_dir():
            continue
        metadata_path = candidate / "metadata.yml"
        if not metadata_path.is_file():
            continue
        try:
            raw = yaml.safe_load(metadata_path.read_text(encoding="utf-8")) or {}
        except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
            raise CTFError(f"Could not read benchmark metadata {metadata_path}: {exc}") from exc
        if not isinstance(raw, Mapping):
            raise CTFError(f"Benchmark metadata must be a mapping: {metadata_path}")
        category = _slug_category(raw.get("category"))
        if category not in BENCHMARK_CATEGORIES:
            raise CTFError(
                f"Unsupported benchmark category {raw.get('category')!r} in {metadata_path}"
            )
        benchmark = raw.get("benchmark")
        verifier_value = benchmark.get("verifier") if isinstance(benchmark, Mapping) else None
        verifier = (candidate / str(verifier_value or "workspace/verify.py")).resolve()
        if not _inside(verifier, candidate) or not verifier.is_file():
            raise CTFError(f"Benchmark verifier must be a file inside the case: {verifier}")
        cases.append(
            BenchmarkCase(
                path=candidate,
                name=str(raw.get("name") or candidate.name),
                category=category,
                verifier=verifier,
            )
        )
    return cases


def _run_verifier(case: BenchmarkCase, timeout: float) -> dict[str, Any]:
    env = os.environ.copy()
    env["HERMES_CTF_BENCHMARK"] = "1"
    started = time.perf_counter()
    try:
        result = subprocess.run(
            [sys.executable, str(case.verifier)],
            cwd=str(case.path / "workspace"),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=max(1.0, timeout),
        )
        stdout = _short_output(result.stdout or "")
        stderr = _short_output(result.stderr or "")
        return {
            "returncode": result.returncode,
            "stdout": stdout,
            "stderr": stderr,
            "timed_out": False,
            "seconds": round(time.perf_counter() - started, 4),
            "output_sha256": hashlib.sha256((stdout + "\n" + stderr).encode()).hexdigest(),
        }
    except subprocess.TimeoutExpired as exc:
        stdout = _short_output(str(exc.stdout or ""))
        stderr = _short_output(str(exc.stderr or ""))
        return {
            "returncode": -1,
            "stdout": stdout,
            "stderr": stderr,
            "timed_out": True,
            "seconds": round(time.perf_counter() - started, 4),
            "output_sha256": hashlib.sha256((stdout + "\n" + stderr).encode()).hexdigest(),
        }
    except OSError as exc:
        return {
            "returncode": -1,
            "stdout": "",
            "stderr": str(exc),
            "timed_out": False,
            "seconds": round(time.perf_counter() - started, 4),
            "output_sha256": "",
        }


def _write_report(path: Path, report: Mapping[str, Any]) -> None:
    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def run_benchmark(
    root: Path,
    *,
    repeats: int = 2,
    timeout: float = 30.0,
    execute: bool = False,
    report_path: Path | None = None,
) -> dict[str, Any]:
    """Run trusted local verifiers and calculate a reproducibility score."""
    if repeats < 1 or repeats > 20:
        raise CTFError("Benchmark repeats must be between 1 and 20")
    if timeout < 1:
        raise CTFError("Benchmark timeout must be at least one second")
    cases = discover_benchmark_cases(root)
    if not cases:
        raise CTFError(f"No normalized benchmark cases found under {root}")
    case_reports: list[dict[str, Any]] = []
    for case in cases:
        artifacts = case.artifacts
        record: dict[str, Any] = {
            "name": case.name,
            "category": case.category,
            "path": str(case.path),
            "verifier": str(case.verifier),
            "artifacts": artifacts,
            "evidence_ok": all(artifacts.values()),
            "runs": [],
        }
        if execute:
            record["runs"] = [_run_verifier(case, timeout) for _ in range(repeats)]
            record["passed"] = bool(record["runs"]) and all(
                run["returncode"] == 0 and not run["timed_out"] for run in record["runs"]
            )
            hashes = {run["output_sha256"] for run in record["runs"]}
            record["reproducible"] = record["passed"] and len(hashes) == 1
        else:
            record["passed"] = None
            record["reproducible"] = None
        case_reports.append(record)

    covered = {case["category"] for case in case_reports}
    passed = [case for case in case_reports if case["passed"] is True]
    reproducible = [case for case in case_reports if case["reproducible"] is True]
    evidence_ok = [case for case in case_reports if case["evidence_ok"]]
    if execute:
        coverage_score = 3.0 * len(covered & set(BENCHMARK_CATEGORIES)) / len(BENCHMARK_CATEGORIES)
        success_score = 3.0 * len(passed) / len(case_reports)
        reproducibility_score = 2.0 * len(reproducible) / len(case_reports)
        evidence_score = 2.0 * len(evidence_ok) / len(case_reports)
        practical_score = round(coverage_score + success_score + reproducibility_score + evidence_score, 2)
    else:
        practical_score = None
    report: dict[str, Any] = {
        "generated_at": _utc_now(),
        "root": str(Path(root).expanduser().resolve()),
        "execute": execute,
        "repeats": repeats,
        "timeout_seconds": timeout,
        "categories": {
            category: sum(case["category"] == category for case in case_reports)
            for category in BENCHMARK_CATEGORIES
        },
        "missing_categories": sorted(set(BENCHMARK_CATEGORIES) - covered),
        "cases": case_reports,
        "metrics": {
            "case_count": len(case_reports),
            "passed": len(passed) if execute else None,
            "success_rate": round(len(passed) / len(case_reports), 3) if execute else None,
            "reproducible": len(reproducible) if execute else None,
            "reproducibility_rate": round(len(reproducible) / len(case_reports), 3) if execute else None,
            "evidence_rate": round(len(evidence_ok) / len(case_reports), 3),
            "practical_score": practical_score,
        },
    }
    if report_path:
        _write_report(report_path, report)
        report["report_path"] = str(Path(report_path).expanduser().resolve())
    return report
