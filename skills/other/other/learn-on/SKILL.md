---
name: learn-on
description: Enable continuous learning mode for automatic insight extraction
user_invokable: true
---

# Learn On

Enable continuous learning mode. When active, the router will periodically extract insights during the session.

## What This Does

Activates continuous learning mode where:
- The router monitors query activity
- After a threshold (10 queries or 30 minutes), extraction is triggered automatically
- Insights are appended to the knowledge base without manual intervention

This is useful for long sessions where you want to capture insights as you go without remembering to run `/learn` manually.

## Instructions

1. Read `knowledge/state.json`
2. Update the state:
   ```json
   {
     "learning_mode": true,
     "learning_mode_since": "[current ISO timestamp]",
     "queries_since_extraction": 0
   }
   ```
3. Write updated state back to `knowledge/state.json`
4. Confirm to user

## Output Format

```
Continuous Learning: ENABLED
────────────────────────────
Learning mode is now active.

Extraction will trigger automatically:
  - Every 10 queries, or
  - Every 30 minutes of activity

Insights will be saved to:
  - knowledge/learnings/patterns.md
  - knowledge/learnings/quirks.md
  - knowledge/learnings/decisions.md

Use /learn-off to disable, or /learn for manual extraction.
```

## Notes

- Learning mode persists across the session but resets on new sessions
- The router checks this state on each query and triggers extraction when thresholds are met
- You can still run `/learn` manually while continuous mode is active
- Use `/knowledge` to see current learning status
