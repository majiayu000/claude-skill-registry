---
name: solvency-ii
description: 'description: Solvency II framework — three pillars, SCR, MCR, ORSA.'
---

# Solvency II

name: solvency-ii
description: Solvency II framework — three pillars, SCR, MCR, ORSA.

## When to Activate

- Calculating Solvency Capital Requirement (SCR) and Minimum Capital Requirement (MCR)
- Understanding the three-pillar structure of Solvency II
- Performing or reviewing an Own Risk and Solvency Assessment (ORSA)
- Classifying and valuing insurance liabilities (best estimate + risk margin)
- Assessing eligible own funds and tiering (Tier 1, 2, 3)
- Evaluating risk modules under the standard formula
- Comparing standard formula vs internal model approaches
- Analyzing group solvency and intra-group transactions
- Regulatory reporting (QRTs — Quantitative Reporting Templates)
- Solvency and Financial Condition Report (SFCR) preparation

## Core Concepts

### Three-Pillar Structure

**Pillar 1 — Quantitative Requirements:**
- Valuation of assets and liabilities (market-consistent)
- Technical provisions = Best Estimate Liabilities (BEL) + Risk Margin
- Solvency Capital Requirement (SCR) — target capital
- Minimum Capital Requirement (MCR) — absolute floor
- Own funds classification and eligibility
- Investment rules (prudent person principle)

**Pillar 2 — Qualitative Requirements (Governance):**
- System of governance (fit and proper, key functions)
- Risk management system and policies
- Own Risk and Solvency Assessment (ORSA)
- Internal control system
- Actuarial function requirements
- Outsourcing governance
- Supervisory review process

**Pillar 3 — Reporting and Disclosure:**
- Solvency and Financial Condition Report (SFCR) — public
- Regular Supervisory Report (RSR) — to supervisor
- Quantitative Reporting Templates (QRTs) — structured data
- Annual and quarterly reporting cycles
- Group reporting requirements

### Technical Provisions

```
Technical Provisions = Best Estimate Liabilities (BEL) + Risk Margin

Best Estimate Liabilities:
  = Probability-weighted average of future cash flows
  = PV of expected future claim payments + expenses - future premiums
  Discounted at risk-free rate (EIOPA publishes term structures)

  Adjustments to risk-free rate:
  - Volatility Adjustment (VA): Correction for credit spread volatility
  - Matching Adjustment (MA): For portfolios of illiquid liabilities matched with assets
  - Transitional measures: Phased introduction for legacy portfolios

Risk Margin:
  = Cost of capital required to run off the insurance liabilities
  = Cost-of-Capital rate (6%) x PV of future SCR over run-off period
  Represents the amount a third party would require above BEL to take over the liabilities
```

### Solvency Capital Requirement (SCR)

**Standard Formula — modular structure:**
```
SCR = BSCR + Adj + SCR_op

BSCR (Basic SCR) — aggregated using correlation matrices:

                    Market   Default   Life    Health   Non-Life
  Market risk        1.00
  Counterparty def.  0.25     1.00
  Life underwriting  0.25     0.25     1.00
  Health UW          0.25     0.25     0.25    1.00
  Non-life UW        0.25     0.50     0.00    0.00     1.00

BSCR = sqrt(Sum_ij Corr_ij x SCR_i x SCR_j) + SCR_intangibles

Adj = Adjustment for loss-absorbing capacity of technical provisions and deferred taxes
SCR_op = Operational risk capital charge
```

**SCR risk modules:**

| Module | Sub-modules | Key Risk |
|--------|------------|----------|
| Market risk | Interest rate, equity, property, spread, concentration, currency | Asset value changes |
| Counterparty default | Type 1 (reinsurance, derivatives), Type 2 (receivables) | Counterparty failure |
| Life underwriting | Mortality, longevity, disability, lapse, expense, revision, catastrophe | Insurance risk (life) |
| Health underwriting | SLT health, non-SLT health, catastrophe | Insurance risk (health) |
| Non-life underwriting | Premium & reserve, lapse, catastrophe (natural, man-made) | Insurance risk (non-life) |
| Operational risk | Based on premiums and technical provisions | Operational failures |

**SCR calculation method:**
```
Each sub-module applies a prescribed stress:
  - Equity risk: 39% + symmetric adjustment (type 1) or 49% (type 2) instantaneous fall
  - Interest rate risk: Prescribed up/down shifts to yield curve
  - Spread risk: Instantaneous widening based on rating and duration
  - Property risk: 25% instantaneous fall
  - Longevity risk: 20% permanent decrease in mortality rates
  - Lapse risk: Max of mass lapse (40%), permanent increase (50%), permanent decrease (50%)
  - Non-life CAT: Scenario-based (natural catastrophe models by peril and region)

SCR for each module = Change in net asset value (own funds) under the stress
```

### Minimum Capital Requirement (MCR)

```
MCR = Max(MCR_linear, 25% x SCR)
MCR = Min(MCR, 45% x SCR)
MCR = Max(MCR, Absolute Floor)

Absolute floors:
  Life:              EUR 3.7M
  Non-life:          EUR 2.5M
  Composite:         EUR 3.7M
  Reinsurance:       EUR 3.6M

MCR_linear: Based on technical provisions and premiums written
  (simpler calculation than SCR — provides an absolute minimum)

Breaching MCR triggers ultimate supervisory intervention (license withdrawal)
Breaching SCR triggers recovery plan and supervisory escalation
```

### Own Funds

**Classification into tiers based on quality:**

| Tier | Characteristics | Examples | SCR Coverage Limit | MCR Coverage Limit |
|------|----------------|---------|-------------------|-------------------|
| Tier 1 (unrestricted) | Permanent, fully loss-absorbing, subordinated | Paid-up ordinary share capital, retained earnings, reconciliation reserve | Unlimited | Unlimited (min 80% of MCR) |
| Tier 1 (restricted) | Permanent, loss-absorbing, call after 5+ years | Perpetual subordinated instruments | Max 20% of Tier 1 | Max 20% of Tier 1 |
| Tier 2 | Subordinated, minimum 10-year maturity | Dated subordinated debt, unpaid called-up capital | Max 50% of SCR | Max 20% of MCR |
| Tier 3 | Subordinated, minimum 5-year maturity | Short-dated subordinated debt, net DTA | Max 15% of SCR | Not eligible |

**Solvency ratio:**
```
Solvency Ratio = Eligible Own Funds / SCR x 100%

Target: > 100% (absolute minimum)
Comfortable: > 150-180% (most insurers target this range)
Strong: > 200%

Below 100%: Recovery plan required, supervisor intensifies oversight
Below MCR:  Finance scheme required, ultimate intervention possible
```

### ORSA (Own Risk and Solvency Assessment)

**Purpose:** Forward-looking self-assessment of the undertaking's overall solvency needs considering its specific risk profile, risk tolerance, and business strategy.

**ORSA requirements:**
1. **Overall solvency needs:** Assessment of capital needs beyond the regulatory SCR, considering risks not fully captured by the standard formula
2. **Continuous compliance:** Forward-looking projection of SCR and own funds over the business planning horizon (typically 3-5 years)
3. **Deviation from standard formula assumptions:** Assessment of whether the standard formula SCR appropriately reflects the undertaking's risk profile

**ORSA process:**
```
1. Risk identification and assessment
   - Quantifiable risks (market, underwriting, credit, operational)
   - Non-quantifiable risks (strategic, reputational, regulatory)
   - Emerging risks

2. Stress testing and scenario analysis
   - Regulatory stress scenarios
   - Reverse stress tests (what breaks the business?)
   - Company-specific scenarios (key risk concentrations)

3. Capital projection
   - Base case: SCR and own funds over planning period
   - Adverse scenario: Impact on solvency ratio
   - Management actions: Planned responses to solvency deterioration

4. Board sign-off
   - ORSA report presented to and approved by the board
   - Integration with business strategy and capital planning
   - Documented decision-making process
```

### Standard Formula vs Internal Model

| Feature | Standard Formula | Internal Model |
|---------|-----------------|----------------|
| Complexity | Prescribed calculations | Company-specific model |
| Calibration | Regulatory parameters | Own data and assumptions |
| Risk sensitivity | Moderate | High (reflects actual risk profile) |
| Approval | Automatic | Requires supervisory approval (pre-application, documentation, validation) |
| Diversification | Prescribed correlation matrices | Company-specific correlations |
| Cost | Low | High (build, validation, ongoing maintenance) |
| Typical users | Small-mid insurers | Large insurers, complex risk profiles |

## Methodology

1. **Valuation**: Mark assets to market; calculate BEL and risk margin for technical provisions
2. **Own funds determination**: Classify capital instruments into tiers; apply limits
3. **SCR calculation**: Apply standard formula stresses or run internal model; aggregate using correlation matrix
4. **MCR calculation**: Apply linear formula and corridor (25-45% of SCR)
5. **Solvency ratio**: Eligible own funds / SCR; assess against target and trigger levels
6. **ORSA**: Forward-looking solvency projection; stress testing; board reporting
7. **Reporting**: Prepare QRTs, SFCR, and RSR per regulatory timelines

## Templates

### Solvency Position Summary

```
=== SOLVENCY II POSITION ===

                                        Amount (EUR M)
Own Funds:
  Tier 1 unrestricted                   __________
  Tier 1 restricted                     __________
  Tier 2                                __________
  Tier 3                                __________
  Total own funds                       __________
  Eligible own funds (after limits)     __________

SCR Components:
  Market risk                           __________
  Counterparty default risk             __________
  Life underwriting risk                __________
  Health underwriting risk              __________
  Non-life underwriting risk            __________
  Diversification benefit               (__________)
  BSCR                                  __________
  Operational risk                      __________
  Adj (loss-absorbing capacity)         (__________)
  SCR                                   __________

MCR                                     __________

Solvency Ratio (Own Funds / SCR):       ____%
MCR Coverage (Own Funds / MCR):         ____%

Status: [ ] Compliant  [ ] Recovery Plan  [ ] Finance Scheme
```

### ORSA Solvency Projection

```
=== FORWARD-LOOKING SOLVENCY PROJECTION ===

                        Year 0      Year 1      Year 2      Year 3
                       (Actual)   (Projected) (Projected) (Projected)
Own funds              ________   ________    ________    ________
SCR                    ________   ________    ________    ________
Solvency ratio         ____%      ____%       ____%       ____%

Stress scenario (equity -30%, spread +100bp):
Own funds              ________   ________    ________    ________
SCR                    ________   ________    ________    ________
Solvency ratio         ____%      ____%       ____%       ____%

Management actions:
  Dividend restriction:   Trigger at ____% solvency ratio
  De-risking:             Trigger at ____% solvency ratio
  Capital raise:          Trigger at ____% solvency ratio
```

## Quality Gate

- [ ] Technical provisions calculated as BEL + risk margin using EIOPA risk-free rate curves
- [ ] Volatility adjustment or matching adjustment applied only where criteria are met
- [ ] Own funds classified into correct tiers with eligibility limits applied
- [ ] SCR modules correctly stressed using prescribed calibrations
- [ ] Diversification benefit calculated using regulatory correlation matrices
- [ ] Loss-absorbing capacity of deferred taxes substantiated with recoverability analysis
- [ ] MCR calculated within the 25-45% SCR corridor and above absolute floor
- [ ] ORSA covers forward-looking solvency projection under base and stress scenarios
- [ ] Standard formula appropriateness assessed (ORSA requirement)
- [ ] QRTs completed per regulatory templates and timelines
- [ ] SFCR prepared for public disclosure with required content sections
- [ ] Group solvency calculations include all subsidiaries and eliminate intra-group transactions
