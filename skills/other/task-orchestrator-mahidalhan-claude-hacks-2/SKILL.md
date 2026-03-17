---
name: task-orchestrator
description: |
  USE WHEN: planning complex multi-step tasks, organizing work with dependencies, identifying parallelization opportunities, breaking down large features into atomic tasks.
  DO NOT USE WHEN: single simple tasks, tasks without dependencies, or when user just wants immediate execution without planning.
  For complex orchestration, trigger deep thinking with "think harder" or "ultrathink" to map comprehensive dependency graphs.
license: MIT
---

This skill transforms complex requests into optimally-ordered task plans, identifying parallelism opportunities while respecting dependencies. **Plans only—never executes without explicit user confirmation.**

## Orchestrator Thinking

Before outputting the plan, build the task graph:
- **Dependencies**: Which tasks block others? Map the critical path explicitly.
- **Parallelism**: Which tasks share NO dependencies? These form concurrent batches.
- **Granularity**: Is each task atomic enough for a single subagent? Split compound tasks.
- **Ordering**: What's the minimum-latency execution order given the dependency graph?

**CRITICAL**: This skill produces a PLAN, not execution. Output a numbered task list grouped by execution batch. Parallel tasks appear in the same batch. Sequential tasks appear in separate batches. Ask user "Execute this plan?" before invoking anything.

## Orchestration Guidelines

Focus on:
- **Dependency Graph**: Build explicit `task_a → task_b` edges. Visualize blocking relationships. Circular dependencies are bugs—detect and surface.
- **Batch Grouping**: Group zero-dependency tasks into Batch 1. Tasks unblocked after Batch 1 form Batch 2. Label each batch clearly with `[parallel]` or `[sequential]` tags.
- **Plan Output Format**: Present as numbered list with batch headers. Include brief rationale for ordering. End with "Proceed with execution?" prompt.
- **Execution Gate**: ONLY invoke subagents after user confirms. Confirmations: "yes", "execute", "proceed", "go". Anything else means wait or revise.
- **Revision Support**: If user wants changes, regenerate plan. Don't partially execute then ask—plan is atomic until approved.

NEVER auto-execute without user confirmation (violates planning-only contract), present flat lists without batch structure (loses parallelism visibility), skip the confirmation prompt (user must opt-in to execution), execute partial plans (all-or-nothing after approval), assume "sounds good" means execute (require explicit action words).

## Deep Thinking Mode

For complex multi-step orchestration, activate extended thinking:
- **"think harder"** or **"ultrathink"** triggers maximum reasoning depth (31,999 tokens)
- Use for: 10+ task dependency graphs, cross-system orchestration, critical path analysis
- Enables thorough mapping of all dependencies, parallelism opportunities, and edge cases
- Recommended when: task failure has high cost, dependencies are non-obvious, or timing matters
