---
name: gh-read-issue-context
description: "Read context from GitHub issue including body and comments. Use before starting implementation work or when prior context is needed."
category: github
agent: test-engineer
user-invocable: false
---

# Read Issue Context

Retrieve all context from a GitHub issue before starting work.

## When to Use

- Before starting implementation work
- When context is needed from prior work
- When checking if issue has been partially addressed
- When understanding design decisions made earlier
- When resuming work after a break

## Quick Reference

```bash
# Get issue details
gh issue view <number>

# Get issue with all comments (implementation history)
gh issue view <number> --comments

# Get structured JSON for parsing
gh issue view <number> --json title,body,comments,labels,assignees,milestone,state

# Get specific field
gh issue view <number> --json body --jq '.body'

# Get linked PRs
gh pr list --search "issue:<number>"

# Get issue timeline
gh api repos/{owner}/{repo}/issues/<number>/timeline
```

## Workflow

### Starting Work on an Issue

1. **Get issue details**: `gh issue view <number>`
2. **Read all comments**: `gh issue view <number> --comments`
3. **Check linked PRs**: `gh pr list --search "issue:<number>"`
4. **Note key context**:
   - Design decisions from comments
   - Blockers or dependencies
   - Acceptance criteria
   - Related issues

### Example Session

```bash
# 1. Read issue #123
gh issue view 123

# 2. Check for prior work
gh issue view 123 --comments

# 3. See if any PRs exist
gh pr list --search "issue:123"

# 4. Get machine-readable data if needed
gh issue view 123 --json title,body,labels,state
```

## Data Extraction

### Get Specific Fields

```bash
# Title only
gh issue view <number> --json title --jq '.title'

# Body content
gh issue view <number> --json body --jq '.body'

# Labels as list
gh issue view <number> --json labels --jq '.labels[].name'

# Comment bodies
gh issue view <number> --json comments --jq '.comments[].body'

# Comment count
gh issue view <number> --json comments --jq '.comments | length'
```

### Parse Comments for Keywords

```bash
# Find design decisions
gh issue view <number> --json comments --jq '.comments[].body' | grep -i "design decision"

# Find blockers
gh issue view <number> --json comments --jq '.comments[].body' | grep -i "blocked\|blocker"

# Find completed items
gh issue view <number> --json comments --jq '.comments[].body' | grep -i "completed\|done"
```

## Status Checking

### Issue State

```bash
# Check if open or closed
gh issue view <number> --json state --jq '.state'

# Check closure reason
gh issue view <number> --json stateReason --jq '.stateReason'

# Check assignees
gh issue view <number> --json assignees --jq '.assignees[].login'
```

### Related Items

```bash
# Find PRs that close this issue
gh pr list --search "closes:#<number>"

# Find mentions in other issues
gh issue list --search "in:body #<number>"

# Find commits referencing issue
gh api search/commits?q=repo:{owner}/{repo}+<number>
```

## Error Handling

| Problem | Solution |
|---------|----------|
| Issue not found | Check issue number, may be in different repo |
| No comments | Issue may be new or have minimal discussion |
| Auth error | Run `gh auth status` to verify |
| Rate limited | Wait or use authenticated requests |

## Best Practices

1. **Always read comments first** - They contain implementation history
2. **Check for linked PRs** - Prior attempts may exist
3. **Note acceptance criteria** - Success criteria should be clear
4. **Look for blockers** - Dependencies may not be resolved
5. **Extract key decisions** - Design choices should inform implementation

## References

- See `.claude/shared/github-issue-workflow.md` for complete workflow
- See CLAUDE.md for project conventions
