---
name: ac-memory-manager
description: Manage persistent memory for autonomous coding. Use when storing/retrieving knowledge, managing Graphiti integration, persisting learnings, or accessing episodic memory.
---

# AC Memory Manager

Manage persistent memory using Graphiti for cross-session knowledge.

## Purpose

Integrates with Graphiti memory system to store and retrieve knowledge, enabling learning across sessions and projects.

## Quick Start

```python
from scripts.memory_manager import MemoryManager

memory = MemoryManager(project_dir)
await memory.store("auth patterns", {"jwt": True, "session": False})
knowledge = await memory.retrieve("authentication")
```

## Memory Types

- **Episodic**: Past events and experiences
- **Semantic**: Facts and knowledge
- **Procedural**: Learned skills and patterns

## Integration

Uses Graphiti + LadybugDB for persistent storage.

## API Reference

See `scripts/memory_manager.py` for full implementation.
