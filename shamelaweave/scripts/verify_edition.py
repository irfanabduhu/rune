#!/usr/bin/env python3
"""Check a shamelaweave book folder conforms to the trilingual format.

Usage: python3 verify_edition.py <book_dir>

Each unit starts with a ⟨صN⟩ page marker (the delimiter — there are no unit
numbers), then a voweled Arabic blockquote, an English paragraph, and a Bengali
paragraph (notes optional). Fails (exit 1) if any chapter has '## ص' page-divider
headers, a range tag using an ASCII hyphen instead of the en dash, or a unit
missing its Arabic, English, or Bengali.
"""
import sys, os, re, glob

PAGE = re.compile(r"^⟨\s*ص\s*([^⟩]+?)\s*⟩")
BENGALI = re.compile(r"[ঀ-৿]")


def check_file(path):
    errs, nunits = [], 0
    base = os.path.basename(path)
    cur = None          # (start_lineno, page, has_ar, has_en, has_bn)
    awaiting_ar = False

    def close(u):
        if not u:
            return
        ln, page, ar, en, bn = u
        if not ar:
            errs.append(f"{base}:{ln}: unit ⟨ص{page}⟩ missing Arabic")
        if not en:
            errs.append(f"{base}:{ln}: unit ⟨ص{page}⟩ missing English")
        if not bn:
            errs.append(f"{base}:{ln}: unit ⟨ص{page}⟩ missing Bengali")

    for lineno, raw in enumerate(open(path, encoding="utf-8"), 1):
        line = raw.rstrip("\n")
        if not line.strip():
            continue
        if re.match(r"^##\s*ص", line):
            errs.append(f"{base}:{lineno}: page-divider header '{line.strip()}'")
            continue
        m = PAGE.match(line)
        if m:
            close(cur)
            page = m.group(1).strip()
            if re.search(r"\d-\d", page):
                errs.append(f"{base}:{lineno}: range tag uses ASCII hyphen; use en dash – (U+2013)")
            cur = [lineno, page, False, False, False]
            nunits += 1
            awaiting_ar = True
            continue
        if line.startswith("> "):
            if cur and awaiting_ar:
                cur[2] = True; awaiting_ar = False
            continue
        if line.startswith("*Notes:*") or line.startswith(("# ", "## ")):
            continue
        if cur is not None:                       # a translation paragraph
            if BENGALI.search(line):
                cur[4] = True
            else:
                cur[3] = True
    close(cur)
    return errs, nunits


def main():
    if len(sys.argv) < 2:
        print("usage: verify_edition.py <book_dir>", file=sys.stderr)
        sys.exit(2)
    book = sys.argv[1].rstrip("/")
    files = sorted(f for f in glob.glob(os.path.join(book, "*.md"))
                   if re.match(r"\d+", os.path.basename(f)))
    all_errs, total = [], 0
    for f in files:
        errs, n = check_file(f)
        all_errs += errs
        total += n
        print(f"{os.path.basename(f)}: {n} units, {'OK' if not errs else str(len(errs)) + ' issue(s)'}")
    if all_errs:
        print("\n".join(all_errs), file=sys.stderr)
        print(f"FAIL: {len(all_errs)} issue(s)", file=sys.stderr)
        sys.exit(1)
    print(f"OK: {len(files)} chapters, {total} units conform")


if __name__ == "__main__":
    main()
