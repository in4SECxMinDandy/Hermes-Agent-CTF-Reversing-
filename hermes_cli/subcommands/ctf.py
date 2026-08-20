"""Argument parser for the ``hermes ctf`` CLI edge."""

from __future__ import annotations

from typing import Callable


def build_ctf_parser(subparsers, *, cmd_ctf: Callable) -> None:
    """Attach CTFd, solver-runner, and Attack & Defense actions."""
    ctf_parser = subparsers.add_parser(
        "ctf",
        help="Automate authorized CTF workflows",
        description=(
            "Discover, pull, solve, submit, and score authorized CTF challenges. "
            "Attack & Defense commands require an explicit authorized config."
        ),
    )
    actions = ctf_parser.add_subparsers(dest="ctf_action")

    doctor = actions.add_parser("doctor", help="Check CTF automation prerequisites")
    doctor.add_argument(
        "--network",
        action="store_true",
        help="Probe the configured CTFd API in addition to local checks",
    )
    doctor.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    assess = actions.add_parser("assess", help="Score the CTF automation capability out of 10")
    assess.add_argument(
        "--network",
        action="store_true",
        help="Include a live CTFd connectivity check",
    )
    assess.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    init = actions.add_parser("init", help="Create a local challenge workspace contract")
    init.add_argument(
        "source",
        nargs="?",
        default=".",
        help="Challenge directory or file (default: current directory)",
    )
    init.add_argument(
        "--root",
        default="challenges",
        help="Destination root for a new workspace",
    )

    triage = actions.add_parser(
        "triage",
        help="Run fixed category probes in an isolated CTF sandbox",
    )
    triage.add_argument("challenge", help="Normalized challenge workspace directory")
    triage.add_argument(
        "--engine",
        choices=("auto", "docker", "local"),
        default="auto",
        help="Triage execution engine (default: auto)",
    )
    triage.add_argument(
        "--network",
        choices=("none", "host"),
        default="none",
        help="Sandbox network policy (default: none)",
    )
    triage.add_argument(
        "--yes",
        action="store_true",
        help="Approve this invocation when using host networking",
    )
    triage.add_argument("--image", help="Override the CTF sandbox image")
    triage.add_argument("--timeout", type=float, default=90.0, help="Probe timeout in seconds")
    triage.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    benchmark = actions.add_parser(
        "benchmark",
        help="Measure category coverage, verifier success, and reproducibility",
    )
    benchmark.add_argument("--root", help="Benchmark workspace root (default: ctf.workspace)")
    benchmark.add_argument("--repeats", type=int, default=2, help="Verifier runs per case (1-20)")
    benchmark.add_argument("--timeout", type=float, default=30.0, help="Verifier timeout in seconds")
    benchmark.add_argument(
        "--execute",
        action="store_true",
        help="Run trusted local verifier scripts; default only discovers cases",
    )
    benchmark.add_argument("--report", help="Optional JSON report path")
    benchmark.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    case = actions.add_parser("case", help="Persist compact evidence and a resumable CTF case brief")
    case_actions = case.add_subparsers(dest="case_action")
    case_init = case_actions.add_parser("init", help="Create the workspace-local casebook")
    case_init.add_argument("challenge", help="Normalized challenge workspace directory")
    case_init.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    case_status = case_actions.add_parser("status", help="Show casebook counts and status")
    case_status.add_argument("challenge", help="Normalized challenge workspace directory")
    case_status.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    case_brief = case_actions.add_parser("brief", help="Render a bounded brief for an agent or worker")
    case_brief.add_argument("challenge", help="Normalized challenge workspace directory")
    case_brief.add_argument("--max-entries", type=int, default=6, help="Entries per section (1-20)")
    case_brief.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    case_record = case_actions.add_parser("record", help="Append evidence, a hypothesis, or a next step")
    case_record.add_argument("challenge", help="Normalized challenge workspace directory")
    record_value = case_record.add_mutually_exclusive_group(required=False)
    record_value.add_argument("--hypothesis", help="Evidence-backed line of inquiry")
    record_value.add_argument("--evidence", help="Observed fact or verified result")
    record_value.add_argument("--dead-end", help="Approach that should not be repeated")
    record_value.add_argument("--next-step", help="Concrete next probe")
    record_value.add_argument("--artifact", help="Path inside the challenge workspace")
    case_record.add_argument("--artifact-summary", help="Why the artifact matters")
    case_record.add_argument("--confidence", type=int, help="Hypothesis confidence from 0 to 100")
    case_record.add_argument("--status", choices=("open", "blocked", "solved"), help="Challenge status")
    case_record.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    swarm = actions.add_parser(
        "swarm",
        help="Create CTF workers in the existing Kanban dependency graph",
        description=(
            "Create parallel specialist workers plus a verifier and synthesizer "
            "on the existing Kanban board."
        ),
    )
    swarm.add_argument("challenge", help="Normalized challenge workspace directory")
    swarm.add_argument(
        "--worker",
        action="append",
        required=True,
        metavar="PROFILE:TITLE[:SKILL,SKILL]",
        help="Parallel worker specification; repeat for each specialist",
    )
    swarm.add_argument("--verifier", default="ctf-verifier", help="Kanban assignee for evidence gating")
    swarm.add_argument("--synthesizer", default="ctf-synthesizer", help="Kanban assignee for final synthesis")
    swarm.add_argument("--board", help="Kanban board slug (default: current board)")
    swarm.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    pull = actions.add_parser("pull", help="Pull visible challenges and files from CTFd")
    pull.add_argument("--root", help="Workspace root (default: ctf.workspace)")
    pull.add_argument("--category", help="Only pull one challenge category")
    pull.add_argument(
        "--unsolved-only",
        action="store_true",
        help="Skip challenges already solved by the current user/team",
    )
    pull.add_argument("--limit", type=int, help="Maximum number of challenges to pull")
    pull.add_argument(
        "--force",
        action="store_true",
        help="Redownload files that already exist in distfiles",
    )
    pull.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    score = actions.add_parser("score", help="Show the live CTFd scoreboard")
    score.add_argument("--top", type=int, help="Limit the result to the top N teams")
    score.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    status = actions.add_parser("status", help="Show live challenges, solves, and scoreboard")
    status.add_argument("--top", type=int, help="Limit the scoreboard portion to the top N teams")
    status.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    submit = actions.add_parser("submit", help="Submit one flag to CTFd")
    submit.add_argument("challenge", help="Exact CTFd challenge name")
    submit.add_argument("flag", help="Flag value to submit")
    submit.add_argument(
        "--yes",
        action="store_true",
        help="Confirm this external side effect (not needed with ctf.auto_submit)",
    )
    submit.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    run = actions.add_parser("run", help="Run the optional ctf-agent solver orchestrator")
    run.add_argument("--challenge", help="Solve one normalized challenge directory")
    run.add_argument(
        "--challenges-dir",
        help="Directory containing normalized challenge workspaces",
    )
    run.add_argument(
        "--submit",
        action="store_true",
        help="Allow the solver runner to submit flags (also enabled by ctf.auto_submit)",
    )
    run.add_argument(
        "--coordinator",
        choices=("claude", "codex"),
        default="claude",
        help="Solver coordinator backend",
    )
    run.add_argument(
        "--model",
        action="append",
        default=[],
        help="Model override; repeat for fallback models",
    )

    attack = actions.add_parser(
        "attack",
        help="List the curated Attack & Defense tool catalog",
    )
    attack.add_argument(
        "attack_action",
        nargs="?",
        choices=("list",),
        default="list",
        help="Catalog action (default: list)",
    )
    attack.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    ad = actions.add_parser(
        "ad",
        help="Run an authorized Attack & Defense configuration",
        description=(
            "Validate or run a scoped Attack & Defense service loop. "
            "Execution is dry-run unless --live is supplied."
        ),
    )
    ad_actions = ad.add_subparsers(dest="ad_action")

    ad_doctor = ad_actions.add_parser("doctor", help="Validate an A&D configuration")
    ad_doctor.add_argument("config", help="Path to the authorized A&D YAML")
    ad_doctor.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    ad_status = ad_actions.add_parser("status", help="Show the persisted A&D scoreboard")
    ad_status.add_argument("config", help="Path to the authorized A&D YAML")
    ad_status.add_argument("--state", help="Override the scoreboard JSON path")
    ad_status.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    ad_run = ad_actions.add_parser("run", help="Run one or more A&D cycles")
    ad_run.add_argument("config", help="Path to the authorized A&D YAML")
    ad_run.add_argument("--state", help="Override the scoreboard JSON path")
    ad_run.add_argument(
        "--live",
        action="store_true",
        help="Execute configured healthcheck, patch, attack, and flag commands",
    )
    ad_run.add_argument("--cycles", type=int, default=1, help="Number of live cycles")
    ad_run.add_argument(
        "--watch",
        action="store_true",
        help="Continue live cycles until interrupted",
    )
    ad_run.add_argument(
        "--interval",
        type=float,
        default=30.0,
        help="Seconds between live cycles in watch mode",
    )
    ad_run.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    ctf_parser.set_defaults(func=cmd_ctf)
