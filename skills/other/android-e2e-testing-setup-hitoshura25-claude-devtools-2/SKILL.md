---
name: android-e2e-testing-setup
description: Setup UI Automator 2.4 smoke test for validating app launches (works with debug and release builds)
category: android
version: 4.0.0
inputs:
  - project_path: Path to Android project
outputs:
  - UI Automator 2.4 dependencies added
  - SmokeTest.kt created with modern API
verify: "./gradlew connectedDebugAndroidTest"
---

# Android E2E Testing Setup

Sets up a lightweight smoke test using UI Automator 2.4 to verify the app launches without crashing.

**Works with BOTH debug and release builds** because UI Automator interacts with apps externally (doesn't require debuggable builds).

## Prerequisites

- Android project with Gradle
- Minimum SDK 21+
- Device or emulator available (MANDATORY)

## Process

### Step 1: Add Dependencies

Update `app/build.gradle.kts`:

```kotlin
dependencies {
    // UI Automator 2.4 - Modern API with built-in waiting
    androidTestImplementation("androidx.test.uiautomator:uiautomator:2.4.0-alpha05")

    // AndroidX Test
    androidTestImplementation("androidx.test:core:1.5.0")
    androidTestImplementation("androidx.test:runner:1.5.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")

    // Truth assertions
    androidTestImplementation("com.google.truth:truth:1.1.5")
}
```

**Note:** UI Automator 2.4 introduces a modern Kotlin DSL. See:
https://developer.android.com/training/testing/other-components/ui-automator

### Step 1b: Configure Test Build Type for Release Testing (Optional)

To run instrumented tests against the **release** build (for ProGuard validation), add this to `app/build.gradle.kts`:

```kotlin
android {
    // ... existing config ...

    // Change test build type from "debug" to "release"
    // This makes connectedAndroidTest run against release builds
    // IMPORTANT: Both app and test APK will be signed with release key
    testBuildType = "release"
}
```

**What this does:**
- `./gradlew connectedAndroidTest` now runs against release build
- Both app APK and test APK are signed with the same (release) key
- ProGuard/R8 runs on the app APK
- Tests validate the actual release build

**When to use this:**
- During release validation (before publishing)
- To catch ProGuard/R8 issues
- CI/CD release pipelines

**When NOT to use this:**
- Day-to-day development (debug builds are faster)
- When you don't have release signing configured locally

**To toggle back to debug testing:**
```kotlin
testBuildType = "debug"  // Or just remove the line (debug is default)
```

### Step 2: Create Smoke Test

Create `app/src/androidTest/kotlin/{package_path}/SmokeTest.kt`:

```kotlin
package {PACKAGE_NAME}

import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.uiautomator.uiAutomator
import androidx.test.uiautomator.UiAutomatorTestScope
import com.google.common.truth.Truth.assertThat
import org.junit.Test
import org.junit.runner.RunWith

/**
 * Smoke test using modern UI Automator 2.4 API.
 *
 * This test works with BOTH debug and release APKs because UI Automator
 * interacts with the app externally (doesn't require debuggable build).
 *
 * Primary purpose: Validate app launches without crashing.
 * For release builds: Validates ProGuard/R8 didn't break critical code paths.
 *
 * @see https://developer.android.com/training/testing/other-components/ui-automator
 */
@RunWith(AndroidJUnit4::class)
class SmokeTest {

    companion object {
        private const val PACKAGE_NAME = "{PACKAGE_NAME}"
    }

    @Test
    fun appLaunches_doesNotCrash() = uiAutomator {
        // Start the app
        startApp(PACKAGE_NAME)

        // Wait for app to be visible
        waitForAppToBeVisible(PACKAGE_NAME)

        // Handle HealthConnect permission dialogs if they appear
        handleHealthConnectPermissions()

        // Verify app is running by checking for any element with our package
        val appElement = onElementOrNull(5000) {
            packageName == PACKAGE_NAME
        }

        assertThat(appElement).isNotNull()
    }

    @Test
    fun appLaunches_hasVisibleContent() = uiAutomator {
        // Start the app
        startApp(PACKAGE_NAME)
        waitForAppToBeVisible(PACKAGE_NAME)

        // Handle permissions
        handleHealthConnectPermissions()

        // Verify app has UI content (didn't crash to blank screen)
        val appStillRunning = onElementOrNull(2000) {
            packageName == PACKAGE_NAME
        }

        assertThat(appStillRunning).isNotNull()
    }

    // =========================================================================
    // HealthConnect Permission Handling
    // =========================================================================

    /**
     * Navigate through HealthConnect permission UI.
     *
     * HealthConnect has a multi-screen permission flow:
     * 1. Data permissions screen - toggle "Allow all" then click "Allow"
     * 2. Background access screen - click "Allow"
     */
    private fun UiAutomatorTestScope.handleHealthConnectPermissions() {
        // Screen 1: Data permissions ("fitness and wellness data")
        val dataPermScreen = onElementOrNull(3000) {
            text?.contains("fitness and wellness data") == true
        }

        if (dataPermScreen != null) {
            // Click "Allow all" toggle to enable all permissions
            onElementOrNull(1000) { text == "Allow all" }?.click()

            // Click "Allow" button at bottom
            onElement {
                text == "Allow" && className == "android.widget.Button"
            }.click()
        }

        // Screen 2: Background access ("access data in the background")
        val backgroundScreen = onElementOrNull(2000) {
            text?.contains("access data in the background") == true
        }

        if (backgroundScreen != null) {
            // Click "Allow" button
            onElement {
                text == "Allow" && className == "android.widget.Button"
            }.click()
        }
    }

    // =========================================================================
    // Standard Runtime Permissions (Optional)
    // =========================================================================

    /**
     * Handle standard Android runtime permission dialogs.
     */
    private fun UiAutomatorTestScope.handleRuntimePermissions() {
        val allowButton = onElementOrNull(1000) {
            text?.matches(Regex("(?i)allow|while using the app")) == true
        }
        allowButton?.click()
    }
}
```

**Replace {PACKAGE_NAME} with the actual package name (e.g., `com.hitoshura25.healthsync`).**

To find the package name:
```bash
grep "applicationId" app/build.gradle.kts
# Or check AndroidManifest.xml
grep "package=" app/src/main/AndroidManifest.xml
```

**Note:** The `UiAutomatorTestScope` extension functions allow accessing the scope's methods like `onElement` from within helper functions.

## Verification (MANDATORY)

⛔ **DO NOT SKIP THIS STEP**

### Prerequisite: Device/Emulator Required

First, verify a device or emulator is available:

```bash
adb devices
```

**If no devices listed:**
1. Start an emulator:
   ```bash
   # List available AVDs
   emulator -list-avds

   # Start an emulator (replace with actual AVD name)
   emulator -avd Pixel_6_API_34 &

   # Wait for device to be ready
   adb wait-for-device
   ```
2. Or connect a physical device with USB debugging enabled
3. Re-run `adb devices` to confirm

**If no device/emulator available, STOP. Inform user this skill cannot complete without a device.**

### Run Tests

```bash
# Run debug tests
./gradlew connectedDebugAndroidTest
```

**If tests fail:**
1. Read the error message carefully
2. Fix compilation errors (usually import issues)
3. Fix test failures (adjust permission handling if needed)
4. Re-run until tests pass

**Only proceed to completion when tests pass.**

### Expected Output

```
> Task :app:connectedDebugAndroidTest
Tests on Pixel_6_API_34 - 14

SmokeTest > appLaunches_doesNotCrash PASSED
SmokeTest > appLaunches_hasVisibleContent PASSED

2 tests, 2 passed, 0 failed
```

## Completion Criteria

Do NOT mark complete unless ALL are verified:

- [ ] UI Automator 2.4 dependency in `app/build.gradle.kts`
- [ ] `SmokeTest.kt` exists using modern `uiAutomator { }` API
- [ ] `./gradlew connectedDebugAndroidTest` executes successfully
- [ ] At least 2 tests pass
- [ ] Device/emulator was used (tests cannot run without one)

**If tests fail, fix them before marking complete.**

## Troubleshooting

### No device found
**Cause:** No connected device or running emulator
**Fix:** Start emulator or connect physical device (see Verification section)

### Tests fail to compile
**Cause:** Incorrect package name in SmokeTest.kt
**Fix:** Verify package name matches AndroidManifest.xml

### Permission dialog blocks test
**Cause:** App requires permissions not handled in handleHealthConnectPermissions()
**Fix:** See `PERMISSION_DEBUGGING.md` for guide on debugging UI Automator selectors

### "waitForAppToBeVisible timed out"
**Cause:** App crashed or took too long to start
**Fix:** Check logcat: `adb logcat -d | grep -i crash`

## UI Automator 2.4 API Benefits

The modern API provides several advantages over the old approach:

| Old API (deprecated) | New API (UI Automator 2.4) |
|---------------------|----------------------------|
| `UiDevice.getInstance(...)` | `uiAutomator { }` scope |
| `device.waitForIdle()` | `waitForAppToBeVisible()` |
| `device.findObject(UiSelector().text("X"))` | `onElement { text == "X" }` |
| Manual timeout loops | Built-in timeout: `onElement(5000) { }` |
| `element.exists()` + click | `onElementOrNull { }?.click()` |
| `device.findObject(By.pkg(...))` | `onElement { packageName == "..." }` |

**Key benefits:**
- Cleaner Kotlin DSL
- Built-in waiting (no more `waitForIdle()` everywhere)
- More readable predicates
- Better null handling with `onElementOrNull`
- Works with non-debuggable APKs (can test actual release builds)

## Next Steps

After smoke tests pass:
1. For release testing: Install release APK and run tests against it (see `android-release-validation`)
2. Add more comprehensive tests if needed (use `android-additional-tests` skill)
3. Integrate with CI/CD pipeline
