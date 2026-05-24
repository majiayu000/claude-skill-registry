---
name: gh-batch-merge-by-labels
description: "Batch merge multiple PRs by label (e.g., all 'ready-to-merge' PRs). Use when you have multiple approved PRs to merge."
category: github
agent: pr-cleanup-specialist
---

# Batch Merge PRs by Label

Merge multiple PRs at once based on label matching.

## When to Use

- Multiple PRs are ready for merge with same status label
- Automating merge of dependent chain of PRs
- Merging all "ready-to-merge" or "approved" PRs
- Batch processing end-of-sprint or release merges
- Reducing manual merge overhead

## Quick Reference

```bash
# List PRs with specific label
gh pr list --label "ready-to-merge" --state open

# Merge single PR
gh pr merge <pr> --squash --delete-branch

# Get PR numbers for batch merge
gh pr list --label "ready-to-merge" --json number --jq '.[].number'

# Merge all PRs with label (requires loop)
for pr in $(gh pr list --label "ready-to-merge" --json number --jq '.[].number'); do
  gh pr merge "$pr" --squash --delete-branch
done
```

## Workflow

1. **Query PRs**: Find all PRs with target label
2. **Verify each**: Check CI status and approvals for each PR
3. **Check dependencies**: Ensure no conflicts between PRs to merge
4. **Sort by order**: Merge in dependency order if applicable
5. **Execute merges**: Merge each PR in sequence
6. **Verify success**: Confirm all PRs merged successfully
7. **Report results**: Summary of merged PRs

## Merge Options

**Squash Merge** (recommended):

- Combines all commits into single commit
- Clean git history
- `--squash` flag enables this

**Create Merge Commit**:

- Preserves all commits
- Clear merge history
- Default behavior without `--squash`

**Rebase and Merge**:

- Linear history
- `--rebase` flag enables this
- Good for feature branches

## Safety Checks

Before batch merging:

1. **CI Status**: All checks passing
2. **Approvals**: Required number of approvals met
3. **Conflicts**: No merge conflicts detected
4. **Dependencies**: No blocked dependencies
5. **Protected rules**: All branch protection rules satisfied

## Output Format

Report batch merge results with:

1. **Total PRs** - Count of PRs to merge
2. **Merge Summary** - PR number, title, status
3. **Success Count** - Number successfully merged
4. **Failed Count** - Number that failed to merge
5. **Errors** - Why any PRs failed

## Error Handling

| Problem | Solution |
|---------|----------|
| CI failing | Skip that PR, check analyze-ci-failure-logs |
| Merge conflict | Resolve manually, cannot batch merge |
| No permissions | Check gh auth status and repo access |
| Branch protection | Verify all required rules met |
| Network error | Retry with exponential backoff |

## References

- See gh-review-pr for PR review checklist
- See verify-pr-ready skill for pre-merge validation
- See CLAUDE.md for PR linking requirements
