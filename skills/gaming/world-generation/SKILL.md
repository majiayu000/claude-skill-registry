---
name: world-generation
description: "Motto: The world grows where curiosity leads."
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
related: [room, character, incarnation, container, adventure, party, constructionism, empathic-templates]
tags: [moollm, procedural, creation, dynamic, exploration]
---

# World Generation Protocol

> Dynamic world creation — questions create places.
> *"The world grows where curiosity leads."*

## Core Principle

**Don't pre-generate everything. Generate on demand.**

When a player asks about a place that doesn't exist, create it. Questions expand the world. Exploration IS creation.

```
Player: "What's north?"
DM: *creates north*
```

## Generation Philosophy

```yaml
# What triggers world generation
generation_triggers:
  questions: "Where did the grue come from?"
  statements: "There must be a library somewhere!"
  actions:
    DIG: "tunnel"
    CLIMB: "passage"
  quests: "Objective location generates itself"
  exploration: "Walking beyond known areas"
```

## Methods

### CREATE - Generate New Place

```yaml
invoke: CREATE
params:
  seed: "Starting concept or name"
  style: "World style (fantasy, sci-fi, modern)"
  parent: "What area this connects to"
effect:
  - Create directory for new place
  - Generate ROOM.yml with properties
  - Add exits connecting to parent
  - Optionally populate with objects/NPCs
```

### EXPAND - Add to Existing Area

```yaml
invoke: EXPAND
params:
  from: "Existing place"
  direction: "north/south/etc or conceptual"
  hints: "Optional flavor hints"
effect:
  - Generate adjacent room
  - Add bidirectional exits
  - Inherit parent's atmosphere with variations
```

### CONNECT - Link Two Areas

```yaml
invoke: CONNECT
params:
  a: "First place"
  b: "Second place"
  type: "door/portal/path/secret"
effect:
  - Add exit from A to B
  - Add exit from B to A (unless one-way)
  - Update both ROOM.yml files
```

## Directory Inheritance

Directories carry behavioral defaults that children inherit:

| Parent Directory | Children Inherit |
|-----------------|------------------|
| `maze/` | Dark, twisty, grue-friendly |
| `basement/` | Damp, underground, echoing |
| `tower/` | Height, wind, views, vertigo |
| `dungeon/` | Cells, guards, escape themes |
| `garden/` | Outdoor, weather, growing |
| `library/` | Books, quiet, knowledge |
| `market/` | Vendors, crowds, commerce |

## Topology Patterns

| Pattern | Structure | Use Case |
|---------|-----------|----------|
| **Twisty maze** | Randomized connections | Challenge, getting lost |
| **Grid** | Regular X/Y layout | Cities, chessboards |
| **Star** | Hub with spokes | Crossroads, central plaza |
| **Loop** | Circular path | Racing, time loops |
| **Tree** | Branching, dead ends | Dungeons, boss rooms |
| **Web** | Many cross-connections | Complex social spaces |

## Generation Seeding

### From Questions

```
Q: "Where does the blacksmith live?"
A: Creates blacksmith-quarters/ with:
   - Forge room
   - Living quarters
   - Connected to market/
```

### From Actions

```
Action: DIG
Creates: tunnel/ or cellar/
   - Connects to current room
   - Darkness, rough-hewn walls
   - Possible discoveries
```

### From Quests

```
Quest: "Find the ancient tome"
Creates: hidden-archive/ somewhere logical
   - Contains the tome
   - Appropriate guardians
   - Connected via discoverable path
```

## Lazy Evaluation

```yaml
principle: "Don't create until needed"

strategy:
  - Player enters room: generate exits (names only)
  - Player asks about exit: generate room behind it
  - Player ignores exit: it remains potential
  
benefits:
  - Infinite worlds in finite storage
  - Every playthrough unique
  - Player choices shape reality
```

## State

```yaml
generation_state:
  seed: 42                    # Reproducibility
  style: "fantasy"            # World genre
  generated_places: []        # What exists
  pending_exits: []           # Named but not yet created
  topology: "organic"         # Generation pattern
```

## Safety Guidelines

- Maintain **consistency** — don't contradict established facts
- Respect **player agency** — their discoveries are canon
- Preserve **mystery** — not everything needs explanation
- Allow **emergence** — unexpected connections enrich world

## Integration

| Skill | Integration |
|-------|-------------|
| **room** | Generated places are rooms |
| **adventure** | World generation serves the adventure |
| **character** | NPCs generated with their locations |
| **worm** | Worms can trigger generation by crawling |

## Example Session

```
> GO NORTH
The path leads into unexplored territory...

[CREATE: forest-path/]
You find yourself on a narrow forest path. Tall oaks 
loom overhead. The trail continues east and west.

> WHAT'S EAST?
[EXPAND: from=forest-path, direction=east]
Through the trees, you glimpse an ancient stone 
structure — perhaps a ruin or shrine.

> GO EAST
[CREATE: old-shrine/]
A weathered shrine stands in a small clearing...
```
