---
name: fix-ci-failures
description: Diagnose and fix CI/CD failures by analyzing logs, reproducing locally, and applying fixes. Use when CI checks fail on pull requests.
mcp_fallback: none
category: ci
---

# Fix CI Failures Skill

Diagnose and fix CI failures systematically.

## When to Use

- CI checks fail on PR
- Workflow runs fail
- Tests pass locally but fail in CI
- Need to debug CI issues

## Quick Reference

```bash
# View PR checks
gh pr checks <pr-number>

# View specific run details
gh run view <run-id> --log-failed

# Reproduce locally
./scripts/reproduce_ci.sh <run-id>
```

## Workflow

1. **Check status** - View failed PR checks
2. **Get logs** - Download or view failure details
3. **Reproduce** - Run same commands locally
4. **Fix issue** - Apply necessary changes
5. **Verify** - Test passes locally
6. **Push** - Commit and push fix
7. **Monitor** - Check CI passes

## Common Failures

| Failure | Command | Fix |
|---------|---------|-----|
| Trailing whitespace | `just pre-commit-all` | Stage and re-commit |
| Test failure | `pixi run mojo test tests/` | Fix code, re-run tests |
| Markdown lint | `npx markdownlint-cli2 --fix "**/*.md"` | Commit fixes |
| Build error | Check imports/deps | Update and rebuild |

## Diagnosis Workflow

```bash
# 1. View CI status
gh pr checks 123

# 2. Get failure details
gh run view <run-id> --log-failed

# 3. Download logs for analysis
gh run download <run-id>

# 4. Reproduce issue locally
./scripts/reproduce_ci.sh <run-id>

# 5. Fix the issue
# ... make changes ...

# 6. Verify locally
./scripts/run_ci_locally.sh

# 7. Push fix
git add .
git commit -m "fix: address CI failure"
git push

# 8. Monitor CI
gh pr checks 123 --watch
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| "Cannot find module" | Missing import or broken path | Fix import, check file structure |
| "Syntax error" | Invalid code | Correct syntax, test compile |
| "Test failed" | Logic error | Debug test, fix implementation |
| "Hook failed" | Formatting/whitespace | Run formatters, re-commit |

## Scripts Available

- `scripts/get_ci_logs.sh` - Download CI logs
- `scripts/reproduce_ci_failure.sh` - Reproduce locally
- `scripts/run_ci_locally.sh` - Run CI checks locally
- `scripts/fix_common_ci_issues.sh` - Auto-fix common issues

## Prevention

- Run pre-commit before pushing
- Run tests locally
- Check formatting before commit
- Review CI logs regularly

## References

- Related skill: `quality-run-linters` for linting
- Related skill: `run-precommit` for pre-commit hooks
- Workflow configuration: `.github/workflows/`
