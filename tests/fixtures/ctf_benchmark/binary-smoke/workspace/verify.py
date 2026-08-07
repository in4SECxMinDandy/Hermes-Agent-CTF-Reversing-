from pathlib import Path


header = bytes.fromhex(Path("../distfiles/elf-header.hex").read_text(encoding="utf-8").strip())
assert header.startswith(b"\x7fELF")
assert header[4] == 2
print("64-bit ELF triage confirmed")
