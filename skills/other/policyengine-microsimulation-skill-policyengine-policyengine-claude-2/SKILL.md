---
name: policyengine-microsimulation
description: |
  ALWAYS USE THIS SKILL for PolicyEngine microsimulation, population-level analysis, winners/losers calculations.
  Triggers: "microsimulation", "share who would lose/gain", "policy impact", "national average", "weighted analysis",
  "cost", "revenue impact", "budgetary", "estimate the cost", "federal revenues", "tax revenue", "budget score",
  "how much would it cost", "how much would the policy cost", "total cost of", "aggregate impact",
  "cost to the government", "revenue loss", "fiscal impact".
  NOT for single-household calculations like "what would my benefit be" — use policyengine-us or policyengine-uk for those.
  Use this skill's code pattern, but explore the codebase to find specific parameter paths if needed.
---

# PolicyEngine Microsimulation

## Documentation References

- **Microsimulation API**: https://policyengine.github.io/policyengine-us/usage/microsimulation.html
- **Parameter Discovery**: https://policyengine.github.io/policyengine-us/usage/parameter-discovery.html
- **Reform.from_dict()**: https://policyengine.github.io/policyengine-core/usage/reforms.html

## CRITICAL: Use calc() with MicroSeries - No Manual Weights Ever

**MicroSeries handles all weighting automatically. Never access .weights or do manual weight math.**

### NEVER strip weights with .values

`calc()` and `calculate()` return MicroSeries with embedded weights. Calling `.values` strips them and returns a plain numpy array where `.mean()` is **unweighted**.

```python
# ❌ WRONG - .values strips weights, .mean() is UNWEIGHTED
result = sim.calc("household_net_income", period=2026).values
wrong_mean = result.mean()  # Unweighted!

# ❌ WRONG - same problem with .to_numpy()
result = sim.calc("household_net_income", period=2026).to_numpy()

# ✅ CORRECT - keep as MicroSeries, all operations are weighted
result = sim.calc("household_net_income", period=2026)
correct_mean = result.mean()  # Weighted automatically!
```

### Correct patterns

```python
# ✅ CORRECT - MicroSeries handles everything
change = reformed.calc('household_net_income', period=2026, map_to='person') - \
         baseline.calc('household_net_income', period=2026, map_to='person')
loser_share = (change < 0).mean()  # Weighted automatically!

# ❌ WRONG - never access .weights or do manual math
loser_share = change.weights[change.values < 0].sum() / change.weights.sum()
```

## Quick Start

```python
from policyengine_us import Microsimulation
from policyengine_core.reforms import Reform

baseline = Microsimulation()
reform = Reform.from_dict({
    'gov.irs.credits.ctc.amount.base[0].amount': {'2026-01-01.2100-12-31': 3000}
}, 'policyengine_us')
reformed = Microsimulation(reform=reform)

# calc() returns MicroSeries - all operations are weighted automatically
baseline_income = baseline.calc('household_net_income', period=2026, map_to='person')
reformed_income = reformed.calc('household_net_income', period=2026, map_to='person')
change = reformed_income - baseline_income

# Weighted stats - no manual weight handling needed!
print(f"Average impact: ${change.mean():,.0f}")
print(f"Total cost: ${-change.sum()/1e9:,.1f}B")
print(f"Share losing: {(change < 0).mean():.1%}")
```

## Available Datasets (HuggingFace)

```python
# National (default)
sim = Microsimulation()

# State-level
sim = Microsimulation(dataset='hf://policyengine/policyengine-us-data/states/NY.h5')

# Congressional district - SEE policyengine-district-analysis skill for full examples
sim = Microsimulation(dataset='hf://policyengine/policyengine-us-data/districts/NY-17.h5')
```

**For congressional district analysis** (representative's constituents, district-level impacts), use the `policyengine-district-analysis` skill which has complete examples.

## Key MicroSeries Methods

```python
income = sim.calc('household_net_income', period=2026, map_to='person')

income.mean()           # Weighted mean
income.sum()            # Weighted sum
income.median()         # Weighted median
(income > 50000).mean() # Weighted share meeting condition
```

## Finding Parameter Paths

```bash
grep -r "salt" policyengine_us/parameters/gov/irs/ --include="*.yaml"
```

**Parameter tree:** `gov.irs.deductions`, `gov.irs.credits`, `gov.states.{state}.tax`

**Patterns:** Filing status variants (SINGLE, JOINT, etc.), bracket syntax `[index]`, date format `'YYYY-MM-DD.YYYY-MM-DD'`
