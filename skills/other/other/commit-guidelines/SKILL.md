---
name: commit-guidelines
description: Provides commit message formatting standards for this project. Claude should use this skill when creating git commits to ensure messages follow project conventions, including proper co-authorship attribution and concise formatting.
---

# Commit Message Guidelines

**IMPORTANT**: Always invoke this skill (`idea-to-code:commit-guidelines`) before creating any git commit in projects that use it. This ensures commit messages follow project conventions.

When writing commit messages for this project, follow these guidelines:

## Message Structure

- The commit message should be concise and descriptive of the changes made
- The first line of the commit message should describe the high-level goal of the change
- If the work is associated with an issue, include the issue number in the commit message

## Git Add and Commit Separately

Run `git add` and `git commit` as separate tool calls rather than chaining with `&&`. This provides:
- Visibility into what was staged
- Opportunity for user to intervene before commit
- Clearer error attribution if something fails

## Co-authorship Attribution

Use "Co-authored by Claude Code" in the commit message instead of the standard Claude Code attribution format.

Specifically, use:
```
Co-authored by Claude Code
```

Instead of:
```
🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Special Cases

### Converting Classes to Records

When converting classes to records, use a concise commit message that simply says which classes were converted. No need to explain method renames or justification.

Example:
```
Convert UserProfile and AccountSettings classes to records

Co-authored by Claude Code
```
