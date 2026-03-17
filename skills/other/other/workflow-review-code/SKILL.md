---
name: workflow-review-code
description: This skill should be used when reviewing code changes in a branch against main/master/develop. It analyzes commits, integrates JIRA ticket and MR context when available, and produces a structured code review using Conventional Comments format.
---

# Review Code Workflow

## Overview

Review commits and changes in the current branch against main/master/develop. Analyze the diff, integrate available context (JIRA tickets, MR comments), and produce a structured code review.

**Type:** FLEXIBLE - Adapt review depth to the size and complexity of the changes.

**Output:** `review.md` with Conventional Comments format feedback.

## When to Use

Use this workflow when:
- Reviewing a feature branch before merge
- Analyzing code changes for quality issues
- Responding to a merge request review request
- Checking code against ticket requirements

**Announce at start:** "I'm using the review-code workflow to analyze these changes."

## Context Gathering

When this workflow is invoked, gather context from multiple sources:

### Parse Arguments

Extract from provided arguments:
- **JIRA Ticket**: Pattern `[A-Z]+-[0-9]+` (e.g., "RD-1234")
- **MR IID**: Pattern `merge_requests/[0-9]+` (e.g., from GitLab URL)

### Gather JIRA Context (if ticket provided)

Use the `jira-ticket-fetcher` skill to retrieve:
- Ticket description and acceptance criteria
- Requirements to validate against

### Gather MR Context (if MR URL provided)

Use the `mr-tracker` skill to retrieve:
- MR status and description
- Previous review comments and discussions
- Unresolved threads

### Gather Branch Context

```bash
# Working Directory Status
git status --short

# Current Branch
git rev-parse --abbrev-ref HEAD

# Branch Commits (not in main/master/develop)
git log --oneline --no-merges $(git merge-base HEAD $(git for-each-ref --format='%(refname:short)' refs/heads/ | grep -E '^(main|master|develop)$' | head -n1))..HEAD

# Commit Details
git log --no-merges --format="%H%n  Author: %an <%ae>%n  Date: %ad%n  Message: %s%n  Body: %b%n" --date=short $(git merge-base HEAD $(git for-each-ref --format='%(refname:short)' refs/heads/ | grep -E '^(main|master|develop)$' | head -n1))..HEAD

# Files Changed
git diff --name-status $(git merge-base HEAD $(git for-each-ref --format='%(refname:short)' refs/heads/ | grep -E '^(main|master|develop)$' | head -n1))..HEAD

# Full Diff
git diff $(git merge-base HEAD $(git for-each-ref --format='%(refname:short)' refs/heads/ | grep -E '^(main|master|develop)$' | head -n1))..HEAD
```

## Review Instructions

### Using Available Context

**If JIRA Ticket Context is available:**
- **Validate requirements**: Check that the implementation matches the ticket description/acceptance criteria
- **Flag deviations**: If the code diverges from the ticket scope, highlight this in your review
- **Reference the ticket**: Mention the ticket ID when discussing requirement alignment

**If MR Context is available:**
- **Address prior feedback**: Check if previous review comments have been addressed
- **Avoid duplicate comments**: Don't repeat feedback that was already given
- **Acknowledge resolved issues**: Note when prior concerns have been fixed
- **Continue discussions**: If prior comments raised questions, follow up on them

**If neither is provided:**
- Review based solely on code quality, best practices, and the diff content
- If you need more context, use the `jira-ticket-fetcher` or `mr-tracker` skills to fetch additional information

### Review Process

**IMPORTANT**: Review ONLY committed changes. Ignore any uncommitted modifications in the working directory.

1. **Analyze the diff** - Only lines shown in the diff (committed changes)
2. **Read committed versions** of files for context:
   - Use git to read committed versions: `git show HEAD:path/to/file`
   - Do NOT read working directory files that may have uncommitted changes
   - Read direct dependencies (imported modules)
   - Read up to 10 core architectural files (committed versions)
3. **Generate review comments** using Conventional Comments format
4. **Write the review** to `review.md`

## Conventional Comments Format

Use this format for all review comments:

```
<label>: <subject>

<discussion>
```

### Labels

| Label | Description |
|-------|-------------|
| `praise:` | Highlight something positive |
| `nitpick:` | Trivial preference-based request |
| `suggestion:` | Propose an improvement |
| `issue:` | Highlight a problem that needs addressing |
| `question:` | Seek clarification or understanding |
| `thought:` | Share an idea without requiring action |
| `chore:` | Simple task that must be done |

### Decorators

Add decorators in parentheses after the label:

- `(blocking)` - Must be resolved before approval
- `(non-blocking)` - Optional, nice to have
- `(if-minor)` - Only address if the fix is simple

### Examples

```markdown
**issue (blocking):** SQL injection vulnerability

The query on line 45 concatenates user input directly. Use parameterized queries instead.

---

**suggestion (non-blocking):** Consider using a constant

This magic number `86400` appears multiple times. Consider extracting to a named constant like `SECONDS_PER_DAY`.

---

**praise:** Clean error handling

The retry logic with exponential backoff is well implemented and handles edge cases nicely.
```

## Review Checklist

When reviewing, consider:

### Code Quality
- [ ] Clear naming and readability
- [ ] Appropriate error handling
- [ ] No code duplication
- [ ] Follows existing patterns

### Security
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] No SQL injection vulnerabilities
- [ ] Proper authentication/authorization

### Performance
- [ ] No N+1 queries
- [ ] Appropriate caching
- [ ] No unnecessary loops/iterations

### Testing
- [ ] Tests cover new functionality
- [ ] Edge cases tested
- [ ] Tests are maintainable

### Requirements (if JIRA context available)
- [ ] Implements acceptance criteria
- [ ] Stays within scope
- [ ] No scope creep

## Output Format

Write the review to `review.md`:

```markdown
# Code Review: [Branch Name]

**Reviewed:** [Date]
**Commits:** [N commits]
**Files Changed:** [N files]
**JIRA:** [Ticket ID or "N/A"]

## Summary

[2-3 sentence summary of the changes and overall assessment]

## Blocking Issues

[List any blocking issues that must be resolved]

## Suggestions

[List non-blocking suggestions for improvement]

## Praise

[Highlight what was done well]

## Questions

[Any clarifying questions]

## Requirement Validation

[If JIRA context available, validate against acceptance criteria]
```

## Related Skills

- **jira-ticket-fetcher**: Fetches JIRA ticket content for requirement validation
- **mr-tracker**: Monitors MR comments and discussions
- **code-reviewer**: The built-in code review agent for delegated reviews
