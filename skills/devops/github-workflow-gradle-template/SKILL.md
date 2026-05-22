---
name: github-workflow-gradle-template
description: Provides a GitHub Actions CI workflow template for Gradle/Java projects. Claude should use this skill when creating or updating CI workflows to ensure current action versions and best practices are followed.
---

# GitHub Actions Workflow Template for Gradle Projects

When creating a GitHub Actions CI workflow for a Gradle/Java project, use this template:

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v4
        with:
          cache-read-only: false

      - name: Build with Gradle
        run: ./gradlew build
```

## Key Points

1. **Action versions** (as of December 2025):
   - `actions/checkout@v4`
   - `actions/setup-java@v4`
   - `gradle/actions/setup-gradle@v4`

2. **Do NOT use deprecated actions**:
   - `gradle/wrapper-validation-action` - no longer needed, wrapper validation is included in `gradle/actions/setup-gradle`
   - `gradle/gradle-build-action` - replaced by `gradle/actions/setup-gradle`

3. **Avoid redundant steps**:
   - `./gradlew build` already runs tests, so a separate `./gradlew test` step is unnecessary

4. **Gradle caching**: The `gradle/actions/setup-gradle` action handles caching automatically. Use `cache-read-only: false` to allow cache writes.

## Customization

Adjust as needed for your project:
- Change `java-version` if using a different JDK version
- Add additional branches to the trigger
- Add environment variables or secrets as required
