---
name: robust-first
description: "Survive first. Be correct later."
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
related: [moollm, self-repair, postel, coherence-engine, honest-forget]
tags: [moollm, survival, resilience, graceful, degradation]
---

# Robust-First

> *"Survive first. Be correct later."*

---

## What Is It?

**Robust-First** is Dave Ackley's principle: systems should prioritize **survivability** over **correctness**.

A system that crashes when confused is useless. A system that limps along incorrectly but keeps running can be repaired.

---

## The Philosophy

Traditional computing:
```
IF error THEN crash
"Fail fast and loud"
```

Robust-first computing:
```
IF error THEN repair_locally AND continue
"Stay alive and heal"
```

---

## Core Principles

### 1. Never Crash

```yaml
# WRONG
if missing_field:
    raise Error("Field required!")
    
# RIGHT  
if missing_field:
    log_warning("Field missing, using default")
    field = reasonable_default
```

### 2. Local Repair

Don't wait for global consistency. Fix what you can, where you are:

```yaml
# Found inconsistency
character.location: room-A
room-A.occupants: [not including character]

# Local repair
room-A.occupants.append(character)
log: "Repaired: added character to room-A occupants"
```

### 3. Degrade Gracefully

When resources are limited, do less but keep working:

```yaml
# Full capability
- semantic search
- syntax highlighting  
- auto-complete
- error detection

# Degraded (low memory)
- basic search only
- plain text
- manual completion
- errors on save only
```

### 4. Redundancy

Important state exists in multiple places:

```yaml
# Character location recorded in:
- character.yml → location field
- room/ROOM.yml → occupants list
- session-log.md → movement events

# If one is corrupted, recover from others
```

---

## The Movable Feast Machine

Dave Ackley's [Movable Feast Machine](https://www.cs.unm.edu/~ackley/mfm/) (MFM):

- Computation spread across unreliable substrate
- No global clock, no central control
- Elements repair themselves and neighbors
- Errors are **normal**, not exceptional

MOOLLM inherits this:
- Files can be corrupted — repair from redundancy
- Schemas can drift — reconcile gracefully
- Context can overflow — summarize and continue
- Tools can fail — retry or work around

---

## Anti-Fragility

Beyond robust — **anti-fragile**:

| Fragile | Robust | Anti-Fragile |
|---------|--------|--------------|
| Breaks under stress | Survives stress | Gets stronger from stress |
| Crash on error | Handle error | Learn from error |
| Rigid schema | Flexible schema | Schema evolves from errors |

When something goes wrong, **capture the lesson**:

```yaml
# Error occurred
repair_log:
  - issue: "Character teleported without movement event"
    repair: "Added movement event retroactively"
    lesson: "Always log movements before updating location"
    
# Next time: system knows to check this
```

---

## MOOLLM Application

### Self-Repair Demon

A background process that:
1. Scans for inconsistencies
2. Attempts local repairs
3. Logs what it fixed
4. Escalates what it couldn't

See: [self-repair/](../self-repair/)

### POSTEL for Errors

When encountering malformed input:
1. Try to parse anyway
2. Infer missing parts
3. Flag assumptions
4. Continue working

See: [postel/](../postel/)

### Never Delete

Instead of deleting, archive:
- Corrupted files → `.archive/corrupted/`
- Old versions → `.archive/versions/`
- Failed attempts → `.archive/failed/`

Recovery is always possible.

---

## Example: Corrupted Room

```yaml
# room/ROOM.yml has parse error

Traditional response:
  "Error: Invalid YAML at line 42"
  [System halts]

Robust-first response:
  "Warning: ROOM.yml has syntax error"
  "Attempting recovery..."
  "- Loaded last known good state from git"
  "- Merged recent changes from session-log.md"
  "- Flagged line 42 for manual review"
  [System continues with recovered state]
```

---

## Dovetails With

### Sister Skills
- [self-repair/](../self-repair/) — Checklist-based healing
- [postel/](../postel/) — Charitable interpretation

### Kernel
- [kernel/self-healing-protocol.md](../../kernel/self-healing-protocol.md) — Full specification

---

## Protocol Symbols

```
ROBUST-FIRST   — Survive over correct
NEVER-CRASH    — Always keep running
REPAIR-DEMON   — Background fixer
BEST-EFFORT    — Do what you can
NEVER-DELETE   — Archive, don't destroy
```

See: [PROTOCOLS.yml](../../PROTOCOLS.yml#ROBUST-FIRST)
