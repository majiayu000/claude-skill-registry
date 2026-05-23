---
name: fix-bad-practices
description: Fix bad coding practices identified by audit, following fail-fast principles
allowed-tools:
  - Read
  - Edit
  - Bash
  - Grep
context: auto
---

# Fix Bad Practices Skill

Systematically fix bad coding practices identified by audit, following fail-fast principles.

## When to Use

Use this skill:
- After running `/audit-code-quality`
- When fixing specific bad patterns
- During refactoring for code quality
- Autonomously as part of quality workflow

## Philosophy: Fail Fast Fixes

When fixing bad practices:

1. **Make errors visible** - Replace silent failures with loud ones
2. **Be specific** - Catch only exceptions you can handle
3. **Always log** - Enable debugging by humans and LLMs
4. **Preserve stack traces** - Use `raise from` or `raise`
5. **Test after fixing** - Ensure fixes don't break functionality

---

## Fix Patterns

### Fix 1: Bare `except: pass` → Specific Exception + Logging

**Before (BAD)**:
```python
try:
    do_something()
except:
    pass
```

**After (GOOD)**:
```python
try:
    do_something()
except SpecificError as e:
    logger.exception("Failed to do_something: %s", e)
    raise
```

**Or if recovery is possible**:
```python
try:
    result = do_something()
except SpecificError as e:
    logger.warning("do_something failed, using fallback: %s", e)
    result = fallback_value  # Only if fallback is valid!
```

---

### Fix 2: `except Exception` → Specific Exceptions

**Before (BAD)**:
```python
try:
    data = parse_json(text)
except Exception as e:
    logger.error(e)
    return None
```

**After (GOOD)**:
```python
try:
    data = parse_json(text)
except json.JSONDecodeError as e:
    logger.exception("Invalid JSON: %s", e)
    raise ValueError(f"Cannot parse JSON: {e}") from e
except FileNotFoundError as e:
    logger.exception("File not found: %s", e)
    raise
```

---

### Fix 3: Silent `continue` → Explicit Error Handling

**Before (BAD)**:
```python
for item in items:
    if not item.is_valid():
        continue
    process(item)
```

**After (GOOD) - Option A: Fail on first error**:
```python
for item in items:
    if not item.is_valid():
        raise ValueError(f"Invalid item: {item}")
    process(item)
```

**After (GOOD) - Option B: Collect errors, report at end**:
```python
errors = []
for item in items:
    if not item.is_valid():
        errors.append(f"Invalid item: {item}")
        continue
    process(item)

if errors:
    raise ValueError(f"Processing failed with {len(errors)} invalid items:\n" +
                     "\n".join(errors))
```

**After (GOOD) - Option C: Log warning if skip is intentional**:
```python
for item in items:
    if not item.is_valid():
        logger.warning("Skipping invalid item: %s (reason: %s)", item, item.validation_error)
        continue
    process(item)
```

---

### Fix 4: `return None` on Error → Raise Exception

**Before (BAD)**:
```python
def load_config(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)
```

**After (GOOD)**:
```python
def load_config(path: Path) -> dict:
    """Load configuration from path.

    Raises:
        FileNotFoundError: If config file doesn't exist
        json.JSONDecodeError: If config is not valid JSON
    """
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path) as f:
        return json.load(f)
```

---

### Fix 5: Error Return Codes → Exceptions

**Before (BAD)**:
```python
def process_data(data):
    if not data:
        return -1, "No data provided"
    if not validate(data):
        return -2, "Invalid data"
    result = transform(data)
    return 0, result
```

**After (GOOD)**:
```python
def process_data(data):
    """Process the data.

    Raises:
        ValueError: If data is empty or invalid
    """
    if not data:
        raise ValueError("No data provided")
    if not validate(data):
        raise ValueError(f"Invalid data: {get_validation_errors(data)}")
    return transform(data)
```

---

### Fix 6: Defensive None Checks → Fail Fast

**Before (BAD)**:
```python
def process(data):
    if data is None:
        return
    # ... rest of processing
```

**After (GOOD) - If None is never valid**:
```python
def process(data):
    if data is None:
        raise ValueError("data cannot be None")
    # ... rest of processing
```

**After (GOOD) - If function should handle None gracefully**:
```python
def process(data: Optional[Data]) -> Optional[Result]:
    """Process data if provided.

    Args:
        data: Data to process, or None to skip processing

    Returns:
        Result if data was processed, None if data was None
    """
    if data is None:
        logger.debug("process() called with None, returning None")
        return None
    # ... rest of processing
```

---

### Fix 7: subprocess Without Error Checking → check=True

**Before (BAD)**:
```python
subprocess.run(["git", "commit", "-m", "message"])
```

**After (GOOD)**:
```python
try:
    subprocess.run(
        ["git", "commit", "-m", "message"],
        check=True,
        capture_output=True,
        text=True
    )
except subprocess.CalledProcessError as e:
    logger.exception("Git commit failed: %s\nstderr: %s", e, e.stderr)
    raise
```

---

### Fix 8: Catch-Log-Reraise → Add Context or Remove

**Before (BAD) - Adds noise**:
```python
try:
    do_something()
except SomeError as e:
    logger.error(f"Error: {e}")
    raise
```

**After (GOOD) - Option A: Add context**:
```python
try:
    do_something()
except SomeError as e:
    logger.exception("Failed during do_something in context X")
    raise RuntimeError(f"Operation failed in context X") from e
```

**After (GOOD) - Option B: Just let it propagate**:
```python
do_something()  # Let caller handle the exception
```

---

## Adding Proper Logging

### Logger Setup

Ensure each module has a logger:

```python
import logging

logger = logging.getLogger(__name__)
```

### Logging Levels Guide

| Level | Use For |
|-------|---------|
| `logger.debug()` | Detailed diagnostic info |
| `logger.info()` | Normal operation milestones |
| `logger.warning()` | Recoverable issues, degraded operation |
| `logger.error()` | Errors that don't stop execution |
| `logger.exception()` | Errors with stack trace (use in except blocks) |
| `logger.critical()` | Fatal errors, application cannot continue |

### Logging Best Practices

```python
# GOOD - Use exception() in except blocks (includes stack trace)
except SomeError as e:
    logger.exception("Operation failed: %s", e)

# GOOD - Use lazy formatting
logger.debug("Processing item %s of %s", i, total)

# BAD - Eager string formatting
logger.debug(f"Processing item {i} of {total}")  # Formats even if debug disabled

# GOOD - Include relevant context
logger.error("Failed to load preset '%s' from %s: %s", preset_id, path, e)

# BAD - Vague messages
logger.error("Error occurred")
```

---

## Fix Workflow

### Step 1: Run Audit

```bash
# Run audit first
/audit-code-quality

# Or run grep patterns directly
grep -rn "except.*:$" --include="*.py" -A1 | grep -B1 "pass$"
```

### Step 2: Categorize Issues

Priority order:
1. `except: pass` or `except Exception: pass` (CRITICAL)
2. Overly broad `except Exception` (HIGH)
3. Silent continuation patterns (MEDIUM)
4. Missing logging (MEDIUM)
5. Return None on error (LOW)

### Step 3: Fix Each Issue

For each issue:

1. **Understand the intent** - Why was error suppressed?
2. **Determine correct handling**:
   - Should it fail fast? → Raise exception
   - Is recovery possible? → Handle specifically with logging
   - Is it truly optional? → Document and log at DEBUG level
3. **Apply fix pattern** from above
4. **Add/update tests** for error conditions
5. **Run tests** to verify fix

### Step 4: Verify Fixes

```bash
# Run tests
uv run pytest MouseMaster/Testing/Python/ -v

# Run linting
uv run ruff check .

# Re-run audit to confirm
/audit-code-quality
```

---

## Automated Fix Script

For simple patterns, use sed (review changes before committing!):

```bash
#!/bin/bash
# CAUTION: Review all changes manually!

# Find files with except:pass (for manual review)
echo "Files needing manual review:"
grep -rl "except.*:" --include="*.py" | while read f; do
    if grep -q "pass$" "$f"; then
        echo "  $f"
    fi
done
```

**Note**: Automated fixes are risky. Always review manually and run tests.

---

## Exception Handling Decision Tree

```
Is this a programming error (bug)?
├─ Yes → Let it crash (don't catch)
└─ No → Can user/system recover?
         ├─ Yes → Catch, log, handle gracefully
         └─ No → Catch, log with context, re-raise or wrap

When catching:
├─ Can you name the specific exception?
│   ├─ Yes → Catch that specific type
│   └─ No → Research what exceptions can occur
└─ Is logging added?
    ├─ Yes → Good
    └─ No → Add logger.exception() call
```

---

## Valid Exception Handling Cases

Not all exception handling is bad. Valid cases include:

### 1. User Input Validation
```python
try:
    value = int(user_input)
except ValueError:
    logger.warning("Invalid input '%s', prompting user", user_input)
    show_error_to_user("Please enter a valid number")
```

### 2. Optional Feature Degradation
```python
try:
    import optional_dependency
    FEATURE_AVAILABLE = True
except ImportError:
    logger.info("Optional feature unavailable: optional_dependency not installed")
    FEATURE_AVAILABLE = False
```

### 3. Resource Cleanup
```python
try:
    resource = acquire_resource()
    use_resource(resource)
finally:
    resource.cleanup()  # Always runs
```

### 4. Retry Logic
```python
for attempt in range(max_retries):
    try:
        return do_operation()
    except TransientError as e:
        logger.warning("Attempt %d failed: %s", attempt + 1, e)
        if attempt == max_retries - 1:
            raise
        time.sleep(backoff)
```

### 5. Boundary/API Error Translation
```python
try:
    result = external_api.call()
except ExternalAPIError as e:
    logger.exception("External API failed")
    raise OurDomainError(f"Service unavailable: {e}") from e
```

---

## Testing Error Paths

After fixing, add tests for error conditions:

```python
def test_load_config_missing_file():
    """Test that missing config raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError, match="Config file not found"):
        load_config(Path("/nonexistent/path"))

def test_process_invalid_data():
    """Test that invalid data raises ValueError with details."""
    with pytest.raises(ValueError, match="Invalid data"):
        process_data({"bad": "data"})
```

---

## Commit Message Template

After fixes:

```
fix: replace exception swallowing with proper error handling

- Remove except:pass in module_name.py
- Add specific exception types with logging
- Add error path tests

Follows fail-fast principle: errors now surface immediately
with full context for debugging.
```
