<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: analyzing-web-archive-intelligence
description: >-
  Extract intelligence from web archives including historical content,
  removed pages, exposed configurations, and deprecated endpoints using
  the Wayback Machine and related archival services.
domain: cybersecurity
subdomain: osint-recon
tags:
  - web-archive
  - wayback-machine
  - historical-analysis
  - endpoint-discovery
  - content-recovery
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: >-
  waybackurls, gau, waymore, Wayback Machine API, gauplus,
  web.archive.org, archive.today, CommonCrawl, httpx.
metadata:
  mitre-attack:
    - "T1593.002"  # Search Open Websites/Domains: Search Engines
    - "T1596"      # Search Open Technical Databases
    - "T1592.004"  # Gather Victim Host Information: Client Configurations
---

# Analyzing Web Archive Intelligence

## Overview

Web archives preserve historical snapshots of websites, providing intelligence
on removed content, deprecated endpoints, exposed configuration files, old API
documentation, and infrastructure changes over time. The Wayback Machine,
CommonCrawl, and archive services index billions of pages. Analysts extract
forgotten endpoints, leaked credentials in old commits, deprecated admin panels,
and technology migration patterns.

## Prerequisites

- waybackurls for Wayback Machine URL extraction
- gau (GetAllUrls) for multi-source URL aggregation
- waymore for comprehensive archived URL discovery
- httpx for probing discovered endpoints
- Python 3.10+ with `requests`

```bash
go install github.com/tomnomnom/waybackurls@latest
go install github.com/lc/gau/v2/cmd/gau@latest
pip install waymore requests
```

## Quick Reference

| Task | Command |
|------|---------|
| Wayback URLs | `echo target.com \| waybackurls > wayback.txt` |
| All URLs | `echo target.com \| gau --threads 5 --o gau.txt` |
| Waymore | `waymore -i target.com -mode U -oU urls.txt` |
| Snapshots API | `curl -s "https://web.archive.org/cdx/search/cdx?url=target.com/*&output=json&fl=original,timestamp,statuscode"` |
| Probe live | `httpx -l wayback.txt -silent -sc -mc 200,301,302 -o live.txt` |
| Content diff | `curl -s "https://web.archive.org/web/20230101/https://target.com/" > old.html` |
| Param extract | `cat wayback.txt \| grep -oP '\?[^"]+' \| tr '&' '\n' \| cut -d= -f1 \| sort -u` |
| Config files | `cat wayback.txt \| grep -iE '\.(env\|config\|xml\|json\|yaml\|yml\|bak\|old\|sql)$'` |

## Workflow

### Step 1: Historical URL Extraction

```bash
# waybackurls — URLs from Wayback Machine
echo "target.com" | waybackurls | sort -u > wayback_urls.txt

# gau — aggregate from Wayback, CommonCrawl, OTX, URLScan
echo "target.com" | gau --threads 5 --subs | sort -u > gau_urls.txt

# waymore — comprehensive with filtering
waymore -i target.com -mode U -oU waymore_urls.txt -f -t 10
```

### Step 2: Identify Sensitive Endpoints

```bash
# Configuration and backup files
cat wayback_urls.txt | grep -iE \
  '\.(env|config|xml|json|yaml|yml|bak|old|sql|log|conf|ini|properties)$' \
  | sort -u > sensitive_files.txt

# Admin and management panels
cat wayback_urls.txt | grep -iE \
  '(admin|dashboard|manage|panel|console|cpanel|phpmyadmin|wp-admin)' \
  | sort -u > admin_panels.txt

# API endpoints
cat wayback_urls.txt | grep -iE \
  '(/api/|/v[0-9]/|/graphql|/rest/|/swagger|/openapi)' \
  | sort -u > api_endpoints.txt
```

### Step 3: Parameter Discovery

```bash
# Extract unique parameters
cat wayback_urls.txt | grep -oP '\?[^"#]+' | tr '&' '\n' | \
  cut -d= -f1 | sort -u > parameters.txt

# Find potentially injectable parameters
cat wayback_urls.txt | grep -iE \
  '(id=|page=|file=|path=|url=|redirect=|callback=|search=|query=|cmd=)' \
  | sort -u > injectable_params.txt
```

### Step 4: Historical Content Analysis

```bash
# Wayback CDX API — list all snapshots
curl -s "https://web.archive.org/cdx/search/cdx?url=target.com/*&output=json&fl=original,timestamp,statuscode&limit=10000" \
  | jq '.[]' > snapshots.json

# Retrieve specific historical version
curl -s "https://web.archive.org/web/20230601120000*/https://target.com/robots.txt"

# Compare current vs archived robots.txt
diff <(curl -s "https://web.archive.org/web/2023/https://target.com/robots.txt") \
     <(curl -s "https://target.com/robots.txt")
```

### Step 5: Probe Discovered Endpoints

```bash
# Check which historical endpoints are still live
httpx -l sensitive_files.txt -silent -sc -cl -mc 200 -o live_sensitive.txt

# Check admin panels
httpx -l admin_panels.txt -silent -sc -title -mc 200,301,302,401,403 -o live_admin.txt
```

## Detection Opportunities

- Wayback Machine queries are passive — no target interaction
- httpx probing of archived URLs generates direct HTTP requests
- Accessing old admin panels may trigger WAF alerts
- Bulk requests to non-existent historical paths produce 404 floods

## Verification

- [ ] Historical URLs extracted from multiple archive sources
- [ ] Sensitive configuration files and backups identified
- [ ] API endpoints and admin panels catalogued
- [ ] URL parameters extracted for injection testing
- [ ] Content changes over time analyzed for intelligence
- [ ] Live endpoints verified and prioritized for testing

## References

- [Wayback Machine](https://web.archive.org/)
- [waybackurls](https://github.com/tomnomnom/waybackurls)
- [gau](https://github.com/lc/gau)
- [waymore](https://github.com/xnl-h4ck3r/waymore)
- [CommonCrawl](https://commoncrawl.org/)
- [Wayback CDX API](https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server)

---
v1.0 | Validated: 2026-03-17
