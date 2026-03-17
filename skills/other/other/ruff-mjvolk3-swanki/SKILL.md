---
name: ruff
description: Run ruff linter on staged or specified Python files and fix errors following the project's lint strategy.
---

# Ruff Linter

Run ruff check on staged or specified Python files, then fix errors following the project's lint conventions.

## Workflow

```
(edit python) -> /ruff -> /update-py-notes -> /commit
```

## Arguments

- **With arguments** (e.g., `/ruff swanki/config.py`): run ruff on the specified files only.
- **No arguments**: run ruff on all staged `.py` files under `swanki/` and `tests/`. If nothing is staged, run on both directories.

## Step 1: Determine target files

- **If arguments provided**: use the listed file paths directly.
- **If no arguments**: run `git diff --cached --name-only -- '*.py'` to get staged `.py` files. If none, target `swanki/` and `tests/` as a whole.

## Step 2: Run ruff check

```bash
/Users/michaelvolk/opt/miniconda3/envs/swanki/bin/python -m ruff check <files_or_dirs>
```

If ruff passes clean, inform the user and stop.

## Step 3: Auto-fix safe errors

Run ruff with `--fix` for auto-fixable issues (import sorting, unused imports, etc.):

```bash
/Users/michaelvolk/opt/miniconda3/envs/swanki/bin/python -m ruff check --fix <files_or_dirs>
```

## Step 4: Fix remaining errors by type

For errors that cannot be auto-fixed, apply the appropriate strategy:

### Import rules (`I001`, `I002`)

Auto-fixed by `--fix`. If not, manually reorder imports to match isort convention (stdlib, third-party, local).

### Unused imports (`F401`)

Auto-fixed by `--fix`. If the import is intentional (side-effect import), add `# noqa: F401`.

### Unused variables (`F841`)

Remove the variable or prefix with `_` if the assignment has a needed side effect.

### Pyupgrade (`UP` rules)

Auto-fixed by `--fix`. These modernize syntax to Python 3.11+ (e.g., `dict` instead of `typing.Dict`).

### Docstring rules (`D` rules)

These are the most common manual fixes:

#### `D100` - Missing module docstring
Add a module-level docstring. For source files, use the project's frontmatter pattern:
```python
"""
module/path
[[module.path]]
https://github.com/Mjvolk3/Swanki/tree/main/module/path
"""
```

#### `D101` - Missing class docstring
Add a one-line docstring describing the class purpose.

#### `D102` - Missing method docstring
Add a docstring describing what the method does.

#### `D103` - Missing function docstring
Add a docstring.

#### `D417` - Missing description for parameter
Add the missing `Args:` entry in Google-style docstring.

### Pycodestyle (`E` rules)

#### `E501` - Line too long
IGNORED globally. No action needed.

#### Other `E` rules
Fix the style issue (whitespace, indentation, etc.). Usually auto-fixed by `--fix`.

### Pyflakes (`F` rules)

#### `F811` - Redefined unused name
Remove the duplicate definition or rename.

#### `F821` - Undefined name
Add the missing import or fix the typo.

## Step 5: Run ruff format (if needed)

If you made manual edits, run the formatter to ensure consistent style:

```bash
/Users/michaelvolk/opt/miniconda3/envs/swanki/bin/python -m ruff format <files_or_dirs>
```

## Step 6: Re-run ruff check

Run ruff again to verify all fixes. If new errors appear, fix them. Repeat until clean.

## Step 7: Stage fixed files

Run `git add <fixed_files>` for all files that were modified during fixing.

## Project Ruff Configuration

Defined in `pyproject.toml`:
- **Rules**: E, F, I, UP, D (pycodestyle, pyflakes, isort, pyupgrade, pydocstyle)
- **Ignored globally**: E501, D205, D212, D415 (line length, frontmatter docstring exceptions)
- **Per-file ignores**:
  - `tests/**`: D103, D104 (pytest hooks, __init__)
  - `notes/assets/scripts/**`: D100, D103
- **Convention**: Google-style docstrings
- **Format**: double quotes

## Important Rules

- NEVER add blanket `# noqa` without a specific rule code
- NEVER disable rules globally in pyproject.toml without discussing with the user
- Prefer fixing the code over suppressing the warning
- Do NOT ask extra approval questions -- tool approval prompts are the gates

## Example Invocations

- `/ruff` -- check all staged Python files (or entire project)
- `/ruff swanki/config.py` -- check a specific file
- `/ruff tests/` -- check all test files
- "run ruff on the processing module"
- "fix lint errors in pdf_processor.py"
