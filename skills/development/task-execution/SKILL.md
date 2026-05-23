---
description: This skill should be used when executing implementation tasks, running tasks in dependency order, verifying task completion against acceptance criteria, or implementing code changes from generated tasks.
triggers:
  - execute task
  - run task
  - implement task
  - work on task
  - task execution
  - complete task
  - start working on tasks
  - execute pending tasks
---

# Task Execution Skill

This skill provides structured knowledge for executing Claude Code Tasks through a 4-phase workflow with adaptive verification. It bridges the gap between task generation and feature implementation by executing tasks autonomously in dependency order.

## Core Principles

### 1. Understand Before Implementing

Never write code without first understanding:
- What the task requires (acceptance criteria or inferred requirements)
- What code already exists (read before modify)
- What conventions the project follows (CLAUDE.md, existing patterns)
- What earlier tasks discovered (shared execution context)

### 2. Follow Existing Patterns

Match the codebase's established patterns:
- Coding style, naming conventions, file organization
- Error handling approach, logging patterns
- Test framework, test structure, assertion style
- Import ordering, module organization

### 3. Verify Against Criteria

Do not assume implementation is correct. Verify by:
- Walking through each acceptance criterion for PRD-generated tasks
- Running tests and linters for all tasks
- Confirming the core change works as intended
- Checking for regressions in existing functionality

### 4. Report Honestly

Produce accurate verification results:
- PASS only when all Functional criteria pass and tests pass
- PARTIAL when non-critical criteria fail but core works
- FAIL when Functional criteria or tests fail
- Never mark a task complete if verification fails

## Task Classification

Determine whether a task is PRD-generated or general to select the right verification approach.

### Detection Algorithm

1. **Check description format**: Look for `**Acceptance Criteria:**` with categorized criteria (`_Functional:_`, `_Edge Cases:_`, etc.)
2. **Check metadata**: Look for `metadata.prd_path` field
3. **Check source reference**: Look for `Source: {path} Section {number}` in the description

If any check matches → **PRD-generated task** (use criterion-based verification)

If none match → **General task** (use inferred verification)

## 4-Phase Workflow

Execute each task through these phases in order:

### Phase 1: Understand

Load context and understand scope before writing code.

- Read the task-execution skill and references
- Read `.claude/execution-context.md` for learnings from prior tasks
- Load task details via `TaskGet`
- Classify the task (PRD-generated vs general)
- Parse acceptance criteria or infer requirements from description
- Explore affected files via Glob/Grep
- Read `CLAUDE.md` for project conventions

### Phase 2: Implement

Execute the code changes following project patterns.

- Read all target files before modifying them
- Follow the project's implementation order (data → service → interface → tests)
- Match existing coding patterns and conventions
- Write tests if specified in testing requirements
- Run mid-implementation checks (linter, existing tests) to catch issues early

### Phase 3: Verify

Verify implementation against task requirements using the adaptive approach.

- **PRD-generated tasks**: Walk each acceptance criteria category (Functional, Edge Cases, Error Handling, Performance), check testing requirements, run tests
- **General tasks**: Infer "done" from description, run existing tests, run linter, verify core change is implemented

### Phase 4: Complete

Report results and share learnings.

- Determine status (PASS/PARTIAL/FAIL) based on verification results
- If PASS: mark task as `completed` via `TaskUpdate`
- If PARTIAL or FAIL: leave as `in_progress` for the orchestrator to decide on retry
- Append learnings to `.claude/execution-context.md` (files discovered, patterns learned, issues encountered)
- Return structured report with verification results

## Adaptive Verification Overview

Verification adapts based on task type:

| Task Type | Verification Method | Pass Threshold |
|-----------|-------------------|----------------|
| PRD-generated | Criterion-by-criterion evaluation | All Functional + Tests must pass |
| General | Inferred checklist from description | Core change works + Tests pass |

**Critical rule**: All Functional criteria must pass for a PASS result. Edge Cases, Error Handling, and Performance failures result in PARTIAL but do not block completion.

## Shared Execution Context

Tasks within an execution session share learnings through `.claude/execution-context.md`:

- **Read at start**: Check for prior task learnings before beginning work
- **Write at end**: Always append learnings regardless of PASS/PARTIAL/FAIL
- **Sections**: Project Patterns, Key Decisions, Known Issues, File Map, Task History

This enables later tasks to benefit from earlier discoveries and retry attempts to learn from previous failures.

## Reference Files

- `references/execution-workflow.md` - Detailed phase-by-phase procedures for the 4-phase workflow
- `references/verification-patterns.md` - Task classification, criterion verification, pass/fail rules, and failure reporting format
