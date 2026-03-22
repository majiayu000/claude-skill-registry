<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: analyzing-network-flow-data
description: >-
  Analyze NetFlow, IPFIX, Zeek conn logs, and packet captures for threat
  detection. Covers flow analysis, beaconing detection, DNS tunneling,
  data exfiltration, and east-west traffic anomaly identification.
domain: cybersecurity
subdomain: blue-team
tags:
  - network-flow
  - zeek
  - netflow
  - pcap
  - network-security
  - threat-hunting
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1040", "T1071"]
---

# Analyzing Network Flow Data

## Overview

Network flow data provides metadata about connections (source, destination,
ports, bytes, duration) without full packet capture overhead. Zeek conn logs,
NetFlow/IPFIX, and firewall logs enable detection of C2 beaconing, lateral
movement, data exfiltration, and scanning activity.

## Prerequisites

| Requirement | Purpose |
|---|---|
| Zeek | Protocol analysis and conn.log generation |
| nfdump / nfcapd | NetFlow v5/v9/IPFIX collection and analysis |
| tcpdump / tshark | Packet capture and inspection |
| Python `pandas` | Flow data analysis at scale |
| SIEM ingestion | Centralized flow correlation |

## Key Concepts

### Zeek Conn Log Fields

| Field | Description | Detection Use |
|---|---|---|
| `id.orig_h` | Source IP | Identify attacking host |
| `id.resp_h` | Destination IP | Identify target / C2 server |
| `id.resp_p` | Destination port | Service identification |
| `proto` | Protocol (tcp/udp/icmp) | Protocol anomalies |
| `duration` | Connection duration | Long-lived C2 sessions |
| `orig_bytes` | Bytes from source | Data exfiltration volume |
| `resp_bytes` | Bytes from destination | Download detection |
| `conn_state` | Connection state | Scan detection (S0, REJ) |
| `history` | State history | Handshake analysis |

### Beaconing Detection

```bash
# Zeek conn.log — find periodic connections
cat conn.log | zeek-cut id.orig_h id.resp_h id.resp_p duration \
  | awk '$4 > 0' \
  | sort | uniq -c | sort -rn | head -20

# Python beaconing analysis
```

```python
import pandas as pd

df = pd.read_csv("conn.log", sep="\t", comment="#",
    names=["ts","uid","orig_h","orig_p","resp_h","resp_p",
           "proto","service","duration","orig_bytes","resp_bytes",
           "conn_state","local_orig","local_resp","missed_bytes",
           "history","orig_pkts","orig_ip_bytes","resp_pkts",
           "resp_ip_bytes","tunnel_parents"])
df["ts"] = pd.to_numeric(df["ts"], errors="coerce")

# Group by src-dst pair, compute inter-arrival times
for (src, dst), group in df.groupby(["orig_h", "resp_h"]):
    if len(group) < 20:
        continue
    times = group["ts"].sort_values().diff().dropna()
    cv = times.std() / times.mean() if times.mean() > 0 else 999
    if cv < 0.1 and len(group) > 50:
        print(f"BEACON: {src} -> {dst} interval={times.mean():.1f}s cv={cv:.3f} count={len(group)}")
```

### DNS Tunneling Detection

```bash
# Find unusually long DNS queries
cat dns.log | zeek-cut query qtype \
  | awk 'length($1) > 50' \
  | sort | uniq -c | sort -rn | head -20

# High-entropy subdomain detection
cat dns.log | zeek-cut query \
  | awk -F. '{print $1}' \
  | awk '{n=split($0,c,""); e=0; for(i=1;i<=n;i++) freq[c[i]]++;
          for(k in freq) {p=freq[k]/n; e-=p*log(p)/log(2); delete freq[k]}
          if(e>3.5 && n>20) print e, $0}' \
  | sort -rn | head -20
```

### Data Exfiltration Indicators

```bash
# Large outbound transfers
cat conn.log | zeek-cut id.orig_h id.resp_h orig_bytes \
  | awk '$3 > 10000000' \
  | sort -t$'\t' -k3 -rn | head -20

# Connections to uncommon ports
cat conn.log | zeek-cut id.resp_p proto \
  | sort | uniq -c | sort -rn \
  | awk '$1 < 5 {print}'
```

### Scan Detection

```bash
# SYN scan — many S0 (no response) connections
cat conn.log | zeek-cut id.orig_h conn_state \
  | grep 'S0' \
  | awk '{print $1}' | sort | uniq -c | sort -rn \
  | awk '$1 > 100 {print}'
```

## Workflow

1. **Collect** — Ensure Zeek/NetFlow is capturing all network segments
2. **Baseline** — Profile normal traffic patterns (top talkers, port usage)
3. **Hunt** — Apply beaconing, exfil, and scan detection queries
4. **Investigate** — Drill into suspicious flows with packet capture
5. **Correlate** — Match network IOCs to endpoint telemetry
6. **Block** — Update firewall rules for confirmed threats

## Detection

```yaml
title: Network Flow Data Detection
id: 942a0c90-39dc-4f1b-bb4f-e4e9df508015
status: experimental
description: Detects suspicious activity related to analyzing network flow data techniques in blue team context
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    CommandLine: "*analyzing*network*"
  condition: selection
level: medium
tags:
  - attack.t1040
  - attack.t1071
  - attack.defense_evasion
falsepositives:
  - Security team running authorized detection validation tools
```

## Verification

| Check | Method |
|---|---|
| Zeek running | `zeekctl status` — all workers running |
| Conn logs generating | `ls -la /var/log/zeek/current/conn.log` |
| NetFlow receiving | `nfdump -R /var/cache/nfcapd -s srcip` — data present |
| DNS logging active | `ls -la /var/log/zeek/current/dns.log` |
| SIEM ingestion | Search for Zeek/NetFlow events in platform |

## References

- [Zeek Documentation](https://docs.zeek.org/)
- [SANS Network Forensics Poster](https://www.sans.org/posters/network-forensics/)
- [RITA Beacon Detection](https://github.com/activecm/rita)
- [JA3/JA4 TLS Fingerprinting](https://github.com/salesforce/ja3)
