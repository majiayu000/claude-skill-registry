---
name: autonomous-code-review
description: Run comprehensive code quality checks, tests, and fixes autonomously
allowed-tools:
  - Bash
  - Read
  - Grep
  - Edit
context: auto
---

# Autonomous Code Review Skill

Run comprehensive code quality checks, tests, and fixes without human intervention.

## When to Use

Use this skill:
- For autonomous code quality maintenance
- When instructed to "review and fix code"
- As a regular maintenance task
- After completing a feature or fix

## Philosophy: LLM-Human Collaboration

This skill enables Claude to work autonomously on code quality:

1. **Run tests first** - Understand current state
2. **Identify issues** - Audit for bad practices
3. **Fix systematically** - Apply fixes one at a time
4. **Verify each fix** - Run tests after each change
5. **Report clearly** - Enable human oversight

---

## Autonomous Workflow

### Phase 1: Assess Current State

```bash
echo "=== Phase 1: Current State Assessment ==="

# 1.1 Check git status
echo "## Git Status"
git status --short

# 1.2 Run existing tests
echo "## Running Tests"
uv run pytest MouseMaster/Testing/Python/ -v --tb=short 2>&1 | tee /tmp/test_results.txt
TEST_EXIT=$?

if [ $TEST_EXIT -eq 0 ]; then
    echo "✓ All tests passing"
else
    echo "✗ Some tests failing - review before proceeding"
    grep -E "FAILED|ERROR" /tmp/test_results.txt
fi

# 1.3 Run linting
echo "## Running Linter"
uv run ruff check . 2>&1 | tee /tmp/lint_results.txt
LINT_EXIT=$?

if [ $LINT_EXIT -eq 0 ]; then
    echo "✓ No linting errors"
else
    echo "✗ Linting issues found"
fi

# 1.4 Run type checking
echo "## Running Type Checker"
uv run mypy MouseMaster/MouseMasterLib/ 2>&1 | tee /tmp/mypy_results.txt || true
```

### Phase 2: Audit Code Quality

```bash
echo "=== Phase 2: Code Quality Audit ==="

# 2.1 Exception swallowing (CRITICAL)
echo "## Critical: Exception Swallowing"
EXCEPT_PASS=$(grep -rn "except.*:" MouseMaster/ --include="*.py" -A1 2>/dev/null | grep -c "pass$" || echo 0)
echo "Found: $EXCEPT_PASS instances of except...pass"

# 2.2 Broad exceptions (HIGH)
echo "## High: Broad Exceptions"
BROAD_EXCEPT=$(grep -rn "except Exception\b\|except:$" MouseMaster/ --include="*.py" 2>/dev/null | wc -l || echo 0)
echo "Found: $BROAD_EXCEPT broad exception handlers"

# 2.3 Missing logging in except blocks
echo "## Medium: Missing Logging"
# Complex pattern - needs manual review
grep -rn "except.*:" MouseMaster/ --include="*.py" -A3 2>/dev/null | head -50

# 2.4 Silent returns
echo "## Medium: Silent Returns"
grep -rn "return None$\|return$" MouseMaster/ --include="*.py" -B2 2>/dev/null | grep -E "(if|error|fail)" | head -20
```

### Phase 3: Generate Issue List

Create a prioritized list of issues to fix:

```python
#!/usr/bin/env python3
"""Generate prioritized issue list for autonomous fixing."""

import subprocess
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List
from enum import Enum

class Priority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

@dataclass
class Issue:
    file: Path
    line: int
    priority: Priority
    category: str
    pattern: str
    context: str

def find_except_pass(src_dir: Path) -> List[Issue]:
    """Find except:pass patterns."""
    issues = []
    for py_file in src_dir.rglob("*.py"):
        content = py_file.read_text()
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if re.search(r'except.*:\s*$', line):
                # Check next non-empty line
                for j in range(i+1, min(i+3, len(lines))):
                    if lines[j].strip() == 'pass':
                        issues.append(Issue(
                            file=py_file,
                            line=i+1,
                            priority=Priority.CRITICAL,
                            category="exception_swallowing",
                            pattern="except:pass",
                            context='\n'.join(lines[max(0,i-1):min(len(lines),i+3)])
                        ))
                        break
    return issues

def find_broad_except(src_dir: Path) -> List[Issue]:
    """Find overly broad exception handlers."""
    issues = []
    for py_file in src_dir.rglob("*.py"):
        content = py_file.read_text()
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if re.search(r'except\s+(Exception|BaseException)\b', line) or \
               re.search(r'except\s*:\s*$', line):
                issues.append(Issue(
                    file=py_file,
                    line=i+1,
                    priority=Priority.HIGH,
                    category="broad_exception",
                    pattern="except Exception/except:",
                    context='\n'.join(lines[max(0,i-1):min(len(lines),i+5)])
                ))
    return issues

# Run and output
if __name__ == "__main__":
    src = Path("MouseMaster")
    all_issues = find_except_pass(src) + find_broad_except(src)
    all_issues.sort(key=lambda x: x.priority.value)

    print(f"Found {len(all_issues)} issues:\n")
    for issue in all_issues:
        print(f"[{issue.priority.name}] {issue.file}:{issue.line}")
        print(f"  Category: {issue.category}")
        print(f"  Pattern: {issue.pattern}")
        print(f"  Context:\n{issue.context}\n")
```

### Phase 4: Fix Issues Systematically

For each issue, following this process:

```
1. Read the file containing the issue
2. Understand the context (what was the intent?)
3. Determine appropriate fix:
   - If error should crash: remove try/except
   - If specific handling needed: use specific exception + logging
   - If recovery is valid: add logging + handle gracefully
4. Apply the fix using Edit tool
5. Run tests to verify fix didn't break anything
6. If tests pass, continue to next issue
7. If tests fail, investigate and adjust fix
```

### Phase 5: Verify All Fixes

```bash
echo "=== Phase 5: Verification ==="

# 5.1 Run full test suite
echo "## Running Tests"
uv run pytest MouseMaster/Testing/Python/ -v
TEST_EXIT=$?

# 5.2 Run linting
echo "## Running Linter"
uv run ruff check .
LINT_EXIT=$?

# 5.3 Run type checking
echo "## Running Type Checker"
uv run mypy MouseMaster/MouseMasterLib/

# 5.4 Re-run audit
echo "## Re-running Audit"
EXCEPT_PASS=$(grep -rn "except.*:" MouseMaster/ --include="*.py" -A1 2>/dev/null | grep -c "pass$" || echo 0)
BROAD_EXCEPT=$(grep -rn "except Exception\b\|except:$" MouseMaster/ --include="*.py" 2>/dev/null | wc -l || echo 0)

echo ""
echo "=== Summary ==="
echo "Tests: $([ $TEST_EXIT -eq 0 ] && echo 'PASS' || echo 'FAIL')"
echo "Lint: $([ $LINT_EXIT -eq 0 ] && echo 'PASS' || echo 'FAIL')"
echo "Remaining except:pass: $EXCEPT_PASS"
echo "Remaining broad except: $BROAD_EXCEPT"
```

### Phase 6: Report Results

Generate a clear report:

```markdown
## Autonomous Code Review Report

**Date**: YYYY-MM-DD
**Duration**: X minutes
**Scope**: MouseMaster/

### Initial State
- Tests: X passing, Y failing
- Lint errors: X
- Critical issues: X
- High issues: X

### Fixes Applied

| File | Line | Issue | Fix Applied |
|------|------|-------|-------------|
| file.py | 42 | except:pass | Replaced with specific exception + logging |

### Final State
- Tests: X passing, Y failing
- Lint errors: X
- Critical issues: X (was Y)
- High issues: X (was Y)

### Remaining Issues
[List any issues that couldn't be auto-fixed]

### Recommendations
[Human action needed for complex issues]
```

---

## Decision Rules for Autonomous Fixing

### When to Auto-Fix

✓ **Auto-fix these patterns**:
- `except: pass` → Add logging and re-raise
- `except Exception: pass` → Add logging and re-raise
- Missing `check=True` in subprocess calls
- Bare `except:` → `except Exception:`

### When to Flag for Human Review

⚠ **Flag these for review**:
- Complex exception handling with multiple branches
- Exception handling in critical paths (data persistence, etc.)
- Patterns that might be intentional (e.g., plugin loading)
- Any fix that causes test failures

### When NOT to Fix

✗ **Don't auto-fix**:
- Code in third-party or vendored directories
- Test files (test code may intentionally test error cases)
- Code marked with `# noqa` or explicit comments explaining the pattern
- Patterns you don't fully understand

---

## Logging Requirements

All exception handling must include logging:

```python
import logging

logger = logging.getLogger(__name__)

# In except blocks, use exception() to include stack trace
try:
    risky_operation()
except SpecificError as e:
    logger.exception("Failed to perform risky_operation: %s", e)
    raise
```

---

## Test Requirements

After fixing error handling:

1. **Existing tests must pass** - Fixes shouldn't break functionality
2. **Add tests for error paths** - Test that errors are raised correctly
3. **Test logging output** - Verify errors are logged (optional but good)

Example error path test:

```python
import pytest

def test_load_preset_invalid_json(tmp_path):
    """Test that invalid JSON raises appropriate error."""
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("not valid json")

    with pytest.raises(json.JSONDecodeError):
        PresetManager.load_preset(bad_file)

def test_load_preset_missing_file():
    """Test that missing file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        PresetManager.load_preset(Path("/nonexistent"))
```

---

## Continuous Quality Commands

Run these regularly or in CI:

```bash
# Full quality check
uv run pytest MouseMaster/Testing/Python/ -v && \
uv run ruff check . && \
uv run mypy MouseMaster/MouseMasterLib/

# Quick audit
grep -rn "except.*:" MouseMaster/ --include="*.py" -A1 | grep -B1 "pass$"

# Pre-commit (if configured)
uv run pre-commit run --all-files
```

---

## Autonomous Session Example

Here's how Claude should approach an autonomous review session:

```
Human: Review and fix code quality issues

Claude:
1. I'll run the test suite first to understand the baseline
   [Runs: uv run pytest ...]
   Result: 67 tests passing

2. Now I'll audit for bad practices
   [Runs: grep patterns for except:pass, etc.]
   Found: 3 instances of except:pass

3. Let me examine each one:

   Issue 1: MouseMasterLib/preset_manager.py:142
   - Context: Loading preset from disk
   - Current: except: pass
   - Intent: Silently skip invalid presets
   - Fix: Add logging, raise on error (fail fast)

   [Applies fix using Edit tool]

4. Running tests to verify...
   [Runs: uv run pytest ...]
   Result: 67 tests passing ✓

5. Moving to next issue...
   [Repeats for each issue]

6. Final verification:
   [Runs full audit again]
   Result: 0 except:pass instances remaining

7. Summary:
   - Fixed 3 exception swallowing issues
   - All 67 tests still passing
   - Code now follows fail-fast principles
```

---

## Integration with Other Skills

This skill works with:

- `/audit-code-quality` - Detailed audit patterns
- `/fix-bad-practices` - Specific fix patterns
- `/test-bindings` - Testing in Slicer context

Workflow:
```
/autonomous-code-review  # Full automated review
# or for specific steps:
/audit-code-quality      # Just audit
/fix-bad-practices       # Just fix (after manual audit)
```
