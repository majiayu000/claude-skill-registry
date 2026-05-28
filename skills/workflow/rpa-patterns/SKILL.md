---
name: rpa-patterns
description: Common RPA automation patterns (retry, polling, circuit breaker) for resilient automation. Use when: implementing RPA workflows, error handling, resilient automation, retry with backoff, polling for conditions, circuit breaker patterns.
---

# RPA Patterns Skill

Resilience and retry patterns for reliable RPA automation.

## Overview

RPA automation must handle unreliable external systems: network timeouts, dynamic UI loading, rate limits, and transient failures. This skill provides proven patterns for building robust automations.

## Quick Reference

| Pattern | Use Case | Example |
|---------|----------|---------|
| **Retry with Backoff** | Transient failures, network issues | `examples/retry-pattern.py` |
| **Polling** | Wait for UI element or condition | `examples/polling-pattern.py` |
| **Circuit Breaker** | Prevent cascade failures, rate limits | `examples/circuit-breaker-pattern.py` |
| **Continue on Error** | Non-critical operations, data collection | Inline below |
| **Recovery Strategy** | Graceful degradation, fallback actions | Inline below |

## Built-in BrowserBaseNode Support

Browser nodes already have retry support via `execute_with_retry()`:

```python
from casare_rpa.nodes.browser.browser_base import BrowserBaseNode

class MyClickNode(BrowserBaseNode):
    async def execute(self, context):
        page = await self.get_page(context)

        # Built-in retry (uses retry_count, retry_interval from config)
        result, attempts = await self.execute_with_retry(
            lambda: page.click("#submit-btn"),
            operation_name="click submit"
        )
```

Config properties (auto-generated in visual nodes):
- `retry_count`: int = 0 (number of retries after initial failure)
- `retry_interval`: int = 1000 (ms between retries)

## Pattern 1: Exponential Backoff Retry

For operations without built-in retry support.

```python
import asyncio
from loguru import logger

async def retry_with_backoff(
    operation: Callable[[], Awaitable[T]],
    max_attempts: int = 3,
    base_delay_ms: int = 1000,
    max_delay_ms: int = 10000,
) -> T:
    """Retry with exponential backoff: 1s, 2s, 4s, 8s..."""
    for attempt in range(1, max_attempts + 1):
        try:
            return await operation()
        except Exception as e:
            if attempt == max_attempts:
                raise

            delay = min(base_delay_ms * (2 ** (attempt - 1)), max_delay_ms)
            logger.warning(f"Attempt {attempt}/{max_attempts} failed: {e}. Retrying in {delay}ms")
            await asyncio.sleep(delay / 1000)
```

## Pattern 2: Polling for Condition

Wait for dynamic UI elements or async operations.

```python
async def poll_for_condition(
    condition: Callable[[], Awaitable[bool]],
    timeout_ms: int = 30000,
    interval_ms: int = 500,
) -> bool:
    """Poll until condition is true or timeout."""
    deadline = asyncio.get_event_loop().time() + (timeout_ms / 1000)

    while asyncio.get_event_loop().time() < deadline:
        if await condition():
            return True
        await asyncio.sleep(interval_ms / 1000)

    raise TimeoutError(f"Condition not met within {timeout_ms}ms")
```

**Usage with Playwright:**

```python
# Instead of hardcoded sleep
await asyncio.sleep(5)  # BAD

# Use polling
async def is_loaded(page):
    return await page.locator(".data-loaded").count() > 0

await poll_for_condition(lambda: is_loaded(page))  # GOOD
```

## Pattern 3: Circuit Breaker

Prevent hammering failing services and enable auto-recovery.

```python
from dataclasses import dataclass
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing recovery

@dataclass
class CircuitBreaker:
    failure_threshold: int = 5
    timeout_ms: int = 60000
    half_open_attempts: int = 1

    def __post_init__(self):
        self._state = CircuitState.CLOSED
        self._failures = 0
        self._last_failure_time = 0

    async def call(self, operation: Callable[[], Awaitable[T]]) -> T:
        """Execute operation with circuit breaker protection."""
        if self._state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self._state = CircuitState.HALF_OPEN
            else:
                raise CircuitBreakerOpenError("Circuit is OPEN")

        try:
            result = await operation()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
```

## Pattern 4: Continue on Error

For non-critical operations where failure should not stop workflow.

```python
@properties(
    PropertyDef("on_error", PropertyType.CHOICE, default="fail",
                options=["fail", "continue", "retry"]),
)
@node(category="data")
class DataCollectNode(BaseNode):
    async def execute(self, context):
        on_error = self.get_parameter("on_error")
        results = []

        for item in items:
            try:
                result = await self.process_item(item)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to process {item}: {e}")

                if on_error == "fail":
                    raise
                elif on_error == "continue":
                    results.append({"error": str(e)})
                elif on_error == "retry":
                    # Retry logic here
                    pass

        self.set_output_value("results", results)
```

## Pattern 5: Recovery Strategy

Fallback actions when primary operation fails.

```python
async def execute_with_fallback(
    primary: Callable[[], Awaitable[T]],
    fallback: Callable[[], Awaitable[T]],
    fallback_reason: str = "primary failed",
) -> T:
    """Try primary, use fallback on failure."""
    try:
        return await primary()
    except Exception as e:
        logger.warning(f"Primary operation failed: {e}. Using fallback: {fallback_reason}")
        return await fallback()
```

## RPA-Specific Error Handling

### Screenshot on Failure

Already built into BrowserBaseNode:

```python
# In node config, enable:
# screenshot_on_fail: True
# screenshot_on_fail: "./screenshots"

# Or manually:
await self.screenshot_on_failure(page, prefix="click_failed")
```

### Element Not Found Recovery

```python
async def click_with_recovery(page, selector):
    """Click with multiple selector strategies."""
    try:
        await page.click(selector)
    except Error:
        # Try alternative selectors
        for alt in get_alternative_selectors(selector):
            try:
                await page.click(alt)
                return
            except Error:
                continue
        raise
```

### Dynamic Wait Strategies

```python
async def smart_wait(page, selector, timeout_ms=30000):
    """Wait with progressive timeouts."""
    # Fast check first
    try:
        if await page.locator(selector).count() > 0:
            return
    except Error:
        pass

    # Then full wait
    await page.wait_for_selector(selector, timeout=timeout_ms)
```

## Examples

See `examples/` folder for complete implementations:

| File | Description |
|------|-------------|
| `retry-pattern.py` | Exponential backoff with jitter |
| `polling-pattern.py` | Condition polling with timeout |
| `circuit-breaker-pattern.py` | Full circuit breaker with metrics |

## Cross-References

| Topic | Location |
|-------|----------|
| BrowserBaseNode retry | `src/casare_rpa/nodes/browser/browser_base.py` |
| Node error handling | `.brain/rules/error-handling.md` |
| Control flow nodes | `src/casare_rpa/nodes/control_flow/` |

---

*Parent: [../_index.md](../_index.md)*
*Last updated: 2025-12-26*
