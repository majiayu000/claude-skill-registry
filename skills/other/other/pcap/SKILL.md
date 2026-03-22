---
name: pcap
description: Network traffic analysis - C2 detection, exfiltration, lateral movement
---

# PCAP Analysis

Analyze network captures:
- Connection analysis
- C2 beaconing detection
- Data exfiltration identification
- DNS tunneling detection
- Lateral movement patterns
- Protocol anomalies
- Artifact extraction

## Required Context
1. **PCAP File**: Path to capture file
2. **Focus**: C2, exfil, lateral, general
3. **Time Range**: If filtering needed

## Tools Used
zeek, tshark, tcpdump, suricata, NetworkMiner

## Example
```
/pcap
File: /captures/suspicious.pcap
Focus: C2 beaconing, exfiltration
```
