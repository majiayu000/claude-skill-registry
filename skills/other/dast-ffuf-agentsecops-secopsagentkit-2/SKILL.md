---
name: dast-ffuf
description: >
  Fast web fuzzer for DAST testing with directory enumeration, parameter fuzzing, and virtual host
  discovery. Written in Go for high-performance HTTP fuzzing with extensive filtering capabilities.
  Supports multiple fuzzing modes (clusterbomb, pitchfork, sniper) and recursive scanning. Use when:
  (1) Discovering hidden directories, files, and endpoints on web applications, (2) Fuzzing GET and
  POST parameters to identify injection vulnerabilities, (3) Enumerating virtual hosts and subdomains,
  (4) Testing authentication endpoints with credential fuzzing, (5) Finding backup files and sensitive
  data exposures, (6) Performing comprehensive web application reconnaissance.
version: 0.1.0
maintainer: SirAppSec
category: appsec
tags: [dast, fuzzing, web-fuzzer, directory-enumeration, parameter-fuzzing, vhost-discovery, ffuf, reconnaissance]
frameworks: [OWASP]
dependencies:
  tools: [ffuf]
references:
  - https://github.com/ffuf/ffuf
---

# ffuf - Fast Web Fuzzer

## Overview

ffuf is a fast web fuzzer written in Go designed for discovering hidden resources, testing parameters, and performing comprehensive web application reconnaissance. It uses the FUZZ keyword as a placeholder for wordlist entries and supports advanced filtering, multiple fuzzing modes, and recursive scanning for thorough security assessments.

## Installation

```bash
# Using Go
go install github.com/ffuf/ffuf/v2@latest

# Using package managers
# Debian/Ubuntu
apt install ffuf

# macOS
brew install ffuf

# Or download pre-compiled binary from GitHub releases
```

## Quick Start

Basic directory fuzzing:

```bash
# Directory discovery
ffuf -u https://example.com/FUZZ -w /usr/share/wordlists/dirb/common.txt

# File discovery with extension
ffuf -u https://example.com/FUZZ -w wordlist.txt -e .php,.html,.txt

# Virtual host discovery
ffuf -u https://example.com -H "Host: FUZZ.example.com" -w subdomains.txt
```

## Core Workflows

### Workflow 1: Directory and File Enumeration

For discovering hidden resources on web applications:

1. Start with common directory wordlist:
   ```bash
   ffuf -u https://target.com/FUZZ \
     -w /usr/share/seclists/Discovery/Web-Content/common.txt \
     -mc 200,204,301,302,307,401,403 \
     -o results.json
   ```
2. Review discovered directories (focus on 200, 403 status codes)
3. Enumerate files in discovered directories:
   ```bash
   ffuf -u https://target.com/admin/FUZZ \
     -w /usr/share/seclists/Discovery/Web-Content/raft-small-files.txt \
     -e .php,.bak,.txt,.zip \
     -mc all -fc 404
   ```
4. Use recursive mode for deep enumeration:
   ```bash
   ffuf -u https://target.com/FUZZ \
     -w wordlist.txt \
     -recursion -recursion-depth 2 \
     -e .php,.html \
     -v
   ```
5. Document findings and test discovered endpoints

### Workflow 2: Parameter Fuzzing (GET/POST)

Progress:
[ ] 1. Identify target endpoint for parameter testing
[ ] 2. Fuzz GET parameter names to discover hidden parameters
[ ] 3. Fuzz parameter values for injection vulnerabilities
[ ] 4. Test POST parameters with JSON/form data
[ ] 5. Apply appropriate filters to reduce false positives
[ ] 6. Analyze responses for anomalies and vulnerabilities
[ ] 7. Validate findings manually
[ ] 8. Document vulnerable parameters and payloads

Work through each step systematically. Check off completed items.

**GET Parameter Name Fuzzing:**
```bash
ffuf -u https://target.com/api?FUZZ=test \
  -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
  -fs 0  # Filter out empty responses
```

**GET Parameter Value Fuzzing:**
```bash
ffuf -u https://target.com/api?id=FUZZ \
  -w payloads.txt \
  -mc all
```

**POST Data Fuzzing:**
```bash
# Form data
ffuf -u https://target.com/login \
  -X POST \
  -d "username=admin&password=FUZZ" \
  -w passwords.txt \
  -H "Content-Type: application/x-www-form-urlencoded"

# JSON data
ffuf -u https://target.com/api/login \
  -X POST \
  -d '{"username":"admin","password":"FUZZ"}' \
  -w passwords.txt \
  -H "Content-Type: application/json"
```

### Workflow 3: Virtual Host and Subdomain Discovery

For identifying virtual hosts and subdomains:

1. Prepare subdomain wordlist (or use SecLists)
2. Run vhost fuzzing:
   ```bash
   ffuf -u https://target.com \
     -H "Host: FUZZ.target.com" \
     -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
     -fs 0  # Filter by response size to identify valid vhosts
   ```
3. Filter results by comparing response sizes/words
4. Verify discovered vhosts manually
5. Enumerate directories on each vhost
6. Document vhost configurations and exposed services

### Workflow 4: Authentication Endpoint Fuzzing

For testing login forms and authentication mechanisms:

1. Identify authentication endpoint
2. Fuzz usernames:
   ```bash
   ffuf -u https://target.com/login \
     -X POST \
     -d "username=FUZZ&password=test123" \
     -w usernames.txt \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -mr "Invalid password|Incorrect password"  # Match responses indicating valid user
   ```
3. For identified users, fuzz passwords:
   ```bash
   ffuf -u https://target.com/login \
     -X POST \
     -d "username=admin&password=FUZZ" \
     -w /usr/share/seclists/Passwords/Common-Credentials/10-million-password-list-top-1000.txt \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -fc 401,403  # Filter failed attempts
   ```
4. Use clusterbomb mode for combined username/password fuzzing:
   ```bash
   ffuf -u https://target.com/login \
     -X POST \
     -d "username=FUZZ1&password=FUZZ2" \
     -w usernames.txt:FUZZ1 \
     -w passwords.txt:FUZZ2 \
     -mode clusterbomb
   ```

### Workflow 5: Backup and Sensitive File Discovery

For finding exposed backup files and sensitive data:

1. Create wordlist of common backup patterns
2. Fuzz for backup files:
   ```bash
   ffuf -u https://target.com/FUZZ \
     -w backup-files.txt \
     -e .bak,.backup,.old,.zip,.tar.gz,.sql,.7z \
     -mc 200 \
     -o backup-files.json
   ```
3. Test common sensitive file locations:
   ```bash
   ffuf -u https://target.com/FUZZ \
     -w /usr/share/seclists/Discovery/Web-Content/sensitive-files.txt \
     -mc 200,403
   ```
4. Download and analyze discovered files
5. Report findings with severity classification

## Fuzzing Modes

ffuf supports multiple fuzzing modes for different attack scenarios:

**Clusterbomb Mode** - Cartesian product of all wordlists (default):
```bash
ffuf -u https://target.com/FUZZ1/FUZZ2 \
  -w dirs.txt:FUZZ1 \
  -w files.txt:FUZZ2 \
  -mode clusterbomb
```
Tests every combination: dir1/file1, dir1/file2, dir2/file1, dir2/file2

**Pitchfork Mode** - Parallel iteration of wordlists:
```bash
ffuf -u https://target.com/login \
  -X POST \
  -d "username=FUZZ1&password=FUZZ2" \
  -w users.txt:FUZZ1 \
  -w passwords.txt:FUZZ2 \
  -mode pitchfork
```
Tests pairs: user1/pass1, user2/pass2 (stops at shortest wordlist)

**Sniper Mode** - One wordlist, multiple positions:
```bash
ffuf -u https://target.com/FUZZ \
  -w wordlist.txt \
  -mode sniper
```
Standard single-wordlist fuzzing.

## Filtering and Matching

Effective filtering is crucial for reducing noise:

**Match Filters** (only show matching):
- `-mc 200,301` - Match HTTP status codes
- `-ms 1234` - Match response size
- `-mw 100` - Match word count
- `-ml 50` - Match line count
- `-mr "success|admin"` - Match regex pattern in response

**Filter Options** (exclude matching):
- `-fc 404,403` - Filter status codes
- `-fs 0,1234` - Filter response sizes
- `-fw 0` - Filter word count
- `-fl 0` - Filter line count
- `-fr "error|not found"` - Filter regex pattern

**Auto-Calibration:**
```bash
# Automatically filter baseline responses
ffuf -u https://target.com/FUZZ -w wordlist.txt -ac
```

## Common Patterns

### Pattern 1: API Endpoint Discovery

Discover REST API endpoints:

```bash
# Enumerate API paths
ffuf -u https://api.target.com/v1/FUZZ \
  -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt \
  -mc 200,201,401,403 \
  -o api-endpoints.json

# Fuzz API versions
ffuf -u https://api.target.com/FUZZ/users \
  -w <(seq 1 10 | sed 's/^/v/') \
  -mc 200
```

### Pattern 2: Extension Fuzzing

Test multiple file extensions:

```bash
# Brute-force extensions on known files
ffuf -u https://target.com/admin.FUZZ \
  -w /usr/share/seclists/Discovery/Web-Content/web-extensions.txt \
  -mc 200

# Or use -e flag for multiple extensions
ffuf -u https://target.com/FUZZ \
  -w filenames.txt \
  -e .php,.asp,.aspx,.jsp,.html,.bak,.txt
```

### Pattern 3: Rate-Limited Fuzzing

Respect rate limits and avoid detection:

```bash
# Add delay between requests
ffuf -u https://target.com/FUZZ \
  -w wordlist.txt \
  -p 0.5-1.0  # Random delay 0.5-1.0 seconds

# Limit concurrent requests
ffuf -u https://target.com/FUZZ \
  -w wordlist.txt \
  -t 5  # Only 5 concurrent threads
```

### Pattern 4: Custom Header Fuzzing

Fuzz HTTP headers for security misconfigurations:

```bash
# Fuzz custom headers
ffuf -u https://target.com/admin \
  -w headers.txt:HEADER \
  -H "HEADER: true" \
  -mc all

# Fuzz header values
ffuf -u https://target.com/admin \
  -H "X-Forwarded-For: FUZZ" \
  -w /usr/share/seclists/Fuzzing/IPs.txt \
  -mc 200
```

### Pattern 5: Cookie Fuzzing

Test cookie-based authentication and session management:

```bash
# Fuzz cookie values
ffuf -u https://target.com/dashboard \
  -b "session=FUZZ" \
  -w session-tokens.txt \
  -mc 200

# Fuzz cookie names
ffuf -u https://target.com/admin \
  -b "FUZZ=admin" \
  -w cookie-names.txt
```

## Output Formats

Save results in multiple formats:

```bash
# JSON output (recommended for parsing)
ffuf -u https://target.com/FUZZ -w wordlist.txt -o results.json -of json

# CSV output
ffuf -u https://target.com/FUZZ -w wordlist.txt -o results.csv -of csv

# HTML report
ffuf -u https://target.com/FUZZ -w wordlist.txt -o results.html -of html

# All formats
ffuf -u https://target.com/FUZZ -w wordlist.txt -o results -of all
```

## Security Considerations

- **Sensitive Data Handling**: Discovered files may contain credentials, API keys, or PII. Handle findings securely and report responsibly
- **Access Control**: Only fuzz applications with proper authorization. Obtain written permission before testing third-party systems
- **Audit Logging**: Log all fuzzing activities including targets, wordlists used, and findings for compliance and audit trails
- **Compliance**: Ensure fuzzing activities comply with bug bounty program rules, penetration testing agreements, and legal requirements
- **Safe Defaults**: Use reasonable rate limits to avoid DoS conditions. Start with small wordlists before scaling up

## Integration Points

### Reconnaissance Workflow

1. Subdomain enumeration (amass, subfinder)
2. Port scanning (nmap)
3. Service identification
4. **ffuf directory/file enumeration**
5. Content discovery and analysis
6. Vulnerability scanning

### CI/CD Security Testing

Integrate ffuf into automated security pipelines:

```bash
# CI/CD script
#!/bin/bash
set -e

# Run directory enumeration
ffuf -u https://staging.example.com/FUZZ \
  -w /wordlists/common.txt \
  -mc 200,403 \
  -o ffuf-results.json \
  -of json

# Parse results and fail if sensitive files found
if grep -q "/.git/\|/backup/" ffuf-results.json; then
  echo "ERROR: Sensitive files exposed!"
  exit 1
fi
```

### Integration with Burp Suite

1. Use Burp to identify target endpoints
2. Export interesting requests
3. Convert to ffuf commands for automated fuzzing
4. Import ffuf results back to Burp for manual testing

## Troubleshooting

### Issue: Too Many False Positives

**Solution**: Use auto-calibration or manual filtering:
```bash
# Auto-calibration
ffuf -u https://target.com/FUZZ -w wordlist.txt -ac

# Manual filtering by size
ffuf -u https://target.com/FUZZ -w wordlist.txt -fs 1234,5678
```

### Issue: Rate Limiting or Blocking

**Solution**: Reduce concurrency and add delays:
```bash
ffuf -u https://target.com/FUZZ \
  -w wordlist.txt \
  -t 1 \
  -p 2.0 \
  -H "User-Agent: Mozilla/5.0..."
```

### Issue: Large Wordlist Takes Too Long

**Solution**: Start with smaller, targeted wordlists:
```bash
# Use top 1000 instead of full list
head -1000 /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt > small.txt
ffuf -u https://target.com/FUZZ -w small.txt
```

### Issue: Missing Discovered Content

**Solution**: Test with multiple extensions and match codes:
```bash
ffuf -u https://target.com/FUZZ \
  -w wordlist.txt \
  -e .php,.html,.txt,.asp,.aspx,.jsp \
  -mc all \
  -fc 404
```

## OWASP Testing Integration

Map ffuf usage to OWASP Testing Guide categories:

- **WSTG-CONF-04**: Review Old Backup and Unreferenced Files
- **WSTG-CONF-05**: Enumerate Infrastructure and Application Admin Interfaces
- **WSTG-CONF-06**: Test HTTP Methods
- **WSTG-IDENT-01**: Test Role Definitions (directory enumeration)
- **WSTG-ATHZ-01**: Test Directory Traversal/File Include
- **WSTG-INPVAL-01**: Test for Reflected Cross-site Scripting
- **WSTG-INPVAL-02**: Test for Stored Cross-site Scripting

## References

- [ffuf GitHub Repository](https://github.com/ffuf/ffuf)
- [SecLists Wordlists](https://github.com/danielmiessler/SecLists)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
