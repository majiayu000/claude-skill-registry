---
name: setup-ios
description: >-
  Set up iOS development environment for React Native/Expo.
  Use when configuring Xcode, CocoaPods, iOS simulators, or troubleshooting
  iOS-specific build issues.
  Invoked by: "ios setup", "xcode", "cocoapods", "ios environment", "ios simulator".
---

# iOS Development Setup SOP

**Version**: 1.0.0
**Last Updated**: 2026-01-11
**Status**: Active

> **Note**: This is a template. Replace placeholders like `{PROJECT_NAME}`, `{WORKSPACE_NAME}`, and `{BUNDLE_ID}` with your actual project values.

---

## Overview

### Purpose
Configure a complete iOS development environment for building and running the mobile app on iOS simulators and physical devices. This guide covers Xcode installation, command line tools, CocoaPods, watchman, and simulator configuration.

### When to Use
**ALWAYS**: Setting up new Mac for iOS development, Xcode installation, CocoaPods issues, simulator configuration, code signing setup
**SKIP**: Android-only development, Windows/Linux environments (iOS requires macOS)

---

## Quick Start

1. **Install Xcode**: App Store -> Xcode (15-30 GB download)
2. **Install CLI tools**: `xcode-select --install`
3. **Install Watchman**: `brew install watchman`
4. **Install Node via Volta**: `curl https://get.volta.sh | bash && volta install node@20`
5. **Run on simulator**: `task run-ios`

---

## Process Workflow

### Flow Diagram
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Install Xcode  │────>│  Setup CLI      │────>│  Install        │
│  (App Store)    │     │  Tools          │     │  Dependencies   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        v
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Run on         │<────│  Configure      │<────│  Setup          │
│  Simulator      │     │  Simulator      │     │  Node/Ruby      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Phase Summary
| Phase | Description | Time |
|-------|-------------|------|
| 1 | Install Xcode | 30-60 min |
| 2 | Setup CLI Tools | 5 min |
| 3 | Install Dependencies | 10 min |
| 4 | Configure Simulator | 5 min |
| 5 | Verify Installation | 5 min |

---

## Phase 1: Install Xcode

### From Mac App Store

1. Open **App Store** on your Mac
2. Search for **Xcode**
3. Click **Get** / **Install**
4. Wait for installation (15-30 GB download)

### Post-Installation

After installation, open Xcode once to:
- Accept the license agreement
- Install additional components

```bash
# Verify Xcode installation
xcodebuild -version
# Expected: Xcode 15.x or later
```

---

## Phase 2: Setup Command Line Tools

### Install Xcode CLI Tools

```bash
xcode-select --install
```

A dialog will appear. Click **Install** to proceed.

### Verify Installation

```bash
xcode-select -p
# Expected: /Applications/Xcode.app/Contents/Developer
```

### Accept License Agreement

```bash
sudo xcodebuild -license accept
```

---

## Phase 3: Install Dependencies

### Watchman (Required)

Watchman is required for React Native's Metro bundler to efficiently watch file changes.

```bash
brew install watchman
```

Verify installation:
```bash
watchman version
```

### Node.js via Volta (Recommended)

Volta provides automatic version switching for Node.js:

```bash
# Install Volta
curl https://get.volta.sh | bash

# Restart terminal, then install Node 20
volta install node@20

# Pin project to Node 20
volta pin node@20
```

Verify:
```bash
node --version  # Should show v20.x.x
volta --version # Should show version info
```

### CocoaPods (Optional)

CocoaPods is managed automatically by Expo, but you can install manually if needed:

```bash
sudo gem install cocoapods
```

### Ruby (Usually Pre-installed)

Ruby is required for CocoaPods:

```bash
ruby --version  # Should be available on macOS
gem --version   # Should be available
```

If Ruby issues occur:
```bash
brew install ruby
```

### ccache (Recommended for Faster Builds)

ccache dramatically speeds up C/C++ compilation for native iOS builds.

```bash
# Install ccache
brew install ccache

# Add to PATH (add to ~/.zshrc)
export PATH="/opt/homebrew/opt/ccache/libexec:$PATH"

# Verify installation
ccache --version
ccache -s  # Show statistics
```

**Important:** To use ccache with Xcode, launch Xcode from terminal:
```bash
xed ios/{WORKSPACE_NAME}.xcworkspace
```

---

## Phase 4: Configure iOS Simulator

### Open Simulator

From Xcode:
1. Open **Xcode**
2. Go to **Xcode > Open Developer Tool > Simulator**

From terminal:
```bash
open -a Simulator
```

### List Available Simulators

```bash
xcrun simctl list devices
```

### Select a Simulator

When running `task run-ios`, Expo will prompt you to select a simulator. You can also specify directly:

```bash
# Run on specific simulator
expo run:ios --device "iPhone 15 Pro"
```

### Install Additional Simulators

1. Open **Xcode**
2. Go to **Xcode > Settings > Platforms**
3. Click **+** to add new iOS versions
4. Download desired iOS runtime

---

## Phase 5: Verify Installation

### Run All Checks

```bash
# Check Node version
node --version

# Check Watchman
watchman version

# Check Xcode tools
xcode-select -p

# Check Homebrew
brew --version

# Check Ruby
ruby --version
```

### Test iOS Build

```bash
# Ensure environment is set up
task setup-dev

# Run on simulator (SIMULATOR=1 is default in .env.example)
task run-ios
```

---

## Running on iOS Simulator

### Quick Start

```bash
# Ensure environment is set up
task setup-dev

# Run on simulator (SIMULATOR=1 is default in .env.example)
task run-ios
```

### SIMULATOR Environment Variable

The `SIMULATOR` environment variable controls code signing:

| Value | Target | Code Signing |
|-------|--------|--------------|
| `SIMULATOR=1` | iOS Simulator | Not required (default) |
| `SIMULATOR=0` | Physical device | Required |

### Using Local Environment Variables for Simulator

Your `.env.local` file is created by:
```bash
task setup-local-env
```

**To switch targets**, edit `.env.local`:
```bash
SIMULATOR=1  # For simulator (default)
SIMULATOR=0  # For physical device
```

Then rebuild: `task run-ios`

---

## Running on Physical Device

### Requirements

1. **Apple Developer Account** (free or paid)
2. **Code Signing Certificate**
3. **Provisioning Profile**

### Setup Code Signing (Automatic)

Recommended for development:

1. Open `ios/{WORKSPACE_NAME}.xcworkspace` in Xcode
2. Select the project in the navigator
3. Go to **Signing & Capabilities** tab
4. Check **Automatically manage signing**
5. Select your **Team** (Apple ID)

### Setup Code Signing (Manual)

For production builds, use EAS Build which handles signing automatically:

```bash
task eas-build-ios
```

### Run on Device

1. Connect your iPhone via USB
2. Trust the computer on your device
3. Set `SIMULATOR=0` in your `.env` file
4. Run:
   ```bash
   task run-ios
   ```

---

## Xcode Tips

### Clear Derived Data

If you encounter strange build issues:

```bash
rm -rf ~/Library/Developer/Xcode/DerivedData
```

Or in Xcode: **Xcode > Settings > Locations > Derived Data** (click arrow to open in Finder, then delete contents).

### Reset Simulator

```bash
# Reset all simulators
xcrun simctl shutdown all
xcrun simctl erase all
```

### View Simulator Logs

```bash
# In a separate terminal while app is running
xcrun simctl spawn booted log stream --level debug --predicate 'subsystem == "{BUNDLE_ID}"'
```

---

## Quick Reference

### Common Commands

```bash
# Run on simulator
task run-ios

# Build native project only (no run)
task build-ios

# Regenerate native project
task generate

# Clean and rebuild
task clean
task generate
task run-ios

# List available simulators
xcrun simctl list devices

# Open simulator
open -a Simulator

# Reset simulator
xcrun simctl erase all
```

### Environment Variables

```bash
# For simulator (no code signing)
SIMULATOR=1

# For physical device (requires signing)
SIMULATOR=0
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No signing certificate" error | Set `SIMULATOR=1` in `.env` for simulator; configure signing in Xcode for device |
| "Command PhaseScriptExecution failed" | Run `cd ios && pod deintegrate && pod install && cd ..` |
| Simulator not appearing | Run `killall Simulator && open -a Simulator` |
| Build taking too long | Verify ccache is enabled: `ccache -s`, use `task generate-soft` for incremental prebuild |
| ccache not working | Launch Xcode from terminal: `xed ios/*.xcworkspace` |
| Xcode not found | Install Xcode from App Store |
| xcode-select path wrong | Run `sudo xcode-select -s /Applications/Xcode.app/Contents/Developer` |
| CocoaPods version mismatch | Run `sudo gem install cocoapods` to update |
| Metro bundler not connecting | Ensure `pnpm start` is running in a separate terminal |

---

## Push Notifications (Optional)

Push notifications require:

1. Apple Developer Program membership ($99/year)
2. Push notification certificate
3. Real Firebase credentials

For development without push notifications, the placeholder Firebase credentials work fine.

See `/setup-env` skill for Firebase setup details.

---

## Related Skills

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `/setup-dev` | Full environment setup | Complete development environment |
| `/setup-android` | Android environment | Setting up Android development |
| `/setup-env` | Environment variables | Configuring .env files |
| `/help` | Issue diagnosis | When encountering build errors |
| `/deploy` | App deployment | Building for App Store |

> **Note**: Skill paths (`/skill-name`) work after deployment. In the template repo, skills are in domain folders.

---

**End of SOP**
