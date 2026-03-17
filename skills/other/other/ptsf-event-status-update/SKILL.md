---
name: event-status-update-ptsf
description: Generate ProductTank SF event status reports by synthesizing Linear issues, Gmail threads, and past conversations. Use when asked about event status, speaker coordination status, what's happening with an upcoming event, event readiness, or any "what's the status of [event/speaker]" query for ProductTank SF.
---

# Event Status Update Workflow

## Data Sources

| Source | What to Find | How to Access |
|--------|--------------|---------------|
| **Linear** | Issue status, blockers, timelines, checklist progress | `linear-cli i list -t "Product Tank SF"`, `linear-cli i get <ID>`, `linear-cli p get <ID>` |
| **Gmail** | Speaker communications, confirmations, pending replies | `search_gmail_messages` with `q: "from:wmfrederick+producttanksf@gmail.com OR to:wmfrederick+producttanksf@gmail.com [speaker/event name]"` |
| **Speaker Form Results** | Speaker submissions, talk titles, bios, availability | [Speaker Form](https://docs.google.com/spreadsheets/d/1GN2mAqlv_QRdCD4cuIplw_8IbwfjwpdlHTe7CSlcagY/edit?gid=206355470#gid=206355470) — `gdrive:gsheets_read` spreadsheetId: `1GN2mAqlv_QRdCD4cuIplw_8IbwfjwpdlHTe7CSlcagY` |
| **Master Event Spreadsheet** | Event calendar, venue info, budget, sponsor tracking | [Master Events](https://docs.google.com/spreadsheets/d/1RnNx_kF0YsaiG2VlcgMO1oVs56rjKBIxtQKjVsvwq2o/edit?gid=2#gid=2) — `gdrive:gsheets_read` spreadsheetId: `1RnNx_kF0YsaiG2VlcgMO1oVs56rjKBIxtQKjVsvwq2o` |
| **Past Conversations** | Prior context, issue IDs, decisions made | `conversation_search` |

## Process

### 1. Gather Context
- `conversation_search` for event/speaker name to find issue IDs and recent activity
- Note the main coordination issue (e.g., PRO-42)

### 2. Get Linear Details
- `linear-cli p get <PROJECT_ID> --output json` for project description, event date, venue, speaker details
- `linear-cli i get <ISSUE_ID> --output json` for main issue status, timeline, blockers, due dates
- Extract progress from "Event Definition of Done Checklist"

### 3. Check Google Sheets
- **Speaker Form Results** — speaker submissions, proposed talk titles, contact info
- **Master Event Spreadsheet** — event dates, venue details, budget status, sponsor commitments

### 4. Check Recent Communications
- `search_gmail_messages` with `q: "from:wmfrederick+producttanksf@gmail.com OR to:wmfrederick+producttanksf@gmail.com [speaker/event] after:[7-10 days ago]"`
- Note last contact date, what's confirmed vs pending

### 5. Synthesize Using Template Below

## Output Template

```markdown
## Event Status: **[Status]** ([Brief Context])

**Event Date:** [Date, Time]
**Speaker:** [Name] - "[Talk Title]"
**Expected Attendance:** [Number]

### ✅ What's Confirmed:
- [Speaker details, budget, sponsors, locked-in logistics]

### 🔴 What's Blocked:
[Timeline context first (e.g., "30 days behind schedule"), then numbered blockers with issue IDs]

### 📅 Last Communication:
**[Date]**: [Summary]

**Next action needed:** [Specific action with name and deliverable]
```

## Status Labels
- **Confirmed** - All major pieces locked in
- **On Track** - Minor details pending, on schedule
- **At Risk** - Behind schedule but recoverable
- **Blocked** - Cannot proceed without external action
- **On Hold** - Paused pending decision

## Key Principles
- Lead with status assessment, not details
- Include specific dates, names, dollar amounts
- State timeline gaps explicitly (e.g., "30 days behind")
- End with concrete next step (who does what)
- Focus on recent 7-10 days of activity
