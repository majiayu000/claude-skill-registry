---
id: KABSD-TSK-0001
uid: 019b8f52-9f51-76ed-a15e-59745b9b235f
type: Task
title: Create project-backlog skill
state: Done
priority: P2
parent: KABSD-USR-0001
area: infra
iteration: null
tags:
- backlog
- skill
created: 2026-01-02
updated: 2026-01-08
owner: null
external:
  azure_id: null
  jira_key: null
links:
  relates: []
  blocks: []
  blocked_by: []
decisions:
- ADR-0001
---

# Context

We want a local-first backlog system so the demo can show planning before coding
and preserve decision history beyond git log.

# Goal

Create the `project-backlog` skill definition and supporting references so the
agent workflow enforces planning and Ready gate rules in this demo repo.

# Non-Goals

- Implement external sync (Azure Boards/Jira).
- Build UI; rely on file-based views.

# Approach

- Add `skills/kano-agent-backlog-skill/SKILL.md`.
- Add references for schema, templates, workflow, and views.
- Add initial backlog folder structure and views in `_kano/backlog/`.

# Links

- UserStory: [[KABSD-USR-0001_plan-before-code|KABSD-USR-0001 Plan work before coding]]
- ADR: [[_kano/backlog/decisions/ADR-0001_backlog-structure-and-moc|ADR-0001 Backlog structure and MOC]]

# Alternatives

- Keep rules only in `AGENTS.md` (less structured, harder to query).
- Use a dedicated external PM tool now (requires network and setup).

# Acceptance Criteria

- Skill and references exist and are consistent.
- `_kano/backlog/` structure exists with `_meta`, `items`, `decisions`, `views`.
- Dataview examples render in Obsidian.

# Risks / Dependencies

- Requires Obsidian Dataview for views to render.
- Users must follow Ready gate manually until automation exists.

# Worklog

2026-01-02 10:00 [agent=codex] Created task and set state to InProgress per request.
2026-01-02 10:16 [agent=codex] Linked task to KABSD-USR-0001 for hierarchy alignment.
2026-01-02 10:30 [agent=codex] Decided to use per-type item folders and Obsidian-style MOC links with Dataview as a supplemental view.
2026-01-02 10:40 [agent=codex] Added _kano/backlog/tools/workitem_update_state.py to standardize state transitions and Worklog updates.
2026-01-02 10:52 [agent=codex] Kept workitem_update_state.py under _kano/backlog/tools as the project tool; skill references it instead of relocating into skills/scripts.
2026-01-02 10:56 [agent=codex] Added backlog volume control rules to SKILL.md and AGENTS.md to prevent ticket sprawl.
2026-01-02 11:02 [agent=codex] Created ADR-0001 for per-type folders and Obsidian MOC approach.
2026-01-02 11:06 [agent=codex] Added _kano/backlog/_meta/indexes.md to track index files per type.
2026-01-02 11:12 [agent=codex] Added Obsidian wikilink "Links" sections to items and ADR to enable Graph/backlinks.
2026-01-02 11:32 [agent=codex] Logged backlog-wide discussion decisions into Epic/Feature/UserStory Worklogs per request.
2026-01-03 01:15 [agent=codex] Simplified indexes to Epic-only MOC files to reduce file count; updated rules and ADR-0001.
2026-01-03 01:42 [agent=codex] Documented per-100 bucket folders for backlog items in the skill and conventions.
2026-01-03 01:45 [agent=codex] Updated ADR-0001 to include per-100 bucket folders for item storage.
2026-01-03 01:53 [agent=codex] Aligned index registry and conventions examples with bucketed item paths.
2026-01-03 01:19 [agent=codex] Closed per user request; backlog system established and ADR recorded.
2026-01-03 02:14 [agent=codex] Added Active view generator for New/InProgress items (_kano/backlog/views/Active.md).
2026-01-03 02:22 [agent=codex] Generalized view generator and added Active/New wrapper scripts.
2026-01-03 02:31 [agent=codex] Resolved view_generate.py paths relative to repo root to avoid empty outputs.
2026-01-03 12:41 [agent=codex] Renamed backlog ID prefix from BL to QB derived from PROJECT_NAME=Quboto; updated item IDs, links, and views.
2026-01-03 21:56 [agent=codex] Renamed generated views from Active.md/New.md to ActiveWork.md/NewWork.md for demo clarity.
2026-01-04 00:45 [agent=codex] Aligned task narrative with the kano-agent-backlog-skill demo scope.

2026-01-04 00:46 [agent=codex] Marked Done after demo backlog rebuild.
2026-01-08 02:00 [agent=copilot] Phase 3 complete: State and Audit implemented, 80 tests passing, 86% coverage
