---
id: KABSD-TSK-0073
uid: 019b9176-f219-7cc7-95f2-6fcccd481b41
type: Task
title: "Add first-run bootstrap (init_project) for kano-agent-backlog-skill"
state: Planned
priority: P2
parent: KABSD-FTR-0003
area: bootstrap
iteration: null
tags: ["init", "templates", "agents"]
created: 2026-01-06
updated: 2026-01-06
owner: codex-cli
external:
  azure_id: null
  jira_key: null
links:
  relates: []
  blocks: []
  blocked_by: []
decisions: []
---

# Context

# Goal

# Non-Goals

# Approach

# Alternatives

# Acceptance Criteria

# Risks / Dependencies

# Worklog

2026-01-06 12:00 [agent=codex-cli] Create/init backlog scaffold, default config, and optionally write agent guide files (AGENTS.md/CLAUDE.md) from templates.
2026-01-06 12:00 [agent=codex-cli] Start: implement init_project bootstrap + templates; make create_item derive prefix from backlog config.
2026-01-06 12:07 [agent=codex-cli] Implemented self-contained bootstrap: init_backlog now writes baseline config/views; added bootstrap_init_project.py with optional guide templates; config supports project.name/prefix; create_item defaults to config; docs updated.
2026-01-06 12:24 [agent=codex-cli] State -> Planned.
