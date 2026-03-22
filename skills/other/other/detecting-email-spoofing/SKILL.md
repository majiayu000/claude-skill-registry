<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: detecting-email-spoofing
description: >-
  Detect and analyze email spoofing attacks including sender address forgery,
  display name deception, cousin domain abuse, and header manipulation using
  authentication results and heuristic analysis.
domain: cybersecurity
subdomain: email-security
tags:
  - spoofing
  - phishing
  - dmarc
  - header-analysis
  - bec
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1566.001", "T1534"]
  tools: [swaks, dig, python3, grep]
---

# Detecting Email Spoofing

## Overview

Email spoofing exploits the lack of built-in sender verification in SMTP.
Detection requires analyzing authentication headers (SPF, DKIM, DMARC results),
comparing envelope vs header addresses, identifying display name deception,
and detecting lookalike domains used in BEC attacks.

## Prerequisites

- Tools: swaks, dig, python3, grep
- Access to raw email headers for analysis
- List of executive names for display name monitoring

## Key Concepts

- **Envelope vs header**: Return-Path (envelope) may differ from From (header)
- **Display name spoofing**: Attacker uses executive name with external address
- **Cousin domains**: Lookalike domains (examp1e.com vs example.com)
- **Authentication-Results**: Gateway-added header with SPF/DKIM/DMARC verdicts

## Workflow

### Step 1: Authentication Header Analysis

```bash
# Extract authentication results
grep -E "^(Authentication-Results|Received-SPF|ARC-Authentication-Results):" headers.txt

# Check SPF/DKIM/DMARC results
grep "spf=" headers.txt | head -1
grep "dkim=" headers.txt | head -1
grep "dmarc=" headers.txt | head -1
```

### Step 2: Envelope vs Header Comparison

```bash
# Compare Return-Path vs From
RETURN_PATH=$(grep "^Return-Path:" headers.txt | grep -oE '[^< ]+@[^> ]+')
FROM=$(grep "^From:" headers.txt | grep -oE '[^< ]+@[^> ]+')
echo "Return-Path: $RETURN_PATH"
echo "From: $FROM"
[ "$RETURN_PATH" != "$FROM" ] && echo "WARNING: Envelope/header mismatch"

# Check Reply-To mismatch
REPLY_TO=$(grep "^Reply-To:" headers.txt | grep -oE '[^< ]+@[^> ]+')
[ -n "$REPLY_TO" ] && [ "$REPLY_TO" != "$FROM" ] && echo "WARNING: Reply-To differs"
```

### Step 3: Display Name Deception Detection

```python
import re

EXECUTIVES = ["John Smith", "Jane Doe", "CEO", "CFO"]

def check_display_name(from_header: str, org_domain: str) -> list[str]:
    findings = []
    match = re.match(r'"?([^"<]+)"?\s*<([^>]+)>', from_header)
    if not match:
        return ["Could not parse From header"]
    display_name, email = match.group(1).strip(), match.group(2)
    domain = email.split("@")[1] if "@" in email else ""
    for name in EXECUTIVES:
        if name.lower() in display_name.lower() and domain != org_domain:
            findings.append(f"HIGH: Display name '{display_name}' impersonates executive")
    if "@" in display_name:
        findings.append("MEDIUM: Email address in display name — double-from deception")
    return findings
```

### Step 4: Cousin Domain Detection

```bash
# Generate lookalike domain permutations
python3 -c "
domain = 'example.com'
name = domain.split('.')[0]
perms = [
    name.replace('l','1')+'.com', name.replace('o','0')+'.com',
    name+'s.com', name[:-1]+'.com', name+'-mail.com',
]
for p in set(perms):
    if p != domain: print(p)
"

# Check if lookalike domains exist
for d in examp1e.com examp1e.com examples.com; do
  dig A "$d" +short && echo "$d REGISTERED"
done
```

## Detection Opportunities

| Signal | Source | Description |
|--------|--------|-------------|
| DMARC failures | Email gateway | Messages failing DMARC from expected domains |
| Display name spoof | Email gateway | External email with internal executive names |
| Cousin domains | DNS logs | Queries to lookalike domains |

```yaml
title: External Email with Internal Executive Display Name
id: c3d4e5f6-a7b8-9012-cdef-345678901234
status: experimental
description: Detects external emails using display names of internal executives
logsource:
  category: email
  product: exchange
detection:
  selection:
    FromScope: "External"
    SenderDisplayName|contains:
      - "CEO Name"
      - "CFO Name"
  condition: selection
falsepositives:
  - Personal email accounts of actual executives
level: high
tags:
  - attack.t1534
  - attack.initial_access
```

## Verification

- [ ] Authentication header analysis workflow validated
- [ ] Envelope vs header comparison automated
- [ ] Display name deception rules deployed on gateway
- [ ] Cousin domain monitoring configured
- [ ] Spoofing detection integrated with SIEM alerting

## References

- [DMARC RFC 7489](https://datatracker.ietf.org/doc/html/rfc7489)
- [MITRE T1534 — Internal Spearphishing](https://attack.mitre.org/techniques/T1534/)
- [FBI BEC Advisory](https://www.ic3.gov/Media/Y2023/PSA230609)
