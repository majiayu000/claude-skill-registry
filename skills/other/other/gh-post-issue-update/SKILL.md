---
name: gh-post-issue-update
description: "Post structured updates to GitHub issues. Use to report progress, findings, and implementation notes directly to issues."
category: github
agent: test-engineer
user-invocable: false
---

# Post Issue Update

Post implementation notes, status updates, and findings to GitHub issues.

## When to Use

- Reporting implementation progress
- Documenting design decisions
- Posting completion summaries
- Sharing findings or blockers
- Creating audit trail for work done

## Quick Reference

```bash
# Short status update
gh issue comment <number> --body "Status: [brief update]"

# Detailed notes with heredoc
gh issue comment <number> --body "$(cat <<'EOF'
## Implementation Notes

Content here...
EOF
)"

# From file
gh issue comment <number> --body-file /path/to/file.md
```

## Workflow

### Progress Updates

Post regular updates as work progresses:

```bash
gh issue comment <number> --body "$(cat <<'EOF'
## Progress Update

### Completed
- [x] Created module structure
- [x] Implemented core functions

### In Progress
- [ ] Writing unit tests

### Next Steps
1. Complete test coverage
2. Integration testing
EOF
)"
```

### Implementation Complete

Post when work is finished:

```bash
gh issue comment <number> --body "$(cat <<'EOF'
## Implementation Complete

**PR**: #<pr-number>

### Summary
[Brief description of what was implemented]

### Files Changed
- `path/to/file1.mojo` - Added tensor operations
- `path/to/file2.mojo` - Updated imports

### Testing
- All 15 tests pass
- Coverage: 85%

### Verification
- [x] `pixi run test` passes
- [x] `just pre-commit-all` passes
- [x] Manual verification complete
EOF
)"
```

### Design Decisions

Document important decisions:

```bash
gh issue comment <number> --body "$(cat <<'EOF'
## Design Decision

### Context
[Why this decision was needed]

### Options Considered
1. Option A - [pros/cons]
2. Option B - [pros/cons]

### Decision
Chose Option A because [reasoning]

### Consequences
- [Impact 1]
- [Impact 2]
EOF
)"
```

### Blockers

Report blockers clearly:

```bash
gh issue comment <number> --body "$(cat <<'EOF'
## Blocked

### Blocker
[Description of what's blocking]

### Impact
- Cannot proceed with [task]
- Waiting on [dependency/decision]

### Resolution Path
- Option 1: [approach]
- Option 2: [approach]

### Help Needed
@[username] - [specific request]
EOF
)"
```

## Templates

### Status Update

```markdown
## Status Update

**Status**: [In Progress | Blocked | Complete]

### Summary
[1-2 sentences about current state]

### Details
[Additional context if needed]

### Next Steps
1. [Step 1]
2. [Step 2]
```

### Review Findings

```markdown
## Review Complete

### Summary
[Brief summary of review]

### Findings
1. [Finding 1]
2. [Finding 2]

### Recommendations
- [Recommendation 1]
- [Recommendation 2]
```

### Bug Investigation

```markdown
## Investigation Complete

### Root Cause
[What's causing the issue]

### Evidence
- [Evidence 1]
- [Evidence 2]

### Fix Approach
[How to fix it]

### Testing Plan
- [ ] Unit test for regression
- [ ] Integration test
```

## Best Practices

1. **Be Concise**: Focus on actionable information
2. **Use Structure**: Headers and lists improve readability
3. **Include Context**: Future readers need to understand decisions
4. **Link Related Items**: Reference PRs, other issues, commits
5. **Update Regularly**: Don't wait until completion

## Using Body Files

For complex content with special characters:

```bash
# Create temp file
cat > /tmp/update.md << 'EOF'
## Update

Complex content with `code` and special chars...
EOF

# Post using file
gh issue comment <number> --body-file /tmp/update.md

# Clean up
rm /tmp/update.md
```

## Error Handling

| Problem | Solution |
|---------|----------|
| Issue locked | Contact maintainer or use PR comments |
| Rate limited | Wait and retry |
| Auth error | Run `gh auth status` |
| Content too long | Split into multiple comments |

## References

- See `.claude/shared/github-issue-workflow.md` for complete workflow
- See CLAUDE.md for project conventions
