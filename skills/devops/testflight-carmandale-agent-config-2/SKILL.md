---
name: testflight
description: Build and upload visionOS/iOS/macOS apps to TestFlight via App Store Connect API. Handles archive, export, and upload workflow with rsync bug workaround. Use when deploying to TestFlight or App Store Connect.
---

# TestFlight Upload Skill

Build, export, and upload visionOS/iOS/macOS apps to TestFlight using App Store Connect API.

## Quick Start

```bash
# Full build + upload for internal testing (default)
~/.pi/agent/skills/testflight/upload.sh <project_name> <scheme_name>

# Full build + upload for App Store submission
~/.pi/agent/skills/testflight/upload.sh <project_name> <scheme_name> --appstore

# Upload existing IPA only (skip archive/export)
~/.pi/agent/skills/testflight/upload.sh --upload-only <scheme_name>
```

### Examples

```bash
# Internal testing only (default) - works in TestFlight, NOT selectable for App Store
~/.pi/agent/skills/testflight/upload.sh PfizerOutdoCancer PfizerOutdoCancer

# App Store distribution - works in TestFlight AND selectable for App Store submission
~/.pi/agent/skills/testflight/upload.sh PfizerOutdoCancer PfizerOutdoCancer --appstore

# Upload only - if IPA/PKG already exists at ~/Desktop/<scheme>_Export/
~/.pi/agent/skills/testflight/upload.sh --upload-only PfizerOutdoCancer

# macOS app (Media Server) - run from repo root, not subdirectory!
cd /path/to/groovetech-media-server
~/.pi/agent/skills/testflight/upload.sh GrooveTechMediaServer "GrooveTech Media Server" --appstore macos
```

Credentials are auto-loaded from `~/.config/testflight/credentials.env`.

## Distribution Modes

| Mode | Flag | TestFlight | App Store Submission |
|------|------|------------|---------------------|
| Internal Only | (default) | ✅ Works | ❌ NOT selectable |
| App Store | `--appstore` | ✅ Works | ✅ Selectable |

**Use Internal Only (default)** for regular testing - faster iteration, no review needed.

**Use `--appstore`** when you're ready to submit to the App Store - build will be selectable in the "Build" section of your App Store version.

## ⚠️ Timeout Warning for Large Apps

**Upload of large IPAs (1GB+) takes 15-30 minutes.** This exceeds typical agent command timeouts.

**Recommended workflow for large apps:**

1. Run full script via agent (archive + export will complete):
   ```bash
   ~/.pi/agent/skills/testflight/upload.sh PfizerOutdoCancer PfizerOutdoCancer
   ```
   (Let it timeout on upload step - IPA is already created)

2. Complete upload manually in terminal:
   ```bash
   ~/.pi/agent/skills/testflight/upload.sh --upload-only PfizerOutdoCancer
   ```

The `--upload-only` flag skips rebuild and directly uploads the existing IPA from `~/Desktop/<scheme>_Export/`.

## Important: The Correct Upload Workflow

**DO NOT upload archives directly.** The workflow is:

1. **Archive** → Build `.xcarchive`
2. **Export** → Convert to `.ipa` with App Store signing
3. **Upload** → Send `.ipa` to App Store Connect

The export step is critical because:
- Re-signs the app for App Store distribution
- Creates proper IPA structure with Payload directory
- Works around macOS rsync bug (set `uploadSymbols=false`)

## Credentials

**Location:** `~/.config/testflight/credentials.env`

```bash
TESTFLIGHT_API_KEY_ID="KPQ86W6JWV"
TESTFLIGHT_ISSUER_ID="69a6de8c-f4be-47e3-e053-5b8c7c11a4d1"
TESTFLIGHT_TEAM_ID="UTK59YE75G"
```

**API Key files:** `~/.appstoreconnect/private_keys/AuthKey_<KEY_ID>.p8`

## The Three Steps (Manual)

### Step 1: Build Archive

```bash
xcodebuild -project YourApp.xcodeproj \
  -scheme YourApp \
  archive \
  -archivePath ~/Desktop/YourApp.xcarchive \
  -destination 'generic/platform=visionOS'
```

**Success:** `** ARCHIVE SUCCEEDED **`

### Step 2: Export to IPA

Create `ExportOptions.plist` (**uploadSymbols must be false** for rsync bug):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>compileBitcode</key>
    <false/>
    <key>destination</key>
    <string>export</string>
    <key>method</key>
    <string>app-store</string>
    <key>signingStyle</key>
    <string>automatic</string>
    <key>stripSwiftSymbols</key>
    <true/>
    <key>teamID</key>
    <string>UTK59YE75G</string>
    <key>testFlightInternalTestingOnly</key>
    <true/>
    <key>uploadSymbols</key>
    <false/>
</dict>
</plist>
```

> **Note:** Set `testFlightInternalTestingOnly` to `true` for internal testing only (build won't be selectable for App Store). Remove this key or set to `false` for App Store submission builds.

```bash
xcodebuild -exportArchive \
  -archivePath ~/Desktop/YourApp.xcarchive \
  -exportOptionsPlist ~/Desktop/ExportOptions.plist \
  -exportPath ~/Desktop/YourApp_Export \
  -allowProvisioningUpdates
```

**Success:** `** EXPORT SUCCEEDED **`

### Step 3: Upload IPA

```bash
xcrun altool --upload-package ~/Desktop/YourApp_Export/YourApp.ipa \
  --type visionos \
  --apiKey KPQ86W6JWV \
  --apiIssuer 69a6de8c-f4be-47e3-e053-5b8c7c11a4d1
```

**Success:** `No errors uploading`

## Common Errors

### "IPA is invalid. It does not include a Payload directory"

**Cause:** Tried to upload `.xcarchive` instead of exported `.ipa`

**Fix:** Run the export step first. Never upload archives directly.

### rsync Error During Export

```
error: exportArchive Copy failed
rsync: --extended-attributes: unknown option
```

**Cause:** macOS ships with ancient rsync (2006)

**Fix:** Set `uploadSymbols` to `false` in ExportOptions.plist

### CFBundleVersion Mismatch

**Cause:** Extension build number doesn't match main app

**Fix:** Update extension build number in Xcode to match main app

### API Key Not Found

**Fix:** Copy `.p8` file to `~/.appstoreconnect/private_keys/AuthKey_<KEY_ID>.p8`

### RPBroadcastProcessMode Not Specified (Broadcast Extension)

```
Invalid Info.plist value. The value for the key 'RPBroadcastProcessMode' 
in bundle YourApp.app/PlugIns/Extension.appex is invalid.
The key was not specified.
```

**Cause:** `RPBroadcastProcessMode` is in wrong location in extension Info.plist

**Fix:** The key MUST be a direct child of `NSExtension` dict (not at top level, not inside `NSExtensionAttributes`):

```xml
<key>NSExtension</key>
<dict>
    <key>NSExtensionPointIdentifier</key>
    <string>com.apple.broadcast-services-upload</string>
    <key>NSExtensionPrincipalClass</key>
    <string>$(PRODUCT_MODULE_NAME).SampleHandler</string>
    <key>RPBroadcastProcessMode</key>
    <string>RPBroadcastProcessModeSampleBuffer</string>
</dict>
```

### Invalid Bundle Type (screen-capture entitlement)

```
Invalid bundle type. The com.apple.developer.screen-capture.include-passthrough 
entitlement is not valid for bundles of type XPC!.
```

**Cause:** `com.apple.developer.screen-capture.include-passthrough` is in the main app

**Fix:** Remove from main app `.entitlements`. This entitlement is ONLY valid in broadcast extensions.

### Missing NSEnterpriseMCAMUsageDescription

**Cause:** App uses enterprise camera APIs without privacy description

**Fix:** Add to main app Info.plist:
```xml
<key>NSEnterpriseMCAMUsageDescription</key>
<string>This app uses main camera access for enterprise features.</string>
```

### Missing BGTaskSchedulerPermittedIdentifiers

**Cause:** App has `processing` background mode but no task identifiers

**Fix:** Add to main app Info.plist:
```xml
<key>BGTaskSchedulerPermittedIdentifiers</key>
<array>
    <string>com.yourcompany.app.background-refresh</string>
</array>
```

## Platform Types

| Platform | `--type` value | Destination | Package |
|----------|----------------|-------------|---------|
| visionOS | `visionos` | `generic/platform=visionOS` | `.ipa` |
| iOS | `ios` | `generic/platform=iOS` | `.ipa` |
| macOS | `macos` | `platform=macOS` | `.pkg` |

## macOS Apps (Media Server)

Media Server has a special setup - it uses a **workspace** at the repo root, not a project file in a subdirectory.

### Why It's Different

- Uses `GrooveTechMediaServer.xcworkspace` (not `.xcodeproj`)
- Workspace lives at repo root (not in a subdirectory)
- Needs local `build/DerivedData` for proper SPM package resolution
- Exports `.pkg` instead of `.ipa`

### How to Upload Media Server

```bash
# 1. Navigate to repo ROOT (not the subdirectory!)
cd "/path/to/groovetech-media-server"

# 2. Run upload with workspace name, scheme, and macos platform
~/.pi/agent/skills/testflight/upload.sh GrooveTechMediaServer "GrooveTech Media Server" --appstore macos
```

**Common mistake:** Running from `groovetech-media-server/GrooveTech Media Server/` subdirectory - this will fail because the workspace is at the parent level.

### What the Script Does for macOS

1. Detects workspace and uses `-workspace` flag
2. Uses `platform=macOS` destination (not `generic/platform=macOS`)
3. Sets `-derivedDataPath ./build/DerivedData` for correct SPM resolution
4. Looks for `.pkg` output instead of `.ipa`

## Post-Upload

1. Wait 10-15 minutes for Apple processing
2. Check: https://appstoreconnect.apple.com/apps
3. Go to your app → TestFlight tab
4. Add testers (internal = immediate, external = beta review required)

---

## Enterprise Delivery (for IT re-signing)

When a client needs to re-sign the app with their enterprise certificate (e.g., for internal app stores/MDM), provide the `.xcarchive` with a README.

### Create Delivery Package

```bash
~/.pi/agent/skills/testflight/create-delivery.sh \
  ~/Desktop/MyApp.xcarchive \
  "App Name" \
  "1.0" \
  "42" \
  "com.company.bundleid" \
  "visionOS (Apple Vision Pro)" \
  "Description of the app"
```

This creates: `~/Desktop/App_Name_Delivery_v1.0_Build42/`
- `MyApp.xcarchive`
- `README.md` (re-signing instructions)

### GrooveTech Apps Reference

| App | Bundle ID | Platform | Project | Scheme |
|-----|-----------|----------|---------|--------|
| Outdo Cancer | `com.groovejones.PfizerOutdoCancer` | visionOS | PfizerOutdoCancerV2.xcodeproj | PfizerOutdoCancer |
| GMP | `com.groovetech.media-player` | visionOS | groovetech-media-player.xcodeproj | groovetech-media-player |
| Media Server | `com.groovetech.media-server` | macOS | GrooveTechMediaServer.xcworkspace | GrooveTech Media Server |
| Orchestrator | `com.groovejones.orchestrator` | iOS | orchestrator.xcodeproj | orchestrator |

### ⚠️ CRITICAL: Build Number Workflow

**ALWAYS check ASC build numbers BEFORE incrementing local builds!**

Local project files can get out of sync with App Store Connect. Using stale local build numbers will cause duplicate build failures or confusion.

#### Step 1: Query Current ASC Build Numbers

```bash
# Query all 4 apps at once
node ~/.pi/agent/skills/testflight/query-builds.js
```

Output shows latest builds on App Store Connect:
```
=== Pfizer (6737364780) ===
  Build 80 - 2026-02-03 - VALID
=== GMP (6757438008) ===
  Build 97 - 2026-02-03 - VALID
...
```

#### Step 2: Increment to ASC_LATEST + 1

For each app, set `CURRENT_PROJECT_VERSION` to **ASC latest + 1**:

```bash
# Example: If ASC shows build 97, set local to 98
sed -i '' "s/CURRENT_PROJECT_VERSION = [0-9]*;/CURRENT_PROJECT_VERSION = 98;/g" "path/to/project.pbxproj"
```

#### Step 3: Commit Build Number Changes

```bash
git add -A && git commit -m "chore: Bump build numbers for TestFlight"
git push
```

#### Step 4: Run Upload

```bash
~/.pi/agent/skills/testflight/upload.sh <project> <scheme> --appstore [platform]
```

### App IDs Reference

| App | App Store Connect ID |
|-----|---------------------|
| Pfizer | 6737364780 |
| GMP | 6757438008 |
| Orchestrator | 6754814714 |
| Media Server | 6757471795 |

## Session History (for agents)

**To find the original sessions where this workflow was developed and tested:**

```bash
# Search for TestFlight upload sessions
cass search "upload-to-testflight-complete" --robot --limit 10 --days 365

# Key sessions:
# - Claude debug file with failed archive upload + successful IPA workflow:
#   ~/.claude/debug/a8d1679e-6d2f-4e2c-b4a9-7379c4181945.txt
#
# - Git commit that added the scripts (Oct 22, 2025):
#   git show e4cccf46 --stat
#
# - Git commit that updated guide after successful upload (Oct 31, 2025):
#   git show d4f0674c
```

**Key learnings from sessions:**
1. Direct archive upload (`--upload-app`) FAILS with "IPA is invalid. It does not include a Payload directory"
2. Must export to IPA first with `uploadSymbols=false` (rsync bug workaround)
3. Then upload IPA with `--upload-package`
4. Successful upload: Version 1.2 (67) on Oct 31, 2025 at 4:45 PM
