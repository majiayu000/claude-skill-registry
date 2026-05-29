---
name: hook-event-architecture
description: Design hook-based event systems for ADW observability. Use when implementing real-time event broadcasting, creating hook pipelines, or building agent activity monitoring.
allowed-tools: Read, Grep, Glob
---

# Hook Event Architecture

Design hook-based event systems for capturing and broadcasting agent activities in AI Developer Workflows.

## MANDATORY: docs-management Delegation

> **Documentation Verification:** This skill references Claude Code hook events and configuration
> that may change between releases. Before implementing, invoke `hook-management` skill to verify
> current event types and hook configuration patterns.

**Verification Checkpoint:**

- [ ] Did I invoke `hook-management` for current event types?
- [ ] Did official documentation confirm the event schema?
- [ ] Is my implementation based on official docs?

## When to Use

- Implementing real-time event broadcasting
- Building observability infrastructure
- Creating swimlane visualizations
- Logging agent activities to database
- Generating AI-powered event summaries

## Prerequisites

- Understanding of Claude Code hooks (@hook-event-patterns.md)
- Familiarity with WebSocket patterns (@websocket-architecture.md)
- Access to Claude Agent SDK for full implementation

## SDK Requirement

> **Implementation Note**: Full hook event architecture requires Claude Agent SDK with custom tooling. This skill provides design patterns and specifications.

## Event Types

> **Documentation Verification:** The event types listed here are Claude Code internal types that may change between releases. For authoritative current event types, query the `hook-management` skill which delegates to `docs-management` for official documentation.

ADW systems capture these event types:

| Event Type | Icon | Source | Payload |
| --- | --- | --- | --- |
| `PreToolUse` | 🪝 | Hook | Tool name, inputs, session |
| `PostToolUse` | 🪝 | Hook | Tool name, outputs, duration |
| `TextBlock` | 💬 | Agent | Response text, tokens |
| `ToolUseBlock` | 🛠️ | Agent | Tool invocation record |
| `ThinkingBlock` | 🧠 | Agent | Extended thinking content |
| `StepStart` | ⚙️ | System | Step name, inputs |
| `StepEnd` | ⚙️ | System | Step name, outputs, duration |

## Architecture Design Process

### Step 1: Define Event Schema

Create Pydantic models for events:

```python
class ADWEvent(BaseModel):
    type: str                    # Event type from table
    adw_id: str                  # 8-char correlation ID
    step: str                    # Current step name
    timestamp: datetime
    payload: dict                # Type-specific data
    summary: str | None          # AI-generated summary
```

### Step 2: Configure Hook Triggers

Set up Claude Code hooks:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": ".*",
      "command": "python hooks/pre_tool.py"
    }],
    "PostToolUse": [{
      "matcher": ".*",
      "command": "python hooks/post_tool.py"
    }]
  }
}
```

### Step 3: Design Event Pipeline

```text
Agent Execution
      │
      ├── PreToolUse ──► Hook Script ──┬── Log to DB
      │                                ├── Summarize (Haiku)
      ▼                                └── Broadcast (WebSocket)
Tool Execution
      │
      ├── PostToolUse ──► Hook Script ──┬── Log to DB
      │                                  ├── Summarize (Haiku)
      ▼                                  └── Broadcast (WebSocket)
Continue...
```

### Step 4: Implement Summarization

AI-generated event summaries using Haiku:

```python
async def summarize_event(event: ADWEvent) -> str:
    prompt = f"""Summarize in 15 words or less:
    Event: {event.type}
    Tool: {event.payload.get('tool_name', 'N/A')}
    Data: {str(event.payload)[:500]}
    """
    return await claude.complete(prompt, model="haiku")
```

### Step 5: Design Broadcast Pattern

Event distribution to clients:

```python
class EventBroadcaster:
    def __init__(self, ws_manager, db_client):
        self.ws = ws_manager
        self.db = db_client

    async def broadcast(self, event: ADWEvent):
        # Log to database first
        await self.db.log_event(event)

        # Broadcast to WebSocket clients
        await self.ws.broadcast(event.dict())
```

## Hook Script Templates

### PreToolUse Hook

```python
#!/usr/bin/env python
import sys, json, asyncio
from adw_modules import broadcast, summarize

async def main():
    data = json.load(sys.stdin)

    event = {
        "type": "PreToolUse",
        "adw_id": data.get("adw_id"),
        "step": data.get("step"),
        "payload": {
            "tool_name": data["tool_name"],
            "tool_input": data["tool_input"]
        }
    }

    event["summary"] = await summarize(event)
    await broadcast(event)

if __name__ == "__main__":
    asyncio.run(main())
```

### PostToolUse Hook

```python
#!/usr/bin/env python
import sys, json, asyncio
from adw_modules import broadcast, summarize

async def main():
    data = json.load(sys.stdin)

    event = {
        "type": "PostToolUse",
        "adw_id": data.get("adw_id"),
        "step": data.get("step"),
        "payload": {
            "tool_name": data["tool_name"],
            "tool_output": data.get("tool_output", "")[:1000],
            "duration_ms": data.get("duration_ms", 0)
        }
    }

    event["summary"] = await summarize(event)
    await broadcast(event)

if __name__ == "__main__":
    asyncio.run(main())
```

## Output Format

When designing hook event architecture:

```markdown
## Hook Event Architecture Design

### Event Types

| Type | Trigger | Payload Schema |
| --- | --- | --- |
| [type] | [when triggered] | [fields] |

### Hook Configuration

```json
[hooks.json configuration]
```

### Event Pipeline

```text
[ASCII diagram of flow]
```

### Summarization Strategy

[How Haiku generates summaries]

### Broadcasting Pattern

[WebSocket or other broadcast mechanism]

### Database Schema

```sql
[Event logging tables]
```

### Implementation Checklist

- [ ] [Step 1]
- [ ] [Step 2]
...

``` <!-- markdownlint-disable-line MD040 -->

## Design Checklist

- [ ] Event types defined with payloads
- [ ] Hook configuration specified
- [ ] Event pipeline documented
- [ ] Summarization prompt designed
- [ ] Broadcast mechanism chosen
- [ ] Database schema defined
- [ ] Error handling considered
- [ ] Performance implications assessed

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| --- | --- | --- |
| Sync broadcasting | Blocks agent execution | Async dispatch |
| No correlation ID | Can't trace workflows | Use adw_id |
| Raw payload logging | Token waste | Truncate large data |
| Missing summaries | Hard to scan | Always summarize |
| No error handling | Silent failures | Log and recover |

## Cross-References

- @hook-event-patterns.md - Event type details
- @websocket-architecture.md - Broadcasting patterns
- @production-patterns.md - Database logging
- @adw-framework.md - ADW overview

## Version History

- **v1.0.0** (2026-01-01): Initial release (Lesson 14)

---

## Last Updated

**Date:** 2026-01-01
**Model:** claude-opus-4-5-20251101
