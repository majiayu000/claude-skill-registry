---
name: plan-ci
version: 1.0.0
description: '[Planning] Analyze Github Actions logs and provide a plan to fix the issues'
disable-model-invocation: false
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing.

> **Skill Variant:** Variant of `/plan` — specialized for CI/GitHub Actions failure analysis.

## Quick Summary

**Goal:** Analyze GitHub Actions CI logs and create a plan to fix the identified issues.

**Workflow:**

1. **Fetch** — Download CI logs from GitHub Actions
2. **Analyze** — Identify root causes from build/test failures
3. **Plan** — Create implementation plan to fix CI issues

**Key Rules:**

- PLANNING-ONLY: do not implement, only create fix plan
- Focus on CI-specific issues (build, test, env, Docker, dependencies)
- Always offer `/plan-review` after plan creation

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

Activate `planning` skill.

## PLANNING-ONLY — Collaboration Required

> **DO NOT** use the `EnterPlanMode` tool — you are ALREADY in a planning workflow.
> **DO NOT** implement or execute any code changes.
> **COLLABORATE** with the user: ask decision questions, present options with recommendations.
> After plan creation, ALWAYS run `/plan-review` to validate the plan.
> ASK user to confirm the plan before any next step.

## Github Actions URL

$ARGUMENTS

Use the `planner` subagent to read the github actions logs, analyze and find the root causes of the issues, then provide a detailed plan for implementing the fixes.

**Plan File Specification:**

- Every `plan.md` MUST start with YAML frontmatter:
    ```yaml
    ---
    title: '{Brief title}'
    description: '{One sentence for card preview}'
    status: pending
    priority: P1
    effort: { estimated fix time }
    branch: { current git branch }
    tags: [ci, bugfix]
    created: { YYYY-MM-DD }
    ---
    ```

**Output:**
Provide at least 2 implementation approaches with clear trade-offs, and explain the pros and cons of each approach, and provide a recommended approach.

## **IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using `TaskCreate`
- Always add a final review todo task to verify work quality and identify fixes/enhancements
- **MANDATORY FINAL TASKS:** After creating all planning todo tasks, ALWAYS add these two final tasks:
    1. **Task: "Run /plan-validate"** — Trigger `/plan-validate` skill to interview the user with critical questions and validate plan assumptions
    2. **Task: "Run /plan-review"** — Trigger `/plan-review` skill to auto-review plan for validity, correctness, and best practices

## Important Notes

**IMPORTANT:** Analyze the skills catalog and activate the skills that are needed for the task during the process.
**IMPORTANT:** Sacrifice grammar for the sake of concision when writing outputs.

## REMINDER — Planning-Only Command

> **DO NOT** use `EnterPlanMode` tool.
> **DO NOT** start implementing.
> **ALWAYS** validate with `/plan-review` after plan creation.
> **ASK** user to confirm the plan before any implementation begins.
> **ASK** user decision questions with your recommendations when multiple approaches exist.
