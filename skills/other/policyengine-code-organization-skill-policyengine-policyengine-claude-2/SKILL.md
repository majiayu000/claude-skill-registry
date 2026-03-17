---
name: policyengine-code-organization
description: Code organization patterns for PolicyEngine - variable naming conventions, folder structure, file organization
---

# PolicyEngine Code Organization

Patterns for organizing PolicyEngine code - naming conventions, folder structure, and file organization.

## Using the Variable Prefix

**The variable prefix is defined in `sources/working_references.md`.**

Look for this section:
```markdown
## Official Program Name

**Federal Program**: [Federal program name]
**State's Official Name**: [State's official name]
**Abbreviation**: [Abbreviation]
**Source**: [Legal citation]

**Variable Prefix**: `[state]_[abbreviation]`
```

**Use this prefix for all variable and parameter names.**

---

## Variable Naming Patterns

### State Programs

```python
# Pattern: {state}_{program}
az_liheap      # Arizona LIHEAP
ca_calfresh    # California CalFresh (SNAP)
ny_heap        # New York HEAP (LIHEAP)
ma_snap        # Massachusetts SNAP (uses federal name)

# Sub-variables: {state}_{program}_{component}
az_liheap_eligible
az_liheap_income_eligible
az_liheap_benefit_amount
```

### Federal Programs

```python
# Pattern: just {program}
snap
liheap
wic

# Sub-variables: {program}_{component}
snap_eligible
snap_gross_income
liheap_eligible
```

---

## Standard Variable Components

Use these standard suffixes with your variable prefix:

### Eligibility Variables
```yaml
{prefix}_eligible              # Final eligibility (combines all checks)
{prefix}_income_eligible       # Income eligibility
{prefix}_resource_eligible     # Resource/asset eligibility
{prefix}_categorical_eligible  # Categorical eligibility
{prefix}_demographic_eligible  # Age, household composition eligibility
{prefix}_immigration_eligible  # Immigration status eligibility
```

### Calculation Variables
```yaml
{prefix}                       # Final benefit amount
{prefix}_maximum_benefit       # Maximum possible benefit
{prefix}_countable_income      # Income after deductions
{prefix}_countable_earned_income
{prefix}_countable_unearned_income
{prefix}_gross_income          # Total income before deductions
```

### Deduction/Disregard Variables
```yaml
{prefix}_earned_income_disregard
{prefix}_work_expense_deduction
{prefix}_dependent_care_deduction
{prefix}_standard_deduction
```

### Threshold/Limit Variables
```yaml
{prefix}_income_limit
{prefix}_resource_limit
{prefix}_payment_standard
{prefix}_need_standard         # Use state's terminology
```

---

## State-Specific Terminology

**Use the terminology from `sources/working_references.md`.**

States use different terms for the same concepts:

| Concept | Possible Terms | Example |
|---------|---------------|---------|
| Benefit amount | Payment Standard, Need Standard, Grant Amount | `{prefix}_need_standard` |
| Income threshold | Gross Income Limit, GMI, Countable Income Limit | `{prefix}_gmi_limit` |
| Earnings deduction | Earned Income Disregard, Work Expense Deduction | `{prefix}_earned_income_disregard` |

**Match the exact terms from the documentation.**

---

## Folder Organization Principles

### Core Principles

1. **Group logically** - Files that relate to the same aspect should be together
2. **Don't create subfolder for 1 file** - If only 1 file for an aspect, keep it at parent level
3. **Final output at root** - The main benefit variable (e.g., `{prefix}.py`) stays at the program folder root

### Common Aspects (adapt to your program)

- `income/` - Income calculations, limits, deductions
- `eligibility/` - Eligibility checks
- `resources/` - Asset/resource calculations
- `deductions/` - Deductions and disregards

### Study Existing Implementations

Each program is different. Before organizing, look at similar programs in the codebase:
```bash
ls policyengine_us/variables/gov/states/{state}/{agency}/
```

---

## Folder Structure Patterns

### Small Program (~5 files) - Keep Flat
```
policyengine_us/variables/gov/states/{state}/{agency}/{program}/
├── {prefix}.py                    # Final benefit (at root)
├── {prefix}_eligible.py
├── {prefix}_income_eligible.py
├── {prefix}_maximum_benefit.py
└── {prefix}_countable_income.py
```

### Medium Program (6-15 files) - Light Organization
```
policyengine_us/variables/gov/states/{state}/{agency}/{program}/
├── {prefix}.py                    # Final benefit (at root)
├── eligibility/
│   ├── {prefix}_eligible.py
│   ├── {prefix}_income_eligible.py
│   └── {prefix}_resource_eligible.py
└── income/
    ├── {prefix}_countable_income.py
    └── {prefix}_gross_income.py
```

### Large Program (>15 files) - Full Structure
```
policyengine_us/variables/gov/states/{state}/{agency}/{program}/
├── {prefix}.py                    # Final benefit (at root)
├── eligibility/
│   ├── {prefix}_eligible.py
│   ├── {prefix}_income_eligible.py
│   ├── {prefix}_resource_eligible.py
│   └── {prefix}_demographic_eligible.py
├── income/
│   ├── {prefix}_countable_income.py
│   ├── {prefix}_countable_earned_income.py
│   └── {prefix}_gross_income.py
└── deductions/
    ├── {prefix}_earned_income_disregard.py
    └── {prefix}_work_expense_deduction.py
```

### Tests
```
policyengine_us/tests/policy/baseline/gov/states/{state}/{agency}/{program}/
├── {prefix}.yaml
├── {prefix}_eligible.yaml
├── {prefix}_income_eligible.yaml
└── integration.yaml          # Always named integration.yaml
```

---

## Finding Existing Examples

To see naming patterns from similar programs:

```bash
# Find state programs
ls policyengine_us/variables/gov/states/{state}/

# Find similar program implementations
grep -r "class {state}_" policyengine_us/variables/gov/states/{state}/ | head -10

# Check parameter structure
ls policyengine_us/parameters/gov/states/{state}/{agency}/{program}/
```

---

## Common Mistakes to Avoid

### Variable Names
```python
# ❌ WRONG - Using federal name when state has official name
ca_tanf_eligible          # California calls it CalWORKs

# ✅ CORRECT - Using state's official name
ca_calworks_eligible

# ❌ WRONG - Inconsistent naming
az_liheap_benefit
az_liheap_eligible_status  # Should be az_liheap_eligible

# ✅ CORRECT - Consistent pattern
az_liheap
az_liheap_eligible
```

### Test File Names
```yaml
# ❌ WRONG - Prefixed integration test
az_liheap_integration.yaml

# ✅ CORRECT - Standard integration test name
integration.yaml

# ❌ WRONG - Descriptive test names
test_low_income_family.yaml

# ✅ CORRECT - Variable-based test names
az_liheap.yaml
az_liheap_eligible.yaml
```

---

## Quick Reference

| Element | Pattern | Example |
|---------|---------|---------|
| Main benefit | `{prefix}` | `az_liheap` |
| Eligibility | `{prefix}_eligible` | `az_liheap_eligible` |
| Income eligibility | `{prefix}_income_eligible` | `az_liheap_income_eligible` |
| Maximum benefit | `{prefix}_maximum_benefit` | `az_liheap_maximum_benefit` |
| Integration test | `integration.yaml` | `integration.yaml` |
| Unit test | `{variable_name}.yaml` | `az_liheap_eligible.yaml` |
