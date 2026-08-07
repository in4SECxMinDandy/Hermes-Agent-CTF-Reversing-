"""CTF orchestration helpers used by ``hermes ctf``.

This module deliberately lives at the CLI edge.  CTFd, challenge workspaces,
the optional solver runner, and Attack & Defense command orchestration do not
belong in the model tool schema that is sent on every agent turn.
"""

from __future__ import annotations

import ipaddress
import json
import logging
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping
from urllib.parse import urljoin, urlparse

import httpx
import yaml

from hermes_cli.config import get_env_value, load_config
from hermes_cli.attack_tools import (
    AttackToolError,
    get_attack_tool,
    normalize_attack_requests,
    run_attack_tool,
)

logger = logging.getLogger(__name__)

DEFAULT_CTF_SANDBOX_IMAGE = "ctf-sandbox"
DEFAULT_CTF_WORKSPACE = "challenges"
DEFAULT_REQUEST_TIMEOUT = 30.0
DEFAULT_FLAG_PATTERN = r"(?:[A-Za-z0-9_.-]+\{[^\r\n{}]+\}|FLAG\[[^\r\n\]]+\])"
MAX_OUTPUT_CHARS = 12000


class CTFError(RuntimeError):
    """A user-actionable CTF orchestration error."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json_dump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False)


def _slugify(value: str) -> str:
    """Create a portable workspace name without allowing path traversal."""
    text = re.sub(r"[^A-Za-z0-9._-]+", "-", str(value).strip().lower())
    text = re.sub(r"-+", "-", text).strip(".-")
    return text[:96] or "challenge"


def _safe_filename(value: str, fallback: str = "file") -> str:
    name = Path(str(value)).name
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip(".")
    if name in {"", ".", ".."}:
        return fallback
    return name[:180]


def _inside(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _as_command(value: Any) -> str | list[str] | None:
    if value is None:
        return None
    if isinstance(value, str) and value.strip():
        return value.strip()
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return list(value) if value else None
    raise CTFError("Attack & Defense commands must be a string or a list of strings")


def _target_host(value: str) -> tuple[str, str | None]:
    """Return a normalized host and optional port from a service/scope value."""
    raw = value.strip().lower()
    parsed = urlparse(raw if "://" in raw else f"//{raw}")
    host = (parsed.hostname or "").strip("[]")
    port: str | None
    try:
        port = str(parsed.port) if parsed.port is not None else None
    except ValueError:
        port = None
    return host, port


def _target_is_in_scope(target: str, scope: Iterable[str]) -> bool:
    """Fail closed unless a target exactly matches an authorized scope entry."""
    target_host, target_port = _target_host(target)
    if not target_host:
        return False
    try:
        target_ip = ipaddress.ip_address(target_host)
    except ValueError:
        target_ip = None
    for raw_scope in scope:
        scope_text = raw_scope.strip().lower()
        if scope_text.startswith("*.") and target_host.endswith(scope_text[1:]):
            return True
        scope_host, scope_port = _target_host(scope_text)
        if not scope_host:
            continue
        try:
            if target_ip is not None and target_ip in ipaddress.ip_network(scope_host, strict=False):
                return scope_port is None or scope_port == target_port
        except ValueError:
            pass
        if target_host == scope_host and (scope_port is None or scope_port == target_port):
            return True
    return False


def _short_output(value: str, limit: int = MAX_OUTPUT_CHARS) -> str:
    if len(value) <= limit:
        return value
    return value[:limit] + f"\n...[truncated {len(value) - limit} chars]"


def _config_section(config: Mapping[str, Any] | None = None) -> dict[str, Any]:
    source = config if config is not None else load_config()
    section = source.get("ctf", {}) if isinstance(source, Mapping) else {}
    return dict(section) if isinstance(section, Mapping) else {}


def _find_ctf_agent(configured: str | None = None) -> Path | None:
    candidates: list[Path] = []
    if configured:
        candidates.append(Path(configured).expanduser())
    repo_root = Path(__file__).resolve().parents[1]
    candidates.extend(
        [
            Path.cwd() / "ctf-agent",
            repo_root.parent / "ctf-agent",
            repo_root / ".." / "ctf-agent",
        ]
    )
    seen: set[str] = set()
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        key = str(resolved).casefold()
        if key in seen:
            continue
        seen.add(key)
        if (resolved / "pyproject.toml").is_file() and (
            resolved / "backend" / "cli.py"
        ).is_file():
            return resolved
    return None


@dataclass(frozen=True)
class CTFSettings:
    url: str = ""
    token: str = ""
    workspace: Path = Path(DEFAULT_CTF_WORKSPACE)
    agent_dir: Path | None = None
    sandbox_image: str = DEFAULT_CTF_SANDBOX_IMAGE
    max_challenges: int = 10
    request_timeout: float = DEFAULT_REQUEST_TIMEOUT
    verify_tls: bool = True


def load_ctf_settings(config: Mapping[str, Any] | None = None) -> CTFSettings:
    section = _config_section(config)
    url = str(section.get("url") or section.get("ctfd_url") or "").strip().rstrip("/")
    env_url = get_env_value("CTFD_URL")
    if env_url:
        url = str(env_url).strip().rstrip("/")
    token = str(get_env_value("CTFD_TOKEN") or get_env_value("CTFD_API_TOKEN") or "").strip()
    workspace = Path(
        str(section.get("workspace") or (Path.cwd() / DEFAULT_CTF_WORKSPACE))
    ).expanduser()
    agent_dir = _find_ctf_agent(section.get("agent_dir"))
    try:
        max_challenges = max(1, int(section.get("max_challenges", 10)))
    except (TypeError, ValueError):
        max_challenges = 10
    try:
        request_timeout = max(1.0, float(section.get("request_timeout", DEFAULT_REQUEST_TIMEOUT)))
    except (TypeError, ValueError):
        request_timeout = DEFAULT_REQUEST_TIMEOUT
    return CTFSettings(
        url=url,
        token=token,
        workspace=workspace,
        agent_dir=agent_dir,
        sandbox_image=str(section.get("sandbox_image") or DEFAULT_CTF_SANDBOX_IMAGE),
        max_challenges=max_challenges,
        request_timeout=request_timeout,
        verify_tls=bool(section.get("verify_tls", True)),
    )


def _require_ctfd(settings: CTFSettings) -> None:
    if not settings.url:
        raise CTFError(
            "CTFd URL is not configured. Set ctf.url in ~/.hermes/config.yaml."
        )
    if not settings.token:
        raise CTFError(
            "CTFd token is not configured. Put CTFD_TOKEN in ~/.hermes/.env."
        )


class CTFdClient:
    """Small synchronous CTFd API client for CLI and test use."""

    def __init__(
        self,
        base_url: str,
        token: str,
        *,
        timeout: float = DEFAULT_REQUEST_TIMEOUT,
        verify_tls: bool = True,
    ) -> None:
        parsed = urlparse(base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise CTFError("CTFd URL must be an absolute http:// or https:// URL")
        self.base_url = base_url.rstrip("/")
        self._origin = (parsed.scheme, parsed.netloc.lower())
        self._client = httpx.Client(
            timeout=timeout,
            verify=verify_tls,
            follow_redirects=False,
            headers={
                "Accept": "application/json",
                "Authorization": f"Token {token}",
            },
        )
        self._challenge_ids: dict[str, int] = {}

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "CTFdClient":
        return self

    def __exit__(self, *_args: Any) -> None:
        self.close()

    def _api_url(self, path: str) -> str:
        return f"{self.base_url}/api/v1/{path.lstrip('/')}"

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        try:
            response = self._client.request(method, self._api_url(path), **kwargs)
        except httpx.HTTPError as exc:
            raise CTFError(f"CTFd request failed: {exc}") from exc
        if response.status_code >= 400:
            body = _short_output(response.text.strip(), 1000)
            raise CTFError(f"CTFd returned HTTP {response.status_code}: {body}")
        try:
            payload = response.json()
        except ValueError as exc:
            raise CTFError("CTFd returned a non-JSON response") from exc
        if isinstance(payload, Mapping) and payload.get("success") is False:
            raise CTFError(str(payload.get("message") or "CTFd rejected the request"))
        return payload

    def list_challenges(self, *, page_size: int = 500) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        seen_ids: set[Any] = set()
        page = 1
        for _ in range(100):
            payload = self._request(
                "GET", "/challenges", params={"page": page, "per_page": page_size}
            )
            rows = payload.get("data", []) if isinstance(payload, Mapping) else []
            if not isinstance(rows, list):
                raise CTFError("CTFd challenge response has an invalid data field")
            new_rows = [
                dict(row)
                for row in rows
                if isinstance(row, Mapping)
                and row.get("id") not in seen_ids
                and row.get("type") != "hidden"
                and row.get("state") != "hidden"
            ]
            result.extend(new_rows)
            seen_ids.update(row.get("id") for row in new_rows)
            pagination = payload.get("meta", {}).get("pagination", {}) if isinstance(payload, Mapping) else {}
            next_page = pagination.get("next") if isinstance(pagination, Mapping) else None
            if next_page in (None, 0, False) or not rows:
                break
            try:
                next_page_int = int(next_page)
            except (TypeError, ValueError):
                break
            if next_page_int <= page:
                break
            page = next_page_int
            if len(rows) < page_size and not next_page:
                break
        return result

    def get_challenge(self, challenge_id: int) -> dict[str, Any]:
        payload = self._request("GET", f"/challenges/{int(challenge_id)}")
        data = payload.get("data", {}) if isinstance(payload, Mapping) else {}
        return dict(data) if isinstance(data, Mapping) else {}

    def challenge_id(self, name: str) -> int:
        if name in self._challenge_ids:
            return self._challenge_ids[name]
        for row in self.list_challenges():
            if row.get("name") and row.get("id") is not None:
                self._challenge_ids[str(row["name"])] = int(row["id"])
        try:
            return self._challenge_ids[name]
        except KeyError as exc:
            raise CTFError(f'Challenge "{name}" was not found in CTFd') from exc

    def solved_names(self) -> set[str]:
        me = self._request("GET", "/users/me")
        user = me.get("data", {}) if isinstance(me, Mapping) else {}
        team_id = user.get("team_id") if isinstance(user, Mapping) else None
        if team_id:
            payload = self._request("GET", f"/teams/{int(team_id)}/solves")
        else:
            user_id = user.get("id") if isinstance(user, Mapping) else None
            if not user_id:
                return set()
            payload = self._request("GET", f"/users/{int(user_id)}/solves")
        rows = payload.get("data", []) if isinstance(payload, Mapping) else []
        names: set[str] = set()
        for row in rows:
            if not isinstance(row, Mapping):
                continue
            challenge = row.get("challenge", {})
            if isinstance(challenge, Mapping) and challenge.get("name"):
                names.add(str(challenge["name"]))
        return names

    def scoreboard(self, *, top: int | None = None) -> list[dict[str, Any]]:
        path = "/scoreboard" if top is None else f"/scoreboard/top/{max(1, int(top))}"
        payload = self._request("GET", path)
        rows = payload.get("data", []) if isinstance(payload, Mapping) else []
        return [dict(row) for row in rows if isinstance(row, Mapping)]

    def challenge_files(self, challenge_id: int) -> list[dict[str, Any]]:
        try:
            payload = self._request("GET", f"/challenges/{int(challenge_id)}/files")
        except CTFError:
            return []
        rows = payload.get("data", []) if isinstance(payload, Mapping) else []
        return [dict(row) for row in rows if isinstance(row, Mapping)]

    def _download_url(self, raw: str) -> str:
        if raw.startswith("http://") or raw.startswith("https://"):
            parsed = urlparse(raw)
            if (parsed.scheme, parsed.netloc.lower()) != self._origin:
                raise CTFError("Refusing to send the CTFd token to a different download host")
            return raw
        path = raw if raw.startswith("/") else f"/files/{raw.lstrip('/')}"
        return urljoin(self.base_url + "/", path.lstrip("/"))

    def download_file(self, raw: str, destination: Path) -> int:
        url = self._download_url(raw)
        try:
            with self._client.stream("GET", url) as response:
                if response.status_code >= 400:
                    raise CTFError(f"CTFd file download returned HTTP {response.status_code}")
                destination.parent.mkdir(parents=True, exist_ok=True)
                with destination.open("wb") as handle:
                    size = 0
                    for chunk in response.iter_bytes():
                        handle.write(chunk)
                        size += len(chunk)
                    return size
        except httpx.HTTPError as exc:
            raise CTFError(f"CTFd file download failed: {exc}") from exc

    def submit_flag(self, challenge: str, flag: str) -> dict[str, Any]:
        payload = self._request(
            "POST",
            "/challenges/attempt",
            json={"challenge_id": self.challenge_id(challenge), "submission": flag.strip()},
        )
        data = payload.get("data", {}) if isinstance(payload, Mapping) else {}
        data = dict(data) if isinstance(data, Mapping) else {}
        return {
            "challenge": challenge,
            "status": str(data.get("status", "unknown")),
            "message": str(data.get("message", "")),
        }


def live_status(settings: CTFSettings, *, top: int | None = None) -> dict[str, Any]:
    """Return one authoritative CTFd status snapshot for operators/scripts."""
    _require_ctfd(settings)
    with CTFdClient(
        settings.url,
        settings.token,
        timeout=settings.request_timeout,
        verify_tls=settings.verify_tls,
    ) as client:
        challenges = client.list_challenges()
        solved = client.solved_names()
        scoreboard = client.scoreboard(top=top)
    return {
        "workspace": str(settings.workspace),
        "challenges": len(challenges),
        "solved": len(solved),
        "unsolved": max(0, len(challenges) - len(solved)),
        "solved_names": sorted(solved),
        "scoreboard": scoreboard,
    }


def _metadata_for_challenge(challenge: Mapping[str, Any]) -> dict[str, Any]:
    fields = (
        "name",
        "category",
        "description",
        "value",
        "connection_info",
        "tags",
        "solves",
        "hints",
    )
    result: dict[str, Any] = {field: challenge.get(field, "") for field in fields}
    result["name"] = str(result.get("name") or "Unknown")
    result["category"] = str(result.get("category") or "")
    result["description"] = str(result.get("description") or "")
    result["value"] = int(result.get("value") or 0)
    result["connection_info"] = str(result.get("connection_info") or "")
    result["tags"] = list(result.get("tags") or [])
    result["solves"] = int(result.get("solves") or 0)
    result["hints"] = list(result.get("hints") or [])
    return result


def ensure_challenge_workspace(
    challenge_dir: Path,
    metadata: Mapping[str, Any],
    *,
    replace_metadata: bool = True,
) -> Path:
    """Create the challenge contract without deleting existing solver work."""
    challenge_dir = challenge_dir.expanduser().resolve()
    challenge_dir.mkdir(parents=True, exist_ok=True)
    for name in ("distfiles", "workspace", "traces"):
        (challenge_dir / name).mkdir(exist_ok=True)
    metadata_path = challenge_dir / "metadata.yml"
    if replace_metadata or not metadata_path.exists():
        metadata_path.write_text(
            yaml.safe_dump(dict(metadata), allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
    findings_path = challenge_dir / "findings.md"
    if not findings_path.exists():
        findings_path.write_text(
            f"# {metadata.get('name', challenge_dir.name)} findings\n\n"
            "## Workspace\n\n"
            "- Created by `hermes ctf`\n"
            "- `distfiles/` is input material; generated work belongs in `workspace/`.\n",
            encoding="utf-8",
        )
    return challenge_dir


def _file_reference(file_info: Any) -> tuple[str, str]:
    if isinstance(file_info, str):
        raw = file_info
        name = Path(urlparse(raw).path).name
    elif isinstance(file_info, Mapping):
        raw = str(
            file_info.get("url")
            or file_info.get("location")
            or file_info.get("path")
            or ""
        )
        name = str(file_info.get("name") or Path(urlparse(raw).path).name)
    else:
        raise CTFError("CTFd file entry must be a URL, path, or object")
    if not raw:
        raise CTFError("CTFd file entry has no download location")
    return raw, _safe_filename(name)


def pull_challenges(
    settings: CTFSettings,
    *,
    root: Path | None = None,
    category: str | None = None,
    unsolved_only: bool = False,
    limit: int | None = None,
    force: bool = False,
) -> list[dict[str, Any]]:
    _require_ctfd(settings)
    root = (root or settings.workspace).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    with CTFdClient(
        settings.url,
        settings.token,
        timeout=settings.request_timeout,
        verify_tls=settings.verify_tls,
    ) as client:
        challenges = client.list_challenges()
        solved = client.solved_names() if unsolved_only else set()
        for stub in challenges:
            name = str(stub.get("name") or "Unknown")
            if category and str(stub.get("category", "")).casefold() != category.casefold():
                continue
            if name in solved:
                continue
            if limit is not None and len(records) >= max(0, limit):
                break
            detail = client.get_challenge(int(stub["id"]))
            if not detail:
                detail = stub
            metadata = _metadata_for_challenge(detail)
            challenge_dir = ensure_challenge_workspace(root / _slugify(name), metadata)
            file_entries = detail.get("files") or client.challenge_files(int(stub["id"]))
            downloaded: list[str] = []
            for file_info in file_entries or []:
                raw, filename = _file_reference(file_info)
                destination = challenge_dir / "distfiles" / filename
                if destination.exists() and not force:
                    downloaded.append(filename)
                    continue
                client.download_file(raw, destination)
                downloaded.append(filename)
            records.append(
                {
                    "name": name,
                    "category": metadata["category"],
                    "value": metadata["value"],
                    "solves": metadata["solves"],
                    "path": str(challenge_dir),
                    "files": downloaded,
                }
            )
    return records


def init_local_challenge(source: Path, destination_root: Path) -> Path:
    """Normalize a local directory or archive into the workspace contract."""
    source = source.expanduser().resolve()
    if not source.exists():
        raise CTFError(f"Challenge source does not exist: {source}")
    destination_root = destination_root.expanduser().resolve()
    destination_root.mkdir(parents=True, exist_ok=True)
    if source.is_dir() and (source / "metadata.yml").is_file():
        challenge_dir = source
        metadata = yaml.safe_load((source / "metadata.yml").read_text(encoding="utf-8")) or {}
        return ensure_challenge_workspace(challenge_dir, metadata, replace_metadata=False)
    name = source.stem if source.is_file() else source.name
    challenge_dir = destination_root / _slugify(name)
    metadata = {
        "version": "beta1",
        "name": name,
        "category": "",
        "description": "",
        "value": 0,
        "connection_info": "",
        "tags": [],
        "solves": 0,
        "hints": [],
    }
    ensure_challenge_workspace(challenge_dir, metadata)
    if source.is_file():
        shutil.copy2(source, challenge_dir / "distfiles" / _safe_filename(source.name))
    else:
        target = challenge_dir / "distfiles"
        for child in source.iterdir():
            if child.is_file():
                shutil.copy2(child, target / _safe_filename(child.name))
    return challenge_dir


def _run_process(
    command: str | list[str],
    *,
    cwd: Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float = 60.0,
) -> dict[str, Any]:
    shell = isinstance(command, str)
    try:
        result = subprocess.run(
            command,
            cwd=str(cwd) if cwd else None,
            env=dict(env) if env else None,
            shell=shell,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=max(1.0, timeout),
        )
        return {
            "returncode": result.returncode,
            "stdout": _short_output(result.stdout or ""),
            "stderr": _short_output(result.stderr or ""),
            "timed_out": False,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "returncode": -1,
            "stdout": _short_output(str(exc.stdout or "")),
            "stderr": _short_output(str(exc.stderr or "")),
            "timed_out": True,
        }
    except OSError as exc:
        return {"returncode": -1, "stdout": "", "stderr": str(exc), "timed_out": False}


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    temporary.write_text(_json_dump(value) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_ad_config(path: Path) -> dict[str, Any]:
    path = path.expanduser().resolve()
    if not path.is_file():
        raise CTFError(f"Attack & Defense config does not exist: {path}")
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise CTFError(f"Could not read Attack & Defense config: {exc}") from exc
    if not isinstance(raw, Mapping):
        raise CTFError("Attack & Defense config root must be a mapping")
    if raw.get("authorized") is not True:
        raise CTFError(
            "Attack & Defense config must set authorized: true for an explicitly authorized CTF/lab"
        )
    scope = raw.get("scope")
    if not isinstance(scope, list) or not scope or not all(isinstance(item, str) and item.strip() for item in scope):
        raise CTFError("Attack & Defense config requires a non-empty scope list")
    services = raw.get("services")
    if not isinstance(services, list) or not services:
        raise CTFError("Attack & Defense config requires at least one service")
    allow_high_risk = raw.get("allow_high_risk") is True
    normalized: list[dict[str, Any]] = []
    names: set[str] = set()
    for item in services:
        if not isinstance(item, Mapping):
            raise CTFError("Each Attack & Defense service must be a mapping")
        name = str(item.get("name") or "").strip()
        target = str(item.get("target") or "").strip()
        healthcheck = _as_command(item.get("healthcheck"))
        if not name or name in names:
            raise CTFError(f"Service name is missing or duplicated: {name!r}")
        if not target or healthcheck is None:
            raise CTFError(f"Service {name!r} requires target and healthcheck")
        if not _target_is_in_scope(target, scope):
            raise CTFError(
                f"Service {name!r} target {target!r} is outside the declared scope"
            )
        try:
            attack_tools = normalize_attack_requests(item.get("attack_tools"))
        except AttackToolError as exc:
            raise CTFError(f"Service {name!r} has invalid attack_tools: {exc}") from exc
        high_risk_tools = [
            request["id"]
            for request in attack_tools
            if get_attack_tool(request["id"]).risk == "high"
        ]
        if high_risk_tools and not allow_high_risk:
            raise CTFError(
                "Attack & Defense config must set allow_high_risk: true for: "
                + ", ".join(high_risk_tools)
            )
        names.add(name)
        normalized.append(
            {
                **dict(item),
                "name": name,
                "target": target,
                "healthcheck": healthcheck,
                "patch": _as_command(item.get("patch")),
                "attack": _as_command(item.get("attack")),
                "attack_tools": attack_tools,
                "flag_command": _as_command(item.get("flag_command")),
            }
        )
    result = dict(raw)
    result["allow_high_risk"] = allow_high_risk
    result["scope"] = list(scope)
    result["services"] = normalized
    result["flag_pattern"] = str(raw.get("flag_pattern") or DEFAULT_FLAG_PATTERN)
    try:
        result["command_timeout"] = max(1.0, float(raw.get("command_timeout", 60)))
    except (TypeError, ValueError):
        result["command_timeout"] = 60.0
    return result


def _ad_state_path(config_path: Path, state: Path | None) -> Path:
    if state:
        return state.expanduser().resolve()
    return config_path.expanduser().resolve().with_suffix(".scoreboard.json")


def _extract_flags(text: str, pattern: str) -> list[str]:
    try:
        found = re.findall(pattern, text)
    except re.error as exc:
        raise CTFError(f"Invalid flag_pattern: {exc}") from exc
    values: list[str] = []
    for item in found:
        value = item if isinstance(item, str) else item[0]
        value = value.strip()
        if value and value not in values:
            values.append(value)
    return values


def run_attack_defense_once(
    config_path: Path,
    *,
    state_path: Path | None = None,
    live: bool = False,
) -> dict[str, Any]:
    """Run one authorized A&D cycle and persist an auditable scoreboard."""
    config = load_ad_config(config_path)
    if not live:
        return {
            "mode": "dry-run",
            "authorized": True,
            "services": [
                {
                    "name": service["name"],
                    "target": service["target"],
                    "commands": [key for key in ("healthcheck", "patch", "attack", "flag_command") if service.get(key)],
                    "attack_tools": [request["id"] for request in service.get("attack_tools", [])],
                }
                for service in config["services"]
            ],
        }
    state_path = _ad_state_path(config_path, state_path)
    try:
        state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
    except (OSError, json.JSONDecodeError):
        state = {}
    state.setdefault("authorized_scope", config["scope"])
    state.setdefault("services", {})
    state.setdefault("flags", [])
    events: list[dict[str, Any]] = []
    pattern = config["flag_pattern"]
    for service in config["services"]:
        name = service["name"]
        service_state = state["services"].setdefault(name, {"health_failures": 0, "attacks": 0, "flags": []})
        env = os.environ.copy()
        env.update(
            {
                "HERMES_CTF_MODE": "attack-defense",
                "HERMES_CTF_SERVICE": name,
                "HERMES_CTF_TARGET": service["target"],
            }
        )
        health = _run_process(
            service["healthcheck"],
            cwd=config_path.parent,
            env=env,
            timeout=config["command_timeout"],
        )
        if health["returncode"] == 0:
            service_state["health_failures"] = 0
        else:
            service_state["health_failures"] = int(service_state.get("health_failures", 0)) + 1
        service_state["last_health"] = health
        service_state["last_checked_at"] = _now()
        events.append({"time": _now(), "service": name, "action": "healthcheck", "result": health})
        if health["returncode"] != 0 and service.get("patch"):
            patch_result = _run_process(
                service["patch"],
                cwd=config_path.parent,
                env=env,
                timeout=config["command_timeout"],
            )
            service_state["last_patch"] = patch_result
            events.append({"time": _now(), "service": name, "action": "patch", "result": patch_result})
        tool_state = service_state.setdefault("attack_tools", {})
        for request in service.get("attack_tools", []):
            tool_id = request["id"]
            tool_result = run_attack_tool(
                tool_id,
                service["target"],
                args=request["args"],
                backend=request["backend"],
                distro=request.get("distro"),
                network=request["network"],
                docker_image=request.get("docker_image"),
                cwd=config_path.parent,
                timeout=request["timeout"],
                allow_high_risk=config["allow_high_risk"],
            )
            current = tool_state.setdefault(tool_id, {"runs": 0, "ok": 0, "errors": 0})
            current["runs"] = int(current.get("runs", 0)) + 1
            if tool_result.get("status") == "ok":
                current["ok"] = int(current.get("ok", 0)) + 1
            else:
                current["errors"] = int(current.get("errors", 0)) + 1
            current["last_result"] = tool_result
            events.append(
                {
                    "time": _now(),
                    "service": name,
                    "action": "attack_tool",
                    "tool": tool_id,
                    "result": tool_result,
                }
            )
        if service.get("attack"):
            attack_result = _run_process(
                service["attack"],
                cwd=config_path.parent,
                env=env,
                timeout=config["command_timeout"],
            )
            service_state["attacks"] = int(service_state.get("attacks", 0)) + 1
            events.append({"time": _now(), "service": name, "action": "attack", "result": attack_result})
        if service.get("flag_command"):
            flag_result = _run_process(
                service["flag_command"],
                cwd=config_path.parent,
                env=env,
                timeout=config["command_timeout"],
            )
            flags = _extract_flags(flag_result["stdout"] + "\n" + flag_result["stderr"], pattern)
            for flag in flags:
                if flag not in state["flags"]:
                    state["flags"].append(flag)
                if flag not in service_state["flags"]:
                    service_state["flags"].append(flag)
            events.append(
                {"time": _now(), "service": name, "action": "flag", "result": flag_result, "flags": flags}
            )
        state["services"][name] = service_state
    state["updated_at"] = _now()
    state["events"] = events[-100:]
    state["score"] = sum(
        int(config_service.get("flag_points", config_service.get("points", 0)) or 0)
        for config_service in config["services"]
        if any(flag in state["flags"] for flag in state["services"].get(config_service["name"], {}).get("flags", []))
    )
    _write_json(state_path, state)
    return state


def _check_docker_image(image: str) -> dict[str, Any]:
    docker = shutil.which("docker")
    if not docker:
        return {"ok": False, "detail": "docker executable not found"}
    result = _run_process([docker, "image", "inspect", image], timeout=15)
    return {"ok": result["returncode"] == 0, "detail": result["stderr"] or image}


def doctor(settings: CTFSettings, *, network: bool = False) -> dict[str, Any]:
    checks: dict[str, dict[str, Any]] = {}
    skill_root = Path(__file__).resolve().parents[1] / "optional-skills" / "security" / "ctf-solver"
    skill_path = skill_root / "SKILL.md"
    checks["ctf_solver_skill"] = {"ok": skill_path.is_file(), "detail": str(skill_path)}
    checks["workspace"] = {
        "ok": settings.workspace.is_dir() or settings.workspace.parent.is_dir(),
        "detail": str(settings.workspace),
    }
    checks["docker"] = {"ok": shutil.which("docker") is not None, "detail": shutil.which("docker") or "missing"}
    checks["sandbox_image"] = _check_docker_image(settings.sandbox_image) if checks["docker"]["ok"] else {"ok": False, "detail": "docker unavailable"}
    agent_files = (
        Path("backend/cli.py"),
        Path("backend/ctfd.py"),
        Path("backend/poller.py"),
        Path("backend/sandbox.py"),
        Path("backend/agents/swarm.py"),
    )
    agent_missing = [
        str(path)
        for path in agent_files
        if settings.agent_dir is None or not (settings.agent_dir / path).is_file()
    ]
    checks["ctf_agent"] = {
        "ok": not agent_missing,
        "detail": str(settings.agent_dir or "not found")
        if not agent_missing
        else "missing: " + ", ".join(agent_missing),
    }
    checks["solver_runtime"] = {
        "ok": shutil.which("uv") is not None,
        "detail": shutil.which("uv") or "uv executable not found",
    }
    checks["ctfd_config"] = {"ok": bool(settings.url and settings.token), "detail": settings.url or "ctf.url not configured"}
    playbook_files = [
        skill_root / "references" / "category-playbooks.md",
        skill_root / "references" / "sandbox-toolbox.md",
        skill_root / "references" / "ctfd-workflow.md",
    ]
    try:
        category_text = (skill_root / "references" / "category-playbooks.md").read_text(encoding="utf-8").casefold()
    except OSError:
        category_text = ""
    required_categories = ("web", "crypto", "reverse", "forensics", "pwn")
    checks["playbooks"] = {
        "ok": all(path.is_file() for path in playbook_files)
        and all(category in category_text for category in required_categories),
        "detail": ", ".join(str(path) for path in playbook_files),
    }
    try:
        skill_text = skill_path.read_text(encoding="utf-8") if skill_path.is_file() else ""
    except OSError:
        skill_text = ""
    checks["evidence_contract"] = {
        "ok": bool(skill_text) and "findings.md" in skill_text and "traces/" in skill_text,
        "detail": "findings.md, traces/, and loop-detection rules",
    }
    checks["ad_runner"] = {"ok": True, "detail": "hermes ctf ad run"}
    if network and settings.url and settings.token:
        try:
            with CTFdClient(settings.url, settings.token, timeout=settings.request_timeout, verify_tls=settings.verify_tls) as client:
                challenges = client.list_challenges()
                scoreboard = client.scoreboard(top=1)
            checks["ctfd_connectivity"] = {
                "ok": True,
                "detail": f"{len(challenges)} visible challenge(s), scoreboard reachable ({len(scoreboard)} row(s))",
            }
        except CTFError as exc:
            checks["ctfd_connectivity"] = {"ok": False, "detail": str(exc)}
    else:
        checks["ctfd_connectivity"] = {"ok": None, "detail": "not probed; use --network"}
    return {"checks": checks, "ok": all(item["ok"] is not False for item in checks.values())}


def assessment(settings: CTFSettings, *, network: bool = False) -> dict[str, Any]:
    report = doctor(settings, network=network)
    checks = report["checks"]
    ctfd_ready = checks["ctfd_config"]["ok"] and (
        not network or checks["ctfd_connectivity"]["ok"] is True
    )
    rubric = [
        ("Authorization and scope discipline", checks["ctf_solver_skill"]["ok"], "skill requires CTF/lab authorization"),
        ("Workspace contract", checks["workspace"]["ok"], "metadata, distfiles, workspace, findings, traces"),
        ("Isolated CTF toolchain", checks["sandbox_image"]["ok"], "ctf-sandbox is available"),
        ("Five-category playbooks", checks["playbooks"]["ok"], "web, crypto, reverse, forensics, pwn"),
        ("Parallel solver orchestration", checks["ctf_agent"]["ok"] and checks["solver_runtime"]["ok"], "external ctf-agent coordinator/swarm"),
        ("Evidence and loop discipline", checks["evidence_contract"]["ok"], "findings, traces, deduplication, bump"),
        ("CTFd discovery and pull", checks["ctfd_config"]["ok"], "API URL and token configured"),
        ("Verified flag submission", ctfd_ready, "attempt endpoint with explicit submit"),
        ("Scoreboard and live status", ctfd_ready and checks["ctf_agent"]["ok"], "scoreboard API and poll-capable runner"),
        ("Attack & Defense orchestration", checks["ad_runner"]["ok"], "authorized config, health, patch, attack, flag state"),
    ]
    score = sum(1 for _, ok, _ in rubric if ok)
    return {
        "score": score,
        "out_of": 10,
        "label": "ready" if score == 10 else "partial",
        "rubric": [{"item": item, "ok": ok, "detail": detail} for item, ok, detail in rubric],
        "doctor": report,
    }


def build_ctf_agent_command(
    settings: CTFSettings,
    *,
    challenge: str | None = None,
    challenges_dir: Path | None = None,
    submit: bool = False,
    coordinator: str = "claude",
    models: Iterable[str] = (),
) -> tuple[list[str], dict[str, str], Path]:
    if settings.agent_dir is None:
        raise CTFError("ctf-agent checkout was not found; set ctf.agent_dir in config.yaml")
    uv = shutil.which("uv")
    if not uv:
        raise CTFError("uv is required to run ctf-agent")
    env = os.environ.copy()
    if settings.url:
        env["CTFD_URL"] = settings.url
    if settings.token:
        env["CTFD_TOKEN"] = settings.token
    command = [uv, "run", "ctf-solve", "--image", settings.sandbox_image, "--coordinator", coordinator]
    if challenge:
        command.extend(["--challenge", str(Path(challenge).expanduser().resolve())])
    else:
        command.extend(["--challenges-dir", str((challenges_dir or settings.workspace).expanduser().resolve())])
        command.extend(["--max-challenges", str(settings.max_challenges)])
    for model in models:
        command.extend(["--models", model])
    if not submit:
        command.append("--no-submit")
    return command, env, settings.agent_dir


def run_ctf_agent(
    settings: CTFSettings,
    *,
    challenge: str | None = None,
    challenges_dir: Path | None = None,
    submit: bool = False,
    coordinator: str = "claude",
    models: Iterable[str] = (),
) -> int:
    if submit:
        _require_ctfd(settings)
    command, env, cwd = build_ctf_agent_command(
        settings,
        challenge=challenge,
        challenges_dir=challenges_dir,
        submit=submit,
        coordinator=coordinator,
        models=models,
    )
    print(f"Running CTF solver in {cwd}")
    print("Command: " + " ".join(shlex.quote(part) for part in command))
    return subprocess.call(command, cwd=str(cwd), env=env)


def _print(value: Any, *, as_json: bool = False) -> None:
    print(_json_dump(value) if as_json else value)


def cmd_ctf(args: Any) -> int | None:
    try:
        return _cmd_ctf(args)
    except CTFError as exc:
        print(f"CTF error: {exc}", file=sys.stderr)
        return 2


def _cmd_ctf(args: Any) -> int | None:
    settings = load_ctf_settings()
    action = getattr(args, "ctf_action", None)
    if action == "doctor":
        result = doctor(settings, network=args.network)
        _print(result, as_json=args.json)
        return 0 if result["ok"] else 1
    if action == "assess":
        result = assessment(settings, network=args.network)
        _print(result, as_json=args.json)
        return 0 if result["score"] == 10 else 2
    if action == "init":
        source = Path(args.source).expanduser() if args.source else Path.cwd()
        result = init_local_challenge(source, Path(args.root))
        _print({"path": str(result)})
        return 0
    if action == "triage":
        from hermes_cli.ctf_triage import run_triage

        result = run_triage(
            Path(args.challenge),
            image=args.image or settings.sandbox_image,
            engine=args.engine,
            network=args.network,
            timeout=args.timeout,
        )
        _print(result, as_json=args.json)
        return 0 if result["result"]["returncode"] == 0 else 2
    if action == "benchmark":
        from hermes_cli.ctf_benchmark import run_benchmark

        result = run_benchmark(
            Path(args.root) if args.root else settings.workspace,
            repeats=args.repeats,
            timeout=args.timeout,
            execute=args.execute,
            report_path=Path(args.report) if args.report else None,
        )
        _print(result, as_json=args.json)
        return 0 if not args.execute or result["metrics"]["practical_score"] == 10 else 2
    if action == "pull":
        result = pull_challenges(
            settings,
            root=Path(args.root) if args.root else settings.workspace,
            category=args.category,
            unsolved_only=args.unsolved_only,
            limit=args.limit,
            force=args.force,
        )
        _print({"count": len(result), "challenges": result}, as_json=args.json)
        return 0
    if action == "score":
        _require_ctfd(settings)
        with CTFdClient(settings.url, settings.token, timeout=settings.request_timeout, verify_tls=settings.verify_tls) as client:
            result = client.scoreboard(top=args.top)
        _print(result, as_json=args.json)
        return 0
    if action == "status":
        result = live_status(settings, top=args.top)
        _print(result, as_json=args.json)
        return 0
    if action == "submit":
        if not args.yes:
            raise CTFError("Flag submission is an external side effect; pass --yes explicitly")
        _require_ctfd(settings)
        with CTFdClient(settings.url, settings.token, timeout=settings.request_timeout, verify_tls=settings.verify_tls) as client:
            result = client.submit_flag(args.challenge, args.flag)
        _print(result, as_json=args.json)
        return 0 if result["status"] in {"correct", "already_solved"} else 2
    if action == "run":
        if args.challenge is None:
            _require_ctfd(settings)
        return run_ctf_agent(
            settings,
            challenge=args.challenge,
            challenges_dir=Path(args.challenges_dir) if args.challenges_dir else settings.workspace,
            submit=args.submit,
            coordinator=args.coordinator,
            models=args.model or (),
        )
    if action == "attack":
        if args.attack_action == "list":
            from hermes_cli.attack_tools import list_attack_tools

            _print(list_attack_tools(), as_json=args.json)
            return 0
    if action == "ad":
        if not args.ad_action:
            raise CTFError("Choose an A&D action; use `hermes ctf ad --help`")
        config_path = Path(args.config).expanduser().resolve()
        if args.ad_action == "doctor":
            result = load_ad_config(config_path)
            _print({"ok": True, "scope": result["scope"], "services": result["services"]}, as_json=args.json)
            return 0
        if args.ad_action == "status":
            state_path = _ad_state_path(config_path, Path(args.state) if args.state else None)
            result = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {"status": "not started"}
            _print(result, as_json=args.json)
            return 0
        if args.ad_action == "run":
            if not args.live:
                result = run_attack_defense_once(config_path, state_path=Path(args.state) if args.state else None, live=False)
                _print(result, as_json=args.json)
                return 0
            cycles = None if args.watch else max(1, args.cycles)
            result: dict[str, Any] = {}
            completed = 0
            while cycles is None or completed < cycles:
                result = run_attack_defense_once(config_path, state_path=Path(args.state) if args.state else None, live=True)
                completed += 1
                if cycles is None or completed < cycles:
                    time.sleep(max(1.0, args.interval))
            _print(result, as_json=args.json)
            return 0
    raise CTFError("Choose a ctf action; use `hermes ctf --help`")
