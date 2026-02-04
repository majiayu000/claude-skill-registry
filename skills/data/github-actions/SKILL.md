# GitHub Actions Skill

## Purpose

Master GitHub Actions workflow patterns, triggers, optimization, and best practices for CI/CD pipelines.

## Workflow Structure

### Basic Anatomy
```yaml
name: Workflow Name          # Display name in GitHub UI

on:                          # Trigger events
  push:
    branches: [main]

permissions:                 # Required permissions (use minimal)
  contents: read
  pull-requests: write

jobs:                        # One or more jobs
  job-id:                   # Unique job identifier
    runs-on: ubuntu-latest   # Runner environment
    steps:                   # Sequential steps
      - name: Step name
        run: command
```

## Common Triggers

### Push Events
```yaml
# Push to any branch
on: push

# Push to specific branches
on:
  push:
    branches:
      - main
      - develop

# Push to branches matching pattern
on:
  push:
    branches:
      - 'releases/**'
      - 'feature/*'

# Exclude branches
on:
  push:
    branches-ignore:
      - 'docs/**'
```

### Pull Request Events
```yaml
# Any pull request
on: pull_request

# PR to specific branches
on:
  pull_request:
    branches: [main]

# PR types
on:
  pull_request:
    types: [opened, synchronize, reopened, closed]
```

### Manual and Scheduled Triggers
```yaml
# Manual trigger (workflow_dispatch)
on: workflow_dispatch

# With inputs
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        type: choice
        options:
          - dev
          - staging
          - production

# Scheduled (cron)
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
    - cron: '0 */6 * * *'  # Every 6 hours
```

## Optimization Patterns

### Dependency Caching
```yaml
# Automatic npm caching (recommended)
- uses: actions/setup-node@v3
  with:
    node-version: '18'
    cache: 'npm'

# Manual caching (more control)
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### Build Artifact Caching
```yaml
- name: Cache build
  uses: actions/cache@v3
  with:
    path: build/
    key: build-${{ github.sha }}

- name: Upload artifacts
  uses: actions/upload-artifact@v3
  with:
    name: build-files
    path: build/
    retention-days: 7
```

### Parallel Jobs
```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: npm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  build:
    runs-on: ubuntu-latest
    needs: [lint, test]  # Wait for lint and test
    steps:
      - run: npm run build
```

## Conditional Execution

### If Conditions
```yaml
# Run only on push to main
- name: Deploy
  if: github.ref == 'refs/heads/main'
  run: npm run deploy

# Run only on pull requests
- name: Preview
  if: github.event_name == 'pull_request'
  run: npm run preview

# Run only on merged PR
- name: Cleanup
  if: github.event.pull_request.merged == true
  run: ./cleanup.sh

# Complex conditions
- name: Deploy to prod
  if: |
    github.ref == 'refs/heads/main' &&
    github.event_name == 'push' &&
    !contains(github.event.head_commit.message, '[skip ci]')
  run: deploy
```

## Environment Variables and Secrets

### Using Secrets
```yaml
env:
  # Global environment variables
  NODE_VERSION: '18'
  API_KEY: ${{ secrets.API_KEY }}

jobs:
  deploy:
    steps:
      - name: Deploy with secrets
        env:
          # Step-specific environment variables
          FIREBASE_TOKEN: ${{ secrets.FIREBASE_TOKEN }}
          API_URL: ${{ secrets.API_URL }}
        run: |
          echo "Deploying..."
          firebase deploy --token $FIREBASE_TOKEN
```

### GitHub Context Variables
```yaml
# Common context variables
${{ github.repository }}     # owner/repo
${{ github.ref }}            # refs/heads/main
${{ github.sha }}            # commit SHA
${{ github.event_name }}     # push, pull_request, etc.
${{ github.actor }}          # User who triggered workflow
${{ github.run_id }}         # Unique run ID

# Pull request specific
${{ github.event.pull_request.number }}
${{ github.event.pull_request.title }}
${{ github.head_ref }}       # PR source branch
${{ github.base_ref }}       # PR target branch
```

## Matrix Builds

### Test Multiple Versions
```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node-version: [16, 18, 20]
    steps:
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm test
```

### Matrix with Exclusions
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node: [16, 18, 20]
    exclude:
      - os: windows-latest
        node: 16  # Skip Windows + Node 16
```

## Common Patterns

### React App CI
```yaml
name: React CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Test
        run: npm test -- --coverage --watchAll=false
        env:
          CI: true

      - name: Build
        run: npm run build
```

### Deployment with Approval
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://myapp.com
    steps:
      - run: npm run deploy
```

### Conditional Deployment
```yaml
jobs:
  deploy:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: ./deploy.sh
```

## Performance Optimization

### Fast npm Install
```yaml
# ✅ Use npm ci (faster, more reliable)
- run: npm ci

# ❌ Don't use npm install in CI
- run: npm install  # Slower, non-deterministic
```

### Caching Strategy
```yaml
# Cache node_modules
- uses: actions/cache@v3
  with:
    path: node_modules
    key: ${{ runner.os }}-npm-${{ hashFiles('package-lock.json') }}

# Cache .npm directory (smaller, faster)
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('package-lock.json') }}
```

### Skip Unnecessary Runs
```yaml
# Skip CI for docs-only changes
on:
  push:
    paths-ignore:
      - '**.md'
      - 'docs/**'

# Run only for specific paths
on:
  push:
    paths:
      - 'src/**'
      - 'package*.json'
```

## Best Practices

### ✅ Do
- Use `npm ci` not `npm install`
- Cache dependencies
- Set specific Node version
- Use latest action versions (`@v3`, `@v4`)
- Set minimal permissions
- Quote strings with special characters
- Use meaningful job and step names

### ❌ Don't
- Hardcode secrets in workflow files
- Use deprecated actions
- Skip dependency caching
- Use `npm install` in CI
- Leave complex workflows undocumented
- Ignore workflow failures

## Debugging Workflows

```bash
# View workflow runs
gh run list --workflow=workflow-name.yml

# View specific run with logs
gh run view RUN_ID --log

# Re-run failed workflow
gh run rerun RUN_ID

# Download logs
gh run download RUN_ID

# Watch workflow in real-time
gh run watch
```

## Common Issues

**Issue**: Workflow not triggering
**Solution**: Check trigger conditions, branch names, path filters

**Issue**: `npm ci` fails
**Solution**: Ensure package-lock.json is committed, check Node version

**Issue**: Secrets not available
**Solution**: Verify secret exists (`gh secret list`), check spelling

**Issue**: Slow builds
**Solution**: Enable caching, use `npm ci`, parallelize jobs

## Project Usage

Music-app workflows:
- `trunk-based-checks.yml`: PR validation, testing, build verification
- `firebase-hosting-merge.yml`: Production deployment (manual trigger)
- `firebase-hosting-pull-request.yml`: PR preview (manual trigger)

All workflows use Node 18, npm caching, and trunk-based development checks.
