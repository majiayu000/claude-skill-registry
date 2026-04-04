---
name: ci-cd-integration
description: CI/CD integration - GitHub Actions, automation, pipeline integration
version: 1.0.0
author: Claude Code SDK
tags: [ci-cd, github-actions, automation, pipelines]
---

# CI/CD Integration

Integrate Claude Code into your CI/CD pipelines for automated code review, testing, quality gates, and release automation.

## Quick Reference

| Integration | Tool | Use Case |
|-------------|------|----------|
| GitHub Actions | `claude -p` | Automated PR review, test fixing |
| Pre-commit | hooks | Local validation before push |
| Quality Gates | Claude API | PR approval requirements |
| Release Automation | headless mode | Changelog, versioning |

## Core Concept

Claude Code's headless mode (`-p` flag) enables non-interactive execution in CI pipelines. Combined with GitHub Actions and hooks, you can automate code review, testing, and release workflows.

```bash
# Basic CI usage
claude -p "Review this PR diff for issues" --output-format json
```

## GitHub Actions Basics

### Minimal Workflow

```yaml
name: Claude Code Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Run Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          gh pr diff ${{ github.event.pull_request.number }} | \
          claude -p "Review this diff for bugs and improvements" \
            --output-format json > review.json
```

### Key Environment Variables

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | API authentication |
| `GITHUB_TOKEN` | GitHub API access (auto-provided) |
| `CI=true` | Indicates CI environment |

See [GITHUB-ACTIONS.md](./GITHUB-ACTIONS.md) for complete workflow examples.

## Pre-commit Integration

### Quick Setup

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: claude-review
        name: Claude Code Review
        entry: claude -p "Check this diff for obvious issues" --max-turns 1
        language: system
        stages: [pre-commit]
        pass_filenames: false
```

### Staged Files Review

```bash
#!/bin/bash
# .git/hooks/pre-commit
staged_files=$(git diff --cached --name-only)
if [ -n "$staged_files" ]; then
  git diff --cached | claude -p "Quick review of staged changes. Report only critical issues." \
    --max-turns 1 --output-format text
fi
```

See [AUTOMATION.md](./AUTOMATION.md) for more automation patterns.

## Quality Gates

### PR Approval Gate

```yaml
- name: Quality Gate
  run: |
    result=$(claude -p "Analyze PR #${{ github.event.pull_request.number }} \
      for security issues, breaking changes, and test coverage. \
      Output JSON: {\"approved\": boolean, \"blockers\": string[]}" \
      --output-format json --json-schema '...')

    if [ "$(echo $result | jq -r '.structured_output.approved')" != "true" ]; then
      echo "Quality gate failed"
      exit 1
    fi
```

### Test Coverage Gate

```yaml
- name: Coverage Analysis
  run: |
    bun test --coverage > coverage.txt
    claude -p "Analyze coverage report. Fail if coverage < 80% \
      or critical paths uncovered." < coverage.txt
```

See [PIPELINES.md](./PIPELINES.md) for pipeline integration patterns.

## Automated Review Workflow

### Standard PR Review

```yaml
name: Automated PR Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get PR Diff
        run: gh pr diff ${{ github.event.pull_request.number }} > diff.txt
        env:
          GH_TOKEN: ${{ github.token }}

      - name: Claude Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          review=$(claude -p "Review this PR diff. Focus on:
          - Security vulnerabilities
          - Logic errors
          - Performance issues
          - Missing error handling

          Format as markdown with sections." < diff.txt)

          gh pr comment ${{ github.event.pull_request.number }} --body "$review"
        env:
          GH_TOKEN: ${{ github.token }}
```

## Test Automation

### Fix Failing Tests

```yaml
- name: Run Tests
  id: tests
  continue-on-error: true
  run: bun test 2>&1 | tee test-output.txt

- name: Fix Failing Tests
  if: steps.tests.outcome == 'failure'
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  run: |
    claude -p "Fix the failing tests. Test output:
    $(cat test-output.txt)

    Make minimal changes to fix the tests." \
    --allowedTools "Read,Edit,Bash(bun test:*)"
```

### Generate Missing Tests

```yaml
- name: Generate Tests for Changed Files
  run: |
    changed_files=$(git diff --name-only origin/main...HEAD -- '*.ts' '*.tsx')
    for file in $changed_files; do
      claude -p "Generate comprehensive tests for $file if none exist" \
        --allowedTools "Read,Write,Glob"
    done
```

## Release Automation

### Changelog Generation

```yaml
- name: Generate Changelog
  run: |
    claude -p "Generate changelog from commits since last release:
    $(git log $(git describe --tags --abbrev=0)..HEAD --oneline)

    Format: Conventional changelog with Breaking, Features, Fixes sections." \
    --output-format text > CHANGELOG_ENTRY.md
```

### Version Bumping

```yaml
- name: Determine Version Bump
  run: |
    bump=$(claude -p "Analyze commits since last tag. Output only: major, minor, or patch
    $(git log $(git describe --tags --abbrev=0)..HEAD --oneline)" \
    --output-format text)

    npm version $bump --no-git-tag-version
```

## Security Scanning

### Code Security Review

```yaml
- name: Security Scan
  run: |
    claude -p "Security audit of changes in this PR:
    $(gh pr diff ${{ github.event.pull_request.number }})

    Check for:
    - SQL injection
    - XSS vulnerabilities
    - Hardcoded secrets
    - Insecure dependencies
    - Authentication issues

    Output JSON: {\"secure\": boolean, \"issues\": [{\"severity\": string, \"description\": string, \"line\": number}]}" \
    --output-format json > security.json
```

## Best Practices

### CI Performance

| Practice | Benefit |
|----------|---------|
| Use `--max-turns 1-3` | Predictable execution time |
| Limit tools with `--allowedTools` | Faster, safer execution |
| Cache Claude installation | Faster workflow starts |
| Use `--output-format json` | Reliable parsing |

### Security

| Practice | Implementation |
|----------|----------------|
| Store API keys as secrets | `${{ secrets.ANTHROPIC_API_KEY }}` |
| Limit tool permissions | `--allowedTools "Read,Grep"` |
| Avoid `--dangerously-skip-permissions` | Use explicit tool lists |
| Validate Claude output | Parse JSON, check structure |

### Cost Management

| Practice | Benefit |
|----------|---------|
| Filter files before review | Fewer tokens |
| Use targeted prompts | Focused analysis |
| Set `--max-turns` | Bounded execution |
| Skip generated files | Reduce noise |

## Common Patterns

### Conditional Review

```yaml
- name: Check for High-Risk Changes
  id: risk
  run: |
    if gh pr diff ${{ github.event.pull_request.number }} | grep -q "security\|auth\|password"; then
      echo "high_risk=true" >> $GITHUB_OUTPUT
    fi

- name: Deep Security Review
  if: steps.risk.outputs.high_risk == 'true'
  run: claude -p "Deep security review..." --max-turns 5
```

### Multi-Stage Review

```yaml
jobs:
  quick-check:
    runs-on: ubuntu-latest
    steps:
      - name: Fast Lint Check
        run: claude -p "Quick lint check" --max-turns 1

  deep-review:
    needs: quick-check
    runs-on: ubuntu-latest
    steps:
      - name: Comprehensive Review
        run: claude -p "Full code review" --max-turns 5
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| API key not found | Check `secrets.ANTHROPIC_API_KEY` is set |
| Timeout in CI | Add `--max-turns` limit |
| Permission denied | Use `--allowedTools` instead of skip-permissions |
| JSON parse error | Use `jq` to validate output |
| PR comment fails | Check `permissions: pull-requests: write` |

## Reference Files

| File | Contents |
|------|----------|
| [GITHUB-ACTIONS.md](./GITHUB-ACTIONS.md) | Complete GitHub Actions workflows |
| [AUTOMATION.md](./AUTOMATION.md) | Pre-commit, scheduled tasks, triggers |
| [PIPELINES.md](./PIPELINES.md) | Pipeline integration, quality gates |
