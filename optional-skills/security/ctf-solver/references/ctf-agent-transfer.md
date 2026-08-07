# CTF Agent Transfer Notes

This reference maps the behavior of `ctf-agent` into Hermes-native practice.

## Architecture Mapping

| ctf-agent component | Purpose | Hermes transfer |
|---|---|---|
| `backend/cli.py` | CLI entrypoint, single challenge or coordinator mode | Use `hermes ctf run` to launch the configured checkout |
| `backend/ctfd.py` | CTFd auth, challenge pull, solved names, flag submission | Use `hermes ctf pull`, `score`, and `submit`, or the wrapped runner |
| `backend/poller.py` | Poll every 5 seconds for new/solved challenges | `hermes ctf run` delegates to this coordinator loop |
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

## Running ctf-agent through Hermes

Use the Hermes CLI when the user wants full automation against CTFd and the checkout is available:

```bash
hermes ctf doctor --network
hermes ctf run --challenges-dir ~/ctf-challenges
```

The wrapper uses `--no-submit` by default for dry-run analysis. Add `--submit` only for explicit
live scoring. Use `hermes ctf run --challenge <workspace>/<slug>` for one local challenge. While it
runs, Hermes can monitor logs, send operator messages with `ctf-msg`, or inspect the challenge
directory.
