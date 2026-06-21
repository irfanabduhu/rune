# ShamelaWeave Plugin

Turn a Maktabat al-Shamela book into a bilingual study edition: fully-voweled
(tashkeel) Arabic paragraphs, each followed by a faithful English translation
and the editor's glosses, plus a single self-contained HTML reader.

Paragraphs follow the *sense* of the text, not the print page — a paragraph the
printed edition split across a page turn is joined into one flowing unit, and
print-page numbers live in the margin as citation metadata.

## Command

| Command                | Input                                   | Output                                              |
| ---------------------- | --------------------------------------- | --------------------------------------------------- |
| `/shamelaweave:weave`  | A shamela.ws book URL                   | A per-chapter markdown edition + `index.html` reader |

The skill also activates automatically when you paste a `shamela.ws/book/<id>/…` URL and ask for it voweled and translated.

## Usage

```bash
/shamelaweave:weave https://shamela.ws/book/7528
```

## How it works

1. **Resolve metadata** — `book_meta.py` returns title, author, and the table of contents.
2. **Map chapters to page ranges** — group shamela print pages into logical chapters from the TOC.
3. **Translate** — for each chapter, fetch its pages (`fetch_page.py`), vowel the Arabic, translate faithfully, and write logical-paragraph units. A whole book is fanned out to parallel agents per page range, assembled in order.
4. **Render** — `build_html.py` turns the book folder into one offline HTML reader (light/dark, RTL naskh typography, Both/Arabic/English switch, contents drawer with a page index).

Voweling is best-effort classical tashkeel; translation is faithful but reads as natural English prose.

## Requirements

Python 3 (standard library only). No third-party packages.

## Installation

**From the marketplace (recommended):**

```bash
claude plugin marketplace add irfanabduhu/shamelaweave
claude plugin install shamelaweave@irfanabduhu
```

**Per-session (alternative):**

```bash
git clone https://github.com/irfanabduhu/shamelaweave.git ~/shamelaweave
claude --plugin-dir ~/shamelaweave
```
