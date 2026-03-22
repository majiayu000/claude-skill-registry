---
name: 1-1-prep
description: Prepare for a 1:1 meeting with context from person file, meeting history, and shared projects
allowed-tools: Read, Glob, Grep, Bash, mcp__gworkspace-mcp__calendar_events, mcp__playground-slack-mcp__get_messages, mcp__qmd__search, mcp__qmd__deep_search, mcp__qmd__vector_search
---

# 1:1 Prep

Generate a briefing for an upcoming 1:1 meeting with cross-file context synthesis.

## Arguments

- Person name: The person you're meeting with (e.g., "jane", "alex")
- No argument: Check calendar for next 1:1 and prep for that

## Steps

1. **Identify the person:**
   - If name provided, search `people/*.md` for match
   - If no argument, check calendar for next meeting with a single external attendee
   - Read the person file for context

2. **Pull person context:**
   - Role, team, reporting chain
   - Working style notes (if captured)
   - Last interaction date
   - Any notes from previous 1:1s

3. **Semantic search for person context (qmd):**
   - Use `qmd_deep_search` MCP tool: query "discussions with [name] about projects decisions feedback", limit 10
   - This finds notes mentioning the person even without explicit links
   - Look for implicit mentions, topics discussed, decisions made together

4. **Check recent Slack context:**
   - Read person file for `slack:` handle in frontmatter
   - If handle exists, use `mcp__playground-slack-mcp__get_messages` with action: `search`
   - Query: `from:@[slack-handle]` or `to:@[slack-handle]` (last 14 days)
   - Extract: Recent DM topics, @mentions involving them, threads you both participated in
   - Skip gracefully if Slack MCP unavailable or no handle

5. **Find meeting history:**
   - Glob `*/*/meeting-*-[name].md` for past meetings
   - Read last 3-5 meetings with this person
   - Extract: key topics, decisions made, action items (completed and open)

6. **Check shared projects:**
   - Read frontmatter of project files
   - Find projects where person is listed as contributor/lead
   - Note project status and any blockers

7. **Check for open items:**
   - Grep for person's name in recent weekly reports
   - Find any `- [ ]` items assigned to them or waiting on them
   - Note items from previous meetings marked incomplete

8. **Check calendar context:**
   - Use `mcp__gworkspace-mcp__calendar_events` to find the upcoming meeting
   - Note time, duration, any agenda in description

9. **Generate prep briefing:**
   - Output structured prep doc
   - Do not write to file (this is a read-only briefing)

## qmd Tools

Use these MCP tools for semantic search (preferred over Bash):

- **`qmd_deep_search`**: query "conversations with [name]", limit 10 (hybrid: best quality)
- **`qmd_deep_search`**: query "[name] feedback decisions reviews", limit 5
- **`qmd_search`**: query "[name]", limit 10 (fast keyword search for exact mentions)

Bash fallback (if MCP unavailable):
```bash
source ~/.zshrc && qmd query "conversations with [name]" -n 10 --md
source ~/.zshrc && qmd search "[name]" -n 10 --md
```

## Output Format

```markdown
## 1:1 Prep: [Name]

**Meeting:** [Day, Date] at [Time] ([duration])
**Role:** [Title] on [Team]
**Last 1:1:** [Date] ([X days/weeks ago])

### About [Name]

[2-3 sentences from person file: role context, working style, current focus]

### Recent Slack

**Last message:** [Date] - [Topic/context]
**Notable threads:**
- #[channel]: [Topic] ([date])
- DM: [Topic] ([date])

_Skip this section if no Slack handle or MCP unavailable._

### Previous Meeting Recap

**[Date]**: [Topic summary]
- Decision: [key decision]
- Action: [action item status]

**[Date]**: [Topic summary]
- ...

### Open Items

Items waiting on [Name]:
- [ ] [Item] (from [date/source])

Items you owe [Name]:
- [ ] [Item] (from [date/source])

### Shared Projects

| Project | Status | [Name]'s Role | Notes |
|---------|--------|---------------|-------|
| [[project]] | active | contributor | [brief note] |

### Suggested Topics

Based on history and open items:
1. Follow up on [open item from last meeting]
2. [Project] status check
3. [Any blocked item involving them]
```

## Notes

- Focus on actionable context, not exhaustive history
- Highlight anything overdue or potentially awkward
- If person file is sparse, note that as "Consider updating [[person-name]] after this meeting"
- Keep output scannable: this is pre-meeting prep, not a research paper
- If no meeting history exists, note this is a first/early 1:1

## Person File Schema

<!-- TODO: customize - Adjust frontmatter fields to match your person files -->

Person files live in `people/` with this frontmatter:

```yaml
---
type: person
name: First Last
role: Job Title
team: Team Name
slack: slack-handle
last_updated: YYYY-MM-DD
---
```
