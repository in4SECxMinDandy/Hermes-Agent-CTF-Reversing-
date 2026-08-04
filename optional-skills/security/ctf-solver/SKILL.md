---
name: ctf-solver
description: "Use when solving authorized CTF and CTFd challenges."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
category: security
triggers:
  - "solve this CTF"
  - "CTFd"
  - "reverse challenge"
  - "pwn challenge"
  - "crypto challenge"
  - "forensics challenge"
  - "stego challenge"
  - "find the flag"
toolsets:
  - terminal
  - file
  - web
  - browser
  - delegation
metadata:
  hermes:
    tags: [ctf, ctfd, reverse-engineering, pwn, crypto, forensics, stego, sandbox, multi-agent]
    category: security
    related_skills: [web-pentest, systematic-debugging, subagent-driven-development]
---

# CTF Solver

## Overview

This skill transfers the operating discipline of the `ctf-agent` project into Hermes. It is for
authorized CTFs, local challenge labs, and intentionally vulnerable services. Treat every target as
in-scope only when it is a CTF platform, a local challenge, or the operator explicitly confirms
authorization.

Core idea: run like a coordinator. Put each challenge in a reproducible workspace, inspect it in an
isolated environment, delegate parallel solver angles when useful, share findings through files, and
submit only verified candidate flags.

## When to Use

Use this skill for:

- CTFd competitions, downloaded challenge folders, or one-off flag hunts.
- Reverse engineering, pwn, crypto, web, forensics, stego, and misc challenges.
- Building a Hermes-native replacement for `ctf-agent` swarm behavior.
- Running `ctf-agent` from Hermes when that checkout is available.

Do not use this skill for real-world systems without written authorization. For ordinary web app
security assessments, use `web-pentest` instead.

## Source Transfer

The transferred behavior comes from these `ctf-agent` concepts:

- `poller.py` and `ctfd.py`: discover CTFd challenges, download files, track solves, submit flags.
- `prompts.py`: service-first prompt discipline, metadata-driven challenge briefs, image and binary hints.
- `sandbox.py` and `sandbox/Dockerfile.sandbox`: isolate solver work in Docker with CTF tooling.
- `agents/swarm.py`: run multiple solvers per challenge, race them, share findings, stop on confirmed flag.
- `loop_detect.py`: stop repeated identical tool calls and force a new angle.
- `tools/core.py`: keep sandbox operations small, truncate output, treat binary reads as command-driven analysis.

Load `references/ctf-agent-transfer.md` when you need a detailed mapping from the source project to
Hermes behavior.

## Workspace Contract

Create or normalize each challenge into this layout:

```text
challenge-name/
  metadata.yml
  distfiles/
  workspace/
  findings.md
  traces/
```

`metadata.yml` should include `name`, `category`, `description`, `value`, `connection_info`, `tags`,
`hints`, and `solves` when available. Use `templates/challenge-metadata.yml` as the shape.

`distfiles/` is input material. Treat it as read-only. `workspace/` is for generated scripts, patched
files, decoded artifacts, exploit drafts, and solver notes. `findings.md` is the shared blackboard.

## Operating Loop

1. **Scope and setup.** Confirm this is a CTF/lab target if not obvious. Create the workspace and
   record target URLs, hostnames, ports, flag format, and submission mode. Completion: `metadata.yml`
   and `findings.md` exist.

2. **Prefer an isolated shell.** Use Docker when available. If the `ctf-agent` sandbox image exists,
   run commands there. If not, use local tooling carefully or build a sandbox from the CTF agent
   Dockerfile. Completion: you know where commands execute and where files are mounted.

3. **First action rule.** If `connection_info` exists, connect to the service before exploring local
   files. For TCP services, use a heredoc or a small Python/pwntools script so a single command can
   exercise stateful interaction. Completion: the service greeting/protocol or first HTTP response is
   captured in `findings.md`.

4. **Triage.** Inspect metadata, file types, strings, headers, archive contents, and obvious encodings.
   For images, visually inspect early before deep stego. For binaries, capture `file`, `checksec`,
   imports, strings, and architecture before deeper work. Completion: `findings.md` states likely
   category, promising attack surfaces, and dead ends already tried.

5. **Choose playbooks.** Load `references/category-playbooks.md` for category-specific commands and
   decision trees. Load `references/sandbox-toolbox.md` when deciding which tool to try next.
   Completion: each active hypothesis has a next command or proof probe.

6. **Delegate when parallelism helps.** Use `delegate_task` for independent angles, not for tiny
   mechanical commands. Give each subagent the metadata, exact paths, scope, current findings, and a
   required output schema. Completion: every subagent returns a flag candidate, evidence, or a useful
   negative result, and the parent verifies important claims.

7. **Verify and submit.** Never report placeholder flags like `CTF{flag}`. Prefer platform submission
   over eyeballing. Deduplicate exact flag attempts and slow down after wrong submissions. Completion:
   the platform returns `CORRECT` or `ALREADY SOLVED`, or dry-run evidence is strong enough to label
   the result unsubmitted.

8. **Stop or bump.** When a solver loops, stop repeating the same command. Inject sibling findings and
   require a different approach. Completion: either a confirmed flag is found, or the final note lists
   all explored surfaces and why the challenge remains unsolved.

## Delegation Pattern

Use one parent coordinator and focused workers. A good batch is 3 to 5 workers:

```text
Worker A: service interaction and protocol behavior
Worker B: file/binary/reverse analysis
Worker C: crypto/encoding/format analysis
Worker D: web/forensics/stego angle when relevant
Worker E: independent sanity-check of findings and flag candidates
```

Pass this output contract to each worker:

```json
{
  "status": "flag_found | promising | blocked | exhausted",
  "flag_candidate": "",
  "evidence": ["commands run", "observations", "why candidate is real"],
  "new_findings": ["facts the parent should add to findings.md"],
  "dead_ends": ["approaches not worth repeating"],
  "next_best_step": ""
}
```

The parent owns submission. Subagent reports are self-reports; verify candidate flags, URLs, offsets,
and exploit claims before telling the user.

## CTFd Mode

If the user gives a CTFd URL and token, prefer the existing `ctf-agent` runner when available:

```bash
cd /path/to/ctf-agent
uv sync
docker build -f sandbox/Dockerfile.sandbox -t ctf-sandbox .
uv run ctf-solve --ctfd-url "$CTFD_URL" --ctfd-token "$CTFD_TOKEN" --challenges-dir challenges -v
```

For a single challenge:

```bash
uv run ctf-solve --challenge challenges/<challenge-slug> --no-submit -v
```

If using native Hermes instead, download challenge details and files into the workspace, then follow
the Operating Loop. Keep tokens out of chat history; put credentials in environment variables or the
operator's existing secret store.

Load `references/ctfd-workflow.md` for CTFd API and submission discipline.

## Common Pitfalls

1. **Exploring files before connecting to a provided service.** Many challenge flags live behind the
   remote service. Capture the service behavior first.

2. **Reading binary files with text tools.** Use `file`, `xxd`, `strings`, `binwalk`, `readelf`,
   `objdump`, `r2`, `gdb`, or pyghidra instead.

3. **Repeating identical commands.** After three identical attempts, write what you learned and switch
   tools or hypotheses. After five, force a new angle.

4. **Trusting a candidate flag without submission.** A plausible string is not a solve until CTFd
   accepts it, unless the user explicitly requested dry-run.

5. **Letting subagents diverge.** Re-broadcast important findings by appending them to `findings.md`
   and passing a fresh excerpt to later workers.

6. **Over-delegating browser work.** Browser-heavy subagents are slow. Keep browser interaction in the
   parent unless there are genuinely independent web surfaces.

7. **Skipping low-solve hints.** Points, solves, tags, and hints often encode intended difficulty and
   technique. Record them before deep work.

## Verification Checklist

- [ ] Target is a CTF/lab or explicitly authorized.
- [ ] Workspace has metadata, distfiles, workspace, findings, and traces.
- [ ] Service connection was tested first when `connection_info` exists.
- [ ] File types and category-specific triage are recorded.
- [ ] Every delegated worker got the current findings and returned structured output.
- [ ] Candidate flags were deduplicated and submitted or clearly marked dry-run.
- [ ] Final answer includes confirmed flag or a concise unsolved status with next steps.
