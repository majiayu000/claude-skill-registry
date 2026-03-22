<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: building-threat-hunting-notebooks
description: >-
  Build automated threat hunting notebooks that query SIEM data, correlate events,
  detect anomalies, and generate hunt hypotheses. Covers KQL, SPL, and Sigma-based
  hunting with structured output for hunt documentation and playbook creation.
domain: cybersecurity
subdomain: automation-scripting
tags:
  - threat-hunting
  - siem
  - kql
  - splunk
  - sigma
  - anomaly-detection
  - mitre-attack
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1053.005", "T1059.001"]
---

# Building Threat Hunting Notebooks

## Overview

Threat hunting notebooks codify hunt hypotheses, data sources, queries, and
analysis steps into repeatable automation. This skill covers building Python-based
hunting tools that generate SIEM queries from ATT&CK techniques, analyze log
data for anomalies, track hunt progress, and produce structured hunt reports.

Mode: `[MODE: PURPLE]` — Detection engineering through proactive hunting.

## Prerequisites

| Requirement | Details |
|---|---|
| Python 3.10+ with `pandas` for data analysis (`pip install pandas`) | Required |
| SIEM access | Splunk (SPL), Microsoft Sentinel (KQL), or Elastic (DSL) |
| MITRE ATT&CK framework knowledge | Required |
| Log sources | endpoint, network, authentication, cloud |

## Key Concepts

### Hunt Hypothesis Generator

```python
HUNT_HYPOTHESES = {
    "T1059.001": {
        "name": "PowerShell Execution",
        "hypothesis": "Adversary uses PowerShell for execution and C2",
        "data_sources": ["process_creation", "script_block_logging"],
        "kql": 'DeviceProcessEvents | where FileName == "powershell.exe" | where ProcessCommandLine has_any ("-enc", "-nop", "IEX", "Invoke-")',
        "spl": 'index=endpoint process_name=powershell.exe (CommandLine="*-enc*" OR CommandLine="*IEX*" OR CommandLine="*Invoke-*")',
    },
    "T1053.005": {
        "name": "Scheduled Task",
        "hypothesis": "Adversary creates scheduled tasks for persistence",
        "data_sources": ["process_creation", "scheduled_task"],
        "kql": 'DeviceProcessEvents | where FileName == "schtasks.exe" | where ProcessCommandLine has "/create"',
        "spl": 'index=endpoint process_name=schtasks.exe CommandLine="*/create*"',
    },
}
```

### Anomaly Detection on Login Data

```python
from collections import Counter

def detect_login_anomalies(logins: list[dict], threshold: int = 3) -> list[dict]:
    """Detect anomalous login patterns — unusual hours, locations, frequency."""
    anomalies = []
    user_hours = {}
    for login in logins:
        user = login.get("user", "")
        hour = login.get("hour", 0)
        user_hours.setdefault(user, []).append(hour)

    for user, hours in user_hours.items():
        off_hours = [h for h in hours if h < 6 or h > 22]
        if len(off_hours) >= threshold:
            anomalies.append({
                "type": "off_hours_login",
                "user": user,
                "off_hours_count": len(off_hours),
                "severity": "medium",
            })
    return anomalies
```

## Workflow

### Step 1: Generate Hunt Queries

```bash
node scripts/agent.js --action generate-hunt --technique T1059.001 --format kql
```

### Step 2: Analyze Log Data

```bash
node scripts/agent.js --action analyze --log-file /tmp/auth-events.json
```

### Step 3: Create Hunt Report

```bash
node scripts/agent.js --action report --technique T1059.001 --output /tmp/hunt-report.json
```

## Verification

- [ ] Hunt queries are valid KQL/SPL syntax
- [ ] Hypothesis maps to specific ATT&CK technique
- [ ] Anomaly detection identifies off-hours and brute-force patterns
- [ ] Hunt report documents hypothesis, queries, findings, and conclusions
- [ ] Queries are tested against sample data before deployment

## References

- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [Sigma Rules Repository](https://github.com/SigmaHQ/sigma)
- [KQL Reference](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/)
- [Splunk SPL Reference](https://docs.splunk.com/Documentation/Splunk/latest/SearchReference)
