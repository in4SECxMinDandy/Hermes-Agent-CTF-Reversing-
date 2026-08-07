"""Curated, argv-based attack tools for authorized CTF workflows.

This is intentionally a small Hermes-native subset of the external
``hackingtool`` catalog.  It provides useful discovery and validation tools
without importing the upstream install scripts, shell runner, or high-risk
tool categories into Hermes.
"""

from __future__ import annotations

import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping
from urllib.parse import urlsplit


MAX_OUTPUT_CHARS = 12_000
MAX_TIMEOUT_SECONDS = 3_600.0
_BACKENDS = {"auto", "local", "wsl", "docker"}
_NETWORKS = {"none", "bridge", "host"}
_TARGET_OPTIONS = {
    "-d",
    "--domain",
    "-p",
    "--ports",
    "-target",
    "-targets",
    "-u",
    "--url",
}


class AttackToolError(ValueError):
    """Raised when a curated attack-tool request is invalid."""


@dataclass(frozen=True)
class AttackTool:
    """Metadata needed to render and execute one curated tool."""

    id: str
    category: str
    executable: str
    description: str
    target_mode: str = "url"
    target_flag: str | None = None
    target_suffix: str = ""
    default_args: tuple[str, ...] = ()
    risk: str = "active"
    docker_image: str | None = None
    docker_entrypoint: bool = True


# These are the practical recon/web tools from hackingtool's much larger
# inventory.  Deliberately omitted: phishing, DDoS, wireless attacks, RAT/C2,
# payload generators, credential capture, and post-exploitation automation.
ATTACK_TOOL_CATALOG: dict[str, AttackTool] = {
    "nmap": AttackTool(
        id="nmap",
        category="network-recon",
        executable="nmap",
        description="Service and version discovery for the declared target.",
        target_mode="host",
        default_args=("-sT", "-Pn", "-sV"),
        docker_image="instrumentisto/nmap",
    ),
    "subfinder": AttackTool(
        id="subfinder",
        category="subdomain-recon",
        executable="subfinder",
        description="Passive subdomain enumeration.",
        target_mode="host",
        target_flag="-d",
        default_args=("-silent",),
        docker_image="projectdiscovery/subfinder",
    ),
    "amass": AttackTool(
        id="amass",
        category="subdomain-recon",
        executable="amass",
        description="Passive attack-surface and subdomain enumeration.",
        target_mode="host",
        target_flag="-d",
        default_args=("enum", "-passive"),
        docker_image="caffix/amass",
    ),
    "httpx": AttackTool(
        id="httpx",
        category="http-recon",
        executable="httpx",
        description="HTTP probing with status, title, and technology hints.",
        target_mode="url",
        default_args=("-silent", "-status-code", "-title", "-tech-detect"),
        docker_image="projectdiscovery/httpx",
    ),
    "katana": AttackTool(
        id="katana",
        category="web-recon",
        executable="katana",
        description="Crawl the declared web target for routes and links.",
        target_mode="url",
        default_args=("-silent",),
        docker_image="projectdiscovery/katana",
    ),
    "nuclei": AttackTool(
        id="nuclei",
        category="vulnerability-discovery",
        executable="nuclei",
        description="Template-based vulnerability discovery at medium severity and above.",
        target_mode="url",
        default_args=("-silent", "-severity", "medium,high,critical"),
        docker_image="projectdiscovery/nuclei",
    ),
    "ffuf": AttackTool(
        id="ffuf",
        category="web-discovery",
        executable="ffuf",
        description="Web path and parameter discovery; provide a wordlist in args.",
        target_mode="url",
        target_flag="-u",
        target_suffix="/FUZZ",
        risk="active",
        docker_image="secsi/ffuf",
    ),
    "gobuster": AttackTool(
        id="gobuster",
        category="web-discovery",
        executable="gobuster",
        description="Directory, DNS, or virtual-host discovery; provide mode and wordlist in args.",
        target_mode="url",
        target_flag="-u",
        default_args=("dir",),
        docker_image="devopsworks/gobuster",
    ),
    "testssl": AttackTool(
        id="testssl",
        category="tls-audit",
        executable="testssl.sh",
        description="TLS protocol, cipher, and certificate checks.",
        target_mode="host_port",
        docker_image="drwetter/testssl.sh",
    ),
    "wafw00f": AttackTool(
        id="wafw00f",
        category="web-fingerprinting",
        executable="wafw00f",
        description="Web application firewall fingerprinting.",
        target_mode="url",
        docker_image="0xsauby/wafw00f",
    ),
    "sqlmap": AttackTool(
        id="sqlmap",
        category="injection-testing",
        executable="sqlmap",
        description="SQL injection testing; requires explicit high-risk opt-in.",
        target_mode="url",
        target_flag="-u",
        default_args=("--batch",),
        risk="high",
        docker_image="paoloo/sqlmap",
    ),
}


def get_attack_tool(tool_id: str) -> AttackTool:
    """Return a curated tool or fail closed with an actionable error."""

    key = str(tool_id or "").strip().lower()
    try:
        return ATTACK_TOOL_CATALOG[key]
    except KeyError as exc:
        available = ", ".join(sorted(ATTACK_TOOL_CATALOG))
        raise AttackToolError(f"Unknown attack tool {tool_id!r}; choose one of: {available}") from exc


def list_attack_tools() -> list[dict[str, Any]]:
    """Return stable, JSON-friendly catalog entries for CLI/skill discovery."""

    return [
        {
            "id": tool.id,
            "category": tool.category,
            "description": tool.description,
            "risk": tool.risk,
            "backends": ["local", "wsl", "docker"],
        }
        for tool in sorted(ATTACK_TOOL_CATALOG.values(), key=lambda item: item.id)
    ]


def _target_parts(target: str) -> tuple[str, str | None, str, str]:
    raw = str(target or "").strip()
    if not raw:
        raise AttackToolError("Attack tool target must not be empty")
    parsed = urlsplit(raw if "://" in raw else f"//{raw}")
    host = parsed.hostname
    if not host:
        raise AttackToolError(f"Attack tool target has no host: {target!r}")
    try:
        port = str(parsed.port) if parsed.port is not None else None
    except ValueError as exc:
        raise AttackToolError(f"Attack tool target has an invalid port: {target!r}") from exc
    host_port = host if port is None else f"[{host}]:{port}" if ":" in host else f"{host}:{port}"
    url = raw if "://" in raw else f"http://{raw}"
    return host, port, host_port, url


def _render_target(tool: AttackTool, target: str) -> tuple[str, str | None]:
    host, port, host_port, url = _target_parts(target)
    if tool.target_mode == "host":
        return host, port
    if tool.target_mode == "host_port":
        return host_port, port
    if tool.target_mode == "url":
        return url.rstrip("/") + tool.target_suffix, port
    raise AttackToolError(f"Unsupported target mode for {tool.id}: {tool.target_mode!r}")


def _normalize_args(args: Iterable[str] | None) -> list[str]:
    if args is None:
        return []
    if isinstance(args, (str, bytes)):
        raise AttackToolError("Attack tool args must be a list of strings, not a command string")
    normalized = list(args)
    if not all(isinstance(item, str) for item in normalized):
        raise AttackToolError("Attack tool args must contain only strings")
    if len(normalized) > 64:
        raise AttackToolError("Attack tool args may contain at most 64 entries")
    if any("\x00" in item for item in normalized):
        raise AttackToolError("Attack tool args must not contain NUL bytes")
    return normalized


def build_attack_command(
    tool_id: str,
    target: str,
    *,
    args: Iterable[str] | None = None,
) -> list[str]:
    """Build a shell-free command whose target comes from the service config."""

    tool = get_attack_tool(tool_id)
    extra_args = _normalize_args(args)
    if any(item in _TARGET_OPTIONS for item in extra_args):
        raise AttackToolError(
            f"{tool.id} target-selection flags are managed by Hermes; put the target in the service target"
        )
    rendered_target, port = _render_target(tool, target)
    command = [tool.executable, *tool.default_args]
    if tool.id == "nmap" and port is not None:
        command.extend(("-p", port))
    if tool.target_flag:
        command.extend((tool.target_flag, rendered_target))
    else:
        command.append(rendered_target)
    command.extend(extra_args)
    return command


def normalize_attack_requests(value: Any) -> list[dict[str, Any]]:
    """Validate service-level ``attack_tools`` entries for A&D configs."""

    if value is None:
        return []
    if not isinstance(value, list):
        raise AttackToolError("attack_tools must be a list")
    requests: list[dict[str, Any]] = []
    for item in value:
        if isinstance(item, str):
            raw: Mapping[str, Any] = {"id": item}
        elif isinstance(item, Mapping):
            raw = item
        else:
            raise AttackToolError("Each attack_tools entry must be a tool id or mapping")
        tool = get_attack_tool(str(raw.get("id") or raw.get("tool") or ""))
        args = _normalize_args(raw.get("args", []))
        backend = str(raw.get("backend") or "auto").strip().lower()
        if backend not in _BACKENDS:
            raise AttackToolError(f"Unsupported backend {backend!r} for attack tool {tool.id}")
        network = str(raw.get("network") or "bridge").strip().lower()
        if network not in _NETWORKS:
            raise AttackToolError(f"Unsupported Docker network {network!r} for attack tool {tool.id}")
        try:
            timeout = float(raw.get("timeout", 180))
        except (TypeError, ValueError) as exc:
            raise AttackToolError(f"Invalid timeout for attack tool {tool.id}") from exc
        if timeout < 1 or timeout > MAX_TIMEOUT_SECONDS:
            raise AttackToolError(
                f"Timeout for attack tool {tool.id} must be between 1 and {int(MAX_TIMEOUT_SECONDS)} seconds"
            )
        request = {
            "id": tool.id,
            "args": args,
            "backend": backend,
            "network": network,
            "timeout": timeout,
        }
        for key in ("distro", "docker_image"):
            if raw.get(key) is not None:
                text = str(raw[key]).strip()
                if not text or "\x00" in text:
                    raise AttackToolError(f"Invalid {key} for attack tool {tool.id}")
                request[key] = text
        requests.append(request)
    return requests


def _short_output(value: str, limit: int = MAX_OUTPUT_CHARS) -> str:
    if len(value) <= limit:
        return value
    return value[:limit] + f"\n...[truncated {len(value) - limit} chars]"


def _select_backend(tool: AttackTool, requested: str) -> str:
    if requested != "auto":
        return requested
    if shutil.which(tool.executable):
        return "local"
    if shutil.which("wsl"):
        return "wsl"
    if shutil.which("docker"):
        return "docker"
    return "unavailable"


def _backend_command(
    tool: AttackTool,
    command: list[str],
    *,
    backend: str,
    distro: str | None,
    network: str,
    docker_image: str | None,
    cwd: Path | None,
) -> list[str]:
    if backend == "local":
        return command
    if backend == "wsl":
        result = ["wsl"]
        if distro:
            result.extend(("-d", distro))
        return [*result, "--", *command]
    if backend == "docker":
        image = docker_image or tool.docker_image
        if not image:
            raise AttackToolError(f"No Docker image is configured for attack tool {tool.id}")
        result = ["docker", "run", "--rm", "--network", network]
        if cwd:
            result.extend(("-v", f"{cwd.resolve()}:/work:rw", "-w", "/work"))
        result.append(image)
        if tool.docker_entrypoint:
            result.extend(command[1:])
        else:
            result.extend(command)
        return result
    raise AttackToolError(f"Unsupported attack tool backend: {backend}")


def run_attack_tool(
    tool_id: str,
    target: str,
    *,
    args: Iterable[str] | None = None,
    backend: str = "auto",
    distro: str | None = None,
    network: str = "bridge",
    docker_image: str | None = None,
    cwd: Path | None = None,
    timeout: float = 180,
    allow_high_risk: bool = False,
) -> dict[str, Any]:
    """Run one curated tool and return bounded structured output."""

    tool = get_attack_tool(tool_id)
    if tool.risk == "high" and not allow_high_risk:
        raise AttackToolError(f"Attack tool {tool.id} requires allow_high_risk: true")
    if backend not in _BACKENDS:
        raise AttackToolError(f"Unsupported backend {backend!r} for attack tool {tool.id}")
    if network not in _NETWORKS:
        raise AttackToolError(f"Unsupported Docker network {network!r} for attack tool {tool.id}")
    try:
        timeout_value = float(timeout)
    except (TypeError, ValueError) as exc:
        raise AttackToolError(f"Invalid timeout for attack tool {tool.id}") from exc
    if timeout_value < 1 or timeout_value > MAX_TIMEOUT_SECONDS:
        raise AttackToolError(
            f"Timeout for attack tool {tool.id} must be between 1 and {int(MAX_TIMEOUT_SECONDS)} seconds"
        )
    command = build_attack_command(tool.id, target, args=args)
    selected_backend = _select_backend(tool, backend)
    if selected_backend == "unavailable":
        return {
            "status": "fallback",
            "reason": "no_backend",
            "tool": tool.id,
            "command": command,
            "message": "Tool is not installed and neither WSL nor Docker is available",
        }
    if selected_backend == "wsl" and not shutil.which("wsl"):
        return {"status": "error", "tool": tool.id, "message": "wsl executable not found"}
    if selected_backend == "docker" and not shutil.which("docker"):
        return {"status": "error", "tool": tool.id, "message": "docker executable not found"}
    actual_command = _backend_command(
        tool,
        command,
        backend=selected_backend,
        distro=distro,
        network=network,
        docker_image=docker_image,
        cwd=cwd,
    )
    started = time.perf_counter()
    try:
        result = subprocess.run(
            actual_command,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdin=subprocess.DEVNULL,
            timeout=timeout_value,
        )
        return {
            "status": "ok" if result.returncode == 0 else "error",
            "tool": tool.id,
            "backend": selected_backend,
            "command": actual_command,
            "returncode": result.returncode,
            "stdout": _short_output(result.stdout or ""),
            "stderr": _short_output(result.stderr or ""),
            "timed_out": False,
            "seconds": round(time.perf_counter() - started, 4),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "status": "timeout",
            "tool": tool.id,
            "backend": selected_backend,
            "command": actual_command,
            "returncode": -1,
            "stdout": _short_output(str(exc.stdout or "")),
            "stderr": _short_output(str(exc.stderr or "")),
            "timed_out": True,
            "seconds": round(time.perf_counter() - started, 4),
        }
    except OSError as exc:
        return {
            "status": "error",
            "tool": tool.id,
            "backend": selected_backend,
            "command": actual_command,
            "returncode": -1,
            "stdout": "",
            "stderr": str(exc),
            "timed_out": False,
            "seconds": round(time.perf_counter() - started, 4),
        }
