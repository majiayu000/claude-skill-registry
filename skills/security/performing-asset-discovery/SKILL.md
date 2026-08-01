---
name: performing-asset-discovery
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: performing-asset-discovery
description: >-
  Systematically discover and inventory target assets including domains, IPs, and web apps within bug bounty scope.
domain: cybersecurity
subdomain: bug-bounty
tags:
  - asset-discovery
  - reconnaissance
  - bug-bounty
  - attack-surface
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1595", "T1590"]
---

# Performing Asset Discovery

## Overview

Systematically discover and inventory target assets including domains, IPs, and web apps within bug bounty scope.

## Prerequisites

| Requirement | Install |
|---|---|
| Amass | `go install github.com/owasp-amass/amass/v4/...@master` |
| httpx | `go install github.com/projectdiscovery/httpx/cmd/httpx@latest` |
| Python 3.10+ | For agent tooling |

## Key Concepts

Asset discovery maps the complete attack surface. Combines passive
sources (CT logs, DNS, WHOIS) with active probing (port scanning,
HTTP probing, technology fingerprinting).

## Quick Reference

```bash
amass enum -passive -d target.com -o domains.txt
cat domains.txt | httpx -status-code -title -o live.txt
node agent.js discover --domain target.com --mode passive
node agent.js probe --input domains.txt --output live.json
```

## Workflow

1. Define scope from program
2. Run passive enumeration
3. Active brute-forcing
4. Probe live services
5. Fingerprint technologies
6. Map API endpoints
7. Prioritize by exposure

## Verification

- Verify domains in scope
- Confirm probing accurate
- Validate fingerprinting
- Check deduplication
- Verify parseable output

## References

- OWASP Testing Guide — https://owasp.org/www-project-web-security-testing-guide/
- MITRE ATT&CK — https://attack.mitre.org/
- NIST SP 800-53 — https://csf.tools/reference/nist-sp-800-53/
