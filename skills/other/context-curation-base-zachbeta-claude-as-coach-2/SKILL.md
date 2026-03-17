---
name: context-curation-base
description: Framework for managing project file context after retros/planning. Trigger after weekly retro + planning complete, after monthly retro + planning complete, or when context feels bloated. Also triggers with "context curation", "clean up project files", "archive old summaries", "what can we remove". Uses fractal compression with fold-before-archive pattern.
---

# Context Curation Skill

**Created:** Monday, January 19, 2026
**Updated:** Monday, January 20, 2026
**Purpose:** Systematic process for managing project file context after retros/planning sessions
**Status:** Experimental

---

## Overview

Context curation follows the "fractal compression" pattern: each level of summary makes the previous level's raw inputs archivable. Before archiving, **fold extractable data** into addendums or reference docs.

**Trigger phrases:**
- "context curation"
- "clean up project files"
- "archive old summaries"
- "what can we remove"

---

## Compression Hierarchy

```
Daily summaries → Weekly retros → Monthly retros → Quarterly retros → Yearly retros
```

| After completing... | These can be archived... |
|---------------------|--------------------------|
| Daily summary | Raw conversation logs for that day |
| Weekly retro | Daily summaries for that week |
| Monthly retro | Weekly retros for that month |
| Quarterly retro | Monthly retros for that quarter |
| Yearly retro | Quarterly retros for that year |

**Principle:** Keep at least one copy at each granularity level.

---

## Retention Minimums

Keep at least one document at each granularity level:

| Level | Minimum to Keep |
|-------|-----------------|
| Daily | 1-2 most recent summaries |
| Weekly | Current week's plan + most recent retro |
| Monthly | Current month's plan + most recent retro |
| Quarterly | Current quarter's plan + most recent retro |
| Yearly | Current year's plan + most recent retro |

**Principle:** Even after compression, maintain the ability to see recent state at each time scale.

---

## Fold Before Archive

Before archiving daily summaries, extract data that should persist in reference docs.

### What to Extract
- Quantitative progress (reps, times, measurements, PRs)
- Protocol changes or discoveries
- Status updates for tracked items
- Confirmed additions (new safe foods, new movements, etc.)

### Where to Extract

**Addendum files** for reference docs that accumulate data:
- `Reference-Doc.md` → `Reference-Doc-Addendum-YYYY-MM-DD-to-DD.md`
- Date range matches the weekly retro period
- Example: `Training-Log-Addendum-2026-02-16-to-22.md`

**Direct updates** for simple status changes:
- Single value changes can go directly to main doc
- Level progressions, status flips, etc.

### Addendum Naming Pattern

```
{Reference-Doc}-Addendum-YYYY-MM-DD-to-DD.md
```

Where date range matches the weekly retro being processed.

### When Addendums Get Compressed

During weekly curation, fold addendums into their main docs:
1. Review addendum content
2. Integrate into appropriate sections of main doc
3. Update revision date on main doc (e.g., `**Updated:** 2026-02-23`)
4. Save updated doc to project (replaces old version)
5. Archive the processed addendum

**Why revision dates matter:** When Claude produces an artifact for a reference doc, the revision date makes it clear which version is current. Old version can then be archived/removed from project.

### Reference Doc Versioning

**Date-in-filename** (preferred for periodic revisions):
- `Identity-Ecosystem-2025-12.md` → `Identity-Ecosystem-2026-03.md`
- Old version archived when new version created

**Updated-in-content** (for incremental updates):
- Keep same filename, update internal `**Updated:** YYYY-MM-DD`
- Works when addendums fold in small changes

---

## File Categories

### Always Keep (Reference Docs)
Documents with ongoing reference value that don't get "rolled up":
- Protocol docs (training plans, nutrition guidelines, recovery routines)
- Framework docs (goal hierarchies, progress tracking systems)
- Context docs (current status, background information)
- Research plans (active investigation threads)

### Keep Current Layer
Most recent documents at each temporal scale:
- Current week's plan + most recent weekly retro
- Current month's plan + most recent monthly retro
- 1-2 most recent daily summaries (bridge to current conversation)

### Archive Candidates
Documents whose content has been synthesized into higher-level summaries:
- Daily summaries covered by weekly retro (after extraction complete)
- Weekly retros covered by monthly retro
- Past weekly plans (executed, retro complete)
- Past monthly plans (after monthly retro captures outcomes)
- Processed addendums (folded into main docs)
- Old versions of reference docs (replaced by updated version)

---

## Process

### 1. Identify Temporal Boundary

What retro just completed?
- Weekly retro → daily summaries for that week can archive
- Monthly retro → weekly retros for that month can archive

### 2. Review Dailies for Extractable Data

Scan the daily summaries being archived for:
- Quantitative data that belongs in reference docs
- Protocol changes or confirmations
- Progress markers that should persist

### 3. Extract to Addendums

For each reference doc with extractable data:
- Create or append to addendum file for this week
- Use naming: `{Reference-Doc}-Addendum-YYYY-MM-DD-to-DD.md`

### 4. Compress Addendums into Main Docs

If any addendums exist from previous weeks:
- Review addendum content
- Integrate into appropriate sections of main doc
- Mark addendum for archiving

### 5. List Archive Candidates

Quick pass through project files:
- **Reference docs:** List, confirm keeping, check freshness
- **Current layer:** Identify most recent at each scale
- **Archive candidates:** List with reasoning

Format:
```
**EXTRACT - From this week's dailies:**
- [file]: "[data]" → [addendum file]

**COMPRESS - Addendums ready to fold:**
- [addendum file] (N entries) → [main doc]

**KEEP - Reference Docs:**
- [file] - [brief reason if not obvious]

**KEEP - Current Layer:**
- [file] - [which layer: daily/weekly/monthly]

**REFRESH - May Be Stale:**
- [file] - [why it may need updating]

**ARCHIVE - Folded into [Retro Name]:**
- [file]
- [file]
```

**Refresh triggers** (reference docs don't get archived, but they do get stale):
- Time-based: Last updated 30+ days ago
- Event-based: Major milestone, level change, protocol shift
- Content-based: Information contradicts recent summaries/retros

### 6. User Confirms and Archives

User reacts with:
- ✓ (agree with recommendation)
- ✗ (keep/reconsider specific file)
- Additional context ("also archive X" or "actually keep Y because...")

User then:
- Extracts data to addendums
- Compresses addendums into main docs
- Removes archived files from project

---

## Edge Cases

### Files Not Clearly Covered

If a time period's retro is missing or incomplete:
- Keep the lower-level docs until coverage exists
- Example: Keep Week 11 retro if December monthly doesn't clearly cover that period

### Reference Docs That Need Updates

Some "reference" docs get stale:
- Training plans → update as fitness levels change
- Equipment/gear lists → update as needs evolve
- Goal frameworks → update after major milestone shifts

Flag these for refresh rather than archive.

### Blended Summaries

When daily summaries span multiple days (due to missed days or combined entries):
- Still archive after weekly retro covers the period
- The blending itself is captured in the retro
- Extract any quantitative data before archiving

### No Extractable Data

If dailies have no quantitative/protocol data to extract:
- Skip the extract step
- Proceed directly to archiving
- Retro synthesis is sufficient

---

## Decision Principles

1. **Fold before archive:** Extract persistent data before removing source
2. **When in doubt, keep:** Can always archive later
3. **Compression preserves signal:** Higher-level synthesis captures what mattered
4. **Context is finite:** Project files affect conversation quality
5. **Recent > old:** Prefer keeping recent docs over historical
6. **Reference > temporal:** Reference docs have longer shelf life than summaries

---

## Example Session

**After Week 8 Retro (Rob's running project):**

```
Claude: Let's do context curation. First, any data to extract before archiving?

**EXTRACT - From this week's dailies:**
- Summary-02-16: "3.1mi at 9:45 pace" → Training-Log-Addendum-2026-02-16-to-22.md
- Summary-02-18: "New stretching routine working well" → Recovery-Protocol-Addendum-2026-02-16-to-22.md
- Summary-02-20: "PR: 5K in 28:32" → Training-Log-Addendum-2026-02-16-to-22.md

**COMPRESS - Addendums ready to fold:**
- Training-Log-Addendum-2026-02-09-to-15.md (4 entries) → Training-Log.md
- Recovery-Protocol-Addendum-2026-02-09-to-15.md (2 entries) → Recovery-Protocol.md

**KEEP - Reference Docs:**
- Training-Plan-5K.md
- Race-Schedule-2026.md
- Training-Log.md
- Recovery-Protocol.md

**KEEP - Current Layer:**
- Weekly-Plan-2026-02-23.md (current)
- Weekly-Retro-2026-02-16.md (just created)
- Summary-02-21.md, Summary-02-22.md (most recent)

**REFRESH - May Be Stale:**
- Training-Plan-5K.md - last updated 6 weeks ago, you've progressed past Week 4 intervals

**ARCHIVE - Folded into Week 8 Retro:**
- Weekly-Plan-2026-02-16.md
- Summary-02-16.md through Summary-02-20.md
- Training-Log-Addendum-2026-02-09-to-15.md (after compression)
- Recovery-Protocol-Addendum-2026-02-09-to-15.md (after compression)

User: Extracted the training data to addendums. Compressed last week's addendums into main docs. Archived the rest.

Claude: Good. Data preserved in reference docs. Context curated.
```

---

## Integration Notes

**When to trigger:**
- After weekly retro + planning complete
- After monthly retro + planning complete
- When context feels bloated / conversation quality degrading

**Typical weekly curation flow:**
1. Weekly retro (summary-of-summaries)
2. Weekly planning
3. Context curation:
   a. Extract from dailies → addendums
   b. Compress addendums → main reference docs
   c. Archive dailies (now folded into retro)
   d. Archive processed addendums (now folded into main docs)

**Cognitive load:**
- Keep it lightweight (quick pass, not deep analysis)
- User makes final call on each file
- Don't force decisions when depleted

**Skill dependencies:**
- Works alongside retrospective skills (uses their outputs)
- Works alongside planning skills (happens after planning complete)

---

*"Fold before archive. Keep most recent at each layer."*
