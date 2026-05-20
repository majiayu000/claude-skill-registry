---
name: ios-release
description: Build, archive, and prepare iOS app for TestFlight/App Store. Handles version bumping, build number configuration, Xcode archiving, and upload. Use when preparing a new iOS release for TestFlight beta testing or App Store submission.
---

# iOS Release

Build and prepare iOS app for TestFlight/App Store.

## Critical Warning

**NEVER use `yarn tauri ios dev` or `yarn tauri ios dev --open` for archiving!**
- `dev` creates a DEBUG build pointing to `localhost:1420` (Vite dev server)
- Installing from TestFlight will show blank screen (no dev server on device)
- Always use `yarn tauri ios build` (release mode by default)

## 1. Gather Info

Ask user for:
- Version number (x.x.x) - or keep current if re-uploading
- If re-uploading same version: need to bump build number only

## 2. Update Version/Build Number

**New version release:**
Use `/bump-version` workflow to update all config files.

**Re-uploading same version (e.g., fixing previous bad build):**
Only bump the build number in `tauri.conf.json`:

```json
{
  "bundle": {
    "iOS": {
      "bundleVersion": "2"
    }
  }
}
```

Note: Do NOT edit files in `gen/apple/` directly - they get regenerated. Use tauri.conf.json.

## 3. Setup Share Extension (Conditional)

**Only required after running `yarn tauri ios init`** (regenerates apple folder).

Skip if Share Extension is already configured. To check:
```bash
ls decentpaste-app/src-tauri/gen/apple/ShareExtension/
```

If missing, run:
```bash
cd decentpaste-app && ./tauri-plugin-decentshare/scripts/setup-ios-share-extension.sh
```

## 4. Fix Share Extension Version Mismatch

After version bumps, the Share Extension's `MARKETING_VERSION` in the Xcode project may be out of sync with the main app. Check for this warning during build:

```
warning: The CFBundleShortVersionString of an app extension ('X.X.X') must match that of its containing parent app ('Y.Y.Y').
```

**To fix**, update the Share Extension's version in the Xcode project file:

```bash
# Replace OLD_VERSION with the outdated version, NEW_VERSION with current app version
sed -i '' 's/MARKETING_VERSION = OLD_VERSION;/MARKETING_VERSION = NEW_VERSION;/g' \
  decentpaste-app/src-tauri/gen/apple/decentpaste-app.xcodeproj/project.pbxproj
```

Example: `sed -i '' 's/MARKETING_VERSION = 0.4.2;/MARKETING_VERSION = 0.5.0;/g' ...`

**Why this happens**: The `/bump-version` workflow updates `tauri.conf.json`, but the Share Extension's version lives in `gen/apple/` which doesn't get auto-updated.

## 5. Build & Open Xcode

Ask user to run this in a **separate terminal** (long-running):

```bash
cd decentpaste-app && yarn tauri ios build --open
```

This command:
1. Builds the **frontend in production mode** (bundles assets)
2. Opens Xcode project when frontend build completes

**IMPORTANT**: Wait for `yarn tauri ios build` to complete before archiving in Xcode. The build compiles the frontend assets that get bundled into the iOS app. If you archive before it finishes, you may get an incomplete or broken build.

The actual iOS compilation and archiving happens in Xcode (next step).

## 6. Archive & Upload in Xcode

User performs in Xcode:
1. Select scheme: `decentpaste-app_iOS`
2. Select destination: `Any iOS Device (arm64)`
3. Menu: **Product → Archive** (or ⇧⌘A)
4. Wait for archive (~5-15 min)
5. In Organizer: **Distribute App → App Store Connect → Upload**
6. Check "Upload your app's symbols"
7. Use automatic signing
8. Click **Upload**

### Alternative: Full CLI with IPA

Build everything via CLI (no Xcode GUI needed):
```bash
cd decentpaste-app && yarn tauri ios build --export-method app-store-connect
```

IPA location: `src-tauri/gen/apple/build/arm64/DecentPaste.ipa`

Upload via Transporter app (free from Mac App Store) or `xcrun altool` with API keys.

## 7. Verify Production Build

To confirm the archive is a production build (not dev):

```bash
# Check for Vite-hashed asset filenames in binary (production indicator)
ARCHIVE=$(ls -td ~/Library/Developer/Xcode/Archives/**/*.xcarchive 2>/dev/null | head -1)
strings "$ARCHIVE/Products/Applications/DecentPaste.app/DecentPaste" | grep -E "/assets/index-[A-Za-z0-9]+\.(js|css)"
```

**Production build**: Shows hashed filenames like `/assets/index-BauF9ln8.css`
**Dev build**: No hashed assets (would only show `localhost:1420`)

Note: `localhost:1420` appearing in strings is normal (embedded config) - check for hashed assets.

## 8. TestFlight Configuration

After upload completes (~5-15 min processing):

1. Go to [App Store Connect](https://appstoreconnect.apple.com/) → TestFlight
2. Select the new build
3. Fill **Test Information** (what to test)
4. Answer **Export Compliance** (DecentPaste uses encryption → Yes, but exempt)
5. For external testers: Wait for Beta App Review (~24-48h)

## 9. Report

Report: version updated, build number, build verified as production, upload status.

## Key Files

| File                | Value                                        |
|---------------------|----------------------------------------------|
| Bundle ID           | `com.decentpaste.application`                |
| Extension Bundle ID | `com.decentpaste.application.ShareExtension` |
| App Group           | `group.com.decentpaste.application`          |
| Team ID             | `SNDGGHFSJ2`                                 |

## Troubleshooting

| Issue                            | Solution                                                              |
|----------------------------------|-----------------------------------------------------------------------|
| `--release` flag error           | Don't use it - `tauri ios build` is release by default                |
| Blank screen on device           | You archived a dev build - rebuild with `yarn tauri ios build --open` |
| Code signing errors              | In Xcode, verify Team selected for BOTH targets                       |
| Share Extension missing          | Run `setup-ios-share-extension.sh`                                    |
| Share Extension version mismatch | See step 4 - update MARKETING_VERSION in project.pbxproj              |
| "Build number already used"      | Bump `bundle.iOS.bundleVersion` in tauri.conf.json                    |
| Upload fails                     | Check Xcode → Settings → Accounts for valid credentials               |
