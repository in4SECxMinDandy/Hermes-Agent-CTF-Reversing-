"""Integration tests for the CLI-edge CTF automation contract."""

from __future__ import annotations

import json
import sys
import argparse
import shutil
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import parse_qs, urlparse

import pytest
import yaml

from hermes_cli.ctf import (
    CTFError,
    CTFSettings,
    CTFdClient,
    doctor,
    live_status,
    load_ad_config,
    pull_challenges,
    run_attack_defense_once,
)
from hermes_cli.ctf_benchmark import run_benchmark
from hermes_cli.ctf_triage import run_triage


class _FakeCTFdHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    seen_auth: list[str] = []
    submissions: list[dict] = []

    def log_message(self, *_args) -> None:
        return

    @property
    def base_url(self) -> str:
        host, port = self.server.server_address[:2]
        return f"http://{host}:{port}"

    def _auth_ok(self) -> bool:
        value = self.headers.get("Authorization", "")
        self.seen_auth.append(value)
        return value == "Token secret"

    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if not self._auth_ok():
            self._send_json({"success": False, "message": "unauthorized"}, 401)
            return
        path = urlparse(self.path).path
        if path == "/api/v1/challenges":
            query = parse_qs(urlparse(self.path).query)
            page = int(query.get("page", ["1"])[0])
            rows = (
                [
                    {
                        "id": 1,
                        "name": "Demo Web",
                        "category": "Web",
                        "value": 100,
                        "solves": 2,
                        "type": "standard",
                    }
                ]
                if page == 1
                else []
            )
            self._send_json(
                {
                    "success": True,
                    "data": rows,
                    "meta": {"pagination": {"next": None}},
                }
            )
            return
        if path == "/api/v1/challenges/1":
            self._send_json(
                {
                    "success": True,
                    "data": {
                        "id": 1,
                        "name": "Demo Web",
                        "category": "Web",
                        "description": "A local integration fixture",
                        "value": 100,
                        "solves": 2,
                        "files": [
                            {
                                "name": "../payload.bin",
                                "url": f"{self.base_url}/files/payload.bin",
                            }
                        ],
                    },
                }
            )
            return
        if path == "/api/v1/challenges/1/files":
            self._send_json({"success": True, "data": []})
            return
        if path == "/api/v1/users/me":
            self._send_json({"success": True, "data": {"id": 7}})
            return
        if path == "/api/v1/users/7/solves":
            self._send_json({"success": True, "data": []})
            return
        if path == "/api/v1/scoreboard":
            self._send_json({"success": True, "data": [{"name": "team", "score": 100}]})
            return
        if path.startswith("/api/v1/scoreboard/top/"):
            self._send_json({"success": True, "data": [{"name": "team", "score": 100}]})
            return
        if path == "/files/payload.bin":
            body = b"fixture-payload\x00\x01"
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(body)
            return
        self._send_json({"success": False, "message": "not found"}, 404)

    def do_POST(self) -> None:  # noqa: N802
        if not self._auth_ok():
            self._send_json({"success": False, "message": "unauthorized"}, 401)
            return
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(length) or b"{}")
        if path != "/api/v1/challenges/attempt":
            self._send_json({"success": False, "message": "not found"}, 404)
            return
        self.submissions.append(body)
        status = "correct" if body.get("submission") == "FLAG{ok}" else "incorrect"
        self._send_json({"success": True, "data": {"status": status, "message": status}})


@pytest.fixture()
def fake_ctfd():
    _FakeCTFdHandler.seen_auth = []
    _FakeCTFdHandler.submissions = []
    server = ThreadingHTTPServer(("127.0.0.1", 0), _FakeCTFdHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address[:2]
    try:
        yield f"http://{host}:{port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_pull_submit_score_and_origin_guard(fake_ctfd: str, tmp_path: Path) -> None:
    settings = CTFSettings(
        url=fake_ctfd,
        token="secret",
        workspace=tmp_path / "challenges",
    )

    records = pull_challenges(settings)

    assert records[0]["name"] == "Demo Web"
    challenge_dir = Path(records[0]["path"])
    assert challenge_dir.name == "demo-web"
    assert (challenge_dir / "distfiles" / "payload.bin").read_bytes() == b"fixture-payload\x00\x01"
    assert (challenge_dir / "workspace").is_dir()
    assert (challenge_dir / "traces").is_dir()
    assert yaml.safe_load((challenge_dir / "metadata.yml").read_text())[
        "category"
    ] == "Web"

    with CTFdClient(fake_ctfd, "secret") as client:
        result = client.submit_flag("Demo Web", "FLAG{ok}")
        scoreboard = client.scoreboard(top=5)
        with pytest.raises(CTFError, match="different download host"):
            client.download_file("https://other.example/secret", tmp_path / "secret")

    report = doctor(settings, network=True)
    assert report["checks"]["ctfd_connectivity"] == {
        "ok": True,
        "detail": "1 visible challenge(s), scoreboard reachable (1 row(s))",
    }
    assert live_status(settings, top=1)["unsolved"] == 1

    assert result["status"] == "correct"
    assert scoreboard == [{"name": "team", "score": 100}]
    assert _FakeCTFdHandler.submissions == [{"challenge_id": 1, "submission": "FLAG{ok}"}]
    assert "Token secret" in _FakeCTFdHandler.seen_auth


def test_attack_defense_requires_scope_and_persists_score(tmp_path: Path) -> None:
    config_path = tmp_path / "ad.yml"
    config_path.write_text(
        yaml.safe_dump(
            {
                "authorized": True,
                "scope": ["127.0.0.1:31337"],
                "services": [
                    {
                        "name": "fixture",
                        "target": "127.0.0.1:31337",
                        "healthcheck": [sys.executable, "-c", "print('healthy')"],
                        "flag_command": [sys.executable, "-c", "print('FLAG{ad}')"],
                        "points": 5,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    dry_run = run_attack_defense_once(config_path, live=False)
    assert dry_run["mode"] == "dry-run"
    state_path = tmp_path / "scoreboard.json"
    state = run_attack_defense_once(config_path, state_path=state_path, live=True)

    assert state["score"] == 5
    assert state["flags"] == ["FLAG{ad}"]
    assert state["services"]["fixture"]["health_failures"] == 0
    assert json.loads(state_path.read_text(encoding="utf-8"))["score"] == 5
    assert load_ad_config(config_path)["services"][0]["name"] == "fixture"

    config_path.write_text(
        yaml.safe_dump({"authorized": False, "scope": ["127.0.0.1"], "services": []}),
        encoding="utf-8",
    )
    with pytest.raises(CTFError, match="authorized: true"):
        load_ad_config(config_path)

    config_path.write_text(
        yaml.safe_dump(
            {
                "authorized": True,
                "scope": ["127.0.0.1:31337"],
                "services": [
                    {
                        "name": "out-of-scope",
                        "target": "192.0.2.10:31337",
                        "healthcheck": [sys.executable, "-c", "print('healthy')"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(CTFError, match="outside the declared scope"):
        load_ad_config(config_path)


def test_attack_defense_runs_curated_tools_with_service_target(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config_path = tmp_path / "ad-tools.yml"
    config_path.write_text(
        yaml.safe_dump(
            {
                "authorized": True,
                "scope": ["127.0.0.1:31337"],
                "services": [
                    {
                        "name": "fixture",
                        "target": "127.0.0.1:31337",
                        "healthcheck": [sys.executable, "-c", "print('healthy')"],
                        "attack_tools": [
                            {"id": "nmap", "args": ["-T3"], "backend": "local"}
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    captured: list[dict[str, object]] = []

    def fake_run(tool_id: str, target: str, **kwargs):
        captured.append({"tool_id": tool_id, "target": target, **kwargs})
        return {"status": "ok", "tool": tool_id, "returncode": 0, "stdout": "ports"}

    monkeypatch.setattr("hermes_cli.ctf.run_attack_tool", fake_run)
    state = run_attack_defense_once(config_path, live=True)

    assert captured[0]["tool_id"] == "nmap"
    assert captured[0]["target"] == "127.0.0.1:31337"
    assert captured[0]["args"] == ["-T3"]
    assert state["services"]["fixture"]["attack_tools"]["nmap"]["ok"] == 1
    assert any(event["action"] == "attack_tool" for event in state["events"])


def test_attack_defense_rejects_high_risk_curated_tool_without_opt_in(tmp_path: Path) -> None:
    config_path = tmp_path / "ad-high-risk.yml"
    config_path.write_text(
        yaml.safe_dump(
            {
                "authorized": True,
                "scope": ["example.test"],
                "services": [
                    {
                        "name": "fixture",
                        "target": "https://example.test",
                        "healthcheck": [sys.executable, "-c", "print('healthy')"],
                        "attack_tools": [{"id": "sqlmap"}],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(CTFError, match="allow_high_risk: true"):
        load_ad_config(config_path)


def test_benchmark_fixture_covers_all_categories_reproducibly(tmp_path: Path) -> None:
    root = Path(__file__).parents[1] / "fixtures" / "ctf_benchmark"
    report_path = tmp_path / "ctf-benchmark.json"

    report = run_benchmark(root, repeats=2, execute=True, report_path=report_path)

    assert report["categories"] == {
        "web": 1,
        "crypto": 1,
        "reverse": 1,
        "forensics": 1,
        "binary": 1,
    }
    assert report["missing_categories"] == []
    assert report["metrics"]["practical_score"] == 10
    assert report["metrics"]["success_rate"] == 1
    assert report["metrics"]["reproducibility_rate"] == 1
    assert json.loads(report_path.read_text(encoding="utf-8"))["metrics"]["practical_score"] == 10


def test_triage_persists_evidence_in_workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = Path(__file__).parents[1] / "fixtures" / "ctf_benchmark" / "web-smoke"
    challenge_dir = tmp_path / "web-smoke"
    shutil.copytree(source, challenge_dir)
    captured: dict[str, object] = {}

    def fake_which(name: str) -> str | None:
        return None if name == "docker" else "sh"

    def fake_run(command: list[str], *, cwd: Path, timeout: float) -> dict[str, object]:
        captured.update({"command": command, "cwd": cwd, "timeout": timeout})
        return {
            "command": command,
            "returncode": 0,
            "stdout": "fixture triage output",
            "stderr": "",
            "timed_out": False,
            "seconds": 0.01,
        }

    monkeypatch.setattr("hermes_cli.ctf_triage.shutil.which", fake_which)
    monkeypatch.setattr("hermes_cli.ctf_triage._run", fake_run)

    report = run_triage(challenge_dir, engine="auto", network="none", timeout=12)

    report_path = Path(report["report_path"])
    assert report["category"] == "web"
    assert report["engine"] == "local"
    assert report_path.is_file()
    assert json.loads(report_path.read_text(encoding="utf-8"))["result"]["returncode"] == 0
    assert "Automated web triage" in (challenge_dir / "findings.md").read_text(encoding="utf-8")
    assert captured["cwd"] == challenge_dir


def test_ctf_parser_wires_nested_actions() -> None:
    from hermes_cli.subcommands.ctf import build_ctf_parser

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    build_ctf_parser(subparsers, cmd_ctf=lambda _args: 0)

    args = parser.parse_args(["ctf", "submit", "Demo Web", "FLAG{ok}", "--yes"])

    assert args.ctf_action == "submit"
    assert args.challenge == "Demo Web"
    assert args.flag == "FLAG{ok}"
    assert args.yes is True

    triage_args = parser.parse_args(
        ["ctf", "triage", "tests/fixtures/ctf_benchmark/web-smoke", "--network", "none"]
    )
    assert triage_args.ctf_action == "triage"
    assert triage_args.engine == "auto"
    assert triage_args.network == "none"

    benchmark_args = parser.parse_args(
        ["ctf", "benchmark", "--root", "tests/fixtures/ctf_benchmark", "--execute"]
    )
    assert benchmark_args.ctf_action == "benchmark"
    assert benchmark_args.execute is True

    attack_args = parser.parse_args(["ctf", "attack", "list", "--json"])
    assert attack_args.ctf_action == "attack"
    assert attack_args.attack_action == "list"
    assert attack_args.json is True
