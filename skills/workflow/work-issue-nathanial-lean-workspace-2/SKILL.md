---
name: work-issue
description: Start working on a tracked issue. Use when beginning work on an issue, logging progress, or managing issue workflow.
---

# Work on Issue

Manage the full lifecycle of working on a tracked issue.

## Quick Start

1. Get the issue ID from the user or list available issues
2. Mark the issue as in-progress
3. Show issue details for context
4. Track progress as you work
5. Close when complete

## Workflow

### Starting Work

```bash
# List available issues
tracker list

# List issues for a specific project
tracker list --project=parlance

# Mark issue as in-progress
tracker update <id> --status=in-progress

# Show full details
tracker show <id>
```

### During Work

Log progress regularly as you work on the issue:

```bash
tracker progress <id> "Found root cause in Parser.lean:142"
tracker progress <id> "Implemented fix, running tests"
tracker progress <id> "Tests pass, ready for review"
```

### Completing Work

```bash
tracker close <id> "Fixed in commit abc123. Added regression test."
```

## Arguments

- `<id>` - Issue ID to work on
- `start` - Begin working (marks as in-progress)
- `progress "<message>"` - Log progress update
- `block "<reason>"` - Mark issue as blocked
- `done "<summary>"` - Close the issue

## Example Usage

```
/work-issue 001              # Show issue and start working
/work-issue 001 start        # Mark as in-progress
/work-issue 001 progress "Found the bug"
/work-issue 001 done "Fixed in commit xyz"
```

## Best Practices

1. **Always mark in-progress** before starting work
2. **Log progress frequently** - helps track what was tried
3. **Include context** - file paths, line numbers, commit hashes
4. **Close with details** - what was done, how to verify

## Integration with Git

When closing an issue, suggest:
- Include issue ID in commit message: `Fix #001: Memory leak in parser`
- Commit `.issues/` changes with related code changes
- Reference issue in PR description

## Blocked Issues

If blocked on something:

```bash
tracker block <id> "Waiting on upstream dependency release"
```

This preserves progress while indicating the issue can't proceed.
