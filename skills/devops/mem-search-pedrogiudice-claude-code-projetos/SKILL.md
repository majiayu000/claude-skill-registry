---
name: mem-search
description: 'Search through past session context and observations. Use when asking
  about past work, previous implementations, how something was done before, or recalling
  decisions. Keywords: remember, recall, last'
---

---
name: mem-search
description: Search through past session context and observations. Use when asking about past work, previous implementations, how something was done before, or recalling decisions. Keywords: remember, recall, last time, before, history, what did we, how did we
---

# Memory Search - Cross-Session Context

## Overview

Search through stored observations from past Claude Code sessions. Use this skill when the user asks about:

- "What did we do last session?"
- "How did we implement X before?"
- "What bugs did we fix recently?"
- "What decisions were made about Y?"
- "Show me recent work on this project"

## How to Use

Run the search command to query the context memory database:

```bash
python3 "$CLAUDE_PROJECT_DIR/.claude/memory/context_memory.py" search "<query>"
```

### Common Queries

**Recent activity:**
```bash
python3 "$CLAUDE_PROJECT_DIR/.claude/memory/context_memory.py" recent
```

**Search for specific topic:**
```bash
python3 "$CLAUDE_PROJECT_DIR/.claude/memory/context_memory.py" search "authentication"
```

**Get statistics:**
```bash
python3 "$CLAUDE_PROJECT_DIR/.claude/memory/context_memory.py" stats
```

**Get full context for current branch:**
```bash
python3 "$CLAUDE_PROJECT_DIR/.claude/memory/context_memory.py" context "branch-name"
```

## Observation Types

The memory stores these types of observations:

| Type | Symbol | Description |
|------|--------|-------------|
| decision | D | Choices made about architecture, tools, approaches |
| bugfix | B | Bug fixes and error resolutions |
| feature | F | New features implemented |
| refactor | R | Code refactoring and cleanup |
| discovery | i | Information discovered during exploration |
| change | C | General code changes |

## Database Location

The context memory is stored at: `~/.claude/context_memory.duckdb`

## Response Format

When presenting search results:

1. Group by type (decisions, bugfixes, features, etc.)
2. Show most recent first
3. Include timestamp and branch if relevant
4. Summarize rather than dump raw data

## Example Response

"Based on context memory, here's what happened:

**Recent Decisions:**
- [2 days ago] Chose DuckDB over SQLite + Chroma for context storage
- [3 days ago] Adopted tiered context injection strategy

**Recent Bugfixes:**
- [Yesterday] Fixed authentication timeout in API routes

**Recent Features:**
- [Today] Implemented context memory hooks"
