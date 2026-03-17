---
name: cook-fast
version: 1.0.0
description: '[Implementation] Fast implementation - skip research, minimal planning'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` before executing.

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
