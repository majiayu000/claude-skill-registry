---
name: workflow-development
description: Create, debug, and optimize GitHub Actions workflows with security best practices. USE THIS SKILL when user says "create workflow", "fix workflow", "workflow fails", "add CI", "reusable workflow", or needs help with GitHub Actions.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Workflow Development Skill

## Purpose

Create, debug, and optimize GitHub Actions workflows with security best practices.

## Triggers

- "create a CI workflow"
- "add a release workflow"
- "my workflow is failing"
- "make this workflow reusable"
- "workflow security audit"
- "add [language] CI"

## Usage

Invoke this skill to create new CI/CD workflows, debug failing workflows, or convert existing workflows to use reusable patterns with proper SHA pinning and minimal permissions.

## Security Requirements (Non-Negotiable)

### SHA Pinning

```yaml
# CORRECT
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2

# WRONG - Never use tags
- uses: actions/checkout@v4
```

### Minimal Permissions

```yaml
permissions:
  contents: read  # Start with minimum

# Only add what's needed:
# pull-requests: write  # For PR comments
# packages: write       # For container registry
```

## Reusable Workflow Pattern

### Caller (in project)

```yaml
name: CI
on: [push, pull_request]

jobs:
  ci:
    uses: zircote/.github/.github/workflows/reusable-ci-python.yml@main
    with:
      python-version: '3.12'
      coverage-threshold: 80
    secrets: inherit
```

### Reusable Definition (in .github repo)

```yaml
name: Reusable Python CI

on:
  workflow_call:
    inputs:
      python-version:
        required: false
        type: string
        default: '3.12'
      coverage-threshold:
        required: false
        type: number
        default: 80

permissions:
  contents: read

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
      - uses: zircote/.github/actions/setup-python-uv@main
        with:
          python-version: ${{ inputs.python-version }}
      - run: uv run ruff check .
```

## Available Reusable Workflows

| Workflow | Purpose |
|----------|---------|
| `reusable-ci-python.yml` | Python with uv, ruff, pyright, pytest |
| `reusable-ci-typescript.yml` | TypeScript with pnpm, ESLint, Vitest |
| `reusable-ci-go.yml` | Go with golangci-lint |
| `reusable-release.yml` | Semantic release |
| `reusable-security.yml` | Gitleaks + dependency scanning |
| `reusable-docs.yml` | Documentation deployment |
| `reusable-content.yml` | Content validation |

## Composite Action Pattern

```yaml
# action.yml
name: 'Setup Python with uv'
description: 'Install Python and uv with caching'

inputs:
  python-version:
    required: false
    default: '3.12'

runs:
  using: 'composite'
  steps:
    - uses: astral-sh/setup-uv@v4
      with:
        enable-cache: true
    - shell: bash
      run: uv python install ${{ inputs.python-version }}
```

## Debugging Workflows

### Common Failures

| Error | Cause | Fix |
|-------|-------|-----|
| "Resource not accessible" | Missing permission | Add to `permissions:` |
| Cache never hits | Wrong key | Check hashFiles path |
| Secrets unavailable | Wrong context | Use `secrets: inherit` |
| Workflow not triggered | Event mismatch | Check `on:` config |

### Debug Step

```yaml
- name: Debug
  run: |
    echo "Event: ${{ github.event_name }}"
    echo "Ref: ${{ github.ref }}"
    echo "Actor: ${{ github.actor }}"
```

## Validation

```bash
# Validate SHA pinning
./scripts/validate-sha-pinning.sh .github/workflows/

# Check for unpinned actions
grep -rn "uses:.*@v[0-9]" .github/workflows/

# Validate workflow structure
./scripts/validate-workflows.sh .github/workflows/
```

## Performance Optimization

### Caching

```yaml
- uses: actions/cache@0c907a75c2c80ebcb7f088228285e798b750cf8f
  with:
    path: ~/.cache/uv
    key: ${{ runner.os }}-uv-${{ hashFiles('uv.lock') }}
```

### Matrix Builds

```yaml
strategy:
  fail-fast: false
  matrix:
    os: [ubuntu-latest, macos-latest]
    python: ['3.11', '3.12']
```

### Concurrency

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```
