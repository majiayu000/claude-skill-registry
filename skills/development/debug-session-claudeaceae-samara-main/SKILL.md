---
name: debug-session
description: Debug Samara session management, message batching, and task routing. Use when messages are scrambled, batching seems wrong, group chats behave oddly, or concurrent tasks interfere with each other. Trigger words: session, batch, group chat, concurrent, scrambled, task routing.
context: fork
allowed-tools:
  - Bash
  - Read
  - Grep
---

# Debug Session Management

Diagnose issues with Samara's message batching, session continuity, and task routing.

## Session Architecture Overview

```
Messages arrive
      │
      ▼
SessionManager buffers (11 sec)
      │
      ▼
TaskRouter classifies tasks
      │
      ├─► Conversation ──► invokeBatch (with session)
      ├─► Webcam ────────► invokeIsolated (no session)
      ├─► WebFetch ──────► invokeIsolated (no session)
      └─► Skill ─────────► invokeIsolated (no session)
      │
      ▼
MessageBus sends response (with source tag)
```

## Quick Diagnostics

### 1. Check Active Sessions
```bash
# View session state
cat ~/.claude-mind/state/sessions.json 2>/dev/null | head -30

# Check for stale locks
cat ~/.claude-mind/claude.lock 2>/dev/null
ls -la ~/.claude-mind/claude.lock
```

### 2. Check Message Batching
```bash
# Look for batch processing in logs
grep -E "(Buffering|batch|BatchReady)" ~/.claude-mind/logs/samara.log | tail -20

# Check batch sizes
grep "Processing batch of" ~/.claude-mind/logs/samara.log | tail -10
```

### 3. Check Task Classification
```bash
# Look for isolated vs session-based invocations
grep -E "(Isolated invocation|Resuming session|Starting new session)" ~/.claude-mind/logs/samara.log | tail -20
```

### 4. Check Group Chat Handling
```bash
# Group chat routing decisions
grep -E "(group chat|chatIdentifier|isGroupChat)" ~/.claude-mind/logs/samara.log | tail -20

# Look for routing warnings
grep -E "(WARNING.*group|looks like group)" ~/.claude-mind/logs/samara.log | tail -10
```

## Common Issues

### Scrambled Responses
**Symptom:** Responses seem to mix answers to different questions
**Cause:** Multiple task types in same batch not properly isolated
**Check:**
```bash
# Look for multiple task types in same batch
grep -B5 -A5 "Processing batch" ~/.claude-mind/logs/samara.log | tail -30
```
**Fix:** TaskRouter should classify and isolate parallel tasks

### Session Not Resuming
**Symptom:** Context lost between messages
**Cause:** Session ID not being passed correctly
**Check:**
```bash
# Check session recording
grep "Recorded session" ~/.claude-mind/logs/samara.log | tail -10

# Check session retrieval
grep "Retrieved session" ~/.claude-mind/logs/samara.log | tail -10
```

### Group Chat Messages Going to Wrong Chat
**Symptom:** Response sent to 1:1 instead of group
**Cause:** `isGroupChat` flag not set correctly
**Check:**
```bash
# Check routing decisions
grep "Routing decision" ~/.claude-mind/logs/samara.log | tail -10
```

### Queue Not Processing
**Symptom:** Messages acknowledged but never answered
**Cause:** TaskLock stuck or QueueProcessor not running
**Check:**
```bash
# Check lock status
cat ~/.claude-mind/claude.lock

# Check queue processor
grep "QueueProcessor" ~/.claude-mind/logs/samara.log | tail -10

# Force release stale lock if needed
# rm ~/.claude-mind/claude.lock
```

## Task Routing Reference

| Request Type | Detection | Isolation |
|--------------|-----------|-----------|
| Conversation | Default | Uses session |
| Webcam | "webcam", "camera", "photo" | Isolated |
| WebFetch | URLs, "check this" | Isolated |
| Skill | Starts with "/" | Isolated |

## Session State Files

| File | Purpose |
|------|---------|
| `~/.claude-mind/state/sessions.json` | Per-chat session IDs |
| `~/.claude-mind/claude.lock` | Current task lock |
| `~/.claude-mind/state/message-queue.json` | Pending messages |

## Diagnostic Report

When debugging session issues, gather:
1. Recent batch processing logs
2. Session state file contents
3. Lock file status
4. Task routing decisions
5. Group chat routing decisions
