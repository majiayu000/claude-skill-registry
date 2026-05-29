---
name: art-pipeline-nano-banana
description: Use nano banana (Gemini CLI) to generate references and inputs for the deterministic 2.5D pipeline
compatibility: opencode
---
# Skill: Art Pipeline (nano banana as input generator)

## Objective
Use nano banana to generate **inputs** (concept refs, mood boards, modular parts) while keeping final game assets deterministic via templates + palettes.

This repo does **not** accept “AI images dropped directly into game/assets” as final art.

## What nano banana is allowed for
- Mood boards for biomes (to derive palettes)
- Concept sheets for props/characters (to guide modeling)
- UI style exploration (boxes, typography, icon language)

## Where outputs must go
All generated images must land under:
- `art/source/ai/nanobanana-output/`

## Prompting patterns (examples)

### Biome mood board (Bubblegum Bay)
- Goal: palette direction (NOT final textures)
- Prompt template:
  - “Landscape-only JRPG biome mood board, low-poly toon, 4-band shading feel, playful pastel seaside town, calm ocean blues, candy accents, no text, 6 panels.”

### Prop concept sheet
- “Turnaround concept sheet for a low-poly toon prop: <prop>, simple shapes, clean silhouettes, no text, white background, 3 views.”

### UI exploration
- “Turn-based JRPG UI mockup, top HUD with portraits and HP/MP bars, bottom command menu boxes, cozy kid-friendly, no cassette theme, no text labels.”

## Next step (convert to deterministic assets)
After generation:
1) Extract palette candidates (tools/python)
2) Build the prop/character in Blender using templates
3) Bake sprites/backgrounds via scripts
4) Validate outputs

## Acceptance checks
- Any nano banana output used in production must have:
  - a recipe stub referencing it
  - a deterministic conversion step (Blender bake or modeling)