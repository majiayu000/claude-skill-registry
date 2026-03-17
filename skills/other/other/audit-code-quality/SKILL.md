---
name: audit-code-quality
description: Scan codebase for bad coding practices that violate fail-fast principles
allowed-tools:
  - Bash
  - Grep
  - Read
context: auto
---

# Audit Code Quality Skill

Systematically scan codebase for bad coding practices that violate fail-fast principles.

## When to Use

Use this skill:
- Before committing changes
- During code review
- Periodically to maintain code quality
- When onboarding to understand code health
- Autonomously as part of CI/quality workflow

## Philosophy: Fail Fast

This codebase follows **fail-fast, test-driven development** with detailed logging:

1. **Errors should surface immediately** - Never hide or swallow errors
2. **Exceptions are for exceptional cases** - Not for flow control
3. **All exceptions must be logged** - For human and LLM debugging
4. **Tests catch bugs early** - Not error suppression in production
5. **Humans and LLMs collaborate** - Clear logs enable autonomous fixing

---

## Bad Practices to Detect

### Category 1: Exception Swallowing (CRITICAL)

**Pattern: Bare except with pass**
```python
# BAD - Swallows ALL errors silently
try:
    do_something()
except:
    pass

# BAD - Catches everything, logs, but continues as if nothing happened
try:
    do_something()
except Exception as e:
    logger.error(e)
    pass
```

**Detection**:
```bash
# Find bare except:pass
grep -rn "except.*:$" --include="*.py" -A1 | grep -B1 "pass$"

# Find except Exception with pass
grep -rn "except.*Exception" --include="*.py" -A2 | grep -B2 "pass$"

# Find except with only logging then pass/continue
grep -rn "except" --include="*.py" -A3 | grep -E "(log|print).*\n.*pass"
```

---

### Category 2: Silent Continuation (CRITICAL)

**Pattern: Check-and-continue without action**
```python
# BAD - Silently skips errors
for item in items:
    if not item.is_valid():
        continue  # Error hidden!
    process(item)

# BAD - Returns None on error without indication
def get_data():
    if error_condition:
        return None  # Caller can't distinguish from valid None
    return data
```

**Detection**:
```bash
# Find if-continue patterns (manual review needed)
grep -rn "if.*:$" --include="*.py" -A1 | grep -B1 "continue$"

# Find return None after error checks
grep -rn "return None" --include="*.py" -B2 | grep -E "(error|fail|invalid|bad)"
```

---

### Category 3: Overly Broad Exception Handling (HIGH)

**Pattern: Catching Exception or BaseException**
```python
# BAD - Too broad, catches SystemExit, KeyboardInterrupt
try:
    do_something()
except Exception:
    handle_error()

# BAD - Catches literally everything
try:
    do_something()
except BaseException:
    handle_error()
```

**Detection**:
```bash
# Find broad exception catches
grep -rn "except Exception" --include="*.py"
grep -rn "except BaseException" --include="*.py"
grep -rn "except:$" --include="*.py"
```

---

### Category 4: Missing Exception Logging (HIGH)

**Pattern: Catch without logging**
```python
# BAD - Handles error but doesn't log
try:
    do_something()
except SpecificError:
    return default_value  # No log!

# BAD - Re-raises without logging
try:
    do_something()
except SpecificError:
    raise  # No context added
```

**Detection**:
```bash
# Find except blocks without logging (heuristic)
grep -rn "except.*:" --include="*.py" -A5 | grep -v -E "(log|print|raise)"
```

---

### Category 5: Error Return Values (MEDIUM)

**Pattern: Returning error codes instead of raising**
```python
# BAD - C-style error handling
def process():
    if error:
        return -1  # Magic number
    return result

# BAD - Boolean success flag
def process():
    if error:
        return False, None
    return True, result
```

**Detection**:
```bash
# Find return -1 or return False patterns
grep -rn "return -1\|return False" --include="*.py" -B3
```

---

### Category 6: Defensive None Checks Hiding Bugs (MEDIUM)

**Pattern: Excessive None guards**
```python
# BAD - Hides the real bug (why is it None?)
def process(data):
    if data is None:
        return  # Silently does nothing
    # ... process

# BAD - None propagation
result = obj.method() if obj else None  # Hides missing object bug
```

**Detection**:
```bash
# Find if None return patterns
grep -rn "if.*None.*:$" --include="*.py" -A1 | grep -B1 "return$"
grep -rn "if.*is None" --include="*.py" -A1 | grep -B1 "return$"
```

---

### Category 7: Ignored Function Returns (MEDIUM)

**Pattern: Not checking return values**
```python
# BAD - Ignores potential failure
subprocess.run(["cmd"])  # Might fail silently

# BAD - Ignores result that might indicate error
file.write(data)  # Might not write all data
```

**Detection**:
```bash
# Find subprocess calls without check=True or capture
grep -rn "subprocess\." --include="*.py" | grep -v "check=True\|capture"
```

---

### Category 8: Catch-Log-Reraise Anti-pattern (LOW)

**Pattern: Logging then re-raising without adding value**
```python
# BAD - Adds noise without value
try:
    do_something()
except SpecificError as e:
    logger.error(f"Error: {e}")
    raise  # Just re-raises, logging was pointless
```

**Detection**:
```bash
# Find except blocks that log then raise (manual review)
grep -rn "except.*:" --include="*.py" -A3 | grep -E "log.*\n.*raise$"
```

---

## Automated Audit Script

Run this to generate a full audit report:

```bash
#!/bin/bash
# audit-code-quality.sh

echo "=== Code Quality Audit ==="
echo "Date: $(date)"
echo ""

SRC_DIR="${1:-.}"

echo "## CRITICAL: Exception Swallowing"
echo ""

echo "### Bare except:pass"
grep -rn "except.*:$" "$SRC_DIR" --include="*.py" -A1 2>/dev/null | grep -B1 "^\s*pass$" || echo "None found"
echo ""

echo "### except Exception...pass"
grep -rn "except.*Exception" "$SRC_DIR" --include="*.py" -A3 2>/dev/null | grep -B3 "^\s*pass$" || echo "None found"
echo ""

echo "## HIGH: Overly Broad Exceptions"
echo ""

echo "### except Exception (should be specific)"
grep -rn "except Exception\b" "$SRC_DIR" --include="*.py" 2>/dev/null || echo "None found"
echo ""

echo "### except: (bare except)"
grep -rn "except:$" "$SRC_DIR" --include="*.py" 2>/dev/null || echo "None found"
echo ""

echo "## MEDIUM: Silent Continuation"
echo ""

echo "### if...continue patterns (review manually)"
grep -rn "if.*:" "$SRC_DIR" --include="*.py" -A1 2>/dev/null | grep -B1 "continue$" | head -30 || echo "None found"
echo ""

echo "### return None after error conditions"
grep -rn "return None" "$SRC_DIR" --include="*.py" -B2 2>/dev/null | grep -E "(error|fail|invalid|bad|cannot|unable)" | head -20 || echo "None found"
echo ""

echo "## Summary"
CRITICAL=$(grep -rn "except.*:$" "$SRC_DIR" --include="*.py" -A1 2>/dev/null | grep -c "pass$" || echo 0)
BROAD=$(grep -rn "except Exception\b\|except:$" "$SRC_DIR" --include="*.py" 2>/dev/null | wc -l || echo 0)
echo "Critical issues (except...pass): $CRITICAL"
echo "Broad exceptions: $BROAD"
```

---

## Per-File Audit Checklist

For each Python file, verify:

- [ ] No `except: pass` or `except Exception: pass`
- [ ] No `except:` without specific exception type
- [ ] All `except` blocks either:
  - Log the error AND re-raise, OR
  - Log the error AND return a meaningful error indicator, OR
  - Handle a specific recoverable case with clear documentation
- [ ] No silent `if error: continue` patterns
- [ ] No `return None` that hides errors
- [ ] All subprocess calls use `check=True` or explicit error handling
- [ ] Functions that can fail raise exceptions (not return codes)

---

## Output Format

Generate audit results as:

```markdown
## Code Quality Audit Report

**Date**: YYYY-MM-DD
**Scope**: [files/directories audited]

### Critical Issues (Must Fix)
| File | Line | Issue | Pattern |
|------|------|-------|---------|
| path/file.py | 42 | Exception swallowing | `except: pass` |

### High Priority Issues
| File | Line | Issue | Pattern |
|------|------|-------|---------|

### Medium Priority Issues
| File | Line | Issue | Recommendation |
|------|------|-------|----------------|

### Summary
- Critical: X issues
- High: X issues
- Medium: X issues
- **Action Required**: [Yes/No]
```

---

## Integration with Tests

After audit, run tests to ensure code still works:

```bash
# Run unit tests
uv run pytest MouseMaster/Testing/Python/ -v

# Run with coverage to find untested error paths
uv run pytest --cov=MouseMaster --cov-report=term-missing
```

---

## Next Steps After Audit

1. **Critical issues**: Run `/fix-bad-practices` immediately
2. **High issues**: Schedule fixes before next release
3. **Medium issues**: Add to technical debt backlog
4. **Run tests**: Ensure fixes don't break functionality
5. **Update tests**: Add tests for error conditions found
