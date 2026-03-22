---
name: managing-sba-lending
description: Structures SBA loan origination with eligibility verification, packaging requirements, and guarantee documentation. Use when processing SBA loans, verifying eligibility, or preparing SBA packages.
tags:
  - management
  - commercial-banking
metadata:
  author: casemark
  practice_areas:
    - Commercial Banking
    - Trade Finance
    - Lending
  document_types:
    - Management Report
  skill_modes:
    - Management
    - Coordination
---
# Managing SBA Lending

Structures SBA loan origination with eligibility verification, packaging requirements, and guarantee documentation.

## When To Use

- Processing a new SBA 7(a), 504, or Express loan application through origination
- Verifying borrower and project eligibility against current SBA SOPs
- Assembling the loan authorization package for SBA guaranty submission
- Coordinating between borrower, lender, CDC (for 504), and SBA district office
- Auditing an in-progress SBA file for completeness before closing or purchase review

## Inputs To Gather

- **Borrower profile**: entity type, ownership structure (all 20%+ owners), citizenship/residency status, NAICS code, years in business, number of employees
- **Financial statements**: 3 years of business tax returns, personal tax returns for all guarantors, interim financials (P&L + balance sheet), personal financial statements (SBA Form 413)
- **Loan request details**: loan amount, use of proceeds breakdown (real estate, equipment, working capital, refinance, acquisition), term and amortization requested
- **Collateral schedule**: real estate appraisals, equipment valuations, existing liens (UCC search results, title commitments)
- **SBA-specific forms**: SBA Form 1919 (Borrower Information), SBA Form 1920 (Lender's Application), SBA Form 148/148L (guaranty forms), SBA Form 912 (Statement of Personal History) [VERIFY: confirm current form numbers against active SBA SOP 50 10]
- **Credit reports**: business credit report (D&B or SBSS score), personal credit reports for all guarantors
- **Eligibility documentation**: size standard verification, credit-elsewhere test narrative, franchise agreement (if applicable, check SBA Franchise Directory)

## Workflow

1. **Screen eligibility**
   - Confirm the business meets SBA size standards by NAICS code (revenue or employee count) [VERIFY: current size standard table at sba.gov]
   - Verify the business is for-profit, operates in the U.S., and is not on the SBA ineligible industries list (SOP 50 10, Subpart B, Chapter 2)
   - Check ownership: all 20%+ owners must pass character screening (Form 912); confirm no debarment via SAM.gov
   - For 504 loans: confirm the project meets job creation/retention requirements (typically 1 job per $65,000 of SBA debenture) [VERIFY: current job creation ratio]

2. **Perform credit analysis**
   - Run the borrower through SBA SBSS (Small Business Scoring Service) — score ≥155 typically allows delegated processing [VERIFY: current SBSS threshold]
   - Analyze repayment ability: global debt service coverage ratio (minimum 1.15x–1.25x is typical; lender policy may vary)
   - Document the credit-elsewhere test: demonstrate the borrower cannot obtain credit on reasonable terms without the SBA guaranty
   - Assess collateral coverage; SBA requires lender to collateralize to the maximum extent possible but does not decline for insufficient collateral alone on 7(a) loans

3. **Structure the loan**
   - Match the appropriate SBA program to the use of proceeds:
     - **7(a)**: general purpose, max $5M, up to 85% guaranty (≤$150K) or 75% (>$150K) [VERIFY: current guaranty percentages and max loan amount]
     - **504**: fixed-asset projects (real estate/equipment), typically 50/40/10 structure (bank/CDC-SBA/borrower equity)
     - **Express**: expedited processing, max $500K, 50% guaranty [VERIFY: current Express cap]
   - Determine maturity: 25 years (real estate), 10 years (equipment), 10 years (working capital); blended terms for mixed-use
   - Calculate the SBA guaranty fee schedule based on loan amount and maturity [VERIFY: current fee tiers in SBA SOP 50 10]

4. **Package the loan authorization**
   - Complete SBA Form 1920 (Lender's Application for Guaranty) with full credit memo narrative
   - Attach all required exhibits: borrower financials, appraisals, environmental questionnaire (for real estate), franchise review (if applicable), standby agreements for any seller financing or equity injection
   - For PLP (Preferred Lender Program) lenders: prepare the file under delegated authority with the SBA Authorization boilerplate
   - For non-PLP: submit through SBA General Processing via E-Tran [VERIFY: confirm current E-Tran submission requirements]

5. **Manage closing and post-closing**
   - Track all SBA Authorization conditions (environmental clearance, equity injection verification, insurance requirements, lien perfection)
   - Ensure SBA note and guaranty documents use the required SBA form language — deviations void the guaranty
   - Confirm guaranty fee payment within the required timeframe (typically within 90 days of Authorization) [VERIFY: current guaranty fee payment deadline]
   - Submit the completed settlement sheet and any post-closing items to the SBA Loan Servicing Center

## Output

- **Eligibility determination memo**: confirms or denies SBA eligibility with specific SOP citations for each criterion
- **Credit analysis summary**: DSCR calculation, collateral analysis, credit-elsewhere narrative, SBSS score reference
- **Loan structure recommendation**: program type, amount, term, guaranty percentage, fee calculation
- **Packaging checklist**: itemized list of all required forms and exhibits with completion status
- **Conditions tracker**: matrix of Authorization conditions, responsible party, deadline, and current status

## Quality Checks

- Every eligibility determination cites the specific SOP 50 10 section (Subpart, Chapter, Paragraph)
- Guaranty fee calculation matches the current SBA fee schedule — errors here cause purchase denials
- All 20%+ owners are listed on Form 1919 and have completed Form 912 with fingerprint cards
- Equity injection is documented with source-and-use tracing (gift letters, bank statements, asset sale proceeds)
- Environmental review level matches the loan type and collateral (Phase I required for real estate over certain thresholds) [VERIFY: current environmental review thresholds]
- No SBA-prohibited fees are charged to the borrower (e.g., lender cannot charge a separate guaranty fee)
- Loan file is audit-ready for SBA purchase review — incomplete files are the primary cause of guaranty repair or denial
