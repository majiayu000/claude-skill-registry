---
name: implementing-attack-path-validation
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: implementing-attack-path-validation
description: >-
  Validate attack paths through systematic testing of chained vulnerabilities and
  misconfigurations. Covers Active Directory attack path analysis, BloodHound
  integration, privilege escalation chain validation, and lateral movement path
  testing to verify that theoretical attack paths are exploitable in practice.
domain: cybersecurity
subdomain: purple-team
tags:
  - attack-path
  - bloodhound
  - active-directory
  - lateral-movement
  - privilege-escalation
  - graph-analysis
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1078"]
---

# Implementing Attack Path Validation

## Overview

Attack path validation confirms whether theoretical paths from initial access to
high-value targets are exploitable. Using BloodHound graph analysis combined with
Atomic Red Team execution, purple teams test each link in privilege escalation and
lateral movement chains to verify real-world exploitability and detection coverage.

## Prerequisites

| Requirement | Install |
|---|---|
| BloodHound CE | `docker compose -f docker-compose.yml up -d` |
| SharpHound | BloodHound data collector |
| Invoke-AtomicRedTeam | PowerShell module |
| Python 3.10+ | For agent tooling |
| Neo4j | Graph database (included with BloodHound) |
| bloodhound-python | `pip install bloodhound` |

## Key Concepts

### Attack Path Structure

```yaml
attack_path:
  name: "Domain Admin via Kerberoasting"
  start: "compromised-user@CORP.LOCAL"
  target: "Domain Admins"
  links:
    - step: 1
      from: "compromised-user"
      to: "svc-sql"
      technique: T1558.003  # Kerberoasting
      description: "Kerberoast SPN-enabled service account"
    - step: 2
      from: "svc-sql"
      to: "SQL-SERVER-01"
      technique: T1021.001  # Remote Desktop
      description: "RDP to SQL server with cracked creds"
    - step: 3
      from: "SQL-SERVER-01"
      to: "Domain Admins"
      technique: T1003.001  # LSASS dump
      description: "Extract DA token from LSASS"
```

### BloodHound Cypher Queries

```cypher
// Find shortest path to Domain Admins
MATCH p=shortestPath((u:User {name:'COMPROMISED@CORP.LOCAL'})-[*1..]->(g:Group {name:'DOMAIN ADMINS@CORP.LOCAL'}))
RETURN p

// Find Kerberoastable users with admin paths
MATCH (u:User {hasspn:true})
MATCH p=shortestPath((u)-[*1..]->(g:Group {name:'DOMAIN ADMINS@CORP.LOCAL'}))
RETURN u.name, length(p) ORDER BY length(p)

// Find unconstrained delegation computers
MATCH (c:Computer {unconstraineddelegation:true})
RETURN c.name, c.operatingsystem
```

## Workflow

### 1. Collect AD Data

```bash
# Run SharpHound collection
node agent.js collect-ad \
  --domain CORP.LOCAL \
  --method bloodhound-python \
  --output collections/

# Or via SharpHound
# SharpHound.exe -c All --outputdirectory collections/
```

### 2. Identify Attack Paths

```bash
# Query BloodHound for attack paths
node agent.js find-paths \
  --bloodhound-url http://localhost:8080 \
  --start "COMPROMISED@CORP.LOCAL" \
  --target "DOMAIN ADMINS@CORP.LOCAL" \
  --output paths/da_paths.json
```

### 3. Validate Each Link

```bash
# Test each step in the attack path
node agent.js validate-path \
  --path paths/da_paths.json \
  --output results/path_validation.json
```

### 4. Measure Detection Coverage

```bash
# Check detections for each path step
node agent.js path-coverage \
  --results results/path_validation.json \
  --siem-url https://splunk:8089 \
  --output reports/path_coverage.json
```

## Detection

```yaml
title: Attack Path Validation Detection
id: d8206bc4-8a2f-4a36-838d-306a15516d79
status: experimental
description: Detects suspicious activity related to implementing attack path validation techniques in purple team context
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    CommandLine: "*implementing*attack*"
  condition: selection
level: medium
tags:
  - attack.t1078
  - attack.defense_evasion
falsepositives:
  - Authorized adversary simulation exercises during scheduled windows
```

## Verification

| Check | Method |
|---|---|
| AD data collected | BloodHound shows graph data |
| Paths identified | At least one path from start to target |
| Links validated | Each step tested with atomic or manual test |
| Coverage measured | Detection status for each path step |

## References

- [BloodHound Community Edition](https://github.com/SpecterOps/BloodHound)
- [MITRE ATT&CK Lateral Movement](https://attack.mitre.org/tactics/TA0008/)
- [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)
