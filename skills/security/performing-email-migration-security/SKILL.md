<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
<!-- CIPHER is a trademark of defconxt. -->
---
name: performing-email-migration-security
description: >-
  Secure email platform migrations including tenant-to-tenant moves,
  on-premises to cloud transitions, and cross-platform migrations.
  Covers data protection during transfer, authentication continuity,
  encryption key management, and post-migration security validation.
domain: cybersecurity
subdomain: email-security
tags:
  - migration
  - tenant-migration
  - data-protection
  - encryption
  - authentication
  - cloud-security
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1114", "T1530"]
  tools: [python3, powershell, openssl, curl]
---

# Performing Email Migration Security

## Overview

Email migrations are high-risk windows where data protection controls may
lapse, authentication chains break, and encryption keys require careful
transfer. Security assessment before, during, and after migration ensures
continuity of email authentication (SPF/DKIM/DMARC), data-in-transit
protection, retention policy preservation, and access control integrity.

## Prerequisites

| Requirement | Purpose |
|---|---|
| Admin access (source + target) | Audit configurations both sides |
| DNS management | Update MX, SPF, DKIM, DMARC records |
| Migration tool access | Validate encryption in transit |
| Compliance documentation | Map retention and legal hold requirements |

## Workflow

### Step 1: Pre-Migration Security Assessment

```python
from typing import Any

def pre_migration_checklist(source: str, target: str) -> dict[str, Any]:
    checks = {
        "spf_record_documented": False,
        "dkim_keys_exported": False,
        "dmarc_policy_recorded": False,
        "retention_policies_mapped": False,
        "legal_holds_identified": False,
        "admin_accounts_audited": False,
        "mfa_enforced_target": False,
        "encryption_at_rest_target": False,
        "conditional_access_planned": False,
        "third_party_integrations_listed": False,
    }
    return {
        "source": source,
        "target": target,
        "checklist": checks,
        "status": "incomplete",
    }
```

### Step 2: Validate Data-in-Transit Protection

```bash
# Verify TLS on source SMTP
openssl s_client -connect mail.source.com:587 -starttls smtp 2>/dev/null | \
  grep -E "(Protocol|Cipher|Server certificate)"

# Verify TLS on target SMTP
openssl s_client -connect mail.target.com:587 -starttls smtp 2>/dev/null | \
  grep -E "(Protocol|Cipher|Server certificate)"

# Check migration tool uses encrypted channel
# Verify no plaintext IMAP (port 143) — only IMAPS (993)
nmap -p 143,993,587,465 mail.source.com --script ssl-enum-ciphers
```

### Step 3: DNS Cutover Security

```bash
# Document current records BEFORE cutover
dig MX example.com +short > pre_migration_mx.txt
dig TXT example.com +short | grep "v=spf1" > pre_migration_spf.txt
dig TXT _dmarc.example.com +short > pre_migration_dmarc.txt
dig TXT selector1._domainkey.example.com +short > pre_migration_dkim.txt

# Post-cutover — verify new records propagated
dig MX example.com +short
dig TXT example.com +short | grep "v=spf1"

# Lower DMARC to monitor during transition
# v=DMARC1; p=none; rua=mailto:dmarc@example.com; pct=100
# Then progressively enforce: none -> quarantine -> reject
```

### Step 4: Post-Migration Security Validation

```powershell
# Verify MFA enforcement on target tenant
Get-MgUser -All | Where-Object { $_.StrongAuthenticationMethods.Count -eq 0 } |
  Select-Object UserPrincipalName

# Verify retention policies migrated
Get-RetentionPolicy | Select-Object Name, RetentionPolicyTagLinks

# Verify no orphaned mailbox permissions
Get-Mailbox -ResultSize Unlimited | Get-MailboxPermission |
  Where-Object { $_.User -ne "NT AUTHORITY\SELF" -and $_.IsInherited -eq $false }

# Verify conditional access policies active
Get-MgIdentityConditionalAccessPolicy | Select-Object DisplayName, State
```

## Detection Opportunities

| Signal | Source | Description |
|--------|--------|-------------|
| Auth failures spike | Sign-in logs | Expected during cutover, investigate if prolonged |
| MX record change | DNS monitoring | Verify points to authorized target |
| Unencrypted migration | Network logs | Migration traffic on non-TLS ports |

```yaml
title: Email Migration Security Detection
id: 06cc5a6e-6311-4250-86af-0ab67f287554
status: experimental
description: Detects suspicious activity related to performing email migration security techniques in email security context
logsource:
  category: email
  service: exchange
detection:
  selection:
    Subject: "*urgent*"
  condition: selection
level: medium
tags:
  - attack.t1114
  - attack.t1530
  - attack.initial_access
falsepositives:
  - Bulk email migration by authorized IT administration tools
```

## Verification

- [ ] Pre-migration DNS records documented and backed up
- [ ] TLS verified on source and target SMTP endpoints
- [ ] DKIM keys regenerated or transferred to target
- [ ] SPF updated to include target mail servers
- [ ] DMARC policy in monitor mode during transition
- [ ] MFA enforced on all target mailboxes
- [ ] Retention policies and legal holds preserved
- [ ] Post-migration authentication records enforce reject

## References

- [Microsoft — Cross-tenant mailbox migration](https://learn.microsoft.com/en-us/microsoft-365/enterprise/cross-tenant-mailbox-migration)
- [NIST SP 800-177 — Trustworthy Email](https://csrc.nist.gov/publications/detail/sp/800-177/rev-1/final)

---
v1.0 | Validated: 2026-03-18
