---
name: legal
description: |
    Use when identifying legal, regulatory, and compliance considerations that affect software companies operating globally. Covers data privacy, intellectual property, open-source licensing, AI regulation, accessibility, export controls, financial regulation, healthcare, cybersecurity compliance, and more.
    USE FOR: legal risk identification, regulatory compliance overview, jurisdiction mapping, legal topic discovery, risk and compliance consultation triggers, understanding which laws apply to software products
    DO NOT USE FOR: actual legal advice (consult a licensed attorney), drafting legal documents, specific legal interpretation for your situation
license: MIT
metadata:
  displayName: "Legal & Compliance"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "GDPR Official Text"
    url: "https://gdpr-info.eu"
  - title: "NIST Privacy Framework"
    url: "https://www.nist.gov/privacy-framework"
---

# Legal & Compliance

> **Disclaimer**: This skill provides general educational information about legal topics relevant to software development. It is **not legal advice**. Laws vary by jurisdiction and change frequently. Always consult a qualified attorney licensed in the relevant jurisdiction before making legal decisions for your organization.

## Overview

Software companies face an increasingly complex web of regulations that vary by jurisdiction, industry, and data type. Whether you are a startup shipping your first product or an enterprise expanding into new markets, understanding the legal landscape is essential to avoiding costly missteps. This skill tree helps developers and product teams identify which legal domains may affect their products so they can engage appropriate legal counsel early.

## Regulatory Landscape Map

```
┌─────────────────────────────────────────────────────────────┐
│                  Privacy & Data Protection                   │
├───────────────────┬───────────────────┬─────────────────────┤
│   Intellectual    │   Open Source     │    AI Regulation    │
│     Property      │    Licensing      │                     │
├───────────────────┼───────────────────┼─────────────────────┤
│  Accessibility    │  Export Controls  │     Consumer        │
│                   │                   │     Protection      │
├───────────────────┼───────────────────┼─────────────────────┤
│    Financial      │    Healthcare     │    Cybersecurity    │
│    Regulation     │                   │    Compliance       │
├───────────────────┴───────────────────┴─────────────────────┤
│  Content Moderation  │    Contracts    │    Employment      │
├──────────────────────┴────────────────┴─────────────────────┤
│  Attribution   │  Billing & Taxation  │                     │
└────────────────┴──────────────────────┴─────────────────────┘
```

## Jurisdiction Quick Reference

| Jurisdiction | Key Privacy Law | Key AI Law | Accessibility Law | Key Financial Law |
|---|---|---|---|---|
| **EU** | GDPR | EU AI Act | European Accessibility Act (EAA) | PSD2 / DORA |
| **US Federal** | Sectoral (HIPAA, COPPA, FERPA, etc.) | Executive Orders on AI | ADA / Section 508 | SOX / Dodd-Frank |
| **US California** | CCPA / CPRA | - | - | - |
| **UK** | UK GDPR | AI White Paper (principles-based) | Equality Act 2010 | FCA rules |
| **Brazil** | LGPD | - | - | Banco Central regulations |
| **China** | PIPL | AI regulations (generative AI measures) | - | PBOC regulations |
| **India** | DPDPA 2023 | - | - | RBI regulations |
| **Canada** | PIPEDA / Bill C-27 | AIDA (proposed) | ACA | - |
| **Australia** | Privacy Act 1988 | - | DDA | APRA standards |
| **Japan** | APPI | - | JIS standards | FSA regulations |
| **South Korea** | PIPA | - | - | FSC regulations |

## When to Engage Legal Counsel

The following situations should trigger a conversation with qualified legal counsel:

1. **Processing personal data in any jurisdiction** — Privacy laws apply broadly and carry significant penalties.
2. **Using or distributing open-source software** — License obligations can affect your entire codebase and business model.
3. **Deploying AI/ML models** — Rapidly evolving regulations create new obligations around transparency, bias, and accountability.
4. **Entering new geographic markets** — Each jurisdiction brings its own regulatory requirements across multiple legal domains.
5. **Handling financial or healthcare data** — Sector-specific regulations impose heightened obligations and penalties.
6. **Exporting software with encryption** — Export control regimes restrict the distribution of cryptographic technology.
7. **Publishing user-generated content** — Content moderation obligations and liability frameworks vary by jurisdiction.
8. **Drafting customer contracts or Terms of Service** — Contract terms must comply with local consumer protection and contract law.
9. **Hiring across borders** — Employment law varies dramatically and affects IP ownership, benefits, and termination rights.
10. **Receiving a legal notice or subpoena** — Timely response is critical; failure to act can result in default judgments or sanctions.
11. **Implementing prepaid credits, tokens, or virtual currency** — Stored-value and money transmission regulations may apply.
12. **Selling into new tax jurisdictions** — VAT, GST, sales tax, and e-invoicing requirements vary by country and state.

## Choosing the Right Sub-Skill

| Problem | Look In |
|---|---|
| Which data privacy laws apply to my product? | `privacy-data-protection` |
| How do I protect my software IP? | `intellectual-property` |
| Can I use this open-source library? | `open-source-licensing` |
| What rules apply to my AI/ML system? | `ai-regulation` |
| How do I make my product accessible? | `accessibility` |
| Can I sell my software in this country? | `export-controls` |
| What consumer protection rules apply? | `consumer-protection` |
| My product handles financial data | `financial-regulation` |
| My product handles health data | `healthcare` |
| What security compliance is required? | `cybersecurity-compliance` |
| How do I moderate user content? | `content-moderation` |
| What should my contracts include? | `contracts` |
| I am hiring employees or contractors | `employment-labor` |
| What attribution is required for third-party assets (OSS, fonts, media, APIs)? | `attribution` |
| How do I handle billing, taxes, VAT/GST, cloud credits, or revenue recognition? | `billing-taxation` |

## Best Practices

- **Always consult qualified legal counsel.** This skill tree helps you identify issues but does not replace professional legal advice tailored to your specific situation and jurisdiction.
- **Treat compliance as a product feature, not an afterthought.** Building legal requirements into your product roadmap from the start is far less expensive than retrofitting later.
- **Adopt privacy by design.** Minimize data collection, implement strong defaults, and build consent mechanisms into your architecture from day one.
- **Document all legal and compliance decisions.** Maintain a record of what was considered, what was decided, and why. This documentation is invaluable during audits or disputes.
- **Monitor the regulatory landscape continuously.** Laws change frequently. Subscribe to legal updates for every jurisdiction in which you operate.
- **Build cross-functional compliance teams.** Legal compliance requires collaboration between engineering, product, legal, and business teams.
- **Conduct regular compliance audits.** Periodic reviews help catch gaps before regulators or opposing counsel do.
- **Maintain an incident response plan.** Have a documented process for handling data breaches, legal notices, and regulatory inquiries so you can respond quickly and appropriately.
