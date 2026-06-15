---
name: atlas
description: >-
  The Atlas engine — turn any goal into a validated PRD and an executable, verified
  task graph. Brand-name entrypoint; a thin alias for the `go` orchestrator. Use when
  the user types /prd:atlas, says "I want to build", or asks for a PRD / task-driven build.
user-invocable: true
allowed-tools:
  - Skill
---

# atlas (entrypoint alias)

This is the brand-name entrypoint for the Atlas engine. It holds no procedure of its
own — **immediately invoke the `go` orchestrator** via the Skill tool (`/prd:go`).

`go` reads pipeline state and dispatches to the correct phase
(SETUP → DISCOVER → GENERATE → HANDOFF → EXECUTE). Do not duplicate that routing here.
