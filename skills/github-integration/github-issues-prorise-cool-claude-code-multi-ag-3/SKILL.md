---
name: github-issues
description: Query and search GitHub issues using gh CLI with web fallback. Supports filtering by labels, state, assignees, and full-text search. Use when troubleshooting errors, checking if an issue is already reported, or finding workarounds.
allowed-tools: Bash, Read, Glob, Grep, WebFetch, WebSearch
---

# GitHub Issues Lookup

Query and search GitHub issues for troubleshooting, bug tracking, and finding workarounds. Supports `gh` CLI with automatic web fallback.

## Overview

This skill provides comprehensive guidance for querying GitHub issues from any repository. It prioritizes the GitHub CLI (`gh`) for fast, reliable access with automatic fallback to web-based methods when gh is unavailable.

**Core value:** Quickly find relevant issues when troubleshooting errors, checking if bugs are already reported, or discovering workarounds for known problems.

## When to Use This Skill

This skill should be used when:

- **Troubleshooting errors** - Search for issues matching error messages or symptoms
- **Checking if issue exists** - Before reporting a bug, search for duplicates
- **Finding workarounds** - Discover solutions from issue discussions
- **Tracking features** - Search for feature requests and their status
- **Understanding history** - Find closed issues explaining past decisions

**Trigger keywords:** github issues, search issues, find issue, bug report, issue lookup, gh issue, troubleshoot, workaround, known issue

## Prerequisites

**Recommended (not required):**

- **GitHub CLI (gh)** - Install from <https://cli.github.com/>
- **Authentication** - Run `gh auth login` for private repos

The skill works without `gh` by falling back to web-based methods.

## Quick Start

### Search Issues (gh CLI)

```bash
# Check if gh is available
gh --version

# Search for issues by keyword
gh issue list --repo owner/repo --search "keyword" --state all

# Filter by label
gh issue list --repo owner/repo --label "bug" --state open

# View specific issue
gh issue view 11984 --repo owner/repo

# Search with multiple terms
gh issue list --repo owner/repo --search "error message here" --limit 20
```

### Search Issues (Web Fallback)

When gh is unavailable, use WebSearch or WebFetch:

```text
# Search via web (using WebSearch tool)
Search: "site:github.com/owner/repo/issues keyword"

# Direct URL pattern
https://github.com/owner/repo/issues?q=keyword
```

## Core Capabilities

### 1. Basic Issue Search

Search issues by keywords, matching title and body text.

**gh CLI:**

```bash
# Basic keyword search (all states)
gh issue list --repo anthropics/claude-code --search "path doubling" --state all

# Open issues only
gh issue list --repo anthropics/claude-code --search "path doubling" --state open

# Closed issues only
gh issue list --repo anthropics/claude-code --search "path doubling" --state closed
```

**For detailed query syntax:** See [references/query-patterns.md](references/query-patterns.md)

---

### 2. Filter by Labels

Narrow results using repository labels.

```bash
# Single label
gh issue list --repo owner/repo --label "bug"

# Multiple labels (AND)
gh issue list --repo owner/repo --label "bug" --label "high-priority"

# Common label patterns
gh issue list --repo owner/repo --label "enhancement" --state open
gh issue list --repo owner/repo --label "documentation"
```

---

### 3. Filter by Assignee/Author

Find issues by who created or is assigned to them.

```bash
# By assignee
gh issue list --repo owner/repo --assignee username

# By author
gh issue list --repo owner/repo --author username

# Combined filters
gh issue list --repo owner/repo --author username --state closed
```

---

### 4. View Issue Details

Get full issue content including description and comments.

```bash
# View issue (opens in terminal)
gh issue view 11984 --repo anthropics/claude-code

# View with comments
gh issue view 11984 --repo anthropics/claude-code --comments

# JSON output for parsing
gh issue view 11984 --repo anthropics/claude-code --json title,body,comments
```

---

### 5. Web Fallback Strategy

When gh CLI is unavailable, fall back to web-based methods.

**Detection:**

```bash
# Check if gh is available
if command -v gh &> /dev/null; then
    echo "gh available"
else
    echo "falling back to web"
fi
```

**Web methods (in order of preference):**

1. **WebSearch tool**: `site:github.com/owner/repo/issues keyword`
2. **firecrawl MCP**: Scrape GitHub search results
3. **Direct URL**: `https://github.com/owner/repo/issues?q=keyword`

**For detailed fallback guidance:** See [references/web-fallback.md](references/web-fallback.md)

---

## Output Formats

The skill supports three output formats:

### Compact (default)

One line per issue, good for scanning:

```text
#11984 [open] Path doubling in PowerShell hooks (bug, hooks)
#11523 [closed] Fix memory leak in long sessions (bug, fixed)
#10892 [open] Add custom status line support (enhancement)
```

### Table

Markdown table format for structured display:

```markdown
| # | State | Title | Labels |
| --- | --- | --- | --- |
| 11984 | open | Path doubling in PowerShell hooks | bug, hooks |
| 11523 | closed | Fix memory leak in long sessions | bug, fixed |
```

### Detailed

Full information for deep investigation:

```markdown
### #11984 - Path doubling in PowerShell hooks
**State:** open | **Labels:** bug, hooks | **Created:** 2024-12-01
**URL:** https://github.com/anthropics/claude-code/issues/11984

When using cd && in PowerShell, paths get doubled...
```

---

## Common Workflows

### Troubleshooting an Error

1. Extract key terms from error message
2. Search issues with those terms
3. Check both open and closed issues
4. Look for workarounds in comments

```bash
# Example: Troubleshoot a specific error
gh issue list --repo anthropics/claude-code --search "ENOENT" --state all --limit 10
```

### Before Reporting a Bug

1. Search for existing issues with similar symptoms
2. Check closed issues for past fixes
3. If duplicate exists, add your context as a comment

```bash
# Search before reporting
gh issue list --repo owner/repo --search "feature not working" --state all
```

### Finding Workarounds

1. Search closed issues with your problem keywords
2. Look for issues with "workaround" or "solution" in body
3. Check issue comments for community solutions

```bash
# Find workarounds
gh issue list --repo owner/repo --search "workaround" --state closed --label "bug"
```

---

## Error Handling

### gh not installed

```text
Error: gh: command not found

Solution: Install GitHub CLI from https://cli.github.com/
  - macOS: brew install gh
  - Windows: winget install --id GitHub.cli
  - Linux: See https://github.com/cli/cli/blob/trunk/docs/install_linux.md

Alternatively, falling back to web-based search...
```

### Not authenticated

```text
Error: gh requires authentication

Solution: Run `gh auth login` and follow the prompts.
For public repos, web fallback can be used without authentication.
```

### Rate limited

```text
Error: API rate limit exceeded

Solution: Wait 60 seconds before retrying.
Authenticated requests have higher limits (5000/hour vs 60/hour).
```

### No results found

```text
No issues found matching "very specific query"

Suggestions:
- Try broader search terms
- Remove filters (state, label)
- Check spelling
- Search closed issues too (--state all)
```

---

## References

**Detailed Guides:**

- [references/gh-cli-guide.md](references/gh-cli-guide.md) - Installation, authentication, advanced usage
- [references/query-patterns.md](references/query-patterns.md) - Search syntax and filter examples
- [references/web-fallback.md](references/web-fallback.md) - Web-based fallback strategies

**Related Agents:**

- **history-reviewer** agent - Git history exploration and summarization

---

## Test Scenarios

### Scenario 1: Basic issue search

**Query:** "Search for issues about hooks in the Claude Code repo"

**Expected Behavior:**

- Skill activates on "issues", "hooks", "Claude Code"
- Checks if gh CLI is available
- Runs `gh issue list --repo anthropics/claude-code --search "hooks" --state all`
- Returns formatted results

### Scenario 2: Troubleshooting error

**Query:** "I'm getting a path doubling error in PowerShell. Is this a known issue?"

**Expected Behavior:**

- Skill activates on "error", "known issue", "PowerShell"
- Searches for related issues
- Finds #11984 and similar
- Provides workaround if available

### Scenario 3: Fallback to web

**Query:** "Search for issues but gh isn't installed"

**Expected Behavior:**

- Detects gh not available
- Falls back to WebSearch with `site:github.com/owner/repo/issues`
- Returns results in same format

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-05
**Model:** claude-opus-4-5-20251101

**Audit Status:** NEW - Pending initial audit
