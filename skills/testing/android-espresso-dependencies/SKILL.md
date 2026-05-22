---
name: android-espresso-dependencies
description: Add Espresso and AndroidX Test dependencies to Android project
category: android
version: 1.0.0
inputs:
  - project_path: Path to Android project
outputs:
  - Updated app/build.gradle.kts with test dependencies
verify: "./gradlew dependencies | grep espresso"
---

# Android Espresso Dependencies

Adds Espresso and AndroidX Test dependencies required for E2E UI testing.

## Prerequisites

- Android project with Gradle
- Kotlin DSL (build.gradle.kts)
- Minimum SDK 21+ (Espresso requirement)

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| project_path | Yes | . | Android project root |

## Process

### Step 1: Add Espresso Dependencies

Add to `app/build.gradle.kts`:

```kotlin
dependencies {
    // Existing dependencies...

    // Espresso core
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
    androidTestImplementation("androidx.test.espresso:espresso-contrib:3.5.1")
    androidTestImplementation("androidx.test.espresso:espresso-intents:3.5.1")

    // AndroidX Test
    androidTestImplementation("androidx.test:runner:1.5.2")
    androidTestImplementation("androidx.test:rules:1.5.0")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.ext:junit-ktx:1.1.5")
}
```

**Detection logic:**
- Check if dependencies already exist (don't duplicate)
- Use latest stable versions
- Keep existing test dependencies

### Step 2: Configure Test Runner (Optional)

If user wants test orchestrator for better isolation:

```kotlin
android {
    // ... existing config ...

    defaultConfig {
        // ... existing config ...
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    testOptions {
        execution = "ANDROIDX_TEST_ORCHESTRATOR"
        animationsDisabled = true
    }
}

dependencies {
    // ... existing dependencies ...
    androidTestUtil("androidx.test:orchestrator:1.4.2")
}
```

**Ask user:** "Enable test orchestrator for better test isolation? (Recommended for large test suites)"

## Verification

**MANDATORY:** Run these commands:

```bash
# Sync Gradle
./gradlew dependencies --configuration androidTestRuntimeClasspath

# Verify Espresso dependencies
./gradlew dependencies | grep espresso && echo "✓ Espresso dependencies added"

# Verify AndroidX Test dependencies
./gradlew dependencies | grep "androidx.test" && echo "✓ AndroidX Test dependencies added"
```

**Expected output:**
- ✓ Espresso dependencies added
- ✓ AndroidX Test dependencies added

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Dependencies | app/build.gradle.kts | Espresso and AndroidX Test libs |

## Troubleshooting

### "Dependency resolution failed"
**Cause:** Version conflict with existing dependencies
**Fix:** Check for conflicting androidx.test versions, align all to same version

### "Minimum SDK too low"
**Cause:** minSdk < 21
**Fix:** Espresso requires API 21+, update minSdk in defaultConfig

## Completion Criteria

- [ ] Espresso dependencies in app/build.gradle.kts
- [ ] AndroidX Test dependencies in app/build.gradle.kts
- [ ] Test runner configured
- [ ] `./gradlew dependencies` shows espresso libraries
