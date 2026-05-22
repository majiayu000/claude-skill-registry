---
name: android-workflow-internal
description: Generate GitHub Actions workflows for CI and internal testing track deployment (Option D - Split Workflows)
category: android
version: 2.0.0
inputs:
  - package_name: Android app package name
outputs:
  - .github/workflows/build.yml
  - .github/workflows/release-internal.yml
verify: "yamllint .github/workflows/build.yml .github/workflows/release-internal.yml"
---

# Android Internal Track Workflows (Option D - Split)

Generates **two separate** GitHub Actions workflows following Option D architecture:
1. **build.yml** - CI only (build & test on every push/PR)
2. **release-internal.yml** - Manual releases with version management

**Clear separation of concerns:**
- CI validates code quality automatically
- Releases are always intentional (manual trigger)
- Version management integrated into release process
- No accidental deployments

## Prerequisites

- Service account setup complete
- Package name known

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| package_name | Yes | - | App package name |

## Process

### Step 1: Verify Fastlane Setup

Ensure Fastlane is configured by running `/devtools:android-fastlane-setup` first.

Verify setup:
```bash
bundle exec fastlane lanes
```

Expected output should show `deploy_internal` lane.

### Step 2: Verify Metadata Structure

Ensure Fastlane metadata exists:
```bash
ls fastlane/metadata/android/en-US/
```

If missing, run `/devtools:android-fastlane-setup`.

### Step 3: Create Workflow Directory

```bash
mkdir -p .github/workflows
```

### Step 4: Create Build Workflow (CI)

Create `.github/workflows/build.yml`:

```yaml
name: Build & Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
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

      - name: Build
        run: ./gradlew assembleRelease

      - name: Run Unit Tests
        run: ./gradlew test

      - name: Upload Test Results
        if: always()
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02  # v4.6.0
        with:
          name: test-results
          path: app/build/reports/tests/
          retention-days: 7
```

**Purpose:** CI only - validates code quality, no deployment.

---

### Step 5: Create Release Workflow (Manual)

Create `.github/workflows/release-internal.yml`:

```yaml
name: Release to Internal Track

on:
  workflow_dispatch:
    inputs:
      version_bump:
        description: 'Version bump type'
        required: true
        type: choice
        options:
          - patch
          - minor
          - major
        default: 'patch'

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write  # For pushing commits and tags
    steps:
      - name: Checkout code
        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
        with:
          fetch-depth: 0  # Full history for tags
          token: ${{ secrets.GITHUB_TOKEN }}

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

      - name: Calculate Version
        id: version
        run: |
          chmod +x scripts/gradle-version.sh
          scripts/gradle-version.sh generate ${{ inputs.version_bump }}

      - name: Update version.properties
        run: |
          scripts/gradle-version.sh update ${{ steps.version.outputs.version }}

      - name: Commit Version Bump
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add version.properties
          git commit -m "chore: release v${{ steps.version.outputs.version }}"
          git push origin main

      - name: Decode Keystore
        env:
          ENCODED_KEYSTORE: ${{ secrets.SIGNING_KEY_STORE_BASE64 }}
        run: |
          echo $ENCODED_KEYSTORE | base64 -d > app/release.jks

      - name: Build Release Bundle
        env:
          SIGNING_KEY_STORE_PATH: ${{ github.workspace }}/app/release.jks
          SIGNING_STORE_PASSWORD: ${{ secrets.SIGNING_STORE_PASSWORD }}
          SIGNING_KEY_ALIAS: ${{ secrets.SIGNING_KEY_ALIAS }}
          SIGNING_KEY_PASSWORD: ${{ secrets.SIGNING_KEY_PASSWORD }}
        run: ./gradlew bundleRelease

      - name: Upload Artifact
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02  # v4.6.0
        with:
          name: release-${{ steps.version.outputs.tag }}
          path: app/build/outputs/bundle/release/app-release.aab
          retention-days: 90

      - name: Create Git Tag
        run: |
          git tag -a ${{ steps.version.outputs.tag }} -m "Release ${{ steps.version.outputs.version }}"
          git push origin ${{ steps.version.outputs.tag }}

      - name: Set up Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true

      - name: Create Service Account File
        run: echo "${{ secrets.SERVICE_ACCOUNT_JSON_PLAINTEXT }}" > service-account.json

      - name: Deploy with Fastlane
        env:
          SIGNING_KEY_STORE_PATH: ${{ github.workspace }}/app/release.jks
          SIGNING_STORE_PASSWORD: ${{ secrets.SIGNING_STORE_PASSWORD }}
          SIGNING_KEY_ALIAS: ${{ secrets.SIGNING_KEY_ALIAS }}
          SIGNING_KEY_PASSWORD: ${{ secrets.SIGNING_KEY_PASSWORD }}
          PLAY_STORE_SERVICE_ACCOUNT: service-account.json
        run: bundle exec fastlane deploy_internal

      - name: Cleanup
        if: always()
        run: |
          rm -f app/release.jks
          rm -f service-account.json

      - name: Release Summary
        run: |
          echo "## Release Complete" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "| Property | Value |" >> $GITHUB_STEP_SUMMARY
          echo "|----------|-------|" >> $GITHUB_STEP_SUMMARY
          echo "| Version | ${{ steps.version.outputs.version }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Tag | ${{ steps.version.outputs.tag }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Version Code | ${{ steps.version.outputs.version-code }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Track | Internal |" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "### Next Steps" >> $GITHUB_STEP_SUMMARY
          echo "1. Open Play Console - Internal Testing" >> $GITHUB_STEP_SUMMARY
          echo "2. Verify the new version is available" >> $GITHUB_STEP_SUMMARY
          echo "3. Add internal testers if needed" >> $GITHUB_STEP_SUMMARY
```

**Purpose:** Manual releases with version management - always intentional, never automatic.

**Key differences from combined approach:**
- ✅ Clear separation: CI validates code, Release deploys
- ✅ Version management integrated into release workflow
- ✅ Commits version bump before building
- ✅ Creates git tags as part of release process
- ✅ Release is always manual (workflow_dispatch only)
- ✅ Build/test runs on every PR and push (no deployment)
- ✅ No accidental deployments on regular commits

## Verification

**MANDATORY:** Validate both workflows:

```bash
# Validate YAML syntax
yamllint .github/workflows/build.yml
yamllint .github/workflows/release-internal.yml

# Verify workflows exist
test -f .github/workflows/build.yml && echo "✓ Build workflow created"
test -f .github/workflows/release-internal.yml && echo "✓ Release workflow created"

# Verify Fastlane commands
grep "fastlane deploy_internal" .github/workflows/release-internal.yml
```

**Expected output:**
- ✓ Build workflow created
- ✓ Release workflow created
- Fastlane deploy command found

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Build workflow | .github/workflows/build.yml | CI: build & test on every push/PR |
| Release workflow | .github/workflows/release-internal.yml | Manual releases with version management |

## How to Use

### Continuous Integration (Automatic)

Every push to main or PR triggers **build.yml**:
- Builds the app
- Runs unit tests
- Uploads test results

**No deployment** - just validation.

### Release to Internal Track (Manual)

1. Go to **Actions** → **Release to Internal Track**
2. Click **Run workflow**
3. Select version bump type (patch/minor/major)
4. Click **Run workflow**

**What happens:**
1. Calculates next version from git tags
2. Updates `version.properties`
3. Commits version bump
4. Creates git tag
5. Builds release bundle
6. Deploys to Play Store internal track

## Workflow Separation Benefits

✅ **Clear intent:** CI validates, releases deploy
✅ **No accidents:** Releases are always manual
✅ **Version control:** Version bumps committed before release
✅ **Git tags:** Automatic tag creation on release
✅ **Fast CI:** Build/test runs quickly without deployment overhead
✅ **Audit trail:** Clear history of releases vs. regular commits

## Troubleshooting

### "YAML syntax error"
**Cause:** Invalid YAML format
**Fix:** Check indentation (use spaces, not tabs)

### "Workflow not triggering"
**Cause:** Build workflow not running on push
**Fix:** Verify branch name in workflow matches your main branch (main or master)

### "Version calculation fails"
**Cause:** version-manager.sh script not found or not executable
**Fix:** Run `/devtools:version-management` first to setup version scripts

## Completion Criteria

- [ ] `.github/workflows/build.yml` exists and is valid
- [ ] `.github/workflows/release-internal.yml` exists and is valid
- [ ] Fastlane configured (`bundle exec fastlane lanes` works)
- [ ] Metadata exists in `fastlane/metadata/android/en-US/`
- [ ] Version management scripts available
- [ ] Build workflow runs on push/PR
- [ ] Release workflow available for manual trigger
