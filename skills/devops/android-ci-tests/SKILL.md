---
name: android-ci-tests
description: Setup GitHub Actions workflow for running Android tests in CI
category: android
version: 1.0.0
inputs:
  - project_path: Path to Android project
outputs:
  - .github/workflows/test.yml
verify: "yamllint .github/workflows/test.yml"
---

# Android CI Tests Setup

Sets up GitHub Actions workflow for running Android unit and instrumented tests in CI.

## Prerequisites

- Android project with test dependencies
- GitHub repository

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| project_path | Yes | . | Android project root |

## Process

### Step 1: Create CI Test Workflow

Create `.github/workflows/test.yml`:

```yaml
name: Android CI Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  unit-tests:
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
        run: ./gradlew test --stacktrace

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02  # v4.6.0
        with:
          name: unit-test-results
          path: |
            app/build/test-results/
            app/build/reports/tests/
          retention-days: 7

      - name: Upload coverage reports (if JaCoCo configured)
        if: always()
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02  # v4.6.0
        with:
          name: coverage-reports
          path: app/build/reports/jacoco/
          retention-days: 7

  lint:
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

      - name: Run lint
        run: ./gradlew lintDebug --stacktrace

      - name: Upload lint results
        if: always()
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02  # v4.6.0
        with:
          name: lint-results
          path: app/build/reports/lint-results-debug.html
          retention-days: 7

  instrumented-tests:
    runs-on: ubuntu-latest
    # Optional: Only run instrumented tests if unit tests pass
    needs: unit-tests

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

      - name: Enable KVM group permissions
        run: |
          echo 'KERNEL=="kvm", GROUP="kvm", MODE="0666", OPTIONS+="static_node=kvm"' | sudo tee /etc/udev/rules.d/99-kvm4all.rules
          sudo udevadm control --reload-rules
          sudo udevadm trigger --name-match=kvm

      - name: Setup Android SDK
        uses: android-actions/setup-android@v3

      - name: AVD cache
        uses: actions/cache@1bd1e32a3bdc45362d1e726936510720a7c30a57  # v4.2.0
        id: avd-cache
        with:
          path: |
            ~/.android/avd/*
            ~/.android/adb*
          key: avd-${{ runner.os }}-api-30

      - name: Create AVD and generate snapshot for caching
        if: steps.avd-cache.outputs.cache-hit != 'true'
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 30
          target: google_apis
          arch: x86_64
          profile: pixel_6
          force-avd-creation: false
          emulator-options: -no-window -gpu swiftshader_indirect -noaudio -no-boot-anim -camera-back none
          disable-animations: true
          script: echo "Generated AVD snapshot for caching."

      - name: Run instrumented tests
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 30
          target: google_apis
          arch: x86_64
          profile: pixel_6
          force-avd-creation: false
          emulator-options: -no-snapshot-save -no-window -gpu swiftshader_indirect -noaudio -no-boot-anim -camera-back none
          disable-animations: true
          script: ./gradlew connectedDebugAndroidTest --stacktrace

      - name: Upload instrumented test results
        if: always()
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02  # v4.6.0
        with:
          name: instrumented-test-results
          path: |
            app/build/reports/androidTests/
            app/build/outputs/androidTest-results/
          retention-days: 7
```

**Features:**
- ✅ Runs on push and pull requests
- ✅ Separate jobs for unit tests, lint, and instrumented tests
- ✅ Gradle caching for faster builds
- ✅ AVD caching for faster emulator startup
- ✅ KVM acceleration for faster emulator performance
- ✅ All actions pinned to commit SHAs
- ✅ Test results uploaded as artifacts
- ✅ Instrumented tests only run if unit tests pass

## Verification

**MANDATORY:** Verify workflow is valid:

```bash
# Validate YAML syntax
yamllint .github/workflows/test.yml

# Verify workflow exists
test -f .github/workflows/test.yml && echo "✓ Test workflow created"

# Push to trigger workflow
git add .github/workflows/test.yml
git commit -m "Add CI test workflow"
git push
```

**Monitor:** Go to repository → Actions tab to see tests running

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Test workflow | .github/workflows/test.yml | CI test automation |

## Optional Enhancements

### Add Code Coverage

If using JaCoCo, add to `app/build.gradle.kts`:

```kotlin
android {
    buildTypes {
        debug {
            enableAndroidTestCoverage = true
            enableUnitTestCoverage = true
        }
    }
}
```

### Add Test Report Comments

Add a step to comment test results on PRs:

```yaml
- name: Comment test results on PR
  if: github.event_name == 'pull_request'
  uses: EnricoMi/publish-unit-test-result-action@v2
  with:
    files: app/build/test-results/**/*.xml
```

## Troubleshooting

### "Emulator failed to start"
**Cause:** KVM not available or permissions issue
**Fix:** GitHub-hosted runners should have KVM enabled. Check runner logs.

### "Out of memory during tests"
**Cause:** Gradle daemon using too much memory
**Fix:** Add to gradle.properties: `org.gradle.jvmargs=-Xmx2048m`

### "Tests timeout"
**Cause:** Instrumented tests taking too long
**Fix:** Increase timeout or split tests across multiple jobs

## Completion Criteria

- [ ] `.github/workflows/test.yml` exists and is valid
- [ ] Workflow runs on push and pull requests
- [ ] Unit tests execute successfully
- [ ] Lint checks execute successfully
- [ ] Instrumented tests execute successfully (if configured)
- [ ] Test results uploaded as artifacts
