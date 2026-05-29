---
name: policyengine-us
description: PolicyEngine-US federal and state tax/benefit rules - variables, parameters, household situations. For national/state microsimulation see policyengine-microsimulation; for district-level see policyengine-district-analysis.
---

# PolicyEngine-US

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
            "age": {2024: 30},
            "employment_income": {2024: 50000}
        }
    },
    "families": {"family": {"members": ["you"]}},
    "marital_units": {"marital_unit": {"members": ["you"]}},
    "tax_units": {"tax_unit": {"members": ["you"]}},
    "spm_units": {"spm_unit": {"members": ["you"]}},
    "households": {
        "household": {
            "members": ["you"],
            "state_name": {2024: "CA"}
        }
    }
}

# Calculate taxes and benefits
sim = Simulation(situation=situation)
income_tax = sim.calculate("income_tax", 2024)[0]
eitc = sim.calculate("eitc", 2024)[0]

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

### When to Use This Skill

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
            "age": {2024: 35},
            "employment_income": {2024: 50000},
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
            "state_name": {2024: "CA"}
        }
    }
}
```

**Key Rules:**
- All entities must have consistent member lists
- Use year keys for all values: `{2024: value}`
- State must be two-letter code (e.g., "CA", "NY", "TX")
- All monetary values in dollars (not cents)

### 2. Creating Simulations

```python
from policyengine_us import Simulation

# Create simulation from situation
simulation = Simulation(situation=situation)

# Calculate variables
income_tax = simulation.calculate("income_tax", 2024)
eitc = simulation.calculate("eitc", 2024)
household_net_income = simulation.calculate("household_net_income", 2024)
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
        "period": 2024
    }]]
}

simulation = Simulation(situation=situation)
# Now calculate() returns arrays of 1001 values
incomes = simulation.calculate("employment_income", 2024)  # Array of 1001 values
taxes = simulation.calculate("income_tax", 2024)  # Array of 1001 values
```

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
        "2024-01-01.2100-12-31": 5000  # Increase CTC to $5000
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
            "age": {2024: 35},
            "employment_income": {2024: 60000}
        },
        "child": {
            "age": {2024: 5}
        }
    },
    "families": {"family": {"members": ["parent", "child"]}},
    "marital_units": {"marital_unit": {"members": ["parent"]}},
    "tax_units": {"tax_unit": {"members": ["parent", "child"]}},
    "spm_units": {"spm_unit": {"members": ["parent", "child"]}},
    "households": {
        "household": {
            "members": ["parent", "child"],
            "state_name": {2024: "NY"}
        }
    }
}

sim = Simulation(situation=situation)
income_tax = sim.calculate("income_tax", 2024)[0]
ctc = sim.calculate("ctc", 2024)[0]
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
        "period": 2024
    }]]
}

sim = Simulation(situation=situation_with_axes)
incomes = sim.calculate("employment_income", 2024)
taxes = sim.calculate("income_tax", 2024)

# Calculate marginal tax rate
import numpy as np
mtr = np.gradient(taxes) / np.gradient(incomes)
```

### Pattern 3: Charitable Donation Impact

```python
# Baseline (no donation)
situation_baseline = create_situation(income=100000, donation=0)
sim_baseline = Simulation(situation=situation_baseline)
tax_baseline = sim_baseline.calculate("income_tax", 2024)[0]

# With donation
situation_donation = create_situation(income=100000, donation=5000)
sim_donation = Simulation(situation=situation_donation)
tax_donation = sim_donation.calculate("income_tax", 2024)[0]

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
        "state_income_tax": sim.calculate("state_income_tax", 2024)[0],
        "total_tax": sim.calculate("household_tax", 2024)[0]
    }
```

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
**Problem:** `"age": 35` instead of `"age": {2024: 35}`

**Solution:** Always use year dictionary:
```python
"age": {2024: 35},
"employment_income": {2024: 50000}
```

### Pitfall 3: Net Taxes vs Gross Taxes
**Problem:** Forgetting to subtract benefits from taxes

**Solution:** Use proper calculation:
```python
# Net taxes (what household actually pays)
net_tax = sim.calculate("household_tax", 2024) - \
          sim.calculate("household_benefits", 2024)
```

### Pitfall 4: Axes Persistence
**Problem:** Axes remain in situation when creating single-point simulation

**Solution:** Remove axes before single-point simulation:
```python
situation_single = situation.copy()
situation_single.pop("axes", None)
```

### Pitfall 5: State-Specific Variables
**Problem:** Using NYC-specific variables without `in_nyc: True`

**Solution:** Set NYC flag for NY residents in NYC:
```python
"households": {
    "household": {
        "state_name": {2024: "NY"},
        "in_nyc": {2024: True}  # Required for NYC taxes
    }
}
```

## NYC Handling

For New York City residents:
```python
situation = {
    # ... people setup ...
    "households": {
        "household": {
            "members": ["person"],
            "state_name": {2024: "NY"},
            "in_nyc": {2024: True}  # Enable NYC tax calculations
        }
    }
}
```

## Version Compatibility

- Always use `policyengine-us>=1.155.0` for 2024 calculations
- Check version: `import policyengine_us; print(policyengine_us.__version__)`
- Different years may require different package versions

## Debugging Tips

1. **Enable tracing:**
   ```python
   simulation.trace = True
   result = simulation.calculate("variable_name", 2024)
   ```

2. **Check intermediate calculations:**
   ```python
   agi = simulation.calculate("adjusted_gross_income", 2024)
   taxable_income = simulation.calculate("taxable_income", 2024)
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
