---
name: godot-setup-export
version: 1.0.0
displayName: Godot Export Setup
description: Use when setting up multi-platform exports for Godot projects, configuring export presets, icons, feature tags, build scripts, or CI/CD pipelines
author: Godot Superpowers Team
license: MIT
repository: https://github.com/anomalyco/godot-superpowers
homepage: https://github.com/anomalyco/godot-superpowers/tree/main/mini-skills/godot-setup-export
category: Godot
type: tool
difficulty: intermediate
audience: developers
keywords:
  - godot
  - export
  - build
  - ci/cd
  - github-actions
  - cross-platform
  - windows
  - mac
  - linux
  - web
  - mobile
platforms:
  - linux
  - macos
  - windows
---

# Godot Setup Export

## Overview

**Automates multi-platform export configuration for Godot projects.**

Setting up exports is tedious, error-prone, and requires platform-specific knowledge. This skill generates export presets, configures icons and splash screens, sets up feature tags, creates build scripts, and integrates with CI/CD pipelines.

## When to Use

**Use when:**
- Creating exports for a new Godot project
- Adding support for new platforms (Windows, Mac, Linux, Web, Mobile)
- Setting up automated builds via GitHub Actions
- Configuring icons, splash screens, or feature tags
- Creating custom export build scripts
- Migrating from local exports to CI/CD

**Don't use for:**
- Debugging export failures (use godot-debug-exports instead)
- Platform-specific native code compilation
- One-off manual exports (use Godot editor)

## Quick Reference

| Task | Tool/Method |
|------|-------------|
| Generate export presets | `godot --headless --generate-export-presets` |
| Set icons | `export_presets.cfg` icon field |
| Configure feature tags | `project.godot` `[feature]` sections |
| Automated builds | GitHub Actions workflow |
| Custom scripts | `export_presets.cfg` `custom_template/release` |

## Core Pattern

### Export Preset Generation

**Windows Desktop:**
```ini
[preset.0]
name="Windows Desktop"
platform="Windows Desktop"
export_filter="all_resources"
include_filter=""
export_files=[]
include_filter=""
export_path="builds/windows/Game.exe"
custom_features=""
export_filter="scenes"
export_files=PackedStringArray("res://main.tscn")
[preset.0.options]
custom_template/release=""
custom_template/debug=""

binary_format/architecture="x86_64"
codesign/enable=false
icon="res://assets/icons/windows_icon.ico"
```

**macOS:**
```ini
[preset.1]
name="macOS"
platform="macOS"
export_filter="all_resources"
export_path="builds/macos/Game.zip"
[preset.1.options]
binary_format/architecture="universal"
codesign/certificate_file=""
codesign/identity=""
icon="res://assets/icons/mac_icon.icns"
export/distribution_type=1
```

**Linux:**
```ini
[preset.2]
name="Linux"
platform="Linux"
export_filter="all_resources"
export_path="builds/linux/Game.x86_64"
[preset.2.options]
binary_format/architecture="x86_64"
custom_template/release=""
icon="res://assets/icons/linux_icon.png"
```

**Web:**
```ini
[preset.3]
name="Web"
platform="Web"
export_filter="all_resources"
export_path="builds/web/index.html"
[preset.3.options]
custom_template/release=""
custom_template/debug=""
variant/size_limit=16777216
vram_texture_compression/for_desktop=true
html/canvas_resize_policy=2
html/experimental_virtual_keyboard=false
progressive_web_app/enabled=false
```

**Android:**
```ini
[preset.4]
name="Android"
platform="Android"
export_filter="all_resources"
export_path="builds/android/Game.apk"
[preset.4.options]
gradle_build/use_gradle_build=false
gradle_build/export_format=0
gradle_build/min_sdk=21
gradle_build/target_sdk=33
version/code=1
version/name="1.0"
architectures/armeabi-v7a=false
architectures/arm64-v8a=true
architectures/x86=false
architectures/x86_64=false
keystore/debug=""
keystore/debug_user=""
keystore/debug_password=""
keystore/release=""
keystore/release_user=""
keystore/release_password=""
icon/export_identifier="com.example.game"
```

**iOS:**
```ini
[preset.5]
name="iOS"
platform="iOS"
export_filter="all_resources"
export_path="builds/ios/Game.xcodeproj"
[preset.5.options]
binary_format/architecture=1
application/app_store_team_id=""
application/bundle_identifier="com.example.game"
application/short_version="1.0"
application/version="1.0"
application/icon_interpolation=4
application/export_method_release=0
application/targeted_device_family=2
application/remove_simulator_arch=true
codesign/codesign=1
codesign/identity=""
codesign/provisioning_profile=""
```

## Icon and Splash Screen Setup

### Icon Requirements by Platform

| Platform | Format | Size | Notes |
|----------|--------|------|-------|
| Windows | `.ico` | 256x256 | Multi-resolution ICO file |
| macOS | `.icns` | 1024x1024 | Apple icon format |
| Linux | `.png` | 256x256 | Standard PNG |
| Web | `.png` | 512x512 | Used for favicon/PWA |
| Android | `.png` | 512x512 | Adaptive icons supported |
| iOS | `.png` | 1024x1024 | App Store icon |

### Project Configuration

**project.godot:**
```ini
[application]
config/name="Game Name"
config/description="Game description"
run/main_scene="res://scenes/main.tscn"
config/features=PackedStringArray("4.2", "Mobile")
boot_splash/bg_color=Color(0.14, 0.14, 0.14, 1)
boot_splash/image="res://assets/splash/splash_screen.png"
boot_splash/fullsize=true
boot_splash/use_filter=true

[display]
window/size/viewport_width=1920
window/size/viewport_height=1080
window/stretch/mode="canvas_items"
window/stretch/aspect="expand"
```

## Feature Tags Configuration

**Use feature tags for platform-specific behavior:**

```ini
[feature_tags]
editor=false
standalone=true
debug=false
release=true

; Platform-specific features
windows=false
macos=false
linux=false
android=false
ios=false
web=false
mobile=false
desktop=false
```

**In GDScript:**
```gdscript
# Platform-specific code
if OS.has_feature("mobile"):
    # Mobile touch controls
    touch_controls.visible = true
elif OS.has_feature("desktop"):
    # Desktop keyboard/mouse
    touch_controls.visible = false

# Debug vs release
if OS.has_feature("debug"):
    show_debug_info()
    enable_cheats()
```

## Custom Build Scripts

### Windows Batch Script
```batch
@echo off
set PROJECT_PATH=%~dp0
set GODOT_PATH="C:\Program Files\Godot\Godot_v4.x.exe"
set BUILD_DIR=%PROJECT_PATH%builds\windows

if not exist %BUILD_DIR% mkdir %BUILD_DIR%

%GODOT_PATH% --headless --path %PROJECT_PATH% --export-release "Windows Desktop" "%BUILD_DIR%\Game.exe"

if %ERRORLEVEL% NEQ 0 (
    echo Export failed!
    exit /b 1
)

echo Export complete: %BUILD_DIR%\Game.exe
```

### Linux/macOS Shell Script
```bash
#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GODOT_PATH="/usr/bin/godot"
BUILD_DIR="$PROJECT_DIR/builds"

mkdir -p "$BUILD_DIR/linux" "$BUILD_DIR/macos" "$BUILD_DIR/web"

# Linux
$GODOT_PATH --headless --path "$PROJECT_DIR" \
    --export-release "Linux" "$BUILD_DIR/linux/Game.x86_64"

# macOS  
$GODOT_PATH --headless --path "$PROJECT_DIR" \
    --export-release "macOS" "$BUILD_DIR/macos/Game.zip"

# Web
$GODOT_PATH --headless --path "$PROJECT_DIR" \
    --export-release "Web" "$BUILD_DIR/web/index.html"

echo "All exports complete!"
```

### PowerShell Script
```powershell
$ProjectPath = $PSScriptRoot
$GodotPath = "C:\Program Files\Godot\Godot_v4.x.exe"
$BuildDir = Join-Path $ProjectPath "builds"

New-Item -ItemType Directory -Force -Path $BuildDir | Out-Null

$Presets = @(
    @{ Name = "Windows Desktop"; Path = "$BuildDir\windows\Game.exe" },
    @{ Name = "Linux"; Path = "$BuildDir\linux\Game.x86_64" }
)

foreach ($Preset in $Presets) {
    $Dir = Split-Path $Preset.Path -Parent
    New-Item -ItemType Directory -Force -Path $Dir | Out-Null
    
    & $GodotPath --headless --path $ProjectPath `
        --export-release $Preset.Name $Preset.Path
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Export failed for $($Preset.Name)"
        exit 1
    }
}

Write-Host "Exports complete!"
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
name: Build and Export

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  GODOT_VERSION: 4.2.1
  EXPORT_NAME: game-name

jobs:
  export-windows:
    name: Windows Export
    runs-on: ubuntu-22.04
    container:
      image: barichello/godot-ci:4.2.1
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        
      - name: Setup Godot
        run: |
          mkdir -p ~/.config/godot/
          echo "[export_presets]" > ~/.config/godot/editor_settings-4.tres
          
      - name: Windows Build
        run: |
          mkdir -p build/windows
          godot --headless --verbose --export-release "Windows Desktop" ./build/windows/$EXPORT_NAME.exe
          
      - name: Upload Artifact
        uses: actions/upload-artifact@v4
        with:
          name: windows
          path: build/windows

  export-linux:
    name: Linux Export
    runs-on: ubuntu-22.04
    container:
      image: barichello/godot-ci:4.2.1
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        
      - name: Linux Build
        run: |
          mkdir -p build/linux
          godot --headless --verbose --export-release "Linux" ./build/linux/$EXPORT_NAME.x86_64
          
      - name: Upload Artifact
        uses: actions/upload-artifact@v4
        with:
          name: linux
          path: build/linux

  export-web:
    name: Web Export
    runs-on: ubuntu-22.04
    container:
      image: barichello/godot-ci:4.2.1
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        
      - name: Web Build
        run: |
          mkdir -p build/web
          godot --headless --verbose --export-release "Web" ./build/web/index.html
          
      - name: Upload Artifact
        uses: actions/upload-artifact@v4
        with:
          name: web
          path: build/web
          
      - name: Deploy to GitHub Pages
        if: github.ref == 'refs/heads/main'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build/web

  export-android:
    name: Android Export
    runs-on: ubuntu-22.04
    container:
      image: barichello/godot-ci:4.2.1
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        
      - name: Setup Android SDK
        run: |
          mkdir -p ~/.config/godot/
          echo "[export_presets]" > ~/.config/godot/editor_settings-4.tres
          
      - name: Android Build
        run: |
          mkdir -p build/android
          godot --headless --verbose --export-release "Android" ./build/android/$EXPORT_NAME.apk
          
      - name: Upload Artifact
        uses: actions/upload-artifact@v4
        with:
          name: android
          path: build/android

  export-macos:
    name: macOS Export
    runs-on: ubuntu-22.04
    container:
      image: barichello/godot-ci:4.2.1
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        
      - name: macOS Build
        run: |
          mkdir -p build/macos
          godot --headless --verbose --export-release "macOS" ./build/macos/$EXPORT_NAME.zip
          
      - name: Upload Artifact
        uses: actions/upload-artifact@v4
        with:
          name: macos
          path: build/macos

  create-release:
    name: Create Release
    needs: [export-windows, export-linux, export-web, export-android, export-macos]
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
    steps:
      - name: Download All Artifacts
        uses: actions/download-artifact@v4
        
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            windows/*.exe
            linux/*
            android/*.apk
            macos/*.zip
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Common Mistakes

| Mistake | Solution |
|---------|----------|
| Missing export presets file | Run Godot editor once to generate or copy template |
| Wrong export path format | Use forward slashes on all platforms |
| Icons not loading | Ensure icon files exist at specified paths |
| Android keystore errors | Set up debug keystore or configure release keystore |
| Web export fails | Check export template is installed |
| CI/CD can't find Godot | Use godot-ci Docker image or install Godot manually |

## Examples

### Before: Manual Export (❌)
```gdscript
# Manual export via Godot editor
# 1. Open Project > Export
# 2. Click Add for each platform
# 3. Configure each preset manually
# 4. Click Export Project for each
# 5. Repeat every time you want to build
```

### After: Automated Setup (✅)
```ini
# export_presets.cfg - generated once, committed to repo
[preset.0]
name="Windows Desktop"
export_path="builds/windows/Game.exe"
...

[preset.1]
name="macOS"
export_path="builds/macos/Game.zip"
...

[preset.2]
name="Linux"
export_path="builds/linux/Game.x86_64"
...

[preset.3]
name="Web"
export_path="builds/web/index.html"
...

# Then run: ./build.sh or let GitHub Actions handle it automatically
```

### Complete Project Structure
```
my-game/
├── project.godot
├── export_presets.cfg          # All export configurations
├── .github/
│   └── workflows/
│       └── export.yml          # CI/CD pipeline
├── assets/
│   └── icons/
│       ├── windows_icon.ico
│       ├── mac_icon.icns
│       ├── linux_icon.png
│       ├── android_icon.png
│       └── ios_icon.png
├── scripts/
│   └── build.sh                # Local build script
└── builds/                     # Output directory (gitignored)
    ├── windows/
    ├── macos/
    ├── linux/
    ├── web/
    └── android/
```

## Export Command Reference

```bash
# Export release build
godot --headless --export-release "Preset Name" "output/path"

# Export debug build
godot --headless --export-debug "Preset Name" "output/path"

# Export with pack file only (no executable)
godot --headless --export-pack "Preset Name" "output.pck"

# Export from specific project path
godot --headless --path /path/to/project --export-release "Preset" "output"

# Verbose output for debugging
godot --headless --verbose --export-release "Preset" "output"
```

## Platform-Specific Notes

### Windows
- Requires export template: `windows_x86_64.exe`
- Icon must be `.ico` format with multiple resolutions
- Codesigning optional but recommended for distribution

### macOS
- Requires export template: `macos.zip`
- App Store requires specific provisioning profile
- Notarization required for distribution outside App Store

### Linux
- Most straightforward export
- Single executable file
- No special requirements

### Web
- Requires export template: `web.zip`
- SharedArrayBuffer required for threads
- May need custom HTML template for fullscreen

### Android
- Requires Android SDK and export templates
- Keystore required for release builds
- Debug keystore auto-generated if not specified

### iOS
- Requires macOS and Xcode
- Must export to Xcode project, then build
- Apple Developer account required

## Version Control

**Commit to repo:**
- `export_presets.cfg` - Contains all export configurations
- `.github/workflows/export.yml` - CI/CD pipeline
- Build scripts (`build.sh`, `build.bat`, `build.ps1`)

**Add to `.gitignore`:**
```
builds/
*.tmp
*.import
```

## Troubleshooting

### "Export preset not found"
- Ensure preset name matches exactly (case-sensitive)
- Check `export_presets.cfg` exists in project root
- Verify preset is configured in Godot editor

### "Export template not found"
- Install export templates: Editor > Manage Export Templates
- For CI/CD, use godot-ci Docker image with templates included

### "Cannot open file for writing"
- Ensure output directory exists
- Check write permissions
- Use absolute paths in CI/CD environments

### Android build fails
- Verify ANDROID_HOME environment variable
- Check keystore configuration
- Ensure minimum SDK version matches template

### Web export blank
- Check browser console for errors
- Verify SharedArrayBuffer headers if using threads
- Try disabling threads in export options

## Real-World Impact

- **Setup time**: 2 hours → 10 minutes
- **Build consistency**: Manual errors eliminated
- **Release cadence**: Days → Hours
- **Multi-platform**: Set up once, build anywhere
