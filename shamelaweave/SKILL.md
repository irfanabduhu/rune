---
name: shamelaweave
description: Use when the user gives a Maktabat al-Shamela book URL (shamela.ws/book/<id>/...) and wants it voweled (tashkeel) and translated — produces a per-chapter markdown edition with fully-diacritized Arabic followed by lucid English and Bengali translations, then a self-contained HTML reader.
---

# ShamelaWeave — Shamela Book Translator

Turn a Maktabat al-Shamela book into a trilingual edition: fully-voweled (tashkeel) Arabic
paragraphs, each followed by a lucid English translation and a lucid Bengali translation,
with the editor's glosses as notes. One markdown file per logical chapter; one folder per
book; an optional self-contained HTML reader.

**Paragraphs follow the sense of the text, not the printed page.** A paragraph that the
print edition split across a page turn is joined into one flowing unit; print-page numbers
are recorded as per-unit metadata and rendered in the margin, never as dividers in the text.

**Content over ceremony.** Units carry no section numbers — a unit is simply its Arabic and
its translations. The only marker is the print-page tag `⟨صN⟩`, which doubles as the unit
delimiter and renders in the margin.

**Division of labor:** the bundled scripts do the fragile, mechanical work (fetching, HTML
parsing, UI stripping, rendering, format checks). **You** do the voweling and translation —
those require judgment and cannot be scripted.

## Workflow

1. **Resolve metadata.** From the URL take the book id. Run:
   `python3 scripts/book_meta.py <book_id>` → title, author, TOC `[{page, title}]`.
   (TOC pages are URL page indices, not printed page numbers.)

2. **Map chapters to page ranges.** Chapter *i* spans `[toc[i].page, toc[i+1].page)`.
   The last chapter runs to the book's end — walk pages until `fetch_page` returns
   `next_page: null` or an empty body. Skip index-only sections (الفهارس / indexes)
   unless the user wants them.

3. **Create the book folder.** `<book-slug>/` with a `README.md` (title, author, source
   URL, section map, generation notes). Use a short ASCII slug of the title.

4. **Process each chapter.** For every page in the range run:
   `python3 scripts/fetch_page.py <book_id> <page>` → `{heading, body[], footnotes[], print_page, next_page}`.
   **Concatenate `body` across page breaks** and segment the result into *logical*
   paragraphs — sense units, not print pages. A paragraph that the print edition broke
   across a page turn becomes ONE unit. Then write each unit in the format below.
   Save as `NN-slug.md` (e.g. `01-al-adab-al-saghir.md`).

5. **Scale.** For a whole book, fan chapters (or page ranges) out to parallel subagents —
   each subagent gets a page range and the format spec, writes its piece to a `.parts/`
   dir, and you assemble the chapter files in page order. Re-check the slice seams for a
   paragraph that spans two subagents' ranges. Always process a small sample first and have
   the user confirm format before the full run.

6. **Verify & render.** Run `python3 scripts/verify_edition.py <book_dir>` (no `## ص`
   dividers; every unit has a `⟨صN⟩` tag, Arabic, English, and Bengali; ranges use the en
   dash). Then `python3 scripts/build_html.py <book_dir>` writes a single self-contained
   `index.html` — offline, light/dark theme, RTL Arabic typography, an
   All / العربية / English / বাংলা view switch, a contents drawer with a page index, and
   print-page numbers floated in the margin.

## Output format

Per chapter file. No unit numbers — each unit begins with its print-page tag, which is also
the delimiter. Arabic, then English, then Bengali, in that order:

```markdown
# <Chapter title (English)> — <Arabic title>

> *Source: <url> — pages X–Y.*

⟨ص11⟩

> <fully-voweled Arabic logical paragraph>

<lucid English translation, as flowing prose>

<lucid Bengali translation, as flowing prose>

*Notes:* <translated editor glosses / clarifications, only where warranted>

⟨ص11–12⟩

> <voweled Arabic — one paragraph the print edition split across the page turn>

<continuous English prose for the whole joined paragraph>

<continuous Bengali prose for the whole joined paragraph>
```

- `⟨صN⟩` is the print page the unit sits on; `⟨صN–M⟩` (en dash, U+2013) when a unit spans a
  page turn. This tag starts every unit — there are no `**[n]**` numbers.
- Arabic goes in a blockquote, **fully voweled** (every word diacritized).
- English first, then Bengali, each as its own paragraph. (The renderer routes them by
  script, so a stray ordering still renders correctly — but author them English-then-Bengali.)
- *Notes:* (optional, English) carry the editor's footnote glosses and clarifications.
  Inline markers (Arabic-Indic digits like ١ ٢) map to those glosses — you may drop the
  digits from the voweled text once you've used them to line up the notes.
- Genuine source headings (a real section title in the text) use `## <heading>` and render
  as a subheading. Do **not** create headings for page numbers — pages are unit tags only.

## Quality bar

- **Paragraph flow is sacred.** Never let a print-page break chop a paragraph. Concatenate
  body across page turns and translate the *joined whole*; the seam must read as continuous
  prose, not two stitched halves. The output should never stop mid-thought the way a printed
  page does.
- **Both translations are lucid and faithful** — preserve the argument and structure, but
  produce readable, natural prose in each language, not word-salad. Render rhymed/parallel
  prose (سجع) so its parallelism survives where natural. The Bengali should read as good
  Bengali (সাধু/চলিত as fits the register), not a transliteration of the English.
- **Voweling is best-effort.** LLM classical-Arabic tashkeel is strong but not infallible.
  When a vowel is genuinely ambiguous, pick the reading that fits the sense and flag real
  uncertainty in a note rather than guessing silently.
- Preserve `بسم الله الرحمن الرحيم`, Qur'anic quotations, and proper names accurately in all
  three languages.
- Page numbers are **citation metadata, never structure.**

## Common mistakes

- **Don't translate from the raw HTML** — always go through `fetch_page.py`; it strips the
  copy-buttons, navigation, and modal UI that otherwise leak into the text.
- **Don't treat shamela pages as chapters** — they're print-page breaks. Group by the TOC.
- **Don't let a page break split a paragraph** — concatenate body across pages and join the
  logical paragraph into one unit (tag it `⟨صN–M⟩`).
- **Don't add unit numbers or other ceremony** — the page tag is the only marker.
- **Don't skip the footnotes** — the editor's glosses are the main source of clarifying notes.

## Scripts

- `scripts/book_meta.py <book_id>` — title, author, TOC.
- `scripts/fetch_page.py <book_id> <page> [--raw]` — one page as structured JSON; `--raw` dumps the HTML.
- `scripts/build_html.py <book_dir> [out.html]` — render the finished book folder to a self-contained HTML reader.
- `scripts/verify_edition.py <book_dir>` — check the format (no `## ص` dividers; each unit has a `⟨صN⟩` tag, Arabic, English, and Bengali; en-dash ranges).

`book_meta.py` and `fetch_page.py` use a browser User-Agent (plain WebFetch gets 403 from shamela).
