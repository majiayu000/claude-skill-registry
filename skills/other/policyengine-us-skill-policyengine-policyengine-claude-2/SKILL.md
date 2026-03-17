---
name: policyengine-us
description: |
  ALWAYS LOAD THIS SKILL FIRST before writing any PolicyEngine-US code.
  Contains the correct situation dictionary structure, entity names, variable names, and state_code format
  that are required to avoid common errors (e.g., state_name vs state_code, missing entity groups).
  Use for ANY US household benefit/tax calculation, eligibility question, or PolicyEngine-US code.
  Triggers: "what would", "how much would a", "benefit be", "eligible for", "qualify for",
  "single parent", "married couple", "family of", "household of", "if they earn", "with income of",
  "earning $", "making $", "calculate benefits", "calculate taxes", "benefit for a", "tax for a",
  "what benefits", "how much tax", "what would I get", "what would they get",
  "what is the maximum", "what is the rate", "what is the threshold", "poverty line",
  "income limit", "benefit amount", "how much is", "maximum benefit", "compare states",
  "TANF", "SNAP", "EITC", "CTC", "SSI", "WIC", "Section 8", "Medicaid", "ACA", "food stamps",
  "child tax credit", "earned income", "supplemental security", "housing voucher".
  For national/state microsimulation see policyengine-microsimulation; for district-level see policyengine-district-analysis.
---

# PolicyEngine-US

> **IMPORTANT: Always use the current year (2026) in situation dictionaries and calculate() calls, not 2024 or 2025.**

PolicyEngine-US models the US federal and state tax and benefit system.

## For Users 👥

### What is PolicyEngine-US?

PolicyEngine-US is the "calculator" for US taxes and benefits. When you use policyengine.org/us, PolicyEngine-US runs behind the scenes.

**What it models:**

**Federal taxes:**
- Income tax (with standard/itemized deductions)
- Payroll tax (Social Security, Medicare)
- Capital gains tax

**Federal benefits:**
- Earned Income Tax Credit (EITC)
- Child Tax Credit (CTC)
- SNAP (food stamps)
- WIC, ACA premium tax credits
- Social Security, SSI, TANF

**State programs (varies by state):**
- State income tax (all 50 states + DC)
- State EITC, CTC
- State-specific benefits

**See full list:** https://policyengine.org/us/parameters

### Understanding Variables

When you see results in PolicyEngine, these are variables:

**Income variables:**
- `employment_income` - W-2 wages
- `self_employment_income` - 1099 income
- `qualified_dividend_income` - Dividends
- `capital_gains` - Capital gains

**Tax variables:**
- `income_tax` - Federal income tax
- `state_income_tax` - State income tax
- `payroll_tax` - FICA taxes

**Benefit variables:**
- `eitc` - Earned Income Tax Credit
- `ctc` - Child Tax Credit
- `snap` - SNAP benefits

**Summary variables:**
- `household_net_income` - Income after taxes and benefits
- `household_tax` - Total taxes
- `household_benefits` - Total benefits

## For Analysts 📊

### Installation and Setup

```bash
# Install PolicyEngine-US
pip install policyengine-us

# Or with uv (recommended)
uv pip install policyengine-us
```

### Quick Start

```python
from policyengine_us import Simulation

# Create a household
situation = {
    "people": {
        "you": {
            "age": {2026: 30},
            "employment_income": {2026: 50000}
        }
    },
    "families": {"family": {"members": ["you"]}},
    "marital_units": {"marital_unit": {"members": ["you"]}},
    "tax_units": {"tax_unit": {"members": ["you"]}},
    "spm_units": {"spm_unit": {"members": ["you"]}},
    "households": {
        "household": {
            "members": ["you"],
            "state_name": {2026: "CA"}
        }
    }
}

# Calculate taxes and benefits
sim = Simulation(situation=situation)
income_tax = sim.calculate("income_tax", 2026)[0]
eitc = sim.calculate("eitc", 2026)[0]

print(f"Income tax: ${income_tax:,.0f}")
print(f"EITC: ${eitc:,.0f}")
```

### Web App to Python

**Web app URL:**
```
policyengine.org/us/household?household=12345
```

**Equivalent Python (conceptually):**
The household ID represents a situation dictionary. To replicate in Python, you'd create a similar situation.

### Parameter lookup (for "what is the maximum/rate/threshold" questions)

When users ask about a specific policy value (maximum benefit, tax rate, income threshold, etc.),
look up the parameter directly instead of running a simulation. This is faster and more direct.

```python
from policyengine_us import CountryTaxBenefitSystem

# Load the parameter tree
params = CountryTaxBenefitSystem().parameters

# Look up a specific parameter value for 2026
# Navigate the tree: params.gov.<agency>.<program>.<parameter>
# For scalar parameters, call with a date string:
ctc_amount = params.gov.irs.credits.ctc.amount.base_amount("2026-01-01")
print(f"CTC base amount: ${ctc_amount:,.0f}")  # $2,000

# For bracket/indexed parameters (by family size, income bracket, etc.),
# use .children["N"] where N is a string:
dc_tanf_max = params.gov.states.dc.dhs.tanf.standard_payment.amount.children["3"]("2026-01-01")
print(f"DC TANF max (family of 3): ${dc_tanf_max:,.0f}/month")

# SNAP max allotment for a family of 4
snap_max = params.gov.usda.snap.income.max_allotment.children["4"]("2026-01-01")

# Federal poverty level for family of 3
fpl = params.gov.hhs.poverty_guideline.children["3"]("2026-01-01")
```

**IMPORTANT**: For indexed/bracket parameters, always use `.children["N"]` (string key),
NOT `[N]` (integer subscript). The `[N]` syntax does not work on ParameterNode objects.

**When to use parameter lookup vs simulation:**
- **Parameter lookup**: "What is the maximum TANF benefit?", "What is the CTC amount?", "What is the poverty line?"
- **Simulation**: "What would my TANF benefit be if I earn $500/mo?", "Am I eligible for SNAP?"

**Finding parameter paths:**
- Browse: https://policyengine.org/us/parameters
- Or explore the tree: `params.gov.states.dc` and inspect children
- State parameters follow pattern: `params.gov.states.<state_code>.<agency>.<program>`

### When to Use This Skill

- Looking up policy parameter values (rates, thresholds, maximum benefits)
- Creating household situations for tax/benefit calculations
- Understanding variables, parameters, and policy reforms
- Building tools that use PolicyEngine-US (calculators, analysis notebooks)
- Debugging PolicyEngine-US calculations

**For microsimulation/population analysis**, see the `policyengine-microsimulation` skill.
**For congressional district analysis**, see the `policyengine-district-analysis` skill.

## For Contributors 💻

### Repository

**Location:** PolicyEngine/policyengine-us

**To see current implementation:**
```bash
git clone https://github.com/PolicyEngine/policyengine-us
cd policyengine-us

# Explore structure
tree policyengine_us/
```

**Key directories:**
```bash
ls policyengine_us/
# - variables/   - Tax and benefit calculations
# - parameters/  - Policy rules (YAML)
# - reforms/     - Pre-defined reforms
# - tests/       - Test cases
```

## Core Concepts

### 1. Situation Dictionary Structure

PolicyEngine requires a nested dictionary defining household composition and characteristics:

```python
situation = {
    "people": {
        "person_id": {
            "age": {2026: 35},
            "employment_income": {2026: 50000},
            # ... other person attributes
        }
    },
    "families": {
        "family_id": {"members": ["person_id", ...]}
    },
    "marital_units": {
        "marital_unit_id": {"members": ["person_id", ...]}
    },
    "tax_units": {
        "tax_unit_id": {"members": ["person_id", ...]}
    },
    "spm_units": {
        "spm_unit_id": {"members": ["person_id", ...]}
    },
    "households": {
        "household_id": {
            "members": ["person_id", ...],
            "state_name": {2026: "CA"}
        }
    }
}
```

**Key Rules:**
- All entities must have consistent member lists
- Use year keys for all values: `{2026: value}`
- State must be two-letter code (e.g., "CA", "NY", "TX")
- All monetary values in dollars (not cents)

### 2. Creating Simulations

```python
from policyengine_us import Simulation

# Create simulation from situation
simulation = Simulation(situation=situation)

# Calculate variables
income_tax = simulation.calculate("income_tax", 2026)
eitc = simulation.calculate("eitc", 2026)
household_net_income = simulation.calculate("household_net_income", 2026)
```

**Common Variables:**

**Income:**
- `employment_income` - W-2 wages
- `self_employment_income` - 1099/business income
- `qualified_dividend_income` - Qualified dividends
- `capital_gains` - Capital gains
- `interest_income` - Interest income
- `social_security` - Social Security benefits
- `pension_income` - Pension/retirement income

**Deductions:**
- `charitable_cash_donations` - Cash charitable giving
- `real_estate_taxes` - State and local property taxes
- `mortgage_interest` - Mortgage interest deduction
- `medical_expense` - Medical and dental expenses
- `casualty_loss` - Casualty and theft losses

**Tax Outputs:**
- `income_tax` - Total federal income tax
- `payroll_tax` - FICA taxes
- `state_income_tax` - State income tax
- `household_tax` - Total taxes (federal + state + local)

**Benefits:**
- `eitc` - Earned Income Tax Credit
- `ctc` - Child Tax Credit
- `snap` - SNAP benefits
- `household_benefits` - Total benefits

**Summary:**
- `household_net_income` - Income minus taxes plus benefits

### 3. Using Axes for Parameter Sweeps

To vary a parameter across multiple values:

```python
situation = {
    # ... normal situation setup ...
    "axes": [[{
        "name": "employment_income",
        "count": 1001,
        "min": 0,
        "max": 200000,
        "period": 2026
    }]]
}

simulation = Simulation(situation=situation)
# Now calculate() returns arrays of 1001 values
incomes = simulation.calculate("employment_income", 2026)  # Array of 1001 values
taxes = simulation.calculate("income_tax", 2026)  # Array of 1001 values
```

**Important — multi-person households with axes:**

Person-level variables (like `employment_income`) return `n_people × count` values,
while unit-level variables (like `tanf`, `income_tax`) return just `count` values.
Use `map_to` to aggregate person-level results to a group entity for aligned arrays:

```python
# map_to sums person-level values to the group level
income = simulation.calculate("employment_income", 2026, map_to="household")  # (1001,)
tanf = simulation.calculate("tanf", 2026)  # (1001,) - already at spm_unit level
# These arrays are now aligned and can be plotted/compared directly
```

Valid `map_to` targets: `"household"`, `"spm_unit"`, `"tax_unit"`, `"family"`, `"marital_unit"`.
Use singular form (e.g., `"household"` not `"households"`).

**Important:** Remove axes before creating single-point simulations:
```python
situation_single = situation.copy()
situation_single.pop("axes", None)
simulation = Simulation(situation=situation_single)
```

### 4. Policy Reforms

```python
from policyengine_us import Simulation

# Define a reform (modifies parameters)
reform = {
    "gov.irs.credits.ctc.amount.base_amount": {
        "2026-01-01.2100-12-31": 5000  # Increase CTC to $5000
    }
}

# Create simulation with reform
simulation = Simulation(situation=situation, reform=reform)
```

## Common Patterns

### Pattern 1: Single Household Calculation

```python
from policyengine_us import Simulation

situation = {
    "people": {
        "parent": {
            "age": {2026: 35},
            "employment_income": {2026: 60000}
        },
        "child": {
            "age": {2026: 5}
        }
    },
    "families": {"family": {"members": ["parent", "child"]}},
    "marital_units": {"marital_unit": {"members": ["parent"]}},
    "tax_units": {"tax_unit": {"members": ["parent", "child"]}},
    "spm_units": {"spm_unit": {"members": ["parent", "child"]}},
    "households": {
        "household": {
            "members": ["parent", "child"],
            "state_name": {2026: "NY"}
        }
    }
}

sim = Simulation(situation=situation)
income_tax = sim.calculate("income_tax", 2026)[0]
ctc = sim.calculate("ctc", 2026)[0]
```

### Pattern 2: Marginal Tax Rate Analysis

```python
# Create baseline with axes varying income
situation_with_axes = {
    # ... situation setup ...
    "axes": [[{
        "name": "employment_income",
        "count": 1001,
        "min": 0,
        "max": 200000,
        "period": 2026
    }]]
}

sim = Simulation(situation=situation_with_axes)
# Use map_to for person-level vars to align with unit-level outputs
incomes = sim.calculate("employment_income", 2026, map_to="tax_unit")
taxes = sim.calculate("income_tax", 2026)

# Calculate marginal tax rate
import numpy as np
mtr = np.gradient(taxes) / np.gradient(incomes)
```

### Pattern 3: Charitable Donation Impact

```python
# Baseline (no donation)
situation_baseline = create_situation(income=100000, donation=0)
sim_baseline = Simulation(situation=situation_baseline)
tax_baseline = sim_baseline.calculate("income_tax", 2026)[0]

# With donation
situation_donation = create_situation(income=100000, donation=5000)
sim_donation = Simulation(situation=situation_donation)
tax_donation = sim_donation.calculate("income_tax", 2026)[0]

# Tax savings from donation
tax_savings = tax_baseline - tax_donation
effective_discount = tax_savings / 5000  # e.g., 0.24 = 24% discount
```

### Pattern 4: State Comparison

```python
states = ["CA", "NY", "TX", "FL"]
results = {}

for state in states:
    situation = create_situation(state=state, income=75000)
    sim = Simulation(situation=situation)
    results[state] = {
        "state_income_tax": sim.calculate("state_income_tax", 2026)[0],
        "total_tax": sim.calculate("household_tax", 2026)[0]
    }
```

### Pattern 5: Benefit Cliff Analysis

Use axes to sweep income and find where benefits drop sharply:

```python
from policyengine_us import Simulation
import numpy as np

# Setup situation with axes (see Pattern 1 for full situation dict)
# ... situation with axes varying employment_income from 0 to max_income ...

sim = Simulation(situation=situation)

# Use map_to to align person-level income with unit-level benefits
income = sim.calculate("employment_income", 2026, map_to="household")
benefit = sim.calculate("tanf", 2026)  # or ca_tanf, snap, etc.
net_income = sim.calculate("household_net_income", 2026)

# Find the cliff: biggest single-step drop in benefits
benefit_diffs = np.diff(benefit)
biggest_drop_idx = np.argmin(benefit_diffs)
cliff_size = benefit[biggest_drop_idx] - benefit[biggest_drop_idx + 1]

# Find all cliffs (MTR > 100% = net income drops when earnings rise)
net_diffs = np.diff(net_income)
income_diffs = np.diff(income)
mtr = 1 - net_diffs / np.where(income_diffs > 0, income_diffs, 1)
cliff_indices = np.where(mtr > 1)[0]
```

**Tips:**
- Use 1000+ axis points for fine granularity around cliffs
- Set the income range to cover the expected phase-out zone
- `household_net_income` captures interactions across all programs (TANF, SNAP, taxes, etc.)
- For state-specific benefits, use the state-prefixed variable (e.g., `ca_tanf`, `ny_tanf`)

## Helper Scripts

This skill includes helper scripts in the `scripts/` directory:

```python
from policyengine_skills.situation_helpers import (
    create_single_filer,
    create_married_couple,
    create_family_with_children,
    add_itemized_deductions
)

# Quick situation creation
situation = create_single_filer(
    income=50000,
    state="CA",
    age=30
)

# Add deductions
situation = add_itemized_deductions(
    situation,
    charitable_donations=5000,
    mortgage_interest=10000,
    real_estate_taxes=8000
)
```

## Common Pitfalls and Solutions

### Pitfall 1: Member Lists Out of Sync
**Problem:** Different entities have different members
```python
# WRONG
"tax_units": {"tax_unit": {"members": ["parent"]}},
"households": {"household": {"members": ["parent", "child"]}}
```

**Solution:** Keep all entity member lists consistent:
```python
# CORRECT
all_members = ["parent", "child"]
"families": {"family": {"members": all_members}},
"tax_units": {"tax_unit": {"members": all_members}},
"households": {"household": {"members": all_members}}
```

### Pitfall 2: Forgetting Year Keys
**Problem:** `"age": 35` instead of `"age": {2026: 35}`

**Solution:** Always use year dictionary:
```python
"age": {2026: 35},
"employment_income": {2026: 50000}
```

### Pitfall 3: Net Taxes vs Gross Taxes
**Problem:** Forgetting to subtract benefits from taxes

**Solution:** Use proper calculation:
```python
# Net taxes (what household actually pays)
net_tax = sim.calculate("household_tax", 2026) - \
          sim.calculate("household_benefits", 2026)
```

### Pitfall 4: Axes Persistence
**Problem:** Axes remain in situation when creating single-point simulation

**Solution:** Remove axes before single-point simulation:
```python
situation_single = situation.copy()
situation_single.pop("axes", None)
```

### Pitfall 5: Geography Variables
**Problem:** Missing geography inputs for sub-state programs (county, city, region).

Many state programs vary by county or region. Set these on the `household` entity:

```python
"households": {
    "household": {
        "members": [...],
        "state_name": {2026: "CA"},
        # County (UPPER_SNAKE_CASE with state suffix):
        "county_str": {2026: "LOS_ANGELES_COUNTY_CA"},
        # City flags (boolean):
        "in_nyc": {2026: True},   # NYC taxes
        "in_la": {2026: True},    # LA-specific programs
    }
}
```

**County format:** `county_str` uses `UPPER_SNAKE_CASE_STATE` (e.g., `"LOS_ANGELES_COUNTY_CA"`,
`"HARRIS_COUNTY_TX"`, `"COOK_COUNTY_IL"`).

**SPM unit flags** for state program variants:
```python
"spm_units": {
    "spm_unit": {
        "members": [...],
        "ca_tanf_exempt": {2026: False},  # CA TANF exempt vs non-exempt
    }
}
```

**Discovering geography variables:** Search for county/region variables relevant to your program:
```python
system = CountryTaxBenefitSystem()
geo_vars = [v for v in system.variables if 'county' in v or 'region' in v]
```

## Discovering State-Specific Variables

State variables follow the naming convention `{state_code}_{program}` (e.g., `ca_tanf`, `ny_tanf`, `dc_tanf`).

**Finding variables for a state or program:**
```python
from policyengine_us import CountryTaxBenefitSystem
system = CountryTaxBenefitSystem()

# All variables for a state
ca_vars = [v for v in system.variables if v.startswith("ca_")]

# All TANF variables (any state)
tanf_vars = [v for v in system.variables if "tanf" in v]

# Check a variable's entity (person, spm_unit, household, etc.)
var = system.variables["ca_tanf"]
print(var.entity.key)  # "spm_unit"
```

**Common state program prefixes:**
- `{state}_tanf` — TANF/cash assistance (entity: `spm_unit`)
- `{state}_income_tax` — State income tax (entity: `tax_unit`, but just use `state_income_tax`)
- `{state}_eitc` — State EITC (entity: `tax_unit`)
- `{state}_ctc` — State child tax credit (entity: `tax_unit`)
- `{state}_cdcc` — State child/dependent care credit (entity: `tax_unit`)

**Finding parameters for a state:**
```python
params = CountryTaxBenefitSystem().parameters
# Browse: params.gov.states.{state_code}
ca_params = params.gov.states.ca
print([c for c in ca_params.children])  # List agencies/programs
```

## Version Compatibility

- Always use the latest `policyengine-us` for current year calculations
- Check version: `import policyengine_us; print(policyengine_us.__version__)`
- Different years may require different package versions

## Debugging Tips

1. **Enable tracing:**
   ```python
   simulation.trace = True
   result = simulation.calculate("variable_name", 2026)
   ```

2. **Check intermediate calculations:**
   ```python
   agi = simulation.calculate("adjusted_gross_income", 2026)
   taxable_income = simulation.calculate("taxable_income", 2026)
   ```

3. **Verify situation structure:**
   ```python
   import json
   print(json.dumps(situation, indent=2))
   ```

4. **Test with PolicyEngine web app:**
   - Go to policyengine.org/us/household
   - Enter same inputs
   - Compare results

## Additional Resources

- **Documentation:** https://policyengine.org/us/docs
- **API Reference:** https://github.com/PolicyEngine/policyengine-us
- **Example Notebooks:** https://github.com/PolicyEngine/analysis-notebooks
- **Variable Explorer:** https://policyengine.org/us/variables

## Examples Directory

See `examples/` for complete working examples:
- `single_filer.yaml` - Single person household
- `married_couple.yaml` - Married filing jointly
- `family_with_children.yaml` - Family with dependents
- `itemized_deductions.yaml` - Using itemized deductions
- `donation_sweep.yaml` - Analyzing donation impacts with axes
