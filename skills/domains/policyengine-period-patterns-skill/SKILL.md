---
name: policyengine-period-patterns
description: PolicyEngine period handling - converting between YEAR, MONTH definition periods and testing patterns
---

# PolicyEngine Period Patterns

Essential patterns for handling different definition periods (YEAR, MONTH) in PolicyEngine.

## Quick Reference

| From | To | Method | Example |
|------|-----|--------|---------|
| MONTH formula | YEAR variable | `period.this_year` | `age = person("age", period.this_year)` |
| YEAR formula | MONTH variable | `period.first_month` | `person("monthly_rent", period.first_month)` |
| Any | Year integer | `period.start.year` | `year = period.start.year` |
| Any | Month integer | `period.start.month` | `month = period.start.month` |
| Annual → Monthly | Divide by 12 | `/ MONTHS_IN_YEAR` | `monthly = annual / 12` |
| Monthly → Annual | Multiply by 12 | `* MONTHS_IN_YEAR` | `annual = monthly * 12` |

---

## 1. Definition Periods in PolicyEngine US

### Available Periods
- **YEAR**: Annual values (most common - 2,883 variables)
- **MONTH**: Monthly values (395 variables)
- **ETERNITY**: Never changes (1 variable - structural relationships)

**Note:** QUARTER is NOT used in PolicyEngine US

### Examples
```python
from policyengine_us.model_api import *

class annual_income(Variable):
    definition_period = YEAR  # Annual amount

class monthly_benefit(Variable):
    definition_period = MONTH  # Monthly amount

class is_head(Variable):
    definition_period = ETERNITY  # Never changes
```

---

## 2. The Golden Rule

**When accessing a variable with a different definition period than your formula, you must specify the target period explicitly.**

```python
# ✅ CORRECT - MONTH formula accessing YEAR variable
def formula(person, period, parameters):
    age = person("age", period.this_year)  # Gets actual age

# ❌ WRONG - Would get age/12
def formula(person, period, parameters):
    age = person("age", period)  # BAD: gives age divided by 12!
```

---

## 3. Common Patterns

### Pattern 1: MONTH Formula Accessing YEAR Variable

**Use Case**: Monthly benefits need annual demographic data

```python
class monthly_benefit_eligible(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH  # Monthly eligibility

    def formula(person, period, parameters):
        # Age is YEAR-defined, use period.this_year
        age = person("age", period.this_year)  # ✅ Gets full age

        # is_pregnant is MONTH-defined, just use period
        is_pregnant = person("is_pregnant", period)  # ✅ Same period

        return (age < 18) | is_pregnant
```

### Pattern 2: Accessing Stock Variables (Assets)

**Stock variables** (point-in-time values like assets) are typically YEAR-defined

```python
class tanf_countable_resources(Variable):
    value_type = float
    entity = SPMUnit
    definition_period = MONTH  # Monthly check

    def formula(spm_unit, period, parameters):
        # Assets are stocks (YEAR-defined)
        cash = spm_unit("cash_assets", period.this_year)  # ✅
        vehicles = spm_unit("vehicles_value", period.this_year)  # ✅

        p = parameters(period).gov.tanf.resources
        return cash + max_(0, vehicles - p.vehicle_exemption)
```

---

## 4. Understanding Auto-Conversion: When to Use `period` vs `period.this_year`

### The Key Question

**When accessing a YEAR variable from a MONTH formula, should the value be divided by 12?**

- **If YES** → Use `period` (let auto-conversion happen)
- **If NO** → Use `period.this_year` (prevent auto-conversion)

### When Auto-Conversion Makes Sense (Use `period`)

**Flow variables** where you want the monthly portion:

```python
class monthly_benefit(Variable):
    definition_period = MONTH

    def formula(person, period, parameters):
        # ✅ Use period - want $2,000/month from $24,000/year
        monthly_income = person("employment_income", period)

        # Compare to monthly threshold
        p = parameters(period).gov.program
        return monthly_income < p.monthly_threshold
```

Why: If annual income is $24,000, you want $2,000/month for monthly eligibility checks.

### When Auto-Conversion Breaks Things (Use `period.this_year`)

**Stock variables and counts** where division by 12 is nonsensical:

**1. Age**
```python
# ❌ WRONG - gives age/12
age = person("age", period)  # 30 years → 2.5 "monthly age" ???

# ✅ CORRECT - gives actual age
age = person("age", period.this_year)  # 30 years
```

**2. Assets/Resources (Stocks)**
```python
# ❌ WRONG - gives assets/12
assets = spm_unit("spm_unit_assets", period)  # $12,000 → $1,000 ???

# ✅ CORRECT - gives point-in-time value
assets = spm_unit("spm_unit_assets", period.this_year)  # $12,000
```

**3. Counts (Household Size, Number of Children)**
```python
# ❌ WRONG - gives count/12
size = spm_unit("household_size", period)  # 4 people → 0.33 people ???

# ✅ CORRECT - gives actual count
size = spm_unit("household_size", period.this_year)  # 4 people
```

**4. Boolean/Enum Variables**
```python
# ❌ WRONG - weird fractional conversion
status = person("is_disabled", period)

# ✅ CORRECT - actual status
status = person("is_disabled", period.this_year)
```

### Decision Tree

```
Accessing YEAR variable from MONTH formula?
│
├─ Is it an INCOME or FLOW variable?
│  └─ YES → Use period (auto-convert to monthly) ✅
│           Example: employment_income, self_employment_income
│
└─ Is it AGE, ASSET, COUNT, or BOOLEAN?
   └─ YES → Use period.this_year (prevent conversion) ✅
            Examples: age, assets, household_size, is_disabled
```

### Complete Example

```python
class monthly_tanf_eligible(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH

    def formula(person, period, parameters):
        # Age: Use period.this_year (don't want age/12)
        age = person("age", period.this_year)  # ✅

        # Assets: Use period.this_year (don't want assets/12)
        assets = person("assets", period.this_year)  # ✅

        # Income: Use period (DO want monthly income from annual)
        monthly_income = person("employment_income", period)  # ✅

        p = parameters(period).gov.tanf.eligibility

        age_eligible = (age >= 18) & (age <= 64)
        asset_eligible = assets <= p.asset_limit
        income_eligible = monthly_income <= p.monthly_income_limit

        return age_eligible & asset_eligible & income_eligible
```

### Quick Reference for Auto-Conversion

| Variable Type | Use `period` | Use `period.this_year` | Why |
|--------------|-------------|----------------------|-----|
| Income (flow) | ✅ | ❌ | Want monthly portion |
| Age | ❌ | ✅ | Age/12 is meaningless |
| Assets/Resources (stock) | ❌ | ✅ | Point-in-time value |
| Household size/counts | ❌ | ✅ | Can't divide people |
| Boolean/status flags | ❌ | ✅ | True/12 is nonsense |
| Demographic attributes | ❌ | ✅ | Properties don't divide |

**Rule of thumb:** If dividing by 12 makes the value meaningless → use `period.this_year`

### Pattern 3: Converting Annual to Monthly

```python
class monthly_income_limit(Variable):
    definition_period = MONTH

    def formula(household, period, parameters):
        # Get annual parameter
        annual_limit = parameters(period).gov.program.annual_limit

        # Convert to monthly
        monthly_limit = annual_limit / MONTHS_IN_YEAR  # ✅

        return monthly_limit
```

### Pattern 4: Getting Period Components

```python
class federal_poverty_guideline(Variable):
    definition_period = MONTH

    def formula(entity, period, parameters):
        # Get year and month as integers
        year = period.start.year  # e.g., 2024
        month = period.start.month  # e.g., 1-12

        # FPG updates October 1st
        if month >= 10:
            instant_str = f"{year}-10-01"
        else:
            instant_str = f"{year - 1}-10-01"

        # Access parameters at specific date
        p_fpg = parameters(instant_str).gov.hhs.fpg
        return p_fpg.first_person / MONTHS_IN_YEAR
```

---

## 5. Parameter Access

### Standard Access
```python
def formula(entity, period, parameters):
    # Parameters use current period
    p = parameters(period).gov.program.benefit
    return p.amount
```

### Specific Date Access
```python
def formula(entity, period, parameters):
    # Access parameters at specific instant
    p = parameters("2024-10-01").gov.hhs.fpg
    return p.amount
```

**Important**: Never use `parameters(period.this_year)` - parameters always use the formula's period

---

## 6. Testing with Different Periods

### Critical Testing Rules

**For MONTH period tests** (`period: 2025-01`):
- **Input** YEAR variables as **annual amounts**
- **Output** YEAR variables show **monthly values** (÷12)

### Test Examples

**Example 1: Basic MONTH Test**
```yaml
- name: Monthly income test
  period: 2025-01  # MONTH period
  input:
    people:
      person1:
        employment_income: 12_000  # Input: Annual
  output:
    employment_income: 1_000  # Output: Monthly (12_000/12)
```

**Example 2: Mixed Variables**
```yaml
- name: Eligibility with age and income
  period: 2024-01  # MONTH period
  input:
    age: 30  # Age doesn't convert
    employment_income: 24_000  # Annual input
  output:
    age: 30  # Age stays same
    employment_income: 2_000  # Monthly output
    monthly_eligible: true
```

**Example 3: YEAR Period Test**
```yaml
- name: Annual calculation
  period: 2024  # YEAR period
  input:
    employment_income: 18_000  # Annual
  output:
    employment_income: 18_000  # Annual output
    annual_tax: 2_000
```

### Testing Best Practices

1. **Always specify period explicitly**
2. **Input YEAR variables as annual amounts**
3. **Expect monthly output for YEAR variables in MONTH tests**
4. **Use underscore separators**: `12_000` not `12000`
5. **Add calculation comments** in integration tests

---

## 7. Common Mistakes and Solutions

### ❌ Mistake 1: Not Using period.this_year
```python
# WRONG - From MONTH formula
def formula(person, period, parameters):
    age = person("age", period)  # Gets age/12!

# CORRECT
def formula(person, period, parameters):
    age = person("age", period.this_year)  # Gets actual age
```

### ❌ Mistake 2: Mixing Annual and Monthly
```python
# WRONG - Comparing different units
monthly_income = person("monthly_income", period)
annual_limit = parameters(period).gov.limit
if monthly_income < annual_limit:  # BAD comparison

# CORRECT - Convert to same units
monthly_income = person("monthly_income", period)
annual_limit = parameters(period).gov.limit
monthly_limit = annual_limit / MONTHS_IN_YEAR
if monthly_income < monthly_limit:  # Good comparison
```

### ❌ Mistake 3: Wrong Test Expectations
```yaml
# WRONG - Expecting annual in MONTH test
period: 2024-01
input:
  employment_income: 12_000
output:
  employment_income: 12_000  # Wrong!

# CORRECT
period: 2024-01
input:
  employment_income: 12_000  # Annual input
output:
  employment_income: 1_000  # Monthly output
```

---

## 8. Quick Patterns Cheat Sheet

### Accessing Variables
| Your Formula | Target Variable | Use |
|--------------|-----------------|-----|
| MONTH | YEAR | `period.this_year` |
| YEAR | MONTH | `period.first_month` |
| Any | ETERNITY | `period` |

### Common Variables That Need period.this_year
- `age`
- `household_size`, `spm_unit_size`
- `cash_assets`, `vehicles_value`
- `state_name`, `state_code`
- Any demographic variable

### Period Conversion
```python
# Annual to monthly
monthly = annual / MONTHS_IN_YEAR

# Monthly to annual
annual = monthly * MONTHS_IN_YEAR

# Get year/month numbers
year = period.start.year  # 2024
month = period.start.month  # 1-12
```

---

## 9. Real-World Example

```python
class tanf_income_eligible(Variable):
    value_type = bool
    entity = SPMUnit
    definition_period = MONTH  # Monthly eligibility

    def formula(spm_unit, period, parameters):
        # YEAR variables need period.this_year
        household_size = spm_unit("spm_unit_size", period.this_year)
        state = spm_unit.household("state_code", period.this_year)

        # MONTH variables use period
        gross_income = spm_unit("tanf_gross_income", period)

        # Parameters use period
        p = parameters(period).gov.states[state].tanf

        # Convert annual limit to monthly
        annual_limit = p.income_limit[household_size]
        monthly_limit = annual_limit / MONTHS_IN_YEAR

        return gross_income <= monthly_limit
```

---

## 10. Checklist for Period Handling

When writing a formula:

- [ ] Identify your formula's `definition_period`
- [ ] Check `definition_period` of accessed variables
- [ ] Use `period.this_year` for YEAR variables from MONTH formulas
- [ ] Use `period` for parameters (not `period.this_year`)
- [ ] Convert units when comparing (annual ↔ monthly)
- [ ] Test with appropriate period values

---

## Related Skills

- **policyengine-aggregation-skill**: For summing across entities with period handling
- **policyengine-core-skill**: For understanding variable and parameter systems

---

## For Agents

1. **Always check definition_period** before accessing variables
2. **Default to period.this_year** for demographic/stock variables from MONTH formulas
3. **Test thoroughly** - period mismatches cause subtle bugs
4. **Document period conversions** in comments
5. **Follow existing patterns** in similar variables