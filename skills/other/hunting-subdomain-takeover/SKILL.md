<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
<!-- CIPHER is a trademark of defconxt. -->
---
name: hunting-subdomain-takeover
description: >-
  Hunt for subdomain takeover vulnerabilities by identifying dangling DNS records pointing to deprovisioned cloud services, abandoned CNAME targets, and unclaimed resources.
domain: cybersecurity
subdomain: bug-bounty
tags:
  - subdomain-takeover
  - dns
  - dangling-cname
  - cloud
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1584.001"]
  frameworks: ["MITRE ATT&CK"]
  tools: ["subfinder", "subjack", "nuclei"]
---

# Hunting Subdomain Takeover

## Overview

Hunt for subdomain takeover vulnerabilities by identifying dangling DNS records pointing to deprovisioned cloud services, abandoned CNAME targets, and unclaimed resources.

## Prerequisites

| Tool / Requirement | Details |
|---|---|
| `subfinder` | Security tooling |
| `subjack` | Security tooling |
| `nuclei` | Security tooling |
| subfinder, subjack/can-i-take-over-xyz, nuclei templates, DNS access | Environment requirement |

## Quick Reference

```bash
# Quick start commands
node scripts/agent.js --help
subfinder -d target.com -o subdomains.txt
```

## Workflow

### Step 1: Enumerate Subdomains

```bash
subfinder -d target.com -o subdomains.txt
```

### Step 2: Check Takeover Candidates

```bash
node scripts/agent.js scan --domain target.com --subdomains subdomains.txt
```

### Step 3: Verify Takeover

```bash
node scripts/agent.js verify --subdomain vuln.target.com --service s3
```


## Verification

- **Verify scan**: `node scripts/agent.js scan --domain target.com --subdomains subdomains.txt`
- **Confirm takeover**: `node scripts/agent.js verify --subdomain vuln.target.com --service s3`

## References

- MITRE ATT&CK: T1584.001
- Frameworks: MITRE ATT&CK
- Tools: subfinder, subjack, nuclei
