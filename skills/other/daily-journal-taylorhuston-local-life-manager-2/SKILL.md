---
name: daily-journal
description: Daily journal management for the my-vault Obsidian vault. Use for morning routines, daily reviews, quick journal updates, checking yesterday's entry, or setting today's highlight. Triggers on "good morning", "daily review", "journal", "what did I do", "highlight".
---

# Daily Journal

Manage daily journal entries in the my-vault Obsidian vault.

## Workflows

| Command | Purpose |
|---------|---------|
| `/good-morning` | Morning check-in, review yesterday, set up today |
| `/daily-review` | Evening review, fill in the day's entries |
| `/quick-journal [entry]` | Quick update to today's journal |

## Data

- Journal location: `my-vault/02 Calendar/YYYY-MM-DD.md`
- Template: `my-vault/09 System/Templates/Daily Template.md`
- Structure: See `references/template.md`

## Key Sections

- **Highlight**: Main focus for the day
- **What Did I Do?**: Personal activities (errands, social, health)
- **What Did I Work On?**: Technical work (projects, coding, GitHub)
- **What Did I Study?**: Learning sessions, courses, deliberate study

## GitHub Integration

```bash
gh search commits --author=TaylorHuston --committer-date=YYYY-MM-DD
```

Summarize commits into meaningful bullets.

## Approach

Keep it conversational - ask one thing at a time, don't overwhelm.
