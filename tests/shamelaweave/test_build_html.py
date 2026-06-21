#!/usr/bin/env python3
"""Render-level checks for the trilingual, number-free shamelaweave build_html.py."""
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

⟨ص11⟩

> النَّصُّ الْعَرَبِيُّ الْأَوَّلُ

The first English paragraph.

প্রথম বাংলা অনুচ্ছেদ।

*Notes:* a clarifying note.

⟨ص11–12⟩

> النَّصُّ الَّذِي يَمْتَدُّ عَبْرَ الصَّفْحَتَيْنِ

A paragraph the print edition split across the page turn, now joined into one.

মুদ্রিত সংস্করণে যে অনুচ্ছেদ পৃষ্ঠার মোড়ে ভাগ হয়ে গিয়েছিল, এখন একত্র করা হয়েছে।
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
        "no unit-number markers": 'class="num"' not in html,
        "margin page tag present": 'class="pg-tag"' in html,
        "page 11 tag rendered": "ص11" in html,
        "spanning range tag rendered": "ص11–12" in html,
        "unit 1 anchor id": 'id="01-test--u1"' in html,
        "unit 2 anchor id": 'id="01-test--u2"' in html,
        "english paragraph rendered": 'class="u-en"' in html and "first English paragraph" in html,
        "bengali paragraph rendered": 'class="u-bn"' in html and "প্রথম বাংলা" in html,
        "bengali view button": 'data-view="bn"' in html,
        "page index has two chips": html.count('class="pg"') == 2,
    }
    bad = [k for k, ok in checks.items() if not ok]
    if bad:
        print("FAIL:", bad); sys.exit(1)
    print("OK: build_html trilingual format"); sys.exit(0)

main()
