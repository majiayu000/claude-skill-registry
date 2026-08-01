---
name: analyzing-netflow-data
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: analyzing-netflow-data
description: >-
  Collect and analyze NetFlow/IPFIX/sFlow data for network visibility, threat hunting, capacity planning, and anomaly detection using nfdump, SiLK, and flow-based analysis techniques.
domain: cybersecurity
subdomain: network-security
tags:
  - netflow
  - ipfix
  - sflow
  - nfdump
  - silk
  - traffic-analysis
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack: ["T1071", "T1048", "T1572"]
  nist-csf: ["DE.CM-1", "DE.AE-2", "PR.PT-4"]
  uuid: 0167163b-13c9-4fd0-aa88-de9af8b58be0
---

# Analyzing NetFlow Data

## Overview

NetFlow provides metadata about every network conversation without capturing packet payloads.
This makes it ideal for long-term traffic analysis, threat hunting at scale, and detecting
anomalies like data exfiltration, lateral movement, and C2 beaconing. Flow data is orders
of magnitude smaller than full PCAP, enabling months of retention.

Mode: `[MODE: BLUE]` for monitoring; `[MODE: INCIDENT]` for flow-based forensics.

## Prerequisites

| Requirement | Details |
|---|---|
| NetFlow v5/v9 or IPFIX export from routers/switches | Required |
| Flow collector (nfcapd, softflowd, or commercial) | Required |
| nfdump for CLI analysis | Required |
| SiLK for large-scale flow analysis | Required |
| Storage for flow data (~1-5GB/day per busy network) | Required |

## Key Concepts

### NetFlow Record Fields

```
Key Fields:
├── Source IP / Destination IP
├── Source Port / Destination Port
├── Protocol (TCP/UDP/ICMP)
├── Bytes transferred
├── Packets count
├── Flow start / end time
├── TCP flags
├── Type of Service (ToS)
└── Input / Output interface
```

### nfdump Analysis Commands

```bash
# Top talkers by bytes
nfdump -r nfcapd.* -s srcip/bytes -n 20

# Top destination ports
nfdump -r nfcapd.* -s dstport/flows -n 20

# Large outbound transfers (exfiltration hunting)
nfdump -r nfcapd.* -o extended "src net 10.0.0.0/8 and bytes > 100000000" \
  -s record/bytes -n 20

# Long-duration flows (C2 beaconing)
nfdump -r nfcapd.* -o extended "duration > 3600" -s record/duration -n 20

# Unusual ports (non-standard services)
nfdump -r nfcapd.* "dst port > 1024 and proto tcp and flags S" \
  -s dstport/flows -n 50

# Specific host investigation
nfdump -r nfcapd.* "src ip 10.10.1.50 or dst ip 10.10.1.50" \
  -o extended -O tstart

# Lateral movement detection
nfdump -r nfcapd.* "src net 10.0.0.0/8 and dst net 10.0.0.0/8 and \
  (dst port 445 or dst port 135 or dst port 3389 or dst port 22)" \
  -s record/bytes -n 30
```

### Flow-Based Threat Hunting

```bash
# Beaconing detection — regular interval connections
nfdump -r nfcapd.* "src ip 10.10.1.50 and dst port 443" \
  -o "fmt:%ts %td %sa %da %dp %byt" | \
  awk '{print $1}' | sort | uniq -c

# DNS exfiltration — high-volume DNS
nfdump -r nfcapd.* "dst port 53 and bytes > 10000" \
  -s srcip/bytes -n 20

# Scan detection — many destinations from single source
nfdump -r nfcapd.* "flags S and not flags A" \
  -s srcip/flows -n 20
```

## Workflow

### Step 1: Configure Flow Collection

```bash
# Start nfcapd collector
nfcapd -w -D -l /var/cache/nfdump -p 2055 -T all
```

### Step 2: Baseline Normal Traffic

```bash
# Weekly traffic profile
nfdump -r nfcapd.* -s srcip/bytes -n 50 > baseline_talkers.txt
nfdump -r nfcapd.* -s dstport/flows -n 50 > baseline_ports.txt
```

### Step 3: Anomaly Detection

```bash
# Compare current to baseline
nfdump -r nfcapd.* -t "$(date -d '1 hour ago' +%Y/%m/%d.%H:%M:%S)" \
  -s srcip/bytes -n 20
```

### Step 4: Investigation

Drill down on anomalous hosts/flows with targeted nfdump queries.

## Detection

```yaml
title: Netflow Data Detection
id: a6c02d9d-06c9-45b9-a299-036bacd52017
status: experimental
description: Detects suspicious activity related to analyzing netflow data techniques in network security context
logsource:
  category: firewall
  product: linux
detection:
  selection:
    Action: blocked
  condition: selection
level: medium
tags:
  - attack.t1071
  - attack.t1048
  - attack.t1572
  - attack.command_and_control
falsepositives:
  - Network monitoring tools performing scheduled connectivity checks
```


**Detection Opportunities**

| Indicator | Source | Detection Logic |
|---|---|---|
| Netflow Data Detection | linux/firewall | Sigma rule (medium) |
| ATT&CK Coverage | MITRE ATT&CK | T1071, T1048, T1572 |

## Verification

- [ ] Flow export enabled on all network devices
- [ ] Flow collector running and ingesting data
- [ ] Baseline traffic profiles documented
- [ ] Alerting on anomalous traffic volumes
- [ ] Long-duration flow monitoring for C2
- [ ] Large transfer detection for exfiltration
- [ ] Lateral movement flow patterns monitored
- [ ] Flow data retained per compliance requirements

## References

- [nfdump Documentation](https://github.com/phaag/nfdump)
- [SiLK Analysis Suite](https://tools.netsa.cert.org/silk/)
- NIST SP 800-86: Guide to Integrating Forensic Techniques
- Cisco NetFlow Configuration Guide
