---
name: ruff
description: This skill should be used when users need to lint, format, or validate Python code using the Ruff command-line tool. Use this skill for tasks involving Python code quality checks, automatic code formatting, enforcing style rules (PEP 8), identifying bugs and security issues, or modernizing Python code. This skill should be invoked PROACTIVELY whenever Python code is written or modified to ensure code quality.
---

# Ruff Skill

## Contents

- [Proactive Usage](#proactive-usage)
- [Quick Reference](#quick-reference)
- [Linting Workflow](#linting-workflow)
- [Formatting Workflow](#formatting-workflow)
- [Rule Selection](#rule-selection)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Proactive Usage

**IMPORTANT**: Use this skill proactively after writing or modifying Python code.

### Standard Workflow

```bash
# Step 1: Format the code
uv run ruff format .

# Step 2: Fix auto-fixable linting issues
uv run ruff check --fix .

# Step 3: Report remaining issues
uv run ruff check .
```

### Project Commands

```bash
just fmt-python    # Format Python code
just lint-python   # Lint Python code
```

## Quick Reference

### Commands

| Command | Purpose |
|---------|---------|
| `uv run ruff check .` | Lint code |
| `uv run ruff check --fix .` | Fix auto-fixable issues |
| `uv run ruff format .` | Format code |
| `uv run ruff format --check .` | Check formatting |
| `uv run ruff check --diff .` | Preview fixes |

### Common Flags

| Flag | Effect |
|------|--------|
| `--fix` | Auto-fix issues |
| `--unsafe-fixes` | Apply risky fixes |
| `--diff` | Show changes without applying |
| `--select E,F` | Check specific rules |
| `--ignore E501` | Skip specific rules |
| `--statistics` | Show issue counts |
| `--watch` | Continuous linting |

## Linting Workflow

### 1. Check for Issues

```bash
uv run ruff check .                    # All files
uv run ruff check src/                 # Directory
uv run ruff check script.py            # Single file
```

### 2. Auto-fix Safe Issues

```bash
uv run ruff check --fix .
```

### 3. Review Unsafe Fixes

```bash
uv run ruff check --diff --unsafe-fixes .   # Preview
uv run ruff check --fix --unsafe-fixes .    # Apply
```

### 4. Address Remaining Issues

Fix manually or suppress with `# noqa`:

```python
import unused_module  # noqa: F401
```

## Formatting Workflow

### 1. Format Code

```bash
uv run ruff format .
```

### 2. Check Without Modifying (CI/CD)

```bash
uv run ruff format --check .
```

### 3. Preview Changes

```bash
uv run ruff format --diff .
```

## Rule Selection

### Essential Rules (Start Here)

```toml
[tool.ruff]
select = ["F", "E", "I"]
```

| Prefix | Source | Purpose |
|--------|--------|---------|
| F | Pyflakes | Errors, undefined names |
| E | pycodestyle | PEP 8 errors |
| I | isort | Import sorting |

### Recommended Rules

```toml
[tool.ruff]
select = ["F", "E", "I", "W", "UP", "B", "SIM"]
```

| Prefix | Source | Purpose |
|--------|--------|---------|
| W | pycodestyle | PEP 8 warnings |
| UP | pyupgrade | Modernize syntax |
| B | bugbear | Likely bugs |
| SIM | simplify | Simplification |

### Security Rules

```toml
[tool.ruff]
extend-select = ["S"]
```

## Project Configuration

### Basic pyproject.toml

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

select = ["E", "F", "I", "B", "UP"]
ignore = ["E501"]

[tool.ruff.per-file-ignores]
"tests/**/*.py" = ["S101"]
"__init__.py" = ["F401"]

[tool.ruff.format]
quote-style = "double"
```

### Per-file Ignores

| Pattern | Common Ignores | Reason |
| --------- | ---------------- | -------- |
| `tests/**/*.py` | S101 | Allow assert |
| `__init__.py` | F401 | Allow unused imports |
| `scripts/*.py` | T201 | Allow print |

## Inline Suppression

```python
# Ignore all rules for line
import os  # noqa

# Ignore specific rule
import os  # noqa: F401

# Ignore for entire file (at top)
# ruff: noqa: F401
```

## Troubleshooting

### Too Many Issues

1. Start with essential rules only:
   ```bash
   uv run ruff check --select=F,E .
   ```

2. Add noqa comments to existing violations:
   ```bash
   uv run ruff check --add-noqa .
   ```

3. Fix auto-fixable issues first:
   ```bash
   uv run ruff check --fix .
   ```

4. Enable rules gradually over time

### Configuration Not Loading

1. Check file names: `ruff.toml`, `.ruff.toml`, or `pyproject.toml`
2. Validate syntax: `uv run ruff check --config=ruff.toml .`
3. Check for conflicts in parent directories

### Formatter vs Linter Conflicts

Run formatter before linter to avoid conflicts:

```bash
uv run ruff format .
uv run ruff check --fix .
```

### Output Formats for CI

```bash
uv run ruff check --output-format=github .   # GitHub Actions
uv run ruff check --output-format=gitlab .   # GitLab CI
uv run ruff check --output-format=json .     # JSON
```

## References

### Project References

- [Rules Reference](references/rules.md) - Complete rule descriptions by category
- [Configuration Reference](references/configuration.md) - Config templates and options

### External Resources

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Linter Rules](https://docs.astral.sh/ruff/rules/)
- [Formatter Docs](https://docs.astral.sh/ruff/formatter/)
- [Configuration](https://docs.astral.sh/ruff/configuration/)

## Best Practices

1. **Format first** - Run `ruff format` before `ruff check`
2. **Use --fix liberally** - Most auto-fixes are safe
3. **Review unsafe fixes** - Always check `--unsafe-fixes` changes
4. **Start simple** - Begin with F, E, I rules; expand gradually
5. **Configure CI/CD** - Enforce checks in continuous integration
6. **Document exceptions** - Comment why rules are disabled
