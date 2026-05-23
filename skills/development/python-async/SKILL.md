---
name: python-async
description: Asyncio patterns in Python for high-concurrency IO-bound tasks. Includes coroutines, task management, and asynchronous resource handling. Triggers: asyncio, python-async, coroutine, await, async-gather, async-generator, event-loop.
---

# Python Async

## Overview
Asyncio is a concurrency model designed for IO-bound and high-level structured network code. It uses cooperative multitasking on a single thread, allowing routines to pause while waiting for I/O, yielding control back to the event loop.

## When to Use
- **Network IO**: Web scraping, API requests, and database queries.
- **Web Servers**: Handling thousands of concurrent connections (e.g., FastAPI).
- **Concurrent Tasks**: Running multiple independent IO-bound operations simultaneously.

## Decision Tree
1. Is the task CPU-bound (e.g., heavy math, image processing)? 
   - YES: Use `multiprocessing` instead.
   - NO: Is the task waiting for external resources (API, Disk)? 
     - YES: Use `asyncio`.
2. Are you using `time.sleep`? 
   - YES: Replace with `await asyncio.sleep` to avoid blocking the event loop.

## Workflows

### 1. Concurrent Task Execution
1. Define multiple coroutine functions with `async def`.
2. Initiate the tasks using `asyncio.gather(*coros)` to run them concurrently.
3. Await the results to aggregate outputs efficiently.

### 2. Asynchronous Resource Management
1. Implement an asynchronous context manager using `__aenter__` and `__aexit__`.
2. Use the `async with` syntax to ensure resources (like network connections) are opened and closed without blocking the loop.
3. Perform I/O operations inside the context using `await`.

### 3. Processing Async Streams
1. Create an asynchronous generator using `yield` inside an `async def` function.
2. Iterate over the generator using `async for` to process data as it becomes available.
3. Avoid materializing the entire sequence in memory to keep memory overhead low.

## Non-Obvious Insights
- **Cooperative Multitasking**: Async is NOT parallelism; it is single-threaded. If one coroutine blocks (e.g., `time.sleep`), the entire program stops.
- **Modern Entry Point**: Always use `asyncio.run(main())` for the main entry point; avoid manual event loop management in modern Python.
- **Materialization Risk**: Using `async for` is essential for large datasets to prevent OOM (Out of Memory) errors by processing items one by one as they arrive.

## Evidence
- "asyncio is often a perfect fit for IO-bound and high-level structured network code." - [Python Docs](https://docs.python.org/3/library/asyncio.html)
- "Async I/O is a single-threaded, single-process technique that uses cooperative multitasking." - [Real Python](https://realpython.com/async-io-python/)
- "The await keyword suspends the execution of the surrounding coroutine and passes control back to the event loop." - [Real Python](https://realpython.com/async-io-python/)

## Scripts
- `scripts/python-async_tool.py`: Examples of `asyncio.gather` and `async for` generators.
- `scripts/python-async_tool.js`: Equivalent JavaScript `Promise.all` and async iterator examples.

## Dependencies
- `asyncio` (Standard Library)
- `aiohttp` or `httpx` (Recommended for async HTTP)

## References
- [references/README.md](references/README.md)