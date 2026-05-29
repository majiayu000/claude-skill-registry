---
name: policyengine-uk
description: PolicyEngine-UK tax and benefit microsimulation patterns, situation creation, and common workflows
---

# PolicyEngine-UK

PolicyEngine-UK models the UK tax and benefit system, including devolved variations for Scotland and Wales.

## For Users 👥

### What is PolicyEngine-UK?

PolicyEngine-UK is the "calculator" for UK taxes and benefits. When you use policyengine.org/uk, PolicyEngine-UK runs behind the scenes.

**What it models:**

**Direct taxes:**
- Income tax (UK-wide, Scottish, and Welsh variations)
- National Insurance (Classes 1, 2, 4)
- Capital gains tax
- Dividend tax

**Property and transaction taxes:**
- Council Tax
- Stamp Duty Land Tax (England/NI)
- Land and Buildings Transaction Tax (Scotland)
- Land Transaction Tax (Wales)

**Universal Credit:**
- Standard allowance
- Child elements
- Housing cost element
- Childcare costs element
- Carer element
- Work capability elements

**Legacy benefits (being phased out):**
- Working Tax Credit
- Child Tax Credit
- Income Support
- Income-based JSA/ESA
- Housing Benefit

**Other benefits:**
- Child Benefit
- Pension Credit
- Personal Independence Payment (PIP)
- Disability Living Allowance (DLA)
- Attendance Allowance
- State Pension

**See full list:** https://policyengine.org/uk/parameters

### Understanding Variables

When you see results in PolicyEngine, these are variables:

**Income variables:**
- `employment_income` - Gross employment earnings/salary
- `self_employment_income` - Self-employment profits
- `pension_income` - Private pension income
- `property_income` - Rental income
- `savings_interest_income` - Interest from savings
- `dividend_income` - Dividend income

**Tax variables:**
- `income_tax` - Total income tax liability
- `national_insurance` - Total NI contributions
- `council_tax` - Council tax liability

**Benefit variables:**
- `universal_credit` - Universal Credit amount
- `child_benefit` - Child Benefit amount
- `pension_credit` - Pension Credit amount
- `working_tax_credit` - Working Tax Credit (legacy)
- `child_tax_credit` - Child Tax Credit (legacy)

**Summary variables:**
- `household_net_income` - Income after taxes and benefits
- `disposable_income` - Income after taxes
- `equivalised_household_net_income` - Adjusted for household size

## For Analysts 📊

### Installation and Setup

```bash
# Install PolicyEngine-UK
pip install policyengine-uk

# Or with uv (recommended)
uv pip install policyengine-uk
```

### Quick Start

```python
from policyengine_uk import Simulation

# Create a household
situation = {
    "people": {
        "person": {
            "age": {2025: 30},
            "employment_income": {2025: 30000}
        }
    },
    "benunits": {
        "benunit": {
            "members": ["person"]
        }
    },
    "households": {
        "household": {
            "members": ["person"],
            "region": {2025: "LONDON"}
        }
    }
}

# Calculate taxes and benefits
sim = Simulation(situation=situation)
income_tax = sim.calculate("income_tax", 2025)[0]
universal_credit = sim.calculate("universal_credit", 2025)[0]

print(f"Income tax: £{income_tax:,.0f}")
print(f"Universal Credit: £{universal_credit:,.0f}")
```

### Web App to Python

**Web app URL:**
```
policyengine.org/uk/household?household=12345
```

**Equivalent Python (conceptually):**
The household ID represents a situation dictionary. To replicate in Python, you'd create a similar situation.

### When to Use This Skill

- Creating household situations for tax/benefit calculations
- Running microsimulations with PolicyEngine-UK
- Analyzing policy reforms and their impacts
- Building tools that use PolicyEngine-UK (calculators, analysis notebooks)
- Debugging PolicyEngine-UK calculations

## For Contributors 💻

### Repository

**Location:** PolicyEngine/policyengine-uk

**To see current implementation:**
```bash
git clone https://github.com/PolicyEngine/policyengine-uk
cd policyengine-uk

# Explore structure
tree policyengine_uk/
```

**Key directories:**
```bash
ls policyengine_uk/
# - variables/   - Tax and benefit calculations
# - parameters/  - Policy rules (YAML)
# - reforms/     - Pre-defined reforms
# - tests/       - Test cases
```

## Core Concepts

### 1. Situation Dictionary Structure

PolicyEngine UK requires a nested dictionary defining household composition:

```python
situation = {
    "people": {
        "person_id": {
            "age": {2025: 35},
            "employment_income": {2025: 30000},
            # ... other person attributes
        }
    },
    "benunits": {
        "benunit_id": {
            "members": ["person_id", ...]
        }
    },
    "households": {
        "household_id": {
            "members": ["person_id", ...],
            "region": {2025: "SOUTH_EAST"}
        }
    }
}
```

**Key Rules:**
- All entities must have consistent member lists
- Use year keys for all values: `{2025: value}`
- Region must be one of the ITL 1 regions (see below)
- All monetary values in pounds (not pence)
- UK tax year runs April 6 to April 5 (but use calendar year in code)

**Important Entity Difference:**
- UK uses **benunits** (benefit units): a single adult OR couple + dependent children
- This is the assessment unit for most means-tested benefits
- Unlike US which uses families/marital_units/tax_units/spm_units

### 2. Creating Simulations

```python
from policyengine_uk import Simulation

# Create simulation from situation
simulation = Simulation(situation=situation)

# Calculate variables
income_tax = simulation.calculate("income_tax", 2025)
universal_credit = simulation.calculate("universal_credit", 2025)
household_net_income = simulation.calculate("household_net_income", 2025)
```

**Common Variables:**

**Income:**
- `employment_income` - Gross employment earnings
- `self_employment_income` - Self-employment profits
- `pension_income` - Private pension income
- `property_income` - Rental income
- `savings_interest_income` - Interest income
- `dividend_income` - Dividend income
- `miscellaneous_income` - Other income sources

**Tax Outputs:**
- `income_tax` - Total income tax liability
- `national_insurance` - Total NI contributions
- `council_tax` - Council tax liability
- `VAT` - Value Added Tax paid

**Benefits:**
- `universal_credit` - Universal Credit
- `child_benefit` - Child Benefit
- `pension_credit` - Pension Credit
- `working_tax_credit` - Working Tax Credit (legacy)
- `child_tax_credit` - Child Tax Credit (legacy)
- `personal_independence_payment` - PIP
- `attendance_allowance` - Attendance Allowance
- `state_pension` - State Pension

**Summary:**
- `household_net_income` - Income after taxes and benefits
- `disposable_income` - Income after taxes
- `equivalised_household_net_income` - Adjusted for household size

### 3. Using Axes for Parameter Sweeps

To vary a parameter across multiple values:

```python
situation = {
    # ... normal situation setup ...
    "axes": [[{
        "name": "employment_income",
        "count": 1001,
        "min": 0,
        "max": 100000,
        "period": 2025
    }]]
}

simulation = Simulation(situation=situation)
# Now calculate() returns arrays of 1001 values
incomes = simulation.calculate("employment_income", 2025)  # Array of 1001 values
taxes = simulation.calculate("income_tax", 2025)  # Array of 1001 values
```

**Important:** Remove axes before creating single-point simulations:
```python
situation_single = situation.copy()
situation_single.pop("axes", None)
simulation = Simulation(situation=situation_single)
```

### 4. Policy Reforms

```python
from policyengine_uk import Simulation

# Define a reform (modifies parameters)
reform = {
    "gov.hmrc.income_tax.rates.uk.brackets[0].rate": {
        "2025-01-01.2100-12-31": 0.25  # Increase basic rate to 25%
    }
}

# Create simulation with reform
simulation = Simulation(situation=situation, reform=reform)
```

## Common Patterns

### Pattern 1: Single Person Household Calculation

```python
from policyengine_uk import Simulation

situation = {
    "people": {
        "person": {
            "age": {2025: 30},
            "employment_income": {2025: 30000}
        }
    },
    "benunits": {
        "benunit": {
            "members": ["person"]
        }
    },
    "households": {
        "household": {
            "members": ["person"],
            "region": {2025: "LONDON"}
        }
    }
}

sim = Simulation(situation=situation)
income_tax = sim.calculate("income_tax", 2025)[0]
national_insurance = sim.calculate("national_insurance", 2025)[0]
universal_credit = sim.calculate("universal_credit", 2025)[0]
```

### Pattern 2: Couple with Children

```python
situation = {
    "people": {
        "parent_1": {
            "age": {2025: 35},
            "employment_income": {2025: 35000}
        },
        "parent_2": {
            "age": {2025: 33},
            "employment_income": {2025: 25000}
        },
        "child_1": {
            "age": {2025: 8}
        },
        "child_2": {
            "age": {2025: 5}
        }
    },
    "benunits": {
        "benunit": {
            "members": ["parent_1", "parent_2", "child_1", "child_2"]
        }
    },
    "households": {
        "household": {
            "members": ["parent_1", "parent_2", "child_1", "child_2"],
            "region": {2025: "NORTH_WEST"}
        }
    }
}

sim = Simulation(situation=situation)
child_benefit = sim.calculate("child_benefit", 2025)[0]
universal_credit = sim.calculate("universal_credit", 2025)[0]
```

### Pattern 3: Marginal Tax Rate Analysis

```python
# Create baseline with axes varying income
situation_with_axes = {
    "people": {
        "person": {
            "age": {2025: 30}
        }
    },
    "benunits": {"benunit": {"members": ["person"]}},
    "households": {
        "household": {
            "members": ["person"],
            "region": {2025: "LONDON"}
        }
    },
    "axes": [[{
        "name": "employment_income",
        "count": 1001,
        "min": 0,
        "max": 100000,
        "period": 2025
    }]]
}

sim = Simulation(situation=situation_with_axes)
incomes = sim.calculate("employment_income", 2025)
net_incomes = sim.calculate("household_net_income", 2025)

# Calculate marginal tax rate
import numpy as np
mtr = 1 - (np.gradient(net_incomes) / np.gradient(incomes))
```

### Pattern 4: Regional Comparison

```python
regions = ["LONDON", "SCOTLAND", "WALES", "NORTH_EAST"]
results = {}

for region in regions:
    situation = create_situation(region=region, income=30000)
    sim = Simulation(situation=situation)
    results[region] = {
        "income_tax": sim.calculate("income_tax", 2025)[0],
        "national_insurance": sim.calculate("national_insurance", 2025)[0],
        "total_tax": sim.calculate("income_tax", 2025)[0] +
                     sim.calculate("national_insurance", 2025)[0]
    }
```

### Pattern 5: Policy Reform Impact

```python
from policyengine_uk import Microsimulation, Reform

# Define reform: Increase basic rate to 25%
class IncreaseBasicRate(Reform):
    def apply(self):
        def modify_parameters(parameters):
            parameters.gov.hmrc.income_tax.rates.uk.brackets[0].rate.update(
                period="year:2025:10", value=0.25
            )
            return parameters
        self.modify_parameters(modify_parameters)

# Run microsimulation
baseline = Microsimulation()
reformed = Microsimulation(reform=IncreaseBasicRate)

# Calculate revenue impact
baseline_revenue = baseline.calc("income_tax", 2025).sum()
reformed_revenue = reformed.calc("income_tax", 2025).sum()
revenue_change = (reformed_revenue - baseline_revenue) / 1e9  # in billions

# Calculate household impact
baseline_net_income = baseline.calc("household_net_income", 2025)
reformed_net_income = reformed.calc("household_net_income", 2025)
```

## Helper Scripts

This skill includes helper scripts in the `scripts/` directory:

```python
from policyengine_uk_skills.situation_helpers import (
    create_single_person,
    create_couple,
    create_family_with_children,
    add_region
)

# Quick situation creation
situation = create_single_person(
    income=30000,
    region="LONDON",
    age=30
)

# Create couple
situation = create_couple(
    income_1=35000,
    income_2=25000,
    region="SCOTLAND"
)
```

## Common Pitfalls and Solutions

### Pitfall 1: Member Lists Out of Sync

**Problem:** Different entities have different members
```python
# WRONG
"benunits": {"benunit": {"members": ["parent"]}},
"households": {"household": {"members": ["parent", "child"]}}
```

**Solution:** Keep all entity member lists consistent:
```python
# CORRECT
all_members = ["parent", "child"]
"benunits": {"benunit": {"members": all_members}},
"households": {"household": {"members": all_members}}
```

### Pitfall 2: Forgetting Year Keys

**Problem:** `"age": 35` instead of `"age": {2025: 35}`

**Solution:** Always use year dictionary:
```python
"age": {2025: 35},
"employment_income": {2025: 30000}
```

### Pitfall 3: Wrong Region Format

**Problem:** Using lowercase or incorrect region names

**Solution:** Use uppercase ITL 1 region codes:
```python
# CORRECT regions:
"region": {2025: "LONDON"}
"region": {2025: "SCOTLAND"}
"region": {2025: "WALES"}
"region": {2025: "NORTH_EAST"}
"region": {2025: "SOUTH_EAST"}
```

### Pitfall 4: Axes Persistence

**Problem:** Axes remain in situation when creating single-point simulation

**Solution:** Remove axes before single-point simulation:
```python
situation_single = situation.copy()
situation_single.pop("axes", None)
```

### Pitfall 5: Missing Benunits

**Problem:** Forgetting to include benunits (benefit units)

**Solution:** Always include benunits in UK simulations:
```python
# UK requires benunits
situation = {
    "people": {...},
    "benunits": {"benunit": {"members": [...]}},  # Required!
    "households": {...}
}
```

## Regions in PolicyEngine UK

UK uses ITL 1 (International Territorial Level 1, formerly NUTS 1) regions:

**Regions:**
- `NORTH_EAST` - North East England
- `NORTH_WEST` - North West England
- `YORKSHIRE` - Yorkshire and the Humber
- `EAST_MIDLANDS` - East Midlands
- `WEST_MIDLANDS` - West Midlands
- `EAST_OF_ENGLAND` - East of England
- `LONDON` - London
- `SOUTH_EAST` - South East England
- `SOUTH_WEST` - South West England
- `WALES` - Wales
- `SCOTLAND` - Scotland
- `NORTHERN_IRELAND` - Northern Ireland

**Regional Tax Variations:**

**Scotland:**
- Has devolved income tax with 6 bands (starter 19%, basic 20%, intermediate 21%, higher 42%, advanced 45%, top 47%)
- Scottish residents automatically calculated with Scottish rates

**Wales:**
- Has Welsh Rate of Income Tax (WRIT)
- Currently maintains parity with England/NI rates

**England/Northern Ireland:**
- Standard UK rates: basic 20%, higher 40%, additional 45%

## Key Parameters and Values (2025/26)

### Income Tax
- **Personal Allowance:** £12,570
- **Basic rate threshold:** £50,270
- **Higher rate threshold:** £125,140
- **Rates:** 20% (basic), 40% (higher), 45% (additional)
- **Personal allowance tapering:** £1 reduction for every £2 over £100,000

### National Insurance (Class 1)
- **Lower Earnings Limit:** £6,396/year
- **Primary Threshold:** £12,570/year
- **Upper Earnings Limit:** £50,270/year
- **Rates:** 12% (between primary and upper), 2% (above upper)

### Universal Credit
- **Standard allowance:** Varies by single/couple and age
- **Taper rate:** 55% (rate at which UC reduced as income increases)
- **Work allowance:** Amount you can earn before UC reduced

### Child Benefit
- **First child:** Higher rate
- **Subsequent children:** Lower rate
- **High Income Charge:** Tapered withdrawal starting at £60,000

## Version Compatibility

- Use `policyengine-uk>=1.0.0` for 2025 calculations
- Check version: `import policyengine_uk; print(policyengine_uk.__version__)`
- Different years may require different package versions

## Debugging Tips

1. **Enable tracing:**
   ```python
   simulation.trace = True
   result = simulation.calculate("variable_name", 2025)
   ```

2. **Check intermediate calculations:**
   ```python
   gross_income = simulation.calculate("gross_income", 2025)
   disposable_income = simulation.calculate("disposable_income", 2025)
   ```

3. **Verify situation structure:**
   ```python
   import json
   print(json.dumps(situation, indent=2))
   ```

4. **Test with PolicyEngine web app:**
   - Go to policyengine.org/uk/household
   - Enter same inputs
   - Compare results

## Additional Resources

- **Documentation:** https://policyengine.org/uk/docs
- **API Reference:** https://github.com/PolicyEngine/policyengine-uk
- **Variable Explorer:** https://policyengine.org/uk/variables
- **Parameter Explorer:** https://policyengine.org/uk/parameters

## Examples Directory

See `examples/` for complete working examples:
- `single_person.yaml` - Single person household
- `couple.yaml` - Couple without children
- `family_with_children.yaml` - Family with dependents
- `universal_credit_sweep.yaml` - Analyzing UC with axes

## UK Legislation References

**All UK parameters MUST have legislation.gov.uk references** with exact section links.

### Finding Legislation References

UK legislation is consolidated at [legislation.gov.uk](https://www.legislation.gov.uk/). Key sources:

**Primary legislation (Acts of Parliament):**
- Welfare Reform Act 2012 - Universal Credit
- Social Security Contributions and Benefits Act 1992
- Income Tax Act 2007
- Taxation of Chargeable Gains Act 1992

**Secondary legislation (Statutory Instruments):**
- Universal Credit Regulations 2013 (SI 2013/376)
- The Social Security (Claims and Payments) Regulations 1987
- Income Tax (Earnings and Pensions) Act 2003

### Reference Format for UK Parameters

```yaml
metadata:
  reference:
    - title: Universal Credit Regulations 2013, Schedule 4, Table 3
      href: https://www.legislation.gov.uk/uksi/2013/376/schedule/4
    - title: Welfare Reform Act 2012, Section 8
      href: https://www.legislation.gov.uk/ukpga/2012/5/section/8
```

### Universal Credit Legislation References

Universal Credit parameters are primarily in:
- **The Universal Credit Regulations 2013 (SI 2013/376)**
  - Schedule 1: Capital limits and disregards
  - Schedule 4: Standard allowances and amounts
  - Schedule 5: Work capability amounts
  - Regulation 22: Work allowance

**Example - Standard Allowance:**
```yaml
# parameters/gov/dwp/universal_credit/standard_allowance/single/under_25.yaml
description: Standard allowance for single claimants under 25.
values:
  2024-04-01: 311.68
metadata:
  unit: currency-GBP
  period: month
  label: UC standard allowance (single, under 25)
  reference:
    - title: Universal Credit Regulations 2013, Schedule 4, Table 3
      href: https://www.legislation.gov.uk/uksi/2013/376/schedule/4
```

### Uprating Orders

UK benefits are uprated annually via Statutory Instruments. Current rates are in:
- **The Social Security Benefits Up-rating Order** (annual)
- **The Universal Credit (Transitional Provisions) (Amendment) Regulations** (as needed)

When updating parameter values, reference the specific uprating order:
```yaml
reference:
  - title: The Social Security Benefits Up-rating Order 2024, Schedule, Part II
    href: https://www.legislation.gov.uk/uksi/2024/217/schedule/part/II
```

### Finding the Right Section

1. Go to legislation.gov.uk
2. Search for the regulation (e.g., "Universal Credit Regulations 2013")
3. Navigate to the relevant section/schedule
4. Use the URL which includes the section (e.g., `/schedule/4` or `/section/8`)
5. Include section details in the title for clarity

## Key Differences from US System

1. **Benefit Units:** UK uses `benunits` (single/couple + children) instead of US multiple entity types
2. **Universal Credit:** Consolidated means-tested benefit (vs separate SNAP, TANF, etc. in US)
3. **National Insurance:** Separate from income tax with own thresholds (vs US Social Security tax)
4. **Devolved Taxes:** Scotland and Wales have different income tax rates
5. **Tax Year:** April 6 to April 5 (vs calendar year in US)
6. **No State Variation:** Council Tax is local, but most taxes/benefits are national (vs 50 US states)
