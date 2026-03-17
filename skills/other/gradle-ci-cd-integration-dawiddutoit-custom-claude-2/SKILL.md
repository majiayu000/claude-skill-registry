---
name: gradle-ci-cd-integration
description: |
  Configures Gradle builds for CI/CD platforms including GitHub Actions,
  GitLab CI, Jenkins, and CircleCI. Use when setting up automated builds,
  configuring caching strategies, running tests in pipelines, or building
  Docker images in CI. Triggers on "setup Gradle CI", "configure GitHub Actions",
  "optimize build cache", or "CI pipeline for Gradle". Works with .github/workflows,
  .gitlab-ci.yml, Jenkinsfile, and includes performance optimization and artifact handling.

---

# Gradle CI/CD Integration

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
- [Requirements](#requirements)
- [See Also](#see-also)

## Purpose

Configure Gradle builds for continuous integration and deployment with caching, artifact management, test reporting, and Docker image building. Covers GitHub Actions, GitLab CI, Jenkins, and CircleCI with production-ready optimizations.

## When to Use

Use this skill when you need to:
- Set up automated builds in GitHub Actions, GitLab CI, Jenkins, or CircleCI
- Configure dependency and build caching for faster CI pipelines
- Generate and publish test reports in CI/CD
- Build and push Docker images in automated pipelines
- Optimize CI build performance with parallel execution
- Handle build artifacts and code coverage reports

## Quick Start

**GitHub Actions** `.github/workflows/build.yml`:

```yaml
name: Build

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - uses: actions/setup-java@v4
      with:
        java-version: '21'
        distribution: 'temurin'

    - uses: gradle/actions/setup-gradle@v4
      with:
        cache-encryption-key: ${{ secrets.GRADLE_ENCRYPTION_KEY }}

    - run: ./gradlew build --parallel --build-cache --scan
```

**GitLab CI** `.gitlab-ci.yml`:

```yaml
image: gradle:8.11-jdk21-alpine

variables:
  GRADLE_OPTS: "-Dorg.gradle.daemon=false -Dorg.gradle.caching=true"

build:
  script:
    - ./gradlew build --parallel --build-cache
  cache:
    paths:
      - .gradle/wrapper
      - .gradle/caches
```

## Instructions

### Step 1: Use Gradle Wrapper in CI

Always use the Gradle wrapper for consistent versions:

```bash
# Use wrapper (recommended)
./gradlew build

# Not this
gradle build
```

Ensure wrapper is executable:
```bash
chmod +x ./gradlew
git add gradlew
```

### Step 2: Configure Build Caching

Enable caching in your CI configuration:

**GitHub Actions:**
```yaml
- uses: gradle/actions/setup-gradle@v4
  with:
    cache-encryption-key: ${{ secrets.GRADLE_ENCRYPTION_KEY }}
    cache-read-only: ${{ github.ref != 'refs/heads/main' }}
```

**GitLab CI:**
```yaml
cache:
  key: "$CI_COMMIT_REF_SLUG"
  paths:
    - .gradle/wrapper
    - .gradle/caches
```

**Jenkins:**
```groovy
agent {
    docker {
        image 'gradle:8.11-jdk21'
        args '-v $HOME/.gradle:/home/gradle/.gradle'
    }
}
```

See [references/detailed-guide.md](./references/detailed-guide.md) for complete caching strategies.

### Step 3: Optimize Build Performance

Use these flags for faster CI builds:

```bash
./gradlew build \
  --parallel \              # Parallel execution
  --build-cache \          # Remote build cache
  --configuration-cache \  # Configuration cache (Gradle 8+)
  --scan                   # Build scan for analysis
```

Configure in `gradle.properties`:
```properties
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.daemon=false  # Disable for CI
```

### Step 4: Configure Test Reporting

**JUnit XML reports:**

```yaml
# GitHub Actions
- name: Publish Test Results
  uses: mikepenz/action-junit-report@v4
  if: always()
  with:
    report_paths: '**/build/test-results/test/TEST-*.xml'
```

**GitLab CI:**
```yaml
test:
  script:
    - ./gradlew test
  artifacts:
    reports:
      junit: build/test-results/test/TEST-*.xml
```

See [references/detailed-guide.md](./references/detailed-guide.md) for coverage reporting with JaCoCo.

### Step 5: Build and Push Docker Images

**GitHub Actions with Jib:**

```yaml
- name: Build Docker Image (PR)
  if: github.event_name == 'pull_request'
  run: ./gradlew jibDockerBuild

- name: Build and Push (Main)
  if: github.ref == 'refs/heads/main'
  run: ./gradlew jib
  env:
    DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
    DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
```

**GitLab CI:**
```yaml
docker-build:
  stage: deploy
  only:
    - main
  script:
    - ./gradlew jib
  environment:
    name: production
```

See [references/detailed-guide.md](./references/detailed-guide.md) for Jenkins and CircleCI configurations.

### Step 6: Handle Build Artifacts

**Upload artifacts:**

```yaml
# GitHub Actions
- name: Upload Build Artifacts
  uses: actions/upload-artifact@v4
  with:
    name: build-artifacts
    path: |
      build/libs/
      build/reports/
```

**GitLab CI:**
```yaml
build:
  artifacts:
    paths:
      - build/libs/
    expire_in: 1 day
```

### Step 7: Implement Build Scans

Enable build scans for troubleshooting:

```kotlin
// build.gradle.kts
plugins {
    id("com.gradle.enterprise") version "3.16.1"
}

gradleEnterprise {
    buildScan {
        termsOfServiceUrl = "https://gradle.com/terms-of-service"
        termsOfServiceAgree = "yes"
        publishAlways()
    }
}
```

Run with `--scan`:
```bash
./gradlew build --scan
```

## Requirements

- **Gradle Wrapper:** 8.11+ recommended
- **Java:** JDK 17+ (21 recommended for latest features)
- **CI Platform:** GitHub Actions, GitLab CI, Jenkins, or CircleCI
- **Dependencies:**
  - `gradle/actions/setup-gradle@v4` for GitHub Actions
  - Docker for container-based builds
- **Secrets:** Store credentials securely
  - `GRADLE_ENCRYPTION_KEY` for cache encryption
  - `DOCKER_USERNAME`, `DOCKER_PASSWORD` for registry auth

## See Also

- [references/detailed-guide.md](./references/detailed-guide.md) - Comprehensive examples for all CI platforms, commands reference, best practices, and troubleshooting
- [gradle-performance-optimization](../gradle-performance-optimization/SKILL.md) - Optimize build caching
- [gradle-docker-jib](../gradle-docker-jib/SKILL.md) - Build Docker images
- [gradle-testing-setup](../gradle-testing-setup/SKILL.md) - Configure test reporting
- [GitHub Actions Gradle Setup](https://github.com/gradle/actions) - Official Gradle Actions
