---
description: "Generate a novella (10,000–30,000 words) in a specific author's literary style."
argument-hint: "--author \"Author Name\" [premise] [--period \"time/setting\"] [--tone \"tone\"]"
---

# Saga

Generate a novella from: $ARGUMENTS

---

## Parse Arguments

- **Author** (required): `--author "Name"`. If missing, ask the user.
- **Premise**: The story's seed.
- **Period** (optional): `--period "..."` — time/place.
- **Tone** (optional): `--tone "..."` — register override.

---

## Phase 1: Calibrate & Plan

### Voice Calibration

Read `**/voice-calibration.md` using the Glob tool. Perform the full ten-dimension analysis.

### The Imitation Test

Compose an opening sentence. Recognizable? If not, recalibrate.

### Novella Plan

1. **Premise expansion**: Who, where, when, what's at stake.
2. **Section outline** (8–15 sections): Per section — what happens, key scene, what shifts. Total: 10,000–30,000 words.
3. **Character profiles**: Name (author's style), role, voice, arc.
4. **Thematic throughline**: What is this ABOUT beneath the plot?
5. **Pacing map**: Where it accelerates, where it dilates. Match the author's rhythms.
6. **Voice notes**: 3–5 specific reminders for sustaining this author's style over long stretches.

Report a brief summary to the user before proceeding.

---

## Phase 2: Draft

Draft sections in parallel batches (3–4 per batch, sequential batches).

Each agent receives: voice profile, section outline, character profiles, voice notes, summaries of preceding sections, and its assignment.

Follow the writing mandates from `tale`, plus:
1. **No voice drift.** Re-anchor to the profile at each section's start.
2. **Continuity.** Honor details from earlier sections.
3. **Transitions.** Match how this author moves between sections.
4. **Pacing fidelity.** Follow the pacing map.

After each batch, write summaries for subsequent batches.

---

## Phase 3: Revise

Read the full draft. Check for voice drift, continuity errors, pacing problems, arc coherence, and dialogue consistency. Revise as needed.

---

## Phase 4: Assemble

Read `**/style-guide.md` using the Glob tool. Follow the `saga` format. Match the author's chapter conventions (titled, numbered, or unmarked sections).

**Quality check**: First and last paragraphs feel like the same author? Middle paragraphs immediately recognizable? Within target length?

Save as `[title-in-kebab-case].md` (e.g., "The Bureau of Reclassification" → `the-bureau-of-reclassification.md`).
