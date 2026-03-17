---
name: plan
version: 1.0.0
description: '[Planning] Intelligent plan creation with prompt enhancement'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` before executing.

## Quick Summary

**Goal:** Intelligently create implementation plans by analyzing task complexity and routing to `/plan-fast` or `/plan-hard`.

**Workflow:**

1. **Analyze** — Understand task, ask clarifying questions via AskUserQuestion
2. **Route** — Decide `/plan-fast` (simple) or `/plan-hard` (complex) based on scope
3. **Create** — Execute chosen plan variant, write plan to `plans/` directory
4. **Validate** — Offer `/plan-review` and `/plan-validate` for quality assurance

**Key Rules:**

- PLANNING-ONLY: never implement, never use EnterPlanMode tool
- Parent skill for all plan-* variants (plan-fast, plan-hard, plan-ci, plan-cro, plan-two, plan-parallel)
- Always collaborate with user; ask decision questions, present options
- Always add final `/plan-validate` and `/plan-review` tasks

## PLANNING-ONLY — Collaboration Required

> **DO NOT** use the `EnterPlanMode` tool — you are ALREADY in a planning workflow.
> **DO NOT** implement or execute any code changes.
> **COLLABORATE** with the user: ask decision questions, present options with recommendations.
> After plan creation, ALWAYS use `AskUserQuestion` tool to offer `/plan-review` validation.
> ASK user to confirm the plan before any next step.

## Your mission

<task>
$ARGUMENTS
</task>

## Pre-Creation Check (Active vs Suggested Plan Detection)

Check the `## Plan Context` section in the injected context:

- If "Plan:" shows a path → Active plan exists. Ask user: "Active plan found: {path}. Continue with this? [Y/n]"
- If "Suggested:" shows a path → Branch-matched plan hint only. Ask user if they want to activate it or create new.
- If "Plan: none" → Proceed to create new plan using naming pattern from `## Naming` section.

## Workflow

- Analyze the given task and use `AskUserQuestion` tool to ask for more details if needed.
- Decide to use `/plan-fast` or `/plan-hard` SlashCommands based on the complexity.
- Execute SlashCommand: `/plan-fast <detailed-instructions-prompt>` or `/plan-hard <detailed-instructions-prompt>`
- Activate `planning` skill.
- Note: `detailed-instructions-prompt` is **an enhanced prompt** that describes the task in detail based on the provided task description.

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

## REMINDER — Planning-Only Command

> **DO NOT** use `EnterPlanMode` tool.
> **DO NOT** start implementing.
> **ALWAYS** use `AskUserQuestion` tool to offer `/plan-review` validation after plan creation.
> **ASK** user to confirm the plan before any implementation begins.
> **ASK** user decision questions using `AskUserQuestion` tool when multiple approaches exist.
