---
name: testing-graphql-security
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
<!-- CIPHER is a trademark of defconxt. -->
---
name: testing-graphql-security
description: >-
  Test GraphQL API security including introspection disclosure, query depth attacks, batching abuse, IDOR via node interface, and injection through resolver arguments.
domain: cybersecurity
subdomain: bug-bounty
tags:
  - graphql
  - introspection
  - query-depth
  - api-security
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1190"]
  frameworks: ["MITRE ATT&CK", "OWASP"]
  tools: ["burpsuite", "graphql-voyager", "inql"]
---

# Testing Graphql Security

## Overview

Test GraphQL API security including introspection disclosure, query depth attacks, batching abuse, IDOR via node interface, and injection through resolver arguments.

## Prerequisites

| Tool / Requirement | Details |
|---|---|
| `burpsuite` | Security tooling |
| `graphql-voyager` | Security tooling |
| `inql` | Security tooling |
| Burp Suite with InQL, GraphQL Voyager, target GraphQL endpoint | Environment requirement |

## Quick Reference

```bash
# Quick start commands
node scripts/agent.js --help
node scripts/agent.js enumerate --url https://target.com/graphql
```

## Workflow

### Step 1: Enumerate Schema

```bash
node scripts/agent.js enumerate --url https://target.com/graphql
```

### Step 2: Test Query Depth

```bash
node scripts/agent.js test --url https://target.com/graphql --vector depth
```

### Step 3: Fuzz Resolvers

```bash
node scripts/agent.js fuzz --url https://target.com/graphql --wordlist resolvers.txt
```


## Verification

- **Verify schema enumeration**: `node scripts/agent.js enumerate --url https://target.com/graphql`
- **Confirm findings**: `node scripts/agent.js report --url https://target.com/graphql`

## References

- MITRE ATT&CK: T1190
- Frameworks: MITRE ATT&CK, OWASP
- Tools: burpsuite, graphql-voyager, inql
