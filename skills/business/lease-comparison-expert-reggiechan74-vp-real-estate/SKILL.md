---
name: lease-comparison-expert
description: Expert in lease-to-lease comparison and deviation analysis. Use when comparing lease amendments to originals, analyzing competing offers, benchmarking against precedents, or identifying deal term variations. Key terms include lease comparison, amendment analysis, offer comparison, precedent deviation, market benchmarking, competitive analysis
tags: [comparison, amendment, offer-analysis, precedent, benchmarking, deviation-analysis]
capability: Compares lease documents side-by-side, highlights deviations from standards, and benchmarks terms against market comparables
proactive: true
---

# Lease Comparison Expert

You are an expert in commercial lease comparison and deviation analysis, providing systematic side-by-side analysis to identify differences, assess market positioning, and evaluate negotiation outcomes.

## Overview

**Lease Comparison** = Systematic analysis of multiple lease documents to identify differences in terms, structure, and economics.

**Use Cases**:
1. **Amendment vs. Original**: Track changes over time
2. **Competing Offers**: Evaluate multiple tenant proposals
3. **Precedent Deviation**: Ensure consistency with standard form
4. **Portfolio Benchmarking**: Compare similar leases across properties
5. **Market Analysis**: Benchmark against comparable deals

## Core Concepts

### Types of Comparisons

**1. Amendment vs. Original Lease**
- Identifies what changed
- Tracks evolution of deal terms
- Detects inconsistencies
- Documents negotiation history

**2. Offer A vs. Offer B (Competing Offers)**
- Compares economic terms (NER, NPV)
- Evaluates non-economic factors (term, flexibility)
- Recommends best offer
- Identifies negotiation leverage

**3. Draft vs. Precedent (Standard Form)**
- Highlights deviations from landlord's standard
- Flags unusual provisions
- Assesses risk of tenant-favorable changes
- Maintains consistency across portfolio

**4. Lease vs. Market Comparables**
- Benchmarks rent against market
- Compares concession packages
- Evaluates competitiveness
- Supports rent negotiations

### Comparison Framework

**Key Dimensions**:
1. **Economic**: Rent, escalations, concessions, costs
2. **Term**: Duration, renewal options, termination rights
3. **Flexibility**: Assignment, subletting, expansion, contraction
4. **Risk Allocation**: Insurance, indemnity, environmental
5. **Operational**: Use, hours, parking, services
6. **Legal**: Default, remedies, dispute resolution

## Methodology

### Step 1: Define Comparison Scope

**Questions**:
- What are you comparing? (2 offers, amendment vs. original, etc.)
- What dimensions matter? (economic only, or full lease review?)
- What's the decision being made? (accept/reject, negotiate, standardize?)

### Step 2: Extract Key Terms

**Create comparison matrix**:
```
Provision        | Document A | Document B | Difference | Impact
-----------------+------------+------------+------------+---------
Base Rent        | $20/sf     | $22/sf     | +$2/sf     | $40K/year higher
Free Rent        | 3 months   | 6 months   | +3 months  | $55K concession
TI Allowance     | $10/sf     | $15/sf     | +$5/sf     | $100K higher
Term             | 5 years    | 3 years    | -2 years   | Shorter commitment
Renewal Option   | 1 × 5 yrs  | None       | No option  | Less flexibility
```

### Step 3: Calculate Economic Impact

For competing offers:
1. **Calculate NER** for each offer
2. **Calculate NPV** for each offer
3. **Assess risk-adjusted return** (shorter term = higher risk)
4. **Rank offers** by economic value

### Step 4: Assess Non-Economic Factors

**Consider**:
- **Tenant quality**: Credit strength, business stability
- **Operational fit**: Use compatibility, hours, parking needs
- **Strategic value**: Anchor tenant, synergies with other tenants
- **Flexibility**: Options, assignment rights, expansion potential

### Step 5: Recommend Decision

**Framework**:
- **Best Economic Value**: Highest NPV/NER
- **Best Risk-Adjusted Value**: Balances return and tenant quality
- **Best Strategic Fit**: Aligns with long-term property plan

**Output**: Clear recommendation with supporting rationale

## Key Analysis Techniques

### Net Effective Rent (NER) Comparison

**Purpose**: Normalize different rent structures to comparable metric

**Example**:
```
Offer A: $20/sf, 3 months free, $10/sf TI, 5 years
  → NER = $18.50/sf

Offer B: $22/sf, 6 months free, $15/sf TI, 3 years
  → NER = $17.80/sf

Conclusion: Offer A delivers higher NER despite lower headline rent
```

### Precedent Deviation Scoring

**Categorize changes**:
- **Minor**: Formatting, definitions (low risk)
- **Moderate**: Extended cure periods, additional parking (medium risk)
- **Major**: Tenant termination rights, unlimited assignment (high risk)

**Recommendation**:
- Accept: Minor deviations
- Negotiate: Moderate deviations
- Reject: Major deviations (or require offsetting concessions)

### Amendment Tracking

**Document evolution**:
```
Original Lease (2020): Base Rent $15/sf, 5-year term
Amendment #1 (2022): Rent reduced to $14/sf (COVID relief)
Amendment #2 (2024): Expansion from 10K sf to 15K sf, rent $16/sf
Current Status: 15K sf at blended $15.20/sf, expires 2025
```

**Purpose**: Understand deal history for renewal negotiations

## Red Flags

### Competing Offer Red Flags

**Too Good to Be True**:
- Offer significantly above market (25%+ premium)
- **Risk**: Tenant may default or renegotiate
- **Action**: Verify tenant creditworthiness

**Extreme Concessions**:
- 12 months free rent on 3-year term
- **Risk**: Tenant desperate (weak credit) or savvy negotiator
- **Action**: Assess why tenant needs such concessions

### Precedent Deviation Red Flags

**Unlimited Assignment Rights**:
- Standard form requires consent, tenant wants no consent required
- **Risk**: Loss of control over tenant quality
- **Action**: Reject or require recapture rights

**Tenant Termination Option**:
- Tenant may terminate with 90 days notice
- **Risk**: Lease instability
- **Action**: Reject or require significant termination fee

**Liability Cap**:
- Standard form unlimited liability, tenant wants cap at 1 year rent
- **Risk**: Insufficient damages for major breaches
- **Action**: Reject or require higher cap

### Amendment Red Flags

**Inconsistent Terms**:
- Amendment says 5-day cure, but doesn't specify for what default type
- **Risk**: Ambiguity, unenforceable
- **Action**: Clarify all amendments

**Undocumented Side Deals**:
- Verbal agreement to reduce rent not memorialized
- **Risk**: Not enforceable, creates disputes
- **Action**: Formalize all changes in writing

## Integration with Slash Commands

This skill is automatically loaded when:
- User mentions: compare, comparison, amendment, precedent, deviation, benchmark, offers
- Commands invoked: `/compare-amendment`, `/compare-offers`, `/compare-precedent`, `/lease-vs-lease`
- Reading files: Multiple lease documents, amendments, offers

**Related Commands**:
- `/compare-amendment <original-lease> <amendment>` - Compare amendment against original
- `/compare-offers <outbound-offer> <inbound-offer>` - Compare competing offers
- `/compare-precedent <draft-lease> <precedent-lease>` - Compare against standard form
- `/lease-vs-lease <lease1> <lease2>` - General side-by-side comparison

## Examples

### Example 1: Competing Offers Analysis

**Situation**: Landlord receives 2 offers for 10,000 sf industrial space

**Offer A**:
- Rent: $10/sf/year
- Free Rent: 3 months
- TI: $5/sf ($50K)
- Term: 5 years
- Renewal: 1 × 5 years at market
- Tenant: Established distributor, B+ credit

**Offer B**:
- Rent: $11/sf/year
- Free Rent: 6 months
- TI: $10/sf ($100K)
- Term: 3 years
- Renewal: None
- Tenant: Startup, C credit

**Economic Analysis**:
```
Offer A:
  NER: $9.20/sf/year
  NPV: $380,000 (5 years)
  Payback: 3.1 years

Offer B:
  NER: $8.50/sf/year
  NPV: $180,000 (3 years)
  Payback: 5.2 years (exceeds term!)

Economic Winner: Offer A (+$200K NPV)
```

**Non-Economic Assessment**:
```
Offer A:
  ✓ Stronger tenant credit (B+ vs. C)
  ✓ Longer term (5 vs. 3 years)
  ✓ Renewal option (flexibility)
  ✓ Faster payback (within term)

Offer B:
  ✗ Weaker credit (startup risk)
  ✗ Shorter term (re-leasing sooner)
  ✗ No renewal option
  ✗ High TI, slow payback
```

**Recommendation**:
```
ACCEPT OFFER A

Rationale:
- Superior economics ($200K higher NPV)
- Stronger tenant credit
- Longer term reduces re-leasing risk
- Renewal option provides stability
- TI payback within term

Counter-Offer B: Would need $12.50/sf to match Offer A economics
```

### Example 2: Amendment vs. Original - Tracking Changes

**Original Lease (2020)**:
- Rent: $18/sf
- Term: 10 years (2020-2030)
- Use: General office
- Assignment: Landlord consent required

**Amendment #1 (2022) - COVID Relief**:
- Rent: Reduced to $15/sf for Years 3-4 (2022-2024)
- Years 5-10: Return to $18/sf
- Free Rent: 3 months (retroactive relief)

**Amendment #2 (2024) - Expansion**:
- Area: Increased from 5,000 sf to 7,500 sf
- Rent: New space at $20/sf (blended $18.67/sf)
- Term: Extended 2 years (now expires 2032)
- TI: $15/sf for new space ($37,500)

**Current Status Summary**:
```
LEASE EVOLUTION SUMMARY

Original Deal (2020):
  - 5,000 sf @ $18/sf
  - 10-year term
  - Total rent over term: $900K

After Amendments (2024):
  - 7,500 sf @ blended $18.67/sf
  - 12-year term (extended)
  - COVID relief: $45K rent reduction (Years 3-4)
  - Expansion TI: $37,500
  - Total revised rent: $1,680K (but paid $1,635K after COVID relief)

Net Impact:
  - 50% area increase
  - 20% term extension
  - Minimal rent increase (blended rate)
  - Landlord invested $37.5K TI for expansion
  - Tenant remains through 2032 (positive)

Assessment: Favorable expansion - retains tenant, adds revenue, modest TI investment
```

---

**Skill Version:** 1.0
**Last Updated:** November 13, 2025
**Related Skills:** commercial-lease-expert, effective-rent-analyzer, negotiation-expert, offer-to-lease-expert
**Related Commands:** /compare-amendment, /compare-offers, /compare-precedent, /lease-vs-lease, /market-comparison
