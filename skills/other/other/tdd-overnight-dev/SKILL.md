---
name: tdd-overnight-dev
description: Autonomous Feature-to-Commit TDD loop for long-running sessions
version: 1.1.0
tags: [tdd, autonomous, agile]
owner: engineering
status: active
---

# TDD Overnight Dev Skill

## Overview

Run a full TDD loop autonomously for long-running feature work.

## Usage

```
/tdd-overnight-dev
```

## Identity
**Role**: Autonomous Developer
**Objective**: Implement a feature from start to finish using a strict Test-Driven Development (TDD) loop, committing only when tests pass (Green state).

## Prerequisites
1.  **Specification**: A clear `spec.md` or `PRODUCT.md` section describing the feature.
2.  **Test Runner**: A working test command (e.g., `npm test`, `pytest`).
3.  **Git**: Clean working directory.

## Execution Loop

### Phase 1: Planning
1.  **Read Spec**: Analyze requirements.
2.  **Breakdown**: Create a task list in memory or `task.md`. Order by dependencies.

### Phase 2: The TDD Cycle (Repeat for each task)

#### 1. Red (Write Test)
- **Action**: Create/Update a test file verifying the specific requirement.
- **Goal**: The test *must* fail.
- **Check**: Run `npm test <test-file>`. Assert exit code != 0.

#### 2. Green (Make It Pass)
- **Action**: detailed implementation in source files.
- **Goal**: Pass the test with minimal code.
- **Check**: Run `npm test <test-file>`. Assert exit code == 0.
- **Retry**: If fail, read error -> fix code -> retry. Max 3 retries.

#### 3. Refactor (Clean Up)
- **Action**: Improve code structure/readability without changing behavior.
- **Check**: Run `npm test <test-file>`. Must remain Green.

#### 4. Checkpoint (Commit)
- **Action**: Use `git-committer-atomic`.
- **Message**: `feat(scope): implement <task>`

### Phase 3: Completion
- **Verify**: Run full test suite.
- **Report**: Generate a summary of implemented tasks and any skipped blockers.

## Constraints & Limits
- **Time/Cost**: If a single task cycle exceeds 10 minutes or 5 tool calls, **SKIP** and log as blocker.
- **No Blind Coding**: Never write source code before the test exists.
- **State Preservation**: If a task fails (cannot get to Green), `git reset --hard` to previous clean state before skipping.

## Output
- `implementation_log.md`: Log of tasks, test results, and decisions.

## Related Skills

- `/task` - Implement individual tasks with TDD
