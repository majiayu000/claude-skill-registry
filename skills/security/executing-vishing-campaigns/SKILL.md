<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: executing-vishing-campaigns
description: >-
  Plan and execute voice phishing campaigns to test employee resilience against phone-based social engineering.
domain: cybersecurity
subdomain: social-engineering
tags:
  - vishing
  - voice-phishing
  - social-engineering
  - phone-security
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1566.004"]
---

# Executing Vishing Campaigns

## Overview

Plan and execute voice phishing campaigns to test employee resilience against phone-based social engineering.

## Prerequisites

| Requirement | Install |
|---|---|
| VoIP platform | SIP infrastructure |
| Call recording | Authorized setup |
| Python 3.10+ | For agent tooling |

## Key Concepts

Vishing uses phone calls to manipulate targets into revealing
sensitive information. Campaigns require call scripts, caller ID
management, recording, and metrics tracking.

## Quick Reference

```bash
node agent.js prepare --campaign helpdesk-impersonation
node agent.js script --scenario password-reset --target IT-dept
node agent.js track --call-id C-001 --outcome success
node agent.js report --campaign helpdesk-impersonation
```

## Workflow

1. Define campaign scope and authorized targets
2. Set up VoIP infrastructure
3. Develop call scripts with branching logic
4. Train operators
5. Execute calls with tracking
6. Record outcomes
7. Analyze and report

## Verification

- Verify VoIP works
- Confirm recording captures both sides
- Validate script branches
- Check metrics capture outcomes
- Verify report includes success rates

## References

- OWASP Testing Guide — https://owasp.org/www-project-web-security-testing-guide/
- MITRE ATT&CK — https://attack.mitre.org/
- NIST SP 800-53 — https://csf.tools/reference/nist-sp-800-53/
