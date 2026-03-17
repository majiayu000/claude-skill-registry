---
name: ci-cd-integration
description: GitHub Actions CI/CD patterns for FinanceApp. Use when setting up build pipelines, automated testing, TestFlight deployment, or release workflows.
---

# CI/CD Integration — GitHub Actions

## Workflow Structure
```
.github/workflows/
  ci.yml           — Build + test on every PR
  release.yml      — TestFlight / App Store release
  lint.yml         — SwiftLint check on PR
```

## CI Workflow (ci.yml)
```yaml
name: CI
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test-packages:
    runs-on: macos-15
    strategy:
      matrix:
        package: [FinanceCore, FinanceData, FinanceUI]
    steps:
      - uses: actions/checkout@v4
      - name: Select Xcode
        run: sudo xcode-select -s /Applications/Xcode_16.app
      - name: Test ${{ matrix.package }}
        run: swift test --package-path Packages/${{ matrix.package }}

  build-ios:
    runs-on: macos-15
    steps:
      - uses: actions/checkout@v4
      - name: Select Xcode
        run: sudo xcode-select -s /Applications/Xcode_16.app
      - name: Build iOS
        run: |
          xcodebuild build-for-testing \
            -scheme FinanceApp-iOS \
            -destination 'platform=iOS Simulator,name=iPhone 16' \
            -skipPackagePluginValidation

  build-macos:
    runs-on: macos-15
    steps:
      - uses: actions/checkout@v4
      - name: Select Xcode
        run: sudo xcode-select -s /Applications/Xcode_16.app
      - name: Build macOS
        run: |
          xcodebuild build-for-testing \
            -scheme FinanceApp-macOS \
            -destination 'platform=macOS'

  lint:
    runs-on: macos-15
    steps:
      - uses: actions/checkout@v4
      - name: Install SwiftLint
        run: brew install swiftlint
      - name: Lint
        run: swiftlint lint --strict --reporter github-actions-logging
```

## Release Workflow (release.yml)
```yaml
name: Release
on:
  push:
    tags: ['v*']

jobs:
  testflight:
    runs-on: macos-15
    steps:
      - uses: actions/checkout@v4
      - name: Select Xcode
        run: sudo xcode-select -s /Applications/Xcode_16.app
      - name: Import certificates
        uses: apple-actions/import-codesign-certs@v2
        with:
          p12-file-base64: ${{ secrets.CERTIFICATES_P12 }}
          p12-password: ${{ secrets.CERTIFICATES_PASSWORD }}
      - name: Archive & Upload to TestFlight
        run: |
          xcodebuild archive \
            -scheme FinanceApp-iOS \
            -archivePath $RUNNER_TEMP/FinanceApp.xcarchive \
            -destination 'generic/platform=iOS'
          xcodebuild -exportArchive \
            -archivePath $RUNNER_TEMP/FinanceApp.xcarchive \
            -exportPath $RUNNER_TEMP/export \
            -exportOptionsPlist ExportOptions.plist
          xcrun altool --upload-app \
            -f $RUNNER_TEMP/export/*.ipa \
            -u ${{ secrets.APPLE_ID }} \
            -p ${{ secrets.APP_SPECIFIC_PASSWORD }}
```

## Required Secrets
| Secret | Purpose |
|--------|---------|
| `CERTIFICATES_P12` | Apple signing certificate (base64) |
| `CERTIFICATES_PASSWORD` | Certificate password |
| `APPLE_ID` | Apple Developer account email |
| `APP_SPECIFIC_PASSWORD` | App-specific password for uploads |
| `TEAM_ID` | Apple Developer Team ID |

## Branch Protection Rules
- Require CI to pass before merge to `main`
- Require at least 1 review approval
- Require linear history (squash merge)
- Auto-delete head branches after merge

## Versioning
- Use semantic versioning: `MAJOR.MINOR.PATCH`
- Tag releases: `git tag v1.0.0 && git push --tags`
- Build number auto-incremented by CI
