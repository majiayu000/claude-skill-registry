---
name: project-metadata
description: Guide for updating app name, bundle identifier, and company metadata across all platforms (project)
---

# Flutter App Metadata Skill

This skill guides updating application metadata (app name, bundle identifier, company info) across all platforms in this Flutter project.

## When to Use

Trigger this skill when:
- Renaming the application
- Changing the bundle/application identifier
- Updating company name or copyright information
- Setting up a new project from this template
- User asks to "change app name", "update identifier", "rename app", or "change bundle id"

## Quick Reference: All Files to Update

| Platform | File | What to Change |
|----------|------|----------------|
| **Android** | `android/app/build.gradle.kts` | `namespace`, `applicationId` |
| **Android** | `android/app/src/main/kotlin/<package>/MainActivity.kt` | `package` declaration + directory path |
| **Android** | `android/fastlane/Appfile` | `package_name` |
| **iOS** | `ios/Runner.xcodeproj/project.pbxproj` | `PRODUCT_BUNDLE_IDENTIFIER` (6 occurrences) |
| **iOS** | `ios/fastlane/Appfile` | `app_identifier` |
| **iOS** | `ios/fastlane/Matchfile` | `app_identifier` |
| **iOS** | `ios/fastlane/Fastfile` | `bundle_identifier`, profile names |
| **macOS** | `macos/Runner/Configs/AppInfo.xcconfig` | `PRODUCT_NAME`, `PRODUCT_BUNDLE_IDENTIFIER`, `PRODUCT_COPYRIGHT` |
| **macOS** | `macos/Runner.xcodeproj/project.pbxproj` | `PRODUCT_BUNDLE_IDENTIFIER` (3 occurrences) |
| **Linux** | `linux/CMakeLists.txt` | `BINARY_NAME`, `APPLICATION_ID` |
| **Windows** | `windows/runner/Runner.rc` | `CompanyName`, `FileDescription`, `InternalName`, `LegalCopyright`, `OriginalFilename`, `ProductName` |
| **Flutter** | `pubspec.yaml` | `name`, `description` |

## Detailed Platform Updates

### 1. Flutter (pubspec.yaml)

```yaml
name: my_app_name          # Package name (snake_case)
description: My App Description
```

### 2. Android

#### build.gradle.kts
Location: `android/app/build.gradle.kts`

```kotlin
android {
    namespace = "com.example.myapp"        // Line ~19
    // ...
    defaultConfig {
        applicationId = "com.example.myapp" // Line ~33
    }
}
```

#### MainActivity.kt
Location: `android/app/src/main/kotlin/<package>/MainActivity.kt`

**Important:** The directory structure must match the package name!

```kotlin
package com.example.myapp  // Must match applicationId

import io.flutter.embedding.android.FlutterActivity

class MainActivity : FlutterActivity()
```

**Directory rename required:**
```bash
# Old: android/app/src/main/kotlin/dev/gsmlg/flutter_app_template/
# New: android/app/src/main/kotlin/com/example/myapp/

mkdir -p android/app/src/main/kotlin/com/example/myapp
mv android/app/src/main/kotlin/<old>/<package>/MainActivity.kt \
   android/app/src/main/kotlin/com/example/myapp/
rm -rf android/app/src/main/kotlin/<old>
```

#### Fastlane Appfile
Location: `android/fastlane/Appfile`

```ruby
package_name("com.example.myapp")
```

### 3. iOS

#### Xcode Project
Location: `ios/Runner.xcodeproj/project.pbxproj`

Search and replace all occurrences of `PRODUCT_BUNDLE_IDENTIFIER`:
- Main app: `com.example.myapp`
- Tests: `com.example.myapp.RunnerTests`

**6 occurrences total** (Debug, Release, Profile for both Runner and RunnerTests)

#### Fastlane Files

**Appfile** (`ios/fastlane/Appfile`):
```ruby
app_identifier("com.example.myapp")
```

**Matchfile** (`ios/fastlane/Matchfile`):
```ruby
app_identifier(["com.example.myapp"])
```

**Fastfile** (`ios/fastlane/Fastfile`):
```ruby
# In update_code_signing_settings:
bundle_identifier: "com.example.myapp",
profile_name: ENV["sigh_com.example.myapp_appstore_profile-name"] || "match AppStore com.example.myapp",

# In export_options provisioningProfiles:
"com.example.myapp" => ENV["sigh_com.example.myapp_appstore_profile-name"] || "match AppStore com.example.myapp"
```

### 4. macOS

#### AppInfo.xcconfig
Location: `macos/Runner/Configs/AppInfo.xcconfig`

```xcconfig
PRODUCT_NAME = my_app_name
PRODUCT_BUNDLE_IDENTIFIER = com.example.myapp
PRODUCT_COPYRIGHT = Copyright © 2025 My Company. All rights reserved.
```

#### Xcode Project
Location: `macos/Runner.xcodeproj/project.pbxproj`

Search and replace `PRODUCT_BUNDLE_IDENTIFIER`:
- Tests: `com.example.myapp.RunnerTests`

**3 occurrences** (Debug, Release, Profile for RunnerTests)

### 5. Linux

Location: `linux/CMakeLists.txt`

```cmake
set(BINARY_NAME "my_app_name")
set(APPLICATION_ID "com.example.myapp")
```

### 6. Windows

Location: `windows/runner/Runner.rc`

```rc
BEGIN
    BLOCK "StringFileInfo"
    BEGIN
        BLOCK "040904e4"
        BEGIN
            VALUE "CompanyName", "My Company" "\0"
            VALUE "FileDescription", "My App Name" "\0"
            VALUE "FileVersion", VERSION_AS_STRING "\0"
            VALUE "InternalName", "my_app_name" "\0"
            VALUE "LegalCopyright", "Copyright (C) 2025 My Company. All rights reserved." "\0"
            VALUE "OriginalFilename", "my_app_name.exe" "\0"
            VALUE "ProductName", "My App Name" "\0"
            VALUE "ProductVersion", VERSION_AS_STRING "\0"
        END
    END
END
```

## Identifier Naming Conventions

| Platform | Format | Example |
|----------|--------|---------|
| Android | Lowercase, dots, underscores | `com.example.my_app` |
| iOS/macOS | Reverse domain, mixed case OK | `com.example.myApp` |
| Linux | Lowercase, dots only | `com.example.myapp` |
| Windows | N/A (uses company name) | `My Company` |

**Recommended:** Use consistent lowercase with dots across all platforms:
- `app.mycompany.myappname`

## Automated Rename Script

This project includes a setup script for initial renaming:

```bash
dart run bin/setup_project.dart my_new_project_name
```

**Note:** This script handles basic renaming but may not update all metadata fields. Use this skill for comprehensive updates.

## Post-Update Checklist

After updating metadata:

1. **Android**: Clean and rebuild
   ```bash
   cd android && ./gradlew clean
   flutter clean && flutter pub get
   ```

2. **iOS**: Reinstall pods and regenerate
   ```bash
   cd ios && rm -rf Pods Podfile.lock && pod install
   ```

3. **iOS/macOS Signing**: If bundle ID changed, regenerate certificates
   ```bash
   cd ios/fastlane && fastlane match nuke appstore  # Caution: removes existing
   cd ios/fastlane && fastlane sync_certificates
   ```

4. **Verify Build**:
   ```bash
   flutter clean
   melos bootstrap
   flutter build apk --debug
   flutter build ios --debug --no-codesign
   flutter build macos --debug
   flutter build linux --debug
   flutter build windows --debug
   ```

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Android build fails | Package directory mismatch | Ensure Kotlin directory matches `applicationId` |
| iOS signing fails | Bundle ID changed | Regenerate provisioning profiles |
| App won't install over old | Different identifier | Uninstall old app first |
| macOS sandbox issues | Bundle ID mismatch | Update entitlements if needed |

## Search Commands

Find all identifier references:
```bash
# Find old identifier pattern
grep -r "old\.identifier" --include="*.gradle*" --include="*.kt" --include="*.pbxproj" \
  --include="*.xcconfig" --include="*.rc" --include="*.cmake" --include="Appfile" \
  --include="Matchfile" --include="Fastfile" --include="pubspec.yaml" .
```

## Example: Full Rename

Renaming from `dev.gsmlg.flutterAppTemplate` to `app.mycompany.myapp`:

```bash
# 1. Update pubspec.yaml name
# 2. Update Android (build.gradle.kts, MainActivity.kt + directory, Appfile)
# 3. Update iOS (project.pbxproj, Appfile, Matchfile, Fastfile)
# 4. Update macOS (AppInfo.xcconfig, project.pbxproj)
# 5. Update Linux (CMakeLists.txt)
# 6. Update Windows (Runner.rc)
# 7. Clean and rebuild all platforms
```
