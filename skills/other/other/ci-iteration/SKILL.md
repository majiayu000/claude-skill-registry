---
name: ci-iteration
description: >
  This skill should be used when running CI checks iteratively and fixing failures. Use when
  executing make targets (fast-ci, all-ci, ci), iterating on lint/format/type/test errors, or
  needing the devrun agent pattern for pytest/ty/ruff/prettier/make/gt commands.
---

# CI Iteration

## Overview

Run the specified CI target and automatically fix any failures. Keep iterating until all checks pass or you get stuck on an issue that requires human intervention.

**IMPORTANT**: All `make` commands must be run from the repository root directory. The Makefile is located at the root of the repository, not in subdirectories.

## Sub-Agent Policy

**CRITICAL**: When spawning sub-agents to run `make`, `pytest`, `ty`, `ruff`, `prettier`, or `gt` commands, you MUST use `devrun`:

```
Task tool with:
- subagent_type: devrun  <- MUST be devrun, NEVER general-purpose
```

**Why**: devrun has hard tool constraints (no Edit/Write) preventing destructive changes. The parent agent (you) processes reports and applies fixes - sub-agents only report.

**FORBIDDEN**:

- Spawning general-purpose or other sub-agents for make/pytest/ty/ruff/prettier/gt
- Giving sub-agents prompts like "fix issues" or "iterate until passing"

**REQUIRED**:

- Sub-agents run ONE command and report results
- Parent agent decides what to fix based on reports

## Core Workflow

### 1. Initial Run

Use the devrun agent to run the specified make target from the repository root:

```
Task tool with:
- subagent_type: devrun
- description: "Run [make target] from repo root"
- prompt: "Change to repository root and execute: [make target]"
```

### 2. Parse Failures

Analyze the output to identify which check(s) failed:

- **Ruff lint failures**: "ruff check" errors
- **Format failures**: "ruff format --check" or files needing reformatting
- **Prettier failures**: Markdown files needing formatting
- **MD-check failures**: CLAUDE.md files not properly referencing AGENTS.md
- **ty failures**: Type errors with file paths and line numbers
- **Test failures**: pytest failures with test names and assertion errors

### 3. Apply Targeted Fixes

Based on failure type, apply appropriate fixes:

| Failure Type | Fix Command                                 |
| ------------ | ------------------------------------------- |
| Ruff lint    | `make fix` via devrun                       |
| Ruff format  | `make format` via devrun                    |
| Prettier     | `make prettier` via devrun                  |
| Sync-Kit     | `erk sync` directly                         |
| MD-check     | Edit CLAUDE.md to contain only `@AGENTS.md` |
| ty           | Edit files to fix type annotations          |
| Tests        | Read and edit source/test files             |

### 4. Verify and Repeat

After applying fixes, run the make target again via devrun. Continue the cycle: run -> identify failures -> fix -> verify.

## Iteration Control

**Safety Limits:**

- **Maximum iterations**: 10 attempts
- **Stuck detection**: If the same error appears 3 times in a row, stop
- **Progress tracking**: Use TodoWrite to show iteration progress

## Progress Reporting

Use TodoWrite to track progress:

```
Iteration 1: Fixing lint errors
Iteration 2: Fixing format errors
Iteration 3: Fixing type errors in src/erk/cli/commands/switch.py
Iteration 4: All checks passed
```

## When to Stop

**SUCCESS**: Stop when the make target exits with code 0 (all checks passed)

**STUCK**: Stop and report to user if:

1. You've completed 10 iterations without success
2. The same error persists after 3 fix attempts
3. You encounter an error you cannot automatically fix

## Reporting Formats

### Success Format

```markdown
## Finalization Status: SUCCESS

All CI checks passed after N iteration(s):

(check) **Lint (ruff check)**: PASSED

(check) **Format (ruff format --check)**: PASSED

(check) **Prettier**: PASSED

(check) **AGENTS.md Standard (md-check)**: PASSED

(check) **ty**: PASSED

(check) **Tests**: PASSED

(check) **Sync-Kit (erk check)**: PASSED

The code is ready for commit/PR.
```

**IMPORTANT**: Each check line MUST be separated by a blank line in the markdown output to render properly in the CLI.

### Stuck Format

```markdown
## Finalization Status: STUCK

I was unable to resolve the following issue after N attempts:

**Check**: [lint/format/prettier/md-check/ty/test]

**Error**:
[Exact error message]

**File**: [file path if applicable]

**Attempted Fixes**:

1. [What you tried first]
2. [What you tried second]
3. [What you tried third]

**Next Steps**:
[Suggest what needs to be done manually]
```

## Guidelines

1. **Be systematic**: Fix one type of error at a time
2. **Run full CI**: Always run the full make target, not individual checks
3. **Use devrun agent**: Always use the Task tool with devrun agent for ALL make commands
4. **Run from repo root**: Always ensure make commands execute from repository root
5. **Track progress**: Use TodoWrite for every iteration
6. **Don't guess**: Read files before making changes
7. **Follow standards**: Adhere to AGENTS.md coding standards
8. **Fail gracefully**: Report clearly when stuck
9. **Be efficient**: Use targeted fixes (don't reformat everything for one lint error)

## Example Flow

```
Iteration 1:
- Use Task tool with devrun agent to run make target from repo root
- Found: 5 lint errors, 2 files need formatting
- Fix: Use Task tool with devrun agent to run make fix, then make format from repo root
- Result: 3 lint errors remain

Iteration 2:
- Use Task tool with devrun agent to run make target from repo root
- Found: 3 lint errors (imports)
- Fix: Edit files to fix import issues
- Result: All lint/format pass, 2 type errors

Iteration 3:
- Use Task tool with devrun agent to run make target from repo root
- Found: 2 ty errors in switch.py:45 and switch.py:67
- Fix: Add type annotations
- Result: All checks pass

SUCCESS
```

## Important Reminders

- NEVER run pytest/ty/ruff/prettier/make/gt directly via Bash
- Always use the Task tool with subagent_type: devrun
- Covered tools: pytest, ty, ruff, prettier, make, gt
- Always ensure make commands execute from the repository root directory
