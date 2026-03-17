---
name: Hacking Fundamentals
description: This skill should be used when the user asks to "understand hacking basics", "learn about hacker types", "understand network protocols", "learn DNS concepts", "understand attack types", or "explore security tool categories". It provides foundational cybersecurity knowledge.
version: 1.0.0
tags: [hacking, fundamentals, networking, DNS, protocols, attacks]
---

# Hacking Fundamentals

## Purpose

Provide foundational knowledge of hacking concepts, network protocols, attack methodologies, and security tools. This skill covers essential theory for aspiring penetration testers and security professionals including network architecture, DNS operations, attack classifications, and tool categories.

## Prerequisites

### Required Knowledge
- Basic computer literacy
- Understanding of operating systems
- Familiarity with command-line interfaces

### Recommended Background
- Networking concepts
- TCP/IP fundamentals
- Basic security awareness

## Outputs and Deliverables

1. **Conceptual Understanding** - Hacking terminology and classifications
2. **Network Knowledge** - Protocol and architecture comprehension
3. **Attack Recognition** - Active and passive attack identification
4. **Tool Familiarity** - Security tool categories and applications

## Core Workflow

### Phase 1: Hacker Classifications

Understanding hacker types and motivations:

**White Hat Hackers**
- Ethical hackers and security professionals
- Perform authorized penetration testing
- Work to improve organizational security
- Also called: penetration testers, sneakers, red teams

**Black Hat Hackers**
- Malicious actors seeking unauthorized access
- Breach systems for profit or damage
- Also known as crackers
- Target selection: reconnaissance → information gathering → attack

**Grey Hat Hackers**
- Operate between ethical and malicious
- May act illegally with good intentions
- Often disclose vulnerabilities publicly
- Not motivated by personal gain

**Other Categories**
- **Blue Hat**: External consultants testing systems pre-launch
- **Elite Hackers**: Highly skilled, discover zero-days
- **Script Kiddies**: Use pre-made tools without understanding
- **Hacktivists**: Politically or socially motivated
- **Nation State**: Government-sponsored cyber operatives

### Phase 2: Network Fundamentals

Understanding network types and architecture:

**Network Types**
| Type | Description |
|------|-------------|
| LAN | Local Area Network - computers in same building |
| WAN | Wide Area Network - geographically distributed |
| MAN | Metropolitan Area Network - city-wide coverage |
| VPN | Virtual Private Network - encrypted tunnel |
| Intranet | Private internal company network |
| Extranet | Extended intranet for external partners |

**Network Benefits for Attackers**
- Resource sharing creates attack surfaces
- File sharing enables data exfiltration
- Program sharing may expose vulnerabilities
- Centralized services create single points of failure

### Phase 3: Protocol Understanding

Key protocols for security assessment:

**IP Addressing**
```bash
# Private IP ranges (non-routable)
10.0.0.0 - 10.255.255.255        # Class A
172.16.0.0 - 172.31.255.255      # Class B
192.168.0.0 - 192.168.255.255    # Class C

# Find your IP
ipconfig /all                     # Windows
ip addr                           # Linux
curl ifconfig.me                  # Public IP
```

**Common Protocols**
| Protocol | Port | Purpose |
|----------|------|---------|
| FTP | 20, 21 | File transfer |
| SSH | 22 | Secure remote access |
| Telnet | 23 | Unencrypted remote access |
| SMTP | 25 | Email transmission |
| DNS | 53 | Name resolution |
| HTTP | 80 | Web traffic |
| POP3 | 110 | Email retrieval |
| IMAP | 143 | Email access |
| HTTPS | 443 | Encrypted web traffic |
| RDP | 3389 | Windows remote desktop |

**SSH Capabilities**
- Secure encrypted remote login
- Protection against IP spoofing
- Port forwarding/tunneling
- Replacement for rlogin, rsh, rcp

```bash
# SSH connection
ssh user@target.com

# SSH tunneling (port forwarding)
ssh -L 8080:localhost:80 user@target.com

# Dynamic port forwarding (SOCKS proxy)
ssh -D 9050 user@target.com
```

### Phase 4: DNS Architecture

Understand Domain Name System operations:

**DNS Hierarchy**
```
Root (.)
├── .com (gTLD)
│   └── example.com
│       └── www.example.com
├── .org (gTLD)
├── .net (gTLD)
└── .uk (ccTLD - Country Code)
```

**DNS Record Types**
| Record | Purpose |
|--------|---------|
| A | Maps hostname to IPv4 address |
| AAAA | Maps hostname to IPv6 address |
| PTR | Reverse lookup (IP to hostname) |
| NS | Authoritative name servers |
| MX | Mail exchange servers |
| CNAME | Canonical name (alias) |
| TXT | Text records (SPF, DKIM) |
| SOA | Start of authority |

**DNS Query Process**
1. Client queries local DNS resolver
2. Resolver checks cache
3. If not cached, query root servers
4. Root refers to TLD servers (.com)
5. TLD refers to authoritative nameserver
6. Authoritative returns IP address
7. Resolver caches and returns to client

**DNS Enumeration Commands**
```bash
# Basic DNS lookup
nslookup target.com
dig target.com

# Specific record types
dig target.com MX         # Mail servers
dig target.com NS         # Name servers
dig target.com TXT        # Text records
dig target.com AXFR       # Zone transfer attempt

# Reverse lookup
dig -x 192.168.1.1

# Use specific DNS server
dig @8.8.8.8 target.com
```

### Phase 5: Proxy Servers

Understanding proxy types and uses:

**Proxy Types**
| Type | Description |
|------|-------------|
| Anonymous | Hides client IP from server |
| High Anonymity | Doesn't identify as proxy |
| Transparent | Forwards requests without hiding identity |
| Reverse | Protects backend servers |

**Proxy for Security Testing**
```bash
# Configure proxy in terminal
export http_proxy=http://proxy:port
export https_proxy=http://proxy:port

# Burp Suite default proxy
http://127.0.0.1:8080

# Tor SOCKS proxy
socks5://127.0.0.1:9050
```

**Privacy Benefits**
- Mask source IP address
- Bypass geographic restrictions
- Encrypted tunnels for sensitive traffic
- Chain proxies for enhanced anonymity

### Phase 6: Active Attack Types

Attacks requiring direct interaction:

**Masquerade Attack**
- Attacker impersonates legitimate user
- Uses stolen credentials or session tokens
- Exploits authentication weaknesses
- Gains unauthorized privileges

**Session Replay Attack**
- Captures valid session tokens
- Replays authentication to gain access
- Requires interception of session data
- Mitigated by session timeouts and tokens

**Message Modification Attack**
- Intercepts data in transit
- Modifies packet headers or content
- Redirects traffic to malicious destinations
- Man-in-the-middle variations

**Denial of Service (DoS)**
- Overwhelms target with traffic
- Depletes system resources
- Prevents legitimate access
- Variations: SYN flood, UDP flood, HTTP flood

**Distributed DoS (DDoS)**
- Multiple sources attack single target
- Uses botnet/zombie networks
- Harder to mitigate than single-source
- Amplification attacks multiply traffic

### Phase 7: Passive Attack Types

Attacks gathering information without detection:

**Passive Reconnaissance**
- Monitors without interaction
- Session capture and analysis
- Network traffic sniffing
- No direct engagement with target

**Active Reconnaissance**
- Engages with target system
- Port scanning
- Service enumeration
- Banner grabbing

**Specific Techniques**
- **War Driving**: Detecting vulnerable WiFi networks
- **Dumpster Diving**: Searching discarded materials
- **Shoulder Surfing**: Observing user activity
- **Promiscuous Mode**: Capturing all network traffic

### Phase 8: Password Cracking Tools

Tools for password recovery and testing:

**Online Attack Tools**
```bash
# Hydra - network password cracker
hydra -l admin -P wordlist.txt ssh://target.com
hydra -L users.txt -P passwords.txt ftp://target.com

# Medusa - parallel password cracker
medusa -h target.com -u admin -P wordlist.txt -M ssh

# Ncrack - network authentication cracker
ncrack -p 22 --user admin -P wordlist.txt target.com
```

**Offline Attack Tools**
```bash
# John the Ripper
john --wordlist=rockyou.txt hashes.txt
john --show hashes.txt

# Hashcat - GPU-accelerated
hashcat -m 0 hashes.txt rockyou.txt      # MD5
hashcat -m 1000 hashes.txt rockyou.txt   # NTLM

# Ophcrack - Windows password cracker
ophcrack -g -d tables -t tables -f hash.txt
```

**WiFi Password Tools**
```bash
# Aircrack-ng suite
airmon-ng start wlan0
airodump-ng wlan0mon
airodump-ng -c [channel] --bssid [BSSID] -w capture wlan0mon
aireplay-ng -0 10 -a [BSSID] wlan0mon
aircrack-ng -w wordlist.txt capture.cap
```

### Phase 9: Network Scanning Tools

Tools for discovery and enumeration:

**Nmap - Network Mapper**
```bash
# Host discovery
nmap -sn 192.168.1.0/24

# Port scanning
nmap -sS target.com              # SYN scan
nmap -sV target.com              # Version detection
nmap -O target.com               # OS detection
nmap -A target.com               # Aggressive scan
nmap -p- target.com              # All ports

# Script scanning
nmap --script=vuln target.com
nmap --script=http-enum target.com
```

**Traffic Analysis Tools**
```bash
# Wireshark - GUI packet analyzer
wireshark

# tcpdump - CLI packet capture
tcpdump -i eth0 -w capture.pcap
tcpdump -r capture.pcap

# Ettercap - MITM tool
ettercap -T -M arp:remote /target1// /target2//
```

**Web Scanning**
```bash
# Nikto - web vulnerability scanner
nikto -h http://target.com

# Skipfish - web application scanner
skipfish -o output http://target.com

# W3af - web attack framework
w3af_console
```

### Phase 10: Forensics and Debugging Tools

Tools for investigation and analysis:

**Digital Forensics**
| Tool | Purpose |
|------|---------|
| Sleuth Kit | Disk image analysis |
| Autopsy | GUI for Sleuth Kit |
| Volatility | Memory forensics |
| FTK Imager | Disk imaging |
| Encase | Enterprise forensics |

**File System Analysis**
```bash
# Sleuth Kit commands
fls -r image.dd               # List files recursively
icat image.dd [inode]         # Extract file by inode
mmls image.dd                 # Partition layout

# Volatility memory analysis
volatility -f memory.dmp imageinfo
volatility -f memory.dmp --profile=Win7SP1x64 pslist
volatility -f memory.dmp --profile=Win7SP1x64 netscan
```

**Packet Crafting**
```bash
# Scapy - Python packet manipulation
from scapy.all import *
packet = IP(dst="target.com")/TCP(dport=80)
send(packet)

# Hping3 - packet crafting
hping3 -S target.com -p 80     # SYN packet
hping3 --flood target.com       # Flood mode
```

## Quick Reference

### Essential Ports

| Port | Service | Notes |
|------|---------|-------|
| 21 | FTP | File transfer |
| 22 | SSH | Secure shell |
| 23 | Telnet | Unencrypted |
| 25 | SMTP | Email |
| 53 | DNS | Name resolution |
| 80 | HTTP | Web |
| 443 | HTTPS | Secure web |
| 445 | SMB | Windows shares |
| 3389 | RDP | Remote desktop |

### Attack Type Summary

| Attack | Type | Goal |
|--------|------|------|
| DoS/DDoS | Active | Deny availability |
| Masquerade | Active | Impersonate user |
| Session Replay | Active | Steal access |
| War Driving | Passive | Find WiFi |
| Sniffing | Passive | Capture traffic |

### Tool Categories

| Category | Examples |
|----------|----------|
| Password | Hydra, John, Hashcat |
| Scanning | Nmap, Nessus, Nikto |
| Traffic | Wireshark, tcpdump |
| Forensics | Sleuth Kit, Volatility |
| Exploitation | Metasploit, Burp Suite |

## Constraints and Limitations

### Legal Considerations
- Only test systems with authorization
- Document all testing activities
- Understand local cybercrime laws
- Obtain written permission before testing

### Ethical Guidelines
- White hat mindset required
- Report vulnerabilities responsibly
- Protect discovered data
- Never cause unnecessary harm

## Troubleshooting

### Network Issues

**Cannot reach target:**
1. Verify network connectivity
2. Check firewall rules
3. Confirm target is online
4. Try different ports/protocols

### Tool Failures

**Scans returning no results:**
1. Verify target address
2. Check for IDS/IPS blocking
3. Try slower scan rates
4. Use different techniques
