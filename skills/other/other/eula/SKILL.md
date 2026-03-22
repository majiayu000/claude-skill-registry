---
name: eula
description: Drafts enforceable End-User License Agreements for software licensors across desktop, mobile, SaaS, and cloud models. Covers click-wrap formation, IP ownership, liability limitations, data privacy compliance (GDPR/CCPA/COPPA), and export controls. Use when drafting software license agreements, app store terms, SaaS subscription agreements, or trial/freemium license terms.
---

# End-User License Agreement (EULA)

Drafts an enforceable EULA protecting licensor IP, limiting liability, and satisfying consumer protection standards across jurisdictions.

## Intake Checklist

Gather before drafting:

1. **Software** — product name, version, deployment model (desktop / mobile / SaaS / cloud / embedded)
2. **License model** — perpetual, subscription, usage-based, freemium, or trial
3. **User population** — B2C, B2B, or mixed; users under 13 (COPPA trigger)
4. **Geography** — US-only, EU, or global (drives GDPR, CCPA applicability)
5. **Data collected** — personal data categories; PHI (HIPAA), financial (GLBA), student (FERPA), payment (PCI-DSS)
6. **Third-party components** — open-source (copyleft vs. permissive) or proprietary
7. **App store** — Apple App Store, Google Play, or direct distribution
8. **Risk posture** — arbitration/class-action waiver? IP indemnification? Benchmark restrictions?

## Drafting Workflow

### 1. Header & Acceptance

- Title: "END-USER LICENSE AGREEMENT" prominently displayed
- Specify triggering act: install / account creation / first use
- Click-wrap required: scrollable full text, accept button active only after scroll opportunity (*ProCD v. Zeidenberg*; avoid browse-wrap per *Specht v. Netscape*)
- Mobile: present in app-store listing + first launch; must not contradict platform terms
- Version date + 30-day advance notice for material amendments; affirmative re-acceptance for paid-tier changes reducing rights

### 2. Definitions

| Term | Scope |
|---|---|
| Software | Product name, version, included modules |
| Updates | Bug fixes / security patches (included) |
| Upgrades | Major versions (may require separate fee) |
| Authorized Users | Named / concurrent / site license scope |
| Documentation | Manuals, API docs, specs |
| Confidential Information | Source code, algorithms, benchmarks, designated materials |

### 3. License Grant

- Non-exclusive, non-transferable, revocable for breach, [perpetual / subscription-term]
- Specify device count or concurrent user cap
- Permitted use: internal business / personal; per Documentation
- One archival backup copy; proprietary notices intact
- SaaS: frame as access right, not installation right
- Trial: evaluation-only, non-production, time-limited with end date; auto-terminates at expiry

### 4. Restrictions

| Category | Prohibited Conduct |
|---|---|
| Reverse engineering | Decompile, disassemble, derive source — except as required by law for interoperability (EU Directive 2009/24/EC) |
| Derivative works | Modify, translate, adapt, or create based on Software |
| Distribution | Sublicense, rent, lease, lend, transfer, service-bureau use |
| Circumvention | Bypass license enforcement, DRM, or security features (17 U.S.C. § 1201 [VERIFY]) |
| Notices | Remove/alter copyright, trademark, or proprietary legends |
| Competitive use | Benchmark for competitive analysis; publish results without consent |
| Safety-critical | Aircraft nav, nuclear, life support, weapons |
| Export | Export/re-export violating EAR, ITAR, or OFAC sanctions |

### 5. IP Ownership

- Licensor retains all rights — copyright, patents, trademarks, trade secrets
- **License, not a sale**; first-sale doctrine inapplicable
- User data: user owns; licensor gets limited processing license for service delivery
- Aggregated/anonymized data: licensor owns derived insights
- Feedback: user assigns all rights; moral rights waived to extent permitted
- Third-party components: designated as intended third-party beneficiaries; confirm no GPL copyleft contamination
- Trademarks: no right to use licensor marks except to identify Software

### 6. Payment & Renewals

- State fees in specific currency (not by reference to pricing page)
- Auto-renewal: conspicuous pre-purchase disclosure per Cal. Bus. & Prof. Code § 17600 et seq. [VERIFY]; easy cancellation; advance renewal reminder
- Non-payment: notice + 5–10 day cure → suspension; 10–15 day cure → termination
- Refunds: state terms explicitly; app-store refunds per platform policy
- Taxes: exclusive of taxes; user bears sales/use/VAT; EU VAT reverse charge for B2B

### 7. Term & Termination

- **For cause**: immediate upon material breach (IP violation, non-payment, export violation, insolvency)
- **Without cause**: free licenses — 30 days notice; paid perpetual — generally not permitted
- **User termination**: cancel per stated procedure; cease use; destroy all copies
- **Post-termination**: uninstall all devices; destroy copies (including backup/cached); written certification on request; SaaS — 30-day data export window then deletion
- **Survival**: IP ownership, restrictions, confidentiality (3–5 years / indefinite for trade secrets), disclaimers, liability caps, indemnification, dispute resolution

### 8. Warranty Disclaimer

> **MUST BE ALL-CAPS OR BOLD (conspicuousness requirement)**

- Limited warranty (if offered): Software substantially conforms to Documentation for [30/60/90] days; excludes modified software, misuse, unauthorized combinations
- Exclusive remedy: patch → replacement → pro-rata refund + termination
- **Disclaimer**: SOFTWARE PROVIDED "AS IS" AND "AS AVAILABLE." LICENSOR DISCLAIMS ALL WARRANTIES — EXPRESS, IMPLIED, STATUTORY — INCLUDING MERCHANTABILITY, FITNESS FOR PARTICULAR PURPOSE, NON-INFRINGEMENT, TITLE, QUIET ENJOYMENT, ACCURACY. NO WARRANTY OF UNINTERRUPTED OR ERROR-FREE OPERATION.
- Savings clause for jurisdictions prohibiting full warranty exclusions
- Magnuson-Moss Warranty Act compliance for consumer products [VERIFY applicability]

### 9. Limitation of Liability

> **MUST BE ALL-CAPS OR BOLD**

- **Consequential damages exclusion**: NO LIABILITY FOR INDIRECT, INCIDENTAL, CONSEQUENTIAL, SPECIAL, EXEMPLARY, OR PUNITIVE DAMAGES INCLUDING LOST PROFITS, LOST DATA, BUSINESS INTERRUPTION, REGARDLESS OF CAUSE OR FORESEEABILITY.
- **Aggregate cap**: fees paid in prior 12 months; free software — $[50–100] or max permitted by law
- Cap is collective across all claims; does not reset per claim
- **Carve-outs** (narrow): gross negligence / willful misconduct; death/personal injury; fraud; mandatory statutory rights
- Claims must be brought within 1 year of accrual
- Savings clause for jurisdictions limiting damage exclusions

### 10. Indemnification

**Licensor → User (IP, if offered):**
- Defend/indemnify for claims that unmodified Software infringes registered patents, copyrights, or trademarks
- Conditions: prompt notice (≤10 days); licensor controls defense; user cooperates
- Exclusions: user modifications; unauthorized combinations; non-current version; out-of-scope use
- Remedies: procure license → modify → replace → pro-rata refund + terminate (exclusive remedy)

**User → Licensor:**
- Defend/indemnify for: breach of agreement; law/third-party rights violations; user content/data; user negligence/misconduct
- Not subject to aggregate liability cap

### 11. Governing Law & Disputes

- [State] internal law; exclude conflict-of-law principles and CISG
- Exclusive jurisdiction: [County, State] state and federal courts
- **Arbitration** (if included): AAA Commercial Rules; [city]; 1 arbitrator (<$100K) / 3 (≥$100K); licensor pays costs for consumer claims
- **Class action waiver**: individual capacity only [enforceability limited in CA consumer contexts — confirm]
- Carve-out: equitable/injunctive relief for IP or confidentiality violations
- Consumer savings clause: unenforceable forum selection defaults to user's jurisdiction

### 12. Data Protection

**Include provisions for each applicable regime:**

| Regime | Trigger | Key Obligations |
|---|---|---|
| GDPR | EU/EEA users | Lawful basis, data subject rights, 72-hr breach notice, SCCs, DPO if required |
| CCPA/CPRA | CA users | Category disclosure, opt-out of sale/sharing, deletion/correction rights |
| COPPA | Users under 13 | Verifiable parental consent before collection |
| HIPAA | PHI for covered entities | BAA required; Privacy & Security Rule compliance |
| GLBA | Financial data | Safeguards Rule compliance |
| FERPA | Student records | Institutional consent; no unauthorized disclosure |

- Disclose: data collected, purpose, retention, third-party sharing, security measures
- No absolute security guarantees; user responsible for credential security
- If software not designed for sensitive data: explicit prohibition + liability disclaimer

### 13. Export Controls

- Software subject to EAR (15 C.F.R. Parts 730–774 [VERIFY]); ITAR if defense application
- User represents: not in embargoed country (Cuba, Iran, North Korea, Syria, Crimea/Donetsk/Luhansk — verify current OFAC/BIS lists); not on SDN, Denied Persons, or Entity List
- No export/re-export without required licenses
- Violation = material breach → immediate termination; user indemnifies

### 14. General Provisions

| Provision | Key Points |
|---|---|
| Entire Agreement | Supersedes all prior; no extra-contractual reliance |
| Amendment | Post + 30-day notice; material paid-license changes require re-acceptance |
| Severability | Reform to minimum extent; per-jurisdiction independence |
| Waiver | Written and signed; no implied waiver |
| Assignment | User cannot assign; licensor assigns freely (including M&A) |
| Force Majeure | Acts of God, war, pandemic, infrastructure failure; termination right if >60–90 days |
| No Partnership | Independent contractors; no agency/JV/franchise |
| Third-Party Beneficiaries | None except third-party component licensors (IP) |
| Notices | Email (confirmed) or certified mail; in-software posting for general notices |
| Counterparts | Electronic signatures valid |

## Pitfalls & Checks

- **Conspicuousness**: warranty disclaimers and liability caps MUST be ALL CAPS or bold — never buried in body text
- **Click-wrap over browse-wrap**: require affirmative acceptance; no pre-checked boxes
- **EU consumer contracts**: Unfair Contract Terms Directive prohibits significant-imbalance provisions; user's habitual-residence law applies (Rome I) — disclaim only what is permissible
- **Class action waiver**: may be unenforceable in CA consumer contexts — confirm before including
- **Open-source audit**: confirm no GPL/AGPL copyleft that would require disclosing proprietary code
- **App store overlay**: Apple/Google impose payment, refund, and content terms — EULA must complement, not contradict
- **Do not include**: specific hypothetical damages amounts; representations about unlicensed third-party products; absolute security guarantees
