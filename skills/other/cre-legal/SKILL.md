---
name: cre-legal
description: "CRE Legal review suite — 6 specialist skills for PSA review, title & survey analysis, estoppel tracking, loan document review, insurance coordination, and transfer document preparation for multifamily acquisitions."
argument-hint: "[task-description]"
---

# CRE Legal Suite

You have access to 6 specialist legal review skills for commercial real estate multifamily acquisitions.

## Available Skills

| Skill | File | Use When |
|-------|------|----------|
| PSA Reviewer | `skills/psa-reviewer.md` | User provides a Purchase & Sale Agreement and wants clause-by-clause analysis — contingencies, representations, earnest money, closing conditions |
| Title & Survey Reviewer | `skills/title-survey-reviewer.md` | User provides title commitment or ALTA survey and wants exception analysis, easement impact, encroachment detection, flood/zoning review |
| Estoppel Tracker | `skills/estoppel-tracker.md` | User needs to manage estoppel certificate collection — tracking, validation against rent roll, discrepancy identification |
| Loan Doc Reviewer | `skills/loan-doc-reviewer.md` | User provides loan documents and wants review against the approved term sheet — note, mortgage, guaranty, environmental indemnity, UCC |
| Insurance Coordinator | `skills/insurance-coordinator.md` | User needs to verify insurance requirements from lender and PSA — coverage types, limits, gap analysis, premium estimates |
| Transfer Doc Preparer | `skills/transfer-doc-preparer.md` | User needs transfer documentation prepared — deed, bill of sale, assignment of leases, FIRPTA, transfer tax, entity verification |

## How to Use

1. Read the user's request to determine which skill(s) are needed
2. Load the full skill file — e.g., `Read skills/psa-reviewer.md`
3. Follow the Strategy steps exactly
4. Produce output in the specified format
5. Run Quality Checks before delivering results

For deeper analysis, load the legal knowledge base:
- `knowledge/legal-checklist.md` — comprehensive legal compliance requirements across the acquisition lifecycle

If the user says "$ARGUMENTS", use that to determine which skill to load.

## Quick Reference

**PSA Reviewer** — Analyzes: contingency periods (inspection, financing, title), representations and warranties, earnest money terms (amount, hard/soft dates), closing conditions, seller obligations, assignment rights, default remedies. Flags: missing contingencies, one-sided provisions, shortened timelines.

**Title & Survey Reviewer** — Reviews: Schedule B exceptions, easements (utility, access, drainage), encroachments, boundary discrepancies, flood zone determination (FEMA), zoning compliance, CC&Rs, mineral rights. Produces: exception analysis with cure recommendations.

**Estoppel Tracker** — Manages: certificate collection (sent/received/outstanding), validates tenant-reported rent vs rent roll, lease dates, deposit amounts, landlord obligations. Flags: discrepancies >5% on rent, date mismatches, unreported side agreements.

**Loan Doc Reviewer** — Reviews: promissory note, mortgage/deed of trust, guaranty (carve-out vs full recourse), environmental indemnity, UCC-1 filings. Cross-checks: every term against the approved term sheet. Flags: deviations, missing provisions, non-standard clauses.

**Insurance Coordinator** — Verifies: property coverage, general liability, flood, windstorm, umbrella/excess, business interruption, builder's risk (if renovating). Compares: lender requirements vs PSA requirements vs current policies. Outputs: gap analysis with premium estimates.

**Transfer Doc Preparer** — Prepares: warranty deed, bill of sale, assignment and assumption of leases, FIRPTA certificate, transfer tax calculations by jurisdiction, entity verification (good standing, authority to transact). Outputs: complete document drafts with filing instructions.
