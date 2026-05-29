---
name: policyengine-aggregation
description: PolicyEngine aggregation patterns - using adds attribute and add() function for summing variables across entities
---

# PolicyEngine Aggregation Patterns

Essential patterns for summing variables across entities in PolicyEngine.

## Quick Decision Guide

```
Is the variable ONLY a sum of other variables?
│
├─ YES → Use `adds` attribute (NO formula needed!)
│         adds = ["var1", "var2"]
│
└─ NO → Use `add()` function in formula
         (when you need max_, where, conditions, etc.)
```

## Quick Reference

| Need | Use | Example |
|------|-----|---------|
| Simple sum | `adds` | `adds = ["var1", "var2"]` |
| Sum from parameters | `adds` | `adds = "gov.path.to.list"` |
| Sum + max_() | `add()` | `max_(0, add(...))` |
| Sum + where() | `add()` | `where(cond, add(...), 0)` |
| Sum + conditions | `add()` | `if cond: add(...)` |
| Count booleans | `adds` | `adds = ["is_eligible"]` |

---

## 1. `adds` Class Attribute (Preferred When Possible)

### When to Use
Use `adds` when a variable is **ONLY** the sum of other variables with **NO additional logic**.

### Syntax
```python
class variable_name(Variable):
    value_type = float
    entity = Entity
    definition_period = PERIOD

    # Option 1: List of variables
    adds = ["variable1", "variable2", "variable3"]

    # Option 2: Parameter tree path
    adds = "gov.path.to.parameter.list"
```

### Key Points
- ✅ No `formula()` method needed
- ✅ Automatically handles entity aggregation (person → household/tax_unit/spm_unit)
- ✅ Clean and declarative

### Example: Simple Income Sum
```python
class tanf_gross_earned_income(Variable):
    value_type = float
    entity = SPMUnit
    label = "TANF gross earned income"
    unit = USD
    definition_period = MONTH

    adds = ["employment_income", "self_employment_income"]
    # NO formula needed! Automatically:
    # 1. Gets each person's employment_income
    # 2. Gets each person's self_employment_income
    # 3. Sums all values across SPM unit members
```

### Example: Using Parameter List
```python
class income_tax_refundable_credits(Variable):
    value_type = float
    entity = TaxUnit
    definition_period = YEAR

    adds = "gov.irs.credits.refundable"
    # Parameter file contains list like:
    # - earned_income_tax_credit
    # - child_tax_credit
    # - additional_child_tax_credit
```

### Example: Counting Boolean Values
```python
class count_eligible_people(Variable):
    value_type = int
    entity = SPMUnit
    definition_period = YEAR

    adds = ["is_eligible_person"]
    # Automatically sums True (1) and False (0) across members
```

---

## 2. `add()` Function (When Logic Needed)

### When to Use
Use `add()` inside a `formula()` when you need:
- To apply `max_()`, `where()`, or conditions
- To combine with other operations
- To modify values before/after summing

### Syntax
```python
from policyengine_us.model_api import *

def formula(entity, period, parameters):
    result = add(entity, period, variable_list)
```

**Parameters:**
- `entity`: The entity to operate on
- `period`: The time period for calculation
- `variable_list`: List of variable names or parameter path

### Example: With max_() to Prevent Negatives
```python
class adjusted_earned_income(Variable):
    value_type = float
    entity = SPMUnit
    definition_period = MONTH

    def formula(spm_unit, period, parameters):
        # Need max_() to clip negative values
        gross = add(spm_unit, period, ["employment_income", "self_employment_income"])
        return max_(0, gross)  # Prevent negative income
```

### Example: With Additional Logic
```python
class household_benefits(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR

    def formula(household, period, parameters):
        # Sum existing benefits
        BENEFITS = ["snap", "tanf", "ssi", "social_security"]
        existing = add(household, period, BENEFITS)

        # Add new benefit conditionally
        new_benefit = household("special_benefit", period)
        p = parameters(period).gov.special_benefit

        if p.include_in_total:
            return existing + new_benefit
        return existing
```

### Example: Building on Previous Variables
```python
class total_deductions(Variable):
    value_type = float
    entity = TaxUnit
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.irs.deductions

        # Get standard deductions using parameter list
        standard = add(tax_unit, period, p.standard_items)

        # Apply phase-out logic
        income = tax_unit("adjusted_gross_income", period)
        phase_out_rate = p.phase_out_rate
        phase_out_start = p.phase_out_start

        reduction = max_(0, (income - phase_out_start) * phase_out_rate)
        return max_(0, standard - reduction)
```

---

## 3. Common Anti-Patterns to Avoid

### ❌ NEVER: Manual Summing
```python
# WRONG - Never do this!
def formula(spm_unit, period, parameters):
    person = spm_unit.members
    employment = person("employment_income", period)
    self_emp = person("self_employment_income", period)
    return spm_unit.sum(employment + self_emp)  # ❌ BAD
```

### ✅ CORRECT: Use adds
```python
# RIGHT - Clean and simple
adds = ["employment_income", "self_employment_income"]  # ✅ GOOD
```

### ❌ WRONG: Using add() When adds Suffices
```python
# WRONG - Unnecessary complexity
def formula(spm_unit, period, parameters):
    return add(spm_unit, period, ["income1", "income2"])  # ❌ Overkill
```

### ✅ CORRECT: Use adds
```python
# RIGHT - Simpler
adds = ["income1", "income2"]  # ✅ GOOD
```

---

## 4. Entity Aggregation Explained

When using `adds` or `add()`, PolicyEngine automatically handles entity aggregation:

```python
class household_total_income(Variable):
    entity = Household  # Higher-level entity
    definition_period = YEAR

    adds = ["employment_income", "self_employment_income"]
    # employment_income is defined for Person (lower-level)
    # PolicyEngine automatically:
    # 1. Gets employment_income for each person in household
    # 2. Gets self_employment_income for each person
    # 3. Sums all values to household level
```

This works across all entity hierarchies:
- Person → Tax Unit
- Person → SPM Unit
- Person → Household
- Tax Unit → Household
- SPM Unit → Household

---

## 5. Parameter Lists

Parameters can define lists of variables to sum:

**Parameter file** (`gov/irs/credits/refundable.yaml`):
```yaml
description: List of refundable tax credits
values:
  2024-01-01:
    - earned_income_tax_credit
    - child_tax_credit
    - additional_child_tax_credit
```

**Usage in variable**:
```python
adds = "gov.irs.credits.refundable"
# Automatically sums all credits in the list
```

---

## 6. Decision Matrix

| Scenario | Solution | Code |
|----------|----------|------|
| Sum 2-3 variables | `adds` attribute | `adds = ["var1", "var2"]` |
| Sum many variables | Parameter list | `adds = "gov.path.list"` |
| Sum + prevent negatives | `add()` with `max_()` | `max_(0, add(...))` |
| Sum + conditional | `add()` with `where()` | `where(eligible, add(...), 0)` |
| Sum + phase-out | `add()` with calculation | `add(...) - reduction` |
| Count people/entities | `adds` with boolean | `adds = ["is_child"]` |

---

## 7. Key Principles

1. **Default to `adds` attribute** when variable is only a sum
2. **Use `add()` function** only when additional logic is needed
3. **Never manually sum** with `entity.sum(person(...) + person(...))`
4. **Let PolicyEngine handle** entity aggregation automatically
5. **Use parameter lists** for maintainable, configurable sums

---

## Related Skills

- **policyengine-period-patterns-skill**: For period conversion when summing across different time periods
- **policyengine-core-skill**: For understanding entity hierarchies and relationships

---

## For Agents

When implementing or reviewing code:

1. **Check if `adds` can be used** before writing a formula
2. **Prefer declarative over imperative** when possible
3. **Follow existing patterns** in the codebase
4. **Test entity aggregation** carefully in YAML tests
5. **Document parameter lists** clearly for `adds` references

---

## Common Use Cases

### Earned Income
```python
adds = ["employment_income", "self_employment_income"]
```

### Unearned Income
```python
adds = ["interest_income", "dividend_income", "rental_income"]
```

### Total Benefits
```python
adds = ["snap", "tanf", "wic", "ssi", "social_security"]
```

### Tax Credits
```python
adds = "gov.irs.credits.refundable"
```

### Counting Children
```python
adds = ["is_child"]  # Returns count of children
```