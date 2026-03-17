---
name: claude-historian
description: Automatic history search — checks past sessions before web research, planning, and debugging, siblings deepen coverage
triggers: [PreToolUse, PostToolUse]
---

# Historian Plugin

Session memory. Checks past sessions before redundant research, planning, or debugging.

## Hooks

| Hook | When | Action |
|------|------|--------|
| **PreToolUse(WebSearch/WebFetch)** | Before web research | Checks `find_similar_queries()` first |
| **PreToolUse(EnterPlanMode)** | Before planning | Searches `search_plans()` for past approaches |
| **PreToolUse(Task)** | Before agents | Checks `find_tool_patterns()` for workflows |
| **PostToolUse(Bash)** | After errors | Suggests `get_error_solutions()` |

## Commands

| Command | Description |
|---------|-------------|
| `/search-historian <query>` | Search past sessions for solutions, decisions, context |

## Workflows

### Search (standalone)

1. `search_conversations("query")` — full-text across all sessions
2. If error-related: `get_error_solutions("error pattern")`
3. If file-related: `find_file_context("filename")`
4. Summarize relevant findings

### Search (with siblings)

1. `search_conversations("query")` — historian's own search
2. If **praetorian** active: `praetorian_restore("query")` for compacted context (denser than raw history)
3. If **oracle** active: `search("query")` when error patterns suggest a missing tool
4. Combine: historian provides breadth (all sessions), praetorian provides depth (curated insights)

### Error Resolution (standalone)

1. `get_error_solutions("error pattern")` — how was this fixed before?
2. If found: apply the previous solution
3. If not: proceed with normal debugging

### Error Resolution (with siblings)

1. `get_error_solutions("error pattern")` — historian checks past fixes
2. If **oracle** active: `search("error tool")` for tools that address this error class
3. If **gladiator** active: check if this error was already observed as a pattern
4. Present combined findings: past fix + available tools + pattern context

## Sibling Synergy

| Sibling | Value | How |
|---------|-------|-----|
| **Praetorian** | Research will be compacted after | Praetorian prompts saving after web searches historian triggers |
| **Oracle** | Tools found for error patterns | Oracle searches for tools when historian finds recurring errors |
| **Gladiator** | Observations correlate with history | Past solutions enrich gladiator reflection |
| **Vigil** | Checkpoints complement history | File state preserved alongside session history |

## MCP Tools Reference

| Tool | Purpose |
|------|---------|
| `search_conversations` | General history search |
| `find_similar_queries` | Find related past questions |
| `get_error_solutions` | Find how errors were fixed |
| `find_file_context` | Track file changes |
| `find_tool_patterns` | Discover successful workflows |
| `list_recent_sessions` | Browse recent work |
| `search_plans` | Find past implementation plans |

## Requires

```
claude mcp add historian -- npx claude-historian-mcp
```
