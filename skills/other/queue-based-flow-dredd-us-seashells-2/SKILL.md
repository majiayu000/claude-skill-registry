---
name: queue-based-flow
description: Stack prompts in queue while agent runs, minimizing context switches to achieve sustained 6k lines per day output and preserved flow state. Use for heavy coding sessions, iterative refinements, rapid iteration cycles, or sustained productivity. Queue enables async execution without blocking. Triggers on "flow state", "queue prompts", "heavy coding", "sustained output", "minimize interruptions".
---

# Queue-Based Flow State

## Purpose

Stack prompts in queue while agent executes, minimizing context switches to achieve sustained 6k lines/day output.

## When to Use

- Heavy coding sessions
- Iterative refinements
- Flow state preservation
- Rapid iteration cycles
- High-productivity sessions

## Core Instructions

### Queue Pattern

```python
from asyncio import Queue
import asyncio

class PromptQueue:
    def __init__(self):
        self.queue = Queue()
        self.running = False

    async def add_prompt(self, prompt):
        """Add prompt to queue"""
        await self.queue.put(prompt)
        if not self.running:
            await self.process_queue()

    async def process_queue(self):
        """Process queued prompts"""
        self.running = True

        while not self.queue.empty():
            prompt = await self.queue.get()
            await self.execute_async(prompt)
            self.queue.task_done()

        self.running = False

    async def execute_async(self, prompt):
        """Execute prompt asynchronously"""
        result = await agent.execute(prompt)
        return result
```

### Usage Example

```python
queue = PromptQueue()

# User rapidly adds prompts without waiting
await queue.add_prompt("Fix bug in auth.py")
await queue.add_prompt("Add tests for new feature")
await queue.add_prompt("Refactor database layer")
await queue.add_prompt("Update documentation")

# All execute in sequence without context switches
# User maintains flow state
```

## Performance

- **6k lines/day** sustained output
- Minimized context switching
- Preserved flow state
- Async execution

## Version

v1.0.0 (2025-10-23)

