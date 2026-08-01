---
name: performing-api-fuzzing
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: performing-api-fuzzing
description: >-
  Fuzz REST/GraphQL APIs for IDOR, injection, broken auth, and mass assignment.
domain: cybersecurity
subdomain: red-team
tags:
  - api-fuzzing
  - rest-api
  - graphql
  - ffuf
  - idor
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1190"]
  tools: ["ffuf", "nuclei", "arjun", "kiterunner"]
---

# Performing API Fuzzing

## Overview

API fuzzing discovers vulnerabilities by testing endpoints with unexpected input. Targets BOLA/IDOR, mass assignment, injection flaws, and auth bypasses.

## Prerequisites

- Tools: ["ffuf", "nuclei", "arjun", "kiterunner"]
- Authorized testing engagement with written scope

## Key Concepts

See workflow sections for technique-specific concepts.

## Workflow

### Step 1: Endpoint Discovery
```bash
ffuf -u https://api.target.com/api/FUZZ -w api-endpoints.txt -mc 200,201,301,401,403
kr scan https://api.target.com -w routes-large.kite
```

### Step 2: Parameter Discovery
```bash
arjun -u https://api.target.com/api/users -m GET
ffuf -u 'https://api.target.com/api/users?FUZZ=test' -w params.txt -mc all -fc 404
```

### Step 3: IDOR Testing
```bash
ffuf -u https://api.target.com/api/users/FUZZ -w <(seq 1 1000) -H "Authorization: Bearer TOKEN" -mc 200
```

### Step 4: Input Fuzzing
```bash
ffuf -u https://api.target.com/api/search -X POST -d '{"query":"FUZZ"}' -w sqli.txt -mc all -fc 400
```

### Step 5: Auth Testing
```bash
nuclei -u https://api.target.com -t api/ -severity critical,high
```

## Detection Opportunities

| Signal | Source | Description |
|--------|--------|------------|
| High request rate | API gateway | Unusual volume |
| Sequential IDs | Logs | IDOR patterns |

```yaml
title: API Endpoint Fuzzing
id: d5e6f7a8-9b0c-1d2e-3f4a-5b6c7d8e9f0a
status: experimental
logsource:
  category: webserver
detection:
  selection:
    cs-uri-stem|startswith: '/api/'
    sc-status: [404, 405]
  timeframe: 1m
  condition: selection | count() by c-ip > 50
level: medium
tags:
  - attack.t1190
```

## Verification

- [ ] Technique executed successfully within scope
- [ ] Results documented with evidence
- [ ] Detection artifacts identified
- [ ] Cleanup performed after testing

## References

- [OWASP API Top 10](https://owasp.org/API-Security/)
- [ffuf](https://github.com/ffuf/ffuf)
- [Nuclei](https://github.com/projectdiscovery/nuclei)
