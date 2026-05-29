---
name: monday
description: Full Monday morning setup. Creates week folder, pulls carry-forward, and generates briefing in one pass. Use on Monday mornings or when the user says "monday", "start my week", or "monday morning".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__gworkspace-mcp__calendar_events, mcp__playground-slack-mcp__get_messages
---

# Monday Morning

Combined flow for starting the week. Creates the week folder (if needed), pulls carry-forward, and generates a briefing in one pass.

## When to Use

- Monday mornings (primary use case)
- Any time you need both folder setup and briefing
- If folder already exists, skips creation and just generates briefing

For folder-only setup: use `/new-week`
For briefing-only (mid-week): use `/week-prep`

## Steps

### 1. Calculate week info

From today's date, determine:
- ISO week number
- Monday's date for folder name (format: `mm-dd`)
- Date range for report title (e.g., "Jan 6 - Jan 10")
- Previous week's folder path

### 2. Check if week folder exists

- Look for `YYYY/w##-mm-dd/`
- If exists: note "Week folder already exists, skipping creation"
- If not: create the folder

### 3. Read previous week's report (ONCE)

This is the efficiency gain: read it once, extract everything needed.

- Find previous week's report in `YYYY/w##-mm-dd/weekly-report-*.md`
- Extract:
  - Unchecked items from "Carry Forward" section
  - Unchecked items from "Time Blocks" section
  - Projects mentioned in frontmatter `projects` field
- Store these for use in steps 4 and 7

### 4. Create weekly report (if folder was new)

Use this structure, pre-populating carry-forward from step 3:

```markdown
---
type: weekly
week: w##
projects: [from previous week]
---
# W##: Date Range

## Tasks Due This Week

```tasks
not done
due after YYYY-MM-DD (Sunday before week starts)
due before YYYY-MM-DD (Saturday after week ends)
short mode
```

## Time Blocks
_One deep work block per day. That's the win._

### Mon
- [ ]

### Tue
- [ ]

### Wed
- [ ]

### Thu
- [ ]

### Fri
- [ ]

---

## Focus
-

## Log
-

## Decisions Made
| Decision | Project | Rationale |
|----------|---------|-----------|

## Friday Wrap-Up
<!-- Auto-populated by /friday skill. Everything below this heading is generated. -->

### Wins
-

### Blockers
-

### Slack Decisions
| Date | Channel | Decision | Logged? |
|------|---------|----------|---------|

### Carry Forward
[items from previous week's carry-forward and incomplete time blocks]
```

<!-- TODO: customize - Adjust sections to match your weekly report template -->

### 5. Pull calendar for the week

- Use `mcp__gworkspace-mcp__calendar_events`
- Time range: Monday through Friday (natural language dates)
- Group by day
- Note meeting-free blocks of 2+ hours for deep work windows

### 6. Check project health (efficient pattern)

Instead of reading all project files:
1. Read `projects/index.md` first (contains summary of project status)
2. Only read individual project files if they appear overdue or blocked in the index
3. Flag projects where `next_review` is past or this week

<!-- TODO: customize - Adjust project index path if your vault uses a different structure -->

### 7. Check Slack (optional)

- Use `mcp__playground-slack-mcp__get_messages` with action: `my_messages`
- Last 48 hours
- Flag items needing response
- Skip gracefully if MCP unavailable

### 8. Output the briefing

Combine all gathered context into one scannable output:

```markdown
## Monday Setup Complete

**Week folder:** `YYYY/w##-mm-dd/` [created / already existed]
**Weekly report:** [created with X carry-forward items / already existed]

---

## Week Prep: W## (Mon [date] - Fri [date])

### Calendar at a Glance

| Day | Events |
|-----|--------|
| Mon | [events] |
| Tue | [events] |
| Wed | [events] |
| Thu | [events] |
| Fri | [events] |

### Deep Work Windows

Based on your calendar:
- **[Day]**: [time range] ([duration])

### Carry Forward

From last week:
- [ ] Item 1
- [ ] Item 2

### Projects Needing Attention

- **[[project]]**: Review overdue by X days
- **[[project]]**: Status is `blocked`

### Slack Check

- X mentions in last 48h
- [Notable items if any]
```

## Notes

- Calendar uses natural language dates: "Monday January 13 12:00am" (not ISO timestamps, which fail silently)
- If calendar or Slack MCPs fail, skip those sections and note the skip
- Keep output scannable: structure over prose
- The weekly report is the only file written; briefing is output only
- Tasks query date math: `due after` Sunday, `due before` Saturday (captures Mon-Fri)
