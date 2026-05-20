---
name: pre-commit-validation
description: Ensures all quality checks pass locally before committing changes. Use this skill to validate code quality, tests, and type checking before creating commits to catch issues early and avoid CI failures.
license: MIT
metadata:
  version: "1.0.0"
  workflow: "code changes -> run validation -> commit"
---

# Pre-Commit Validation

This skill ensures code quality and test coverage before committing changes to the repository.

## Purpose

Run comprehensive validation locally before committing to:
- Catch issues early (before CI runs)
- Ensure all tests pass
- Verify code quality (linting, formatting, type checking)
- Maintain code coverage standards
- Reduce CI failures and iteration time

## Validation Checklist

Before creating any commit, ensure ALL of the following pass:

### 1. Run Tests

```bash
# Run all tests
pytest tests/

# Or with coverage (recommended)
pytest tests/ --cov=src --cov-report=term
```

**Requirements:**
- ✅ All tests must pass (exit code 0)
- ✅ No test failures or errors
- ✅ Coverage should not decrease (if checking coverage)

### 2. Run Code Quality Checks

```bash
# Check formatting
black --check src/ tests/

# Check linting
ruff check src/ tests/

# Check types
mypy src/ --strict --explicit-package-bases
```

**Requirements:**
- ✅ All checks must pass (exit code 0)
- ✅ No formatting issues
- ✅ No linting errors
- ✅ No type errors

### 3. Run Pre-commit Hooks (Optional but Recommended)

```bash
# Run all pre-commit hooks manually
pre-commit run --all-files
```

**Note**: Pre-commit hooks run automatically on `git commit`, but running them manually gives faster feedback.

## Workflow Integration

### When to Use This Skill

Use this skill in the following scenarios:

1. **Before any commit**: Always run validation before creating a commit
2. **After implementing features**: Before committing new code
3. **After refactoring**: Before committing refactored code
4. **Before pushing**: As a final check before pushing to remote
5. **When pre-commit is skipped**: If using `git commit --no-verify`, run validation manually

### Integration with Phase Implementation

When implementing features following the phase-implementation skill:

1. Implement code changes
2. **Run pre-commit validation** (this skill)
3. Fix any issues found
4. Repeat validation until all checks pass
5. Commit changes (following commit-format skill)
6. Push to GitHub

## Quick Validation Command

For convenience, you can run all checks in sequence:

```bash
# Run all validation checks
pytest tests/ --cov=src --cov-report=term && \
black --check src/ tests/ && \
ruff check src/ tests/ && \
mypy src/ --strict --explicit-package-bases
```

If all commands succeed (exit code 0), you're ready to commit.

## Auto-fix Common Issues

Many issues can be auto-fixed:

```bash
# Auto-fix formatting
black src/ tests/

# Auto-fix linting issues (many can be fixed automatically)
ruff check --fix src/ tests/
```

After auto-fixing, re-run validation to ensure everything passes.

## Handling Failures

### Test Failures

1. **Review test output**: Understand why tests are failing
2. **Fix the code**: Address the root cause
3. **Re-run tests**: Verify the fix works
4. **Run full test suite**: Ensure no regressions

### Code Quality Failures

1. **Formatting issues**: Run `black src/ tests/` to auto-fix
2. **Linting errors**: Run `ruff check --fix src/ tests/` to auto-fix many issues
3. **Type errors**: Fix type annotations or add type ignores (with justification)
4. **Re-run checks**: Verify all issues are resolved

### Coverage Decreases

1. **Review coverage report**: Identify uncovered code
2. **Add tests**: Write tests for uncovered code paths
3. **Verify coverage**: Ensure coverage meets or exceeds threshold (80%)

## Best Practices

1. **Run validation frequently**: Don't wait until the end - validate after each logical change
2. **Fix issues immediately**: Address problems as soon as they're found
3. **Don't skip validation**: Even for small commits, run at least basic checks
4. **Use pre-commit hooks**: They provide automatic validation, but manual checks are still valuable
5. **Check coverage regularly**: Ensure test coverage doesn't regress

## Relationship to CI/CD

**Important**: Local validation does NOT replace CI/CD checks.

- **Local validation** (this skill): Fast feedback, catch issues early
- **CI/CD pipeline**: Final gate, runs on all pushes and PRs

Even if local validation passes, CI may still catch:
- Environment-specific issues
- Issues missed locally
- Integration problems

However, running validation locally:
- Reduces CI failures
- Provides faster feedback
- Saves CI resources
- Improves development workflow

## Exceptions

### When to Skip Validation

Validation should only be skipped in exceptional circumstances:

1. **WIP commits**: Work-in-progress commits with `[WIP]` prefix (but still validate before final commit)
2. **Merge commits**: Usually safe to skip (CI will validate)
3. **Documentation-only changes**: May skip type checking, but still run formatting/linting

**Note**: Even in exceptions, consider running at least formatting checks to maintain code quality.

## See Also

- [Development Workflow](docs/DEVELOPMENT.md#development-workflow) - General development guidelines
- [Pre-commit Hooks Setup](docs/DEVELOPMENT.md#pre-commit-hooks-setup) - Automatic validation setup
- [Commit Message Conventions](docs/DEVELOPMENT.md#commit-message-conventions) - Commit format guidelines
