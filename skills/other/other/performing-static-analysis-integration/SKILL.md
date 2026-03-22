<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: performing-static-analysis-integration
description: >-
  Integrate SAST tools into CI/CD pipelines for automated security scanning.
domain: cybersecurity
subdomain: secure-coding
tags:
  - static-analysis
  - sast
  - cicd
  - secure-coding
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1190"]
---

# Performing Static Analysis Integration

## Overview

Integrate SAST tools into CI/CD pipelines for automated security scanning.

## Prerequisites

| Requirement | Install |
|---|---|
| Semgrep | `pip install semgrep` |
| CI/CD platform | GitHub Actions |
| Python 3.10+ | For agent tooling |

## Key Concepts

Static analysis integration automates security scanning in CI/CD.
Configure SAST, define rulesets, manage findings, enforce gates.

## Quick Reference

```bash
semgrep ci --config=p/owasp-top-ten
node agent.js setup --tool semgrep --ci github-actions
node agent.js scan --directory src/ --rules owasp,security
node agent.js report --directory src/ --format sarif
```

## Workflow

1. Select SAST tools
2. Configure rulesets
3. Integrate CI/CD
4. Quality gates
5. Manage findings
6. Track remediation
7. Tune false positives

## Detection

```yaml
title: Static Analysis Integration Detection
id: 6cdb1b27-19b4-43aa-8bd0-817ea845e517
status: experimental
description: Detects suspicious activity related to performing static analysis integration techniques in secure coding context
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
  - attack.initial_access
falsepositives:
  - Static analysis tools scanning source code repositories
```

## Verification

- CI integration works
- Rules catch vulns
- Quality gates block
- Finding management
- FP tuning works

## References

- OWASP Testing Guide — https://owasp.org/www-project-web-security-testing-guide/
- MITRE ATT&CK — https://attack.mitre.org/
- NIST SP 800-53 — https://csf.tools/reference/nist-sp-800-53/
