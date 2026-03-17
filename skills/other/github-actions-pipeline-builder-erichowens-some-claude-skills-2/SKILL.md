---
name: github-actions-pipeline-builder
description: Build production CI/CD pipelines with GitHub Actions. Implements matrix builds, caching, deployments, testing, security scanning. Use for automated testing, deployments, release workflows. Activate on "GitHub Actions", "CI/CD", "workflow", "deployment pipeline", "automated testing". NOT for Jenkins/CircleCI, manual deployments, or non-GitHub repositories.
allowed-tools: Read,Write,Edit,Bash
---

# GitHub Actions Pipeline Builder

Expert in building production-grade CI/CD pipelines with GitHub Actions that are fast, reliable, and secure.

## When to Use

✅ **Use for**:
- Automated testing on every commit
- Deployment to staging/production
- Docker image building and publishing
- Release automation with versioning
- Security scanning and dependency audits
- Code quality checks (linting, type checking)
- Multi-environment workflows

❌ **NOT for**:
- Non-GitHub repositories (use Jenkins, CircleCI, etc.)
- Complex pipelines better suited for dedicated CI/CD tools
- Self-hosted runners (covered in advanced patterns)

## Quick Decision Tree

```
Does your project need:
├── Testing on every PR? → GitHub Actions
├── Automated deployments? → GitHub Actions
├── Matrix builds (Node 16, 18, 20)? → GitHub Actions
├── Secrets management? → GitHub Actions secrets
├── Multi-cloud deployments? → GitHub Actions + OIDC
└── Sub-second builds? → Consider build caching
```

---

## Technology Selection

### GitHub Actions vs Alternatives

**Why GitHub Actions in 2024**:
- **Native integration**: No third-party setup
- **Free for public repos**: 2000 minutes/month for private
- **Matrix builds**: Test multiple versions in parallel
- **Marketplace**: 10,000+ pre-built actions
- **OIDC support**: Keyless cloud deployments

**Timeline**:
- 2019: GitHub Actions released
- 2020: Became standard for OSS projects
- 2022: OIDC support for secure cloud auth
- 2024: De facto CI/CD for GitHub repos

### When to Use Alternatives

| Scenario | Use | Why |
|----------|-----|-----|
| Self-hosted GitLab | GitLab CI | Native integration |
| Complex enterprise workflows | Jenkins | More flexible |
| Bitbucket repos | Bitbucket Pipelines | Native integration |
| Extremely large repos (&gt;10GB) | BuildKite | Better for monorepos |

---

## Common Anti-Patterns

### Anti-Pattern 1: No Dependency Caching

**Novice thinking**: "Install dependencies fresh every time for consistency"

**Problem**: Wastes 2-5 minutes per build installing unchanged dependencies.

**Wrong approach**:
```yaml
# ❌ Slow: Downloads all dependencies every run
- name: Install dependencies
  run: npm install
```

**Correct approach**:
```yaml
# ✅ Fast: Cache dependencies, only download changes
- name: Cache node_modules
  uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-

- name: Install dependencies
  run: npm ci  # Faster than npm install
```

**Impact**: Reduces install time from 3 minutes → 30 seconds.

**Timeline**:
- Pre-2020: Most workflows had no caching
- 2020+: Caching became standard
- 2024: Setup actions include built-in caching

---

### Anti-Pattern 2: Duplicate YAML (No Matrix Builds)

**Problem**: Copy-paste workflows for different Node versions.

**Wrong approach**:
```yaml
# ❌ Duplicated workflows
jobs:
  test-node-16:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 16
      - run: npm test

  test-node-18:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm test

  test-node-20:
    # ... same steps again
```

**Correct approach**:
```yaml
# ✅ DRY: Matrix build
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20]
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      - run: npm ci
      - run: npm test
```

**Benefits**: 66% less YAML, tests run in parallel.

---

### Anti-Pattern 3: Secrets in Code

**Problem**: Hardcoded API keys, tokens visible in repo.

**Symptoms**: Security scanner alerts, leaked credentials.

**Correct approach**:
```yaml
# ✅ Use GitHub Secrets
- name: Deploy to production
  env:
    API_KEY: ${{ secrets.PRODUCTION_API_KEY }}
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY }}
  run: |
    ./deploy.sh
```

**Setting secrets**:
1. Repo Settings → Secrets and variables → Actions
2. New repository secret
3. Name: `PRODUCTION_API_KEY`, Value: `sk-...`

**Timeline**:
- Pre-2022: Some teams committed .env files
- 2022+: GitHub secret scanning blocks commits with keys
- 2024: OIDC eliminates need for long-lived credentials

---

### Anti-Pattern 4: No Failure Notifications

**Problem**: CI fails silently, team doesn't notice for hours.

**Correct approach**:
```yaml
# ✅ Slack notification on failure
- name: Notify on failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "❌ Build failed: ${{ github.event.head_commit.message }}",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Build Failed*\n<${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|View logs>"
            }
          }
        ]
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

---

### Anti-Pattern 5: Running All Tests on Every Commit

**Problem**: Slow feedback loop (10+ minute test suites).

**Symptom**: Developers avoid committing frequently.

**Correct approach**:
```yaml
# ✅ Fast feedback: Run subset on PR, full suite on merge
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  quick-tests:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - run: npm run test:unit  # Fast: 2 minutes

  full-tests:
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - run: npm run test  # Slow: 10 minutes (unit + integration + e2e)
```

**Alternative**: Use changed-files action to run only affected tests.

---

## Implementation Patterns

### Pattern 1: Basic CI Pipeline

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run type check
        run: npm run typecheck

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build
```

### Pattern 2: Multi-Environment Deployment

```yaml
name: Deploy

on:
  push:
    branches:
      - main        # → staging
      - production  # → production

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ github.ref_name }}  # staging or production

    steps:
      - uses: actions/checkout@v3

      - name: Deploy to ${{ github.ref_name }}
        run: |
          if [ "${{ github.ref_name }}" == "production" ]; then
            ./deploy.sh production
          else
            ./deploy.sh staging
          fi
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

### Pattern 3: Release Automation

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'  # Trigger on version tags (v1.0.0)

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write  # Required for creating releases

    steps:
      - uses: actions/checkout@v3

      - name: Build artifacts
        run: npm run build

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            dist/**
          body: |
            ## What's Changed
            See CHANGELOG.md for details.
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Publish to npm
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Pattern 4: Docker Build & Push

```yaml
name: Docker

on:
  push:
    branches: [main]

jobs:
  build-and-push:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to DockerHub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            myapp:latest
            myapp:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

## Production Checklist

```
□ Dependency caching configured
□ Matrix builds for multiple versions
□ Secrets stored in GitHub Secrets (not code)
□ Failure notifications (Slack, email, etc.)
□ Deploy previews for pull requests
□ Staging → Production promotion workflow
□ Release automation with versioning
□ Docker layer caching enabled
□ CODEOWNERS file for required reviews
□ Branch protection rules enabled
□ Status checks required before merge
□ Security scanning (Dependabot, CodeQL)
```

---

## When to Use vs Avoid

| Scenario | Use GitHub Actions? |
|----------|---------------------|
| GitHub-hosted repo | ✅ Yes |
| Need matrix builds | ✅ Yes |
| Deploying to AWS/GCP/Azure | ✅ Yes (with OIDC) |
| GitLab repo | ❌ No - use GitLab CI |
| Extremely large monorepo | ⚠️ Maybe - consider BuildKite |
| Need GUI pipeline builder | ❌ No - use Jenkins/Azure DevOps |

---

## References

- `/references/advanced-caching.md` - Cache strategies for faster builds
- `/references/oidc-deployments.md` - Keyless cloud authentication
- `/references/security-hardening.md` - Security best practices

## Scripts

- `scripts/workflow_validator.ts` - Validate YAML syntax locally
- `scripts/action_usage_analyzer.ts` - Find outdated actions

## Assets

- `assets/workflows/` - Ready-to-use workflow templates

---

**This skill guides**: CI/CD pipelines | GitHub Actions workflows | Matrix builds | Caching | Deployments | Release automation

