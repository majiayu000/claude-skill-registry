---
name: macos-app-bundle
description: macOS application bundling with cargo-bundle and entitlements
tags: [macos, bundling, codesign, notarization, distribution]
---

# macos-app-bundle

Create distributable macOS `.app` bundles for Rust applications using cargo-bundle, with proper code signing, entitlements, and notarization for Gatekeeper approval.

## Quick Reference

```bash
# Install cargo-bundle (Zed's fork)
cargo install cargo-bundle --git https://github.com/zed-industries/cargo-bundle.git --branch zed-deploy

# Build and bundle
cargo bundle --release

# Sign and notarize
codesign --deep --force --timestamp --options runtime \
  --entitlements entitlements.plist \
  --sign "Developer ID Application: Name (TEAM_ID)" \
  "target/release/bundle/osx/App.app"

xcrun notarytool submit App.dmg --apple-id "$APPLE_ID" --password "$APPLE_PASSWORD" --team-id "$TEAM_ID" --wait
xcrun stapler staple App.dmg
```

## cargo-bundle

Use [Zed's fork](https://github.com/zed-industries/cargo-bundle) for GPUI apps - it's battle-tested and actively maintained.

### Installation

```bash
cargo install cargo-bundle --git https://github.com/zed-industries/cargo-bundle.git --branch zed-deploy
```

### Usage

```bash
# Development build
cargo bundle

# Release build
cargo bundle --release

# Specific target (universal binary)
cargo bundle --release --target aarch64-apple-darwin
cargo bundle --release --target x86_64-apple-darwin
```

Output: `target/release/bundle/osx/App Name.app`

## Bundle Metadata

Configure in `Cargo.toml` under `[package.metadata.bundle]`:

```toml
[package.metadata.bundle]
name = "Script Kit"                              # Display name (can include spaces)
identifier = "com.scriptkit.app"                 # Reverse-DNS bundle ID
icon = ["assets/icon.png", "assets/icon@2x.png", "assets/icon.icns"]
version = "0.1.0"                                # Must match package version
copyright = "Copyright (c) 2024 Script Kit. All rights reserved."
category = "public.app-category.developer-tools"
short_description = "Automation made simple"
osx_minimum_system_version = "10.15"             # Catalina minimum
osx_url_schemes = ["scriptkit"]                  # Custom URL handler
resources = ["assets/*"]                         # Bundle these files
osx_info_plist_exts = ["assets/Info.plist.ext"]  # Custom Info.plist additions
```

### Common Categories

| Category | Use Case |
|----------|----------|
| `public.app-category.developer-tools` | IDEs, terminals, automation |
| `public.app-category.productivity` | Task managers, note-taking |
| `public.app-category.utilities` | System tools, menu bar apps |
| `public.app-category.business` | Enterprise applications |

## Info.plist

cargo-bundle generates `Contents/Info.plist` from metadata. Extend it with `osx_info_plist_exts`:

### assets/Info.plist.ext

```xml
<key>LSUIElement</key>
<true/>
<key>LSBackgroundOnly</key>
<false/>
```

### Key Info.plist Fields

| Key | Description | Example |
|-----|-------------|---------|
| `CFBundleIdentifier` | Unique app ID | `com.scriptkit.app` |
| `CFBundleName` | Display name | `Script Kit` |
| `CFBundleVersion` | Build number | `1` |
| `CFBundleShortVersionString` | Version string | `1.0.0` |
| `LSMinimumSystemVersion` | Minimum macOS | `10.15` |
| `CFBundleURLTypes` | URL schemes | See below |
| `LSUIElement` | Agent app (no Dock) | `true`/`false` |
| `LSBackgroundOnly` | Background-only | `true`/`false` |

### URL Scheme Registration

Registered via `osx_url_schemes` in Cargo.toml. Results in:

```xml
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleURLName</key>
        <string>com.scriptkit.app</string>
        <key>CFBundleURLSchemes</key>
        <array>
            <string>scriptkit</string>
        </array>
    </dict>
</array>
```

Handle in Rust via `gpui::AppContext::on_open_urls()`.

## LSUIElement

Makes app an **agent app** - runs without Dock icon or menu bar. Perfect for:
- Launcher apps (like Raycast, Alfred)
- Menu bar utilities
- System tray applications
- Background daemons with UI

```xml
<!-- assets/Info.plist.ext -->
<key>LSUIElement</key>
<true/>
```

### LSUIElement vs LSBackgroundOnly

| Property | Dock Icon | Menu Bar | Windows |
|----------|-----------|----------|---------|
| Neither set | Yes | Yes | Yes |
| `LSUIElement=true` | No | No | Yes |
| `LSBackgroundOnly=true` | No | No | No |

Script Kit uses `LSUIElement=true` with `LSBackgroundOnly=false` - no Dock/menu but can show windows.

## Entitlements

Entitlements enable specific capabilities and are required for notarization.

### entitlements.plist

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- HARDENED RUNTIME EXCEPTIONS -->
    <!-- Required for JIT (bun/Node.js) -->
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    
    <!-- Required for generated code execution -->
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    
    <!-- Load non-Apple signed libraries -->
    <key>com.apple.security.cs.disable-library-validation</key>
    <true/>
    
    <!-- Child process spawning -->
    <key>com.apple.security.cs.disable-executable-page-protection</key>
    <true/>

    <!-- AUTOMATION -->
    <key>com.apple.security.automation.apple-events</key>
    <true/>

    <!-- HARDWARE -->
    <key>com.apple.security.device.audio-input</key>
    <true/>
    <key>com.apple.security.device.camera</key>
    <true/>

    <!-- NETWORK -->
    <key>com.apple.security.network.client</key>
    <true/>
    <key>com.apple.security.network.server</key>
    <true/>

    <!-- FILE ACCESS -->
    <key>com.apple.security.files.user-selected.read-write</key>
    <true/>
    <key>com.apple.security.files.downloads.read-write</key>
    <true/>
</dict>
</plist>
```

### Entitlements vs Runtime Permissions

| Type | When Applied | User Interaction |
|------|--------------|------------------|
| **Entitlements** | Baked into code signature | None - enables capability |
| **Runtime Permissions** | First use | User grants in System Preferences |

**Example:** Accessibility requires BOTH:
1. No special entitlement needed
2. User grants permission in System Preferences > Security & Privacy > Accessibility

### Common Entitlements

| Entitlement | Purpose |
|-------------|---------|
| `com.apple.security.cs.allow-jit` | JavaScript/JIT compilation |
| `com.apple.security.cs.allow-unsigned-executable-memory` | Runtime code generation |
| `com.apple.security.cs.disable-library-validation` | Load third-party dylibs |
| `com.apple.security.automation.apple-events` | AppleScript/osascript |
| `com.apple.security.network.client` | Outbound network |
| `com.apple.security.network.server` | Listen on ports |
| `com.apple.security.device.camera` | Camera access |
| `com.apple.security.device.audio-input` | Microphone access |

## URL Schemes

Register custom URL handlers to open your app via `yourapp://` links.

### Configuration

```toml
# Cargo.toml
[package.metadata.bundle]
osx_url_schemes = ["scriptkit"]
```

### Handling in Code

```rust
// In your GPUI app
cx.on_open_urls(|urls, cx| {
    for url in urls {
        if url.scheme() == "scriptkit" {
            // Handle: scriptkit://action?param=value
            handle_url(url, cx);
        }
    }
});
```

### Testing

```bash
open "scriptkit://run?script=hello"
```

## Code Signing

### Prerequisites

1. **Apple Developer Account** ($99/year)
2. **Developer ID Application certificate** (for distribution outside App Store)

### Find Your Identity

```bash
security find-identity -v -p codesigning
```

### Sign the Bundle

```bash
# Sign with hardened runtime (required for notarization)
codesign --deep --force --timestamp --options runtime \
  --entitlements entitlements.plist \
  --sign "Developer ID Application: Your Name (TEAM_ID)" \
  "target/release/bundle/osx/Script Kit.app"

# Verify
codesign -vvv --deep --strict "Script Kit.app"
spctl -a -vvv "Script Kit.app"
```

### Ad-Hoc Signing (Development Only)

```bash
codesign --force --deep --sign - "Script Kit.app"
```

**Warning:** Ad-hoc signed apps trigger Gatekeeper warnings.

### Environment Variables for CI

```bash
export APPLE_SIGNING_IDENTITY="Developer ID Application: Your Name (TEAM_ID)"
export APPLE_ID="your@email.com"
export APPLE_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"  # App-specific password
export APPLE_TEAM_ID="XXXXXXXXXX"
```

## Notarization

Apple requires notarization for apps distributed outside the App Store (macOS 10.15+).

### Submit for Notarization

```bash
# Create DMG first
hdiutil create -volname "Script Kit" \
  -srcfolder "target/release/bundle/osx/Script Kit.app" \
  -ov -format UDZO \
  "ScriptKit.dmg"

# Sign DMG
codesign --force --sign "$APPLE_SIGNING_IDENTITY" "ScriptKit.dmg"

# Submit and wait
xcrun notarytool submit "ScriptKit.dmg" \
  --apple-id "$APPLE_ID" \
  --password "$APPLE_APP_PASSWORD" \
  --team-id "$APPLE_TEAM_ID" \
  --wait

# Staple ticket to DMG
xcrun stapler staple "ScriptKit.dmg"
```

### Check Notarization Status

```bash
xcrun notarytool history --apple-id "$APPLE_ID" --password "$APPLE_APP_PASSWORD" --team-id "$APPLE_TEAM_ID"
```

### Common Notarization Errors

| Error | Solution |
|-------|----------|
| "Invalid credentials" | Check APPLE_ID and app-specific password |
| "The signature is invalid" | Ensure entitlements.plist exists and is valid |
| "Hardened runtime not enabled" | Add `--options runtime` to codesign |
| "Contains unsigned code" | Sign all nested binaries with `--deep` |

## Icon Generation

### Required Sizes for .icns

| Size | Filename |
|------|----------|
| 16x16 | icon_16x16.png |
| 32x32 | icon_16x16@2x.png, icon_32x32.png |
| 64x64 | icon_32x32@2x.png |
| 128x128 | icon_128x128.png |
| 256x256 | icon_128x128@2x.png, icon_256x256.png |
| 512x512 | icon_256x256@2x.png, icon_512x512.png |
| 1024x1024 | icon_512x512@2x.png |

### Generate from 1024x1024 Source

```bash
mkdir MyIcon.iconset

sips -z 16 16     icon-1024.png --out MyIcon.iconset/icon_16x16.png
sips -z 32 32     icon-1024.png --out MyIcon.iconset/icon_16x16@2x.png
sips -z 32 32     icon-1024.png --out MyIcon.iconset/icon_32x32.png
sips -z 64 64     icon-1024.png --out MyIcon.iconset/icon_32x32@2x.png
sips -z 128 128   icon-1024.png --out MyIcon.iconset/icon_128x128.png
sips -z 256 256   icon-1024.png --out MyIcon.iconset/icon_128x128@2x.png
sips -z 256 256   icon-1024.png --out MyIcon.iconset/icon_256x256.png
sips -z 512 512   icon-1024.png --out MyIcon.iconset/icon_256x256@2x.png
sips -z 512 512   icon-1024.png --out MyIcon.iconset/icon_512x512.png
cp icon-1024.png  MyIcon.iconset/icon_512x512@2x.png

iconutil -c icns MyIcon.iconset
```

## Bundle Structure

```
Script Kit.app/
├── Contents/
│   ├── Info.plist           # App metadata (generated + extensions)
│   ├── MacOS/
│   │   └── script-kit-gpui  # Main executable
│   ├── Resources/
│   │   ├── AppIcon.icns     # App icon
│   │   ├── assets/          # Bundled resources
│   │   └── ...
│   ├── Frameworks/          # Bundled frameworks (if any)
│   └── _CodeSignature/      # Code signature
```

## Anti-patterns

### Don't: Skip Hardened Runtime

```bash
# WRONG - won't notarize
codesign --force --sign "$IDENTITY" App.app

# CORRECT
codesign --force --options runtime --sign "$IDENTITY" App.app
```

### Don't: Forget Entitlements

```bash
# WRONG - JIT apps will crash
codesign --options runtime --sign "$IDENTITY" App.app

# CORRECT
codesign --options runtime --entitlements entitlements.plist --sign "$IDENTITY" App.app
```

### Don't: Sign Before Building

```bash
# WRONG - signature invalidated
codesign ... App.app
cargo bundle --release  # Overwrites!

# CORRECT
cargo bundle --release
codesign ... App.app
```

### Don't: Use Overly Broad Entitlements

```xml
<!-- WRONG - App Store rejection -->
<key>com.apple.security.cs.disable-library-validation</key>
<true/>
<key>com.apple.security.get-task-allow</key>
<true/>
```

Only include entitlements you actually need.

### Don't: Hardcode Signing Identity

```bash
# WRONG - breaks on other machines
codesign --sign "Developer ID Application: John (ABC123)" App.app

# CORRECT - use environment variable
codesign --sign "$APPLE_SIGNING_IDENTITY" App.app
```

### Don't: Forget to Staple

```bash
# WRONG - users still see Gatekeeper warning
xcrun notarytool submit App.dmg --wait
# Done!

# CORRECT - staple the ticket
xcrun notarytool submit App.dmg --wait
xcrun stapler staple App.dmg
```

## CI/CD Integration

### GitHub Actions Secrets

| Secret | Description |
|--------|-------------|
| `APPLE_CERTIFICATE_BASE64` | Base64-encoded .p12 certificate |
| `APPLE_CERTIFICATE_PASSWORD` | Password for .p12 |
| `APPLE_ID` | Apple Developer email |
| `APPLE_APP_PASSWORD` | App-specific password |
| `APPLE_TEAM_ID` | 10-character Team ID |

### Workflow Steps

1. Build release binary
2. Create .app bundle with cargo-bundle
3. Import certificate to temporary keychain
4. Sign with hardened runtime + entitlements
5. Create DMG
6. Notarize and staple
7. Upload to release

See `BUNDLING.md` for full GitHub Actions workflow example.

## References

- [cargo-bundle (Zed fork)](https://github.com/zed-industries/cargo-bundle)
- [Apple Code Signing Guide](https://developer.apple.com/documentation/security/code_signing_services)
- [Notarizing macOS Software](https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution)
- [Info.plist Key Reference](https://developer.apple.com/documentation/bundleresources/information_property_list)
- [Entitlements Reference](https://developer.apple.com/documentation/bundleresources/entitlements)
