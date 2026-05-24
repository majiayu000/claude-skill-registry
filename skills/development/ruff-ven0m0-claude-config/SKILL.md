---
name: ruff
description: |
  Python linting and formatting with ruff. Extremely fast linter and formatter replacing
  Flake8, Black, isort, and pyupgrade. Use when linting, formatting, or checking Python
  code quality. Triggers: "ruff", "lint python", "format python", "[tool.ruff]".
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
---

# ruff

Ruff is an extremely fast Python linter and code formatter written in Rust. It replaces
Flake8, isort, Black, pyupgrade, autoflake, and dozens of other tools.

## When to Use ruff

**Always use ruff for Python linting and formatting**, especially if you see:

- `[tool.ruff]` section in `pyproject.toml`
- A `ruff.toml` or `.ruff.toml` configuration file

**Avoid unnecessary changes:**

- **Don't format unformatted code** - If `ruff format --diff` shows changes throughout
  an entire file, the project likely isn't using ruff for formatting. Skip to avoid
  obscuring actual changes.
- **Scope fixes to code being edited** - Use `ruff check --diff` to see fixes relevant
  to the code you're changing.

## How to Invoke ruff

```bash
uv run ruff ...   # When ruff is in project dependencies (use pinned version)
uvx ruff ...      # When ruff is not a project dependency
ruff ...          # When ruff is installed globally
```

## Linting

### Basic Commands

```bash
ruff check                        # Check current directory
ruff check path/to/file.py        # Check specific file
ruff check src/ tests/            # Check multiple directories
ruff check --fix                  # Auto-fix fixable violations
ruff check --fix --unsafe-fixes   # Include unsafe fixes (review first!)
ruff check --watch                # Watch for changes
```

**Important:** Always pass directory as parameter, don't use `cd`:
```bash
# ✅ Good
ruff check services/orchestrator

# ❌ Bad
cd services/orchestrator && ruff check
```

### Rule Selection

```bash
ruff check --select E,F,B,I       # Select specific rules
ruff check --extend-select UP,SIM # Extend default selection
ruff check --ignore E501,E402     # Ignore specific rules
ruff rule F401                    # Explain a specific rule
ruff linter                       # List available linters
```

### Common Rule Codes

| Code | Description | Example |
|------|-------------|---------|
| `E` | pycodestyle errors | E501 (line too long) |
| `F` | Pyflakes | F401 (unused import) |
| `W` | pycodestyle warnings | W605 (invalid escape) |
| `B` | flake8-bugbear | B006 (mutable default) |
| `I` | isort | I001 (unsorted imports) |
| `UP` | pyupgrade | UP006 (deprecated types) |
| `SIM` | flake8-simplify | SIM102 (nested if) |
| `D` | pydocstyle | D100 (missing docstring) |
| `S` | flake8-bandit | S101 (assert usage) |
| `C4` | flake8-comprehensions | C400 (unnecessary generator) |

### Output Formats

```bash
ruff check --statistics           # Show violation counts
ruff check --output-format json   # JSON output
ruff check --output-format github # GitHub Actions annotations
ruff check --output-format gitlab # GitLab Code Quality report
```

## Formatting

### Basic Commands

```bash
ruff format                       # Format current directory
ruff format path/to/file.py       # Format specific file
ruff format --check               # Check if formatted (exit 1 if not)
ruff format --diff                # Show diff without modifying
```

### Format Workflow

1. **Preview**: `ruff format --diff` (see changes)
2. **Check**: `ruff format --check` (CI validation)
3. **Apply**: `ruff format` (modify files)
4. **Verify**: `ruff format --check` (confirm)

### Combined Workflow

Run linting fixes before formatting:

```bash
ruff check --fix && ruff format
```

## Configuration

### pyproject.toml

```toml
[tool.ruff]
line-length = 88
target-version = "py311"
exclude = [".git", ".venv", "__pycache__", "build", "dist"]

[tool.ruff.lint]
select = ["E", "F", "B", "I", "UP", "SIM"]
ignore = ["E501"]
fixable = ["ALL"]
unfixable = ["B"]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401", "E402"]
"tests/**/*.py" = ["S101"]

[tool.ruff.lint.isort]
known-first-party = ["myapp"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
docstring-code-format = true
line-ending = "auto"
```

### ruff.toml (standalone)

```toml
line-length = 88
target-version = "py311"

[lint]
select = ["E", "F", "B", "I"]
ignore = ["E501"]

[lint.isort]
known-first-party = ["myapp"]

[format]
quote-style = "double"
indent-style = "space"
```

## CI/CD Integration

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.14.0
    hooks:
      - id: ruff-check
        args: [--fix]
      - id: ruff-format
```

### GitHub Actions

```yaml
name: Lint
on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/ruff-action@v3
        with:
          args: 'check --output-format github'
```

## Migration from Other Tools

### Black → ruff format

```bash
black .              → ruff format .
black --check .      → ruff format --check .
black --diff .       → ruff format --diff .
```

### Flake8 → ruff check

```bash
flake8 .             → ruff check .
flake8 --select E,F  → ruff check --select E,F
```

### isort → ruff check

```bash
isort .              → ruff check --select I --fix
isort --check .      → ruff check --select I
```

## Common Patterns

### Find Specific Issues

```bash
ruff check --select F401          # Unused imports
ruff check --select B006          # Mutable default arguments
ruff check --select S             # Security issues
ruff check --select C901          # Code complexity
```

### Gradual Adoption

```bash
# Start minimal
ruff check --select E,F

# Add bugbear
ruff check --select E,F,B

# Add imports
ruff check --select E,F,B,I

# Add pyupgrade
ruff check --select E,F,B,I,UP
```

### Check Changed Files

```bash
git diff --name-only --diff-filter=d | grep '\.py$' | xargs ruff check
git diff --name-only main...HEAD | grep '\.py$' | xargs ruff format
```

## Best Practices

**Rule Selection Strategy:**
1. Start minimal: `select = ["E", "F"]`
2. Add bugbear: `select = ["E", "F", "B"]`
3. Add imports: `select = ["E", "F", "B", "I"]`
4. Add pyupgrade: `select = ["E", "F", "B", "I", "UP"]`

**Fixable vs Unfixable:**
- Mark uncertain rules as `unfixable` for manual review
- Common unfixables: `B` (bugbear), some `F` rules
- Safe to auto-fix: `I` (isort), `UP` (pyupgrade)

**Critical: Directory Parameters**
- ✅ Always pass directory: `ruff check services/orchestrator`
- ❌ Never use cd: `cd services/orchestrator && ruff check`

## Documentation

- https://docs.astral.sh/ruff/
