---
name: conducting-social-engineering
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: conducting-social-engineering
description: >-
  Plan and execute social engineering attacks: pretexting, vishing, physical.
domain: cybersecurity
subdomain: red-team
tags:
  - social-engineering
  - pretexting
  - vishing
  - physical-security
  - osint
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1566", "T1598"]
  tools: ["gophish", "set", "beef-xss"]
---

# Conducting Social Engineering

## Overview

Social engineering exploits human psychology to bypass technical controls. Covers pretexting, vishing (voice phishing), physical access testing, and OSINT-driven targeting.

## Prerequisites

- Tools: ["gophish", "set", "beef-xss"]
- Authorized testing engagement with written scope

## Key Concepts

See workflow sections for technique-specific concepts.

## Workflow

### Step 1: OSINT Reconnaissance
```bash
# LinkedIn/company website enumeration
theHarvester -d target.com -b google,linkedin
# Employee directory mapping
# Organizational hierarchy research
```

### Step 2: Pretext Development
- Define scenario (IT support, vendor, executive)
- Prepare backstory and credentials
- Create supporting materials (badges, emails, letterhead)
- Rehearse conversation flows and objection handling

### Step 3: Vishing Campaign
- Configure caller ID spoofing
- Prepare call scripts with escalation paths
- Record calls (with authorization) for evidence
- Track success/failure metrics

### Step 4: Physical Access Testing
- Tailgating through secured entrances
- Badge cloning (with authorization and equipment)
- Dumpster diving for sensitive documents
- USB drop attacks (rubber ducky, bash bunny)

### Step 5: Reporting
- Document all social engineering attempts
- Include success/failure metrics
- Provide awareness training recommendations

## Detection Opportunities

| Signal | Source | Description |
|--------|--------|------------|
| Unusual calls | Phone logs | IT impersonation calls |
| Badge anomalies | Access logs | Tailgating indicators |
| USB events | EDR | Unknown USB devices |

```yaml
title: Suspicious USB Device Connected
id: f7a8b9c0-1d2e-3f4a-5b6c-7d8e9f0a1b2c
status: experimental
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 6416
  condition: selection
falsepositives:
  - Legitimate USB devices
level: low
tags:
  - attack.initial_access
  - attack.t1566
```

## Verification

- [ ] Technique executed successfully within scope
- [ ] Results documented with evidence
- [ ] Detection artifacts identified
- [ ] Cleanup performed after testing

## References

- [MITRE T1566](https://attack.mitre.org/techniques/T1566/)
- [SET](https://github.com/trustedsec/social-engineer-toolkit)
- [theHarvester](https://github.com/laramies/theHarvester)
