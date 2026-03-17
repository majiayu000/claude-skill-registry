---
area: general
created: '2026-01-16'
decisions: []
external:
  azure_id: null
  jira_key: null
id: KABSD-TSK-0232
iteration: backlog
links:
  blocked_by: []
  blocks: []
  relates: []
owner: codex
parent: null
priority: P2
state: Done
tags: []
title: Add conflict handling policy to config and skill
type: Task
uid: 019bc711-83c9-7185-8294-8b7359e6975a
updated: 2026-01-16
---

# Context

Need a consistent conflict-resolution policy for duplicate IDs/UIDs across agents and tooling.

# Goal

Add a configurable conflict policy and document it in the skill; default to rename on ID conflict and trash shorter content on UID conflict.

# Approach

Add conflict_policy settings to product config, implement enforcement in duplicate-ID normalization, and document behavior in SKILL.md and ADR.

# Acceptance Criteria

Config contains conflict_policy defaults; duplicate-ID normalization honors policy; ADR recorded; skill docs describe behavior.

# Risks / Dependencies

Risk of destructive behavior if UID conflict policy deletes content; mitigate by defaulting to trash and requiring review.

# Worklog

2026-01-16 21:49 [agent=codex] [model=unknown] Created item
2026-01-16 21:49 [agent=codex] [model=unknown] Start implementing conflict policy config + ADR.
2026-01-16 21:54 [agent=codex] [model=unknown] Created ADR-0034 to record conflict handling policy and started implementing config-driven defaults (rename on ID conflict, trash shorter on UID conflict).
2026-01-16 22:21 [agent=codex] [model=unknown] Implemented conflict_policy defaults (rename ID conflicts, trash shorter UID conflicts), documented in skill + ADR-0034, and updated normalize-ids behavior accordingly.
2026-01-16 22:22 [agent=codex] [model=unknown] Conflict policy config + ADR implemented.
