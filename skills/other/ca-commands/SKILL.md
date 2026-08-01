---
name: ca-commands
description: Show the codeArbiter command catalog — the public command list and what each routes to.
argument-hint: (none)
---

# /ca-commands — command catalog

Present the public command list. Read-only, no state change.

## Flow

1. Read the quick-reference table from `<plugin-root>/COMMANDS.md` — the single source of truth
   for the catalog.
2. Output that table only — command, one-line description, route. No prose walkthrough, and no
   second copy maintained here (a hard-coded table drifts against `COMMANDS.md`).

## Hard gate

Read-only. MUST NOT modify a file or route to a skill. MUST render from `COMMANDS.md`, never from a
catalog copied into this file. Output the catalog only.
