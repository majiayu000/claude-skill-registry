---
name: swift-build
description: Build, archive, code signing, and App Store distribution for iOS/macOS apps. Use when configuring build settings, signing, TestFlight, notarization, or CI/CD pipelines.
user-invocable: false
---

# Swift Build & Distribution

## Code Signing (Automatic - Recommended)

```bash
# Xcode: Target → General → "Automatically manage signing" ✓
# Select Development Team

# Command line
xcodebuild archive \
  -scheme MyApp \
  -archivePath ./build/MyApp.xcarchive \
  -allowProvisioningUpdates \
  DEVELOPMENT_TEAM="XXXXXXXXXX"
```

## Archive & Export

```bash
# Archive
xcodebuild archive \
  -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -configuration Release \
  -archivePath ./build/MyApp.xcarchive

# Export IPA
xcodebuild -exportArchive \
  -archivePath ./build/MyApp.xcarchive \
  -exportPath ./build \
  -exportOptionsPlist ExportOptions.plist
```

**ExportOptions.plist:**
```xml
<dict>
    <key>method</key>
    <string>app-store</string>
    <key>teamID</key>
    <string>XXXXXXXXXX</string>
</dict>
```

## Privacy Manifest (REQUIRED)

**PrivacyInfo.xcprivacy:**
```xml
<dict>
    <key>NSPrivacyAccessedAPITypes</key>
    <array>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array><string>CA92.1</string></array>
        </dict>
    </array>
</dict>
```

## macOS Notarization

```bash
# Store credentials
xcrun notarytool store-credentials "notary-profile" \
  --apple-id "dev@company.com" \
  --team-id "XXXXXXXXXX"

# Submit
xcrun notarytool submit ./MyApp.dmg \
  --keychain-profile "notary-profile" --wait

# Staple ticket
xcrun stapler staple ./MyApp.dmg
```

## Build Configurations

**Release.xcconfig:**
```ini
GCC_OPTIMIZATION_LEVEL = s
SWIFT_OPTIMIZATION_LEVEL = -O
SWIFT_COMPILATION_MODE = wholemodule
DEBUG_INFORMATION_FORMAT = dwarf-with-dsym
```

## fastlane Beta Deploy

```ruby
lane :beta do
  match(type: "appstore", readonly: true)
  increment_build_number
  build_app(scheme: "MyApp", export_method: "app-store")
  upload_to_testflight(groups: ["Beta Testers"])
end
```

## Common Info.plist Keys

```xml
<!-- Export compliance (no encryption) -->
<key>ITSAppUsesNonExemptEncryption</key>
<false/>

<!-- Required device capabilities -->
<key>UIRequiredDeviceCapabilities</key>
<array><string>arm64</string></array>
```

## Troubleshooting

```bash
# Check certificates
security find-identity -v -p codesigning

# Check provisioning profiles
ls ~/Library/MobileDevice/Provisioning\ Profiles/

# Verify code signing
codesign -dvvv MyApp.app
```

## Pre-Release Checklist

- [ ] Version & build number incremented
- [ ] PrivacyInfo.xcprivacy complete
- [ ] App Icon all variants (light/dark/tinted)
- [ ] Release configuration selected
- [ ] Archive validates in Organizer
- [ ] TestFlight beta tested
