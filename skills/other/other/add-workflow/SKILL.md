---
name: add-workflow
description: Create a GitHub Actions workflow following x4-mono CI patterns
---

# Add Workflow Skill

Create a new GitHub Actions workflow for x4-mono.

## Arguments

The user describes the workflow. If unclear, ask for:

- Workflow name and purpose
- Trigger events (push, PR, schedule, manual)
- Which workspaces/paths should trigger it
- Required secrets or environment variables

## File Location

`.github/workflows/{name}.yml`

## Workflow Template

Reference: `.github/workflows/ci.yml`

```yaml
name: Workflow Name

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  job-name:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: oven-sh/setup-bun@v2
        with:
          bun-version: '1.3.8'

      - uses: actions/cache@v5
        with:
          path: ~/.bun/install/cache
          key: bun-${{ runner.os }}-${{ hashFiles('bun.lock') }}
          restore-keys: |
            bun-${{ runner.os }}-

      - run: bun install --frozen-lockfile

      - run: # your command here
```

## Common Patterns

### Path Filtering (only run when relevant files change)

```yaml
jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      api: ${{ steps.filter.outputs.api }}
      web: ${{ steps.filter.outputs.web }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            api:
              - 'apps/api/**'
              - 'packages/**'
            web:
              - 'apps/web/**'
              - 'packages/**'

  api-tests:
    needs: changes
    if: needs.changes.outputs.api == 'true'
    # ...
```

### CI Gate (require all jobs pass)

```yaml
ci-passed:
  needs: [quality, api-tests, web-tests]
  if: always()
  runs-on: ubuntu-latest
  steps:
    - run: |
        if [[ "${{ contains(needs.*.result, 'failure') }}" == "true" ]]; then
          exit 1
        fi
```

### Neon Branch (PR database isolation)

```yaml
neon-branch:
  if: github.event_name == 'pull_request'
  runs-on: ubuntu-latest
  outputs:
    db_url: ${{ steps.create-branch.outputs.db_url }}
  steps:
    - uses: neondatabase/create-branch-action@v6
      id: create-branch
      with:
        project_id: ${{ secrets.NEON_PROJECT_ID }}
        api_key: ${{ secrets.NEON_API_KEY }}
        branch_name: pr-${{ github.event.number }}
```

### Manual Trigger with Inputs

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        type: choice
        options:
          - staging
          - production
```

### Scheduled

```yaml
on:
  schedule:
    - cron: '0 6 * * 1' # Every Monday at 6 AM UTC
```

## Conventions

- Always use `actions/checkout@v4`
- Always use `oven-sh/setup-bun@v2` with pinned version
- Always cache Bun install cache
- Always use `--frozen-lockfile` for installs
- Use concurrency with `cancel-in-progress: true`
- Gate jobs on path filters to avoid unnecessary runs
- Include a `ci-passed` gate if there are multiple parallel jobs

## Workflow

1. Read `.github/workflows/ci.yml` to understand existing patterns
2. Create new workflow file at `.github/workflows/{name}.yml`
3. Configure triggers, path filters, and concurrency
4. Add Bun setup + cache steps
5. Add job-specific steps
6. Add CI gate job if there are multiple parallel jobs
7. Test by pushing to a branch or using `act` locally
