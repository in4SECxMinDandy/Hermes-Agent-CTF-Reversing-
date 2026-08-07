---
name: llm4decompile
description: Use for authorized reverse-engineering work when an ELF or Linux x86_64 function needs AI-assisted decompilation from assembly or Ghidra pseudocode. Select LLM4Decompile-End for direct assembly-to-C recovery or LLM4Decompile-Ref for refining Ghidra output, and use Docker/GPU when the local model runtime is available.
---

# LLM4Decompile

## Overview

Use LLM4Decompile as an evidence-producing assistant, not as a replacement for
disassembly, Ghidra, or dynamic validation. The upstream models primarily target
Linux x86_64 binaries compiled by GCC at O0-O3; APK, ARM, Windows PE, heavily
obfuscated, and whole-program recovery tasks need a different first tool.

## Safety And Scope

- Work only on binaries the user is authorized to inspect.
- Preserve the original sample and record its hash before analysis.
- Treat generated C as a hypothesis. It may omit compiler artifacts, misread
  calling conventions, or invent names and types.
- Do not upload samples or source-derived assembly to a remote model without
  explicit user approval. Prefer local inference for private CTF and forensic
  material.
- Do not blindly compile, patch, or execute generated code. Use an isolated
  copy and the CTF Docker backend for validation.
- Do not assume the Hermes `ctf-sandbox` image contains the model, Ghidra, CUDA,
  or the LLM4Decompile repository. Check the runtime before invoking it.

## Choose A Mode

- `LLM4Decompile-End`: normalize a single function's assembly into the
  repository's expected prompt format, then generate C directly. Use when
  Ghidra output is unavailable or a second independent hypothesis is useful.
- `LLM4Decompile-Ref`: obtain a function-level Ghidra decompilation first, then
  ask the model to improve readability and recover likely semantics. Prefer
  this for normal stripped ELF analysis because the decompiler supplies more
  structure than raw assembly.
- `SK2Decompile`: use only when the separate two-phase checkpoints and their
  runtime are explicitly available. Do not silently substitute it for the
  documented End or Ref workflow.

## Workflow

1. Identify the sample type, architecture, endianness, compiler clues, and
   hash. Keep a working copy separate from the original.
2. Map the binary with deterministic tools. For ELF, use `file`, `readelf`,
   `objdump`, and Ghidra headless analysis. Locate the exact function and
   retain its address, symbol state, and callers/callees.
3. Choose End or Ref. Give the model one function at a time when possible;
   include calling-convention clues and relevant data references, but avoid
   dumping an entire binary into the context.
4. Run inference in the configured local container or model environment. If
   the GPU, model weights, or required runtime is missing, report that fact and
   continue with deterministic reversing rather than fabricating model output.
5. Cross-check every material claim against assembly, xrefs, constants,
   memory access widths, return values, and side effects. For a proposed
   algorithm, compile a clean reconstruction and compare behavior only in an
   isolated authorized environment.
6. Record facts, model hypotheses, rejected interpretations, model/checkpoint,
   runtime, and validation results in `reports/reverse/<case-id>.md`.

## Runtime Rules

- The upstream quick start uses Python 3.9 and a local Hugging Face model.
- The upstream Docker path uses a CUDA-enabled PyTorch image, Java 17, Ghidra,
  and Transformers. This is a separate image from `ctf-sandbox:latest` unless
  those dependencies have been deliberately added and tested there.
- Prefer a dedicated image or service for inference so ordinary CTF commands
  remain fast and the main sandbox stays reproducible.
- Start with a model that fits available VRAM. Larger checkpoints increase
  latency and memory use; published re-executability is a benchmark signal,
  not proof that the output is correct for the current binary.
- Do not add model weights, Hugging Face tokens, or user API keys to the Hermes
  repo, skill directory, prompt, or reports.

Read [references/llm4decompile-upstream.md](references/llm4decompile-upstream.md)
when setting up the model, selecting a checkpoint, or troubleshooting Ghidra,
CUDA, or licensing.
