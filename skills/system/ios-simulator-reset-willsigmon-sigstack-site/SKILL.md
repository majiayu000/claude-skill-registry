---
name: ios-simulator-reset
description: Nuclear option - reset simulator and rebuild from scratch
model: haiku
---

# iOS Simulator Full Reset

When things are really broken, start fresh:

1. **Shutdown all simulators:**
```bash
xcrun simctl shutdown all
```

2. **Clean build artifacts:**
```bash
make clean
rm -rf ~/Library/Developer/Xcode/DerivedData/Leavn-*
```

3. **Reset simulator (optional - destructive):**
```bash
# Delete and recreate simulator
xcrun simctl delete [DEVICE_ID]
xcrun simctl create "Leavn Fresh" "iPhone 16 Pro"
```

4. **Fresh build:**
```bash
make sim-build
```

5. **Install and launch:**
```bash
make sim-run
```

**Use this when:**
- "It works in Xcode but not via make"
- Persistent runtime errors that don't make sense
- Simulator state is corrupted
- Nothing else works

**Return status of each step.**
