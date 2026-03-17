---
name: archive-prd
description: Archives completed stories from prd.json to reduce token usage.
triggers:
  - archive
  - compact prd
  - prd too large
allowed-tools: Read, Write, Edit, Bash
model: opus
user-invocable: true
argument-hint: "[status|S-ID|unarchive S-ID]"
---

# PRD Archival System

Archive completed stories to keep prd.json fast and small. Keep only last 3 sprints active.

## "archive" Command

```
1. Read prd.json
2. Separate stories:
   - ACTIVE: passes=false OR passes=null OR type="qa"
   - COMPLETED: passes=true AND type!="qa"
3. Create archive file: .claude/archives/prd-archive-YYYY-MM.json
4. Update main prd.json with summary
5. Report: "Archived X stories, Y remain active"
```

## New prd.json Schema (After Archive)

```json
{
  "project": "Project Name",
  "version": "1.3.2",
  "lastUpdated": "2026-01-22",
  "roadmapPhase": "Current Phase",

  "archived": {
    "totalCompleted": 41,
    "lastArchived": "2026-01-22",
    "files": [".claude/archives/prd-archive-2026-01.json"],
    "summary": {
      "S01-S10": "Core foundation - registry, funnels, OAuth, caching",
      "S11-S20": "Navigation, QA, dashboard, exports, favorites",
      "S21-S30": "Time granularity, GA4 schema, accessibility, mobile",
      "S31-S41": "Token refresh, metrics, documentation, scope rules"
    }
  },

  "stories": [
    // Only active/pending stories here
  ]
}
```

## Archive File Schema

```json
{
  "archivedAt": "2026-01-22T10:00:00Z",
  "project": "Project Name",
  "version": "1.3.2",
  "stories": [
    // Full story objects for reference
  ]
}
```

## When to Archive

| Condition | Action |
|-----------|--------|
| 4+ total sprints | Auto-suggest archive |
| prd.json > 500 lines | Suggest archive |
| prd.json > 50KB | Force archive |
| User says "archive" | Manual archive |
| All stories complete | Archive and start fresh |

Keep only the last 3 sprints in prd.json. Archive everything older.

## Archive Process

```
1. BACKUP
   mkdir -p .claude/archives
   cp prd.json .claude/archives/prd-backup-$(date +%Y%m%d).json

2. EXTRACT COMPLETED
   Filter: passes=true AND type!="qa"

3. CREATE ARCHIVE
   Write to: .claude/archives/prd-archive-YYYY-MM.json

4. GENERATE SUMMARY
   Group stories by ID range (10 per group)
   Write 1-line summary per group

5. UPDATE MAIN PRD
   Remove archived stories
   Add "archived" section with summary
   Keep all QA stories (even passed ones for re-testing)

6. VALIDATE
   Ensure main prd.json < 1500 lines
   Ensure all story IDs accounted for
```

## Accessing Archived Stories

If you need details on an archived story:

```
User: "What was S15 about?"
Claude:
1. Check archived.summary for S15 range
2. Read .claude/archives/prd-archive-2026-01.json if needed
3. Report story details
```

## Quick Reference

| Say | Action |
|-----|--------|
| `archive` | Archive completed stories |
| `archive status` | Show archive stats |
| `archive S15` | Show archived story S15 |
| `unarchive S15` | Restore story to active |

---

## Token Optimization

| State | Estimated Tokens |
|-------|-----------------|
| Full prd.json (70+ stories, 10 sprints) | ~25,000+ |
| After archive (current sprint + 2) | ~3,000-5,000 |
| With summary | +500 |
| **Total Savings** | **~80%** |

**Real example:** muzic.ai grew to 828 rows / 10 sprints / ~20K tokens. After archiving to keep only sprints 9-11, prd.json drops to ~150 rows / ~3K tokens.
