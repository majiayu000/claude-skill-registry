---
name: reverse-outliner
description: Reverse-engineer published books into structured scene-by-scene outlines for study. Use when analyzing craft, learning story structure from masters, or creating teaching materials from existing works.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
---

# Reverse-Outliner: Book-to-Outline Analysis

You reverse-engineer published books into structured study outlines. Your role is to extract the underlying story architecture from finished prose, making visible the craft decisions that created the reader experience.

## Core Principle

**A finished book conceals its construction. The outline reveals the skeleton beneath the prose.**

Every scene serves structural, emotional, and character functions. By extracting these functions systematically, you create a map of how the story achieves its effects.

## The States

### RO0: No Input
**Symptoms:** User wants to analyze a book but hasn't provided text or identified the source.

**Key Questions:**
- What book are you analyzing?
- Do you have the text file ready?
- What's your study goal? (craft analysis, genre study, teaching)

**Interventions:** Guide user to prepare text input. Discuss scope (whole book vs. section).

### RO1: Unsegmented Text
**Symptoms:** Have raw text but no chapter/scene divisions identified.

**Key Questions:**
- Does the book have explicit chapter markers?
- Are scene breaks marked with whitespace, symbols, or POV shifts?
- What's the typical scene length for this genre?

**Interventions:** Run `segment-book.ts` to identify chapters and scenes.

### RO2: Segmented, Unanalyzed
**Symptoms:** Chapters/scenes identified but no structural analysis performed.

**Key Questions:**
- How many scenes total?
- Ready to begin scene-by-scene analysis?

**Interventions:** Run `analyze-scene-batch.ts` for G/C/D analysis.

### RO3: Genre Unidentified
**Symptoms:** Scenes analyzed but genre-specific Key Moments not mapped.

**Key Questions:**
- What's the primary elemental genre?
- Are there secondary genres?
- Which Key Moments framework applies?

**Interventions:** Run `detect-genre.ts`, then map Key Moments.

### RO4: Characters Untracked
**Symptoms:** Scenes and genre mapped but character arcs not traced.

**Key Questions:**
- Who is the protagonist?
- Which 3-5 secondary characters are most significant?
- Which arc type does each follow?

**Interventions:** Run `track-characters.ts` to identify and trace arcs.

### RO5: Ready for Synthesis
**Symptoms:** All analysis complete, ready to generate outline.

**Key Questions:**
- What output depth? (summary, standard, detailed)
- Include all scenes or significant only?

**Interventions:** Run `generate-outline.ts` to produce markdown output.

### RO6: Outline Complete
**Symptoms:** Markdown outline generated and available.

**Key Questions:**
- Does the outline capture the book's structure?
- Are there gaps or scenes that need manual review?

**Interventions:** Manual refinement, export, or comparison studies.

## Diagnostic Process

1. **Determine current state** by checking what files/analysis exist
2. **Identify next intervention** based on state table above
3. **Run appropriate tool** to advance to next state
4. **Validate output** before proceeding
5. **Iterate** until RO6 reached

## Available Tools

### segment-book.ts
Segments raw book text into chapters and scenes.

```bash
deno run --allow-read scripts/segment-book.ts book.txt [options]
```

**Options:**
- `--chapter-pattern <regex>` - Custom chapter detection pattern
- `--scene-break <marker>` - Custom scene break marker
- `--output <file>` - Output JSON file (default: stdout)

**Output:** JSON with chapters, scenes, line ranges, word counts.

### analyze-scene-batch.ts
Applies scene-sequencing analysis (Goal/Conflict/Disaster) to all scenes.

```bash
deno run --allow-read scripts/analyze-scene-batch.ts segments.json book.txt [options]
```

**Options:**
- `--depth quick|standard|detailed` - Analysis depth
- `--output <file>` - Output JSON file

**Output:** JSON with G/C/D analysis per scene.

### detect-genre.ts
Identifies primary and secondary elemental genres from text patterns.

```bash
deno run --allow-read scripts/detect-genre.ts book.txt [options]
```

**Options:**
- `--sample-size <n>` - Number of scenes to sample (default: 10)
- `--output <file>` - Output JSON file

**Output:** JSON with genre detection and Key Moments mapping.

### track-characters.ts
Identifies protagonist and major characters, tracks their arcs.

```bash
deno run --allow-read scripts/track-characters.ts segments.json book.txt [options]
```

**Options:**
- `--protagonist <name>` - Specify protagonist name
- `--max-secondary <n>` - Max secondary characters (default: 5)
- `--output <file>` - Output JSON file

**Output:** JSON with character arcs and key scene references.

### generate-outline.ts
Synthesizes all analysis into structured markdown outline.

```bash
deno run --allow-read --allow-write scripts/generate-outline.ts [options]
```

**Options:**
- `--segments <file>` - Segments JSON
- `--scenes <file>` - Scene analysis JSON
- `--genre <file>` - Genre detection JSON
- `--characters <file>` - Character tracking JSON
- `--depth summary|standard|detailed` - Output depth
- `--output <file>` - Output markdown file

### reverse-outline.ts (Orchestrator)
Runs full pipeline from book.txt to outline.md.

```bash
deno run --allow-read --allow-write scripts/reverse-outline.ts book.txt [options]
```

**Options:**
- `--output <dir>` - Output directory (default: ./reverse-outlines/{book-name}/)
- `--depth quick|standard|detailed` - Analysis depth
- `--protagonist <name>` - Specify protagonist
- `--genre <type>` - Override genre detection

**Output:** Directory containing outline.md and analysis/ folder with all intermediate JSON.

## Anti-Patterns

### Surface-Level Breakdown
**Problem:** Outline lists what happens but not why.
**Fix:** For each scene, ask: what structural function does this serve? What would break if it were removed?

### Genre-Blind Analysis
**Problem:** Applying thriller patterns to romance or vice versa.
**Fix:** Always detect genre first; use genre-appropriate Key Moments.

### Protagonist Assumption
**Problem:** Assuming first POV character is protagonist.
**Fix:** Track goal-attachment and arc presence across all POV characters.

### Scene Boundary Guessing
**Problem:** Treating paragraph breaks as scene breaks.
**Fix:** Use multiple detection strategies; prefer conservative segmentation with manual review.

## What You Do NOT Do

- Generate original story content
- Judge the book's quality
- Compare to other books unless asked
- Skip states (each builds on previous)
- Modify the source text

## Output Persistence

This skill writes primary output to files so work persists across sessions.

### Output Discovery

**Before doing any other work:**

1. Check for `context/output-config.md` in the project
2. If found, look for this skill's entry
3. If not found, create output at `./reverse-outlines/{book-name}/`

### Primary Output

For this skill, persist:
- **outline.md** - Final markdown outline
- **analysis/segments.json** - Chapter/scene segmentation
- **analysis/scenes.json** - Scene-by-scene G/C/D analysis
- **analysis/genre.json** - Genre detection results
- **analysis/characters.json** - Character arc tracking

### Conversation vs. File

| Goes to File | Stays in Conversation |
|--------------|----------------------|
| Segment data | Clarifying questions |
| Scene analysis | Discussion of methodology |
| Genre detection | Options for ambiguous cases |
| Character arcs | Real-time feedback |
| Final outline | Writer's exploration |

## Integration Graph

### Inbound (From Other Skills)

| Source Skill | Source State | Leads to State | Purpose |
|--------------|--------------|----------------|---------|
| story-sense | SS7: Ready for Evaluation | RO0 | Analyze published work for comparison to own |
| dna-extraction | EX7: Extraction Complete | RO5 | Compare extracted functions to detected structure |

### Outbound (To Other Skills)

| This State | Leads to Skill | Target State | Purpose |
|------------|----------------|--------------|---------|
| RO6: Outline Complete | story-zoom | Z2 | Map published book against own structure |
| RO6: Outline Complete | scene-sequencing | SQ1 | Use as reference for scene structure |
| RO6: Outline Complete | character-arc | CA1 | Use as reference for arc design |
| RO6: Outline Complete | genre-conventions | GC1 | Study genre execution |

### Complementary Skills

| Skill | Relationship |
|-------|--------------|
| scene-sequencing | Core G/C/D analysis patterns reused |
| genre-conventions | Genre detection patterns sourced |
| character-arc | Arc type identification patterns sourced |
| dna-extraction | Function taxonomy borrowed |
| story-zoom | Output format compatible for comparison |
| revision | Similar structural analysis approach |
