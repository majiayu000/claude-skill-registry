---
name: gh-activity-report
description: Generate a plain-language activity report of your GitHub work for a given date range, including commits, pull requests, reviews, issues, and comments. Use this when you need to summarize what you've accomplished on GitHub for status updates, retrospectives, or tracking your work.
license: MIT
---

# GitHub activity report

This skill generates a markdown-friendly report of your GitHub activity over a date range using the `gh` CLI.

## Usage

Run the bundled script with optional `START_DATE` and `END_DATE` (format: `YYYY-MM-DD`).

```bash
# Default: last 7 days
bash skills/gh-activity-report/activity-report.sh

# Specific range
bash skills/gh-activity-report/activity-report.sh 2026-01-01 2026-01-07
```

## Requirements

- `gh` (GitHub CLI) - must be authenticated (`gh auth login`)
- `jq` - used for JSON counting and formatting

## What It Does

- Lists commits you authored in the date range.
- Lists pull requests you created and merged.
- Lists pull requests you reviewed.
- Lists issues you created.
- Prints simple summary counts for quick status updates.

## How It Works

- Uses `gh search` to query commits, PRs, and issues scoped to `@me`.
- Uses platform-aware date defaults (macOS vs Linux) when you omit dates.
- Formats output as readable markdown so you can paste it into status updates or pipe it into an LLM for summarization.

To generate a short natural-language summary, you can pipe the report into your preferred model:

```bash
bash skills/gh-activity-report/activity-report.sh 2026-01-01 2026-01-07 | claude "Summarize this in 2-3 sentences"
```
