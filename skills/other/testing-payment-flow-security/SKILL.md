<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: testing-payment-flow-security
description: >-
  Test payment processing for price manipulation, currency abuse, coupon stacking, and replay attacks.
domain: cybersecurity
subdomain: bug-bounty
tags:
  - payment-security
  - financial
  - e-commerce
  - bug-bounty
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1190"]
---

# Testing Payment Flow Security

## Overview

Test payment processing for price manipulation, currency abuse, coupon stacking, and replay attacks.

## Prerequisites

| Requirement | Install |
|---|---|
| Burp Suite | Request interception |
| Test payment creds | Stripe test mode |
| Python 3.10+ | For agent tooling |

## Key Concepts

Payment testing covers price tampering, currency manipulation,
transaction replay, coupon stacking, and race conditions.
Focus on client-side trust boundaries.

## Quick Reference

```bash
node agent.js tamper --url https://target.com/checkout --param price --value 0.01
node agent.js coupon --url https://target.com/apply --codes codes.txt
node agent.js replay --request checkout.txt --count 5
node agent.js currency --url https://target.com/checkout --source USD --dest IRR
```

## Workflow

1. Map payment flow
2. Intercept requests
3. Test price manipulation
4. Test coupon stacking
5. Test replay
6. Test currency edge cases
7. Document financial impact

## Verification

- Verify price tampering
- Confirm coupon combos
- Validate replay detection
- Check currency edges
- Verify financial quantification

## References

- OWASP Testing Guide — https://owasp.org/www-project-web-security-testing-guide/
- MITRE ATT&CK — https://attack.mitre.org/
- NIST SP 800-53 — https://csf.tools/reference/nist-sp-800-53/
