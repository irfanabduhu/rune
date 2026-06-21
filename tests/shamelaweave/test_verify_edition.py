#!/usr/bin/env python3
"""Checks for verify_edition.py: a good edition passes, a malformed one fails."""
import subprocess, sys, tempfile, pathlib

REPO = pathlib.Path(__file__).resolve().parents[2]
VERIFY = REPO / "shamelaweave" / "scripts" / "verify_edition.py"

GOOD = """# Good — [باب]

**[1]** ⟨ص11⟩

> نَصٌّ

Text one.

**[2]** ⟨ص11–12⟩

> نَصٌّ آخَرُ

Text two.
"""

# bad: a leftover page-divider header, a missing tag, and non-contiguous numbering
BAD = """# Bad — [باب]

## ص11 — [باب]

**[1]** ⟨ص11⟩

> نَصٌّ

Text one.

**[3]**

> نَصٌّ آخَرُ

Text two.
"""

def run(content):
    with tempfile.TemporaryDirectory() as d:
        (pathlib.Path(d) / "01-x.md").write_text(content, encoding="utf-8")
        return subprocess.run([sys.executable, str(VERIFY), d],
                              capture_output=True, text=True)

def main():
    good = run(GOOD)
    bad = run(BAD)
    checks = {
        "good edition exits 0": good.returncode == 0,
        "bad edition exits 1": bad.returncode == 1,
        "bad flags page-divider": "ص" in bad.stderr and "divider" in bad.stderr.lower(),
        "bad flags missing tag": "page tag" in bad.stderr.lower(),
        "bad flags numbering": "contiguous" in bad.stderr.lower(),
    }
    miss = [k for k, ok in checks.items() if not ok]
    if miss:
        print("FAIL:", miss)
        print("--- good stderr ---\n", good.stderr)
        print("--- bad stderr ---\n", bad.stderr)
        sys.exit(1)
    print("OK: verify_edition"); sys.exit(0)

main()
