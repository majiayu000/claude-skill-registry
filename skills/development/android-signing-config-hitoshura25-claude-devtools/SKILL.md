---
name: android-signing-config
description: Configure Android release build signing with dual-source credentials (env vars + gradle.properties)
category: android
version: 1.0.0
inputs:
  - project_path: Path to Android project
  - keystores_created: Keystores must exist in keystores/ directory
outputs:
  - Updated app/build.gradle.kts with signingConfigs
verify: "./gradlew assembleRelease"
---

# Android Signing Configuration

Configures release build signing with dual-source strategy: environment variables (CI/CD) and gradle.properties (local dev).

## Prerequisites

- Keystores exist in `keystores/` directory (run `android-keystore-generation` first)
- Android project with Gradle
- Kotlin DSL (build.gradle.kts)

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| project_path | Yes | . | Android project root |

## Process

### Step 1: Detect and Select Environment Variable Prefix

**Purpose:** Avoid variable name conflicts with other projects by using a project-specific prefix.

**Step 1a: Auto-detect project name**

```bash
# From settings.gradle.kts
PROJECT_NAME=$(grep "rootProject.name" settings.gradle.kts | sed 's/.*"\(.*\)".*/\1/' | tr '[:lower:]' '[:upper:]' | tr '-' '_')
echo "Detected project: $PROJECT_NAME"
```

**Step 1b: Ask user for prefix preference**

> "Choose environment variable prefix for signing configuration:
> 1. **${PROJECT_NAME}** (detected from project) - e.g., `${PROJECT_NAME}_SIGNING_KEY_STORE_PATH`
> 2. **APP** (generic) - e.g., `APP_SIGNING_KEY_STORE_PATH`
> 3. **Custom** - Enter your own prefix
>
> Select option (1/2/3):"

**Step 1c: Store selected prefix**

```bash
# Based on user selection:
# Option 1: PREFIX="$PROJECT_NAME"
# Option 2: PREFIX="APP"
# Option 3: PREFIX="{user_custom_prefix}"

echo "Using prefix: $PREFIX"
echo "Example variable: ${PREFIX}_SIGNING_KEY_STORE_PATH"
```

**GitHub Secrets to create later:**
- `${PREFIX}_SIGNING_KEY_STORE_BASE64`
- `${PREFIX}_SIGNING_KEY_ALIAS`
- `${PREFIX}_SIGNING_STORE_PASSWORD`
- `${PREFIX}_SIGNING_KEY_PASSWORD`

### Step 2: Add Signing Configuration to build.gradle.kts

Update `app/build.gradle.kts` to add signing configuration:

```kotlin
android {
    namespace = "com.example.app" // Keep existing
    compileSdk = 34 // Keep existing

    defaultConfig {
        // Keep existing config
    }

    // ADD THIS SECTION
    signingConfigs {
        create("release") {
            // Use the prefix selected in Step 1 (replace {PREFIX} with actual prefix)
            val prefix = "{PREFIX}"  // e.g., "APP" or project-specific prefix

            // Priority: environment variables (CI/CD) > gradle.properties (local dev)
            val keystorePath = System.getenv("${prefix}_SIGNING_KEY_STORE_PATH")
                ?: project.findProperty("${prefix}_SIGNING_KEY_STORE_PATH")?.toString()
            val storePass = System.getenv("${prefix}_SIGNING_STORE_PASSWORD")
                ?: project.findProperty("${prefix}_SIGNING_STORE_PASSWORD")?.toString()
            val alias = System.getenv("${prefix}_SIGNING_KEY_ALIAS")
                ?: project.findProperty("${prefix}_SIGNING_KEY_ALIAS")?.toString()
            val keyPass = System.getenv("${prefix}_SIGNING_KEY_PASSWORD")
                ?: project.findProperty("${prefix}_SIGNING_KEY_PASSWORD")?.toString()

            if (keystorePath != null && storePass != null && alias != null && keyPass != null) {
                storeFile = file(keystorePath)
                storePassword = storePass
                keyAlias = alias
                // For PKCS12 keystores, storePassword and keyPassword must be identical
                keyPassword = keyPass
            }
        }
    }

    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
            // ProGuard config set by android-proguard-setup skill
        }
    }

    // Validate signing config only when building release variants
    tasks.matching {
        it.name.matches(Regex(".*[aA]ssemble.*Release.*|.*[bB]undle.*Release.*"))
    }.configureEach {
        doFirst {
            val releaseConfig = android.signingConfigs.getByName("release")
            if (releaseConfig.storeFile == null) {
                throw GradleException(
                    """
                    Release signing not configured!

                    For CI/CD: Set environment variables (using prefix: $prefix):
                      - ${prefix}_SIGNING_KEY_STORE_PATH
                      - ${prefix}_SIGNING_STORE_PASSWORD
                      - ${prefix}_SIGNING_KEY_ALIAS
                      - ${prefix}_SIGNING_KEY_PASSWORD

                    For local development: Add to ~/.gradle/gradle.properties:
                      ${prefix}_SIGNING_KEY_STORE_PATH=/path/to/local-dev-release.jks
                      ${prefix}_SIGNING_STORE_PASSWORD=your-password
                      ${prefix}_SIGNING_KEY_ALIAS=local-dev
                      ${prefix}_SIGNING_KEY_PASSWORD=your-password
                    """.trimIndent()
                )
            }
        }
    }
}
```

**Detection logic:**
- Check if `signingConfigs` already exists - update if present
- Check if release `buildType` already has signingConfig - preserve other settings
- Don't modify ProGuard settings (handled by separate skill)

### Step 2: Update .gitignore

Ensure sensitive files are gitignored:

```bash
# Add to .gitignore if not present
grep -q "gradle.properties" .gitignore 2>/dev/null || echo -e "\n# Gradle properties with secrets\ngradle.properties" >> .gitignore
```

### Step 3: Configure Local Development

Ask user permission to update `~/.gradle/gradle.properties`:

```bash
# Read credentials from KEYSTORE_INFO.txt
LOCAL_PASSWORD=$(grep "Local.*Store Password:" keystores/KEYSTORE_INFO.txt | cut -d: -f2 | xargs)
PROJECT_PATH=$(pwd)
PREFIX="{PREFIX}"  # Use the prefix selected in Step 1

# Add to ~/.gradle/gradle.properties (using selected prefix)
cat >> ~/.gradle/gradle.properties << EOF

# ${PROJECT_PATH} (using prefix: ${PREFIX})
${PREFIX}_SIGNING_KEY_STORE_PATH=${PROJECT_PATH}/keystores/local-dev-release.jks
${PREFIX}_SIGNING_KEY_ALIAS=local-dev
${PREFIX}_SIGNING_STORE_PASSWORD=${LOCAL_PASSWORD}
${PREFIX}_SIGNING_KEY_PASSWORD=${LOCAL_PASSWORD}
EOF
```

**Important:** Always ask permission before modifying user's global gradle.properties!

## Verification

**MANDATORY:** Run this command to verify signing works:

```bash
# Build release APK
./gradlew assembleRelease

# Verify APK exists
ls -lh app/build/outputs/apk/release/app-release.apk

# Verify APK signature (supports APK Signature Scheme v2/v3)
$ANDROID_HOME/build-tools/34.0.0/apksigner verify --verbose app/build/outputs/apk/release/app-release.apk

# Or if apksigner is in PATH:
apksigner verify --verbose app/build/outputs/apk/release/app-release.apk
```

**Expected output:**
- Release build succeeds
- APK file exists
- `apksigner` shows "Verifies" with v2/v3 scheme confirmation

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Signing config | app/build.gradle.kts | Dual-source signing configuration |
| Local config | ~/.gradle/gradle.properties | Local dev credentials |

## Troubleshooting

### "Signing config not found"
**Cause:** gradle.properties not configured correctly
**Fix:** Verify ~/.gradle/gradle.properties has correct paths and passwords

### "Cannot find keystore file"
**Cause:** Path in gradle.properties is incorrect
**Fix:** Use absolute path: `/full/path/to/keystores/local-dev-release.jks`

### "apksigner verification fails"
**Cause:** Wrong keystore or passwords
**Fix:** Double-check credentials in KEYSTORE_INFO.txt

## Completion Criteria

- [ ] `signingConfigs.release` exists in app/build.gradle.kts
- [ ] Release buildType uses signingConfig
- [ ] `~/.gradle/gradle.properties` configured (or env vars set for CI)
- [ ] `./gradlew assembleRelease` succeeds
- [ ] `apksigner verify` confirms APK is signed (v2/v3 schemes)
