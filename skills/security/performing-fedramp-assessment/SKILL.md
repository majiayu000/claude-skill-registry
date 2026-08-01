---
name: performing-fedramp-assessment
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: performing-fedramp-assessment
description: >-
  Conduct FedRAMP authorization assessments including security control
  evaluation against NIST 800-53 baselines, SSP documentation review,
  POA&M tracking, and continuous monitoring for Low/Moderate/High impact
  levels. Automate evidence collection with OSCAL-formatted artifacts.
domain: cybersecurity
subdomain: compliance-audit
tags:
  - fedramp
  - nist-800-53
  - oscal
  - ssp
  - poam
  - continuous-monitoring
  - compliance
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: []
---

# Performing FedRAMP Assessment

## Overview

FedRAMP provides a standardized approach to security assessment for cloud
services used by federal agencies. Based on NIST 800-53, it defines Low (125
controls), Moderate (325 controls), and High (421 controls) baselines. This
skill automates control evaluation, SSP validation, POA&M management, and
OSCAL artifact generation for authorization packages.

Mode: `[MODE: BLUE]` — Federal compliance assessment and authorization support.

## Prerequisites

| Requirement | Install |
|---|---|
| OSCAL CLI | `npm install -g @oscal/oscal-cli` |
| InSpec | `gem install inspec` |
| AWS CLI | `pip install awscli` |
| Python 3.10+ | For agent tooling |
| jq | `apt install jq` |

## Key Concepts

### FedRAMP Authorization Levels

| Level | Controls | Use Case |
|---|---|---|
| Low | 125 | Low-sensitivity data (public websites) |
| Moderate | 325 | Controlled unclassified information (CUI) |
| High | 421 | Law enforcement, emergency services, financial |

### NIST 800-53 Control Families (FedRAMP Focus)

```
FedRAMP Control Families:
├── AC  — Access Control (25 controls at Moderate)
├── AU  — Audit and Accountability (16 controls)
├── CA  — Assessment, Authorization, Monitoring (9 controls)
├── CM  — Configuration Management (11 controls)
├── CP  — Contingency Planning (13 controls)
├── IA  — Identification and Authentication (11 controls)
├── IR  — Incident Response (10 controls)
├── MA  — Maintenance (6 controls)
├── MP  — Media Protection (8 controls)
├── PE  — Physical and Environmental Protection (20 controls)
├── PL  — Planning (4 controls)
├── PS  — Personnel Security (8 controls)
├── RA  — Risk Assessment (5 controls)
├── SA  — System and Services Acquisition (22 controls)
├── SC  — System and Communications Protection (44 controls)
├── SI  — System and Information Integrity (16 controls)
└── SR  — Supply Chain Risk Management (new in Rev 5)
```

### OSCAL SSP Structure

```json
{
  "system-security-plan": {
    "uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "metadata": {
      "title": "System Security Plan — CloudApp",
      "last-modified": "2026-03-01T00:00:00Z",
      "version": "1.0",
      "oscal-version": "1.1.2"
    },
    "import-profile": {
      "href": "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_MODERATE-baseline_profile.json"
    },
    "system-characteristics": {
      "system-name": "CloudApp Production",
      "security-sensitivity-level": "moderate",
      "system-information": {
        "information-types": [{
          "title": "Controlled Unclassified Information",
          "categorization": "moderate"
        }]
      },
      "authorization-boundary": {
        "description": "AWS VPC boundary with defined ingress/egress"
      }
    },
    "control-implementation": {
      "description": "FedRAMP Moderate baseline implementation",
      "implemented-requirements": []
    }
  }
}
```

### Automated Control Checks

```bash
# AC-2: Account Management — list inactive accounts
lastlog -b 90 | awk 'NR>1 && $2 != "Never" {print $1}'

# AU-2: Audit Events — verify audit daemon
systemctl is-active auditd && auditctl -l | wc -l

# CM-6: Configuration Settings — check SSH hardening
sshd -T | grep -E "^(permitrootlogin|passwordauthentication|maxauthtries)"

# IA-5: Authenticator Management — password aging
grep -E "^PASS_(MAX|MIN|WARN)_AGE" /etc/login.defs

# SC-28: Protection of Information at Rest
lsblk -o NAME,FSTYPE,MOUNTPOINT | grep crypt

# SI-2: Flaw Remediation — check pending patches
apt list --upgradable 2>/dev/null | grep -c security
```

## Workflow

### Step 1: Initialize Assessment Package

```bash
node scripts/agent.js --action init --level moderate \
  --system-name "CloudApp Production" --output /tmp/fedramp-init.json
```

### Step 2: Evaluate Controls

```bash
node scripts/agent.js --action assess --level moderate \
  --families ac,au,cm,ia,sc,si --output /tmp/fedramp-assess.json
```

### Step 3: Generate POA&M and Authorization Package

```bash
node scripts/agent.js --action report --input /tmp/fedramp-assess.json \
  --format poam --output /tmp/fedramp-poam.json
```

## Verification

- [ ] Correct baseline level selected (Low/Moderate/High)
- [ ] All required control families assessed
- [ ] SSP contains implemented-requirements for each control
- [ ] POA&M entries created for non-compliant controls with milestones
- [ ] OSCAL artifacts validate against schema
- [ ] Continuous monitoring plan defines monthly/quarterly/annual tasks

## References

- [FedRAMP Authorization](https://www.fedramp.gov/)
- [NIST 800-53 Rev 5](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [OSCAL Documentation](https://pages.nist.gov/OSCAL/)
- [FedRAMP OSCAL Resources](https://automate.fedramp.gov/)
