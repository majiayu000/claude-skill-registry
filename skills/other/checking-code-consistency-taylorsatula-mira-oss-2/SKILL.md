---
name: Code Consistency - Logging & Standards
description: Check Python logging levels and patterns for correctness. Focus on identifying wrong severity levels and missing exception handling. Use when reviewing code quality.
allowed-tools: Read, Glob, Grep
---

# Code Consistency Checker

Scan Python files for logging issues. Flag incorrect severity levels and missing exception context.

---

## Logging Level Decision Tree

**Ask: What happened in this code?**

```
Variable value, loop iteration, function entry/exit, detailed diagnostics?
  → DEBUG

Successful operation, workflow step completed, state change confirmed?
  → INFO

Unexpected but handled: fallback used, retry attempt, deprecated call, approaching limit?
  → WARNING

Functionality failed: operation error, caught exception, feature broken?
  → ERROR (use logger.exception() in except blocks)

System-wide failure: cannot serve requests, out of resources, imminent crash?
  → CRITICAL
```

---

## Common Logging Mistakes

### Wrong Severity Level

```python
# ❌ WRONG: Exception logged as INFO
try:
    result = risky_operation()
except Exception as e:
    logger.info(f"Operation failed: {e}")  # Should be ERROR

# ✅ CORRECT: Use logger.exception() in except blocks
try:
    result = risky_operation()
except Exception as e:
    logger.exception("Operation failed")  # Automatically ERROR + stack trace
```

```python
# ❌ WRONG: Normal operation logged as ERROR
user = get_user(user_id)
logger.error(f"Retrieved user {user_id}")  # Should be INFO or DEBUG

# ✅ CORRECT: Normal operations are INFO
user = get_user(user_id)
logger.info(f"Retrieved user {user_id}")
```

```python
# ❌ WRONG: Fallback behavior logged as ERROR
cache_value = cache.get(key)
if cache_value is None:
    logger.error("Cache miss, using database")  # Should be WARNING or INFO
    value = db.query(key)

# ✅ CORRECT: Degraded mode is WARNING
cache_value = cache.get(key)
if cache_value is None:
    logger.warning("Cache miss, falling back to database")
    value = db.query(key)
```

```python
# ❌ WRONG: Routine error logged as CRITICAL
if not user_id:
    logger.critical("Missing user_id parameter")  # Should be ERROR
    raise ValueError("user_id required")

# ✅ CORRECT: CRITICAL only for system-wide failures
if connection_pool_exhausted():
    logger.critical("Database connection pool exhausted, cannot serve requests")
    shutdown()
```

### Missing Exception Context

```python
# ❌ WRONG: Missing stack trace
try:
    process_data()
except Exception as e:
    logger.error(f"Failed: {e}")  # No stack trace

# ✅ CORRECT: Use logger.exception() or exc_info=True
try:
    process_data()
except Exception as e:
    logger.exception("Data processing failed")  # Includes stack trace

# ✅ ALSO CORRECT: Explicit exc_info
try:
    process_data()
except Exception as e:
    logger.error("Data processing failed", exc_info=True)
```

### Logger Pattern Violations

```python
# ❌ WRONG: Using root logger
logger = logging.getLogger()
logger.info("message")

# ✅ CORRECT: Named logger
logger = logging.getLogger(__name__)
logger.info("message")
```

```python
# ❌ WRONG: Using print() for logging
print(f"Processing user {user_id}")

# ✅ CORRECT: Use logger
logger.info(f"Processing user {user_id}")
```

### Security Issues

```python
# ❌ WRONG: Logging sensitive data
logger.info(f"User authenticated: {username} / {password}")
logger.debug(f"API request: {api_key}")

# ✅ CORRECT: Redact sensitive information
logger.info(f"User authenticated: {username}")
logger.debug("API request authenticated")
```

---

## Severity Level Guidelines

### DEBUG (Development only, filter out in production)
- Variable values during execution
- Function entry/exit traces
- Loop iteration details
- Cache hits/misses (when debugging)
- Query performance timing
- Internal state inspection

**Production**: Set level to INFO or higher

### INFO (Normal operations)
- User logged in/out
- Batch processing started/completed
- Configuration loaded
- Service started/stopped
- Scheduled job executed
- Workflow step completed
- Major operation succeeded

**If it's expected and good, it's INFO**

### WARNING (Unexpected but handled)
- API rate limit approaching (80% capacity)
- Deprecated function called
- Retry attempt (N of M)
- Using fallback/default value
- Resource usage high but manageable
- Temporary degradation

**If it's weird but working, it's WARNING**

### ERROR (Functionality failed)
- Database query failed
- API call failed
- File not found
- Validation error
- Tool execution failed
- User operation failed
- Any caught exception affecting functionality

**Use `logger.exception()` in except blocks**

### CRITICAL (System failure)
- Database unreachable
- Out of memory
- Connection pool exhausted
- Authentication system down
- Cannot serve requests
- Imminent shutdown

**Should trigger immediate alerts/paging**

---

## Check Execution

1. **Find all logger calls**: `logger.debug/info/warning/error/critical/exception()`

2. **For each call, ask**:
   - What situation triggered this log?
   - Does severity match the decision tree?
   - Is this in an except block? (should use `logger.exception()`)

3. **Check patterns**:
   - Named logger used? (`getLogger(__name__)`)
   - No `print()` statements for operational logging?
   - No sensitive data logged?

4. **Flag issues with**:
   - Line number
   - Current severity vs. correct severity
   - Reason for change

---

## Output Format

```
FILE: path/to/file.py

LOGGING ISSUES:

Line 23: Severity too high
  Current: logger.error("Retrieved user data")
  Should be: logger.info("Retrieved user data")
  Reason: Normal successful operation should be INFO, not ERROR

Line 78: Missing exception context
  Current: logger.error(f"Failed: {e}")
  Should be: logger.exception("Operation failed")
  Reason: Use logger.exception() in except blocks for automatic stack trace

Line 134: Severity too low
  Current: logger.info("API call failed, retrying")
  Should be: logger.warning("API call failed, retrying")
  Reason: Retry indicates unexpected issue, should be WARNING

Line 201: Security violation
  Current: logger.debug(f"Authenticating with token: {api_token}")
  Should be: logger.debug("Authenticating with API")
  Reason: Never log credentials, tokens, or passwords

Line 234: Wrong logger pattern
  Current: logger = logging.getLogger()
  Should be: logger = logging.getLogger(__name__)
  Reason: Use named logger, not root logger

Line 289: Should use logger instead of print
  Current: print(f"Processing {count} items")
  Should be: logger.info(f"Processing {count} items")
  Reason: Use logging module for operational messages

SUMMARY: 6 logging issues found
```

---

## Quick Reference Card

| Situation | Level | Example |
|-----------|-------|---------|
| Loop iteration details | DEBUG | `logger.debug(f"Processing item {i} of {total}")` |
| Successful operation | INFO | `logger.info("Memory consolidation completed")` |
| Fallback/retry | WARNING | `logger.warning("Cache miss, using database")` |
| Operation failed | ERROR | `logger.exception("Failed to process data")` |
| System cannot function | CRITICAL | `logger.critical("Database unreachable")` |

**In except blocks**: Always use `logger.exception()` or `logger.error(..., exc_info=True)`

**Named logger**: Always `logger = logging.getLogger(__name__)`

**Security**: Never log passwords, tokens, API keys, or PII
