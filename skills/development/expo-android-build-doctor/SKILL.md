---
name: expo-android-build-doctor
description: Diagnose and fix Expo/React Native Android Gradle build failures, especially Kotlin metadata/version mismatches (e.g., "Module was compiled with an incompatible version of Kotlin" / metadata 2.1.0 vs expected 1.9.0) when running `npx expo run:android`, `./android/gradlew assembleDebug`, or EAS local Android builds.
---

# Expo Android Build Doctor

## Overview

Triage Android build failures in Expo (prebuild/dev-client) projects and apply targeted fixes with minimal churn. Focus on Kotlin/Gradle version alignment issues that block `:app:compileDebugKotlin`.

## Workflow

### 1) Reproduce and isolate the failing task

- Prefer `./android/gradlew :app:compileDebugKotlin --stacktrace` to avoid Expo CLI noise.
- Only treat errors as blockers; warnings like `CXX5304` usually aren’t fatal.

### 2) If you see a Kotlin metadata/version mismatch

**Trigger strings (any of these):**
- `Module was compiled with an incompatible version of Kotlin`
- `The binary version of its metadata is 2.1.0, expected version is 1.9.0`
- Errors pointing at `.../META-INF/*.kotlin_module` inside a `.jar`

**First: look for dependency overrides that upgraded Firebase/Play Services.**
- Search for app-level/platform overrides like `firebase-bom` in `android/app/build.gradle`.
- If you’re using `@react-native-firebase/*`, avoid adding your own Firebase BoM + `firebase-analytics` in the app module; it can force newer transitive deps than your toolchain supports.

**Then (if still needed): upgrade project Kotlin to match the dependency’s metadata.**

For Expo/RN Android projects, align these in one pass:
- Root `android/build.gradle` (Kotlin version + kotlin-gradle-plugin)
- `android/react-settings-plugin/build.gradle.kts` (Kotlin JVM plugin)

Use the script:
- `python3 skills/expo-android-build-doctor/scripts/bump_kotlin_version.py --version 2.1.0 --apply`

Then rebuild:
- `./android/gradlew :app:compileDebugKotlin`

If upgrading Kotlin causes Gradle evaluation errors (plugin incompatibility), revert and instead pin/downgrade the dependency that introduced newer Kotlin metadata.

If it still fails, identify what pulled in the Kotlin-2.x compiled artifact:
- `./android/gradlew :app:dependencies --configuration debugCompileClasspath`

### 3) If you see Google Mobile Ads `android_app_id` warning

This warning is not a build failure but it *will* crash at runtime if you’re using the native SDK.
- Ensure `app.json`/`app.config.*` includes `react-native-google-mobile-ads.android_app_id`, or confirm you’re using the library’s Expo config plugin that injects it.

## References

Read `skills/expo-android-build-doctor/references/kotlin-metadata-mismatch.md` when you need background or alternative mitigation options.
