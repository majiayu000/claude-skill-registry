---
name: task-handoff-writing
description: Write high-signal handoffs (`HANDOFF.md` or `docs/handoffs/<slug>.md`) with concrete validation evidence and actionable next steps.
---

# Handoff Writing

## When to use

Use this when the task mentions:

- “handoff”, “context limit”, “I can’t finish”, “park this work”
- preparing for review / teammate pickup

## Fast path

1. Capture repo snapshot: `git status -sb` and `git log -n 5 --oneline`
2. Capture quality gate status: `./verify.sh --ui=false`
3. Write a handoff with: Problem Statement → Current Snapshot → Next Steps (with exact commands) → Risks → References.

## Canonical repo doc

Read `docs/skills/handoff-writing.md`.
