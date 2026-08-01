---
name: beta
description: Build and upload iOS app to TestFlight
---

---
name: beta
description: Build and upload iOS app to TestFlight
argument-hint: [--skip-build-increment] [--external] [--changelog "text"]
allowed-tools: Bash, Read
---

## TestFlight Beta Release

Build and upload the iOS app to TestFlight for beta testing.

### Pre-flight Checks
- Fastlane installed: !`fastlane --version 2>/dev/null | grep "fastlane " | head -1 || echo "✗ Not installed - run: brew install fastlane"`
- Fastfile exists: !`ls fastlane/Fastfile 2>/dev/null && echo "✓ Found" || echo "✗ Not found - run /setup-fastlane first"`
- App-specific password: !`[ -n "$FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD" ] && echo "✓ Set" || echo "⚠️ Not set - export FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD='xxxx-xxxx-xxxx-xxxx'"`

### Arguments: ${ARGUMENTS:-none}

---

## What This Does

1. **Syncs certificates** via Match (appstore type)
2. **Increments build number** (unless `--skip-build-increment`)
3. **Builds release archive** with gym
4. **Uploads to TestFlight** via pilot
5. **Optionally distributes to external testers** (if `--external`)

---

## Commands

### Standard Beta (Internal Testers)
```bash
cd project/product/swiftui-ios-app  # or your fastlane directory
fastlane beta
```

### Skip Build Number Increment
```bash
fastlane beta skip_build_increment:true
```

### External Testers (with changelog)
```bash
fastlane beta_external changelog:"Bug fixes and performance improvements"
```

---

## Troubleshooting

### "No value found for 'username'"
Set your Apple ID in `fastlane/Appfile`:
```ruby
apple_id("your@email.com")
```

### "Please sign in with an app-specific password"
1. Go to https://account.apple.com → Sign-In & Security → App-Specific Passwords
2. Generate a password named "Fastlane"
3. Export it:
```bash
export FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD='xxxx-xxxx-xxxx-xxxx'
```

### rsync error during export
If you see `--extended-attributes: unknown option`, Homebrew rsync conflicts with Xcode:
```bash
brew uninstall rsync  # Use system rsync
```

---

## After Upload

- Build will appear in TestFlight within 1-5 minutes
- Internal testers are notified automatically
- External testers require `beta_external` lane or manual distribution in App Store Connect
