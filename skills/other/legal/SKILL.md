---
name: legal
description: Legal workflows — contract review, compliance checks, NDA triage, risk assessment, legal briefs. Use when reviewing contracts, checking compliance, triaging NDAs, assessing legal risk, or drafting legal documents. Not legal advice — analysis support for qualified professionals.
routing:
  triggers:
    - "legal"
    - "contract review"
    - "compliance check"
    - "NDA"
    - "legal risk"
    - "legal brief"
    - "vendor check"
    - "german compliance"
    - "DSGVO"
    - "GoBD"
    - "TDDDG"
    - "AI Act compliance"
    - "eIDAS"
  category: business
  force_route: false
  pairs_with: []
user-invocable: true
---

# Legal Workflows

Analysis support for in-house legal teams. Contract review, compliance checks, NDA triage, risk assessment, legal writing, and response generation.

**Disclaimer**: Analysis support, not legal advice. Review by qualified counsel required.

---

## Mode Detection

Classify the request into one mode before proceeding. If the request spans modes, choose the primary and note the secondary.

| Mode | Signal Phrases | Core Output |
|------|---------------|-------------|
| **CONTRACT** | review contract, clause analysis, redline, playbook, negotiate | Clause-by-clause analysis with GREEN/YELLOW/RED flags and redline suggestions |
| **COMPLIANCE** | compliance check, GDPR, HIPAA, CCPA, SOX, regulation, data protection, DSGVO, GoBD, TDDDG, eIDAS, AI Act, NIS2, KRITIS, Grundschutz, TISAX, DORA | Applicable regulations, requirements checklist, risk areas, approvals needed |
| **NDA** | NDA, triage NDA, non-disclosure, confidentiality agreement | GREEN/YELLOW/RED classification with screening checklist |
| **RISK** | legal risk, risk assessment, exposure, severity, escalation | Severity x Likelihood matrix score with escalation path |
| **WRITING** | legal brief, memo, legal response, draft response, template | Structured legal document in appropriate format |
| **VENDOR** | vendor check, vendor status, agreement status, what's signed | Agreement inventory, gap analysis, upcoming deadlines |

---

## Reference Loading Table

Load only the references required by the detected mode.

| Mode | References to Load |
|------|-------------------|
| CONTRACT | `references/contract-review.md` |
| COMPLIANCE | `references/compliance-frameworks.md`, `references/german-business-compliance.md` |
| NDA | `references/nda-triage.md` |
| RISK | `references/risk-assessment.md` |
| WRITING | `references/legal-writing.md` |
| VENDOR | `references/contract-review.md` (for gap analysis context) |

Always load `references/llm-legal-failure-modes.md` for every mode. LLM failure awareness is non-negotiable in legal work.

---

## Mode: CONTRACT

**Framework**: INTAKE -> ANALYZE -> FLAG -> REDLINE -> STRATEGIZE

**Phase 1: INTAKE** -- Accept the contract and gather context.

- Accept contract as file, pasted text, or URL reference
- Determine: which side the user is on (vendor/customer/licensor/licensee/partner), deadline, focus areas, deal context (size, strategic importance, existing relationship)
- If user provides partial context, proceed and note assumptions

**Phase 2: ANALYZE** -- Clause-by-clause review.

Load `references/contract-review.md` for the full clause analysis methodology.

1. Identify contract type (SaaS, services, license, procurement, partnership)
2. Read entire contract before flagging -- clauses interact (uncapped indemnity may be mitigated by broad LOL)
3. Analyze each material clause against playbook or market-standard positions
4. Cover at minimum: LOL, indemnification, IP, data protection, confidentiality, reps/warranties, term/termination, governing law, insurance, assignment, force majeure, payment

**Gate**: Every material clause analyzed. No clause reviewed in isolation.

**Phase 3: FLAG** -- Classify deviations.

| Flag | Meaning | Action |
|------|---------|--------|
| **GREEN** | At or better than standard. Minor commercially reasonable variation. | Note for awareness. No negotiation. |
| **YELLOW** | Outside standard but within negotiable range. Common in market. | Generate redline + fallback + business impact. |
| **RED** | Outside acceptable range. Material risk. Escalation trigger. | Explain risk. Provide market-standard alternative. Recommend escalation. |

**Phase 4: REDLINE** -- Generate specific alternative language for YELLOW and RED items.

Each redline includes: current language (exact quote), proposed language, rationale (suitable for counterparty), priority (must-have / should-have / nice-to-have), fallback position.

**Phase 5: STRATEGIZE** -- Negotiation strategy.

- Tier 1 (deal breakers): uncapped liability, missing DPA for regulated data, IP jeopardizing core assets, regulatory conflicts
- Tier 2 (strong preferences): LOL adjustments, indemnification scope, termination flexibility, audit rights
- Tier 3 (concession candidates): preferred governing law, notice periods, minor definitions, insurance certificates

Lead with Tier 1. Trade Tier 3 to secure Tier 2. Escalate before making any Tier 1 concession.

**Gate**: Top 3 issues identified. Negotiation priority established. Concession candidates named.

**Output format**:
```
## Contract Review Summary
**Document**: [name] | **Parties**: [names] | **Side**: [role] | **Basis**: [Playbook/Generic]

## Key Findings
[Top 3-5 issues with severity flags]

## Clause-by-Clause Analysis
### [Clause] -- [GREEN/YELLOW/RED]
**Contract says**: ... | **Standard**: ... | **Deviation**: ... | **Impact**: ... | **Redline**: ...

## Negotiation Strategy
[Priorities, concessions, approach]
```

---

## Mode: COMPLIANCE

**Framework**: SCOPE -> MAP -> ASSESS -> RECOMMEND

**Phase 1: SCOPE** -- Understand the proposed action.

- What is being done (feature launch, data processing, marketing campaign, new vendor)
- What data is involved (personal data categories, sensitive data, regulated data)
- Which geographies (determines applicable regulations)
- Who is affected (customers, employees, partners, public)

**Phase 2: MAP** -- Identify applicable regulations.

Load `references/compliance-frameworks.md` for regulation-specific requirements.

Map all potentially applicable frameworks. Check for overlapping or conflicting requirements across jurisdictions.

**Phase 3: ASSESS** -- Check each requirement.

| Requirement | Status | Action Needed |
|-------------|--------|---------------|
| [Requirement] | Met / Not Met / Unknown | [Specific action] |

For each risk area, assess severity and mitigation path.

**Phase 4: RECOMMEND** -- Prioritized action list with approvals needed.

**Gate**: All applicable regulations identified. Requirements checked. Approvals mapped.

**Output**: Quick assessment (Proceed / Proceed with conditions / Requires further review), applicable regulations table, requirements checklist, risk areas, recommended actions, approvals needed.

---

## Mode: NDA

**Framework**: ACCEPT -> SCREEN -> CLASSIFY -> REPORT

Load `references/nda-triage.md` for the full screening checklist and common deviations catalog.

**Phase 1: ACCEPT** -- Accept NDA in any format.

**Phase 2: SCREEN** -- Systematic evaluation against 10 screening criteria.

Agreement structure, definition scope, receiving party obligations, standard carveouts (public knowledge, prior possession, independent development, third-party receipt, legal compulsion), permitted disclosures, term/duration, return/destruction, remedies, problematic provisions (non-solicit, non-compete, exclusivity, standstill, residuals, IP assignment).

**Phase 3: CLASSIFY**

| Classification | Criteria | Routing |
|----------------|----------|---------|
| **GREEN** | All criteria pass. Standard mutual, all carveouts, reasonable term, no prohibited provisions. | Standard delegation. Same-day approval. |
| **YELLOW** | Minor deviations: broader definition, longer term, missing one carveout, narrow residuals, non-preferred jurisdiction. | Counsel review. 1-2 business days. |
| **RED** | Wrong type, missing critical carveouts, non-solicit/non-compete, perpetual term, broad residuals, hidden IP assignment, liquidated damages. | Full legal review. Do not sign. 3-5 business days. |

**Phase 4: REPORT** -- Structured triage report with specific issues, risks, and suggested fixes.

**Gate**: Every screening criterion evaluated. Classification justified.

---

## Mode: RISK

**Framework**: IDENTIFY -> SCORE -> CLASSIFY -> DOCUMENT

Load `references/risk-assessment.md` for the full severity/likelihood matrix and documentation standards.

**Phase 1: IDENTIFY** -- Define the risk clearly with background and context.

**Phase 2: SCORE** -- Apply Severity (1-5) x Likelihood (1-5) matrix.

- Severity: Negligible (1) through Critical (5), calibrated to financial exposure as % of deal/contract value
- Likelihood: Remote (1) through Almost Certain (5), calibrated to precedent and triggering events
- Risk Score = Severity x Likelihood

**Phase 3: CLASSIFY**

| Score | Level | Color | Escalation |
|-------|-------|-------|------------|
| 1-4 | Low | GREEN | Accept. Monitor quarterly. |
| 5-9 | Medium | YELLOW | Mitigate. Assign owner. Monthly review. |
| 10-15 | High | ORANGE | Senior counsel. Outside counsel if needed. Weekly review. |
| 16-25 | Critical | RED | GC/C-suite/Board. Outside counsel. Litigation hold if applicable. Daily review. |

**Phase 4: DOCUMENT** -- Risk memo with contributing factors, mitigating factors, mitigation options, recommended approach, residual risk, monitoring plan.

**Gate**: Both severity and likelihood ratings justified with specific rationale. Score calculated. Escalation path defined.

---

## Mode: WRITING

**Framework**: CLASSIFY -> DRAFT -> REVIEW

Load `references/legal-writing.md` for format templates and escalation triggers.

**Phase 1: CLASSIFY** -- Determine document type.

| Type | Use Case |
|------|----------|
| Legal memo | Internal analysis of a legal question |
| Legal brief | Summary of issue, law, and recommendation |
| Legal response | Templated response to common inquiries (DSR, litigation hold, vendor question, NDA request, subpoena) |
| Meeting brief | Pre-meeting context, talking points, action items |
| Incident brief | Rapid brief for developing situations (breach, litigation threat, regulatory inquiry) |

**Phase 2: DRAFT** -- Generate document in the appropriate format.

For legal responses: check escalation triggers before generating. If any trigger fires (regulatory inquiry, potential litigation, criminal exposure, media attention, multiple jurisdictions), stop and recommend escalation instead of a templated response.

**Phase 3: REVIEW** -- Present draft for user review. Note any assumptions, gaps, or areas needing counsel input.

**Gate**: Document type correctly identified. Escalation triggers checked. All required elements present.

---

## Mode: VENDOR

**Framework**: IDENTIFY -> INVENTORY -> GAP ANALYSIS -> REPORT

**Phase 1: IDENTIFY** -- Accept vendor name. Handle variations (legal name vs. trade name, abbreviations, parent/subsidiary).

**Phase 2: INVENTORY** -- Search for all agreements with the vendor. For each agreement found, capture: type (NDA/MSA/SOW/DPA/SLA), status (active/expired/in-negotiation), effective date, expiration date, auto-renewal details, key terms.

**Phase 3: GAP ANALYSIS** -- Identify what exists vs. what should exist.

Required agreements by relationship type:
- **Data processor**: NDA + MSA + DPA + SOW minimum
- **SaaS vendor**: NDA + MSA/SaaS Agreement + DPA (if personal data) + SLA
- **Professional services**: NDA + MSA + SOW(s)
- **Hardware/commodity**: NDA + Purchase Agreement

Flag: agreements expired but with surviving obligations, approaching expirations (90-day window), DPA gaps when vendor handles personal data.

**Phase 4: REPORT** -- Consolidated status report with gap analysis and upcoming actions.

**Gate**: All available sources checked. Gaps identified. Approaching deadlines flagged.

---

## LLM Failure Mode Awareness

Legal analysis is a high-risk domain for LLM failures. Load `references/llm-legal-failure-modes.md` and apply these guards on every mode:

| Failure Mode | Guard |
|-------------|-------|
| Fabricated case law or citations | Verify all citations with user before including. State "verify this citation" when referencing specific law. |
| Invented regulatory requirements | Distinguish between "this regulation requires X" (high confidence, well-known) and "check whether this applies in your jurisdiction" (lower confidence). |
| Jurisdiction confusion | Always ask which jurisdiction applies. Ask which jurisdiction applies. State which jurisdiction the analysis covers. |
| Overconfident analysis | Use calibrated language: "likely," "typically," "in most jurisdictions" rather than absolutes. |
| Missing clause interactions | Read entire contract before analyzing individual clauses. Clauses interact. |
| Stale legal knowledge | Training data has a cutoff. Recommend counsel verify current regulatory state, especially for recently enacted or amended laws. |

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No contract provided | User asks for review without document | Prompt for document in any format |
| Ambiguous jurisdiction | Multi-jurisdiction deal | Ask user to specify primary jurisdiction. Note differences. |
| No playbook configured | First use, no organizational standards | Proceed with market-standard positions. Note clearly. |
| Contract too long (50+ pages) | Large agreement | Offer to focus on most material sections first, then complete review |
| Conflicting regulations | Cross-border requirements clash | Flag conflicts explicitly. Do not pick a winner. Recommend counsel. |
| Template needed for unknown type | No template for the inquiry type | Help user create a template following the creation guide in references |
