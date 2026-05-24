---
name: dev-coordination-message-formats
description: JSON schemas for Ralph message system
category: coordination
---

# Message Formats

All messages use this standard format for the Ralph event-driven system.

## Message Structure

```json
{
  "id": "msg-{recipient}-{timestamp}-{seq}",
  "from": "sender",
  "to": "recipient",
  "type": "message_type",
  "priority": "normal|high|urgent",
  "payload": { },
  "timestamp": "2025-01-23T12:00:00.0000000Z",
  "status": "pending",
  "replyTo": null
}
```

## Message ID Format

`msg-{recipient}-{yyyyMMdd-HHmmss}-{sequence}`

Examples:
- `msg-developer-20250123-120000-001`
- `msg-qa-20250123-120005-001`

## Message Types

### Task Messages

#### task_assign
PM → Developer: Assign a new task
```json
{
  "type": "task_assign",
  "payload": {
    "taskId": "feat-001",
    "title": "Feature title",
    "description": "Description...",
    "acceptanceCriteria": [...],
    "worktree": "path/to/worktree"
  }
}
```

#### implementation_complete
Developer → QA: Implementation ready for validation
```json
{
  "type": "implementation_complete",
  "payload": {
    "taskId": "feat-001",
    "summary": "Brief summary",
    "commitHash": "abc123",
    "branch": "developer-worktree",
    "filesModified": ["file1.ts", "file2.ts"]
  }
}
```

### Validation Messages

#### validation_passed
QA → PM: Validation successful
```json
{
  "type": "validation_passed",
  "payload": {
    "taskId": "feat-001",
    "results": {
      "typecheck": "pass",
      "lint": "pass",
      "test": "pass",
      "build": "pass"
    }
  }
}
```

#### bug_report
QA → Developer: Bugs found
```json
{
  "type": "bug_report",
  "payload": {
    "taskId": "feat-001",
    "bugs": [
      { "file": "file.ts", "line": 10, "issue": "Bug description" }
    ]
  }
}
```

### Coordination Messages

#### question
Any Agent → PM: Ask for clarification
```json
{
  "type": "question",
  "payload": {
    "taskId": "feat-001",
    "question": "Question text..."
  }
}
```

#### answer
PM → Any Agent: Response to question
```json
{
  "type": "answer",
  "payload": {
    "questionId": "...",
    "answer": "Answer text..."
  }
}
```

#### status_update
Any Agent → Watchdog: Status heartbeat
```json
{
  "type": "status_update",
  "payload": {
    "agent": "developer",
    "status": "working|idle",
    "taskId": "feat-001"
  }
}
```

## Priority Levels

- `low` - Background tasks
- `normal` - Standard work (default)
- `high` - Important work
- `urgent` - Critical issues/blocks

## Message Locations

Messages are stored in inbox directories:
```
.claude/session/messages/
├── pm/           # PM's inbox
├── developer/    # Developer's inbox
├── qa/           # QA's inbox
└── watchdog/     # Watchdog's inbox (status updates)
```

## Message Lifecycle

1. **Created** - Written to recipient's inbox
2. **Delivered** - Watchdog restarts recipient with message
3. **Processed** - Recipient handles message
4. **Deleted** - Removed from inbox after processing
