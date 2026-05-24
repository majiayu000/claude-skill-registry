---
name: describe-pr
description: Generate clear PR descriptions from code changes
disable-model-invocation: true
---

# Generate PR Description

Create a comprehensive pull request description based on the actual changes in the PR.

## Process

### Step 1: Identify the PR

**If on branch with associated PR:**
```bash
gh pr view --json url,number,title,state,baseRefName
```

**If not on PR branch or PR doesn't exist:**
```bash
# List open PRs
gh pr list --limit 10 --json number,title,headRefName,author

# Ask user which PR to describe
```

### Step 2: Gather PR Information

```bash
# Get full diff
gh pr diff {number}

# Get commit history
gh pr view {number} --json commits --jq '.commits[] | "\(.oid[0:7]) \(.messageHeadline)"'

# Get PR metadata
gh pr view {number} --json url,title,number,state,baseRefName,additions,deletions
```

### Step 3: Analyze Changes Deeply

Review all changes and understand:

**What changed:**
- Files modified, added, removed
- Lines added/removed
- Key functions/classes affected

**Why it changed:**
- What problem does this solve?
- What requirement does this fulfill?
- What was wrong before?

**Impact:**
- User-facing changes
- API changes
- Breaking changes
- Performance implications
- Security considerations

**Context:**
- Related issues
- Related plans or design docs
- Dependencies on other PRs
- Follow-up work needed

### Step 4: Generate Description

**Template:**

```markdown
## Summary

[2-3 sentence overview of what this PR does and why it's needed]

## Changes

**Key changes:**
- [Specific change 1 with reasoning]
- [Specific change 2 with reasoning]
- [Specific change 3 with reasoning]

**Files changed:**
- `path/to/file1.ext` - [What changed and why]
- `path/to/file2.ext` - [What changed and why]

## Motivation

[Explain the problem this PR solves or the requirement it fulfills.
Reference related issues, user requests, or technical debt.]

## Implementation Details

[Explain key implementation decisions, trade-offs considered,
and why this approach was chosen over alternatives.]

**Key decisions:**
1. [Decision 1]: [Rationale]
2. [Decision 2]: [Rationale]

## Related

- Issue: #123 [if applicable]
- Plan: `plans/2026-01-12-feature-name.md` [if applicable]
- Design doc: `docs/design-xyz.md` [if applicable]
- Depends on: PR #456 [if applicable]
- Blocks: PR #789 [if applicable]

## Testing

**Automated tests:**
- [ ] Unit tests pass (`npm test`)
- [ ] Integration tests pass
- [ ] E2E tests pass [if applicable]

**Manual testing:**
- [ ] [Specific manual test 1]
- [ ] [Specific manual test 2]
- [ ] [Specific manual test 3]

**Test coverage:**
- [Coverage stats if available]

## Breaking Changes

[If any breaking changes, list them prominently here with migration guidance]

**None** [if no breaking changes]

## Migration Guide

[If breaking changes exist, provide step-by-step migration instructions]

## Security Considerations

[Any security implications, or state "None identified"]

## Performance Impact

[Any performance changes, benchmarks, or state "No significant impact"]

## Screenshots / Demos

[For UI changes, include before/after screenshots or GIFs]

## Rollout Plan

[If phased rollout needed, describe the plan]

## Follow-up Work

[List any follow-up work needed in future PRs]
- [ ] [Follow-up task 1]
- [ ] [Follow-up task 2]

## Reviewer Notes

[Specific things you want reviewers to focus on or be aware of]
```

### Step 5: Present to User

Show the generated description and ask for approval:

```
I've generated a PR description for PR #{number}. Here's what I've created:

[Show description]

Would you like me to:
1. Update the PR with this description
2. Make changes to the description first
3. Copy to clipboard for manual update
```

### Step 6: Update PR

Upon approval:

```bash
# Save description to temp file (for complex descriptions with newlines)
cat > /tmp/pr-description.md <<'EOF'
[description content]
EOF

# Update PR
gh pr edit {number} --body-file /tmp/pr-description.md

# Verify
gh pr view {number}
```

## Guidelines

1. **Focus on "why" not just "what"** - Diff shows what, description explains why
2. **Be specific** - Vague descriptions aren't helpful
3. **Include context** - Link to issues, plans, discussions
4. **Think about reviewers** - What do they need to know?
5. **Highlight breaking changes** - Make them impossible to miss
6. **Provide testing guidance** - Help reviewers verify
7. **Be thorough but scannable** - Use headers and bullets
