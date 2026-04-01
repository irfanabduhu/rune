# Fablesmith

Generate creative fiction in markdown, mimicking specific authors' literary styles.

## Commands

| Command              | Output           | Length              | Input                  |
| -------------------- | ---------------- | ------------------- | ---------------------- |
| `/fablesmith:tale`   | Short story      | 1,000–5,000 words   | Author + premise       |
| `/fablesmith:tales`  | Story collection | 3–7 stories         | Author + shared theme  |
| `/fablesmith:saga`   | Novella          | 10,000–30,000 words | Author + premise       |
| `/fablesmith:novel`  | Full novel       | 40,000–80,000 words | Author + premise       |
| `/fablesmith:play`   | Theatrical play  | 2–5 acts            | Playwright + premise   |
| `/fablesmith:verse`  | Poetry collection| 10–20 poems         | Poet + theme           |
| `/fablesmith:fable`  | Fable/parable    | 500–2,000 words     | Author + premise/moral |

## Installation

```bash
# Marketplace
claude plugin marketplace add irfanabduhu/fablesmith
claude plugin install fablesmith@irfanabduhu

# Per-session
git clone https://github.com/irfanabduhu/fablesmith.git ~/fablesmith
claude --plugin-dir ~/fablesmith

# Pi
git clone https://github.com/irfanabduhu/fablesmith.git .pi/skills/fablesmith

# OpenCode
cp -r path/to/fablesmith/commands/. .opencode/commands/
```

## Usage

```bash
/fablesmith:tale --author "Hemingway" A soldier returns to his hometown --period "1920s Michigan"
/fablesmith:tales --author "Borges" Impossible libraries and infinite texts --count 5
/fablesmith:saga --author "Kafka" A man's apartment is reclassified as a government office
/fablesmith:novel --author "Le Guin" A propertyless society confronts first contact --period "far future"
/fablesmith:play --author "Pinter" Two old friends reveal a betrayal over drinks
/fablesmith:verse --author "Plath" Motherhood and the dissolution of self --count 15
/fablesmith:fable --author "Kafka" A dog discovers food falls from the sky
```

## Flags

| Flag       | Description                          | Default                     | Applies to        |
| ---------- | ------------------------------------ | --------------------------- | ----------------- |
| `--author` | Author whose style to mimic         | *(required)*                | All               |
| `--period` | Time period and/or setting           | Author's typical era        | All except fable  |
| `--tone`   | Emotional register override          | Author's natural tendencies | All               |
| `--count`  | Number of stories or poems           | 5 stories / 12 poems        | tales, verse      |

## How It Works

Before writing, the plugin performs a **voice calibration** — analyzing the author across ten dimensions: sentence architecture, paragraph rhythm, diction, dialogue style, narrative perspective, thematic obsessions, what's left unsaid, opening/closing strategies, sensory detail, and temporal handling.

This produces specific, nameable techniques — not "writes beautifully" but "uses polysyndetic 'and' chains with suppressed emotional subtext."

## Output

Filenames come from the story's title: `the-last-good-country.md`, `histories-of-the-infinite.md`.

Every file includes a style attribution and a disclaimer that the work is original fiction.

## Limitations

- Works best for authors with **distinctive, well-documented styles** — Hemingway, Kafka, Woolf, Borges, Austen, etc.
- Less effective for styles that are primarily structural rather than sentence-level.
- The `novel` command pauses after planning for user approval before generating 40,000+ words.
- This is skilled pastiche, not forgery. It captures patterns, not lived experience.
