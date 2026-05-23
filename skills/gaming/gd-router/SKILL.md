---
name: gd-router
description: Routes to appropriate Game Designer skills based on task keywords. Use when selecting which skill to invoke for a design task.
---

# Game Designer Skill Router

> "Right skill for the right design task."

## Quick Route by Keyword

| Trigger Keywords | Route To |
| ---------------- | -------- |
| **GDD Creation** | | |
| "create GDD", "start GDD", "no GDD", "initialize design" | `Skill("gd-gdd-creation")` |
| **Mechanics** | | |
| "mechanic", "gameplay system", "ability", "player action" | `Skill("gd-design-mechanic")` |
| **Level Design** | | |
| "level design", "map layout", "environment design" | `Skill("gd-design-level")` |
| **Character** | | |
| "character", "hero", "skin", "avatar" | `Skill("gd-design-character")` |
| **Weapons** | | |
| "weapon", "gun", "item", "equipment" | `Skill("gd-design-weapon")` |
| **Game Loop** | | |
| "game loop", "match flow", "session structure" | `Skill("gd-design-game-loop")` |
| **Playtesting** | | |
| "playtest", "test gameplay", "validate design" | `Skill("gd-validation-playtest")` |
| "GDD review", "design gaps", "GDD analysis" | `Skill("gd-playtest-gdd-review")` |
| "skill gap", "missing skill" | `Skill("gd-skill-gap-analysis")` |
| **Assets** | | |
| "asset performance", "optimize 3D" | `Skill("gd-assets-impact-analysis")` |
| "check assets", "what assets exist" | `Task({ subagent_type: "gamedesigner-asset-analyst", ... })` |
| **Design Sessions** | | |
| "design session", "Boardroom Retreat" | `Skill("gd-thermite-integration")` |
| **Research** | | |
| "visual ref", "art reference" | `Task({ subagent_type: "gamedesigner-visual-reference-researcher", ... })` |
| "Splatoon", "Arc Raiders", "reference game" | `Task({ subagent_type: "gamedesigner-reference-game-researcher", ... })` |

## Skill Dependencies

```
gd-validation-playtest ──┬──▶ gd-playtest-gdd-review
                           └──▶ gd-skill-gap-analysis
```

## Common Combinations

| Task | Skills |
|------|--------|
| New GDD | `gd-gdd-creation` + `gd-thermite-integration` |
| New Mechanic | `gd-design-mechanic` + `gd-thermite-integration` |
| Full Playtest | `gd-validation-playtest` + `gd-playtest-gdd-review` + `gd-skill-gap-analysis` |
| Asset Request | `gd-assets-impact-analysis` + `asset-analyst` sub-agent |
