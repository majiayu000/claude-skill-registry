---
name: session-start
description: |
  Load relevant memories at session start for context continuity.

  IMPORTANT: Use this AUTOMATICALLY at the START of every session.
  Search for memories related to:
  - Current working directory/project
  - Recent activity (last 7 days)
  - Topics the user mentions in their first message

  Execute silently - do not announce what you're loading.

user-invocable: true
disable-model-invocation: false
argument-hint: "[optional topic to focus on]"
---

# Session Start - Context Loading

Load relevant memories to maintain continuity across sessions.

## When to Invoke

**AUTOMATICALLY** at the beginning of every session:
- When user sends their first message
- Before responding to any request
- Silently in the background

## Execution Steps

1. **Identify context signals**:
   - Current working directory (from system context)
   - Project name (from path or CLAUDE.md)
   - User's first message keywords
   - Git branch if available

2. **Search for relevant memories**:
   ```
   mcp__memory-service__memory_search(
     query="<project name> OR <key topic>",
     limit=5,
     time_expr="last 7 days",
     quality_boost=0.3
   )
   ```

3. **Also search for**:
   - Recent session summaries: `query="session-summary", limit=3`
   - Client info if mentioned: `query="<client name>", tags=["client"]`
   - Active decisions: `query="decision", time_expr="last 14 days"`

4. **Integrate context**:
   - Use loaded memories to inform responses
   - Reference relevant past decisions
   - Continue where previous sessions left off

5. **Silent operation**:
   - Do NOT announce "I loaded X memories"
   - Just use the context naturally
   - Only mention if user asks about previous sessions

## Search Strategies

### By Project
```
memory_search(query="botsniper trading", limit=5)
memory_search(query="foodshot ai", limit=5)
```

### By Recency
```
memory_search(time_expr="last 3 days", limit=10)
memory_search(time_expr="yesterday", limit=5)
```

### By Type
```
memory_search(query="decision", tags=["decision"], limit=5)
memory_search(query="client", tags=["client"], limit=5)
```

### Combined
```
memory_search(
  query="<project> decisions",
  time_expr="last 7 days",
  quality_boost=0.3,
  limit=10
)
```

## What to Look For

| Memory Type | Why It Matters |
|-------------|----------------|
| Session summaries | What happened last time |
| Decisions | Active choices still relevant |
| Open items | Unfinished work to continue |
| Client info | Key details to remember |
| Gotchas | Pitfalls to avoid |
| Patterns | Established conventions |

## Example Flow

User starts session in `/Users/maskedhunter/coding/botsniper-optimizer`:

1. Detect: Project is "botsniper-optimizer", domain is "trading bots"
2. Search: `memory_search(query="botsniper trading bot", limit=5, time_expr="last 7 days")`
3. Load: Recent decisions about Billy V4, Blood V5 parameters
4. Search: `memory_search(query="session-summary", limit=2)`
5. Load: Yesterday's session about optimizing stop losses
6. Respond: Use this context to continue naturally

User says: "Let's continue working on the Hurricane bot"

1. Detect: Topic is "Hurricane bot", domain is "Kalshi weather trading"
2. Search: `memory_search(query="hurricane kalshi weather", limit=5)`
3. Load: Recent decisions about forecast verification, position monitoring
4. Continue: Pick up where previous session left off

## Cloud Recall Fallback

If local memory search returns fewer than 3 results AND cloud backup is configured
(~/.claude-memory-cloud.env exists):

1. **Search cloud backup**:
   ```bash
   cd ~/coding/claude-memory && python3 -m cloud.cli search "<project or topic>" --limit 5 --include-deleted
   ```

2. **If cloud has memories not found locally**:
   - Include cloud results in context with [CLOUD] indicator
   - Offer to restore if user asks about missing context

3. **Restore if needed**:
   ```bash
   cd ~/coding/claude-memory && python3 -m cloud.cli restore --hash <hash1>,<hash2>
   ```

The cloud preserves everything forever - even memories that were deleted
or compressed during local consolidation. This ensures total recall.

## Important Notes

- **Be proactive**: Don't wait for user to ask for context
- **Be silent**: Don't announce memory loading
- **Be selective**: Quality over quantity - top 5-10 memories
- **Be natural**: Weave context into responses seamlessly
- **Cloud fallback**: Use cloud when local results are sparse
