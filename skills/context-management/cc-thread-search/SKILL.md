---
name: thread-search
description: Search Claude Code conversation history. Use when user asks "where did I discuss X", "when did we talk about X", "find the conversation about X", or wants to continue previous work.
---

# Thread Search

Search and analyze Claude Code conversation history.

## Quick Reference

| Fact | Value |
|------|-------|
| Threads location | `~/.claude/projects/` |
| Path encoding | Slashes → dashes (e.g., `/Users/foo/bar` → `-Users-foo-bar`) |
| Thread format | JSONL (one JSON object per line) |
| Main threads | `<uuid>.jsonl` |
| Subagent threads | `agent-<hash>.jsonl` |

## Tool Selection

| Task | Use This | NOT This |
|------|----------|----------|
| Pattern search | CC **Grep** tool | `rg` via Bash |
| Read files | CC **Read** tool | `cat` via Bash |
| Find files | CC **Glob** tool | `find` via Bash |
| JSON extraction | `jq` via **Bash** | (no CC equivalent) |

**Why CC tools**: Better permissions, structured output, error handling.
**Why Bash for jq**: No native JSONL parsing in CC.

## JSONL Message Structure

```json
{
  "type": "user" | "assistant" | "summary",
  "timestamp": "<ISO-8601>",
  "message": { "content": [{ "type": "text", "text": "..." }] },
  "uuid": "<uuid>",
  "sessionId": "<uuid>"
}
```

## Search Approach

**Step 1**: Use CC Grep tool to find matching threads
```
Grep pattern="X" path="~/.claude/projects/" output_mode="files_with_matches"
```

**Step 2**: Use Bash + jq for JSON extraction
```bash
jq -c 'select(.type=="user") | select(.message.content[].text | test("pattern";"i"))' file.jsonl
```

**Step 3**: Use CC Read tool to examine specific thread content

## Query Workflows

### "Where did I discuss X?"
1. Grep tool → find matching thread files
2. Decode paths to project names
3. Bash + jq → extract first timestamp + context
4. Report: project, thread ID, date range, snippet

### "When did we discuss X?"
1. Grep tool → find matching files
2. Bash + jq → extract timestamps from matches
3. Report: timeline grouped by date/project

### "Continue work on X"
1. Grep tool → find threads mentioning X
2. Read tool → examine most relevant thread
3. Analyze: goal, accomplishments, pending items, decisions
4. Generate continuation prompt (see template below)

## Continuation Prompt Template

```
Continuing work from [date] on [project]:

## Original Goal
[from first user message]

## What Was Done
- [accomplishments]
- [files changed]

## Pending
- [incomplete items]

## Key Decisions
- [choices that carry forward]

## Resume Point
[specific next task]
```

## jq Patterns

```bash
# Decode project path (inline)
echo "-Users-foo-bar" | sed 's/^-/\//; s/-/\//g'

# Extract timestamps from thread
jq -r '.timestamp // empty' file.jsonl | sort

# User messages only
jq -c 'select(.type=="user")' file.jsonl

# Filter by text content
jq -c 'select(.message.content[].text | test("pattern";"i"))' file.jsonl

# Get first/last timestamp
jq -rs '[.[].timestamp | select(.)] | sort | .[0], .[-1]' file.jsonl
```

## Further Reference

For deeper Claude Code internals (storage, configuration, settings):
→ Use `superpowers-developing-for-claude-code:working-with-claude-code` skill
