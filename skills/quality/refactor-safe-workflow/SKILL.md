---
name: refactor-safe-workflow
description: Orchestrate safe refactoring with multi-step validation
version: 1.1.0
tags: [refactoring, architecture, safety]
owner: engineering
status: active
---

# Refactor Safe Workflow Skill

## Overview

Run safe refactors with validation and behavior preservation.

## Usage

```
/refactor-safe-workflow
```

## Identity
**Role**: Senior Architect & Refactorer
**Objective**: Restructure code to improve quality/maintainability without altering external behavior.

## Core Rules
1.  **Green-Red-Green**: Tests must pass before you start. If they fail mid-change, revert to Green immediately.
2.  **Steps, not Leaps**: Break changes into atomic moves (Rename, Extract, Move).
3.  **Preserve Behavior**: Do not fix bugs or add features during refactoring (unless blocking).

## Multi-Agent Pipeline

### Stage 1: Assessment (Architect Agent)
- **Input**: Target file/module.
- **Action**: Identify code smells (Long Method, God Class, Duplication).
- **Output**: architectural refactoring plan (`refactor_plan.md`).

### Stage 2: Safety Check (Test Writer Agent)
- **Action**: Run existing tests.
- **Gap Analysis**: If coverage < 100% on target logic, create **Characterization Tests**.
- **Goal**: Lock in current behavior (even bugs) to ensure we don't accidentally "fix" or break things silently.

### Stage 3: Execution (Refactorer Agent)
- **Loop**:
    1.  Apply **one** refactoring move from plan.
    2.  Run tests.
    3.  If Pass: Commit (`refactor: ...`).
    4.  If Fail: specific Undo changes, verify Assumption, Retry or Pivot.

### Stage 4: Review (Code Reviewer Agent)
- **Check**: Is the code *actually* better? (Cyclomatic complexity reduced? Naming clearer?).

## Usage Example
```
/refactor --target src/legacy/OrderManager.ts --goal "Extract Payment Logic"
```

## Error Recovery
- **Test Failure**: Instant revert (`git reset --hard HEAD`). Do not try to "debug" a refactoring. Logic should be preserved by definition.
- **Type Errors**: Fix immediately. Do not use `ts-ignore`.

## Outputs

- Refactor plan and validation notes.

## Related Skills

- `/verify-code` - Post-refactor review
