---
description: "Generate a single short story (1,000–5,000 words) in a specific author's literary style."
argument-hint: "--author \"Author Name\" [premise] [--period \"time/setting\"] [--tone \"tone\"]"
---

# Tale

Generate a short story from: $ARGUMENTS

---

## Parse Arguments

- **Author** (required): `--author "Name"`. If missing, ask the user.
- **Premise**: Everything not a flag — the story's seed.
- **Period** (optional): `--period "..."` — time/place. Defaults to the author's typical era.
- **Tone** (optional): `--tone "..."` — emotional register override.

---

## Phase 1: Calibrate & Plan

### Voice Calibration

Read `**/voice-calibration.md` within this plugin's directory using the Glob tool. Perform the full ten-dimension analysis for the named author.

### The Imitation Test

Compose an opening sentence. Could a well-read person guess the author from that sentence alone? If not, sharpen the profile.

### Story Plan

- **Opening**: How would THIS author begin THIS story?
- **Characters**: 1–3 characters. Name them in the author's naming style.
- **Arc**: In the author's structural terms — Chekhov: revealed, not resolved. O'Connor: grace through violence. Borges: a puzzle that inverts itself.
- **POV and tense**: Per the voice calibration.
- **Length**: 1,000–5,000 words. Shorter for spare authors, longer for expansive ones.

---

## Phase 2: Write

Generate the complete story in a single pass.

### Writing Mandates

1. **Inhabit the voice from the first word.** No warm-up. The first sentence IS the voice.
2. **Maintain voice consistency.** The author's patterns — conjunction chains, paragraph rhythms, dialogue conventions — must appear throughout, not just in the opening.
3. **Let the author's obsessions drive the story.** The premise provides the situation; the author's thematic obsessions shape what it's ABOUT beneath the surface.
4. **Match the author's pacing.** Carver moves in small increments. García Márquez leaps decades in a sentence. Woolf dilates a moment into pages.
5. **Handle dialogue the author's way.** Match the ratio, tag style, punctuation, and subtext density.
6. **End as the author would end.** Epiphanic (Joyce). Ambiguous (Chekhov). Violent (O'Connor). Circular (Borges). Understated (Carver).
7. **Resist the generic.** At every decision point, ask: would THIS author make this choice? If any competent writer might, it's not specific enough.
8. **Honor the author's silences.** What the author does NOT do is the style. If Hemingway wouldn't name the emotion, don't name it.

### Output

Read `**/style-guide.md` using the Glob tool. Follow the `tale` format.

Save as `[title-in-kebab-case].md` (e.g., "The Last Good Country" → `the-last-good-country.md`).

### Quality Check

Before saving, re-read the opening and a middle paragraph:
1. Could a reader guess the author without seeing the attribution?
2. Are there any words this author would never use?
3. Does the story move the way this author's stories move — the same kinds of revelations, tensions, silences?
