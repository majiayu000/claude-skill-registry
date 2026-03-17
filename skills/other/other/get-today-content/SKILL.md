---
name: get-today-content
description: Read and parse Today.md content for daily review. Returns structured data including frontmatter, sections, completeness assessment, and extracted entities.
disable-model-invocation: true
allowed-tools: Read, Bash(ls)
---

# Get Today Content Sub-Skill

Reads Today.md from the Captive folder and parses it into structured data for the daily review process.

## Prerequisites

This sub-skill expects `$VAULT` to be set by the calling skill (via `get-config`).

## File Location

- **Today.md:** `$VAULT/00_Brain/Captive/Today.md`

## Execution Steps

### 1. Check File Existence

Verify Today.md exists:

```bash
ls -la "$VAULT/00_Brain/Captive/Today.md"
```

If missing, return error result.

### 2. Read Today.md

Read the full content of Today.md.

### 3. Parse Frontmatter

Extract YAML frontmatter fields:
- `date` - Target date (YYYY-MM-DD)
- `day` - Day of week
- `week` - ISO week (YYYY-Www)
- `month` - Month (YYYY-MM)
- `quarter` - Quarter (YYYY-QN)
- `energy` - Energy level (High/Medium/Low)
- `location` - Work location
- `focus_hours` - Available focus hours
- `meetings` - Number of meetings

### 4. Parse Sections

Extract each section by heading:

**Focus Section:**
- `priorities[]` - The 3 top priorities (including completion status if marked)
- `leadership_intention` - The chosen intention for the day

**Meetings Section:**
- `meetings[]` - Array of meeting blocks with:
  - `title` - Meeting name
  - `type` - "1:1" or "group" or "interview"
  - `person` - For 1:1s, the person's wikilink
  - `content` - Full meeting notes content

**Capture Section:**
- `captures[]` - Items dumped during the day (links, notes, ideas)

**Wins Section:**
- `wins.personal` - Personal wins content
- `wins.organisational` - Team/org wins content
- `wins.strategic` - Strategic/project wins content

**Insights Section:**
- `insights.what_went_well` - Content
- `insights.what_could_be_better` - Content
- `insights.key_insight` - Content

**Carry Forward Section:**
- `carry_forward[]` - Items marked for tomorrow

### 5. Assess Completeness

Determine which sections have meaningful content vs. just prompts:

- `wins_filled`: true if any wins subsection has content beyond prompts
- `insights_filled`: true if any insights subsection has content beyond prompts
- `priorities_status`: "complete" / "partial" / "empty" based on check marks

Prompts are identified by:
- Starting with `*` (italic)
- Containing question marks
- Being placeholder text like `[content]`

### 6. Extract Entities

Scan all content for wikilinks and extract:

- `people[]` - `[[PersonName]]` references (from meetings, wins, etc.)
- `projects[]` - `[[project-name]]` references
- `areas[]` - `[[area-name]]` references
- `resources[]` - External links captured

### 7. Return Structured Result

**Success:**
```json
{
  "success": true,
  "path": "/path/to/vault/00_Brain/Captive/Today.md",
  "frontmatter": {
    "date": "2026-02-14",
    "day": "Friday",
    "week": "2026-W07",
    "month": "2026-02",
    "quarter": "2026-Q1",
    "energy": "High",
    "location": "Office",
    "focus_hours": 4,
    "meetings": 3
  },
  "sections": {
    "priorities": [
      { "text": "Complete API design", "status": "completed" },
      { "text": "Review PRs", "status": "partial" },
      { "text": "Plan Q2 roadmap", "status": "not_started" }
    ],
    "leadership_intention": "Focused",
    "meetings": [
      { "title": "Sarah K", "type": "1:1", "person": "[[SarahK]]", "content": "..." },
      { "title": "Platform Sync", "type": "group", "content": "..." }
    ],
    "captures": [
      { "type": "link", "content": "https://..." },
      { "type": "note", "content": "Idea about..." }
    ],
    "wins": {
      "personal": "Kept boundaries...",
      "organisational": "Marcus shipped...",
      "strategic": "[[platform-migration]]: API finalized"
    },
    "insights": {
      "what_went_well": "Morning focus block...",
      "what_could_be_better": "Too many context switches...",
      "key_insight": "Realized that..."
    },
    "carry_forward": ["[ ] Follow up with Sarah", "[ ] Review budget"]
  },
  "completeness": {
    "wins_filled": true,
    "insights_filled": true,
    "priorities_status": "partial"
  },
  "entities": {
    "people": ["[[SarahK]]", "[[MarcusT]]"],
    "projects": ["[[platform-migration]]", "[[q2-roadmap]]"],
    "areas": ["[[engineering]]"],
    "resources": ["https://example.com/article"]
  }
}
```

**File Not Found:**
```json
{
  "success": false,
  "error": "file_not_found",
  "message": "Today.md not found at $VAULT/00_Brain/Captive/Today.md",
  "suggestion": "Run `/daily-planning` to create a daily plan first."
}
```

**Already Archived:**
```json
{
  "success": false,
  "error": "already_archived",
  "message": "Today.md shows archived marker. The day has already been reviewed.",
  "archived_date": "2026-02-14",
  "suggestion": "Check Periodic/Daily/2026-02-14.md for the archive."
}
```

For backwards compatibility, also output human-readable summary:
```
Today.md loaded for 2026-02-14 (Friday)

Energy: High | Location: Office | Focus Hours: 4 | Meetings: 3

Priorities:
1. [x] Complete API design
2. [~] Review PRs
3. [ ] Plan Q2 roadmap

Completeness: wins=filled, insights=filled

Entities found:
- People: SarahK, MarcusT
- Projects: platform-migration, q2-roadmap
```
