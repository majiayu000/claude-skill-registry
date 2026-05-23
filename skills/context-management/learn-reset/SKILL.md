---
name: learn-reset
description: Clear the knowledge base and start fresh
user_invokable: true
---

# Learn Reset

Clear all accumulated knowledge and reset to a fresh state.

## What This Does

- Clears all entries from `knowledge/learnings/` files (patterns, quirks, decisions)
- Resets the classification cache
- Resets learning state (extraction count, queries)
- Preserves file structure (doesn't delete files)

**Warning:** This action cannot be undone. All accumulated insights will be lost.

## Instructions

1. **Confirm with user** - This is destructive, ask for confirmation first
2. **Reset learnings files** - Clear entries from:
   - `knowledge/learnings/patterns.md`
   - `knowledge/learnings/quirks.md`
   - `knowledge/learnings/decisions.md`
3. **Reset cache** - Clear `knowledge/cache/classifications.md`
4. **Reset session** - Clear `knowledge/context/session.md`
5. **Reset state** - Reset `knowledge/state.json` to initial values
6. **Confirm completion**

## Reset File Format

After reset, each learnings file should have:
```yaml
---
type: [type]
version: "1.0"
description: [original description]
last_updated: null
entry_count: 0
---

# [Title]

[Description]

**Purpose:** [Purpose]

---

<!-- Entries will be appended below this line -->
```

## State Reset

Reset `knowledge/state.json` to:
```json
{
  "version": "1.0",
  "learning_mode": false,
  "learning_mode_since": null,
  "last_extraction": null,
  "extraction_count": 0,
  "queries_since_extraction": 0,
  "extraction_threshold_queries": 10,
  "extraction_threshold_minutes": 30
}
```

## Output Format

```
Knowledge Base Reset
────────────────────
Are you sure you want to clear all knowledge? This cannot be undone.

[After confirmation]

Knowledge base has been reset:
  - Cleared 8 patterns
  - Cleared 3 quirks
  - Cleared 5 decisions
  - Cleared 23 cached classifications
  - Reset learning state

The knowledge base is now empty. Use /learn to start fresh.
```

## Notes

- Always confirm before resetting
- This does not delete the knowledge directory structure
- Learning mode is disabled after reset
- Git history may still contain old knowledge if previously committed
