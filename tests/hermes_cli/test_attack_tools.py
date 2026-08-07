"""Tests for the curated Hermes Attack & Defense tool catalog."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

import hermes_cli.attack_tools as attack_tools
from hermes_cli.attack_tools import (
    AttackToolError,
    build_attack_command,
    list_attack_tools,
    normalize_attack_requests,
    run_attack_tool,
)


def test_catalog_is_curated_and_excludes_weaponized_categories() -> None:
    entries = list_attack_tools()
    ids = {entry["id"] for entry in entries}

    assert {"nmap", "httpx", "nuclei", "ffuf", "testssl", "sqlmap"} <= ids
    assert not ids.intersection({"ddos", "phishing", "evilginx", "sliver", "wifite"})
    assert next(entry for entry in entries if entry["id"] == "sqlmap")["risk"] == "high"


def test_nmap_receives_the_scoped_host_and_exact_port() -> None:
    assert build_attack_command("nmap", "127.0.0.1:31337", args=["-T3"]) == [
        "nmap",
        "-sT",
        "-Pn",
        "-sV",
        "-p",
        "31337",
        "127.0.0.1",
        "-T3",
    ]


def test_web_tools_normalize_host_targets_to_urls() -> None:
    assert build_attack_command("nuclei", "127.0.0.1:31337")[-1] == "http://127.0.0.1:31337"
    assert build_attack_command("ffuf", "https://example.test", args=["-w", "words.txt"]) == [
        "ffuf",
        "-u",
        "https://example.test/FUZZ",
        "-w",
        "words.txt",
    ]


def test_target_selection_cannot_be_overridden_in_extra_args() -> None:
    with pytest.raises(AttackToolError, match="target-selection flags"):
        build_attack_command("sqlmap", "https://example.test", args=["--url", "https://other.test"])


def test_high_risk_tools_require_explicit_opt_in() -> None:
    with pytest.raises(AttackToolError, match="allow_high_risk"):
        run_attack_tool("sqlmap", "https://example.test", backend="local")


def test_run_uses_argv_without_shell(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    def fake_run(command, **kwargs):
        captured["command"] = command
        captured["kwargs"] = kwargs
        return SimpleNamespace(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr(attack_tools.subprocess, "run", fake_run)
    result = run_attack_tool(
        "httpx",
        "https://example.test",
        args=["-follow-redirects"],
        backend="local",
    )

    assert result["status"] == "ok"
    assert captured["command"] == [
        "httpx",
        "-silent",
        "-status-code",
        "-title",
        "-tech-detect",
        "https://example.test",
        "-follow-redirects",
    ]
    assert "shell" not in captured["kwargs"]
    assert captured["kwargs"]["stdin"] is attack_tools.subprocess.DEVNULL


def test_request_normalization_rejects_command_strings() -> None:
    with pytest.raises(AttackToolError, match="list of strings"):
        normalize_attack_requests([{"id": "nmap", "args": "-T3"}])
