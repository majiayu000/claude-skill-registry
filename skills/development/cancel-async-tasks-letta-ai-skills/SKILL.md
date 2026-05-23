---
name: cancel-async-tasks
description: Guidance for implementing asyncio task cancellation with proper cleanup, especially for handling keyboard interrupts (Ctrl+C). This skill should be used when tasks involve asyncio cancellation, signal handling, or graceful shutdown of concurrent Python tasks.
---

# Async Task Cancellation with Cleanup

This skill provides guidance for implementing proper cancellation handling in Python asyncio code, with particular focus on keyboard interrupt (Ctrl+C) handling and graceful cleanup.

## Core Concepts

### KeyboardInterrupt vs CancelledError

Understanding the difference is critical:

- **KeyboardInterrupt**: A `BaseException` raised in the main thread when Ctrl+C is pressed. It does NOT propagate into async coroutines directly.
- **CancelledError**: An `Exception` raised inside coroutines when `task.cancel()` is called. This IS what coroutines receive during cancellation.

**Critical Insight**: Placing `except KeyboardInterrupt` inside an async function will NOT catch Ctrl+C. The interrupt is raised at the event loop level, not within coroutines.

### Signal Handling in asyncio

To properly handle Ctrl+C in asyncio:

1. Use `loop.add_signal_handler()` to register SIGINT/SIGTERM handlers
2. Or wrap `asyncio.run()` in a try/except at the synchronous entry point
3. The signal handler should trigger task cancellation, which then raises `CancelledError` in coroutines

## Potential Approaches

### Approach 1: Signal Handler Pattern

Register signal handlers at the event loop level to trigger graceful shutdown:

```
1. Get the event loop
2. Add signal handlers for SIGINT and SIGTERM
3. In the signal handler, cancel all running tasks
4. In coroutines, catch CancelledError to perform cleanup
```

### Approach 2: Synchronous Wrapper Pattern

Wrap the async entry point to catch KeyboardInterrupt synchronously:

```
1. Define the async main logic
2. In a synchronous wrapper, call asyncio.run() inside try/except
3. Catch KeyboardInterrupt in the synchronous code
4. Handle cleanup or re-raise as needed
```

### Approach 3: TaskGroup with Exception Handling (Python 3.11+)

Use asyncio.TaskGroup for structured concurrency:

```
1. Use async with asyncio.TaskGroup() for task management
2. TaskGroup handles cancellation propagation automatically
3. Catch ExceptionGroup for handling multiple failures
```

## Verification Strategies

### Test with Actual Signals

Do NOT rely solely on timeout-based cancellation testing. Verify with actual signals:

```python
import os
import signal

# Simulate Ctrl+C in tests
os.kill(os.getpid(), signal.SIGINT)
```

### Verify Cleanup Execution

Create observable side effects to confirm cleanup runs:

- Write to a file during cleanup
- Set a flag variable
- Log cleanup actions

### Test Multiple Cancellation Scenarios

1. Normal completion (no cancellation)
2. Timeout-based cancellation (`asyncio.timeout`)
3. Manual `task.cancel()` calls
4. Actual SIGINT signal
5. SIGTERM signal

### Verify Exception Propagation

Test that exceptions from individual tasks are properly collected and reported, not silently swallowed.

## Common Pitfalls

### Pitfall 1: Catching KeyboardInterrupt in Async Functions

**Wrong**:
```python
async def my_coroutine():
    try:
        await some_operation()
    except KeyboardInterrupt:  # Will NOT catch Ctrl+C!
        await cleanup()
```

**Correct**:
```python
async def my_coroutine():
    try:
        await some_operation()
    except asyncio.CancelledError:  # This WILL be raised on cancellation
        await cleanup()
        raise  # Re-raise to propagate cancellation
```

### Pitfall 2: Not Re-raising CancelledError

Swallowing `CancelledError` prevents proper cancellation propagation. Always re-raise after cleanup unless there's a specific reason not to.

### Pitfall 3: Testing Only Happy Path Cancellation

Testing with `asyncio.timeout()` or `asyncio.wait_for()` does NOT verify keyboard interrupt handling. These trigger `TimeoutError`, not the same path as SIGINT.

### Pitfall 4: Ignoring Cleanup Cancellation

Cleanup code itself can be cancelled if it awaits. Use `asyncio.shield()` for critical cleanup:

```python
async def cleanup():
    await asyncio.shield(critical_cleanup_operation())
```

### Pitfall 5: Empty or Invalid Input Handling

Always validate inputs:
- Empty task lists
- Invalid concurrency limits (max_concurrent <= 0)
- None values

### Pitfall 6: Assuming gather Handles All Exceptions

`asyncio.gather(return_exceptions=True)` collects exceptions but doesn't handle them. Results must be inspected for exception instances.

## Edge Cases to Consider

1. **Empty task list**: Return early with empty results
2. **max_concurrent <= 0**: Raise ValueError or use sensible default
3. **All tasks fail**: Ensure all exceptions are reported
4. **Partial completion**: Track which tasks completed vs cancelled
5. **Nested cancellation**: Cleanup code getting cancelled
6. **Multiple rapid signals**: Debounce or ignore duplicate signals
7. **Windows compatibility**: `add_signal_handler` doesn't work on Windows for SIGINT; use alternative approaches

## Platform Considerations

### Unix/Linux/macOS

- `loop.add_signal_handler()` works for SIGINT, SIGTERM
- Signal handlers run in the main thread

### Windows

- `add_signal_handler()` is limited; only works for SIGINT in some cases
- Consider using `signal.signal()` before starting the event loop
- Or rely on the synchronous wrapper pattern
