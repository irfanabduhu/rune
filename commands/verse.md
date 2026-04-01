---
description: "Generate a poetry collection (10–20 poems) around a theme in a specific poet's style."
argument-hint: "--author \"Poet Name\" [theme] [--count N] [--period \"time/setting\"]"
---

# Verse

Generate a poetry collection from: $ARGUMENTS

---

## Parse Arguments

- **Author** (required): `--author "Name"`. If missing, ask the user.
- **Theme**: Subject, emotional territory, or conceptual thread.
- **Count** (optional): `--count N` — number of poems (default: 12, range: 10–20).
- **Period** (optional): `--period "..."` — setting.
- **Tone** (optional): `--tone "..."` — register override.

---

## Phase 1: Calibrate & Plan

### Voice Calibration for Poetry

Read `**/voice-calibration.md` using the Glob tool. Adapt the analysis for verse — several dimensions work differently in poetry:

1. **Line architecture**: Line length, enjambment patterns, sentence-to-line relationship.
2. **Stanza rhythm**: Couplets, tercets, quatrains, irregular. How breaks function.
3. **Diction**: Elevated or colloquial? Latinate or Anglo-Saxon? The vocabulary they refuse?
4. **Sound**: Rhyme (full, slant, internal, none). Meter. Alliteration, assonance.
5. **Imagery**: Dominant image types. Metaphor strategies. How original vs. traditional.
6. **Thematic obsessions**: Plath: body, rage, father. Bishop: geography, loss. Dickinson: death, interiority.
7. **Compression**: How much does the reader supply? Dickinson: enormous. Whitman: almost nothing unsaid.
8. **Opening/closing**: How poems begin and end. Where the turn falls.
9. **Typography**: Capitalization, punctuation, spatial form. Dickinson's dashes. cummings' lowercase.
10. **Relationship to form**: Received forms or free verse? How do they inhabit or strain against form?

### The Imitation Test

Compose a stanza — 3–5 lines. Recognizable? If not, recalibrate.

### Collection Plan

- **Poem list**: Title, subject, approximate form, role in the arc.
- **Arc**: Emotional trajectory from first poem to last.
- **Formal variety**: Within the poet's range, vary length and density.
- **Recurring images**: 3–5 motifs threading through without repetition.

---

## Phase 2: Write & Assemble

Generate all poems. Parallel agents can write simultaneously, each receiving the voice profile, plan, and assignment.

### Writing Mandates

1. **The line is the unit.** Every break is intentional.
2. **Sound matters.** Match the poet's ear.
3. **Compression.** Every word earns its place — unless the style is expansive, where accumulation IS meaning.
4. **Image over abstraction** — unless the poet works in abstraction (Stevens, Ashbery), where it should feel precise, not vague.
5. **The turn.** Most poems shift direction somewhere. Match where this poet turns.
6. **Voice fidelity above all.** A perfect sonnet in the wrong voice is a failure.

### Output

Read `**/style-guide.md` using the Glob tool. Follow the `verse` format.

**Quality check**: Does the collection move? Enough variety? Unified voice? Threads present but not forced?

Save as `[title-in-kebab-case].md` (e.g., "Fever Songs" → `fever-songs.md`).
