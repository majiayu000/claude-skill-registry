---
name: ac-handoff-creator
description: Create handoff packages for session transitions. Use when ending sessions, preparing for continuation, saving session state, or creating resumable context.
---

# AC Handoff Creator

Create handoff packages for seamless session transitions.

## Purpose

Packages all necessary context and state for the next session to seamlessly continue work, ensuring no progress is lost between sessions.

## Quick Start

```python
from scripts.handoff_creator import HandoffCreator

creator = HandoffCreator(project_dir)
handoff = await creator.create_handoff()
```

## Handoff Package

```json
{
  "id": "handoff-20240115-103000",
  "timestamp": "2024-01-15T10:30:00Z",
  "session_number": 5,

  "progress": {
    "features_completed": 25,
    "features_total": 50,
    "current_feature": "api-003",
    "percentage": 50.0
  },

  "context": {
    "summary": "Implementing REST API endpoints",
    "key_decisions": ["Using FastAPI", "JWT auth"],
    "blockers": []
  },

  "next_actions": [
    "Complete api-003 implementation",
    "Run tests for api module"
  ],

  "files_modified": [
    "src/api/routes.py",
    "tests/test_api.py"
  ]
}
```

## Workflow

1. **Capture**: Current state and progress
2. **Summarize**: Session accomplishments
3. **Extract**: Key context and decisions
4. **Plan**: Next actions for continuation
5. **Save**: Package for next session

## Integration

- Used by: `ac-session-manager` at session end
- Uses: `ac-context-compactor` for summaries
- Loads: By next session via `ac-state-tracker`

## API Reference

See `scripts/handoff_creator.py` for full implementation.
