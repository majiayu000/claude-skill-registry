---
name: cook-hard
version: 1.0.0
description: '[Implementation] Thorough implementation with maximum verification'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` before executing.

- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)
- `docs/test-specs/` — Test specifications by module (read existing TCs; generate/update test specs via `/tdd-spec` after implementation)

> **Skill Variant:** Variant of `/cook` — thorough implementation with maximum verification.

## Quick Summary

**Goal:** Implement features with deep research, comprehensive planning, and maximum quality verification.

**Workflow:**

1. **Research** — Deep investigation with multiple researcher subagents
2. **Plan** — Detailed plan with `/plan-hard`, user approval required
3. **Implement** — Execute with full code review and SRE review
4. **Verify** — Run all tests, review changes, update docs

**Key Rules:**

- Maximum thoroughness: research → plan → implement → review → test → docs
- User approval required at plan stage
- Break work into todo tasks; add final self-review task

### Frontend/UI Context (if applicable)

When this task involves frontend or UI changes, **MUST READ** `.claude/skills/shared/ui-system-context.md` and the following docs:

- Component patterns: `docs/project-reference/frontend-patterns-reference.md`
- Styling/BEM guide: `docs/project-reference/scss-styling-guide.md`
- Design system tokens: `docs/project-reference/design-system/README.md`

**Ultrathink** to plan and implement these tasks with maximum verification:

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

<tasks>$ARGUMENTS</tasks>

**Mode:** HARD - Extra research, detailed planning, mandatory reviews.

## Workflow

### 1. Deep Research Phase

- Launch 2-3 `researcher` subagents in parallel covering:
    - Technical approach validation
    - Edge cases and failure modes
    - Security implications
    - Performance considerations
- Use `/scout-ext` for comprehensive codebase analysis
- Generate research reports (max 150 lines each)
- **External Memory**: Write all research to `.ai/workspace/analysis/{task-name}.analysis.md`. Re-read ENTIRE file before planning.

### 2. Comprehensive Planning

- Use `planner` subagent with all research reports
- Create full plan directory with:
    - `plan.md` - Overview with risk assessment
    - `phase-XX-*.md` - Detailed phase files
    - Success criteria for each phase
    - Rollback strategy

### 3. Verified Implementation

- Implement one phase at a time
- After each phase:
    - Run type-check and compile
    - Run relevant tests
    - Self-review before proceeding

### Batch Checkpoint (Large Plans)

For plans with 10+ tasks, execute in batches with human review:

1. **Execute batch** — Complete next 3 tasks (or user-specified batch size)
2. **Report** — Show what was implemented, verification output, any concerns
3. **Wait** — Say "Ready for feedback" and STOP. Do NOT continue automatically.
4. **Apply feedback** — Incorporate changes, then execute next batch
5. **Repeat** until all tasks complete

<HARD-GATE>
For plans with 10+ tasks, do NOT execute all tasks continuously without checkpoint.
Stop after every batch for human review. This prevents runaway execution where early
mistakes compound through later tasks.
</HARD-GATE>

### 4. Mandatory Testing

- Use `tester` subagent for full test coverage
- Write tests for:
    - Happy path scenarios
    - Edge cases from research
    - Error handling paths
- NO mocks or fake data allowed
- Repeat until all tests pass

### 5. Mandatory Code Review

- Use `code-reviewer` subagent
- Address all critical and major findings
- Re-run tests after fixes
- Repeat until approved

### 6. Documentation Update

- Use `docs-manager` to update relevant docs
- Use `project-manager` to update project status
- Record any architectural decisions

### 7. Final Report

- Summary of all changes
- Test coverage metrics
- Security considerations addressed
- Unresolved questions (if any)
- Ask user to review and approve

## When to Use

- Critical production features
- Security-sensitive changes
- Public API modifications
- Database schema changes
- Cross-service integrations

## Quality Gates

| Gate     | Criteria                  |
| -------- | ------------------------- |
| Research | 2+ researcher reports     |
| Planning | Full plan directory       |
| Tests    | All pass, no mocks        |
| Review   | 0 critical/major findings |
| Docs     | Updated if needed         |

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
