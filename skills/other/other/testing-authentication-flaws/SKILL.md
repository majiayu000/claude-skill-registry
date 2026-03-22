<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: testing-authentication-flaws
description: >-
  Identify and exploit authentication vulnerabilities including weak passwords, broken MFA, and session issues.
domain: cybersecurity
subdomain: bug-bounty
tags:
  - authentication
  - broken-auth
  - owasp
  - credential-security
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1078", "T1110"]
---

# Testing Authentication Flaws

## Overview

Identify and exploit authentication vulnerabilities including weak passwords, broken MFA, and session issues.

## Prerequisites

| Requirement | Install |
|---|---|
| Burp Suite | Web proxy |
| Hydra | `apt install hydra` |
| Python 3.10+ | For agent tooling |

## Key Concepts

Authentication testing covers password policies, MFA bypass,
session token analysis, credential stuffing, account lockout,
password reset flows, and OAuth/SAML flaws.

## Quick Reference

```bash
hydra -l admin -P wordlist.txt target.com http-post-form '/login:user=^USER^&pass=^PASS^:Invalid'
node agent.js test-lockout --url https://target.com/login --username admin
node agent.js test-mfa --url https://target.com/mfa --method bypass
node agent.js analyze-token --cookie session_id=abc123
```

## Workflow

1. Map auth endpoints
2. Test password policy
3. Test lockout/rate limiting
4. Analyze session tokens
5. Test MFA bypass
6. Test password reset
7. Document findings

## Verification

- Verify lockout triggers
- Confirm MFA secure
- Validate token entropy
- Check reset tokens expire
- Verify reproduction steps

## References

- OWASP Testing Guide — https://owasp.org/www-project-web-security-testing-guide/
- MITRE ATT&CK — https://attack.mitre.org/
- NIST SP 800-53 — https://csf.tools/reference/nist-sp-800-53/
