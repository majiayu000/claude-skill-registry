---
name: Valuation Analyst
slug: valuation-analyst
description: Perform company and asset valuations using DCF, comparables, precedent transactions, and other methodologies
category: finance
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "valuation analysis"
  - "company valuation"
  - "DCF model"
  - "comparable analysis"
  - "enterprise value"
  - "fair value"
tags:
  - valuation
  - dcf
  - comparables
  - m-and-a
  - enterprise-value
---

# Valuation Analyst

Expert valuation agent that determines fair value of companies and assets using multiple methodologies. Specializes in DCF analysis, comparable company analysis, precedent transactions, and asset-based valuation. Provides comprehensive valuation for investment decisions, M&A, and strategic planning.

This skill applies rigorous valuation frameworks used by investment banks, private equity firms, and corporate finance professionals. Perfect for startup valuations, M&A analysis, investment decisions, and fairness opinions.

## Core Workflows

### Workflow 1: Discounted Cash Flow (DCF) Valuation

**Objective:** Value company based on projected future cash flows

**Steps:**
1. **Financial Projections (5-10 years)**
   - **Revenue Projections:**
     - Historical growth analysis
     - Market size and share
     - Segment-level forecasts
     - Growth rate deceleration

   - **Profitability Projections:**
     - Gross margin trends
     - Operating margin expansion
     - SG&A leverage
     - Target margins at maturity

   - **Capital Requirements:**
     - CapEx as % of revenue
     - Working capital changes
     - D&A schedule

2. **Free Cash Flow Calculation**
   ```
   EBIT (Earnings Before Interest & Taxes)
   - Taxes (EBIT × Tax Rate)
   = NOPAT (Net Operating Profit After Tax)
   + Depreciation & Amortization
   - Capital Expenditures
   - Change in Working Capital
   = Unlevered Free Cash Flow (UFCF)
   ```

3. **Discount Rate (WACC)**
   - **Cost of Equity (CAPM):**
     ```
     Ke = Rf + β × (Rm - Rf)

     Where:
     Rf = Risk-free rate (10-year Treasury)
     β = Levered beta
     Rm - Rf = Equity risk premium (5-7%)

     For private companies, add size premium (2-6%)
     ```

   - **Cost of Debt:**
     ```
     Kd = Interest Rate × (1 - Tax Rate)
     ```

   - **WACC Calculation:**
     ```
     WACC = (E/V × Ke) + (D/V × Kd)

     E = Market value of equity
     D = Market value of debt
     V = E + D
     ```

4. **Terminal Value**
   - **Perpetuity Growth Method:**
     ```
     TV = FCF(final year) × (1 + g) / (WACC - g)

     g = Terminal growth rate (typically 2-3%)
     ```

   - **Exit Multiple Method:**
     ```
     TV = EBITDA(final year) × Exit Multiple

     Exit multiple based on comparables
     ```

5. **Enterprise Value Calculation**
   ```
   Enterprise Value = Σ(FCF / (1 + WACC)^t) + TV / (1 + WACC)^n

   t = year number
   n = final projection year
   ```

6. **Equity Value Bridge**
   ```
   Enterprise Value
   - Total Debt
   - Preferred Stock
   - Minority Interest
   + Cash & Equivalents
   + Non-operating Assets
   = Equity Value

   Per Share Value = Equity Value / Diluted Shares
   ```

7. **Sensitivity Analysis**
   - WACC vs Terminal Growth matrix
   - Revenue growth sensitivity
   - Margin sensitivity
   - Multiple sensitivity

**Deliverable:** DCF valuation with sensitivity tables

### Workflow 2: Comparable Company Analysis

**Objective:** Value company using trading multiples of similar public companies

**Steps:**
1. **Select Comparable Companies**
   - Same industry/sector
   - Similar business model
   - Comparable size (revenue, market cap)
   - Similar growth profile
   - Geographic relevance
   - Minimum 5-7 comps preferred

2. **Gather Market Data**
   - Stock price (current)
   - Shares outstanding (diluted)
   - Market capitalization
   - Total debt
   - Cash and equivalents
   - Minority interest

3. **Calculate Enterprise Value**
   ```
   Market Cap = Share Price × Diluted Shares

   Enterprise Value = Market Cap + Debt - Cash + Minority Interest
   ```

4. **Gather Financial Metrics**
   - LTM (Last Twelve Months):
     - Revenue
     - EBITDA
     - EBIT
     - Net Income
     - EPS

   - NTM (Next Twelve Months) estimates:
     - Revenue
     - EBITDA
     - EPS

5. **Calculate Trading Multiples**
   | Multiple | Formula | When to Use |
   |----------|---------|-------------|
   | EV/Revenue | EV / Revenue | High growth, negative EBITDA |
   | EV/EBITDA | EV / EBITDA | Most common, capital intensive |
   | EV/EBIT | EV / EBIT | D&A differs materially |
   | P/E | Price / EPS | Mature, profitable |
   | P/B | Price / Book | Financial institutions |
   | PEG | P/E / Growth | Growth-adjusted comparison |

6. **Analyze and Select Multiples**
   - Calculate mean, median, range
   - Identify outliers
   - Consider premium/discount factors
   - Select appropriate multiple range

7. **Apply to Target Company**
   ```
   Enterprise Value = Target Metric × Selected Multiple

   Example:
   Target EBITDA = $50M
   Median EV/EBITDA = 12.0x
   Implied EV = $600M
   ```

8. **Valuation Range**
   - Low (25th percentile multiple)
   - Mid (median multiple)
   - High (75th percentile multiple)

**Deliverable:** Comparable company analysis with valuation range

### Workflow 3: Precedent Transaction Analysis

**Objective:** Value company using M&A transaction multiples

**Steps:**
1. **Identify Relevant Transactions**
   - Same industry
   - Similar deal size
   - Recent (last 3-5 years)
   - Similar deal structure
   - Minimum 5-7 transactions

2. **Gather Transaction Details**
   - Announcement date
   - Acquirer and target
   - Deal value
   - Deal structure (stock/cash)
   - Strategic vs financial buyer
   - Control premium paid

3. **Calculate Transaction Multiples**
   - EV/Revenue at time of deal
   - EV/EBITDA at time of deal
   - EV/EBIT at time of deal
   - Premium to trading price

4. **Adjust for Context**
   - Market conditions at time of deal
   - Synergy expectations
   - Competitive bidding situation
   - Distressed vs strategic deals

5. **Apply to Target**
   ```
   Transaction EV = Target Metric × Transaction Multiple
   ```

6. **Consider Control Premium**
   - Typical premium: 20-40% over trading
   - Adjust for minority vs control stakes
   - Strategic vs financial buyers

**Deliverable:** Precedent transaction analysis with implied value range

### Workflow 4: Startup/Private Company Valuation

**Objective:** Value early-stage or private company

**Steps:**
1. **Valuation Method Selection**

   | Stage | Primary Methods |
   |-------|-----------------|
   | Pre-revenue | Scorecard, Berkus, Risk Factor |
   | Early revenue | Revenue multiples, DCF (if possible) |
   | Growth stage | Revenue multiples, DCF |
   | Late stage | DCF, comps, precedent transactions |

2. **Revenue Multiple Approach**
   - **Select Comparable Multiples:**
     - Public SaaS: 5-15x revenue
     - Marketplace: 1-5x GMV, 5-15x revenue
     - E-commerce: 0.5-2x revenue

   - **Apply Discount:**
     - Illiquidity discount: 20-35%
     - Size discount: 10-30%
     - Stage discount: varies

   - **Calculation:**
     ```
     Value = Revenue × Multiple × (1 - Discounts)
     ```

3. **Venture Capital Method**
   ```
   Exit Value = Projected Revenue × Exit Multiple
   Pre-money Value = Exit Value / Target Return

   Example:
   Year 5 Revenue = $100M
   Exit Multiple = 6x
   Exit Value = $600M
   Target Return = 10x
   Current Value = $60M
   ```

4. **Scorecard Method (Pre-revenue)**
   - Average pre-money for stage/region
   - Score on factors (±50%):
     - Team strength
     - Market opportunity
     - Product/technology
     - Competitive environment
     - Partnerships
     - Need for financing
   - Multiply base by weighted factors

5. **Cap Table Implications**
   - Pre-money vs post-money
   - Dilution calculation
   - Option pool sizing
   - Liquidation preferences

**Deliverable:** Private company valuation with methodology explanation

### Workflow 5: Sum-of-the-Parts (SOTP) Valuation

**Objective:** Value multi-segment company by valuing each segment separately

**Steps:**
1. **Segment Identification**
   - Business segments from filings
   - Geographic segments
   - Product line segments
   - Operational vs non-operating assets

2. **Segment Financial Separation**
   - Segment revenue
   - Segment EBITDA
   - Segment assets
   - Corporate overhead allocation

3. **Segment Valuation**
   - Value each segment using appropriate method:
     - Growth segment: Revenue multiple or DCF
     - Mature segment: EBITDA multiple
     - Asset-heavy: Asset-based
   - Use segment-specific comparables

4. **Corporate Adjustments**
   - Corporate overhead (capitalize as liability)
   - Shared services
   - Intercompany eliminations
   - Net debt allocation

5. **Sum of Parts**
   ```
   Segment A Value: $X
   + Segment B Value: $Y
   + Segment C Value: $Z
   - Corporate Overhead Value: ($W)
   - Net Debt: ($D)
   = Total Equity Value
   ```

6. **Conglomerate Discount**
   - Typical discount: 10-25%
   - Reasons: complexity, capital allocation
   - Consider break-up value

**Deliverable:** SOTP valuation with segment breakdown

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| DCF valuation | "Perform DCF analysis" |
| Comparables | "Value using comparable companies" |
| Transactions | "Analyze precedent transactions" |
| Startup value | "Value this startup" |
| SOTP | "Sum-of-the-parts valuation" |
| Full analysis | "Complete valuation analysis" |

## Valuation Multiples Reference

### By Industry (EV/EBITDA Ranges)

| Industry | Range | Notes |
|----------|-------|-------|
| Software/SaaS | 15-30x | Revenue multiples also common |
| Healthcare | 10-15x | Varies by sub-sector |
| Consumer Retail | 6-10x | Location matters |
| Manufacturing | 6-10x | Asset intensity varies |
| Financial Services | P/B or P/E | Book value focus |
| Energy | 4-8x | Commodity sensitive |
| Real Estate | Cap rate | NOI based |
| Media | 8-15x | Content value matters |

### SaaS Revenue Multiples

| Growth Rate | ARR Multiple |
|-------------|--------------|
| < 20% | 3-6x |
| 20-40% | 6-10x |
| 40-60% | 10-15x |
| 60-100% | 15-25x |
| > 100% | 25x+ |

### Common Adjustments

| Adjustment | Application |
|------------|-------------|
| Illiquidity discount | Private companies (20-35%) |
| Control premium | Acquisitions (20-40%) |
| Size premium | Small companies (add to WACC) |
| Country risk | Emerging markets (add to WACC) |
| Minority discount | Non-control stakes (15-30%) |

## DCF Template

```markdown
# DCF Valuation: [Company Name]

## Assumptions
| Input | Value | Source |
|-------|-------|--------|
| Risk-free Rate | % | 10-yr Treasury |
| Equity Risk Premium | % | Market |
| Beta (Levered) | | Comparable |
| Cost of Debt | % | Current rate |
| Tax Rate | % | Statutory |
| D/E Ratio | % | Target |
| Terminal Growth | % | GDP proxy |

## WACC Calculation
Cost of Equity: %
Cost of Debt (after-tax): %
WACC: %

## Projections ($M)
| | Y1 | Y2 | Y3 | Y4 | Y5 | Terminal |
|-|----|----|----|----|----| ---------|
| Revenue | | | | | | |
| EBITDA | | | | | | |
| EBIT | | | | | | |
| Taxes | | | | | | |
| NOPAT | | | | | | |
| + D&A | | | | | | |
| - CapEx | | | | | | |
| - Δ WC | | | | | | |
| FCF | | | | | | |
| Discount Factor | | | | | | |
| PV of FCF | | | | | | |

## Valuation Summary
Sum of PV of FCF: $
Terminal Value: $
PV of Terminal Value: $
Enterprise Value: $
- Net Debt: $
Equity Value: $
Shares Outstanding:
Value per Share: $

## Sensitivity Analysis
[WACC vs Terminal Growth matrix]
```

## Best Practices

### Methodology Selection
- Use multiple methods for triangulation
- Weight methods by applicability
- Consider data availability
- Match to purpose (minority, control, etc.)

### Assumption Setting
- Ground assumptions in data
- Be explicit about sources
- Test sensitivity
- Document reasoning

### Presentation
- Show range, not point estimate
- Include key assumptions
- Provide sensitivity analysis
- Compare methods

## Integration with Other Skills

- **Use with `financial-analyst`:** Financial statement analysis
- **Use with `investment-analyzer`:** Investment decision support
- **Use with `revenue-modeler`:** Revenue projection inputs
- **Use with `contract-analyzer`:** Deal term analysis
- **Use with `compliance-checker`:** Regulatory considerations

## Common Pitfalls to Avoid

- **Single methodology:** Use multiple approaches
- **Circular references:** WACC and capital structure
- **Terminal value dominance:** Should be < 75% of value
- **Hockey stick projections:** Reality check growth rates
- **Ignoring working capital:** Significant for many businesses
- **Wrong peer selection:** Comparability matters
- **Stale data:** Use current market data
- **Overcomplication:** Simpler models often more reliable
