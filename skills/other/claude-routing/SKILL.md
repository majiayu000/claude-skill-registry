---
name: claude-routing
description: Skills for the Claude Code model routing system — managing persistent subagents (haiku/sonnet/opus).
---

# Claude Routing Skills

## /route

Explicitly evaluate and route a task to the appropriate subagent.

**Usage:** `/route <task description>`

**Behavior:**
1. Evaluate task complexity
2. Select model tier: haiku / sonnet / opus
3. Scan conversation history for existing agent IDs
4. Resume via `Agent(resume=id)` or initialize new subagent
5. Return result to user

**Examples:**
- `/route znajdź wszystkie pliki zawierające useState` → Haiku
- `/route zaimplementuj OAuth2 login` → Sonnet
- `/route zdebuguj memory leak w worker thread` → Opus

---

## /agents

Show status of persistent subagents in the current session.

**Usage:** `/agents`

**Behavior:** Scan conversation history and report:
- `haiku_id`: `<id>` or `not initialized`
- `sonnet_id`: `<id>` or `not initialized`
- `opus_id`: `<id>` or `not initialized`

Useful to verify which subagents are already running and can be resumed without re-initialization.
