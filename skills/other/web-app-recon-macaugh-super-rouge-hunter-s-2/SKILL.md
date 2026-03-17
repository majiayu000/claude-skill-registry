---
name: Web Application Reconnaissance
description: Systematic methodology for mapping web application attack surface, discovering hidden endpoints, and identifying technologies
when_to_use: After identifying live web applications during subdomain enumeration, when starting security assessment of a web app, or when hunting for hidden functionality and forgotten endpoints
version: 1.0.0
languages: bash, python, javascript
---

# Web Application Reconnaissance

## Overview

Web application reconnaissance goes beyond simple subdomain discovery to map the full attack surface of a web application. This includes discovering hidden endpoints, analyzing client-side code, identifying backend technologies, and understanding the application's architecture.

**Core principle:** Systematic enumeration combined with intelligent analysis reveals hidden attack surface that automated scanners miss.

## When to Use

Use this skill when:
- Starting security assessment of a web application
- Building comprehensive understanding of app structure
- Looking for hidden admin panels, APIs, or debug endpoints
- Analyzing JavaScript for hardcoded secrets or endpoints
- Mapping application functionality before deeper testing

**Don't use when:**
- Not authorized to test the target
- Application has strict rate limiting (adjust methodology)
- Need to remain completely passive (use only public sources)

## The Four-Phase Methodology

### Phase 1: Initial Discovery and Fingerprinting

**Goal:** Understand what you're dealing with - technologies, frameworks, and basic structure.

**Techniques:**

1. **Technology Detection**
   ```bash
   # Comprehensive tech stack identification
   whatweb -v -a 3 https://target.com
   
   # HTTP headers analysis
   curl -I https://target.com
   
   # Wappalyzer or similar
   wappalyzer https://target.com
   ```

2. **Common Files and Directories**
   ```bash
   # robots.txt - often reveals hidden directories
   curl https://target.com/robots.txt
   
   # sitemap.xml - complete site structure
   curl https://target.com/sitemap.xml
   
   # security.txt - contact info, may reveal scope
   curl https://target.com/.well-known/security.txt
   
   # Common config/info files
   for file in readme.md humans.txt crossdomain.xml; do
     curl -s https://target.com/$file
   done
   ```

3. **SSL/TLS Analysis**
   ```bash
   # Certificate information may reveal additional domains
   echo | openssl s_client -connect target.com:443 2>/dev/null | \
     openssl x509 -noout -text | \
     grep -A1 "Subject Alternative Name"
   ```

### Phase 2: Content Discovery

**Goal:** Find hidden endpoints, forgotten files, backup directories, and undocumented functionality.

**Techniques:**

1. **Directory and File Fuzzing**
   ```bash
   # ffuf - fast web fuzzer
   ffuf -w /path/to/wordlist.txt \
        -u https://target.com/FUZZ \
        -mc 200,301,302,403 \
        -o directories.json
   
   # gobuster for directory brute-forcing
   gobuster dir -u https://target.com \
                -w /path/to/wordlist.txt \
                -x php,html,js,txt,json \
                -o gobuster_results.txt
   
   # feroxbuster - recursive directory discovery
   feroxbuster -u https://target.com \
                -w /path/to/wordlist.txt \
                --depth 3 \
                -x php js json
   ```

2. **Intelligent Wordlist Selection**
   ```bash
   # Technology-specific wordlists
   # For WordPress:
   ffuf -w wordpress_wordlist.txt -u https://target.com/FUZZ
   
   # For APIs:
   ffuf -w api_wordlist.txt -u https://target.com/api/FUZZ
   
   # Custom wordlist from discovered technologies
   # If tech stack is Python/Django, use Django-specific paths
   ```

3. **Backup and Sensitive File Discovery**
   ```bash
   # Common backup patterns
   for ext in .bak .old .backup .swp ~; do
     ffuf -w discovered_files.txt -u https://target.com/FUZZ$ext -mc 200
   done
   
   # Source code disclosure
   ffuf -w discovered_files.txt -u https://target.com/FUZZ.txt -mc 200
   
   # Git exposure
   curl -s https://target.com/.git/HEAD
   # If found, use git-dumper or similar to extract repository
   ```

### Phase 3: JavaScript Analysis

**Goal:** Extract hardcoded secrets, discover API endpoints, and understand client-side logic.

**Techniques:**

1. **Enumerate All JavaScript Files**
   ```bash
   # Extract JS URLs from HTML
   curl -s https://target.com | \
     grep -oP 'src="[^"]+\.js"' | \
     sed 's/src="//;s/"$//' > js_files.txt
   
   # Use LinkFinder or similar
   python3 linkfinder.py -i https://target.com -o results.html
   ```

2. **Search for Sensitive Data in JS**
   ```bash
   # Download all JS files
   while read url; do
     curl -s "$url" > "js/$(basename "$url")"
   done < js_files.txt
   
   # Search for patterns
   grep -r -E "(api_key|apikey|secret|password|token|aws_access)" js/
   grep -r -E "(https?://[^\"\'\ ]+)" js/ | grep -v "fonts\|cdn"
   
   # Find API endpoints
   grep -r -E "(/api/|/v[0-9]+/)" js/
   ```

3. **Beautify and Analyze Minified Code**
   ```bash
   # Beautify JS for easier analysis
   for file in js/*.js; do
     js-beautify "$file" > "js_beautified/$(basename "$file")"
   done
   
   # Look for interesting functions
   grep -r "function" js_beautified/ | grep -i "admin\|debug\|test"
   ```

4. **Extract Subdomains and Endpoints from JS**
   ```bash
   # Use tools like JSFinder, relative-url-extractor
   python3 relative-url-extractor.py -u https://target.com > endpoints.txt
   ```

### Phase 4: Architecture Mapping

**Goal:** Understand application structure, authentication flows, and data flows.

**Techniques:**

1. **Crawling and Spidering**
   ```bash
   # Burp Suite spider (manual)
   # Or use automated crawlers
   gospider -s https://target.com -d 3 -c 10 -o spider_output
   
   # katana - fast crawler
   katana -u https://target.com -d 5 -ps -jc -o crawl_results.txt
   ```

2. **Parameter Discovery**
   ```bash
   # Find URL parameters
   arjun -u https://target.com/search -m GET
   
   # ParamSpider - discover parameters from wayback
   python3 paramspider.py -d target.com
   ```

3. **API Endpoint Enumeration**
   ```bash
   # If API discovered, enumerate versions and endpoints
   for version in v1 v2 v3; do
     ffuf -w api_endpoints.txt -u https://api.target.com/$version/FUZZ
   done
   
   # Swagger/OpenAPI documentation
   curl https://api.target.com/swagger.json
   curl https://api.target.com/openapi.json
   curl https://api.target.com/api-docs
   ```

4. **Authentication and Session Analysis**
   ```bash
   # Analyze authentication mechanisms
   # - Cookie attributes (HttpOnly, Secure, SameSite)
   # - JWT tokens (decode and analyze claims)
   # - OAuth flows
   # - Session management
   
   # Check for JWT
   # Decode JWT token (use jwt_tool or jwt.io)
   echo "eyJhbG..." | base64 -d
   ```

## Automation Pipeline

**Complete reconnaissance pipeline:**

```bash
#!/bin/bash
# web_app_recon.sh

TARGET=$1
OUTPUT_DIR="${TARGET//[.:\/]/_}_webapp_recon"
mkdir -p "$OUTPUT_DIR"/{js,crawl,endpoints}

echo "[*] Starting web application reconnaissance for $TARGET"

# Phase 1: Fingerprinting
echo "[*] Phase 1: Technology fingerprinting"
whatweb -v -a 3 "$TARGET" > "$OUTPUT_DIR/whatweb.txt"
curl -I "$TARGET" > "$OUTPUT_DIR/headers.txt"
curl -s "$TARGET/robots.txt" > "$OUTPUT_DIR/robots.txt"
curl -s "$TARGET/sitemap.xml" > "$OUTPUT_DIR/sitemap.xml"

# Phase 2: Content Discovery
echo "[*] Phase 2: Content discovery"
feroxbuster -u "$TARGET" \
            -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt \
            -x php,html,js,txt,json \
            --depth 2 \
            -o "$OUTPUT_DIR/feroxbuster.txt"

# Phase 3: JavaScript Analysis
echo "[*] Phase 3: JavaScript analysis"
katana -u "$TARGET" -jc -o "$OUTPUT_DIR/crawl/katana_js.txt"
# Download and analyze JS files
grep "\.js$" "$OUTPUT_DIR/crawl/katana_js.txt" | while read js_url; do
  filename=$(echo "$js_url" | md5sum | cut -d' ' -f1)
  curl -s "$js_url" > "$OUTPUT_DIR/js/${filename}.js"
done

# Search for secrets in JS
echo "[*] Searching for sensitive data in JavaScript"
grep -r -E "(api[_-]?key|secret|password|token)" "$OUTPUT_DIR/js/" > "$OUTPUT_DIR/js_secrets.txt"

# Phase 4: Endpoint extraction
echo "[*] Phase 4: Endpoint extraction"
cat "$OUTPUT_DIR/js"/*.js | grep -oP '(/api/[^"'"'"'\s]+)' | sort -u > "$OUTPUT_DIR/endpoints/api_endpoints.txt"

echo "[+] Reconnaissance complete. Results in $OUTPUT_DIR/"
echo "[+] Review the following files:"
echo "    - whatweb.txt: Technology stack"
echo "    - feroxbuster.txt: Discovered directories/files"
echo "    - js_secrets.txt: Potential secrets in JavaScript"
echo "    - endpoints/api_endpoints.txt: API endpoints found"
```

## Tool Recommendations

**Content Discovery:**
- ffuf (fast, flexible, modern)
- feroxbuster (recursive, Rust-based)
- gobuster (reliable, simple)

**Crawling:**
- katana (fast, modern)
- gospider (feature-rich)
- Burp Suite spider (manual, thorough)

**JavaScript Analysis:**
- LinkFinder (extract endpoints from JS)
- JSFinder (find subdomains/endpoints)
- relative-url-extractor
- js-beautify (beautify minified code)

**General:**
- httpx (probing and tech detection)
- nuclei (vulnerability templates)
- waybackurls (historical URLs)

## Common Patterns and Findings

**High-value targets to look for:**

1. **Admin/Debug Panels**
   ```
   /admin, /administrator, /admin.php
   /debug, /test, /dev
   /phpinfo.php, /info.php
   /console, /terminal
   ```

2. **Configuration Files**
   ```
   /config.php, /.env, /settings.py
   /web.config, /application.yml
   /config.json, /.git/config
   ```

3. **API Documentation**
   ```
   /api-docs, /swagger, /api/v1/docs
   /graphql, /graphiql
   /redoc, /openapi.json
   ```

4. **Backup Files**
   ```
   /backup, /backups, /old
   index.php.bak, database.sql.old
   site.tar.gz, backup.zip
   ```

## Organizing Findings

**Create structured documentation:**

```markdown
# Web App Recon: target.com

## Executive Summary
- Application Type: [E-commerce, API, CMS, etc.]
- Primary Technology: [PHP/Laravel, Python/Django, Node.js, etc.]
- Notable Findings: [X hidden endpoints, Y exposed configs]

## Technology Stack
- Frontend: React 18.2, Bootstrap 5
- Backend: Laravel 9.x
- Server: Nginx 1.21
- Database: MySQL (inferred from error messages)

## Discovered Endpoints
### Public
- /api/v1/products - Product listing API
- /api/v1/users - User profiles (requires auth)

### Hidden/Interesting
- /api/v1/admin - Admin API (403, exists!)
- /api/internal/metrics - Internal metrics endpoint
- /debug/routes - Laravel route list (exposed!)

## Sensitive Files Found
- /storage/logs/laravel.log - Application logs exposed
- /.env.backup - Backup of environment config
- /phpinfo.php - Server info disclosure

## JavaScript Findings
- API keys found: 2 (one appears to be test key)
- Hardcoded API endpoints: 15 additional endpoints
- Subdomains discovered: api-staging.target.com

## Priority Items for Further Testing
1. /debug/routes - Full route disclosure
2. /.env.backup - May contain database credentials
3. /api/internal/metrics - Potential IDOR or info disclosure
4. Staging subdomain - May have weaker security

## Next Steps
- Test IDOR on /api/v1/users endpoints
- Attempt to access admin API with discovered tokens
- Manual review of staging environment
- Test for SQL injection in search parameters
```

## Legal and Ethical Considerations

**CRITICAL - Always follow these rules:**

1. **Authorization Required**
   - Never test without explicit permission
   - Understand scope and boundaries
   - Don't access sensitive data unless authorized

2. **Responsible Disclosure**
   - Report findings through proper channels
   - Don't publicly disclose before remediation
   - Follow responsible disclosure timelines

3. **Data Handling**
   - Don't exfiltrate sensitive data
   - Don't store credentials or PII
   - Delete reconnaissance data after assessment

4. **Avoid DoS Conditions**
   - Rate limit your requests
   - Don't overload servers
   - Use appropriate concurrency settings

## Common Pitfalls

| Mistake | Impact | Solution |
|---------|--------|----------|
| Relying only on automated tools | Miss context-specific findings | Combine automation with manual analysis |
| Skipping JavaScript analysis | Miss API endpoints and secrets | Always analyze client-side code |
| Not checking robots.txt first | Waste time on known paths | Start with obvious information sources |
| Ignoring error messages | Miss technology fingerprinting | Pay attention to verbose errors |
| Too aggressive fuzzing | Detection, IP blocking | Start with smaller wordlists, increase gradually |

## Integration with Other Skills

This skill works with:
- skills/reconnaissance/automated-subdomain-enum - Feeds discovered subdomains here
- skills/exploitation/* - Use discovered endpoints for exploitation
- skills/analysis/static-vuln-analysis - Analyze discovered source code
- skills/documentation/* - Document findings systematically

## Success Metrics

A successful web app reconnaissance should:
- Identify all major technologies used
- Discover hidden or forgotten functionality
- Extract API endpoints and parameters
- Find configuration or sensitive file exposures
- Map authentication and authorization flows
- Prioritize findings for further testing
- Complete without triggering security alerts (if stealth required)

## References and Further Reading

- OWASP Web Security Testing Guide
- "The Web Application Hacker's Handbook" by Dafydd Stuttard
- "Bug Bounty Bootcamp" by Vickie Li (Chapters 4-5)
- PortSwigger Web Security Academy
- HackerOne disclosed reports for real-world examples
