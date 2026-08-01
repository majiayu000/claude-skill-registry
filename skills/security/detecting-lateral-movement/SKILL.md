---
name: detecting-lateral-movement
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: detecting-lateral-movement
description: >-
  Detect adversary lateral movement across Windows and Linux environments.
  Covers PsExec, WMI, RDP, SSH, SMB, WinRM, and DCOM abuse with Sigma rules,
  KQL/SPL queries, and network-based detection strategies.
domain: cybersecurity
subdomain: blue-team
tags:
  - lateral-movement
  - detection-engineering
  - threat-hunting
  - mitre-attack
  - windows
  - network-security
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1021.001", "T1021.002", "T1021.003", "T1021.004", "T1021.006", "T1550.002"]
---

# Detecting Lateral Movement

## Overview

Lateral movement (MITRE ATT&CK Tactic TA0008) allows adversaries to pivot
through a network after initial access. Detection requires correlating
authentication events, service creation, network connections, and process
execution across multiple hosts and log sources.

## Prerequisites

| Requirement | Purpose |
|---|---|
| Windows Event Forwarding | Centralized Security/Sysmon logs |
| Sysmon with EID 1,3,17,18 | Process, network, pipe events |
| Network flow data | East-west traffic visibility |
| SIEM with cross-host correlation | Multi-source join capability |

## Key Concepts

### Lateral Movement Techniques

| Technique | ATT&CK ID | Telemetry Sources |
|---|---|---|
| PsExec | T1021.002 | EID 7045 (PSEXESVC), EID 4624 Type 3, Sysmon EID 17/18 |
| WMI | T1021.003 | EID 4624 Type 3, Sysmon EID 1 (wmiprvse child) |
| RDP | T1021.001 | EID 4624 Type 10, EID 1149 (TerminalServices) |
| WinRM | T1021.006 | EID 4624 Type 3, EID 91/168 (WinRM Operational) |
| SSH | T1021.004 | auth.log, sshd accepted/failed entries |
| DCOM | T1021.003 | Sysmon EID 1 (mmc.exe/dllhost child), network 135 |
| SMB | T1021.002 | EID 5140/5145 (share access), Sysmon EID 3 port 445 |
| Pass-the-Hash | T1550.002 | EID 4624 Type 3 + NTLM, LogonProcessName NTLMSSP |

### PsExec Detection (Sigma)

```yaml
title: PsExec Service Installation
id: c3f7a8d2-1b4e-4f6a-9d2c-8e7f5a3b6c1d
status: experimental
description: Detects PsExec service installation indicating lateral movement
logsource:
  product: windows
  service: system
detection:
  selection:
    EventID: 7045
    ServiceName|contains:
      - 'PSEXESVC'
      - 'psexec'
  condition: selection
falsepositives:
  - Legitimate admin use of PsExec with documented change ticket
level: high
tags:
  - attack.lateral_movement
  - attack.t1021.002
```

### WMI Lateral Movement Detection (KQL)

```kql
DeviceProcessEvents
| where Timestamp > ago(24h)
| where InitiatingProcessFileName =~ "wmiprvse.exe"
| where FileName in~ ("cmd.exe", "powershell.exe", "mshta.exe")
| project Timestamp, DeviceName, FileName, ProcessCommandLine,
    InitiatingProcessCommandLine
| join kind=inner (
    DeviceLogonEvents
    | where LogonType == "Network"
    | where Timestamp > ago(24h)
) on DeviceName
| project Timestamp, DeviceName, RemoteIP, FileName, ProcessCommandLine
```

### RDP Lateral Movement Detection (SPL)

```spl
index=windows (EventCode=4624 Logon_Type=10)
| stats earliest(_time) as first_rdp, latest(_time) as last_rdp,
    dc(dest) as dest_count, values(dest) as destinations by src_ip, user
| where dest_count > 2
| eval first_rdp=strftime(first_rdp, "%Y-%m-%d %H:%M:%S")
| sort -dest_count
```

### Network-Based Detection

```yaml
title: SMB Lateral Movement - Unusual Internal SMB Traffic
id: d4e8f9a1-2c5b-4d7e-8f3a-9b6c1d2e5f4a
status: experimental
description: Detects workstation-to-workstation SMB connections outside baseline
logsource:
  category: network_connection
  product: windows
detection:
  selection:
    DestinationPort: 445
    Initiated: 'true'
  filter_servers:
    DestinationIp|cidr:
      - '10.0.1.0/24'
  condition: selection and not filter_servers
falsepositives:
  - Peer-to-peer file sharing in flat networks
level: medium
tags:
  - attack.lateral_movement
  - attack.t1021.002
```

### Multi-Hop Detection Pattern

```kql
// Detect chains: Host A -> Host B -> Host C
DeviceLogonEvents
| where Timestamp > ago(24h)
| where LogonType == "Network"
| project SourceHost = RemoteDeviceName, DestHost = DeviceName,
    User = AccountName, T = Timestamp
| join kind=inner (
    DeviceLogonEvents
    | where LogonType == "Network"
    | project SourceHost2 = RemoteDeviceName, DestHost2 = DeviceName,
        User2 = AccountName, T2 = Timestamp
) on $left.DestHost == $right.SourceHost2
| where T2 > T and datetime_diff('minute', T2, T) < 30
| where User == User2
| project T, User, Hop1_Src = SourceHost, Hop1_Dest = DestHost,
    Hop2_Dest = DestHost2
```

## Workflow

1. **Baseline** — Map normal admin tool usage and approved remote access paths
2. **Monitor** — Deploy detections for each lateral movement technique
3. **Correlate** — Link authentication events to process creation on destination
4. **Hunt** — Search for multi-hop chains and unusual source-destination pairs
5. **Contain** — Isolate compromised hosts via EDR or VLAN reassignment
6. **Update** — Feed findings back into detection rules

## Verification

| Check | Method |
|---|---|
| PsExec detection fires | Run PsExec in test environment, verify alert |
| WMI detection fires | `wmic /node:target process call create "cmd"` triggers alert |
| RDP detection fires | RDP to test host, verify Type 10 logon captured |
| Network rules active | Sysmon EID 3 / Zeek conn.log generating for port 445 |
| Multi-hop detection | Simulate A→B→C chain, verify correlation query results |

## References

- [MITRE ATT&CK Lateral Movement](https://attack.mitre.org/tactics/TA0008/)
- [SANS Lateral Movement Detection](https://www.sans.org/white-papers/)
- [Sigma Lateral Movement Rules](https://github.com/SigmaHQ/sigma/tree/main/rules/windows/builtin/security)
