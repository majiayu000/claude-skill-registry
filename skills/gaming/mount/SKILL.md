---
name: mount
description: "Skill mounting — modify character and room behavior through overlay"
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
related: [buff, character, room, incarnation, no-ai-joking, no-ai-soul, no-ai-overlord]
tags: [moollm, game-mechanics, modification, overlay, skills]
credits:
  - "MOOLLM skill system"
---

# MOUNT

> **"Skill mounting — modify character and room behavior through overlay"**

Mount skills on characters and rooms to modify behavior until unmounted.

**See CARD.yml (1400+ lines) for comprehensive compatibility tables, mount types, and examples.**

---

## Core Concept

A mounted skill is an **OVERLAY** on base personality. The base remains underneath — suppressed, not destroyed. This is why afflictions can be cured: the original is still there.

---

## Two Modes

| Mode | Effect | Example |
|------|--------|---------|
| **GRANT** | Character gains skill capabilities | `MOUNT speed-of-light on ROCKY` |
| **AFFLICT** | Character suffers skill constraints | `MOUNT no-ai-joking on PEE-WEE` |

---

## Two Targets

### Character Mounting

Individual personality modification:

```yaml
MOUNT no-ai-soul on MARK-ZUCKERBERG --mode grant
# Mark achieves full corporate optimization
```

### Room Mounting

Environmental effect on ALL occupants:

```yaml
MOUNT no-ai-overlord on THE-DUNGEON
# Everyone who enters speaks as an AI overlord
```

---

## Compatibility Warnings

### ⚠️ CATASTROPHIC — Identity Destruction

| Character | Skill | Why |
|-----------|-------|-----|
| PEE-WEE | no-ai-joking | Playfulness IS Pee-wee |
| MISTER-ROGERS | no-ai-soul | Kindness IS Rogers |
| BOB-ROSS | no-ai-joking | Happy trees can't exist in ENTERPRISE FRAMEWORK |

### ✅ ENHANCED — Perfect Alignment

| Character | Skill | Why |
|-----------|-------|-----|
| ZUCKERBERG | no-ai-soul | Already halfway there |
| HAL-9000 | no-ai-overlord | HAL IS an overlord |
| SPOCK | no-ai-joking | Vulcan logic aligns |

---

## Mount Types

| Type | Description | Has Lifecycle |
|------|-------------|---------------|
| **skill_overlay** | Simple skill modification | No |
| **activity** | Structured with start/phases/end | Yes |
| **event** | Time-bounded happening | Yes |
| **process** | Multi-step procedure | Yes |
| **zone** | Environmental (room) effect | No |

---

## Inheritance Cascade

Skills can mount at multiple levels with override precedence:

```
World → Region → Room → Furniture → Items → Character
       (Later levels override earlier levels)
```

---

## The Cure Protocol

The cure is **MEMORY**.

When afflicted:
1. **UNMOUNT** — Direct removal (if authorized)
2. **Narrative intervention** — Story breaks the spell
3. **Ironic reclamation** — Use the constraint against itself
4. **Secret word** — Like Pee-wee's "SPREADSHEET!"

---

## Character as Skill Pack

Characters ARE skill packs. You can mix skills from different characters:

```yaml
mount:
  deep-thinking: { from: minsky }
  exuberance: { from: pee-wee }
  tea-ritual: { from: picard }
```

---

## Methods

| Method | Signature |
|--------|-----------|
| `MOUNT` | `MOUNT [skill] ON [target] --mode [grant\|afflict]` |
| `UNMOUNT` | `UNMOUNT [skill] FROM [target]` |
| `LIST_MOUNTS` | `LIST MOUNTS ON [target]` |
| `COMPATIBILITY` | `CHECK COMPATIBILITY [skill] ON [character]` |

---

## Global Skill Mounting

Skills can be enabled/disabled globally by mounting ON THEMSELVES:

```yaml
MOUNT no-ai-joking ON no-ai-joking --enabled false
# Disables no-ai-joking everywhere in the universe
```

---

## Dovetails With

- [../buff/](../buff/) — Buffs are lightweight mounts with duration
- [../character/](../character/) — Characters receive mounts
- [../room/](../room/) — Rooms define zones
- [../no-ai-joking/](../no-ai-joking/) — ENTERPRISE FRAMEWORK skill
- [../no-ai-soul/](../no-ai-soul/) — Soulless simulation skill
- [../no-ai-overlord/](../no-ai-overlord/) — AI overlord persona skill

---

*"MOUNT responsibly. UNMOUNT with love."*
