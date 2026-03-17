---
name: Service Fingerprinting
description: Techniques for accurately identifying services, versions, and technologies running on discovered hosts
when_to_use: After discovering live hosts during reconnaissance, when mapping technology stack for vulnerability assessment, or when preparing targeted exploitation strategies
version: 1.0.0
languages: bash, python
---

# Service Fingerprinting

## Overview

Service fingerprinting identifies the specific software, version, and configuration of network services. Accurate fingerprinting enables targeted vulnerability assessment, exploit selection, and understanding of the attack surface. This skill combines active probing, banner grabbing, and behavioral analysis.

**Core principle:** Start passive, escalate to active when needed. Combine multiple techniques for accuracy.

## When to Use

- After discovering live hosts (from subdomain enumeration)
- Before vulnerability scanning or exploitation
- When building detailed target intelligence
- During penetration testing reconnaissance phase

## Techniques

### Port Scanning

```bash
# Fast SYN scan of common ports
nmap -sS -F target.com

# Comprehensive scan of all ports
nmap -p- -T4 target.com

# Service version detection
nmap -sV -p 80,443,22,3306 target.com

# OS detection
sudo nmap -O target.com

# Aggressive scan (version, OS, scripts, traceroute)
nmap -A target.com
```

### Banner Grabbing

```bash
# Manual banner grab
nc target.com 80
GET / HTTP/1.0

# Automated with nmap
nmap -sV --version-intensity 9 -p 80,443 target.com

# Multiple services
for port in 21 22 25 80 443 3306; do
  echo "=== Port $port ===" 
  nc -w 2 target.com $port
done
```

### HTTP/HTTPS Fingerprinting

```bash
# Detailed HTTP headers
curl -I https://target.com

# Technology detection
whatweb -a 3 https://target.com

# Certificate information
echo | openssl s_client -connect target.com:443 2>/dev/null | openssl x509 -noout -text
```

### Specialized Scanners

```bash
# Database fingerprinting
nmap -p 3306 --script mysql-info target.com
nmap -p 5432 --script pgsql-info target.com

# SMB enumeration
nmap -p 445 --script smb-os-discovery target.com

# SSH fingerprinting
ssh-audit target.com
```

## Common Services

| Port | Service | Fingerprinting Command |
|------|---------|------------------------|
| 21 | FTP | `nc target.com 21` |
| 22 | SSH | `nc target.com 22` |
| 80/443 | HTTP/HTTPS | `curl -I https://target.com` |
| 3306 | MySQL | `nmap -p 3306 --script mysql-info` |
| 5432 | PostgreSQL | `nmap -p 5432 --script pgsql-info` |
| 6379 | Redis | `redis-cli -h target.com info` |
| 27017 | MongoDB | `nmap -p 27017 --script mongodb-info` |

## Integration with Other Skills

- skills/reconnaissance/automated-subdomain-enum - Provides targets
- skills/reconnaissance/web-app-recon - Detailed HTTP analysis
- skills/exploitation/* - Informs exploit selection
