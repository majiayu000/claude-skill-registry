---
name: msvc-build
description: Compile MSVC C++ projects with multi-processor support, automatic MSBuild detection, and intelligent error analysis.
version: 1.0
---

# MSVC Build Skill

Compile and build Microsoft Visual C++ projects using MSBuild with intelligent error detection and resolution suggestions.

## When to Use

Use this skill when you need to:
- Compile C++ projects in Visual Studio solutions (.sln)
- Build individual project files (.vcxproj)
- Debug compilation errors
- Perform incremental or clean builds
- Compile with specific configurations (Debug/Release, Win32/x64)

## Prerequisites

- Visual Studio 2019/2022 installed
- MSBuild available in PATH or at standard location
- Project solution (.sln) or project file (.vcxproj)

## Workflow

### Step 1: Detect Build Environment

Automatically locate MSBuild:
1. Check PATH for `msbuild.exe`
2. Search standard VS2019/2022 installation paths
3. Report MSBuild version and location

### Step 2: Analyze Project Structure

Identify:
- Solution file (.sln) location
- Project dependencies
- Available configurations (Debug/Release)
- Available platforms (Win32/x64)

### Step 3: Execute Build

**Full Solution Build**:
```
MSBuild Solution.sln /p:Configuration=Debug /p:Platform=Win32 /m
```

**Single Project Build**:
```
MSBuild Solution.sln /t:ProjectName /p:Configuration=Debug /p:Platform=Win32 /m
```

**Incremental Build** (faster):
```
MSBuild Project.vcxproj /p:Configuration=Debug /p:Platform=Win32
```

**Clean Build**:
```
MSBuild Solution.sln /t:Clean
MSBuild Solution.sln /p:Configuration=Debug /p:Platform=Win32 /m
```

### Step 4: Error Analysis

Parse MSBuild output and categorize errors:

| Error Type | Pattern | Suggestion |
|------------|---------|------------|
| Missing include | `C1083: Cannot open include file` | Check include paths, verify file exists |
| Undeclared identifier | `C2065: 'X': undeclared identifier` | Check header includes, verify declaration |
| Syntax error | `C2143`, `C2061` | Check syntax, missing semicolons |
| Type undefined | `C2027: use of undefined type` | Forward declaration or missing include |
| Link error | `LNK2019`, `LNK2001` | Check library dependencies, export macros |
| Precompiled header | `C2857`, `C1853` | Ensure `#include "StableHeaders.h"` first |

## Build Commands Reference

### Basic Build

```cmd
# Debug Win32 (most common for development)
MSBuild Project.sln /p:Configuration=Debug /p:Platform=Win32 /m

# Release Win32
MSBuild Project.sln /p:Configuration=Release /p:Platform=Win32 /m

# Debug x64
MSBuild Project.sln /p:Configuration=Debug /p:Platform=x64 /m
```

### Targeted Build

```cmd
# Build specific project only
MSBuild Project.sln /t:WorldServer /p:Configuration=Debug /p:Platform=Win32

# Build multiple specific projects
MSBuild Project.sln /t:LibClient;Network;Common;WorldServer
```

### Verbosity Levels

```cmd
# Quiet - only errors
/v:q

# Minimal - errors and warnings (default)
/v:m

# Normal - standard output
/v:n

# Detailed - verbose output
/v:d

# Diagnostic - maximum detail
/v:diag
```

### Parallel Build

```cmd
# Use all processors (recommended)
/m

# Use specific number of processors
/m:4
```

## Common Issues and Solutions

### Issue 1: MSBuild Not Found

**Error**:
```
The term 'msbuild' is not recognized
```

**Solution**:
- Use Developer Command Prompt for Visual Studio
- Or provide full path to MSBuild:
  - VS2022: `C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\MSBuild.exe`
  - VS2019: `C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\MSBuild\Current\Bin\MSBuild.exe`

### Issue 2: Missing Include Files

**Error**:
```
error C1083: Cannot open include file: 'Serialization/OutStream.h'
```

**Causes**:
- Missing AdditionalIncludeDirectories in .vcxproj
- Using command-line without proper environment setup
- Relative path errors in #include statements

**Solutions**:
1. Use Visual Studio IDE (handles include paths correctly)
2. Ensure Property Sheets (.props) are imported
3. Check AdditionalIncludeDirectories in project settings

### Issue 3: Precompiled Header Errors

**Error**:
```
error C2857: #include statement specified with the /Ycstdafx.h command-line option was not found
```

**Solution**:
- Ensure first line of .cpp file is `#include "StableHeaders.h"` (or project's PCH header)
- Check Precompiled Header settings in project properties

### Issue 4: Link Errors

**Error**:
```
error LNK2019: unresolved external symbol
```

**Solutions**:
- Check Additional Dependencies in Linker settings
- Ensure required .lib files are built
- Verify __declspec(dllexport/dllimport) macros for DLLs

## Integration with VS IDE

### Running from IDE

1. Open `.sln` file in Visual Studio
2. Select configuration from toolbar (Debug/Release, Win32/x64)
3. Build → Build Solution (Ctrl+Shift+B)
4. View errors in Error List window (Ctrl+\, E)

## Best Practices

1. **Always use /m for parallel builds** - Significantly faster on multi-core systems
2. **Start with minimal verbosity** - Use `/v:m`, increase only when debugging
3. **Clean build after major changes** - Delete `Debug/` or `Release/` folders
4. **Build dependencies first** - Core libs → Network → Common → Executables
5. **Check Property Sheets** - Ensure `.props` files are correctly imported

## Safety Notes

- Never modify `.vcxproj` files directly without backups
- Property Sheets (.props) changes affect multiple projects
- Precompiled header changes require full rebuild
- Be cautious with compiler warnings treated as errors

## Example Session

**User**: Compile WorldServer project in Debug Win32

**Agent**:
```
📋 Build Plan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Solution: Project/Server/Project.sln
Target: WorldServer
Configuration: Debug | Win32
Parallel: Yes (/m)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Finding MSBuild...
✓ Found: C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\MSBuild.exe
Version: 17.14.40

Executing build...
MSBuild Project.sln /t:WorldServer /p:Configuration=Debug /p:Platform=Win32 /m /v:minimal

Build Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ LibClient.lib
✓ Network.lib
✓ Database.lib
✓ Common.lib
✓ WorldServer.exe

Build succeeded with 0 errors, 3 warnings
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Limitations

- Cannot fix source code errors automatically
- Cannot modify project dependencies
- Cannot resolve missing third-party libraries
- Large solutions may require IDE for full context

## See Also

- Microsoft MSBuild documentation: https://docs.microsoft.com/visualstudio/msbuild/
