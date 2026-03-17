---
name: clean-code
description: Format, lint, and fix all warnings across the entire codebase — including test files and pre-existing issues.
---

# Clean Code

Format, lint, and fix all warnings across the entire codebase — including test files and pre-existing issues.

## Usage

```
/clean-code
```

## Instructions

### 1. Run the project's clean-code target

Each project defines a `make clean-code` Makefile target with the appropriate tooling for its language/stack.

```bash
make clean-code
```

### 2. Fix remaining issues

If `make clean-code` fails or reports warnings/errors that couldn't be auto-fixed, investigate and fix them manually. Do NOT leave any warnings unresolved.

### 3. Verify clean state

Re-run the target to confirm it passes cleanly:

```bash
make clean-code
```

It must exit with zero warnings and zero errors.

## Rules

- Do not skip or suppress warnings (e.g. `eslint-disable`, `#[allow(...)]`, `@SuppressWarnings`) unless there is a genuine false positive with a clear justification
- Do not change the project's formatter or linter configuration
- If a fix changes behavior (not just style), flag it to the user before applying
- Test files are in scope — do not skip them
- Pre-existing issues must be fixed, not just new code
