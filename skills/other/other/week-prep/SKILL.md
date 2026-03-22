---
name: week-prep
description: Generate a briefing with calendar, tasks, and attention flags. Use for "week prep", "briefing", or "what's on this week".
allowed-tools: Read, Glob, Grep, Bash, mcp__gworkspace-mcp__calendar_events, mcp__playground-slack-mcp__get_messages, mcp__qmd__search, mcp__qmd__deep_search
---

# Week Prep

Generate a briefing for the current week with calendar overview, carry-forward items, due tasks, and projects needing attention.

## Related Skills

- `/monday`: Combined Monday flow (creates folder + briefing in one pass). **Recommended for Mondays.**
- `/week-prep`: This skill. Generates briefing only (read-only, can run any day).

This skill assumes the week folder already exists. If it doesn't, suggest running `/monday` first.

## Steps

1. **Determine current week:**
   - Calculate ISO week number and date range (Mon-Fri)
   - Find current week folder: `YYYY/w##-mm-dd/`
   - If folder doesn't exist, prompt to run `/monday` first

2. **Pull calendar events:**
   - Use `mcp__gworkspace-mcp__calendar_events`
   - Time range: Monday 00:00 to Friday 23:59 of current week
   - Include attendees for context
   - Group by day for display

3. **Find carry-forward items:**
   - Locate previous week's report
   - Read "Carry Forward" section
   - Also check current week's report for existing carry-forward

4. **Scan for due tasks:**
   - Grep for Tasks emoji `📅 YYYY-MM-DD` in these locations only:
     - `projects/` folder
     - Current week folder (`YYYY/w##-mm-dd/`)
     - Previous week folder
   - Filter to dates within current week (Mon-Sun)
   - Include file path for context

5. **Check projects needing attention:**
   - Read `projects/index.md` (contains summary of project health)
   - Only read individual project files if flagged as overdue or blocked
   - Flag projects where `next_review` is:
     - Past (overdue)
     - This week (due soon)
   - Also flag projects with `status: blocked`
   <!-- TODO: customize - Adjust project index path if your vault uses a different structure -->

6. **Semantic context for calendar (qmd):**
   - For each meeting with a person, use `qmd_search` MCP tool: query "[person name]", limit 3
   - This surfaces recent context to prep for meetings
   - Focus on people you're meeting this week

7. **Check Slack activity (optional):**
   - Use `mcp__playground-slack-mcp__get_messages`
   - Action: `my_messages`, last 24-48 hours
   - Flag items that may need response
   - Skip if Slack MCP is unavailable

8. **Identify deep work windows:**
   - Analyze calendar for gaps
   - Find blocks of 2+ hours without meetings
   - Suggest these as focus time

9. **Output the briefing:**
   - Display all sections in scannable format
   - Do not write to files (this is a read-only briefing)

## qmd Tools

Use these MCP tools for semantic context (preferred over Bash):

- **`qmd_search`**: query "[person]", limit 5 (find recent notes about a person)
- **`qmd_deep_search`**: query "blocked waiting on open items", limit 5 (find open items)

Bash fallback (if MCP unavailable):
```bash
source ~/.zshrc && qmd search "[person]" -n 5 --md
source ~/.zshrc && qmd query "blocked waiting on open items" -n 5 --md
```

## Output Format

```markdown
## Week Prep: W## (Mon [date] - Fri [date])

### Calendar at a Glance

| Day | Events |
|-----|--------|
| Mon | [Event 1] (10am), [Event 2] (2pm) |
| Tue | [Event] (11am) |
| Wed | No meetings |
| Thu | [Event 1] (9am), [Event 2] (3pm) |
| Fri | [Event] (10am) |

### Carry Forward

From last week's report:
- [ ] Item 1 📅 [date]
- [ ] Item 2

### Tasks Due This Week

- [ ] Task from [[project]] 📅 [date] (in `file.md`)
- [ ] Task 📅 [date]

### Projects Needing Attention

- **[[project-name]]**: Review overdue by [X] days
- **[[project-name]]**: Status is `blocked`

### Deep Work Windows

Based on your calendar, you have focus time available:
- **Mon**: 8-10am (before first meeting)
- **Wed**: All day (no meetings scheduled)
- **Fri**: 1-5pm (afternoon clear)

### Slack Check

- [X] mentions in last 24h
- Notable: [brief summary if anything urgent]
```

## Notes

- This is a **read-only** skill: it outputs a briefing but does not modify files
- Calendar uses natural language dates for the MCP tool (not ISO timestamps, which fail silently)
- If calendar or Slack MCPs fail, skip those sections gracefully and note the skip
- Keep the briefing scannable: prioritize structure over prose
- Flag anything that looks urgent or overdue

## Session Context Hint

If you just ran `/monday` in this same conversation, reuse the previous week's report content from that execution rather than re-reading it. The carry-forward items were already extracted.
