---
name: distributing-tauri-for-android
description: Guides the user through distributing Tauri applications for Android, including Google Play Store submission, APK and AAB generation, build configuration, signing setup, and version management.
---

# Distributing Tauri Apps for Android

This skill covers the complete workflow for preparing and distributing Tauri v2 applications on Android, including Google Play Store publication.

## Prerequisites

Before distributing your Tauri app for Android:

1. **Play Console Account**: Create a developer account at https://play.google.com/console/developers
2. **Android SDK**: Ensure Android SDK is installed and configured
3. **Code Signing**: Set up Android code signing (keystore)
4. **Tauri Android Initialized**: Run `tauri android init` if not already done

## App Icon Configuration

After initializing Android support, configure your app icon:

```bash
# npm
npm run tauri icon /path/to/app-icon.png

# yarn
yarn tauri icon /path/to/app-icon.png

# pnpm
pnpm tauri icon /path/to/app-icon.png

# cargo
cargo tauri icon /path/to/app-icon.png
```

This generates icons in all required sizes for Android.

## Build Configuration

### tauri.conf.json Android Settings

Configure Android-specific settings in your `tauri.conf.json`:

```json
{
  "bundle": {
    "android": {
      "minSdkVersion": 24,
      "versionCode": 1
    }
  }
}
```

### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `minSdkVersion` | 24 | Minimum Android SDK version (Android 7.0) |
| `versionCode` | Auto-calculated | Integer version code for Play Store |

### Version Code Calculation

Tauri automatically calculates the version code from your app version:

```
versionCode = major * 1000000 + minor * 1000 + patch
```

**Example**: Version `1.2.3` becomes version code `1002003`

Override this in `tauri.conf.json` if you need sequential numbering:

```json
{
  "bundle": {
    "android": {
      "versionCode": 42
    }
  }
}
```

### Minimum SDK Version

Default minimum is Android 7.0 (SDK 24). For higher requirements:

```json
{
  "bundle": {
    "android": {
      "minSdkVersion": 28
    }
  }
}
```

**Common SDK versions**:
- SDK 24: Android 7.0 (Nougat)
- SDK 26: Android 8.0 (Oreo)
- SDK 28: Android 9.0 (Pie)
- SDK 29: Android 10
- SDK 30: Android 11
- SDK 31: Android 12
- SDK 33: Android 13
- SDK 34: Android 14

## Building for Distribution

### Android App Bundle (AAB) - Recommended

Google Play requires AAB format for new apps. Generate an AAB:

```bash
# npm
npm run tauri android build -- --aab

# yarn
yarn tauri android build --aab

# pnpm
pnpm tauri android build -- --aab

# cargo
cargo tauri android build --aab
```

**Output location**:
```
gen/android/app/build/outputs/bundle/universalRelease/app-universal-release.aab
```

### APK Generation

For testing or alternative distribution channels:

```bash
# npm
npm run tauri android build -- --apk

# yarn
yarn tauri android build --apk

# pnpm
pnpm tauri android build -- --apk

# cargo
cargo tauri android build --apk
```

### Architecture-Specific Builds

Build for specific CPU architectures:

```bash
# Single architecture
npm run tauri android build -- --target aarch64

# Multiple architectures
npm run tauri android build -- --target aarch64 --target armv7
```

**Available targets**:
- `aarch64` - ARM 64-bit (most modern devices)
- `armv7` - ARM 32-bit (older devices)
- `i686` - Intel 32-bit (emulators)
- `x86_64` - Intel 64-bit (emulators, some Chromebooks)

### Split APKs by Architecture

Create separate APKs per architecture (useful for testing):

```bash
npm run tauri android build -- --apk --split-per-abi
```

**Note**: Not needed for Play Store submission. Google Play automatically serves the correct architecture from your AAB.

## Code Signing

### Generate a Keystore

Create a release keystore for signing:

```bash
keytool -genkey -v -keystore release-key.keystore \
  -alias my-app-alias \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000
```

**Important**: Store your keystore securely. Losing it means you cannot update your app.

### Configure Signing in Gradle

Create or update `gen/android/keystore.properties`:

```properties
storePassword=your_store_password
keyPassword=your_key_password
keyAlias=my-app-alias
storeFile=/path/to/release-key.keystore
```

Update `gen/android/app/build.gradle.kts` to use the keystore:

```kotlin
import java.util.Properties
import java.io.FileInputStream

val keystorePropertiesFile = rootProject.file("keystore.properties")
val keystoreProperties = Properties()
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(FileInputStream(keystorePropertiesFile))
}

android {
    signingConfigs {
        create("release") {
            keyAlias = keystoreProperties["keyAlias"] as String
            keyPassword = keystoreProperties["keyPassword"] as String
            storeFile = file(keystoreProperties["storeFile"] as String)
            storePassword = keystoreProperties["storePassword"] as String
        }
    }
    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
        }
    }
}
```

### Environment Variables for CI/CD

For automated builds, use environment variables:

```kotlin
android {
    signingConfigs {
        create("release") {
            keyAlias = System.getenv("ANDROID_KEY_ALIAS")
            keyPassword = System.getenv("ANDROID_KEY_PASSWORD")
            storeFile = file(System.getenv("ANDROID_KEYSTORE_PATH"))
            storePassword = System.getenv("ANDROID_STORE_PASSWORD")
        }
    }
}
```

## Google Play Store Submission

### Pre-Submission Checklist

1. **App signed** with release keystore
2. **Version code** incremented from previous release
3. **App icon** configured in all required sizes
4. **Screenshots** prepared (required by Play Store)
5. **Privacy policy** URL ready (required for most apps)
6. **Content rating** questionnaire completed

### Upload Process

1. **Navigate** to Play Console: https://play.google.com/console/developers
2. **Create application** or select existing app
3. **Upload AAB** file from:
   ```
   gen/android/app/build/outputs/bundle/universalRelease/app-universal-release.aab
   ```
4. **Complete store listing** (title, description, screenshots)
5. **Set content rating**
6. **Configure pricing and distribution**
7. **Submit for review**

### First Release Requirements

The initial submission requires manual upload through Play Console for signature verification. Google will manage your app signing key through Play App Signing.

### Automation Note

Tauri currently does not offer built-in automation for creating Android releases. However, you can use the Google Play Developer API for automated submissions in CI/CD pipelines.

## Troubleshooting

### Build Fails with Signing Error

Ensure your keystore path is absolute or relative to the correct directory:

```properties
# Absolute path
storeFile=/Users/username/keys/release-key.keystore

# Relative to gen/android directory
storeFile=../../release-key.keystore
```

### Version Code Not Incrementing

If using auto-calculation, ensure your `package.json` or `Cargo.toml` version is updated. For manual control:

```json
{
  "bundle": {
    "android": {
      "versionCode": 2
    }
  }
}
```

### APK Not Installing on Device

Check minimum SDK version compatibility:

```bash
# Check device Android version
adb shell getprop ro.build.version.sdk
```

### AAB Too Large

Consider using `--split-per-abi` for testing, but for Play Store, Google handles this automatically. If still too large:

1. Optimize your frontend assets
2. Use dynamic feature modules
3. Enable ProGuard/R8 minification

## Quick Reference

### Common Build Commands

```bash
# Development build
npm run tauri android dev

# Release AAB for Play Store
npm run tauri android build -- --aab

# Release APK for testing
npm run tauri android build -- --apk

# Specific architecture
npm run tauri android build -- --aab --target aarch64
```

### File Locations

| File | Location |
|------|----------|
| AAB output | `gen/android/app/build/outputs/bundle/universalRelease/app-universal-release.aab` |
| APK output | `gen/android/app/build/outputs/apk/universal/release/app-universal-release-unsigned.apk` |
| Gradle config | `gen/android/app/build.gradle.kts` |
| Keystore properties | `gen/android/keystore.properties` |
| Android manifest | `gen/android/app/src/main/AndroidManifest.xml` |

### Resources

- [Google Play Console](https://play.google.com/console/developers)
- [Tauri Android Documentation](https://v2.tauri.app/distribute/google-play)
- [Google Play Release Checklist](https://developer.android.com/distribute/best-practices/launch/launch-checklist)
- [Play App Signing](https://developer.android.com/studio/publish/app-signing)
