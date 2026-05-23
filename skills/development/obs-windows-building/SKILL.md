---
name: obs-windows-building
description: Build OBS Studio plugins for Windows using MSVC or MinGW. Covers Visual Studio setup, .def file exports, Windows linking (ws2_32, comctl32), platform-specific sources, and DLL verification. Use when building OBS plugins natively on Windows or troubleshooting Windows builds.
version: 1.0.0
---

# OBS Windows Building

## Purpose

Build OBS Studio plugins for Windows using MSVC (Visual Studio) or MinGW. Covers symbol exports, Windows-specific linking, platform source files, and DLL verification.

## When NOT to Use

- Cross-compiling from Linux → Use **obs-cross-compiling**
- Qt/C++ frontend development → Use **obs-cpp-qt-patterns**
- Audio plugin implementation → Use **obs-audio-plugin-writing**
- Code review → Use **obs-plugin-reviewing**

## Quick Start: Windows Build in 4 Steps

### Step 1: Install Prerequisites

**Visual Studio 2022:**
- Workload: "Desktop development with C++"
- Individual components: CMake, Windows SDK

**Or MinGW (via MSYS2):**

```bash
pacman -S mingw-w64-x86_64-gcc mingw-w64-x86_64-cmake
```

### Step 2: Create Windows CMake Preset

```json
{
  "name": "windows-x64",
  "displayName": "Windows x64",
  "description": "Build for Windows x64 with Visual Studio",
  "binaryDir": "${sourceDir}/build_x64",
  "generator": "Visual Studio 17 2022",
  "architecture": "x64",
  "cacheVariables": {
    "OBS_SOURCE_DIR": "${sourceDir}/.deps/windows-x64/obs-studio-32.0.4"
  }
}
```

### Step 3: Create .def Export File

Create `src/plugin.def`:

```def
LIBRARY my-plugin
EXPORTS
    obs_module_load
    obs_module_unload
    obs_module_post_load
    obs_module_ver
    obs_module_set_pointer
    obs_current_module
    obs_module_description
    obs_module_set_locale
    obs_module_free_locale
    obs_module_get_string
    obs_module_text
```

### Step 4: Configure CMakeLists.txt

```cmake
if(WIN32)
    # Windows system libraries
    target_link_libraries(${PROJECT_NAME} PRIVATE ws2_32 comctl32)

    # Export module functions via .def file
    if(CMAKE_C_COMPILER_ID STREQUAL "GNU")
        # MinGW
        set_target_properties(${PROJECT_NAME} PROPERTIES
            LINK_FLAGS "${CMAKE_CURRENT_SOURCE_DIR}/src/plugin.def -Wl,--unresolved-symbols=ignore-all"
        )
    else()
        # MSVC
        set_target_properties(${PROJECT_NAME} PROPERTIES
            LINK_FLAGS "/DEF:${CMAKE_CURRENT_SOURCE_DIR}/src/plugin.def"
        )
    endif()
endif()
```

## MSVC vs MinGW Comparison

| Aspect | MSVC | MinGW |
|--------|------|-------|
| IDE | Visual Studio | VS Code, CLion |
| Debugging | Full VS debugger | GDB |
| Build speed | Slower | Faster |
| ABI | Native Windows | GCC-based |
| Qt compat | Requires MSVC Qt | Works with MinGW Qt |
| CI/CD | Windows runner | Linux cross-compile |

**Recommendation:** Use MSVC for native Windows development, MinGW for CI cross-compilation.

## Symbol Export with .def Files

### Why .def Files?

OBS loads plugins at runtime and looks up functions **by name**. Without explicit exports:
- MSVC may not export functions without `__declspec(dllexport)`
- MinGW may export by ordinal only (numbers, not names)

### .def File Format

```def
; Comments start with semicolon
LIBRARY my-plugin        ; DLL name
EXPORTS
    obs_module_load      ; Function to export
    obs_module_unload
    ; Add all OBS_DECLARE_MODULE() and OBS_MODULE_USE_DEFAULT_LOCALE() functions
```

### MSVC Linker Flag

```cmake
set_target_properties(${PROJECT_NAME} PROPERTIES
    LINK_FLAGS "/DEF:${CMAKE_CURRENT_SOURCE_DIR}/src/plugin.def"
)
```

### MinGW Linker Flag

```cmake
set_target_properties(${PROJECT_NAME} PROPERTIES
    LINK_FLAGS "${CMAKE_CURRENT_SOURCE_DIR}/src/plugin.def -Wl,--unresolved-symbols=ignore-all"
)
```

## Windows System Libraries

### Common Libraries

| Library | Purpose | Header |
|---------|---------|--------|
| `ws2_32` | Windows Sockets 2 (networking) | `<winsock2.h>` |
| `comctl32` | Common controls (UI widgets) | `<commctrl.h>` |
| `user32` | Windows API (windows, messages) | `<windows.h>` |
| `kernel32` | Core Windows API | `<windows.h>` |
| `ole32` | COM support | `<objbase.h>` |
| `uuid` | GUID/UUID support | `<guiddef.h>` |

### CMake Linking

```cmake
if(WIN32)
    target_link_libraries(${PROJECT_NAME} PRIVATE
        ws2_32      # Sockets
        comctl32    # UI controls
    )
endif()
```

### Include Order (CRITICAL)

```c
/* WRONG - will cause compile errors */
#include <windows.h>
#include <winsock2.h>

/* CORRECT - winsock2.h must come first */
#include <winsock2.h>
#include <windows.h>
```

## Platform-Specific Source Files

### Directory Structure

```
src/
├── plugin-main.c           # Cross-platform
├── my-source.c             # Cross-platform
└── platform/
    ├── socket-posix.c      # Linux/macOS
    └── socket-win32.c      # Windows
```

### CMakeLists.txt Pattern

```cmake
# Common sources
target_sources(${PROJECT_NAME} PRIVATE
    src/plugin-main.c
    src/my-source.c
)

# Platform-specific sources
if(WIN32)
    target_sources(${PROJECT_NAME} PRIVATE
        src/platform/socket-win32.c
    )
else()
    target_sources(${PROJECT_NAME} PRIVATE
        src/platform/socket-posix.c
    )
endif()
```

### Platform Header Pattern

```c
/* platform.h - Platform abstraction */
#pragma once

#ifdef _WIN32
    #include "platform/socket-win32.h"
#else
    #include "platform/socket-posix.h"
#endif

/* Common interface */
int platform_socket_init(void);
void platform_socket_cleanup(void);
int platform_socket_send(const char *host, int port, const void *data, size_t len);
```

## Windows-Specific Code Patterns

### Winsock Initialization

```c
/* socket-win32.c */
#include <winsock2.h>
#include <ws2tcpip.h>

static bool winsock_initialized = false;

int platform_socket_init(void)
{
    WSADATA wsa_data;
    int result = WSAStartup(MAKEWORD(2, 2), &wsa_data);
    if (result != 0) {
        return -1;
    }
    winsock_initialized = true;
    return 0;
}

void platform_socket_cleanup(void)
{
    if (winsock_initialized) {
        WSACleanup();
        winsock_initialized = false;
    }
}
```

### Windows API Loader Pattern

For optional Windows APIs (not always available):

```c
/* api-loader.c */
#include <windows.h>

typedef BOOL (WINAPI *SetProcessDpiAwarenessContext_t)(DPI_AWARENESS_CONTEXT);

static SetProcessDpiAwarenessContext_t pSetProcessDpiAwarenessContext = NULL;

void load_optional_apis(void)
{
    HMODULE user32 = GetModuleHandleW(L"user32.dll");
    if (user32) {
        pSetProcessDpiAwarenessContext = (SetProcessDpiAwarenessContext_t)
            GetProcAddress(user32, "SetProcessDpiAwarenessContext");
    }
}

void set_dpi_awareness(void)
{
    if (pSetProcessDpiAwarenessContext) {
        pSetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2);
    }
}
```

## OBS Plugin Installation Paths

### User Installation (Recommended)

```
%APPDATA%\obs-studio\plugins\my-plugin\
├── bin\
│   └── 64bit\
│       └── my-plugin.dll
└── data\
    └── locale\
        └── en-US.ini
```

### System Installation

```
C:\ProgramData\obs-studio\plugins\my-plugin\
├── bin\
│   └── 64bit\
│       └── my-plugin.dll
└── data\
    └── locale\
        └── en-US.ini
```

### CMake Install Target

```cmake
if(WIN32)
    set(OBS_PLUGIN_DIR "$ENV{APPDATA}/obs-studio/plugins/${PROJECT_NAME}")
endif()

install(TARGETS ${PROJECT_NAME}
    RUNTIME DESTINATION ${OBS_PLUGIN_DIR}/bin/64bit
)

install(DIRECTORY data/locale
    DESTINATION ${OBS_PLUGIN_DIR}/data
)
```

## DLL Verification

### Check File Type

```cmd
:: PowerShell
Get-Item my-plugin.dll | Select-Object Name, Length
```

### Check Exports with dumpbin (MSVC)

```cmd
dumpbin /exports my-plugin.dll
```

**Expected output:**

```
    ordinal hint RVA      name
          1    0 00001000 obs_current_module
          2    1 00001010 obs_module_description
          3    2 00001020 obs_module_load
          ...
```

### Check Exports with objdump (MinGW)

```bash
x86_64-w64-mingw32-objdump -p my-plugin.dll | grep -A 50 "Export Table"
```

## FORBIDDEN Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| Missing .def file | Functions not exported by name | Create plugin.def |
| Wrong include order | winsock2 errors | Include winsock2.h before windows.h |
| Missing WSAStartup | Socket functions fail | Call platform_socket_init() |
| Hardcoded paths | Breaks on other machines | Use %APPDATA% or relative paths |
| ANSI APIs | Unicode issues | Use wide (W) APIs or UTF-8 |
| Missing /DEF linker flag | No exports in DLL | Add LINK_FLAGS in CMake |

## Troubleshooting

### Plugin Not Visible in OBS

**Check:**
1. DLL is in `bin/64bit/` subdirectory
2. Path is correct: `%APPDATA%\obs-studio\plugins\{name}\bin\64bit\`
3. DLL exports are present: `dumpbin /exports my-plugin.dll`

### "Entry Point Not Found" Error

**Cause:** Missing `obs_module_load` export

**Fix:** Ensure .def file includes `obs_module_load` and linker flag is set.

### Winsock Errors

**Symptom:** Socket functions return -1 or WSANOTINITIALISED

**Fix:** Call `WSAStartup()` before any socket operations.

### Unicode/ANSI Mismatch

**Symptom:** String corruption, "???" characters

**Fix:**
```c
/* Use wide APIs or define UNICODE */
#define UNICODE
#define _UNICODE
#include <windows.h>
```

## Build Commands

### Visual Studio

```cmd
:: Configure
cmake --preset windows-x64

:: Build
cmake --build --preset windows-x64 --config RelWithDebInfo

:: Install
cmake --install build_x64 --config RelWithDebInfo
```

### MinGW (MSYS2)

```bash
# Configure
cmake -G "Ninja" -B build -DCMAKE_BUILD_TYPE=RelWithDebInfo

# Build
cmake --build build

# Install
cmake --install build
```

## External Documentation

### Context7

```
mcp__context7__query-docs
libraryId: "/obsproject/obs-studio"
query: "Windows plugin build Visual Studio MSVC"
```

### Official References

- **OBS Windows Build**: https://obsproject.com/wiki/Building-OBS-Studio
- **Visual Studio Docs**: https://docs.microsoft.com/en-us/visualstudio/
- **Windows SDK**: https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/

## Related Skills

- **obs-cross-compiling** - Cross-compile from Linux to Windows
- **obs-cpp-qt-patterns** - Qt frontend integration
- **obs-plugin-developing** - Plugin architecture overview
- **obs-audio-plugin-writing** - Audio plugin implementation

## Related Agent

Use **obs-plugin-expert** for coordinated guidance across all OBS plugin skills.
