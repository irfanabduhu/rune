#!/usr/bin/env python3
"""Renumber **[n]** unit markers in a chapter file sequentially from 1.

Usage: python3 renumber.py <chapter.md> [more.md ...]

Preserves each marker's ⟨صN⟩ page tag and any trailing title text. Run after
assembling parallel subagent parts so numbering is continuous within a chapter.
"""
import sys, re

MARK = re.compile(r"^\*\*\[\d+\]\*\*(.*)$")


def renumber(path):
    out, n = [], 0
    for line in open(path, encoding="utf-8"):
        m = MARK.match(line.rstrip("\n"))
        if m:
            n += 1
            out.append(f"**[{n}]**{m.group(1)}\n")
        else:
            out.append(line)
    with open(path, "w", encoding="utf-8") as fh:
        fh.writelines(out)
    return n


def main():
    if len(sys.argv) < 2:
        print("usage: renumber.py <chapter.md> ...", file=sys.stderr)
        sys.exit(2)
    for p in sys.argv[1:]:
        print(f"{p}: {renumber(p)} units")


if __name__ == "__main__":
    main()
