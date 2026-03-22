---
name: decision-extractor
description: Scan recent notes for decision language and offer to update project Decision Logs
allowed-tools: Read, Edit, Glob, Grep, mcp__playground-slack-mcp__get_messages
---

# Decision Extractor

Scan recent notes (weekly reports, meetings) for decision language and surface decisions that should be logged in project files.

## Arguments

- Time range (optional): "this week", "last 2 weeks", "this month" (default: last 2 weeks)
- Project filter (optional): Only look for decisions about a specific project
- `--include-slack`: Also scan Slack for decision language (default: vault only)

## Steps

1. **Find files to scan:**
   - Glob recent weekly reports based on time range
   - Glob meeting notes in those week folders
   - If project filter, narrow scope

2. **Scan vault for decision language:**
   Pattern match for phrases indicating decisions:
   - "decided to", "decision:", "the call is"
   - "agreed on", "agreed to", "we'll go with"
   - "chose to", "choosing", "selected"
   - "approved", "signed off on"
   - "not doing", "won't pursue", "deprioritizing"
   - "the plan is", "moving forward with"
   - "resolved to", "committed to"

3. **Scan Slack for decisions (if --include-slack):**
   - Use `mcp__playground-slack-mcp__get_messages` with action: `my_messages`
   - Time range: Match the vault time range argument
   - Search sent messages and @mentions for same decision patterns
   - These are "async decisions" that may not have made it to vault notes
   - Skip gracefully if Slack MCP unavailable

4. **Extract decision context:**
   - The decision itself
   - Date (from file or section)
   - People involved (if mentioned)
   - Project/topic it relates to
   - Rationale (if stated)
   - Source: vault file or Slack (channel + thread link)

5. **Match to projects:**
   - For each decision, identify which project it relates to
   - Check if project has a Decision Log section
   - Check if decision is already logged

6. **Present findings:**
   - Show decisions found
   - Indicate which are already logged vs. new
   - Group by project
   - Mark Slack decisions with source channel

7. **Offer to update:**
   - For new decisions, ask if user wants to add to Decision Log
   - If confirmed, use Edit tool to append to project file

## Output Format

```markdown
## Decisions Found ([time range])

### [[project-1]]

**Already Logged:**
- [Date]: [Decision] ?

**New (not in Decision Log):**
- [Date]: [Decision]
  - Source: `meeting-2025-01-06-person.md`
  - Context: [brief rationale if found]
  - -> Add to Decision Log? [Y/N]

### [[project-2]]

**New:**
- [Date]: [Decision]
  - Source: `weekly-report-w02.md`
  - -> Add to Decision Log? [Y/N]

### Unmatched (no clear project)

- [Date]: [Decision]
  - Source: [file]
  - Possible projects: [[project-a]], [[project-b]]

### From Slack (--include-slack)

- [Date]: [Decision]
  - Source: #[channel] ([thread link])
  - Participants: @person1, @person2
  - -> Add to Decision Log? [Y/N]
```

## Decision Log Format

When adding to project files, use this table format:

```markdown
## Decision Log

| Date | Decision | Context |
|------|----------|---------|
| 2025-01-06 | Chose Figma over Sketch for prototypes | Team familiarity, better collaboration |
| 2025-01-08 | Scoped out mobile for v1 | #proj-channel (Slack) |
```

For Slack decisions, include channel name as context. Link to thread if available.

## Notes

- Don't add duplicates. Check existing Decision Log first.
- If a project doesn't have a Decision Log section, offer to create one
- For decisions that span multiple projects, log in the primary project and note the connection
- "Context" should be brief (one sentence). Link to source file for details.
- Ask before writing. This skill modifies files.
- Some "decisions" are actually action items. Use judgment. Decisions are choices between options; actions are tasks to do.
