---
name: obs-cross-compiling
description: Cross-compile OBS Studio plugins from Linux to Windows using MinGW, CMake presets, and CI/CD workflows. Covers toolchain files, headers-only linking, OBS SDK fetching, and multi-platform artifact packaging. Use when building OBS plugins for Windows from Linux or setting up CI pipelines.
version: 1.0.0
---

# OBS Cross-Compilation

## Purpose

Cross-compile OBS Studio plugins from Linux to Windows using MinGW-w64. Covers CMake presets, toolchain configuration, headers-only linking, CI/CD workflows, and artifact packaging.

## When NOT to Use

- Native Windows builds with MSVC → Use **obs-windows-building**
- Qt/C++ frontend development → Use **obs-cpp-qt-patterns**
- Audio plugin implementation → Use **obs-audio-plugin-writing**
- Code review → Use **obs-plugin-reviewing**

## Quick Start: Cross-Compile in 5 Steps

### Step 1: Install MinGW on Linux

```bash
# Ubuntu/Debian
sudo apt install mingw-w64 gcc-mingw-w64-x86-64 g++-mingw-w64-x86-64

# Verify
x86_64-w64-mingw32-gcc --version
```

### Step 2: Create Toolchain File

Create `cmake/mingw-w64-toolchain.cmake`:

```cmake
# Target Windows from Linux
set(CMAKE_SYSTEM_NAME Windows)
set(CMAKE_SYSTEM_PROCESSOR x86_64)

# Cross-compilers
set(CMAKE_C_COMPILER x86_64-w64-mingw32-gcc)
set(CMAKE_CXX_COMPILER x86_64-w64-mingw32-g++)
set(CMAKE_RC_COMPILER x86_64-w64-mingw32-windres)

# Target environment (search for libraries here)
set(CMAKE_FIND_ROOT_PATH /usr/x86_64-w64-mingw32)

# Host programs (cmake, etc.) - use from host system
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)

# Target libraries/includes - only search in target environment
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

# Windows flags
set(WIN32 TRUE)
set(MINGW TRUE)
set(CMAKE_SHARED_LIBRARY_SUFFIX ".dll")
set(CMAKE_EXECUTABLE_SUFFIX ".exe")

# Static link C runtime (avoid DLL dependencies)
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -static-libgcc -static-libstdc++")
set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -static-libgcc -static-libstdc++")
set(CMAKE_MODULE_LINKER_FLAGS "${CMAKE_MODULE_LINKER_FLAGS} -static-libgcc -static-libstdc++")

# CRITICAL: Allow unresolved OBS symbols (resolved at runtime)
set(CMAKE_MODULE_LINKER_FLAGS "${CMAKE_MODULE_LINKER_FLAGS} -Wl,--unresolved-symbols=ignore-all,--warn-unresolved-symbols,--noinhibit-exec")
```

### Step 3: Create CMakePresets.json

```json
{
  "version": 8,
  "configurePresets": [
    {
      "name": "linux-cross-windows-x64",
      "displayName": "Cross-compile Windows x64 (from Linux)",
      "description": "Cross-compile for Windows x64 using MinGW-w64 on Linux",
      "binaryDir": "${sourceDir}/build_windows_x64",
      "condition": {
        "type": "equals",
        "lhs": "${hostSystemName}",
        "rhs": "Linux"
      },
      "generator": "Ninja",
      "toolchainFile": "${sourceDir}/cmake/mingw-w64-toolchain.cmake",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "RelWithDebInfo",
        "CROSS_COMPILE_WINDOWS": true
      }
    }
  ],
  "buildPresets": [
    {
      "name": "linux-cross-windows-x64",
      "configurePreset": "linux-cross-windows-x64"
    }
  ]
}
```

### Step 4: Configure Headers-Only Linking

In CMakeLists.txt:

```cmake
option(CROSS_COMPILE_WINDOWS "Cross-compile for Windows from Linux" OFF)

if(CROSS_COMPILE_WINDOWS)
    # Headers only - OBS provides symbols at runtime
    add_library(obs-headers INTERFACE)
    target_include_directories(obs-headers INTERFACE
        "${OBS_SOURCE_DIR}/libobs"
        "${OBS_SOURCE_DIR}/frontend/api"
    )
    target_compile_definitions(obs-headers INTERFACE
        UNICODE _UNICODE _CRT_SECURE_NO_WARNINGS WIN32 _WIN32
    )
    target_link_libraries(${PROJECT_NAME} PRIVATE obs-headers)

    # Windows system libraries
    target_link_libraries(${PROJECT_NAME} PRIVATE ws2_32 comctl32)

    # CRITICAL: Use .def file for exports
    set_target_properties(${PROJECT_NAME} PROPERTIES
        LINK_FLAGS "${CMAKE_CURRENT_SOURCE_DIR}/src/plugin.def -Wl,--unresolved-symbols=ignore-all"
    )
else()
    # Native build - full OBS libraries
    find_package(libobs REQUIRED)
    target_link_libraries(${PROJECT_NAME} PRIVATE OBS::libobs)
endif()
```

### Step 5: Build

```bash
# Fetch OBS SDK headers
./ci/fetch-obs-sdk.sh windows

# Configure
cmake --preset linux-cross-windows-x64 \
    -DOBS_SOURCE_DIR="$PWD/.deps/windows-x64/obs-studio-32.0.4"

# Build
cmake --build --preset linux-cross-windows-x64

# Verify
file build_windows_x64/my-plugin.dll | grep "PE32+"
```

## Headers-Only Linking Pattern

**Why headers-only?** OBS plugins are loaded at runtime by OBS Studio. The plugin doesn't link against libobs.dll - instead:

1. OBS loads the plugin DLL
2. Plugin exports `obs_module_load()` and other functions
3. OBS provides all `obs_*` symbols at load time

**Critical linker flags:**

```cmake
-Wl,--unresolved-symbols=ignore-all   # Don't fail on missing OBS symbols
-Wl,--warn-unresolved-symbols         # Downgrade to warnings
-Wl,--noinhibit-exec                  # Create output despite warnings
```

## Symbol Export with .def File

MinGW sometimes exports functions by ordinal only. OBS requires **named exports**.

Create `src/plugin.def`:

```def
LIBRARY my-plugin
EXPORTS
    ; Required OBS module entry points
    obs_module_load
    obs_module_unload
    obs_module_post_load
    obs_module_ver
    obs_module_set_pointer
    obs_current_module
    obs_module_description

    ; Locale functions (from OBS_MODULE_USE_DEFAULT_LOCALE)
    obs_module_set_locale
    obs_module_free_locale
    obs_module_get_string
    obs_module_text
```

**Verify exports:**

```bash
x86_64-w64-mingw32-objdump -p my-plugin.dll | grep -A 100 "Export Table"
```

## OBS SDK Fetching

For cross-compilation, you need OBS headers (not full libraries).

**Pattern from translate-live:**

```bash
#!/bin/bash
# fetch-obs-sdk.sh

PLATFORM="$1"  # "windows" or "linux"
OBS_VERSION="32.0.4"
OBS_HASH="5e17f2e99..."  # From buildspec.json

# Create deps directory
mkdir -p .deps/${PLATFORM}-x64

# Download OBS source (for headers)
curl -L "https://github.com/obsproject/obs-studio/archive/refs/tags/${OBS_VERSION}.tar.gz" \
    -o obs-studio.tar.gz

# Verify checksum
echo "${OBS_HASH}  obs-studio.tar.gz" | sha256sum -c

# Extract
tar -xzf obs-studio.tar.gz -C .deps/${PLATFORM}-x64

# Create stub obsconfig.h (normally generated by CMake)
cat > .deps/${PLATFORM}-x64/obs-studio-${OBS_VERSION}/libobs/obsconfig.h << 'EOF'
#pragma once
#define OBS_VERSION "32.0.4"
#define OBS_DATA_PATH ""
#define OBS_INSTALL_PREFIX ""
#define OBS_PLUGIN_PATH ""
EOF
```

## CI/CD Workflow

### Gitea Actions / GitHub Actions

```yaml
build-windows:
  name: Build Windows x64 (Cross-compile)
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4

    - name: Install dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y \
          cmake ninja-build jq curl unzip \
          mingw-w64 gcc-mingw-w64-x86-64 g++-mingw-w64-x86-64

    - name: Fetch OBS SDK
      run: ./ci/fetch-obs-sdk.sh windows

    - name: Configure
      run: |
        OBS_VERSION=$(jq -r '.dependencies["obs-studio"].version' buildspec.json)
        cmake --preset linux-cross-windows-ci-x64 \
          -DOBS_SOURCE_DIR="${PWD}/.deps/windows-x64/obs-studio-${OBS_VERSION}"

    - name: Build
      run: cmake --build --preset linux-cross-windows-ci-x64

    - name: Verify DLL
      run: |
        file build_windows_x64/my-plugin.dll | grep "PE32+"
        x86_64-w64-mingw32-objdump -p build_windows_x64/my-plugin.dll | grep -A 100 "Export Table"

    - name: Package
      run: |
        VERSION=$(jq -r '.version' buildspec.json)
        COMMIT=$(git rev-parse --short=9 HEAD)
        ARTIFACT="my-plugin-${VERSION}-windows-x64-${COMMIT}"

        mkdir -p "release/${ARTIFACT}/bin/64bit"
        cp build_windows_x64/my-plugin.dll "release/${ARTIFACT}/bin/64bit/"
        cd release && zip -rq "${ARTIFACT}.zip" "${ARTIFACT}"
```

## Artifact Naming Convention

```
{plugin-name}-{version}-{platform}-{commit}.{ext}
```

**Examples:**

- `my-plugin-1.0.0-linux-x86_64-abc123def.tar.xz`
- `my-plugin-1.0.0-windows-x64-abc123def.zip`

**Structure inside archive:**

```
my-plugin-1.0.0-windows-x64-abc123def/
├── bin/
│   └── 64bit/
│       └── my-plugin.dll
└── data/
    └── locale/
        └── en-US.ini
```

## buildspec.json Pattern

Centralize dependencies and versions:

```json
{
  "name": "my-plugin",
  "displayName": "My OBS Plugin",
  "version": "1.0.0",
  "author": "Your Name",
  "dependencies": {
    "obs-studio": {
      "version": "32.0.4",
      "hashes": {
        "windows-x64": "5e17f2e99213af77ee15c047755ee3e3e88b78e5eee17351c113d79671ffb98b"
      }
    }
  }
}
```

## FORBIDDEN Patterns

| Pattern                  | Problem                       | Solution                             |
| ------------------------ | ----------------------------- | ------------------------------------ |
| Missing toolchain file   | Build uses host compiler      | Always use `-DCMAKE_TOOLCHAIN_FILE`  |
| Linking libobs.a/dll     | Import library not available  | Headers-only + runtime resolution    |
| Missing .def file        | Functions exported by ordinal | Create plugin.def with named exports |
| Missing `-static-libgcc` | Requires MinGW runtime DLLs   | Add to linker flags                  |
| Hardcoded OBS paths      | Breaks on different systems   | Use `OBS_SOURCE_DIR` variable        |
| No checksum verification | Security risk                 | Verify SHA256 of downloaded SDK      |

## Troubleshooting

### DLL has no exports

**Symptom:** Plugin loads but OBS can't find `obs_module_load`

**Cause:** Missing or incorrect .def file

**Fix:**

```bash
# Check exports
x86_64-w64-mingw32-objdump -p my-plugin.dll | grep -A 50 "Export Table"

# Should show named functions, not just ordinals
```

### Undefined reference to OBS functions

**Symptom:** Linker errors about `obs_register_source`, etc.

**Cause:** Missing unresolved-symbols flag

**Fix:** Add to CMakeLists.txt:

```cmake
set_target_properties(${PROJECT_NAME} PROPERTIES
    LINK_FLAGS "-Wl,--unresolved-symbols=ignore-all"
)
```

### Wrong file format

**Symptom:** `file` shows "ELF" instead of "PE32+"

**Cause:** Using host compiler instead of cross-compiler

**Fix:** Ensure toolchain file is loaded:

```bash
cmake -DCMAKE_TOOLCHAIN_FILE=cmake/mingw-w64-toolchain.cmake ..
```

## External Documentation

### Context7 (Real-time docs)

```
mcp__context7__query-docs
libraryId: "/obsproject/obs-studio"
query: "CMake cross-compile Windows Linux plugin"
```

### Official References

- **OBS CMake Guide**: https://docs.obsproject.com/building
- **MinGW Wiki**: https://www.mingw-w64.org/
- **CMake Presets**: https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html

## Related Skills

- **obs-windows-building** - Native Windows builds (MSVC, MinGW)
- **obs-cpp-qt-patterns** - Qt frontend integration
- **obs-plugin-developing** - Plugin architecture overview
- **obs-audio-plugin-writing** - Audio plugin implementation

## Related Agent

Use **obs-plugin-expert** for coordinated guidance across all OBS plugin skills.
