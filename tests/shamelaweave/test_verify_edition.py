#!/usr/bin/env python3
"""Checks for verify_edition.py: a good trilingual edition passes, a malformed one fails."""
import subprocess, sys, tempfile, pathlib

REPO = pathlib.Path(__file__).resolve().parents[2]
VERIFY = REPO / "shamelaweave" / "scripts" / "verify_edition.py"

GOOD = """# Good — [باب]

⟨ص11⟩

> نَصٌّ عَرَبِيٌّ

English text one.

বাংলা পাঠ এক।

⟨ص11–12⟩

> نَصٌّ آخَرُ

English text two.

বাংলা পাঠ দুই।
"""

# bad: a leftover page-divider header, an ASCII-hyphen range, and a unit missing Bengali
BAD = """# Bad — [باب]

## ص11 — [باب]

⟨ص11⟩

> نَصٌّ عَرَبِيٌّ

English text one.

বাংলা পাঠ এক।

⟨ص12-13⟩

> نَصٌّ آخَرُ

English text two only, no Bengali.
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
        "bad flags page-divider": "divider" in bad.stderr.lower(),
        "bad flags ascii hyphen": "hyphen" in bad.stderr.lower(),
        "bad flags missing bengali": "missing bengali" in bad.stderr.lower(),
    }
    miss = [k for k, ok in checks.items() if not ok]
    if miss:
        print("FAIL:", miss)
        print("--- good stderr ---\n", good.stderr)
        print("--- bad stderr ---\n", bad.stderr)
        sys.exit(1)
    print("OK: verify_edition"); sys.exit(0)

main()
