---
name: run-tests
description: Run the full test suite with linting, type checking, and code quality audit
allowed-tools:
  - Bash
  - Grep
context: auto
---

# Run Tests Skill

Run the full test suite with linting, type checking, and code quality audit.

## When to Use

- After making code changes
- Before committing
- To verify code quality
- When asked to "run tests" or "check the code"

## Quick Run

Execute all checks in sequence:

```bash
# 1. Unit tests
uv run pytest MouseMaster/Testing/Python/ -v --tb=short

# 2. Linter
uv run ruff check .

# 3. Type checker
uv run mypy MouseMaster/MouseMasterLib/

# 4. Code quality audit
grep -rn "except.*:" MouseMaster/ --include="*.py" -A1 | grep -B1 "pass$" || echo "No except:pass found"
```

## Expected Results

| Check | Expected |
|-------|----------|
| Unit tests | 67+ passed |
| Ruff | 0 errors (or 1 import order) |
| Mypy | 0 errors |
| Audit | No except:pass patterns |

## If Tests Fail

1. Read the failing test output
2. Identify which test failed and why
3. Read the test file to understand what it checks
4. Read the code being tested
5. Fix the issue
6. Re-run tests

## If Lint Fails

Auto-fix safe issues:
```bash
uv run ruff check --fix .
```

For other issues, review and fix manually.

## If Audit Finds Issues

Follow `/fix-bad-practices` skill to correct:
- `except: pass` → specific exception + logging
- `except Exception` → specific exception types
- Silent continuation → explicit error handling

## Report Format

After running, summarize:

```
## Test Results

| Check | Status |
|-------|--------|
| Tests | ✓ 67 passed |
| Lint | ✓ clean |
| Types | ✓ clean |
| Audit | ✓ no violations |

Issues: None / [list issues]
```

## Related

- Agent: `.claude/agents/test-runner.md` - Full autonomous workflow
- Skill: `/audit-code-quality` - Detailed audit patterns
- Skill: `/fix-bad-practices` - Fix patterns
