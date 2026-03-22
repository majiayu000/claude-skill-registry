---
name: time
description: "Motto: Time flows as the story requires."
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
related: [simulation, adventure, buff, needs, action-queue, speed-of-light, session-log]
tags: [moollm, turns, duration, narrative, flow]
---

# Time Skill

Simulation turns vs LLM iterations.

**Motto:** *"Time flows as the story requires."*

## Key Concepts

- **Simulation turns** — Game time, what mechanics track
- **LLM iterations** — Meta-level, one response
- **They're not the same!** One LLM response might be 0, 1, or many turns

## Turn Definition

| Action | Turns |
|--------|-------|
| GO NORTH | 1 |
| PAT TERPIE | 1 |
| LOOK | 0 |
| INVENTORY | 0 |
| Pet all 8 kittens | 8 |
| Take a nap | ~10 |

## Duration Types

- **Turns** — X simulation turns (primary unit)
- **Conditional** — Until condition met
- **While present** — While in location/with item
- **Permanent** — Until explicitly removed

## See Also

- [buff](../buff/) — Buff durations use simulation turns
- [needs](../needs/) — Needs decay over simulation turns
