---
name: detecting-identity-sprawl
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: detecting-identity-sprawl
description: >-
  Identify and remediate identity sprawl — uncontrolled proliferation of accounts, service accounts, and entitlements that increases attack surface.
domain: cybersecurity
subdomain: identity-security
tags:
  - identity-sprawl
  - account-proliferation
  - shadow-identity
  - attack-surface
  - identity-hygiene
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1078"]
---

# Detecting Identity Sprawl

## Overview

Identity sprawl occurs when identities proliferate across systems without
centralized visibility or governance. Orphaned accounts, unused service
principals, and dormant entitlements create attack surface that adversaries
exploit.

## Prerequisites

| Requirement | Install |
|---|---|
| Multi-cloud visibility | Access to identity providers |
| CMDB / asset inventory | Known identity sources |
| IGA platform | Entitlement analytics |
| Python 3.10+ | For agent tooling |

## Key Concepts

### Sprawl Indicators

- **Orphaned accounts** — Active accounts for terminated employees
- **Dormant accounts** — No login activity for 90+ days
- **Duplicate identities** — Same person with multiple accounts
- **Unused entitlements** — Permissions never exercised
- **Shadow identities** — Accounts outside governance
- **Service account sprawl** — Ungoverned service principals

### Detection Methods

| Method | Target | Signal |
|---|---|---|
| Last login analysis | Dormant accounts | No sign-in > 90 days |
| HR correlation | Orphaned accounts | Active account, no HR record |
| Entitlement analytics | Unused permissions | Access never exercised |
| Cross-system correlation | Duplicates | Same email across providers |
| App registration audit | Shadow identities | Unmanaged OAuth apps |

### Remediation Approach

1. **Identify** — Discover sprawl through automated analysis
2. **Classify** — Categorize by sprawl type and risk
3. **Notify** — Alert account owners or managers
4. **Grace period** — Allow time for justification
5. **Disable** — Deactivate unjustified accounts
6. **Delete** — Remove after retention period
7. **Prevent** — Enforce governance for new creation

## Workflow

1. **Inventory all identity sources** — catalog identity providers
2. **Correlate with HR data** — identify orphaned accounts
3. **Analyze login activity** — flag accounts with no sign-in for 90+ days
4. **Audit entitlements** — identify permissions never exercised
5. **Detect shadow identities** — find accounts outside governance
6. **Calculate sprawl metrics** — quantify identity attack surface
7. **Remediate and govern** — disable orphaned accounts, establish controls

## Quick Reference

```bash
# Run the agent
node scripts/agent.js analyze --target <scope>
node scripts/agent.js report --target <scope>
```

## Detection

```yaml
title: Identity Sprawl Detection
id: 56b5d7c8-82d1-4cfa-93c5-6f3c52fe9ce5
status: experimental
description: Detects suspicious activity related to detecting identity sprawl techniques in identity security context
logsource:
  category: authentication
  product: windows
detection:
  selection:
    EventType: authentication
    Status: failure
  condition: selection
level: high
tags:
  - attack.t1078
  - attack.credential_access
falsepositives:
  - Service account authentication during scheduled batch processing
```

## Verification

| Check | Method |
|---|---|
| Sources inventoried | All identity providers cataloged |
| Orphans detected | Terminated employee accounts identified |
| Dormant flagged | Accounts with 90+ days inactivity listed |
| Sprawl quantified | Identity attack surface metrics calculated |
| Remediation started | Orphaned and dormant accounts disabled |

## References

- [CIS Control 5 — Account Management](https://www.cisecurity.org/controls)
- [NIST SP 800-53 AC-2](https://csrc.nist.gov/)
- [Azure AD Access Reviews](https://learn.microsoft.com/en-us/entra/id-governance/access-reviews-overview)
- [Gartner — ITDR](https://www.gartner.com/)
