"""Persistent, append-only investigation state for authorized CTF workspaces.

The JSON casebook remains as a compact compatibility projection. The durable
source of truth is the JSONL event log beside it, which lets workers and new
sessions audit what was observed without mutating prior evidence.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from uuid import uuid4


CASEBOOK_VERSION = 1
CASEBOOK_RELATIVE_PATH = Path("workspace") / "casebook.json"
CASEBOOK_EVENTS_RELATIVE_PATH = Path("workspace") / "casebook.events.jsonl"
CASEBOOK_EVENT_VERSION = 1
MAX_ENTRY_CHARS = 4000
VALID_STATUSES = frozenset({"open", "blocked", "solved"})


class CasebookError(ValueError):
    """Raised when a casebook cannot be read or updated safely."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _challenge_dir(value: Path) -> Path:
    challenge_dir = value.expanduser().resolve()
    if not challenge_dir.is_dir():
        raise CasebookError(f"Challenge directory does not exist: {challenge_dir}")
    return challenge_dir


def casebook_path(challenge_dir: Path) -> Path:
    """Return the fixed, workspace-local location for a challenge casebook."""
    return _challenge_dir(challenge_dir) / CASEBOOK_RELATIVE_PATH


def casebook_event_path(challenge_dir: Path) -> Path:
    """Return the append-only event log for a challenge."""
    return _challenge_dir(challenge_dir) / CASEBOOK_EVENTS_RELATIVE_PATH


def _clean_text(value: str, *, label: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise CasebookError(f"{label} must not be empty")
    if len(text) > MAX_ENTRY_CHARS:
        raise CasebookError(f"{label} exceeds the {MAX_ENTRY_CHARS}-character limit")
    return text


def _challenge_metadata(metadata: Mapping[str, Any] | None, challenge_dir: Path) -> dict[str, str]:
    source = metadata or {}
    return {
        "name": str(source.get("name") or challenge_dir.name),
        "category": str(source.get("category") or ""),
        "connection_info": str(source.get("connection_info") or ""),
    }


def _load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CasebookError(f"Could not read casebook {path}: {exc}") from exc
    if not isinstance(value, dict) or value.get("version") != CASEBOOK_VERSION:
        raise CasebookError(f"Unsupported CTF casebook format: {path}")
    return value


def _write(path: Path, value: Mapping[str, Any]) -> None:
    """Atomically refresh the derived projection."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
    try:
        temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(path)
    except OSError as exc:
        raise CasebookError(f"Could not write casebook {path}: {exc}") from exc
    finally:
        if temporary.exists():
            temporary.unlink()


def _append_event_line(
    path: Path,
    kind: str,
    payload: Mapping[str, Any],
    *,
    recorded_at: str | None = None,
) -> dict[str, Any]:
    if not isinstance(kind, str) or not kind.strip():
        raise CasebookError("Casebook event kind must be a non-empty string")
    event_payload = dict(payload)
    try:
        json.dumps(event_payload)
    except (TypeError, ValueError) as exc:
        raise CasebookError("Casebook event payload must be JSON serializable") from exc

    event = {
        "event_version": CASEBOOK_EVENT_VERSION,
        "event_id": uuid4().hex,
        "recorded_at": recorded_at or _now(),
        "kind": kind,
        "payload": event_payload,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    line = (json.dumps(event, ensure_ascii=True, sort_keys=True) + "\n").encode("utf-8")
    try:
        descriptor = os.open(path, os.O_APPEND | os.O_CREAT | os.O_WRONLY)
        try:
            os.write(descriptor, line)
        finally:
            os.close(descriptor)
    except OSError as exc:
        raise CasebookError(f"Could not append casebook event: {exc}") from exc
    return event


def _read_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise CasebookError(
                        f"Invalid casebook event at line {line_number}: {exc}"
                    ) from exc
                if (
                    not isinstance(event, dict)
                    or event.get("event_version") != CASEBOOK_EVENT_VERSION
                    or not isinstance(event.get("kind"), str)
                    or not isinstance(event.get("payload"), dict)
                ):
                    raise CasebookError(f"Invalid casebook event at line {line_number}")
                events.append(event)
    except OSError as exc:
        raise CasebookError(f"Could not read casebook events: {exc}") from exc
    return events


def _new_casebook(
    challenge_dir: Path,
    metadata: Mapping[str, Any] | None = None,
    *,
    created_at: str | None = None,
) -> dict[str, Any]:
    timestamp = created_at or _now()
    return {
        "version": CASEBOOK_VERSION,
        "created_at": timestamp,
        "updated_at": timestamp,
        "status": "open",
        "challenge": _challenge_metadata(metadata, challenge_dir),
        "hypotheses": [],
        "evidence": [],
        "dead_ends": [],
        "next_steps": [],
        "artifacts": [],
    }


def _project_events(
    challenge_dir: Path,
    events: list[dict[str, Any]],
    fallback: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Fold known events into the legacy casebook JSON shape."""
    initialized = next(
        (event for event in events if event["kind"] == "casebook_initialized"),
        None,
    )
    if initialized:
        payload = initialized["payload"]
        metadata = payload.get("challenge")
        casebook = _new_casebook(
            challenge_dir,
            metadata if isinstance(metadata, Mapping) else None,
            created_at=str(payload.get("created_at") or initialized["recorded_at"]),
        )
    elif fallback:
        casebook = dict(fallback)
        for field in ("hypotheses", "evidence", "dead_ends", "next_steps", "artifacts"):
            casebook[field] = list(casebook.get(field) or [])
    else:
        casebook = _new_casebook(challenge_dir)

    for event in events:
        payload = event["payload"]
        kind = event["kind"]
        if kind == "casebook_record":
            field = payload.get("field")
            if field not in {"hypotheses", "evidence", "dead_ends", "next_steps", "artifacts"}:
                continue
            entry = {"text": str(payload.get("text", "")), "recorded_at": event["recorded_at"]}
            metadata = payload.get("metadata")
            if isinstance(metadata, Mapping):
                entry.update(metadata)
            casebook[field].append(entry)
        elif kind == "casebook_status":
            status = payload.get("status")
            if isinstance(status, str) and status in VALID_STATUSES:
                casebook["status"] = status

    if events:
        casebook["updated_at"] = events[-1]["recorded_at"]
    casebook["version"] = CASEBOOK_VERSION
    return casebook


def _seed_event_log(challenge_dir: Path, current: dict[str, Any]) -> None:
    """Migrate a legacy projection into events exactly once."""
    event_path = casebook_event_path(challenge_dir)
    if _read_events(event_path):
        return
    created_at = str(current.get("created_at") or _now())
    _append_event_line(
        event_path,
        "casebook_initialized",
        {"challenge": current.get("challenge") or {}, "created_at": created_at},
        recorded_at=created_at,
    )
    for field in ("hypotheses", "evidence", "dead_ends", "next_steps", "artifacts"):
        for entry in current.get(field) or []:
            if isinstance(entry, Mapping):
                text = entry.get("text", "")
                metadata = {key: value for key, value in entry.items() if key not in {"text", "recorded_at"}}
                recorded_at = entry.get("recorded_at")
            else:
                text = entry
                metadata = {}
                recorded_at = None
            _append_event_line(
                event_path,
                "casebook_record",
                {"field": field, "text": str(text), "metadata": metadata},
                recorded_at=str(recorded_at) if recorded_at else None,
            )
    if current.get("status") not in {None, "open"}:
        _append_event_line(event_path, "casebook_status", {"status": current["status"]})


def initialize_casebook(
    challenge_dir: Path,
    metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a casebook if absent and return its current projection."""
    challenge_dir = _challenge_dir(challenge_dir)
    path = casebook_path(challenge_dir)
    if path.exists():
        current = _load(path)
        _seed_event_log(challenge_dir, current)
        projected = _project_events(challenge_dir, _read_events(casebook_event_path(challenge_dir)), current)
        _write(path, projected)
        return projected

    casebook = _new_casebook(challenge_dir, metadata)
    _append_event_line(
        casebook_event_path(challenge_dir),
        "casebook_initialized",
        {"challenge": casebook["challenge"], "created_at": casebook["created_at"]},
        recorded_at=casebook["created_at"],
    )
    _write(path, casebook)
    return casebook


def append_casebook_event(
    challenge_dir: Path,
    kind: str,
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    """Append an audit/evidence event and refresh the JSON projection."""
    challenge_dir = _challenge_dir(challenge_dir)
    initialize_casebook(challenge_dir)
    event = _append_event_line(casebook_event_path(challenge_dir), kind, payload)
    projected = _project_events(challenge_dir, _read_events(casebook_event_path(challenge_dir)))
    _write(casebook_path(challenge_dir), projected)
    return event


def _workspace_artifact(challenge_dir: Path, artifact: str | Path) -> str:
    candidate = Path(artifact).expanduser()
    resolved = (challenge_dir / candidate).resolve() if not candidate.is_absolute() else candidate.resolve()
    try:
        return resolved.relative_to(challenge_dir).as_posix()
    except ValueError as exc:
        raise CasebookError("Artifacts must remain inside the challenge workspace") from exc


def record_casebook(
    challenge_dir: Path,
    *,
    hypothesis: str | None = None,
    evidence: str | None = None,
    dead_end: str | None = None,
    next_step: str | None = None,
    artifact: str | Path | None = None,
    artifact_summary: str | None = None,
    confidence: int | None = None,
    status: str | None = None,
) -> dict[str, Any]:
    """Append one or more concise investigation facts to a casebook."""
    challenge_dir = _challenge_dir(challenge_dir)
    casebook = initialize_casebook(challenge_dir)
    if confidence is not None and not 0 <= confidence <= 100:
        raise CasebookError("confidence must be between 0 and 100")
    if status is not None and status not in VALID_STATUSES:
        raise CasebookError(f"status must be one of: {', '.join(sorted(VALID_STATUSES))}")

    records: list[tuple[str, str, dict[str, Any]]] = []
    if hypothesis is not None:
        records.append(("hypotheses", _clean_text(hypothesis, label="hypothesis"), {"confidence": confidence}))
    if evidence is not None:
        records.append(("evidence", _clean_text(evidence, label="evidence"), {}))
    if dead_end is not None:
        records.append(("dead_ends", _clean_text(dead_end, label="dead end"), {}))
    if next_step is not None:
        records.append(("next_steps", _clean_text(next_step, label="next step"), {}))
    if artifact is not None:
        relative_path = _workspace_artifact(challenge_dir, artifact)
        summary = _clean_text(artifact_summary or relative_path, label="artifact summary")
        records.append(("artifacts", relative_path, {"summary": summary}))
    if not records and status is None:
        raise CasebookError("Record at least one hypothesis, evidence, dead end, next step, artifact, or status")

    event_path = casebook_event_path(challenge_dir)
    for field, text, metadata in records:
        _append_event_line(event_path, "casebook_record", {"field": field, "text": text, "metadata": metadata})
    if status is not None:
        _append_event_line(event_path, "casebook_status", {"status": status})
    projected = _project_events(challenge_dir, _read_events(event_path), casebook)
    _write(casebook_path(challenge_dir), projected)
    return projected


def casebook_status(challenge_dir: Path) -> dict[str, Any]:
    """Return compact machine-readable status without expanding entry content."""
    challenge_dir = _challenge_dir(challenge_dir)
    casebook = initialize_casebook(challenge_dir)
    path = casebook_path(challenge_dir)
    return {
        "path": str(path),
        "event_log": str(casebook_event_path(challenge_dir)),
        "status": casebook["status"],
        "challenge": casebook["challenge"],
        "updated_at": casebook["updated_at"],
        "counts": {
            name: len(casebook.get(name, []))
            for name in ("hypotheses", "evidence", "dead_ends", "next_steps", "artifacts")
        },
    }


def render_casebook_brief(challenge_dir: Path, *, max_entries: int = 6) -> str:
    """Render a bounded brief suitable for a fresh agent or focused worker."""
    if not 1 <= max_entries <= 20:
        raise CasebookError("max_entries must be between 1 and 20")
    challenge_dir = _challenge_dir(challenge_dir)
    casebook = initialize_casebook(challenge_dir)
    challenge = casebook["challenge"]
    lines = [
        "# CTF Case Brief",
        f"- Workspace: `{challenge_dir}`",
        f"- Name: {challenge.get('name') or challenge_dir.name}",
        f"- Category: {challenge.get('category') or 'unknown'}",
        f"- Status: {casebook.get('status', 'open')}",
    ]
    if challenge.get("connection_info"):
        lines.append(f"- Connection: {challenge['connection_info']}")
    sections = (
        ("Active hypotheses", "hypotheses"),
        ("Evidence", "evidence"),
        ("Do not repeat", "dead_ends"),
        ("Next steps", "next_steps"),
        ("Artifacts", "artifacts"),
    )
    for heading, field in sections:
        entries = casebook.get(field, [])[-max_entries:]
        if not entries:
            continue
        lines.extend(("", f"## {heading}"))
        for entry in entries:
            text = str(entry.get("text") or "")
            if field == "artifacts":
                text = f"`{text}` - {entry.get('summary', '')}"
            if field == "hypotheses" and entry.get("confidence") is not None:
                text = f"{text} (confidence: {entry['confidence']}%)"
            lines.append(f"- {text}")
    return "\n".join(lines) + "\n"
