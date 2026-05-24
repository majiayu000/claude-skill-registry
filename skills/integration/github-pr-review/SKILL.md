---
name: github-pr-review
description: Extract and review GitHub Pull Requests with comprehensive analysis
---

# GitHub PR Review Skill

## Purpose

This skill extracts comprehensive GitHub Pull Request data and provides a structured methodology for code review. It fetches PR metadata, commits, comments, reviews, file changes, and diffs via the GitHub API, then guides analysis across code quality, security, testing, and best practices.

## When to Use

Use this skill when you need to:

- Review a GitHub Pull Request
- Extract detailed PR information for analysis
- Generate a comprehensive PR summary
- Provide structured code review feedback

## Prerequisites

### Required Tools

- `curl` - for GitHub API requests
- `jq` - for JSON parsing
- `git` - for repository operations

### Environment

- `GITHUB_TOKEN` - GitHub personal access token (optional for public repos, required for private)

## Usage

### Via Agent (Recommended)

Use the `pr-reviewer` agent for context isolation:

```
/review-pr https://github.com/owner/repo/pull/123
```

### Direct Skill Invocation

Follow the instructions in `instructions.md`:

1. Run extraction:

```bash
$HOME/.claude/skills/github-pr-review/scripts/extract.sh \
  --owner <owner> --repo <repo> --pr <number>
```

2. Read the generated `extract.md` from the output directory

3. Apply the review methodology from `instructions.md`

4. Save the review to `review.md` in the same directory

## What Gets Extracted

| Data | Source |
|------|--------|
| PR metadata | Title, author, URL, description |
| Commit history | All commits with SHA, title, description, author |
| Comments | General PR comments with timestamps |
| Review comments | Line-specific comments with file:line context |
| Reviews | Approval states (APPROVED, CHANGES_REQUESTED, etc.) |
| File changes | Diffs and full post-change content |
| Documentation links | Auto-detected based on file types |

## Output

The skill creates a directory structure for each PR review:

```
$BRAIN_HOME/github-pr-reviews/{owner}/{repo}/pr-{number}/
├── extract.md    # Raw PR data from GitHub API
└── review.md     # Structured analysis with summary, findings, and verdict
```

This organization:

- Keeps all PR reviews in a central location
- Preserves review history for future reference
- Groups reviews by repository for easy navigation

## Integration

- **Agent**: `agents/pr-reviewer.md` - runs skill in isolated context
- **Command**: `commands/review-pr.md` - invokes the agent
