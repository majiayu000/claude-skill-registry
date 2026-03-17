---
name: PowerShell Scripting for Security
description: This skill should be used when the user asks to "write PowerShell scripts", "automate security tasks with PowerShell", "create PowerShell functions", "work with PowerShell modules", "parse data with PowerShell", or "build security automation scripts". It provides comprehensive PowerShell scripting fundamentals for security professionals.
version: 1.0.0
tags: [powershell, scripting, automation, windows, security, penetration-testing]
---

# PowerShell Scripting for Security

## Purpose

Develop PowerShell scripting skills for security automation, penetration testing, and system administration. This skill covers variables, operators, control structures, functions, modules, error handling, and practical security automation examples essential for red team operations and security assessments.

## Prerequisites

### Required Environment
- Windows PowerShell 5.1 or PowerShell 7+
- Administrator access for certain operations
- Text editor (VS Code with PowerShell extension recommended)

### Required Knowledge
- Basic command-line familiarity
- Understanding of programming concepts
- Windows operating system fundamentals

## Outputs and Deliverables

1. **Reusable Security Scripts** - Automation scripts for common security tasks
2. **Custom PowerShell Functions** - Modular security tools
3. **PowerShell Modules** - Packaged security utilities
4. **Automation Workflows** - Complete security assessment scripts

## Core Workflow

### Phase 1: Variables and Data Types

Work with PowerShell variables:

```powershell
# Variable declaration ($ prefix required)
$target = "192.168.1.100"
$ports = @(21, 22, 80, 443, 3389)
$credentials = Get-Credential

# Check data type
$target.GetType().Name  # String
$ports.GetType().Name   # Object[]

# Type casting
$portString = "443"
$portInt = [int]$portString

# Common data types
[string]   # Text
[int]      # Integer
[bool]     # True/False
[array]    # Array of values
[hashtable]# Key-value pairs
[datetime] # Date and time
[psobject] # PowerShell object
```

Important automatic variables:

```powershell
$_         # Current pipeline object
$?         # Last command success (True/False)
$Error     # Array of recent errors
$null      # Empty/null value
$true      # Boolean True
$false     # Boolean False
$PSScriptRoot  # Script directory path
$env:USERNAME  # Environment variables
```

### Phase 2: Operators

Master PowerShell operators:

```powershell
# Arithmetic operators
$a = 10; $b = 3
$a + $b   # 13 (addition)
$a - $b   # 7 (subtraction)
$a * $b   # 30 (multiplication)
$a / $b   # 3.33 (division)
$a % $b   # 1 (modulus)

# Comparison operators
$a -eq $b    # Equal
$a -ne $b    # Not equal
$a -lt $b    # Less than
$a -gt $b    # Greater than
$a -le $b    # Less or equal
$a -ge $b    # Greater or equal

# String comparison
"PowerShell" -like "*Shell*"     # Wildcard match
"PowerShell" -match "Shell$"     # Regex match
"192.168.1.1" -match "^\d+\.\d+\.\d+\.\d+$"  # IP pattern

# Logical operators
($a -gt 5) -and ($b -lt 5)  # AND
($a -gt 5) -or ($b -gt 5)   # OR
-not ($a -eq 10)            # NOT
!($a -eq 10)                # NOT (alternative)

# Assignment operators
$a += 5   # Add and assign
$a -= 5   # Subtract and assign
$a *= 2   # Multiply and assign
$a++      # Increment
$a--      # Decrement
```

### Phase 3: Control Structures

Implement conditional logic:

```powershell
# If/ElseIf/Else
$status = "open"
if ($status -eq "open") {
    Write-Host "Port is open"
} elseif ($status -eq "filtered") {
    Write-Host "Port is filtered"
} else {
    Write-Host "Port is closed"
}

# Switch statement
$port = 443
switch ($port) {
    21 { "FTP" }
    22 { "SSH" }
    80 { "HTTP" }
    443 { "HTTPS" }
    3389 { "RDP" }
    default { "Unknown service" }
}

# Switch with regex
switch -Regex ($input) {
    "^[A-Z]" { "Starts with letter" }
    "^[0-9]" { "Starts with number" }
    default { "Unknown format" }
}
```

Implement loops:

```powershell
# ForEach-Object (pipeline)
$targets | ForEach-Object {
    Write-Host "Scanning: $_"
    Test-Connection -ComputerName $_ -Count 1
}

# Foreach statement
foreach ($target in $targets) {
    Write-Host "Scanning: $target"
}

# For loop
for ($i = 1; $i -le 254; $i++) {
    $ip = "192.168.1.$i"
    Test-Connection -ComputerName $ip -Count 1 -Quiet
}

# While loop
$count = 0
while ($count -lt 10) {
    Write-Host "Attempt: $count"
    $count++
}

# Do-While / Do-Until
do {
    $response = Invoke-WebRequest -Uri $url
} while ($response.StatusCode -ne 200)

# Break and Continue
foreach ($port in $ports) {
    if ($port -eq 0) { continue }  # Skip invalid
    if ($port -gt 65535) { break } # Stop loop
    Test-NetConnection -Port $port
}
```

### Phase 4: Functions

Create reusable functions:

```powershell
# Basic function
function Test-Port {
    param (
        [string]$ComputerName,
        [int]$Port
    )
    
    $connection = Test-NetConnection -ComputerName $ComputerName -Port $Port
    return $connection.TcpTestSucceeded
}

# Call the function
Test-Port -ComputerName "192.168.1.100" -Port 80

# Advanced function with CmdletBinding
function Invoke-PortScan {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory, ValueFromPipeline)]
        [string]$Target,
        
        [Parameter()]
        [int[]]$Ports = @(21, 22, 80, 443, 3389),
        
        [Parameter()]
        [int]$Timeout = 1000
    )
    
    begin {
        Write-Verbose "Starting port scan"
        $results = @()
    }
    
    process {
        foreach ($port in $Ports) {
            $tcpClient = New-Object System.Net.Sockets.TcpClient
            $connect = $tcpClient.BeginConnect($Target, $port, $null, $null)
            $wait = $connect.AsyncWaitHandle.WaitOne($Timeout, $false)
            
            if ($wait -and $tcpClient.Connected) {
                $results += [PSCustomObject]@{
                    Target = $Target
                    Port = $port
                    Status = "Open"
                }
            }
            $tcpClient.Close()
        }
    }
    
    end {
        Write-Verbose "Scan complete"
        return $results
    }
}

# Usage
Invoke-PortScan -Target "192.168.1.100" -Ports 80,443 -Verbose
```

### Phase 5: Error Handling

Implement robust error handling:

```powershell
# Try/Catch/Finally
function Test-RemoteConnection {
    param([string]$Computer)
    
    try {
        $session = New-PSSession -ComputerName $Computer -ErrorAction Stop
        Write-Host "Connected to $Computer"
        return $session
    }
    catch [System.Management.Automation.Remoting.PSRemotingTransportException] {
        Write-Warning "Cannot connect to $Computer - Access denied"
    }
    catch {
        Write-Warning "Error: $($_.Exception.Message)"
    }
    finally {
        Write-Verbose "Connection attempt completed"
    }
}

# ErrorAction parameter
Get-Service -Name "FakeService" -ErrorAction SilentlyContinue
Get-Service -Name "FakeService" -ErrorAction Stop  # Throws terminating error

# Check for errors
if ($Error.Count -gt 0) {
    Write-Host "Last error: $($Error[0].Exception.Message)"
}
```

### Phase 6: Working with Objects

Manipulate PowerShell objects:

```powershell
# Create custom objects
$scanResult = [PSCustomObject]@{
    Target = "192.168.1.100"
    Port = 80
    Status = "Open"
    Timestamp = Get-Date
}

# Add properties
$scanResult | Add-Member -NotePropertyName "Banner" -NotePropertyValue "Apache"

# Select specific properties
Get-Process | Select-Object Name, CPU, WorkingSet

# Filter objects
Get-Process | Where-Object { $_.CPU -gt 10 }

# Sort objects
Get-Process | Sort-Object CPU -Descending

# Group objects
Get-EventLog -LogName Security -Newest 1000 | 
    Group-Object -Property EntryType

# Export objects
$results | Export-Csv -Path "results.csv" -NoTypeInformation
$results | ConvertTo-Json | Out-File "results.json"
```

### Phase 7: Arrays and Hashtables

Work with collections:

```powershell
# Arrays
$targets = @("192.168.1.1", "192.168.1.2", "192.168.1.3")
$targets += "192.168.1.4"  # Add element
$targets[0]                 # Access first element
$targets[-1]                # Access last element
$targets.Count              # Array length

# Hashtables
$credentials = @{
    Username = "admin"
    Password = "password123"
    Domain = "CORP"
}
$credentials["Username"]    # Access value
$credentials.Keys           # List keys
$credentials.Values         # List values

# Ordered hashtable
$config = [ordered]@{
    Target = "192.168.1.100"
    Ports = @(80, 443)
    Timeout = 5000
}

# ArrayList (dynamic sizing)
$results = [System.Collections.ArrayList]@()
$results.Add($scanResult) | Out-Null
```

### Phase 8: File Operations

Handle files and output:

```powershell
# Read files
$content = Get-Content -Path "targets.txt"
$json = Get-Content -Path "config.json" | ConvertFrom-Json
$csv = Import-Csv -Path "hosts.csv"

# Write files
$data | Out-File -Path "output.txt"
$data | Set-Content -Path "output.txt"
$results | Export-Csv -Path "results.csv" -NoTypeInformation
$config | ConvertTo-Json | Out-File "config.json"

# Append to file
Add-Content -Path "log.txt" -Value "$(Get-Date): Scan started"

# Test file existence
if (Test-Path -Path $filePath) {
    $content = Get-Content -Path $filePath
}

# Create directories
New-Item -ItemType Directory -Path ".\results" -Force
```

### Phase 9: Network Operations

Perform network-related tasks:

```powershell
# Web requests
$response = Invoke-WebRequest -Uri "https://target.com"
$response.StatusCode
$response.Content

# REST API calls
$apiResult = Invoke-RestMethod -Uri "https://api.target.com/users" -Method Get

# Download files
Invoke-WebRequest -Uri $url -OutFile "downloaded.exe"

# DNS lookups
Resolve-DnsName -Name "target.com" -Type A
Resolve-DnsName -Name "target.com" -Type MX

# Test connections
Test-Connection -ComputerName "192.168.1.100" -Count 4
Test-NetConnection -ComputerName "192.168.1.100" -Port 443

# Get network adapters
Get-NetAdapter | Where-Object Status -eq "Up"
Get-NetIPAddress -AddressFamily IPv4
```

### Phase 10: Security Scripts

Create practical security scripts:

```powershell
# Simple port scanner
function Invoke-QuickScan {
    param(
        [string]$Target,
        [int[]]$Ports = @(21,22,23,25,53,80,110,135,139,143,443,445,993,995,1433,3306,3389,5432,8080)
    )
    
    $openPorts = @()
    
    foreach ($port in $Ports) {
        $socket = New-Object System.Net.Sockets.TcpClient
        try {
            $socket.Connect($Target, $port)
            if ($socket.Connected) {
                $openPorts += $port
                Write-Host "[+] Port $port is OPEN" -ForegroundColor Green
            }
            $socket.Close()
        }
        catch {
            Write-Verbose "[-] Port $port is closed"
        }
    }
    
    return $openPorts
}

# Password generator
function New-SecurePassword {
    param([int]$Length = 16)
    
    $chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    $password = ""
    
    for ($i = 0; $i -lt $Length; $i++) {
        $randomIndex = Get-Random -Minimum 0 -Maximum $chars.Length
        $password += $chars[$randomIndex]
    }
    
    return $password
}

# Log analyzer
function Search-SecurityLog {
    param(
        [int]$EventID,
        [int]$Hours = 24
    )
    
    $startTime = (Get-Date).AddHours(-$Hours)
    
    Get-WinEvent -FilterHashtable @{
        LogName = 'Security'
        ID = $EventID
        StartTime = $startTime
    } | Select-Object TimeCreated, Message
}
```

## Quick Reference

### Common Cmdlets

| Cmdlet | Purpose |
|--------|---------|
| `Get-Command` | Find commands |
| `Get-Help` | Get documentation |
| `Get-Member` | Inspect object properties |
| `Select-Object` | Choose properties |
| `Where-Object` | Filter objects |
| `ForEach-Object` | Process each object |
| `Sort-Object` | Sort output |
| `Export-Csv` | Export to CSV |
| `ConvertTo-Json` | Convert to JSON |

### Comparison Operators

| Operator | Meaning |
|----------|---------|
| `-eq` | Equal |
| `-ne` | Not equal |
| `-lt` | Less than |
| `-gt` | Greater than |
| `-le` | Less or equal |
| `-ge` | Greater or equal |
| `-like` | Wildcard match |
| `-match` | Regex match |

### Special Variables

| Variable | Description |
|----------|-------------|
| `$_` | Current pipeline object |
| `$PSScriptRoot` | Script directory |
| `$Error` | Error collection |
| `$null` | Null value |
| `$true` / `$false` | Boolean values |
| `$env:VAR` | Environment variable |

### Script Structure Template

```powershell
#Requires -Version 5.1
<#
.SYNOPSIS
    Brief description
.DESCRIPTION
    Detailed description
.PARAMETER Target
    Parameter description
.EXAMPLE
    Usage example
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$Target
)

# Script logic here
```

## Constraints and Limitations

### Execution Policy
- May need to set: `Set-ExecutionPolicy RemoteSigned`
- Scripts from internet may be blocked
- Consider signing scripts for production

### Security Considerations
- Credentials should use SecureString
- Avoid hardcoding passwords
- Use `Get-Credential` for interactive input
- Store secrets in secure vaults

### Performance
- Large loops can be slow
- Use `-Parallel` in PowerShell 7+ for parallelism
- Avoid excessive pipeline operations
- Pre-filter data when possible

## Troubleshooting

### Script Won't Execute

**Solutions:**
1. Check execution policy: `Get-ExecutionPolicy`
2. Unblock downloaded scripts: `Unblock-File script.ps1`
3. Run as administrator if required
4. Check PowerShell version compatibility

### Module Not Found

**Solutions:**
1. Install module: `Install-Module -Name ModuleName`
2. Check PSModulePath: `$env:PSModulePath`
3. Import explicitly: `Import-Module -Name ModuleName`
4. Verify repository: `Get-PSRepository`

### Permission Denied

**Solutions:**
1. Run PowerShell as Administrator
2. Check file permissions
3. Verify user has required access
4. Check remote PowerShell is enabled
