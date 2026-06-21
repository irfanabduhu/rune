---
name: shamelaweave
description: Use when the user gives a Maktabat al-Shamela book URL (shamela.ws/book/<id>/...) and wants it voweled (tashkeel) and translated — produces a per-chapter markdown edition with fully-diacritized Arabic interleaved with faithful English translation, then a self-contained HTML reader.
---

# ShamelaWeave — Shamela Book Translator

Turn a Maktabat al-Shamela book into a bilingual edition: fully-voweled (tashkeel) Arabic
paragraphs, each followed by a faithful English translation and the editor's glosses as
notes. One markdown file per logical chapter; one folder per book; an optional
self-contained HTML reader.

**Paragraphs follow the sense of the text, not the printed page.** A paragraph that the
print edition split across a page turn is joined into one flowing unit; print-page numbers
are recorded as per-unit metadata and rendered in the margin, never as dividers in the text.

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
   dir, and you assemble the chapter files in page order. After assembly run
   `python3 scripts/renumber.py NN-*.md` so numbering is continuous, and re-check the
   slice seams for a paragraph that spans two subagents' ranges. Always process a small
   sample first and have the user confirm format before the full run.

6. **Verify & render.** Run `python3 scripts/verify_edition.py <book_dir>` (no `## ص`
   dividers, contiguous numbering, every unit page-tagged). Then
   `python3 scripts/build_html.py <book_dir>` writes a single self-contained `index.html` —
   offline, light/dark theme, RTL Arabic typography, a Both/Arabic/English view switch, a
   contents drawer with a page index, and print-page numbers floated in the margin. Verify
   the reported unit count matches the markdown (`grep -c '^\*\*\[' *.md`).

## Output format

Per chapter file. Number paragraph units **continuously within the chapter** (start at 1,
no per-page reset); tag each unit with the print page(s) it covers:

```markdown
# <Chapter title (English)> — <Arabic title>

> *Source: <url> — pages X–Y.*

**[7]** ⟨ص11⟩

> <fully-voweled Arabic logical paragraph>

<faithful English translation, as flowing prose>

*Notes:* <translated editor glosses / clarifications, only where warranted>

**[8]** ⟨ص11–12⟩

> <voweled Arabic — one paragraph the print edition split across the page turn>

<continuous English prose for the whole joined paragraph>
```

- `⟨صN⟩` is the print page the unit sits on; `⟨صN–M⟩` (en dash) when a unit spans a page turn.
- Arabic goes in a blockquote, **fully voweled** (every word diacritized).
- English plain underneath. Faithful to meaning; add a short clarifying note only when the
  text or an editor's gloss genuinely needs it. Don't over-annotate.
- The editor's footnote glosses come from `footnotes[]`; fold the relevant ones into
  *Notes:* (translate them). Inline markers (Arabic-Indic digits like ١ ٢) in the body text
  map to those glosses — you may drop the digits from the voweled text once you've used them
  to line up the notes.
- Genuine source headings (a real section title in the text) use `## <heading>` and render
  as a subheading. Do **not** create headings for page numbers — pages are unit tags only.

## Quality bar

- **Paragraph flow is sacred.** Never let a print-page break chop a paragraph. Concatenate
  body across page turns and translate the *joined whole*; the seam must read as continuous
  prose, not two stitched halves. The output should never stop mid-thought the way a printed
  page does.
- **Translation is faithful**, not loose paraphrase — preserve the argument and structure,
  but produce readable, natural English paragraphs, not word-salad. Render rhymed/parallel
  prose (سجع) in a way that keeps its parallelism where natural.
- **Voweling is best-effort.** LLM classical-Arabic tashkeel is strong but not infallible.
  When a vowel is genuinely ambiguous, pick the reading that fits the sense and flag real
  uncertainty in a note rather than guessing silently.
- Preserve `بسم الله الرحمن الرحيم`, Qur'anic quotations, and proper names accurately.
- Page numbers are **citation metadata, never structure.**

## Common mistakes

- **Don't translate from the raw HTML** — always go through `fetch_page.py`; it strips the
  copy-buttons, navigation, and modal UI that otherwise leak into the text.
- **Don't treat shamela pages as chapters** — they're print-page breaks. Group by the TOC.
- **Don't let a page break split a paragraph** — concatenate body across pages and join the
  logical paragraph into one unit (tag it `⟨صN–M⟩`).
- **Don't reset numbering per page** — number units continuously within the chapter.
- **Don't skip the footnotes** — the editor's glosses are the main source of clarifying notes.

## Scripts

- `scripts/book_meta.py <book_id>` — title, author, TOC.
- `scripts/fetch_page.py <book_id> <page> [--raw]` — one page as structured JSON; `--raw` dumps the HTML.
- `scripts/build_html.py <book_dir> [out.html]` — render the finished book folder to a self-contained HTML reader.
- `scripts/verify_edition.py <book_dir>` — check the format (no `## ص` dividers, contiguous numbering, every unit page-tagged).
- `scripts/renumber.py <chapter.md> ...` — renumber `**[n]**` markers sequentially after assembling parallel parts.

`book_meta.py` and `fetch_page.py` use a browser User-Agent (plain WebFetch gets 403 from shamela).
