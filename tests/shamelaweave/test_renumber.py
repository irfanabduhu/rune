#!/usr/bin/env python3
"""renumber.py renumbers markers 1..N and preserves their page tags."""
import subprocess, sys, tempfile, pathlib

REPO = pathlib.Path(__file__).resolve().parents[2]
RENUM = REPO / "shamelaweave" / "scripts" / "renumber.py"

INPUT = """# Chapter

**[3]** ⟨ص11⟩

> أ

A.

**[9]** ⟨ص11–12⟩

> ب

B.

**[2]** ⟨ص13⟩

> ج

C.
"""

def main():
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "01-x.md"
        p.write_text(INPUT, encoding="utf-8")
        r = subprocess.run([sys.executable, str(RENUM), str(p)],
                           capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        out = p.read_text(encoding="utf-8")
    checks = {
        "first is 1 with its tag": "**[1]** ⟨ص11⟩" in out,
        "second is 2 with range tag": "**[2]** ⟨ص11–12⟩" in out,
        "third is 3 with its tag": "**[3]** ⟨ص13⟩" in out,
        "old numbers gone": "**[9]**" not in out and "**[0]**" not in out,
        "body preserved": "> أ" in out and "> ب" in out and "> ج" in out,
    }
    bad = [k for k, ok in checks.items() if not ok]
    if bad:
        print("FAIL:", bad); print(out); sys.exit(1)
    print("OK: renumber"); sys.exit(0)

main()
