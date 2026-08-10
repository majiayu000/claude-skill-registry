---
name: proposal-generation
description: Create tailored sales proposals and RFP responses that address prospect needs, articulate solution value, and include pricing, timelines, and social proof. Use when the user requests proposal generation or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: community
  version: "1.0"
---

# Sales Proposal Generation

Generate compelling, customized sales proposals and RFP responses from prospect requirements. This skill analyzes buyer needs, maps your solution to their pain points, structures executive summaries, pricing tables, implementation timelines, and weaves in relevant case studies to maximize win rates.

## Workflow

1. **Analyze Requirements or RFP** — Parse the prospect's RFP document, requirements list, or briefing notes to extract mandatory criteria, evaluation weightings, submission formatting rules, and any compliance requirements. Categorize items as must-have vs. nice-to-have and flag disqualification risks early.

2. **Research the Prospect** — Gather firmographic data (revenue, headcount, industry vertical), recent news, strategic initiatives, and known technology stack. Identify the decision-making unit — economic buyer, champion, technical evaluator — and tailor messaging to each stakeholder's priorities.

3. **Draft the Executive Summary** — Write a concise summary (250–400 words) that mirrors the prospect's language, restates their core challenge, positions your solution as the best fit, and previews quantified business outcomes. This section sells the rest of the proposal.

4. **Detail Solution and Pricing** — Map each requirement to a specific product capability or service offering. Build a pricing table with line items, optional tiers, and volume discounts. Include an implementation timeline with milestones, dependencies, and resource assumptions.

5. **Add Case Studies and Social Proof** — Select 2–3 case studies from similar industries or company sizes. For each, include the customer's challenge, the solution deployed, and measurable results (revenue lift, cost savings, time-to-value). Append relevant logos, testimonials, or analyst quotes.

6. **Format and Finalize the Deliverable** — Assemble the proposal into the required format (PDF, DOCX, slide deck). Apply brand guidelines, insert a table of contents, add appendices for technical specs or SLAs, and run a compliance checklist to ensure every RFP question is answered.

## Usage

Provide the prospect's requirements or RFP text, your company's solution details, and any relevant case studies. Optionally specify the output format and tone.

**Example prompt:**
> Generate a sales proposal for Acme Corp, a 500-person logistics company evaluating our warehouse management SaaS. Their RFP requires cloud deployment, real-time inventory tracking, and ERP integration. Budget range is $80K–$120K/year. Include executive summary, solution mapping, pricing, timeline, and at least two case studies.

## Examples

### Example 1: SaaS Implementation Proposal

**Input:** Proposal for Acme Corp (logistics, 500 employees, $80K–$120K budget) evaluating warehouse management SaaS.

**Output:**

**Executive Summary**

Acme Corp's rapid expansion across three distribution centers has exposed visibility gaps in inventory accuracy and order fulfillment speed. Our Warehouse Management Platform delivers real-time inventory tracking, automated replenishment triggers, and native ERP integration — enabling logistics teams to reduce stockouts by 34% and cut fulfillment cycle time by 22%, based on results from comparable deployments. This proposal outlines a phased rollout that meets Acme's cloud-first mandate and delivers measurable ROI within 90 days of go-live.

**Solution Overview**

| Requirement | Capability | Details |
|---|---|---|
| Cloud deployment | Multi-tenant AWS infrastructure | SOC 2 Type II certified, 99.95% uptime SLA |
| Real-time inventory | IoT sensor integration + live dashboards | Sub-second updates across all warehouse zones |
| ERP integration | Pre-built SAP and Oracle connectors | Bi-directional sync with < 5-minute latency |

**Pricing**

| Item | Annual Cost |
|---|---|
| Platform license (up to 500 users) | $72,000 |
| ERP integration module | $18,000 |
| Premium support (24/7) | $12,000 |
| **Total** | **$102,000** |

**Timeline**

- Weeks 1–2: Discovery and configuration
- Weeks 3–5: ERP integration and data migration
- Week 6: UAT and training
- Week 7: Go-live at primary DC
- Weeks 8–10: Rollout to remaining DCs

### Example 2: RFP Compliance Response

**Input:** Answer Section 4.2 of an RFP on data security and compliance for a healthcare prospect.

**Output:**

**Section 4.2 — Data Security & Compliance**

| # | Requirement | Response | Compliance |
|---|---|---|---|
| 4.2.1 | HIPAA BAA execution | We execute BAAs with all healthcare customers prior to data onboarding. | ✅ Full |
| 4.2.2 | Data encryption at rest | AES-256 encryption on all data stores, key management via AWS KMS. | ✅ Full |
| 4.2.3 | Annual penetration testing | Conducted by independent third party (NCC Group); most recent report available under NDA. | ✅ Full |
| 4.2.4 | Data residency in US | All data stored in AWS us-east-1 and us-west-2 regions. No cross-border transfer. | ✅ Full |
| 4.2.5 | Role-based access control | Granular RBAC with SSO (SAML 2.0/OIDC) and mandatory MFA for admin roles. | ✅ Full |

## Best Practices

- Mirror the prospect's terminology and priorities — don't make them translate your jargon.
- Lead every section with the business outcome, not the feature description.
- Keep pricing transparent; hidden costs erode trust faster than higher sticker prices.
- Quantify ROI with metrics from real deployments, not theoretical projections.
- Tailor case studies to the prospect's industry and company size for maximum relevance.
- Have a clear call-to-action and defined next steps at the end of every proposal.

## Edge Cases

- **Incomplete RFP requirements** — When the RFP is vague or missing sections, document assumptions explicitly and include a clarification questions appendix.
- **No matching case studies** — Use adjacent-industry examples and emphasize transferable outcomes; disclose the industry difference upfront.
- **Multi-stakeholder conflicting priorities** — Create stakeholder-specific sections (e.g., a technical appendix for IT, an ROI summary for finance) within the same proposal.
- **Strict page or word limits** — Prioritize executive summary and solution fit; move detailed specs to a separately referenced appendix.
- **Competitor-specific evaluation criteria** — When RFP criteria clearly favor a competitor's architecture, address the requirement honestly and reframe around your differentiated strengths.
