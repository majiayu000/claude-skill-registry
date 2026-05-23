---
name: mcaf-architecture-overview
description: "Create or update `docs/Architecture/Overview.md` (architecture diagrams): maintain Mermaid diagrams for system/modules, interfaces/contracts, and key classes/types; document dependency rules; link to ADRs/features. Use when onboarding, refactoring, or adding modules/boundaries."
compatibility: "Requires repository write access; produces Markdown docs with Mermaid diagrams."
---

# MCAF: Architecture Overview

## Output

- `docs/Architecture/Overview.md` (create or update)

## Architecture Thinking (keep it a map)

This doc is the **global map**: boundaries, modules, and dependency rules.

- Keep it lean and structural:
  - modules/boundaries + responsibility + dependency direction
  - Mermaid diagrams are the primary context:
    - system/module map (blocks + dependency direction)
    - interfaces/contracts map (how modules talk)
    - key classes/types map (high-signal only; not exhaustive)
- Treat it as the main “start here” card for humans and AI agents:
  - diagram elements must use real names (no placeholders)
  - every diagram element must have an explicit reference link (docs/code) so an agent can navigate without repo-wide scanning
  - keep diagrams readable; if a diagram becomes “spaghetti”, split by boundary and link out
- Keep behaviour out of the overview:
  - feature flows live in `docs/Features/*`
  - decision-specific diagrams/invariants live in `docs/ADR/*`
- Anti-“AI slop” rule: never invent components/services/DBs — only document what exists (or what this change will explicitly add).

## Workflow

1. Open `docs/Architecture/Overview.md` if it exists; otherwise start from `docs/templates/Architecture-Template.md`.
   - Ensure it contains a short `## Scoping (read first)` section (this is how we prevent “scan everything” behaviour).
2. Identify the **real** top-level boundaries:
   - entry points (HTTP/API, CLI, UI, jobs, events)
   - modules/layers (group by folders/namespaces, not individual files)
   - external dependencies (only those that actually exist)
3. Fill the **Summary** so a new engineer can orient in ~1 minute.
4. Maintain the Mermaid diagrams (the map people and agents start from):
   - **system/module map**: keep it small (roughly 8–15 nodes), label arrows (calls/events/reads/writes)
   - **interfaces/contracts map**: show ports/interfaces, APIs, events, queues, file formats (only what exists)
   - **key classes/types map**: capture the main types that matter across modules (avoid inventories)
   - don’t invent DB/queues/services/modules that aren’t present
5. Fill the module index:
   - one row per diagram node (not every internal module/class)
   - responsibilities and “depends on” must be concrete
   - prefer a short navigation list with links over big tables/inventories
6. Write explicit dependency rules:
   - what is allowed
   - what is forbidden
   - how integration happens (sync / async / shared lib)
7. Add a short “Key decisions (ADRs)” section:
   - link to the ADRs that define boundaries, dependencies, and major cross-cutting patterns
   - keep it link-based (no detailed flows here)
8. Link out to deeper docs:
   - ADRs for key decisions
   - Features for behaviour details
   - Testing/Development for how to run and verify

## Guardrails

- Do not list every file/class. This is a **map**, not an inventory (key classes/types only).
- Keep the document stable: update it when boundaries or interactions change.
