# Deferred Tax Accounting

name: deferred-taxes
description: Deferred tax accounting — temporary differences, DTA recognition. Cover temp vs permanent, DTA/DTL, tax loss carryforwards.

## When to Activate

- Identifying and measuring temporary differences between tax and accounting bases
- Recognizing deferred tax assets (DTA) and deferred tax liabilities (DTL)
- Assessing recoverability of deferred tax assets
- Accounting for tax loss carryforwards and tax credit carryforwards
- Distinguishing temporary from permanent differences
- Calculating the effective tax rate and reconciling to statutory rate
- Business combinations: deferred taxes arising from purchase price allocations
- Changes in tax rates: remeasuring deferred tax balances
- Intragroup transactions: deferred tax on unrealized profits
- Presenting and disclosing deferred taxes in financial statements

## Core Concepts

### Temporary vs Permanent Differences

**Temporary differences** — differences between the carrying amount of an asset or liability in the financial statements and its tax base that will reverse in future periods:

| Type | Example | Effect |
|------|---------|--------|
| Taxable temporary | Accelerated tax depreciation (tax base < book value) | DTL — tax paid later |
| Deductible temporary | Warranty provisions (tax base > book value) | DTA — tax saved later |
| Taxable temporary | Revenue recognized for tax before book (e.g., installment) | DTL |
| Deductible temporary | Impairment losses not yet tax-deductible | DTA |

**Permanent differences** — differences that will never reverse. No deferred tax is recognized:
- Tax-exempt income (e.g., municipal bond interest under US GAAP)
- Non-deductible expenses (e.g., certain fines, entertainment in some jurisdictions)
- Tax credits
- Participation exemption on dividends (many EU jurisdictions)

**Key distinction:** Temporary differences create deferred taxes; permanent differences affect only the effective tax rate.

### Deferred Tax Assets (DTA)

**Recognition:**
```
DTA arises from:
  - Deductible temporary differences
  - Tax loss carryforwards
  - Tax credit carryforwards

IAS 12 (IFRS):
  Recognize DTA to the extent that it is PROBABLE (> 50%) that
  future taxable profit will be available against which the
  deductible differences/losses can be utilized.

ASC 740 (US GAAP):
  Recognize DTA in full, then assess need for VALUATION ALLOWANCE.
  Reduce DTA by valuation allowance if it is MORE LIKELY THAN NOT
  (> 50%) that some or all of the DTA will NOT be realized.
```

**Evidence for DTA recoverability:**
- Future reversals of existing taxable temporary differences (most reliable)
- Projected future taxable income (requires forecasts — apply judgment)
- Tax planning strategies available and feasible
- Carryback potential (where tax law permits carryback of losses)
- History of taxable profits (pattern of losses weakens the case)

**Positive evidence (supports recognition):**
- Strong history of profitability
- Existing contracts or backlog generating future income
- Taxable temporary differences reversing in the same period as deductible differences
- Appreciated built-in gains in assets

**Negative evidence (weighs against recognition):**
- Cumulative losses in recent years (ASC 740: 3-year cumulative loss is significant negative evidence)
- History of tax loss carryforwards expiring unused
- Unsettled circumstances that may create losses
- Short carryforward periods with expiration risk

### Deferred Tax Liabilities (DTL)

**Recognition:** Generally recognize all DTLs. Limited exceptions:
- Initial recognition exception (IFRS only): Do not recognize DTL on initial recognition of goodwill, or on initial recognition of an asset/liability in a transaction that is not a business combination and affects neither accounting nor taxable profit
- Investments in subsidiaries/associates/JVs: Do not recognize DTL if the parent can control the timing of reversal AND reversal is not expected in the foreseeable future
- Undistributed profits: DTL required if distribution is probable (IFRS) or expected (US GAAP) and would trigger additional tax

### Tax Loss Carryforwards

```
=== TAX LOSS CARRYFORWARD ANALYSIS ===

Jurisdiction: __________    Statutory rate: ____%

Year of Origin | Loss Amount | Expiry Date | Utilized to Date | Remaining
---------------|-------------|-------------|------------------|----------
20X1           | _________   | __________  | _________        | _________
20X2           | _________   | __________  | _________        | _________
20X3           | _________   | __________  | _________        | _________
20X4           | _________   | __________  | _________        | _________
Total          | _________   |             | _________        | _________

DTA on carryforwards: Remaining x Tax Rate = _________
Valuation allowance / non-recognition:       (_________)
Net DTA recognized:                          _________

Utilization constraints:
[ ] Annual usage limit (e.g., Germany: only 60% of income above EUR 1M)
[ ] Minimum tax provisions
[ ] Change of ownership restrictions (e.g., Section 382 US, §8c KStG Germany)
[ ] Separate return limitation year (SRLY) rules
```

### Effective Tax Rate Reconciliation

```
=== EFFECTIVE TAX RATE RECONCILIATION ===

                                                    Amount       Rate
Pre-tax book income                                 _________
Statutory tax rate                                              ____%
Expected tax at statutory rate                      _________

Adjustments:
  + Non-deductible expenses                         _________   ____%
  - Tax-exempt income                               (_________)  ____%
  + Foreign rate differential                       _________   ____%
  - Tax credits                                     (_________)  ____%
  + Change in valuation allowance / non-recognition _________   ____%
  + Prior year adjustments                          _________   ____%
  + Rate change impact on deferred taxes            _________   ____%
  + Withholding taxes                               _________   ____%
  +/- Other                                         _________   ____%
Actual tax expense                                  _________
Effective tax rate                                              ____%
```

### Measurement

**Rate to apply:** Enacted (US GAAP) or substantively enacted (IFRS) tax rate expected to apply when the temporary difference reverses.

**Rate changes:** When tax rates change, remeasure all deferred tax balances at the new rate. Recognize the effect in:
- P&L: If the underlying transaction was recognized in P&L
- OCI: If the underlying transaction was in OCI
- Equity: If the underlying transaction was in equity

**Offsetting:** DTAs and DTLs are offset only when there is a legally enforceable right to offset current tax assets/liabilities AND the deferred taxes relate to the same taxable entity and same tax authority.

### Business Combinations

In a purchase price allocation (IFRS 3 / ASC 805):
- Recognize DTLs on fair value step-ups of acquired assets (book value for tax remains at historical cost, but accounting base is now at fair value — creating a taxable temporary difference)
- Recognize DTAs on acquired liabilities measured at fair value (e.g., unfavorable contracts, warranty obligations at fair value)
- Exception: No deferred tax on goodwill (under IFRS initial recognition exception)
- Deferred tax impacts can significantly increase or decrease goodwill

## Methodology

1. **Identify** all assets and liabilities with different carrying amounts for book and tax purposes
2. **Classify** each difference as temporary (reversible) or permanent
3. **Measure** deferred taxes at the expected reversal rate
4. **Assess** DTA recoverability (IFRS: probability test; US GAAP: valuation allowance)
5. **Present** current and deferred tax separately; offset only where permitted
6. **Reconcile** effective tax rate to statutory rate with clear explanation of each item
7. **Disclose** expiry dates of losses, unrecognized DTAs, and significant judgments

## Templates

### Deferred Tax Balance Sheet

```
=== DEFERRED TAX SCHEDULE ===

                                    Book Base    Tax Base    Temp Diff    Rate    DTA/(DTL)
Assets:
  Property, plant & equipment       _________    _________   _________   ___%    _________
  Intangible assets                 _________    _________   _________   ___%    _________
  Right-of-use assets               _________    _________   _________   ___%    _________
  Financial instruments at FV       _________    _________   _________   ___%    _________

Liabilities:
  Provisions (warranties, etc.)     _________    _________   _________   ___%    _________
  Lease liabilities                 _________    _________   _________   ___%    _________
  Pension obligations               _________    _________   _________   ___%    _________
  Accrued liabilities               _________    _________   _________   ___%    _________

Tax loss carryforwards              n/a          n/a         _________   ___%    _________
Tax credit carryforwards            n/a          n/a         _________   ___%    _________

Gross DTA                                                                        _________
Valuation allowance / non-recognition                                           (_________)
Net DTA                                                                          _________
DTL                                                                             (_________)
Net deferred tax position                                                        _________
```

## Quality Gate

- [ ] All temporary differences identified (including embedded ones like leases, pensions)
- [ ] Permanent differences correctly excluded from deferred tax calculation
- [ ] DTA recoverability assessed with documented positive and negative evidence
- [ ] Tax loss carryforwards tracked with expiry dates and utilization constraints
- [ ] Change-of-ownership limitations on loss usage evaluated (Section 382, §8c KStG)
- [ ] Tax rate used reflects enacted/substantively enacted rates at expected reversal date
- [ ] Rate change impact on deferred tax balances correctly recognized
- [ ] Offsetting applied only where legally enforceable right exists for same entity/authority
- [ ] ETR reconciliation prepared with clear explanation of each reconciling item
- [ ] Business combination deferred taxes properly calculated on PPA fair value adjustments
- [ ] Disclosure requirements met: nature of evidence supporting DTA, expiry, unrecognized amounts
