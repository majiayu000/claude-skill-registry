---
name: biome-pack
description: Create and integrate a new biome pack (docs, data, art stubs)
compatibility: opencode
---
# Skill: New biome pack

## Objective
Make adding a new biome a predictable checklist-driven workflow.

## Steps
1) Create docs folder: `docs/biomes/<biome_id>/`
- Start from `docs/biomes/BIOME_TEMPLATE.md`

2) Create data stubs: `game/data/biomes/<biome_id>/`
- palette id references
- encounter table stubs

3) Create art stubs
- `art/palettes/<biome_id>.palette.json`
- `art/ramps/<biome_id>_ramp_4.png`

4) Add at least one area scene stub under `game/scenes/areas/<biome_id>/`

## Verification
- Biome appears in biome list
- Placeholder area can load and be traversed
