---
name: managing-liquidity-risk
description: Structures liquidity risk management with cash flow projections, stress testing, and contingency planning. Use when managing liquidity risk, projecting cash needs, or developing liquidity contingency plans.
tags:
  - management
  - risk-management
  - risk
metadata:
  author: casemark
  practice_areas:
    - Risk Management
    - Enterprise Risk
    - Market Risk
  document_types:
    - Management Report
  skill_modes:
    - Management
    - Coordination
---
# Managing Liquidity Risk

## When To Use

- Building or updating a liquidity risk management framework for a fund, bank, or corporate treasury
- Projecting cash flow needs across operating, investing, and financing activities over 30/60/90/180/360-day horizons
- Designing stress test scenarios (market-wide, idiosyncratic, or combined) for liquidity adequacy
- Developing or revising a contingency funding plan (CFP)
- Preparing liquidity coverage ratio (LCR) or net stable funding ratio (NSFR) reporting [VERIFY: applicable regulatory framework — Basel III, local banking regulator, or internal policy]
- Responding to a liquidity event, margin call acceleration, or counterparty credit deterioration

## Inputs To Gather

- **Cash flow data**: Operating receipts/disbursements, scheduled debt maturities, committed credit facility terms, and capital expenditure pipeline
- **Asset inventory**: Unencumbered high-quality liquid assets (HQLA) with haircut assumptions, repo-eligible collateral, and time-to-monetize estimates
- **Funding sources**: Committed vs. uncommitted lines, deposit composition (sticky vs. hot money), wholesale funding maturities, and intercompany lending arrangements
- **Counterparty exposure**: Margin call triggers, collateral substitution rights, and cross-default/cross-acceleration clauses
- **Regulatory parameters**: Applicable LCR/NSFR thresholds, intraday liquidity requirements, and internal risk appetite limits [VERIFY: jurisdiction-specific minimums]
- **Historical data**: Prior stress episodes, seasonal cash flow patterns, and drawdown experience on credit facilities

## Workflow

1. **Map the liquidity position**
   - Aggregate all cash inflows and outflows by time bucket (overnight, 1–7 days, 8–30 days, 31–90 days, 91–180 days, 181–360 days)
   - Classify assets by liquidity tier: Tier 1 (cash, central bank reserves, sovereign bonds), Tier 2A (agency MBS, high-grade corporates), Tier 2B (lower-grade corporates, equities) [VERIFY: HQLA classification per applicable regime]
   - Identify concentration risks — single-counterparty funding, currency mismatches, or maturity cliffs

2. **Build cash flow projections**
   - Construct a base-case projection using contractual maturities and expected behavioral cash flows
   - Layer in behavioral assumptions for non-maturity deposits, prepayments, and drawdown rates on revolving facilities
   - Flag any bucket where cumulative net cash flow turns negative as a gap requiring action

3. **Design and run stress scenarios**
   - **Idiosyncratic scenario**: Credit downgrade (1–3 notches), loss of unsecured wholesale funding, accelerated deposit outflows (10–30% runoff over 30 days), collateral margin calls
   - **Market-wide scenario**: Credit spread widening (e.g., +200–500 bps), repo market disruption, central bank facility access constraints, asset price declines (20–40% on equities, 5–15% on fixed income)
   - **Combined scenario**: Simultaneous idiosyncratic and market stress; assume no access to unsecured markets for 30–90 days
   - For each scenario, calculate the survival horizon — the number of days the entity can meet all obligations without external support

4. **Develop the contingency funding plan**
   - Rank liquidity actions by speed and cost: (a) draw on committed facilities, (b) sell HQLA, (c) repo unencumbered collateral, (d) reduce discretionary outflows, (e) negotiate liability extensions
   - Assign trigger levels (early warning, escalation, crisis) tied to specific metrics — e.g., available liquidity buffer falling below 120% of 30-day stressed outflows
   - Define governance: who declares each trigger level, communication protocols (board, regulators, counterparties), and decision authority for asset sales

5. **Compile the liquidity risk report**
   - Present current liquidity ratios (LCR, NSFR, internal metrics) against limits
   - Summarize stress test results with survival horizons and buffer adequacy
   - Highlight top 3–5 risk concentrations and recommended mitigants
   - Include an action tracker for open items from prior reviews

## Output

The deliverable is a **Liquidity Risk Management Report** containing:

- **Executive summary**: Current liquidity posture, key ratios vs. thresholds, and overall risk rating (green/amber/red)
- **Cash flow projection tables**: Base-case and stressed, by time bucket, with cumulative net position
- **Stress test dashboard**: Scenario assumptions, impact on liquid asset buffer, and survival horizon per scenario
- **Contingency funding plan**: Trigger framework, ranked action list with estimated capacity and mobilization time, and governance matrix
- **Risk concentration map**: Funding source concentration, maturity cliff analysis, and currency mismatch summary
- **Recommendations and action items**: Prioritized list with owners and deadlines

## Quality Checks

- All cash flow buckets reconcile to general ledger or treasury management system totals
- Stress scenario assumptions are documented and internally consistent — no double-counting of asset liquidation and repo capacity for the same collateral
- Survival horizons are calculated net of contingent outflows (margin calls, commitment drawdowns)
- Trigger levels in the CFP align with the institution's risk appetite statement and board-approved limits
- HQLA classifications and haircuts match the applicable regulatory framework [VERIFY: confirm against current regulatory guidance]
- Report distinguishes between contractual and behavioral cash flows with explicit disclosure of behavioral assumptions
- All [VERIFY] items are flagged for subject-matter expert review before distribution
