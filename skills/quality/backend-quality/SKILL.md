---
name: backend-quality
description: Runs backend quality checks including formatting, linting, and tests. Use before commits, to verify code quality, or when the user says "check backend", "run backend tests", "format backend".
allowed-tools: Bash(uv run ruff:*), Bash(uv run pytest:*), Bash(docker compose:*), Bash(task:*)
---

# Backend Quality Checks

Runs formatting, linting, and tests for the backend.

## Quick Run (Recommended)

Using task automation:
```bash
cd back && task format && task tests
```

Or run individually:

## 1. Format Code

```bash
cd back && task format
```

This runs pre-commit hooks including:
- **Ruff**: Linting and formatting
- **Autoflake**: Remove unused imports

## 2. Check Linting

```bash
cd back && uv run ruff check src tests
```

Fix issues automatically:
```bash
cd back && uv run ruff check --fix src tests
```

## 3. Check Formatting

```bash
cd back && uv run ruff format --check src tests
```

Apply formatting:
```bash
cd back && uv run ruff format src tests
```

## 4. Run Tests

All tests:
```bash
cd back && task tests
```

Or with pytest directly:
```bash
cd back && uv run pytest tests/ -v
```

Specific module:
```bash
cd back && uv run pytest tests/api/example/ -v
```

Single test file:
```bash
cd back && uv run pytest tests/api/example/domain/test_create_item.py -v
```

## Configuration

- **Ruff**: Configured in `back/pyproject.toml`
- **Line length**: 110 characters
- **Python version**: 3.13

## Common Issues

### Import Order
Ruff handles import sorting automatically. Run `task format` to fix.

### Unused Imports
Autoflake removes them. Run `task format` to fix.

### Type Hints
Use `|` for optional types:
```python
# Good
def foo(x: str | None) -> int | None:

# Bad (deprecated)
def foo(x: Optional[str]) -> Optional[int]:
```

### Test Failures
Check that Docker containers are running:
```bash
docker compose ps
```

If database tests fail, ensure database is initialized:
```bash
docker compose down && docker compose up -d
```

## Pre-commit Checklist

Before committing:
1. `task format` - Format and lint
2. `task tests` - Run all tests
3. Review changes
4. Commit
