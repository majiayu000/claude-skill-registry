---
name: install-local-tool
version: 1.0.0
date: 2026-01-21
description: Build and install a dotnet tool locally to global tools, handling platform-specific packaging and process cleanup.
canonical_repo: https://github.com/stoicstudio/ClaudeSkills
canonical_path: skills/install-local-tool/SKILL.md
---

# install-local-tool

Builds the current project as a dotnet tool and installs it to the global dotnet tools, replacing any existing version.

> **Canonical Source**: This skill is maintained at [stoicstudio/ClaudeSkills](https://github.com/stoicstudio/ClaudeSkills).
> Run `/update-skill install-local-tool` to update.

## Prerequisites

Before running, ensure:
1. The project is a dotnet tool (`<PackAsTool>true</PackAsTool>` in .csproj)
2. All code changes are complete
3. `dotnet test` passes (if tests exist)
4. Version number has been updated in .csproj or VersionInfo.cs

## Steps

### 1. Locate the Tool Project

Find the main .csproj file that defines the tool:

```bash
# Look for .csproj with PackAsTool in src/ directory
grep -r "<PackAsTool>true</PackAsTool>" src/**/*.csproj
```

Or use the project structure convention: `src/{ProjectName}/{ProjectName}.csproj`

### 2. Extract Tool Configuration from .csproj

Read the .csproj file and extract these properties:

| Property | Purpose | Example |
|----------|---------|---------|
| `ToolCommandName` | CLI command name | `clang-codex` |
| `PackageId` | NuGet package identifier | `clang-codex.mcp` |
| `Version` | Package version | `0.22.4` |

**Detect Platform-Specific Packaging**:

Check if PackageId is conditional on `$(TargetRid)`:
```xml
<!-- Platform-specific pattern -->
<PackageId Condition="'$(TargetRid)' != ''">clang-codex.mcp.$(TargetRid)</PackageId>
<PackageId Condition="'$(TargetRid)' == ''">clang-codex.mcp</PackageId>
```

If this pattern exists, the project requires platform-specific packaging.

### 3. Determine Current Platform RID

If platform-specific packaging is needed, detect the runtime identifier:

```bash
# Windows
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OS" == "Windows_NT" ]]; then
    # Check architecture
    if [[ "$(uname -m)" == "aarch64" || "$PROCESSOR_ARCHITECTURE" == "ARM64" ]]; then
        RID="win-arm64"
    else
        RID="win-x64"
    fi
# Linux
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if [[ "$(uname -m)" == "aarch64" ]]; then
        RID="linux-arm64"
    else
        RID="linux-x64"
    fi
# macOS
elif [[ "$OSTYPE" == "darwin"* ]]; then
    if [[ "$(uname -m)" == "arm64" ]]; then
        RID="osx-arm64"
    else
        RID="osx-x64"
    fi
fi
```

### 4. Construct Package Name

```bash
# If platform-specific
if [[ "$PLATFORM_SPECIFIC" == "true" ]]; then
    PACKAGE_NAME="${BASE_PACKAGE_ID}.${RID}"  # e.g., clang-codex.mcp.win-x64
else
    PACKAGE_NAME="$BASE_PACKAGE_ID"  # e.g., roslyn-codex.mcp
fi
```

### 5. Stop Running Processes

Kill any running instances of the tool to allow file replacement:

```bash
# Get the tool command name from .csproj
TOOL_CMD="clang-codex"  # from ToolCommandName

# Windows (via taskkill)
taskkill /F /IM "${TOOL_CMD}.exe" 2>/dev/null || true

# Linux/macOS (via pkill)
pkill -f "$TOOL_CMD" 2>/dev/null || true
```

**Note**: The process name is typically `{ToolCommandName}.exe` on Windows or just `{ToolCommandName}` on Unix.

### 6. Uninstall Existing Version

```bash
dotnet tool uninstall --global "$PACKAGE_NAME" 2>/dev/null || true
```

The `|| true` ensures the command succeeds even if the tool isn't installed.

### 7. Build and Pack the Tool

```bash
# Navigate to project directory
cd src/{ProjectName}

# Clean previous artifacts
rm -rf bin/Release/*.nupkg

# Build and pack
if [[ "$PLATFORM_SPECIFIC" == "true" ]]; then
    # Platform-specific: pass TargetRid to get correct PackageId
    dotnet pack -c Release -p:TargetRid=$RID
else
    # Standard: no RID needed
    dotnet pack -c Release
fi
```

The .nupkg will be created in `bin/Release/`.

### 8. Install from Local Package

```bash
# Find the generated .nupkg
NUPKG=$(ls bin/Release/*.nupkg | head -1)

# Install globally from local package
dotnet tool install --global --add-source ./bin/Release "$PACKAGE_NAME"
```

### 9. Verify Installation

```bash
# Check installation
dotnet tool list --global | grep "$TOOL_CMD"

# Test the tool
$TOOL_CMD --version 2>/dev/null || $TOOL_CMD --help 2>/dev/null || echo "Tool installed (no --version/--help flag)"
```

### 10. Report Result

Report success with:
- Tool command name
- Package name
- Version installed
- Installation path (from `dotnet tool list --global`)

## Example Output

```
✓ Stopped 2 running instances of clang-codex
✓ Uninstalled clang-codex.mcp.win-x64 (previous version)
✓ Built and packed clang-codex.mcp.win-x64 v0.22.4
✓ Installed globally

Tool: clang-codex
Package: clang-codex.mcp.win-x64
Version: 0.22.4
Path: C:\Users\john\.dotnet\tools\clang-codex.exe
```

## Platform-Specific Projects

Projects that bundle native libraries (like ClangCodex.Mcp with libclang) require platform-specific packaging. Detection:

**Indicators in .csproj**:
- `<TargetRid>` property
- Conditional `<PackageId>` based on `$(TargetRid)`
- `<RuntimeIdentifiers>` listing multiple platforms
- References to `*.runtime.*` native library packages

**Why needed**: Native libraries must match the target platform. A single "any" package cannot contain all platform variants efficiently.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Tool already installed" | Uninstall failed; manually run `dotnet tool uninstall --global {name}` |
| "Process in use" | Close IDE or apps using the tool, or use Task Manager |
| "Package not found" | Check that `dotnet pack` succeeded and .nupkg exists |
| "Version mismatch" | Ensure Version in .csproj matches expected version |
| "Wrong platform" | Verify RID detection matches your actual platform |

## See Also

- [publish-release](../publish-release/SKILL.md) - For publishing to GitHub Packages
- [update-skill](../update-skill/SKILL.md) - Update this skill from canonical repo
