---
name: codex-plan-writer
description: Create structured task plan files for complex coding requests. Use during planning phases to write verifiable, dependency-aware task breakdowns and checkpoint criteria before implementation.
load_priority: on-demand
---

## TL;DR
Create `{task-slug}.md` plan file for complex requests. Required sections: Overview, Success Criteria, Tech Stack, Task Breakdown (with dependencies, verify, rollback), Phase X Checklist. Use bite-sized tasks with concrete files/code/commands/verification details. Wait for user approval.

# Plan Writer

## Activation

1. Activate during workflow planning phases.
2. Activate on explicit `$codex-plan-writer`.
3. Mandatory for complex requests with scope `medium` or `large`.

## Output File Naming

- Derive a short kebab-case slug from the task intent (2-3 keywords).
- Maximum 30 characters.
- Examples: `ecommerce-cart.md`, `login-fix.md`, `dark-mode.md`.

## Output Location

Write plan file to project root: `./{task-slug}.md`

## Required Plan Structure

### 1. Overview

- what is being built or changed
- why it matters

### 2. Success Criteria

- measurable "done" conditions

### 3. Tech Stack (if relevant)

- selected technologies and rationale

### 4. Task Breakdown

For each task include:

- task name and id
- domain (`frontend | backend | mobile | debug`)
- priority (`P0 | P1 | P2 | P3`)
- dependencies
- input
- output
- verify method
- rollback strategy

### 5. Phase X Verification Checklist

- lint passes
- tests pass
- security scan reviewed
- all tasks completed

## Plan Granularity: Bite-Sized Tasks

Each task in an implementation plan should be **completable in 2-5 minutes**. Break down as follows:
1. "Write the failing test" - one step
2. "Run it to verify it fails" - one step
3. "Implement minimal code to pass" - one step
4. "Run tests to verify they pass" - one step
5. "Commit" - one step

### Task Structure

Each task MUST include:
- **Files:** Exact paths to create/modify/test
- **Code:** Complete code (not "add validation here")
- **Commands:** Exact commands with expected output
- **Verification:** How to confirm this task is done

## Rules

- Do not use vague placeholders in implementation tasks.
- Keep tasks small and verifiable.
- Explain why each task exists, not only what to do.

## Script Invocation Discipline

1. When plan execution calls scripts from other skills, run `--help` first.
2. Treat scripts as black-box helpers and execute by contract.
3. Read script source only when customization or bug fixing is required.

## Exit Gate

Plan writing is complete only when:

1. plan file exists at `./{task-slug}.md`
2. all required sections exist
3. user has reviewed and approved the plan
