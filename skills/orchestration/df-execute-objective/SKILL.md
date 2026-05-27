---
name: df:execute-objective
description: |
  Execute all jobs in an objective with wave-based parallelization.
  Use when the user wants to build, run, or execute a planned objective.
  Triggers on: "execute objective", "run objective", "build objective", "start building", "run the jobs", "let's build"
argument-hint: "<phase-number> [--gaps-only]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
  - TaskCreate
  - AskUserQuestion
---
<objective>
Execute all jobs in an objective using wave-based parallel execution.

Orchestrator stays lean: discover plans, analyze dependencies, group into waves, spawn subagents, collect results. Each subagent loads the full execute-job context and handles its own job.

Context budget: ~15% orchestrator, 100% fresh per subagent.
</objective>

<execution_context>
@~/.claude/devflow/workflows/execute-objective.md
@~/.claude/devflow/references/ui-brand.md
</execution_context>

<context>
Objective: $ARGUMENTS

**Flags:**
- `--gaps-only` — Execute only gap closure plans (plans with `gap_closure: true` in frontmatter). Use after verify-work creates fix plans.

@.planning/ROADMAP.md
@.planning/STATE.md
</context>

<process>
Execute the execute-objective workflow from @~/.claude/devflow/workflows/execute-objective.md end-to-end.
Preserve all workflow gates (wave execution, checkpoint handling, verification, state updates, routing).
</process>
