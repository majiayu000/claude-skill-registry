# Comparable Company Analysis

name: comparable-analysis
description: Comparable company analysis (trading comps)

## When to Activate

- User needs to value a company using market-based relative valuation
- Selecting peer groups or relevant trading multiples
- Calendarizing financials for peer comparison
- Applying multiples to derive an implied valuation range
- Benchmarking a company's valuation against its sector

## Core Concepts

### What Trading Comps Measure

Trading comps derive implied valuation from how the public market values similar companies today. Unlike DCF (intrinsic value) or precedent transactions (transaction value with control premium), comps reflect current market sentiment and minority-stake value.

### Peer Group Selection

**Primary screening criteria:**
- Industry / sub-sector (SIC/NAICS codes as starting point, then refine)
- Business model similarity (asset-light vs asset-heavy, recurring vs transactional revenue)
- Geographic exposure (domestic vs international revenue mix)
- Size (enterprise value within 0.5x-2.0x of target, or revenue-based)
- Growth profile (revenue growth rate within similar band)
- Margin profile (EBITDA margin within comparable range)
- Capital structure (leverage ratios)

**Best practice:** Start with 15-25 candidates, narrow to 8-12 core peers. Include a "broader universe" for context.

**Common pitfalls:**
- Including conglomerates where the comparable segment is a small fraction
- Mixing high-growth SaaS companies with mature software businesses
- Ignoring geographic or regulatory differences that drive margin divergence

### Relevant Multiples by Sector

| Sector | Primary Multiples | Secondary Multiples |
|--------|-------------------|---------------------|
| Technology / SaaS | EV/Revenue, EV/ARR | EV/EBITDA, P/E, Rule of 40 |
| Industrials | EV/EBITDA | P/E, EV/EBIT |
| Financial Services | P/E, P/Book | ROE-adjusted P/B |
| Real Estate / REITs | P/FFO, P/AFFO | EV/EBITDA, NAV |
| Healthcare / Pharma | EV/EBITDA | EV/Revenue (pre-revenue biotech) |
| Retail / Consumer | EV/EBITDA | EV/Revenue, P/E |
| Energy / Mining | EV/EBITDA | EV/DACF, EV/2P reserves |
| Banks | P/E, P/TBV | Net interest margin, ROE |
| Insurance | P/E, P/Book | Combined ratio |
| Telecom | EV/EBITDA | EV/Subscriber, EV/Revenue |

### Calendarization

When peers have different fiscal year-ends, calendarize to a common period:

```
Calendarized Metric = (Stub Months / 12) × Next FY Estimate
                    + (Remaining Months / 12) × Current FY Estimate
```

**Example:** Target has Dec year-end. Peer has Mar year-end.
- For CY2025: 3/12 of FY Mar-2025 + 9/12 of FY Mar-2026

Always calendarize to the target's fiscal year-end or calendar year.

### Key Adjustments

**One-time / non-recurring items:**
- Restructuring charges
- Litigation settlements
- Asset impairments
- Gain/loss on asset sales
- Use "adjusted EBITDA" as reported by company, but verify adjustments are legitimate

**Stock-based compensation:**
- SBC is a real economic cost; preferred to use EBITDA less SBC for tech companies
- At minimum, show multiples both with and without SBC adjustment

**Operating lease adjustments (pre-IFRS 16):**
- Capitalize operating leases: add PV of lease commitments to EV, add back rent to EBITDA
- Post-IFRS 16/ASC 842: already on balance sheet, but be consistent across peers

**Pension adjustments:**
- Add unfunded pension obligations to enterprise value
- Ensure consistency across peer group

**Net debt calculation:**
```
Net Debt = Short-term Debt + Long-term Debt + Capital Leases
         + Preferred Stock + Minority Interest
         - Cash & Cash Equivalents
         - Short-term Investments (if liquid)
```

## Methodology

### Step-by-Step Trading Comps Process

1. **Select peer universe** — use criteria above, document rationale for inclusion/exclusion
2. **Gather financial data** — historical (LTM) and consensus estimates (NTM, NTM+1)
3. **Calendarize** — align all peers to common fiscal period
4. **Calculate enterprise value** — market cap + net debt + minority interest + preferred
5. **Compute multiples** — EV-based (EV/Revenue, EV/EBITDA, EV/EBIT) and equity-based (P/E, P/Book)
6. **Apply adjustments** — normalize for one-time items, SBC, lease treatment
7. **Analyze distribution** — mean, median, 25th/75th percentile
8. **Apply to target** — multiply target's metrics by selected multiple range
9. **Derive implied valuation range** — present as range, not point estimate

### Applying Multiples to Derive Valuation

```
Implied Enterprise Value = Target Metric × Selected Multiple

Example:
Target NTM EBITDA:     $150m
Peer Median EV/EBITDA: 12.0x
Peer 25th-75th:        10.5x - 13.5x

Implied EV Range:      $1,575m - $2,025m (median: $1,800m)
```

Then apply equity bridge (subtract net debt, minority interest, etc.) to arrive at equity value.

### Premium / Discount Considerations

Apply a premium or discount to peer multiples when target differs materially:
- **Growth premium:** Target grows faster than peers → justify higher multiple
- **Margin premium:** Target has structurally higher margins → higher multiple
- **Size discount:** Target is meaningfully smaller → lower multiple (illiquidity)
- **Geographic discount:** Target operates in higher-risk jurisdictions
- **Customer concentration discount:** Revenue concentrated in few customers

## Templates

### Trading Comps Table

```
=== COMPARABLE COMPANY ANALYSIS ===

Valuation Date: [Date]
Target Company: [Name]

--- Peer Group ---
Company          | EV ($m) | Rev ($m) | EBITDA ($m) | NTM Rev Gr | EBITDA Margin
Peer A           |  ____   |  ____    |    ____     |    ___%    |    ___%
Peer B           |  ____   |  ____    |    ____     |    ___%    |    ___%
Peer C           |  ____   |  ____    |    ____     |    ___%    |    ___%
...              |         |          |             |            |

--- Trading Multiples ---
Company          | EV/Rev LTM | EV/Rev NTM | EV/EBITDA LTM | EV/EBITDA NTM | P/E NTM
Peer A           |    ___x    |    ___x    |     ___x      |     ___x      |  ___x
Peer B           |    ___x    |    ___x    |     ___x      |     ___x      |  ___x
Peer C           |    ___x    |    ___x    |     ___x      |     ___x      |  ___x

Mean             |    ___x    |    ___x    |     ___x      |     ___x      |  ___x
Median           |    ___x    |    ___x    |     ___x      |     ___x      |  ___x
25th Percentile  |    ___x    |    ___x    |     ___x      |     ___x      |  ___x
75th Percentile  |    ___x    |    ___x    |     ___x      |     ___x      |  ___x

--- Implied Valuation ---
Metric Applied       | Target Value | Low Multiple | High Multiple | Low EV   | High EV
EV/EBITDA NTM        |    $____m    |    ___x      |     ___x      | $____m   | $____m
EV/Revenue NTM       |    $____m    |    ___x      |     ___x      | $____m   | $____m

Implied EV Range:    $____m - $____m
Less: Net Debt       ($____m)
Implied Equity:      $____m - $____m
Per Share:           $____ - $____
```

### Peer Selection Documentation

```
=== PEER GROUP RATIONALE ===

Included:
- [Peer A]: [Rationale — similar business model, size, geography]
- [Peer B]: [Rationale]

Excluded:
- [Company X]: [Reason — conglomerate, different growth profile, etc.]
- [Company Y]: [Reason]
```

## Quality Gate

Before finalizing a comparable analysis, verify:

- [ ] Peer group contains 8-12 companies with genuine business model similarity
- [ ] Financials are calendarized to a common period
- [ ] Enterprise value includes all non-equity claims (debt, minorities, preferred, pensions)
- [ ] Multiples are calculated on both LTM and NTM basis
- [ ] One-time items are adjusted consistently across all peers
- [ ] SBC treatment is consistent (either included or excluded for all peers)
- [ ] Outliers are identified and explained (do not silently exclude)
- [ ] NTM estimates use consensus from a reliable source (FactSet, Bloomberg, Capital IQ)
- [ ] Implied valuation is presented as a range, not a single point
- [ ] Premium/discount to peers is justified with specific operational differences
- [ ] Multiples are cross-checked for reasonableness given sector norms
- [ ] Diluted share count uses treasury stock method for target
