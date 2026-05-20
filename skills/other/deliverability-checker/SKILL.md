---
name: deliverability-checker
description: "Check email deliverability and DNS configuration. Use when: diagnosing email delivery issues; setting up new email domains; auditing email authentication; checking SPF/DKIM/DMARC; troubleshooting spam folder issues"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Email Deliverability Checker

> Diagnose email deliverability issues by checking SPF, DKIM, DMARC, and other DNS records - fix why your emails land in spam.

## When to Use This Skill

- **Delivery troubleshooting** - Emails landing in spam
- **New domain setup** - Configure email authentication
- **Migration audit** - Verify email config after domain change
- **Client onboarding** - Check client email health
- **Compliance check** - Ensure proper authentication


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures analysis frameworks | Metric definitions |
| Identifies patterns in data | Business interpretation |
| Creates visualization templates | Dashboard design |
| Suggests optimization areas | Action priorities |
| Calculates statistical measures | Decision thresholds |

## Dependencies

```bash
pip install dnspython click
```

## Commands

### Full Audit
```bash
python scripts/main.py audit example.com
python scripts/main.py audit example.com --output report.html
```

### Check SPF
```bash
python scripts/main.py spf example.com
```

### Check DKIM
```bash
python scripts/main.py dkim example.com --selector google
python scripts/main.py dkim example.com --selector default
```

### Check DMARC
```bash
python scripts/main.py dmarc example.com
```

### Check MX Records
```bash
python scripts/main.py mx example.com
```

## Examples

### Example 1: Full Email Audit
```bash
python scripts/main.py audit acme-corp.com

# Output:
# Email Deliverability Audit: acme-corp.com
# ──────────────────────────────────────────
# MX Records:      ✓ Found (Google Workspace)
# SPF:             ✓ Valid
# DKIM (google):   ✓ Valid
# DMARC:           ✗ Missing (CRITICAL)
#
# Score: 75/100
#
# Issues Found:
# 1. [CRITICAL] No DMARC record found
#    Fix: Add TXT record for _dmarc.acme-corp.com
#    Value: v=DMARC1; p=none; rua=mailto:dmarc@acme-corp.com
```

### Example 2: Diagnose SPF Issues
```bash
python scripts/main.py spf newsletter-sender.com

# Output:
# SPF Analysis: newsletter-sender.com
# ────────────────────────────────────
# Record: v=spf1 include:_spf.google.com include:sendgrid.net ~all
#
# Status: ✓ Valid
#
# Authorized Senders:
# - Google Workspace (include:_spf.google.com)
# - SendGrid (include:sendgrid.net)
#
# Policy: ~all (soft fail)
# Warning: Consider changing to -all (hard fail) for better security
```

## Email Authentication Records

| Record | Purpose | Location |
|--------|---------|----------|
| **SPF** | Authorize sending servers | `TXT` on root domain |
| **DKIM** | Cryptographic signature | `TXT` on `selector._domainkey` |
| **DMARC** | Policy and reporting | `TXT` on `_dmarc` subdomain |
| **MX** | Mail delivery servers | `MX` on root domain |

## Common SPF Includes

| Provider | SPF Include |
|----------|-------------|
| Google Workspace | `include:_spf.google.com` |
| Microsoft 365 | `include:spf.protection.outlook.com` |
| SendGrid | `include:sendgrid.net` |
| Mailchimp | `include:servers.mcsv.net` |
| Amazon SES | `include:amazonses.com` |

## DKIM Selectors by Provider

| Provider | Common Selector |
|----------|-----------------|
| Google Workspace | `google` |
| Microsoft 365 | `selector1`, `selector2` |
| SendGrid | `s1`, `s2` |
| Mailchimp | `k1` |

## Deliverability Score Factors

| Factor | Weight | Impact |
|--------|--------|--------|
| Valid MX | 20% | Can't receive replies |
| Valid SPF | 25% | Server authorization |
| Valid DKIM | 25% | Message integrity |
| Valid DMARC | 30% | Policy enforcement |

## Skill Boundaries

### What This Skill Does Well
- Structuring data analysis
- Identifying patterns and trends
- Creating visualization frameworks
- Calculating statistical measures

### What This Skill Cannot Do
- Access your actual data
- Replace statistical expertise
- Make business decisions
- Guarantee prediction accuracy

## Related Skills

- [dns-audit](../dns-audit/) - Full DNS health check

## Skill Metadata


- **Mode**: centaur
```yaml
category: email-tools
subcategory: deliverability
dependencies: [dnspython]
difficulty: beginner
time_saved: 2+ hours/week
```
