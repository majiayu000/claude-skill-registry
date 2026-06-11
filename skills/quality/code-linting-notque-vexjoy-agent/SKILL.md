---
name: code-linting
user-invocable: false
description: "Run Python (ruff) and JavaScript (Biome) linting."
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Edit
  - Write
routing:
  triggers:
    - "lint code"
    - "run ruff"
    - "run biome"
    - "format code"
    - "lint errors"
  category: code-quality
  pairs_with:
    - code-cleanup
    - universal-quality-gate
    - python-quality-gate
---

# Code Linting Skill

Unified linting workflow for Python (ruff) and JavaScript (Biome). Covers check, format, and auto-fix for both languages. Only handles Python and JavaScript/TypeScript -- complex logic issues and other languages are out of scope.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| Python violations, ruff rules, F401/E711/B006/UP errors | `ruff-rules-reference.md` | Routes to the matching deep reference |
| ruff not found, pyproject.toml config, ruff version differences | `ruff-rules-reference.md` | Routes to the matching deep reference |
| JavaScript/TypeScript violations, Biome rules, noVar/useConst/noDoubleEquals | `biome-rules-reference.md` | Routes to the matching deep reference |
| biome not found, biome.json config, migrating from ESLint | `biome-rules-reference.md` | Routes to the matching deep reference |
| Linting CI failures, format check vs lint check differences | `biome-rules-reference.md` | Routes to the matching deep reference |

## Instructions

### 1. Read Project Configuration

Before running any linter, read the repository's CLAUDE.md for project-specific linting rules -- those override every default below. Then locate the project's linter config files (`pyproject.toml` for ruff, `biome.json` for Biome). All linter invocations must use these configs as-is; never override line width, rule sets, or other project settings.

### 2. Detect Languages and Run Checks

When a project contains both Python and JavaScript/TypeScript, lint both unless the user explicitly requests a single language. Run the check command first to see what violations exist:

```bash
# Python -- use project venv when available
ruff check .
# or: ./venv/bin/ruff check .

# JavaScript/TypeScript
npx @biomejs/biome check src/
```

**Always display the complete linter output.** Never summarize results as "no issues found" or describe output secondhand -- show the actual command output so the user can see every error, warning, and style issue together.

### 3. Review Output Before Fixing

Read the full output and understand what violations exist and their severity before applying any fixes. Jumping straight to `--fix` without reviewing risks auto-removing imports that are still needed or making changes that reduce readability.

### 4. Apply Auto-Fixes

Apply `--fix` for safe categories: formatting, import ordering, and style issues that the linter can correct mechanically.

```bash
# Python
ruff check --fix .
ruff format .

# JavaScript/TypeScript
npx @biomejs/biome check --write src/
npx @biomejs/biome format --write src/
```

Only run the linters and fixes that were requested. Do not add custom rules, configuration changes, or additional tooling unless the user explicitly asks.

### 5. Review the Diff

After auto-fix, review the diff to verify changes are correct and safe:

```bash
git diff
```

Auto-fixes can occasionally remove imports that are still needed, reformat code in ways that hurt readability, or introduce subtle bugs through variable shadowing changes. Revert any problematic auto-fixes before proceeding.

### 6. Fix Remaining Issues Manually

For violations that cannot be auto-fixed, explain each one and how to resolve it:

**Python common fixes:**
- Unused import (F401): Remove or use the import
- Import order (I001): Run `ruff check --fix`
- Line too long (E501): Break into multiple lines or adjust line-length config

**JavaScript common fixes:**
- noVar: Replace `var` with `let`/`const`
- useConst: Use `const` for unchanging values
- noDoubleEquals: Use `===` instead of `==`

### 7. Verify Before Commit

Run the linter one final time to confirm zero violations before suggesting a commit:

```bash
ruff check .
ruff format --check .
npx @biomejs/biome check src/
```

Report output factually -- no self-congratulation, just the command results.

### 8. Clean Up

Remove any temporary lint report files or cache files created during execution.

### Combined Commands (if Makefile configured)

```bash
make lint       # Check both Python and JS
make lint-fix   # Fix both Python and JS
```

### Configuration Reference

| Tool | Config | Typical Line Width |
|------|--------|-------------------|
| ruff | pyproject.toml | 88-120 |
| biome | biome.json | 80-120 |

### Optional Modes

- **Strict mode**: Treat warnings as errors (fail on any issue) -- enable when requested
- **Format only**: Skip linting, only run formatting -- enable when requested
- **Ignore specific rules**: Disable particular lint rules for edge cases -- enable when requested

## Error Handling

### Error: "ruff not found"
**Cause**: Virtual environment not activated or ruff not installed
**Solution**:
- Use virtual environment path: `./venv/bin/ruff` or `./env/bin/ruff`
- Or install globally: `pip install ruff`
- Or use pipx: `pipx run ruff check .`

### Error: "biome not found"
**Cause**: Biome not installed in project
**Solution**: Run `npx @biomejs/biome` to use npx-based execution

### Error: "Configuration file not found"
**Cause**: Running from wrong directory
**Solution**: cd to project root where pyproject.toml/biome.json exist

## Reference Loading

Load these files when the task involves the corresponding domain:

| Task type | Reference file |
|-----------|---------------|
| Python violations, ruff rules, F401/E711/B006/UP errors | `references/ruff-rules-reference.md` |
| ruff not found, pyproject.toml config, ruff version differences | `references/ruff-rules-reference.md` |
| JavaScript/TypeScript violations, Biome rules, noVar/useConst/noDoubleEquals | `references/biome-rules-reference.md` |
| biome not found, biome.json config, migrating from ESLint | `references/biome-rules-reference.md` |
| Linting CI failures, format check vs lint check differences | `references/ruff-rules-reference.md` + `references/biome-rules-reference.md` |

## References

- [ruff documentation](https://docs.astral.sh/ruff/)
- [Biome documentation](https://biomejs.dev/)
