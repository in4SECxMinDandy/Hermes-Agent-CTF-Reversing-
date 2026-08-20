import json
from pathlib import Path

import pytest

from hermes_cli.ctf_approval import ApprovalError, authorize_once
from hermes_cli.ctf_casebook import (
    append_casebook_event,
    casebook_event_path,
    initialize_casebook,
    record_casebook,
)
from hermes_cli.ctf_kanban import create_ctf_worker_swarm
from hermes_cli.kanban_swarm import SwarmWorkerSpec


def _challenge(tmp_path: Path) -> Path:
    challenge = tmp_path / "demo"
    challenge.mkdir()
    (challenge / "metadata.yml").write_text(
        "name: Demo\ncategory: reverse\nconnection_info: ''\n",
        encoding="utf-8",
    )
    return challenge


def test_casebook_events_are_append_only_and_projected(tmp_path: Path) -> None:
    challenge = _challenge(tmp_path)
    initialize_casebook(challenge)
    append_casebook_event(challenge, "observation", {"source": "worker-a", "fact": "ELF"})
    record_casebook(challenge, evidence="The file is an ELF executable", confidence=80)

    events = [json.loads(line) for line in casebook_event_path(challenge).read_text(encoding="utf-8").splitlines()]
    assert [event["kind"] for event in events] == [
        "casebook_initialized",
        "observation",
        "casebook_record",
    ]
    projection = json.loads((challenge / "workspace" / "casebook.json").read_text(encoding="utf-8"))
    assert projection["evidence"][0]["text"] == "The file is an ELF executable"
    assert projection["hypotheses"] == []


def test_approval_is_one_shot_and_audited(tmp_path: Path) -> None:
    audit_path = tmp_path / "approval.events.jsonl"
    approval = authorize_once("ctf.submit", approved=True, audit_path=audit_path)
    approval.consume()
    with pytest.raises(ApprovalError, match="already consumed"):
        approval.consume()

    kinds = [
        json.loads(line)["kind"]
        for line in audit_path.read_text(encoding="utf-8").splitlines()
    ]
    assert kinds == ["approval_requested", "approval_decided", "approval_consumed"]

    with pytest.raises(ApprovalError, match="explicit one-shot approval"):
        authorize_once("ctf.live_attack", approved=False, audit_path=audit_path)


def test_ctf_workers_use_existing_kanban_dependency_graph(tmp_path: Path) -> None:
    challenge = _challenge(tmp_path)
    result = create_ctf_worker_swarm(
        challenge,
        workers=[
            SwarmWorkerSpec(profile="web-worker", title="Inspect protocol", body="Map the protocol"),
            SwarmWorkerSpec(profile="rev-worker", title="Inspect binary", body="Recover the check"),
        ],
        verifier_assignee="ctf-verifier",
        synthesizer_assignee="ctf-synthesizer",
        db_path=tmp_path / "kanban.db",
    )

    assert len(result["kanban"]["worker_ids"]) == 2
    assert result["kanban"]["verifier_id"]
    assert result["kanban"]["synthesizer_id"]
