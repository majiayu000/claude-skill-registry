---
name: cook-fast
version: 1.0.0
description: '[Implementation] Fast implementation - skip research, minimal planning'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` before executing.

- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)
- `docs/test-specs/` — Test specifications by module (read existing TCs; generate/update test specs via `/tdd-spec` after implementation)

> **Process Discipline:** MUST READ `.claude/skills/shared/rationalization-prevention-protocol.md` — counter "too simple for a plan" and "I'll refactor later" evasions.

> **Process Discipline:** MUST READ `.claude/skills/shared/red-flag-stop-conditions-protocol.md` — STOP after 3+ failed attempts or when fix requires modifying 5+ files for a "simple" change.

> **Skill Variant:** Variant of `/cook` — fast implementation skipping research with minimal planning.

## Quick Summary

**Goal:** Implement features quickly with minimal research and streamlined planning.

**Workflow:**

1. **Scout** — Quick codebase scan for patterns
2. **Plan** — Lightweight implementation plan
3. **Implement** — Execute with code-simplifier review

**Key Rules:**

- Skip deep research; rely on codebase patterns
- Still requires user approval before implementing
- Break work into todo tasks; add final self-review task

### Frontend/UI Context (if applicable)

When this task involves frontend or UI changes, **MUST READ** `.claude/skills/shared/ui-system-context.md` and the following docs:

- Component patterns: `docs/project-reference/frontend-patterns-reference.md`
- Styling/BEM guide: `docs/project-reference/scss-styling-guide.md`
- Design system tokens: `docs/project-reference/design-system/README.md`

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

Start working on these tasks immediately with minimal planning:
<tasks>$ARGUMENTS</tasks>

**Mode:** FAST - Skip research, minimal planning, trust your knowledge.

## Workflow

1. **Quick Planning** (skip research phase)
    - Analyze task requirements directly
    - Create minimal todo list with `TaskCreate`
    - NO researcher subagents, NO scout commands
    - For non-trivial tasks: write brief analysis to `.ai/workspace/analysis/{task-name}.analysis.md` before implementing.

2. **Rapid Implementation**
    - Use `/code` directly on tasks
    - Skip multi-step planning documents
    - Focus on working code over documentation

3. **Quick Validation**
    - Run type-check and compile
    - Manual spot-check over full test suite
    - Skip code-reviewer subagent

4. **Commit** (optional)
    - Ask user if ready to commit via `AskUserQuestion`
    - If yes, use `/commit`

## When to Use

- Simple features with clear requirements
- Bug fixes with known solutions
- Refactoring tasks
- When user says "just do it"

## Trade-offs

| Aspect   | Fast Mode   | Full Mode       |
| -------- | ----------- | --------------- |
| Research | Skipped     | Multiple agents |
| Planning | Minimal     | Full plan docs  |
| Testing  | Quick check | Full test suite |
| Review   | Skipped     | Code-reviewer   |
| Speed    | ~2x faster  | Thorough        |

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
