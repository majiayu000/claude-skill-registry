---
name: psake
description: PowerShell build automation tool for creating task-based build scripts. Use when Claude needs to create, modify, or troubleshoot psake build scripts (psakefile.ps1), automate builds for .NET/Node.js/Docker projects, set up CI/CD pipelines with psake (GitHub Actions, Azure Pipelines, GitLab CI), or work with PowerShell-based build automation. Triggers include mentions of psake, psakefile, PowerShell build scripts, Invoke-psake, or build task dependencies.
---

# psake Build Automation

psake is a PowerShell build automation tool using a DSL for task-based builds with dependencies.

## Decision Tree

**What kind of build are you creating?**

1. **PowerShell module** → Use PowerShellBuild module (see references/powershell-modules.md)
2. **.NET/Node.js/Docker** → See references/build-types.md
3. **Simple custom build** → Continue below for core psake patterns

**Build complexity?**

- **Simple** (< 5 tasks, single project) → Use patterns in this file
- **Complex** (CI/CD, multiple environments, dynamic tasks) → See references/advanced.md

## Quick Start

```powershell
# Install
Install-Module -Name psake -Scope CurrentUser -Force

# Run
Invoke-psake                              # Run 'Default' task
Invoke-psake -taskList Build, Test        # Run specific tasks
Invoke-psake -docs                        # Show task documentation
```

## Minimal psakefile.ps1

```powershell
Properties {
    $BuildDir = Join-Path $PSScriptRoot 'build'
}

Task Default -depends Build

Task Clean {
    if (Test-Path $BuildDir) { Remove-Item $BuildDir -Recurse -Force }
    New-Item -ItemType Directory -Path $BuildDir -Force | Out-Null
}

Task Build -depends Clean {
    exec { dotnet build -o $BuildDir }
}

Task Test -depends Build {
    exec { dotnet test }
}
```

## Core Commands

### Task

```powershell
Task <name> [-depends <tasks>] [-precondition <scriptblock>] [-description <string>] { <action> }
```

```powershell
Task Deploy -depends Build -precondition { $env:CI -eq 'true' } -description "Deploy to prod" {
    exec { ./deploy.ps1 }
}
```

### Properties

Variables that can be overridden via `-properties` parameter:

```powershell
Properties {
    $Configuration = 'Release'
    $Version = '1.0.0'
}
```

Override: `Invoke-psake -properties @{ Configuration = 'Debug' }`

### exec

Runs external commands, fails build on non-zero exit:

```powershell
exec { dotnet build }                                    # Basic
exec { npm install } "npm install failed"                # Custom error
exec { nuget restore } -maxRetries 3                     # Retry flaky ops
exec { npm test } -workingDirectory './frontend'         # Different directory
```

### Assert

```powershell
Assert (Test-Path $SrcDir) "Source directory not found"
Assert (-not [string]::IsNullOrEmpty($ApiKey)) "API key required"
```

### Include

```powershell
Include "./shared/common-tasks.ps1"
```

### FormatTaskName

```powershell
FormatTaskName "▶ {0}"
# Or with scriptblock:
FormatTaskName { param($taskName) Write-Host "[$taskName]" -ForegroundColor Cyan }
```

### TaskSetup / TaskTearDown

```powershell
TaskSetup { Write-Host "Starting: $($psake.context.currentTaskName)" }
TaskTearDown { Write-Host "Finished: $($psake.context.currentTaskName)" }
```

## Invoke-psake Parameters

| Parameter | Description |
|-----------|-------------|
| `-buildFile` | Path to build script (default: psakefile.ps1) |
| `-taskList` | Tasks to execute (default: 'Default') |
| `-parameters` | Hashtable passed to build script (set before Properties) |
| `-properties` | Hashtable to override Properties block (set after Properties) |
| `-docs` | Display task documentation |
| `-nologo` | Suppress banner |

## Common Patterns

### Conditional Execution

```powershell
Task Deploy -precondition { $env:GITHUB_REF -eq 'refs/heads/main' } {
    # Only runs on main branch
}
```

### Environment-Specific

```powershell
Properties {
    $Env = if ($env:ENVIRONMENT) { $env:ENVIRONMENT } else { 'Development' }
}

Task Deploy {
    switch ($Env) {
        'Production' { exec { ./deploy-prod.ps1 } }
        default      { Write-Host "Skipping deploy for $Env" }
    }
}
```

### Multi-Project

```powershell
Task BuildAll -depends BuildBackend, BuildFrontend

Task BuildBackend {
    Push-Location ./backend
    try { exec { dotnet build } }
    finally { Pop-Location }
}

Task BuildFrontend {
    Push-Location ./frontend
    try { exec { npm run build } }
    finally { Pop-Location }
}
```

### Variable Scoping Between Tasks

Tasks don't share local variables. Use `$script:` scope to pass data between dependent tasks:

```powershell
Task GetFiles {
    $script:Files = Get-ChildItem -Path $SrcDir -Filter *.ps1
}

Task ProcessFiles -depends GetFiles {
    foreach ($file in $script:Files) {
        # Process each file
    }
}
```

> **Note:** psake tasks don't have return values. `$script:` scoped variables are the recommended approach for task-to-task data sharing.

### File Management

psake works for any automation, not just builds:

```powershell
Task CleanTempFiles {
    $cutoff = (Get-Date).AddDays(-30)
    Get-ChildItem -Path $TempDir -File |
        Where-Object { $_.LastWriteTime -lt $cutoff } |
        Remove-Item -Force
}
```

### Console Output Formatting

For reporting-style tasks:

```powershell
Task Report {
    Write-Host "Processing: " -NoNewline
    Write-Host $item.Name -ForegroundColor Cyan
    
    $results | Format-Table Name, Size, Age -AutoSize
}
```

## Validating a psakefile

After generating a psakefile, always validate it.

### Syntax Check

```powershell
# Parse without executing - returns errors if invalid
$file = 'psakefile.ps1'
$errors = $null
$null = [System.Management.Automation.Language.Parser]::ParseFile(
    (Resolve-Path $file),
    [ref]$null,
    [ref]$errors
)
if ($errors) {
    $errors | ForEach-Object { Write-Error $_.ToString() }
} else {
    Write-Host "✓ Syntax valid" -ForegroundColor Green
}
```

### Structure Check

Verify the psakefile uses correct psake functions:

```powershell
$content = Get-Content 'psakefile.ps1' -Raw

# Required elements
$checks = @(
    @{ Name = 'Task definitions'; Pattern = 'Task\s+\w+' }
    @{ Name = 'Properties block'; Pattern = 'Properties\s*\{' }
    @{ Name = 'exec for external commands'; Pattern = 'exec\s*\{' }
)

foreach ($check in $checks) {
    if ($content -match $check.Pattern) {
        Write-Host "✓ $($check.Name)" -ForegroundColor Green
    } else {
        Write-Host "✗ $($check.Name) - not found" -ForegroundColor Yellow
    }
}
```

### Quick Validation One-Liner

```powershell
pwsh -NoProfile -Command "$e=$null;[void][System.Management.Automation.Language.Parser]::ParseFile('psakefile.ps1',[ref]$null,[ref]$e);if($e){$e}else{'Valid'}"
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Build fails but CI shows success | Use `exec { }` for all external commands |
| Cross-platform path issues | Use `Join-Path` instead of `\` or `/` |
| Module not found in CI | `Install-Module -Name psake -Scope CurrentUser -Force` |
| Properties not overriding | Use `-properties` (not `-parameters`) to override Properties block |
| Variable undefined in dependent task | Use `$script:VarName` to share data between tasks |

## References

- **references/powershell-modules.md** - PowerShellBuild module for PS module development
- **references/build-types.md** - .NET, Node.js, Docker build patterns
- **references/advanced.md** - Dynamic tasks, custom logging, CI/CD integration
