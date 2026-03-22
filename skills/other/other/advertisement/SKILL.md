---
name: advertisement
description: Objects announce what they can do — The Sims style
allowed-tools:
  - read_file
  - write_file
  - list_dir
tier: 1
protocol: ADVERTISEMENT
related: [card, object, society-of-mind, room, action-queue, coherence-engine, needs]
tags: [moollm, game, interaction, sims, behavior, autonomy]
---

# Advertisement

> *"Objects don't wait to be used — they announce what they can do."*

---

## What Is It?

**Advertisement** is The Sims-style object interaction: every object in a room broadcasts its available actions, scored by relevance to the current context.

Instead of the user memorizing commands, objects **advertise** what's possible:

```
You approach the workbench.

Available actions (sorted by relevance):
  ⭐ CRAFT tool (you have materials)
  • EXAMINE blueprints
  • ORGANIZE parts
  • MORE options...
```

---

## The Sims Connection

In **The Sims**, objects have "advertisements" — each interaction scores based on:
- The Sim's current needs (hunger, fun, social)
- Object properties (a fridge scores high for hunger)
- Context (can't use stove if broken)

This extensible object architecture was **key to The Sims' massive success**:
- **User-created objects** — anyone could make new furniture, appliances, characters
- **Expansion packs** — just drop in new objects with their advertisements
- **No code changes** — objects self-describe their behaviors
- **Infinite variety** — the community created millions of objects

The same YAML file that defines what an object *is* also defines what it *can do*. Plug-in architecture for free.

MOOLLM applies this to **any object**:

```yaml
# workbench.yml
type: object
advertisements:
  - action: CRAFT
    score_if: "has_materials AND has_skill"
    satisfies: [productivity, creativity]
    
  - action: EXAMINE
    score_if: "always"
    satisfies: [curiosity]
    
  - action: MORE
    score_if: "always"
    satisfies: [exploration]
```

---

## How It Works

### 1. Objects Broadcast

Every object in the room has an `advertisements` list:

```yaml
advertisements:
  - action: USE
    description: "Activate this tool"
    preconditions: [in_inventory, charged]
    score: 80
    
  - action: EXAMINE
    description: "Look closely"
    preconditions: []  # always available
    score: 50
```

### 2. Context Scores

Scores adjust based on:
- **Character needs** — hungry character scores FOOD higher
- **Current goals** — research goal scores EXAMINE higher
- **Environment** — dark room scores LIGHT higher

### 3. Pie Menu Appears

Top actions surface in the [PIE-MENU](../room/):

```
    [CRAFT]
       ⭐
[ORGANIZE] • [EXAMINE]
       •
    [MORE]
```

Center = highest score = default action.

---

## Autonomous Selection

For **autonomous agents**, advertisements enable self-direction:

```
Agent evaluates all objects in room:
  workbench: CRAFT (85), EXAMINE (50)
  bookshelf: READ (70), ORGANIZE (30)
  door: EXIT (40)
  
Agent selects: CRAFT at workbench (score 85)
```

No hardcoded behavior. Objects define possibilities. Agent selects based on goals.

---

## Example: Smart Room

```yaml
# research-lab/ROOM.yml
objects:
  - microscope:
      advertisements:
        - action: ANALYZE_SAMPLE
          score_if: "has_sample"
          score: 90
        - action: CALIBRATE
          score_if: "accuracy < 0.9"
          score: 60
          
  - notebook:
      advertisements:
        - action: WRITE_NOTES
          score_if: "has_observations"
          score: 75
        - action: REVIEW
          score: 40
          
  - coffee_maker:
      advertisements:
        - action: BREW
          score_if: "fatigue > 0.3"
          score: 65
        - action: CLEAN
          score_if: "uses > 5"
          score: 30
```

Agent enters, sees:
```
Top actions:
  1. ANALYZE_SAMPLE at microscope (90) — you have a sample!
  2. WRITE_NOTES at notebook (75) — observations pending
  3. BREW at coffee_maker (65) — you're a bit tired
```

---

## SimAntics Heritage

This is **SimAntics** — The Sims' behavioral engine:

| SimAntics | MOOLLM |
|-----------|--------|
| Object advertisement | `advertisements:` list in YAML |
| Motive scores | Context-based scoring |
| Autonomous selection | Agent picks highest-scored action |
| Pie menu | [PIE-MENU](../room/) for user interaction |

Don Hopkins worked on SimAntics. This is that tradition, for LLM agents.

---

## HyperCard-Style Event Bubbling

When you click an advertised action, it triggers a **symbolic event** that bubbles up:

```
Click CRAFT on workbench

Event path:
  1. workbench (object)     → handles CRAFT? no, pass up
  2. workshop/ (room)       → handles CRAFT? no, pass up  
  3. building/ (parent)     → handles CRAFT? no, pass up
  4. world/ (root)          → handles CRAFT? no, check inheritance
  5. workbench-prototype    → handles CRAFT? YES → execute
```

Just like HyperCard: events bubble from button → card → background → stack.

### Containment Tree (Spatial)

Events bubble **up** the room hierarchy:

```
object in room in parent-room in world
   ↑         ↑              ↑        ↑
              event bubbles up
```

### Inheritance Graph (Prototype)

If no handler in containment tree, check the **prototype chain**:

```
workbench
   ↓ inherits from
furniture-prototype  
   ↓ inherits from
object-prototype     → has default CRAFT handler!
```

### Combined Path

```yaml
# Event resolution order:
1. The object itself
2. Parent room
3. Grandparent room
4. ... up to world root
5. Object's prototype
6. Prototype's prototype
7. ... up to root prototype
```

First handler that responds wins. Unhandled events can:
- Log a warning
- Trigger POSTEL (charitable interpretation)
- Invoke a default handler

### Example: Custom Behavior

```yaml
# workshop/ROOM.yml
handles:
  CRAFT: |
    # Room-level craft handler
    Check if character has required skill.
    Check if materials available in room.
    If conditions met, delegate to object.
    Otherwise, suggest where to get materials.
```

The room intercepts CRAFT before it reaches the object, adding room-specific logic.

---

## Dovetails With

- [Room](../room/) — Where objects live and advertise
- [PIE-MENU](../room/) — How advertisements surface to users
- [SNAP-CURSOR](../room/) — Context-aware object interaction
- [Coherence Engine](../coherence-engine/) — Evaluates and selects actions
- [Trading Card](../card/) — Cards can advertise too
- [Rubric](../rubric/) — **Scoring criteria** for advertisement evaluation
- [Scoring](../scoring/) — How scores are calculated and valued

---

## Protocol Symbols

```
ADVERTISEMENT        — Objects announce available actions
AUTONOMOUS-SELECTION — Agent picks based on scores
SIMANTICS            — The Sims behavioral model
PIE-MENU             — Radial display of options
FLY-UNDER-RADAR      — Normalize through defaults
PROCEDURAL-RHETORIC  — Rules carry ideology
```

See: [PROTOCOLS.yml](../../PROTOCOLS.yml)

---

## The Deep Insight

From [SIMANTICS](../../PROTOCOLS.yml):

> *"The Sims' AI isn't centralized — it's distributed throughout objects."*
> *"A refrigerator knows it offers food. A bed knows it offers sleep."*
> *"The Sim chooses from what's advertised nearby."*

This IS MOOLLM's architecture. Objects self-describe. The coherence engine orchestrates. Intelligence is **distributed** throughout the world.

The advertisements ARE the AI.
