<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
<!-- CIPHER is a trademark of defconxt. -->
---
name: detecting-endpoint-lateral-movement
description: >-
  Detect lateral movement techniques on endpoints including remote service
  exploitation, pass-the-hash, WMI/WinRM abuse, RDP hijacking, PsExec usage,
  and SMB-based propagation through behavioral analysis and log correlation.
domain: cybersecurity
subdomain: endpoint-security
tags:
  - lateral-movement
  - pass-the-hash
  - wmi
  - winrm
  - rdp
  - psexec
  - smb
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1021.001", "T1021.002", "T1021.003", "T1021.006", "T1047", "T1550.002"]
  tools: [python3, powershell, sysmon, wireshark]
---

# Detecting Endpoint Lateral Movement

## Overview

Lateral movement allows attackers to pivot across the network after initial
compromise. Detection focuses on anomalous authentication patterns, remote
service usage from unexpected sources, network connection baselines, and
behavioral analysis of remote execution tools. Correlating endpoint logs
with network telemetry significantly improves detection fidelity.

## Prerequisites

| Requirement | Purpose |
|---|---|
| Sysmon | Process creation, network connection, named pipe events |
| Windows Security Log | Logon events (Type 3, 10), explicit credentials |
| Network flow data | SMB, WMI, WinRM, RDP connection baselines |
| EDR platform | Behavioral detection of lateral movement tools |

## Workflow

### Step 1: Detect PsExec and SMB-Based Execution

```powershell
# Sysmon EID 1 — PsExec service installation
Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Sysmon/Operational';Id=1} |
  Where-Object { $_.Properties[4].Value -like '*PSEXESVC*' -or
                 $_.Properties[4].Value -like '*psexec*' }

# Sysmon EID 17/18 — Named pipe creation (PsExec uses \psexesvc)
Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Sysmon/Operational';Id=17} |
  Where-Object { $_.Properties[5].Value -match 'psexesvc|msagent_|ATSVC' }

# Security EID 5145 — SMB share access from unusual sources
Get-WinEvent -FilterHashtable @{LogName='Security';Id=5145} |
  Where-Object { $_.Properties[8].Value -match 'ADMIN\$|C\$|IPC\$' }
```

### Step 2: Detect WMI and WinRM Remote Execution

```powershell
# WMI — process creation via remote WMI
Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Sysmon/Operational';Id=1} |
  Where-Object { $_.Properties[20].Value -like '*WmiPrvSE*' }

# WinRM — remote PowerShell sessions
Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-WinRM/Operational';Id=91} |
  Select-Object TimeCreated, Message

# Security EID 4648 — Explicit credential usage (runas/lateral)
Get-WinEvent -FilterHashtable @{LogName='Security';Id=4648} |
  Select-Object TimeCreated, @{N='Account';E={$_.Properties[1].Value}},
  @{N='Target';E={$_.Properties[5].Value}}
```

### Step 3: Detect RDP Lateral Movement

```powershell
# Security EID 4624 Type 10 — RDP logon
Get-WinEvent -FilterHashtable @{LogName='Security';Id=4624} |
  Where-Object { $_.Properties[8].Value -eq 10 } |
  Select-Object TimeCreated, @{N='User';E={$_.Properties[5].Value}},
  @{N='Source';E={$_.Properties[18].Value}}

# RDP session hijacking — tscon.exe without proper auth
Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Sysmon/Operational';Id=1} |
  Where-Object { $_.Properties[4].Value -like '*tscon*' }
```

### Step 4: Network-Based Correlation

```python
from typing import Any

def analyze_lateral_movement(connections: list[dict[str, str]]) -> dict[str, Any]:
    """Analyze network connections for lateral movement patterns."""
    findings = []
    smb_targets: dict[str, list[str]] = {}
    rdp_targets: dict[str, list[str]] = {}

    for conn in connections:
        src = conn.get("source", "")
        dst = conn.get("destination", "")
        port = int(conn.get("port", 0))

        if port == 445:
            smb_targets.setdefault(src, []).append(dst)
        elif port == 3389:
            rdp_targets.setdefault(src, []).append(dst)
        elif port == 5985:
            findings.append(f"WinRM: {src} -> {dst}")

    for src, targets in smb_targets.items():
        if len(targets) > 3:
            findings.append(f"HIGH: {src} contacted {len(targets)} SMB targets — possible sweep")

    return {
        "smb_sources": len(smb_targets),
        "rdp_sources": len(rdp_targets),
        "findings": findings,
    }
```

## Detection Opportunities

| Signal | Source | Description |
|--------|--------|-------------|
| PsExec service install | Sysmon EID 1/17 | PSEXESVC named pipe or process |
| Type 3 logon anomaly | Security EID 4624 | Network logon from workstation to workstation |
| SMB admin share access | Security EID 5145 | ADMIN$ or C$ access from non-admin host |

```yaml
title: PsExec Service Installation on Endpoint
id: f6a7b8c9-d012-3456-efgh-789012345678
status: experimental
description: Detects PsExec-style remote service installation via named pipe creation
logsource:
  category: pipe_created
  product: windows
detection:
  selection:
    PipeName|contains:
      - '\psexesvc'
      - '\msagent_'
      - '\ATSVC'
  condition: selection
falsepositives:
  - Legitimate PsExec usage by system administrators
level: high
tags:
  - attack.t1021.002
  - attack.lateral_movement
```

## Verification

- [ ] PsExec named pipe and service creation events detected
- [ ] WMI remote process creation logged and alerted
- [ ] WinRM session creation from unexpected sources triggers alert
- [ ] RDP Type 10 logon from workstation-to-workstation flagged
- [ ] SMB admin share access correlated with non-admin source hosts
- [ ] Network connection baselines established for lateral movement ports

## References

- [MITRE T1021 — Remote Services](https://attack.mitre.org/techniques/T1021/)
- [MITRE T1550.002 — Pass the Hash](https://attack.mitre.org/techniques/T1550/002/)
- [Detecting Lateral Movement — SANS](https://www.sans.org/white-papers/detecting-lateral-movement/)

---
v1.0 | Validated: 2026-03-18
