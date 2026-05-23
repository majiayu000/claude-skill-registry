---
name: 40-02-module-boundaries
description: When to extract a module, what belongs together, what stays coupled. Prevents premature extraction and god modules alike.
---

# 40.02 Module Boundaries

A module is a file (or small group of files) that owns one concern. The question is never "can I extract this?" — it's "does this concern have its own reason to change?"

## When to Extract

Extract when **two or more** of these are true:

- **> 500 lines** — too much to hold in your head
- **Multiple concerns** — entity management AND connection lifecycle AND queries
- **Independent change reasons** — query functions change when UI needs change, not when connection protocol changes
- **Can't test in isolation** — the thing you want to test is trapped inside something you don't want to set up

Do NOT extract just because a file is large. A 800-line file with one concern (subscription wiring that genuinely shares lifecycle) is fine.

## What Belongs Together

Things that **change for the same reason** stay in the same module:

| Together | Why |
|----------|-----|
| `connect()` + `cleanupConnection()` + `scheduleReconnect()` | Connection lifecycle — all change when protocol changes |
| `upsertShip()` + `removeShip()` + `shipEntities` Map | Ship ECS management — all change when entity schema changes |
| `questAccept()` + `questComplete()` + `questAbandon()` | Quest domain actions — all change when quest system changes |

Things that **change for different reasons** go in different modules:

| Separate | Why |
|----------|-----|
| SQL query definitions vs. subscription orchestration | Queries change when schema changes; orchestration changes when connection protocol changes |
| Table → store callbacks vs. ECS entity management | Store wiring changes when store shape changes; ECS changes when rendering changes |
| Reducer wrappers vs. read-only queries | Writes change when server API changes; reads change when UI needs change |

## The Extraction Test

Before extracting, answer:

1. **What shared state does it need?** If it only reads from shared refs/Maps → easy extraction to standalone functions.
2. **What does it write?** If it writes closure-local `let` variables → move the state first (see 40.01), then extract.
3. **Does it need constructor-time values?** (world, renderer) → put them in a ref object set once at init. Not a factory.
4. **Does it reset on disconnect?** → It's connection lifecycle. Stays in the closure.

## The God Module Test

Your module might be a god module if:

- It has functions that don't call each other
- It imports from > 15 different modules
- You can draw a line through the file where "above" and "below" don't interact
- New features keep getting added to it because "it has access to everything"

## File Size Guidelines

| Lines | Assessment |
|-------|-----------|
| < 200 | Fine. Don't merge small modules to "reduce files." |
| 200-500 | Normal. Single concern, well-structured. |
| 500-1000 | Review. Probably has 2-3 concerns. Consider extraction. |
| > 1000 | Almost certainly a god module. Decompose. |
