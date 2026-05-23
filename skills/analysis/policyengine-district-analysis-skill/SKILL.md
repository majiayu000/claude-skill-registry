---
name: policyengine-district-analysis
description: Analyze policy impacts for congressional districts and representatives' constituents. Use when the user mentions a specific district (NY-17, CA-52), a representative's name, or asks about geographic policy impacts at district level. Provides HuggingFace district datasets.
---

# Congressional District Policy Analysis

## Documentation References

- **Microsimulation API**: https://policyengine.github.io/policyengine-us/usage/microsimulation.html
- **Parameter Discovery**: https://policyengine.github.io/policyengine-us/usage/parameter-discovery.html

## CRITICAL: Use calc() - No Manual Weights Ever

**MicroSeries handles all weighting automatically. Never access .weights or do manual math.**

```python
# ✅ CORRECT
change = reformed.calc('household_net_income', period=2026, map_to='person') - \
         baseline.calc('household_net_income', period=2026, map_to='person')
loser_share = (change < 0).mean()  # Weighted automatically!

# ❌ WRONG
loser_share = change.weights[change.values < 0].sum() / change.weights.sum()
```

## Complete Example

```python
from policyengine_us import Microsimulation
from policyengine_core.reforms import Reform

# 1. Load district data
district = "NY-17"  # Mike Lawler's district
baseline = Microsimulation(dataset=f'hf://policyengine/policyengine-us-data/districts/{district}.h5')

# 2. Define reform (find params with: grep -r "salt" policyengine_us/parameters/gov/irs/)
reform = Reform.from_dict({
    'gov.irs.deductions.itemized.salt_and_real_estate.cap.SINGLE': {'2026-01-01.2100-12-31': 10000},
    'gov.irs.deductions.itemized.salt_and_real_estate.cap.JOINT': {'2026-01-01.2100-12-31': 10000},
    'gov.irs.deductions.itemized.salt_and_real_estate.cap.SEPARATE': {'2026-01-01.2100-12-31': 5000},
    'gov.irs.deductions.itemized.salt_and_real_estate.cap.HEAD_OF_HOUSEHOLD': {'2026-01-01.2100-12-31': 10000},
    'gov.irs.deductions.itemized.salt_and_real_estate.cap.SURVIVING_SPOUSE': {'2026-01-01.2100-12-31': 10000},
}, 'policyengine_us')

reformed = Microsimulation(dataset=f'hf://policyengine/policyengine-us-data/districts/{district}.h5', reform=reform)

# 3. Calculate impact - MicroSeries handles weights automatically!
baseline_income = baseline.calc('household_net_income', period=2026, map_to='person')
reformed_income = reformed.calc('household_net_income', period=2026, map_to='person')
change = reformed_income - baseline_income

# 4. Results - no manual weight math needed
print(f"Share losing: {(change < 0).mean():.1%}")
print(f"Average change: ${change.mean():,.0f}")
print(f"Total impact: ${change.sum()/1e6:,.1f}M")
```

## Compare to National

```python
national_baseline = Microsimulation()
national_reformed = Microsimulation(reform=reform)

national_change = national_reformed.calc('household_net_income', period=2026, map_to='person') - \
                  national_baseline.calc('household_net_income', period=2026, map_to='person')

print(f"District: {(change < 0).mean():.1%} lose")
print(f"National: {(national_change < 0).mean():.1%} lose")
```

