---
name: android-release
description: App signing, bundling, and Play Store deployment automation. Use when signing APK/AAB, generating release builds, preparing Play Store upload, or configuring ProGuard.
license: MIT
version: 1.0.0
---

# Android Release Skill

App signing, bundling, and Play Store deployment automation.

## When to Use

- Signing APK/AAB for release
- Generating release builds
- Preparing Play Store upload
- Managing signing keys
- Configuring ProGuard/R8

## Signing Configuration

### keystore.properties (gitignored)

```properties
storeFile=release-key.jks
storePassword=your_store_password
keyAlias=your_key_alias
keyPassword=your_key_password
```

### build.gradle.kts

```kotlin
val keystoreProperties = Properties().apply {
    val file = file("keystore.properties")
    if (file.exists()) file.inputStream().use { load(it) }
}

android {
    signingConfigs {
        create("release") {
            storeFile = file(keystoreProperties["storeFile"] as String)
            storePassword = keystoreProperties["storePassword"] as String
            keyAlias = keystoreProperties["keyAlias"] as String
            keyPassword = keystoreProperties["keyPassword"] as String
        }
    }
    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
}
```

## Build Commands

```bash
# Build signed AAB (for Play Store)
./gradlew bundleRelease

# Build signed APK
./gradlew assembleRelease

# Clean and build
./gradlew clean bundleRelease

# Build with specific variant
./gradlew bundleProdRelease
```

## ProGuard/R8 Rules

```proguard
# Keep data classes for serialization
-keepclassmembers class * {
    @kotlinx.serialization.Serializable *;
}

# Keep Compose
-keep class androidx.compose.** { *; }
-dontwarn androidx.compose.**

# Keep Koin
-keep class org.koin.** { *; }

# Keep Supabase/Ktor
-keep class io.github.jan.supabase.** { *; }
-keep class io.ktor.** { *; }

# Keep Retrofit models (if used)
-keepclassmembers class * {
    @com.google.gson.annotations.SerializedName <fields>;
}

# Remove debug logs
-assumenosideeffects class android.util.Log {
    public static int d(...);
    public static int v(...);
}
```

## Play Store Deployment

### Using Gradle Play Publisher Plugin

```kotlin
// plugins block
id("com.github.triplet.play") version "3.10.1"

play {
    serviceAccountCredentials.set(file("play-service-account.json"))
    track.set("internal") // internal, alpha, beta, production
    defaultToAppBundles.set(true)
}
```

```bash
# Upload to internal testing
./gradlew publishBundle

# Upload to production
./gradlew publishReleaseBundle --track production

# Promote from internal to production
./gradlew promoteArtifact --from-track internal --to-track production
```

### Manual Upload

1. Build AAB: `./gradlew bundleRelease`
2. Find at: `app/build/outputs/bundle/release/app-release.aab`
3. Upload via Play Console

## Version Management

```kotlin
android {
    defaultConfig {
        versionCode = 10
        versionName = "1.2.0"
    }
}

// Or auto-generate from git
val gitVersionCode = "git rev-list --count HEAD".execute().toInt()
val gitVersionName = "git describe --tags --always".execute()
```

## Version Compatibility

| AGP | Gradle | JDK | Target SDK |
|-----|--------|-----|------------|
| 8.8+ | 8.10+ | 17+ | 35 |
| 8.5+ | 8.5+ | 17+ | 34 |

## Error Handling

```bash
# Validate AAB before upload
bundletool validate --bundle=app-release.aab

# Check signing
jarsigner -verify -verbose -certs app-release.apk

# Test release build locally
./gradlew assembleRelease && adb install -r app/build/outputs/apk/release/app-release.apk
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Signing failed | Verify keystore path and passwords |
| ProGuard errors | Add keep rules for affected classes |
| APK too large | Enable R8 shrinking, check resources |
| Upload rejected | Check version code, target SDK |

## Security Checklist

- [ ] Keystore NOT in version control
- [ ] Passwords in environment variables
- [ ] Play App Signing enabled
- [ ] ProGuard/R8 enabled for release
- [ ] Service account key secured
- [ ] Backup rules exclude sensitive data

## CI/CD Integration

```yaml
# GitHub Actions Release
- name: Build Release
  run: ./gradlew bundleRelease
  env:
    KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
    KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}

- name: Upload to Play Store
  uses: r0adkll/upload-google-play@v1
  with:
    serviceAccountJsonPlainText: ${{ secrets.SERVICE_ACCOUNT_JSON }}
    packageName: com.example.app
    releaseFiles: app/build/outputs/bundle/release/app-release.aab
    track: internal
```

## Release Checklist

- [ ] Version code/name incremented
- [ ] ProGuard rules updated for new libraries
- [ ] Release notes prepared
- [ ] Screenshots updated (if UI changed)
- [ ] Test on release build before upload
- [ ] Staged rollout configured

## References

- [App Signing](https://developer.android.com/studio/publish/app-signing)
- [Play Console](https://play.google.com/console)
- [R8 Shrinking](https://developer.android.com/build/shrink-code)
- [Gradle Play Publisher](https://github.com/Triple-T/gradle-play-publisher)

Use this skill for secure, automated release workflows.
