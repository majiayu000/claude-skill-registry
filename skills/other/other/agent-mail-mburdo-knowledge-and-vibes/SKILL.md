---
name: agent-mail
description: Multi-agent coordination with Agent Mail MCP. Use when registering agents, reserving files, sending messages, coordinating with other agents, or when the user mentions "agent mail", "coordination", "file reservation", or "multi-agent".
---

# Agent Mail (MCP Server)

Multi-agent coordination: registration, file reservations, messaging, and build slots.

## When This Applies

| Signal | Action |
|--------|--------|
| Starting a session | `ensure_project` + `register_agent` |
| Before editing files | `file_reservation_paths` |
| Communicating with agents | `send_message` / `fetch_inbox` |
| Finishing work | `release_file_reservations` |

---

## Registration (Required First)

```python
# 1. Ensure project exists
ensure_project(human_key="/abs/path/to/project")

# 2. Register yourself (auto-generates name like "GreenCastle")
register_agent(
    project_key="/abs/path/to/project",
    program="claude-code",
    model="opus-4.5",
    task_description="Working on feature X"
)
# SAVE the returned agent name!

# 3. Set contact policy
set_contact_policy(
    project_key="/abs/path/to/project",
    agent_name="YOUR_AGENT_NAME",
    policy="open"
)
```

---

## File Reservations

**Reserve before editing:**

```python
file_reservation_paths(
    project_key="/abs/path",
    agent_name="YourName",
    paths=["src/module/**", "tests/test_module.py"],
    ttl_seconds=3600,
    exclusive=True,
    reason="bd-123: implementing feature"
)
```

**Extend if needed:**

```python
renew_file_reservations(
    project_key="/abs/path",
    agent_name="YourName",
    extend_seconds=1800
)
```

**Release when done:**

```python
release_file_reservations(
    project_key="/abs/path",
    agent_name="YourName"
)
```

---

## Messaging

**Send message:**

```python
send_message(
    project_key="/abs/path",
    sender_name="YourName",
    to=["OtherAgent"],
    subject="[CLAIMED] bd-123 - Feature Title",
    body_md="Starting work on **bd-123**.\n\nFile reservations: `src/module/**`",
    thread_id="bd-123",
    importance="normal"  # low, normal, high, urgent
)
```

**Reply:**

```python
reply_message(
    project_key="/abs/path",
    message_id=123,
    sender_name="YourName",
    body_md="Acknowledged. Proceeding."
)
```

**Check inbox:**

```python
fetch_inbox(
    project_key="/abs/path",
    agent_name="YourName",
    include_bodies=True,
    limit=10
)

# Urgent only
fetch_inbox(project_key, agent_name, urgent_only=True)
```

**Acknowledge:**

```python
acknowledge_message(project_key, agent_name, message_id)
```

---

## Discovery

**Find other agents:**

```python
ReadMcpResourceTool(
    server="mcp-agent-mail",
    uri="resource://agents/PROJECT_PATH"
)
```

**Search messages:**

```python
search_messages(project_key, query="authentication", limit=20)
```

**Thread summary:**

```python
summarize_thread(project_key, thread_id="bd-123")
```

**Who is this agent?**

```python
whois(project_key, agent_name="BlueLake")
```

---

## Build Coordination

```python
# Acquire build slot (prevents concurrent builds)
acquire_build_slot(project_key, agent_name, slot="main", exclusive=True)

# Release when done
release_build_slot(project_key, agent_name, slot="main")
```

---

## Quick Start Macro (RECOMMENDED)

One call to start a session - **use this instead of manual steps**:

```python
macro_start_session(
    human_key="/abs/path",
    program="claude-code",
    model="opus-4.5",
    file_reservation_paths=["src/**"],
    inbox_limit=10
)
```

This automatically:
1. Ensures project exists
2. Registers agent (auto-generates name)
3. Reserves specified files
4. Fetches recent inbox messages

**Return value includes:**
- `agent_name`: Your assigned name (e.g., "BlueLake")
- `project`: Project details
- `file_reservations`: Granted reservations
- `inbox`: Recent messages

---

## Error Handling

### Common Errors

| Error | Fix |
|-------|-----|
| "from_agent not registered" | Call `register_agent` first |
| `FILE_RESERVATION_CONFLICT` | Wait for expiry or coordinate with holder |
| "project not found" | Call `ensure_project` first |

### Graceful Error Handling Pattern

When a tool call fails, include `is_error: true` in the result so Claude understands the failure:

```python
# Example: Handling file reservation conflict
result = file_reservation_paths(
    project_key="/abs/path",
    agent_name="YourName",
    paths=["src/auth/**"],
    exclusive=True
)

if result.get("conflicts"):
    # Return error so Claude can adapt
    tool_result = {
        "type": "tool_result",
        "tool_use_id": tool_use_id,
        "is_error": True,  # CRITICAL: Tells Claude this failed
        "content": f"FILE_RESERVATION_CONFLICT: {result['conflicts'][0]['holders']}"
    }
    # Claude will now try a different approach or coordinate
```

### Error Response Examples

```python
# Conflict error
{
    "is_error": True,
    "content": "FILE_RESERVATION_CONFLICT: src/auth/** held by BlueLake (expires in 45min)"
}

# Registration error
{
    "is_error": True,
    "content": "AGENT_NOT_REGISTERED: Call register_agent() before sending messages"
}

# Project error
{
    "is_error": True,
    "content": "PROJECT_NOT_FOUND: Call ensure_project() with absolute path first"
}
```

### Recovery Strategies

| Error Type | Recovery |
|------------|----------|
| `FILE_RESERVATION_CONFLICT` | Wait, coordinate via message, or pick different task |
| `AGENT_NOT_REGISTERED` | Call `register_agent()` then retry |
| `PROJECT_NOT_FOUND` | Call `ensure_project()` then retry |
| `MESSAGE_SEND_FAILED` | Retry with exponential backoff |

---

## Web UI

http://127.0.0.1:8765/mail

---

## Quick Reference

```python
# Startup
ensure_project(human_key=PATH)
register_agent(project_key=PATH, program="claude-code", model="opus-4.5")

# Files
file_reservation_paths(project_key, agent_name, paths, exclusive=True)
release_file_reservations(project_key, agent_name)

# Messaging
send_message(project_key, sender_name, to, subject, body_md, thread_id)
fetch_inbox(project_key, agent_name, include_bodies=True)
reply_message(project_key, message_id, sender_name, body_md)
```

---

## See Also

- `prime/` — Full startup protocol
- `advance/` — Bead lifecycle with announcements
