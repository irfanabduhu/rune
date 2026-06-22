#!/usr/bin/env python3
"""Render a shamelaweave book folder into one self-contained HTML file.

Usage:
    python3 build_html.py <book_dir> [output.html]

Reads README.md (title/author/source) and every NN-*.md chapter file in the folder,
parses the shamelaweave markdown shape (## optional subheading / ⟨صP⟩ page marker /
> Arabic / English / Bengali / *Notes:*), and writes a single offline HTML file with:
  - light/dark theme (system default + manual toggle, persisted)
  - RTL Arabic naskh typography, English + Bengali serif bodies, rubricated markers
  - print-page numbers floated in the margin (hidden on narrow screens)
  - a view switch (All / العربية / English / বাংলা) and a contents drawer with a page index

Units are delimited by their ⟨صP⟩ page marker; there are no unit numbers. English and
Bengali are routed by script, so their order in the source is not load-bearing.

No external assets, no dependencies — everything is inlined so the file works offline.
"""
import sys, os, re, glob, html


# ---------- markdown parsing (specialised to the shamelaweave format) ----------

BENGALI = re.compile(r"[ঀ-৿]")
# unit marker:  ⟨ص11⟩  or  ⟨ص11–12⟩  optionally followed by an Arabic title
PAGE_RE = re.compile(r"^⟨\s*ص\s*([^⟩]+?)\s*⟩\s*(.*)$")


def inline(text):
    """Escape, then apply the small subset of markdown our files use."""
    t = html.escape(text, quote=False)
    t = re.sub(r'&lt;(https?://[^\s&]+)&gt;',
               r'<a href="\1" target="_blank" rel="noopener">\1</a>', t)
    t = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',
               r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*(?!\s)([^*]+?)\*', r'<em>\1</em>', t)
    return t


def parse_readme(path):
    meta = {"ar_title": None, "subtitle": None, "author": None, "source": None}
    if not os.path.exists(path):
        return meta
    for line in open(path, encoding="utf-8"):
        s = line.rstrip("\n")
        if s.startswith("# ") and meta["ar_title"] is None:
            meta["ar_title"] = s[2:].strip()
        elif s.startswith("### ") and meta["subtitle"] is None:
            meta["subtitle"] = s[4:].strip()
        elif "**Author:**" in s and meta["author"] is None:
            meta["author"] = s.split("**Author:**", 1)[1].strip()
        elif "Source" in s and meta["source"] is None:
            m = re.search(r"https?://[^\s>)]+", s)
            if m:
                meta["source"] = m.group(0)
    return meta


def parse_chapter(path):
    title, source = None, None
    blocks = []
    cur = None
    awaiting_ar = False

    def push():
        nonlocal cur
        if cur:
            blocks.append(cur)
        cur = None

    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        if line.strip() == "":
            continue
        if line.startswith("# ") and title is None:
            title = line[2:].strip(); continue
        if line.startswith("## "):
            push()
            blocks.append({"kind": "heading", "text": line[3:].strip()})
            awaiting_ar = False; continue
        m = PAGE_RE.match(line)
        if m:
            push()
            cur = {"kind": "unit", "page": m.group(1).strip(),
                   "title": m.group(2).strip(),
                   "ar": "", "en": "", "bn": "", "notes": ""}
            awaiting_ar = True; continue
        if line.startswith("> "):
            content = line[2:]
            if cur is not None and awaiting_ar:
                cur["ar"] = content; awaiting_ar = False
            elif source is None and cur is None:
                source = content
            continue
        if line.startswith("*Notes:*"):
            if cur is not None:
                cur["notes"] = line[len("*Notes:*"):].strip()
            continue
        if cur is not None:                       # a translation paragraph
            key = "bn" if BENGALI.search(line) else "en"
            cur[key] = (cur[key] + " " + line).strip() if cur[key] else line
    push()
    return {"title": title, "source": source, "blocks": blocks}


def split_title(title):
    """'Al-Adab al-Ṣaghīr — [الأدب الصغير]' -> ('Al-Adab al-Ṣaghīr', '[الأدب الصغير]')."""
    if not title:
        return ("", "")
    m = re.match(r"^(.*?)\s*[—-]\s*(\[.*\])\s*$", title)
    return (m.group(1).strip(), m.group(2).strip()) if m else (title, "")


# ---------- HTML assembly ----------

CSS = r"""
*{box-sizing:border-box}
:root{
  --ground:#FBFAF7; --raised:#FFFFFF; --text:#1F1B17; --muted:#8A8175;
  --rubric:#A8322D; --lapis:#28456C; --rule:#E7E1D5; --rule-strong:#D2C9B8;
  --ar-size:1.6rem;
  --ar-font:'Amiri','Scheherazade New','Noto Naskh Arabic','Traditional Arabic','Geeza Pro',serif;
  --bn-font:'Noto Serif Bengali','Kalpurush','Siyam Rupali','Vrinda','Nirmala UI',serif;
  --en-serif:'Iowan Old Style','Palatino Linotype','Palatino','Georgia','Times New Roman',serif;
  --label:ui-sans-serif,-apple-system,'Segoe UI',system-ui,'Helvetica Neue',sans-serif;
}
:root[data-theme="dark"]{
  --ground:#15120D; --raised:#1D1913; --text:#EAE4D7; --muted:#9D9789;
  --rubric:#DB6B61; --lapis:#94B4DC; --rule:#2A2620; --rule-strong:#3C362D;
}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--ground);color:var(--text);
  font-family:var(--en-serif);line-height:1.75;
  -webkit-font-smoothing:antialiased;transition:background .3s,color .3s}

/* ---- header ---- */
header{position:sticky;top:0;z-index:30;
  display:flex;align-items:center;gap:1rem;
  padding:.55rem clamp(.8rem,3vw,2rem);
  background:color-mix(in srgb,var(--ground) 86%,transparent);
  backdrop-filter:saturate(1.1) blur(8px);border-bottom:1px solid var(--rule)}
header .brand{font-family:var(--ar-font);font-size:1.15rem;color:var(--text);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1}
.ctrl{font-family:var(--label);font-size:.8rem;color:var(--text);
  background:transparent;border:1px solid var(--rule-strong);border-radius:.4rem;
  padding:.32rem .55rem;cursor:pointer;line-height:1;transition:.15s}
.ctrl:hover{border-color:var(--rubric);color:var(--rubric)}
.ctrl:focus-visible{outline:2px solid var(--lapis);outline-offset:2px}
.seg{display:inline-flex;border:1px solid var(--rule-strong);border-radius:.4rem;overflow:hidden}
.seg button{font-family:var(--label);font-size:.78rem;background:transparent;color:var(--muted);
  border:0;border-inline-start:1px solid var(--rule-strong);padding:.32rem .5rem;cursor:pointer}
.seg button:first-child{border-inline-start:0}
.seg button[aria-pressed="true"]{background:var(--rubric);color:#fff}
.seg button:focus-visible{outline:2px solid var(--lapis);outline-offset:-2px}

/* ---- contents drawer ---- */
.scrim{position:fixed;inset:0;background:rgba(0,0,0,.4);opacity:0;pointer-events:none;
  z-index:40;transition:opacity .25s}
.scrim.open{opacity:1;pointer-events:auto}
nav.toc{position:fixed;inset-block:0;inset-inline-start:0;z-index:50;width:min(85vw,320px);
  background:var(--raised);border-inline-end:1px solid var(--rule-strong);
  transform:translateX(-100%);transition:transform .28s;overflow-y:auto;padding:1.2rem 1rem 3rem}
[dir="rtl"] nav.toc{transform:translateX(100%)}
nav.toc.open{transform:translateX(0)}
nav.toc h2{font-family:var(--label);font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;
  color:var(--muted);margin:.2rem 0 1rem}
nav.toc .ch{font-family:var(--en-serif);font-size:1.02rem;color:var(--text);
  text-decoration:none;display:block;margin-top:1rem;font-weight:600}
nav.toc .ch:hover{color:var(--rubric)}
nav.toc .pages{display:flex;flex-wrap:wrap;gap:.3rem;margin:.5rem 0 .2rem}
nav.toc .pg{font-family:var(--label);font-size:.74rem;color:var(--muted);text-decoration:none;
  border:1px solid var(--rule);border-radius:.3rem;padding:.12rem .4rem;direction:rtl}
nav.toc .pg:hover{color:var(--rubric);border-color:var(--rubric)}

/* ---- reading column ---- */
main{max-width:50rem;margin:0 auto;padding:0 clamp(1rem,4vw,2rem) 6rem}

/* frontispiece */
.front{text-align:center;padding:clamp(3rem,12vh,7rem) 0 3rem;
  border-bottom:1px solid var(--rule);margin-bottom:1rem}
.front .orn{color:var(--rubric);font-size:1.6rem;font-family:var(--ar-font)}
.front .ar-title{font-family:var(--ar-font);font-size:clamp(2.1rem,7vw,3.4rem);
  line-height:1.5;margin:.6rem 0 .2rem;font-weight:700}
.front .subtitle{font-family:var(--en-serif);font-style:italic;color:var(--muted);
  font-size:1.05rem;margin:.2rem auto;max-width:34rem}
.front .author{font-family:var(--label);font-size:.85rem;letter-spacing:.04em;
  color:var(--text);margin-top:1.1rem}
.front .src{font-family:var(--label);font-size:.76rem;margin-top:.6rem}
.front .src a{color:var(--lapis)}
.rule-orn{display:flex;align-items:center;justify-content:center;gap:.8rem;
  color:var(--rubric);margin:1.4rem auto 0;max-width:18rem}
.rule-orn::before,.rule-orn::after{content:"";height:1px;flex:1;background:var(--rule-strong)}

/* chapter */
.chap{padding-top:2.4rem}
.chap h2{font-family:var(--en-serif);font-size:clamp(1.5rem,4vw,2rem);line-height:1.2;
  margin:0 0 .15rem;letter-spacing:.01em}
.chap h2 .ar{display:block;font-family:var(--ar-font);font-size:1.5rem;color:var(--rubric);
  margin-top:.25rem;font-weight:700}
.chap .chap-src{font-family:var(--label);font-size:.78rem;color:var(--muted);margin:.4rem 0 0}

/* optional in-chapter subheading (real source headings only) */
.subhead{font-family:var(--ar-font);font-size:1.3rem;color:var(--rubric);
  direction:rtl;text-align:right;margin:2.2rem 0 .6rem;font-weight:700}

/* unit */
.unit{margin:1.8rem 0;position:relative;padding-top:.2rem;
  border-top:1px solid color-mix(in srgb,var(--rule) 70%,transparent)}
.unit:first-of-type{border-top:0}
/* print-page number floated into the margin; hidden when there is no gutter */
.pg-tag{position:absolute;inset-inline-start:-3.6rem;top:.7rem;
  font-family:var(--label);font-size:.7rem;color:var(--muted);
  letter-spacing:.03em;direction:rtl;white-space:nowrap;user-select:none}
@media (max-width:60rem){.pg-tag{display:none}}
.u-title{font-family:var(--ar-font);font-size:1.2rem;font-weight:700;color:var(--rubric);
  direction:rtl;text-align:right;margin:0 0 .35rem}
.u-ar{font-family:var(--ar-font);font-size:var(--ar-size);line-height:2.05;
  direction:rtl;text-align:right;color:var(--text);margin:.4rem 0 0}
.u-en{margin:.7rem 0 0;color:var(--text)}
.u-bn{font-family:var(--bn-font);line-height:1.9;margin:.7rem 0 0;color:var(--text)}
.u-notes{font-family:var(--en-serif);font-size:.9rem;color:var(--muted);
  border-inline-start:2px solid color-mix(in srgb,var(--rubric) 55%,transparent);
  padding-inline-start:.85rem;margin:.7rem 0 0}
.u-notes .lbl{font-family:var(--label);font-size:.68rem;text-transform:uppercase;
  letter-spacing:.12em;color:var(--rubric);display:block;margin-bottom:.15rem}
.u-notes em{font-style:italic}

/* view modes: default shows all three; each view isolates one language */
body.view-ar .u-en,body.view-ar .u-bn,body.view-ar .u-notes{display:none}
body.view-en .u-ar,body.view-en .u-bn,body.view-en .u-title{display:none}
body.view-bn .u-ar,body.view-bn .u-en,body.view-bn .u-title,body.view-bn .u-notes{display:none}

a{color:var(--lapis)}
.totop{position:fixed;inset-inline-end:1rem;bottom:1rem;z-index:20;
  font-family:var(--label);font-size:.8rem;text-decoration:none;color:var(--text);
  background:var(--raised);border:1px solid var(--rule-strong);border-radius:50%;
  width:2.6rem;height:2.6rem;display:flex;align-items:center;justify-content:center;
  opacity:0;pointer-events:none;transition:opacity .25s}
.totop.show{opacity:.85;pointer-events:auto}
.totop:hover{opacity:1;border-color:var(--rubric);color:var(--rubric)}
"""

JS = r"""
const root=document.documentElement, body=document.body;
const KEY_T='shamela-theme', KEY_V='shamela-view';
function setTheme(t){root.setAttribute('data-theme',t);
  try{localStorage.setItem(KEY_T,t)}catch(e){}
  document.getElementById('theme').textContent = t==='dark' ? '☀ Light' : '☾ Dark';}
function setView(v){body.classList.remove('view-ar','view-en','view-bn');
  if(v!=='all') body.classList.add('view-'+v);
  try{localStorage.setItem(KEY_V,v)}catch(e){}
  document.querySelectorAll('.seg button').forEach(b=>
    b.setAttribute('aria-pressed', b.dataset.view===v ? 'true':'false'));}
document.getElementById('theme').addEventListener('click',()=>
  setTheme(root.getAttribute('data-theme')==='dark'?'light':'dark'));
document.querySelectorAll('.seg button').forEach(b=>
  b.addEventListener('click',()=>setView(b.dataset.view)));
const toc=document.getElementById('toc'), scrim=document.getElementById('scrim');
function closeToc(){toc.classList.remove('open');scrim.classList.remove('open')}
document.getElementById('menu').addEventListener('click',()=>{
  toc.classList.toggle('open');scrim.classList.toggle('open')});
scrim.addEventListener('click',closeToc);
toc.addEventListener('click',e=>{if(e.target.closest('a'))closeToc()});
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeToc()});
const totop=document.getElementById('totop');
addEventListener('scroll',()=>totop.classList.toggle('show',scrollY>800),{passive:true});
setView((()=>{try{return localStorage.getItem(KEY_V)||'all'}catch(e){return 'all'}})());
"""

PRELUDE = r"""(function(){try{var t=localStorage.getItem('shamela-theme');
if(!t)t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';
document.documentElement.setAttribute('data-theme',t);}catch(e){}})();"""


def build(book_dir, out_path):
    meta = parse_readme(os.path.join(book_dir, "README.md"))
    files = sorted(f for f in glob.glob(os.path.join(book_dir, "*.md"))
                   if re.match(r"\d+", os.path.basename(f)))
    chapters = []
    for f in files:
        ch = parse_chapter(f)
        ch["id"] = re.sub(r"[^a-z0-9]+", "-", os.path.basename(f)[:-3].lower()).strip("-")
        # assign a stable per-chapter index to each unit for anchors
        i = 0
        for b in ch["blocks"]:
            if b["kind"] == "unit":
                i += 1
                b["uid"] = f'{ch["id"]}--u{i}'
        chapters.append(ch)

    # ---- contents drawer (chapters + a page index built from unit tags) ----
    toc_html = ['<nav class="toc" id="toc" aria-label="Contents"><h2>Contents</h2>']
    for ch in chapters:
        lat, _ = split_title(ch["title"])
        toc_html.append(f'<a class="ch" href="#{ch["id"]}">{inline(lat or ch["title"] or ch["id"])}</a>')
        pages, last = [], None
        for b in ch["blocks"]:
            if b["kind"] != "unit" or not b["page"]:
                continue
            if b["page"] != last:
                pages.append(f'<a class="pg" href="#{b["uid"]}">{inline("ص"+b["page"])}</a>')
                last = b["page"]
        if pages:
            toc_html.append('<div class="pages">' + "".join(pages) + "</div>")
    toc_html.append("</nav>")

    # ---- frontispiece ----
    src = meta["source"] or ""
    front = ['<div class="front">', '<div class="orn">۞</div>']
    if meta["ar_title"]:
        front.append(f'<h1 class="ar-title">{inline(meta["ar_title"])}</h1>')
    if meta["subtitle"]:
        front.append(f'<p class="subtitle">{inline(meta["subtitle"])}</p>')
    front.append('<div class="rule-orn">۞</div>')
    if meta["author"]:
        front.append(f'<p class="author">{inline(meta["author"])}</p>')
    if src:
        front.append(f'<p class="src">Source · <a href="{html.escape(src)}" target="_blank" rel="noopener">{html.escape(src)}</a></p>')
    front.append("</div>")

    # ---- chapters ----
    body_parts = []
    for ch in chapters:
        lat, ar = split_title(ch["title"])
        body_parts.append(f'<section class="chap" id="{ch["id"]}">')
        h2 = f'<h2>{inline(lat or ch["title"] or "")}'
        if ar:
            h2 += f'<span class="ar">{inline(ar)}</span>'
        body_parts.append(h2 + "</h2>")
        if ch["source"]:
            body_parts.append(f'<p class="chap-src">{inline(ch["source"])}</p>')
        for b in ch["blocks"]:
            if b["kind"] == "heading":
                body_parts.append(f'<h3 class="subhead" lang="ar" dir="rtl">{inline(b["text"])}</h3>')
                continue
            u = b
            parts = [f'<div class="unit" id="{u["uid"]}">']
            if u["page"]:
                parts.append(f'<span class="pg-tag" aria-hidden="true">{inline("ص"+u["page"])}</span>')
            if u.get("title"):
                parts.append(f'<p class="u-title" lang="ar" dir="rtl">{inline(u["title"])}</p>')
            if u["ar"]:
                parts.append(f'<p class="u-ar" lang="ar" dir="rtl">{inline(u["ar"])}</p>')
            if u["en"]:
                parts.append(f'<p class="u-en">{inline(u["en"])}</p>')
            if u["bn"]:
                parts.append(f'<p class="u-bn" lang="bn">{inline(u["bn"])}</p>')
            if u["notes"]:
                parts.append(f'<aside class="u-notes"><span class="lbl">Notes</span>{inline(u["notes"])}</aside>')
            parts.append("</div>")
            body_parts.append("".join(parts))
        body_parts.append("</section>")

    brand = meta["ar_title"] or (chapters[0]["title"] if chapters else "Book")
    page_title = meta["subtitle"] or meta["ar_title"] or "Translated edition"

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(re.sub('<[^>]+>', '', page_title))}</title>
<script>{PRELUDE}</script>
<style>{CSS}</style>
</head>
<body>
<header>
<button class="ctrl" id="menu" aria-label="Contents">☰ Contents</button>
<span class="brand">{inline(brand)}</span>
<span class="seg" role="group" aria-label="View">
<button data-view="all" aria-pressed="true">All</button>
<button data-view="ar" lang="ar">العربية</button>
<button data-view="en">English</button>
<button data-view="bn" lang="bn">বাংলা</button>
</span>
<button class="ctrl" id="theme">☾ Dark</button>
</header>
<div class="scrim" id="scrim"></div>
{''.join(toc_html)}
<main>
{''.join(front)}
{''.join(body_parts)}
</main>
<a class="totop" id="totop" href="#" aria-label="Back to top">↑</a>
<script>{JS}</script>
</body>
</html>
"""
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(html_doc)
    units = sum(1 for ch in chapters for b in ch["blocks"] if b["kind"] == "unit")
    return len(chapters), units, len(html_doc.encode("utf-8"))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print("usage: build_html.py <book_dir> [output.html]", file=sys.stderr)
        sys.exit(2)
    book_dir = args[0].rstrip("/")
    out_path = args[1] if len(args) > 1 else os.path.join(book_dir, "index.html")
    nch, nu, size = build(book_dir, out_path)
    print(f"wrote {out_path} — {nch} chapters, {nu} units, {size/1024:.0f} KB")


if __name__ == "__main__":
    main()
