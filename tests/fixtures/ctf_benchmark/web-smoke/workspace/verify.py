from pathlib import Path

case = Path(__file__).resolve().parents[1]
request = (case / "distfiles" / "request.txt").read_text(encoding="utf-8")
assert "GET /search" in request
assert "X-CTF-Workflow: web" in request
print("web-smoke: PASS")
