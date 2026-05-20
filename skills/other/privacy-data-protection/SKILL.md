---
name: privacy-data-protection
description: |
    Use when identifying data privacy and protection laws that apply to your software product. Covers GDPR, CCPA/CPRA, LGPD, PIPL, PIPA, DPDPA, PIPEDA, and other global privacy regulations with jurisdiction mapping, key obligations, and compliance triggers.
    USE FOR: GDPR, CCPA, CPRA, LGPD, PIPL, PIPA, DPDPA, PIPEDA, UK GDPR, data privacy compliance, data subject rights, consent management, cross-border data transfers, DPO requirements, breach notification
    DO NOT USE FOR: encryption implementation (use security/cryptography), data masking techniques (use security/data-protection), specific DPA drafting (consult legal counsel)
license: MIT
metadata:
  displayName: "Privacy & Data Protection"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "GDPR Official Text"
    url: "https://gdpr-info.eu"
  - title: "California Consumer Privacy Act (CCPA) Official Text"
    url: "https://oag.ca.gov/privacy/ccpa"
  - title: "GDPR Full Regulation Text (EUR-Lex)"
    url: "https://eur-lex.europa.eu/eli/reg/2016/679/oj"
---

# Privacy & Data Protection

> **Disclaimer**: This skill provides general educational information about legal topics relevant to software development. It is **not legal advice**. Laws vary by jurisdiction and change frequently. Always consult a qualified attorney licensed in the relevant jurisdiction before making legal decisions for your organization.

## Overview

Data privacy is the most universally applicable legal domain for software companies. Nearly every country has enacted or is developing data protection legislation. The obligations these laws impose -- from obtaining lawful consent to enabling data subject rights to reporting breaches within tight deadlines -- have profound implications for software architecture, product design, and business operations. Understanding which laws apply and what they require is the essential first step toward compliance.

## Global Privacy Law Comparison

| Law | Jurisdiction | Effective | Scope | Key Rights | Penalties |
|---|---|---|---|---|---|
| **GDPR** | EU | 2018 | Any company processing EU residents' data | Access, erasure, portability, objection | Up to 4% global annual revenue or EUR 20M |
| **CCPA / CPRA** | California, US | 2020 / 2023 | Businesses meeting revenue or data volume thresholds | Know, delete, opt-out of sale, correct | Up to $7,500 per intentional violation |
| **UK GDPR** | UK | 2021 | Same as GDPR, post-Brexit | Mirrors GDPR rights | GBP 17.5M or 4% global annual revenue |
| **LGPD** | Brazil | 2020 | Similar to GDPR in scope | Access, correction, deletion, portability | Up to 2% of revenue, capped at BRL 50M |
| **PIPL** | China | 2021 | Processing Chinese residents' data | Access, correction, deletion, portability | Up to 5% of annual revenue |
| **PIPA** | South Korea | 2011 (amended 2023) | Broad scope covering personal information | Access, correction, deletion | Up to 3% of revenue |
| **DPDPA** | India | 2023 | Processing Indian residents' data | Access, correction, erasure, nomination | Up to INR 250 crore (approx. USD 30M) |
| **PIPEDA / Bill C-27** | Canada | 2000 / pending | Commercial activity involving personal information | Access, correction | Up to CAD 100K per violation under PIPEDA |
| **APPI** | Japan | 2022 (amended) | Handling personal information of individuals in Japan | Access, correction, deletion | Up to JPY 100M for organizations |
| **Privacy Act** | Australia | 1988 (amended) | Organizations meeting size or activity thresholds | Access, correction | Civil penalties up to AUD 50M |

## Universal Obligations

Most privacy laws share a common set of core obligations. While specific requirements differ, preparing for these areas will provide a strong compliance foundation across jurisdictions:

- **Lawful basis for processing** — You must have a recognized legal basis (consent, contract, legitimate interest, legal obligation, etc.) before collecting or processing personal data.
- **Consent management** — Where consent is the lawful basis, it must be freely given, specific, informed, and unambiguous. Mechanisms to obtain, record, and withdraw consent are essential.
- **Data subject rights** — Individuals have the right to access, correct, delete, and (in many laws) port their data. Your systems must be able to respond to these requests within legally mandated timeframes.
- **Breach notification** — Most laws require notification to regulators and affected individuals within strict timelines (e.g., 72 hours under GDPR).
- **Cross-border data transfer restrictions** — Transferring personal data across national borders often requires specific legal mechanisms (see below).
- **Records of processing** — Organizations must maintain documented records of what data they process, why, and how.
- **Data Protection Officer (DPO) or privacy officer** — Many laws require or recommend appointing a dedicated privacy officer, particularly for large-scale or sensitive data processing.
- **Privacy impact assessments** — High-risk processing activities require a formal assessment of privacy risks and mitigations before the processing begins.

## Cross-Border Data Transfers

Moving personal data across national borders is one of the most complex areas of privacy compliance. The following mechanisms are commonly used:

| Mechanism | Used By | Description |
|---|---|---|
| **Adequacy decisions** | EU | The European Commission determines that a non-EU country provides an adequate level of data protection, allowing free data flow. |
| **Standard Contractual Clauses (SCCs)** | EU | Pre-approved contract templates that impose GDPR-equivalent obligations on the data importer in a non-adequate country. |
| **Binding Corporate Rules (BCRs)** | EU | Internally binding data protection policies approved by EU regulators for intra-group international transfers. |
| **Data Privacy Framework (DPF)** | US-EU | A self-certification framework allowing US companies to receive EU personal data, replacing the invalidated Privacy Shield. |
| **APEC Cross-Border Privacy Rules (CBPR)** | Asia-Pacific | A voluntary certification system enabling data transfers among participating APEC economies. |

## Compliance Triggers

Understanding when privacy laws apply to your organization is critical. The following triggers commonly bring software companies into scope:

| Trigger | Example |
|---|---|
| **Collecting personal data from users** | Sign-up forms, analytics tracking, cookies, device identifiers |
| **Processing data of residents in a regulated jurisdiction** | An app available in the EU app store collects user data, regardless of where the company is based |
| **Meeting revenue or data volume thresholds** | CCPA applies to businesses with > $25M annual revenue or processing data of > 100K consumers |
| **Processing sensitive or special category data** | Health data, biometric data, racial/ethnic origin, political opinions, sexual orientation |
| **Sharing or selling personal data to third parties** | Ad tech integrations, data broker partnerships, analytics providers |
| **Automated decision-making or profiling** | Credit scoring, content recommendation, hiring algorithms |
| **Processing children's data** | Apps or services directed at or knowingly used by minors (COPPA, GDPR Art. 8, Age Appropriate Design Code) |
| **Operating in a regulated industry** | Healthcare (HIPAA), finance (GLBA), education (FERPA) add sector-specific obligations on top of general privacy laws |

## Best Practices

- **Always consult qualified privacy counsel.** This overview identifies applicable laws and common obligations, but a licensed attorney can interpret how they apply to your specific product, data flows, and jurisdictions.
- **Conduct a data mapping exercise.** Before you can comply, you must understand what personal data you collect, where it flows, where it is stored, and who has access. Data mapping is the foundation of every privacy program.
- **Implement privacy by design and by default.** Minimize data collection, pseudonymize where possible, enforce purpose limitation, and set privacy-protective defaults for all users.
- **Build data subject rights into your architecture.** Design your systems so that you can efficiently respond to access, deletion, correction, and portability requests within legally mandated timeframes.
- **Establish a breach response plan.** Document who is responsible for what, how breaches are assessed, and how notifications are sent. Practice with tabletop exercises so the team is prepared.
- **Use lawful transfer mechanisms for cross-border data flows.** Identify every international data transfer and ensure each one is covered by an appropriate legal mechanism (SCCs, adequacy, BCRs, etc.).
- **Keep consent records and processing logs.** Regulators expect you to demonstrate compliance, not just assert it. Maintain auditable records of consent, processing activities, and privacy impact assessments.
- **Review and update your privacy program regularly.** Privacy laws evolve rapidly. Schedule periodic reviews of your data practices, privacy notices, and compliance posture to keep pace with legal changes.
