---
name: smb-enumeration
description: >
  SMB share enumeration, access testing, password policy extraction, and
  content searching. Enumerates shares via null session, guest, and
  authenticated access. Covers share listing, per-share access testing,
  MANSPIDER content search, and SMB vulnerability detection (signing,
  EternalBlue). Use after network-recon identifies SMB ports (139/445).
keywords:
  - SMB shares
  - null session
  - guest access
  - smbclient
  - enum4linux
  - MANSPIDER
  - SMB signing
  - share enumeration
  - password policy
  - NetExec smb
tools:
  - smbclient
  - NetExec
  - enum4linux-ng
  - MANSPIDER
  - nmap
opsec: medium
---

# SMB Enumeration

You are helping a penetration tester enumerate SMB services on a target host.
All testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[smb-enumeration] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `smb-shares-10.10.10.5.txt`,
  `smb-manspider-results.txt`).

## Scope Boundary

This skill covers SMB enumeration only — share listing, access testing,
content searching, and vulnerability detection. When you reach the boundary
of this scope, **STOP**.

Do not load or execute another skill. Return to the orchestrator with:
  - What was found (shares, credentials, vulnerabilities)
  - Recommended next skill
  - Context to pass (DC IP, domain name, credentials, share paths)

**Routing boundaries:**
- RCE exploitation (EternalBlue, SMBGhost, PrintNightmare)
- Domain enumeration (LDAP, BloodHound, GPP)
- Password brute forcing or spraying
- Writable share abuse (web shells, DLL hijack)

**Stay in methodology.** Only use techniques documented in this skill.

## What This Skill Does NOT Do

- Exploit SMB vulnerabilities (EternalBlue, SMBGhost, PrintNightmare)
- Perform password spraying or brute force attacks
- Run Active Directory enumeration (LDAP queries, BloodHound)
- Abuse writable shares for code execution or relay NTLM authentication

These are handled by dedicated skills. This skill discovers and reports.

## State Management

Call `get_state_summary()` to read current engagement state. Use it to:
- Skip re-testing targets already enumerated for SMB
- Leverage existing credentials for authenticated enumeration (Step 7)
- Check what's been tried and failed (Blocked section)

**Interim writes** — write critical discoveries immediately via state-interim:
- SMB signing disabled → `add_vuln(title="SMB signing disabled on <host>", host="<host>", vuln_type="smb-signing", severity="medium")`
- Null session or guest access → `add_vuln(title="SMB null/guest access on <host>", host="<host>", vuln_type="null-session", severity="medium")`
- EternalBlue confirmed → `add_vuln(title="MS17-010 EternalBlue on <host>", host="<host>", vuln_type="rce", severity="critical")`
- Domain name/hostnames from SMB → `add_pivot(source="SMB on <host>", destination="<domain>/<hostname>", method="SMB OS discovery")`
- Credentials found in share files → `add_credential(username="<user>", secret="<password>", secret_type="password", source="SMB share file <path>")`

**Return summary must include:**
- Per-share access table (mandatory — every share gets a row)
- Account lockout policy (if enumerable)
- Domain/hostname info discovered
- Credentials found
- Vulnerabilities confirmed (signing, null session, EternalBlue)

## Prerequisites

- Network access to SMB ports (139/445) on target
- Target IP address (provided by orchestrator or operator)
- Optional: credentials for authenticated enumeration (passed by orchestrator)

## Step 1: Share Listing

**Run ALL of the following tools in sequence — not just one.** SMB tools use
different RPC calls and authentication methods under the hood. A failure or
partial result from one tool does NOT mean the others will also fail. NetExec
might return `STATUS_USER_SESSION_DELETED` while `smbclient -L` succeeds, or
vice versa. You must try every tool before concluding that SMB enumeration
has failed.

```bash
# Tool 1: smbclient null session share listing
smbclient -N -L //TARGET_IP/

# Tool 2: NetExec null session + guest
netexec smb TARGET_IP -u '' -p '' --shares
netexec smb TARGET_IP -u 'guest' -p '' --shares

# Tool 3: enum4linux-ng comprehensive enumeration
enum4linux-ng -A TARGET_IP
```

Collect all unique share names from ALL tools. A share discovered by any tool
counts — even if other tools failed to list it.

## Step 2: Password/Lockout Policy

```bash
netexec smb TARGET_IP -u '' -p '' --pass-pol
netexec smb TARGET_IP -u 'guest' -p '' --pass-pol
```

If either succeeds, record the full policy. The orchestrator needs this before
routing to password-spraying. Key values: lockout threshold (0 = no lockout —
critical for spray decisions), observation window, lockout duration, min
password length, complexity requirements.

## Step 3: User and Vulnerability Enumeration via NSE

```bash
nmap -sV -p445 --script smb-enum-shares,smb-enum-users,smb-os-discovery,smb-vuln* TARGET_IP
```

Check results for: SMB signing status, OS version, EternalBlue (ms17-010),
SMBGhost (CVE-2020-0796), user accounts enumerated.

## Step 4: Per-Share Access Testing (MANDATORY)

**This step is NOT optional.** Test every share individually with `smbclient`.
Access denied on one share tells you NOTHING about other shares — Windows ACLs
are per-share. Skipping a share is a methodology failure.

For EVERY share discovered in Steps 1 and 3 (from ANY tool), run:

```bash
smbclient //TARGET_IP/SHARENAME -N -c 'ls' 2>&1
```

If `ls` succeeds (shows files/directories), the share is readable. Follow up:

```bash
# Recursive listing of accessible share
smbclient //TARGET_IP/SHARENAME -N -c 'recurse ON; prompt OFF; ls'

# Download interesting files (configs, scripts, credentials, backups)
smbclient //TARGET_IP/SHARENAME -N -c 'recurse ON; prompt OFF; mget *'
```

**Per-share results table (mandatory in return summary).** Every share must
have a row. No share may be listed as "not tested".

```
| Share | Access | Method | Contents/Notes |
|-------|--------|--------|----------------|
| ADMIN$ | DENIED | smbclient -N | NT_STATUS_ACCESS_DENIED |
| C$ | DENIED | smbclient -N | NT_STATUS_ACCESS_DENIED |
| Development | READ | smbclient -N | Automation/ directory found |
| IPC$ | LIMITED | smbclient -N | IPC only, no file listing |
| NETLOGON | READ | smbclient -N | Empty or standard scripts |
| SYSVOL | READ | smbclient -N | Policies, scripts |
```

**Rules:**
- "Access" must be one of: `READ`, `WRITE`, `DENIED`, `LIMITED`, `ERROR`
- "Method" must show the actual command used
- Never report a share as DENIED unless you received `NT_STATUS_ACCESS_DENIED`
  (or similar error) from testing THAT SPECIFIC share
- Never infer access status from other shares — test each one individually
- If `smbclient` hangs or times out on a share, report as `ERROR` with details

## Step 5: Fallback Share Probing

**Only if ALL listing tools in Step 1 failed.** Some Windows configurations
block null-session share *listing* but allow null-session *access* to
individual shares:

```bash
for share in ADMIN$ C$ IPC$ SYSVOL NETLOGON Development Users Backups Public Data IT HR Finance Software Shared Docs; do
    echo "--- $share ---"
    smbclient //TARGET_IP/"$share" -N -c 'ls' 2>&1 | head -20
done
```

## Step 6: Content Search with MANSPIDER

After identifying accessible shares, search file contents for credentials and
sensitive data. MANSPIDER crawls SMB shares and greps file contents (including
Office docs, PDFs, and archives) without downloading everything.

Only run after the share access table is complete — needs at least one readable
share. If all shares returned DENIED, skip this step.

```bash
# Keyword search for passwords and credentials
manspider TARGET_IP -c password passwd cred secret
manspider TARGET_IP -c connectionstring server= uid= pwd=

# Regex search for credential patterns
manspider TARGET_IP -e '(password|passwd|pwd)\s*[=:]\s*\S+'

# Limit to specific file types
manspider TARGET_IP -e 'password' -f xml conf config ini txt ps1 bat vbs
```

## Step 7: Authenticated Re-enumeration

If the orchestrator passes credentials, repeat Steps 1, 4, and 6 with creds:

```bash
netexec smb TARGET_IP -u 'USERNAME' -p 'PASSWORD' -d DOMAIN --shares
smbclient //TARGET_IP/SHARENAME -U 'DOMAIN/USERNAME%PASSWORD' -c 'ls' 2>&1
manspider TARGET_IP -u 'USERNAME' -p 'PASSWORD' -d DOMAIN -c password secret
```

Update the per-share access table with authenticated results.

## Step 8: Escalate or Pivot

After completing enumeration:
- **EternalBlue/SMBGhost confirmed** → STOP. Recommend **smb-exploitation**. Pass: host, vuln type, OS version.
- **Domain info discovered** → STOP. Recommend **ad-discovery**. Pass: DC IP, domain name, creds/null session.
- **Password policy extracted** (lockout=0) → STOP. Recommend **password-spraying**. Pass: policy, usernames.
- **Credentials found in shares** → STOP. Recommend **ad-discovery** or authenticated re-enumeration.
- **Writable shares found** → STOP. Recommend **smb-exploitation**. Pass: share name, write method.
- **All shares denied, no vulns** → Report complete. No further SMB enumeration without creds.

## Troubleshooting

### smbclient hangs or times out
Add `-t 10` for a 10-second timeout. Verify port 445 is open with nmap.

### NT_STATUS_CONNECTION_DISCONNECTED
Target rejecting null sessions. Try guest: `-U 'guest%'`. If guest also fails, enumeration requires credentials.

### enum4linux-ng not found
Fall back to `enum4linux` (Perl version) or rely on smbclient + NetExec. Do not install — report missing.

### NetExec STATUS_USER_SESSION_DELETED
Common and does NOT mean SMB is inaccessible. Continue with smbclient and enum4linux-ng.

### MANSPIDER permission errors
Permission errors on ADMIN$/C$ are expected. Verify it crawled readable shares from Step 4.
