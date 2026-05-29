---
name: error-recovery
description: RPA error handling patterns (fallback, retry, skip, user notification) for resilient automation workflows. Use when: handling errors in RPA workflows, error recovery strategies, retry patterns, graceful degradation, error classification, logging standards.
---

# Error Recovery Skill

RPA error handling patterns for resilient automation workflows.

## Exception Types

| Domain Exception | Use Case |
|------------------|----------|
| `NodeExecutionError` | Node failed during execution |
| `NodeTimeoutError` | Node exceeded timeout |
| `NodeValidationError` | Invalid node configuration |
| `ValidationError` | Data validation failure |
| `ResourceError` | File, network, API errors |
| `AuthenticationError` | Credential failure |
| `NetworkError` | Connection/timeout errors |

## Recovery Strategies

| Strategy | When to Use |
|----------|-------------|
| **RETRY** | Transient errors (timeout, stale element, connection) |
| **SKIP** | Non-critical node, optional data |
| **FALLBACK** | Alternative value/path available |
| **COMPENSATE** | Rollback needed (database writes) |
| **ABORT** | Critical error, cannot continue |
| **ESCALATE** | Max retries exceeded, human needed |

## Error Classification

```python
from casare_rpa.domain.errors.types import ErrorClassification

# TRANSIENT: Temporary, retryable
# - TIMEOUT, CONNECTION_TIMEOUT, ELEMENT_STALE
# - NETWORK_ERROR, RESOURCE_LOCKED

# PERMANENT: Will not fix with retry
# - SELECTOR_INVALID, PERMISSION_DENIED
# - FILE_NOT_FOUND, CONFIG_INVALID

# UNKNOWN: First occurrence
# - Try once, then escalate
```

## Quick Patterns

### 1. Try-Except with Context

```python
from loguru import logger
from casare_rpa.domain.errors.exceptions import NodeExecutionError, ErrorContext

try:
    await page.click(selector)
except Exception as exc:
    logger.error(f"Click failed for {selector}: {exc}")
    raise NodeExecutionError(
        message="Element click failed",
        node_id=self.node_id,
        node_type=self.node_type,
        context=ErrorContext(
            component="ClickElementNode",
            operation="click_element",
            details={"selector": selector, "timeout_ms": 5000}
        ),
        original_error=exc
    )
```

### 2. Retry with Exponential Backoff

```python
import asyncio
from loguru import logger

max_retries = 3
base_delay = 1000  # ms

for attempt in range(max_retries):
    try:
        result = await operation()
        return result
    except TimeoutError as exc:
        if attempt < max_retries - 1:
            delay = base_delay * (2 ** attempt)
            logger.warning(f"Retry {attempt + 1}/{max_retries} after {delay}ms")
            await asyncio.sleep(delay / 1000)
        else:
            logger.error(f"Operation failed after {max_retries} retries")
            raise
```

### 3. Graceful Degradation

```python
# Primary then fallback
result = await primary_operation()
if not result:
    logger.info("Primary failed, trying fallback")
    result = await fallback_operation()

# Return empty/default
try:
    data = await fetch_optional_data()
except Exception as exc:
    logger.warning(f"Optional data unavailable: {exc}")
    data = {}
```

### 4. Error Handler Registry

```python
from casare_rpa.domain.errors.registry import get_error_handler_registry

registry = get_error_handler_registry()

# Handle error and get decision
context, decision = registry.handle_error(
    exception=exc,
    node_id=self.node_id,
    node_type=self.node_type,
    retry_count=attempt,
    max_retries=3,
)

if decision.action == RecoveryAction.RETRY:
    await asyncio.sleep(decision.retry_delay_ms / 1000)
    # retry operation
```

## Logging Standards

```python
from loguru import logger

# ERROR: Failures that stop execution
logger.error(f"Failed to write file {path}: {exc}")

# WARNING: Recovered errors
logger.warning(f"Retrying operation, attempt {attempt}/{max_retries}")

# INFO: Expected error cases
logger.info(f"Skipping optional node: {reason}")

# Always include context
logger.error(
    f"Node {self.node_type} failed",
    extra={
        "node_id": self.node_id,
        "selector": selector,
        "error_type": type(exc).__name__,
    }
)
```

## ErrorCode Reference

| Code | Value | Type |
|------|-------|------|
| `TIMEOUT` | 1001 | Transient |
| `ELEMENT_NOT_FOUND` | 2005 | Permanent |
| `ELEMENT_STALE` | 2008 | Transient |
| `SELECTOR_INVALID` | 2009 | Permanent |
| `CONNECTION_TIMEOUT` | 6002 | Transient |
| `FILE_NOT_FOUND` | 7005 | Permanent |
| `PERMISSION_DENIED` | 1006 | Permanent |

## Examples

See `examples/` folder for:
- `retry-pattern.py` - Exponential backoff
- `fallback-pattern.py` - Alternative strategies
- `skip-pattern.py` - Non-critical nodes
- `user-notification.py` - Escalation patterns
