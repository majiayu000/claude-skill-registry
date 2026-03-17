---
name: build-cmake
description: Build an iPlug2 plugin project using CMake (Ninja or Xcode generator)
---

# Build iPlug2 Plugin with CMake

Use this skill when the user wants to build their plugin project using CMake.

## Workflow

1. **Identify the project:**
   - Look for `CMakeLists.txt` in project directories

2. **Choose a preset** based on platform and build requirements

## Using CMake Presets

The project uses CMake presets for standardized builds. Prefer `--preset` instead of manual `-G` flags.

### List Available Presets

```bash
cmake --list-presets
```

### macOS Builds

```bash
# Configure with Ninja (fast builds)
cmake --preset macos-ninja -S [ProjectName]

# Build
cmake --build build/macos-ninja --target [ProjectName]-app

# Or with Xcode (for debugging)
cmake --preset macos-xcode -S [ProjectName]
cmake --build build/macos-xcode --config Release --target [ProjectName]-app

# Universal binary (arm64 + x86_64)
cmake --preset macos-xcode-universal -S [ProjectName]
cmake --build build/macos-xcode-universal --config Release
```

### iOS Builds

```bash
# iOS Device
cmake --preset ios-xcode -S [ProjectName]
cmake --build build/ios-xcode --config Release

# iOS Simulator
cmake --preset ios-sim-xcode -S [ProjectName]
cmake --build build/ios-sim-xcode --config Release
```

For running in Simulator, use the `run-ios-simulator` skill.

### visionOS Builds

```bash
# visionOS Device
cmake --preset visionos-xcode -S [ProjectName]
cmake --build build/visionos-xcode --config Release

# visionOS Simulator
cmake --preset visionos-sim-xcode -S [ProjectName]
cmake --build build/visionos-sim-xcode --config Release
```

### Windows Builds

```bash
# Visual Studio 2022 (x64)
cmake --preset windows-vs2022 -S [ProjectName]
cmake --build build/windows-vs2022 --config Release

# ARM64EC
cmake --preset windows-vs2022-arm64ec -S [ProjectName]
cmake --build build/windows-vs2022-arm64ec --config Release
```

### Web/WAM Build (Emscripten)

```bash
# Configure (requires EMSDK environment)
cmake --preset wam -S [ProjectName]

# Build
cmake --build build/wam --target [ProjectName]-wam

# Create distribution
cmake --build build/wam --target [ProjectName]-wam-dist
```

Output in `build/wam/out/[ProjectName]-wam/`

## Available Configure Presets

| Preset | Platform | Generator | Description |
|--------|----------|-----------|-------------|
| `macos-ninja` | macOS | Ninja | Fast command-line builds (NanoVG/Metal) |
| `macos-make` | macOS | Make | Unix Makefiles (NanoVG/Metal) |
| `macos-xcode` | macOS | Xcode | IDE builds with debugging |
| `macos-xcode-universal` | macOS | Xcode | Universal binary (arm64+x86_64) |
| `ios-xcode` | iOS | Xcode | iOS device builds |
| `ios-sim-xcode` | iOS | Xcode | iOS Simulator builds |
| `visionos-xcode` | visionOS | Xcode | visionOS device builds |
| `visionos-sim-xcode` | visionOS | Xcode | visionOS Simulator builds |
| `windows-ninja` | Windows | Ninja | Fast Windows command-line builds |
| `windows-vs2022` | Windows | VS2022 | Windows x64 builds |
| `windows-vs2022-arm64ec` | Windows | VS2022 | Windows ARM64EC builds |
| `wam` | Web | Ninja | Emscripten/WebAssembly builds |

## Available Targets

- `[ProjectName]-app` - Standalone application
- `[ProjectName]-vst3` - VST3 plugin
- `[ProjectName]-au` - Audio Unit (AUv2)
- `[ProjectName]-clap` - CLAP plugin
- `[ProjectName]AU-framework` - AUv3 framework
- `[ProjectName]AUv3-appex` - AUv3 app extension
- `[ProjectName]-ios-app` - iOS standalone app
- `[ProjectName]-wam` - Web Audio Module

## Graphics Backend and Renderer

Default configuration uses NanoVG with Metal (macOS/iOS) or GL2 (Windows).

To use Skia backend, add cache variables:

```bash
cmake --preset macos-ninja -S [ProjectName] \
  -DIGRAPHICS_BACKEND=SKIA \
  -DIGRAPHICS_RENDERER=METAL
```

Valid combinations:
- **NanoVG**: GL2, GL3, METAL
- **Skia**: GL3, METAL, CPU

**Note:** Skia requires prebuilt libraries:
```bash
./iPlug2/Dependencies/download-prebuilt-libs.sh mac
```

## Build Locations (symlinked on macOS)

- APP: `~/Applications/[ProjectName].app`
- VST3: `~/Library/Audio/Plug-Ins/VST3/`
- AU: `~/Library/Audio/Plug-Ins/Components/`
- CLAP: `~/Library/Audio/Plug-Ins/CLAP/`

## Clean Build

```bash
# Remove build directory and reconfigure
rm -rf build/macos-ninja
cmake --preset macos-ninja -S [ProjectName]
```

## Example

```bash
# Quick build of standalone app
cmake --preset macos-ninja -S MySynth
cmake --build build/macos-ninja --target MySynth-app

# Open the built app
open ~/Applications/MySynth.app

# Build for iOS Simulator
cmake --preset ios-sim-xcode -S MySynth
cmake --build build/ios-sim-xcode --config Release
```
