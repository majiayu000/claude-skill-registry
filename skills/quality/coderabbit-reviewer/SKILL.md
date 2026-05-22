---
name: coderabbit-reviewer
description: Integrates CodeRabbit for automated PR code review. Use after PR creation to get AI-powered review feedback before human review.
---

# CodeRabbit Reviewer

Processes CodeRabbit automated review feedback and helps address issues. Assumes CodeRabbit is already installed on the repository.

## Prerequisites

- PR created and pushed to GitHub
- CodeRabbit installed on Comfy-Org/ComfyUI_frontend (it is)

## Workflow

### 1. Verify PR Exists

```bash
PR_NUMBER=$(gh pr view --json number -q '.number')
echo "PR #$PR_NUMBER"
```

### 2. Wait for CodeRabbit Review

CodeRabbit reviews automatically on PR creation. Check for review comment:

```bash
# Check for CodeRabbit review comment
gh pr view $PR_NUMBER --json comments --jq '.comments[] | select(.author.login == "coderabbitai")'
```

Typical wait time: 2-5 minutes for small PRs.

To manually trigger a re-review:

```bash
gh pr comment $PR_NUMBER --body "@coderabbitai review"
```

### 3. Parse Review Feedback

Extract actionable items from CodeRabbit's review:

```markdown
## CodeRabbit Review Summary

### Critical Issues

- [ ] {file:line} - {issue description}

### Suggestions

- [ ] {file:line} - {suggestion}

### Nitpicks

- [ ] {file:line} - {minor improvement}
```

### 4. Categorize by Severity

| Category   | Action Required       | Auto-fixable |
| ---------- | --------------------- | ------------ |
| Critical   | Must fix before merge | Sometimes    |
| Suggestion | Should consider       | Often        |
| Nitpick    | Nice to have          | Usually      |

### 5. Present to User

```
CodeRabbit Review Complete

## Summary
- Critical: 2 issues
- Suggestions: 5 items
- Nitpicks: 3 items

## Critical Issues (must fix)
1. src/components/Feature.vue:45 - Potential null reference
2. src/stores/data.ts:23 - Missing error handling

Options:
1. Auto-fix critical issues
2. Show all feedback details
3. Dismiss and proceed to human review

Your choice:
```

### 6. Fix Issues

For fixable issues, apply changes directly or dispatch subagents:

```
Fix CodeRabbit critical issue:

File: {file}
Line: {line}
Issue: {description}
Suggestion: {CodeRabbit's suggestion}

Apply fix and verify with `pnpm typecheck`.
```

### 7. Request Re-Review

After fixes:

```bash
git add -A
git commit -m "fix: address CodeRabbit review feedback"
git push

# Request re-review
gh pr comment $PR_NUMBER --body "@coderabbitai review"
```

### 8. Update Status

```bash
jq '.coderabbitReview = {
  "reviewedAt": now,
  "critical": N,
  "suggestions": N,
  "fixed": N
}' "$RUN_DIR/status.json" > tmp && mv tmp "$RUN_DIR/status.json"
```

## CodeRabbit Commands

Trigger via PR comments:

| Command                 | Purpose               |
| ----------------------- | --------------------- |
| `@coderabbitai review`  | Full review           |
| `@coderabbitai summary` | Generate PR summary   |
| `@coderabbitai resolve` | Mark threads resolved |

## Integration with Pipeline

**Before:** pr-creator (PR exists)
**After:** review-orchestrator (human review)

Recommended flow:

1. PR created → CodeRabbit auto-reviews
2. Fix critical issues
3. Human review with CodeRabbit context
4. Merge
