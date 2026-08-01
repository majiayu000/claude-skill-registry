---
name: gaap-standards
description: 'description: Key US GAAP standards — ASC 606, 842, 350, 805'
---

# US GAAP Standards

name: gaap-standards
description: Key US GAAP standards — ASC 606, 842, 350, 805

## When to Activate

- User asks about US GAAP accounting treatment for revenue, leases, goodwill, or business combinations
- Applying ASC 606 revenue recognition
- Accounting for leases under ASC 842
- Goodwill and intangible asset impairment testing under ASC 350
- Purchase price allocation under ASC 805
- Income tax accounting under ASC 740
- Comparing IFRS vs US GAAP treatment

## Core Concepts

### ASC 606 — Revenue from Contracts with Customers

ASC 606 mirrors IFRS 15 with the same five-step model. Key differences from IFRS 15 are narrow but important.

**Five-step model (same as IFRS 15):**
1. Identify the contract
2. Identify performance obligations
3. Determine the transaction price
4. Allocate the transaction price to POs
5. Recognize revenue as POs are satisfied

**Key US GAAP-specific guidance:**
- **Licensing:** ASC 606 provides specific guidance for IP licenses — functional IP (recognized at a point in time) vs symbolic IP (recognized over time)
- **Contract costs:** ASC 340-40 requires capitalizing incremental costs of obtaining a contract (e.g., sales commissions) and amortizing over the benefit period
- **Disclosure:** Extensive disaggregation requirements (by geography, timing, type)

**Practical expedients:**
- Portfolio approach: apply to a portfolio of contracts with similar characteristics
- Significant financing component: ignore if payment expected within 1 year
- Shipping and handling: may treat as fulfillment activity (not separate PO)
- Completed contracts: no need to restate contracts completed before adoption

### ASC 842 — Leases

Unlike IFRS 16, ASC 842 retains a dual classification model for lessees.

**Classification test (any ONE triggers finance lease):**
1. Transfer of ownership at end of lease
2. Purchase option reasonably certain to be exercised
3. Lease term is major part (≥ 75% rule of thumb) of asset's economic life
4. PV of lease payments is substantially all (≥ 90% rule of thumb) of fair value
5. Asset is specialized with no alternative use to lessor

**Finance lease (formerly capital lease):**
```
Balance sheet: ROU asset + lease liability (same as IFRS 16)
P&L: Amortization of ROU asset (straight-line, in operating expense)
     + Interest on lease liability (front-loaded, in interest expense)
     = Total expense is front-loaded
Cash flow: Interest in operating; principal in financing
```

**Operating lease:**
```
Balance sheet: ROU asset + lease liability (same recognition as IFRS 16)
P&L: Single lease expense, recognized straight-line over lease term
     (allocated between amortization and interest for BS purposes,
      but reported as a single operating expense line)
     = Total expense is straight-line
Cash flow: All payments in operating activities
```

**Key difference from IFRS 16:** Operating leases under ASC 842 produce straight-line expense (not front-loaded). This affects EBITDA, operating income, and interest expense comparability.

### ASC 350 — Goodwill and Other Intangible Assets

**Goodwill impairment (simplified one-step test since ASU 2017-04):**

```
Step 1 (optional): Qualitative assessment — is it more likely than not (>50%)
that fair value of reporting unit < carrying amount? If no, stop — no impairment.

Step 2 (quantitative): Compare fair value of reporting unit to its carrying amount
(including goodwill).
  If FV < Carrying Amount → impairment loss = Carrying Amount - FV
  Impairment loss cannot exceed the goodwill allocated to that reporting unit.
```

**Key differences from IFRS (IAS 36):**
- US GAAP tests at the reporting unit level (one level below operating segment)
- IFRS tests at the CGU level (often smaller)
- US GAAP uses fair value; IFRS uses the higher of fair value less costs of disposal and value in use
- Under IFRS, goodwill impairment is never reversed; same under US GAAP
- US GAAP allows the qualitative assessment (Step 0); IFRS does not have an explicit qualitative screen

**Indefinite-lived intangible assets (e.g., trade names):**
- Annual impairment test: compare fair value to carrying amount
- If FV < carrying → impairment loss recognized
- Same qualitative assessment option available

**Finite-lived intangible assets:**
- Amortized over useful life
- Tested for impairment only when triggering events occur (ASC 360 two-step test)

### ASC 805 — Business Combinations

**Acquisition method (same framework as IFRS 3):**

```
Goodwill = Consideration transferred (FV)
         + NCI (at fair value or proportionate share — policy election per deal)
         - Net identifiable assets acquired at fair value
```

**Key US GAAP-specific differences from IFRS 3:**
- **Contingent consideration:** Both IFRS and US GAAP measure at fair value at acquisition. Subsequent remeasurement through P&L under both, but US GAAP has more detailed guidance on classification (liability vs equity).
- **In-process R&D:** Capitalized as an intangible asset (indefinite-lived until project completes or is abandoned); under IFRS 3, same treatment.
- **Bargain purchase:** Gain recognized in P&L immediately (IFRS 3: same, but reassess measurements first).
- **Measurement period:** Up to 1 year; adjustments are retrospective during the measurement period.

**Acquisition-related costs:** Expensed as incurred (not part of consideration). Same under IFRS 3.

### ASC 740 — Income Taxes

**Deferred tax framework:**
```
Temporary Difference = Book Basis of Asset/Liability - Tax Basis

If Book Basis of Asset > Tax Basis → Deferred Tax Liability (DTL)
If Book Basis of Asset < Tax Basis → Deferred Tax Asset (DTA)
(Reverse for liabilities)
```

**DTA recognition:**
- US GAAP: recognize DTA in full, then assess need for a valuation allowance
- Valuation allowance if "more likely than not" (>50%) that some/all DTA will not be realized
- Sources of taxable income to support DTA: reversing DTLs, future taxable income, tax planning strategies, carryback availability

**Key differences from IFRS (IAS 12):**
- IFRS recognizes DTA only to the extent it is "probable" that taxable profit will be available (no valuation allowance concept)
- US GAAP recognizes full DTA then assesses valuation allowance (gross-up approach)
- US GAAP prohibits discounting deferred taxes; IFRS also prohibits discounting
- US GAAP uses enacted tax rates; IFRS uses enacted or substantively enacted rates

**Tax rate reconciliation:**
```
Statutory Rate                          ___%
+ State taxes (net of federal benefit)  ___%
+ Non-deductible expenses               ___%
- Tax-exempt income                    (__%)
+ Foreign rate differential             ___%
+ Valuation allowance change            ___%
+ Other                                 ___%
= Effective Tax Rate                    ___%
```

## Methodology

### IFRS vs US GAAP Key Differences Summary

| Topic | US GAAP | IFRS |
|-------|---------|------|
| Revenue (general) | ASC 606 | IFRS 15 — largely converged |
| Leases (lessee) | ASC 842: dual model (operating + finance) | IFRS 16: single model (all on BS, front-loaded) |
| Goodwill impairment | One-step quantitative (or qualitative screen) | Higher of FVLCOD and VIU at CGU level |
| Inventory | LIFO permitted | LIFO prohibited |
| Development costs | Expensed (except software under ASC 985/350) | Capitalized if criteria met (IAS 38) |
| Extraordinary items | Prohibited (since ASU 2015-01) | Prohibited (IAS 1) |
| Deferred tax — DTA | Full recognition + valuation allowance | Recognize only if probable |
| Revaluation of PP&E | Not permitted (cost model only) | Permitted (revaluation model, IAS 16) |
| Contingencies | ASC 450: probable + estimable → accrue | IAS 37: probable (>50%) + reliable estimate → provision |
| Business combinations | ASC 805 | IFRS 3 — largely converged |

### Common US GAAP Pitfalls

- Forgetting to capitalize contract costs (ASC 340-40) — commissions on multi-year deals
- Misclassifying operating vs finance leases — the 75%/90% bright lines are guidelines, not absolute rules
- Not testing goodwill at the correct reporting unit level
- Ignoring the requirement for a valuation allowance assessment each period
- Inconsistent treatment of SBC in adjusted/non-GAAP metrics (SEC scrutiny)

## Templates

### US GAAP Compliance Checklist

```
=== US GAAP COMPLIANCE CHECKLIST ===

Standard   | Area                           | Status | Notes
ASC 606    | Revenue policy documented      | [ ]    |
ASC 606    | PO identification              | [ ]    |
ASC 606    | Contract cost capitalization    | [ ]    |
ASC 842    | Lease classification assessed   | [ ]    |
ASC 842    | ROU assets/liabilities on BS    | [ ]    |
ASC 842    | Discount rate documented        | [ ]    |
ASC 350    | Reporting units defined         | [ ]    |
ASC 350    | Annual goodwill impairment test | [ ]    |
ASC 350    | Indefinite-lived intangibles    | [ ]    |
ASC 805    | PPA completed within 1 year     | [ ]    |
ASC 805    | Contingent consideration FV     | [ ]    |
ASC 740    | DTA valuation allowance         | [ ]    |
ASC 740    | Rate reconciliation             | [ ]    |
ASC 740    | Uncertain tax positions (FIN 48)| [ ]    |
```

### Lease Classification Decision Tree

```
=== ASC 842 LEASE CLASSIFICATION ===

Does ownership transfer to lessee? → YES → Finance Lease
                                    → NO ↓
Is there a bargain purchase option? → YES → Finance Lease
                                    → NO ↓
Is lease term ≥ 75% of economic life? → YES → Finance Lease
                                       → NO ↓
Is PV of payments ≥ 90% of FV?    → YES → Finance Lease
                                    → NO ↓
Is asset specialized?              → YES → Finance Lease
                                    → NO → Operating Lease
```

## Quality Gate

Before finalizing US GAAP accounting, verify:

- [ ] ASC 606: performance obligations are identified with documented basis for distinct/not distinct
- [ ] ASC 606: SSP estimates are supportable and consistent period-over-period
- [ ] ASC 606: contract costs (commissions) are capitalized and amortized per ASC 340-40
- [ ] ASC 842: lease classification (operating vs finance) is documented with quantitative support
- [ ] ASC 842: all leases are on balance sheet (ROU asset and lease liability)
- [ ] ASC 842: discount rate uses rate implicit in lease or IBR (not generic benchmark)
- [ ] ASC 350: goodwill is allocated to reporting units and tested annually
- [ ] ASC 350: triggering events are monitored between annual tests
- [ ] ASC 805: all identifiable intangibles are separately recognized in PPA
- [ ] ASC 805: acquisition costs are expensed, not capitalized
- [ ] ASC 740: valuation allowance is assessed each reporting period
- [ ] ASC 740: uncertain tax positions are evaluated under the two-step process (FIN 48)
- [ ] All non-GAAP measures reconcile to the nearest GAAP measure (SEC compliance)
