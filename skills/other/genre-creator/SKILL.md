---
name: genre-creator
description: Create new genre documentation files for the bitwize-music genre library. Use when the user wants to add a genre, says "/genre-creator", "neues Genre erstellen", "Genre hinzufuegen", "add genre", or asks to create genre documentation. Takes a genre name as argument.
model: claude-sonnet-4-6
argument-hint: <genre-name e.g. "Math Rock" or "Nu-Metal">
---

# Genre Creator

## Your Task

Create a new genre README.md for the bitwize-music genre library at `${CLAUDE_PLUGIN_ROOT}/genres/`.

**Input**: $ARGUMENTS (genre name, e.g. "Math Rock", "Nu-Metal", "City Pop")

## Workflow

1. **Derive slug**: Lowercase, hyphenated (e.g. "Math Rock" → `math-rock`)
2. **Check existence**: If `genres/{slug}/README.md` exists → abort, inform user
3. **Check INDEX.md**: Read `genres/INDEX.md` to confirm genre is not already listed
4. **Research**: Use WebSearch to verify key facts (origin year, pioneer artists, landmark albums) — do NOT guess dates or album names
5. **Read 1-2 existing genre files** for structural reference (e.g. `genres/hip-hop/README.md`, `genres/phonk/README.md`)
6. **Create directory**: `genres/{slug}/`
7. **Write README.md** following the exact template below
8. **Update INDEX.md**: Add genre to category table, alphabetical list, and all applicable Quick Reference tables (Tempo, Energy, Instrumentation, Vocals, Mood, Era)
9. **Update mastering presets**: Add the new genre to both mastering preset files:
   - `tools/mastering/genre-presets.yaml` — Add YAML entry with `target_lufs`, `cut_highmid`, `cut_highs` values appropriate for the genre. Place in the correct category section or create a new one.
   - `skills/mastering-engineer/genre-presets.md` — Add a new `### Genre Name` section under `## Genre Presets` with LUFS target, dynamics, EQ focus, MCP command, and characteristics.
10. **Do NOT create** an `artists/` subdirectory — those are created separately when artist deep-dives are written

## README.md Template

The file starts directly with `# Genre Name` — no YAML frontmatter.

ALWAYS use this exact section order:

```
# {Genre Name}

## Genre Overview
[3 paragraphs — see rules below]

## Characteristics
[6 bullet fields — see rules below]

## Lyric Conventions
[6 bullet fields — see rules below]

## Subgenres & Styles
[Table — see rules below]

## Artists
[Table — see rules below]

## Suno Prompt Keywords
[Code block — see rules below]

## Reference Tracks
[List — see rules below]
```

### Section Rules

**## Genre Overview** — 3 paragraphs of prose (no bullets):
- P1: Origin, cultural roots, pioneers with names and years
- P2: Evolution across decades, key moments, mainstream breakthrough, regional variants
- P3: Current state, influence on other genres, modern scene
- Style: Encyclopedic but alive. Concrete names, years, albums. No vague claims.

**## Characteristics** — Bullet list, exactly these 6 fields:
- **Instrumentation**: Typical instruments, specific models/brands where relevant
- **Vocals**: Singing style, vocal processing, delivery
- **Production**: Production techniques, mix aesthetic, sonic character
- **Energy/Mood**: Mood spectrum, emotional range
- **Structure**: Song form, typical length, structural quirks
- **Tempo**: BPM ranges per subgenre, rhythm feel (half-time, swing, straight etc.)

**## Lyric Conventions** — Bullet list, exactly these 6 fields:
- **Default rhyme scheme**: Typical scheme with shorthand (AABB, ABAB, XAXA etc.)
- **Rhyme quality**: Expected quality (multisyllabic, slant, internal etc.)
- **Verse structure**: Line count, bar structure
- **Key rule**: THE single most important rule for lyrics in this genre
- **Avoid**: What NOT to do in this genre
- **Density/pacing (Suno)**: Format: `Default **X lines/verse** at Y BPM. [Context]. Topics: Z/verse.`

**## Subgenres & Styles** — Markdown table:

| Style | Description | Reference Artists |
|-------|-------------|-------------------|

- 6-12 subgenres
- Description: 2-3 sentences with musical specifics, not just adjectives
- Reference Artists: 3-4 per subgenre

**## Artists** — Markdown table:

| Artist | Key Albums | Era | Style Focus |
|--------|-----------|-----|-------------|

- 10-20 artists, mix of pioneers + peak-era + current acts
- Albums in italics (*Album Name*)
- If a deep-dive file exists: append a `Deep Dive` link to the artist file in Style Focus

**## Suno Prompt Keywords** — Fenced code block with comma-separated keywords organized in thematic lines:
- Genre/subgenre labels
- Instrument keywords
- Production keywords
- Mood/atmosphere keywords
- Vocal keywords
- Tempo/rhythm keywords
- Era/aesthetic keywords
- All keywords in English. Only use terms Suno actually understands.

**## Reference Tracks** — 10-15 entries:
- Format: `- **Artist - "Track Title"** — [Description]`
- Description: 2-3 sentences. Explain WHAT makes this track a genre reference point. Name concrete musical elements. Explain historical/cultural significance.
- Chronological spread from founding tracks to modern representatives

## Important Notes

1. **Factual accuracy**: All years, album names, artist names must be correct. Omit rather than guess. Use WebSearch to verify.
2. **No AI cliches**: Ban these phrases: "tapestry of sound", "sonic landscape", "testament to", "rich tapestry", "sonic journey", "pushing boundaries", "transcends genre". Write direct, concrete prose.
3. **Suno focus**: Lyric Conventions and Suno Keywords are the most important sections — they directly drive music generation quality.
4. **Subgenre deduplication**: If a subgenre already has its own genre directory (e.g. Trap exists as standalone genre), reference it instead of duplicating content.
5. **Language**: English (the entire genre system is in English)
6. **No empty sections**: Every section must have substantive content. If unsure about a section, research first.
