---
name: powershell-2025-changes
description: Critical PowerShell changes, deprecations, and migrations for 2025
---

# PowerShell 2025 Breaking Changes & Migrations

Critical changes, deprecations, and migration paths for PowerShell in 2025.

## PowerShell 2.0 Removal (August-September 2025)

### What's Removed

PowerShell 2.0 has been **completely removed** from:
- **Windows 11 version 24H2** (August 2025)
- **Windows Server 2025** (September 2025)

**Why:** Security improvements, reduced attack surface, legacy code cleanup

### Migration Path

```powershell
# Check if PowerShell 2.0 is installed
Get-WindowsOptionalFeature -Online -FeatureName MicrosoftWindowsPowerShellV2Root

# If you still need PowerShell 2.0 (NOT RECOMMENDED)
# - Use older Windows versions
# - Use Windows containers with older base images
# - Upgrade scripts to PowerShell 5.1 or 7+

# Recommended: Migrate to PowerShell 7.5+
winget install Microsoft.PowerShell
```

**Action Required:** Audit all scripts and remove `-Version 2.0` parameters from any PowerShell invocations.

---

## MSOnline & AzureAD Module Retirement

### Retirement Timeline

| Module | Stop Working | Retirement Complete |
|--------|--------------|---------------------|
| **MSOnline** | Late May 2025 | May 31, 2025 |
| **AzureAD** | March 30, 2025 | After July 1, 2025 |

**Critical:** These modules will stop functioning - not just deprecated, but **completely non-functional**.

### Migration Path

**From MSOnline/AzureAD to Microsoft.Graph:**

```powershell
# OLD (MSOnline) - STOPS WORKING MAY 2025
Connect-MsolService
Get-MsolUser
Set-MsolUser -UserPrincipalName "user@domain.com" -UsageLocation "US"

# NEW (Microsoft.Graph 2.32.0)
Connect-MgGraph -Scopes "User.ReadWrite.All"
Get-MgUser
Update-MgUser -UserId "user@domain.com" -UsageLocation "US"

# OLD (AzureAD) - STOPS WORKING MARCH 2025
Connect-AzureAD
Get-AzureADUser
New-AzureADUser -DisplayName "John Doe" -UserPrincipalName "john@domain.com"

# NEW (Microsoft.Graph 2.32.0)
Connect-MgGraph -Scopes "User.ReadWrite.All"
Get-MgUser
New-MgUser -DisplayName "John Doe" -UserPrincipalName "john@domain.com"
```

**Alternative:** Use Microsoft Entra PowerShell module (successor to AzureAD)

```powershell
Install-Module -Name Microsoft.Graph.Entra -Scope CurrentUser
Connect-Entra
Get-EntraUser
```

### Common Command Mappings

| MSOnline/AzureAD | Microsoft.Graph | Notes |
|------------------|----------------|-------|
| `Get-MsolUser` / `Get-AzureADUser` | `Get-MgUser` | Requires User.Read.All scope |
| `Get-MsolGroup` / `Get-AzureADGroup` | `Get-MgGroup` | Requires Group.Read.All scope |
| `Get-MsolDevice` / `Get-AzureADDevice` | `Get-MgDevice` | Requires Device.Read.All scope |
| `Connect-MsolService` / `Connect-AzureAD` | `Connect-MgGraph` | Scope-based permissions |

---

## WMIC Removal (Windows 11 25H2)

### What's Removed

**Windows Management Instrumentation Command-line (WMIC)** tool removed after upgrading to Windows 11 25H2+.

### Migration Path

**From WMIC to PowerShell WMI/CIM:**

```powershell
# OLD (WMIC) - REMOVED
wmic process list brief
wmic os get caption

# NEW (PowerShell CIM)
Get-CimInstance -ClassName Win32_Process | Select-Object Name, ProcessId, CommandLine
Get-CimInstance -ClassName Win32_OperatingSystem | Select-Object Caption, Version

# For detailed process info
Get-Process | Format-Table Name, Id, CPU, WorkingSet -AutoSize

# For system info
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion
```

---

## PowerShellGet → PSResourceGet Migration

### Modern Package Management (2025)

**PSResourceGet** is the official successor to PowerShellGet (2x faster, actively developed).

```powershell
# Install PSResourceGet (ships with PowerShell 7.4+)
Install-Module -Name Microsoft.PowerShell.PSResourceGet -Force

# New commands (PSResourceGet)
Install-PSResource -Name Az -Scope CurrentUser  # Replaces Install-Module
Find-PSResource -Name "*Azure*"                 # Replaces Find-Module
Update-PSResource -Name Az                      # Replaces Update-Module
Get-InstalledPSResource                         # Replaces Get-InstalledModule

# Compatibility layer available for legacy scripts
# Your old Install-Module commands still work but call PSResourceGet internally
```

**Performance Comparison:**
- **PowerShellGet**: 10-15 seconds to install module
- **PSResourceGet**: 5-7 seconds to install module (2x faster)

---

## Test-Json Schema Changes

### Breaking Change (PowerShell 7.4+)

**Test-Json** now uses **JsonSchema.NET** instead of **Newtonsoft.Json.Schema**.

**Impact:** No longer supports Draft 4 JSON schemas.

```powershell
# OLD (Draft 4 schema) - NO LONGER SUPPORTED
$schema = @"
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object"
}
"@

Test-Json -Json $json -Schema $schema  # FAILS in PowerShell 7.4+

# NEW (Draft 6+ schema) - SUPPORTED
$schema = @"
{
  "$schema": "http://json-schema.org/draft-06/schema#",
  "type": "object"
}
"@

Test-Json -Json $json -Schema $schema  # WORKS
```

---

## #Requires -PSSnapin Removed

### Breaking Change (PowerShell 7.4+)

All code related to `#Requires -PSSnapin` has been removed.

```powershell
# OLD (PowerShell 5.1 and earlier)
#Requires -PSSnapin Microsoft.Exchange.Management.PowerShell.SnapIn

# NEW (Use modules instead)
#Requires -Modules ExchangeOnlineManagement

Import-Module ExchangeOnlineManagement
Connect-ExchangeOnline
```

---

## Security Hardening (2025 Standards)

### Just Enough Administration (JEA)

**JEA** is now a security requirement for production environments:

```powershell
# Create JEA session configuration
New-PSSessionConfigurationFile -SessionType RestrictedRemoteServer `
    -Path "C:\JEA\RestrictedAdmin.pssc" `
    -VisibleCmdlets @{
        Name = 'Restart-Service'
        Parameters = @{ Name = 'Name'; ValidateSet = 'Spooler' }
    } `
    -LanguageMode NoLanguage

# Register JEA endpoint
Register-PSSessionConfiguration -Name RestrictedAdmin `
    -Path "C:\JEA\RestrictedAdmin.pssc" `
    -Force

# Connect with limited privileges
Enter-PSSession -ComputerName Server01 -ConfigurationName RestrictedAdmin
```

### Windows Defender Application Control (WDAC)

**WDAC** replaces AppLocker for PowerShell script control:

```powershell
# Create WDAC policy for PowerShell scripts
New-CIPolicy -FilePath "C:\WDAC\PowerShellPolicy.xml" `
    -ScanPath "C:\Scripts" `
    -Level FilePublisher `
    -Fallback Hash

# Convert to binary and deploy
ConvertFrom-CIPolicy -XmlFilePath "C:\WDAC\PowerShellPolicy.xml" `
    -BinaryFilePath "C:\Windows\System32\CodeIntegrity\SIPolicy.p7b"
```

### Constrained Language Mode

**Constrained Language Mode** is now recommended for all users without admin privileges:

```powershell
# Check current language mode
$ExecutionContext.SessionState.LanguageMode
# Output: FullLanguage (admin) or ConstrainedLanguage (standard user)

# Set system-wide constrained language mode via Group Policy or Environment Variable
# Set HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment\__PSLockdownPolicy = 4
```

---

## PowerShell 7.6 Preview Features

### Current Status (October 2025)

PowerShell 7.6.0 Preview 5 available (built on .NET 9.0.101)

**New Features:**
- **PSRedirectToVariable**: Allow redirecting to a variable
- **Module Rename**: ThreadJob → Microsoft.PowerShell.ThreadJob
- **PSResourceGet 1.1.0**: Improved performance and Azure Artifacts support

```powershell
# Check PowerShell version
$PSVersionTable.PSVersion
# 7.5.4 (stable) or 7.6.0-preview.5

# .NET version
[System.Runtime.InteropServices.RuntimeInformation]::FrameworkDescription
# .NET 9.0.101
```

---

## Migration Checklist

### Immediate Actions Required (2025)

- [ ] **Audit MSOnline/AzureAD usage** - Migrate to Microsoft.Graph 2.32.0 before May 2025
- [ ] **Remove PowerShell 2.0 references** - Upgrade to PowerShell 7.5+
- [ ] **Replace WMIC commands** - Use Get-CimInstance/Get-Process
- [ ] **Update JSON schemas** - Migrate Draft 4 to Draft 6+
- [ ] **Remove PSSnapin requirements** - Convert to modules
- [ ] **Adopt PSResourceGet** - Faster, modern package management
- [ ] **Implement JEA** - Role-based access control for production
- [ ] **Enable WDAC** - Application control for PowerShell scripts
- [ ] **Test Constrained Language Mode** - For non-admin users

### Recommended Actions

- [ ] **Upgrade to PowerShell 7.5.4** - Latest stable with .NET 9
- [ ] **Adopt Az 14.5.0** - Latest Azure module with zone redundancy
- [ ] **Use Microsoft.Graph 2.32.0** - Actively maintained Graph SDK
- [ ] **Enable Script Block Logging** - Security auditing
- [ ] **Implement Code Signing** - For production scripts
- [ ] **Use Azure Key Vault** - For credential management

---

## Testing Migration

```powershell
# Test for deprecated module usage
Get-Module MSOnline, AzureAD -ListAvailable
# If found, plan migration immediately

# Test for PowerShell 2.0 dependencies
Get-Content "script.ps1" | Select-String -Pattern "powershell.exe -Version 2"
# If found, remove version parameter

# Test for WMIC usage
Get-ChildItem -Path "C:\Scripts" -Recurse -Filter "*.ps1" |
    Select-String -Pattern "wmic" |
    Select-Object Path, Line

# Verify PowerShell version compatibility
#Requires -Version 7.0
Test-Path $PSCommandPath  # Ensures script is PowerShell 7+
```

---

## Resources

- [PowerShell 7.5 Release Notes](https://learn.microsoft.com/en-us/powershell/scripting/whats-new/what-s-new-in-powershell-75)
- [MSOnline/AzureAD Retirement Info](https://techcommunity.microsoft.com/blog/microsoft-entra-blog/action-required-msonline-and-azuread-powershell-retirement---2025-info-and-resou/4364991)
- [PSResourceGet Documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.psresourceget)
- [JEA Documentation](https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/jea/overview)
- [WDAC Documentation](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/windows-defender-application-control)

---

**Last Updated:** October 2025
