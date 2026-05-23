---
name: clean
description: Clean build artifacts and reset state
model: haiku
allowed-tools:
  - Bash
---

# Clean Build

Remove build artifacts and optionally reset simulator.

## Steps

### 1. Clean Xcode Build
```bash
xcodebuild -scheme GridRacer clean 2>&1 | tail -5
```

### 2. Remove DerivedData (optional, for deep clean)
```bash
rm -rf ~/Library/Developer/Xcode/DerivedData/GridRacer-*
echo "DerivedData cleaned"
```

### 3. Reset Simulator (optional)
```bash
# Stop the app if running
xcrun simctl terminate booted trouarat.GridRacer 2>/dev/null || true

# Uninstall the app
xcrun simctl uninstall booted trouarat.GridRacer 2>/dev/null || true

echo "Simulator reset"
```

### 4. Verify
```bash
# Check no cached builds
ls ~/Library/Developer/Xcode/DerivedData/ | grep -c GridRacer || echo "Clean"
```

## Output
```
Build artifacts cleaned.
Ready for fresh build with /build.
```
