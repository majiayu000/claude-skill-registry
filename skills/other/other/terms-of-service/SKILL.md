---
name: terms-of-service
description: Drafts enforceable U.S. Terms of Service agreements for websites, apps, platforms, and SaaS with acceptance mechanics, liability limits, dispute resolution, IP/content rules, and privacy hooks. Use when asked to draft "terms of service", "terms of use", "TOS", "user agreement", "platform terms", "website terms", "app terms", or "SaaS terms".
---

# Terms of Service Agreement

Drafts an enforceable TOS tailored to the service model, data flows, and jurisdictional compliance needs.

## Quick Start

Gather before drafting:

| Item | Required | Notes |
|---|---|---|
| Company legal name, address, contact email | Yes | Contracting entity |
| Service name and URL/app identifiers | Yes | Defines "Service" |
| Eligibility/age minimum | Yes | COPPA if under 13 [VERIFY] |
| Countries/states served | Yes | Triggers GDPR/CCPA/other |
| Payment terms | If paid | Auto-renew, cancellation, refunds |
| IP assets | Yes | Trademarks, content ownership |
| UGC + moderation approach | If UGC | DMCA workflow |
| APIs/integrations | If any | Third-party terms |

## Core Workflow

### 1. Clause Selection

| Clause | Include When | Key Points |
|---|---|---|
| Acceptance mechanism | Always | Clickwrap preferred; continued-use fallback |
| Accounts & security | Accounts exist | Credentials, MFA, responsibility |
| Acceptable use | Always | Prohibited conduct list |
| UGC license | UGC exists | Scope, duration, takedown |
| IP ownership | Always | Service IP, limited license |
| Payments | Paid tiers | Billing, taxes, refunds |
| Termination | Always | For cause/at will, effects |
| Disclaimers | Always | AS IS / AS AVAILABLE |
| Liability cap | Always | Cap amount, exclusions, carve-outs |
| Indemnity | B2B or UGC | IP claims, violations |
| Dispute resolution | Always | Governing law, venue/arbitration |

### 2. Drafting Sequence

1. **Definitions & acceptance** — clickwrap + versioning/effective date
2. **Eligibility & authority** — age, entity authority
3. **Account rules** — registration, security, accuracy
4. **Acceptable use** — law compliance + prohibited conduct
5. **UGC & IP** — ownership, license grant, feedback assignment
6. **Third-party services** — links, integrations, no endorsement
7. **Payment terms** — if applicable
8. **Termination & suspension** — rights, effect, survival
9. **Disclaimers & limitation of liability**
10. **Indemnification** — if applicable
11. **Dispute resolution** — law, venue, arbitration
12. **Boilerplate** — severability, assignment, notices

### 3. Prohibited Conduct (always include)

- Illegal activity, fraud, misrepresentation
- Malware, phishing, security bypass
- Unauthorized access, scraping, rate-limit evasion
- IP infringement or circumvention of protections
- Harassment, hate, abusive conduct
- Interference with service availability

### 4. Dispute Resolution Selection

| Option | Use When | Notes |
|---|---|---|
| Arbitration + class waiver | B2B or low-risk consumer | Include small-claims carve-out |
| Court litigation | High consumer scrutiny | Specify venue + jury waiver |
| EU consumer carve-out | Serving EU | Mandatory local rights preserved |

## Templates

### UGC License (edit scope as needed)

` ` `
User Content License. You retain ownership of Your Content. You grant Company a worldwide, non-exclusive, royalty-free, sublicensable, transferable license to host, store, use, display, reproduce, modify for technical purposes, distribute, and create derivative works of Your Content solely to operate, improve, and promote the Service. License ends upon deletion except for content already shared or cached in ordinary operation.
` ` `

### Liability & Warranty (edit cap as needed)

` ` `
Disclaimer. THE SERVICE IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING MERCHANTABILITY, FITNESS, AND NON-INFRINGEMENT, TO THE MAXIMUM EXTENT PERMITTED BY LAW.

Limitation. TO THE MAXIMUM EXTENT PERMITTED BY LAW, COMPANY SHALL NOT BE LIABLE FOR INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, OR LOSS OF DATA, PROFITS, OR REVENUE. TOTAL LIABILITY SHALL NOT EXCEED THE AMOUNTS PAID BY YOU TO COMPANY IN THE 12 MONTHS BEFORE THE CLAIM (OR $100 IF NONE). EXCEPTIONS: LIABILITY FOR DEATH/PERSONAL INJURY, FRAUD, OR WILLFUL MISCONDUCT WHERE PROHIBITED.
` ` `

## Privacy & Data Hooks

- Incorporate Privacy Policy by reference
- Specify data processing roles (controller/processor)
- Reference security measures at high level only — do not promise beyond actual controls
- Address cross-border transfers if applicable (EU SCCs [VERIFY])

## Final QC Checklist

- [ ] Definitions consistent, capitalization standardized
- [ ] Effective date + version history included
- [ ] Notice method and update mechanism defined
- [ ] Survival clauses listed
- [ ] Hyperlinks to all incorporated policies working

## Pitfalls

- **Browsewrap is weak** — prefer clickwrap acceptance; browsewrap risks unenforceability.
- **EU/UK users** — include GDPR-consistent rights hooks and consumer protections; avoid overbroad waivers. [VERIFY]
- **California residents** — include CCPA/CPRA notice hooks and no-sale/share language. [VERIFY]
- **UGC services** — must include DMCA agent designation and takedown procedure. [VERIFY]
- **Unconscionability risk** — keep liability caps and waivers reasonable for consumer users.
- **Regulated industries** (health, finance, telecom) — flag for additional statutory modules.
