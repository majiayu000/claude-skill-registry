---
name: gather-week-context
description: Collect and synthesize all daily archives for a given week. Returns aggregated data including wins, insights, people interactions, and completeness status.
disable-model-invocation: true
allowed-tools: Read, Bash(ls, date)
---

# Gather Week Context Sub-Skill

Collects all daily archives for a specified week and synthesizes them into structured data for weekly review.

## Input Arguments

Arguments are passed as key-value pairs:
- `vault`: Path to the vault
- `week`: Target week in YYYY-Www format
- `week_start`: First day of week (YYYY-MM-DD, Monday)
- `week_end`: Last day of week (YYYY-MM-DD, Sunday)

## Instructions

### 1. Determine Workdays

Calculate all workdays (Monday-Friday) for the target week using the `week_start` date:

```bash
# week_start is always Monday
# Calculate: Monday, Tuesday, Wednesday, Thursday, Friday
# week_start + 0, +1, +2, +3, +4 days
```

### 2. Check Daily Archive Existence

For each workday, check if archive exists:

```bash
ls "$VAULT/00_Brain/Periodic/Daily/{date}.md" 2>/dev/null
```

Track:
- `existing_archives[]` - Dates with archives
- `missing_days[]` - Dates without archives (format: "YYYY-MM-DD (DayName)")

### 3. Read Each Daily Archive

For each existing archive, read and parse:

**Frontmatter:**
- `date` - The archive date
- `day` - Day of week
- `energy` - Energy level (High/Medium/Low)
- `location` - Work location
- `focus_hours` - Hours of focused work
- `meetings` - Number of meetings

**Sections:**
- `priorities[]` - The 3 priorities with completion status
- `leadership_intention` - The intention for the day
- `meetings[]` - Meeting blocks (extract person from 1:1s)
- `wins` - Personal, organisational, strategic subsections
- `insights` - what_went_well, what_could_be_better, key_insight
- `carry_forward[]` - Items marked for next day

### 4. Aggregate Data

Compile across all daily archives:

**Metrics:**
- `total_meetings`: Sum of all meeting counts
- `total_focus_hours`: Sum of all focus hours
- `avg_energy`: Average energy level (High=3, Medium=2, Low=1)
- `energy_trend`: "increasing", "stable", or "decreasing" based on Mon→Fri
- `priority_completion_rate`: Percentage of priorities marked complete

**Collections:**
- `wins.personal[]`: All personal wins with dates
- `wins.organisational[]`: All org wins with dates
- `wins.strategic[]`: All strategic wins with dates
- `insights[]`: All key insights with dates
- `what_went_well[]`: All positive patterns with dates
- `what_could_be_better[]`: All friction points with dates
- `carry_forward[]`: All incomplete items from final day

**Entity Aggregates:**
- `unique_people[]`: All `[[PersonName]]` references with interaction counts
- `unique_projects[]`: All `[[project-name]]` references with mention counts
- `leadership_intentions[]`: All daily intentions with dates

**People Interactions:**
For each unique person, compile:
- `interaction_count`: How many days they appeared
- `topics`: Extracted from meeting notes and wins
- `notable_moment`: Most significant interaction (from wins/insights)

### 5. Generate Daily Links

Create wikilinks to each daily archive for the weekly archive:

```markdown
- [[00_Brain/Periodic/Daily/2026-02-09|Monday]] - [One-line summary from day]
- [[00_Brain/Periodic/Daily/2026-02-10|Tuesday]] - [One-line summary]
...
```

Use the first line of daily notes or a summary of wins as the one-liner.

### 6. Return Structured Result

**Success (full week):**
```json
{
  "success": true,
  "week": "2026-W07",
  "daily_archives": [
    {
      "date": "2026-02-09",
      "day_name": "Monday",
      "exists": true,
      "path": "/path/to/.../Periodic/Daily/2026-02-09.md",
      "energy": "High",
      "meeting_count": 5,
      "focus_hours": 3,
      "priority_completion": "2/3",
      "leadership_intention": "Focused",
      "wins_count": 4,
      "key_insight": "Delegation creates capacity",
      "themes": ["delegation", "team growth"]
    },
    {
      "date": "2026-02-10",
      "day_name": "Tuesday",
      "exists": true,
      "path": "/path/to/.../Periodic/Daily/2026-02-10.md",
      "energy": "Medium",
      "meeting_count": 3,
      "focus_hours": 5,
      "priority_completion": "3/3",
      "leadership_intention": "Supportive",
      "wins_count": 3,
      "key_insight": "Deep work compounds",
      "themes": ["focus", "execution"]
    }
  ],
  "missing_days": [],
  "aggregates": {
    "total_meetings": 18,
    "total_focus_hours": 15,
    "avg_energy": 2.4,
    "energy_trend": "stable",
    "priority_completion_rate": 73,
    "unique_people": [
      { "name": "[[SarahK]]", "interaction_count": 3 },
      { "name": "[[MarcusT]]", "interaction_count": 2 }
    ],
    "unique_projects": [
      { "name": "[[platform-migration]]", "mention_count": 5 },
      { "name": "[[q2-roadmap]]", "mention_count": 2 }
    ],
    "leadership_intentions": [
      { "date": "2026-02-09", "intention": "Focused" },
      { "date": "2026-02-10", "intention": "Supportive" }
    ]
  },
  "wins": {
    "personal": [
      { "date": "2026-02-09", "content": "Protected morning focus" },
      { "date": "2026-02-10", "content": "Set clear boundary on late meeting" }
    ],
    "organisational": [
      { "date": "2026-02-09", "content": "Team shipped feature X" }
    ],
    "strategic": [
      { "date": "2026-02-09", "content": "[[platform-migration]]: API design complete" },
      { "date": "2026-02-10", "content": "[[platform-migration]]: Integration tests passing" }
    ]
  },
  "insights": [
    { "date": "2026-02-09", "key_insight": "Delegation creates capacity" },
    { "date": "2026-02-10", "key_insight": "Deep work compounds" }
  ],
  "what_went_well": [
    { "date": "2026-02-09", "content": "Morning routine paying off" },
    { "date": "2026-02-10", "content": "No interruptions during focus block" }
  ],
  "what_could_be_better": [
    { "date": "2026-02-09", "content": "Too many context switches" }
  ],
  "people_interactions": [
    {
      "person": "[[SarahK]]",
      "interaction_count": 3,
      "dates": ["2026-02-09", "2026-02-10", "2026-02-12"],
      "topics": ["career growth", "tech lead path", "Q2 planning"],
      "notable_moment": "Great discussion about leadership aspirations"
    },
    {
      "person": "[[MarcusT]]",
      "interaction_count": 2,
      "dates": ["2026-02-09", "2026-02-11"],
      "topics": ["platform migration", "API design"],
      "notable_moment": "Shipped API milestone together"
    }
  ],
  "carry_forward": [
    { "source_date": "2026-02-13", "item": "Review budget" },
    { "source_date": "2026-02-13", "item": "Follow up with Sarah on tech lead timeline" }
  ],
  "daily_links": "- [[00_Brain/Periodic/Daily/2026-02-09|Monday]] - Heavy meetings, good energy, API design work\n- [[00_Brain/Periodic/Daily/2026-02-10|Tuesday]] - Deep work day, integration tests passing\n- [[00_Brain/Periodic/Daily/2026-02-11|Wednesday]] - Mixed day, platform sync\n- [[00_Brain/Periodic/Daily/2026-02-12|Thursday]] - Career conversations, planning\n- [[00_Brain/Periodic/Daily/2026-02-13|Friday]] - Wrap up, reflection time"
}
```

**Success (partial week):**
```json
{
  "success": true,
  "partial": true,
  "week": "2026-W07",
  "daily_archives": [...],
  "missing_days": ["2026-02-11 (Wednesday)", "2026-02-13 (Friday)"],
  "message": "3 of 5 workdays archived. Proceeding with available data.",
  "aggregates": {...},
  "wins": {...},
  "insights": [...],
  "people_interactions": [...],
  "carry_forward": [...],
  "daily_links": "..."
}
```

**No archives found:**
```json
{
  "success": false,
  "error": "no_archives",
  "week": "2026-W07",
  "missing_days": ["2026-02-09 (Monday)", "2026-02-10 (Tuesday)", "2026-02-11 (Wednesday)", "2026-02-12 (Thursday)", "2026-02-13 (Friday)"],
  "message": "No daily archives found for this week.",
  "suggestion": "Run `/daily-review` for each day, or proceed with Week.md content only."
}
```

For backwards compatibility, also output human-readable summary:
```
Daily Archives for 2026-W07

Found: 5/5 workdays archived

Totals:
- Meetings: 18
- Focus Hours: 15h
- Energy: 2.4 avg (stable)
- Priority Completion: 73%

People: SarahK (3), MarcusT (2)
Projects: platform-migration (5), q2-roadmap (2)

Key Insights:
- Mon: "Delegation creates capacity"
- Tue: "Deep work compounds"
...
```

## Design for Reuse

This sub-skill is designed to be reusable by:
- **weekly-review**: Primary consumer for weekly synthesis
- **monthly-review**: Can call multiple times to gather all weeks in a month
- **quarterly-review**: Can aggregate weekly data for quarterly patterns

The date range inputs allow flexibility for different time periods.
