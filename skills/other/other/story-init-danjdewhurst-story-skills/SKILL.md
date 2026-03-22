---
name: story-init
description: This skill should be used when the user asks to "start a new story", "initialize a story project", "create a story", "new book", "set up a story", or wants to begin a new fiction writing project from scratch.
---

# Story Initialization

## Overview

Initialize a new story project with a structured markdown folder layout. Creates the story bible, character registry, worldbuilding index, plot structure, and chapter tracker - all as cross-referenced markdown files with YAML frontmatter.

## When to Use

- Starting a new story, book, or fiction project
- Setting up the folder structure for an existing story idea
- NOT for adding to an existing story project (use the domain-specific skills instead)

## Workflow

1. Ask for basic story information:
   - Title
   - Genre and sub-genre
   - Brief synopsis (2-3 sentences)
   - Setting era/time period
   - Key themes (2-4)
   - POV style (first-person, third-person-limited, third-person-omniscient)
   - Tense (past, present)

2. Create the folder structure at the current working directory:

```
{story-title-kebab}/
├── story.md
├── characters/
│   └── _index.md
├── worldbuilding/
│   ├── _index.md
│   ├── locations/
│   └── systems/
├── plot/
│   ├── _index.md
│   ├── arcs/
│   └── timeline.md
└── chapters/
    └── _index.md
```

3. Populate `story.md` with the story bible:

```yaml
---
title: "{Title}"
genre: {genre}
sub-genre: {sub-genre}
setting-era: {era}
status: planning
themes:
  - {theme-1}
  - {theme-2}
pov: {pov-style}
tense: {tense}
---
```

Below the frontmatter, include sections:
- **Synopsis** - the 2-3 sentence synopsis provided
- **Tone & Style** - brief notes on the story's voice (derive from genre/themes)
- **Notes** - empty section for the user to fill in

4. Populate each `_index.md` with an empty registry:

**`characters/_index.md`:**
```markdown
---
type: character-registry
story: {story-title-kebab}
---

# Characters

## Registry

| Name | Role | Status | File |
|------|------|--------|------|
| *No characters yet* | | | |

## Family Trees

*No family trees defined yet.*

## Relationship Map

*No relationships defined yet.*
```

**`worldbuilding/_index.md`:**
```markdown
---
type: world-registry
story: {story-title-kebab}
---

# Worldbuilding

## World Overview

*Describe the world at a high level here.*

## Locations

| Name | Type | Region | File |
|------|------|--------|------|
| *No locations yet* | | | |

## Systems

| Name | Type | File |
|------|------|------|
| *No systems yet* | | |
```

**`plot/_index.md`:**
```markdown
---
type: plot-registry
story: {story-title-kebab}
structure: three-act
---

# Plot Structure

## Story Structure

**Model:** Three-Act Structure (adjust as needed)

## Arcs

| Name | Type | Status | File |
|------|------|--------|------|
| *No arcs yet* | | | |

## Theme Tracking

| Theme | Arcs | Chapters |
|-------|------|----------|
| *No themes tracked yet* | | |
```

**`plot/timeline.md`:**
```markdown
---
type: timeline
story: {story-title-kebab}
---

# Story Timeline

| When | Event | Arc | Chapter |
|------|-------|-----|---------|
| *No events yet* | | | |
```

**`chapters/_index.md`:**
```markdown
---
type: chapter-registry
story: {story-title-kebab}
---

# Chapters

## Registry

| # | Title | POV | Status | Word Count | File |
|---|-------|-----|--------|------------|------|
| *No chapters yet* | | | | | |

## Total Word Count: 0
```

5. Present a summary of what was created and suggest next steps:
   - "Add your first character" (triggers character-management skill)
   - "Start worldbuilding" (triggers worldbuilding skill)
   - "Define your plot structure" (triggers plot-structure skill)

## Conventions

These conventions apply across ALL story skills:

- **Kebab-case filenames** for all entity files (e.g., `sera-voss.md`, `ashen-citadel.md`)
- **YAML frontmatter** on every file for structured metadata
- **`_index.md`** files are authoritative registries for each domain
- **`story.md`** is the top-level bible read by all skills for context
- **Bidirectional cross-links** - when referencing another entity, update both files
- **Character identifiers** use the kebab-case filename without extension (e.g., `sera-voss`)
