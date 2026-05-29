---
name: android-build-apk-copy
description: Build TermLink Android debug APK only, then copy the generated APK to E:\\project\\TermLink. Use when you only need a fresh APK artifact for distribution/testing without install or adb debug steps.
---

# Android Build APK Copy

Use this skill when you only need to compile APK and copy artifact.

Run commands from repository root:
`E:\coding\TermLink`

## Quick Start

```powershell
powershell -ExecutionPolicy Bypass -File ./skills/android-build-apk-copy/scripts/build-apk-and-copy.ps1
```

## Behavior

1. Run `npm run android:sync`.
2. Run `android\\gradlew.bat :app:assembleDebug`.
3. Copy `android/app/build/outputs/apk/debug/app-debug.apk` to `E:\project\TermLink`.

## Optional Parameters

```powershell
powershell -ExecutionPolicy Bypass -File ./skills/android-build-apk-copy/scripts/build-apk-and-copy.ps1 -OutDir E:\project\TermLink -OutName app-debug.apk -JdkHome D:\ProgramCode\openjdk\jdk-21
```

## Rules

1. This skill does not install APK to device.
2. Keep default output directory as `E:\project\TermLink`.
3. Build requires JDK 21 compatible environment.
