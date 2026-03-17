---
name: df:add-objective
description: |
  Add objective to end of current milestone in roadmap.
  Structural roadmap modification — use only when explicitly requested.
argument-hint: <description>
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Bash
---

<objective>
Add a new integer objective to the end of the current milestone in the roadmap.

Routes to the add-objective workflow which handles:
- Objective number calculation (next sequential integer)
- Directory creation with slug generation
- Roadmap structure updates
- STATE.md roadmap evolution tracking
</objective>

<execution_context>
@.planning/ROADMAP.md
@.planning/STATE.md
@~/.claude/devflow/workflows/add-objective.md
</execution_context>

<process>
**Follow the add-objective workflow** from `@~/.claude/devflow/workflows/add-objective.md`.

The workflow handles all logic including:
1. Argument parsing and validation
2. Roadmap existence checking
3. Current milestone identification
4. Next objective number calculation (ignoring decimals)
5. Slug generation from description
6. Objective directory creation
7. Roadmap entry insertion
8. STATE.md updates
</process>
