---
name: android-screenshot-automation
description: Setup automated screenshot capture for Play Store using Fastlane Screengrab
category: android
version: 1.0.0
prerequisites:
  - android-fastlane-setup
  - android-e2e-tests (UI Automator tests)
inputs:
  - screens: List of screens to capture
  - locales: Locales to support (default: en-US)
outputs:
  - app/src/androidTest/.../screenshots/ScreenshotTest.kt
  - app/src/debug/AndroidManifest.xml
  - fastlane/metadata/android/{locale}/images/phoneScreenshots/
verify: "bundle exec fastlane screenshots"
---

# Android Screenshot Automation

Setup automated screenshot capture using Fastlane Screengrab, integrating with existing e2e test infrastructure.

## Prerequisites

- `/devtools:android-fastlane-setup` completed
- `/devtools:android-e2e-tests` completed (UI Automator tests exist)
- Emulator or device available for testing

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| screens | Yes | - | List of screens to capture (e.g., home, settings, profile) |
| locales | No | en-US | Comma-separated locales (e.g., en-US,de-DE,es-ES) |

## Process

### Step 1: Add Screengrab Dependency

Add to `app/build.gradle.kts`:

```kotlin
dependencies {
    // Existing test dependencies...

    // Screengrab for automated screenshots
    androidTestImplementation("tools.fastlane:screengrab:2.1.1")
}
```

Sync Gradle after adding.

### Step 2: Create Debug Manifest

Create or update `app/src/debug/AndroidManifest.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <!-- Screengrab permissions -->

    <!-- Store screenshots on external storage (API <= 18) -->
    <uses-permission
        android:name="android.permission.WRITE_EXTERNAL_STORAGE"
        android:maxSdkVersion="18" />

    <!-- Change device locale during tests -->
    <uses-permission
        android:name="android.permission.CHANGE_CONFIGURATION"
        tools:ignore="ProtectedPermissions" />

    <!-- Enable demo mode for clean status bar -->
    <uses-permission
        android:name="android.permission.DUMP"
        tools:ignore="ProtectedPermissions" />

</manifest>
```

### Step 3: Create Demo Mode Helper (Optional but Recommended)

Create `app/src/androidTest/{package_path}/screenshots/DemoModeRule.kt`:

```kotlin
package {PACKAGE_NAME}.screenshots

import android.os.ParcelFileDescriptor
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.rules.TestRule
import org.junit.runner.Description
import org.junit.runners.model.Statement
import java.io.BufferedReader
import java.io.InputStreamReader

/**
 * JUnit Rule that enables Android Demo Mode for clean status bar screenshots.
 *
 * Demo mode shows:
 * - Full battery (100%)
 * - Full signal strength
 * - Fixed time (12:00)
 * - No notifications
 */
class DemoModeRule : TestRule {

    override fun apply(base: Statement, description: Description): Statement {
        return object : Statement() {
            override fun evaluate() {
                enableDemoMode()
                try {
                    base.evaluate()
                } finally {
                    disableDemoMode()
                }
            }
        }
    }

    private fun enableDemoMode() {
        executeShellCommand("settings put global sysui_demo_allowed 1")
        executeShellCommand("am broadcast -a com.android.systemui.demo -e command enter")
        executeShellCommand("am broadcast -a com.android.systemui.demo -e command clock -e hhmm 1200")
        executeShellCommand("am broadcast -a com.android.systemui.demo -e command battery -e level 100 -e plugged false")
        executeShellCommand("am broadcast -a com.android.systemui.demo -e command network -e wifi show -e level 4")
        executeShellCommand("am broadcast -a com.android.systemui.demo -e command network -e mobile show -e datatype none -e level 4")
        executeShellCommand("am broadcast -a com.android.systemui.demo -e command notifications -e visible false")
    }

    private fun disableDemoMode() {
        executeShellCommand("am broadcast -a com.android.systemui.demo -e command exit")
    }

    private fun executeShellCommand(command: String) {
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        val automation = instrumentation.uiAutomation

        val pfd: ParcelFileDescriptor = automation.executeShellCommand(command)
        val reader = BufferedReader(InputStreamReader(ParcelFileDescriptor.AutoCloseInputStream(pfd)))
        reader.readLines() // Consume output
        reader.close()
    }
}
```

### Step 4: Create Screenshot Test Class

Create `app/src/androidTest/{package_path}/screenshots/ScreenshotTest.kt`:

```kotlin
package {PACKAGE_NAME}.screenshots

import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.action.ViewActions.click
import androidx.test.espresso.matcher.ViewMatchers.withId
import org.junit.Before
import org.junit.ClassRule
import org.junit.Rule
import org.junit.Test
import org.junit.rules.RuleChain
import org.junit.runner.RunWith
import tools.fastlane.screengrab.Screengrab
import tools.fastlane.screengrab.UiAutomatorScreenshotStrategy
import tools.fastlane.screengrab.locale.LocaleTestRule

import {PACKAGE_NAME}.R
import {PACKAGE_NAME}.MainActivity

/**
 * Automated screenshot capture for Play Store listing.
 *
 * Run with: bundle exec fastlane screenshots
 *
 * Screenshots are saved to: fastlane/metadata/android/{locale}/images/phoneScreenshots/
 */
@RunWith(AndroidJUnit4::class)
class ScreenshotTest {

    companion object {
        // Automatically switches device locale between test runs
        @get:ClassRule
        @JvmField
        val localeTestRule = LocaleTestRule()
    }

    // Launch main activity for each test
    @get:Rule
    val activityRule = ActivityScenarioRule(MainActivity::class.java)

    // Enable demo mode for clean status bar (optional)
    @get:Rule
    val demoModeRule = DemoModeRule()

    @Before
    fun setup() {
        // Use UI Automator strategy for better screenshots
        // This captures dialogs, shadows, and system UI correctly
        Screengrab.setDefaultScreenshotStrategy(UiAutomatorScreenshotStrategy())
    }

    @Test
    fun captureScreenshots() {
        // Wait for app to fully load
        Thread.sleep(1000)

        // Screenshot 1: Main/Home screen
        Screengrab.screenshot("01_home")

        // TODO: Navigate to next screen and capture
        // Example:
        // onView(withId(R.id.settings_button)).perform(click())
        // Thread.sleep(500)
        // Screengrab.screenshot("02_settings")

        // TODO: Add more screenshots as needed
        // Recommendation: Capture 4-8 key screens that showcase your app's features
    }

    // Optional: Separate test methods for different flows
    // This helps organize screenshots and makes debugging easier

    @Test
    fun captureOnboardingFlow() {
        // If your app has onboarding, capture those screens
        // Screengrab.screenshot("onboarding_01_welcome")
        // onView(withId(R.id.next_button)).perform(click())
        // Screengrab.screenshot("onboarding_02_features")
    }
}
```

**Important:** Replace `{PACKAGE_NAME}` with your actual package name and customize the screenshot capture logic.

### Step 5: Update Screengrabfile

Ensure `./fastlane/Screengrabfile` has the correct test class:

```ruby
# Use the screenshot test class
use_tests_in_classes(["{PACKAGE_NAME}.screenshots.ScreenshotTest"])
```

### Step 6: Run Screenshots

```bash
# Build and capture screenshots
bundle exec fastlane screenshots

# Or run screengrab directly
bundle exec fastlane run capture_android_screenshots
```

## Adding Multiple Device Sizes

For tablet screenshots, you can run screengrab with different device types:

```ruby
# Add to Fastfile
desc "Capture screenshots for all device types"
lane :screenshots_all_devices do
  # Phone screenshots
  capture_android_screenshots(device_type: "phone")

  # 7-inch tablet (requires tablet emulator running)
  # capture_android_screenshots(device_type: "sevenInch")

  # 10-inch tablet (requires tablet emulator running)
  # capture_android_screenshots(device_type: "tenInch")
end
```

## Verification

**MANDATORY:** Run these commands:

```bash
# Build APKs
./gradlew assembleDebug assembleAndroidTest

# Start emulator
# emulator -avd <avd_name> &

# Run screenshots (with emulator running)
bundle exec fastlane screenshots

# Check output
ls -la fastlane/metadata/android/en-US/images/phoneScreenshots/
```

**Expected output:**
- Screenshots appear in `fastlane/metadata/android/en-US/images/phoneScreenshots/`
- Files named like `01_home_en-US.png`, `02_settings_en-US.png`

## Completion Criteria

- [ ] `tools.fastlane:screengrab` dependency added to `app/build.gradle.kts`
- [ ] Debug manifest (`app/src/debug/AndroidManifest.xml`) has required permissions
- [ ] `ScreenshotTest.kt` exists with at least one screenshot
- [ ] `DemoModeRule.kt` created for clean status bar
- [ ] `bundle exec fastlane screenshots` runs successfully
- [ ] Screenshots appear in `fastlane/metadata/android/en-US/images/phoneScreenshots/`

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Screenshot test | `app/src/androidTest/.../screenshots/ScreenshotTest.kt` | Test class for capturing screenshots |
| Demo mode rule | `app/src/androidTest/.../screenshots/DemoModeRule.kt` | Clean status bar helper |
| Debug manifest | `app/src/debug/AndroidManifest.xml` | Permissions for screengrab |
| Screenshots | `fastlane/metadata/android/{locale}/images/phoneScreenshots/` | Captured screenshots |

## Troubleshooting

### "Permission denied" errors
**Cause:** Debug manifest permissions not applied
**Fix:** Clean and rebuild: `./gradlew clean assembleDebug assembleAndroidTest`

### "Test not found"
**Cause:** Wrong test class in Screengrabfile
**Fix:** Ensure package name and class name match exactly

### Screenshots are blank/black
**Cause:** Activity not fully loaded before screenshot
**Fix:** Add `Thread.sleep()` before `Screengrab.screenshot()`

### Demo mode not working
**Cause:** Permission denied for DUMP permission
**Fix:** Run on API 23+ emulator (demo mode requires API 23+)

## Next Steps

After completing this skill:
1. Customize `ScreenshotTest.kt` to capture your app's key screens
2. Run `/devtools:android-store-listing` to create feature graphic
3. Run screenshots regularly to keep store listing updated
