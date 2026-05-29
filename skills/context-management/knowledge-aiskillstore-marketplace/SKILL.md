---
name: knowledge
description: Display knowledge base status and recent learnings
user_invokable: true
---

# Knowledge

Display the current state of the project's knowledge base and recent learnings.

## What This Does

Shows:
- Learning mode status (on/off)
- Knowledge base statistics (entry counts per category)
- Recent learnings extracted
- Cache statistics

## Instructions

1. Read `knowledge/state.json` for learning mode status
2. Read each knowledge file and count entries:
   - `knowledge/cache/classifications.md`
   - `knowledge/learnings/patterns.md`
   - `knowledge/learnings/quirks.md`
   - `knowledge/learnings/decisions.md`
3. Extract recent entries (last 5) from learnings files
4. Format and display

## Output Format

```
╔═══════════════════════════════════════════════════╗
║           Project Knowledge Base                   ║
╚═══════════════════════════════════════════════════╝

📚 Learning Status
───────────────────────────────────────────────────
Mode: ON (since 2026-01-08 14:00)
Last Extraction: 5 minutes ago
Extractions This Session: 3

📊 Knowledge Statistics
───────────────────────────────────────────────────
Cache:
  - Classification entries: 23

Learnings:
  - Patterns: 8 entries
  - Quirks: 3 entries
  - Decisions: 5 entries
  - Total: 16 insights

📝 Recent Learnings
───────────────────────────────────────────────────
[Pattern] "Use async/await for API calls in this codebase"
  Discovered: 2026-01-08 | Confidence: high

[Quirk] "Auth module uses non-standard token format"
  Discovered: 2026-01-07 | Confidence: high

[Decision] "Chose Redis over in-memory cache for session storage"
  Made: 2026-01-06 | Confidence: high

💡 Commands
───────────────────────────────────────────────────
/learn      - Extract insights now
/learn-on   - Enable continuous learning
/learn-off  - Disable continuous learning
```

## When Knowledge Base is Empty

```
╔═══════════════════════════════════════════════════╗
║           Project Knowledge Base                   ║
╚═══════════════════════════════════════════════════╝

📚 Learning Status
───────────────────────────────────────────────────
Mode: OFF
No extractions yet

📊 Knowledge Statistics
───────────────────────────────────────────────────
Knowledge base is empty.

💡 Get Started
───────────────────────────────────────────────────
Use /learn to extract insights from your current session.
Use /learn-on to enable continuous learning.

The knowledge base will grow as you work, capturing:
  - Patterns that work well in this project
  - Quirks and gotchas to remember
  - Decisions and their rationale
```

## Steps

1. Read `knowledge/state.json`
2. Read frontmatter from each knowledge file to get entry counts
3. Parse recent entries from learnings files (look for `## Pattern:`, `## Quirk:`, `## Decision:` headers)
4. Format and display the summary
5. If files are missing or empty, show the "empty" state

## Notes

- Entry counts come from frontmatter `entry_count` field or by counting `##` headers
- Recent learnings are shown most recent first (by discovered/made date)
- This is a read-only command - it doesn't modify any files
