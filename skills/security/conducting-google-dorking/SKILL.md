---
name: conducting-google-dorking
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: conducting-google-dorking
description: >-
  Leverage advanced Google search operators and dorking techniques to discover
  exposed files, admin panels, credentials, sensitive directories, and
  misconfigurations on target domains.
domain: cybersecurity
subdomain: osint-recon
tags:
  - google-dorking
  - search-operators
  - ghdb
  - exposed-files
  - information-disclosure
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: >-
  Google Search, Bing, DuckDuckGo, pagodo, dorkscout,
  Google Hacking Database (GHDB).
metadata:
  mitre-attack:
    - "T1593.002"  # Search Open Websites/Domains: Search Engines
    - "T1596"      # Search Open Technical Databases
---

# Conducting Google Dorking

## Overview

Google dorking uses advanced search operators to locate information that
standard searches miss — exposed configuration files, login portals, directory
listings, database dumps, and inadvertently public documents. The Google
Hacking Database (GHDB) catalogs thousands of proven dork queries. Automated
tools like pagodo and dorkscout scale dorking across large target sets.

## Prerequisites

- Web browser or `curl` for manual dorking
- pagodo for automated GHDB-based dorking
- Python 3.10+ with `requests`, `beautifulsoup4`
- GHDB categories reference from Exploit-DB
- Awareness of Google rate limiting and CAPTCHA triggers

```bash
pip install pagodo requests beautifulsoup4
```

## Quick Reference

| Operator | Example | Purpose |
|----------|---------|---------|
| `site:` | `site:example.com` | Restrict to domain |
| `filetype:` | `filetype:pdf` | File type filter |
| `inurl:` | `inurl:admin` | URL path matching |
| `intitle:` | `intitle:"index of"` | Title matching |
| `intext:` | `intext:"password"` | Body text search |
| `ext:` | `ext:sql` | File extension |
| `cache:` | `cache:example.com` | Cached version |
| `-` | `-site:www.example.com` | Exclusion |
| `"..."` | `"exact phrase"` | Exact match |
| `OR` | `admin OR login` | Boolean OR |

## Workflow

### Step 1: Domain-Specific Dorks

```
# Exposed files and documents
site:example.com filetype:pdf OR filetype:xlsx OR filetype:docx
site:example.com filetype:sql OR filetype:bak OR filetype:old

# Configuration and environment files
site:example.com ext:conf OR ext:cfg OR ext:env OR ext:ini
site:example.com filetype:xml inurl:config

# Admin panels and login pages
site:example.com inurl:admin OR inurl:login OR inurl:portal
site:example.com intitle:"admin" OR intitle:"dashboard"

# Directory listings
site:example.com intitle:"index of" OR intitle:"directory listing"

# Error pages revealing stack info
site:example.com "stack trace" OR "error on line" OR "syntax error"
site:example.com "Warning:" "mysql_" OR "pg_" OR "ORA-"
```

### Step 2: Credential and Secret Discovery

```
# Exposed credentials
site:example.com "password" OR "passwd" filetype:txt
site:example.com inurl:credentials OR inurl:secret

# Git and version control exposure
site:example.com inurl:.git OR inurl:.svn
"example.com" site:github.com "password" OR "secret" OR "api_key"

# Cloud storage exposure
site:s3.amazonaws.com "example"
site:blob.core.windows.net "example"
site:storage.googleapis.com "example"
```

### Step 3: Technology Fingerprinting via Dorks

```
# Identify web technologies
site:example.com inurl:wp-content OR inurl:wp-admin
site:example.com inurl:joomla OR inurl:administrator
site:example.com "powered by" OR "running on"

# API endpoints
site:example.com inurl:api OR inurl:swagger OR inurl:graphql
site:example.com filetype:json inurl:api
```

### Step 4: Automated Dorking

```bash
# Pagodo — Google Hacking Database automation
pagodo -d example.com -g dorks.txt -l 100 -o results.json

# Custom dork list execution
while IFS= read -r dork; do
  echo "Dorking: $dork"
  curl -s "https://www.google.com/search?q=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$dork'))")" \
    -H "User-Agent: Mozilla/5.0" >> dork_results.html
  sleep 10  # Rate limiting
done < dorks.txt
```

### Step 5: Cross-Engine Dorking

```
# Bing equivalents
site:example.com filetype:pdf
instreamset:(url title):admin site:example.com

# DuckDuckGo
site:example.com filetype:env
```

## Detection Opportunities

- Web server logs show Google bot cache fetch patterns
- Exposed files discovered via dorking indicate misconfiguration
- Monitoring `site:yourdomain.com` results tracks information exposure
- Google Search Console alerts on indexing of sensitive paths

## Verification

- [ ] Domain-specific dorks executed for files, admin, configs
- [ ] Credential exposure checked in search results
- [ ] Technology stack fingerprinted via search operators
- [ ] Cloud storage exposure assessed
- [ ] Results documented with dork query and finding severity
- [ ] Rate limiting respected to avoid CAPTCHA/blocking

## References

- [Google Hacking Database (GHDB)](https://www.exploit-db.com/google-hacking-database)
- [Pagodo](https://github.com/opsdisk/pagodo)
- [Google Search Operators](https://ahrefs.com/blog/google-advanced-search-operators/)
- [DorkSearch](https://dorksearch.com/)

---
v1.0 | Validated: 2026-03-17
