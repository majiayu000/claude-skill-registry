---
name: app-store-deployment
description: Publishes mobile applications to iOS App Store and Google Play with code signing, versioning, and CI/CD automation. Use when preparing app releases, configuring signing certificates, or setting up automated deployment pipelines.
---

# App Store Deployment

Publish mobile applications to iOS App Store and Google Play with proper procedures.

## iOS Deployment

### Build and Archive
```bash
# Build archive
xcodebuild -workspace App.xcworkspace \
  -scheme App \
  -sdk iphoneos \
  -configuration Release \
  -archivePath build/App.xcarchive \
  archive

# Export IPA
xcodebuild -exportArchive \
  -archivePath build/App.xcarchive \
  -exportOptionsPlist ExportOptions.plist \
  -exportPath build/
```

### Upload to App Store Connect
```bash
xcrun altool --upload-app \
  --type ios \
  --file build/App.ipa \
  --username "$APPLE_ID" \
  --password "$APP_SPECIFIC_PASSWORD"
```

## Android Deployment

### Build Release APK/Bundle
```bash
# Generate keystore (once)
keytool -genkey -v -keystore release.keystore \
  -alias app -keyalg RSA -keysize 2048 -validity 10000

# Build release bundle
./gradlew bundleRelease
```

### gradle.properties
```properties
RELEASE_STORE_FILE=release.keystore
RELEASE_KEY_ALIAS=app
RELEASE_STORE_PASSWORD=****
RELEASE_KEY_PASSWORD=****
```

## Version Management

```json
{
  "version": "1.2.3",
  "ios": { "buildNumber": "45" },
  "android": { "versionCode": 45 }
}
```

## Pre-Deployment Checklist

- [ ] All tests passing (>80% coverage)
- [ ] App icons for all sizes
- [ ] Screenshots for store listing
- [ ] Privacy policy URL configured
- [ ] Permissions justified
- [ ] Tested on minimum supported OS
- [ ] Release notes prepared

## CI/CD (GitHub Actions)

```yaml
on:
  push:
    tags: ['v*']

jobs:
  deploy-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up environment
        run: |
          # Accept Xcode license if needed
          sudo xcodebuild -license accept || true

      - name: Build archive
        run: |
          xcodebuild -workspace App.xcworkspace \
            -scheme App \
            -sdk iphoneos \
            -configuration Release \
            -archivePath build/App.xcarchive \
            archive

      - name: Export IPA
        run: |
          xcodebuild -exportArchive \
            -archivePath build/App.xcarchive \
            -exportOptionsPlist ExportOptions.plist \
            -exportPath build/

      - name: Upload to App Store Connect
        env:
          APPLE_ID: ${{ secrets.APPLE_ID }}
          APP_SPECIFIC_PASSWORD: ${{ secrets.APP_SPECIFIC_PASSWORD }}
        run: |
          xcrun altool --upload-app \
            --type ios \
            --file build/App.ipa \
            --username "$APPLE_ID" \
            --password "$APP_SPECIFIC_PASSWORD"

  deploy-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./gradlew bundleRelease
      - uses: r0adkll/upload-google-play@v1
```

## Best Practices

- Automate deployment with CI/CD
- Test on physical devices
- Secure signing materials separately
- Monitor crash reports post-launch
