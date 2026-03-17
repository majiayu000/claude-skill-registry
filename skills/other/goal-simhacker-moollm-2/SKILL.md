---
name: goal
description: Quest objectives that drive narrative — the WANTS of adventure
allowed-tools:
  - read_file
  - write_file
tier: 1
protocol: SCHEMA-MECHANISM
tags: [moollm, quest, objective, narrative, game]
related: [adventure, character, needs, hero-story]
adversary: aimlessness
---

# Goal

> *"A goal is not always meant to be reached. Often it serves simply as something to aim at."*
> — Bruce Lee

---

## What Is It?

A **Goal** is a quest objective that drives the adventure forward. It defines what the player is trying to achieve and when they've succeeded (or failed).

Goals create **narrative tension** — the gap between current state and desired state.

---

## Schema Mechanism Connection

From Gary Drescher's theory:

```
Context → Action → Result
```

Goals define the desired **Result** that motivates **Action**. The adventure is a laboratory for learning causal chains that achieve goals.

---

## Goal Properties

| Property | Purpose |
|----------|---------|
| `id` | Unique identifier |
| `name` | Short display name |
| `description` | What you're trying to achieve |
| `status` | pending, active, complete, failed |
| `complete_when` | Natural language condition |
| `fail_when` | When goal becomes impossible |
| `reward` | What you get on completion |
| `progress` | Partial completion tracking |

---

## Completion Conditions

Natural language conditions that compile to JS/PY:

```yaml
complete_when: "player has the treasure"
complete_when_js: "(ctx) => ctx.player.inventory.includes('treasure')"
```

---

## Rewards

Goals can grant various rewards:

```yaml
reward:
  buff: "Hero's Glory"           # Temporary effect
  item: "champion-medal"         # Object
  unlock: "secret-room"          # New access
  narrative: "The kingdom celebrates!"  # Story beat
```

---

## Progress Tracking

For multi-step goals:

```yaml
progress:
  collected: 3
  needed: 5
```

---

## Goal Hierarchies

Goals can nest:

```yaml
parent: defeat-dragon
children:
  - find-magic-sword
  - learn-dragon-weakness
  - reach-dragon-lair
```

Complete all children to complete the parent.

---

## Failure Conditions

Goals can fail:

```yaml
fail_when: "time reaches midnight AND prisoner is not freed"
fail_message: "You were too late."
```

---

## Examples

### Simple Quest

```yaml
goal:
  id: find-treasure
  name: "Find the Treasure"
  complete_when: "player has the treasure"
```

### Timed Challenge

```yaml
goal:
  id: rescue-mission
  name: "Save the Prisoner"
  complete_when: "prisoner is freed"
  fail_when: "10 turns pass without rescue"
  priority: urgent
```

### Collection Quest

```yaml
goal:
  id: gather-keys
  name: "Collect All Keys"
  complete_when: "player has 5 enchanted keys"
  progress:
    collected: 2
    needed: 5
```

---

## Related Skills

- [adventure](../adventure/) — Contains active goals
- [hero-story](../hero-story/) — Narrative structure
- [needs](../needs/) — Internal motivations

---

## Protocol Symbol

```
SCHEMA-MECHANISM — Goals drive causal learning
```
