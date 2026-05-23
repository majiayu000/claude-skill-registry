---
name: gh-activity
description: Reports your GitHub activity for a specific day using the gh CLI, showing commits, issues, and activity timeline. Use this when you need to review what you accomplished on GitHub for a particular date.
license: MIT
---

# GitHub Activity Reporter

This skill reports your GitHub activity for a specific day using the `gh` CLI.

## Usage

Run the script with an optional date argument (defaults to today):

```bash
# Get today's activity
bash gh-activity.sh

# Get activity for a specific date
bash gh-activity.sh 2025-12-15
```

The date format must be `YYYY-MM-DD`.

## Requirements

- `gh` (GitHub CLI) - must be authenticated with your GitHub account
- `jq` - for JSON processing

## What It Reports

**Commits**: Lists all commits you made with their actual commit messages, grouped by repository and branch.

**Issues**: Shows all issues you created, commented on, or interacted with, including issue titles and the type of interaction.

**Activity Timeline**: A chronological view of all your GitHub events for the day (pushes, PRs, issue comments, etc.).

## How It Works

1. Verifies you're authenticated with GitHub CLI
2. Fetches your events using `gh api /users/{username}/events`
3. Filters events to the specified date
4. For each push event, fetches actual commits using `gh api /repos/{repo}/compare/{before}...{head}`
5. Extracts and displays issue information from issue events
6. Formats everything into a clear, organized report
