---
name: setup-python
description: Sets up Python development environment using UV for fast dependency management. Configures virtual environment, dependencies, testing (pytest), linting/formatting (ruff), and type checking (mypy). ALWAYS use UV - NEVER use pip directly. Use when starting work on Python projects, after cloning Python repositories, setting up CI/CD for Python, or troubleshooting Python environment issues.
version: 2.0.0
---

# Python Development Setup Skill

## Purpose

Quickly set up and verify a Python development environment using **UV** for fast, reliable dependency management.

## CRITICAL: Always Use UV

**NEVER use pip directly. ALWAYS use UV for Python dependency management.**

UV is 10-100x faster than pip and provides:

- Deterministic dependency resolution
- Lockfile support
- Virtual environment management
- Drop-in pip replacement

## Workflow

### Quick Setup Checklist

1. ✅ Verify Python 3.10+
2. ✅ Install UV (required package manager)
3. ✅ Setup virtual environment with UV
4. ✅ Install dependencies
5. ✅ Setup Ruff (linting + formatting)
6. ✅ Setup MyPy (type checking)
7. ✅ Setup pytest (testing)
8. ✅ Setup pre-commit hooks
9. ✅ Verify imports and dependencies
10. ✅ Run quality checks
11. ✅ Run tests
12. ✅ Verify environment reproducibility

**For detailed step-by-step instructions with UV commands and troubleshooting, see `references/DETAILED-WORKFLOW.md`.**

## Troubleshooting

### Issue: "uv: command not found"

**Solution**: UV not installed

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Then restart shell or source profile
```

### Issue: "No Python found"

**Solution**: Install Python with UV

```bash
uv python install 3.12
```

### Issue: "Resolution failed"

**Solution**: Dependency conflict

```bash
# Show what's conflicting
uv pip install --dry-run -r requirements.txt

# Try with looser constraints
uv pip install --resolution=lowest .
```

### Issue: "ModuleNotFoundError: No module named 'X'"

**Solution**: Dependency not installed

```bash
uv pip install -e ".[dev]"
# or
uv pip install <module-name>
```

---

## Best Practices

1. **Always use UV** - Never use pip directly
2. **Use pyproject.toml** - Modern Python standard
3. **Use Ruff** - Replaces flake8, black, isort (faster)
4. **Lock dependencies** - Use `uv lock` or `uv pip compile`
5. **Pin Python version** - Use `uv python pin`
6. **Enable mypy strict mode** - Catch type errors early
7. **Use pre-commit hooks** - Automate checks
8. **Target 90%+ coverage** - Comprehensive testing

---

## Migration from pip

If you have an existing project using pip:

```bash
# Create new venv with UV
rm -rf venv .venv
uv venv

# Activate
source .venv/bin/activate

# Install existing requirements
uv pip install -r requirements.txt

# Generate lock file
uv pip compile requirements.txt -o requirements.lock
```

---

## Integration with Other Skills

This skill may be invoked by:

- **`quality-check`** - When checking Python code quality
- **`run-tests`** - When running Python tests
