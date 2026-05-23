---
name: git-code-review
description: Get git records for specified users and days, perform code review for each commit, and generate detailed code review reports
---

# Git Code Review

This skill analyzes git commit history for specified users and generates comprehensive code review reports. It fetches commit data, analyzes changes, and provides structured feedback on code quality, best practices, and potential improvements.

## Capabilities

- **User-Specific Git History**: Fetch commit history for one or multiple users
- **Time-Based Filtering**: Filter commits by days (defaults to current day)
- **Commit Analysis**: Analyze each commit's changes, additions, and deletions
- **File-Level Summaries**: Summarize changes organized by file
- **Line-by-Line Review**: Provide detailed feedback on specific code changes
- **Report Generation**: Create structured markdown reports with recommendations
- **Automated Reporting**: Save reports to organized directory structure

## Input Requirements

**Required Parameters:**
- **User Names**: One or multiple git usernames, separated by commas (e.g., "john,mary,alex")
- **Days**: Optional number of days to look back (defaults to current day)

**Data Sources:**
- Current git repository must be initialized
- Git command-line tools must be available
- User must have read access to git history

**Format:**
- Text-based invocation with parameters
- Can be called via Claude interface with user specifications

## Output Formats

**Report Files:**
- **Format**: Markdown (.md)
- **Naming**: `username-date.md` (e.g., `john-2025-12-14.md`)
- **Location**: `current-repo/.claude/git_code_review/`

**Report Structure:**
1. **Summary**: Overview of commits analyzed
2. **File-Level Analysis**: Changes organized by file
3. **Commit Details**: Individual commit analysis
4. **Line-by-Line Review**: Specific code change feedback
5. **Recommendations**: Actionable improvement suggestions
6. **Best Practices**: Relevant coding standards guidance

**Content Includes:**
- Code snippets with highlighted changes
- Quality assessment scores
- Potential issues flagged
- Performance considerations
- Security implications
- Maintainability suggestions

## How to Use

"Review git commits for users 'john,mary' from the last 3 days"
"Generate code review report for user 'alex' for today's commits"
"Analyze all commits by 'sarah' and 'mike' this week"
"Get detailed code review for current user's recent changes"

## Scripts

- `git_code_review.py`: Main script for fetching git history, analyzing commits, and generating reports

## Best Practices

1. **Repository Context**: Run from within the git repository you want to analyze
2. **User Validation**: Ensure usernames match git commit author names
3. **Time Windows**: Use reasonable day ranges to avoid overwhelming reports
4. **Review Focus**: Prioritize recent changes for most relevant feedback
5. **Follow-up**: Use reports as starting points for team discussions

## Limitations

- Requires git repository with commit history
- Limited to commit metadata and diff analysis
- Cannot analyze unstaged or uncommitted changes
- Performance may degrade with very large commit histories
- Analysis is based on commit diffs only (no runtime behavior analysis)
- Some git configurations may affect user name matching accuracy
- Binary files are not analyzed for content changes