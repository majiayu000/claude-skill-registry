---
name: story-workflow
description: Story management, estimation, and Shortcut integration for backlog workflow. Use when (1) Starting new work from backlog, (2) Estimating story points, (3) Creating feature/bug/chore stories, (4) Defining acceptance criteria, (5) Working with Shortcut/issue tracking, (6) Classifying work types. Covers Fibonacci estimation (0/1/2/3/5/8), branch naming, story types, and TDD workflow integration.
---

# Story Workflow & Estimation

## Backlog Rules (Shortcut-first)

* Work the **top unstarted story**. If unclear, write acceptance criteria and proceed.
* **Branch names:** `{type}/{shortcut-id}-{slug}` where type = feature/bug/chore

## TDD Workflow Commits

* **Red:** Write failing tests first (commit: `WIP: red tests for {story}`)
* **Green:** Minimal code to pass (commit: `green: {behavior}`)
* **Refactor:** Improve design with tests green (commit: `refactor: {area}`)

## PR/Story Flow

* Mark story **Finished** → open PR → CI runs → code review → merge → mark **Delivered** → PM **Accept/Reject**

## Daily Discipline

* Create a **WIP commit** when starting work
* **End-of-day commit** summarizing progress

## Story Types

* **Feature:** New functionality or capability
* **Bug:** Fixing broken or incorrect behavior
* **Chore:** Maintenance, refactoring, dependencies, infrastructure

Classify explicitly in PR and branch name.

## Fibonacci Points (0/1/2/3/5/8)

* **0:** Trivial (typo, tiny UI tweak, config change)
* **1:** Clear, contained (single endpoint, simple UI component)
* **2:** Slightly complex, well-defined (multiple files, some unknowns)
* **3/5/8:** Large - **SPLIT** into smaller stories first

Always attach your point **rationale** in PR template.

## When to Split Stories

If estimating **3, 5, or 8 points:**

1. **Break into smaller stories** before starting work
2. Each sub-story should be **≤2 points**
3. Sub-stories should deliver incremental value
4. Document split in parent story

## Reference Files

See `references/estimation-guide.md` for detailed estimation examples, complexity criteria, and splitting strategies.

See `references/story-templates.md` for story description templates with problem/solution/acceptance criteria formats.

See `references/shortcut-integration.md` for Shortcut-specific workflow, state transitions, and linking conventions.
