# Fablesmith Style Guide

## File Structure

Every output file:

```
# [Title]
*In the style of [Author Name]*

---

[Body]

---

*This is original fiction generated in the style of [Author Name].
It is not the work of the named author.*
```

## Typography

- Smart quotes: `"` `"` `'` `'` (Unicode, not straight)
- Em-dash: `—` (no spaces)
- En-dash: `–` (ranges)
- Ellipsis: `…` (single character)

## Formatting by Command

### tale

Scene breaks: `* * *`. No section headers unless the author uses them.

### tales

Stories separated by `---` + `## Story Title`. Internal scene breaks: `* * *`. Optional epigraph after the collection title.

### saga / novel

Chapters: `## Chapter N: Title`. Scene breaks within chapters: `* * *`. Chapter breaks: `---`. Match the author's conventions — unnumbered, untitled, or part/chapter structure.

### play

```
## Dramatis Personae
- **CHARACTER** — Description

## Act I
### Scene 1
*Stage direction in italics.*

**CHARACTER.** Dialogue.
**OTHER.** *(quietly)* Response.
*A pause.*
```

Stage directions: `*italics*`. Character names: `**BOLD.**` No quotation marks around dialogue.

### verse

Each line break preserved. Stanzas separated by blank lines. Poems separated by `---`. Reproduce the poet's typography conventions (Dickinson's dashes, cummings' lowercase, etc.).

### fable

Short prose. `**Moral:**` line after a `* * *` break — only if the author's style calls for explicit morals. Omit entirely for Kafka, Borges, Le Guin, etc.

## General Rules

1. No meta-commentary in the fiction. The style speaks for itself.
2. Paragraph breaks follow the mimicked author's conventions.
3. Unconventional punctuation is part of the mimicry (McCarthy's missing quotes, Joyce's dashes for dialogue).
4. **File naming**: Kebab-case the title, keep articles. `"The Old Man at the River"` → `the-old-man-at-the-river.md`
