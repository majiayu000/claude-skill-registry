---
name: quality
description: Review recent code changes with "fresh eyes" and fix any issues found. Use before commits to catch bugs. Trigger with /quality or before git commit, bd sync, or bd close.
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git show:*), Bash(uv run ruff *), Bash(uv run mypy *), Read, Edit, Glob, Grep
---

Review all code changes with "fresh eyes" before committing. This catches bugs that accumulate during implementation when focus is on making things work.

This is a **Python ML project** using PyTorch, transformers, and type hints throughout.

## Why This Matters

During implementation, we focus on "does it work?" and can miss:
- Logic errors that compile but behave incorrectly
- Missing error handling for edge cases
- Type mismatches or implicit conversions
- Dead code or unused imports
- Integration issues between components

## Process

### 1. Identify Changed Files

```bash
git status
git diff HEAD --name-only
```

### 2. Read ENTIRE Files (Not Just Diffs)

For each changed file, read the **complete file** to understand full context. Diffs show what changed but hide the surrounding code that may be affected.

### 3. Review Checklist

For each file, check:

**Logic & Correctness**
- [ ] Does the logic match the intended behavior?
- [ ] Are edge cases handled (null, empty, boundary values)?
- [ ] Are error conditions caught and handled appropriately?

**Type Safety**
- [ ] Are types consistent throughout the call chain?
- [ ] Are there implicit type conversions that could fail?

**Integration**
- [ ] Do function signatures match their call sites?
- [ ] Are API contracts (request/response shapes) consistent?
- [ ] Do state updates flow correctly between components?

**Code Hygiene**
- [ ] Remove dead code, unused imports, commented-out code
- [ ] Remove debug statements (`print(`, `breakpoint()`, `pdb.set_trace()`, `ic()`)
- [ ] Are variable names clear and consistent?

**ML/PyTorch Specific**
- [ ] Tensor shapes consistent across operations?
- [ ] Device placement consistent (`.to(device)` not mixed with hardcoded "cuda"/"cpu")?
- [ ] Gradients handled correctly (`.detach()` when needed, no unintended graph retention)?
- [ ] Numerical stability (division by small values uses epsilon, no log(0))?

### 4. Run Automated Checks

```bash
uv run ruff check src/
uv run mypy src/
```

Fix any issues these tools report before proceeding.

### 5. Fix Issues Immediately

When you find an issue:
1. Fix it using the Edit tool
2. Document what you fixed in the summary

Do NOT just flag issues—fix them. Only flag issues that require human judgment (design decisions, unclear requirements).

### 6. Report Summary

After reviewing all files, provide:

```
## Quality Review Summary

**Files Reviewed:** <list>

**Issues Fixed:**
- <file>: <what was fixed and why>

**Issues for Human Review:** (if any)
- <file>: <issue that requires human decision>

**Confidence:** <High/Medium/Low> - <brief explanation>
```
