---
name: Network Ports Reference
description: |
  The assistant provides comprehensive network port and protocol reference information for security assessments and penetration testing. Activate when users ask about "port numbers," "common ports," "service ports," "TCP/UDP ports," "what runs on port X," or "protocol identification."
version: "1.0.0"
tags:
  - networking
  - ports
  - protocols
  - reconnaissance
  - enumeration
---

# Network Ports Reference

## Purpose

Provide quick reference for TCP/UDP port numbers and their associated protocols during reconnaissance, enumeration, and security assessments. Enable rapid identification of services running on target systems and support port-based attack surface mapping.

## Inputs/Prerequisites

- Target IP address or hostname for port scanning
- Network access to the target system
- Port scanning tools (nmap, masscan, netcat)
- Basic understanding of TCP/IP networking

## Outputs/Deliverables

- Identified open ports and associated services
- Protocol-specific enumeration data
- Service version information
- Attack surface documentation
- Port-to-vulnerability mapping

## Core Workflow

### 1. Identify Common Service Ports

Reference these critical ports during reconnaissance:

| Port | Protocol | Service |
|------|----------|---------|
| 20 | TCP | FTP Data Transfer |
| 21 | TCP | FTP Control |
| 22 | TCP | SSH |
| 23 | TCP | Telnet |
| 25 | TCP | SMTP |
| 53 | TCP/UDP | DNS |
| 67-68 | UDP | DHCP |
| 69 | UDP | TFTP |
| 80 | TCP | HTTP |
| 88 | TCP | Kerberos |
| 110 | TCP | POP3 |
| 111 | TCP/UDP | RPC Portmapper |
| 119 | TCP | NNTP |
| 123 | UDP | NTP |
| 135 | TCP | MS RPC |
| 137-139 | TCP/UDP | NetBIOS |
| 143 | TCP | IMAP |
| 161-162 | UDP | SNMP |
| 389 | TCP | LDAP |
| 443 | TCP | HTTPS |
| 445 | TCP | SMB/CIFS |
| 465 | TCP | SMTPS |
| 500 | UDP | IKE/IPSec |
| 514 | UDP | Syslog |
| 587 | TCP | SMTP Submission |
| 636 | TCP | LDAPS |
| 993 | TCP | IMAPS |
| 995 | TCP | POP3S |
| 1433 | TCP | MS SQL |
| 1521 | TCP | Oracle DB |
| 2049 | TCP | NFS |
| 3306 | TCP | MySQL |
| 3389 | TCP | RDP |
| 5432 | TCP | PostgreSQL |
| 5900 | TCP | VNC |
| 6379 | TCP | Redis |
| 8080 | TCP | HTTP Proxy |
| 8443 | TCP | HTTPS Alt |

### 2. Perform Port Discovery

Scan for open ports on target systems:

```bash
# Quick TCP SYN scan of common ports
nmap -sS -T4 192.168.1.1

# Comprehensive port scan (all 65535 ports)
nmap -p- -sS -T4 192.168.1.1

# UDP port scan
nmap -sU -T4 --top-ports 100 192.168.1.1

# Service version detection
nmap -sV -sC 192.168.1.1

# Fast scan with masscan
masscan -p1-65535 192.168.1.0/24 --rate=1000

# Check specific port with netcat
nc -zv 192.168.1.1 22
```

### 3. Enumerate Services by Port

Perform targeted enumeration based on discovered ports:

```bash
# FTP (21) - Check anonymous access
ftp 192.168.1.1
nmap --script ftp-anon 192.168.1.1

# SSH (22) - Grab banner and check versions
ssh -v 192.168.1.1
nmap --script ssh-hostkey 192.168.1.1

# SMTP (25) - Enumerate users
nmap --script smtp-enum-users 192.168.1.1

# DNS (53) - Zone transfer
dig axfr @192.168.1.1 domain.com

# HTTP (80/443) - Web enumeration
nikto -h http://192.168.1.1
gobuster dir -u http://192.168.1.1 -w /usr/share/wordlists/dirb/common.txt

# SMB (445) - Share enumeration
smbclient -L //192.168.1.1 -N
enum4linux -a 192.168.1.1

# SNMP (161) - Community string discovery
snmpwalk -c public -v1 192.168.1.1
onesixtyone 192.168.1.1 public

# LDAP (389) - Query directory
ldapsearch -x -h 192.168.1.1 -s base

# MySQL (3306) - Database enumeration
nmap --script mysql-enum 192.168.1.1
```

### 4. Map Attack Surface

Document findings for exploitation:

```bash
# Generate port scan report
nmap -sV -sC -oA scan_results 192.168.1.1

# Create service inventory
nmap -sV 192.168.1.1 -oG - | grep open
```

## Quick Reference

### High-Value Target Ports

| Port | Why It Matters |
|------|----------------|
| 21 | Anonymous FTP access, file upload |
| 22 | SSH brute force, key-based auth bypass |
| 23 | Telnet cleartext credentials |
| 25 | Mail relay, user enumeration |
| 53 | DNS zone transfer, cache poisoning |
| 80/443 | Web vulnerabilities (SQLi, XSS, RCE) |
| 135/445 | SMB exploits (EternalBlue) |
| 139 | NetBIOS enumeration |
| 161 | SNMP default communities |
| 389/636 | LDAP injection, AD enumeration |
| 1433/3306 | Database access, SQL injection |
| 3389 | RDP brute force, BlueKeep |
| 5985/5986 | WinRM remote execution |
| 6379 | Redis unauthenticated access |

### Database Ports

| Port | Database |
|------|----------|
| 1433 | Microsoft SQL Server |
| 1521 | Oracle |
| 3306 | MySQL/MariaDB |
| 5432 | PostgreSQL |
| 5984 | CouchDB |
| 6379 | Redis |
| 27017 | MongoDB |

### Remote Access Ports

| Port | Service |
|------|---------|
| 22 | SSH |
| 23 | Telnet |
| 3389 | RDP |
| 5900 | VNC |
| 5985/5986 | WinRM |

## Constraints

- Always verify port assignments as services can run on non-standard ports
- Some ports are registered but rarely used in practice
- Firewalls may filter or redirect traffic
- NAT and port forwarding can obscure actual service locations
- Service banners can be spoofed for deception

## Examples

### Example 1: Quick Web Server Identification

```bash
# Scan common web ports
nmap -p 80,443,8080,8443 192.168.1.0/24

# Get HTTP headers
curl -I http://192.168.1.1
```

### Example 2: Database Discovery

```bash
# Scan for common database ports
nmap -p 1433,1521,3306,5432,27017 192.168.1.0/24 -sV

# Test MySQL connection
mysql -h 192.168.1.1 -u root -p
```

### Example 3: Full Port Audit

```bash
# Comprehensive scan with service detection
nmap -p- -sV -sC -A 192.168.1.1 -oA full_audit
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Ports appear filtered | Try different scan techniques (-sA, -sW) |
| Service detection fails | Use more aggressive version probing (-sV --version-all) |
| UDP scan too slow | Reduce port range or increase timing (-T5) |
| False positives | Verify with manual connection (nc, telnet) |
| Firewall blocking scans | Use fragmentation (-f) or decoys (-D) |
| Service on non-standard port | Always perform full port scans (-p-) |
