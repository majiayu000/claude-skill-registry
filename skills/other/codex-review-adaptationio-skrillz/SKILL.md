---
name: codex-review
description: Code review workflows with Codex CLI including automated reviews, diff analysis, and PR improvements. Use for code review, quality checks, or automated improvement suggestions.
---

# Codex Code Review

Comprehensive code review and analysis workflows with full automation.

**Last Updated**: December 2025 (GPT-5.2 Release)

## Automated Code Review

```bash
# Full automated review
codex exec --dangerously-bypass-approvals-and-sandbox \
  --json \
  "Review entire codebase:
  1. Code quality analysis
  2. Security vulnerabilities
  3. Performance issues
  4. Best practice violations
  5. Missing tests
  6. Documentation gaps
  Generate prioritized report" \
  > review-report.json

# Review with fixes
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Review code and auto-fix all issues found"
```

## Git Diff Review

```bash
# Review uncommitted changes
git diff | codex exec --dangerously-bypass-approvals-and-sandbox \
  "Review this diff and suggest improvements"

# Review PR changes
gh pr view 123 --json body,diff | \
  codex exec --dangerously-bypass-approvals-and-sandbox \
  "Review PR and provide detailed feedback"
```

## Apply Codex Suggestions

```bash
# Apply latest diff from Codex
codex apply
# or
codex a

# Review before applying
git diff  # Review what Codex changed
git add -p  # Stage selectively
```

## Automated Review Workflows

```bash
#!/bin/bash
# Complete automated review workflow

auto_review_and_fix() {
  local scope="${1:-.}"

  codex exec --dangerously-bypass-approvals-and-sandbox \
    "Automated review and fix for $scope:
    1. Analyze all code
    2. Identify issues
    3. Auto-fix all issues
    4. Run tests
    5. Fix test failures
    6. Generate review report
    7. Create clean git commits" \
    > review-summary.md

  echo "Review complete: review-summary.md"
}

# Usage
auto_review_and_fix "./src"
```

## PR Automation

```bash
# Automated PR review
gh pr view $PR_NUMBER --json diff | \
  codex exec --dangerously-bypass-approvals-and-sandbox \
  --json \
  "Review PR comprehensively:
  1. Code quality
  2. Security
  3. Performance
  4. Tests
  5. Documentation
  Provide actionable feedback"
```

## Related Skills

- `codex-cli`: Main integration
- `codex-git`: Git workflows
- `codex-tools`: Tool execution
