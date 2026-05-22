---
name: compound-workflows
description: Use Plan → Work → Review → Compound to compound skills and maintain project context.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-27T17:03:09.731823+00:00"
  updated_at: "2026-01-27T17:03:09.731823+00:00"
  version: "1"
  tags: "workflow,compounding"
---

<!-- BEGIN:compound:skill-managed -->
## Purpose

This repository uses a loop:

1. **Plan**: turn an idea into a ticketed plan (loom ticket), informed by recalled notes (loom memory).
2. **Work**: execute in an isolated git worktree (loom workspace), updating ticket status.
3. **Review**: run a multi-angle review before merging.
4. **Compound**: extract reusable patterns into skills (procedural memory) + store memos for future planning.

The point is not vibes. The point is *reusable procedure*.

## Commands

### `/workflows:plan <idea>`

- Recall relevant memos for planning:
  - `compound_memory_recall(query="<idea>", command="workflows:plan")`
- Create/organize tickets:
  - `compound_ticket(argv=["init"])` (if needed)
  - `compound_ticket(argv=["create", "..."])`
  - `compound_ticket(argv=["dep-add", "<id>", "<dep-id>"])` (optional)
- Output a plan with:
  - ticket IDs
  - sequencing / dependencies
  - acceptance criteria and tests
  - risk list

### `/workflows:work <ticket-id>`

- Fetch ticket, set status to `in_progress`.
- Create/ensure a worktree:
  - Branch convention: `ticket-<id>-<slug>`
  - `compound_workspace(argv=["repo", "worktree", "add", "<branch>"])`
- Do the work in that worktree.
- Update ticket as you go (`add-note`, `update --status`).

### `/workflows:review <ticket-id>`

- Run fast checks (lint/tests if applicable).
- Do a review pass with multiple lenses:
  - correctness & maintainability
  - security & foot-guns
  - performance/regressions
  - docs & ergonomics
- Update the ticket with required follow-ups.

### `/workflows:compound <ticket-id>`

- Write memory notes (loom memory) that future planning can recall.
- Propose skill changes as a **CompoundSpec v1** JSON object.
- Call `compound_apply(spec_json=...)` to make it real:
  - create/update skills under `.opencode/skills/`
  - update AI-managed blocks in AGENTS/PROJECT/ROADMAP
  - append an agent-optimized CHANGELOG entry
  - sync derived indexes

## Operational defaults

- Keep skills small, scoped, and action-oriented.
- Prefer updating an existing skill over creating a near-duplicate.
- A skill should be applicable in at least 2 future contexts.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
