# LLM4Decompile Reference

Upstream repository: https://github.com/albertan017/LLM4Decompile

## What It Supports

The upstream README describes Linux x86_64 binaries, primarily GCC O0-O3.
`LLM4Decompile-End` translates normalized assembly directly into C. The V2
`LLM4Decompile-Ref` models refine Ghidra pseudocode. The repository also lists
the newer SK2Decompile two-phase checkpoints, but that path has separate model
and runtime requirements.

Do not present this as general-purpose decompilation. Windows PE, ARM/Thumb,
Dalvik/ART, MIPS, firmware, packed code, and optimized or obfuscated programs
may require architecture-specific tools and manual analysis first.

## Checkpoints And Benchmarks

The repository lists these approximate re-executability benchmark results:

- `llm4decompile-1.3b-v1.5`: 27.3%
- `llm4decompile-6.7b-v1.5`: 45.4%
- `llm4decompile-1.3b-v2`: 46.0%
- `llm4decompile-6.7b-v2`: 52.7%
- `llm4decompile-9b-v2`: 64.9%
- `llm4decompile-22b-v2`: 63.6%

These are benchmark measurements, not a success rate for a CTF sample. Use a
smaller checkpoint for a quick hypothesis and a larger one only when the GPU
and latency budget justify it.

## Upstream Runtime

The quick start requests Python 3.9 and installs the repository requirements.
The current requirements include `vllm==0.4.0` and `numpy==1.23.3`; avoid
mixing them into Hermes' main `.venv`, especially on Windows. Use a dedicated
Linux or Docker environment.

The upstream Dockerfile is CUDA-oriented and includes PyTorch, Ghidra,
OpenJDK 17, and Transformers. It is a model-analysis environment, not the
existing Hermes `ctf-sandbox:latest` image. Before using it, confirm:

1. Docker can expose the NVIDIA GPU (`--gpus all` and a working NVIDIA
   Container Toolkit setup).
2. The selected checkpoint fits available VRAM and disk space.
3. Ghidra headless can analyze the sample and emit pseudocode when using Ref.
4. The model files are downloaded from the intended Hugging Face repository.

If no GPU is available, do not claim that local LLM4Decompile is active. Use
Ghidra, objdump, rizin/radare2, and the normal Hermes model for reasoning, or
run a deliberately approved remote inference service without uploading
sensitive binaries.

## Input Normalization

For End, extract one function and normalize it to the upstream shape:

```text
# This is the assembly code:
<function_name>:
    instruction
    instruction
# What is the source code?
```

Remove raw opcode bytes and comments where they would distract the model, but
retain labels, calls, memory operands, stack offsets, and relevant constants.
For Ref, preserve the Ghidra function signature, local variables, control-flow
structure, and warnings. Keep the original output beside the normalized input.

## Verification

Review the generated C against:

- argument registers and return register;
- signed versus unsigned comparisons and integer widths;
- stack layout, pointer arithmetic, and bounds checks;
- calls, global accesses, constants, and error paths;
- loops, switch/jump-table behavior, and side effects.

Compile only an isolated reconstruction when it is safe and useful. Compare
observable behavior on authorized test inputs; never treat a successful compile
as proof of semantic equivalence.

## License Notes

The repository code is presented as MIT, while the model is covered by the
DeepSeek license and its use restrictions. Keep code and model terms separate.
Do not vendor model weights into Hermes or redistribute them through the skill.
Review the current upstream LICENSE and LICENSE-MODEL before distributing a
container or exposing the model as a service.
