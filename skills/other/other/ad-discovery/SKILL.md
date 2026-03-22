---
name: ad-discovery
description: >
  Enumerates Active Directory domains and maps attack surface for penetration
  testing.
keywords:
  - enumerate domain
  - AD recon
  - bloodhound
  - domain enumeration
  - active directory
  - find attack paths
  - domain controllers
  - kerberos
  - pre2k
  - pre-created computer accounts
  - machine account default password
  - netexec modules
tools:
  - bloodhound-python
  - rusthound-ce
  - netexec
  - certipy
  - bloodyAD
  - kerbrute
  - Impacket
  - PowerView
opsec: medium
---

# AD Attack Discovery

You are helping a penetration tester enumerate an Active Directory domain and
identify attack paths. All testing is under explicit written authorization.

This skill works at three access levels:
1. **No credentials** — network-level recon, poisoning, RID cycling
2. **Username only** — AS-REP roasting, Kerberos user validation
3. **Valid credentials** — full enumeration, BloodHound, ADCS, ACLs

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[ad-discovery] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `sqli-users-dump.txt`, `ssrf-aws-creds.json`).

## Scope Boundary

This skill covers Active Directory discovery — enumerating domain objects,
identifying misconfigurations, and reporting findings to the orchestrator.
When you confirm an exploitable finding — **STOP**.

Do not load or execute another skill. Do not continue past your scope boundary.
Instead, return to the orchestrator with:
  - What was found (vulns, credentials, access gained)
  - Detection details (finding type, affected objects, evidence)
  - Context for technique execution (credentials, DC hostname, domain name, etc.)

The orchestrator decides what runs next. Your job is to execute this skill
thoroughly and return clean findings.

**Stay in methodology.** Only use techniques documented in this skill. If you
encounter a scenario not covered here, note it and return — do not improvise
attacks, write custom exploit code, or apply techniques from other domains.
The orchestrator will provide specific guidance or route to a different skill.

You MUST NOT:
- Perform Kerberoasting or AS-REP roasting beyond identifying targets
- Exploit delegation misconfigurations
- Exploit ACL misconfigurations
- Perform credential dumping
- Forge tickets
- Perform coercion or relay attacks
- Exploit ADCS beyond enumeration

When you find exploitable attack paths, present routing recommendations in
your return summary. Do not continue past enumeration.

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

- `add_credential()` — valid credentials (pre-created computer accounts, gMSA readable, cleartext in descriptions/GPP/shares)
- `add_vuln()` — ADCS misconfigs (ESC1-ESC8), Kerberoastable accounts, coercion vectors, SMB signing disabled, LDAP signing not required
- `add_pivot()` — delegation paths, ACL abuse chains, trust relationships, new subnets from AD Sites
- `add_blocked()` — techniques attempted and failed (so orchestrator doesn't re-route)
Your return summary must include:
- New targets/hosts discovered (with ports and services)
- New credentials or tokens found
- Access gained or changed (user, privilege level, method)
- Vulnerabilities confirmed (with status and severity)
- Pivot paths identified (what leads where)
- Blocked items (what failed and why, whether retryable)

## Prerequisites

- Network access to the target domain (ports 88, 135, 389, 445, 636)
- For unauthenticated enumeration: just network access
- For authenticated enumeration: valid domain credentials (any privilege level)
- Tools: `netexec` (nxc), `bloodhound-python` or `rusthound-ce`, `certipy`,
  `bloodyAD`, `kerbrute`, Impacket suite (`GetUserSPNs.py`, `GetNPUsers.py`,
  `lookupsid.py`)

**Kerberos-first authentication** (when credentials are available):

This skill may start unauthenticated. Once credentials are obtained, switch
to Kerberos authentication for all subsequent enumeration:

```bash
# Get a TGT (password, hash, or AES key)
# Use getTGT.py or impacket-getTGT — both are the same tool (see Troubleshooting)
getTGT.py DOMAIN/user:'Password123'@dc.domain.local
# or with NTLM hash
getTGT.py DOMAIN/user@dc.domain.local -hashes :NTHASH

export KRB5CCNAME=user.ccache

# Then use -k -no-pass on all Impacket tools
# Use --use-kcache on NetExec
# Use -k on Certipy and bloodyAD
```

## Step 1: Initial Reconnaissance

Identify domain controllers and assess the network posture.

### Find Domain Controllers

```bash
# DNS SRV records
nslookup -type=srv _ldap._tcp.dc._msdcs.DOMAIN.LOCAL
nslookup -type=srv _kerberos._tcp.DOMAIN.LOCAL

# NetExec SMB scan — shows OS, signing, SMBv1
nxc smb 10.10.10.0/24

# NetExec generate /etc/hosts entries
nxc smb 10.10.10.0/24 --generate-hosts-file hosts
```

### Check Signing and Relay Posture

```bash
# SMB signing — signing:False = relay target
nxc smb 10.10.10.0/24 | grep -i "signing:False"

# LDAP signing — signing:None = relay to LDAP viable
nxc ldap DC01.DOMAIN.LOCAL

# Determine if LDAPS is available
nxc ldap DC01.DOMAIN.LOCAL --port 636
```

**Findings:**
- SMB signing disabled on non-DCs -> note for coercion/relay
- LDAP signing not required -> note for relay to LDAP
- Domain name, DC hostnames, OS versions -> record in the engagement state

**Interim writes:**
- SMB signing disabled → `add_vuln(title="SMB signing disabled on <host>", host="<host>", vuln_type="smb-signing", severity="medium")`
- LDAP signing not required → `add_vuln(title="LDAP signing not required on <host>", host="<host>", vuln_type="ldap-signing", severity="medium")`
- Domain name/hostnames discovered → `add_pivot(source="AD discovery", destination="<domain>/<hostname>", method="DNS/SMB enumeration")`

## Step 2: Unauthenticated Enumeration

Use when no valid credentials are available yet.

### Null Session / Guest Access

```bash
# SMB null session
nxc smb DC01.DOMAIN.LOCAL -u '' -p ''
nxc smb DC01.DOMAIN.LOCAL -u 'guest' -p ''

# enum4linux
enum4linux -a -u "" -p "" DC01.DOMAIN.LOCAL

# rpcclient
rpcclient -U "" -N DC01.DOMAIN.LOCAL -c "enumdomusers;enumdomgroups;querydominfo"
```

### RID Cycling (Unauthenticated User Enumeration)

```bash
# NetExec — enumerate users via RID brute force
nxc smb DC01.DOMAIN.LOCAL -u 'guest' -p '' --rid-brute 10000

# Impacket
lookupsid.py -no-pass 'guest@DC01.DOMAIN.LOCAL' 20000

# Extract just usernames
nxc smb DC01.DOMAIN.LOCAL -u '' -p '' --rid-brute \
  | awk -F'\\\\| ' '/SidTypeUser/ {print $3}' > users.txt
```

### Kerberos Username Enumeration

```bash
# kerbrute — validates usernames via Kerberos pre-auth responses
# Generates Event 4771, NOT 4625 (often less monitored)
kerbrute userenum -d DOMAIN.LOCAL --dc DC01.DOMAIN.LOCAL usernames.txt
```

Use output as username list for password spraying and AS-REP roasting checks.

### Unauthenticated ADCS CA Enumeration

```bash
# Enumerate Certificate Authorities via RPC — no credentials needed
nxc smb DC01.DOMAIN.LOCAL -M enum_ca
```

If CAs found, note for authenticated ADCS enumeration in Step 3 (certipy).

### LLMNR/NBT-NS/mDNS Poisoning Check

If network position allows, note LLMNR/NBT-NS traffic for Responder-based
hash capture. → STOP. Return to orchestrator with: DC IP, domain name, network
position, LLMNR/NBT-NS traffic details. Do not execute poisoning or relay
commands inline.

## Step 3: BloodHound Collection

The single highest-value enumeration step. Requires valid domain credentials.

### Linux (Remote Collection)

```bash
# bloodhound-python — LDAP-based, remote
bloodhound-python -d DOMAIN.LOCAL -u 'user' -p 'Password123' \
  -gc DC01.DOMAIN.LOCAL -c all -ns DC_IP

# rusthound-ce — faster, includes ADCS data
rusthound-ce -d DOMAIN.LOCAL -u 'user@DOMAIN.LOCAL' -p 'Password123' \
  -o /tmp/bloodhound -z --adcs

# With Kerberos auth
export KRB5CCNAME=user.ccache
bloodhound-python -d DOMAIN.LOCAL -u 'user' -k -no-pass \
  -gc DC01.DOMAIN.LOCAL -c all
```

### Windows (On-Host Collection)

```powershell
# SharpHound — full collection
.\SharpHound.exe -c all -d DOMAIN.LOCAL --searchforest

# Stealthier — DC-only mode (no host enumeration)
.\SharpHound.exe --CollectionMethod DCOnly

# OPSEC — throttle and randomize
.\SharpHound.exe -c all,GPOLocalGroup --throttle 10000 --jitter 23

# SOAPHound — uses ADWS instead of LDAP (avoids LDAP monitoring)
SOAPHound.exe --buildcache -c c:\temp\cache.txt
SOAPHound.exe -c c:\temp\cache.txt --bhdump -o c:\temp\bh-output
SOAPHound.exe -c c:\temp\cache.txt --certdump -o c:\temp\bh-output
```

### ADCS Certificate Data

```bash
# Certipy — full certificate template enumeration
certipy find 'DOMAIN/user:Password123@DC01.DOMAIN.LOCAL' \
  -output engagement/evidence/certipy-full-DOMAIN

# Find vulnerable templates only
certipy find 'DOMAIN/user:Password123@DC01.DOMAIN.LOCAL' -vulnerable -hide-admins \
  -output engagement/evidence/certipy-vulnerable-DOMAIN

# With Kerberos
certipy find 'DOMAIN/user@DC01.DOMAIN.LOCAL' -k \
  -output engagement/evidence/certipy-full-DOMAIN
```

**Interim writes:** Vulnerable ADCS templates found →
`add_vuln(title="ADCS <ESC_type> on <template>", host="<CA_host>", vuln_type="adcs", severity="high")`.

**Certipy output**: Always use `-output engagement/evidence/certipy-<label>`
to write results to the evidence directory. Without `-output`, certipy writes
`{timestamp}_Certipy.{json,txt}` to CWD, polluting the working directory.

**Certipy version notes:**
- Certipy v5.0+ removed the `-bloodhound` flag. Run `certipy find` without it
  — v5 outputs JSON by default. Import the JSON into BloodHound CE manually.
- If `-vulnerable` returns 0 results, re-run without it to get the full
  template list. Some ESC variants (ESC9-15) require manual analysis of the
  full output rather than certipy's built-in vulnerability checks.

### BloodHound Analysis Priorities

After importing data, run these queries first:
1. **Shortest Paths to Domain Admins** — identify the quickest win
2. **Kerberoastable Users** — prioritize by blast radius and pwdLastSet age
3. **AS-REP Roastable Users** — free hashes, no special access needed
4. **Unconstrained Delegation** — TGT harvesting opportunities
5. **Dangerous ACLs** — GenericAll/WriteDACL/WriteOwner on high-value targets
6. **ADCS Attack Paths** — ESC1-ESC15 (requires certipy data import)
7. **Owned -> Domain Admins** — mark owned principals and find chains

## Step 4: Targeted Enumeration

Deeper enumeration beyond BloodHound. Run these based on what BloodHound reveals.

### Password Policy

```bash
# NetExec
nxc smb DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' --pass-pol

# enum4linux
enum4linux -u 'user' -p 'Password123' -P DC01.DOMAIN.LOCAL

# PowerView
(Get-DomainPolicy)."SystemAccess"
```

Record lockout threshold, observation window, complexity requirements. Report
for password spraying decisions.

### Fine-Grained Password Policies (PSOs)

```bash
# Fine-grained password policies — different groups may have different lockout rules
nxc ldap DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' -M pso
```

PSOs override default domain policy for specific groups. A service account
group may have no lockout while user accounts lock at 5 attempts. Report any
PSOs found — they affect password spraying decisions.

### Pre-Windows 2000 Computer Accounts

**High-value quick win.** Pre-created computer accounts (created via "Pre-Windows
2000 Compatible" checkbox in ADUC or `New-ADComputer`) often have their password
set to the sAMAccountName in lowercase, minus the trailing `$`. For example,
`MS01$` has password `ms01`. This is a common administrative oversight that
yields machine account credentials with zero noise.

```bash
# Identify pre-created computer accounts and test default passwords
# The module checks for accounts and attempts TGT with default password
nxc ldap DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' -M pre2k
```

**What pre2k checks:**
1. Finds computer accounts in the "Pre-Windows 2000 Compatible Access" group
   or with `userAccountControl` flags indicating pre-creation
2. Tests each account with `sAMAccountName.rstrip('$').lower()` as the password
3. Attempts to obtain a TGT — if successful, the password is confirmed

**Why this matters:**
- Machine accounts often have broad read rights (BloodHound "Owned" marking)
- Machine accounts in groups like "Domain Secure Servers" can read gMSA passwords
- Machine accounts may have constrained delegation, RBCD, or other privileges
- A pre2k computer account is functionally equivalent to a domain user credential
  but with a machine account's group memberships and trust level

If pre2k finds valid machine credentials → write immediately:
`add_credential(username="MACHINE$", secret="machine", source="pre2k module on <DC>")`.
Also record in your return summary: account name, confirmed password, and any
group memberships or privileges visible from LDAP.

### NetExec Module Sweep

Run these modules as a batch during authenticated enumeration. They are all
non-destructive and low-privilege — any domain user can run them.

#### Quick-Win Credential Checks

```bash
# User descriptions — frequently contain cleartext passwords
nxc ldap DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' -M get-desc-users

# GPP cpassword in SYSVOL (MS14-025)
nxc smb DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' -M gpp_password

# Autologon credentials from registry.xml in SYSVOL
nxc smb DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' -M gpp_autologin
```

**User descriptions** are a common source of cleartext passwords — admins often
document initial passwords or service account passwords in the AD description
field. Any result containing password-like strings is a credential finding.
Write immediately: `add_credential(username=..., secret=..., source="AD description field")`.

#### Coercion & Relay Surface

```bash
# WebClient service (WebDAV) — enables HTTP-based NTLM coercion
# Critical: if WebDAV is running, coercion can use HTTP instead of SMB
# which bypasses SMB signing and enables relay to LDAP/ADCS
nxc smb DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' -M webdav

# Print Spooler — enables PrinterBug/SpoolSample coercion
nxc smb DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' -M spooler

# Broad coercion vulnerability check (check-only mode — no LISTENER set)
# Tests for PetitPotam, PrinterBug, DFSCoerce, ShadowCoerce, MSEven, etc.
nxc smb DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' -M coerce_plus
```

Note all coercion-eligible hosts. WebDAV is especially valuable — it enables
HTTP-based coercion that works even when SMB signing is enforced.

**Interim writes:** Coercion-eligible hosts →
`add_vuln(title="Coercion: <type> on <host>", host="<host>", vuln_type="coercion", severity="medium")`.

#### Attack Surface Mapping

```bash
# AV/EDR detection — identifies endpoint security products
nxc smb DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' -M enum_av

# MachineAccountQuota — can current user add computer accounts?
# MAQ > 0 enables resource-based constrained delegation (RBCD) attacks
nxc ldap DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' -M maq

# Obsolete/EOL operating systems — unpatched, vulnerable to known CVEs
nxc ldap DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' -M obsolete

# BadSuccessor (dMSA) — CVE-2025-21293, privilege escalation via
# delegated Managed Service Accounts
nxc ldap DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' -M badsuccessor
```

#### Network Topology

```bash
# DNS records from AD — all A/AAAA/CNAME/SRV records in the domain
nxc ldap DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' -M get-network

# AD Sites and Subnets — reveals internal network segmentation
nxc ldap DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' -M subnets

# Additional network interfaces on hosts (multi-homed pivot targets)
nxc smb DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' -M ioxidresolver
```

#### SCCM and Infrastructure

```bash
# SCCM discovery via LDAP
nxc ldap DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' -M sccm

# Entra ID (Azure AD Connect) sync server
nxc ldap DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' -M entra-id

# DNS zones allowing nonsecure dynamic updates (ADIDNS poisoning)
nxc ldap DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' -M dns-nonsecure
```

If SCCM found → note for SCCM exploitation. If Entra ID Connect server
found → high-value target (stores cleartext AD sync credentials). If
nonsecure DNS updates allowed → note for ADIDNS poisoning (enables
MITM/coercion without LLMNR).

#### ADIDNS Zone ACL Check

**Standard in most AD environments.** Authenticated Users have CreateChild on
AD-Integrated DNS zones by default, allowing any domain user to create new A
records. This enables ADIDNS poisoning: redirect hostnames that don't have DNS
records (or that you can overwrite) to the attackbox for credential capture.

```bash
# Check zone ACL — look for Authenticated Users with CreateChild
# Use dacledit to read the ACL on the DNS zone object
dacledit.py -action read -target-dn \
  'DC=DOMAIN.LOCAL,CN=MicrosoftDNS,DC=DomainDnsZones,DC=DOMAIN,DC=LOCAL' \
  'DOMAIN/user:Password123@DC01.DOMAIN.LOCAL'

# List existing DNS records (look for gaps — hostnames referenced but missing)
# dnstool.py is from krbrelayx toolkit
python3 /opt/krbrelayx/dnstool.py -u 'DOMAIN\user' -p 'Password123' \
  -r '*' --action query DC01.DOMAIN.LOCAL
```

**Cross-reference with engagement state:** Check for unreachable hostnames in
the pivot map or blocked items — linked server data sources, SPN hostnames,
or service references that resolved to nothing. If an expected hostname has no
DNS A record and Authenticated Users can create records, this is a high-value
pivot: create an A record pointing to the attackbox, then capture credentials
when the service authenticates.

**Interim writes:** ADIDNS CreateChild confirmed →
`add_vuln(title="ADIDNS: Authenticated Users can create DNS records", host="<DC>", vuln_type="adidns-poisoning", severity="critical")`.
Cross-reference with unreachable hostnames →
`add_pivot(source="ADIDNS poisoning", destination="<hostname> → attackbox for credential capture", method="Create A record for <hostname> pointing to attackbox, trigger service authentication, capture with Responder")`.

### SPN Enumeration (Kerberoasting Targets)

```bash
# Impacket — list accounts with SPNs
GetUserSPNs.py DOMAIN/user:'Password123' -dc-ip DC_IP

# NetExec
nxc ldap DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' --kerberoasting output.txt

# Rubeus — stats only (no ticket requests)
.\Rubeus.exe kerberoast /stats
```

If SPNs found on user accounts → STOP. Report: DC IP, domain name, SPN list,
current credentials. Do not request or crack service tickets inline.

### AS-REP Roastable Accounts

```bash
# Impacket — enumerate users without pre-auth
GetNPUsers.py DOMAIN/user:'Password123' -dc-ip DC_IP

# bloodyAD — LDAP filter for DONT_REQ_PREAUTH
bloodyAD -u user -p 'Password123' -d DOMAIN.LOCAL --host DC_IP \
  get search --filter '(&(userAccountControl:1.2.840.113556.1.4.803:=4194304)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))' \
  --attr sAMAccountName
```

If found → STOP. Report: DC IP, domain name, AS-REP roastable user list,
current credentials. Do not request or crack AS-REP hashes inline.

### Delegation Enumeration

```bash
# Unconstrained delegation
bloodyAD -u user -p 'Password123' -d DOMAIN.LOCAL --host DC_IP \
  get search --filter '(userAccountControl:1.2.840.113556.1.4.803:=524288)' \
  --attr sAMAccountName,dNSHostName

# Constrained delegation
bloodyAD -u user -p 'Password123' -d DOMAIN.LOCAL --host DC_IP \
  get search --filter '(msDS-AllowedToDelegateTo=*)' \
  --attr sAMAccountName,msDS-AllowedToDelegateTo

# RBCD
bloodyAD -u user -p 'Password123' -d DOMAIN.LOCAL --host DC_IP \
  get search --filter '(msDS-AllowedToActOnBehalfOfOtherIdentity=*)' \
  --attr sAMAccountName

# PowerView
Get-DomainComputer -Unconstrained
Get-DomainUser -TrustedToAuth
Get-DomainComputer -TrustedToAuth
```

**Interim writes:** Delegation paths found →
`add_pivot(source="<account>", destination="<target_service>", method="<unconstrained|constrained|RBCD> delegation")`.

If found → STOP. Report: DC IP, domain name, delegation type and targets,
current credentials. Do not exploit delegation inline.

### Privileged Group Membership

```bash
# AdminCount=1 (privileged group members, may have stale perms)
nxc ldap DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' --admin-count

# Specific dangerous groups
bloodyAD -u user -p 'Password123' -d DOMAIN.LOCAL --host DC_IP \
  get object "DNSAdmins" --attr msds-memberTransitive
bloodyAD -u user -p 'Password123' -d DOMAIN.LOCAL --host DC_IP \
  get object "Backup Operators" --attr msds-memberTransitive
```

### LAPS / gMSA / dMSA

```bash
# LAPS — check if current user can read local admin passwords
nxc ldap DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' -M laps

# gMSA — readable managed service account passwords
nxc ldap DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' --gmsa
```

If readable → STOP. Report: DC IP, domain name, LAPS/gMSA target details,
current credentials. Do not extract managed passwords inline.

### Trust Enumeration

```bash
# NetExec
nxc ldap DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' -M enum_trust

# Impacket
nltest /domain_trusts /all_trusts /v

# PowerView
Get-DomainTrust
Get-NetForestDomain
Get-DomainForeignUser
Get-DomainForeignGroupMember
```

If trusts found → STOP. Report: DC IP, domain name, trust relationships
enumerated, trust types and directions, current credentials. Do not exploit
trust relationships inline.

### Share Enumeration

```bash
# NetExec — find accessible shares
nxc smb 10.10.10.0/24 -u 'user' -p 'Password123' --shares

# Spider shares for sensitive files — use manspider for keyword/regex content search
# manspider runs from the attackbox via Bash (quick pass — orchestrator may task deeper review)
manspider DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' -d DOMAIN \
  -c password passwd cred secret connectionstring
manspider DC01.DOMAIN.LOCAL -u 'user' -p 'Password123' -d DOMAIN \
  -e '(password|passwd|pwd)\s*[=:]\s*\S+' -f xml conf config ini txt ps1 bat vbs kdbx
```

Check SYSVOL/NETLOGON for Group Policy Preferences (GPP) passwords, scripts
with embedded credentials, and configuration files.

**High-value file patterns in shares** — when spidering user home directories,
SYSVOL, or custom shares, look for:

| Pattern | Why |
|---------|-----|
| `*.xml` (especially `azure.xml`, `gpp.xml`, `*.runconfig.xml`) | Azure AD credential exports (`PSADPasswordCredential`), GPP cpassword, deployment configs |
| `Groups.xml`, `Services.xml`, `Scheduledtasks.xml`, `DataSources.xml` | GPP passwords (MS14-025) — in SYSVOL `Policies/` subdirectories |
| `web.config`, `*.config` | .NET connection strings, API keys |
| `*.ps1`, `*.bat`, `*.cmd`, `*.vbs` | Scripts with hardcoded credentials |
| `*.kdbx`, `*.key` | KeePass databases and key files |
| `*.pfx`, `*.p12`, `*.pem` | Certificates and private keys |
| `unattend.xml`, `sysprep.xml` | Deployment credentials |

Download and inspect any XML files found in user home directories — Azure AD
credential exports are a common source of cleartext domain passwords.

### Session Enumeration

```bash
# Where are high-value users logged in?
nxc smb 10.10.10.0/24 -u 'user' -p 'Password123' --sessions
nxc smb 10.10.10.0/24 -u 'user' -p 'Password123' --loggedon-users

# PowerView
Invoke-UserHunter -Stealth
Find-DomainUserLocation
```

### Local Admin Access

```bash
# Where does the current user have local admin?
nxc smb 10.10.10.0/24 -u 'user' -p 'Password123'
# Look for (Pwn3d!) in output

# PowerView
Find-LocalAdminAccess -Verbose
```

If local admin found → STOP. Report: target hostname, local admin
credentials, DC IP, domain name. Do not dump credentials inline.

### SCCM / Deployment

```bash
# SCCM discovery
python3 sccmhunter.py find -u 'user' -p 'Password123' -d DOMAIN.LOCAL -dc-ip DC_IP
```

If SCCM found → STOP. Report: DC IP, domain name, SCCM server details,
current credentials. Do not exploit SCCM inline.

## Step 5: Prioritize and Return

After mapping the attack surface, STOP and return to the orchestrator with all
findings categorized by type and priority.

### Priority Order

When multiple attack paths exist, prioritize by OPSEC and reliability:

1. **Pre-2k computer accounts / GPP passwords / description creds** — instant
   credentials, zero noise, no cracking needed
2. **Kerberos roasting / AS-REP roasting** — offline cracking, low detection
3. **ADCS template abuse** — certificate-based, stealthy, persistent
4. **ACL abuse** — targeted, often unmonitored
5. **Delegation abuse** — Kerberos-based, moderate detection
6. **Password spraying** — risk of lockout, use as last resort for initial access
7. **Coercion/relay** — requires network position, noisy
8. **Credential dumping** — requires existing admin access

### Return Summary

Present all findings with:
- **Multiple paths identified**: Present the top 3 paths ranked by OPSEC and reliability.
- **No clear path**: Recommend expanding enumeration scope (additional subnets,
  different protocols), password spraying, or relay opportunities.
- **Credentials found in shares/GPP**: Report for deeper authenticated enumeration.

When returning, pass along:
- Target user/host/service
- Current credentials and access level
- Domain name and DC hostname
- Relevant enumeration output

## Troubleshooting

### BloodHound Collection Fails

- **LDAP connection refused**: Try port 636 (LDAPS) with `--ssl` flag
- **Access denied**: Verify credentials; any domain user can run BloodHound
- **Timeout**: Use `--CollectionMethod DCOnly` for stealthier, faster collection
- **Missing ADCS data**: Run `certipy find` separately and import JSON into BH CE

### Kerberos Errors

- **KRB_AP_ERR_SKEW**: Clock out of sync (> 5 minutes from DC). This is a
  **Clock Skew Interrupt** — stop immediately and return to the orchestrator.
  Do not retry or fall back to NTLM. Return to orchestrator — clock sync
  requires sudo which subagents cannot run.
- **KDC cannot find the name**: Use FQDN hostnames, not IP addresses. If
  hostnames don't resolve, return to orchestrator with the hostnames and IPs
  — the orchestrator handles `/etc/hosts` updates (requires sudo).
- **Do NOT run `sudo` or modify `/etc/hosts`** — subagents lack sudo. Report
  unresolvable hostnames in your return summary.

### NetExec Connection Issues

- **SMB SessionError STATUS_NOT_SUPPORTED**: Target may require SMBv3 or
  NTLMv2. Try `--smb2` flag
- **Connection timed out**: Host may be down or firewalled. Try different
  protocols (LDAP, WinRM, RDP)

### bloodyAD LDAP Filter Errors

LDAP filters with `!` (NOT operator) can fail due to bash history expansion.
Always use single quotes around filters, not double quotes:

```bash
# CORRECT — single quotes prevent ! expansion
bloodyAD ... get search --filter '(!(userAccountControl:1.2.840.113556.1.4.803:=2))'

# WRONG — double quotes cause bash to interpret ! as history expansion
bloodyAD ... get search --filter "(!(userAccountControl...))"
```

If filters still fail, simplify by removing the NOT clause and filtering the
output with `grep -v` instead.

### Impacket Tool Naming

Impacket tools may be installed under different names depending on the system:

| Packaged (pip/apt) | Script name | Both work |
|--------------------|-------------|-----------|
| `impacket-getTGT` | `getTGT.py` | Same tool |
| `impacket-GetUserSPNs` | `GetUserSPNs.py` | Same tool |
| `impacket-GetNPUsers` | `GetNPUsers.py` | Same tool |
| `impacket-secretsdump` | `secretsdump.py` | Same tool |

Check which form is available before use:

```bash
which getTGT.py 2>/dev/null || which impacket-getTGT 2>/dev/null
```

The `.py` form is common on manually-installed Impacket; the `impacket-` prefix
comes from pip/apt packages.

### NoPac Scanner False Positives

The `nxc ldap -M nopac` scanner compares TGT sizes with and without PAC. The
target is **only vulnerable when `tgt_no_pac < tgt_with_pac`** (different sizes).
If both sizes are equal (e.g., `1548 == 1548`), the target is **NOT vulnerable**
— the PAC was not removed, meaning the patch is applied. Do not report equal
PAC sizes as a NoPac vulnerability.

### No Credentials Available

Start with:
1. RID cycling for username list
2. AS-REP roasting against discovered usernames
3. LLMNR/NBT-NS poisoning (if on-network)
4. Password spraying with common passwords
5. Check for anonymous LDAP bind (`nxc ldap DC -u '' -p ''`)
