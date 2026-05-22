---
name: PowerShell Core Builder
description: Guide and commands for building PowerShell Core on Windows from source. Use when working in the PowerShell repository.
---

# PowerShell Core Builder Skill

This skill contains the workflows for building PowerShell on Windows targeting .NET Core.

## When to use

Use this skill when:

- You are working in the recursively cloned `PowerShell/PowerShell` repository.
- You need to clean, bootstrap, build, or test the PowerShell source code.
- You encounter build errors related to the PowerShell project.

## Environment Setup

These instructions target Windows 10/Server 2012 R2+ and require:

- **Visual Studio 2019+** (Community edition works)
- **PowerShell Core 6 Beta.9+** (if using VS Code)
- **Git** (configured correctly)

## Build Workflows

### 1. Bootstrapping (Dependencies)

We use the `.NET CLI`. The `Start-PSBootstrap` function installs the correct version defined in `global.json`.

```powershell
Import-Module ./build.psm1
Start-PSBootstrap -Scenario Dotnet
# Or call directly:
# Install-Dotnet
```

### 2. Building the Module

Use the `Start-PSBuild` helper function.

**Standard Build:**

```powershell
Import-Module ./build.psm1
Start-PSBuild -Clean -PSModuleRestore -UseNuGetOrg
```

*Note: `-UseNuGetOrg` is crucial if you don't have access to the private Azure Artifacts feed.*

**Build Output:**
The executable will be located at:
`./src/powershell-win-core/bin/Debug/net6.0/win7-x64/publish/pwsh.exe`

### 3. Testing

Run cross-platform Pester tests.

```powershell
Import-Module ./build.psm1
Start-PSPester -UseNuGetOrg
```

## Debugging

- You can execute the development copy via: `& (Get-PSOutput)`
- Validated on Windows 10 and Windows Server 2012 R2.
