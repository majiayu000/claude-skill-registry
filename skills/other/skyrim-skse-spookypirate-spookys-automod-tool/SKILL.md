---
name: skyrim-skse
description: Create and manage SKSE C++ plugin projects. Use when the user wants to create native plugins, add Papyrus native functions, or extend Skyrim's functionality at the native level.
---

# Skyrim SKSE Module

Create and manage SKSE (Skyrim Script Extender) C++ plugin projects using Spooky's AutoMod Toolkit.

## Prerequisites

Run all commands from the toolkit directory:
```bash
cd "<TOOLKIT_PATH>"
# Example: cd "C:\Tools\spookys-automod-toolkit"
```

### Build Requirements

**IMPORTANT:** Building SKSE plugins requires:

| Tool | Purpose | Installation |
|------|---------|--------------|
| **CMake 3.21+** | Build system | [Download](https://cmake.org/download/) |
| **MSVC Build Tools** | C++ compiler | [MSVC Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022) |
| vcpkg | Dependencies | Auto-bootstrapped by project |

**Note:** You do NOT need the full Visual Studio IDE - only the MSVC Build Tools (C++ compiler). The Build Tools can be installed standalone without Visual Studio.

## Overview

SKSE plugins are DLL files that extend Skyrim's functionality at a native level. This module generates project scaffolding using **CommonLibSSE-NG**, which supports Skyrim SE, AE, GOG, and VR from a single codebase.

## Command Reference

### List Available Templates
```bash
dotnet run --project src/SpookysAutomod.Cli -- skse templates
```

**Available Templates:**
| Template | Description |
|----------|-------------|
| `basic` | Minimal SKSE plugin with logging |
| `papyrus-native` | Plugin with Papyrus native function support |

### Create SKSE Project
```bash
dotnet run --project src/SpookysAutomod.Cli -- skse create "<name>" [options]
```
| Option | Default | Description |
|--------|---------|-------------|
| `--template` | `basic` | Template to use |
| `--output` | `.` | Output directory |
| `--author` | `Unknown` | Author name |
| `--description` | - | Project description |

### Get Project Info
```bash
dotnet run --project src/SpookysAutomod.Cli -- skse info "<path>"
```
| Option | Description |
|--------|-------------|
| `<path>` | Project directory (default: current) |

### Add Papyrus Native Function
```bash
dotnet run --project src/SpookysAutomod.Cli -- skse add-function "<project>" --name "<name>" [options]
```
| Option | Default | Description |
|--------|---------|-------------|
| `--name` | Required | Function name |
| `--return` | `void` | Return type |
| `--param` | - | Parameters (format: `type:name`, repeatable) |

## Common Workflows

### Create Basic SKSE Plugin
```bash
# 1. Create project
dotnet run --project src/SpookysAutomod.Cli -- skse create "MyPlugin" --output "./" --author "YourName"

# 2. Build (requires CMake and MSVC)
cd MyPlugin
cmake -B build -S .
cmake --build build --config Release

# Output: build/Release/MyPlugin.dll
```

### Create Plugin with Papyrus Functions
```bash
# 1. Create project with papyrus-native template
dotnet run --project src/SpookysAutomod.Cli -- skse create "MyNativePlugin" --template papyrus-native --author "YourName" --output "./"

# 2. Add custom functions
dotnet run --project src/SpookysAutomod.Cli -- skse add-function "./MyNativePlugin" --name "GetActorSpeed" --return "Float" --param "Actor:target"

dotnet run --project src/SpookysAutomod.Cli -- skse add-function "./MyNativePlugin" --name "SetActorSpeed" --return "void" --param "Actor:target" --param "Float:speed"

dotnet run --project src/SpookysAutomod.Cli -- skse add-function "./MyNativePlugin" --name "GetPluginVersion" --return "Int"

# 3. Build
cd MyNativePlugin
cmake -B build -S .
cmake --build build --config Release
```

### Check Existing Project
```bash
# Get project info
dotnet run --project src/SpookysAutomod.Cli -- skse info "./MyPlugin"
```

## Papyrus Type Mapping

| Papyrus Type | C++ Type | Notes |
|--------------|----------|-------|
| Int | int | 32-bit integer |
| Float | float | 32-bit float |
| Bool | bool | Boolean |
| String | std::string | Text string |
| Actor | RE::Actor* | Actor reference |
| ObjectReference | RE::TESObjectREFR* | Object reference |
| Form | RE::TESForm* | Any form |

### Function Parameter Format
```
--param "Type:name"
```

Examples:
- `--param "Actor:target"` - Actor parameter named "target"
- `--param "Float:speed"` - Float parameter named "speed"
- `--param "Int:count"` - Integer parameter named "count"
- `--param "String:message"` - String parameter named "message"

## Generated Project Structure

```
MyPlugin/
  CMakeLists.txt          # CMake build configuration
  vcpkg.json              # C++ dependencies
  skse_config.json        # Toolkit configuration
  src/
    main.cpp              # SKSE plugin entry point
    plugin.cpp            # Plugin implementation
    plugin.h              # Plugin header
  cmake/
    CommonLibSSE.cmake    # CommonLibSSE-NG integration
```

## Template Details

### basic Template
Minimal plugin with:
- Modern C++20 plugin metadata (`.RuntimeCompatibility()`)
- Precompiled headers (PCH) for fast builds
- Comprehensive event handler examples (OnHit, OnEquip)
- Safe NiPointer and Actor casting patterns
- Correct form lookup methods (EditorID vs FormID)
- Logging setup
- Message handler for game events

**Modern API Features:**
```cpp
// Modern plugin version declaration
extern "C" __declspec(dllexport) constinit SKSE::PluginVersionData SKSEPlugin_Version = [] {
    SKSE::PluginVersionData data{};
    data.RuntimeCompatibility(SKSE::RuntimeCompatibility::Independent);
    return data;
}();

// Safe NiPointer handling
auto target = event->target.get();  // Get raw pointer
auto actor = target->As<RE::Actor>();  // Safe cast

// Correct form lookup
auto form = RE::TESForm::LookupByEditorID("MyForm"sv);  // By EditorID
auto form = RE::TESForm::LookupByID(0x00012EB7);  // By FormID
```

**Build Options:**
- VCPKG (automatic dependency management)
- Manual vendor/ folder (no VCPKG required)
- Windows CMD build script included (`build.bat`)

### papyrus-native Template
Includes everything in `basic` plus:
- Papyrus native function registration
- Script interface
- Example function

```cpp
// Register functions
bool RegisterFunctions(RE::BSScript::IVirtualMachine* vm) {
    vm->RegisterFunction("MyFunction", "MyScript", MyFunction);
    return true;
}

// Example native function
int MyFunction(RE::StaticFunctionTag*) {
    return 42;
}
```

## Using Native Functions in Papyrus

After building the plugin, call native functions from Papyrus:
```papyrus
ScriptName MyScript

; Declare native functions
Int Function GetPluginVersion() global native
Float Function GetActorSpeed(Actor target) global native
Function SetActorSpeed(Actor target, Float speed) global native

; Usage
Event OnInit()
    Int version = GetPluginVersion()
    Debug.Notification("Plugin version: " + version)

    Actor player = Game.GetPlayer()
    Float speed = GetActorSpeed(player)
    SetActorSpeed(player, speed * 1.5)
EndEvent
```

## CommonLibSSE-NG

This toolkit uses **CommonLibSSE-NG** (Next Generation), which provides:

- **Multi-version support**: Single DLL works on SE, AE, GOG, VR
- **Address independence**: No hardcoded addresses
- **Modern C++**: Uses C++20 features
- **Complete API**: Covers most game functions

### Supported Skyrim Versions
| Version | Support |
|---------|---------|
| Skyrim SE 1.5.x | Full |
| Skyrim SE 1.6.x (AE) | Full |
| Skyrim GOG | Full |
| Skyrim VR | Partial |

## Building Projects

### Standard Build
```bash
cd MyPlugin
cmake -B build -S .
cmake --build build --config Release
```

### Debug Build
```bash
cmake --build build --config Debug
```

### Clean Rebuild
```bash
rm -rf build
cmake -B build -S .
cmake --build build --config Release
```

### Output Location
- Release: `build/Release/MyPlugin.dll`
- Debug: `build/Debug/MyPlugin.dll`

## Installing SKSE Plugins

1. Copy DLL to `Data/SKSE/Plugins/`
2. Copy any config files to same folder
3. Launch game with SKSE loader

## Limitations

This module **CAN**:
- Generate project scaffolding
- Add Papyrus native function stubs
- Manage project configuration

This module **CANNOT**:
- Write custom C++ logic
- Compile projects (requires local build tools)
- Debug plugins
- Generate complex game hooks

For advanced SKSE development:
- [CommonLibSSE-NG Wiki](https://github.com/CharmedBaryon/CommonLibSSE-NG/wiki)
- [SKSE Plugin Development Guide](https://www.creationkit.com/index.php?title=Category:SKSE)

## Important Notes

1. **Build tools required** - CMake and MSVC Build Tools needed (NOT full Visual Studio IDE)
2. **Single codebase, all versions** - CommonLibSSE-NG handles version differences
3. **vcpkg auto-bootstraps** - Dependencies downloaded on first build (~5 minutes first time)
4. **Native functions need matching Papyrus declarations** - Script must declare functions as `native`
5. **Use `--json` flag** for machine-readable output when scripting
6. **LLMs can build plugins** - Use Bash tool to invoke CMake commands for end-to-end workflow

## JSON Output

All commands support `--json` for structured output:
```bash
dotnet run --project src/SpookysAutomod.Cli -- skse info "./MyPlugin" --json
```

Example response:
```json
{
  "success": true,
  "result": {
    "name": "MyPlugin",
    "author": "YourName",
    "version": "1.0.0",
    "template": "papyrus-native",
    "description": "My SKSE Plugin",
    "targetVersions": ["SE", "AE"],
    "papyrusFunctions": [
      {
        "name": "GetActorSpeed",
        "returnType": "Float",
        "parameters": [
          { "type": "Actor", "name": "target" }
        ]
      }
    ]
  }
}
```
