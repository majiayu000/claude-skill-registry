---
name: simulation
description: "Abstract base for runtime state — adventure, city-sim, ecosystem all inherit from this"
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
related: [adventure, society-of-mind, time, party, character, needs, buff, action-queue, prototype, speed-of-light]
tags: [moollm, runtime, state, turns, engine]
---

# Simulation Skill

**Abstract base** for runtime state management. Concrete simulations (adventure, city-sim, ecosystem) inherit from this.

**Motto:** *"The simulation is the world. The world is the simulation."*

> [!IMPORTANT]
> **This is the abstract base.** Don't create `SIMULATION.yml` directly.
> Use `ADVENTURE.yml` (for narrative exploration) or create your own concrete type.
> The concrete file INCLUDES all simulation properties plus type-specific ones.

## Key Concepts

- **SIMULATION.yml** — Source of truth for "now"
- **Global parameters** — Configurable via chat
- **Git time machine** — Commits = deterministic undo
- **Turn tracking** — Increments on significant actions

## Global Parameters

### Time Control

| Parameter | Default | Chat Command |
|-----------|---------|--------------|
| `paused` | false | `PAUSE` / `RESUME` |
| `advancement` | normal | `SET TIME ADVANCEMENT [none\|slow\|normal\|fast]` |
| `turn` | 0 | `TICK [n]` / `REWIND [n]` |

### Git Automation

| Parameter | Default | Chat Command |
|-----------|---------|--------------|
| `auto_commit` | false | `SET AUTO COMMIT [on\|off]` |
| `auto_push` | false | `SET AUTO PUSH [on\|off]` |
| `git_remote` | origin | `SET GIT REMOTE [name]` |
| `git_branch` | main | `SET GIT BRANCH [name]` |

### Display

| Parameter | Default | Chat Command |
|-----------|---------|--------------|
| `narration_level` | normal | `SET NARRATION [minimal\|normal\|verbose]` |
| `show_mechanics` | false | `SET SHOW MECHANICS [on\|off]` |
| `debug_mode` | false | `DEBUG [on\|off]` |

### Output (all ON by default)

| Parameter | Default | Chat Command |
|-----------|---------|--------------|
| `write_to_chat` | **true** | `SET CHAT OUTPUT [on\|off]` |
| `write_to_transcript` | **true** | `SET TRANSCRIPT [on\|off]` |
| `transcript_path` | ./README.md | `SET TRANSCRIPT PATH [path]` |
| `include_yaml_islands` | **true** | `SET YAML ISLANDS [on\|off]` |
| `include_links` | **true** | `SET LINKS [on\|off]` |
| `link_format` | markdown | `SET LINK FORMAT [markdown\|plain\|none]` |

Transcript paths are relative to adventure directory:
- `./README.md` (default)
- `./logs/session-log.md`
- `./narrative/chapter-1.md`

**Example output with all flags ON:**

> You're in the [pub](./pub/ROOM.yml) with [Marieke](./pub/budtender-marieke.yml).
> 
> You examine the lamp:
> ```yaml
> object:
>   id: brass-lamp
>   state: lit
>   oil: 75%
>   # Warm. Faithful. Flickering slightly.
> ```

### Gameplay

| Parameter | Default | Chat Command |
|-----------|---------|--------------|
| `difficulty` | normal | `SET DIFFICULTY [easy\|normal\|hard]` |

## SIMULATION.yml Structure

```yaml
simulation:
  turn: 47
  paused: false
  
parameters:
  git:
    auto_commit: true
    auto_push: false
    
  gameplay:
    difficulty: normal
    permadeath: false
    
  display:
    show_mechanics: false
    
player:
  character: characters/don-hopkins/
  location: pub/
  
party:
  members: [characters/don-hopkins/, pub/cat-cave/terpie.yml]
  
selection:
  targets: []
  
active_buffs: []
world_state: {}
flags: {}
```

## Commands

| Command | Effect |
|---------|--------|
| `STATUS` | Current simulation state |
| `SHOW SETTINGS` | List all parameters |
| `SET [param] [value]` | Configure parameter |
| `GET [param]` | Query parameter value |
| `PAUSE` / `RESUME` | Time control |
| `TICK [n]` | Force advance turns |
| `SAVE` / `LOAD` | Persistence |

## Git Time Machine

With `auto_commit: true`, every turn is a git commit:

```bash
# Commits look like:
Turn 47: Entered pub
Turn 48: Ordered Monkey's Blessing
Turn 49: Pet Terpie (+Serenity buff)
```

**Time travel commands:**
- `REWIND [n]` — Go back n turns
- `BRANCH [name]` — Create alternate timeline
- `TIMELINES` — List all branches
- `MERGE TIMELINE [branch]` — Merge narratives

## See Also

- [time](../time/) — Turn tracking, duration
- [party](../party/) — Party and selection
- [buff](../buff/) — Active effects
- [character](../character/) — Player state
- [adversarial-committee](../adversarial-committee/) — **Decision-making** within simulation
- [speed-of-light](../speed-of-light/) — Multi-agent simulation in one call