---
name: deal-structuring
description: 'name: deal-structuring'
---

# Deal Structuring

name: deal-structuring
description: M&A deal structuring — stock vs cash, earn-outs, tax considerations

## When to Activate

- User needs to evaluate deal consideration types (cash, stock, mixed)
- Performing accretion/dilution analysis on a proposed transaction
- Structuring earn-outs, escrow, or contingent consideration
- Analyzing tax implications of transaction structures
- Evaluating deal protection mechanisms or merger agreement terms

## Core Concepts

### Deal Consideration Types

**All-cash deal:**
- Certainty of value for target shareholders
- Acquirer bears all post-close risk
- Requires cash on hand, debt financing, or both
- Taxable event for target shareholders (capital gains)
- No dilution to acquirer's existing shareholders (but increases leverage)

**All-stock deal:**
- Target shareholders share in combined company's upside/downside
- Exchange ratio: fixed (set number of shares) or floating (fixed value)
- Potential for tax-free reorganization (Section 368)
- Dilutive to acquirer's existing shareholders
- Subject to market risk between signing and closing

**Mixed consideration (cash + stock):**
- Balances interests of both parties
- May offer election mechanism (shareholder choice, subject to proration)
- Partial tax deferral possible depending on structure

**Other consideration elements:**
- CVRs (Contingent Value Rights) — tradeable instruments tied to milestones
- Assumed debt — acquirer takes on target's existing obligations
- Rollover equity — target management reinvests portion of proceeds (common in PE deals)

### Accretion / Dilution Analysis

Determines whether a transaction is accretive (increases) or dilutive (decreases) to the acquirer's EPS.

```
Acquirer Standalone EPS:     $X.XX
Pro Forma Combined EPS:      $Y.YY
Accretion / (Dilution):      $(Y.YY - X.XX) = $Z.ZZ
Accretion / (Dilution) %:    Z.ZZ / X.XX = ___%
```

**Pro forma EPS calculation:**

```
Acquirer Net Income
+ Target Net Income
+ After-Tax Cost Synergies
- After-Tax Revenue Dis-synergies (if any)
- Incremental Interest Expense (on new debt, after tax)
+ Interest Income Foregone (on cash used, after tax) — negative
- Incremental D&A from Fair Value Step-Ups (after tax)
- Goodwill Amortization (if applicable under GAAP for private acquirers)
= Pro Forma Net Income

÷ Pro Forma Diluted Shares (acquirer shares + new shares issued)
= Pro Forma EPS
```

**Key drivers of accretion/dilution:**
- Relative P/E ratios: acquirer P/E > target P/E tends to be accretive (stock deal)
- Synergy magnitude and timing
- Cost of financing (interest rate on debt) vs target's earnings yield
- Purchase price premium

### Tax Structures

**Taxable transactions:**
- Asset purchase (buyer perspective): step-up in tax basis of acquired assets, creating future tax deductions (amortizable goodwill under Section 197 — 15 years)
- Stock purchase (no 338(h)(10) election): no asset step-up, carry-over tax basis
- Cash tender offer: generally taxable to target shareholders

**Tax-free reorganizations (Section 368):**
- Type A: Statutory merger — most flexible, allows up to 60% cash
- Type B: Stock-for-stock — must be 100% stock consideration
- Type C: Asset acquisition — substantially all assets for stock
- Requirements: continuity of interest, continuity of business enterprise, valid business purpose
- Benefit: target shareholders defer capital gains tax

**Section 338(h)(10) election:**
- Stock purchase treated as asset purchase for tax purposes
- Buyer gets asset step-up (tax shield via amortization)
- Seller treated as if assets were sold (may result in double tax for C-corps)
- Most beneficial for S-corps, partnerships, or subsidiaries

### Earn-Out Structures

Earn-outs bridge valuation gaps by making a portion of consideration contingent on future performance.

**Design parameters:**
```
Metric:          Revenue, EBITDA, gross profit, or specific milestones
Period:          1-3 years (longer periods create more friction)
Measurement:     Annual vs cumulative
Cap:             Maximum earn-out payable
Floor:           Minimum performance threshold before any payout
Acceleration:    Change of control triggers full payout
Dispute resolution: Independent accountant for financial metrics
```

**Common structures:**
- Linear: pro-rata payout between floor and cap
- Tiered: step-function payouts at defined thresholds
- Binary: all-or-nothing at a single milestone
- Hybrid: combination of financial and non-financial milestones

**Risks and mitigation:**
- Buyer manipulation: seller demands operational covenants (maintain sales force, R&D spending)
- Integration conflicts: earn-out period operations may conflict with integration plans
- Accounting: ASC 805 requires fair value estimation of contingent consideration at close

### Escrow and Indemnification

```
Escrow Amount:        Typically 5-15% of purchase price
Escrow Period:        12-24 months (longer for specific indemnities like tax)
Release:              Scheduled release or at expiry, less claims
R&W Insurance:        Increasingly common alternative to large escrow
Indemnification Cap:  Often 10-20% of purchase price (excluding fundamental reps)
Basket/Deductible:    0.5-1.0% of purchase price (tipping vs true deductible)
```

### Deal Protection Mechanisms

**Seller-favorable protections:**
- Go-shop period: 30-60 days post-signing to solicit competing bids
- Fiduciary out: board can terminate if superior proposal received
- Reverse break-up fee: acquirer pays if it fails to close (financing failure, regulatory block) — typically 3-6% of EV

**Buyer-favorable protections:**
- No-shop clause: target cannot solicit or engage with other bidders
- Break-up fee: target pays if it terminates to accept a superior offer — typically 2-4% of EV
- Matching rights: acquirer has right to match any superior proposal
- Force-the-vote: target must submit deal to shareholder vote even if board changes recommendation
- Lockup option: acquirer gets option to buy shares or assets at favorable price if deal breaks

### Material Adverse Change (MAC)

MAC clause allows the acquirer to terminate if the target experiences a material adverse change between signing and closing.

**Typically carved out (not considered MAC):**
- General economic or market conditions
- Industry-wide changes
- Changes in law or accounting standards
- Effects of the announced transaction itself
- Natural disasters, pandemics (increasingly carved out post-2020)

**MAC litigation is rare but high-stakes — courts apply a high bar (durationally significant impact on long-term earnings power).**

## Methodology

### Deal Structure Decision Framework

1. **Assess acquirer's capacity** — cash on hand, debt capacity, share price/currency strength
2. **Evaluate tax implications** — taxable vs tax-free for both buyer and seller
3. **Model accretion/dilution** — under cash, stock, and mixed scenarios
4. **Consider seller preferences** — tax deferral, continued upside participation, certainty
5. **Address valuation gaps** — earn-outs, CVRs if buyer and seller disagree on value
6. **Structure protections** — escrow, indemnification, MAC clause, deal protection
7. **Negotiate governance** — board seats, management retention, integration approach

## Templates

### Accretion / Dilution Summary

```
=== ACCRETION / DILUTION ANALYSIS ===

Transaction: [Acquirer] acquiring [Target]
Consideration: [Cash / Stock / Mixed]
Purchase Price: $____m (___x EV/EBITDA)

--- Pro Forma EPS Impact ---
                               | 100% Cash | 100% Stock | 50/50 Mix
Acquirer Standalone EPS        |   $____   |    $____   |   $____
Target Net Income              |   $____m  |    $____m  |   $____m
+ Cost Synergies (after-tax)   |   $____m  |    $____m  |   $____m
- Incremental Interest (a-t)   |  ($____m) |      —     |  ($____m)
- D&A Step-Up (after-tax)      |  ($____m) |   ($____m) |  ($____m)
Pro Forma Net Income           |   $____m  |    $____m  |   $____m
Pro Forma Shares               |   ____m   |    ____m   |   ____m
Pro Forma EPS                  |   $____   |    $____   |   $____
Accretion / (Dilution)         |   ____%   |    ____%   |   ____%

Break-even Synergies:          $____m pre-tax
```

### Earn-Out Term Sheet

```
=== EARN-OUT STRUCTURE ===

Metric:              [EBITDA / Revenue / Milestone]
Measurement Period:  Year 1: [Date] to [Date]
                     Year 2: [Date] to [Date]
Threshold (Floor):   $____m [Metric]
Target:              $____m [Metric]
Maximum (Cap):       $____m [Metric]

Payout Schedule:
- Below Floor:       $0
- At Threshold:      $____m
- At Target:         $____m
- At/Above Cap:      $____m (maximum)
- Linear interpolation between thresholds

Payment Form:        [Cash / Stock / Election]
Payment Timing:      Within 90 days of measurement period end
Dispute Resolution:  [Independent accounting firm]
Acceleration:        [Full payout on change of control]
```

## Quality Gate

Before finalizing deal structure analysis, verify:

- [ ] Accretion/dilution analysis covers all consideration scenarios (cash, stock, mixed)
- [ ] Tax structure is appropriate for both buyer and seller objectives
- [ ] Earn-out metrics are clearly measurable and not easily manipulated
- [ ] Escrow amount and period are within market norms for deal size
- [ ] Deal protection mechanisms are balanced and market-standard
- [ ] MAC clause carve-outs reflect current market practice
- [ ] Pro forma share count includes dilutive impact of new shares issued
- [ ] Synergy assumptions are phased realistically (not 100% in year 1)
- [ ] Interest rate assumptions on acquisition debt reflect current market
- [ ] Regulatory approval timeline is factored into the deal timeline
- [ ] Break-up fee and reverse break-up fee are within customary range (2-4%, 3-6%)
- [ ] Indemnification structure balances risk allocation between buyer and seller
- [ ] Accounting treatment (ASC 805/IFRS 3) for consideration is correctly modeled
