# Labor Market Economics

name: labor-markets
description: Labor market economics — unemployment, wages, Phillips Curve. Cover NAIRU, Phillips Curve, Okun's law.

## When to Activate

- Analyzing unemployment dynamics (structural, cyclical, frictional)
- Estimating the NAIRU and its implications for monetary policy
- Applying the Phillips Curve to assess inflation-unemployment trade-offs
- Using Okun's Law to relate output gaps to unemployment
- Evaluating wage growth dynamics and labor share of income
- Assessing labor market tightness and its implications for inflation
- Analyzing minimum wage effects on employment and welfare
- Evaluating labor market policies (active vs passive measures)
- Comparing labor market institutions across countries

## Core Concepts

### Types of Unemployment

| Type | Definition | Duration | Policy Response |
|------|-----------|----------|----------------|
| Frictional | Workers transitioning between jobs; normal search process | Short-term | Improve information, matching platforms |
| Structural | Mismatch between worker skills and job requirements | Long-term | Retraining, education, relocation support |
| Cyclical | Demand-deficient unemployment during recessions | Varies with cycle | Fiscal/monetary stimulus |
| Seasonal | Predictable fluctuations (tourism, agriculture, construction) | Recurring | Seasonal adjustment in data |

**Measurement:**
```
Unemployment rate = Unemployed / Labor Force x 100%
Labor force = Employed + Unemployed (actively seeking work)
Participation rate = Labor Force / Working-age Population x 100%
Employment rate = Employed / Working-age Population x 100%

Broader measures:
  U-3: Official unemployment rate (ILO definition)
  U-6: Includes marginally attached workers and involuntary part-time
       (better measure of labor market slack)

Beveridge Curve: Relationship between vacancy rate and unemployment rate
  - Outward shift = increased mismatch (structural unemployment rising)
  - Movement along curve = cyclical changes
```

### NAIRU (Non-Accelerating Inflation Rate of Unemployment)

The unemployment rate consistent with stable inflation. Below NAIRU, inflation accelerates; above NAIRU, inflation decelerates.

```
NAIRU estimation approaches:
  1. Phillips Curve estimation: Extract NAIRU as the unemployment rate
     where inflation is stable (inflation expectations = actual inflation)
  2. Kalman filter / state-space models: Estimate time-varying NAIRU
  3. Structural models: Based on wage-setting and price-setting equations
  4. Reduced-form: HP filter or similar statistical decomposition

Typical NAIRU estimates (as of mid-2020s):
  US:          ~4.0-4.5%
  Eurozone:    ~6.5-7.0%
  Germany:     ~3.0-3.5%
  UK:          ~4.0-4.5%
  Japan:       ~2.5-3.0%

NAIRU is NOT constant — it shifts due to:
  - Labor market reforms (flexibility, matching efficiency)
  - Demographic changes (aging workforce)
  - Globalization and trade openness
  - Hysteresis effects (prolonged unemployment raises NAIRU)
  - Technology and automation
```

**Policy significance:** Central banks use NAIRU estimates to gauge labor market slack and calibrate monetary policy. If unemployment < NAIRU, expect inflationary pressure. Wide uncertainty bands around NAIRU estimates limit its precision as a policy guide.

### Phillips Curve

**Original Phillips Curve (1958):** Negative relationship between wage growth and unemployment.

**Expectations-Augmented Phillips Curve (Friedman-Phelps):**
```
pi = pi_e - beta * (u - u*) + supply_shock

pi     = actual inflation
pi_e   = expected inflation
u      = actual unemployment rate
u*     = NAIRU
beta   = slope parameter (sensitivity of inflation to unemployment gap)
supply_shock = cost-push factors (oil prices, exchange rate, etc.)

When u < u*: inflation exceeds expectations (economy overheating)
When u > u*: inflation falls below expectations (slack in economy)
When u = u*: inflation equals expectations (stable)
```

**New Keynesian Phillips Curve:**
```
pi_t = beta * E[pi_t+1] + kappa * x_t

pi_t      = current inflation
E[pi_t+1] = expected future inflation (forward-looking)
x_t       = output gap (or real marginal cost)
kappa     = slope (sensitivity to the output gap)

Key feature: Forward-looking expectations (rational expectations),
not backward-looking (adaptive expectations)
```

**Phillips Curve flattening:** Since the 1990s, the Phillips Curve has appeared flatter in many economies — inflation is less responsive to unemployment changes. Explanations:
- Better-anchored inflation expectations
- Globalization (global slack matters, not just domestic)
- Gig economy and labor market flexibility
- Measurement issues (output gap uncertainty)
- Non-linear: Curve may steepen at very low unemployment rates

### Okun's Law

**Relationship between output gap and unemployment gap:**
```
u - u* = -beta * (Y - Y*) / Y*

Typical beta: ~0.4-0.5 for the US
  → A 1 percentage point increase in unemployment corresponds to
    roughly 2-2.5% decline in GDP relative to potential

Alternative (growth rate form):
  Change in u = -beta * (g - g*)

  g   = actual GDP growth
  g*  = potential GDP growth (typically ~2% for advanced economies)
  beta = ~0.4-0.5

  → If GDP growth is 1pp below potential, unemployment rises ~0.4-0.5pp
```

**Limitations:**
- Relationship varies across countries (labor market flexibility matters)
- Asymmetric: Unemployment rises faster in downturns than it falls in recoveries
- Structural breaks possible (post-crisis periods may shift the relationship)
- Labor hoarding in some countries dampens the response

### Wage Determination

**Wage-setting frameworks:**
- **Marginal productivity theory:** Wages = marginal product of labor in competitive markets
- **Efficiency wages:** Firms pay above market-clearing wages to reduce turnover, increase effort, and attract better workers
- **Insider-outsider theory:** Employed workers (insiders) have bargaining power; unemployed (outsiders) cannot underbid them due to hiring/firing costs
- **Collective bargaining:** Wages set through negotiations between unions and employers. Wage outcomes depend on union density, bargaining coverage, and coordination

**Wage Phillips Curve:**
```
Nominal wage growth = Inflation expectations + Productivity growth - beta * (u - u*)

Real wage growth should track productivity growth in equilibrium.
If real wages grow faster than productivity → unit labor costs rise → inflationary
If real wages grow slower than productivity → labor share of income falls
```

**Labor share of income:**
- Labor share = Total compensation / GDP
- Declining trend in many advanced economies since the 1980s
- Drivers: Globalization, automation, declining union power, superstar firms, capital-biased technical change

### Labor Market Institutions

| Institution | Effect on NAIRU | Effect on Resilience |
|------------|----------------|---------------------|
| Employment protection (strict) | Raises NAIRU (slower adjustment) | Dampens cyclical fluctuations |
| Unemployment benefits (generous) | Raises NAIRU (higher reservation wage) | Provides automatic stabilization |
| Active labor market policies | Lowers NAIRU (better matching) | Supports reallocation |
| Minimum wage (moderate) | Ambiguous (depends on level) | Floor on wages, may reduce inequality |
| Collective bargaining (coordinated) | Lowers NAIRU (wage moderation) | Facilitates adjustment |
| Flexible contracts (widespread) | Lowers NAIRU (easier hiring) | Increases volatility (dual labor market) |

## Methodology

1. **Labor market slack assessment**: Compare unemployment rate to NAIRU estimate; examine U-6, participation rate, and vacancy-unemployment (Beveridge Curve) data
2. **Phillips Curve estimation**: Estimate the relationship between inflation and unemployment using appropriate specification (expectations-augmented or New Keynesian)
3. **Okun's Law application**: Estimate the output gap implied by unemployment data, or vice versa
4. **Wage dynamics analysis**: Decompose wage growth into productivity, inflation expectations, and labor market tightness components
5. **Policy evaluation**: Assess impact of labor market reforms on NAIRU, employment, and welfare
6. **Cross-country comparison**: Compare labor market outcomes relative to institutional frameworks

## Templates

### Labor Market Dashboard

```
Country: __________    Period: __________

Employment Indicators:
  Unemployment rate (U-3):        ____%    (NAIRU estimate: ____%)
  Unemployment rate (U-6):        ____%
  Labor force participation:      ____%
  Employment rate:                ____%
  Vacancy rate:                   ____%
  V/U ratio:                     _____

Wage Indicators:
  Nominal wage growth (YoY):      ____%
  Real wage growth (YoY):         ____%
  Productivity growth (YoY):      ____%
  Unit labor cost growth (YoY):   ____%
  Labor share of GDP:             ____%

Phillips Curve Assessment:
  Unemployment gap (u - u*):      ____%
  Implied inflation pressure:     [ ] Disinflationary  [ ] Neutral  [ ] Inflationary

Okun's Law Implied:
  Output gap from unemployment:   ____%
  Consistent with GDP growth:     ____%
```

## Quality Gate

- [ ] Unemployment decomposed by type (frictional, structural, cyclical)
- [ ] NAIRU estimate used with explicit uncertainty range acknowledged
- [ ] Phillips Curve specification appropriate (expectations-augmented or NK)
- [ ] Phillips Curve flattening considered when interpreting slope estimates
- [ ] Okun's Law coefficient appropriate for the country analyzed
- [ ] Wage growth decomposed into productivity, expectations, and slack components
- [ ] Broader measures of slack considered (U-6, participation, underemployment)
- [ ] Labor market institutions accounted for in cross-country comparisons
- [ ] Beveridge Curve shifts assessed for structural change in matching efficiency
- [ ] Distributional effects of labor market conditions analyzed (by skill, age, region)
