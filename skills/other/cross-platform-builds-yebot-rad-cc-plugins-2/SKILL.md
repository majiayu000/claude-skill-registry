---
name: cross-platform-builds
description: Comprehensive guide to building JUCE plugins for macOS, Windows, and Linux with CMake, code signing, notarization, and CI/CD. Use when configuring builds, setting up CI/CD pipelines, troubleshooting cross-platform compilation, implementing code signing, or creating installers for multiple platforms.
allowed-tools: Read, Grep, Glob
---

# Cross-Platform Builds for JUCE Plugins

Comprehensive guide to building JUCE audio plugins across macOS, Windows, and Linux with proper configuration, code signing, and continuous integration.

## Overview

JUCE audio plugins must be built for multiple platforms and plugin formats:
- **macOS**: VST3, AU (Audio Unit), AAX
- **Windows**: VST3, AAX
- **Linux**: VST3

Each platform has specific requirements for build tools, code signing, and packaging. This skill covers:
1. CMake configuration for all platforms and formats
2. Platform-specific build instructions
3. Code signing and notarization
4. Continuous integration setup
5. Reproducible builds

---

## 1. CMake Configuration

### Root CMakeLists.txt Structure

```cmake
cmake_minimum_required(VERSION 3.22)

project(MyPlugin VERSION 1.0.0)

# C++17 minimum for JUCE 7+
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Export compile_commands.json for IDEs
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Add JUCE
add_subdirectory(JUCE)

# Plugin formats to build
set(PLUGIN_FORMATS VST3 AU Standalone)

# Add AAX if PACE SDK is available
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/SDKs/AAX")
    list(APPEND PLUGIN_FORMATS AAX)
    juce_set_aax_sdk_path("${CMAKE_CURRENT_SOURCE_DIR}/SDKs/AAX")
endif()

# Define the plugin
juce_add_plugin(MyPlugin
    COMPANY_NAME "YourCompany"
    PLUGIN_MANUFACTURER_CODE Manu  # 4-character code
    PLUGIN_CODE Plug                # 4-character code (unique!)
    FORMATS ${PLUGIN_FORMATS}
    PRODUCT_NAME "MyPlugin"

    # Bundle IDs
    BUNDLE_ID com.yourcompany.myplugin

    # Plugin characteristics
    IS_SYNTH FALSE
    NEEDS_MIDI_INPUT FALSE
    NEEDS_MIDI_OUTPUT FALSE
    IS_MIDI_EFFECT FALSE
    EDITOR_WANTS_KEYBOARD_FOCUS FALSE

    # Copy plugin to system folder after build
    COPY_PLUGIN_AFTER_BUILD TRUE

    # VST3 category
    VST3_CATEGORIES Fx

    # AU type (aufx = effect, aumu = instrument)
    AU_MAIN_TYPE kAudioUnitType_Effect
)

# Source files
target_sources(MyPlugin PRIVATE
    Source/PluginProcessor.cpp
    Source/PluginEditor.cpp
    Source/DSP/Filter.cpp
    Source/DSP/Modulation.cpp
)

# Public compile definitions
target_compile_definitions(MyPlugin PUBLIC
    JUCE_WEB_BROWSER=0
    JUCE_USE_CURL=0
    JUCE_VST3_CAN_REPLACE_VST2=0
    JUCE_DISPLAY_SPLASH_SCREEN=0  # Commercial license only!
)

# Link JUCE modules
target_link_libraries(MyPlugin PRIVATE
    juce::juce_audio_utils
    juce::juce_dsp
    juce::juce_recommended_config_flags
    juce::juce_recommended_lto_flags
    juce::juce_recommended_warning_flags
)

# Platform-specific settings
if(APPLE)
    # macOS deployment target
    set(CMAKE_OSX_DEPLOYMENT_TARGET "10.13" CACHE STRING "Minimum macOS version")

    # Universal binary (Apple Silicon + Intel)
    set(CMAKE_OSX_ARCHITECTURES "arm64;x86_64" CACHE STRING "macOS architectures")

    # Hardened runtime for notarization
    target_compile_options(MyPlugin PUBLIC
        -Wall -Wextra -Wpedantic
    )
elseif(WIN32)
    # Static runtime for standalone distribution
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")

    # Windows-specific definitions
    target_compile_definitions(MyPlugin PRIVATE
        _CRT_SECURE_NO_WARNINGS
    )
elseif(UNIX)
    # Linux-specific flags
    target_compile_options(MyPlugin PRIVATE
        -Wall -Wextra
    )

    # Link against ALSA, JACK, etc.
    find_package(PkgConfig REQUIRED)
    pkg_check_modules(ALSA REQUIRED alsa)
    target_link_libraries(MyPlugin PRIVATE ${ALSA_LIBRARIES})
endif()

# Tests (optional)
option(BUILD_TESTS "Build unit tests" ON)
if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(Tests)
endif()
```

### Key Configuration Options

#### Plugin Codes
```cmake
PLUGIN_MANUFACTURER_CODE Manu  # Your unique 4-character manufacturer ID
PLUGIN_CODE Plug                # Unique 4-character plugin ID
```

**Important**: Register manufacturer code at [Steinberg](https://www.steinberg.net/en/company/developers.html) to avoid conflicts.

#### Bundle Identifiers
```cmake
BUNDLE_ID com.yourcompany.myplugin  # Reverse domain notation
```

Must be unique and consistent across versions for AU validation.

#### Plugin Characteristics
```cmake
IS_SYNTH TRUE                   # Instrument vs effect
NEEDS_MIDI_INPUT TRUE          # Accept MIDI input
NEEDS_MIDI_OUTPUT FALSE        # Send MIDI output
IS_MIDI_EFFECT FALSE           # MIDI-only processing (no audio)
```

#### VST3 Categories
```cmake
VST3_CATEGORIES Fx              # Effect
VST3_CATEGORIES Instrument      # Instrument
VST3_CATEGORIES Fx Dynamics     # Multiple categories
```

Available categories: `Fx`, `Instrument`, `Analyzer`, `Delay`, `Distortion`, `Dynamics`, `EQ`, `Filter`, `Mastering`, `Modulation`, `Restoration`, `Reverb`, `Spatial`, `Synth`, `Tools`

#### AU Types
```cmake
AU_MAIN_TYPE kAudioUnitType_Effect           # Effect
AU_MAIN_TYPE kAudioUnitType_MusicDevice      # Instrument
AU_MAIN_TYPE kAudioUnitType_MIDIProcessor    # MIDI effect
```

---

## 2. macOS Builds

### Prerequisites

1. **Xcode** (latest version recommended)
   ```bash
   xcode-select --install
   ```

2. **CMake** (3.22+)
   ```bash
   brew install cmake
   ```

3. **Developer ID Certificate** (for distribution)
   - Enroll in Apple Developer Program ($99/year)
   - Create "Developer ID Application" certificate in Xcode

### Building

```bash
# Configure
cmake -B build-mac -G Xcode \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_OSX_DEPLOYMENT_TARGET=10.13 \
      -DCMAKE_OSX_ARCHITECTURES="arm64;x86_64"

# Build all formats
cmake --build build-mac --config Release --parallel

# Or build with Xcode
open build-mac/MyPlugin.xcodeproj
```

### Universal Binaries (Apple Silicon + Intel)

```cmake
# In CMakeLists.txt
set(CMAKE_OSX_ARCHITECTURES "arm64;x86_64")
```

Or at build time:
```bash
cmake -B build-mac -DCMAKE_OSX_ARCHITECTURES="arm64;x86_64"
```

Verify architectures:
```bash
lipo -info build-mac/MyPlugin_artefacts/Release/VST3/MyPlugin.vst3/Contents/MacOS/MyPlugin

# Output: Architectures in the fat file: MyPlugin are: x86_64 arm64
```

### Code Signing

#### Manual Signing
```bash
# Sign VST3
codesign --force \
         --sign "Developer ID Application: Your Name (TEAM_ID)" \
         --options runtime \
         --entitlements Resources/Entitlements.plist \
         --timestamp \
         --deep \
         MyPlugin.vst3

# Sign AU
codesign --force \
         --sign "Developer ID Application: Your Name (TEAM_ID)" \
         --options runtime \
         --timestamp \
         --deep \
         MyPlugin.component

# Verify signature
codesign --verify --deep --strict --verbose=2 MyPlugin.vst3
```

#### Entitlements File (Resources/Entitlements.plist)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
         "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- Allow JIT for DSP optimization -->
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>

    <!-- Allow loading unsigned plugins (for VST3 presets, etc.) -->
    <key>com.apple.security.cs.disable-library-validation</key>
    <true/>

    <!-- For networked plugins (optional) -->
    <key>com.apple.security.network.client</key>
    <true/>
</dict>
</plist>
```

#### Automated Signing in CMake
```cmake
# Add to CMakeLists.txt
if(APPLE AND CMAKE_BUILD_TYPE STREQUAL "Release")
    set(CODESIGN_IDENTITY "Developer ID Application: Your Name")

    add_custom_command(TARGET MyPlugin POST_BUILD
        COMMAND codesign --force
                --sign "${CODESIGN_IDENTITY}"
                --options runtime
                --entitlements "${CMAKE_SOURCE_DIR}/Resources/Entitlements.plist"
                --timestamp
                $<TARGET_BUNDLE_DIR:MyPlugin>
        COMMENT "Code signing ${TARGET}"
    )
endif()
```

### Notarization

Required for macOS 10.15+ (Catalina and later).

#### Setup
1. Create app-specific password at [appleid.apple.com](https://appleid.apple.com)
2. Store credentials in keychain:
   ```bash
   xcrun notarytool store-credentials "notary-profile" \
         --apple-id "developer@example.com" \
         --team-id "TEAM_ID" \
         --password "xxxx-xxxx-xxxx-xxxx"
   ```

#### Notarize Plugin
```bash
# 1. Create ZIP for notarization
ditto -c -k --keepParent MyPlugin.vst3 MyPlugin-vst3.zip

# 2. Submit to notary service
xcrun notarytool submit MyPlugin-vst3.zip \
      --keychain-profile "notary-profile" \
      --wait

# 3. If successful, staple the ticket
xcrun stapler staple MyPlugin.vst3

# 4. Verify
spctl -a -vvv -t install MyPlugin.vst3
xcrun stapler validate MyPlugin.vst3
```

#### Troubleshooting Notarization

Check submission status:
```bash
xcrun notarytool info <submission-id> --keychain-profile "notary-profile"
```

View detailed log:
```bash
xcrun notarytool log <submission-id> --keychain-profile "notary-profile"
```

Common issues:
- **Missing entitlements**: Add to Entitlements.plist
- **Unsigned nested binaries**: Sign all frameworks before parent bundle
- **Invalid bundle structure**: Verify with `pkgutil --check-signature`

### AU Validation

```bash
# Validate AU (required for App Store distribution)
auval -v aufx Plug Manu

# Output should end with "PASSED"
```

Fix common AU validation errors:
- **"Could not open component"**: Check bundle ID and AU type
- **"Plugin crash"**: Debug in Xcode, check for exceptions in initialization
- **"Latency reporting"**: Implement `getTailLengthSeconds()` correctly

---

## 3. Windows Builds

### Prerequisites

1. **Visual Studio 2022** (Community, Professional, or Enterprise)
   - Install "Desktop development with C++" workload
   - Includes Windows 10 SDK

2. **CMake** (3.22+)
   ```powershell
   # Via Chocolatey
   choco install cmake

   # Or download from cmake.org
   ```

3. **Code Signing Certificate** (optional, for distribution)
   - EV or standard code signing certificate
   - From vendors: DigiCert, Sectigo, GlobalSign

### Building

```powershell
# Configure for Visual Studio 2022
cmake -B build-win -G "Visual Studio 17 2022" -A x64

# Build Release
cmake --build build-win --config Release --parallel

# Or open in Visual Studio
start build-win/MyPlugin.sln
```

### MSVC Runtime Linking

**Static Runtime** (recommended for plugins):
```cmake
# Statically link MSVC runtime (no DLL dependencies)
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
```

**Dynamic Runtime** (smaller binary, requires MSVC redistributable):
```cmake
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")
```

### Code Signing

#### Manual Signing with signtool
```powershell
# Sign with PFX file
signtool sign /f certificate.pfx /p <password> `
              /tr http://timestamp.digicert.com `
              /td sha256 /fd sha256 `
              MyPlugin.vst3

# Sign with certificate store
signtool sign /n "Your Company Name" `
              /tr http://timestamp.digicert.com `
              /td sha256 /fd sha256 `
              MyPlugin.vst3

# Verify signature
signtool verify /pa /v MyPlugin.vst3
```

#### Automated Signing in CMake
```cmake
if(WIN32 AND CMAKE_BUILD_TYPE STREQUAL "Release")
    find_program(SIGNTOOL_EXECUTABLE signtool
        PATHS "C:/Program Files (x86)/Windows Kits/10/bin/*/x64"
    )

    if(SIGNTOOL_EXECUTABLE)
        add_custom_command(TARGET MyPlugin POST_BUILD
            COMMAND ${SIGNTOOL_EXECUTABLE} sign
                    /f "${CMAKE_SOURCE_DIR}/certificate.pfx"
                    /p "$ENV{CERT_PASSWORD}"
                    /tr http://timestamp.digicert.com
                    /td sha256 /fd sha256
                    $<TARGET_FILE:MyPlugin>
            COMMENT "Code signing ${TARGET}"
        )
    endif()
endif()
```

### Visual Studio Configuration

#### Optimization Settings
```cmake
if(MSVC)
    # Enable whole program optimization (Release)
    target_compile_options(MyPlugin PRIVATE
        $<$<CONFIG:Release>:/GL>  # Whole program optimization
        /MP                        # Multi-processor compilation
    )

    target_link_options(MyPlugin PRIVATE
        $<$<CONFIG:Release>:/LTCG>  # Link-time code generation
    )
endif()
```

#### Suppress Warnings
```cmake
target_compile_definitions(MyPlugin PRIVATE
    _CRT_SECURE_NO_WARNINGS      # Disable CRT security warnings
    NOMINMAX                     # Prevent min/max macros
)
```

---

## 4. Linux Builds

### Prerequisites

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    cmake \
    libasound2-dev \
    libjack-jackd2-dev \
    libfreetype6-dev \
    libx11-dev \
    libxrandr-dev \
    libxinerama-dev \
    libxcursor-dev \
    libgl1-mesa-dev \
    libcurl4-openssl-dev
```

**Fedora/RHEL:**
```bash
sudo dnf install -y \
    gcc-c++ \
    cmake \
    alsa-lib-devel \
    jack-audio-connection-kit-devel \
    freetype-devel \
    libX11-devel \
    libXrandr-devel \
    libXinerama-devel \
    libXcursor-devel \
    mesa-libGL-devel \
    libcurl-devel
```

### Building

```bash
# Configure
cmake -B build-linux -DCMAKE_BUILD_TYPE=Release

# Build
cmake --build build-linux --config Release --parallel

# Install to system (optional)
sudo cmake --install build-linux
```

### Packaging

#### Create .tar.gz
```bash
tar -czf MyPlugin-1.0.0-Linux-x86_64.tar.gz \
    -C build-linux/MyPlugin_artefacts/Release/VST3 \
    MyPlugin.vst3
```

#### Create .deb Package
```bash
# Install packaging tools
sudo apt-get install checkinstall

# Create .deb
sudo checkinstall \
    --pkgname=myplugin \
    --pkgversion=1.0.0 \
    --pkgrelease=1 \
    --pkggroup=sound \
    --maintainer="you@example.com" \
    cmake --install build-linux
```

---

## 5. AAX Format (Pro Tools)

### Prerequisites

1. **AAX SDK** (requires iLok account)
   - Sign up at [developer.avid.com](https://developer.avid.com)
   - Download AAX SDK
   - Extract to `SDKs/AAX/`

2. **PACE Licensing** (for distribution)
   - Create account at [paceap.com](https://www.paceap.com)
   - Use PACE Eden for signing (replaces codesign for AAX)

### CMake Configuration

```cmake
# Set AAX SDK path
juce_set_aax_sdk_path("${CMAKE_CURRENT_SOURCE_DIR}/SDKs/AAX")

# Add AAX to plugin formats
set(PLUGIN_FORMATS VST3 AU AAX Standalone)
```

### Building AAX

```bash
# macOS
cmake -B build-mac -DAAX_SDK_PATH=SDKs/AAX
cmake --build build-mac --config Release

# Windows
cmake -B build-win -DAAX_SDK_PATH=SDKs/AAX
cmake --build build-win --config Release
```

### AAX Signing with PACE Eden

AAX plugins **must** be signed with PACE Eden (not regular codesign).

```bash
# Sign AAX (macOS/Windows)
wraptool sign \
    --account <your-pace-account> \
    --password <password> \
    --signid <signid> \
    --in MyPlugin.aaxplugin \
    --out MyPlugin-signed.aaxplugin

# Verify
wraptool verify --verbose MyPlugin-signed.aaxplugin
```

**Note**: Keep AAX signing credentials secure. Never commit to version control.

---

## 6. Continuous Integration

### GitHub Actions Workflow

**.github/workflows/build.yml:**
```yaml
name: Build Plugin

on: [push, pull_request]

jobs:
  build:
    name: ${{ matrix.name }}
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        include:
          - name: macOS
            os: macos-latest
            cmake_args: -DCMAKE_OSX_ARCHITECTURES="arm64;x86_64"

          - name: Windows
            os: windows-latest
            cmake_args: -G "Visual Studio 17 2022" -A x64

          - name: Linux
            os: ubuntu-latest
            cmake_args: ""

    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          submodules: recursive

      - name: Install Linux dependencies
        if: runner.os == 'Linux'
        run: |
          sudo apt-get update
          sudo apt-get install -y libasound2-dev libjack-jackd2-dev \
              libfreetype6-dev libx11-dev libxrandr-dev libxinerama-dev \
              libxcursor-dev libgl1-mesa-dev

      - name: Configure
        run: cmake -B build ${{ matrix.cmake_args }} -DCMAKE_BUILD_TYPE=Release

      - name: Build
        run: cmake --build build --config Release --parallel

      - name: Test
        run: ctest --test-dir build -C Release --output-on-failure

      - name: Upload Artifacts
        uses: actions/upload-artifact@v3
        with:
          name: ${{ matrix.name }}
          path: |
            build/*_artefacts/Release/VST3/*.vst3
            build/*_artefacts/Release/AU/*.component
```

### Secrets for Code Signing

Store signing credentials in GitHub Secrets:

1. Go to repository **Settings → Secrets → Actions**
2. Add secrets:
   - `MACOS_CERTIFICATE_BASE64`: Base64-encoded .p12 file
   - `MACOS_CERTIFICATE_PASSWORD`: Certificate password
   - `APPLE_ID`: Apple ID for notarization
   - `APPLE_TEAM_ID`: Developer team ID
   - `APPLE_APP_PASSWORD`: App-specific password
   - `WINDOWS_CERTIFICATE_BASE64`: Base64-encoded .pfx file
   - `WINDOWS_CERTIFICATE_PASSWORD`: Certificate password

### Automated Code Signing in CI

**macOS:**
```yaml
- name: Import Certificate
  env:
    CERTIFICATE_BASE64: ${{ secrets.MACOS_CERTIFICATE_BASE64 }}
    CERTIFICATE_PASSWORD: ${{ secrets.MACOS_CERTIFICATE_PASSWORD }}
  run: |
    echo $CERTIFICATE_BASE64 | base64 --decode > certificate.p12
    security create-keychain -p temp build.keychain
    security import certificate.p12 -k build.keychain -P $CERTIFICATE_PASSWORD -T /usr/bin/codesign
    security set-keychain-settings -lut 21600 build.keychain
    security unlock-keychain -p temp build.keychain
    security set-key-partition-list -S apple-tool:,apple:,codesign: -s -k temp build.keychain

- name: Sign and Notarize
  env:
    APPLE_ID: ${{ secrets.APPLE_ID }}
    APPLE_TEAM_ID: ${{ secrets.APPLE_TEAM_ID }}
    APPLE_APP_PASSWORD: ${{ secrets.APPLE_APP_PASSWORD }}
  run: |
    codesign --force --sign "Developer ID Application" --options runtime MyPlugin.vst3
    xcrun notarytool submit MyPlugin.vst3.zip --apple-id $APPLE_ID --team-id $APPLE_TEAM_ID --password $APPLE_APP_PASSWORD --wait
    xcrun stapler staple MyPlugin.vst3
```

**Windows:**
```yaml
- name: Import Certificate
  env:
    CERTIFICATE_BASE64: ${{ secrets.WINDOWS_CERTIFICATE_BASE64 }}
    CERTIFICATE_PASSWORD: ${{ secrets.WINDOWS_CERTIFICATE_PASSWORD }}
  run: |
    [System.Convert]::FromBase64String($env:CERTIFICATE_BASE64) | Set-Content -Path certificate.pfx -Encoding Byte
    certutil -importpfx -p $env:CERTIFICATE_PASSWORD certificate.pfx

- name: Sign Binary
  run: |
    signtool sign /f certificate.pfx /p $env:CERTIFICATE_PASSWORD /tr http://timestamp.digicert.com /td sha256 /fd sha256 MyPlugin.vst3
```

---

## 7. Reproducible Builds

### Deterministic Builds

Ensure builds are reproducible across machines:

1. **Pin JUCE version** (use git submodule or specific release)
   ```bash
   git submodule add https://github.com/juce-framework/JUCE.git
   cd JUCE && git checkout 7.0.9
   ```

2. **Lock dependency versions** (CMake FetchContent)
   ```cmake
   FetchContent_Declare(
       googletest
       GIT_REPOSITORY https://github.com/google/googletest.git
       GIT_TAG v1.14.0  # Specific version
   )
   ```

3. **Document toolchain versions** (README.md)
   ```markdown
   Build Requirements:
   - CMake 3.22+
   - JUCE 7.0.9
   - macOS: Xcode 14.3+
   - Windows: Visual Studio 2022
   - Linux: GCC 11+ or Clang 14+
   ```

4. **Disable timestamp embedding**
   ```cmake
   # Remove __DATE__ and __TIME__ macros
   target_compile_definitions(MyPlugin PRIVATE
       NO_BUILD_TIMESTAMP=1
   )
   ```

### Build Verification

Generate checksums for reproducibility:
```bash
# macOS/Linux
shasum -a 256 MyPlugin.vst3 > checksums.txt

# Windows
certutil -hashfile MyPlugin.vst3 SHA256 >> checksums.txt
```

---

## 8. Troubleshooting

### Common Build Errors

#### "JUCE modules not found"
```
Solution:
git submodule update --init --recursive
```

#### "Symbol not found" (macOS)
```
Solution:
- Check deployment target matches minimum system requirement
- Verify all symbols are available in target SDK
- Use `nm` to inspect missing symbols:
  nm -gU MyPlugin.vst3/Contents/MacOS/MyPlugin | grep <symbol>
```

#### "Unresolved external symbol" (Windows)
```
Solution:
- Ensure all .cpp files are in CMakeLists.txt
- Check library linking order
- Verify static/dynamic runtime consistency (/MT vs /MD)
```

#### "Undefined reference" (Linux)
```
Solution:
- Install missing libraries (libasound2-dev, etc.)
- Add libraries to target_link_libraries()
- Check pkg-config: pkg-config --libs alsa
```

### Plugin Doesn't Load in DAW

**macOS:**
1. Check signing: `codesign --verify --deep --strict MyPlugin.vst3`
2. Verify notarization: `spctl -a -vvv -t install MyPlugin.vst3`
3. Check Gatekeeper: `xattr -l MyPlugin.vst3` (remove quarantine if needed)
4. AU validation: `auval -v aufx Plug Manu`

**Windows:**
1. Check dependencies: Use [Dependency Walker](http://www.dependencywalker.com/)
2. Verify signature: `signtool verify /pa MyPlugin.vst3`
3. Check registry (for VST3): `Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Classes\VST3`

**Linux:**
1. Check shared library dependencies: `ldd MyPlugin.vst3`
2. Verify VST3 path: `~/.vst3/` or `/usr/lib/vst3/`
3. Check permissions: `chmod 755 MyPlugin.vst3`

---

## 9. Best Practices

### Version Management

```cmake
project(MyPlugin VERSION 1.2.3)

# Access in code
target_compile_definitions(MyPlugin PRIVATE
    PLUGIN_VERSION="${CMAKE_PROJECT_VERSION}"
)
```

### Conditional Compilation

```cpp
#if JUCE_MAC
    // macOS-specific code
#elif JUCE_WINDOWS
    // Windows-specific code
#elif JUCE_LINUX
    // Linux-specific code
#endif

#if JUCE_DEBUG
    // Debug-only code
#endif
```

### Minimize Plugin Size

- **Strip symbols** in Release builds
- **Enable LTO** (link-time optimization)
- **Remove unused JUCE modules**
- **Compress resources** (images, fonts)

### Cross-Platform File Paths

```cpp
// Use JUCE File class for portability
juce::File presetFolder = juce::File::getSpecialLocation(
    juce::File::userApplicationDataDirectory
).getChildFile("MyPlugin").getChildFile("Presets");

// Not hardcoded paths like:
// "C:\\Users\\...\\Presets"  ❌
```

---

## Summary

**Key Takeaways:**

1. **Use CMake** for cross-platform builds - single configuration for all platforms
2. **Code signing is essential** for distribution (macOS requires notarization)
3. **Test on all platforms** - behavior can differ (especially AU vs VST3)
4. **Automate in CI/CD** - GitHub Actions, GitLab CI, or Jenkins
5. **Reproducible builds** - pin dependency versions, document toolchain

**Platform Checklist:**

- [ ] macOS: Universal binary (arm64 + x86_64)
- [ ] macOS: Code signed with Developer ID
- [ ] macOS: Notarized (10.15+ requirement)
- [ ] macOS: AU validation passes (`auval`)
- [ ] Windows: Code signed (recommended)
- [ ] Windows: Static runtime linked (/MT)
- [ ] Linux: Dependencies documented
- [ ] All: Tested in major DAWs on each platform

---

**Related Resources:**
- `/release-build` command - Automated release workflow
- BUILD_GUIDE.md - Detailed build procedures
- RELEASE_CHECKLIST.md - Pre-release validation steps
- @build-engineer - CI/CD and build automation expert
