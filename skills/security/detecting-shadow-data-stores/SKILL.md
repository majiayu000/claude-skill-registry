---
name: detecting-shadow-data-stores
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: detecting-shadow-data-stores
description: >-
  Discover and inventory shadow data stores — unauthorized copies of sensitive
  data in personal drives, unsanctioned SaaS, developer machines, non-production
  databases, and cloud storage outside governance controls.
domain: cybersecurity
subdomain: data-security
tags:
  - shadow-data
  - dspm
  - data-sprawl
  - cloud-security
  - shadow-it
  - data-governance
  - casb
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1213"]
---

# Detecting Shadow Data Stores

## Overview

Shadow data stores are copies of sensitive data that exist outside governed
infrastructure — developer local databases, personal cloud storage, exported
CSVs on shared drives, unsanctioned SaaS tools, and non-production environments
with production data. These untracked copies evade DLP, encryption, access
controls, and retention policies, creating blind spots for compliance and
breach response. This skill covers discovery techniques using network analysis,
cloud API enumeration, endpoint scanning, and SaaS audit logs.

Mode: `[MODE: BLUE]` — Shadow data discovery and data sprawl remediation.

## Prerequisites

- Cloud provider API access (AWS, GCP, Azure) for resource enumeration
- CASB or SaaS management platform for shadow IT detection
- Network monitoring for unauthorized data transfer patterns
- Endpoint visibility for local data store detection

## Key Concepts

### Shadow Data Categories

| Category | Examples | Risk |
|----------|----------|------|
| Personal cloud | Google Drive, Dropbox, OneDrive personal | Data outside DLP |
| Developer copies | Local databases, docker volumes, dev exports | Unencrypted PII |
| SaaS uploads | Unsanctioned tools with data import | Third-party exposure |
| Non-prod with prod data | Staging/dev with real customer data | Reduced controls |
| Backup sprawl | Ad-hoc copies, snapshot clones | Untracked retention |
| Email attachments | Sensitive data in mailboxes | Long-term persistence |

### Discovery Methods

```
Shadow data discovery:
├── Cloud API enumeration
│   ├── List all S3 buckets, GCS buckets, Azure blobs
│   ├── Identify untagged or unclassified storage
│   ├── Check for public access misconfigurations
│   └── Scan for sensitive data patterns in metadata
├── Network analysis
│   ├── Monitor DNS for unsanctioned SaaS domains
│   ├── Detect uploads to personal cloud storage
│   ├── Identify database connections to unknown hosts
│   └── Track large outbound transfers
├── Endpoint scanning
│   ├── Scan for database files (*.sql, *.db, *.sqlite)
│   ├── Detect spreadsheets with sensitive data patterns
│   ├── Find exported CSVs/JSONs on user machines
│   └── Check for local database server processes
└── SaaS audit
    ├── OAuth app authorization logs
    ├── Data import/export activity in sanctioned SaaS
    ├── File sharing external link creation
    └── Third-party integration data flows
```

### Scanning CLI

```bash
# Scan for shadow data indicators in network logs
node scripts/agent.js --action scan --input /var/log/proxy.log \
  --output /tmp/shadow_data.json

# Enumerate cloud storage for unclassified data stores
node scripts/agent.js --action cloud-audit --input /tmp/cloud_inventory.json \
  --output /tmp/cloud_shadow.json

# Scan endpoint for local data stores
node scripts/agent.js --action endpoint --input /home/ \
  --extensions ".sql,.db,.sqlite,.csv,.xlsx" --output /tmp/endpoint_shadow.json
```

## Workflow

### Step 1: Enumerate Known Data Stores

Build baseline inventory of all sanctioned data locations.

### Step 2: Scan for Shadow Copies

```bash
node scripts/agent.js --action scan --input /var/log/proxy.log \
  --output /tmp/shadow_data.json
```

### Step 3: Audit Cloud Resources

```bash
node scripts/agent.js --action cloud-audit --input /tmp/cloud_inventory.json
```

### Step 4: Remediate Shadow Stores

Migrate data to governed locations or securely delete unauthorized copies.

## Detection

```yaml
title: Shadow Data Stores Detection
id: c55b5641-bd72-47c4-965a-db0449e17c85
status: experimental
description: Detects suspicious activity related to detecting shadow data stores techniques in data security context
logsource:
  category: file_access
  product: windows
detection:
  selection:
    TargetFilename: "*suspicious*"
  condition: selection
level: medium
tags:
  - attack.t1213
  - attack.exfiltration
falsepositives:
  - Data loss prevention tools scanning files during classification
```

## Verification

- [ ] Cloud storage enumeration identifies all untagged buckets
- [ ] Network monitoring detects unsanctioned SaaS data uploads
- [ ] Endpoint scanning finds local database and export files
- [ ] Non-production environments scanned for production data
- [ ] Shadow data remediation plan created with timelines
- [ ] Recurring discovery scans scheduled monthly
- [ ] Data governance policy updated with shadow data controls

## References

- [NIST SP 800-53 CM-8 — System Component Inventory](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [Cloud Security Alliance — Data Security Posture Management](https://cloudsecurityalliance.org/)
- [GDPR Article 30 — Records of Processing Activities](https://gdpr-info.eu/art-30-gdpr/)
- [Gartner — Data Security Posture Management Market Guide](https://www.gartner.com/)
