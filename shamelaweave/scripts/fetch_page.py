#!/usr/bin/env python3
"""Fetch one page of a Maktabat al-Shamela book and return clean structured text.

Usage:
    python3 fetch_page.py <book_id> <page_no> [--raw]

Output: JSON on stdout:
    {
      "book_id": "7528",
      "url_page": 5,          # the /N in the URL
      "print_page": "11",     # printed page number (the "ص" shown on shamela), may be null
      "heading": "[الأدب الصغير]" | null,
      "body": ["paragraph 1", "paragraph 2", ...],
      "footnotes": [{"marker": "١", "text": "وقَّت: حدد وقتًا."}, ...],
      "next_page": 6 | null   # url page id of the next page if one exists
    }

Notes:
- plain WebFetch is 403-blocked by shamela; a browser User-Agent is required.
- Text lives in <div class="nass">. <hr> separates body from footnotes (<p class="hamesh">).
- Inline footnote markers (Arabic-Indic digits attached to words) are left in the body
  text on purpose so the translator can line them up with the gloss list.
"""
import sys, json, re, html, urllib.request

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")


def fetch(book_id, page_no):
    url = f"https://shamela.ws/book/{book_id}/{page_no}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def strip_tags(s):
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s).strip()


def clean_inline(p):
    # drop anchor spans and the per-paragraph copy button, keep the real text
    p = re.sub(r'<span class="anchor"[^>]*></span>', "", p)
    p = re.sub(r'<a href="#p\d+"[^>]*>.*?</a>', "", p, flags=re.S)
    return p


def parse(htmltext, url_page):
    m = re.search(r'<div class="nass[^"]*"([^>]*)>(.*?)<div id="appended_pages"',
                  htmltext, re.S)
    if not m:
        return {"url_page": url_page, "print_page": None, "heading": None,
                "body": [], "footnotes": [], "next_page": None}
    attrs, block = m.group(1), m.group(2)
    pn = re.search(r'data-page-num="([^"]*)"', attrs)
    print_page = pn.group(1) if pn else None

    # split body vs footnotes on the <hr>
    parts = re.split(r"<hr\s*/?>", block, maxsplit=1)
    body_html = parts[0]
    foot_html = parts[1] if len(parts) > 1 else ""

    heading = None
    body = []
    for pm in re.findall(r"<p\b[^>]*>(.*?)</p>", body_html, re.S):
        pm = clean_inline(pm)
        hm = re.search(r'<span class="c4">(.*?)</span>', pm, re.S)
        if hm and heading is None:
            heading = strip_tags(hm.group(1))
            # a heading-only paragraph contributes no body text
            rest = strip_tags(re.sub(r'<span class="c4">.*?</span>', "", pm, flags=re.S))
            if rest:
                body.append(rest)
            continue
        txt = strip_tags(pm)
        if txt:
            body.append(txt)

    footnotes = []
    fm = re.search(r'<p class="hamesh"[^>]*>(.*?)</p>', foot_html, re.S)
    if fm:
        for line in re.split(r"<br\s*/?>", fm.group(1)):
            line = strip_tags(line)
            if not line:
                continue
            mm = re.match(r"^([٠-٩\d]+)\s*(.*)$", line)
            if mm:
                footnotes.append({"marker": mm.group(1), "text": mm.group(2).strip()})
            else:
                footnotes.append({"marker": None, "text": line})

    has_next = ('id="load_next_wrap"' in htmltext) or (f'/{url_page + 1}"' in htmltext)
    next_page = url_page + 1 if has_next else None

    return {"url_page": url_page, "print_page": print_page, "heading": heading,
            "body": body, "footnotes": footnotes, "next_page": next_page}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        print("usage: fetch_page.py <book_id> <page_no> [--raw]", file=sys.stderr)
        sys.exit(2)
    book_id, page_no = args[0], int(args[1])
    htmltext = fetch(book_id, page_no)
    if "--raw" in sys.argv:
        sys.stdout.write(htmltext)
        return
    out = parse(htmltext, page_no)
    out["book_id"] = book_id
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
