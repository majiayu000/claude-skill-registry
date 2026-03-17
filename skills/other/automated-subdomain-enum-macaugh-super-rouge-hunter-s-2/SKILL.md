---
name: Automated Subdomain Enumeration
description: Systematic approach to discovering subdomains through passive and active reconnaissance techniques
when_to_use: When performing initial reconnaissance on a target domain, building an attack surface map, or identifying forgotten or misconfigured subdomains that may present vulnerabilities
version: 1.0.0
languages: bash, python, go
---

# Automated Subdomain Enumeration

## Overview

Subdomain discovery is a critical first step in reconnaissance. Forgotten subdomains often contain vulnerabilities, outdated software, or misconfigurations that attackers can exploit. A systematic approach combines multiple data sources and techniques to build a comprehensive subdomain list.

**Core principle:** Combine passive reconnaissance (non-intrusive) with active enumeration (DNS queries, brute-forcing) to maximize coverage while respecting scope and legal boundaries.

## When to Use

Use this skill when:
- Starting reconnaissance on a new target domain
- Building an inventory of an organization's attack surface
- Hunting for forgotten or shadow IT assets
- Looking for development, staging, or test environments
- Preparing for comprehensive vulnerability assessment

**Don't use when:**
- Outside authorized scope (get written permission first)
- Rate limiting or WAF might trigger alerts prematurely
- Target has strict testing windows you must respect

## The Multi-Phase Approach

### Phase 1: Passive Reconnaissance

**Goal:** Gather subdomains without directly touching target infrastructure.

**Techniques:**

1. **Certificate Transparency Logs**
   ```bash
   # Use crt.sh or similar CT log search
   curl -s "https://crt.sh/?q=%25.target.com&output=json" | \
     jq -r '.[].name_value' | \
     sed 's/\*\.//g' | \
     sort -u > ct_subdomains.txt
   ```

2. **Search Engine Dorking**
   ```bash
   # Google dorks for subdomains
   # site:target.com -www
   # Use tools like subfinder, amass with passive sources
   subfinder -d target.com -silent -all -o passive_subdomains.txt
   ```

3. **DNS Aggregators**
   - SecurityTrails
   - VirusTotal
   - DNSdumpster
   - Shodan

4. **GitHub/GitLab Code Search**
   ```bash
   # Search for domain mentions in code
   # "target.com" site:github.com
   # Look for: config files, API endpoints, documentation
   ```

5. **Web Archives**
   ```bash
   # Wayback Machine API
   curl -s "http://web.archive.org/cdx/search/cdx?url=*.target.com/*&output=json&fl=original&collapse=urlkey" | \
     jq -r '.[] | .[0]' | \
     grep -oP '(?<=://)[^/]*' | \
     sort -u >> archive_subdomains.txt
   ```

### Phase 2: Active Enumeration

**Goal:** Actively query DNS infrastructure to discover additional subdomains.

**Techniques:**

1. **Brute Force with Wordlists**
   ```bash
   # Use tools like puredns, massdns, or dnsx
   puredns bruteforce wordlist.txt target.com \
     --resolvers resolvers.txt \
     --write active_subdomains.txt
   ```

2. **DNS Zone Transfers (if misconfigured)**
   ```bash
   # Test for zone transfer vulnerability
   dig axfr @ns1.target.com target.com
   ```

3. **Reverse DNS Lookups**
   ```bash
   # Get IP ranges, perform reverse lookups
   # Useful for finding additional subdomains on same infrastructure
   ```

4. **Permutation Scanning**
   ```bash
   # Generate permutations of found subdomains
   # Example: dev.api.target.com, staging.api.target.com
   altdns -i subdomains.txt -o permuted.txt -w words.txt
   dnsx -l permuted.txt -o verified_permuted.txt
   ```

### Phase 3: Validation and Enrichment

**Goal:** Verify discovered subdomains are live and gather additional context.

1. **Live Host Detection**
   ```bash
   # Use httpx to probe for web services
   cat all_subdomains.txt | httpx -silent -o live_hosts.txt
   
   # Get status codes, titles, tech stack
   httpx -l all_subdomains.txt -title -tech-detect -status-code -o enriched.txt
   ```

2. **Port Scanning**
   ```bash
   # Identify services on discovered hosts
   naabu -list live_hosts.txt -p 80,443,8080,8443 -o ports.txt
   ```

3. **Screenshot Capture**
   ```bash
   # Visual reconnaissance of web interfaces
   gowitness file -f live_hosts.txt -P screenshots/
   ```

4. **Technology Fingerprinting**
   ```bash
   # Identify web technologies, frameworks, CMS
   wappalyzer -l live_hosts.txt -o tech_stack.json
   ```

### Phase 4: Organization and Analysis

**Goal:** Structure discovered data for efficient analysis and next steps.

1. **Categorize Subdomains**
   - Production vs. development/staging/test
   - Internal-facing vs. external-facing
   - By technology stack or function
   - By sensitivity/criticality

2. **Prioritize Targets**
   - High-value targets: admin, api, dev, staging, test, vpn, mail
   - Outdated software versions
   - Unusual ports or services
   - Error messages or debug pages

3. **Document Findings**
   ```markdown
   # Target: target.com
   
   ## Statistics
   - Total subdomains discovered: X
   - Live hosts: Y
   - Unique IP addresses: Z
   - Technologies identified: [list]
   
   ## High-Priority Targets
   1. dev.api.target.com - Swagger UI exposed, no auth
   2. old-admin.target.com - PHP 5.6, potential RCE
   3. test-payment.target.com - Test environment with prod data?
   
   ## Next Steps
   - Deep enumeration of api.target.com endpoints
   - Vulnerability scan of outdated PHP instance
   - Manual inspection of test environment
   ```

## Tool Recommendations

**All-in-one suites:**
- Amass (comprehensive, integrates many sources)
- Subfinder (fast passive enumeration)
- Assetfinder (simple, effective)

**Specialized tools:**
- Puredns (DNS validation and brute-forcing)
- DNSx (DNS toolkit with various features)
- Httpx (HTTP probing and enrichment)
- Naabu (fast port scanner)
- Gowitness (screenshot capture)

**Setup example:**
```bash
# Install Go tools
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest

# Install other dependencies
pip install altdns
```

## Automation Script Template

```bash
#!/bin/bash
# automated_subdomain_enum.sh

DOMAIN=$1
OUTPUT_DIR="${DOMAIN}_recon_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

echo "[*] Starting subdomain enumeration for $DOMAIN"

# Phase 1: Passive
echo "[*] Phase 1: Passive reconnaissance"
subfinder -d "$DOMAIN" -all -silent -o "$OUTPUT_DIR/subfinder.txt"
assetfinder --subs-only "$DOMAIN" > "$OUTPUT_DIR/assetfinder.txt"
curl -s "https://crt.sh/?q=%25.$DOMAIN&output=json" | jq -r '.[].name_value' | sed 's/\*\.//g' | sort -u > "$OUTPUT_DIR/crtsh.txt"

# Combine and deduplicate
cat "$OUTPUT_DIR"/{subfinder,assetfinder,crtsh}.txt | sort -u > "$OUTPUT_DIR/passive_all.txt"
echo "[+] Found $(wc -l < "$OUTPUT_DIR/passive_all.txt") unique subdomains (passive)"

# Phase 2: Active (optional, comment out if too noisy)
# echo "[*] Phase 2: Active enumeration"
# puredns bruteforce /path/to/wordlist.txt "$DOMAIN" -r /path/to/resolvers.txt -w "$OUTPUT_DIR/bruteforce.txt"

# Phase 3: Validation
echo "[*] Phase 3: Validating and probing subdomains"
cat "$OUTPUT_DIR/passive_all.txt" | dnsx -silent -o "$OUTPUT_DIR/validated.txt"
httpx -l "$OUTPUT_DIR/validated.txt" -title -status-code -tech-detect -silent -o "$OUTPUT_DIR/live_hosts.txt"

echo "[+] Found $(wc -l < "$OUTPUT_DIR/live_hosts.txt") live hosts"
echo "[*] Results saved to $OUTPUT_DIR/"
```

## Legal and Ethical Considerations

**CRITICAL:** Always follow these rules:

1. **Get Written Authorization**
   - Never test targets without explicit permission
   - Scope must be clearly defined in writing
   - Understand what techniques are permitted

2. **Respect Rate Limits**
   - Don't overwhelm target DNS servers
   - Use reasonable delays between requests
   - Consider impact on production systems

3. **Handle Data Responsibly**
   - Discovered subdomains may reveal sensitive information
   - Don't publicly disclose findings without permission
   - Follow responsible disclosure practices

4. **Document Everything**
   - Keep records of authorization
   - Log all activities with timestamps
   - Document findings systematically

## Common Pitfalls

| Mistake | Impact | Solution |
|---------|--------|----------|
| Only using one data source | Miss many subdomains | Combine multiple techniques |
| Skipping validation | False positives waste time | Always verify with DNS queries |
| Too aggressive active scanning | Detection, blocking, legal issues | Start passive, escalate carefully |
| Not categorizing results | Inefficient analysis | Organize findings by priority |
| Ignoring out-of-scope domains | Legal/ethical violations | Strictly adhere to authorized scope |

## Integration with Other Skills

This skill works with:
- skills/reconnaissance/web-app-recon - Next step after finding live web apps
- skills/reconnaissance/service-fingerprinting - Identify services on discovered hosts
- skills/automation/* - Automate the full recon pipeline
- skills/documentation/* - Organize findings in knowledge base

## Success Metrics

A successful subdomain enumeration should:
- Discover both obvious and hidden subdomains
- Identify live hosts and their technologies
- Categorize findings by risk/priority
- Provide actionable next steps
- Complete within scope and authorization
- Document findings for future reference

## References and Further Reading

- OWASP Testing Guide: Information Gathering
- "Bug Bounty Bootcamp" by Vickie Li (Chapter on Reconnaissance)
- ProjectDiscovery blog on subdomain enumeration
- DNS RFC standards for understanding DNS behavior
