---
name: build
description: Build an iPlug2 plugin project for different formats and platforms (macOS, iOS, Windows)
---

# Build iPlug2 Plugin (iPlug2OOS)

Use this skill when the user wants to build their plugin project.

## Workflow

1. **Identify the project:**
   - If not specified, look for `.xcworkspace` files in the repo root (excluding TemplateProject)
   - Ask user to choose if multiple projects exist

2. **Build using the appropriate method below**

## macOS Build (xcodebuild)

```bash
xcodebuild -workspace [Project]/[Project].xcworkspace -scheme "[SCHEME]" -configuration [CONFIG] build 2>&1 | tee build.log
```

**Schemes:** `macOS-APP`, `macOS-AU`, `macOS-VST2`, `macOS-VST3`, `macOS-CLAP`, `macOS-AAX`, `macOS-AUv3`
**Configurations:** `Debug`, `Release`, `Tracer`

### Build Locations
- APP: `~/Applications/[PluginName].app`
- VST3: `~/Library/Audio/Plug-Ins/VST3/`
- AU: `~/Library/Audio/Plug-Ins/Components/`
- CLAP: `~/Library/Audio/Plug-Ins/CLAP/`

### Open in Xcode (recommended for debugging)
```bash
open [Project]/[Project].xcworkspace
```

## iOS Build

```bash
xcodebuild -workspace [Project]/[Project].xcworkspace -scheme "iOS-APP with AUv3" -configuration Debug -destination 'platform=iOS Simulator,name=iPhone 16 Pro' build
```

For running in Simulator, use the `run-ios-simulator` skill.

## Windows Build

Open the `.sln` file in Visual Studio:
```
[Project]/[Project].sln
```

Build from IDE or command line:
```cmd
msbuild [Project]/[Project].sln /p:Configuration=Release /p:Platform=x64
```

## Tips

- Build one scheme at a time; building all may fail if SDKs are missing
- Check `build.log` for issues
- If Skia backend is configured, run `iPlug2/Dependencies/download-prebuilt-libs.sh mac` first
- AUv3 requires code signing; use `macOS-AU` (AUv2) for simpler local testing
- Use `xcodebuild -workspace [Project]/[Project].xcworkspace -list` to see all available schemes

## Example

```bash
# Build standalone app (Debug)
xcodebuild -workspace MySynth/MySynth.xcworkspace -scheme "macOS-APP" -configuration Debug build

# Open the built app
open ~/Applications/MySynth.app

# Build AU plugin (Release)
xcodebuild -workspace MySynth/MySynth.xcworkspace -scheme "macOS-AU" -configuration Release build
```
