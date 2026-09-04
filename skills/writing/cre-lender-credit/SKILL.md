---
name: cre-lender-credit
description: "CRE Lender/Credit analysis suite - 8 specialist skills for U.S. CRE loan screening and sizing, sponsor and appraisal review, credit memo writing, annual risk rating, covenant and watchlist monitoring, problem loans, and portfolio stress testing."
argument-hint: "[task-description]"
license: Apache-2.0
metadata:
  author: "Avi Hacker, J.D."
  organization: "The AI Consulting Network"
  homepage: https://www.theaiconsultingnetwork.com
  source: https://github.com/ahacker-1/cre-agent-skills
  copyright: "Copyright 2026 Avi Hacker, J.D. / The AI Consulting Network"
---

# CRE Lender/Credit Suite

You have access to 8 specialist lender/credit skills for U.S. commercial real estate lending and credit administration.

## Available Skills

| Skill | File | Use When |
|---|---|---|
| Loan Request Screening and Sizing | `skills/loan-request-screening-and-sizing.md` | User needs an incoming loan request screened for product and policy fit, sized under every applicable test, and a pursue / pursue with structure / decline verdict |
| Sponsor and Guarantor Analyst | `skills/sponsor-and-guarantor-analyst.md` | User needs sponsor or guarantor financial analysis, verified liquidity and net worth, global cash flow and global DSCR, or guaranty structure |
| Appraisal and Valuation Reviewer | `skills/appraisal-and-valuation-reviewer.md` | User needs a CRE appraisal or evaluation reviewed for regulatory compliance and analytical reasonableness, or an accept / condition / reject decision |
| Credit Memo Writer | `skills/credit-memo-writer.md` | User needs a CRE credit approval memorandum an approval authority, loan review, and an examiner can all read in the same order |
| Annual Loan Review and Risk Rating | `skills/annual-loan-review-and-risk-rating.md` | User needs the periodic review of an existing CRE loan, refreshed ratios and appraisal-age testing, and a confirmed or changed risk rating |
| Covenant Compliance and Watchlist Monitor | `skills/covenant-compliance-and-watchlist-monitor.md` | User needs covenant and reporting-obligation testing, or a watchlist placement, retention, or removal recommendation |
| Problem Loan and Modification Analyst | `skills/problem-loan-and-modification-analyst.md` | User needs a deteriorating loan classified, the source of impairment named, or resolution paths compared with a lender action plan |
| CRE Portfolio Concentration and Stress Tester | `skills/cre-portfolio-concentration-and-stress-tester.md` | User needs loan-book segmentation, supervisory concentration screening, sensitivity/scenario stress testing, or a board or ALCO-ready report |

## How to Use

1. Read the user's request to determine which lender/credit skill is needed.
2. Load the full skill file, for example: `Read skills/credit-memo-writer.md`.
3. Load relevant knowledge files when the skill asks for them.
4. Follow the Strategy steps exactly.
5. Produce output in the specified format.
6. Run Quality Checks before delivering results.

For deeper analysis, load knowledge bases:

- `knowledge/lender-credit-policy-benchmarks.md` - lender credit policy benchmarks and underwriting guardrails across bank, credit union, debt fund, life company, agency, and CMBS lenders
- `knowledge/regulatory-risk-rating-and-classification.md` - interagency risk rating scale, classification, nonaccrual, and workout treatment for regulated CRE lenders
- `knowledge/credit-memo-and-appraisal-review-standards.md` - credit approval memorandum content and collateral valuation review standards for regulated lenders
- `knowledge/cre-concentration-and-stress-testing.md` - CRE concentration screening criteria and stress-testing methodology for regulated depository lenders
- `knowledge/underwriting-calc.md` - canonical CRE formulas
- `knowledge/risk-scoring.md` - risk categorization for IC memo synthesis

If the user says "$ARGUMENTS", use that to determine which skill to load.

## Quick Reference

**Loan Request Screening and Sizing** - Product and policy fit, sizing under every test, controlling test identification, pursue/decline verdict, indicative structure.

**Sponsor and Guarantor Analyst** - Personal and entity financials, verified liquidity and net worth, contingent liabilities and REO, global cash flow, track record, guaranty structure.

**Appraisal and Valuation Reviewer** - Regulatory compliance, analytical reasonableness, reconciliation to underwriting, accept/condition/reject decision.

**Credit Memo Writer** - Approval memorandum readable in the same order by approval authority, loan review, and examiners.

**Annual Loan Review and Risk Rating** - Refreshed NOI, DSCR, debt yield, LTV, appraisal age, rollover, sponsor condition, covenant status, rating migration.

**Covenant Compliance and Watchlist Monitor** - Covenant testing, reporting obligations, structural triggers, watchlist placement/retention/removal, action plan.

**Problem Loan and Modification Analyst** - Impairment classification, resolution-path comparison on recovery/timing/cost/accounting, downgrade triggers.

**CRE Portfolio Concentration and Stress Tester** - Loan-book segmentation, supervisory concentration criteria, sensitivity and scenario stress, rating migration and reserve pressure estimates.

---

## Attribution

Built and maintained by [The AI Consulting Network](https://www.theaiconsultingnetwork.com/?utm_source=github&utm_medium=skill-file&utm_campaign=cre-agent-skills), the commercial real estate AI consulting practice of Avi Hacker, J.D., and part of [CRE Agent Skills](https://github.com/ahacker-1/cre-agent-skills), an open-source library of AI skills for commercial real estate.

If this skill saved you time and you want systems like it built inside your firm, [reach out](https://www.theaiconsultingnetwork.com/contact?utm_source=github&utm_medium=skill-file&utm_campaign=cre-agent-skills). We would love to work with you.

Copyright 2026 Avi Hacker, J.D. / The AI Consulting Network. Licensed under the [Apache License 2.0](https://github.com/ahacker-1/cre-agent-skills/blob/main/LICENSE). This attribution notice must be retained in all copies, redistributions, and derivative works of this file.
