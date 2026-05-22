---
name: python-quality-checker
description: Validate Python code quality with formatting, type checking, linting,
  and security analysis. Use for Python codebases to ensure PEP 8 compliance, type
  safety, and code quality.
allowed-tools: Read, Bash, Grep, Glob
---

# Python Quality Checker Skill

## Purpose

This skill provides comprehensive Python code quality validation including formatting (Black), type checking (mypy), linting (flake8/ruff), security analysis (bandit), and complexity analysis. Ensures code meets Python best practices and project standards.

## When to Use

- Validating Python code quality before commit
- Running pre-commit quality checks
- CI/CD quality gate validation
- Code review preparation
- Ensuring PEP 8 compliance
- Type safety validation
- Security vulnerability detection

## Quality Check Workflow

### 1. Environment Setup

**Verify Tools Installed:**
```bash
# Check Python version
python --version

# Check quality tools
black --version
mypy --version
flake8 --version
bandit --version

# Or install missing tools
pip install black mypy flake8 bandit ruff
```

**Install Development Dependencies:**
```bash
# Install all dev tools
pip install -e ".[dev]"

# Or from requirements
pip install -r requirements-dev.txt
```

**Deliverable:** Quality tools ready

---

### 2. Code Formatting Check (Black)

**Check Formatting:**
```bash
# Check if code is formatted
black --check src/ tests/

# Check with diff
black --check --diff src/ tests/

# Check specific files
black --check src/tools/feature/core.py

# Check with color output
black --check --color src/ tests/
```

**Auto-Format Code:**
```bash
# Format all code
black src/ tests/

# Format specific directory
black src/tools/feature/

# Format with specific line length
black --line-length 100 src/

# Preview changes without applying
black --check --diff src/
```

**Configuration (pyproject.toml):**
```toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # Directories
  \.eggs
  | \.git
  | \.venv
  | build
  | dist
)/
'''
```

**Deliverable:** Formatting validation report

---

### 3. Type Checking (mypy)

**Run Type Checks:**
```bash
# Check entire codebase
mypy src/

# Check specific module
mypy src/tools/feature/

# Check with stricter settings
mypy --strict src/

# Show error codes
mypy --show-error-codes src/

# Generate HTML report
mypy --html-report mypy-report/ src/
```

**Common Type Issues:**
```bash
# Check for missing type hints
mypy --disallow-untyped-defs src/

# Check for Any types
mypy --disallow-any-explicit src/

# Check for incomplete definitions
mypy --check-untyped-defs src/
```

**Configuration (pyproject.toml):**
```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true
show_error_codes = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

**Deliverable:** Type checking report

---

### 4. Linting (flake8/ruff)

**Flake8 Linting:**
```bash
# Lint entire codebase
flake8 src/ tests/

# Lint with statistics
flake8 --statistics src/

# Lint with detailed output
flake8 --show-source --show-pep8 src/

# Generate HTML report
flake8 --format=html --htmldir=flake8-report/ src/
```

**Ruff Linting (Faster Alternative):**
```bash
# Lint with ruff
ruff check src/ tests/

# Auto-fix issues
ruff check --fix src/ tests/

# Show violations
ruff check --output-format=full src/

# Specific rules
ruff check --select=E,F,I src/
```

**Flake8 Configuration (.flake8):**
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude =
    .git,
    __pycache__,
    .venv,
    venv,
    build,
    dist
max-complexity = 10
per-file-ignores =
    __init__.py:F401
```

**Ruff Configuration (pyproject.toml):**
```toml
[tool.ruff]
line-length = 88
target-version = "py311"
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "N",  # pep8-naming
    "UP", # pyupgrade
    "B",  # flake8-bugbear
    "C4", # flake8-comprehensions
]
ignore = ["E203", "W503"]
exclude = [
    ".git",
    "__pycache__",
    ".venv",
    "build",
    "dist",
]

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]
```

**Deliverable:** Linting report

---

### 5. Security Analysis (bandit)

**Run Security Checks:**
```bash
# Basic security scan
bandit -r src/

# Detailed report
bandit -r src/ -f json -o bandit-report.json

# Exclude test files
bandit -r src/ --exclude tests/

# Specific confidence level
bandit -r src/ -ll  # Low confidence
bandit -r src/ -l   # Medium confidence
bandit -r src/      # All levels

# Skip specific issues
bandit -r src/ -s B101,B601
```

**Common Security Issues:**
```bash
# Check for hardcoded passwords
bandit -r src/ -t B105,B106

# Check for SQL injection
bandit -r src/ -t B608

# Check for command injection
bandit -r src/ -t B602,B603

# Check for unsafe YAML loading
bandit -r src/ -t B506
```

**Configuration (.bandit):**
```yaml
# .bandit
exclude_dirs:
  - /tests/
  - /venv/
  - /.venv/

skips:
  - B101  # Skip assert warnings in production code
  - B601  # Skip shell=True warnings (if justified)

tests:
  - B201  # flask_debug_true
  - B501  # request_with_no_cert_validation
  - B502  # ssl_with_bad_version
```

**Deliverable:** Security analysis report

---

### 6. Import Sorting (isort)

**Check Import Organization:**
```bash
# Check imports
isort --check-only src/ tests/

# Check with diff
isort --check-only --diff src/ tests/

# Auto-fix imports
isort src/ tests/
```

**Configuration (pyproject.toml):**
```toml
[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
```

**Deliverable:** Import sorting validation

---

### 7. Complexity Analysis

**Check Code Complexity:**
```bash
# Cyclomatic complexity with radon
pip install radon
radon cc src/ -a

# Show complex functions (>10)
radon cc src/ -nc

# Maintainability index
radon mi src/

# Raw metrics
radon raw src/
```

**McCabe Complexity (via flake8):**
```bash
# Check complexity with flake8
flake8 --max-complexity=10 src/

# Show complexity metrics
pip install flake8-mccabe
flake8 --statistics --select=C src/
```

**Deliverable:** Complexity analysis report

---

### 8. Comprehensive Quality Check

**Run All Checks:**
```bash
#!/bin/bash
# scripts/quality-check.sh

set -e  # Exit on first error

echo "=== Python Quality Checks ==="

echo "1. Code Formatting (Black)..."
black --check src/ tests/

echo "2. Import Sorting (isort)..."
isort --check-only src/ tests/

echo "3. Type Checking (mypy)..."
mypy src/

echo "4. Linting (ruff)..."
ruff check src/ tests/

echo "5. Security Analysis (bandit)..."
bandit -r src/ -ll

echo "6. Complexity Check..."
radon cc src/ -nc

echo "=== All Quality Checks Passed ✅ ==="
```

**Make script executable:**
```bash
chmod +x scripts/quality-check.sh
./scripts/quality-check.sh
```

**Deliverable:** Comprehensive quality report

---

## Quality Standards

### Code Formatting
- [ ] All code formatted with Black
- [ ] Line length ≤ 88 characters
- [ ] Imports sorted with isort
- [ ] Trailing whitespace removed
- [ ] Consistent string quotes

### Type Checking
- [ ] All functions have type hints
- [ ] No `Any` types (except justified)
- [ ] No missing return types
- [ ] No implicit Optional
- [ ] mypy passes with no errors

### Linting
- [ ] No PEP 8 violations
- [ ] No undefined names
- [ ] No unused imports
- [ ] No unused variables
- [ ] Complexity ≤ 10 per function

### Security
- [ ] No hardcoded secrets/passwords
- [ ] No SQL injection vulnerabilities
- [ ] No command injection risks
- [ ] Safe YAML/pickle usage
- [ ] Proper input validation

### Code Quality
- [ ] Functions < 50 lines
- [ ] Files < 500 lines
- [ ] Classes < 300 lines
- [ ] Max nesting depth: 4
- [ ] Cyclomatic complexity < 10

---

## Quality Check Matrix

| Check | Tool | Threshold | Auto-Fix |
|-------|------|-----------|----------|
| Formatting | Black | Must pass | Yes |
| Type hints | mypy | 0 errors | No |
| Linting | ruff/flake8 | 0 errors | Partial |
| Imports | isort | Must pass | Yes |
| Security | bandit | 0 high severity | No |
| Complexity | radon | ≤ 10 | No |

---

## Pre-commit Integration

**Setup pre-commit hooks:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ["-ll", "-r", "src/"]
```

**Install and run:**
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

**Deliverable:** Pre-commit hooks configured

---

## CI/CD Integration

**GitHub Actions Example:**
```yaml
# .github/workflows/quality.yml
name: Python Quality Checks

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install black mypy ruff bandit isort radon
          pip install -r requirements.txt

      - name: Check formatting
        run: black --check src/ tests/

      - name: Check imports
        run: isort --check-only src/ tests/

      - name: Type checking
        run: mypy src/

      - name: Linting
        run: ruff check src/ tests/

      - name: Security scan
        run: bandit -r src/ -ll

      - name: Complexity check
        run: radon cc src/ -nc
```

**Deliverable:** CI/CD quality pipeline

---

## Quality Check Troubleshooting

### Black Formatting Failures

```bash
# Check what would change
black --check --diff src/

# Apply fixes
black src/

# Check specific file
black --check src/tools/feature/core.py
```

### mypy Type Errors

```bash
# Show detailed error
mypy --show-error-codes src/

# Check specific file
mypy src/tools/feature/core.py

# Ignore specific error (last resort)
# type: ignore[error-code]
```

### Ruff/Flake8 Violations

```bash
# Show violation details
ruff check --output-format=full src/

# Auto-fix safe violations
ruff check --fix src/

# Ignore specific line (last resort)
# noqa: F401
```

### Bandit Security Issues

```bash
# Show detailed report
bandit -r src/ -f json

# Skip false positives
# nosec B101

# Exclude specific tests
bandit -r src/ -s B101,B601
```

---

## Quality Report Template

```markdown
# Python Quality Check Report

## Summary
- **Status**: ✅ All checks passed
- **Date**: 2024-01-15
- **Code Base**: src/

## Checks Performed

### Formatting (Black)
- **Status**: ✅ PASS
- **Files Checked**: 45
- **Issues**: 0

### Type Checking (mypy)
- **Status**: ✅ PASS
- **Files Checked**: 45
- **Errors**: 0
- **Warnings**: 0

### Linting (ruff)
- **Status**: ✅ PASS
- **Files Checked**: 45
- **Violations**: 0

### Security (bandit)
- **Status**: ✅ PASS
- **Files Scanned**: 45
- **High Severity**: 0
- **Medium Severity**: 0
- **Low Severity**: 2 (acceptable)

### Complexity (radon)
- **Status**: ✅ PASS
- **Average Complexity**: 4.2
- **Max Complexity**: 8
- **Files > 10**: 0

## Details

All Python quality checks passed successfully. Code is well-formatted, type-safe, lint-free, secure, and maintainable.

## Recommendations

- Continue maintaining type hints for all new functions
- Keep cyclomatic complexity below 10
- Run pre-commit hooks before commits
```

---

## Integration with Code Quality Specialist

**Input:** Python codebase quality check request
**Process:** Run all Python quality tools and analyze results
**Output:** Comprehensive quality report with pass/fail status
**Next Step:** Report to code-quality-specialist for consolidation

---

## Best Practices

### Development
- Run Black on save (IDE integration)
- Enable mypy in IDE for real-time feedback
- Use pre-commit hooks
- Fix linting issues immediately

### Pre-Commit
- Run full quality check script
- Ensure all checks pass
- Fix issues before pushing
- Review security warnings

### CI/CD
- Run quality checks on every PR
- Fail build on quality violations
- Generate quality reports
- Track quality metrics over time

### Code Review
- Verify quality checks passed
- Review type hints
- Check security scan results
- Validate complexity metrics

---

## Supporting Resources

- **Black**: https://black.readthedocs.io
- **mypy**: https://mypy.readthedocs.io
- **ruff**: https://docs.astral.sh/ruff
- **bandit**: https://bandit.readthedocs.io
- **isort**: https://pycqa.github.io/isort
- **radon**: https://radon.readthedocs.io

---

## Success Metrics

- [ ] All code formatted with Black
- [ ] All type checks passing
- [ ] Zero linting violations
- [ ] No high-severity security issues
- [ ] Complexity under threshold
- [ ] All quality checks automated