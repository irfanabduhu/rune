#!/usr/bin/env python3
"""Fetch a Maktabat al-Shamela book's metadata and table of contents.

Usage:
    python3 book_meta.py <book_id>

Output: JSON on stdout:
    {
      "book_id": "7528",
      "title": "كتاب الأدب الصغير والأدب الكبير",
      "author": "ابن المقفع",
      "url": "https://shamela.ws/book/7528",
      "toc": [{"page": 1, "title": "مقدمة"}, {"page": 5, "title": "الأدب الصغير"}, ...]
    }

The TOC pages are URL page indices (the /N in shamela URLs), not printed page numbers.
A chapter spans [toc[i].page, toc[i+1].page); the last chapter runs to the book's end.
"""
import sys, json, re, html, urllib.request

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def main():
    if len(sys.argv) < 2:
        print("usage: book_meta.py <book_id>", file=sys.stderr)
        sys.exit(2)
    book_id = sys.argv[1]
    url = f"https://shamela.ws/book/{book_id}"
    raw = fetch(url)

    tm = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    title = html.unescape(re.sub(r"<[^>]+>", "", tm.group(1)).strip()) if tm else None

    am = re.search(r'/author/\d+">([^<]+)</a>', raw)
    author = html.unescape(am.group(1).strip()) if am else None

    toc = []
    idx = re.search(r'<div class="betaka-index">(.*?)</div>', raw, re.S)
    scope = idx.group(1) if idx else raw
    for pg, ttl in re.findall(
            r'href="(?:https://shamela\.ws)?/book/%s/(\d+)(?:#p\d+)?"[^>]*>([^<]+)</a>' % book_id,
            scope):
        ttl = html.unescape(ttl).strip()
        if ttl:
            toc.append({"page": int(pg), "title": ttl})

    print(json.dumps({"book_id": book_id, "title": title, "author": author,
                      "url": url, "toc": toc}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
