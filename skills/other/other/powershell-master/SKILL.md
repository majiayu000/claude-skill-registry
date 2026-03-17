---
name: powershell-master
description: "Complete PowerShell expertise system across ALL platforms (Windows/Linux/macOS). PROACTIVELY activate for: (1) ANY PowerShell task (scripts/modules/cmdlets), (2) CI/CD automation (GitHub Actions/Azure DevOps/Bitbucket), (3) Cross-platform scripting, (4) Module discovery and management (PSGallery), (5) Azure/AWS/Microsoft 365 automation, (6) Script debugging and optimization, (7) Best practices and security. Provides: PowerShell 7+ features, popular module expertise (Az, Microsoft.Graph, PnP, AWS Tools), PSGallery integration, platform-specific guidance, CI/CD pipeline patterns, cmdlet syntax mastery, and production-ready scripting patterns. Ensures professional-grade, cross-platform PowerShell automation following industry standards."
---

# PowerShell Master

## 🚨 CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

**Examples:**
- ❌ WRONG: `D:/repos/project/file.tsx`
- ✅ CORRECT: `D:\repos\project\file.tsx`

This applies to:
- Edit tool file_path parameter
- Write tool file_path parameter
- All file operations on Windows systems

### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

- **Priority**: Update existing README.md files rather than creating new documentation
- **Repository cleanliness**: Keep repository root clean - only README.md unless user requests otherwise
- **Style**: Documentation should be concise, direct, and professional - avoid AI-generated tone
- **User preference**: Only create additional .md files when user specifically asks for documentation



---

Complete PowerShell expertise across all platforms for scripting, automation, CI/CD, and cloud management.

---

## 🎯 When to Activate

PROACTIVELY activate for ANY PowerShell-related task:

- ✅ **PowerShell Scripts** - Creating, reviewing, optimizing any .ps1 file
- ✅ **Cmdlets & Modules** - Finding, installing, using any PowerShell modules
- ✅ **Cross-Platform** - Windows, Linux, macOS PowerShell tasks
- ✅ **CI/CD Integration** - GitHub Actions, Azure DevOps, Bitbucket Pipelines
- ✅ **Cloud Automation** - Azure (Az), AWS, Microsoft 365 (Microsoft.Graph)
- ✅ **Module Management** - PSGallery search, installation, updates
- ✅ **Script Debugging** - Troubleshooting, performance, security
- ✅ **Best Practices** - Code quality, standards, production-ready scripts

---

## 📋 PowerShell Overview

### PowerShell Versions & Platforms

**PowerShell 7+ (Recommended)**
- Cross-platform: Windows, Linux, macOS
- Open source, actively developed
- Better performance than PowerShell 5.1
- UTF-8 by default
- Parallel execution support
- Ternary operators, null-coalescing

**Windows PowerShell 5.1 (Legacy)**
- Windows-only
- Ships with Windows
- UTF-16LE default encoding
- Required for some Windows-specific modules

**Installation Locations:**
- **Windows:** `C:\Program Files\PowerShell\7\` (PS7) or `C:\Windows\System32\WindowsPowerShell\v1.0\` (5.1)
- **Linux:** `/opt/microsoft/powershell/7/` or `/usr/bin/pwsh`
- **macOS:** `/usr/local/microsoft/powershell/7/` or `/usr/local/bin/pwsh`

---

## 🔧 Cross-Platform Best Practices

### 1. Path Handling

**DO:**
```powershell
# Use Join-Path for cross-platform paths
$configPath = Join-Path -Path $PSScriptRoot -ChildPath "config.json"

# Use [System.IO.Path] for path manipulation
$fullPath = [System.IO.Path]::Combine($home, "documents", "file.txt")

# Forward slashes work on all platforms in PowerShell 7+
$path = "$PSScriptRoot/subfolder/file.txt"
```

**DON'T:**
```powershell
# Hardcoded backslashes (Windows-only)
$path = "C:\Users\Name\file.txt"

# Assume case-insensitive file systems
Get-ChildItem "MyFile.txt"  # Works on Windows, fails on Linux/macOS if casing is wrong
```

### 2. Platform Detection

```powershell
# Use automatic variables
if ($IsWindows) {
    # Windows-specific code
    $env:Path -split ';'
}
elseif ($IsLinux) {
    # Linux-specific code
    $env:PATH -split ':'
}
elseif ($IsMacOS) {
    # macOS-specific code
    $env:PATH -split ':'
}

# Check PowerShell version
if ($PSVersionTable.PSVersion.Major -ge 7) {
    # PowerShell 7+ features
}
```

### 3. Avoid Aliases in Scripts

```powershell
# DON'T use aliases (they may differ across platforms)
ls | ? {$_.Length -gt 1MB} | % {$_.Name}

# DO use full cmdlet names
Get-ChildItem | Where-Object {$_.Length -gt 1MB} | ForEach-Object {$_.Name}
```

**Why:** On Linux/macOS, aliases might invoke native commands instead of PowerShell cmdlets, causing unexpected results.

### 4. Text Encoding

```powershell
# PowerShell 7+ uses UTF-8 by default
"Hello" | Out-File -FilePath output.txt

# For PowerShell 5.1 compatibility, specify encoding
"Hello" | Out-File -FilePath output.txt -Encoding UTF8

# Best practice: Always specify encoding for cross-platform scripts
$content | Set-Content -Path $file -Encoding UTF8NoBOM
```

### 5. Environment Variables (Cross-Platform)

```powershell
# BEST PRACTICE: Use .NET Environment class for cross-platform compatibility
[Environment]::UserName      # Works on all platforms
[Environment]::MachineName   # Works on all platforms
[IO.Path]::GetTempPath()     # Works on all platforms

# AVOID: These are platform-specific
$env:USERNAME                # Windows only
$env:USER                    # Linux/macOS only

# Environment variable names are CASE-SENSITIVE on Linux/macOS
$env:PATH    # Correct on Linux/macOS
$env:Path    # May not work on Linux/macOS
```

### 6. Shell Detection (Windows: PowerShell vs Git Bash)

**CRITICAL:** On Windows, distinguish between PowerShell and Git Bash/MSYS2 environments:

```powershell
# PowerShell detection (most reliable)
if ($env:PSModulePath -and ($env:PSModulePath -split ';').Count -ge 3) {
    Write-Host "Running in PowerShell"
}

# Platform-specific automatic variables (PowerShell 7+)
if ($IsWindows) {
    # Windows-specific code
}
elseif ($IsLinux) {
    # Linux-specific code
}
elseif ($IsMacOS) {
    # macOS-specific code
}
```

**Git Bash/MSYS2 Detection:**
```bash
# Bash detection - check MSYSTEM environment variable
if [ -n "$MSYSTEM" ]; then
    echo "Running in Git Bash/MSYS2: $MSYSTEM"
    # MSYSTEM values: MINGW64, MINGW32, MSYS
fi
```

**When to Use Each Shell:**
- **PowerShell:** Windows automation, Azure/M365, PSGallery modules, object pipelines
- **Git Bash:** Git operations, Unix tools (sed/awk/grep), POSIX scripts, text processing

**Path Handling Differences:**
- **PowerShell:** `C:\Users\John` or `C:/Users/John` (both work in PS 7+)
- **Git Bash:** `/c/Users/John` (Unix-style, auto-converts to Windows when calling Windows tools)

See `powershell-shell-detection` skill for comprehensive cross-shell guidance.

### 7. Line Endings

```powershell
# PowerShell handles line endings automatically
# But be explicit for git or cross-platform tools
git config core.autocrlf input  # Linux/macOS
git config core.autocrlf true   # Windows
```

---

## 📦 Module Management (PSResourceGet & PSGallery)

### PSResourceGet - Modern Package Manager (2025)

**PSResourceGet** is 2x faster than PowerShellGet and actively maintained:

```powershell
# PSResourceGet ships with PowerShell 7.4+ (or install manually)
Install-Module -Name Microsoft.PowerShell.PSResourceGet -Force

# Modern commands (PSResourceGet)
Install-PSResource -Name Az -Scope CurrentUser        # 2x faster
Find-PSResource -Name "*Azure*"                       # Faster search
Update-PSResource -Name Az                            # Batch updates
Get-InstalledPSResource                               # List installed
Uninstall-PSResource -Name OldModule                  # Clean uninstall

# Compatibility: Your old Install-Module commands still work
# They automatically call PSResourceGet internally
Install-Module -Name Az -Scope CurrentUser            # Works, uses PSResourceGet
```

### Finding Modules

```powershell
# PSResourceGet (Modern)
Find-PSResource -Name "*Azure*"
Find-PSResource -Tag "Security"
Find-PSResource -Name Az | Select-Object Name, Version, PublishedDate

# Legacy PowerShellGet (still works)
Find-Module -Name "*Azure*"
Find-Command -Name Get-AzVM
```

### Installing Modules

```powershell
# RECOMMENDED: PSResourceGet (2x faster)
Install-PSResource -Name Az -Scope CurrentUser -TrustRepository
Install-PSResource -Name Microsoft.Graph -Version 2.32.0

# Legacy: PowerShellGet (slower, but still works)
Install-Module -Name Az -Scope CurrentUser -Force
Install-Module -Name Pester -Scope AllUsers  # Requires elevation
```

### Managing Installed Modules

```powershell
# List installed (PSResourceGet)
Get-InstalledPSResource
Get-InstalledPSResource -Name Az

# Update modules (PSResourceGet)
Update-PSResource -Name Az
Update-PSResource                              # Updates all

# Uninstall (PSResourceGet)
Uninstall-PSResource -Name OldModule -AllVersions

# Import module
Import-Module -Name Az.Accounts
```

### Offline Installation

```powershell
# Save module (works with both)
Save-PSResource -Name Az -Path C:\OfflineModules
# Or: Save-Module -Name Az -Path C:\OfflineModules

# Install from saved location
Install-PSResource -Name Az -Path C:\OfflineModules
```

---

## 🌟 Popular PowerShell Modules

### Azure (Az Module 14.5.0)

**Latest:** Az 14.5.0 (October 2025) with zone redundancy and symbolic links

```powershell
# Install Azure module 14.5.0
Install-PSResource -Name Az -Scope CurrentUser
# Or: Install-Module -Name Az -Scope CurrentUser -Force

# Connect to Azure
Connect-AzAccount

# Common operations
Get-AzVM
Get-AzResourceGroup
New-AzResourceGroup -Name "MyRG" -Location "EastUS"

# NEW in Az 14.5: Zone redundancy for storage
New-AzStorageAccount -ResourceGroupName "MyRG" -Name "storage123" `
    -Location "EastUS" -SkuName "Standard_LRS" -EnableZoneRedundancy

# NEW in Az 14.5: Symbolic links in NFS File Share
New-AzStorageFileSymbolicLink -Context $ctx -ShareName "nfsshare" `
    -Path "symlink" -Target "/target/path"
```

**Key Submodules:**
- `Az.Accounts` - Authentication (MFA required Sep 2025+)
- `Az.Compute` - VMs, scale sets
- `Az.Storage` - Storage accounts (zone redundancy support)
- `Az.Network` - Virtual networks, NSGs
- `Az.KeyVault` - Key Vault operations
- `Az.Resources` - Resource groups, deployments

### Microsoft Graph (Microsoft.Graph 2.32.0)

**CRITICAL:** MSOnline and AzureAD modules retired (March-May 2025). Use Microsoft.Graph instead.

```powershell
# Install Microsoft Graph 2.32.0 (October 2025)
Install-PSResource -Name Microsoft.Graph -Scope CurrentUser
# Or: Install-Module -Name Microsoft.Graph -Scope CurrentUser

# Connect with required scopes
Connect-MgGraph -Scopes "User.Read.All", "Group.ReadWrite.All"

# Common operations
Get-MgUser
Get-MgGroup
New-MgUser -DisplayName "John Doe" -UserPrincipalName "john@domain.com" -MailNickname "john"
Get-MgTeam

# Migration from AzureAD/MSOnline
# OLD: Connect-AzureAD / Connect-MsolService
# NEW: Connect-MgGraph
# OLD: Get-AzureADUser / Get-MsolUser
# NEW: Get-MgUser
```

### PnP PowerShell (SharePoint/Teams)

```powershell
# Install PnP PowerShell
Install-Module -Name PnP.PowerShell -Scope CurrentUser

# Connect to SharePoint Online
Connect-PnPOnline -Url "https://tenant.sharepoint.com/sites/site" -Interactive

# Common operations
Get-PnPList
Get-PnPFile -Url "/sites/site/Shared Documents/file.docx"
Add-PnPListItem -List "Tasks" -Values @{"Title"="New Task"}
```

### AWS Tools for PowerShell

```powershell
# Install AWS Tools
Install-Module -Name AWS.Tools.Installer -Force
Install-AWSToolsModule AWS.Tools.EC2,AWS.Tools.S3

# Configure credentials
Set-AWSCredential -AccessKey $accessKey -SecretKey $secretKey -StoreAs default

# Common operations
Get-EC2Instance
Get-S3Bucket
New-S3Bucket -BucketName "my-bucket"
```

### Other Popular Modules

```powershell
# Pester (Testing framework)
Install-Module -Name Pester -Force

# PSScriptAnalyzer (Code analysis)
Install-Module -Name PSScriptAnalyzer

# ImportExcel (Excel manipulation without Excel)
Install-Module -Name ImportExcel

# PowerShellGet 3.x (Modern package management)
Install-Module -Name Microsoft.PowerShell.PSResourceGet
```

---

## 🚀 CI/CD Integration

### GitHub Actions

```yaml
name: PowerShell CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install PowerShell modules
        shell: pwsh
        run: |
          Install-Module -Name Pester -Force -Scope CurrentUser
          Install-Module -Name PSScriptAnalyzer -Force -Scope CurrentUser

      - name: Run Pester tests
        shell: pwsh
        run: |
          Invoke-Pester -Path ./tests -OutputFormat NUnitXml -OutputFile TestResults.xml

      - name: Run PSScriptAnalyzer
        shell: pwsh
        run: |
          Invoke-ScriptAnalyzer -Path . -Recurse -ReportSummary
```

**Multi-Platform Matrix:**
```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - name: Test on ${{ matrix.os }}
        shell: pwsh
        run: |
          ./test-script.ps1
```

### Azure DevOps Pipelines

```yaml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: PowerShell@2
  inputs:
    targetType: 'inline'
    script: |
      Install-Module -Name Pester -Force -Scope CurrentUser
      Invoke-Pester -Path ./tests -OutputFormat NUnitXml
  displayName: 'Run Pester Tests'

- task: PowerShell@2
  inputs:
    filePath: '$(System.DefaultWorkingDirectory)/build.ps1'
    arguments: '-Configuration Release'
  displayName: 'Run Build Script'

- task: PublishTestResults@2
  inputs:
    testResultsFormat: 'NUnit'
    testResultsFiles: '**/TestResults.xml'
```

**Cross-Platform Pipeline:**
```yaml
strategy:
  matrix:
    linux:
      imageName: 'ubuntu-latest'
    windows:
      imageName: 'windows-latest'
    mac:
      imageName: 'macos-latest'

pool:
  vmImage: $(imageName)

steps:
- pwsh: |
    Write-Host "Running on $($PSVersionTable.OS)"
    ./test-script.ps1
  displayName: 'Cross-platform test'
```

### Bitbucket Pipelines

```yaml
image: mcr.microsoft.com/powershell:latest

pipelines:
  default:
    - step:
        name: Test with PowerShell
        script:
          - pwsh -Command "Install-Module -Name Pester -Force"
          - pwsh -Command "Invoke-Pester -Path ./tests"

    - step:
        name: Deploy
        deployment: production
        script:
          - pwsh -File ./deploy.ps1
```

---

## 💻 PowerShell Syntax & Cmdlets

### Cmdlet Structure

```powershell
# Verb-Noun pattern
Get-ChildItem
Set-Location
New-Item
Remove-Item

# Common parameters (available on all cmdlets)
Get-Process -Verbose
Set-Content -Path file.txt -WhatIf
Remove-Item -Path folder -Confirm
Invoke-RestMethod -Uri $url -ErrorAction Stop
```

### Variables & Data Types

```powershell
# Variables (loosely typed)
$string = "Hello World"
$number = 42
$array = @(1, 2, 3, 4, 5)
$hashtable = @{Name="John"; Age=30}

# Strongly typed
[string]$name = "John"
[int]$age = 30
[datetime]$date = Get-Date

# Special variables
$PSScriptRoot  # Directory containing the script
$PSCommandPath  # Full path to the script
$args  # Script arguments
$_  # Current pipeline object
```

### Operators

```powershell
# Comparison operators
-eq  # Equal
-ne  # Not equal
-gt  # Greater than
-lt  # Less than
-match  # Regex match
-like  # Wildcard match
-contains  # Array contains

# Logical operators
-and
-or
-not

# PowerShell 7+ ternary operator
$result = $condition ? "true" : "false"

# Null-coalescing (PS 7+)
$value = $null ?? "default"
```

### Control Flow

```powershell
# If-ElseIf-Else
if ($condition) {
    # Code
} elseif ($otherCondition) {
    # Code
} else {
    # Code
}

# Switch
switch ($value) {
    1 { "One" }
    2 { "Two" }
    {$_ -gt 10} { "Greater than 10" }
    default { "Other" }
}

# Loops
foreach ($item in $collection) {
    # Process item
}

for ($i = 0; $i -lt 10; $i++) {
    # Loop code
}

while ($condition) {
    # Loop code
}

do {
    # Loop code
} while ($condition)
```

### Functions

```powershell
function Get-Something {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$Name,

        [Parameter()]
        [int]$Count = 1,

        [Parameter(ValueFromPipeline=$true)]
        [string[]]$InputObject
    )

    begin {
        # Initialization
    }

    process {
        # Process each pipeline object
        foreach ($item in $InputObject) {
            # Work with $item
        }
    }

    end {
        # Cleanup
        return $result
    }
}
```

### Pipeline & Filtering

```powershell
# Pipeline basics
Get-Process | Where-Object {$_.CPU -gt 100} | Select-Object Name, CPU

# Simplified syntax (PS 3.0+)
Get-Process | Where CPU -gt 100 | Select Name, CPU

# ForEach-Object
Get-ChildItem | ForEach-Object {
    Write-Host $_.Name
}

# Simplified (PS 4.0+)
Get-ChildItem | % Name

# Group, Sort, Measure
Get-Process | Group-Object ProcessName
Get-Service | Sort-Object Status
Get-ChildItem | Measure-Object -Property Length -Sum
```

### Error Handling

```powershell
# Try-Catch-Finally
try {
    Get-Content -Path "nonexistent.txt" -ErrorAction Stop
}
catch [System.IO.FileNotFoundException] {
    Write-Error "File not found"
}
catch {
    Write-Error "An error occurred: $_"
}
finally {
    # Cleanup code
}

# Error action preference
$ErrorActionPreference = "Stop"  # Treat all errors as terminating
$ErrorActionPreference = "Continue"  # Default
$ErrorActionPreference = "SilentlyContinue"  # Suppress errors
```

---

## 🔒 Security Best Practices (2025 Standards)

### Modern Security Framework (JEA + WDAC + Logging)

**2025 Security Requirements:**
1. **JEA** - Just Enough Administration for role-based access
2. **WDAC** - Windows Defender Application Control for script approval
3. **Constrained Language Mode** - For non-admin users
4. **Script Block Logging** - For audit trails

### Just Enough Administration (JEA)

**Required for production environments in 2025:**

```powershell
# Create JEA session configuration file
New-PSSessionConfigurationFile -SessionType RestrictedRemoteServer `
    -Path "C:\JEA\HelpDesk.pssc" `
    -VisibleCmdlets @{
        Name = 'Restart-Service'
        Parameters = @{ Name = 'Name'; ValidateSet = 'Spooler', 'Wuauserv' }
    }, @{
        Name = 'Get-Service'
    } `
    -LanguageMode NoLanguage `
    -ExecutionPolicy RemoteSigned

# Register JEA endpoint
Register-PSSessionConfiguration -Name HelpDesk `
    -Path "C:\JEA\HelpDesk.pssc" `
    -Force

# Connect with limited privileges
Enter-PSSession -ComputerName Server01 -ConfigurationName HelpDesk
```

### Windows Defender Application Control (WDAC)

**Replaces AppLocker for PowerShell script control:**

```powershell
# Create WDAC policy for approved scripts
New-CIPolicy -FilePath "C:\WDAC\PowerShellPolicy.xml" `
    -ScanPath "C:\ApprovedScripts" `
    -Level FilePublisher `
    -Fallback Hash

# Convert to binary
ConvertFrom-CIPolicy -XmlFilePath "C:\WDAC\PowerShellPolicy.xml" `
    -BinaryFilePath "C:\Windows\System32\CodeIntegrity\SIPolicy.p7b"

# Deploy via Group Policy or MDM
```

### Constrained Language Mode

**Recommended for all non-admin users:**

```powershell
# Check current language mode
$ExecutionContext.SessionState.LanguageMode
# Output: FullLanguage (admin) or ConstrainedLanguage (standard user)

# Enable system-wide via environment variable
[Environment]::SetEnvironmentVariable(
    "__PSLockdownPolicy",
    "4",
    [System.EnvironmentVariableTarget]::Machine
)
```

### Script Block Logging

**Enable for security auditing:**

```powershell
# Enable via Group Policy or Registry
# HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging
# EnableScriptBlockLogging = 1
# EnableScriptBlockInvocationLogging = 1

# Check logs
Get-WinEvent -LogName "Microsoft-Windows-PowerShell/Operational" |
    Where-Object Id -eq 4104 |  # Script Block Logging
    Select-Object TimeCreated, Message -First 10
```

### Execution Policy

```powershell
# Check current execution policy
Get-ExecutionPolicy

# Set for current user (no admin needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Bypass for single session (use sparingly)
pwsh -ExecutionPolicy Bypass -File script.ps1
```

### Credential Management

```powershell
# NEVER hardcode credentials
# BAD: $password = "MyP@ssw0rd"

# Use SecretManagement module (modern approach)
Install-PSResource -Name Microsoft.PowerShell.SecretManagement
Install-PSResource -Name SecretManagement.KeyVault

Register-SecretVault -Name AzureKeyVault -ModuleName SecretManagement.KeyVault
$secret = Get-Secret -Name "DatabasePassword" -Vault AzureKeyVault

# Legacy: Get-Credential for interactive
$cred = Get-Credential

# Azure Key Vault for production
$vaultName = "MyKeyVault"
$secret = Get-AzKeyVaultSecret -VaultName $vaultName -Name "DatabasePassword"
$secret.SecretValue
```

### Input Validation

```powershell
function Do-Something {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]$Name,

        [Parameter()]
        [ValidateRange(1, 100)]
        [int]$Count,

        [Parameter()]
        [ValidateSet("Option1", "Option2", "Option3")]
        [string]$Option,

        [Parameter()]
        [ValidatePattern('^\d{3}-\d{3}-\d{4}$')]
        [string]$PhoneNumber
    )
}
```

### Code Signing (Production)

```powershell
# Get code signing certificate
$cert = Get-ChildItem Cert:\CurrentUser\My -CodeSigningCert

# Sign script
Set-AuthenticodeSignature -FilePath script.ps1 -Certificate $cert
```

---

## ⚡ Performance Optimization

### PowerShell 7+ Features

```powershell
# Parallel ForEach (PS 7+)
1..10 | ForEach-Object -Parallel {
    Start-Sleep -Seconds 1
    "Processed $_"
} -ThrottleLimit 5

# Ternary operator
$result = $value ? "true" : "false"

# Null-coalescing
$name = $userName ?? "default"

# Null-conditional member access
$length = $string?.Length
```

### Efficient Filtering

```powershell
# Use .NET methods for performance
# Instead of: Get-Content large.txt | Where-Object {$_ -match "pattern"}
[System.IO.File]::ReadLines("large.txt") | Where-Object {$_ -match "pattern"}

# Use -Filter parameter when available
Get-ChildItem -Path C:\ -Filter *.log -Recurse
# Instead of: Get-ChildItem -Path C:\ -Recurse | Where-Object {$_.Extension -eq ".log"}
```

### ArrayList vs Array

```powershell
# Arrays are immutable - slow for additions
$array = @()
1..1000 | ForEach-Object { $array += $_ }  # SLOW

# Use ArrayList for dynamic collections
$list = [System.Collections.ArrayList]::new()
1..1000 | ForEach-Object { [void]$list.Add($_) }  # FAST

# Or use generic List
$list = [System.Collections.Generic.List[int]]::new()
1..1000 | ForEach-Object { $list.Add($_) }
```

---

## 🧪 Testing with Pester

```powershell
# Install Pester
Install-Module -Name Pester -Force

# Basic test structure
Describe "Get-Something Tests" {
    Context "When input is valid" {
        It "Should return expected value" {
            $result = Get-Something -Name "Test"
            $result | Should -Be "Expected"
        }
    }

    Context "When input is invalid" {
        It "Should throw an error" {
            { Get-Something -Name $null } | Should -Throw
        }
    }
}

# Run tests
Invoke-Pester -Path ./tests
Invoke-Pester -Path ./tests -OutputFormat NUnitXml -OutputFile TestResults.xml

# Code coverage
Invoke-Pester -Path ./tests -CodeCoverage ./src/*.ps1
```

---

## 📝 Script Requirements & Versioning

```powershell
# Require specific PowerShell version
#Requires -Version 7.0

# Require modules
#Requires -Modules Az.Accounts, Az.Compute

# Require admin/elevated privileges (Windows)
#Requires -RunAsAdministrator

# Combine multiple requirements
#Requires -Version 7.0
#Requires -Modules @{ModuleName='Pester'; ModuleVersion='5.0.0'}

# Use strict mode
Set-StrictMode -Version Latest
```

---

## 🎓 Common Cmdlets Reference

### File System
```powershell
Get-ChildItem (gci, ls, dir)
Set-Location (cd, sl)
New-Item (ni)
Remove-Item (rm, del)
Copy-Item (cp, copy)
Move-Item (mv, move)
Rename-Item (rn, ren)
Get-Content (gc, cat, type)
Set-Content (sc)
Add-Content (ac)
```

### Process Management
```powershell
Get-Process (ps, gps)
Stop-Process (kill, spps)
Start-Process (start, saps)
Wait-Process
```

### Service Management
```powershell
Get-Service (gsv)
Start-Service (sasv)
Stop-Service (spsv)
Restart-Service (srsv)
Set-Service
```

### Network
```powershell
Test-Connection (ping)
Test-NetConnection
Invoke-WebRequest (curl, wget, iwr)
Invoke-RestMethod (irm)
```

### Object Manipulation
```powershell
Select-Object (select)
Where-Object (where, ?)
ForEach-Object (foreach, %)
Sort-Object (sort)
Group-Object (group)
Measure-Object (measure)
Compare-Object (compare, diff)
```

---

## 🌐 REST API & Web Requests

```powershell
# GET request
$response = Invoke-RestMethod -Uri "https://api.example.com/data" -Method Get

# POST with JSON body
$body = @{
    name = "John"
    age = 30
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "https://api.example.com/users" `
    -Method Post -Body $body -ContentType "application/json"

# With headers and authentication
$headers = @{
    "Authorization" = "Bearer $token"
    "Accept" = "application/json"
}

$response = Invoke-RestMethod -Uri $url -Headers $headers

# Download file
Invoke-WebRequest -Uri $url -OutFile "file.zip"
```

---

## 🏗️ Script Structure Best Practices

```powershell
<#
.SYNOPSIS
    Brief description

.DESCRIPTION
    Detailed description

.PARAMETER Name
    Parameter description

.EXAMPLE
    PS> .\script.ps1 -Name "John"
    Example usage

.NOTES
    Author: Your Name
    Version: 1.0.0
    Date: 2025-01-01
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$Name
)

# Script-level error handling
$ErrorActionPreference = "Stop"

# Use strict mode
Set-StrictMode -Version Latest

try {
    # Main script logic
    Write-Verbose "Starting script"

    # ... script code ...

    Write-Verbose "Script completed successfully"
}
catch {
    Write-Error "Script failed: $_"
    exit 1
}
finally {
    # Cleanup
}
```

---

## 📚 Additional Resources

### Official Documentation
- PowerShell Docs: https://learn.microsoft.com/powershell
- PowerShell Gallery: https://www.powershellgallery.com
- Az Module Docs: https://learn.microsoft.com/powershell/azure
- Microsoft Graph Docs: https://learn.microsoft.com/graph/powershell

### Module Discovery
```powershell
# Find modules by keyword
Find-Module -Tag "Azure"
Find-Module -Tag "Security"

# Explore commands in a module
Get-Command -Module Az.Compute
Get-Command -Verb Get -Noun *VM*

# Get command help
Get-Help Get-AzVM -Full
Get-Help Get-AzVM -Examples
Get-Help Get-AzVM -Online
```

### Update Help System
```powershell
# Update help files (requires internet)
Update-Help -Force -ErrorAction SilentlyContinue

# Update help for specific modules
Update-Help -Module Az -Force
```

---

## 🎯 Quick Decision Guide

**Use PowerShell 7+ when:**
- Cross-platform compatibility needed
- New projects or scripts
- Performance is important
- Modern language features desired

**Use Windows PowerShell 5.1 when:**
- Windows-specific modules required (WSUS, GroupPolicy legacy)
- Corporate environments with strict version requirements
- Legacy script compatibility needed

**Choose Azure CLI when:**
- Simple one-liners needed
- JSON output preferred
- Bash scripting integration

**Choose PowerShell Az module when:**
- Complex automation required
- Object manipulation needed
- PowerShell scripting expertise available
- Reusable scripts and modules needed

---

## ✅ Pre-Flight Checklist for Scripts

Before running any PowerShell script, ensure:

1. ✅ **Platform Detection** - Use `$IsWindows`, `$IsLinux`, `$IsMacOS`
2. ✅ **Version Check** - `#Requires -Version 7.0` if needed
3. ✅ **Module Requirements** - `#Requires -Modules` specified
4. ✅ **Error Handling** - `try/catch` blocks in place
5. ✅ **Input Validation** - Parameter validation attributes used
6. ✅ **No Aliases** - Full cmdlet names in scripts
7. ✅ **Path Handling** - Use `Join-Path` or `[IO.Path]::Combine()`
8. ✅ **Encoding Specified** - UTF-8 for cross-platform
9. ✅ **Credentials Secure** - Never hardcoded
10. ✅ **Verbose Logging** - `Write-Verbose` for debugging

---

## 🚨 Common Pitfalls & Solutions

### Pitfall: Out-GridView Search Broken in 7.5
```powershell
# Known Issue: Out-GridView search doesn't work in PowerShell 7.5 due to .NET 9 changes
# Workaround: Use Where-Object or Select-Object for filtering
Get-Process | Where-Object CPU -gt 100 | Format-Table

# Or export to CSV and use external tools
Get-Process | Export-Csv processes.csv -NoTypeInformation
```

### Pitfall: Case Sensitivity
```powershell
# Linux/macOS are case-sensitive
# This fails on Linux if file is "File.txt"
Get-Content "file.txt"

# Solution: Use exact casing or Test-Path first
if (Test-Path "file.txt") {
    Get-Content "file.txt"
}
```

### Pitfall: Execution Policy
```powershell
# Solution: Set for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or bypass for session
powershell.exe -ExecutionPolicy Bypass -File script.ps1
```

### Pitfall: Module Import Failures
```powershell
# Solution: Check module availability and install
if (-not (Get-Module -ListAvailable -Name Az)) {
    Install-Module -Name Az -Force -Scope CurrentUser
}
Import-Module -Name Az
```

### Pitfall: Array Concatenation Performance
```powershell
# Bad: $array += $item (recreates array each time)

# Good: Use ArrayList or List
$list = [System.Collections.Generic.List[object]]::new()
$list.Add($item)
```

---

Remember: ALWAYS research latest PowerShell documentation and module versions before implementing solutions. The PowerShell ecosystem evolves rapidly, and best practices are updated frequently.
