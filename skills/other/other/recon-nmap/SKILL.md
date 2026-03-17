---
name: recon-nmap
description: >
  Network reconnaissance and security auditing using Nmap for port scanning, service enumeration,
  and vulnerability detection. Use when: (1) Conducting authorized network reconnaissance and asset
  discovery, (2) Enumerating network services and identifying running versions, (3) Detecting
  security vulnerabilities through NSE scripts, (4) Mapping network topology and firewall rules,
  (5) Performing compliance scanning for security assessments, (6) Validating network segmentation
  and access controls.
version: 0.1.0
maintainer: sirappsec@gmail.com
category: offsec
tags: [reconnaissance, nmap, port-scanning, service-enumeration, network-security, osint]
frameworks: [MITRE-ATT&CK, OWASP, PTES]
dependencies:
  packages: [nmap]
  tools: [python3, masscan]
references:
  - https://nmap.org/book/
  - https://nmap.org/nsedoc/
  - https://attack.mitre.org/techniques/T1046/
---

# Nmap Network Reconnaissance

## Overview

Nmap (Network Mapper) is the industry-standard tool for network discovery, security auditing, and vulnerability assessment. This skill provides structured workflows for authorized reconnaissance operations including port scanning, service enumeration, OS fingerprinting, and vulnerability detection using Nmap Scripting Engine (NSE).

**IMPORTANT**: Network scanning may be disruptive and must only be conducted with proper authorization. Always ensure written permission before scanning networks or systems you do not own.

## Quick Start

Basic host discovery and port scanning:

```bash
# Quick scan of common ports
nmap -F <target-ip>

# Scan top 1000 ports with service detection
nmap -sV <target-ip>

# Comprehensive scan with OS detection and default scripts
nmap -A <target-ip>
```

## Core Workflow

### Network Reconnaissance Workflow

Progress:
[ ] 1. Verify authorization and scope
[ ] 2. Perform host discovery and asset enumeration
[ ] 3. Conduct port scanning on live hosts
[ ] 4. Enumerate services and versions
[ ] 5. Perform OS fingerprinting and detection
[ ] 6. Run NSE scripts for vulnerability detection
[ ] 7. Document findings and generate reports
[ ] 8. Validate results and identify false positives

Work through each step systematically. Check off completed items.

### 1. Authorization Verification

**CRITICAL**: Before any scanning activities:
- Confirm written authorization from network owner
- Review scope document for in-scope IP ranges and domains
- Verify scanning windows and rate-limiting requirements
- Document emergency contact for accidental disruption
- Confirm blacklisted hosts (production databases, critical infrastructure)

### 2. Host Discovery

Identify live hosts in target network:

```bash
# Ping sweep (ICMP echo)
nmap -sn <target-network>/24

# ARP scan (local network only, faster and more reliable)
nmap -sn -PR <target-network>/24

# TCP SYN ping (when ICMP blocked)
nmap -sn -PS22,80,443 <target-network>/24

# UDP ping (for hosts blocking TCP)
nmap -sn -PU53,161 <target-network>/24

# Disable ping, assume all hosts alive
nmap -Pn <target-network>/24
```

**Host discovery techniques**:
- **ICMP Echo (-PE)**: Standard ping, often blocked
- **TCP SYN (-PS)**: Half-open connection to specified ports
- **TCP ACK (-PA)**: Sends ACK packets, useful for stateful firewalls
- **UDP (-PU)**: Sends UDP packets to specified ports
- **ARP (-PR)**: Layer 2 discovery, only works on local network

Output live hosts to file for subsequent scanning:

```bash
nmap -sn <target-network>/24 -oG - | awk '/Up$/{print $2}' > live_hosts.txt
```

### 3. Port Scanning

Scan discovered hosts for open ports:

```bash
# Fast scan (top 100 ports)
nmap -F -iL live_hosts.txt

# Top 1000 ports (default)
nmap -iL live_hosts.txt

# Scan all 65535 ports
nmap -p- -iL live_hosts.txt

# Scan specific ports
nmap -p 22,80,443,3389,8080 -iL live_hosts.txt

# Scan port ranges
nmap -p 1-1024,3000-9000 -iL live_hosts.txt
```

**Scan techniques**:

- **TCP SYN Scan (-sS)**: Default, stealthy half-open scan (requires root)
  ```bash
  sudo nmap -sS <target-ip>
  ```

- **TCP Connect Scan (-sT)**: Full TCP connection (no root required)
  ```bash
  nmap -sT <target-ip>
  ```

- **UDP Scan (-sU)**: Scan UDP ports (slow but critical)
  ```bash
  sudo nmap -sU -p 53,161,500 <target-ip>
  ```

- **Version Detection (-sV)**: Probe services for version information
  ```bash
  nmap -sV <target-ip>
  ```

- **Aggressive Scan (-A)**: Enable OS detection, version detection, script scanning, traceroute
  ```bash
  sudo nmap -A <target-ip>
  ```

**Timing and performance**:

```bash
# Paranoid (0) - Extremely slow, IDS evasion
nmap -T0 <target-ip>

# Sneaky (1) - Very slow, IDS evasion
nmap -T1 <target-ip>

# Polite (2) - Slows down to use less bandwidth
nmap -T2 <target-ip>

# Normal (3) - Default timing
nmap -T3 <target-ip>

# Aggressive (4) - Faster, assumes reliable network
nmap -T4 <target-ip>

# Insane (5) - Very fast, may miss results
nmap -T5 <target-ip>
```

**Rate limiting for safety**:

```bash
# Limit to 100 packets/second
nmap --max-rate 100 <target-ip>

# Minimum 10 packets/second
nmap --min-rate 10 <target-ip>

# Scan with delays to avoid detection
nmap --scan-delay 1s <target-ip>
```

### 4. Service Enumeration

Identify services and extract version information:

```bash
# Service version detection
nmap -sV <target-ip>

# Aggressive version detection (more probes)
nmap -sV --version-intensity 5 <target-ip>

# Light version detection (fewer probes, faster)
nmap -sV --version-intensity 0 <target-ip>

# Specific service enumeration
nmap -sV -p 80,443 --script=http-headers,http-title <target-ip>
```

**Service-specific enumeration**:

```bash
# SMB enumeration
nmap -p 445 --script=smb-os-discovery,smb-security-mode <target-ip>

# SSH enumeration
nmap -p 22 --script=ssh-hostkey,ssh-auth-methods <target-ip>

# DNS enumeration
nmap -p 53 --script=dns-nsid,dns-recursion <target-ip>

# HTTP/HTTPS enumeration
nmap -p 80,443 --script=http-methods,http-robots.txt,http-title <target-ip>

# Database enumeration
nmap -p 3306 --script=mysql-info <target-ip>
nmap -p 5432 --script=pgsql-brute <target-ip>
nmap -p 1433 --script=ms-sql-info <target-ip>
```

### 5. Operating System Detection

Identify target operating systems:

```bash
# OS detection
sudo nmap -O <target-ip>

# Aggressive OS detection with version scanning
sudo nmap -A <target-ip>

# Limit OS detection to promising targets
sudo nmap -O --osscan-limit <target-ip>

# Guess OS aggressively
sudo nmap -O --osscan-guess <target-ip>
```

**OS fingerprinting indicators**:
- TCP/IP stack characteristics
- Open port patterns
- Service banners and versions
- TTL values and TCP window sizes

### 6. NSE Script Scanning

Nmap Scripting Engine for advanced reconnaissance and vulnerability detection:

```bash
# Run default NSE scripts
nmap -sC <target-ip>

# Run all scripts in category
nmap --script=vuln <target-ip>
nmap --script=exploit <target-ip>
nmap --script=discovery <target-ip>

# Run specific script
nmap --script=http-sql-injection <target-ip>

# Multiple scripts
nmap --script=smb-vuln-ms17-010,smb-vuln-cve-2017-7494 <target-ip>

# Script with arguments
nmap --script=http-brute --script-args http-brute.path=/admin <target-ip>
```

**NSE script categories**:
- **auth**: Authentication testing
- **broadcast**: Network broadcast/multicast discovery
- **brute**: Brute-force password auditing
- **default**: Default safe scripts (-sC)
- **discovery**: Network and service discovery
- **dos**: Denial of service testing (use with caution)
- **exploit**: Exploitation attempts (authorized only)
- **external**: External resource queries (WHOIS, etc.)
- **fuzzer**: Fuzzing attacks
- **intrusive**: Intrusive scanning (may crash services)
- **malware**: Malware detection
- **safe**: Safe scripts unlikely to crash services
- **version**: Version detection enhancement
- **vuln**: Vulnerability detection

**Common vulnerability detection scripts**:

```bash
# Check for EternalBlue (MS17-010)
nmap -p 445 --script=smb-vuln-ms17-010 <target-ip>

# Heartbleed detection
nmap -p 443 --script=ssl-heartbleed <target-ip>

# Shellshock detection
nmap --script=http-shellshock --script-args uri=/cgi-bin/test.sh <target-ip>

# Check for weak SSL/TLS
nmap -p 443 --script=ssl-enum-ciphers <target-ip>

# SQL injection testing
nmap -p 80 --script=http-sql-injection <target-ip>

# Check for anonymous FTP
nmap -p 21 --script=ftp-anon <target-ip>
```

### 7. Output and Reporting

Generate reports in multiple formats:

```bash
# Normal output to screen and file
nmap <target-ip> -oN scan_results.txt

# XML output (for parsing/import)
nmap <target-ip> -oX scan_results.xml

# Grepable output (for easy parsing)
nmap <target-ip> -oG scan_results.gnmap

# All formats
nmap <target-ip> -oA scan_results

# Script kiddie output (for fun)
nmap <target-ip> -oS scan_results.skid
```

Convert and process results:

```bash
# Convert XML to HTML report
xsltproc /usr/share/nmap/nmap.xsl scan_results.xml -o report.html

# Parse XML with Python
python3 -c "import xml.etree.ElementTree as ET; tree = ET.parse('scan_results.xml'); root = tree.getroot(); [print(host.find('address').get('addr')) for host in root.findall('host')]"

# Extract open ports from grepable output
grep 'Ports:' scan_results.gnmap | awk '{print $2, $5}'
```

### 8. Firewall and IDS Evasion

Techniques to evade detection (authorized testing only):

```bash
# Fragment packets
sudo nmap -f <target-ip>

# Use decoys
sudo nmap -D RND:10 <target-ip>
sudo nmap -D decoy1,decoy2,ME,decoy3 <target-ip>

# Spoof source IP (requires raw packet privileges)
sudo nmap -S <spoofed-ip> -e <interface> <target-ip>

# Randomize target order
nmap --randomize-hosts -iL targets.txt

# Use proxy
nmap --proxies http://proxy:8080 <target-ip>

# Idle scan (zombie host required)
sudo nmap -sI <zombie-host> <target-ip>
```

## Security Considerations

### Authorization & Legal Compliance

- **Written Permission**: Obtain explicit authorization before scanning any network
- **Scope Definition**: Only scan explicitly authorized IP ranges and ports
- **Disruption Risk**: Some scans (DOS, exploit scripts) can crash services
- **Privacy**: Service enumeration may expose sensitive information
- **Log Traces**: Scanning activities are typically logged by firewalls and IDS

### Operational Security

- **Rate Limiting**: Use `--max-rate` to avoid overwhelming targets
- **Timing**: Schedule scans during approved maintenance windows
- **Bandwidth**: Consider network impact, especially for large scans
- **Noise**: Aggressive scans are easily detected by security monitoring
- **False Positives**: Validate findings before reporting vulnerabilities

### Audit Logging

Document all reconnaissance activities:
- Scan start and end timestamps
- Source IP address and scanner hostname
- Target IP ranges and ports scanned
- Nmap command-line arguments used
- Number of hosts discovered and ports found
- Vulnerabilities identified via NSE scripts
- Any service disruptions or anomalies

### Compliance

- **PTES**: Reconnaissance phase of Penetration Testing Execution Standard
- **OWASP**: ASVS verification requirements for network security
- **MITRE ATT&CK**: T1046 (Network Service Scanning)
- **PCI-DSS 11.2**: External and internal vulnerability scanning
- **ISO 27001**: A.12.6 Technical vulnerability management

## Common Patterns

### Pattern 1: External Perimeter Assessment

```bash
# Phase 1: Identify live hosts
nmap -sn -PE -PS80,443 -PA3389 <external-network>/24 -oG - | awk '/Up$/{print $2}' > external_hosts.txt

# Phase 2: Scan common external services
nmap -Pn -sV -p 21,22,25,53,80,110,143,443,587,993,995,3389,8080,8443 -iL external_hosts.txt -oA external_scan

# Phase 3: Vulnerability detection
nmap -Pn -sV --script=vuln -p 21,22,25,80,443,3389,8080,8443 -iL external_hosts.txt -oA external_vulns

# Phase 4: SSL/TLS security audit
nmap -Pn -p 443,8443 --script=ssl-enum-ciphers,ssl-cert -iL external_hosts.txt -oA ssl_audit
```

### Pattern 2: Internal Network Mapping

```bash
# Phase 1: Fast host discovery
nmap -sn -PR <internal-network>/24 -oG - | awk '/Up$/{print $2}' > internal_hosts.txt

# Phase 2: Comprehensive port scan
nmap -sV -p- -T4 -iL internal_hosts.txt -oA internal_full_scan

# Phase 3: OS fingerprinting
sudo nmap -O -iL internal_hosts.txt -oA internal_os_detection

# Phase 4: Service enumeration
nmap -sV --script=default,discovery -iL internal_hosts.txt -oA internal_services
```

### Pattern 3: Web Application Discovery

```bash
# Identify web servers
nmap -p 80,443,8000,8080,8443 --open -oG - <target-network>/24 | grep 'open' | awk '{print $2}' > web_servers.txt

# Enumerate web technologies
nmap -sV -p 80,443,8080,8443 --script=http-enum,http-headers,http-methods,http-title,http-server-header -iL web_servers.txt -oA web_enum

# Check for common web vulnerabilities
nmap -p 80,443 --script=http-sql-injection,http-csrf,http-vuln-cve2017-5638 -iL web_servers.txt -oA web_vulns
```

### Pattern 4: SMB/CIFS Security Audit

```bash
# Enumerate SMB hosts
nmap -p 445 --open <target-network>/24 -oG - | grep 'open' | awk '{print $2}' > smb_hosts.txt

# SMB version and configuration
nmap -p 445 --script=smb-protocols,smb-security-mode,smb-os-discovery -iL smb_hosts.txt -oA smb_enum

# Check for SMB vulnerabilities
nmap -p 445 --script=smb-vuln* -iL smb_hosts.txt -oA smb_vulns

# Enumerate shares (authentication may be required)
nmap -p 445 --script=smb-enum-shares,smb-enum-users -iL smb_hosts.txt -oA smb_shares
```

### Pattern 5: Database Server Discovery

```bash
# Scan for common database ports
nmap -sV -p 1433,1521,3306,5432,5984,6379,9200,27017 <target-network>/24 -oA database_scan

# MySQL enumeration
nmap -p 3306 --script=mysql-info,mysql-databases,mysql-variables <target-ip>

# PostgreSQL enumeration
nmap -p 5432 --script=pgsql-brute <target-ip>

# MongoDB enumeration
nmap -p 27017 --script=mongodb-info,mongodb-databases <target-ip>

# Redis enumeration
nmap -p 6379 --script=redis-info <target-ip>
```

## Integration Points

### CI/CD Integration

Automated security scanning in pipelines:

```bash
#!/bin/bash
# ci_network_scan.sh - Continuous network security validation

TARGET_NETWORK="$1"
OUTPUT_DIR="scan_results/$(date +%Y%m%d_%H%M%S)"

mkdir -p "$OUTPUT_DIR"

# Quick security scan
nmap -Pn -sV --script=vuln -p 21,22,25,80,443,3389,8080 \
  "$TARGET_NETWORK" -oA "$OUTPUT_DIR/security_scan"

# Parse results for critical findings
if grep -i "VULNERABLE" "$OUTPUT_DIR/security_scan.nmap"; then
  echo "CRITICAL: Vulnerabilities detected!"
  exit 1
fi

echo "Security scan completed successfully"
exit 0
```

### Security Tools Integration

- **Metasploit Integration**: Import Nmap XML with `db_import`
- **Vulnerability Scanners**: Feed Nmap results to Nessus, OpenVAS, Qualys
- **SIEM Integration**: Parse Nmap output for security monitoring
- **Asset Management**: Update CMDB with discovered hosts and services
- **Shodan/Censys**: Validate external exposure findings

### MITRE ATT&CK Mapping

Map Nmap reconnaissance to ATT&CK framework:

- **Reconnaissance**: T1595 (Active Scanning)
  - T1595.001 (Scanning IP Blocks)
  - T1595.002 (Vulnerability Scanning)
- **Discovery**: T1046 (Network Service Scanning)
- **Discovery**: T1040 (Network Sniffing)
- **Credential Access**: T1110 (Brute Force) - when using NSE brute scripts

## Troubleshooting

### Issue: No Results Despite Hosts Being Online

**Causes**:
- ICMP blocked by firewall
- Host-based firewall dropping probes
- Network ACLs filtering traffic

**Solutions**:
```bash
# Skip ping, assume all hosts up
nmap -Pn <target-ip>

# Try TCP ping instead of ICMP
nmap -PS80,443 -PA3389 <target-ip>

# Try multiple discovery techniques
nmap -PE -PS22,80,443 -PA3389 -PU53,161 <target-ip>
```

### Issue: Scan Too Slow

**Solutions**:
```bash
# Increase timing template
nmap -T4 <target-ip>

# Scan fewer ports
nmap -F <target-ip>  # Top 100 ports
nmap --top-ports 1000 <target-ip>

# Parallelize by splitting targets
nmap -T4 192.168.1.1-50 &
nmap -T4 192.168.1.51-100 &
nmap -T4 192.168.1.101-150 &
wait

# Use masscan for very fast port scanning
masscan -p 1-65535 --rate 10000 <target-network>/24
```

### Issue: False Positives in Vulnerability Scripts

**Solutions**:
- Manually verify findings with specific exploit tools
- Check service version against CVE databases
- Use `--version-intensity 9` for more accurate version detection
- Run vulnerability-specific NSE scripts instead of broad categories
- Cross-reference with authenticated vulnerability scanners

### Issue: Getting Blocked by Firewall/IDS

**Solutions**:
```bash
# Slow down scan
nmap -T1 --scan-delay 1s <target-ip>

# Fragment packets
sudo nmap -f <target-ip>

# Randomize scan order
nmap --randomize-hosts -iL targets.txt

# Use source port 53 (often allowed)
nmap -g 53 <target-ip>

# Split into smaller scans over time
nmap -p 1-1000 <target-ip>
# Wait several hours
nmap -p 1001-2000 <target-ip>
```

## Defensive Considerations

Organizations can detect Nmap scanning by:

- **Network IDS**: Signature detection of scan patterns (vertical/horizontal sweeps)
- **Firewall Logs**: Multiple connection attempts from single source
- **Port Scan Detection**: Monitoring for SYN packets without completion
- **Honeypots**: Triggering alerts when accessing decoy services
- **Traffic Analysis**: Unusual packet patterns (fragmentation, timing anomalies)

Enhance defensive posture:
- Deploy network intrusion detection systems (Snort, Suricata)
- Enable firewall logging and monitor for scan patterns
- Use port knocking or service hiding for sensitive services
- Implement rate limiting on border firewalls
- Deploy honeypots to detect and track reconnaissance

## References

- [Nmap Network Scanning Official Guide](https://nmap.org/book/)
- [NSE Script Documentation](https://nmap.org/nsedoc/)
- [MITRE ATT&CK: Network Service Scanning](https://attack.mitre.org/techniques/T1046/)
- [PTES Technical Guidelines](http://www.pentest-standard.org/index.php/Intelligence_Gathering)
- [OWASP Testing Guide: Information Gathering](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/01-Information_Gathering/)
