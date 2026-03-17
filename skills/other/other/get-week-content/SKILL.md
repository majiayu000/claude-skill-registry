---
name: get-week-content
description: Read and parse Week.md content for weekly review. Returns structured data including frontmatter, sections, completeness assessment, and extracted entities.
disable-model-invocation: true
allowed-tools: Read, Bash(ls)
---

# Get Week Content Sub-Skill

Reads Week.md from the Captive folder and parses it into structured data for the weekly review process.

## Prerequisites

This sub-skill expects `$VAULT` to be set by the calling skill (via `get-config`).

## File Location

- **Week.md:** `$VAULT/00_Brain/Captive/Week.md`

## Execution Steps

### 1. Check File Existence

Verify Week.md exists:

```bash
ls -la "$VAULT/00_Brain/Captive/Week.md"
```

If missing, return error result.

### 2. Read Week.md

Read the full content of Week.md.

### 3. Parse Frontmatter

Extract YAML frontmatter fields:
- `week` - ISO week (YYYY-Www)
- `dates` - Date range (YYYY-MM-DD to YYYY-MM-DD)
- `month` - Month (YYYY-MM)
- `quarter` - Quarter (YYYY-QN)
- `year` - Year (YYYY)
- `archived` - (optional) If present, week already archived

### 4. Parse Sections

Extract each section by heading:

**Context From Above:**
- `month_theme` - From Month.md
- `month_outcomes` - From Month.md
- `quarter_theme` - From Quarter.md

**Week Overview:**
- `key_outcomes[]` - The 3 key outcomes for the week
- `focus_theme` - The week's focus theme

**Daily Notes:**
- `daily_notes{}` - Map of day name to content (Monday, Tuesday, etc.)

**Coaching Check-in:**
- `patterns_reflection` - User's reflection on patterns
- `best_self_vision` - Vision for operating at best

**Carry Forward:**
- `carry_forward[]` - Items marked for next week

**Wins This Week:**
- `wins.personal[]` - Personal wins
- `wins.organisational[]` - Team/org wins
- `wins.strategic[]` - Strategic/project wins

**Reflections:**
- `reflections.what_went_well[]` - What worked
- `reflections.what_could_be_better[]` - What to improve
- `reflections.key_learning` - Key learning
- `reflections.patterns_observed` - Patterns noted

### 5. Assess Completeness

Determine which sections have meaningful content vs. just prompts:

- `wins_filled`: true if any wins subsection has content beyond prompts
- `reflections_filled`: true if any reflections subsection has content
- `coaching_filled`: true if coaching check-in has meaningful responses
- `daily_notes_count`: number of days with actual content

Prompts are identified by:
- Starting with `*` (italic)
- Starting with `[` (placeholder)
- Being empty or containing only `-`

### 6. Extract Entities

Scan all content for wikilinks and extract:

- `people[]` - `[[PersonName]]` references
- `projects[]` - `[[project-name]]` references
- `areas[]` - `[[area-name]]` references

### 7. Return Structured Result

**Success:**
```json
{
  "success": true,
  "path": "/path/to/vault/00_Brain/Captive/Week.md",
  "frontmatter": {
    "week": "2026-W07",
    "dates": "2026-02-09 to 2026-02-15",
    "month": "2026-02",
    "quarter": "2026-Q1",
    "year": "2026"
  },
  "sections": {
    "context_from_above": {
      "month_theme": "Execution focus",
      "month_outcomes": ["Ship platform", "Hire 2 engineers"],
      "quarter_theme": "Platform launch"
    },
    "key_outcomes": [
      "Personal habit: Morning focus blocks",
      "Org conversation: Team structure",
      "Strategic: API design complete"
    ],
    "focus_theme": "Delivery mode",
    "daily_notes": {
      "Monday": { "content": "Heavy meetings, good 1:1s", "has_content": true },
      "Tuesday": { "content": "Deep work day", "has_content": true },
      "Wednesday": { "content": "", "has_content": false },
      "Thursday": { "content": "", "has_content": false },
      "Friday": { "content": "", "has_content": false }
    },
    "coaching_checkin": {
      "patterns_reflection": "Noticed overcommitting...",
      "best_self_vision": "Clear boundaries, present..."
    },
    "carry_forward": ["Review budget", "Sarah follow-up"],
    "wins": {
      "personal": ["Protected morning focus"],
      "organisational": ["Team shipped feature X"],
      "strategic": ["[[platform-migration]]: API milestone reached"]
    },
    "reflections": {
      "what_went_well": ["Morning routine paying off"],
      "what_could_be_better": ["Too many context switches"],
      "key_learning": "Delegation creates capacity",
      "patterns_observed": "Energy dips on heavy meeting days"
    }
  },
  "completeness": {
    "wins_filled": true,
    "reflections_filled": true,
    "coaching_filled": true,
    "daily_notes_count": 2
  },
  "entities": {
    "people": ["[[SarahK]]", "[[MarcusT]]"],
    "projects": ["[[platform-migration]]", "[[q2-roadmap]]"],
    "areas": ["[[engineering]]"]
  }
}
```

**File Not Found:**
```json
{
  "success": false,
  "error": "file_not_found",
  "message": "Week.md not found at $VAULT/00_Brain/Captive/Week.md",
  "suggestion": "Run `/weekly-planning` to create a weekly plan first."
}
```

**Already Archived:**
```json
{
  "success": false,
  "error": "already_archived",
  "message": "Week.md shows archived marker. The week has already been reviewed.",
  "archived_week": "2026-W07",
  "suggestion": "Check Periodic/Weekly/2026-W07.md for the archive."
}
```

For backwards compatibility, also output human-readable summary:
```
Week.md loaded for 2026-W07 (2026-02-09 to 2026-02-15)

Focus Theme: Delivery mode
Key Outcomes: 3 defined
Daily Notes: 2/5 days with content

Completeness: wins=filled, reflections=filled, coaching=filled

Entities found:
- People: SarahK, MarcusT
- Projects: platform-migration, q2-roadmap
```
