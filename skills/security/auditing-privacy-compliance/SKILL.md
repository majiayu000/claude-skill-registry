---
name: auditing-privacy-compliance
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
<!-- CIPHER is a trademark of defconxt. -->
---
name: auditing-privacy-compliance
description: >-
  Audit organizational privacy compliance against GDPR, CCPA/CPRA, and HIPAA
  frameworks by mapping data flows, assessing lawful bases, evaluating data
  subject rights fulfillment, and producing Data Protection Impact Assessments.
domain: cybersecurity
subdomain: compliance-audit
tags:
  - gdpr
  - ccpa
  - hipaa
  - dpia
  - privacy-audit
  - data-protection
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  frameworks: ["GDPR", "CCPA", "CPRA", "HIPAA"]
  tools: ["python3", "jq", "openssl"]
  mitre-attack: []
---

## Overview

Privacy compliance auditing evaluates how an organization collects, processes,
stores, and shares personal data against applicable regulations. This technique
covers GDPR (EU), CCPA/CPRA (California), and HIPAA (US healthcare) — mapping
data flows, verifying lawful processing bases, assessing data subject rights
implementation, and producing DPIAs for high-risk processing.

## Prerequisites

- Tools: `python3`, `jq`, `openssl`
- Data inventory / records of processing activities (RoPA)
- Privacy policy and consent management documentation
- Access to data processing system configurations
- Legal basis documentation for each processing activity

## Key Concepts

- **RoPA**: Record of Processing Activities — GDPR Art. 30 requirement
- **DPIA**: Data Protection Impact Assessment — required for high-risk processing
- **Lawful basis**: Legal justification for processing (consent, contract, etc.)
- **Data subject rights**: Access, rectification, erasure, portability, objection
- **Data minimization**: Collect only what is necessary for stated purpose
- **Privacy by Design**: GDPR Art. 25 — embed privacy into system design

## Workflow

### Step 1: Map Data Processing Activities

```bash
# Discover databases and data stores containing personal data
# Scan for PII patterns in database schemas
python3 -c "
import json

pii_columns = [
    'email', 'phone', 'ssn', 'social_security', 'date_of_birth',
    'address', 'credit_card', 'ip_address', 'first_name', 'last_name',
    'passport', 'driver_license', 'medical_record', 'diagnosis',
]

# Simulated schema scan — replace with actual DB introspection
schemas = {
    'users': ['id', 'email', 'first_name', 'last_name', 'phone', 'address'],
    'orders': ['id', 'user_id', 'credit_card', 'billing_address'],
    'health_records': ['id', 'patient_id', 'diagnosis', 'ssn'],
}

findings = []
for table, columns in schemas.items():
    pii_found = [c for c in columns if any(p in c for p in pii_columns)]
    if pii_found:
        findings.append({'table': table, 'pii_columns': pii_found})

print(json.dumps(findings, indent=2))
"
```

### Step 2: Assess GDPR Compliance (Art. 5-7, 12-23, 25, 30, 35)

```bash
# GDPR compliance checklist assessment
cat << 'EOF'
GDPR Audit Checklist:
[ ] Art. 5  — Data processing principles documented
[ ] Art. 6  — Lawful basis identified for each processing activity
[ ] Art. 7  — Consent freely given, specific, informed, unambiguous
[ ] Art. 13 — Privacy notice provided at collection point
[ ] Art. 15 — Subject access request (SAR) process implemented
[ ] Art. 17 — Right to erasure / right to be forgotten process
[ ] Art. 20 — Data portability mechanism available
[ ] Art. 25 — Privacy by Design and by Default implemented
[ ] Art. 30 — Records of Processing Activities maintained
[ ] Art. 33 — Breach notification process (72-hour requirement)
[ ] Art. 35 — DPIA conducted for high-risk processing
[ ] Art. 37 — DPO appointed (if required)
EOF
```

### Step 3: Assess CCPA/CPRA Compliance

```bash
# CCPA consumer rights verification
cat << 'EOF'
CCPA/CPRA Audit Checklist:
[ ] Right to Know — Process for consumers to request collected data
[ ] Right to Delete — Deletion mechanism and verification
[ ] Right to Opt-Out — "Do Not Sell" link on website
[ ] Right to Non-Discrimination — No service denial for exercising rights
[ ] Right to Correct — Mechanism to correct inaccurate personal info
[ ] Right to Limit Use of Sensitive PI — Restrict processing
[ ] Financial incentive disclosures — Document value of data
[ ] Service provider contracts — Include CCPA clauses
[ ] Data retention schedule — Defined and enforced
EOF
```

### Step 4: Assess HIPAA Compliance

```bash
# HIPAA Security Rule technical safeguards check
# Verify encryption of PHI at rest
find /data/health -type f -name "*.db" -exec file {} \; | \
  grep -v "encrypted\|SQLCipher"

# Check access controls on PHI systems
getfacl /data/health/ 2>/dev/null

# Verify audit logging for PHI access
grep -c 'health_records' /var/log/audit/audit.log
```

### Step 5: Conduct Data Protection Impact Assessment

```bash
# Generate DPIA template for high-risk processing
python3 -c "
import json

dpia = {
    'processing_activity': 'Customer profiling for marketing',
    'data_categories': ['behavioral', 'demographic', 'purchase_history'],
    'necessity_assessment': {
        'purpose': 'Personalized marketing recommendations',
        'lawful_basis': 'legitimate_interest',
        'proportionality': 'Data limited to purchase and browsing history',
    },
    'risks': [
        {
            'risk': 'Unwanted profiling without awareness',
            'likelihood': 'medium',
            'severity': 'high',
            'mitigation': 'Transparent opt-out mechanism',
        },
        {
            'risk': 'Data breach exposing behavioral profiles',
            'likelihood': 'low',
            'severity': 'high',
            'mitigation': 'Encryption at rest and in transit',
        },
    ],
    'dpo_consultation': True,
    'supervisory_authority_consultation': False,
}
print(json.dumps(dpia, indent=2))
"
```

### Step 6: Verify Data Subject Rights Implementation

```bash
# Test SAR (Subject Access Request) endpoint
curl -s -X POST "https://target.com/api/privacy/sar" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"request_type": "access"}' | jq '.status, .estimated_days'

# Test deletion request endpoint
curl -s -X POST "https://target.com/api/privacy/delete" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"request_type": "erasure", "scope": "all"}' | jq '.status'
```

## Detection Opportunities

| Signal | Source | Description |
|--------|--------|-------------|
| Bulk PII export | DLP | Large volume personal data extraction |
| Consent record modification | Application logs | Tampering with consent records |
| PHI access without authorization | HIPAA audit logs | Unauthorized health data access |
| Cross-border data transfer | Network monitor | PII sent to non-adequate jurisdictions |

```yaml
title: Bulk Personal Data Export Detected
id: e5f6a7b8-c9d0-1234-ef01-23456789abcd
status: experimental
description: Detects large-scale export of personal data records
logsource:
  category: application
detection:
  selection:
    action: "data_export"
    record_count|gt: 1000
  filter_authorized:
    user.role: "dpo"
  condition: selection and not filter_authorized
falsepositives:
  - Authorized data migration by DPO or data engineering team
level: high
tags:
  - attack.t1530
  - attack.collection
```

## Verification

- [ ] Data processing inventory completed with PII mapping
- [ ] Lawful basis documented for each processing activity
- [ ] Data subject rights endpoints tested and functional
- [ ] DPIA conducted for high-risk processing activities
- [ ] Consent management mechanism verified
- [ ] Breach notification process documented and tested
- [ ] Privacy policy reviewed for accuracy and completeness

## References

- [GDPR Full Text](https://gdpr-info.eu/)
- [CCPA/CPRA Text](https://oag.ca.gov/privacy/ccpa)
- [HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/)
- [ICO DPIA Guidance](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/data-protection-impact-assessments-dpias/)
