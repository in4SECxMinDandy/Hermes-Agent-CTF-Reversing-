# Sandbox Toolbox

The `ctf-agent` sandbox image installs a broad CTF toolset. Use this reference to pick tools or to
verify a replacement environment has enough coverage.

## Core Layout

Inside the sandbox:

```text
/challenge/metadata.yml
/challenge/distfiles/     read-only inputs
/challenge/workspace/     writable generated files
/tools.txt                installed tool reference
```

If a service says `localhost` or `127.0.0.1` from the host perspective, containers usually need
`host.docker.internal`.

## Tool Map

| Area | Tools |
|---|---|
| Networking | `nc`, `curl`, `wget`, `nmap`, Python `requests` |
| Binary triage | `file`, `xxd`, `strings`, `readelf`, `objdump`, `binwalk` |
| Debug and trace | `gdb`, `strace`, `ltrace` |
| Reverse engineering | `radare2`, `pyghidra`, `angr`, `capstone`, `unicorn` |
| Pwn | `pwntools`, `ROPgadget`, `gcc`, `g++`, `make`, `cmake` |
| Crypto/math | SageMath, `RsaCtfTool`, `z3`, `gmpy2`, `pycryptodome`, `cado-nfs`, `fpylll`, `flatter` |
| Forensics | `volatility3`, Sleuthkit (`mmls`, `fls`, `icat`), `foremost`, `dcfldd`, `testdisk` |
| Stego/images | `exiftool`, `steghide`, `stegseek`, `zsteg`, `pngcheck`, ImageMagick, Pillow |
| OCR/media | `tesseract`, `ffmpeg`, `sox`, `pytesseract` |
| Containers | `podman`, `buildah` when nested challenge containers are needed |
| ML/numeric | `numpy`, `scipy`, CPU PyTorch, Keras |

## Docker Run Pattern

If reusing the `ctf-sandbox` image outside `ctf-agent`, mount the challenge explicitly:

```bash
docker run --rm -it \
  --add-host host.docker.internal:host-gateway \
  --cap-add SYS_PTRACE \
  --security-opt seccomp=unconfined \
  -v "$PWD/distfiles:/challenge/distfiles:ro" \
  -v "$PWD/workspace:/challenge/workspace:rw" \
  -v "$PWD/metadata.yml:/challenge/metadata.yml:ro" \
  -w /challenge \
  ctf-sandbox bash
```

On Windows PowerShell, prefer absolute paths:

```powershell
docker run --rm -it `
  --add-host host.docker.internal:host-gateway `
  --cap-add SYS_PTRACE `
  --security-opt seccomp=unconfined `
  -v "${PWD}\distfiles:/challenge/distfiles:ro" `
  -v "${PWD}\workspace:/challenge/workspace:rw" `
  -v "${PWD}\metadata.yml:/challenge/metadata.yml:ro" `
  -w /challenge `
  ctf-sandbox bash
```

## Output Hygiene

- Save large command outputs to files in `workspace/` and summarize the key lines in `findings.md`.
- For binary blobs, use command-line inspection instead of reading through text tools.
- Keep generated exploit scripts, extracted archives, and patched binaries out of `distfiles/`.
- Use timeouts for commands that may hang: `timeout 30 command ...`.
