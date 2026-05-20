---
id: KABSD-USR-0011
uid: 019b8f52-9f42-7e1e-a23f-d61218f54169
type: UserStory
title: Enforce Agent Identity in Skill
state: Done
priority: P1
parent: KABSD-FTR-0005
area: general
iteration: null
tags: []
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

To maintain the integrity of audit logs, we must ensure that agents use their real identities in worklogs, rather than blindly copying "codex" from templates.

# Goal

Update the skill documentation and templates to explicitly require agents to use their real identity.

# Non-Goals

- Technical enforcement in the script code (documentation only for now).

# Approach

1. Update `SKILL.md` Non-negotiables.
2. Update `templates.md` with placeholders.
3. Update `conventions.md`.

# Acceptance Criteria

- [ ] `SKILL.md` contains the rule.
- [ ] `templates.md` no longer has hardcoded `codex`.
- [ ] `conventions.md` warns about identity usage.

# Risks / Dependencies

- Agents might ignore the docs; scripts should eventually enforce this (via `--agent` arg).

# Worklog

2026-01-04 23:31 [agent=antigravity] Created from template.
2026-01-04 23:33 [agent=antigravity] State -> Done.
