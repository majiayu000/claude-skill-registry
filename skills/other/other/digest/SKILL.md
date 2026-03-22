---
name: digest
description: Summarize vault learnings and activity for today or a date range.
user-invocable: true
argument-hint: "[today | YYYY-MM-DD | YYYY-MM-DD..YYYY-MM-DD]"
context: fork
agent: researcher
allowed-tools:
  - Read
  - Glob
  - Grep
model: sonnet
---

# Learning Digest

Summarize vault learnings and activity for a given time period.

## Current State
!`ls vault/learnings/ 2>/dev/null | wc -l | tr -d ' '` total learning files
!`ls vault/learnings/*-$(date +%Y%m%d)-* 2>/dev/null || echo "(none today)"`
!`cat vault/daily/$(date +%Y-%m-%d).md 2>/dev/null || echo "(no daily digest yet)"`

## Date Parsing

Parse `$ARGUMENTS` to determine the date range:
- No args or `today` — today's date only
- `YYYY-MM-DD` — specific date
- `YYYY-MM-DD..YYYY-MM-DD` — date range (inclusive)

Convert dates to the `YYYYMMDD` format used in filenames.

## Analysis Steps

1. **Find matching files**: `Glob` for `vault/learnings/*-YYYYMMDD-*` for each date in range
2. **Read each file**: Extract frontmatter (type, status, priority/severity, tags, pattern-key, recurrence-count)
3. **Aggregate**:
   - Count by type (LRN/ERR/FEAT)
   - Count by status
   - Count by area
   - List any with recurrence-count >= 2 (approaching promotion)
   - List any FEAT entries with status `requested` (potential quick wins)
4. **Check for daily digest**: Read `vault/daily/YYYY-MM-DD.md` if it exists
5. **Compile summary**

## Output Format

```
## Learning Digest: YYYY-MM-DD

### Activity
- 3 new learnings, 1 error, 0 feature requests
- 2 entries resolved today
- 1 pattern approaching promotion threshold

### New Entries
| ID | Type | Title | Status |
|----|------|-------|--------|
| LRN-20250310-001 | learning | Title here | new |
| ERR-20250310-001 | error | Title here | resolved |

### Patterns to Watch
- **env-var-stripping** (recurrence: 2/3 for promotion) — Claude CLI env issues
- **file-path-quoting** (recurrence: 2/3 for promotion) — Spaces in paths

### Quick Wins
- FEAT-20250310-001: "Add vault search from CLI" (complexity: simple)

### Daily Digest File
<contents of vault/daily/YYYY-MM-DD.md if it exists, or "(not yet generated)">
```

For date ranges, group entries by date and show per-day breakdowns followed by a range summary.
