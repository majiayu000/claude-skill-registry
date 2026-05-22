---
name: implement-retry-logic
description: |
  Add retry logic with exponential backoff to async operations. Use when implementing
  external service calls, database operations, network requests, or any operation that
  may fail transiently. Follows project patterns for ServiceResult wrapping, configuration
  injection, and resilience patterns. Works with async/await operations in Python.
allowed-tools:
  - Read
  - Grep
  - Edit
  - MultiEdit
---

# Implement Retry Logic

## Purpose

Add retry logic with exponential backoff and jitter to async operations, following project patterns for resilience, configuration injection, and ServiceResult wrapping.

## When to Use

Use this skill when:
- **Implementing external service calls** - API calls that may timeout or fail
- **Database operations** - Database connections that may drop
- **Network requests** - Any network operation subject to transient failures
- **Operations that may fail transiently** - Temporary errors that can be retried

**Trigger phrases:**
- "Add retry logic for X"
- "Implement exponential backoff for Y"
- "Make Z resilient to failures"
- "Handle transient errors in X"

## Table of Contents

### Core Sections

- [Purpose](#purpose)
  - Core capability of the skill
- [Quick Start](#quick-start)
  - Pattern detection and basic implementation
- [Instructions](#instructions)
  - [Step 1: Identify Retry Requirements](#step-1-identify-retry-requirements) - When to use retry logic
  - [Step 2: Add Configuration](#step-2-add-configuration) - Configuration injection patterns
  - [Step 3: Implement Retry Logic](#step-3-implement-retry-logic) - Core retry implementation
  - [Step 4: Add Backoff Helper](#step-4-add-backoff-helper) - Exponential backoff with jitter
  - [Step 5: Classify Errors](#step-5-classify-errors) - Retriable vs permanent errors
  - [Step 6: Add Tests](#step-6-add-tests) - Test coverage for retry behavior

### Examples & Reference

- [Examples](#examples)
  - [Example 1: Database Operation Retry](#example-1-database-operation-retry) - Neo4j database operations with retry
  - [Example 2: External API Retry](#example-2-external-api-retry) - HTTP API calls with rate limiting
- [Requirements](#requirements)
  - Dependencies and project patterns
- [See Also](#see-also)
  - Supporting resources and reference implementations

### Supporting Resources

- [references/reference.md](./references/reference.md) - Advanced patterns and troubleshooting
- [templates/retry-template.py](./templates/retry-template.py) - Copy-paste template

### Utility Scripts
- [Add Retry Logic](./scripts/add_retry_logic.py) - Auto-add retry logic to async service methods
- [Analyze Retryable Operations](./scripts/analyze_retryable_operations.py) - Analyze codebase to find operations that need retry logic
- [Validate Retry Patterns](./scripts/validate_retry_patterns.py) - Validate retry logic implementations against best practices

## Quick Start

**Pattern Detection**: Look for external API calls, database operations, or network requests without retry logic.

**Basic Implementation**: Add retry loop with exponential backoff + jitter:

```python
# Configuration in settings
max_retries: int = 3
retry_delay: float = 1.0

# Implementation
for attempt in range(max_retries):
    try:
        result = await external_operation()
        return ServiceResult.ok(result)
    except RetriableError as e:
        if attempt < max_retries - 1:
            delay = min(retry_delay * (2 ** attempt), 30.0)
            jitter = delay * 0.2 * (2 * (time.time() % 1) - 1)
            await asyncio.sleep(max(0.1, delay + jitter))
        else:
            return ServiceResult.fail(f"Failed after {max_retries} retries: {e}")
```

## Instructions

### Step 1: Identify Retry Requirements

**Check if retry is needed:**
- [ ] External service call (API, database, network)
- [ ] Operation may fail transiently (timeouts, rate limits)
- [ ] Operation is idempotent (safe to retry)
- [ ] Failures should not crash the system

**Anti-patterns to avoid:**
- ❌ Retrying non-idempotent operations (creates duplicates)
- ❌ Retrying permanent errors (syntax errors, bad input)
- ❌ No backoff delay (hammers failing service)
- ❌ Infinite retries (never gives up)

### Step 2: Add Configuration

**Add retry settings to config/settings.py:**

```python
@dataclass
class ServiceSettings:
    """Configuration for [service name]."""

    # Existing fields...

    # Retry configuration
    max_retries: int = 3  # Maximum retry attempts
    retry_delay: float = 1.0  # Base delay in seconds

    @classmethod
    def from_env(cls) -> "ServiceSettings":
        return cls(
            # Existing fields...
            max_retries=int(os.getenv("SERVICE_MAX_RETRIES", "3")),
            retry_delay=float(os.getenv("SERVICE_RETRY_DELAY", "1.0")),
        )
```

**Configuration Rules:**
1. Always inject via Settings (never hardcode)
2. Provide environment variable overrides
3. Use sensible defaults (max_retries=3, retry_delay=1.0)
4. Document units (seconds, milliseconds)

### Step 3: Implement Retry Logic

**Use project pattern with exponential backoff + jitter:**

```python
async def _call_with_retry(self, operation_name: str) -> ServiceResult[T]:
    """Call external service with retry logic.

    Args:
        operation_name: Name for logging

    Returns:
        ServiceResult with operation result or error
    """
    last_error: str = ""

    for attempt in range(self.settings.max_retries):
        try:
            # Perform operation
            result = await self._perform_operation()
            return ServiceResult.ok(result)

        except aiohttp.ClientConnectionError as e:
            # Connection errors are retriable
            last_error = f"Connection error: {e}"
            if attempt < self.settings.max_retries - 1:
                delay = self._calculate_backoff_delay(attempt)
                logger.warning(
                    f"{last_error}. Retrying in {delay:.1f}s "
                    f"(attempt {attempt + 1}/{self.settings.max_retries})"
                )
                await asyncio.sleep(delay)

        except TimeoutError as e:
            # Timeouts are retriable
            last_error = f"Request timed out: {e}"
            if attempt < self.settings.max_retries - 1:
                delay = self._calculate_backoff_delay(attempt)
                logger.warning(
                    f"{last_error}. Retrying in {delay:.1f}s "
                    f"(attempt {attempt + 1}/{self.settings.max_retries})"
                )
                await asyncio.sleep(delay)

        except ValueError as e:
            # Validation errors are NOT retriable (permanent)
            logger.error(f"Validation error (non-retriable): {e}")
            return ServiceResult.fail(f"Validation error: {e}")

        except Exception as e:
            # Unexpected errors - fail fast
            logger.error(f"Unexpected error in {operation_name}: {e}")
            return ServiceResult.fail(f"Unexpected error: {e}")

    # All retries exhausted
    return ServiceResult.fail(
        f"Failed after {self.settings.max_retries} retries: {last_error}"
    )
```

**Key Components:**
1. **Retry Loop**: `for attempt in range(max_retries)`
2. **Error Classification**: Retriable vs permanent errors
3. **Backoff Calculation**: Exponential with jitter
4. **Logging**: Warning on retry, error on failure
5. **ServiceResult**: Always return ServiceResult, never raise

### Step 4: Add Backoff Helper

**Helper method for exponential backoff with jitter:**

```python
def _calculate_backoff_delay(self, attempt: int) -> float:
    """Calculate exponential backoff with jitter.

    Args:
        attempt: Current attempt number (0-based)

    Returns:
        Delay in seconds with jitter
    """
    base_delay = self.settings.retry_delay

    # Exponential backoff: base * 2^attempt, capped at 30s
    delay = min(base_delay * (2 ** attempt), 30.0)

    # Add jitter to avoid thundering herd (±20%)
    jitter = delay * 0.2 * (2 * (time.time() % 1) - 1)

    return max(0.1, delay + jitter)
```

**Jitter prevents thundering herd:**
- Multiple clients don't retry at exact same time
- Uses time.time() fractional seconds for randomness
- ±20% variance is industry standard

### Step 5: Classify Errors

**Determine which exceptions are retriable:**

```python
def _is_retriable_error(self, error: Exception, status_code: int | None = None) -> bool:
    """Determine if error is retriable.

    Args:
        error: Exception that occurred
        status_code: HTTP status code if applicable

    Returns:
        True if error should be retried
    """
    # HTTP status codes
    if status_code:
        # 429 Rate Limited - retriable
        if status_code == 429:
            return True
        # 5xx Server errors - retriable
        if 500 <= status_code < 600:
            return True
        # 4xx Client errors (except 429) - NOT retriable
        if 400 <= status_code < 500:
            return False

    # Network/connection errors - retriable
    if isinstance(error, (
        aiohttp.ClientConnectionError,
        aiohttp.ServerDisconnectedError,
        TimeoutError,
    )):
        return True

    # Validation/syntax errors - NOT retriable
    if isinstance(error, (ValueError, TypeError, SyntaxError)):
        return False

    # Default: not retriable (fail fast)
    return False
```

**Error Classification Rules:**
- **Retriable**: Timeouts, rate limits, 5xx errors, network errors
- **Permanent**: Validation errors, 4xx errors (except 429), syntax errors
- **Default**: When uncertain, fail fast (not retriable)

### Step 6: Add Tests

**Test retry behavior:**

```python
async def test_retry_on_transient_error():
    """Test that transient errors trigger retry."""
    service = MyService(settings)

    # Mock to fail twice, then succeed
    with patch.object(service, "_perform_operation") as mock_op:
        mock_op.side_effect = [
            TimeoutError("timeout"),
            TimeoutError("timeout"),
            {"status": "success"}
        ]

        result = await service._call_with_retry("test")

        assert result.is_success
        assert mock_op.call_count == 3  # 2 failures + 1 success

async def test_no_retry_on_permanent_error():
    """Test that permanent errors do not retry."""
    service = MyService(settings)

    with patch.object(service, "_perform_operation") as mock_op:
        mock_op.side_effect = ValueError("bad input")

        result = await service._call_with_retry("test")

        assert result.is_failure
        assert mock_op.call_count == 1  # No retry
```

**Test Coverage:**
- Retry on transient errors
- No retry on permanent errors
- Exponential backoff delays
- Max retries exhausted
- Jitter variance

## Examples

### Example 1: Database Operation Retry

```python
async def create_database(self, database_name: str) -> ServiceResult[str]:
    """Create database with retry on transient errors."""
    last_error: str = ""

    for attempt in range(self.settings.max_retries):
        try:
            # Attempt database creation
            await self.execute_query(
                f"CREATE DATABASE `{database_name}` IF NOT EXISTS",
                database="system",
            )
            return ServiceResult.ok(database_name, was_created=True)

        except Neo4jConnectionError as e:
            # Connection errors are retriable
            last_error = f"Connection error: {e}"
            if attempt < self.settings.max_retries - 1:
                delay = self._calculate_backoff_delay(attempt)
                logger.warning(f"Retrying in {delay:.1f}s (attempt {attempt + 1})")
                await asyncio.sleep(delay)

        except Neo4jPermissionError as e:
            # Permission errors are NOT retriable
            return ServiceResult.fail(
                f"Permission denied: {e}",
                error_type="PermissionError",
                recoverable=False
            )

    return ServiceResult.fail(f"Failed after {self.settings.max_retries} retries: {last_error}")
```

### Example 2: External API Retry

```python
async def _call_embedding_api(self, texts: list[str]) -> ServiceResult[list[list[float]]]:
    """Call embedding API with retry and rate limit handling."""
    last_error: str = ""

    for attempt in range(self.settings.max_retries):
        try:
            session = await self._get_session()
            payload = {"model": self.model, "input": texts}

            async with session.post(self.api_url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    embeddings = [item["embedding"] for item in data["data"]]
                    return ServiceResult.ok(embeddings)

                elif response.status == 429:
                    # Rate limited - retriable
                    last_error = "Rate limited by API"
                    if attempt < self.settings.max_retries - 1:
                        # Use Retry-After header if available
                        retry_after = response.headers.get("Retry-After", "2")
                        delay = min(float(retry_after), 30.0)
                        logger.warning(f"Rate limited. Retrying in {delay}s")
                        await asyncio.sleep(delay)

                elif 500 <= response.status < 600:
                    # Server error - retriable
                    last_error = f"Server error {response.status}"
                    if attempt < self.settings.max_retries - 1:
                        delay = self._calculate_backoff_delay(attempt)
                        await asyncio.sleep(delay)

                else:
                    # Client error - NOT retriable
                    error_text = await response.text()
                    return ServiceResult.fail(f"API error {response.status}: {error_text}")

        except aiohttp.ClientConnectionError as e:
            last_error = f"Connection error: {e}"
            if attempt < self.settings.max_retries - 1:
                delay = self._calculate_backoff_delay(attempt)
                await asyncio.sleep(delay)

    return ServiceResult.fail(f"Failed after {self.settings.max_retries} retries: {last_error}")
```

## Requirements

**Dependencies:**
- `asyncio` - Async/await and sleep
- `time` - Jitter calculation
- `aiohttp` - HTTP client (for network operations)

**Project Patterns:**
- ServiceResult for return values
- Settings injection for configuration
- OTEL logging (not print statements)
- Fail-fast principle

**Configuration:**
- Add retry settings to config/settings.py
- Provide environment variable overrides
- Never hardcode retry parameters

## See Also

- [references/reference.md](./references/reference.md) - Advanced patterns and troubleshooting
- [templates/retry-template.py](./templates/retry-template.py) - Copy-paste template
- [scripts/add_retry_logic.py](./scripts/add_retry_logic.py) - Auto-add retry logic utility
- [scripts/analyze_retryable_operations.py](./scripts/analyze_retryable_operations.py) - Codebase analysis utility
- [scripts/validate_retry_patterns.py](./scripts/validate_retry_patterns.py) - Validation utility
- [ARCHITECTURE.md](/Users/dawiddutoit/projects/play/project-watch-mcp/ARCHITECTURE.md) - ServiceResult pattern
- [src/project_watch_mcp/infrastructure/embeddings/infinity/embedding_service.py](/Users/dawiddutoit/projects/play/project-watch-mcp/src/project_watch_mcp/infrastructure/embeddings/infinity/embedding_service.py) - Reference implementation
