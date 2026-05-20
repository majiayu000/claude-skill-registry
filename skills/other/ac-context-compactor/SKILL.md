---
name: ac-context-compactor
description: Manage and compact context for long sessions. Use when context is filling up, creating handoff summaries, optimizing context usage, or preparing for session continuation.
---

# AC Context Compactor

Manage context usage and create compact summaries for session continuation.

## Purpose

Monitors context usage and creates compact summaries when approaching limits, enabling seamless session continuation without losing critical information.

## Quick Start

```python
from scripts.context_compactor import ContextCompactor

compactor = ContextCompactor(project_dir)
if await compactor.should_compact():
    summary = await compactor.create_compact_summary()
```

## Context Management

```
Context threshold: 85%
│
├── Below 85%: Continue normally
├── At 85%: Create compact summary
└── Above 90%: Force handoff
```

## Compaction Strategy

1. **Preserve**: Critical state and progress
2. **Summarize**: Completed features
3. **Extract**: Key decisions and context
4. **Compress**: Verbose information

## Summary Structure

```json
{
  "session_summary": {
    "features_completed": ["auth-001", "auth-002"],
    "current_feature": "api-001",
    "progress_percentage": 45.5
  },
  "key_decisions": [
    "Using JWT for auth",
    "PostgreSQL for database"
  ],
  "active_context": {
    "current_file": "src/api/routes.py",
    "current_task": "Implementing user endpoint"
  },
  "next_actions": [
    "Complete user endpoint",
    "Add authentication middleware"
  ]
}
```

## Integration

- Used by: `ac-session-manager` for auto-continuation
- Triggers: `ac-handoff-creator` when compacting

## API Reference

See `scripts/context_compactor.py` for full implementation.
