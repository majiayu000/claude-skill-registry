---
name: creating-pull-requests
description: Use this skill when creating pull requests, drafting PR descriptions, or running `gh pr create`. Ensures proper PR formatting with active-voice titles and structured descriptions explaining why, how, and context links.
---

# Creating Pull Requests

Create well-structured pull requests with clear titles and comprehensive descriptions.

# Critical Rules

**NEVER do these:**
- Do NOT add yourself as a coauthor on commits (no `Co-Authored-By` headers)
- Do NOT include phrases like "Generated with Claude Code" or "Created by Claude"
- Do NOT mention AI or Claude anywhere in commits or PR descriptions

# PR Title Format

Use **active voice** with a present-tense verb:

| Good | Bad |
|------|-----|
| Add user authentication | Added user authentication |
| Fix memory leak in cache | Fixing memory leak |
| Update dependencies to latest | Dependency updates |
| Remove deprecated API endpoints | Removed deprecated API |
| Refactor database connection pool | Database refactoring |

**Pattern**: `<Verb> <what> [to/in/for <context>]`

Common verbs: Add, Fix, Update, Remove, Refactor, Implement, Improve, Replace, Enable, Disable

# PR Description Structure

```markdown
## Why

[Explain the motivation for this change. What problem does it solve? What feature does it enable?]

## Approach

[Explain why this implementation was chosen over alternatives. What trade-offs were considered?]

## How it works

[Describe the technical implementation. How does the code achieve the goal?]

## Links

- [Ticket](url) or JIRA-123
- [Slack thread](url)
```

# Step-by-Step Process

## 1. Gather Context

Before creating the PR, understand what's being changed:

```bash
# See all commits on this branch vs main
git log main..HEAD --oneline

# See the full diff
git diff main...HEAD

# Check current branch name
git branch --show-current
```

## 2. Identify Links and References

Ask the user or search for:
- Jira/ticket numbers (look in commit messages or branch name)
- Related Slack conversations
- Fusion run URLs
- GCS paths for data or artifacts

## 3. Draft the PR

```bash
gh pr create --title "Add feature X to service Y" --body "$(cat <<'EOF'
## Why

[Motivation here]

## Approach

[Implementation rationale here]

## How it works

[Technical details here]

## Links

- [Ticket](url)
EOF
)"
```

# Example

**Branch**: `feature/add-retry-logic`
**Commits**: Adds exponential backoff retry to HTTP client

**Title**: `Add exponential backoff retry to HTTP client`

**Description**:
```markdown
## Why

HTTP requests to external services occasionally fail due to transient network issues. Without retry logic, these failures cascade to users as errors.

## Approach

Chose exponential backoff over fixed-interval retry to avoid thundering herd problems during partial outages. Used a max of 3 retries with jitter to spread out retry attempts.

## How it works

Wraps the existing HTTP client with a retry decorator. On 5xx responses or network errors, waits `2^attempt * 100ms + random(0-50ms)` before retrying. Logs each retry attempt for observability.

## Links

- [PROJ-1234](https://jira.example.com/browse/PROJ-1234)
- [Slack discussion](https://slack.com/archives/...)
```

# CLI Commands

```bash
# Create PR interactively
gh pr create

# Create with title and body
gh pr create --title "Add X" --body "Description here"

# Create as draft
gh pr create --draft --title "Add X" --body "..."

# Create with specific base branch
gh pr create --base develop --title "Add X" --body "..."

# Create and immediately open in browser
gh pr create --title "Add X" --body "..." --web
```

# Validation Checklist

Before creating the PR, verify:
- [ ] Title uses active voice with present-tense verb
- [ ] Description has Why, Approach, and How sections
- [ ] All relevant links are included
- [ ] No AI/Claude attribution anywhere
- [ ] No Co-Authored-By headers in commits
