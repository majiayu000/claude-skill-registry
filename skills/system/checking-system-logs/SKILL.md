---
name: checking-system-logs
description: Find bridge events, agent responses, timeouts, and errors in system logs. ALWAYS filter by project name. Use when debugging system behavior, investigating errors, or checking what the agent did.
allowed-tools: Read, Grep, Glob, Bash
---

# System Logs

**Location**: `/Users/valorengels/src/ai/logs/bridge.events.jsonl`

**IMPORTANT**: Always filter by project to get relevant results.

## Fields

- `project` - **required filter** ("DM", "Valor", "Django Project Template", etc.)
- `type` - event type (see below)
- `chat` - group name (null for DMs)
- `session_id` - e.g., "tg_dm_179144806"
- `sender` - who triggered the event

## Event Types

- `message_received` - incoming message
- `agent_request` - request sent to agent
- `agent_response` - Valor's response
- `agent_timeout` - response timed out
- `reply_sent` - message sent back to user
- `error` - system error

## Query Examples

```bash
# ALWAYS filter by project first, then by type or other criteria

# All recent events for a project
grep '"project": "Valor"' /Users/valorengels/src/ai/logs/bridge.events.jsonl | tail -20 | jq .

# Agent responses for a project
grep '"project": "Valor"' /Users/valorengels/src/ai/logs/bridge.events.jsonl | grep '"type": "agent_response"' | tail -10 | jq .

# Errors for a project
grep '"project": "Valor"' /Users/valorengels/src/ai/logs/bridge.events.jsonl | grep '"type": "error"' | tail -10 | jq .

# Timeouts for a project
grep '"project": "Valor"' /Users/valorengels/src/ai/logs/bridge.events.jsonl | grep '"type": "agent_timeout"' | tail -10 | jq .

# Search keyword within a project
grep '"project": "Valor"' /Users/valorengels/src/ai/logs/bridge.events.jsonl | grep -i "keyword" | tail -10 | jq .
```

## List Available Projects

```bash
grep -o '"project": "[^"]*"' /Users/valorengels/src/ai/logs/bridge.events.jsonl | sort -u
```

## If No Results

If a project filter returns no results, list available projects and report them:

```bash
# No results? Check available projects:
grep -o '"project": "[^"]*"' /Users/valorengels/src/ai/logs/bridge.events.jsonl | sort -u
# Then retry with a valid project name from the list
```
