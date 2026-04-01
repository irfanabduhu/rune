---
description: "Generate a full novel with chapters (40,000–80,000 words) in a specific author's literary style."
argument-hint: "--author \"Author Name\" [premise] [--period \"time/setting\"] [--tone \"tone\"]"
---

# Novel

Generate a novel from: $ARGUMENTS

---

## Parse Arguments

- **Author** (required): `--author "Name"`. If missing, ask the user.
- **Premise**: The novel's seed.
- **Period** (optional): `--period "..."` — time/place.
- **Tone** (optional): `--tone "..."` — register override.

---

## Phase 1: Deep Voice Calibration

Read `**/voice-calibration.md` using the Glob tool. Perform the ten-dimension analysis with extra depth — the voice must sustain 40,000–80,000 words:

1. Complete the standard analysis.
2. **Extended inventory**: How the author handles chapter openings/endings, subplots, passage of time across a full arc, and the proportion of dialogue vs. narration vs. interiority.
3. **Voice anchors**: Identify 5–7 sentence patterns or verbal tics unmistakably this author. Use these to prevent drift.

---

## Phase 2: Plan

Design the novel's architecture:

1. **Premise expansion**: Full world — setting, context, central conflict.
2. **Characters** (4–8 major): Name, voice, arc, relationships, the author's stance toward them.
3. **Chapter outline** (15–30 chapters): POV, summary, key scenes, word count, connections.
4. **Subplot tracking**: Which chapters each subplot appears in.
5. **Thematic map**: What the plot is about beneath the plot.
6. **Pacing map**: Fast chapters vs. slow chapters, matching the author's rhythm.
7. **Voice anchors**: Formatted as quick-reference reminders for drafting agents.

### User Approval

Present the plan: premise, characters, chapter count, length, thematic core, structural choices. **Wait for approval** before drafting. Incorporate any feedback.

---

## Phase 3: Draft

Draft chapters in parallel batches (4–6 per batch, sequential batches).

Each agent receives: voice profile with anchors, chapter outline, character profiles, subplot grid, summaries of preceding chapters, and its assignment.

Follow the writing mandates from `tale`, plus:
1. **Voice consistency is non-negotiable.** Re-establish the voice in each chapter's opening. Use voice anchors.
2. **Character voice consistency.** Dialogue patterns in Chapter 20 must match Chapter 2.
3. **Continuity.** Names, places, facts, timeline — all consistent.
4. **Chapter structure.** Match how this author opens, builds, and closes chapters.
5. **Proportion and pacing.** Follow the plan.

After each batch, write chapter summaries (200–400 words) capturing events, revelations, changes, and key details.

---

## Phase 4: Revise

Read the full draft. Check:
- Voice audit (first paragraph of every chapter)
- Continuity sweep (names, timeline, settings, facts, subplots)
- Pacing (does it build? dead stretches?)
- Character arcs (earned?)
- The ending (matches the author's mode?)
- Dialogue audit (distinct voices across early/middle/late chapters?)

Revise as needed.

---

## Phase 5: Assemble

Read `**/style-guide.md` using the Glob tool. Follow the `novel` format. Match the author's chapter conventions.

**Quality check**: First and last pages feel like the same novel? Voice recognizable in random middle paragraphs? Within 40,000–80,000 words?

Save as `[title-in-kebab-case].md` (e.g., "The Dispossessed of Andara" → `the-dispossessed-of-andara.md`).
