---
name: android-test-structure
description: Create androidTest directory structure with base classes and utilities
category: android
version: 1.0.0
inputs:
  - project_path: Path to Android project
  - package_name: App package name
outputs:
  - app/src/androidTest/
  - BaseTest.kt
  - TestUtils.kt
verify: "test -d app/src/androidTest"
---

# Android Test Structure

Creates androidTest directory structure with base test class and utilities for Espresso testing.

## Prerequisites

- Android project with Gradle
- Espresso dependencies added (run `android-espresso-dependencies` first)
- Package name known

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| project_path | Yes | . | Android project root |
| package_name | Yes | - | App package (e.g., com.example.app) |

## Process

### Step 1: Create Directory Structure

```bash
# Get package path from package name (com.example.app -> com/example/app)
PACKAGE_PATH=$(echo "${PACKAGE_NAME}" | tr '.' '/')

# Create androidTest directories
mkdir -p "app/src/androidTest/kotlin/${PACKAGE_PATH}/base"
mkdir -p "app/src/androidTest/kotlin/${PACKAGE_PATH}/utils"
mkdir -p "app/src/androidTest/kotlin/${PACKAGE_PATH}/screens"
```

### Step 2: Create BaseTest.kt

Create `app/src/androidTest/kotlin/${PACKAGE_PATH}/base/BaseTest.kt`:

```kotlin
package ${PACKAGE_NAME}.base

import android.content.Context
import androidx.test.core.app.ApplicationProvider
import androidx.test.ext.junit.rules.ActivityScenarioRule
import org.junit.After
import org.junit.Before
import org.junit.Rule

/**
 * Base class for all instrumented tests.
 * Provides common setup, teardown, and utilities.
 */
abstract class BaseTest {

    protected val context: Context = ApplicationProvider.getApplicationContext()

    @Before
    open fun setUp() {
        // Common setup for all tests
        // Override in subclasses for specific setup
    }

    @After
    open fun tearDown() {
        // Common cleanup
        // Override in subclasses for specific cleanup
    }

    /**
     * Wait for idle state before proceeding
     */
    protected fun waitForIdle() {
        androidx.test.espresso.Espresso.onIdle()
    }
}
```

### Step 3: Create TestUtils.kt

Create `app/src/androidTest/kotlin/${PACKAGE_PATH}/utils/TestUtils.kt`:

```kotlin
package ${PACKAGE_NAME}.utils

import android.view.View
import androidx.recyclerview.widget.RecyclerView
import androidx.test.espresso.UiController
import androidx.test.espresso.ViewAction
import androidx.test.espresso.matcher.ViewMatchers.isAssignableFrom
import org.hamcrest.Matcher

object TestUtils {

    /**
     * Custom action to get RecyclerView item count
     */
    fun getRecyclerViewItemCount(recyclerView: RecyclerView): Int {
        return recyclerView.adapter?.itemCount ?: 0
    }

    /**
     * Wait for a condition with timeout
     */
    fun waitForCondition(
        timeoutMs: Long = 5000,
        condition: () -> Boolean
    ): Boolean {
        val startTime = System.currentTimeMillis()
        while (System.currentTimeMillis() - startTime < timeoutMs) {
            if (condition()) return true
            Thread.sleep(100)
        }
        return false
    }

    /**
     * Custom ViewAction to perform click on specific position
     */
    fun clickOnViewChild(viewId: Int): ViewAction {
        return object : ViewAction {
            override fun getConstraints(): Matcher<View>? {
                return null
            }

            override fun getDescription(): String {
                return "Click on a child view with specified id."
            }

            override fun perform(uiController: UiController, view: View) {
                val v = view.findViewById<View>(viewId)
                v.performClick()
            }
        }
    }
}
```

### Step 4: Create README for Tests

Create `app/src/androidTest/README.md`:

```markdown
# Android E2E Tests

This directory contains end-to-end UI tests using Espresso.

## Structure

- `base/` - Base classes for all tests
- `utils/` - Test utilities and helpers
- `screens/` - Screen-specific test classes

## Running Tests

```bash
# All tests
./gradlew connectedAndroidTest

# Specific test class
./gradlew connectedAndroidTest -Pandroid.testInstrumentationRunnerArguments.class=com.example.app.screens.MainActivityTest
```

## Writing Tests

1. Extend `BaseTest` for common setup
2. Use utilities from `TestUtils`
3. Follow AAA pattern: Arrange, Act, Assert
```

## Verification

**MANDATORY:** Run these commands:

```bash
# Verify directory structure exists
test -d app/src/androidTest && echo "✓ androidTest directory created"

# Verify base classes exist
test -f app/src/androidTest/kotlin/*/base/BaseTest.kt && echo "✓ BaseTest.kt created"

# Verify utils exist
test -f app/src/androidTest/kotlin/*/utils/TestUtils.kt && echo "✓ TestUtils.kt created"
```

**Expected output:**
- ✓ androidTest directory created
- ✓ BaseTest.kt created
- ✓ TestUtils.kt created

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Directory structure | app/src/androidTest/ | Test source directory |
| BaseTest class | base/BaseTest.kt | Common test setup |
| Test utilities | utils/TestUtils.kt | Helper functions |
| README | README.md | Test documentation |

## Troubleshooting

### "Package path incorrect"
**Cause:** Package name format wrong
**Fix:** Use format: com.example.app (not path format)

### "Directory already exists"
**Cause:** androidTest directory already created
**Fix:** Merge with existing structure, don't overwrite

## Completion Criteria

- [ ] `app/src/androidTest/` directory exists
- [ ] `base/BaseTest.kt` exists
- [ ] `utils/TestUtils.kt` exists
- [ ] `screens/` directory exists
- [ ] README.md created
