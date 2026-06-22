---
description: "Turn a Maktabat al-Shamela book into a voweled, bilingual study edition with a self-contained HTML reader."
argument-hint: "[shamela.ws book URL]"
---

Produce a bilingual, fully-voweled edition of the Shamela book at: $ARGUMENTS

Follow the `shamelaweave` skill. In brief:

1. **Resolve metadata** — take the book id from the URL and run `scripts/book_meta.py <book_id>` for the title, author, and table of contents.
2. **Map chapters** — group print pages into logical chapters from the TOC; skip index-only sections unless asked.
3. **Translate** — for each chapter, fetch its pages with `scripts/fetch_page.py <book_id> <page>`, vowel the Arabic, and translate into faithful, flowing English. Organize the output as logical-paragraph units numbered continuously per chapter, each tagged `⟨صN⟩` with its print page; never let a print-page break chop a paragraph. For a whole book, fan page ranges out to parallel subagents and assemble in order. Sample one chunk first and confirm the format before the full run.
4. **Render** — run `scripts/build_html.py <book_dir>` to produce the offline `index.html` reader, and verify its reported unit count matches `grep -c '^\*\*\[' *.md`.
