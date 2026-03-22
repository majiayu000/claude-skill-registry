---
name: friday
description: End-of-week wrap-up for the weekly report. Use on Fridays, when closing out the week, or when the user says "friday", "week close", or "wrap up week".
allowed-tools: Read, Edit, Glob, Grep, mcp__playground-slack-mcp__get_messages
---

# Friday Wrap-Up

Help complete the weekly report with wins, blockers, and carry-forward items.

## Context: Zone Separation

The weekly report has two zones: **manual** (human-written) and **auto-generated** (skill output). This skill only writes into the auto-generated zone under `## Friday Wrap-Up`. It never touches manual sections (Focus, Log, Decisions Made).

## Steps

1. **Find current week's report** in `YYYY/w##-mm-dd/weekly-report-*.md`

2. **Scan for incomplete tasks**:
   - Check all `- [ ]` items in Time Blocks section
   - Check meeting notes in the week folder for unchecked Next Steps
   - List what's incomplete

3. **Prompt for Wins** (interactive mode):
   - Review the Log section for accomplishments
   - Ask user to confirm or add wins

4. **Prompt for Blockers** (interactive mode):
   - Ask if anything is stuck or waiting on others

5. **Populate Carry Forward**:
   - Move incomplete Time Block items to Carry Forward
   - Add any incomplete meeting action items
   - Use Tasks emoji format for due dates: `📅 YYYY-MM-DD`
   - Ask if anything else should carry over (interactive mode)

6. **Scan Slack for decisions**:
   - Use `mcp__playground-slack-mcp__get_messages` with action: `my_messages`
   - Time range: This week (Monday to Friday)
   - Pattern match for decision language:
     - "decided to", "decision:", "the call is"
     - "agreed on", "agreed to", "we'll go with"
     - "chose to", "choosing", "selected"
     - "approved", "signed off on"
     - "not doing", "won't pursue", "deprioritizing"
     - "the plan is", "moving forward with"
     - "resolved to", "committed to"
   - Present decisions not already in weekly report's Decisions Made table
   - Ask user if any should be logged (interactive mode)
   - Skip gracefully if Slack MCP unavailable

7. **Summarize** the week: wins count, blockers count, items carrying forward.

## Output Format

**All Friday-generated content goes under a single `## Friday Wrap-Up` heading.** This separates auto-generated content from manually written sections. Use `###` subheadings within it.

When updating the report, do NOT write into existing sections like `## Wins` or `## Blockers`. Instead, write under `## Friday Wrap-Up` (before any `## Daily Roundup` sections).

```markdown
## Friday Wrap-Up

### Wins
- Win from this week
- Another win

### Blockers
- Blocker identified
- Another blocker

### Carry Forward

_From W##:_
- [ ] Incomplete item from Time Blocks 📅 2025-01-10
- [ ] Action item from meeting

_From W##:_ (prior weeks, if carrying forward)
- [ ] Older incomplete item

### Slack Decisions
| Date | Channel | Decision | Logged? |
|------|---------|----------|---------|
| M/DD | #channel | Decision summary | ? |
```

### Slack Decisions Prompt (interactive mode)

When Slack decisions are found, prompt user:

```markdown
#### Slack Decisions to Log?

Found decision language in Slack this week:

- **#[channel]** ([date]): "[Decision quote]"
  - Project: [[likely-project]]
  - Add to weekly report? [Y/N]

- **DM with [person]** ([date]): "[Decision quote]"
  - Project: [unclear]
  - Add to weekly report? [Y/N]
```

## Notes

- Don't remove checked items from Time Blocks (they're a record)
- Ask before adding items to Carry Forward when running interactively (user may want to drop them)
- Keep summaries concise: one line per item
- Add `📅` due dates to carried items when there's a clear deadline
- **All output must go under `## Friday Wrap-Up`**. Never write directly into manually curated sections (Focus, Log, Decisions Made)
- When running headlessly (via automation), make best judgment on what to include without prompting
