---
name: gh-check-ci-status
description: "Check CI/CD status of a pull request including workflow runs and test results. Use when verifying if PR checks are passing or investigating CI failures."
category: github
agent: test-engineer
user-invocable: false
---

# Check CI Status

Verify CI/CD status of a pull request and investigate failures.

## When to Use

- Verifying PR is ready to merge
- Investigating CI failures
- Monitoring long-running CI jobs
- Checking before pushing changes

## Quick Reference

```bash
# Check PR CI status
gh pr checks <pr>

# Watch CI in real-time
gh pr checks <pr> --watch

# Get detailed status
gh pr view <pr> --json statusCheckRollup

# View failed logs
gh run view <run-id> --log-failed

# Rerun failed checks
gh run rerun <run-id>
```

## Workflow

1. **Check status**: Run `gh pr checks <pr>` to see all checks
2. **Identify failures**: Look for ✗ (failed) or ○ (pending)
3. **View logs**: Use `gh run view` to see failure details
4. **Fix locally**: Reproduce issue locally and test
5. **Push fix**: Commit and push changes
6. **Verify**: Watch CI with `--watch` flag

## Common CI Failures

**Pre-commit issues** (formatting/linting):

```bash
just pre-commit-all  # Fix locally
git add . && git commit --amend --no-edit
git push --force-with-lease
```

**Test failures**:

```bash
mojo test tests/          # Run locally
pytest tests/             # Python tests
# Fix code and retest
```

**Workflow validation**:

```bash
gh workflow view <name>   # Check syntax
gh run rerun <run-id>     # Rerun failed
```

## Status Indicators

- `✓` - Passing
- `✗` - Failed
- `○` - Pending/In progress
- `-` - Skipped

## Error Handling

| Problem | Solution |
|---------|----------|
| No checks found | PR may not trigger CI (check workflow) |
| Pending forever | Check logs for stuck jobs |
| Auth error | Verify `gh auth status` |
| API rate limit | Wait or authenticate properly |

## Pre-Merge Verification

Before merging:

- [ ] All required checks passing
- [ ] No pending checks
- [ ] Latest commit has checks
- [ ] Branch up-to-date with base

```bash
gh pr checks <pr>          # All passing?
gh pr view <pr>            # Up-to-date?
gh pr diff <pr>            # Changes correct?
```

## References

- See `.github/workflows/` for CI configuration
- See CLAUDE.md for development workflow
