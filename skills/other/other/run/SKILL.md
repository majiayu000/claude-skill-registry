---
name: run
description: Build and launch GridRacer in the iOS Simulator
model: haiku
allowed-tools:
  - Bash
  - Read
---

# Build and Run GridRacer

Quick iteration: build the app and launch in simulator.

## Steps

1. **Detect simulator**:
   ```bash
   SIMULATOR=$(xcrun simctl list devices available | grep -E "iPhone (16|15|14)" | grep -v unavailable | head -1 | sed -E 's/.*iPhone ([0-9]+).*/iPhone \1/')
   echo "Using: $SIMULATOR"
   ```

2. **Build** (stop on failure):
   ```bash
   xcodebuild -scheme GridRacer -configuration Debug -destination 'generic/platform=iOS Simulator' build 2>&1 | grep -E "(error:|warning:|BUILD|FAILED|SUCCEEDED)" | tail -20
   ```

3. **Find built app**:
   ```bash
   APP_PATH=$(find ~/Library/Developer/Xcode/DerivedData -name "GridRacer.app" -path "*/Build/Products/Debug-iphonesimulator/*" -not -path "*Index.noindex*" -type d 2>/dev/null | head -1)
   ```

4. **Boot, install, launch**:
   ```bash
   xcrun simctl boot "$SIMULATOR" 2>/dev/null || true
   xcrun simctl install booted "$APP_PATH"
   xcrun simctl launch booted trouarat.GridRacer
   open -a Simulator
   ```
