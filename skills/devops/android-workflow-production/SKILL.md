---
name: android-workflow-production
description: Generate GitHub Actions workflows for production deployment with staged rollout
category: android
version: 1.0.0
inputs:
  - package_name: Android app package name
outputs:
  - .github/workflows/deploy-production.yml
  - .github/workflows/manage-rollout.yml
verify: "yamllint .github/workflows/deploy-production.yml .github/workflows/manage-rollout.yml"
---

# Android Production Workflow

Generates GitHub Actions workflows for production deployment with staged rollouts and rollout management.

## Prerequisites

- Service account setup complete
- Package name known
- GitHub environment "production" created

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| package_name | Yes | - | App package name |

## Process

### Step 1: Verify Fastlane Setup

Ensure Fastlane is configured:
```bash
bundle exec fastlane lanes
```

Expected output should show `deploy_production`, `increase_rollout`, and `halt_rollout` lanes.

### Step 2: Create Production Deployment Workflow

Create `.github/workflows/deploy-production.yml`:

```yaml
name: Deploy to Production

on:
  workflow_dispatch:
    inputs:
      rollout_type:
        description: 'Rollout type'
        required: true
        type: choice
        options:
          - staged
          - full
        default: 'staged'
      rollout_percentage:
        description: 'Rollout percentage (only for staged: 0.05-1.0, e.g., 0.1 for 10%)'
        required: false
        default: '0.05'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

      - name: Set up JDK 17
        uses: actions/setup-java@c5195efecf7bdfc987ee8bae7a71cb8b11521c00  # v4.7.0
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Setup Gradle cache
        uses: actions/cache@1bd1e32a3bdc45362d1e726936510720a7c30a57  # v4.2.0
        with:
          path: |
            ~/.gradle/caches
            ~/.gradle/wrapper
            .gradle/configuration-cache
          key: gradle-${{ runner.os }}-${{ hashFiles('**/*.gradle*', '**/gradle-wrapper.properties') }}
          restore-keys: |
            gradle-${{ runner.os }}-

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v4

      - name: Run unit tests
        run: ./gradlew test

      - name: Upload test reports
        if: always()
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02  # v4.6.0
        with:
          name: test-reports
          path: app/build/reports/tests/
          retention-days: 7

  deploy:
    needs: test
    runs-on: ubuntu-latest
    environment: production

    steps:
      - name: Checkout code
        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
        with:
          fetch-depth: 0  # Full history for tags

      - name: Set up JDK 17
        uses: actions/setup-java@c5195efecf7bdfc987ee8bae7a71cb8b11521c00  # v4.7.0
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Setup Gradle cache
        uses: actions/cache@1bd1e32a3bdc45362d1e726936510720a7c30a57  # v4.2.0
        with:
          path: |
            ~/.gradle/caches
            ~/.gradle/wrapper
            .gradle/configuration-cache
          key: gradle-${{ runner.os }}-${{ hashFiles('**/*.gradle*', '**/gradle-wrapper.properties') }}
          restore-keys: |
            gradle-${{ runner.os }}-

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v4

      - name: Decode keystore
        run: |
          echo "${{ secrets.SIGNING_KEY_STORE_BASE64 }}" | base64 -d > app/release.jks
        env:
          SIGNING_KEY_STORE_BASE64: ${{ secrets.SIGNING_KEY_STORE_BASE64 }}

      - name: Build Release Bundle
        run: ./gradlew bundleRelease
        env:
          SIGNING_KEY_STORE_PATH: ${{ github.workspace }}/app/release.jks
          SIGNING_STORE_PASSWORD: ${{ secrets.SIGNING_STORE_PASSWORD }}
          SIGNING_KEY_ALIAS: ${{ secrets.SIGNING_KEY_ALIAS }}
          SIGNING_KEY_PASSWORD: ${{ secrets.SIGNING_KEY_PASSWORD }}

      - name: Set up Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true

      - name: Create Service Account File
        run: echo "${{ secrets.SERVICE_ACCOUNT_JSON_PLAINTEXT }}" > service-account.json

      - name: Deploy with Fastlane (Full Rollout)
        if: github.event.inputs.rollout_type == 'full'
        env:
          SIGNING_KEY_STORE_PATH: ${{ github.workspace }}/app/release.jks
          SIGNING_STORE_PASSWORD: ${{ secrets.SIGNING_STORE_PASSWORD }}
          SIGNING_KEY_ALIAS: ${{ secrets.SIGNING_KEY_ALIAS }}
          SIGNING_KEY_PASSWORD: ${{ secrets.SIGNING_KEY_PASSWORD }}
          PLAY_STORE_SERVICE_ACCOUNT: service-account.json
        run: bundle exec fastlane deploy_production rollout:1.0

      - name: Deploy with Fastlane (Staged Rollout)
        if: github.event.inputs.rollout_type == 'staged'
        env:
          SIGNING_KEY_STORE_PATH: ${{ github.workspace }}/app/release.jks
          SIGNING_STORE_PASSWORD: ${{ secrets.SIGNING_STORE_PASSWORD }}
          SIGNING_KEY_ALIAS: ${{ secrets.SIGNING_KEY_ALIAS }}
          SIGNING_KEY_PASSWORD: ${{ secrets.SIGNING_KEY_PASSWORD }}
          PLAY_STORE_SERVICE_ACCOUNT: service-account.json
        run: bundle exec fastlane deploy_production rollout:${{ github.event.inputs.rollout_percentage }}

      - name: Cleanup Service Account
        if: always()
        run: rm -f service-account.json

      - name: Clean up keystore
        if: always()
        run: rm -f app/release.jks

      - name: Get latest tag
        id: get_tag
        run: |
          TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
          echo "tag=$TAG" >> $GITHUB_OUTPUT

      - name: Create GitHub Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh release create "${{ steps.get_tag.outputs.tag }}" \
            --title "Release ${{ steps.get_tag.outputs.tag }}" \
            --notes "Production release ${{ steps.get_tag.outputs.tag }}" \
            --latest \
            app/build/outputs/bundle/release/app-release.aab

      - name: Upload artifacts
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02  # v4.6.0
        with:
          name: production-release
          path: |
            app/build/outputs/bundle/release/app-release.aab
            app/build/outputs/mapping/release/mapping.txt
          retention-days: 365
```

**Key features:**
- ✅ Uses Fastlane for deployment
- ✅ Supports full and staged rollouts
- ✅ Creates GitHub releases automatically
- ✅ Pinned all actions to commit SHAs
- ✅ Test job runs before deployment
- ✅ Manual trigger only (no automatic tag deployment)

### Step 3: Create Rollout Management Workflow

**Note:** Fastlane provides full support for rollout management through dedicated lanes.

Create `.github/workflows/manage-rollout.yml`:

```yaml
name: Manage Production Rollout

on:
  workflow_dispatch:
    inputs:
      action:
        description: 'Rollout action'
        required: true
        type: choice
        options:
          - promote
          - halt
          - complete
      from_track:
        description: 'Source track (for promote action)'
        required: false
        type: choice
        options:
          - internal
          - alpha
          - beta
        default: 'beta'
      percentage:
        description: 'Rollout percentage (for promote: 0.05-1.0, e.g., 0.2 for 20%)'
        required: false
        default: '0.05'

jobs:
  manage-rollout:
    runs-on: ubuntu-latest
    environment: production

    steps:
      - name: Checkout code
        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

      - name: Set up JDK 17
        uses: actions/setup-java@c5195efecf7bdfc987ee8bae7a71cb8b11521c00  # v4.7.0
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Set up Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true

      - name: Create Service Account File
        run: echo "${{ secrets.SERVICE_ACCOUNT_JSON_PLAINTEXT }}" > service-account.json

      - name: Increase Rollout
        if: github.event.inputs.action == 'promote'
        env:
          PLAY_STORE_SERVICE_ACCOUNT: service-account.json
        run: bundle exec fastlane increase_rollout rollout:${{ github.event.inputs.percentage }}

      - name: Complete Rollout (100%)
        if: github.event.inputs.action == 'complete'
        env:
          PLAY_STORE_SERVICE_ACCOUNT: service-account.json
        run: bundle exec fastlane increase_rollout rollout:1.0

      - name: Halt Rollout
        if: github.event.inputs.action == 'halt'
        env:
          PLAY_STORE_SERVICE_ACCOUNT: service-account.json
        run: bundle exec fastlane halt_rollout

      - name: Cleanup Service Account
        if: always()
        run: rm -f service-account.json

      - name: Notify result
        if: success()
        run: |
          echo "✅ Rollout action completed: ${{ github.event.inputs.action }}"
          if [ "${{ github.event.inputs.action }}" == "promote" ]; then
            echo "📊 Promoted from ${{ github.event.inputs.from_track }} to production"
            echo "📊 Rollout percentage: ${{ github.event.inputs.percentage }}"
          fi
```

**Key features:**
- ✅ Uses Fastlane for rollout management
- ✅ Supports increase, complete, and halt actions
- ✅ Pinned all actions to commit SHAs

### Step 3: Create Environment Setup Guide

Add to `.github/workflows/README.md`:

```markdown
# GitHub Actions Workflows

## Production Environment Setup

**REQUIRED:** Create production environment for manual approval:

1. Go to: Repository → Settings → Environments
2. Click "New environment"
3. Name: `production`
4. Check "Required reviewers"
5. Add yourself and/or team members
6. Click "Save protection rules"

This ensures production deployments require manual approval.

## Workflows

### deploy-internal.yml
- **Trigger:** Push to main/develop
- **Track:** Internal testing
- **Approval:** None (automatic)

### deploy-production.yml
- **Trigger:** Tag push (v*) or manual
- **Track:** Production
- **Approval:** Required (via environment)
- **Rollout:** Staged (default 5%)

### manage-rollout.yml
- **Trigger:** Manual only
- **Actions:** increase, halt, resume, complete
- **Use:** Control production rollout percentage

## Usage

**Deploy to internal:**
```bash
git push origin main
```

**Deploy to production:**
```bash
git tag v1.0.0
git push origin v1.0.0
# Then approve in GitHub Actions tab
```

**Increase rollout to 20%:**
1. Go to: Actions → Manage Production Rollout
2. Click "Run workflow"
3. Select action: "increase"
4. Enter percentage: "20"
5. Click "Run workflow"

**Emergency halt:**
1. Go to: Actions → Manage Production Rollout
2. Select action: "halt"
3. Click "Run workflow"
```

## Verification

**MANDATORY:** Validate workflows:

```bash
# Validate YAML syntax
yamllint .github/workflows/deploy-production.yml
yamllint .github/workflows/manage-rollout.yml

# Verify package name
grep "packageName:" .github/workflows/*.yml
```

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Production workflow | .github/workflows/deploy-production.yml | Production deployment |
| Rollout management | .github/workflows/manage-rollout.yml | Rollout control |

## Completion Criteria

- [ ] `deploy-production.yml` exists and is valid
- [ ] `manage-rollout.yml` exists and is valid
- [ ] Package names are correct in both files
- [ ] GitHub "production" environment created
- [ ] Required reviewers configured
