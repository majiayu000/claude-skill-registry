---
name: df:new-milestone
description: |
  Start a new milestone cycle — update PROJECT.md and route to requirements.
  Lifecycle transition that resets requirements and roadmap — needs explicit intent.
argument-hint: "[milestone name, e.g., 'v1.1 Notifications']"
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Task
  - AskUserQuestion
---
<objective>
Start a new milestone: questioning → research (optional) → requirements → roadmap.

Brownfield equivalent of new-project. Project exists, PROJECT.md has history. Gathers "what's next", updates PROJECT.md, then runs requirements → roadmap cycle.

**Creates/Updates:**
- `.planning/PROJECT.md` — updated with new milestone goals
- `.planning/research/` — domain research (optional, NEW features only)
- `.planning/REQUIREMENTS.md` — scoped requirements for this milestone
- `.planning/ROADMAP.md` — objective structure (continues numbering)
- `.planning/STATE.md` — reset for new milestone

**After:** `/df:plan-objective [N]` to start execution.
</objective>

<execution_context>
@~/.claude/devflow/workflows/new-milestone.md
@~/.claude/devflow/references/questioning.md
@~/.claude/devflow/references/ui-brand.md
@~/.claude/devflow/templates/project.md
@~/.claude/devflow/templates/requirements.md
</execution_context>

<context>
Milestone name: $ARGUMENTS (optional - will prompt if not provided)

**Load project context:**
@.planning/PROJECT.md
@.planning/STATE.md
@.planning/MILESTONES.md
@.planning/config.json

**Load milestone context (if exists, from /df:discuss-milestone):**
@.planning/MILESTONE-CONTEXT.md
</context>

<process>
Execute the new-milestone workflow from @~/.claude/devflow/workflows/new-milestone.md end-to-end.
Preserve all workflow gates (validation, questioning, research, requirements, roadmap approval, commits).
</process>
