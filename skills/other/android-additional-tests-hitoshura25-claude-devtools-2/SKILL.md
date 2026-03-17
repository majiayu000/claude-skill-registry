---
name: android-additional-tests
description: Optional - Add comprehensive tests beyond the basic smoke test
category: android
version: 2.0.0
inputs:
  - project_path: Path to Android project
  - package_name: App package name
  - main_activity: Main activity class name
outputs:
  - Additional test files for comprehensive testing
verify: "./gradlew connectedDebugAndroidTest"
---

# Android Additional Tests (Optional)

⚠️ **This skill is OPTIONAL.** The basic E2E testing setup (android-e2e-testing-setup) already includes a smoke test that validates the app launches without crashing.

Use this skill when you want to add more comprehensive tests beyond the smoke test:
- Navigation tests
- User flow tests
- Screen-specific tests
- Integration tests

## Prerequisites

- E2E testing setup complete (android-e2e-testing-setup)
- Smoke test passing
- Package name and main activity known

## When to Use This Skill

**Use this skill if:**
- You need comprehensive test coverage for specific user flows
- You want to test complex navigation patterns
- You need to validate specific UI interactions
- You're building a large app that needs extensive testing

**Skip this skill if:**
- You only need basic smoke tests (already included in e2e-testing-setup)
- You're setting up a simple app
- You want to start with minimal testing and add more later

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| project_path | Yes | . | Android project root |
| package_name | Yes | - | App package name |
| main_activity | Yes | MainActivity | Main activity class name |

## Process

### Step 1: Create Additional Smoke Tests

Create `app/src/androidTest/kotlin/${PACKAGE_PATH}/ExampleInstrumentedTest.kt`:

```kotlin
package ${PACKAGE_NAME}

import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Test
import org.junit.runner.RunWith
import org.junit.Assert.*

/**
 * Additional instrumented tests beyond the basic smoke test
 */
@RunWith(AndroidJUnit4::class)
class ExampleInstrumentedTest {

    @Test
    fun appLaunches_correctPackage() {
        // Verify app package name
        val appContext = InstrumentationRegistry.getInstrumentation().targetContext
        assertEquals("${PACKAGE_NAME}", appContext.packageName)
    }

    @Test
    fun appContext_isNotNull() {
        // Verify app context is accessible
        val appContext = InstrumentationRegistry.getInstrumentation().targetContext
        assertNotNull(appContext)
    }
}
```

### Step 2: Create Screen-Specific Tests

Create `app/src/androidTest/kotlin/${PACKAGE_PATH}/screens/MainActivityTest.kt`:

```kotlin
package ${PACKAGE_NAME}.screens

import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.matcher.ViewMatchers.isDisplayed
import androidx.test.espresso.matcher.ViewMatchers.withId
import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import ${PACKAGE_NAME}.${MAIN_ACTIVITY}
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

/**
 * Comprehensive tests for ${MAIN_ACTIVITY}
 */
@RunWith(AndroidJUnit4::class)
class ${MAIN_ACTIVITY}Test {

    @get:Rule
    val activityRule = ActivityScenarioRule(${MAIN_ACTIVITY}::class.java)

    @Test
    fun mainActivity_launches() {
        // Verify activity launches without crash
        activityRule.scenario.onActivity { activity ->
            assertNotNull(activity)
        }
    }

    @Test
    fun mainActivity_displaysExpectedViews() {
        // TODO: Replace with actual view IDs from your layouts
        // Example:
        // onView(withId(R.id.toolbar))
        //     .check(matches(isDisplayed()))
        // onView(withId(R.id.main_content))
        //     .check(matches(isDisplayed()))
    }

    @Test
    fun mainActivity_navigationWorks() {
        // TODO: Add navigation tests
        // Example:
        // onView(withId(R.id.nav_button))
        //     .perform(click())
        // onView(withId(R.id.destination_screen))
        //     .check(matches(isDisplayed()))
    }
}
```

### Step 3: Create User Flow Tests

Create `app/src/androidTest/kotlin/${PACKAGE_PATH}/flows/UserFlowTest.kt`:

```kotlin
package ${PACKAGE_NAME}.flows

import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import ${PACKAGE_NAME}.${MAIN_ACTIVITY}
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

/**
 * End-to-end user flow tests
 */
@RunWith(AndroidJUnit4::class)
class UserFlowTest {

    @get:Rule
    val activityRule = ActivityScenarioRule(${MAIN_ACTIVITY}::class.java)

    @Test
    fun userFlow_completeOnboarding() {
        // TODO: Implement complete onboarding flow test
        // Navigate through onboarding screens
        // Verify user reaches main screen
    }

    @Test
    fun userFlow_performMainAction() {
        // TODO: Implement main user action flow
        // Example: Create item, edit item, delete item
    }
}
```

### Step 4: Create GitHub Actions Workflow (Optional)

Create `.github/workflows/android-test.yml`:

```yaml
name: Android E2E Tests

on:
  pull_request:
    branches: [ main, develop ]
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Setup Android SDK
        uses: android-actions/setup-android@v2

      - name: Run Espresso Tests
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 30
          target: google_apis
          arch: x86_64
          script: ./gradlew connectedDebugAndroidTest

      - name: Upload Test Reports
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-reports
          path: app/build/reports/androidTests/
```

## Verification

**MANDATORY:** Run tests (requires device or emulator):

```bash
# Start emulator or connect device first

# Run all tests
./gradlew connectedDebugAndroidTest

# View HTML report
open app/build/reports/androidTests/connected/index.html
```

**Expected output:**
- All tests execute successfully
- New tests pass
- HTML report generated

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Additional smoke tests | ExampleInstrumentedTest.kt | Extended sanity checks |
| Screen tests | screens/MainActivityTest.kt | Main activity UI tests |
| Flow tests | flows/UserFlowTest.kt | End-to-end user flows |
| CI workflow | .github/workflows/android-test.yml | GitHub Actions config (optional) |

## Troubleshooting

### "No tests found"
**Cause:** Package structure mismatch
**Fix:** Verify androidTest package matches main package

### "Activity not found"
**Cause:** Main activity name incorrect
**Fix:** Check actual activity class name in app/src/main/

### "Tests fail on emulator"
**Cause:** Animations interfering with tests
**Fix:** Disable animations in Developer Options

### "View with ID not found"
**Cause:** View ID doesn't exist in layout
**Fix:** Update test to use actual view IDs from your layouts

## Completion Criteria

- [ ] Additional test files created
- [ ] Tests compile successfully
- [ ] `./gradlew connectedDebugAndroidTest` executes
- [ ] All new tests pass

## Notes

- This skill adds tests **in addition to** the smoke test from android-e2e-testing-setup
- Start with the smoke test and add these comprehensive tests as needed
- Update the TODO comments with actual view IDs and navigation logic
- These tests require more maintenance than smoke tests as UI changes
