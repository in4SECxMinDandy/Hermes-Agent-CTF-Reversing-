from pathlib import Path

case = Path(__file__).resolve().parents[1]
values = dict(
    line.strip().split("=", 1)
    for line in (case / "distfiles" / "parameters.txt").read_text(encoding="utf-8").splitlines()
)
assert (int(values["a"]) * int(values["d"])) % int(values["m"]) == 1
print("crypto-smoke: PASS")
