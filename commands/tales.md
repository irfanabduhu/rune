---
description: "Generate a collection of 3–7 short stories around a shared theme, in a specific author's literary style."
argument-hint: "--author \"Author Name\" [shared theme] [--count N] [--period \"time/setting\"]"
---

# Tales

Generate a story collection from: $ARGUMENTS

---

## Parse Arguments

- **Author** (required): `--author "Name"`. If missing, ask the user.
- **Theme**: The shared thread connecting the stories.
- **Count** (optional): `--count N` — number of stories (default: 5, range: 3–7).
- **Period** (optional): `--period "..."` — shared time/place.
- **Tone** (optional): `--tone "..."` — register override.

---

## Phase 1: Calibrate & Plan

### Voice Calibration

Read `**/voice-calibration.md` using the Glob tool. Perform the full ten-dimension analysis.

### The Imitation Test

Compose an opening sentence. Recognizable as this author? If not, recalibrate.

### Collection Design

Design the collection as a whole — how stories relate, not just what they contain:

1. **The author's collection strategy**: Joyce (*Dubliners*): progressive. Borges (*Ficciones*): encyclopedic variations. Carver: thematic echoes across households. Munro: shared region, recurring types. Match the named author's approach.

2. **Story premises**: For each story — one-sentence premise, connection to theme, how it echoes or contrasts with others.

3. **Collection arc**: What does the reader understand by the final story that they didn't at the start?

4. **Shared elements**: Recurring setting, character type, image, or phrase threading through.

---

## Phase 2: Write

Generate each story (1,000–5,000 words) following the writing mandates from the `tale` command.

**Parallel execution**: Launch agents to write stories simultaneously. Each receives the voice profile, collection plan, its own premise, and all other premises (for echoes and connections).

---

## Phase 3: Assemble

Read `**/style-guide.md` using the Glob tool. Follow the `tales` format.

**Quality check** before saving:
1. Does the arc build across the collection?
2. No redundant stories — each contributes something unique.
3. Can a reader detect connecting threads without them being heavy-handed?
4. Does the whole collection feel like one author's work?

Save as `[title-in-kebab-case].md` (e.g., "Histories of the Infinite" → `histories-of-the-infinite.md`).
