# CTF Agent Transfer Notes

This reference maps the behavior of `ctf-agent` into Hermes-native practice.

## Architecture Mapping

| ctf-agent component | Purpose | Hermes transfer |
|---|---|---|
| `backend/cli.py` | CLI entrypoint, single challenge or coordinator mode | Use `terminal` to run `ctf-agent` directly, or use this skill's native loop |
| `backend/ctfd.py` | CTFd auth, challenge pull, solved names, flag submission | Use CTFd API or `ctf-agent` runner; keep credentials in env |
| `backend/poller.py` | Poll every 5 seconds for new/solved challenges | Use `cronjob` or a long-running terminal process for live competitions |
| `backend/agents/coordinator_loop.py` | Event loop that spawns swarms and handles operator messages | Parent Hermes session acts as coordinator |
| `backend/agents/swarm.py` | Multiple solvers race one challenge | Use `delegate_task` workers, or spawn separate Hermes/ctf-agent processes |
| `backend/prompts.py` | Builds challenge prompt from metadata and distfiles | Use the same brief fields in `metadata.yml` and worker context |
| `backend/sandbox.py` | Docker container per solver | Prefer Docker or another isolated terminal backend |
| `backend/tools/core.py` | Bash, file, web, webhook, image, submit helpers | Use Hermes terminal, file, browser/web tools, and platform submit commands |
| `backend/loop_detect.py` | Warn and break repeated tool loops | Track repeated command signatures in `findings.md` |

## Important Behavioral Rules

1. Service-first: if a challenge includes `connection_info`, connect before local file exploration.
2. Sandbox-first: run unknown binaries and exploit scripts inside an isolated environment.
3. Workspace discipline: read-only distfiles, writable workspace, append-only findings.
4. Sibling findings: inject useful observations from other workers every few steps.
5. Submission gating: deduplicate exact flags, add cooldown after wrong attempts, treat platform
   confirmation as authoritative.
6. Quota/backoff: if an agent/model fails with quota or context exhaustion, preserve its sandbox
   artifacts and resume with another worker rather than throwing away state.
7. Traceability: save commands, outputs, offsets, extracted keys, and candidate derivations.

## Native Hermes Coordinator Recipe

1. Create `findings.md` with metadata and initial scope.
2. Run a first parent pass: service connect, file triage, obvious strings and encodings.
3. Dispatch focused workers with `delegate_task`:
   - pwn/rev worker for binaries.
   - crypto/encoding worker for math and transforms.
   - web/service worker for HTTP/TCP behavior.
   - forensics/stego worker for archives, images, media, filesystems.
4. Require workers to append or return new findings, dead ends, and candidate flags.
5. Parent verifies the strongest candidate and submits.
6. If no solve, bump workers with a distilled "do not repeat" section.

## Running the Original ctf-agent from Hermes

Use this when the user wants full automation against CTFd and the checkout is available:

```bash
cd C:/Users/haqua/Documents/GitHub/ctf-agent
uv sync
docker build -f sandbox/Dockerfile.sandbox -t ctf-sandbox .
uv run ctf-solve --ctfd-url "$CTFD_URL" --ctfd-token "$CTFD_TOKEN" --challenges-dir challenges --max-challenges 10 -v
```

Use `--no-submit` for dry-run analysis. Use `--challenge challenges/<slug>` to solve a single local
challenge. While it runs, Hermes can monitor logs, send operator messages with `ctf-msg`, or inspect
the challenge directory.
