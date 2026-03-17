---
name: run-ios-simulator
description: Build and run an iPlug2 iOS app in the iOS Simulator
---

# Run iOS App in Simulator

Use this skill when the user wants to run an iPlug2 iOS project in the iOS Simulator.

## Workflow

1. **Identify the project:**
   - If not specified, look for `.xcworkspace` files in the repo root
   - Ask user to choose if multiple projects exist

2. **Check available simulators and get UDID:**
   ```bash
   xcrun simctl list devices available | grep -E "iPhone|iPad"
   ```
   Extract the UDID from the output (the value in parentheses, e.g., `9E866BC3-9E64-4608-B4D0-D20F1DE3E980`)

   Or programmatically:
   ```bash
   xcrun simctl list devices available -j | jq -r '.devices[] | .[] | select(.name=="[DeviceName]") | .udid'
   ```

3. **Build for Simulator:**
   ```bash
   xcodebuild -workspace [Project]/[Project].xcworkspace \
     -scheme "iOS-APP with AUv3" \
     -configuration Debug \
     -destination 'platform=iOS Simulator,name=[DeviceName]' \
     build
   ```

4. **Find the built app:**
   ```bash
   find ~/Library/Developer/Xcode/DerivedData -name "[Project].app" -path "*Debug-iphonesimulator*" -type d 2>/dev/null | head -1
   ```

5. **Boot simulator and install (use UDID, not "booted"):**
   ```bash
   open -a Simulator
   xcrun simctl boot [UDID] 2>/dev/null || true
   xcrun simctl install [UDID] "[path/to/Project.app]"
   ```
   Using the UDID ensures the correct simulator is targeted even when multiple are running.

6. **Launch the app (use UDID):**
   ```bash
   # Get bundle ID from Info.plist
   /usr/libexec/PlistBuddy -c "Print :CFBundleIdentifier" "[path/to/Project.app]/Info.plist"
   xcrun simctl launch [UDID] [bundle.identifier]
   ```

## Notes

- **No code signing required** for Simulator builds
- **Always use UDID** to target a specific simulator, not `booted`
- Default device: iPhone 17 Pro (or latest available)
- The AUv3 plugin is embedded in the app and will be available to host apps in the Simulator
- Use `xcrun simctl list devices available` to see all device options
- If `jq` is not installed, extract UDID manually from `xcrun simctl list devices available` output

## Example

For TemplateProject on iPhone 17 Pro:
```bash
# Get the UDID for iPhone 17 Pro
UDID=$(xcrun simctl list devices available -j | jq -r '.devices[] | .[] | select(.name=="iPhone 17 Pro") | .udid')

# Build
xcodebuild -workspace TemplateProject/TemplateProject.xcworkspace \
  -scheme "iOS-APP with AUv3" -configuration Debug \
  -destination "platform=iOS Simulator,id=$UDID" build

# Install and run using UDID
open -a Simulator
xcrun simctl boot $UDID 2>/dev/null || true
xcrun simctl install $UDID ~/Library/Developer/Xcode/DerivedData/TemplateProject-*/Build/Products/Debug-iphonesimulator/TemplateProject.app
xcrun simctl launch $UDID com.AcmeInc.TemplateProject
```
