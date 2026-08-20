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
  - code_execution
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

The category playbooks explicitly cover the five competition domains: Web Exploitation, Cryptography,
Reverse Engineering, Digital Forensics, and Binary Exploitation.

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

The Android-specific runtime is provided by sandbox/apk-triage.py and the APK playbook. It records
missing tools and failed stages in the report so a solver can choose a fallback instead of assuming
that a successful command was available.

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
`workspace/casebook.events.jsonl` is the append-only source of truth for evidence, sandbox outcomes,
and approval audit events. `workspace/casebook.json` is its compact projection for hypotheses,
evidence, dead ends, next steps, and artifact paths. It lets a new agent turn or focused worker
resume without replaying long tool output.

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

5. **Create a brief before deep work or delegation.** Run `hermes ctf case brief <challenge-dir>` and
use its bounded output as worker context. Record each verified fact with `hermes ctf case record`
instead of relying on chat history alone. Completion: the casebook names active hypotheses, dead ends,
and a concrete next step.

6. **Choose playbooks.** Load `references/category-playbooks.md` for category-specific commands and
   decision trees. Load `references/sandbox-toolbox.md` when deciding which tool to try next.
   Completion: each active hypothesis has a next command or proof probe.

7. **Batch deterministic probes.** When several independent terminal or file probes are needed, use
`execute_code` to call the existing tools programmatically, write durable output below `workspace/`,
and print only a compact JSON or Markdown summary. Do not use it for speculative high-risk actions or
to hide commands from the operator. Completion: one model turn produces a bounded summary and an
artifact path that is recorded in the casebook.

8. **Delegate when parallelism helps.** Use `delegate_task` for independent angles, not for tiny
   mechanical commands. Give each subagent the metadata, exact paths, scope, current findings, and a
   required output schema. Completion: every subagent returns a flag candidate, evidence, or a useful
   negative result, and the parent verifies important claims.

9. **Verify and submit.** Never report placeholder flags like `CTF{flag}`. Prefer platform submission
   over eyeballing. Deduplicate exact flag attempts and slow down after wrong submissions. Completion:
   the platform returns `CORRECT` or `ALREADY SOLVED`, or dry-run evidence is strong enough to label
   the result unsubmitted.

   When the operator has enabled `ctf.auto_submit: true`, submit each verified candidate through
   `hermes ctf submit` immediately; otherwise use `--yes` only after the operator explicitly asks
   for a live submission. Never attempt privilege elevation to solve a challenge. If Docker, WSL,
   `sudo`, or UAC reports that administrator permission is required, stop and tell the operator what
   requires it; wait for their approval before retrying.

10. **Stop or bump.** When a solver loops, stop repeating the same command. Inject sibling findings and
   require a different approach. Completion: either a confirmed flag is found, or the final note lists
   all explored surfaces and why the challenge remains unsolved.

## Automated Practical Readiness

Use the normalized workspace as the durable boundary between discovery, analysis, and verification.
Run category triage before delegating deeper analysis; it stores command output under
`workspace/triage/` and appends a pointer to `findings.md`:

```bash
hermes ctf triage ~/ctf-challenges/<challenge-slug> --engine auto --network none --json
```

The triage engine uses Docker automatically when available and keeps `distfiles/` read-only. Network
access is disabled by default; use `--network host --yes` only for an explicitly authorized challenge
service. Results expose a stable status (`succeeded`, `command_failed`, `timed_out`, or
`runner_failed`) and the report records whether sandbox enforcement was full or partial.

Measure operational readiness with a representative local corpus. Each case must provide all five
workspace artefacts and a trusted `workspace/verify.py`; `--execute` runs each verifier repeatedly and
checks success, stable output, category coverage, and evidence completeness:

```bash
hermes ctf benchmark --root ~/ctf-benchmark --repeats 2 --execute \
  --report ~/ctf-benchmark-report.json --json
```

The practical score is out of 10: category coverage (3), verifier success (3), reproducibility (2),
and evidence completeness (2). This is a workflow-readiness signal, not a claim that every arbitrary
challenge can be solved automatically. Keep real challenge corpora private and never place flags or
tokens in source-controlled fixtures.

For durable parallel work, create workers on the existing Kanban board. The command creates parallel
specialists followed by a dependency-gated verifier and synthesizer:

```bash
hermes ctf swarm <challenge-dir> \
  --worker reverse-worker:"Recover the check" \
  --worker protocol-worker:"Map service behavior" \
  --verifier ctf-verifier --synthesizer ctf-synthesizer
```

## APK Reversing Mode

For an APK challenge, keep the original package under distfiles/ and write all decoded, patched, and
runtime artifacts under workspace/apk/. Run the deterministic wrapper first:

    apk-triage --apk /challenge/distfiles/app.apk --out /challenge/workspace/apk

Read workspace/apk/apk-report.json before opening large decompiler outputs. The report records
package metadata, DEX count, native library ABIs, signer verification, packer detection, and the
status/output of every optional tool. Use references/apk-reversing-playbook.md for the next branch:

- Static: apkid, aapt/aapt2, apksigner, jadx, apktool, and Androguard.
- Native: extract lib/*/*.so, identify each ABI, then use readelf, r2, objdump, or angr.
- Runtime readiness: run `apk-runtime-check --out /challenge/workspace/apk/runtime --package
  com.example.app` and read runtime-report.json before making dynamic claims.
- Dynamic: use an external ADB-connected emulator/device, then Frida, Objection, or uiautomator2.
  Do not execute APK code in the static sandbox.
- Native-only: use a separate unidbg Java sidecar for ARM/JNI emulation when a full Android runtime
  is unavailable; preserve ABI/API-level and argument evidence.
- Network: use apk-mitm or android-unpinner for common pinning, and Frida runtime hooks when pinning
  is implemented in native code or static patching fails.

Dynamic execution is optional and must be explicitly available. A missing emulator is a blocked
runtime branch, not evidence that the APK is benign or fully understood.

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

Configure behavioral settings in `~/.hermes/config.yaml` and keep the API token in
`~/.hermes/.env`:

```yaml
ctf:
  url: https://ctfd.example.invalid
  workspace: ~/ctf-challenges
  agent_dir: ~/src/ctf-agent
  sandbox_image: ctf-sandbox
  max_challenges: 10
  # Opt in only for an authorized event where verified flags should be scored immediately.
  auto_submit: true
```

```text
CTFD_TOKEN=secret-api-token
```

The CLI checks authorization and local prerequisites before contacting CTFd:

```bash
hermes ctf doctor --network
hermes ctf assess --network --json
hermes ctf pull --unsolved-only
hermes ctf score --top 20
hermes ctf status --top 20 --json
```

For full live automation, `hermes ctf run` delegates to the existing `ctf-agent`
coordinator when that checkout is available. The coordinator polls CTFd, pulls new
challenges, starts parallel swarms in the Docker sandbox, verifies submissions, and
stops work after a solve. It defaults to dry-run submission; add `--submit` or enable
`ctf.auto_submit: true` only when the operator explicitly wants live scoring:

```bash
hermes ctf run --challenges-dir ~/ctf-challenges
hermes ctf run --challenges-dir ~/ctf-challenges --submit --coordinator claude
```

For a single challenge:

```bash
hermes ctf run --challenge ~/ctf-challenges/<challenge-slug>
```

If using native Hermes instead, download challenge details and files into the workspace, then follow
the Operating Loop. Keep tokens out of chat history; put credentials in environment variables or the
operator's existing secret store.

Load `references/ctfd-workflow.md` for CTFd API and submission discipline.

## Attack & Defense Mode

Use `templates/attack-defense.yml` as the starting contract. It requires `authorized: true`,
a non-empty target scope, named services, health checks, and explicit patch/attack/flag
commands. Validation is always available without execution:

```bash
hermes ctf ad doctor templates/attack-defense.yml
hermes ctf ad run templates/attack-defense.yml
```

Live commands are executed only after the operator opts in with `--live`; this creates one audited
approval for the live run, including any configured host-network tool. State and extracted flags are
persisted to the configured scoreboard JSON:

```bash
hermes ctf ad run templates/attack-defense.yml --live --watch --interval 30
hermes ctf ad status templates/attack-defense.yml
```

### Curated Attack Tools

Hermes also provides a small, shell-free subset of the larger hackingtool catalog for common
authorized recon and web-testing steps. Discover the current catalog with:

```bash
hermes ctf attack list
```

Attach tools to a service with `attack_tools`. The service `target` is injected by Hermes, so do not
put a second URL or host in tool arguments:

```yaml
services:
  - name: example-service
    target: 127.0.0.1:31337
    healthcheck: [python, -c, "print('healthy')"]
    attack_tools:
      - id: nmap
        args: ["-T3"]
        backend: auto
        timeout: 90
```

The curated set covers network and subdomain recon, HTTP probing, crawling, web discovery, TLS and
WAF fingerprinting, vulnerability discovery, and SQL injection testing. DDoS, phishing, wireless,
credential-capture, RAT/C2, payload-generation, and post-exploitation tools are intentionally not
included. `sqlmap` additionally requires `allow_high_risk: true` in the authorized config.

`backend: auto` prefers a locally installed executable, then WSL, then Docker. Hermes never runs
the upstream install commands automatically, never adds `--privileged`, and executes tool arguments
as an argv list rather than through a shell.

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
