---
name: git-commit-summarizer
description: Summarizes git commits for specified users over a given time period and generates markdown reports
---

# Git Commit Summarizer

This skill analyzes git commit history for specified users and generates detailed markdown summary reports. It helps track developer contributions, code changes, and project progress over time.

## Capabilities

- **User-Specific Analysis**: Summarize commits for one or multiple git users
- **Time-Based Filtering**: Analyze commits from today or over specified number of days
- **Report Generation**: Create detailed markdown reports with commit statistics
- **File Organization**: Automatically save reports to `.claude/git_commit_report/` directory
- **Multi-User Support**: Process multiple users in a single execution

## Input Requirements

The skill requires:
- **Usernames**: One or more git usernames (comma-separated)
- **Days**: Optional number of days to analyze (defaults to today)

**Example Input Format**:
```
@git-commit-summarizer
Usernames: john.doe,jane.smith,alex.wong
Days: 7
```

## Output Formats

**Report Files**: Markdown files saved to `[current_repository]/.claude/git_commit_report/`
- Filename format: `[username]-[date].md`
- Each report includes:
  - User information and analysis period
  - Total commit count
  - Commit details (hash, date, message, files changed)
  - Statistics (commits per day, files per commit)
  - Summary of changes

**Console Output**: Summary of processing results and report locations

## How to Use

"Summarize git commits for user 'john.doe' over the last 3 days"
"Generate commit reports for 'alice,bob,charlie' for today"
"Analyze all commits by 'dev-team' in the last 14 days"

## Scripts

- `git_commit_analyzer.py`: Main module for analyzing git commits and generating reports
- `report_generator.py`: Creates formatted markdown reports from commit data

## Best Practices

1. **Repository Context**: Run this skill within a git repository directory
2. **User Names**: Use exact git usernames as they appear in commit history
3. **Time Range**: Specify days when you need historical analysis (default is today)
4. **Report Location**: Reports are saved in `.claude/git_commit_report/` for easy access
5. **Multiple Users**: Use comma-separated format for analyzing multiple users at once

## Limitations

- Requires git repository with commit history
- Only analyzes commits from the current repository
- Usernames must match exactly as in git commit history
- Time-based filtering uses relative days from current date
- Cannot analyze commits from remote repositories without local clone