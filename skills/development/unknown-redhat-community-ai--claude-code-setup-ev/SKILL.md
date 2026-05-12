---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** This should be run in a dedicated worktree (created by brainstorming skill).

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`
- (User preferences for plan location override this default)

## Plan Structure

Read `skills/plan-template.md` for the complete plan document format, including header, file structure, task granularity, and execution handoff.

## Self-Review

Read `skills/self-review.md` for the post-writing checklist (spec coverage, placeholder scan, type consistency).

## Behavioral Rules

Read `guidelines.md` for hard limits on placeholders, formatting requirements, and quality standards.

## Remember
- Exact file paths always
- Complete code in every step — if a step changes code, show the code
- Exact commands with expected output
- DRY, YAGNI, TDD, frequent commits
