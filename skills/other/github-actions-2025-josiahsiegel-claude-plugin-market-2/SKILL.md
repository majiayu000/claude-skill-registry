---
name: github-actions-2025
description: GitHub Actions 2025 features including 1 vCPU runners, immutable releases, and Node24 migration
---

# GitHub Actions 2025 Features

## 1 vCPU Linux Runners (October 2025 - Public Preview)

**What:** New lightweight runners optimized for automation tasks with lower cost.

**Specs:**
- 1 vCPU
- 5 GB RAM
- 15-minute job limit
- Optimized for short-running tasks

### When to Use 1 vCPU Runners

**Ideal for:**
- Issue triage automation
- Label management
- PR comment automation
- Status checks
- Lightweight scripts
- Git operations (checkout, tag, commit)
- Notification tasks

**NOT suitable for:**
- Build operations
- Test suites
- Complex CI/CD pipelines
- Resource-intensive operations

### Usage

```yaml
# .github/workflows/automation.yml
name: Lightweight Automation

on:
  issues:
    types: [opened, labeled]

jobs:
  triage:
    runs-on: ubuntu-latest-1-core  # New 1 vCPU runner
    timeout-minutes: 10  # Max 15 minutes
    steps:
      - name: Triage Issue
        run: |
          echo "Triaging issue..."
          gh issue edit ${{ github.event.issue.number }} --add-label "needs-review"
```

### Cost Savings Example

```yaml
# Before: Using 2 vCPU runner for simple task
jobs:
  label:
    runs-on: ubuntu-latest  # 2 vCPU, higher cost
    steps:
      - name: Add label
        run: gh pr edit ${{ github.event.number }} --add-label "reviewed"

# After: Using 1 vCPU runner (lower cost)
jobs:
  label:
    runs-on: ubuntu-latest-1-core  # 1 vCPU, 50% cost reduction
    timeout-minutes: 5
    steps:
      - name: Add label
        run: gh pr edit ${{ github.event.number }} --add-label "reviewed"
```

## Immutable Releases (August 2025)

**What:** Releases can now be marked immutable - assets and Git tags cannot be changed or deleted once released.

**Benefits:**
- Supply chain security
- Audit compliance
- Prevent tampering
- Trust in release artifacts

### Create Immutable Release

```bash
# Using GitHub CLI
gh release create v1.0.0 \
  dist/*.zip \
  --title "Version 1.0.0" \
  --notes-file CHANGELOG.md \
  --immutable

# Verify immutability
gh release view v1.0.0 --json isImmutable
```

### GitHub Actions Workflow

```yaml
# .github/workflows/release.yml
name: Create Immutable Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Build artifacts
        run: npm run build

      - name: Create Immutable Release
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const tag = context.ref.replace('refs/tags/', '');

            await github.rest.repos.createRelease({
              owner: context.repo.owner,
              repo: context.repo.repo,
              tag_name: tag,
              name: `Release ${tag}`,
              body: fs.readFileSync('CHANGELOG.md', 'utf8'),
              draft: false,
              prerelease: false,
              make_immutable: true  # Mark as immutable
            });

      - name: Upload Release Assets
        run: gh release upload ${{ github.ref_name }} dist/*.zip --clobber
```

### Immutable Release Policy

```yaml
# Organizational policy for immutable releases
name: Enforce Immutable Releases

on:
  release:
    types: [created]

jobs:
  enforce-immutability:
    runs-on: ubuntu-latest
    if: "!github.event.release.immutable && startsWith(github.event.release.tag_name, 'v')"

    steps:
      - name: Fail if not immutable
        run: |
          echo "ERROR: Production releases must be immutable"
          exit 1
```

## Node24 Migration (September 2025)

**What:** GitHub Actions migrating from Node20 to Node24 in fall 2025.

**Timeline:**
- September 2025: Node24 support added
- October 2025: Deprecation notices for Node20
- November 2025: Node20 phase-out begins
- December 2025: Full migration to Node24

### Update Your Actions

**Check Node version in actions:**

```yaml
# Old - Node20
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-node@v3
        with:
          node-version: '20'  # Update to 24

# New - Node24
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: '24'  # Current LTS
```

### Runner Version Compatibility

```yaml
# Ensure runner supports Node24
jobs:
  test:
    runs-on: ubuntu-latest  # Runner v2.328.0+ supports Node24

    steps:
      - name: Verify Node version
        run: node --version  # Should show v24.x.x
```

### Custom Actions Migration

If you maintain custom actions:

```javascript
// action.yml
runs:
  using: 'node24'  // Updated from 'node20'
  main: 'index.js'
```

```bash
# Update dependencies
npm install @actions/core@latest
npm install @actions/github@latest

# Test with Node24
node --version  # Ensure 24.x
npm test
```

## Actions Environment Variables (May 2025)

**What:** Actions environments now available for all plans (public and private repos).

### Environment Protection Rules

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com

    steps:
      - name: Deploy
        run: |
          echo "Deploying to ${{ vars.DEPLOY_URL }}"
          # Deployment steps...
```

**Environment configuration:**
- Settings → Environments → production
- Add protection rules:
  - Required reviewers
  - Wait timer
  - Deployment branches (only main)

## Allowed Actions Policy Updates (August 2025)

**What:** Enhanced governance with explicit blocking and SHA pinning.

### Block Specific Actions

```yaml
# .github/workflows/policy.yml
# Repository or organization settings
allowed-actions:
  verified-only: true

  # Explicitly block actions
  blocked-actions:
    - 'untrusted/action@*'
    - 'deprecated-org/*'

  # Require SHA pinning for security
  require-sha-pinning: true
```

### SHA Pinning for Security

```yaml
# Before: Version pinning (can be changed by action maintainer)
- uses: actions/checkout@v4

# After: SHA pinning (immutable)
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1
```

### Generate SHA-Pinned Actions

```bash
# Get commit SHA for specific version
gh api repos/actions/checkout/commits/v4.1.1 --jq '.sha'

# Or use action-security tool
npx pin-github-action actions/checkout@v4
# Output: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11
```

## Copilot-Triggered Workflows (April 2025)

**What:** Workflows triggered by Copilot-authored events now require explicit approval.

### Configure Copilot Workflow Approval

```yaml
# .github/workflows/copilot-automation.yml
name: Copilot PR Automation

on:
  pull_request:
    types: [opened]

jobs:
  copilot-review:
    runs-on: ubuntu-latest

    # Copilot-generated PRs require approval
    if: github.event.pull_request.user.login != 'github-copilot[bot]'

    steps:
      - name: Auto-review
        run: gh pr review --approve
```

**Manual approval required for Copilot PRs** (same mechanism as fork PRs).

## Artifact Storage Architecture (February 2025)

**What:** Artifacts moved to new architecture on February 1, 2025.

**Breaking changes:**
- `actions/upload-artifact@v1-v2` retired March 1, 2025
- Must use `actions/upload-artifact@v4+`

### Migration

```yaml
# Old (Retired)
- uses: actions/upload-artifact@v2
  with:
    name: build-artifacts
    path: dist/

# New (Required)
- uses: actions/upload-artifact@v4
  with:
    name: build-artifacts
    path: dist/
    retention-days: 30
```

## Windows Server 2019 Retirement (June 2025)

**What:** `windows-2019` runner image fully retired June 30, 2025.

### Migration

```yaml
# Old
jobs:
  build:
    runs-on: windows-2019  # Retired

# New
jobs:
  build:
    runs-on: windows-2022  # Current
    # Or windows-latest (recommended)
```

## Meta API for Self-Hosted Runners (May 2025)

**What:** New `actions_inbound` section in meta API for network configuration.

```bash
# Get network requirements for self-hosted runners
curl https://api.github.com/meta | jq '.actions_inbound'

# Configure firewall rules based on response
{
  "domains": [
    "*.actions.githubusercontent.com",
    "*.pkg.github.com"
  ],
  "ip_ranges": [
    "140.82.112.0/20",
    "143.55.64.0/20"
  ]
}
```

## Best Practices for 2025

### 1. Use Appropriate Runners

```yaml
# Use 1 vCPU for lightweight tasks
jobs:
  label-management:
    runs-on: ubuntu-latest-1-core
    timeout-minutes: 5

  # Use standard runners for builds/tests
  build:
    runs-on: ubuntu-latest
```

### 2. Immutable Releases for Production

```yaml
# Always mark production releases as immutable
- name: Create Release
  run: gh release create $TAG --immutable
```

### 3. SHA Pinning for Security

```yaml
# Pin actions to SHA, not tags
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11
- uses: actions/setup-node@60edb5dd545a775178f52524783378180af0d1f8
```

### 4. Update to Node24

```yaml
# Use latest Node version
- uses: actions/setup-node@v4
  with:
    node-version: '24'
```

### 5. Environment Protection

```yaml
# Use environments for deployments
jobs:
  deploy:
    environment: production
    # Requires approval, wait timer, branch restrictions
```

## Troubleshooting

**1 vCPU runner timeout:**
```yaml
# Ensure task completes within 15 minutes
jobs:
  task:
    runs-on: ubuntu-latest-1-core
    timeout-minutes: 10  # Safety margin
```

**Node24 compatibility issues:**
```bash
# Test locally with Node24
nvm install 24
nvm use 24
npm test
```

**Artifact upload failures:**
```yaml
# Use v4 of artifact actions
- uses: actions/upload-artifact@v4  # Not v1/v2
```

## Resources

- [GitHub Actions 1 vCPU Runners](https://github.blog/changelog/2025-10-28-1-vcpu-linux-runner-now-available-in-github-actions-in-public-preview/)
- [Immutable Releases](https://github.blog/changelog/2025-08-15-github-actions-policy-now-supports-blocking-and-sha-pinning-actions/)
- [Node24 Migration](https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/)
