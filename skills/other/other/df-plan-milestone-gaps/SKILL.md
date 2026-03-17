---
name: df:plan-milestone-gaps
description: |
  Create objectives to close all gaps identified by milestone audit.
  Specialized gap-closure workflow — runs after audit-milestone.
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---
<objective>
Create all objectives necessary to close gaps identified by `/df:audit-milestone`.

Reads MILESTONE-AUDIT.md, groups gaps into logical objectives, creates objective entries in ROADMAP.md, and offers to plan each objective.

One command creates all fix objectives — no manual `/df:add-objective` per gap.
</objective>

<execution_context>
@~/.claude/devflow/workflows/plan-milestone-gaps.md
</execution_context>

<context>
**Audit results:**
Glob: .planning/v*-MILESTONE-AUDIT.md (use most recent)

**Original intent (for prioritization):**
@.planning/PROJECT.md
@.planning/REQUIREMENTS.md

**Current state:**
@.planning/ROADMAP.md
@.planning/STATE.md
</context>

<process>
Execute the job-milestone-gaps workflow from @~/.claude/devflow/workflows/plan-milestone-gaps.md end-to-end.
Preserve all workflow gates (audit loading, prioritization, objective grouping, user confirmation, roadmap updates).
</process>
