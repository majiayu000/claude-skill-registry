---
name: ifrs-standards
description: 'description: Key IFRS standards — IFRS 9, 15, 16, IAS 36, IFRS 3'
---

# IFRS Standards

name: ifrs-standards
description: Key IFRS standards — IFRS 9, 15, 16, IAS 36, IFRS 3

## When to Activate

- User asks about IFRS accounting treatment for revenue, leases, financial instruments, impairment, or business combinations
- Applying the IFRS 15 five-step revenue recognition model
- Accounting for leases under IFRS 16
- Classifying financial instruments under IFRS 9
- Performing impairment testing under IAS 36
- Purchase price allocation under IFRS 3

## Core Concepts

### IFRS 15 — Revenue from Contracts with Customers

IFRS 15 replaced IAS 18 and IAS 11 with a single, unified five-step model for all revenue recognition.

**Five-step model:**

1. **Identify the contract** — agreement creating enforceable rights/obligations; both parties approved; identifiable rights, payment terms, and commercial substance; collection is probable

2. **Identify performance obligations (POs)** — distinct goods or services promised. A good/service is distinct if the customer can benefit from it independently AND it is separately identifiable from other promises.

3. **Determine the transaction price** — amount of consideration expected. Includes:
   - Fixed consideration
   - Variable consideration (estimated using expected value or most likely amount; constrained to amounts where reversal is not probable)
   - Significant financing component (adjust if payment terms > 12 months)
   - Non-cash consideration (measured at fair value)
   - Consideration payable to a customer (reduce transaction price)

4. **Allocate the transaction price** — to each PO based on relative standalone selling prices (SSP). SSP estimation methods: adjusted market assessment, expected cost plus margin, residual approach (only if SSP is highly variable)

5. **Recognize revenue** — when (or as) each PO is satisfied. Over time if: customer simultaneously receives and consumes benefits; entity creates an asset with no alternative use and has right to payment for performance to date; or entity's performance creates/enhances a customer-controlled asset. Otherwise, at a point in time.

**Key judgments:**
- Identifying distinct POs (especially bundled software + services)
- Estimating variable consideration and applying the constraint
- Determining SSP for items not sold standalone
- Over time vs point in time recognition

### IFRS 16 — Leases

IFRS 16 eliminated the distinction between operating and finance leases for lessees. All leases (except short-term and low-value) go on balance sheet.

**Lessee accounting:**
```
At commencement:
  Right-of-Use (ROU) Asset = Lease Liability
                            + Lease payments made at/before commencement
                            + Initial direct costs
                            - Lease incentives received
                            + Estimated restoration costs

  Lease Liability = PV of future lease payments
                    (discounted at rate implicit in lease, or lessee's IBR)

Subsequent measurement:
  ROU Asset: depreciated over shorter of useful life and lease term (straight-line)
  Lease Liability: increased by interest, reduced by payments (effective interest method)

P&L Impact:
  Depreciation expense (from ROU asset) — in operating expenses
  Interest expense (on lease liability) — in finance costs
  Total expense is front-loaded (higher interest in early periods)
```

**Exemptions:**
- Short-term leases (term ≤ 12 months, no purchase option): expense straight-line
- Low-value assets (underlying asset value < ~$5,000 when new): expense straight-line

**Lease modifications:**
- Scope increase at standalone price: treat as separate lease
- Otherwise: remeasure lease liability using revised discount rate, adjust ROU asset

### IFRS 9 — Financial Instruments

**Classification of financial assets (based on business model + cash flow characteristics):**

| Category | Business Model | SPPI Test | Measurement |
|----------|---------------|-----------|-------------|
| Amortised cost | Hold to collect | Pass | Amortised cost |
| FVOCI | Hold to collect and sell | Pass | Fair value through OCI |
| FVTPL | Trading / other | Fail or irrevocable election | Fair value through P&L |

**SPPI test (Solely Payments of Principal and Interest):** Cash flows must represent only principal and interest on the outstanding amount. Instruments with leverage features, equity conversion, or non-standard interest generally fail.

**Expected Credit Loss (ECL) model:**
- Replaces the IAS 39 incurred loss model
- Requires forward-looking estimation of credit losses
- Three-stage model:
  - Stage 1: 12-month ECL (performing assets)
  - Stage 2: Lifetime ECL (significant increase in credit risk)
  - Stage 3: Lifetime ECL (credit-impaired — interest on net carrying amount)
- Simplified approach for trade receivables: always recognize lifetime ECL (provision matrix)

### IAS 36 — Impairment of Assets

**When to test:**
- Goodwill and indefinite-life intangibles: at least annually
- Other assets: when indicators of impairment exist (internal and external triggers)

**Impairment test:**
```
Carrying Amount vs Recoverable Amount

Recoverable Amount = higher of:
  (a) Fair Value Less Costs of Disposal (FVLCOD)
  (b) Value in Use (VIU) — PV of expected future cash flows

If Carrying Amount > Recoverable Amount → impairment loss recognized
```

**Cash-generating units (CGUs):**
- Test at CGU level when an asset does not generate independent cash flows
- Goodwill allocated to CGUs (or groups of CGUs) that benefit from the acquisition
- Impairment loss allocated: first to goodwill, then to other assets pro rata
- Goodwill impairment is never reversed; other asset impairments can be reversed

**Value in Use calculation:**
- Pre-tax cash flows using pre-tax discount rate (or post-tax/post-tax — must be consistent)
- Projection period: typically 5 years, then terminal value
- Growth rate for terminal value: must not exceed long-term average for the market/industry

### IFRS 3 — Business Combinations

**Acquisition method (mandatory):**
1. Identify the acquirer (who obtains control)
2. Determine the acquisition date
3. Recognize and measure identifiable assets, liabilities, and NCI at fair value
4. Recognize and measure goodwill (or bargain purchase gain)

**Goodwill calculation:**
```
Goodwill = Consideration transferred
         + NCI (at fair value or proportionate share of net assets)
         + Fair value of previously held equity interest (step acquisition)
         - Net identifiable assets at fair value (PPA)
```

**Purchase Price Allocation (PPA) — identifiable intangibles to consider:**
- Customer relationships (valued via multi-period excess earnings)
- Technology / patents (relief from royalty method)
- Trade names / brands (relief from royalty or with-and-without)
- Order backlog (excess earnings on contracted orders)
- Non-compete agreements (with-and-without method)
- Favorable contracts (differential cash flow method)

**Measurement period:** Up to 12 months from acquisition date to finalize PPA. Adjustments during measurement period are retrospective.

## Methodology

### Quick Reference by Standard

```
=== IFRS QUICK REFERENCE ===

Situation                          | Standard | Key Requirement
Revenue from product sales         | IFRS 15  | 5-step model, recognize at point in time
Revenue from long-term services    | IFRS 15  | Over-time recognition if criteria met
New lease signed                   | IFRS 16  | Recognize ROU asset and lease liability
Trade receivable collectibility    | IFRS 9   | Lifetime ECL using provision matrix
Goodwill on balance sheet          | IAS 36   | Annual impairment test at CGU level
Acquired a business                | IFRS 3   | PPA within 12 months, goodwill on BS
Investment in associate (20-50%)   | IAS 28   | Equity method
Foreign subsidiary translation    | IAS 21   | Functional currency, translate at closing rate
Provisions and contingencies       | IAS 37   | Recognize if probable and estimable
Employee benefits / pensions       | IAS 19   | Defined benefit: actuarial valuation
Segment reporting                  | IFRS 8   | Operating segments per management view
```

## Templates

### IFRS Compliance Checklist

```
=== IFRS COMPLIANCE CHECKLIST ===

Standard   | Area                    | Status | Notes
IFRS 15    | Revenue policy documented| [ ]   |
IFRS 15    | PO identification        | [ ]   |
IFRS 15    | SSP determined           | [ ]   |
IFRS 15    | Variable consideration   | [ ]   |
IFRS 16    | Lease inventory complete | [ ]   |
IFRS 16    | IBR determined           | [ ]   |
IFRS 16    | ROU assets recognized    | [ ]   |
IFRS 9     | Classification assessed  | [ ]   |
IFRS 9     | ECL provision computed   | [ ]   |
IAS 36     | CGU mapping done         | [ ]   |
IAS 36     | Annual impairment test   | [ ]   |
IFRS 3     | PPA completed (if M&A)   | [ ]   |
IFRS 3     | Goodwill allocated       | [ ]   |
```

### ECL Provision Matrix Template

```
=== EXPECTED CREDIT LOSS — PROVISION MATRIX ===

Aging Bucket       | Gross AR ($) | Historical Loss Rate | Forward-Looking Adj | ECL Rate | ECL ($)
Current (0-30d)    |    ____      |       ___%           |      ___%           |   ___%   |  ____
31-60 days         |    ____      |       ___%           |      ___%           |   ___%   |  ____
61-90 days         |    ____      |       ___%           |      ___%           |   ___%   |  ____
91-180 days        |    ____      |       ___%           |      ___%           |   ___%   |  ____
> 180 days         |    ____      |       ___%           |      ___%           |   ___%   |  ____
Total              |    ____      |                      |                     |          |  ____
```

## Quality Gate

Before finalizing IFRS-related accounting, verify:

- [ ] IFRS 15: all performance obligations are identified and distinct
- [ ] IFRS 15: SSP estimation method is documented and consistently applied
- [ ] IFRS 15: variable consideration is constrained appropriately
- [ ] IFRS 16: all leases are inventoried (including embedded leases in service contracts)
- [ ] IFRS 16: incremental borrowing rate is supportable and documented
- [ ] IFRS 16: short-term and low-value exemptions are applied consistently
- [ ] IFRS 9: financial assets are classified based on business model and SPPI test
- [ ] IFRS 9: ECL model uses forward-looking information (not just historical)
- [ ] IAS 36: CGU allocation of goodwill is documented and rational
- [ ] IAS 36: discount rate and growth rate assumptions are supportable
- [ ] IFRS 3: PPA identifies all separately recognizable intangible assets
- [ ] IFRS 3: measurement period adjustments are prospective only after 12 months
- [ ] Disclosure requirements for each standard are addressed in the notes
