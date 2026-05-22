---
name: qa-testing-android
description: Android testing with Espresso, UIAutomator, and Compose Testing; layered strategy, flake control, device matrix, CI integration, and ADB automation.
---

# QA Testing (Android)

Android testing automation with Espresso, UIAutomator, and Compose Testing.

**Core References**: [Android Testing Docs](https://developer.android.com/training/testing), [Espresso](https://developer.android.com/training/testing/espresso), [Compose Testing](https://developer.android.com/develop/ui/compose/testing)

## Quick Reference

| Task | Command |
|------|---------|
| List emulators | `emulator -list-avds` |
| Start emulator | `emulator @<avd_name>` |
| List devices | `adb devices` |
| Install APK | `adb install -r <path-to-apk>` |
| Run unit tests | `./gradlew test` |
| Run instrumented tests (connected) | `./gradlew connectedAndroidTest` |
| Run instrumented tests (GMD) | `./gradlew <device><variant>AndroidTest` |
| List GMD tasks | `./gradlew tasks --all | rg -n \"AndroidTest|managedDevice|ManagedDevices\"` |
| Clear app data | `adb shell pm clear <applicationId>` |

## Quick Start (2026 Defaults)

- Prefer Gradle Managed Devices (GMD) + ATD images for CI; use `connectedAndroidTest` for local ad-hoc runs.
- Enable test isolation via AndroidX Test Orchestrator for instrumented tests.
- Disable animations via Gradle `testOptions` (preferred) instead of per-runner ADB steps.
- Keep selectors stable: `withId()` (Views), `testTag` (Compose), resource-id/content-desc (UIAutomator).

Recommended Gradle defaults for stable instrumented tests (version catalog names vary by project):

```kotlin
android {
    testOptions {
        animationsDisabled = true
        execution = "ANDROIDX_TEST_ORCHESTRATOR"
    }
}

dependencies {
    androidTestUtil(libs.androidx.test.orchestrator)
}
```

## When to Use

- Debug or stabilize flaky Android UI tests
- Add Espresso tests for View-based UIs
- Add Compose UI tests for composables
- Add UIAutomator tests for system UI or cross-app flows
- Set up an Android test gate in CI

## Inputs to Gather

- UI stack: Views, Compose, or mixed
- Test layer: unit, Robolectric, instrumented UI, UIAutomator/system
- CI target: PR gate vs nightly vs release; emulator vs device farm
- Device matrix: min/target API, form factors, locales (if relevant)
- Flake symptoms: timeouts, missing nodes, idling/sync, device-only issues
- App seams: DI hooks for fakes, feature flags, test accounts/test data

## Testing Layers

| Layer | Framework | Scope |
|-------|-----------|-------|
| Unit | JUnit + Mockito | JVM, no Android |
| Unit (Android) | Robolectric | JVM, simulated |
| UI (Views) | Espresso | Instrumented |
| UI (Compose) | Compose Testing | Instrumented |
| System | UIAutomator | Cross-app |

## Core Principles (Stability)

### Device Matrix

- Default: emulators for PR gates; real devices for release
- Cover: min supported API level, target API level, plus tablet/foldable if supported

### Flake Control

- Prefer Gradle `testOptions { animationsDisabled = true }` for instrumented tests
- Use AndroidX Test Orchestrator to isolate state and recover from crashes
- Use IdlingResources / Compose idling + `waitUntil` instead of sleeps
- Mock network with `MockWebServer` (or your DI fake) and avoid live backends
- Reset app state per test (test account/data, storage, feature flags)

## Writing Tests

- Espresso (Views): open `references/espresso-patterns.md`
- Compose: open `references/compose-testing.md`
- UIAutomator (system/cross-app): open `references/uiautomator.md`

## Workflows

### Add a New UI Test (Instrumented)

- Pick framework: Espresso (Views) vs Compose Testing vs UIAutomator boundary.
- Add stable selectors: View `id`, Compose `Modifier.testTag`, system `resource-id`/`content-desc`.
- Control externals: fake/mock network + deterministic test data.
- Add waits: IdlingResources / Compose idling + `waitUntil` (avoid sleeps).
- Run locally: `./gradlew connectedAndroidTest` (or a single test via runner args).

### Diagnose a Flaky Instrumented Test

- Confirm reproduces: run the test 10x; isolate to one device/API if needed.
- Remove nondeterminism: network, clock/timezone, locale, feature flags, animations.
- Replace sleeps with idling/explicit waits; validate your IdlingResource actually idles.
- Capture artifacts: logcat + screenshot + screen recording for failures.
- If still flaky, isolate app state (orchestrator + clear data) and bisect the interaction steps.

### Add a CI Gate (Preferred: GMD)

- Configure GMD + ATD images (see `references/gradle-managed-devices.md`).
- Run PR gate on a small matrix; expand via groups for nightly/release.
- Ensure artifacts upload on failure: `**/build/reports/androidTests/`, screenshots/logcat.

## ADB Commands (Triage)

```bash
# Screenshot
adb exec-out screencap -p > screenshot.png

# Screen recording
adb shell screenrecord /sdcard/demo.mp4
```

## CI Integration

Preferred: Gradle Managed Devices (GMD). See `references/gradle-managed-devices.md`.

```yaml
# .github/workflows/android.yml
name: Android CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      - uses: gradle/actions/setup-gradle@v3
      - run: ./gradlew test pixel6api34DebugAndroidTest
```

## Navigating References

The reference guides are intentionally large; search within them instead of loading everything:

- `rg -n \"^## \" frameworks/shared-skills/skills/qa-testing-android/references/compose-testing.md`
- `rg -n \"Idling|waitUntil|Synchronization\" frameworks/shared-skills/skills/qa-testing-android/references/compose-testing.md`
- `rg -n \"RecyclerView|Intents\" frameworks/shared-skills/skills/qa-testing-android/references/espresso-patterns.md`

## Do / Avoid

### Do

- Prefer orchestrator + per-test isolation for instrumented tests
- Use IdlingResources / `waitUntil` for async waits
- Use Robot/Page Object patterns for readability and reuse
- Run a small device matrix on PRs; expand on nightly/release

### Avoid

- `Thread.sleep()` for synchronization
- Tests depending on live network/backends
- Flaky selectors (localized text, position-only selectors)

## Resources

| Resource | Purpose |
|----------|---------|
| [references/espresso-patterns.md](references/espresso-patterns.md) | Espresso matchers, actions |
| [references/compose-testing.md](references/compose-testing.md) | Compose testing guide |
| [references/uiautomator.md](references/uiautomator.md) | UIAutomator patterns (system UI) |
| [references/gradle-managed-devices.md](references/gradle-managed-devices.md) | Managed Devices for CI |
| [data/sources.json](data/sources.json) | Documentation links |

## Templates

| Template | Purpose |
|----------|---------|
| [assets/template-android-test-checklist.md](assets/template-android-test-checklist.md) | Stability checklist |

## Related Skills

| Skill | Purpose |
|-------|---------|
| [software-mobile](../software-mobile/SKILL.md) | Android development |
| [qa-testing-strategy](../qa-testing-strategy/SKILL.md) | Test strategy |
| [qa-testing-mobile](../qa-testing-mobile/SKILL.md) | Cross-platform mobile |
