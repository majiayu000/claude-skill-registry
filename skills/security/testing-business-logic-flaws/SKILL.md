---
name: testing-business-logic-flaws
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: testing-business-logic-flaws
description: >-
  Identify and exploit business logic vulnerabilities including workflow bypasses and trust boundary violations.
domain: cybersecurity
subdomain: bug-bounty
tags:
  - business-logic
  - logic-flaws
  - workflow-bypass
  - bug-bounty
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1190"]
---

# Testing Business Logic Flaws

## Overview

Identify and exploit business logic vulnerabilities including workflow bypasses and trust boundary violations.

## Prerequisites

| Requirement | Install |
|---|---|
| Burp Suite | Request interception |
| App docs | Business rules |
| Python 3.10+ | For agent tooling |

## Key Concepts

Business logic flaws exploit workflow assumptions. Common: skipping
steps, parameter tampering, negative values, race conditions.

## Quick Reference

```bash
node agent.js test-flow --url https://target.com --skip-step 2
node agent.js tamper --request checkout.txt --param price --value -100
node agent.js race --url https://target.com/redeem --threads 50
node agent.js map-flow --url https://target.com --depth 5
```

## Workflow

1. Map workflows
2. Identify trust boundaries
3. Test step-skipping
4. Test tampering
5. Test race conditions
6. Test boundaries
7. Document impact

## Verification

- Verify workflow mapping
- Confirm step-skipping
- Validate tampering detection
- Check concurrency
- Verify business impact

## References

- OWASP Testing Guide — https://owasp.org/www-project-web-security-testing-guide/
- MITRE ATT&CK — https://attack.mitre.org/
- NIST SP 800-53 — https://csf.tools/reference/nist-sp-800-53/
