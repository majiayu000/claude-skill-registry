---
name: lease-accounting
description: 'name: lease-accounting'
---

# Lease Accounting

name: lease-accounting
description: Lease accounting — IFRS 16, ASC 842. Cover lessee model, operating vs finance, transition approaches.

## When to Activate

- Accounting for new leases under IFRS 16 or ASC 842
- Classifying leases as operating vs finance (ASC 842) or applying the single lessee model (IFRS 16)
- Calculating right-of-use (ROU) assets and lease liabilities at commencement
- Handling lease modifications, remeasurements, or terminations
- Transition from legacy standards (IAS 17 / ASC 840) to current standards
- Sale-and-leaseback transactions
- Short-term and low-value lease exemptions
- Lease vs. service contract determination
- Sublease accounting and classification

## Core Concepts

### IFRS 16 — Lessee Model (Single Model)

IFRS 16 requires lessees to recognize virtually all leases on the balance sheet. There is no operating/finance lease distinction for lessees.

**Initial recognition:**
```
Right-of-Use (ROU) Asset = Lease liability at commencement
                         + Lease payments made at or before commencement
                         + Initial direct costs incurred by lessee
                         - Lease incentives received
                         + Estimated dismantling/restoration costs (IAS 37)

Lease Liability = Present value of future lease payments
                  Discounted at the rate implicit in the lease (if determinable)
                  Otherwise, the lessee's incremental borrowing rate (IBR)

Lease payments included:
  - Fixed payments (less lease incentives receivable)
  - Variable payments based on an index or rate (e.g., CPI-linked)
  - Amounts expected to be payable under residual value guarantees
  - Exercise price of purchase option (if reasonably certain)
  - Penalties for terminating the lease (if term reflects exercise)
```

**Subsequent measurement:**
```
ROU Asset:
  - Cost model (default): Cost less accumulated depreciation less impairment
  - Depreciation: Shorter of useful life and lease term (straight-line unless
    another method better reflects pattern of consumption)
  - If ownership transfers or purchase option reasonably certain: depreciate
    over useful life of underlying asset

Lease Liability:
  - Increase by interest (effective interest method)
  - Decrease by lease payments made
  - Remeasure for changes in lease term, purchase option assessment,
    or variable payments linked to index/rate

P&L Impact:
  - Depreciation expense (in operating costs)
  - Interest expense (in finance costs)
  - Total expense is front-loaded (higher interest in early periods)
  - EBITDA improves compared to old operating lease treatment
```

**Exemptions (election available):**
- Short-term leases: Lease term ≤ 12 months at commencement (no purchase option). Expense straight-line. Election by class of underlying asset.
- Low-value assets: Underlying asset value when new ≤ approximately USD 5,000. Expense straight-line. Election on lease-by-lease basis.

### ASC 842 — Dual Model (Operating vs Finance)

ASC 842 retains the operating/finance lease distinction for lessees, unlike IFRS 16.

**Classification test — a lease is a finance lease if ANY of:**
1. Ownership transfers to lessee by end of lease term
2. Lessee has purchase option reasonably certain to be exercised
3. Lease term is for major part of remaining economic life (rule of thumb: ≥ 75%)
4. PV of lease payments is substantially all of fair value (rule of thumb: ≥ 90%)
5. Underlying asset is so specialized that it has no alternative use to lessor

If none of the above: operating lease.

**Finance lease (ASC 842):**
```
Balance sheet: ROU asset and lease liability (same as IFRS 16)
P&L: Amortization of ROU asset + Interest on lease liability (separately stated)
Cash flow: Principal portion in financing; interest in operating or financing
Pattern: Front-loaded total expense (same as IFRS 16)
```

**Operating lease (ASC 842):**
```
Balance sheet: ROU asset and lease liability recognized (on balance sheet — key change from ASC 840)
P&L: Single lease expense recognized on straight-line basis over lease term
Cash flow: All lease payments in operating activities
Pattern: Straight-line expense — ROU asset is a plug (liability reduction less interest equals ROU amortization)
```

### Key Differences: IFRS 16 vs ASC 842

| Feature | IFRS 16 | ASC 842 |
|---------|---------|---------|
| Lessee classification | Single model (all on balance sheet) | Dual model (operating vs finance) |
| P&L pattern (operating type) | Front-loaded (depreciation + interest) | Straight-line single lease expense |
| EBITDA impact | All leases improve EBITDA | Only finance leases improve EBITDA |
| Low-value exemption | Yes (≤ ~$5K) | No equivalent |
| Short-term exemption | Yes (≤ 12 months) | Yes (≤ 12 months, election by class) |
| Discount rate | Rate implicit or IBR | Rate implicit or IBR (non-public: risk-free rate option) |
| Remeasurement | Changes in index/rate trigger remeasurement | Variable payments based on index/rate excluded from liability |

### Incremental Borrowing Rate (IBR)

The IBR is the rate the lessee would have to pay to borrow on a similar secured basis over a similar term in a similar economic environment:

- Currency-specific: Match the currency of the lease payments
- Term-specific: Match the lease term, not the lessee's existing debt maturity
- Secured: Reflect collateral similar to the ROU asset
- Entity-specific: Reflect the lessee's credit standing
- Common approach: Start with the lessee's observable borrowing rate, adjust for term, security, and currency

### Lease Modifications

**IFRS 16 — modification is a separate lease if:**
- Scope increases (additional right of use) AND
- Consideration increases commensurate with standalone price

If not a separate lease: remeasure lease liability using revised discount rate; adjust ROU asset.

**ASC 842 — modification assessment:**
- Grants additional right of use not in original lease: may be separate contract
- Otherwise: reassess classification (finance vs operating) and remeasure

### Transition Approaches

**IFRS 16 transition from IAS 17:**
- Full retrospective: Restate comparatives as if IFRS 16 always applied
- Modified retrospective (most common): Recognize cumulative effect at transition date; no restatement of comparatives. Practical expedients available (e.g., use hindsight for lease term, apply single discount rate to portfolio)

**ASC 842 transition from ASC 840:**
- Modified retrospective at beginning of earliest period presented (or at adoption date with practical expedient)
- Practical expedient package: Do not reassess whether contracts contain leases, lease classification, or initial direct costs

### Sale-and-Leaseback

**Test for sale (IFRS 15 / ASC 606 criteria):**
- If transfer qualifies as a sale: seller-lessee derecognizes asset, recognizes ROU asset and lease liability. Gain/loss limited to the portion relating to rights transferred to buyer-lessor.
- If transfer does not qualify as a sale: treat as financing arrangement. Asset remains on seller's books; proceeds recognized as financial liability.

## Methodology

1. **Lease identification**: Determine whether a contract is or contains a lease (right to control use of identified asset for a period of time)
2. **Lease inventory**: Catalog all lease arrangements including embedded leases in service contracts
3. **Classification** (ASC 842): Apply the five-factor test for finance vs operating
4. **Measurement**: Determine lease term, lease payments, and discount rate
5. **Initial recognition**: Calculate ROU asset and lease liability
6. **Subsequent measurement**: Apply depreciation schedule and effective interest method
7. **Disclosure preparation**: Maturity analysis, weighted average remaining term, weighted average discount rate

## Templates

### Lease Calculation Worksheet

```
=== LEASE RECOGNITION WORKSHEET ===

Lease ID: ___________    Asset: ___________    Standard: [ ] IFRS 16  [ ] ASC 842
Commencement date: ___________    Lease term: ___ years
Classification (ASC 842 only): [ ] Finance  [ ] Operating

Lease Payments:
  Annual fixed payment:                    ___________
  Variable (index-linked, if applicable):  ___________
  Purchase option (if reasonably certain): ___________
  Residual value guarantee:                ___________
  Restoration cost estimate:               ___________

Discount Rate:
  Rate implicit in lease:                  ___________
  IBR (if implicit rate not determinable): ___________

INITIAL MEASUREMENT
  PV of lease payments (lease liability):  ___________
  + Payments at/before commencement:       ___________
  + Initial direct costs:                  ___________
  - Lease incentives received:             ___________
  + Restoration costs:                     ___________
  = ROU Asset at commencement:             ___________

AMORTIZATION SCHEDULE
Period | Opening Liability | Interest | Payment | Closing Liability | ROU Depreciation | ROU Carrying
-------|-------------------|----------|---------|-------------------|------------------|-------------
  1    |     _________     | ________ | _______ |     _________     |     ________     |   ________
  2    |     _________     | ________ | _______ |     _________     |     ________     |   ________
  ...  |     _________     | ________ | _______ |     _________     |     ________     |   ________
```

### Lease Portfolio Summary

```
=== LEASE PORTFOLIO SUMMARY ===

                           Number    ROU Asset    Lease Liability   Wtd Avg Term   Wtd Avg Rate
Real estate                 ____     _________     _________         ___ yrs        ___%
Vehicles                    ____     _________     _________         ___ yrs        ___%
Equipment                   ____     _________     _________         ___ yrs        ___%
IT / technology             ____     _________     _________         ___ yrs        ___%
Total                       ____     _________     _________         ___ yrs        ___%

Short-term lease expense:     _________
Low-value lease expense:      _________
Variable lease expense:       _________

Maturity Analysis (undiscounted):
  Year 1:     _________
  Year 2:     _________
  Year 3:     _________
  Year 4:     _________
  Year 5:     _________
  Beyond:     _________
  Total:      _________
  Less: discount   (_________)
  Lease liability: _________
```

## Quality Gate

- [ ] All contracts assessed for whether they contain a lease (control of identified asset)
- [ ] Lease term includes reasonably certain renewal and termination options
- [ ] Discount rate (IBR) is appropriately determined (currency, term, security, credit)
- [ ] ROU asset includes all required components (prepayments, initial direct costs, restoration)
- [ ] Lease incentives are deducted from the ROU asset, not recognized as separate income
- [ ] Short-term and low-value exemptions are applied consistently and by policy election
- [ ] ASC 842: Classification test properly applied; operating leases use straight-line P&L pattern
- [ ] IFRS 16: Front-loaded expense pattern acknowledged in financial projections
- [ ] Lease modifications assessed for separate lease treatment vs remeasurement
- [ ] Transition approach documented with all practical expedients elected clearly disclosed
- [ ] Disclosure requirements met: maturity analysis, weighted averages, variable lease expense
- [ ] Impact on financial covenants assessed (debt-like treatment of lease liabilities)
