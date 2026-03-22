---
name: plan
version: 1.0.0
description: '[Planning] Intelligent plan creation with prompt enhancement'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` before executing.

- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)
- `.claude/skills/shared/rationalization-prevention-protocol.md` — Anti-evasion rebuttals (prevents "too simple for a plan" shortcuts)
- `docs/test-specs/` — Test specifications by module (read existing TCs to include test strategy in plan)

> **Iterative Quality Gate:** **MUST READ** `.claude/skills/shared/iterative-phase-quality-protocol.md`.
> Before routing, assess complexity score. Score ≥3 → plan MUST produce multiple phases with per-phase quality cycles.

## Quick Summary

**Goal:** Intelligently create implementation plans by analyzing task complexity and routing to `/plan-fast` or `/plan-hard`.

**Workflow:**

1. **Analyze** — Understand task, ask clarifying questions via AskUserQuestion
2. **Route** — Decide `/plan-fast` (simple) or `/plan-hard` (complex) based on scope
3. **Create** — Execute chosen plan variant, write plan to `plans/` directory
4. **Validate** — Offer `/plan-review` and `/plan-validate` for quality assurance

**Key Rules:**

- PLANNING-ONLY: never implement, never use EnterPlanMode tool
- Parent skill for all plan-\* variants (plan-fast, plan-hard, plan-ci, plan-cro, plan-two, plan-parallel)
- Always collaborate with user; ask decision questions, present options
- Always add final `/plan-validate` and `/plan-review` tasks

## Greenfield Mode

> **Auto-detected:** If no existing codebase is found (no code directories like `src/`, `app/`, `lib/`, `server/`, `packages/`, etc., no manifest files like `package.json`/`*.sln`/`go.mod`, no populated `project-config.json`), this skill switches to greenfield mode automatically. Planning artifacts (docs/, plans/, .claude/) don't count — the project must have actual code directories with content.

**When greenfield is detected:**

1. **ALWAYS route to `/plan-hard`** — greenfield planning requires deep research, never fast plans
2. Skip "MUST READ project-structure-reference.md" step (file won't exist or is placeholder)
3. Enable web research for tech landscape analysis (WebSearch + WebFetch)
4. Delegate architecture decisions to `solution-architect` agent
5. Increase user interview frequency (AskUserQuestion at each major decision)
6. If `/greenfield` workflow is not already active, suggest it via AskUserQuestion:
    - "Activate Greenfield Project Init workflow (Recommended)" — full waterfall inception
    - "Continue with standalone /plan-hard" — planning only, no full workflow

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

## Variant Decision Guide

| If the task is...                | Use                  | Why                                    |
| -------------------------------- | -------------------- | -------------------------------------- |
| Simple, clear scope (<5 files)   | `/plan-fast`         | Lightweight plan, faster output        |
| Complex, multi-layer, many files | `/plan-hard`         | Deep research, comprehensive plan      |
| CI/CD pipeline changes           | `/plan-ci`           | CI-specific context and validation     |
| Cross-cutting refactor           | `/plan-cro`          | Cross-service impact analysis          |
| Parallel implementation possible | `/plan-parallel`     | Splits plan into parallelizable phases |
| Two competing approaches         | `/plan-two`          | Creates 2 plans for comparison         |
| Analyzing existing plan          | `/plan-analysis`     | Reviews/critiques an existing plan     |
| Archiving completed plan         | `/plan-archive`      | Moves plan to archive                  |
| General/unknown                  | `/plan` (this skill) | Routes automatically                   |

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

---

## Standalone Review Gate (Non-Workflow Only)

> **MANDATORY IMPORTANT MUST:** If this skill is called **outside a workflow** (standalone `/plan`), the generated plan MUST include `/review-changes` as a **final phase/task** in the plan. This ensures all implementation changes get reviewed before commit even without a workflow enforcing it.
>
> If already running inside a workflow (e.g., `feature`, `bugfix`), skip this — the workflow sequence handles `/review-changes` at the appropriate step.

## Workflow Recommendation

> **IMPORTANT MUST:** If you are NOT already in a workflow, use `AskUserQuestion` to ask the user:
>
> 1. **Activate `pre-development` workflow** (Recommended) — quality-gate → plan → plan-review → plan-validate
> 2. **Execute `/plan` directly** — run this skill standalone
