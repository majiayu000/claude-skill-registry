---
name: cocoapods-privacy-manifests
description: Use when implementing iOS 17+ privacy manifests for CocoaPods libraries. Covers PrivacyInfo.xcprivacy file creation, required reasons API declarations, and proper resource bundle integration for App Store compliance.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# CocoaPods - Privacy Manifests

Implement iOS 17+ privacy manifests for App Store compliance and user transparency.

## What Are Privacy Manifests?

Privacy manifests (`PrivacyInfo.xcprivacy`) are XML property list files that declare:

- Data collection and usage practices
- Required Reasons API usage
- Tracking domains
- Privacy-sensitive APIs

### Why Privacy Manifests?

Starting with iOS 17 and Xcode 15, Apple requires privacy manifests for:

- Apps using privacy-sensitive APIs
- Third-party SDKs and frameworks
- Any code accessing user data

## Privacy Manifest File Format

### Basic Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSPrivacyTracking</key>
    <false/>
    <key>NSPrivacyTrackingDomains</key>
    <array/>
    <key>NSPrivacyCollectedDataTypes</key>
    <array/>
    <key>NSPrivacyAccessedAPITypes</key>
    <array/>
</dict>
</plist>
```

## Including in Podspec

### Resource Bundle (Recommended)

```ruby
Pod::Spec.new do |spec|
  spec.name = 'MyLibrary'
  spec.version = '1.0.0'

  spec.source_files = 'Source/**/*.swift'

  # Include privacy manifest in resource bundle
  spec.resource_bundles = {
    'MyLibrary' => [
      'Resources/**/*.xcprivacy',
      'Resources/**/*.{png,jpg,xcassets}'
    ]
  }
end
```

### Direct Resources (Alternative)

```ruby
spec.resources = 'Resources/PrivacyInfo.xcprivacy'

# Or with glob pattern
spec.resources = 'Resources/**/*.xcprivacy'
```

### File Location

```
MyLibrary/
├── MyLibrary.podspec
├── Source/
│   └── MyLibrary/
└── Resources/
    ├── PrivacyInfo.xcprivacy  # Privacy manifest
    └── Assets.xcassets
```

## Required Reasons APIs

### Common APIs Requiring Reasons

Apple requires declarations for these privacy-sensitive APIs:

#### File Timestamp APIs

```xml
<key>NSPrivacyAccessedAPITypes</key>
<array>
    <dict>
        <key>NSPrivacyAccessedAPIType</key>
        <string>NSPrivacyAccessedAPICategoryFileTimestamp</string>
        <key>NSPrivacyAccessedAPITypeReasons</key>
        <array>
            <string>C617.1</string>
        </array>
    </dict>
</array>
```

**Reason Codes:**

- `C617.1`: Display timestamps to user
- `0A2A.1`: Access timestamps of files in app container
- `3B52.1`: Access timestamps for app functionality
- `DDA9.1`: Timestamp access for debugging

#### User Defaults APIs

```xml
<dict>
    <key>NSPrivacyAccessedAPIType</key>
    <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
    <key>NSPrivacyAccessedAPITypeReasons</key>
    <array>
        <string>CA92.1</string>
    </array>
</dict>
```

**Reason Codes:**

- `CA92.1`: Access user defaults in same app group
- `1C8F.1`: Access user defaults for app functionality
- `C56D.1`: SDK-specific configuration preferences
- `AC6B.1`: Third-party SDK functionality

#### System Boot Time APIs

```xml
<dict>
    <key>NSPrivacyAccessedAPIType</key>
    <string>NSPrivacyAccessedAPICategorySystemBootTime</string>
    <key>NSPrivacyAccessedAPITypeReasons</key>
    <array>
        <string>35F9.1</string>
    </array>
</dict>
```

**Reason Codes:**

- `35F9.1`: Measure time elapsed for app functionality
- `8FFB.1`: Calculate absolute timestamp
- `3D61.1`: Measure time for performance testing

#### Disk Space APIs

```xml
<dict>
    <key>NSPrivacyAccessedAPIType</key>
    <string>NSPrivacyAccessedAPICategoryDiskSpace</string>
    <key>NSPrivacyAccessedAPITypeReasons</key>
    <array>
        <string>85F4.1</string>
    </array>
</dict>
```

**Reason Codes:**

- `85F4.1`: Display disk space to user
- `E174.1`: Check disk space before file operations
- `7D9E.1`: Health/fitness app disk space
- `B728.1`: User-initiated file management

## Data Collection

### Declaring Collected Data

```xml
<key>NSPrivacyCollectedDataTypes</key>
<array>
    <dict>
        <key>NSPrivacyCollectedDataType</key>
        <string>NSPrivacyCollectedDataTypeEmailAddress</string>
        <key>NSPrivacyCollectedDataTypeLinked</key>
        <true/>
        <key>NSPrivacyCollectedDataTypeTracking</key>
        <false/>
        <key>NSPrivacyCollectedDataTypePurposes</key>
        <array>
            <string>NSPrivacyCollectedDataTypePurposeAppFunctionality</string>
        </array>
    </dict>
</array>
```

### Common Data Types

- `NSPrivacyCollectedDataTypeEmailAddress`
- `NSPrivacyCollectedDataTypeName`
- `NSPrivacyCollectedDataTypePhoneNumber`
- `NSPrivacyCollectedDataTypeDeviceID`
- `NSPrivacyCollectedDataTypeUserID`
- `NSPrivacyCollectedDataTypePreciseLocation`
- `NSPrivacyCollectedDataTypeCoarseLocation`
- `NSPrivacyCollectedDataTypeSearchHistory`
- `NSPrivacyCollectedDataTypeBrowsingHistory`

### Collection Purposes

- `NSPrivacyCollectedDataTypePurposeThirdPartyAdvertising`
- `NSPrivacyCollectedDataTypePurposeAppFunctionality`
- `NSPrivacyCollectedDataTypePurposeAnalytics`
- `NSPrivacyCollectedDataTypePurposeProductPersonalization`
- `NSPrivacyCollectedDataTypePurposeOther`

## Tracking Configuration

### No Tracking

```xml
<key>NSPrivacyTracking</key>
<false/>
<key>NSPrivacyTrackingDomains</key>
<array/>
```

### With Tracking

```xml
<key>NSPrivacyTracking</key>
<true/>
<key>NSPrivacyTrackingDomains</key>
<array>
    <string>analytics.example.com</string>
    <string>tracking.example.com</string>
</array>
```

## Complete Example

### Networking SDK Privacy Manifest

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- No tracking -->
    <key>NSPrivacyTracking</key>
    <false/>
    <key>NSPrivacyTrackingDomains</key>
    <array/>

    <!-- Data collection -->
    <key>NSPrivacyCollectedDataTypes</key>
    <array>
        <dict>
            <key>NSPrivacyCollectedDataType</key>
            <string>NSPrivacyCollectedDataTypeUserID</string>
            <key>NSPrivacyCollectedDataTypeLinked</key>
            <true/>
            <key>NSPrivacyCollectedDataTypeTracking</key>
            <false/>
            <key>NSPrivacyCollectedDataTypePurposes</key>
            <array>
                <string>NSPrivacyCollectedDataTypePurposeAppFunctionality</string>
            </array>
        </dict>
    </array>

    <!-- Required Reasons APIs -->
    <key>NSPrivacyAccessedAPITypes</key>
    <array>
        <!-- User Defaults for caching -->
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>CA92.1</string>
            </array>
        </dict>

        <!-- File timestamps for cache validation -->
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryFileTimestamp</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>3B52.1</string>
            </array>
        </dict>
    </array>
</dict>
</plist>
```

### Analytics SDK Privacy Manifest

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- Tracking enabled -->
    <key>NSPrivacyTracking</key>
    <true/>
    <key>NSPrivacyTrackingDomains</key>
    <array>
        <string>analytics.myservice.com</string>
    </array>

    <!-- Data collection -->
    <key>NSPrivacyCollectedDataTypes</key>
    <array>
        <dict>
            <key>NSPrivacyCollectedDataType</key>
            <string>NSPrivacyCollectedDataTypeDeviceID</string>
            <key>NSPrivacyCollectedDataTypeLinked</key>
            <true/>
            <key>NSPrivacyCollectedDataTypeTracking</key>
            <true/>
            <key>NSPrivacyCollectedDataTypePurposes</key>
            <array>
                <string>NSPrivacyCollectedDataTypePurposeAnalytics</string>
            </array>
        </dict>
    </array>

    <!-- Required Reasons APIs -->
    <key>NSPrivacyAccessedAPITypes</key>
    <array>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategorySystemBootTime</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>35F9.1</string>
            </array>
        </dict>
    </array>
</dict>
</plist>
```

## CocoaPods Integration

### Podspec Configuration

```ruby
Pod::Spec.new do |spec|
  spec.name = 'MyAnalyticsSDK'
  spec.version = '1.0.0'

  spec.ios.deployment_target = '13.0'

  spec.source_files = 'Source/**/*.swift'

  # Include privacy manifest
  spec.resource_bundles = {
    'MyAnalyticsSDK' => [
      'Resources/PrivacyInfo.xcprivacy'
    ]
  }

  # Platform-specific privacy manifests
  spec.ios.resource_bundles = {
    'MyAnalyticsSDK_iOS' => ['Resources/iOS/PrivacyInfo.xcprivacy']
  }

  spec.osx.resource_bundles = {
    'MyAnalyticsSDK_macOS' => ['Resources/macOS/PrivacyInfo.xcprivacy']
  }
end
```

## Validation

### Check Privacy Manifest

```bash
# Lint with privacy manifest
pod lib lint

# Validate privacy manifest is included
pod lib lint --verbose | grep -i privacy
```

### Xcode Validation

1. Build your library in Xcode
2. Open **Report Navigator**
3. Check for privacy warnings
4. Verify privacy manifest in bundle

### App Store Validation

```bash
# Generate .xcarchive
xcodebuild archive -workspace MyApp.xcworkspace -scheme MyApp

# Validate before submission
xcodebuild -exportArchive -archivePath MyApp.xcarchive -exportPath MyApp.ipa -exportOptionsPlist ExportOptions.plist
```

## Best Practices

### Minimal Disclosure

```xml
<!-- Only declare what you actually use -->
<key>NSPrivacyCollectedDataTypes</key>
<array>
    <!-- Only include if you actually collect this data -->
</array>
```

### Accurate Reasons

```xml
<!-- Use correct reason codes -->
<key>NSPrivacyAccessedAPITypeReasons</key>
<array>
    <string>CA92.1</string>  <!-- Must match actual usage -->
</array>
```

### Regular Updates

```ruby
# Update privacy manifest when adding new APIs
spec.version = '1.1.0'  # Bump version

# Update PrivacyInfo.xcprivacy with new declarations
```

## Anti-Patterns

### Don't

❌ Omit privacy manifest for iOS 17+ apps

```ruby
# Missing privacy manifest - App Store rejection risk
spec.resource_bundles = {
  'MyLibrary' => ['Resources/**/*.png']
  # No PrivacyInfo.xcprivacy
}
```

❌ Use incorrect reason codes

```xml
<string>WRONG.1</string>  <!-- Invalid code -->
```

❌ Declare tracking without domains

```xml
<key>NSPrivacyTracking</key>
<true/>
<key>NSPrivacyTrackingDomains</key>
<array/>  <!-- Empty - inconsistent -->
```

### Do

✅ Include privacy manifest for all iOS SDKs

```ruby
spec.resource_bundles = {
  'MyLibrary' => ['Resources/PrivacyInfo.xcprivacy']
}
```

✅ Use accurate reason codes

```xml
<string>CA92.1</string>  <!-- Valid, matches usage -->
```

✅ Be truthful about tracking

```xml
<key>NSPrivacyTracking</key>
<true/>
<key>NSPrivacyTrackingDomains</key>
<array>
    <string>analytics.example.com</string>
</array>
```

## Resources

- [Apple Privacy Manifest Documentation](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files)
- [Required Reasons API Reference](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files/describing_use_of_required_reason_api)
- [App Privacy Details](https://developer.apple.com/app-store/app-privacy-details/)

## Related Skills

- cocoapods-podspec-fundamentals
- cocoapods-subspecs-organization
- cocoapods-publishing-workflow
