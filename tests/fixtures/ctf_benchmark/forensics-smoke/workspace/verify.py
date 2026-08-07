from pathlib import Path


capture = Path("../distfiles/capture.txt").read_text(encoding="utf-8")
assert "flag{forensics_trace}" in capture
print("forensics evidence recovered")
