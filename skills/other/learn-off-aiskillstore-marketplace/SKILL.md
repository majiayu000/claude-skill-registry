---
name: learn-off
description: Disable continuous learning mode
user_invokable: true
---

# Learn Off

Disable continuous learning mode. Automatic insight extraction will stop.

## What This Does

Deactivates continuous learning mode:
- Automatic extraction stops
- Query counting stops
- Manual `/learn` commands still work

## Instructions

1. Read `knowledge/state.json`
2. Update the state:
   ```json
   {
     "learning_mode": false,
     "learning_mode_since": null
   }
   ```
3. Write updated state back to `knowledge/state.json`
4. Confirm to user with summary of what was learned

## Output Format

```
Continuous Learning: DISABLED
─────────────────────────────
Learning mode is now inactive.

Session summary:
  - Extractions performed: X
  - Queries analyzed: Y
  - Insights captured: Z

Manual extraction is still available via /learn.
Use /knowledge to view accumulated insights.
```

## Notes

- Disabling learning mode does not delete any captured insights
- The knowledge base remains available for reference
- You can re-enable with `/learn-on` at any time
