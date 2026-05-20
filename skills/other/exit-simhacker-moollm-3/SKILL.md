---
name: exit
description: Navigation links between rooms — the edges of the memory palace
allowed-tools:
  - read_file
  - write_file
tier: 1
protocol: PIE-MENU-TOPOLOGY
tags: [moollm, navigation, room, topology, pie-menu]
related: [room, adventure, memory-palace]
adversary: dead-end
---

# Exit

> *"Every exit is a promise of adventure."*
> — The Gezelligheid Grotto Guest Book

---

## What Is It?

An **Exit** is a navigation link connecting one room to another. In MOOLLM's spatial architecture, exits are the EDGES of the memory palace graph.

Exits can be:
- **Simple** — just a destination
- **Guarded** — require conditions to pass
- **Hidden** — discoverable through exploration
- **Metaphysical** — conceptual rather than physical

---

## Pie Menu Topology

Don Hopkins' **pie menu** insight: direction IS meaning.

| Direction | Purpose |
|-----------|---------|
| **N/S/E/W** | "Highway" links to major rooms |
| **NW/NE/SW/SE** | "Grid" links to expandable sub-rooms |
| **UP/DOWN** | Vertical transitions |
| **IN/OUT** | Conceptual transitions |

Cardinal directions form the **spiderweb** — the main navigation network.
Diagonal directions form **grids** — expandable arrays of sub-rooms.

---

## Guard System

Guards are natural language conditions that control access:

```yaml
guard: "player has the brass key"
guard_js: "(ctx) => ctx.player.inventory.includes('brass-key')"
guard_py: "lambda ctx: 'brass-key' in ctx.player.inventory"
```

The `guard` field contains human-readable intent.
The `guard_js` and `guard_py` fields contain compiled code.

The adventure compiler emits `COMPILE_EXPRESSION` events for guards that need compilation.

---

## Exit Types

### Simple Exit

```yaml
north:
  destination: ../maze/room-a/
  description: "A dark passage leads north."
```

### Guarded Exit

```yaml
east:
  destination: ../treasury/
  description: "A heavy iron door."
  guard: "player has treasury key"
  locked: true
  lock_message: "The door won't budge."
  unlock_with: "treasury-key"
```

### Hidden Exit

```yaml
down:
  destination: ../secret-cellar/
  hidden: true
  hint: "The rug seems oddly placed..."
```

### One-Way Exit

```yaml
down:
  destination: ../pit/
  one_way: true
  description: "A slide into darkness. No going back."
```

### Metaphysical Exit

```yaml
inward:
  destination: ../consciousness/
  metaphysical: true
  description: "Close your eyes and think about who you really are."
```

---

## Memory Palace Integration

From Frances Yates' "The Art of Memory":

> *"The method of loci places items at specific locations along an imagined journey."*

Every exit is a **doorway** in the memory palace. The direction encodes meaning. Players navigate by spatial memory.

---

## Related Skills

- [room](../room/) — Where exits live
- [adventure](../adventure/) — Uses exits for navigation
- [memory-palace](../memory-palace/) — Exits as mnemonic paths

---

## Protocol Symbol

```
PIE-MENU-TOPOLOGY — Direction IS meaning
```
