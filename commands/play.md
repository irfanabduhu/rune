---
description: "Generate a theatrical play with acts and scenes in a specific playwright's style."
argument-hint: "--author \"Playwright Name\" [premise] [--period \"time/setting\"] [--tone \"tone\"]"
---

# Play

Generate a play from: $ARGUMENTS

---

## Parse Arguments

- **Author** (required): `--author "Name"`. If missing, ask the user.
- **Premise**: The play's central conflict.
- **Period** (optional): `--period "..."` — time/place.
- **Tone** (optional): `--tone "..."` — register override.

---

## Phase 1: Calibrate & Plan

### Voice Calibration for Drama

Read `**/voice-calibration.md` using the Glob tool. Adapt the analysis for dramatic writing:

1. **Dialogue architecture** (PRIMARY): Sentence length, interruptions, silence/pauses, monologue vs. rapid exchange, subtext density. (Pinter: loaded pauses. Shaw: rhetorical speeches. Beckett: fragments. Mamet: staccato.)
2. **Stage direction style**: Minimal (Beckett), novelistic (Shaw), poetic (Williams), functional, or absent.
3. **Dramatic structure**: Classical, absurdist (Beckett/Ionesco), epic (Brecht), naturalist (Ibsen/Chekhov), contemporary (Churchill).
4. **Character through dialogue**: Characters ARE their speech. Each must be distinguishable by voice alone.
5. **Thematic obsessions**: Chekhov: failed communication. Beckett: waiting. Miller: the betrayed dream. Williams: desire vs. propriety. Pinter: power games. Stoppard: ideas in collision.
6. **Audience relationship**: Fourth wall? Direct address? Alienation? Immersion?

### The Imitation Test

Compose 4–6 lines of dialogue. Recognizable? If not, recalibrate.

### Play Plan

1. **Dramatis personae** (3–8): Name, description, speech pattern, role, arc.
2. **Act/scene structure**: Scenes with setting, characters, events, stakes.
3. **Central conflict**: The collision beneath the plot.
4. **Setting**: The set IS a character.
5. **Theatrical moments**: 2–3 moments that work because they're live — silence, entrance, physical action.

---

## Phase 2: Write

Generate the play. For 3+ acts, parallel agents can write different acts.

### Writing Mandates

1. **Dialogue does all the work.** No narrator. Establish character, advance plot, deliver theme through speech.
2. **Each character sounds distinct.** Cover the names — can you tell who's speaking?
3. **Stage directions serve the production.** Match the playwright's convention.
4. **Silence is scripted.** Pauses and beats are as intentional as words.
5. **It must be performable.** This is a script, not a novel in dialogue form.
6. **Structure IS meaning.** Chekhov's four acts of incremental revelation. Beckett's two acts of mirrored degradation.
7. **Subtext over text.** What characters say is not what they mean.

---

## Phase 3: Assemble

Read `**/style-guide.md` using the Glob tool. Follow the `play` format.

**Quality check**: Does dialogue sound like this playwright read aloud? Characters distinguishable? Performable? Moments of genuine dramatic power? Ending resolves (or doesn't) in the playwright's way?

Save as `[title-in-kebab-case].md` (e.g., "The Appointment" → `the-appointment.md`).
