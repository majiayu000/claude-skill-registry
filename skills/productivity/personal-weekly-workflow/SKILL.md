---
name: personal-weekly-workflow
description: Manage weekly PM workflows, meeting notes, and action items for the Orient Task Force. Use this skill when asked about "weekly planning", "meeting notes", "action items", "sprint health", "weekly summary", or workflow automation. Covers Monday planning, Wednesday health checks, Friday summaries, meeting note templates, action item format, and JIRA synchronization.
---

# Workflow Management for Orient PM

## Directory Structure

```
meetings/              # Meeting notes
├── weekly/           # Weekly team meetings
├── planning/         # Sprint planning
├── retrospectives/   # Sprint retrospectives
├── 1-on-1/          # One-on-one meetings
├── ad-hoc/          # Ad-hoc meetings
└── templates/       # Meeting templates

workflow/             # Weekly workflow
├── weekly-reviews/  # Weekly planning docs
├── sprint-health/   # Mid-sprint health checks
└── weekly-summaries/# End-of-week summaries
```

## Weekly Rhythm

### Monday - Start Week
```bash
npm run workflow:start-week
```
- Fetches current JIRA state
- Lists blockers and in-progress items
- Creates planning doc

### Wednesday - Mid-Sprint Check
```bash
npm run workflow:mid-sprint
```
- Calculates burndown
- Identifies at-risk items
- Updates health status

### Friday - End Week
```bash
npm run workflow:end-week
npm run update-presentation
```
- Lists completed work
- Calculates velocity
- Updates rolling presentation

## Meeting Notes

### Create Meeting Note
```bash
npm run meeting:new [type] "[title]"
```

Types: `weekly`, `planning`, `retrospective`, `1-on-1`, `ad-hoc`

### Action Item Format
```markdown
- [ ] @username: Description [Task] [Priority: High] #YOUR_PROJECT-123
```

Components:
- `[ ]` = Open, `[x]` = Completed
- `@username` = Assignee (match JIRA user)
- `[Task]` / `[Story]` / `[Bug]` = Issue type
- `[Priority: High]` = Priority level
- `#YOUR_PROJECT-XXX` = Existing JIRA issue (optional)

### Sync Action Items to JIRA
```bash
npm run meeting:sync <file>
```

### List All Action Items
```bash
npm run meeting:list
npm run meeting:report
```

## CLI Commands Quick Reference

```bash
# Meetings
npm run meeting:new [type] "[title]"    # Create meeting note
npm run meeting:sync <file>              # Sync action items to JIRA
npm run meeting:list                     # List all action items
npm run meeting:report                   # Generate report

# Workflow
npm run workflow:start-week              # Monday planning
npm run workflow:mid-sprint              # Wednesday check
npm run workflow:end-week                # Friday summary

# Presentation
npm run update-presentation              # Update rolling deck
```

## Day-Specific Suggestions

### Monday Morning
1. Create weekly planning doc
2. Review last week's summary
3. Check for blockers and SLA breaches
4. List open action items from meetings

### Wednesday
1. Generate sprint health check
2. Show current blockers
3. Check SLA breaches

### Friday Afternoon
1. Generate weekly summary
2. Update rolling presentation
3. Create action items report
4. Preview next week's priorities

## Finding Action Items

**Find all open action items:**
```
Search: "- [ ]" in meetings/
```

**Find your action items:**
```
Search: "@yourusername" and "- [ ]"
```

**Find high priority items:**
```
Search: "[Priority: High]" and "- [ ]"
```

**Find unlinked items (no JIRA):**
```
Search: "- [ ]" NOT "#YOUR_PROJECT"
```

## Meeting → JIRA Flow

1. **During meeting:** Take notes in meeting template
2. **Action items:** Add with format above
3. **Post-meeting:** `npm run meeting:sync <file>`
4. **Result:** JIRA issues created, meeting updated with keys

## Context Awareness

### By Day
- Monday: Focus on planning
- Tuesday-Thursday: Execution, track blockers
- Friday: Summary and wrap-up

### By Sprint Phase
- Sprint start: Planning mode
- Mid-sprint: Execution, health checks
- Sprint end: Retrospective, summary mode

### By Role
- PM: Metrics, reporting, stakeholder updates
- Team member: Action items, blockers
- Stakeholder: Summaries, high-level status
