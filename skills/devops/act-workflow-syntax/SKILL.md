---
name: act-workflow-syntax
description: Use when creating or modifying GitHub Actions workflow files. Provides guidance on workflow syntax, triggers, jobs, steps, and expressions for creating valid GitHub Actions workflows that can be tested locally with act.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Act - GitHub Actions Workflow Syntax

Use this skill when creating or modifying GitHub Actions workflow files (`.github/workflows/*.yml`). This covers workflow structure, triggers, jobs, steps, and best practices for workflows that work both on GitHub and locally with act.

## Workflow File Structure

Every GitHub Actions workflow follows this basic structure:

```yaml
name: Workflow Name
on: [push, pull_request]  # Triggers

jobs:
  job-name:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Step name
        run: echo "Commands here"
```

### Top-Level Fields

- `name`: Human-readable workflow name (optional but recommended)
- `on`: Trigger events (push, pull_request, workflow_dispatch, etc.)
- `env`: Environment variables available to all jobs
- `jobs`: Map of job definitions
- `permissions`: Token permissions for the workflow

## Workflow Triggers

### Event Triggers

```yaml
# Single event
on: push

# Multiple events
on: [push, pull_request]

# Event with filters
on:
  push:
    branches:
      - main
      - 'releases/**'
    paths:
      - '**.js'
      - '!docs/**'
  pull_request:
    types: [opened, synchronize, reopened]
```

### Manual Triggers

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production
```

### Schedule Triggers

```yaml
on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9am UTC
```

## Job Configuration

### Basic Job

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test
```

### Job with Environment Variables

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      NODE_ENV: production
      API_URL: ${{ secrets.API_URL }}
    steps:
      - run: echo "Deploying to $NODE_ENV"
```

### Job Dependencies

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm run build

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  deploy:
    needs: [build, test]
    runs-on: ubuntu-latest
    steps:
      - run: npm run deploy
```

### Matrix Builds

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node: [18, 20, 22]
      fail-fast: false
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm test
```

## Steps

### Using Actions

```yaml
steps:
  # Checkout code
  - uses: actions/checkout@v4

  # Setup Node.js
  - uses: actions/setup-node@v4
    with:
      node-version: '20'
      cache: 'npm'

  # Upload artifacts
  - uses: actions/upload-artifact@v4
    with:
      name: dist
      path: dist/
```

### Running Commands

```yaml
steps:
  # Single line
  - run: npm install

  # Multi-line
  - run: |
      npm ci
      npm run build
      npm test

  # With name
  - name: Install dependencies
    run: npm ci

  # With working directory
  - run: npm test
    working-directory: ./packages/core

  # With shell
  - run: echo "Hello"
    shell: bash
```

### Conditional Steps

```yaml
steps:
  - name: Deploy to production
    if: github.ref == 'refs/heads/main'
    run: npm run deploy

  - name: Run on success
    if: success()
    run: echo "Previous steps succeeded"

  - name: Run on failure
    if: failure()
    run: echo "A step failed"

  - name: Always run
    if: always()
    run: echo "Runs regardless of status"
```

## Expressions and Contexts

### Common Contexts

```yaml
steps:
  - run: echo "Event: ${{ github.event_name }}"
  - run: echo "Branch: ${{ github.ref_name }}"
  - run: echo "SHA: ${{ github.sha }}"
  - run: echo "Actor: ${{ github.actor }}"
  - run: echo "Job status: ${{ job.status }}"
  - run: echo "Runner OS: ${{ runner.os }}"
```

### Using Secrets

```yaml
steps:
  - run: echo "Token is set"
    env:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      API_KEY: ${{ secrets.API_KEY }}
```

### Functions

```yaml
steps:
  - if: contains(github.event.head_commit.message, '[skip ci]')
    run: echo "Skipping CI"

  - if: startsWith(github.ref, 'refs/tags/')
    run: echo "This is a tag"

  - if: endsWith(github.ref, '/main')
    run: echo "This is main branch"

  - run: echo "${{ format('Hello {0}', github.actor) }}"
```

## Act-Specific Considerations

### Testing Locally with Act

```bash
# Run all workflows
act

# Run specific event
act push

# Run specific job
act -j build

# Dry run (validate without executing)
act --dryrun

# List workflows
act -l

# Use specific platform
act -P ubuntu-latest=catthehacker/ubuntu:act-latest
```

### Environment Variables for Act

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Check environment
        run: |
          if [ "$ACT" = "true" ]; then
            echo "Running in act"
          else
            echo "Running on GitHub"
          fi
```

### Secrets with Act

Create `.secrets` file for local testing:

```
GITHUB_TOKEN=ghp_your_token_here
API_KEY=your_api_key_here
```

Then run:

```bash
act --secret-file .secrets
```

Or pass secrets individually:

```bash
act -s GITHUB_TOKEN=ghp_token -s API_KEY=key
```

## Best Practices

### DO

✅ Use semantic job and step names
✅ Pin action versions (`actions/checkout@v4`)
✅ Use `fail-fast: false` for matrix builds to see all results
✅ Set appropriate `timeout-minutes` for jobs
✅ Use `working-directory` instead of cd commands
✅ Test workflows locally with `act --dryrun` before pushing
✅ Use caching for dependencies
✅ Use environments for deployment jobs

### DON'T

❌ Hardcode secrets in workflow files
❌ Use `latest` tags for actions
❌ Run workflows on every file change (use path filters)
❌ Create overly complex workflows (split into multiple files)
❌ Ignore act compatibility when using GitHub-specific features
❌ Forget to validate YAML syntax

## Common Patterns

### Build and Test

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test
      - run: npm run build
```

### Deploy on Tag

```yaml
name: Deploy
on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Get version
        id: version
        run: echo "VERSION=${GITHUB_REF#refs/tags/}" >> $GITHUB_OUTPUT
      - run: echo "Deploying ${{ steps.version.outputs.VERSION }}"
```

### Monorepo with Changed Files

```yaml
jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      api: ${{ steps.changes.outputs.api }}
      web: ${{ steps.changes.outputs.web }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v3
        id: changes
        with:
          filters: |
            api:
              - 'packages/api/**'
            web:
              - 'packages/web/**'

  build-api:
    needs: detect-changes
    if: needs.detect-changes.outputs.api == 'true'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Building API"
```

## Related Skills

- **act-local-testing**: Testing workflows locally before pushing
- **act-docker-setup**: Configuring Docker environments for act
- **act-secrets-management**: Managing secrets for local testing
