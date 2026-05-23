<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: auditing-wireless-encryption-config
description: >-
  Audit wireless encryption configurations to identify weak protocols (WEP, TKIP), misconfigured WPA2/WPA3, open networks, and WPS vulnerabilities.
domain: cybersecurity
subdomain: wireless-security
tags:
  - wireless-audit
  - wpa2
  - wpa3
  - encryption
  - wps
  - compliance
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack: ["T1040", "T1557.002"]
  nist-csf: ["PR.DS-2", "PR.AC-5", "ID.RA-1"]
  uuid: 6774b65e-1e08-4965-8389-d4e6e38a67ad
---

# Auditing Wireless Encryption Config

## Overview

Wireless encryption auditing evaluates the security configuration of access points and
wireless networks. This covers identification of deprecated protocols (WEP, TKIP), WPA2/WPA3
configuration validation, WPS status checking, cipher suite analysis, and compliance verification
against security baselines. Regular auditing prevents configuration drift and weak encryption.

Mode: `[MODE: BLUE]` for this technique.

## Prerequisites

| Requirement | Details |
|---|---|
| Monitor-mode wireless adapter | Required |
| airodump-ng for passive encryption detection | Required |
| wash (from reaver package) for WPS detection | Required |
| wpa_supplicant for configuration testing | Required |
| Compliance baseline (e.g., CIS Wireless Benchmark) | Required |

## Key Concepts

### Encryption Hierarchy

```
Wireless Encryption (Weakest → Strongest):
├── OPN — Open / No encryption [CRITICAL]
├── WEP — Wired Equivalent Privacy [CRITICAL — trivially broken]
├── WPA-TKIP — Temporal Key Integrity Protocol [HIGH — deprecated]
├── WPA2-PSK (CCMP) — AES-based [MEDIUM — dictionary attackable]
├── WPA2-Enterprise (802.1X) — RADIUS auth [LOW — if properly configured]
├── WPA3-SAE — Simultaneous Auth of Equals [LOW — resistant to offline attack]
└── WPA3-Enterprise (192-bit) — Suite B cryptography [INFO — strongest]
```

### Passive Encryption Audit

```bash
# Scan all networks — identify encryption type
sudo airodump-ng wlan0mon --output-format csv -w encryption_audit

# Parse results for weak encryption
cat encryption_audit-01.csv | awk -F',' '/WEP|OPN|TKIP/{print $1,$4,$6,$7}'

# Identify WPA version and cipher from airodump output columns:
# ENC = encryption type (WEP, WPA, WPA2, WPA3, OPN)
# CIPHER = cipher suite (CCMP, TKIP, WEP)
# AUTH = authentication (PSK, MGT/802.1X, SAE)
```

### WPS Audit

```bash
# Scan for WPS-enabled APs
wash -i wlan0mon

# Check WPS lock status
wash -i wlan0mon -C  # Show only APs with WPS enabled

# WPS version and status columns:
# Lck = locked (rate-limited after failed attempts)
# Ver = WPS version
# WPS-enabled APs are vulnerable to PIN brute force (reaver/bully)
```

### Cipher Suite Validation

```bash
# Inspect RSN Information Element in beacon
tshark -i wlan0mon -Y 'wlan.ssid == "CorpWiFi"' \
  -T fields -e wlan.sa -e wlan.rsn.pcs.type -e wlan.rsn.akms.type

# RSN cipher types: 4=CCMP (good), 2=TKIP (bad)
# RSN AKM types: 2=PSK, 1=802.1X, 8=SAE
```

## Workflow

### Step 1: Full Spectrum Scan

```bash
sudo airodump-ng --band abg wlan0mon -w full_audit --output-format csv,pcap
```

### Step 2: Classify Findings

Categorize each network by encryption strength: Critical (OPN/WEP), High (TKIP), Medium (WPA2-PSK), Low (WPA2-Enterprise/WPA3).

### Step 3: WPS Assessment

```bash
wash -i wlan0mon | tee wps_audit.txt
```

### Step 4: Configuration Deep-Dive

Inspect RSN/WPA information elements for cipher and AKM misconfigurations.

### Step 5: Compliance Check

Map findings against organizational wireless security policy and CIS benchmarks.

### Step 6: Generate Audit Report

Document all findings with severity, affected AP, and specific remediation.

## Detection

```yaml
title: Auditing Wireless Encryption Config Detection
id: 0043ca67-101d-4de7-8d68-39c1ca0cfe5b
status: experimental
description: Detects suspicious activity related to auditing wireless encryption config techniques in wireless security context
logsource:
  category: network_connection
  product: windows
detection:
  selection:
    DestinationPort: 443
    Initiated: "true"
  condition: selection
level: medium
tags:
  - attack.t1040
  - attack.t1557.002
  - attack.initial_access
falsepositives:
  - Wireless intrusion detection system performing routine monitoring
```


**Detection Opportunities**

| Indicator | Source | Detection Logic |
|---|---|---|
| Auditing Wireless Encryption Config Detection | windows/network_connection | Sigma rule (medium) |
| ATT&CK Coverage | MITRE ATT&CK | T1040, T1557.002 |

## Verification

- [ ] All wireless networks scanned across all bands (2.4/5 GHz)
- [ ] No WEP or open networks detected (or justified exceptions)
- [ ] TKIP usage flagged and migration planned
- [ ] WPS disabled on all access points
- [ ] WPA2-Enterprise with CCMP minimum for corporate networks
- [ ] Audit findings documented with remediation timeline

## References

- CIS Benchmark for Wireless Networks
- NIST SP 800-153: Guidelines for Securing WLANs
- Wi-Fi Alliance WPA3 Specification
- PCI DSS Requirement 4.1: Wireless Encryption
