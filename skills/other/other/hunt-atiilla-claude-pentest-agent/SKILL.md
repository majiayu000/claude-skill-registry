---
name: hunt
description: Hypothesis-driven threat hunting with MITRE ATT&CK mapping
---

# Threat Hunting

Proactive threat detection:
- Hypothesis-driven hunting
- MITRE ATT&CK TTP searches
- Anomaly detection
- Log analysis (Sysmon, Security, EDR)
- Network traffic hunting
- Cloud log hunting

## Required Context
1. **Hypothesis**: What threat/TTP to hunt
2. **Data Sources**: Available logs (Sysmon, Security, EDR, network)
3. **Time Range**: How far back to search
4. **Known Context**: Recent intel, incidents, or audit findings

## Tools Used
jq, grep, awk, zeek, sigma queries

## Example
```
/hunt
Hypothesis: Lateral movement via WMI (T1047)
Data: Sysmon logs
Time: Last 7 days
```
