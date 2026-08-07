# CTF Category Playbooks

Use these as starting points. Record commands and observations in `findings.md`.

## Universal Triage

For a normalized Hermes workspace, persist the fixed probes before selecting a deeper hypothesis:

```bash
hermes ctf triage ./challenge --engine auto --network none --json
```

Review `workspace/triage/*.json` and `findings.md`; a missing tool is evidence about the environment,
not evidence that the challenge path is exhausted.

```bash
pwd
find distfiles -maxdepth 2 -type f -print
file distfiles/* 2>/dev/null
sha256sum distfiles/* 2>/dev/null
strings -a distfiles/* 2>/dev/null | head -200
```

Check metadata, hints, tags, solve count, point value, and flag format. For archives, extract into
`workspace/extract/` and preserve originals.

## Web

Start with non-destructive mapping:

```bash
curl -i "$URL"
curl -i "$URL/robots.txt"
curl -i "$URL/sitemap.xml"
curl -i "$URL/.well-known/security.txt"
```

Inspect HTML, JS, cookies, headers, redirects, source maps, hidden endpoints, backup files, and API
routes. For forms, compare valid and invalid inputs. For auth, test default creds only when the CTF
context implies it. For SSRF/XSS callbacks, use an operator-controlled webhook or the platform's
intended callback sink; avoid real cloud metadata unless the challenge explicitly asks for it.

## Binary Exploitation (Pwn) and TCP Services

Capture protocol behavior first:

```bash
nc host port <<'EOF'
help
EOF
```

For stateful interaction, write a short script:

```python
from pwn import *

io = remote("host", 31337)
print(io.recvuntil(b">", timeout=3))
io.sendline(b"1")
print(io.recvall(timeout=3))
```

Binary triage:

```bash
file ./binary
checksec --file=./binary || true
strings -a ./binary | head -200
readelf -h ./binary
readelf -s ./binary | head
objdump -d ./binary | head -200
```

Use `gdb`, `pwntools`, `ROPgadget`, `angr`, and `strace/ltrace` as needed. Keep exploit scripts in
`workspace/`, not beside distfiles.

## Reverse Engineering

Start broad, then decompile:

```bash
file sample
strings -a sample | tee workspace/strings.txt
r2 -A -q -c 'afl; izz; q' sample
```

Pyghidra pattern:

```python
import pyghidra

with pyghidra.open_program("sample") as flat:
    program = flat.currentProgram
    listing = program.getListing()
    for fn in listing.getFunctions(True):
        print(fn.getName(), fn.getEntryPoint())
```

Look for flag checks, comparison constants, decoding routines, embedded resources, anti-debug logic,
custom VMs, and checksum loops. Reimplement check logic in Python when possible.

## Crypto

Identify primitives and misuse before brute force. Record all parameters.

Common checks:

- RSA: small `e`, shared primes, close primes, leaked `p/q/d`, Wiener's attack, common modulus,
  partial key exposure. Try `RsaCtfTool`.
- Lattice: small roots, knapsack, biased nonce, ECDSA nonce reuse. Try Sage/fpylll/flatter.
- Symmetric: nonce/IV reuse, ECB blocks, padding oracle, CTR keystream reuse, weak random seed.
- Encoding: base64/base32/hex, rot, xor, zlib/gzip, protobuf/msgpack/json, layered transforms.

Useful commands:

```bash
python3 - <<'PY'
from Crypto.Util.number import *
print(long_to_bytes(0))
PY

RsaCtfTool --publickey pub.pem --uncipherfile flag.enc
sage script.sage
```

## Digital Forensics and Steganography

Never rely on one tool. Inspect metadata, magic bytes, appended data, archives, and visual content.

```bash
file artifact
exiftool artifact
binwalk -e artifact
xxd artifact | head -80
strings -a artifact | head -200
foremost -i artifact -o workspace/foremost
```

Images:

```bash
pngcheck image.png
zsteg image.png
steghide info image.jpg
stegseek image.jpg /usr/share/wordlists/rockyou.txt
```

Filesystems and memory:

```bash
mmls disk.img
fls -r -m / disk.img > workspace/bodyfile.txt
vol -f memory.raw windows.info
```

Audio/video:

```bash
ffprobe media.wav
sox media.wav -n spectrogram -o workspace/spectrogram.png
ffmpeg -i video.mp4 -vf fps=1 workspace/frame-%04d.png
```

## Misc

Look for automation, parsing, game logic, constraints, OCR, QR/barcodes, hidden Unicode, weird
encodings, and protocol quirks. When output looks random, test compression, encryption, xor, image
data, and base conversions before assuming high entropy.
