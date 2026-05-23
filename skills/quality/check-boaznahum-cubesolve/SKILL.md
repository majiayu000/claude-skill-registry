---
name: check
user_invocable: true
description: |
  Code quality checker skill. This skill should be used when the user wants to:
  (1) Run static analysis tools (mypy, pyright, ruff) on the codebase - triggered by "/check", "/check q", or "/check quality"
  (2) Find dead/unused code (functions, imports, variables, unreachable code) - triggered by "/check d" or "/check dead"
---

# Code Quality Checker

This skill provides two main functions for maintaining code quality in this project.

## Commands

| Command | Aliases | Description |
|---------|---------|-------------|
| `/check quality` | `/check`, `/check q` | Run all static analysis tools |
| `/check dead` | `/check d` | Find dead/unused code |

## Quality Check (`/check`, `/check q`, `/check quality`)

Run all three static analysis tools on `src/cube/` in parallel:

```bash
# Run these 3 commands in parallel using the Bash tool
.venv/Scripts/python.exe -m ruff check src/cube
.venv/Scripts/python.exe -m mypy -p cube
.venv/Scripts/python.exe -m pyright src/cube
```

### Output Format

After running all checkers, provide a summary:

1. **Summary table** showing pass/fail status for each tool
2. **Grouped issues** by severity (errors first, then warnings)
3. **Actionable suggestions** for fixing the issues

### Offering to Fix

At the end, if there are fixable issues:

1. For **ruff** issues: Offer to run `.venv/Scripts/python.exe -m ruff check --fix src/cube` to auto-fix
2. For **mypy/pyright** issues: Group by category and offer to fix them one by one or in batches

Example conclusion:
```
## Summary
| Tool    | Status | Issues |
|---------|--------|--------|
| ruff    | FAIL   | 5      |
| mypy    | PASS   | 0      |
| pyright | FAIL   | 3      |

Would you like me to:
1. Auto-fix the 5 ruff issues with `ruff check --fix`?
2. Address the 3 pyright type errors?
```

## Dead Code Detection (`/check d`, `/check dead`)

Find unused code across the entire codebase using comprehensive analysis.

### Analysis Strategy

Use the Task tool with `subagent_type=Explore` to perform thorough dead code analysis:

1. **Unused imports** - Imports that are never used in the file
2. **Unused functions/methods** - Functions defined but never called
3. **Unused variables** - Variables assigned but never read
4. **Unused classes** - Classes defined but never instantiated or subclassed
5. **Unreachable code** - Code after return/raise/break/continue statements

### Execution Steps

1. Launch an Explore agent with thoroughness="very thorough" to analyze:
   - Search for all function/method definitions
   - Cross-reference with all call sites
   - Check `__all__` exports in `__init__.py` files
   - Consider dynamic usage patterns (e.g., `getattr`, reflection)

2. For each category, report:
   - File path and line number
   - The unused element name
   - Confidence level (high/medium/low)
   - Reason why it appears unused

### Output Format

```
## Dead Code Analysis Results

### Unused Functions (High Confidence)
- `src/cube/module.py:42` - `_old_helper()` - No callers found
- `src/cube/other.py:15` - `deprecated_func()` - No callers found

### Unused Imports (High Confidence)
- `src/cube/file.py:3` - `from typing import Optional` - Never used

### Potentially Unused (Medium Confidence)
- `src/cube/utils.py:88` - `helper_func()` - Only called via getattr

Would you like me to remove any of these?
```

### Caveats to Consider

- Functions referenced in `__all__` are public API (not dead)
- Methods may be called via inheritance or protocols
- Some code may be used dynamically (plugin systems, etc.)
- Test files may reference code that appears "unused" in src/
