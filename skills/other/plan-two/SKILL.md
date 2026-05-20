---
name: plan-two
version: 1.0.0
description: '[Planning] Research & create an implementation plan with 2 approaches'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` before executing.

> **Skill Variant:** Variant of `/plan` — creates two alternative implementation approaches for comparison.

## Quick Summary

**Goal:** Research and create an implementation plan with 2 distinct approaches for the user to compare and choose.

**Workflow:**
1. **Research** — Deep investigation of the problem space
2. **Approach A** — Design first implementation approach with trade-offs
3. **Approach B** — Design alternative approach with trade-offs
4. **Compare** — Present side-by-side comparison for user decision

**Key Rules:**
- PLANNING-ONLY: do not implement, only create comparison plan
- Both approaches must be genuinely viable, not strawman vs real
- Always offer `/plan-review` after plan creation

Activate `planning` skill.

## PLANNING-ONLY — Collaboration Required

> **DO NOT** use the `EnterPlanMode` tool — you are ALREADY in a planning workflow.
> **DO NOT** implement or execute any code changes.
> **COLLABORATE** with the user: ask decision questions, present options with recommendations.
> After plan creation, ALWAYS run `/plan-review` to validate the plan.
> ASK user to confirm the plan before any next step.

## Your mission

Use the `planner` subagent to create 2 detailed implementation plans for this following task:
<task>
$ARGUMENTS
</task>

## Workflow

1. First: Create a directory using naming pattern from `## Naming` section in injected context.
   Make sure you pass the directory path to every subagent during the process.
2. Follow strictly to the "Plan Creation & Organization" rules of `planning` skill.
3. Use multiple `researcher` agents in parallel to research for this task, each agent research for a different aspect of the task and perform max 5 researches (max 5 tool calls).
4. Use `scout` agent to search the codebase for files needed to complete the task.
5. Main agent gathers all research and scout report filepaths, and pass them to `planner` subagent with the detailed instructions prompt to create an implementation plan of this task.
   **Output:** Provide at least 2 implementation approaches with clear trade-offs, and explain the pros and cons of each approach, and provide a recommended approach.
6. Main agent receives the implementation plan from `planner` subagent, and ask user to review the plan

## Plan File Specification

- Every `plan.md` MUST start with YAML frontmatter:

    ```yaml
    ---
    title: '{Brief title}'
    description: '{One sentence for card preview}'
    status: pending
    priority: P2
    effort: { sum of phases, e.g., 4h }
    branch: { current git branch }
    tags: [relevant, tags]
    created: { YYYY-MM-DD }
    ---
    ```

## **IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using `TaskCreate`
- Always add a final review todo task to verify work quality and identify fixes/enhancements
- **MANDATORY FINAL TASKS:** After creating all planning todo tasks, ALWAYS add these two final tasks:
  1. **Task: "Run /plan-validate"** — Trigger `/plan-validate` skill to interview the user with critical questions and validate plan assumptions
  2. **Task: "Run /plan-review"** — Trigger `/plan-review` skill to auto-review plan for validity, correctness, and best practices

## Important Notes

**IMPORTANT:** Analyze the skills catalog and activate the skills that are needed for the task during the process.
**IMPORTANT:** Sacrifice grammar for the sake of concision when writing reports.
**IMPORTANT:** Ensure token efficiency while maintaining high quality.
**IMPORTANT:** In reports, list any unresolved questions at the end, if any.

## Post-Plan Validation

After plan creation, use the `AskUserQuestion` tool to ask: "Want me to run `/plan-review` to validate, or proceed to implementation?" with options:

- "Run /plan-review (Recommended)" — Execute `/plan-review` to validate the plan
- "Proceed to implementation" — Skip validation and start implementing

## REMINDER — Planning-Only Command

> **DO NOT** use `EnterPlanMode` tool.
> **DO NOT** start implementing.
> **ALWAYS** validate with `/plan-review` after plan creation.
> **ASK** user to confirm the plan before any implementation begins.
> **ASK** user decision questions with your recommendations when multiple approaches exist.
