---
name: github:issues
description: Issue triage - stale issues, blocking, no attention, should-close analysis
---

# Issue Triage

Analyze open issues to identify priority, stale items, and cleanup candidates.

## When to Use

- Weekly issue grooming
- Before sprint planning
- When backlog grows too large

> **Auto-approved**: All `gh` commands are read-only and auto-approved.

## Analysis Steps

### 1. All Open Issues

```bash
gh issue list --repo kagenti/kagenti --state open --limit 100 --json number,title,labels,createdAt,updatedAt,assignees,comments
```

### 2. Issues Without Attention (no assignee, no comments)

```bash
gh issue list --repo kagenti/kagenti --state open --limit 100 --json number,title,assignees,comments --jq '.[] | select(.assignees | length == 0) | select(.comments == 0) | "#\(.number) \(.title)"'
```

### 3. Stale Issues (no update > 30 days)

```bash
gh issue list --repo kagenti/kagenti --state open --limit 100 --json number,title,updatedAt --jq '.[] | select(.updatedAt < (now - 30*24*3600 | strftime("%Y-%m-%dT%H:%M:%SZ"))) | "#\(.number) \(.title) (last: \(.updatedAt))"'
```

### 4. Blocking / High Priority

```bash
gh issue list --repo kagenti/kagenti --state open --label "priority/critical,priority/high,blocking" --json number,title,labels
```

### 5. Security Issues

```bash
gh issue list --repo kagenti/kagenti --state open --label "security" --json number,title,createdAt
```

## Triage Report

```markdown
## Issue Triage Report

### Needs Attention (no assignee, no comments): N
- [list]

### Stale (> 30 days no activity): N
- [list — consider closing or updating]

### Blocking / High Priority: N
- [list — needs immediate action]

### Candidates to Close
- [issues that are resolved, outdated, or duplicated]
```

### Optionally Close or Comment

```bash
gh issue close <number> --repo kagenti/kagenti --comment "Closing as resolved/outdated. See #<newer-issue> for updated version."
```

## Related Skills

- `github:last-week` - Weekly summary including issues
- `github:prs` - PR health analysis
- `repo:issue` - Create properly formatted issues
