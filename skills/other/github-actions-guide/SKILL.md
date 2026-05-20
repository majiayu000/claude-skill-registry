---
name: github-actions-guide
description: >
  Guide for writing GitHub Actions workflows with triggers, reusable workflows, matrix strategies,
  caching, secrets, and composite actions. Use when the user creates or modifies GitHub Actions
  workflows, asks about CI/CD on GitHub, or needs help with workflow syntax. Trigger whenever
  GitHub Actions, .github/workflows, or CI pipelines on GitHub are mentioned.
---

# GitHub Actions Guide

Write efficient, secure, and maintainable GitHub Actions workflows with proper caching,
secret management, reusable components, and matrix testing strategies.

## When to Use
- User creates or modifies files in `.github/workflows/`
- User asks about CI/CD pipelines on GitHub
- User needs matrix testing across versions or platforms
- User wants to share workflow logic across repositories
- User asks about GitHub Actions caching or secrets

## Core Patterns

### Standard CI Workflow

A well-structured CI workflow with caching, linting, testing, and building.

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}

permissions:
  contents: read

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck

  test:
    runs-on: ubuntu-latest
    needs: lint
    strategy:
      matrix:
        node-version: [18, 20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: npm
      - run: npm ci
      - run: npm test -- --coverage
      - uses: actions/upload-artifact@v4
        if: matrix.node-version == 20
        with:
          name: coverage
          path: coverage/

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: dist/
```

### Matrix Strategy

Test across multiple dimensions -- versions, operating systems, or configurations.

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ["3.10", "3.11", "3.12"]
        exclude:
          - os: windows-latest
            python-version: "3.10"
        include:
          - os: ubuntu-latest
            python-version: "3.12"
            coverage: true
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip
      - run: pip install -r requirements.txt
      - run: pytest --cov=${{ matrix.coverage && '--cov-report=xml' || '' }}
```

### Reusable Workflow

Extract common workflow logic into callable workflows.

```yaml
# .github/workflows/reusable-deploy.yml
name: Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      image-tag:
        required: true
        type: string
    secrets:
      AWS_ROLE_ARN:
        required: true

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1
      - run: |
          aws ecs update-service \
            --cluster ${{ inputs.environment }} \
            --service api \
            --force-new-deployment
```

Caller workflow:

```yaml
jobs:
  deploy-staging:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: staging
      image-tag: ${{ github.sha }}
    secrets:
      AWS_ROLE_ARN: ${{ secrets.STAGING_AWS_ROLE_ARN }}
```

### Composite Action

Bundle multiple steps into a reusable action for shared setup logic.

```yaml
# .github/actions/setup-project/action.yml
name: Setup Project
description: Install dependencies and configure environment

inputs:
  node-version:
    description: Node.js version
    default: "20"

runs:
  using: composite
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: npm
    - run: npm ci
      shell: bash
    - run: cp .env.example .env.test
      shell: bash
```

Usage: `- uses: ./.github/actions/setup-project`

## Anti-Patterns

- **Not pinning action versions**: Use `@v4` at minimum, or pin to a full SHA for critical actions. Never use `@main` or `@latest`.
- **Storing secrets in code**: Use GitHub Secrets or OIDC. Never hardcode credentials in workflow files.
- **No concurrency control**: Without `concurrency`, multiple pushes trigger redundant runs. Always cancel in-progress runs on PRs.
- **Overly broad permissions**: Set `permissions` at the workflow or job level. Default `contents: read` and add only what is needed.
- **Not caching dependencies**: Every job starts fresh. Use built-in caching (`cache: npm`) or `actions/cache` to avoid reinstalling deps every run.
- **Running everything sequentially**: Use `needs` to parallelize independent jobs. Lint and test can run in parallel.

## Quick Reference

```yaml
# Triggers
on:
  push: { branches: [main] }           # Push to main
  pull_request: { branches: [main] }   # PR targeting main
  schedule: [{ cron: "0 6 * * 1" }]    # Weekly Monday 6am
  workflow_dispatch: {}                  # Manual trigger
  workflow_call: {}                      # Called by another workflow

# Conditions
if: github.event_name == 'push'
if: contains(github.event.head_commit.message, '[skip ci]') == false
if: github.actor != 'dependabot[bot]'

# Common caching
- uses: actions/setup-node@v4
  with: { cache: npm }
- uses: actions/setup-python@v5
  with: { cache: pip }
- uses: actions/setup-go@v5
  with: { cache: true }
```
