---
name: python-async
description: 'Consult this skill for async Python patterns and concurrency. Use when
  building async APIs, concurrent systems, I/O-bound applications, implementing rate
  limiting, async context managers. Do not use when CPU-bound optimization - use python-performance
  instead. DO NOT use when: testing async code - use python-testing async module.'
category: async
tags:
- python
- async
- asyncio
- concurrency
- await
- coroutines
tools:
- async-analyzer
- concurrency-checker
usage_patterns:
- async-api-development
- concurrent-io
- websocket-servers
- background-tasks
complexity: intermediate
estimated_tokens: 400
progressive_loading: true
modules:
- basic-patterns
- concurrency-control
- error-handling-timeouts
- advanced-patterns
- testing-async
- real-world-applications
- pitfalls-best-practices
---

# Async Python Patterns

asyncio and async/await patterns for Python applications.

## Quick Start

```python
import asyncio

async def main():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

asyncio.run(main())
```
**Verification:** Run the command with `--help` flag to verify availability.

## When To Use

- Building async web APIs (FastAPI, aiohttp)
- Implementing concurrent I/O operations
- Creating web scrapers with concurrent requests
- Developing real-time applications (WebSockets)
- Processing multiple independent tasks simultaneously
- Building microservices with async communication

## When NOT To Use

- CPU-bound optimization - use python-performance
  instead
- Testing async code - use python-testing async module
- CPU-bound optimization - use python-performance
  instead
- Testing async code - use python-testing async module

## Modules

This skill uses progressive loading. Content is organized into focused modules:

- See `modules/basic-patterns.md` - Core async/await, gather(), and task management
- See `modules/concurrency-control.md` - Semaphores and locks for rate limiting
- See `modules/error-handling-timeouts.md` - Error handling, timeouts, and cancellation
- See `modules/advanced-patterns.md` - Context managers, iterators, producer-consumer
- See `modules/testing-async.md` - Testing with pytest-asyncio
- See `modules/real-world-applications.md` - Web scraping and database operations
- See `modules/pitfalls-best-practices.md` - Common mistakes and best practices

Load specific modules based on your needs, or reference all for detailed guidance.

## Exit Criteria

- Async patterns applied correctly
- No blocking operations in async code
- Proper error handling implemented
- Rate limiting configured where needed
- Tests pass with pytest-asyncio
## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
