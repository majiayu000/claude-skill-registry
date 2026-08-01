---
name: precedent-transactions
description: 'name: precedent-transactions'
---

# Precedent Transaction Analysis

name: precedent-transactions
description: Precedent transaction analysis for M&A valuation

## When to Activate

- User needs to value a company using historical M&A transaction data
- Evaluating what acquirers have paid for similar businesses
- Estimating control premiums or synergy-adjusted valuations
- Comparing transaction multiples against current trading multiples
- Building the precedent transactions section of a pitch book or fairness opinion

## Core Concepts

### What Precedent Transactions Measure

Precedent transactions reflect the price acquirers actually paid for similar companies, including control premiums and expected synergies. Unlike trading comps (minority stake, no control premium), transaction multiples embed the acquirer's willingness to pay above market value for strategic or financial control.

**Typical control premium range:** 20-40% over unaffected share price (varies by sector, deal dynamics, and competitive tension).

### Transaction Screening Criteria

**Primary filters:**
- Industry / sub-sector alignment with target
- Transaction size (enterprise value within 0.3x-3.0x of target, or broader if deal flow is limited)
- Geography (domestic, cross-border considerations)
- Time period (generally last 5-7 years; older deals may reflect different market conditions)
- Deal type (strategic vs financial buyer, majority vs minority stake)

**Secondary filters:**
- Target growth and margin profile at time of transaction
- Competitive auction vs negotiated sale
- Public vs private target (private deals may lack reliable data)
- Distressed vs non-distressed (exclude distressed unless specifically relevant)

### Data Sources

| Source | Coverage | Notes |
|--------|----------|-------|
| Capital IQ / FactSet | Broad, structured data | Best for screening and financial data |
| Bloomberg | Good coverage, deal terms | Transaction-specific fields |
| MergerMarket | Forward-looking, rumored deals | Useful for pipeline intelligence |
| Thomson Reuters / Refinitiv | Historical depth | Strong on older transactions |
| SEC filings (EDGAR) | US public targets | Merger proxies, fairness opinions contain detailed terms |
| Company press releases | First-hand deal terms | Often limited financial detail |

### Key Multiples

**Enterprise value-based (most common):**
- EV / Revenue (LTM at announcement)
- EV / EBITDA (LTM at announcement)
- EV / EBIT (LTM at announcement)

**Equity-based:**
- Price / Earnings
- Price / Book

**Sector-specific:**
- EV / Subscribers (telecom, media)
- Price / AUM (asset management)
- EV / Beds or EV / ARR (healthcare, SaaS)

### Control Premium Analysis

```
Control Premium = (Offer Price - Unaffected Price) / Unaffected Price × 100%
```

**Unaffected price:** Share price before deal rumors or announcement — typically 1 day, 1 week, or 1 month prior to the earliest public disclosure.

**Factors driving higher premiums:**
- Competitive bidding / auction process
- Significant expected synergies
- Strategic necessity for acquirer
- Target has strong standalone prospects
- Scarce asset in a consolidating industry

**Factors driving lower premiums:**
- Negotiated sale with single buyer
- Distressed seller
- Limited synergy potential
- Financial buyer (disciplined on price)

### Synergy-Adjusted Multiples

To compare transaction multiples with trading comps, back out the estimated synergy value:

```
Synergy-Adjusted Multiple = Transaction EV / (Target EBITDA + Expected Synergies)
```

This yields a "pre-synergy" multiple that is more comparable to trading comps. The difference between the raw transaction multiple and trading comp multiple approximates the control premium and synergy sharing.

## Methodology

### Step-by-Step Process

1. **Define screening criteria** — industry, size, geography, time period, deal type
2. **Run transaction screen** — use Capital IQ, FactSet, or Bloomberg
3. **Compile initial universe** — typically 20-40 transactions
4. **Filter to relevant set** — narrow to 10-20 most comparable deals
5. **Gather financial data** — target financials at time of announcement (LTM)
6. **Calculate multiples** — EV/Revenue, EV/EBITDA, EV/EBIT for each transaction
7. **Analyze deal context** — buyer type, auction vs negotiated, strategic rationale
8. **Compute statistics** — mean, median, 25th/75th percentile
9. **Apply time adjustment** — if market conditions have shifted materially
10. **Apply to target** — derive implied valuation range
11. **Compare with trading comps** — the spread indicates implied control premium

### Buyer Type Analysis

**Strategic buyers:**
- Typically pay higher multiples (synergy justification)
- Revenue synergies (cross-sell, market access) and cost synergies (SG&A, procurement)
- Multiple often 1-3x EBITDA turns above financial buyers

**Financial buyers (PE):**
- Disciplined around returns (target 20-25% IRR)
- Willingness to pay constrained by leverage capacity and exit assumptions
- May pay strategic-level multiples in competitive processes

**Separate transaction comps by buyer type when the distinction matters for the specific situation.**

### Time Adjustment

If comparing transactions from different market environments:
- Index transaction multiples to a common market benchmark (e.g., S&P 500 EV/EBITDA at time of deal vs today)
- Weight more recent transactions more heavily
- Flag transactions completed during market peaks or troughs

### Comparison with Trading Comps

```
Implied Control Premium = (Median Transaction Multiple / Median Trading Multiple - 1) × 100%

Example:
Median Transaction EV/EBITDA: 12.5x
Median Trading EV/EBITDA:     10.0x
Implied Control Premium:       25%
```

## Templates

### Precedent Transactions Summary

```
=== PRECEDENT TRANSACTION ANALYSIS ===

Target Company: [Name]
Screening Period: [Start Date] - [End Date]
Industry Focus: [Sector/Sub-sector]

--- Transaction Universe ---
Date     | Target       | Acquirer     | EV ($m) | EV/Rev | EV/EBITDA | Deal Type  | Premium
MM/YYYY  | Company A    | Buyer X      | ____    | ___x   |   ___x    | Strategic  |  ___%
MM/YYYY  | Company B    | Buyer Y      | ____    | ___x   |   ___x    | Financial  |  ___%
MM/YYYY  | Company C    | Buyer Z      | ____    | ___x   |   ___x    | Strategic  |  ___%
...

--- Summary Statistics ---
                    | EV/Revenue | EV/EBITDA | Control Premium
Mean                |    ___x    |   ___x    |     ___%
Median              |    ___x    |   ___x    |     ___%
25th Percentile     |    ___x    |   ___x    |     ___%
75th Percentile     |    ___x    |   ___x    |     ___%

--- Implied Valuation ---
Metric Applied       | Target Value | Low Multiple | High Multiple | Low EV   | High EV
EV/EBITDA            |    $____m    |    ___x      |     ___x      | $____m   | $____m
EV/Revenue           |    $____m    |    ___x      |     ___x      | $____m   | $____m

Implied EV Range:    $____m - $____m
Less: Net Debt       ($____m)
Implied Equity:      $____m - $____m
Per Share:           $____ - $____

--- Comparison to Trading Comps ---
                    | Trading Comps | Precedent Txns | Implied Premium
EV/EBITDA Median    |    ___x       |     ___x       |     ___%
EV/Revenue Median   |    ___x       |     ___x       |     ___%
```

### Transaction Context Notes

```
=== DEAL CONTEXT ===

Transaction: [Acquirer] / [Target] — [Date]
- Deal rationale: [Strategic/financial rationale]
- Process: [Auction / Negotiated / Hostile]
- Synergies announced: [$___m annual run-rate]
- Financing: [Cash / Stock / Mixed]
- Competing bids: [Yes/No — details]
- Relevance to our situation: [High/Medium/Low — why]
```

## Quality Gate

Before finalizing a precedent transaction analysis, verify:

- [ ] Transactions are genuinely comparable (industry, size, business model)
- [ ] Time period is appropriate (5-7 years max, with recency weighting)
- [ ] Financial data reflects LTM at announcement date (not at close)
- [ ] Distressed transactions are flagged or excluded as appropriate
- [ ] Buyer type (strategic vs financial) is documented for each deal
- [ ] Control premium is calculated using unaffected share price (pre-rumor)
- [ ] Transaction multiples are compared against trading comps with premium quantified
- [ ] Deal context is documented (auction vs negotiated, synergy expectations)
- [ ] Outliers are explained, not silently removed
- [ ] Implied valuation is presented as a range with clear methodology
- [ ] Private transactions with limited data are flagged for lower reliability
- [ ] Currency and accounting standard differences are noted
- [ ] At least 8-10 transactions for statistical reliability; fewer requires caveat
