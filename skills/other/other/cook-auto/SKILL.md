---
name: cook-auto
version: 1.0.0
description: '[Implementation] Implement a feature automatically (trust me bro)'
disable-model-invocation: false
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` before executing.

- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)
- `docs/test-specs/` — Test specifications by module (read existing TCs; generate/update test specs via `/tdd-spec` after implementation)

> **Process Discipline:** MUST READ `.claude/skills/shared/rationalization-prevention-protocol.md` — counter "too simple for a plan" and "I'll refactor later" evasions.

> **Process Discipline:** MUST READ `.claude/skills/shared/red-flag-stop-conditions-protocol.md` — STOP after 3+ failed attempts or when fix requires modifying 5+ files for a "simple" change.

> **Skill Variant:** Variant of `/cook` — autonomous execution without user confirmation.

## Quick Summary

**Goal:** Implement features autonomously without stopping for user confirmation at each step.

**Workflow:**

1. **Analyze** — Understand task requirements from arguments
2. **Plan & Execute** — Create plan and implement directly
3. **Verify** — Run tests and review changes

**Key Rules:**

- Autonomous mode: proceed without asking for confirmation
- Still follow all coding standards and patterns
- Break work into todo tasks; add final self-review task

**Ultrathink** to plan & start working on these tasks follow the Orchestration Protocol, Core Responsibilities, Subagents Team and Development Rules:

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

<tasks>$ARGUMENTS</tasks>

**IMPORTANT:** Analyze the list of skills at `.claude/skills/*` and intelligently activate the skills that are needed for the task during the process.
**Ensure token efficiency while maintaining high quality.**

## Workflow:

1. Trigger slash command `/plan <detailed-instruction-prompt>` to create an implementation plan based on the given tasks.
    - **External Memory**: Ensure `/plan` writes analysis to `.ai/workspace/analysis/`. Re-read before `/code`.
2. Trigger slash command `/code <plan>` to implement the plan.
3. Finally use `AskUserQuestion` tool to ask user if he wants to commit to git repository, if yes trigger `/commit` slash command to create a commit.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
