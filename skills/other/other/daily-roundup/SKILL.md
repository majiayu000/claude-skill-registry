---
name: daily-roundup
description: Morning briefing combining email, yesterday's meetings, and Slack into one section appended to the weekly report
allowed-tools: Read,Edit,Write,Glob,Grep,mcp__playground-slack-mcp__get_messages,mcp__gworkspace-mcp__read_mail,mcp__gworkspace-mcp__calendar_events,mcp__gworkspace-mcp__search_drive,mcp__gworkspace-mcp__read_file
---

# Daily Roundup

Generate a combined morning briefing from email, yesterday's meetings, and Slack. Append as a single section to the current week's weekly report.

## Arguments

- None required. Always processes the last 24 hours.

## Steps

### 0. Setup

1. Determine today's date, day of week, and yesterday's date.
2. Find the current week's weekly report: look in the current year folder for the most recent `w##-mm-dd` folder, read the `weekly-report-*.md` file.
3. Check if a `## Daily Roundup: [Today's Day Month Date]` section already exists. If so, you will replace it (idempotent).

### 1. Email (Gmail, last 24h)

1. Use `mcp__gworkspace-mcp__read_mail` with a query to fetch recent messages.
   - Query: `newer_than:1d` to get last 24 hours
   - Set `max_results: 50`, `include_body: true`
2. **Filter out noise:**
   - Skip messages from `noreply@`, `no-reply@`, `notifications@`, `calendar-notification@google.com`
   - Skip Google Calendar invites (subject starts with "Invitation:" or "Updated invitation:")
   - Skip automated newsletters, marketing (look for `unsubscribe` in body as a signal)
   - Skip Jira/GitHub notification emails (automated system notifications)
   <!-- TODO: customize - Add any other automated senders your org uses -->
3. **Categorize remaining emails:**
   - **Needs Response**: Direct questions to you, requests, asks, emails where you're in To (not CC)
   - **Worth Knowing**: Team updates, project threads, decisions being made
   - **FYI**: Announcements, broadcasts, CC'd threads
4. For each email, note: sender, subject, one-line summary, suggested action if applicable.

### 2. Yesterday's Meetings (skip on Mondays)

If today is **Monday**, skip this section entirely. Add a note: "Meetings skipped (Monday). See `/monday` briefing for weekly context."

Otherwise:

1. Use `mcp__gworkspace-mcp__calendar_events` to fetch yesterday's events.
   - Set `time_min` to yesterday 00:00 and `time_max` to yesterday 23:59.
   - Use the primary calendar.
2. For each meeting event:
   - Note: time, title, attendees (first names or short list)
   - Check if a meeting note already exists in the current week folder. Use `Glob` to search for `meeting-[yesterday's date]-*.md` in the week folder.
3. **Check for Gemini transcripts in Google Drive:**
   - Use `mcp__gworkspace-mcp__search_drive` with query: `name contains '[meeting title]' and mimeType contains 'document' and modifiedTime > '[yesterday ISO date]'`
   - Also try: `fullText contains 'transcript' and name contains '[partial meeting title]' and modifiedTime > '[yesterday ISO date]'`
   - If a transcript document is found and no meeting note file exists yet:
     a. Read the transcript with `mcp__gworkspace-mcp__read_file`
     b. Create a meeting note file: `meeting-[YYYY-MM-DD]-[slugified-title].md`
     c. Use this frontmatter:
        ```yaml
        ---
        type: meeting
        date: [YYYY-MM-DD]
        people: []
        projects: []
        tags: []
        ---
        ```
     d. Add a Summary section with key points from the transcript (3-5 bullets)
     e. Add a Next Steps section with action items
     f. Do NOT import the full transcript (leave that for manual review)
     g. Note in the roundup that a meeting note was auto-created
4. For each meeting, produce a brief summary line for the roundup.

### 3. Slack (last 24h)

1. Use `mcp__playground-slack-mcp__get_messages` with action: `my_messages`
   - Set time range to last 24 hours
   - Request count: 100
2. **Categorize:**
   - **Needs Response**: Direct @mentions, questions, requests, DMs needing reply
   - **Worth Knowing**: Thread updates, project decisions, shared context
   - **FYI**: Announcements, links shared, general channel activity
3. Include message snippets, channel names, and suggested actions.

### 4. Consolidate Quick Actions

Across all three sources, collect the top action items into a single checklist. Prioritize:
1. Direct asks/questions waiting for response (from any source)
2. Decisions needing input
3. Items to acknowledge or review

Limit to 5-7 items max. Be specific ("Reply to Jane about project timeline" not "Check email").

### 5. Append to Weekly Report

Construct the full roundup section and append it to the weekly report. If a roundup for today already exists, replace that section.

## Output Format

```markdown
## Daily Roundup: [Day] [Month] [Date]

**Generated:** [YYYY-MM-DD HH:MM]

### Email
**[X] messages scanned, [Y] relevant**

**Needs Response:**
- **[Sender]**: [Subject] - [one-line summary]
  - Action: [specific action]

**Worth Knowing:**
- **[Sender]**: [Subject] - [one-line summary]

**FYI:**
- [Subject] from [Sender] - [brief note]

*[If no relevant emails: "Inbox clear. No action needed."]*

### Yesterday's Meetings
*[If Monday: "Skipped (Monday). See Monday briefing for weekly context."]*

- **[HH:MM] [Meeting Title]** ([Attendee1], [Attendee2])
  - [2-3 line summary or "No transcript available"]
  - [If note created: "Meeting note created: [[meeting-YYYY-MM-DD-slug]]"]

*[If no meetings: "No meetings yesterday."]*

### Slack
**[X] messages scanned**

**Needs Response:**
- **[Person]** in #[channel]: "[snippet]"
  - Action: [specific action]

**Worth Knowing:**
- **[Topic]** in #[channel]: [summary]

**FYI:**
- [summary items]

*[If quiet: "Slack quiet. No action needed."]*

---

**Quick Actions:**
- [ ] [Top consolidated action items from all sources]
```

## Error Handling

- If Gmail MCP is unavailable: skip Email section, add note "Email: skipped (Gmail MCP unavailable)"
- If Calendar MCP is unavailable: skip Meetings section, add note "Meetings: skipped (Calendar MCP unavailable)"
- If Slack MCP is unavailable: skip Slack section, add note "Slack: skipped (Slack MCP unavailable)"
- If Drive search fails when looking for transcripts: note it and continue without transcript
- If weekly report file is not found: create a warning in the log and exit (don't create files in wrong locations)
- Always produce output even if all three sources fail (the section will just note the skips)

## Notes

- On Mondays, skip the meetings section. The `/monday` skill runs earlier and covers Monday context.
- Meeting note auto-creation is lightweight: summary + next steps only. Full transcript import is left to manual review.
- Focus on signal over noise. The goal is a 2-minute scan, not a comprehensive log.
- Email filtering should be aggressive. When in doubt, skip it.
- The idempotent section replacement means you can safely re-run this skill if a data source was temporarily unavailable.
