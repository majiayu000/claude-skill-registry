---
name: github-workflow-fixer
description: Analyze and fix GitHub Actions workflow failures. Use when workflows fail, CI/CD issues occur, or when debugging GitHub Actions runs. Triggers on requests like "fix workflow", "why did the build fail", "check CI status", "debug GitHub Actions", or "workflow failed".
---

# GitHub Workflow Fixer

Analyze GitHub Actions workflow results and provide problem-solving guidance.

## Workflow

1. **Identify failed runs**: Use `gh run list` with `--branch` or `--workflow` flag
2. **Analyze logs**: Use `gh run view <run_id> --log-failed` to view error details
3. **Diagnose issues**: Identify root cause from log output
4. **Fix issues**: Apply necessary fixes to workflow files or source code
5. **Verify**: Re-run workflow to confirm fix

## By Branch (Current Branch)

Find and fix failed workflows on the current branch:

```bash
# Get current branch
BRANCH=$(git branch --show-current)

# List runs on this branch
gh run list --branch "$BRANCH"

# View failed run logs
gh run view <run_id> --log-failed
```

## By Workflow File

Find and fix failed workflows for a specific workflow file:

```bash
# List runs for a workflow file
gh run list --workflow=<workflow_file>

# View failed run logs
gh run view <run_id> --log-failed
```

## Common Issues

- **Dependency failures**: Check package versions and lock files
- **Test failures**: Review test output and fix failing tests
- **Build errors**: Check syntax errors and type issues
- **Permission errors**: Verify workflow permissions and secrets
- **Timeout issues**: Optimize long-running steps or increase timeout
