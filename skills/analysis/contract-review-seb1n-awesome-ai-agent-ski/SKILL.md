---
name: contract-review
description: Analyze contracts for risks, obligations, key clauses, and generate structured risk reports with severity ratings. Use when the user requests contract review or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: community
  version: "1.0"
---

# Contract Review

Analyze legal contracts to identify parties, obligations, risk areas, and problematic clauses. This skill systematically examines contract language for liability exposure, indemnification traps, unfavorable termination terms, IP assignment overreach, and non-compete restrictions. The output is a structured risk report with severity ratings and actionable recommendations.

## Workflow

1. **Receive and Parse Contract** — Ingest the full contract text or relevant excerpts. Identify the contract type (SaaS agreement, employment, freelancer, NDA, MSA, etc.) and establish the reviewing party's perspective (which side of the agreement you represent). Extract metadata such as effective date, governing law, and term length.

2. **Identify Parties and Core Terms** — Map all named parties, their roles, and the fundamental exchange of value. Extract key commercial terms including payment structure, deliverables, service levels, and performance metrics. Note any definitions section that modifies standard legal meanings.

3. **Flag High-Risk Clauses** — Perform clause-by-clause analysis targeting liability caps (or lack thereof), indemnification scope and triggers, termination rights and cure periods, IP assignment breadth, non-compete and non-solicitation restrictions, confidentiality obligations, data handling requirements, and force majeure provisions. Assign each flagged clause a severity rating: Critical, High, Medium, or Low.

4. **Summarize Obligations** — Produce a consolidated view of what each party must do, by when, and the consequences of non-performance. Highlight asymmetric obligations where one party bears disproportionate risk or burden.

5. **Generate Risk Report** — Compile findings into a structured report with an executive summary, clause-by-clause risk table, overall risk score, and prioritized list of recommended modifications or negotiation points.

6. **Suggest Modifications** — For each Critical and High severity finding, draft alternative contract language that better balances risk. Provide brief rationale for why the modification is important and what risk it mitigates.

## Usage

Provide the contract text and specify which party you represent. Optionally indicate areas of particular concern.

**Example prompt:**
```
Review this SaaS agreement from the customer's perspective. Flag any clauses that expose us to unlimited liability or allow the vendor to change terms unilaterally. Here is the contract: [paste contract text]
```

## Examples

### Example 1: SaaS Agreement Review

**Input:** A SaaS subscription agreement where the customer is subscribing to a project management tool. The customer is a 50-person company evaluating a 2-year enterprise commitment. Review from the customer's perspective.

**Output:**

**Executive Summary:** This agreement contains 2 Critical and 3 High severity issues that should be addressed before signing. The liability cap is absent for the vendor while the customer faces unlimited exposure, the IP assignment clause claims ownership of customer-created content, and termination requires 180-day notice with no cure period for the customer. Overall risk score: 7.2/10. We recommend negotiating all Critical items and at least the indemnification clause before execution.

**Overall Risk Score:** 7.2 / 10 (High — do not sign without modifications)

| Clause | Section | Risk | Severity | Recommendation |
|--------|---------|------|----------|----------------|
| Limitation of Liability | §8.2 | Vendor liability capped at fees paid in last 3 months; no cap on customer's liability | Critical | Add mutual liability cap at 12 months of fees |
| IP Assignment | §5.1 | "All materials created using the Service become Vendor's property" | Critical | Narrow to feedback/suggestions only; customer retains IP in their content |
| Auto-Renewal | §3.4 | Auto-renews for successive 2-year terms with 180-day cancellation notice | High | Reduce to 1-year renewal with 30-day notice |
| Indemnification | §9.1 | Customer indemnifies vendor for "any and all claims" including vendor negligence | High | Limit to claims arising from customer's breach or misuse |
| Data Handling | §6.3 | Vendor may use customer data for "service improvement and analytics" without anonymization requirement | High | Require anonymization/aggregation; add DPA reference |

### Example 2: Freelancer Contract Review

**Input:** A freelance development contract from the hiring company's template. The freelancer is a mobile app developer being engaged for a 3-month iOS project. Review from the freelancer's perspective.

**Output:**

**Executive Summary:** 1 Critical and 2 High severity issues identified. The non-compete clause is overly broad and likely unenforceable in most jurisdictions, the IP assignment has a dangerous gap tied to payment, and the payment terms heavily favor the hiring company. Overall risk score: 6.8/10.

**Overall Risk Score:** 6.8 / 10 (Moderate-High — negotiate before signing)

**Red Flags:**
- **Non-Compete (§7, Critical):** Prohibits freelancer from working in "any related field" for 24 months globally. This is almost certainly unenforceable in most jurisdictions and signals aggressive posturing. **Suggested modification:** Narrow to direct competitors, 6-month duration, reasonable geographic scope.
- **IP Assignment (§4, High):** Assigns IP only upon "final payment" but doesn't define what constitutes final payment in a milestone-based project. Gap risk: disputed milestone could leave IP ownership ambiguous. **Suggested modification:** Add that IP transfers per-milestone upon each milestone payment.
- **Payment Terms (§3, High):** Net-90 payment with no late payment penalties. **Suggested modification:** Net-30 with 1.5% monthly late fee.

## Best Practices

- Always establish which party you represent before beginning analysis — risk assessment is perspective-dependent and a favorable clause for one party is a risk for the other.
- Flag the absence of standard protective clauses (liability caps, data processing addendums, SLAs) as risks, not just problematic existing language. Missing protections are often more dangerous than bad language.
- Consider governing law jurisdiction when assessing enforceability — a non-compete valid in Texas may be void in California, and UK consumer law may override B2B contract terms.
- Compare indemnification obligations for symmetry; one-sided indemnification is a common and often successful negotiation point even in take-it-or-leave-it vendor agreements.
- Note any "entire agreement" or "amendment" clauses that could override verbal promises or side agreements. Unilateral amendment rights (where the vendor can change terms by posting to a website) are a critical red flag.
- Review defined terms carefully — a broad definition of "Confidential Information" or "Work Product" can dramatically expand obligations far beyond what the operative clauses appear to require on a casual reading.

## Safety Boundaries

- Treat the output as informational drafting or issue spotting, not legal advice.
- Identify the governing jurisdiction and relevant effective date; verify changing requirements against current primary sources.
- Do not claim that language is compliant, enforceable, or complete. Flag uncertainty and recommend qualified counsel for material decisions.
- Do not file, publish, accept, sign, or send legal terms without the user reviewing and explicitly authorizing that action.

## Edge Cases

- **Contracts referencing external documents** — Terms may incorporate SOWs, SLAs, acceptable use policies, or privacy policies by reference. Flag these as requiring separate review and note that the referenced documents may change unilaterally if the contract doesn't freeze a specific version.
- **Multi-jurisdictional agreements** — When parties are in different countries, flag potential conflicts between governing law, data residency requirements, and local employment/contractor laws. EU consumer protection regulations may render certain limitation of liability clauses unenforceable regardless of the chosen governing law.
- **Unsigned or draft contracts** — Clearly note that analysis is based on draft language and that final terms may differ. Track version numbers if available and compare against any prior versions to identify changes.
- **Contracts with arbitration clauses** — Flag mandatory arbitration with class action waivers, especially in consumer or employment contexts where enforceability varies by jurisdiction. Note the arbitration forum (AAA, JAMS) and whether the cost allocation is fair.
- **Force majeure and pandemic language** — Post-2020 contracts may have expanded force majeure definitions or explicitly include pandemics and government shutdowns. Assess whether they're symmetric and whether they excuse payment obligations or just performance obligations.
