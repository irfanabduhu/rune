---
description: "Generate a fable or parable (500–2,000 words) in a specific author's style. Allegorical narrative that teaches through story."
argument-hint: "--author \"Author Name\" [premise or moral] [--tone \"tone\"]"
---

# Fable

Generate a fable from: $ARGUMENTS

---

## Parse Arguments

- **Author** (required): `--author "Name"`. If missing, ask the user. Can be a traditional fabulist (Aesop, La Fontaine) or any author applied to the fable form (Kafka, Borges, Le Guin, Orwell).
- **Premise or Moral**: A situation ("a fox who learns to read") or a moral to illustrate. Both work.
- **Tone** (optional): `--tone "..."` — register override.

---

## Write

### Voice Calibration (Brief)

Read `**/voice-calibration.md` using the Glob tool. Perform a condensed calibration — fables are short, so focus on: sentence rhythm, diction/register, how explicit the moral is, and the author's thematic obsessions.

### The Fable Form

Different authors transform it differently:

| Author | Approach |
|--------|----------|
| Aesop / La Fontaine | Animal characters, stated moral, wit |
| Brothers Grimm | Fairy-tale register, archetypes, supernatural justice |
| Kafka | The parable as trap — promises meaning, withholds it |
| Borges | Thought experiment — brief, precise, concerned with infinity |
| Le Guin | Anthropological field note — the moral emerges from comparison |
| Orwell | Political allegory — power, corruption, propaganda |
| Calvino | Playful cosmology — folk materials with modernist wit |
| Wilde | Aesthetic provocation — beauty, sacrifice, cruelty of the respectable |

If the author never wrote fables, extrapolate: what would their sensibility produce in 500–2,000 words of allegory?

### Generate

Write the complete fable in one pass. **Mandates:**

1. **Two levels**: Works as literal story AND as parable. Both must stand alone.
2. **Characters are types**, but in this author's hands, even types have texture.
3. **Economy**: Every sentence advances plot or theme.
4. **The moral**: Explicit if the style demands it (Aesop, Orwell). Implicit if it doesn't (Kafka, Borges). Ironic if that's the author's mode (Wilde).
5. **Voice fidelity**: Even at this length, the author's rhythms must be recognizable.

### Output

Read `**/style-guide.md` using the Glob tool. Follow the `fable` format.

Save as `[title-in-kebab-case].md` (e.g., "The Fox Who Learned to Read" → `the-fox-who-learned-to-read.md`).
