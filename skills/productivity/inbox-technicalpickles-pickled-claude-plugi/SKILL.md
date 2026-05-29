---
name: inbox
description: Use when checking what PRs are waiting for your review, or when starting your day to see what needs attention
---

# Git Inbox

## Overview

Show PRs awaiting your review across repositories. Surfaces what needs your attention with context to prioritize.

**Announce:** "Using git:inbox to check PRs awaiting your review..."

## When to Use

- Starting your day - "what needs my attention?"
- User asks about PRs to review
- User says "inbox", "review queue", "what's waiting on me?"

## Workflow

### 1. Fetch PRs Awaiting Review

```bash
# PRs where you're requested reviewer
gh search prs --review-requested=@me --state=open --json repository,number,title,author,createdAt,url

# PRs where you're assigned
gh search prs --assignee=@me --state=open --json repository,number,title,author,createdAt,url
```

### 2. Enrich with Review Status

For each PR, get review state:

```bash
gh pr view {number} --repo {owner}/{repo} --json reviews,reviewRequests
```

### 3. Present Inbox

Format as actionable list:

```markdown
## PRs Awaiting Your Review

### {repo} #{number}: {title}
- **Author:** @{author}
- **Age:** {days} days
- **URL:** {full_url}
- **Status:** {review_status}

---

{N} PRs need your attention. Check out a PR for local review?
```

**Important:**
- Always show full PR URL (clickable/copy-pasteable)
- Sort by age (oldest first) or priority
- Show review status (no reviews yet, changes requested, approved by others)

### 4. Offer Next Action

Use AskUserQuestion:

```
Which PR would you like to check out for review?
(A) #{number} - {title}
(B) #{number} - {title}
(C) #{number} - {title}
(D) None right now
```

If user picks one → invoke `git:checkout` with the PR.

## Quick Reference

| Command | Purpose |
|---------|---------|
| `gh search prs --review-requested=@me --state=open` | PRs requesting your review |
| `gh pr view {n} --repo {r} --json reviews` | Get review status |

## Related

- `git:checkout` - Check out a PR for local review
- `code-review` - Guide the actual review process (separate skill)
