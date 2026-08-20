"""CTF worker orchestration on top of the existing Kanban Swarm graph."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import yaml

from hermes_cli import kanban_db as kb
from hermes_cli.ctf import CTFError
from hermes_cli.ctf_casebook import initialize_casebook, render_casebook_brief
from hermes_cli.kanban_swarm import SwarmWorkerSpec, create_swarm


def create_ctf_worker_swarm(
    challenge_dir: Path,
    *,
    workers: Iterable[SwarmWorkerSpec],
    verifier_assignee: str,
    synthesizer_assignee: str,
    board: str | None = None,
    db_path: Path | None = None,
) -> dict[str, object]:
    """Create a durable CTF worker graph in the user's current Kanban board."""
    challenge_dir = challenge_dir.expanduser().resolve()
    if not challenge_dir.is_dir():
        raise CTFError(f"Challenge directory does not exist: {challenge_dir}")
    metadata_path = challenge_dir / "metadata.yml"
    if not metadata_path.is_file():
        raise CTFError(f"Challenge metadata does not exist: {metadata_path}")
    try:
        metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        raise CTFError(f"Could not read challenge metadata: {exc}") from exc
    if not isinstance(metadata, dict):
        raise CTFError("Challenge metadata root must be a mapping")

    casebook = initialize_casebook(challenge_dir, metadata)
    brief = render_casebook_brief(challenge_dir, max_entries=6)
    worker_specs = list(workers)
    if not worker_specs:
        raise CTFError("At least one --worker is required")
    scoped_workers = [
        SwarmWorkerSpec(
            profile=spec.profile,
            title=spec.title,
            body=(
                f"Work only on authorized CTF challenge `{challenge_dir}`.\n"
                "Treat `distfiles/` as read-only. Put generated artifacts under "
                "`workspace/`, append concise evidence to the casebook, and do "
                "not submit flags or perform live attacks.\n\n"
                f"Current case brief:\n{brief}\n\n"
                f"Worker focus:\n{spec.body}"
            ),
            skills=spec.skills,
            priority=spec.priority,
            max_runtime_seconds=spec.max_runtime_seconds,
        )
        for spec in worker_specs
    ]
    name = str(casebook.get("challenge", {}).get("name") or challenge_dir.name)
    category = str(casebook.get("challenge", {}).get("category") or "unknown")
    goal = (
        f"Solve the authorized CTF challenge {name!r} ({category}) at {challenge_dir}. "
        "Workers investigate independently, the verifier gates evidence-backed findings, "
        "and the synthesizer produces the next casebook update."
    )
    idempotency = f"ctf-worker-swarm:{challenge_dir}"
    with kb.connect_closing(db_path, board=board) as conn:
        created = create_swarm(
            conn,
            goal=goal,
            workers=scoped_workers,
            verifier_assignee=verifier_assignee,
            synthesizer_assignee=synthesizer_assignee,
            root_title=f"CTF: {name}",
            verifier_title=f"Verify CTF evidence: {name}",
            synthesizer_title=f"Synthesize CTF case: {name}",
            tenant=f"ctf:{challenge_dir.name}",
            created_by="ctf-orchestrator",
            workspace_kind="dir",
            workspace_path=str(challenge_dir),
            idempotency_key=idempotency,
        )
    return {
        "challenge": str(challenge_dir),
        "category": category,
        "board": board or "default",
        "kanban": created.as_dict(),
    }
