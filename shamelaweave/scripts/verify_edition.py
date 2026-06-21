#!/usr/bin/env python3
"""Check a shamelaweave book folder conforms to the logical-paragraph format.

Usage: python3 verify_edition.py <book_dir>

Fails (exit 1) if any chapter file has '## ص' page-divider headers, units that
are not numbered 1..N contiguously, or a unit missing its ⟨صN⟩ page tag.
"""
import sys, os, re, glob

UNIT = re.compile(r"^\*\*\[(\d+)\]\*\*\s*(⟨\s*ص\s*[^⟩]+⟩)?")


def check_file(path):
    errs, nums, lineno = [], [], 0
    base = os.path.basename(path)
    for raw in open(path, encoding="utf-8"):
        lineno += 1
        line = raw.rstrip("\n")
        if re.match(r"^##\s*ص", line):
            errs.append(f"{base}:{lineno}: page-divider header '{line.strip()}'")
        m = UNIT.match(line)
        if m:
            nums.append(int(m.group(1)))
            if not m.group(2):
                errs.append(f"{base}:{lineno}: unit [{m.group(1)}] missing ⟨ص…⟩ page tag")
    expected = list(range(1, len(nums) + 1))
    if nums != expected:
        errs.append(f"{base}: units not contiguous 1..{len(nums)} (got {nums[:6]}…)")
    return errs, len(nums)


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
