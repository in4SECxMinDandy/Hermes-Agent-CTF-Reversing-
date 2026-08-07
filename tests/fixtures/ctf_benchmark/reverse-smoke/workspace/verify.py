from pathlib import Path

case = Path(__file__).resolve().parents[1]
encoded = bytes.fromhex((case / "distfiles" / "encoded.hex").read_text(encoding="utf-8").strip())
decoded = bytes(value ^ 0x23 for value in encoded)
assert decoded == b"REVERSE_OK"
print("reverse-smoke: PASS")
