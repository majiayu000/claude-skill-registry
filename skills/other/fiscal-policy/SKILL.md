# Fiscal Policy

name: fiscal-policy
description: Fiscal policy — spending, taxation, debt sustainability. Cover multipliers, automatic stabilizers, debt/GDP dynamics.

## When to Activate

- Analyzing the macroeconomic impact of government spending or taxation changes
- Estimating fiscal multipliers for different policy instruments
- Assessing debt sustainability and fiscal space
- Evaluating automatic stabilizers and their role in business cycle smoothing
- Modeling debt-to-GDP dynamics under different scenarios
- Analyzing fiscal consolidation strategies (austerity vs growth-friendly adjustment)
- Assessing the interaction between fiscal and monetary policy
- Evaluating sovereign creditworthiness from a fiscal perspective
- Comparing fiscal stances across countries or historical periods

## Core Concepts

### Fiscal Policy Instruments

**Spending instruments:**
- Government consumption (public sector wages, goods and services)
- Public investment (infrastructure, R&D, education capital)
- Transfer payments (social security, unemployment benefits, subsidies)
- Interest payments on public debt (non-discretionary)

**Revenue instruments:**
- Income taxes (personal and corporate)
- Consumption taxes (VAT, sales tax, excise duties)
- Social security contributions
- Property taxes, wealth taxes, capital gains taxes
- Non-tax revenue (fees, fines, state-owned enterprise dividends)

**Discretionary vs automatic:**
- Discretionary: Deliberate policy changes (new spending programs, tax rate changes)
- Automatic stabilizers: Revenue and spending that adjust automatically with the business cycle without new legislation

### Fiscal Multipliers

The fiscal multiplier measures how much GDP changes for each unit of fiscal stimulus or contraction:

```
Fiscal Multiplier = Change in GDP / Change in Government Spending (or Tax Revenue)

Spending multiplier (typical ranges):
  Government investment:        1.0 - 2.5  (highest — creates productive capacity)
  Government consumption:       0.6 - 1.5
  Transfers to low-income:      0.5 - 1.2  (high MPC of recipients)
  Transfers to high-income:     0.2 - 0.6  (lower MPC)

Tax multiplier (typical ranges):
  Income tax cuts:              0.3 - 1.0  (lower than spending — some is saved)
  Corporate tax cuts:           0.2 - 0.5  (uncertain investment response)
  Payroll tax cuts:             0.4 - 0.8  (directly affects take-home pay)
  Consumption tax cuts:         0.5 - 1.0  (depends on pass-through to prices)
```

**Factors that increase the multiplier:**
- Economy in recession (slack resources, zero lower bound on rates)
- Closed economy or large economy (less import leakage)
- Fixed exchange rate regime (monetary policy cannot offset)
- Spending targeted at high-MPC agents (liquidity-constrained households)
- Accommodative monetary policy (central bank does not offset stimulus)

**Factors that decrease the multiplier:**
- Economy at full employment (crowding out of private activity)
- Open, small economy (import leakage)
- Flexible exchange rate (monetary offset, exchange rate appreciation)
- High public debt (Ricardian equivalence concerns, risk premium)
- Spending on imports (leakage to foreign economies)

### Automatic Stabilizers

Mechanisms that automatically dampen business cycle fluctuations:

**Revenue side:**
- Progressive income tax: Tax revenue falls faster than income during recessions (and rises faster during expansions) because taxpayers move into lower/higher brackets
- Corporate tax: Profits are volatile; tax revenue falls sharply in downturns
- VAT/sales tax: Consumption declines → revenue declines (but less volatile than income tax)

**Spending side:**
- Unemployment insurance: Spending rises automatically when unemployment increases
- Social assistance/welfare: More claims during economic downturns
- Food stamps / housing benefits: Counter-cyclical by design

**Size of automatic stabilizers:**
- EU/Nordics: Large (comprehensive welfare state, progressive taxation) — stabilizers offset ~40-50% of GDP shock
- US: Moderate — stabilizers offset ~25-35% of GDP shock
- Emerging markets: Small — limited social safety nets, narrow tax bases

### Debt Sustainability Analysis

**Debt dynamics equation:**
```
Change in debt ratio = (r - g) / (1 + g) * d(t-1) + primary deficit

Where:
  d   = debt-to-GDP ratio
  r   = effective nominal interest rate on government debt
  g   = nominal GDP growth rate
  r-g = interest-growth differential (critical variable)

If r < g: Debt ratio stabilizes or declines even with moderate primary deficits
If r > g: Primary surplus required to stabilize the debt ratio

Primary surplus needed to stabilize debt:
  ps* = (r - g) / (1 + g) * d
```

**Debt sustainability indicators:**
| Indicator | Sustainable Range | Watch Level |
|-----------|------------------|-------------|
| Debt/GDP | < 60% (Maastricht) | > 90% |
| Primary balance/GDP | Surplus or small deficit | Deficit > 2% |
| Interest/Revenue | < 10% | > 15% |
| Gross financing needs/GDP | < 15% | > 20% |
| r - g differential | Negative | Positive and widening |

**Fiscal space:** The room a government has to increase spending or cut taxes without jeopardizing debt sustainability. Assessed through:
- Distance from debt limit (market tolerance, rating agency thresholds)
- Interest rate sensitivity of debt service
- Contingent liabilities (bank guarantees, SOE debt, pension obligations)
- Revenue mobilization potential (tax capacity vs actual collection)

### Fiscal Consolidation

**Approaches:**
- **Expenditure-based:** Cut spending (typically more successful historically). Focus on reducing transfers, public sector wages, and subsidies rather than investment.
- **Revenue-based:** Raise taxes. Less successful historically due to growth drag. More effective when broadening the base rather than raising rates.
- **Growth-friendly consolidation:** Cut unproductive spending and distortive taxes; protect public investment and education; reform pensions and social spending for long-term sustainability.

**Fiscal rules (EU framework):**
- Deficit limit: 3% of GDP (Stability and Growth Pact)
- Debt limit: 60% of GDP (with 1/20th annual reduction rule for excess)
- Structural balance: Close to balance or in surplus (medium-term objective)
- Expenditure benchmark: Growth of net primary expenditure ≤ potential GDP growth

## Methodology

1. **Fiscal stance assessment**: Calculate the structural (cyclically-adjusted) budget balance. Distinguish between discretionary policy changes and automatic stabilizer effects
2. **Multiplier estimation**: Select appropriate multiplier based on instrument, economic conditions, and country characteristics
3. **Debt dynamics projection**: Model debt/GDP trajectory under baseline and stress scenarios using the debt dynamics equation
4. **Sustainability assessment**: Evaluate r-g differential, gross financing needs, and fiscal space
5. **Policy simulation**: Estimate GDP and employment impact of proposed fiscal measures using multipliers and macro models
6. **Distributional analysis**: Assess who bears the burden of consolidation or benefits from stimulus

## Templates

### Fiscal Stance Dashboard

```
Country: __________    Year: __________

                                    Actual    Structural    Cyclical
Revenue (% GDP)                     ____%      ____%        ____%
Expenditure (% GDP)                 ____%      ____%        ____%
Budget balance (% GDP)              ____%      ____%        ____%
Primary balance (% GDP)             ____%      ____%        ____%

Debt/GDP:                           ____%
Interest payments/GDP:              ____%
Interest/Revenue:                   ____%
Gross financing needs/GDP:          ____%

Interest-growth differential (r-g): ____%
Primary surplus to stabilize debt:  ____%
Fiscal space assessment:            [ ] Ample  [ ] Moderate  [ ] Limited  [ ] Exhausted
```

### Debt Sustainability Scenario Analysis

```
=== DEBT/GDP PROJECTION ===

                    Base Case    Adverse (r+200bp)    Severe (r+200bp, g-2pp)
Year 0 (actual)     ____%            ____%                ____%
Year 1              ____%            ____%                ____%
Year 2              ____%            ____%                ____%
Year 3              ____%            ____%                ____%
Year 5              ____%            ____%                ____%
Year 10             ____%            ____%                ____%

Assumptions:
  Primary balance:        ____%    ____%                ____%
  Nominal growth (g):     ____%    ____%                ____%
  Effective interest (r): ____%    ____%                ____%
  r - g:                  ____%    ____%                ____%
```

## Quality Gate

- [ ] Structural balance calculated using appropriate output gap estimates
- [ ] Fiscal multiplier selection justified based on economic conditions and instrument type
- [ ] Debt dynamics equation correctly applied with consistent nominal/real rate treatment
- [ ] Interest-growth differential (r-g) assessed under baseline and stress scenarios
- [ ] Contingent liabilities and off-balance-sheet exposures identified
- [ ] Automatic stabilizer contribution separated from discretionary policy impact
- [ ] Fiscal rules compliance assessed (Maastricht, SGP, national rules)
- [ ] Gross financing needs projected including maturing debt rollover
- [ ] Distributional impact of fiscal measures considered
- [ ] Cross-country comparisons use consistent methodologies (IMF, OECD definitions)
