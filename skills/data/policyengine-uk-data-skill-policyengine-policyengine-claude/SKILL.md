---
name: policyengine-uk-data
description: UK survey data enhancement - FRS with WAS imputation patterns
---

# PolicyEngine UK Data

PolicyEngine UK Data provides enhanced Family Resources Survey (FRS) datasets with imputed variables from the Wealth and Assets Survey (WAS).

## For Users

### What is policyengine-uk-data?

PolicyEngine UK uses the Family Resources Survey (FRS) as its primary microdata source. The FRS contains household demographics, income, and benefits but lacks detailed wealth information. The Wealth and Assets Survey (WAS) provides comprehensive wealth data but has a smaller sample. This package imputes wealth variables from WAS to FRS.

**Key datasets:**
- **FRS (Family Resources Survey):** Main UK household survey with ~20,000 households
- **WAS (Wealth and Assets Survey):** Detailed wealth survey with ~20,000 households
- **Enhanced FRS:** FRS with imputed wealth variables from WAS

## For Analysts

### Repository

**Location:** PolicyEngine/policyengine-uk-data

**Clone:**
```bash
git clone https://github.com/PolicyEngine/policyengine-uk-data
cd policyengine-uk-data
```

### Structure

```
policyengine_uk_data/
├── datasets/          # Dataset definitions
│   └── frs/          # FRS enhancement
│       ├── raw_frs.py           # Raw FRS loader
│       ├── calibration.py       # Weight calibration
│       └── imputations/         # Variable imputation
│           ├── wealth.py        # WAS wealth imputation
│           ├── student_loans.py # Student loan balances
│           └── ...
└── storage/          # Data storage utilities
```

### Installation

**From PyPI:**
```bash
pip install policyengine-uk-data
```

**Development:**
```bash
pip install -e .
```

## For Contributors

### Imputation Pattern

The standard pattern for adding WAS-to-FRS imputations:

**1. Identify the variables:**
- Source: WAS variables (complete wealth data)
- Target: FRS (needs these variables)
- Common variables: Demographics that exist in both surveys

**2. Follow the `wealth.py` pattern:**

```python
# In policyengine_uk_data/datasets/frs/imputations/my_variable.py

from policyengine_uk_data.datasets.frs.imputations.imputation_utils import (
    impute_from_was
)

def add_my_variable(frs, was):
    """
    Impute my_variable from WAS to FRS.

    Args:
        frs: Enhanced FRS DataFrame
        was: WAS DataFrame with target variable

    Returns:
        Enhanced FRS with imputed variable
    """
    return impute_from_was(
        donor=was,
        recipient=frs,
        target_variable='my_variable',
        common_variables=[
            'age',
            'region',
            'employment_status',
            # Add relevant predictors
        ],
        method='quantile_forest'  # Or other microimpute method
    )
```

**3. Update the RENAMES dictionary:**

If the variable has different names in WAS vs FRS:

```python
# In the relevant module
RENAMES = {
    "was_variable_name": "standardized_name",
    "frs_variable_name": "standardized_name",
}
```

**4. Add to the pipeline:**

Register the imputation in the FRS enhancement pipeline so it runs automatically.

### Example: Student Loan Imputation

The recent PR #252 added student loan balance imputation:

```python
# policyengine_uk_data/datasets/frs/imputations/student_loans.py

def add_student_loan_balance(frs, was):
    """
    Impute student loan balances from WAS to FRS.

    WAS contains:
    - total_loans: All loan balances
    - total_loans_exc_slc: Loans excluding student loans

    Derived variable:
    - student_loan_balance = total_loans - total_loans_exc_slc
    """
    return impute_from_was(
        donor=was,
        recipient=frs,
        target_variable='student_loan_balance',
        common_variables=[
            'age',
            'highest_qualification',
            'region',
            'employment_status',
            'income'
        ],
        method='quantile_forest'
    )
```

### Common Variables for WAS-FRS Imputation

**Demographics (always available):**
- age
- sex
- region (UK region codes)

**Economic status:**
- employment_status
- income (or income bands)
- hours_worked

**Household:**
- household_size
- num_children
- tenure_type (own/rent)

**Education:**
- highest_qualification
- currently_studying

### Testing

**Run tests:**
```bash
make test

# Or pytest directly
pytest policyengine_uk_data/tests/ -v
```

**Test structure:**
```bash
# Check if imputation was added
pytest policyengine_uk_data/tests/test_imputations.py::test_student_loan_imputation
```

### Validation

After adding an imputation, validate:

**1. Distribution check:**
```python
# Compare imputed FRS distribution to WAS source
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.hist(was['my_variable'], bins=50)
ax1.set_title('WAS (source)')
ax2.hist(frs_imputed['my_variable'], bins=50)
ax2.set_title('FRS (imputed)')
```

**2. Aggregate totals:**
```python
# Check population-weighted totals match administrative data
weighted_total = (frs_imputed['my_variable'] * frs_imputed['weight']).sum()
print(f"Imputed total: {weighted_total:,.0f}")
# Compare to known UK aggregate
```

**3. Conditional relationships:**
```python
# Verify relationships are preserved
# E.g., student loan balance by age and qualification
frs_imputed.groupby(['age_band', 'qualification'])['student_loan_balance'].mean()
```

## Common Patterns

### Pattern 1: Simple Variable Imputation

```python
# Most common: direct variable imputation
def add_variable(frs, was):
    return impute_from_was(
        donor=was,
        recipient=frs,
        target_variable='my_var',
        common_variables=['age', 'income', 'region']
    )
```

### Pattern 2: Derived Variable Imputation

```python
# When WAS has components but not the exact variable
def add_derived_variable(frs, was):
    # First derive the variable in WAS
    was['net_wealth'] = was['total_assets'] - was['total_debts']

    # Then impute
    return impute_from_was(
        donor=was,
        recipient=frs,
        target_variable='net_wealth',
        common_variables=['age', 'income', 'region']
    )
```

### Pattern 3: Multiple Related Variables

```python
# Impute several related variables together
def add_wealth_components(frs, was):
    variables = [
        'property_wealth',
        'financial_wealth',
        'pension_wealth',
        'debt'
    ]

    for var in variables:
        frs = impute_from_was(
            donor=was,
            recipient=frs,
            target_variable=var,
            common_variables=['age', 'income', 'region']
        )

    return frs
```

## Integration with PolicyEngine UK

**Usage flow:**
```
1. Load raw FRS
   ↓
2. Add WAS imputations (wealth, student loans, etc.)
   ↓
3. Calibrate weights to administrative benchmarks
   ↓
4. Validate against known UK totals
   ↓
5. Package for policyengine-uk
   ↓
6. Use for UK policy simulations
```

**In policyengine-uk:**
```python
from policyengine_uk import Microsimulation

# Uses enhanced FRS under the hood
sim = Microsimulation()
sim.calculate('student_loan_repayment', period='2024')
# Uses imputed student_loan_balance variable
```

## Related Skills

- **microimpute-skill** - ML imputation methods (underlying technique)
- **policyengine-uk-skill** - UK policy model (uses this data)
- **microcalibrate-skill** - Weight calibration (next step after imputation)
- **microdf-skill** - Working with survey microdata

## Resources

**Repository:** https://github.com/PolicyEngine/policyengine-uk-data
**Dependencies:** policyengine-uk, policyengine-core, microdf, microimpute
**Data sources:**
- FRS: https://www.gov.uk/government/collections/family-resources-survey
- WAS: https://www.ons.gov.uk/surveys/informationforhouseholdsandindividuals/householdandindividualsurveys/wealthandassetssurvey
