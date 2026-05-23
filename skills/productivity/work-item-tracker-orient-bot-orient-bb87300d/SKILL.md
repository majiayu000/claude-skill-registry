---
name: work-item
description: Update the current work item displayed in the status line. Use when you want to set or analyze what task is being worked on. Triggers on "/work-item", "update work item", "set current task", or "what am I working on".
---

# Work Item Tracker

Updates the current work item displayed in the Claude Code status line.

## Usage

- `/work-item` - Analyze conversation and auto-detect current task
- `/work-item "Custom description"` - Set a specific work item manually

## How It Works

The work item is displayed in the status line between the git branch and model name, giving you constant visibility into what task Claude is tracking.

## Instructions

When this skill is invoked:

### If an argument is provided (e.g., `/work-item "Adding dark mode"`)

1. Extract the argument text (remove surrounding quotes if present)
2. Write it directly to the cache file:
   ```bash
   echo "Adding dark mode" > ~/.claude/work-item-cache.txt
   ```
3. Confirm to the user: "Work item updated to: Adding dark mode"

### If no argument is provided (e.g., just `/work-item`)

1. Analyze the recent conversation context to determine the current task
2. Generate a concise summary (max 25 characters) that describes what's being worked on
3. Use action-oriented phrasing like:
   - "Adding user auth"
   - "Fixing API bug"
   - "Refactoring tests"
   - "Implementing search"
4. Write the summary to the cache file:
   ```bash
   echo "Your summary here" > ~/.claude/work-item-cache.txt
   ```
5. Confirm to the user: "Work item updated to: [summary]"

## Cache File Location

`~/.claude/work-item-cache.txt`

This file is:

- Initialized to "New session" when a Claude Code session starts
- Updated when this skill is invoked
- Read by the statusLine command to display the current work item

## Example Status Line Output

```
orient | dev | Adding user auth | opus | ctx: 15%
```

## Tips

- Run `/work-item` periodically when switching tasks
- Use custom descriptions when auto-detection doesn't capture the right context
- Keep descriptions short - they're truncated to 30 characters in the status line
