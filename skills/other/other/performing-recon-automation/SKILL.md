<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
<!-- CIPHER is a trademark of defconxt. -->
---
name: performing-recon-automation
description: >-
  Automate bug bounty reconnaissance workflows including subdomain enumeration, port scanning, technology fingerprinting, and content discovery with custom pipelines.
domain: cybersecurity
subdomain: bug-bounty
tags:
  - recon
  - automation
  - subdomain
  - content-discovery
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1595"]
  frameworks: ["MITRE ATT&CK"]
  tools: ["subfinder", "httpx", "nuclei", "ffuf"]
---

# Performing Recon Automation

## Overview

Automate bug bounty reconnaissance workflows including subdomain enumeration, port scanning, technology fingerprinting, and content discovery with custom pipelines.

## Prerequisites

| Tool / Requirement | Details |
|---|---|
| `subfinder` | Security tooling |
| `httpx` | Security tooling |
| `nuclei` | Security tooling |
| `ffuf` | Security tooling |
| subfinder, httpx, nuclei, ffuf, automation scripting capability | Environment requirement |

## Quick Reference

```bash
# Quick start commands
node scripts/agent.js --help
node scripts/agent.js pipeline --domain target.com --full
```

## Workflow

### Step 1: Run Full Recon Pipeline

```bash
node scripts/agent.js pipeline --domain target.com --full
```

### Step 2: Enumerate and Probe

```bash
subfinder -d target.com | httpx -title -tech-detect -status-code
```

### Step 3: Content Discovery

```bash
ffuf -u https://target.com/FUZZ -w wordlist.txt -mc 200,301,302,403
```


## Verification

- **Verify pipeline execution**: `node scripts/agent.js pipeline --domain target.com --check`
- **Confirm results**: `node scripts/agent.js report --domain target.com`

## References

- MITRE ATT&CK: T1595
- Frameworks: MITRE ATT&CK
- Tools: subfinder, httpx, nuclei, ffuf
