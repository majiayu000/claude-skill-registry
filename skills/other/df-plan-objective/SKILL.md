---
name: df:plan-objective
description: |
  Create detailed objective plan (JOB.md) with verification loop.
  Use when the user wants to plan an objective, create execution plans, or prepare for building.
  Triggers on: "plan objective", "create plans", "plan the next objective", "let's plan", "prepare objective", "make plans for"
argument-hint: "[objective] [--auto] [--research] [--skip-research] [--gaps] [--skip-verify]"
agent: df-planner
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - Task
  - WebFetch
  - mcp__context7__*
---
<objective>
Create executable objective prompts (JOB.md files) for a roadmap objective with integrated research and verification.

**Default flow:** Research (if needed) → Plan → Verify → Done

**Orchestrator role:** Parse arguments, validate objective, research domain (unless skipped), spawn df-planner, verify with df-job-checker, iterate until pass or max iterations, present results.
</objective>

<execution_context>
@~/.claude/devflow/workflows/plan-objective.md
@~/.claude/devflow/references/ui-brand.md
</execution_context>

<context>
Objective number: $ARGUMENTS (optional — auto-detects next unplanned objective if omitted)

**Flags:**
- `--research` — Force re-research even if RESEARCH.md exists
- `--skip-research` — Skip research, go straight to planning
- `--gaps` — Gap closure mode (reads VERIFICATION.md, skips research)
- `--skip-verify` — Skip verification loop

Normalize objective input in step 2 before any directory lookups.
</context>

<process>
Execute the job-objective workflow from @~/.claude/devflow/workflows/plan-objective.md end-to-end.
Preserve all workflow gates (validation, research, planning, verification loop, routing).
</process>
