---
name: powershell-security
description: Modern PowerShell security practices including SecretManagement, JEA, WDAC, and credential protection
---

# PowerShell Security Best Practices (2025)

Modern security practices for PowerShell scripts and automation, including credential management, SecretManagement module, and hardening techniques.

## SecretManagement Module (Recommended 2025 Standard)

### Overview

**Microsoft.PowerShell.SecretManagement** is the official solution for secure credential storage in PowerShell.

**Why use SecretManagement:**
- Never store plaintext credentials in scripts
- Cross-platform secret storage
- Multiple vault provider support
- Integration with Azure Key Vault, 1Password, KeePass, etc.

### Installation

```powershell
# Install SecretManagement module
Install-Module -Name Microsoft.PowerShell.SecretManagement -Scope CurrentUser

# Install vault provider (choose one or more)
Install-Module -Name Microsoft.PowerShell.SecretStore  # Local encrypted vault
Install-Module -Name Az.KeyVault                        # Azure Key Vault
Install-Module -Name SecretManagement.KeePass          # KeePass integration
```

### Basic Usage

```powershell
# Register a vault
Register-SecretVault -Name LocalVault -ModuleName Microsoft.PowerShell.SecretStore

# Store a secret
$password = Read-Host -AsSecureString -Prompt "Enter password"
Set-Secret -Name "DatabasePassword" -Secret $password -Vault LocalVault

# Retrieve a secret
$dbPassword = Get-Secret -Name "DatabasePassword" -Vault LocalVault -AsPlainText
# Or as SecureString
$dbPasswordSecure = Get-Secret -Name "DatabasePassword" -Vault LocalVault

# List secrets
Get-SecretInfo

# Remove a secret
Remove-Secret -Name "DatabasePassword" -Vault LocalVault
```

### Azure Key Vault Integration

```powershell
# Install and import Az.KeyVault
Install-Module -Name Az.KeyVault -Scope CurrentUser
Import-Module Az.KeyVault

# Authenticate to Azure
Connect-AzAccount

# Register Azure Key Vault as secret vault
Register-SecretVault -Name AzureKV `
    -ModuleName Az.KeyVault `
    -VaultParameters @{
        AZKVaultName = 'MyKeyVault'
        SubscriptionId = 'your-subscription-id'
    }

# Store secret in Azure Key Vault
Set-Secret -Name "ApiKey" -Secret "your-api-key" -Vault AzureKV

# Retrieve from Azure Key Vault
$apiKey = Get-Secret -Name "ApiKey" -Vault AzureKV -AsPlainText
```

### Automation Scripts with SecretManagement

```powershell
<#
.SYNOPSIS
    Secure automation script using SecretManagement

.DESCRIPTION
    Demonstrates secure credential handling without hardcoded secrets
#>

#Requires -Modules Microsoft.PowerShell.SecretManagement

[CmdletBinding()]
param()

# Retrieve credentials from vault
$dbConnectionString = Get-Secret -Name "SQLConnectionString" -AsPlainText
$apiToken = Get-Secret -Name "APIToken" -AsPlainText

# Use credentials securely
try {
    # Database operation
    $connection = New-Object System.Data.SqlClient.SqlConnection($dbConnectionString)
    $connection.Open()

    # API call with token
    $headers = @{ Authorization = "Bearer $apiToken" }
    $response = Invoke-RestMethod -Uri "https://api.example.com/data" -Headers $headers

    # Process results
    Write-Host "Operation completed successfully"
}
catch {
    Write-Error "Operation failed: $_"
}
finally {
    if ($connection) { $connection.Close() }
}
```

## Credential Management Best Practices

### Never Hardcode Credentials

```powershell
# ❌ WRONG - Hardcoded credentials
$password = "MyPassword123"
$username = "admin"

# ❌ WRONG - Plaintext in script
$cred = New-Object System.Management.Automation.PSCredential("admin", "password")

# ✅ CORRECT - SecretManagement
$password = Get-Secret -Name "AdminPassword" -AsPlainText
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential("admin", $securePassword)

# ✅ CORRECT - Interactive prompt (for manual runs)
$cred = Get-Credential -Message "Enter admin credentials"

# ✅ CORRECT - Managed Identity (Azure automation)
Connect-AzAccount -Identity
```

### Service Principal Authentication (Azure)

```powershell
# Store service principal credentials in vault
Set-Secret -Name "AzureAppId" -Secret "app-id-guid"
Set-Secret -Name "AzureAppSecret" -Secret "app-secret-value"
Set-Secret -Name "AzureTenantId" -Secret "tenant-id-guid"

# Retrieve and authenticate
$appId = Get-Secret -Name "AzureAppId" -AsPlainText
$appSecret = Get-Secret -Name "AzureAppSecret" -AsPlainText
$tenantId = Get-Secret -Name "AzureTenantId" -AsPlainText

$secureSecret = ConvertTo-SecureString $appSecret -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential($appId, $secureSecret)

Connect-AzAccount -ServicePrincipal -Credential $credential -Tenant $tenantId
```

## Just Enough Administration (JEA)

### What is JEA?

**Just Enough Administration** restricts PowerShell remoting sessions to specific cmdlets and parameters.

### Use Cases

- Delegate admin tasks without full admin rights
- Compliance requirements (SOC 2, HIPAA, PCI-DSS)
- Production environment hardening
- Audit trail for privileged operations

### Creating a JEA Endpoint

```powershell
# 1. Create role capability file
New-PSRoleCapabilityFile -Path "C:\JEA\RestartServices.psrc" `
    -VisibleCmdlets @{
        Name = 'Restart-Service'
        Parameters = @{
            Name = 'Name'
            ValidateSet = 'Spooler', 'W32Time', 'WinRM'
        }
    }, 'Get-Service'

# 2. Create session configuration file
New-PSSessionConfigurationFile -Path "C:\JEA\RestartServices.pssc" `
    -SessionType RestrictedRemoteServer `
    -RoleDefinitions @{
        'DOMAIN\ServiceAdmins' = @{ RoleCapabilities = 'RestartServices' }
    } `
    -LanguageMode NoLanguage

# 3. Register JEA endpoint
Register-PSSessionConfiguration -Name RestartServices `
    -Path "C:\JEA\RestartServices.pssc" `
    -Force

# 4. Connect to JEA endpoint (as delegated user)
Enter-PSSession -ComputerName Server01 -ConfigurationName RestartServices

# User can ONLY run allowed commands
Restart-Service -Name Spooler  # ✅ Allowed
Restart-Service -Name DNS      # ❌ Denied (not in ValidateSet)
Get-Process                    # ❌ Denied (not visible)
```

### JEA Audit Logging

```powershell
# Enable transcription and logging
New-PSSessionConfigurationFile -Path "C:\JEA\AuditedSession.pssc" `
    -SessionType RestrictedRemoteServer `
    -TranscriptDirectory "C:\JEA\Transcripts" `
    -RunAsVirtualAccount

# All JEA sessions are transcribed to C:\JEA\Transcripts
# Review audit logs
Get-ChildItem "C:\JEA\Transcripts" | Get-Content
```

## Windows Defender Application Control (WDAC)

### PowerShell Script Control

**WDAC** replaces AppLocker for controlling which PowerShell scripts can execute.

```powershell
# Create WDAC policy for signed scripts only
New-CIPolicy -FilePath "C:\WDAC\PowerShellPolicy.xml" `
    -ScanPath "C:\Scripts" `
    -Level FilePublisher `
    -Fallback Hash `
    -UserPEs

# Allow only signed scripts
Set-RuleOption -FilePath "C:\WDAC\PowerShellPolicy.xml" `
    -Option 3 # Required WHQL

# Convert to binary policy
ConvertFrom-CIPolicy -XmlFilePath "C:\WDAC\PowerShellPolicy.xml" `
    -BinaryFilePath "C:\Windows\System32\CodeIntegrity\SIPolicy.p7b"

# Reboot to apply policy
Restart-Computer
```

## Code Signing

### Why Sign Scripts?

- Verify script integrity
- Meet organizational security policies
- Enable WDAC enforcement
- Prevent tampering

### Signing a Script

```powershell
# Get code signing certificate
$cert = Get-ChildItem Cert:\CurrentUser\My -CodeSigningCert

# Sign script
Set-AuthenticodeSignature -FilePath "C:\Scripts\MyScript.ps1" -Certificate $cert

# Verify signature
$signature = Get-AuthenticodeSignature -FilePath "C:\Scripts\MyScript.ps1"
$signature.Status  # Should be "Valid"
```

### Execution Policy

```powershell
# Check current execution policy
Get-ExecutionPolicy

# Set execution policy (requires admin)
Set-ExecutionPolicy RemoteSigned -Scope LocalMachine

# Bypass for single script (testing only)
PowerShell.exe -ExecutionPolicy Bypass -File "script.ps1"
```

## Constrained Language Mode

### What is Constrained Language Mode?

Restricts PowerShell language features to prevent malicious code execution.

```powershell
# Check current language mode
$ExecutionContext.SessionState.LanguageMode
# Output: FullLanguage (admin) or ConstrainedLanguage (standard user)

# Set system-wide constrained language mode
# Via Environment Variable or Group Policy
# Set: __PSLockdownPolicy = 4

# Test constrained mode behavior
# FullLanguage allows:
[System.Net.WebClient]::new()  # ✅ Allowed

# ConstrainedLanguage blocks:
[System.Net.WebClient]::new()  # ❌ Blocked
Add-Type -TypeDefinition "..."  # ❌ Blocked
```

## Script Block Logging

### Enable Logging

```powershell
# Enable via Group Policy or Registry
# HKLM:\Software\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging
New-ItemProperty -Path "HKLM:\Software\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging" `
    -Name "EnableScriptBlockLogging" -Value 1 -PropertyType DWord

# Log location: Windows Event Log
# Event Viewer > Applications and Services Logs > Microsoft > Windows > PowerShell > Operational
```

### Review Logs

```powershell
# Query script block logs
Get-WinEvent -LogName "Microsoft-Windows-PowerShell/Operational" |
    Where-Object { $_.Id -eq 4104 } |  # Script Block Logging event
    Select-Object TimeCreated, Message |
    Out-GridView
```

## Input Validation

### Prevent Injection Attacks

```powershell
# ❌ WRONG - No validation
function Get-UserData {
    param($Username)
    Invoke-Sqlcmd -Query "SELECT * FROM Users WHERE Username = '$Username'"
}
# Vulnerable to SQL injection

# ✅ CORRECT - Parameterized queries
function Get-UserData {
    param(
        [ValidatePattern('^[a-zA-Z0-9_-]+$')]
        [string]$Username
    )
    Invoke-Sqlcmd -Query "SELECT * FROM Users WHERE Username = @Username" `
        -Variable @{Username=$Username}
}

# ✅ CORRECT - ValidateSet for known values
function Restart-AppService {
    param(
        [ValidateSet('Web', 'API', 'Worker')]
        [string]$ServiceName
    )
    Restart-Service -Name "App${ServiceName}Service"
}
```

## Security Checklist

### Script Development

- [ ] Never hardcode credentials (use SecretManagement)
- [ ] Use parameterized queries for SQL operations
- [ ] Validate all user input with `[ValidatePattern]`, `[ValidateSet]`, etc.
- [ ] Enable `Set-StrictMode -Version Latest`
- [ ] Use `try/catch` for error handling
- [ ] Avoid `Invoke-Expression` with user input
- [ ] Sign production scripts
- [ ] Enable Script Block Logging

### Automation

- [ ] Use Managed Identity or Service Principal (never passwords)
- [ ] Store secrets in SecretManagement or Azure Key Vault
- [ ] Implement JEA for delegated admin tasks
- [ ] Enable audit logging for all privileged operations
- [ ] Use least privilege principle
- [ ] Rotate credentials regularly
- [ ] Monitor failed authentication attempts

### Production Environments

- [ ] Implement WDAC policies for script control
- [ ] Use Constrained Language Mode for non-admin users
- [ ] Enable PowerShell logging (Script Block + Transcription)
- [ ] Require signed scripts (via execution policy)
- [ ] Regular security audits
- [ ] Keep PowerShell updated (7.5+)
- [ ] Use JEA for remote administration

## Resources

- [SecretManagement Documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.secretmanagement)
- [JEA Documentation](https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/jea/overview)
- [WDAC Documentation](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/windows-defender-application-control)
- [PowerShell Security Best Practices](https://learn.microsoft.com/en-us/powershell/scripting/security/securing-powershell)
- [Azure Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/)
