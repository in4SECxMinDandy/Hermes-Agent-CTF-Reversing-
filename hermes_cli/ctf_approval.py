"""Fail-closed, one-shot approvals for CTF side effects."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from uuid import uuid4

from hermes_cli.ctf_casebook import append_casebook_event


class ApprovalError(RuntimeError):
    """Raised when a requested CTF side effect is not explicitly approved."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _append_audit(path: Path, kind: str, payload: Mapping[str, Any]) -> None:
    event = {
        "event_version": 1,
        "event_id": uuid4().hex,
        "recorded_at": _now(),
        "kind": kind,
        "payload": dict(payload),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    line = (json.dumps(event, ensure_ascii=True, sort_keys=True) + "\n").encode("utf-8")
    descriptor = os.open(path, os.O_APPEND | os.O_CREAT | os.O_WRONLY)
    try:
        os.write(descriptor, line)
    finally:
        os.close(descriptor)


def _audit(
    kind: str,
    payload: Mapping[str, Any],
    *,
    challenge_dir: Path | None,
    audit_path: Path | None,
) -> None:
    if challenge_dir is not None:
        append_casebook_event(challenge_dir, kind, payload)
    elif audit_path is not None:
        _append_audit(audit_path, kind, payload)


@dataclass
class OneShotApproval:
    request_id: str
    action: str
    _consumed: bool = False
    _challenge_dir: Path | None = None
    _audit_path: Path | None = None

    def consume(self) -> None:
        """Consume the approval immediately before the authorized side effect."""
        if self._consumed:
            raise ApprovalError(f"Approval {self.request_id} was already consumed")
        self._consumed = True
        _audit(
            "approval_consumed",
            {"request_id": self.request_id, "action": self.action},
            challenge_dir=self._challenge_dir,
            audit_path=self._audit_path,
        )


def authorize_once(
    action: str,
    *,
    approved: bool,
    challenge_dir: Path | None = None,
    audit_path: Path | None = None,
    details: Mapping[str, Any] | None = None,
    source: str = "cli",
) -> OneShotApproval:
    """Issue one non-reusable approval or reject the operation.

    The function deliberately accepts only a boolean supplied by the command
    boundary. There is no persistent approval token or ambient allow-list.
    """
    if not action.strip():
        raise ApprovalError("Approval action must not be empty")
    request_id = uuid4().hex
    payload = {
        "request_id": request_id,
        "action": action,
        "source": source,
        "details": dict(details or {}),
    }
    _audit("approval_requested", payload, challenge_dir=challenge_dir, audit_path=audit_path)
    if not approved:
        _audit(
            "approval_decided",
            {**payload, "decision": "rejected"},
            challenge_dir=challenge_dir,
            audit_path=audit_path,
        )
        raise ApprovalError(
            f"{action} requires explicit one-shot approval; pass --yes for this invocation"
        )
    _audit(
        "approval_decided",
        {**payload, "decision": "allowed-once"},
        challenge_dir=challenge_dir,
        audit_path=audit_path,
    )
    return OneShotApproval(
        request_id=request_id,
        action=action,
        _challenge_dir=challenge_dir,
        _audit_path=audit_path,
    )
