---
name: sc-kanban
version: 0.8.0
description: Kanban state machine orchestration with provider abstraction
---

# sc-kanban Skill (v0.7.0 draft)

## Purpose
Invoke kanban agents via Agent Runner to query and transition cards across backlog/board/done using shared board config (`.project/board.config.yaml`).

## Flow
1. Load and validate board config (fail closed on errors).
2. If `provider=kanban`: call `kanban-query` or `kanban-transition` via Agent Runner.
3. If `provider=checklist`: call checklist fallback agent defined in config (same v0.5 envelope).

## Inputs
- Command args from `/kanban` (action, card selector, target status, filters).
- Workspace files: backlog.json, board.json, done.json.

## Outputs
- v0.5 envelope with card data or gate failure details (kanban provider), or checklist results when provider=checklist.

## Notes
- Gate execution, PR/worktree checks, and scrubbing occur inside `kanban-transition` agent.
- Keep envelopes fenced JSON only.*** End Patch
