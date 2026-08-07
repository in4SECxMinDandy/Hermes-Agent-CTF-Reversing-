# CTFd Workflow

Use this when a challenge comes from CTFd.

## Credentials

Put the CTFd URL in `ctf.url` in `~/.hermes/config.yaml` and the API token in `CTFD_TOKEN` inside
`~/.hermes/.env`. If only username/password is available, store them in the operator's secret
mechanism and avoid writing them into chat history.

Never commit `.env`, challenge tokens, session cookies, or downloaded private challenge data.

## Pulling Challenges

Use the Hermes wrapper so the workspace contract and path-safety checks are applied:

```bash
hermes ctf pull --unsolved-only
```

Expected layout:

```text
challenges/<slug>/
  metadata.yml
  distfiles/
```

If pulling manually through the API:

1. `GET /api/v1/challenges?per_page=500`
2. For each visible challenge, `GET /api/v1/challenges/<id>`
3. Download `files` into `distfiles/`
4. Convert HTML description to readable Markdown when possible
5. Write `metadata.yml`

## Submission Discipline

The platform is authoritative. A solve is confirmed only when CTFd returns `correct` or
`already_solved`.

Rules:

- Strip whitespace around the candidate flag.
- Deduplicate exact flag strings across workers.
- After wrong submissions, slow down: first retry can be immediate, then wait roughly 30s, 2m, 5m,
  and 10m as wrong count grows.
- Use dry-run mode when the user asks not to submit.
- Record each submitted candidate and response in `findings.md`.

## Live Competition Loop

For live competitions:

1. Poll challenge list and solved list.
2. Spawn work only for unsolved challenges.
3. Limit concurrent challenge count to avoid burning tokens and containers.
4. Kill or stop workers when a challenge is solved externally.
5. Send operator hints into `findings.md` or the active coordinator prompt.
6. Keep a final scoreboard: solved, unsolved, active workers, cost/time if known.

Hermes implementation:

- `hermes ctf run` uses the `ctf-agent` coordinator as the automation engine and Hermes as
  monitor/operator. Its coordinator polls every five seconds, pulls new challenges, and runs
  parallel swarms.
- `hermes ctf score` provides a direct scoreboard snapshot for scripts and operators.
- `hermes ctf status` combines visible, solved, unsolved, and scoreboard state in one snapshot.
- `hermes ctf ad run` provides the authorized Attack & Defense health/patch/attack/flag loop.
