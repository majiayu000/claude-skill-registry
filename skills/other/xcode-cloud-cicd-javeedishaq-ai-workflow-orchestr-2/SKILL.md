---
description: Xcode Cloud CI/CD setup for Flutter iOS apps. Covers ci_post_clone.sh scripts, workflow configuration, TestFlight deployment, environment secrets, App Store distribution, and API management. Use when setting up CI/CD, troubleshooting builds, deploying to TestFlight/App Store, or managing workflows via API.
version: "1.2.0"
updated: "2025-12-23"
---

# Xcode Cloud CI/CD for Flutter

Comprehensive guide for setting up Xcode Cloud CI/CD for the Ballee Flutter iOS app.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [ci_post_clone.sh Script](#ci_post_clonesh-script)
4. [Xcode Cloud Workflow Setup](#xcode-cloud-workflow-setup)
5. [Environment Variables & Secrets](#environment-variables--secrets)
6. [TestFlight Deployment](#testflight-deployment)
7. [App Store Distribution](#app-store-distribution)
8. [Local Build & Upload](#local-build--upload)
9. [Troubleshooting](#troubleshooting)
10. [App Store Connect API](#app-store-connect-api)

---

## Overview

Xcode Cloud provides native CI/CD for Apple platforms with:
- 25 free compute hours/month (Apple Developer Program)
- Native integration with App Store Connect
- Automatic TestFlight distribution
- Automatic code signing management

### Build Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     XCODE CLOUD BUILD                            │
├─────────────────────────────────────────────────────────────────┤
│  1. Clone Repository                                             │
│  2. Run ci_post_clone.sh (install Flutter, dependencies)        │
│  3. Build Flutter iOS app                                        │
│  4. Archive with automatic code signing                          │
│  5. Export IPA                                                   │
│  6. Upload to App Store Connect                                  │
│  7. Distribute to TestFlight                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

### App Store Connect Configuration

1. **App Created**: App must exist in App Store Connect
   - Bundle ID: `co.ballee`
   - Team: `A86CXY8H75` (Akson Engineering Sàrl)

2. **Certificates**:
   - Apple Distribution Certificate (required for distribution)
   - Apple Development Certificate (for development builds)

3. **API Key** (for local uploads):
   - Key ID: `LGU934Y2XR`
   - Issuer ID: `69a6de96-5d75-47e3-e053-5b8c7c11a4d1`
   - Stored in 1Password: "App Store Connect API Key"
   - Local path: `~/.appstoreconnect/private_keys/AuthKey_LGU934Y2XR.p8`

### Repository Requirements

- Repository connected to Xcode Cloud: `antoineschaller/ballee`
- `ios/ci_scripts/ci_post_clone.sh` script present
- Valid `ios/Podfile` with correct target name

### CLI Management Tool

A Python CLI tool is available for managing Xcode Cloud via App Store Connect API:

```bash
# Location
apps/mobile/ios/scripts/xcode_cloud_cli.py

# Prerequisites
pip3 install pyjwt cryptography requests

# Commands
./xcode_cloud_cli.py list-products      # List Xcode Cloud products
./xcode_cloud_cli.py list-workflows     # List all workflows
./xcode_cloud_cli.py workflow-info <id> # Get workflow details
./xcode_cloud_cli.py delete-workflow <id>  # Delete a workflow
./xcode_cloud_cli.py trigger <id>       # Trigger a build
./xcode_cloud_cli.py build-status <id>  # Check build status
```

---

## ci_post_clone.sh Script

The `ci_post_clone.sh` script runs after Xcode Cloud clones the repository. It installs Flutter and builds the iOS app.

### Script Location

```
apps/mobile/ios/ci_scripts/ci_post_clone.sh
```

### Complete Script

```bash
#!/bin/sh
set -e

# ci_post_clone.sh for Ballee Flutter app
# This script runs after Xcode Cloud clones the repository
# Documentation: https://developer.apple.com/documentation/xcode/writing-custom-build-scripts

echo "=========================================="
echo "CI Post Clone Script - Ballee"
echo "=========================================="

# Navigate to mobile app root
cd "$CI_PRIMARY_REPOSITORY_PATH/apps/mobile"

# ========================================
# Install Flutter
# ========================================
echo "Installing Flutter..."

# Clone Flutter SDK to temp location
FLUTTER_DIR="$HOME/flutter"
if [ ! -d "$FLUTTER_DIR" ]; then
    git clone https://github.com/flutter/flutter.git -b stable "$FLUTTER_DIR"
fi

# Add Flutter to PATH
export PATH="$PATH:$FLUTTER_DIR/bin"

# Pre-download iOS artifacts
flutter precache --ios

# Accept licenses
flutter doctor --android-licenses || true

echo "Flutter version:"
flutter --version

# ========================================
# Install Ruby & CocoaPods (if needed)
# ========================================
echo "Setting up Ruby environment..."

# Xcode Cloud has Ruby but may need CocoaPods
if ! command -v pod &> /dev/null; then
    echo "Installing CocoaPods..."
    gem install cocoapods
fi

# ========================================
# Install Flutter Dependencies
# ========================================
echo "Installing Flutter dependencies..."
flutter pub get

# ========================================
# Generate Code (Freezed, Riverpod)
# ========================================
echo "Running build_runner..."
dart run build_runner build --delete-conflicting-outputs

# ========================================
# Build iOS (Release)
# ========================================
echo "Building Flutter iOS..."
flutter build ios --release --no-codesign

# ========================================
# Install CocoaPods Dependencies
# ========================================
echo "Installing CocoaPods dependencies..."
cd ios
pod install --repo-update

echo "=========================================="
echo "CI Post Clone Complete"
echo "=========================================="
```

### Script Permissions

```bash
chmod +x apps/mobile/ios/ci_scripts/ci_post_clone.sh
```

### Environment Variables in ci_post_clone.sh

| Variable | Description |
|----------|-------------|
| `CI_PRIMARY_REPOSITORY_PATH` | Path to cloned repository |
| `CI_WORKSPACE` | Xcode workspace path |
| `CI_PRODUCT` | Product being built |
| `CI_BRANCH` | Git branch name |
| `CI_TAG` | Git tag (if triggered by tag) |
| `CI_COMMIT` | Git commit SHA |

---

## Xcode Cloud Workflow Setup

### Create Workflow in Xcode

1. Open `apps/mobile/ios/Ballee.xcworkspace` in Xcode
2. Go to **Product > Xcode Cloud > Create Workflow**
3. Select the **Ballee** scheme

### Recommended Workflows

#### 1. Development Build (on PR)

**Start Conditions:**
- Pull Request Changes → `main` branch
- Branch Changes → `dev` branch

**Actions:**
- Build → iOS → Debug/Profile configuration
- No post-actions (just validates build)

#### 2. TestFlight Internal (on merge to main)

**Start Conditions:**
- Branch Changes → `main` branch

**Actions:**
- Archive → iOS → Release configuration

**Post-Actions:**
- Deploy to TestFlight (Internal Testing)
- Notify Slack/Email

#### 3. TestFlight External (on tag)

**Start Conditions:**
- Tag Changes → Pattern: `v*` (e.g., `v1.0.0`)

**Actions:**
- Archive → iOS → Release configuration

**Post-Actions:**
- Deploy to TestFlight (External Testing)
- Submit for Beta Review

### Workflow Configuration (YAML representation)

```yaml
# Conceptual representation - configure in Xcode UI
workflows:
  - name: "TestFlight Internal"
    triggers:
      - type: branch
        branch: main

    environment:
      xcode: latest_release
      macos: latest_release

    actions:
      - action: build
        platform: iOS
        scheme: Ballee
        configuration: Release

    post_actions:
      - action: testflight_internal
        groups:
          - "Internal Testers"
```

---

## Environment Variables & Secrets

### Setting Environment Variables in Xcode Cloud

1. Open workflow in Xcode
2. Go to **Environment** section
3. Add variables (mark sensitive ones as **Secret**)

### Required Variables

| Variable | Value | Secret |
|----------|-------|--------|
| `FLUTTER_VERSION` | `3.24.0` (or `stable`) | No |
| `SUPABASE_URL` | Your Supabase URL | No |
| `SUPABASE_ANON_KEY` | Your anon key | Yes |

### Accessing in ci_post_clone.sh

```bash
# Environment variables are automatically available
echo "Building for branch: $CI_BRANCH"
echo "Commit: $CI_COMMIT"

# Custom variables
if [ -n "$FLUTTER_VERSION" ]; then
    git -C "$FLUTTER_DIR" checkout "$FLUTTER_VERSION"
fi

# Create .env file for app
cat > .env << EOF
SUPABASE_URL=$SUPABASE_URL
SUPABASE_ANON_KEY=$SUPABASE_ANON_KEY
EOF
```

### Secret Management

Secrets are:
- Encrypted at rest
- Only available during build
- Not logged in build output
- Not accessible to forked PRs

---

## TestFlight Deployment

### Automatic Distribution

Configure in Xcode Cloud workflow:

1. **Post-Action**: TestFlight Internal Testing
2. **Groups**: Select internal tester groups
3. **Auto-distribute**: Enable for immediate distribution

### TestFlight Groups

| Group | Purpose | Review Required |
|-------|---------|-----------------|
| Internal Testing | Team members | No |
| External Testing | Beta testers | Yes (first build) |

### Build Number Management

Xcode Cloud auto-increments build numbers. To customize:

```bash
# In ci_post_clone.sh
BUILD_NUMBER=$CI_BUILD_NUMBER

# Update Info.plist
/usr/libexec/PlistBuddy -c "Set :CFBundleVersion $BUILD_NUMBER" ios/Ballee/Info.plist
```

---

## App Store Distribution

### ExportOptions.plist

For local builds and custom export configurations:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store-connect</string>
    <key>teamID</key>
    <string>A86CXY8H75</string>
    <key>uploadBitcode</key>
    <false/>
    <key>uploadSymbols</key>
    <true/>
    <key>signingStyle</key>
    <string>automatic</string>
    <key>destination</key>
    <string>upload</string>
</dict>
</plist>
```

### App Store Submission Workflow

**Start Conditions:**
- Tag Changes → Pattern: `release/*`

**Post-Actions:**
- Submit for App Review
- Set release type (manual/automatic)

---

## Local Build & Upload

### Full Build & Upload Script

```bash
#!/bin/bash
set -e

# Navigate to mobile app
cd apps/mobile

# Clean previous builds
rm -rf build/ios/archive build/ios/export

# Build Flutter
flutter build ios --release --no-codesign

# Archive
cd ios
xcodebuild -workspace Ballee.xcworkspace \
  -scheme Ballee \
  -configuration Release \
  -archivePath ../build/ios/archive/Ballee.xcarchive \
  -destination 'generic/platform=iOS' \
  CODE_SIGN_STYLE=Automatic \
  DEVELOPMENT_TEAM=A86CXY8H75 \
  archive

# Export IPA
xcodebuild -exportArchive \
  -archivePath ../build/ios/archive/Ballee.xcarchive \
  -exportOptionsPlist ExportOptions.plist \
  -exportPath ../build/ios/export \
  -allowProvisioningUpdates

# Upload to App Store Connect
xcrun altool --upload-app \
  --type ios \
  -f ../build/ios/export/Ballee.ipa \
  --apiKey LGU934Y2XR \
  --apiIssuer 69a6de96-5d75-47e3-e053-5b8c7c11a4d1
```

### Validate Before Upload

```bash
xcrun altool --validate-app \
  --type ios \
  -f build/ios/export/Ballee.ipa \
  --apiKey LGU934Y2XR \
  --apiIssuer 69a6de96-5d75-47e3-e053-5b8c7c11a4d1
```

### Using notarytool (for Mac apps)

```bash
# For macOS apps only
xcrun notarytool submit build/macos/Ballee.app.zip \
  --key ~/.appstoreconnect/private_keys/AuthKey_LGU934Y2XR.p8 \
  --key-id LGU934Y2XR \
  --issuer 69a6de96-5d75-47e3-e053-5b8c7c11a4d1 \
  --wait
```

---

## Troubleshooting

### Common Issues

#### 1. "Flutter not found" in Xcode Cloud

**Cause**: ci_post_clone.sh not executed or Flutter not in PATH.

**Fix**:
```bash
# Ensure script is executable
chmod +x ios/ci_scripts/ci_post_clone.sh

# Verify script location (must be ios/ci_scripts/)
ls -la ios/ci_scripts/
```

#### 2. "Code signing error: No certificate"

**Cause**: Distribution certificate not available.

**Fix**:
1. Open Xcode → Settings → Accounts
2. Select team → Manage Certificates
3. Create "Apple Distribution" certificate
4. Xcode Cloud will automatically use it

#### 3. "Provisioning profile doesn't include signing certificate"

**Cause**: Profile was generated before distribution certificate.

**Fix**:
```bash
# Use -allowProvisioningUpdates to regenerate
xcodebuild -exportArchive \
  -archivePath build.xcarchive \
  -exportOptionsPlist ExportOptions.plist \
  -exportPath export \
  -allowProvisioningUpdates
```

#### 4. "Pod install failed"

**Cause**: CocoaPods cache or version mismatch.

**Fix**:
```bash
# In ci_post_clone.sh
cd ios
rm -rf Pods Podfile.lock
pod install --repo-update
```

#### 5. "Build number already exists"

**Cause**: Uploading build with same version+build number.

**Fix**:
```bash
# Auto-increment in ci_post_clone.sh
NEW_BUILD_NUMBER=$(date +%Y%m%d%H%M)
/usr/libexec/PlistBuddy -c "Set :CFBundleVersion $NEW_BUILD_NUMBER" ios/Ballee/Info.plist
```

#### 6. "Embedded frameworks signed with different certificate"

**Cause**: Development-signed frameworks in release build.

**Fix**:
```bash
# Clean and rebuild
flutter clean
flutter build ios --release --no-codesign
cd ios && pod install --repo-update
# Then archive with correct signing
```

### Xcode Cloud Build Logs

1. Open Xcode → Xcode Cloud
2. Select failed build
3. Click "View Logs"
4. Check "ci_post_clone" step for script errors

### Testing ci_post_clone.sh Locally

```bash
# Simulate Xcode Cloud environment
export CI_PRIMARY_REPOSITORY_PATH="/Users/antoineschaller/GitHub/ballee"
export CI_BRANCH="main"
export CI_COMMIT="abc123"

# Run script
cd apps/mobile
./ios/ci_scripts/ci_post_clone.sh
```

---

## Best Practices

### 1. Version Strategy

```
Version: 1.2.3 (CFBundleShortVersionString)
Build:   2024010112 (CFBundleVersion) - auto-incremented by date/time
```

### 2. Branch Strategy

| Branch | Workflow | Distribution |
|--------|----------|--------------|
| `dev` | Build only | None |
| `main` | Archive | TestFlight Internal |
| `v*` tags | Archive | TestFlight External |
| `release/*` tags | Archive | App Store |

### 3. Caching Flutter SDK

To speed up builds, cache Flutter between runs:

```bash
# Check if Flutter exists from previous build
if [ -d "$HOME/.flutter_cache/flutter" ]; then
    export PATH="$PATH:$HOME/.flutter_cache/flutter/bin"
else
    git clone https://github.com/flutter/flutter.git "$HOME/.flutter_cache/flutter"
    export PATH="$PATH:$HOME/.flutter_cache/flutter/bin"
fi
```

### 4. Parallel Builds

Enable concurrent builds for faster feedback on multiple PRs.

### 5. Notifications

Configure Slack/email notifications for:
- Build failures
- Successful TestFlight uploads
- App Store review status changes

---

## Quick Reference

### Local Build Commands

```bash
# Full clean build
flutter clean && flutter pub get && flutter build ios --release

# Archive
xcodebuild -workspace ios/Ballee.xcworkspace -scheme Ballee -configuration Release archive

# Upload
xcrun altool --upload-app --type ios -f Ballee.ipa --apiKey KEY_ID --apiIssuer ISSUER_ID
```

### Xcode Cloud Script Hooks

| Script | When | Purpose |
|--------|------|---------|
| `ci_post_clone.sh` | After clone | Install dependencies |
| `ci_pre_xcodebuild.sh` | Before build | Pre-build setup |
| `ci_post_xcodebuild.sh` | After build | Post-build processing |

### API Key Setup

```bash
# Download from App Store Connect
# Keys > App Store Connect API > Generate API Key
# Save to ~/.appstoreconnect/private_keys/AuthKey_{KEY_ID}.p8
```

---

## App Store Connect API

The App Store Connect API allows programmatic management of Xcode Cloud workflows, builds, and products.

### API Configuration

| Setting | Value |
|---------|-------|
| Key ID | `LGU934Y2XR` |
| Issuer ID | `69a6de96-5d75-47e3-e053-5b8c7c11a4d1` |
| Key Path | `~/.appstoreconnect/private_keys/AuthKey_LGU934Y2XR.p8` |
| Base URL | `https://api.appstoreconnect.apple.com/v1` |

### Xcode Cloud CLI Tool

A Python CLI tool is available for managing Xcode Cloud:

```bash
# Location
apps/mobile/ios/scripts/xcode_cloud_cli.py

# Prerequisites
pip3 install pyjwt cryptography requests

# Make executable
chmod +x apps/mobile/ios/scripts/xcode_cloud_cli.py
```

### Available Commands

```bash
# List all products (apps) with Xcode Cloud enabled
./xcode_cloud_cli.py list-products

# List all workflows
./xcode_cloud_cli.py list-workflows

# Get workflow details
./xcode_cloud_cli.py workflow-info <workflow-id>

# Delete a workflow (with confirmation)
./xcode_cloud_cli.py delete-workflow <workflow-id>

# Delete without confirmation
./xcode_cloud_cli.py delete-workflow <workflow-id> --force

# Trigger a build
./xcode_cloud_cli.py trigger <workflow-id>

# Check build status
./xcode_cloud_cli.py build-status <build-id>
```

### API Endpoints Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ciProducts` | GET | List Xcode Cloud products |
| `/ciProducts/{id}/workflows` | GET | List workflows for a product |
| `/ciWorkflows/{id}` | GET | Get workflow details |
| `/ciWorkflows/{id}` | DELETE | Delete a workflow |
| `/ciBuildRuns` | POST | Trigger a new build |
| `/ciBuildRuns/{id}` | GET | Get build status |

### Example: Delete Unused Workflows

```bash
# 1. List all workflows
./xcode_cloud_cli.py list-workflows

# Output:
# ID                                       Name                    Active
# 81B37E9E-D5BD-482A-9252-761C0093FF9C     Ballee workflow         Yes
# 24FB36D3-8241-47EE-A819-9D1810C2927F     Development Build       No

# 2. Delete the unused workflow
./xcode_cloud_cli.py delete-workflow 24FB36D3-8241-47EE-A819-9D1810C2927F
```

### JWT Authentication

The API uses JWT (JSON Web Token) for authentication. The CLI handles this automatically, but for reference:

```python
import jwt
import time

payload = {
    'iss': ISSUER_ID,
    'iat': int(time.time()),
    'exp': int(time.time()) + 1200,  # 20 min expiry
    'aud': 'appstoreconnect-v1'
}

token = jwt.encode(
    payload,
    private_key,
    algorithm='ES256',
    headers={'kid': KEY_ID}
)
```

### Curl Examples

```bash
# Generate JWT (requires openssl)
JWT=$(python3 -c "
import jwt, time
with open('$HOME/.appstoreconnect/private_keys/AuthKey_LGU934Y2XR.p8') as f:
    key = f.read()
print(jwt.encode({
    'iss': '69a6de96-5d75-47e3-e053-5b8c7c11a4d1',
    'iat': int(time.time()),
    'exp': int(time.time()) + 1200,
    'aud': 'appstoreconnect-v1'
}, key, algorithm='ES256', headers={'kid': 'LGU934Y2XR'}))
")

# List workflows
curl -H "Authorization: Bearer $JWT" \
  "https://api.appstoreconnect.apple.com/v1/ciWorkflows"

# Delete a workflow
curl -X DELETE -H "Authorization: Bearer $JWT" \
  "https://api.appstoreconnect.apple.com/v1/ciWorkflows/{WORKFLOW_ID}"
```

---

## TestFlight Auto-Deploy Configuration

TestFlight deployment is configured in App Store Connect workflow settings (not via code).

### Enable Auto-Deploy to TestFlight

1. Open [App Store Connect](https://appstoreconnect.apple.com/apps/6756874215/ci/workflows)
2. Click on **Ballee workflow**
3. Go to **Post-Actions** section
4. Click **+** and select **TestFlight Internal Testing**
5. Configure:
   - **Groups**: Select "Internal Testers" (or create a new group)
   - **Notify Testers**: Enable if you want email notifications
6. Click **Save**

### TestFlight Groups Setup

If no groups exist:

1. Go to **TestFlight** tab in App Store Connect
2. Click **+** next to Internal Testing or External Testing
3. Create group (e.g., "Internal Testers", "Beta Testers")
4. Add testers by email

### Required Environment Variables

For the build to succeed with TestFlight, ensure these are set in Xcode Cloud:

| Variable | Description | Where to Set |
|----------|-------------|--------------|
| `SUPABASE_URL` | Supabase project URL | Workflow > Environment |
| `SUPABASE_ANON_KEY` | Supabase anonymous key | Workflow > Environment (Secret) |
| `SENTRY_DSN` | Sentry error tracking | Workflow > Environment (Secret) |
| `MIXPANEL_TOKEN` | Analytics token | Workflow > Environment (Secret) |

### Workflow Configuration for TestFlight

**Recommended settings** for "Ballee workflow":

```
Start Conditions:
  - Branch: main (or specific release branches)
  - Auto-cancel: Enabled (only latest commit builds)

Environment:
  - Xcode: Latest Release
  - macOS: Latest Release
  - Environment Variables: (as above)

Archive:
  - Scheme: Ballee
  - Platform: iOS
  - Configuration: Release

Post-Actions:
  - TestFlight Internal Testing
    - Group: Internal Testers
    - Notify: Yes
```

### Verify TestFlight Upload

After a successful build:

1. Check **Xcode Cloud** tab for build status
2. Go to **TestFlight** tab
3. New build should appear under "iOS Builds"
4. Testers will receive notification (if enabled)

---

### Troubleshooting API Issues

#### 1. "FORBIDDEN_ERROR" on list builds

The `/ciBuildRuns` endpoint doesn't support `GET_COLLECTION`. Get builds per workflow instead:
```bash
./xcode_cloud_cli.py workflow-info <workflow-id>
```

#### 2. "No API key found"

Ensure the .p8 file exists:
```bash
ls ~/.appstoreconnect/private_keys/AuthKey_LGU934Y2XR.p8
```

Or set the environment variable:
```bash
export APP_STORE_CONNECT_API_KEY_CONTENT=$(base64 < ~/.appstoreconnect/private_keys/AuthKey_LGU934Y2XR.p8)
```

#### 3. Multiple products with same name

The API may show multiple products (e.g., `ballee` and `Ballee`). Use `list-products` to identify the correct one and check workflows for each.
