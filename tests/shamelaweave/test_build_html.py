#!/usr/bin/env python3
"""Render-level checks for the new shamelaweave build_html.py."""
import subprocess, sys, tempfile, pathlib

REPO = pathlib.Path(__file__).resolve().parents[2]
BUILD = REPO / "shamelaweave" / "scripts" / "build_html.py"

README = """# كتاب الاختبار
### *Test Book*
**Author:** فلان الفلاني
**Source:** <https://shamela.ws/book/9999>
"""

CHAPTER = """# Test Chapter — [باب الاختبار]

> *Source: <https://shamela.ws/book/9999/11> — pages 11–12.*

**[1]** ⟨ص11⟩

> النَّصُّ الْعَرَبِيُّ الْأَوَّلُ

The first English paragraph.

*Notes:* a clarifying note.

**[2]** ⟨ص11–12⟩

> النَّصُّ الَّذِي يَمْتَدُّ عَبْرَ الصَّفْحَتَيْنِ

A paragraph the print edition split across the page turn, now joined into one.
"""

def main():
    with tempfile.TemporaryDirectory() as d:
        dd = pathlib.Path(d)
        (dd / "README.md").write_text(README, encoding="utf-8")
        (dd / "01-test.md").write_text(CHAPTER, encoding="utf-8")
        r = subprocess.run([sys.executable, str(BUILD), str(dd)],
                           capture_output=True, text=True)
        assert r.returncode == 0, f"build failed: {r.stderr}"
        html = (dd / "index.html").read_text(encoding="utf-8")

    checks = {
        "no page-divider sections": 'class="sec"' not in html,
        "margin page tag class present": 'class="pg-tag"' in html,
        "page 11 tag rendered": "ص11" in html,
        "spanning range tag rendered": "ص11–12" in html,
        "unit 1 anchor id": 'id="01-test--u1"' in html,
        "unit 2 anchor id": 'id="01-test--u2"' in html,
        "continuous number 1": '<span class="num">1</span>' in html,
        "continuous number 2": '<span class="num">2</span>' in html,
        "page index has two chips": html.count('class="pg"') == 2,
    }
    bad = [k for k, ok in checks.items() if not ok]
    if bad:
        print("FAIL:", bad); sys.exit(1)
    print("OK: build_html new format"); sys.exit(0)

main()
