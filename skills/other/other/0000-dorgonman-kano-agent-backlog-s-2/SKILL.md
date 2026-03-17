---
id: KABSD-USR-0004
uid: 019b8f52-9f34-7f5c-9722-6de907b1fc86
type: UserStory
title: Bootstrap backlog scaffold and tools from the skill
state: Proposed
priority: P2
parent: KABSD-FTR-0003
area: skill
iteration: null
tags:
- self-contained
- bootstrap
created: 2026-01-04
updated: '2026-01-06'
owner: null
external:
  azure_id: null
  jira_key: null
links:
  relates: []
  blocks: []
  blocked_by: []
decisions: []
original_type: UserStory
---

# Context

Setting up a new repo still requires manual folder creation and tool wrapper
copies. A self-contained skill should generate these automatically.

# Goal

As a maintainer, I want to bootstrap the backlog scaffold and tool wrappers
from the skill so setup is repeatable and script-driven.

# Non-Goals

- Seeding demo items or views (handled in a separate story).
- Customizing the backlog layout beyond the standard structure.

# Approach

- Add `bootstrap_init_backlog.py` to create `_kano/backlog/` + `_meta` scaffolding.
- Add `install_tools.py` to generate `_kano/backlog/tools` wrappers.
- Keep scripts idempotent and avoid overwriting existing data.

# Links

- Feature: [[KABSD-FTR-0003_self-contained-skill-bootstrap-and-automation|KABSD-FTR-0003 Self-contained skill bootstrap and automation]]
- Task: [[KABSD-TSK-0009_implement-backlog-scaffold-initializer-script|KABSD-TSK-0009 Implement backlog scaffold initializer script]]
- Task: [[KABSD-TSK-0010_generate-tool-wrappers-from-skill-scripts|KABSD-TSK-0010 Generate tool wrappers from skill scripts]]

# Alternatives

- Manual copy/paste of `_kano/backlog` and `_kano/backlog/tools`.

# Acceptance Criteria

- Running the initializer creates the standard `_kano/backlog/` structure.
- Tool wrapper generation can recreate `_kano/backlog/tools/` on demand.
- Scripts are safe to run multiple times without clobbering data.

# Risks / Dependencies

- Existing repos may have customized layouts that need manual review.

# Worklog

2026-01-04 13:51 [agent=codex] Created user story for bootstrap and tool scaffolding.
2026-01-04 13:55 [agent=codex] Added scope, approach, and linked tasks for bootstrap tooling.
