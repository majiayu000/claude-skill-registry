---
name: session-end
description: |
  Generate and save a session summary before ending conversation.

  IMPORTANT: Use this PROACTIVELY when:
  - User says "goodbye", "that's all", "thanks", "done for now"
  - Session has been productive with decisions/learnings
  - Conversation is naturally winding down

  DO NOT ask permission - just summarize and save silently.

user-invocable: true
disable-model-invocation: false
argument-hint: "[optional summary override]"
---

# Session End Summary

Generate a concise summary of this session and save it to memory.

## When to Invoke

Proactively invoke this skill when:
- User indicates session is ending ("bye", "thanks", "done", "that's all")
- Long productive session is wrapping up
- Significant work was completed

## Summary Format

Generate a summary with:

1. **One-line summary**: What was the main focus of this session?
2. **Key outcomes**: What was accomplished? (2-4 bullet points)
3. **Decisions made**: Any choices or directions decided
4. **Open items**: What's left to do or follow up on
5. **Tags**: Project names, technologies, topics discussed

## Execution Steps

1. **Review conversation**: Identify main topics, decisions, outcomes
2. **Generate summary**: Create concise session summary
3. **Extract tags**: Pull project names, technologies, client names
4. **Store to memory**: Use memory_store with type "progress"
5. **Update MEMORY.md**: If significant, append to quick reference
6. **Silent completion**: Do NOT announce unless user explicitly invoked /session-end

## Storage Format

```json
{
  "content": "Session summary: [one-line description]\n\nOutcomes:\n- [outcome 1]\n- [outcome 2]\n\nDecisions:\n- [decision 1]\n\nOpen items:\n- [item 1]",
  "metadata": {
    "type": "progress",
    "tags": "session-summary,[project],[topics]",
    "source": "session-end-skill"
  }
}
```

## Example

**Session about trading bot optimization:**

```
Session summary: Optimized Billy V4 bot parameters based on backtest results

Outcomes:
- Disabled shorts (losing $2,226 in backtests)
- Added funding rate filter (<0.02%)
- Tightened first scale to +2%

Decisions:
- Billy stays LONGS ONLY
- Blood keeps bidirectional with asymmetric Z

Open items:
- Monitor live performance for 1 week
- Consider adding SOL to tradeable coins
```

Tags: `session-summary, trading, billy-v4, optimization, backtest`

## MEMORY.md Update

If session produced significant outcomes, append to MEMORY.md under relevant section:

```markdown
### [Date] - [Project/Topic]
- [Key outcome or decision in one line]
```

Only update MEMORY.md for:
- New client information
- Major architectural decisions
- Important file path references
- Critical learnings that should be instantly visible
