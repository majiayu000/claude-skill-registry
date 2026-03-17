---
name: windows-git-bash-compatibility
description: Windows and Git Bash compatibility guidance for Azure Data Factory development and CI/CD
---

# Windows & Git Bash Compatibility for Azure Data Factory

## Overview

Azure Data Factory development frequently occurs on Windows machines using Git Bash (MINGW64) as the primary shell. This introduces path conversion challenges that can break CI/CD pipelines, npm commands, and deployment scripts.

## Git Bash Path Conversion Behavior

### Automatic Path Conversion

Git Bash (MINGW) automatically converts Unix-style paths to Windows paths:

**Conversions:**
- `/foo` → `C:/Program Files/Git/usr/foo`
- `/foo:/bar` → `C:\msys64\foo;C:\msys64\bar` (path lists)
- `--dir=/foo` → `--dir=C:/msys64/foo` (arguments)

**What Triggers Conversion:**
- Leading forward slash (`/`) in arguments
- Colon-separated path lists
- Arguments after `-` or `,` with path components

**What's Exempt:**
- Arguments containing `=` (variable assignments)
- Drive specifiers (`C:`)
- Arguments with `;` (already Windows format)
- Arguments starting with `//` (Windows switches)

## ADF-Specific Path Issues

### npm Build Commands

**Problem:**
```bash
# This fails in Git Bash due to path conversion
npm run build validate ./adf-resources /subscriptions/abc/resourceGroups/rg/providers/Microsoft.DataFactory/factories/myFactory

# Path gets converted incorrectly
```

**Solution:**
```bash
# Disable path conversion before running
export MSYS_NO_PATHCONV=1
npm run build validate ./adf-resources /subscriptions/abc/resourceGroups/rg/providers/Microsoft.DataFactory/factories/myFactory

# Or wrap the command
MSYS_NO_PATHCONV=1 npm run build export ./adf-resources /subscriptions/.../myFactory "ARMTemplate"
```

### PowerShell Scripts

**Problem:**
```bash
# Calling PowerShell scripts from Git Bash
pwsh ./PrePostDeploymentScript.Ver2.ps1 -armTemplate "./ARMTemplate/ARMTemplateForFactory.json"
# Path conversion may interfere
```

**Solution:**
```bash
# Disable conversion for PowerShell calls
MSYS_NO_PATHCONV=1 pwsh ./PrePostDeploymentScript.Ver2.ps1 -armTemplate "./ARMTemplate/ARMTemplateForFactory.json"
```

### ARM Template Paths

**Problem:**
```bash
# Azure CLI deployment from Git Bash
az deployment group create \
  --resource-group myRG \
  --template-file ARMTemplate/ARMTemplateForFactory.json  # Path may get converted
```

**Solution:**
```bash
# Use relative paths with ./ prefix or absolute Windows paths
export MSYS_NO_PATHCONV=1
az deployment group create \
  --resource-group myRG \
  --template-file ./ARMTemplate/ARMTemplateForFactory.json
```

## Shell Detection Patterns

### Bash Shell Detection

```bash
#!/usr/bin/env bash

# Method 1: Check $MSYSTEM (Git Bash/MSYS2 specific)
if [ -n "$MSYSTEM" ]; then
  echo "Running in Git Bash/MinGW ($MSYSTEM)"
  export MSYS_NO_PATHCONV=1
fi

# Method 2: Check uname -s (more portable)
case "$(uname -s)" in
  MINGW64*|MINGW32*|MSYS*)
    echo "Git Bash detected"
    export MSYS_NO_PATHCONV=1
    ;;
  Linux*)
    if grep -q Microsoft /proc/version 2>/dev/null; then
      echo "WSL detected"
    else
      echo "Native Linux"
    fi
    ;;
  Darwin*)
    echo "macOS"
    ;;
esac

# Method 3: Check $OSTYPE (bash-specific)
case "$OSTYPE" in
  msys*)
    echo "Git Bash/MSYS"
    export MSYS_NO_PATHCONV=1
    ;;
  linux-gnu*)
    echo "Linux"
    ;;
  darwin*)
    echo "macOS"
    ;;
esac
```

### Node.js Shell Detection

```javascript
// detect-shell.js - For use in npm scripts or Node tools
function detectShell() {
  const env = process.env;

  // Git Bash/MinGW (MOST RELIABLE)
  if (env.MSYSTEM) {
    return {
      type: 'mingw',
      subsystem: env.MSYSTEM,  // MINGW64, MINGW32, or MSYS
      needsPathFix: true
    };
  }

  // WSL
  if (env.WSL_DISTRO_NAME) {
    return {
      type: 'wsl',
      distro: env.WSL_DISTRO_NAME,
      needsPathFix: false
    };
  }

  // PowerShell (3+ paths in PSModulePath)
  if (env.PSModulePath?.split(';').length >= 3) {
    return {
      type: 'powershell',
      needsPathFix: false
    };
  }

  // CMD
  if (process.platform === 'win32' && env.PROMPT === '$P$G') {
    return {
      type: 'cmd',
      needsPathFix: false
    };
  }

  // Cygwin
  if (env.TERM === 'cygwin') {
    return {
      type: 'cygwin',
      needsPathFix: true
    };
  }

  // Unix shells
  if (env.SHELL?.includes('bash')) {
    return { type: 'bash', needsPathFix: false };
  }
  if (env.SHELL?.includes('zsh')) {
    return { type: 'zsh', needsPathFix: false };
  }

  return {
    type: 'unknown',
    platform: process.platform,
    needsPathFix: false
  };
}

// Usage
const shell = detectShell();
console.log(`Detected shell: ${shell.type}`);

if (shell.needsPathFix) {
  process.env.MSYS_NO_PATHCONV = '1';
  console.log('Path conversion disabled for Git Bash compatibility');
}

module.exports = { detectShell };
```

### PowerShell Detection

```powershell
# Detect PowerShell edition and version
function Get-ShellInfo {
  $info = @{
    Edition = $PSVersionTable.PSEdition
    Version = $PSVersionTable.PSVersion
    OS = $PSVersionTable.OS
    Platform = $PSVersionTable.Platform
  }

  if ($info.Edition -eq 'Core') {
    Write-Host "PowerShell Core (pwsh) - Cross-platform compatible" -ForegroundColor Green
    $info.CrossPlatform = $true
  } else {
    Write-Host "Windows PowerShell - Windows only" -ForegroundColor Yellow
    $info.CrossPlatform = $false
  }

  return $info
}

$shellInfo = Get-ShellInfo
```

## CI/CD Pipeline Patterns

### Local Development Scripts

**validate-adf.sh** (Git Bash compatible):
```bash
#!/usr/bin/env bash
set -e

# Detect and handle Git Bash
if [ -n "$MSYSTEM" ]; then
  export MSYS_NO_PATHCONV=1
  echo "🔧 Git Bash detected - path conversion disabled"
fi

# Configuration
ADF_ROOT="./adf-resources"
FACTORY_ID="/subscriptions/${AZURE_SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}/providers/Microsoft.DataFactory/factories/${FACTORY_NAME}"

# Validate ADF resources
echo "📋 Validating ADF resources..."
npm run build validate "$ADF_ROOT" "$FACTORY_ID"

# Generate ARM templates
echo "📦 Generating ARM templates..."
npm run build export "$ADF_ROOT" "$FACTORY_ID" "ARMTemplate"

echo "✅ Validation complete"
```

**deploy-adf.sh** (Cross-platform):
```bash
#!/usr/bin/env bash
set -e

# Detect shell
detect_shell() {
  if [ -n "$MSYSTEM" ]; then echo "git-bash"
  elif [ -n "$WSL_DISTRO_NAME" ]; then echo "wsl"
  elif [[ "$OSTYPE" == "darwin"* ]]; then echo "macos"
  else echo "linux"
  fi
}

SHELL_TYPE=$(detect_shell)
echo "🖥️  Detected shell: $SHELL_TYPE"

# Handle Git Bash
if [ "$SHELL_TYPE" = "git-bash" ]; then
  export MSYS_NO_PATHCONV=1
fi

# Download PrePostDeploymentScript
curl -sLo PrePostDeploymentScript.Ver2.ps1 \
  https://raw.githubusercontent.com/Azure/Azure-DataFactory/main/SamplesV2/ContinuousIntegrationAndDelivery/PrePostDeploymentScript.Ver2.ps1

# Stop triggers
echo "⏸️  Stopping triggers..."
MSYS_NO_PATHCONV=1 pwsh ./PrePostDeploymentScript.Ver2.ps1 \
  -armTemplate "./ARMTemplate/ARMTemplateForFactory.json" \
  -ResourceGroupName "$RESOURCE_GROUP" \
  -DataFactoryName "$FACTORY_NAME" \
  -predeployment $true \
  -deleteDeployment $false

# Deploy ARM template
echo "🚀 Deploying ARM template..."
az deployment group create \
  --resource-group "$RESOURCE_GROUP" \
  --template-file ./ARMTemplate/ARMTemplateForFactory.json \
  --parameters ./ARMTemplate/ARMTemplateParametersForFactory.json \
  --parameters factoryName="$FACTORY_NAME"

# Start triggers
echo "▶️  Starting triggers..."
MSYS_NO_PATHCONV=1 pwsh ./PrePostDeploymentScript.Ver2.ps1 \
  -armTemplate "./ARMTemplate/ARMTemplateForFactory.json" \
  -ResourceGroupName "$RESOURCE_GROUP" \
  -DataFactoryName "$FACTORY_NAME" \
  -predeployment $false \
  -deleteDeployment $true

echo "✅ Deployment complete"
```

### package.json with Shell Detection

```json
{
  "scripts": {
    "prevalidate": "node scripts/detect-shell.js",
    "validate": "node node_modules/@microsoft/azure-data-factory-utilities/lib/index validate",
    "prebuild": "node scripts/detect-shell.js",
    "build": "node node_modules/@microsoft/azure-data-factory-utilities/lib/index export"
  },
  "dependencies": {
    "@microsoft/azure-data-factory-utilities": "^1.0.3"
  }
}
```

**scripts/detect-shell.js**:
```javascript
const detectShell = () => {
  if (process.env.MSYSTEM) {
    console.log('🔧 Git Bash detected - disabling path conversion');
    process.env.MSYS_NO_PATHCONV = '1';
    return 'git-bash';
  }
  console.log(`🖥️  Shell: ${process.platform}`);
  return process.platform;
};

detectShell();
```

## Common Issues and Solutions

### Issue 1: npm build validate fails with "Resource not found"

**Symptom:**
```bash
npm run build validate ./adf-resources /subscriptions/abc/...
# Error: Resource '/subscriptions/C:/Program Files/Git/subscriptions/abc/...' not found
```

**Cause:** Git Bash converted the factory ID path

**Solution:**
```bash
export MSYS_NO_PATHCONV=1
npm run build validate ./adf-resources /subscriptions/abc/...
```

### Issue 2: PowerShell script paths incorrect

**Symptom:**
```bash
pwsh PrePostDeploymentScript.Ver2.ps1 -armTemplate "./ARM/template.json"
# Error: Cannot find path 'C:/Program Files/Git/ARM/template.json'
```

**Cause:** Git Bash converted the ARM template path

**Solution:**
```bash
MSYS_NO_PATHCONV=1 pwsh PrePostDeploymentScript.Ver2.ps1 -armTemplate "./ARM/template.json"
```

### Issue 3: Azure CLI template-file parameter fails

**Symptom:**
```bash
az deployment group create --template-file ./ARMTemplate/file.json
# Error: Template file not found
```

**Cause:** Path conversion interfering with Azure CLI

**Solution:**
```bash
export MSYS_NO_PATHCONV=1
az deployment group create --template-file ./ARMTemplate/file.json
```

## Best Practices

### 1. Set MSYS_NO_PATHCONV in .bashrc

```bash
# Add to ~/.bashrc for Git Bash
if [ -n "$MSYSTEM" ]; then
  export MSYS_NO_PATHCONV=1
fi
```

### 2. Create Wrapper Scripts

```bash
# adf-cli.sh - Wrapper for ADF npm commands
#!/usr/bin/env bash
export MSYS_NO_PATHCONV=1
npm run build "$@"
```

### 3. Use Relative Paths with ./

```bash
# Prefer this (less likely to trigger conversion)
./ARMTemplate/ARMTemplateForFactory.json

# Over this
ARMTemplate/ARMTemplateForFactory.json
```

### 4. Document Shell Requirements

```markdown
# README.md

## Development Environment

### Windows Users
- Use Git Bash or PowerShell Core (pwsh)
- Git Bash users: Add `export MSYS_NO_PATHCONV=1` to .bashrc
- Alternative: Use WSL2 for native Linux environment
```

### 5. Test on Multiple Shells

```bash
# Test matrix for Windows developers
- Git Bash (MINGW64)
- PowerShell Core 7+
- WSL2 (Ubuntu/Debian)
- cmd.exe (if applicable)
```

## Quick Reference

| Environment Variable | Purpose | Value |
|---------------------|---------|-------|
| `MSYS_NO_PATHCONV` | Disable all path conversion (Git for Windows) | `1` |
| `MSYS2_ARG_CONV_EXCL` | Exclude specific arguments from conversion (MSYS2) | `*` or patterns |
| `MSYSTEM` | Current MSYS subsystem | `MINGW64`, `MINGW32`, `MSYS` |
| `WSL_DISTRO_NAME` | WSL distribution name | `Ubuntu`, `Debian`, etc. |

## Resources

- [Git for Windows Path Conversion](https://github.com/git-for-windows/git/wiki/FAQ#path-conversion)
- [MSYS2 Path Conversion](https://www.msys2.org/docs/filesystem-paths/)
- [Azure CLI on Windows](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows)
- [PowerShell Core](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell)

## Summary

**Key Takeaways:**
1. Git Bash automatically converts Unix-style paths to Windows paths
2. Use `export MSYS_NO_PATHCONV=1` to disable conversion
3. Detect shell environment using `$MSYSTEM` variable
4. Test CI/CD scripts on all shells used by your team
5. Use PowerShell Core (pwsh) for cross-platform scripts
6. Add shell detection to local development scripts
