---
name: verify-pr-ready
description: "Verify a PR is ready for merge (CI passing, approvals, no conflicts). Use before merging to ensure all requirements met."
category: github
---

# Verify PR Ready for Merge

Check that PR meets all requirements before merging.

## When to Use

- Before merging a PR manually
- Checking if PR is ready for automated merge
- Validating PR readiness in batch merge operations
- Before requesting final approval
- Verifying branch protection rule compliance

## Quick Reference

```bash
# Check PR status
gh pr view <pr>

# Check CI status
gh pr checks <pr>

# View PR review status
gh pr view <pr> --json reviews

# Check for conflicts
gh pr status <pr> | grep -i "conflict"

# Get PR details as JSON
gh api repos/OWNER/REPO/pulls/<pr> --jq '.{mergeable, merged, title}'
```

## Readiness Checklist

Before merging, verify:

- [ ] All CI checks passing (no failures or pending)
- [ ] Required number of approvals received
- [ ] No requested changes from reviewers
- [ ] PR is linked to issue
- [ ] No merge conflicts detected
- [ ] Branch is up to date with main
- [ ] All branch protection rules satisfied
- [ ] Code review completed

## Workflow

1. **View PR**: Get full PR details with `gh pr view <pr>`
2. **Check CI**: Verify all checks passing with `gh pr checks <pr>`
3. **Check reviews**: Confirm approvals with `gh pr view --json reviews`
4. **Check conflicts**: Test mergeability (mergeable field)
5. **Verify rules**: Check branch protection satisfaction
6. **Final validation**: Confirm all requirements met
7. **Report status**: Merge or identify blocking issues

## Blocking Issues

PR cannot merge if:

- CI checks failing (pipeline errors or test failures)
- Merge conflicts exist (requires manual resolution)
- Required approvals not met (check branch protection rules)
- Requested changes pending (from required reviewers)
- Branch is stale (needs rebase on main)
- Protected rule violations (size, format, etc.)

## Output Format

Report readiness status with:

1. **Overall Status** - Ready or Not Ready with reasons
2. **CI Status** - All checks + counts of passing/failing
3. **Review Status** - Approvals count and any requested changes
4. **Merge Status** - Mergeable true/false and conflict info
5. **Blocking Issues** - List of what prevents merge (if any)
6. **Recommendation** - Approve for merge or required actions

## Error Handling

| Problem | Solution |
|---------|----------|
| Mergeable check fails | Rebase on main and resolve conflicts |
| CI pending | Wait for checks to complete |
| Approvals missing | Request review from required reviewers |
| Auth error | Check `gh auth status` permissions |
| PR not found | Verify PR number exists |

## References

- See gh-review-pr for comprehensive review checklist
- See gh-batch-merge-by-labels for batch merge workflow
- See CLAUDE.md for PR linking and branch protection rules
