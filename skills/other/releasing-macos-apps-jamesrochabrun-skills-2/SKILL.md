---
name: releasing-macos-apps
description: Create notarized macOS app releases with Sparkle auto-updates, DMG installers, and GitHub releases. Use when releasing macOS apps, creating DMG files, notarizing apps, or setting up Sparkle updates. Handles version updates, code signing, notarization, and distribution.
---

# Releasing macOS Apps

Complete workflow for creating notarized macOS app releases with Sparkle auto-updates, DMG installers, and GitHub releases.

## Release Checklist

Copy this checklist and track progress:

```
Release Progress:
- [ ] Step 1: Check prerequisites (certificates, credentials)
- [ ] Step 2: Update version in .xcconfig file
- [ ] Step 3: Build and archive the app
- [ ] Step 4: Export with proper code signing
- [ ] Step 5: Create zip and generate Sparkle signature
- [ ] Step 6: Create DMG with Applications folder
- [ ] Step 7: Submit for notarization
- [ ] Step 8: Staple notarization ticket to DMG
- [ ] Step 9: Update appcast.xml with new signature
- [ ] Step 10: Commit and push changes
- [ ] Step 11: Update GitHub release assets
- [ ] Step 12: Verify DMG and version number
```

## Prerequisites

Before starting a release, verify:

1. **Apple Developer ID Application certificate** installed and valid
2. **Apple ID credentials** for notarization:
   - Apple ID email
   - App-specific password (generate at appleid.apple.com)
   - Team ID
3. **Sparkle private key** for signing updates
4. **GitHub CLI** (`gh`) installed and authenticated
5. **Version configuration location** identified (usually `.xcconfig` file)

Check certificate:
```bash
security find-identity -v -p codesigning | grep "Developer ID Application"
```

## Step 1: Update Version

Locate your version configuration file (commonly `ProjectName.xcconfig` or `project.pbxproj`).

**For .xcconfig files:**
```bash
# Edit the APP_VERSION line
# Example: APP_VERSION = 1.0.9
```

**Verify the update:**
```bash
xcodebuild -project PROJECT.xcodeproj -showBuildSettings | grep MARKETING_VERSION
```

## Step 2: Build and Archive

Archive the app with the new version:

```bash
xcodebuild -project PROJECT.xcodeproj \
  -scheme SCHEME_NAME \
  -configuration Release \
  -archivePath ~/Desktop/APP-VERSION.xcarchive \
  archive
```

**Verify archive was created:**
```bash
ls -la ~/Desktop/APP-VERSION.xcarchive
```

## Step 3: Export with Code Signing

Create export options file:

```bash
cat > /tmp/ExportOptions.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>destination</key>
	<string>export</string>
	<key>method</key>
	<string>developer-id</string>
	<key>signingStyle</key>
	<string>automatic</string>
	<key>teamID</key>
	<string>YOUR_TEAM_ID</string>
	<key>signingCertificate</key>
	<string>Developer ID Application</string>
</dict>
</plist>
EOF
```

Replace `YOUR_TEAM_ID` with your actual team ID.

Export the archive:

```bash
xcodebuild -exportArchive \
  -archivePath ~/Desktop/APP-VERSION.xcarchive \
  -exportPath ~/Desktop/APP-VERSION-Export \
  -exportOptionsPlist /tmp/ExportOptions.plist
```

**Verify the exported app version:**
```bash
defaults read ~/Desktop/APP-VERSION-Export/APP.app/Contents/Info.plist CFBundleShortVersionString
```

This should show the new version number.

**Verify code signing:**
```bash
codesign -dvvv ~/Desktop/APP-VERSION-Export/APP.app
```

Look for "Developer ID Application" in the Authority lines.

## Step 4: Create Zip and Generate Sparkle Signature

Create zip file for Sparkle auto-updates:

```bash
cd ~/Desktop/APP-VERSION-Export
ditto -c -k --keepParent APP.app APP.app.zip
```

Generate Sparkle EdDSA signature (you'll be prompted for the private key):

```bash
echo "YOUR_SPARKLE_PRIVATE_KEY" | \
  ~/Library/Developer/Xcode/DerivedData/PROJECT-HASH/SourcePackages/artifacts/sparkle/Sparkle/bin/sign_update \
  APP.app.zip --ed-key-file -
```

**Output format:**
```
sparkle:edSignature="BASE64_SIGNATURE" length="FILE_SIZE"
```

Save both the signature and length for updating appcast.xml.

For more details, see [SPARKLE.md](SPARKLE.md).

## Step 5: Create DMG with Applications Folder

Create DMG installer with Applications folder symlink for drag-and-drop installation:

```bash
TEMP_DMG_DIR="/tmp/APP_dmg" && \
rm -rf "${TEMP_DMG_DIR}" && \
mkdir -p "${TEMP_DMG_DIR}" && \
cp -R ~/Desktop/APP-VERSION-Export/APP.app "${TEMP_DMG_DIR}/" && \
ln -s /Applications "${TEMP_DMG_DIR}/Applications" && \
hdiutil create -volname "APP VERSION" \
  -srcfolder "${TEMP_DMG_DIR}" \
  -ov -format UDZO ~/Desktop/APP-VERSION.dmg && \
rm -rf "${TEMP_DMG_DIR}"
```

**Verify DMG contents:**
```bash
hdiutil attach ~/Desktop/APP-VERSION.dmg -readonly -nobrowse -mountpoint /tmp/verify_dmg && \
ls -la /tmp/verify_dmg && \
hdiutil detach /tmp/verify_dmg
```

You should see both `APP.app` and `Applications` (symlink).

## Step 6: Submit for Notarization

Submit the DMG to Apple for notarization (you'll be prompted for credentials):

```bash
xcrun notarytool submit ~/Desktop/APP-VERSION.dmg \
  --apple-id YOUR_APPLE_ID@gmail.com \
  --team-id YOUR_TEAM_ID \
  --password YOUR_APP_SPECIFIC_PASSWORD \
  --wait
```

The `--wait` flag makes the command wait for processing to complete (typically 1-2 minutes).

**Expected output:**
```
Processing complete
  id: [submission-id]
  status: Accepted
```

If status is "Invalid", get detailed logs:
```bash
xcrun notarytool log SUBMISSION_ID \
  --apple-id YOUR_APPLE_ID@gmail.com \
  --team-id YOUR_TEAM_ID \
  --password YOUR_APP_SPECIFIC_PASSWORD
```

For notarization troubleshooting, see [NOTARIZATION.md](NOTARIZATION.md).

## Step 7: Staple Notarization Ticket

Staple the notarization ticket to the DMG:

```bash
xcrun stapler staple ~/Desktop/APP-VERSION.dmg
```

**Expected output:**
```
The staple and validate action worked!
```

**Verify notarization:**
```bash
spctl -a -vvv ~/Desktop/APP-VERSION-Export/APP.app
```

Should show:
```
accepted
source=Notarized Developer ID
```

## Step 8: Update appcast.xml

Update the Sparkle appcast file with the new version, signature, and file size from Step 4:

```xml
<item>
  <title>Version X.X.X</title>
  <link>https://github.com/USER/REPO</link>
  <sparkle:version>X.X.X</sparkle:version>
  <sparkle:channel>stable</sparkle:channel>
  <description><![CDATA[
    Release version X.X.X
  ]]></description>
  <pubDate>DAY, DD MMM YYYY HH:MM:SS -0700</pubDate>
  <enclosure
    url="https://github.com/USER/REPO/releases/download/vX.X.X/APP.app.zip"
    sparkle:version="X.X.X"
    sparkle:edSignature="SIGNATURE_FROM_STEP_4"
    length="FILE_SIZE_FROM_STEP_4"
    type="application/octet-stream" />
</item>
```

**Note:** The gitleaks pre-commit hook may flag the Sparkle signature as a potential secret. This is a false positive - the EdDSA signature is public and safe to commit. Use `git commit --no-verify` if needed.

## Step 9: Commit and Push Changes

Commit the version update and appcast changes:

```bash
git add PROJECT.xcconfig appcast.xml
git commit --no-verify -m "Bump version to X.X.X

Update appcast.xml with new version, Sparkle signature, and file size.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

git push
```

## Step 10: Update GitHub Release

Create or update the GitHub release with new assets:

**For new releases:**
```bash
gh release create vX.X.X \
  --title "APP vX.X.X" \
  --notes "Release version X.X.X" \
  ~/Desktop/APP-VERSION.dmg \
  ~/Desktop/APP-VERSION-Export/APP.app.zip
```

**For updating existing releases:**
```bash
# Upload new assets (overwrites existing with --clobber)
gh release upload vX.X.X \
  ~/Desktop/APP-VERSION.dmg \
  ~/Desktop/APP-VERSION-Export/APP.app.zip \
  --clobber
```

**Note on asset naming:**
The uploaded filename becomes the asset name. To upload with a specific name:
```bash
# Copy to desired name first
cp ~/Desktop/APP-1.0.9.dmg /tmp/APP.dmg
gh release upload vX.X.X /tmp/APP.dmg
```

**Verify release assets:**
```bash
gh release view vX.X.X --json assets -q '.assets[] | "\(.name) - \(.size) bytes"'
```

## Step 11: Final Verification

Verify the release is working correctly:

**Check version in app:**
```bash
defaults read /Applications/APP.app/Contents/Info.plist CFBundleShortVersionString
```

Should show: `X.X.X`

**Test DMG:**
1. Download the DMG from GitHub release
2. Open the DMG
3. Verify Applications folder is present for drag-and-drop
4. Drag app to Applications and launch
5. Should open without any "malicious" or security warnings

**Test Sparkle updates:**
- Users with previous versions should receive automatic update notifications
- The update should download and install smoothly

## Common Issues

If you encounter problems, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions to:

- Version not updating after rebuild
- DMG missing Applications folder
- Notarization failures
- "Malicious app" warnings
- Sparkle signature issues
- CI/CD failures

## Quick Reference

**Check version:**
```bash
defaults read /path/to/APP.app/Contents/Info.plist CFBundleShortVersionString
```

**Check code signing:**
```bash
codesign -dvvv /path/to/APP.app
```

**Check notarization:**
```bash
spctl -a -vvv /path/to/APP.app
```

**Get Sparkle sign_update path:**
```bash
find ~/Library/Developer/Xcode/DerivedData -name sign_update -type f
```
