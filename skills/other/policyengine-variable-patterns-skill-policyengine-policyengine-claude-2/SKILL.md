---
name: policyengine-variable-patterns
description: PolicyEngine variable patterns - variable creation, no hard-coding principle, federal/state separation, metadata standards
---

# PolicyEngine Variable Patterns

Essential patterns for creating PolicyEngine variables for government benefit programs.

## FIRST PRINCIPLE: Legal Code is the Source of Truth

**The law defines WHAT to implement. These patterns are just HOW to implement it.**

```
1. READ the legal code/policy manual FIRST
2. UNDERSTAND what the law actually says
3. IMPLEMENT exactly what the law requires
4. USE these patterns as tools to implement correctly
```

**Patterns are tools, not rules to blindly follow:**
- If the legal code says something different from common patterns → **FOLLOW THE LAW**
- If another state does it differently → **Check YOUR state's legal code**
- If a pattern doesn't fit the regulation → **Implement what the law says**

**Every implementation decision should trace back to a specific legal citation.**

---

## PolicyEngine Architecture Constraints

### What CANNOT Be Simulated (Single-Period Limitation)

**CRITICAL: PolicyEngine uses single-period simulation architecture**

The following CANNOT be implemented and should be SKIPPED when found in documentation:

#### 1. Time Limits and Lifetime Counters
**Cannot simulate:**
- ANY lifetime benefit limits (X months total)
- ANY time windows (X months within Y period)
- Benefit clocks and countable months
- Cumulative time tracking

**Why:** Requires tracking benefit history across multiple periods. PolicyEngine simulates one period at a time with no state persistence.

**What to do:** Document in comments but DON'T parameterize or implement:
```python
# NOTE: [State] has [X]-month lifetime limit on [Program] benefits
# This cannot be simulated in PolicyEngine's single-period architecture
```

#### 2. Work History Requirements
**Cannot simulate:**
- "Must have worked 6 of last 12 months"
- "Averaged 30 hours/week over past quarter"
- Prior employment verification
- Work participation rate tracking

**Why:** Requires historical data from previous periods.

#### 3. Waiting Periods and Benefit Delays
**Cannot simulate:**
- "3-month waiting period for new residents"
- "Benefits start month after application"
- Retroactive eligibility
- Benefit recertification cycles

**Why:** Requires tracking application dates and eligibility history.

#### 4. Progressive Sanctions and Penalties
**Cannot simulate:**
- "First violation: 1-month sanction, Second: 3-month, Third: permanent"
- Graduated penalties
- Strike systems

**Why:** Requires tracking violation history.

#### 5. Asset Spend-Down Over Time
**Cannot simulate:**
- Medical spend-down across months
- Resource depletion tracking
- Accumulated medical expenses

**Why:** Requires tracking expenses and resources across periods.

### What CAN Be Simulated (With Caveats)

PolicyEngine CAN simulate point-in-time eligibility and benefits:
- ✅ Current month income limits
- ✅ Current month resource limits
- ✅ Current benefit calculations
- ✅ Current household composition
- ✅ Current deductions and disregards

### Time-Limited Benefits That Affect Current Calculations

**Special Case: Time-limited deductions/disregards**

When a deduction or disregard is only available for X months:
- **DO implement the deduction** (assume it applies)
- **DO add a comment** explaining the time limitation
- **DON'T try to track or enforce the time limit**

Example:
```python
class state_tanf_countable_earned_income(Variable):
    def formula(spm_unit, period, parameters):
        p = parameters(period).gov.states.xx.tanf.income
        earned = spm_unit("tanf_gross_earned_income", period)

        # NOTE: In reality, this 75% disregard only applies for first 4 months
        # of employment. PolicyEngine cannot track employment duration, so we
        # apply the disregard assuming the household qualifies.
        # Actual rule: [State Code Citation]
        disregard_rate = p.earned_income_disregard_rate  # 0.75

        return earned * (1 - disregard_rate)
```

**Rule: If it requires history or future tracking, it CANNOT be fully simulated - but implement what we can and document limitations**

---

## Critical Principles

### 1. ZERO Hard-Coded Values
**Every numeric value MUST be parameterized**

```python
❌ FORBIDDEN:
return where(eligible, 1000, 0)     # Hard-coded 1000
age < 15                             # Hard-coded 15
benefit = income * 0.33              # Hard-coded 0.33
month >= 10 and month <= 3           # Hard-coded months

✅ REQUIRED:
return where(eligible, p.maximum_benefit, 0)
age < p.age_threshold.minor_child
benefit = income * p.benefit_rate
month >= p.season.start_month
```

**Acceptable literals:**
- `0`, `1`, `-1` for basic math
- `12` for month conversion (`/ 12`, `* 12`)
- Array indices when structure is known

### 2. No Placeholder Implementations
**Delete the file rather than leave placeholders**

```python
❌ NEVER:
def formula(entity, period, parameters):
    # TODO: Implement
    return 75  # Placeholder

✅ ALWAYS:
# Complete implementation or no file at all
```

### 3. Use `adds` or `add()` - NEVER Manual Addition

**CRITICAL: NEVER manually fetch variables and add them with `+`. Always use `adds` or `add()`.**

#### Rule 1: Pure sum → `adds` attribute (no formula)

```python
❌ WRONG - Writing a formula for simple sum:
class tx_tanf_gross_income(Variable):
    def formula(spm_unit, period, parameters):
        earned = spm_unit("tanf_gross_earned_income", period)
        unearned = spm_unit("tanf_gross_unearned_income", period)
        return earned + unearned  # DON'T DO THIS!

✅ CORRECT - Use adds, no formula needed:
class tx_tanf_gross_income(Variable):
    value_type = float
    entity = SPMUnit
    definition_period = MONTH
    adds = ["tanf_gross_earned_income", "tanf_gross_unearned_income"]
    # NO formula method - adds handles it automatically!
```

#### Rule 2: Sum + other operations → `add()` function

```python
❌ WRONG - Manual fetching and adding:
def formula(spm_unit, period, parameters):
    earned = spm_unit("tanf_gross_earned_income", period)
    unearned = spm_unit("tanf_gross_unearned_income", period)
    gross = earned + unearned  # DON'T manually add!
    return gross * p.rate

✅ CORRECT - Use add() function:
def formula(spm_unit, period, parameters):
    gross = add(spm_unit, period, ["tanf_gross_earned_income", "tanf_gross_unearned_income"])
    return gross * p.rate
```

**Decision rule:**
- Is it ONLY a sum? → `adds = [...]` (no formula)
- Sum + other operations? → `add()` function inside formula

**See policyengine-aggregation-skill for detailed patterns.**

---

## Variable Implementation Standards

### Variable Metadata Format

Follow established patterns:
```python
class il_tanf_countable_earned_income(Variable):
    value_type = float
    entity = SPMUnit
    definition_period = MONTH
    label = "Illinois TANF countable earned income"
    unit = USD
    reference = "https://www.law.cornell.edu/regulations/illinois/..."
    defined_for = StateCode.IL

    # Use adds for simple sums
    adds = ["il_tanf_earned_income_after_disregard"]
```

**Key rules:**
- ✅ Use full URL in `reference` (clickable)
- ✅ For PDF links, include page number: `#page=XX`
- ✅ For multiple references, use TUPLE `()` not list `[]`
- ❌ **Don't use `documentation` field** - use `reference` instead
- ❌ Don't use statute citations without URLs

**❌ WRONG - Don't use documentation field:**
```python
class some_variable(Variable):
    documentation = "This is the wrong field"  # DON'T USE THIS
```

**✅ CORRECT - Use reference field:**
```python
class some_variable(Variable):
    reference = "https://example.gov/rules.pdf#page=10"  # USE THIS
```

**Reference format:**
```python
# Single reference:
reference = "https://oregon.gov/dhs/tanf-manual.pdf#page=23"

# Multiple references - use TUPLE ():
reference = (
    "https://oregon.public.law/rules/oar_461-155-0030",
    "https://oregon.gov/dhs/tanf-manual.pdf#page=23",
)

# ❌ WRONG - Don't use list []:
reference = [
    "https://...",
    "https://...",
]
```

### When to Use `adds` vs `formula`

**CRITICAL: Never use both `adds`/`subtracts` AND a custom `formula` in the same variable!**

This causes bugs when the two get out of sync. Choose one approach:

```python
❌ FORBIDDEN - Mixing compositional and formula:
class household_net_income(Variable):
    subtracts = ["employee_pension_contributions"]  # ❌ Has subtracts

    def formula(household, period):  # ❌ AND has formula
        gross = household("household_gross_income", period)
        tax = household("income_tax", period)
        # BUG: Forgot to subtract employee_pension_contributions!
        return gross - tax
```

**Use `adds`/`subtracts` when:**
- Just summing variables
- Passing through a single variable
- No transformations needed

```python
✅ BEST - Pure compositional:
class tanf_gross_income(Variable):
    adds = ["employment_income", "self_employment_income"]

✅ BEST - Compositional with subtracts:
class household_net_income(Variable):
    adds = ["household_gross_income"]
    subtracts = ["income_tax", "employee_pension_contributions"]
```

**Use `formula` when:**
- Applying transformations
- Conditional logic
- Calculations needed

```python
✅ CORRECT - Pure formula:
def formula(entity, period, parameters):
    income = add(entity, period, ["income1", "income2"])
    return max_(0, income)  # Need max_
```

---

## TANF Countable Income Pattern

### Critical: Verify Calculation Order from Legal Code

**MOST IMPORTANT:** Always check the state's legal code or policy manual for the exact calculation order. The pattern below is typical but not universal.

**The Typical Pattern:**
1. Apply deductions/disregards to **earned income only**
2. Use `max_()` to prevent negative earned income
3. Add unearned income (which typically has no deductions)

**This pattern is based on how MOST TANF programs work, but you MUST verify with the specific state's legal code.**

### ❌ WRONG - Applying deductions to total income

```python
def formula(spm_unit, period, parameters):
    gross_earned = spm_unit("tanf_gross_earned_income", period)
    unearned = spm_unit("tanf_gross_unearned_income", period)
    deductions = spm_unit("tanf_earned_income_deductions", period)

    # ❌ WRONG: Deductions applied to total income
    total_income = gross_earned + unearned
    countable = total_income - deductions

    return max_(countable, 0)
```

**Why this is wrong:**
- Deductions should ONLY reduce earned income
- Unearned income (SSI, child support, etc.) is not subject to work expense deductions
- This incorrectly reduces unearned income when earned income is low

**Example error:**
- Earned: $100, Unearned: $500, Deductions: $200
- Wrong result: `max_($100 + $500 - $200, 0) = $400` (reduces unearned!)
- Correct result: `max_($100 - $200, 0) + $500 = $500`

### ✅ CORRECT - Apply deductions to earned only, then add unearned

```python
def formula(spm_unit, period, parameters):
    gross_earned = spm_unit("tanf_gross_earned_income", period)
    unearned = spm_unit("tanf_gross_unearned_income", period)
    deductions = spm_unit("tanf_earned_income_deductions", period)

    # ✅ CORRECT: Deductions applied to earned only, then add unearned
    return max_(gross_earned - deductions, 0) + unearned
```

### Pattern Variations

**With multiple deduction steps:**
```python
def formula(spm_unit, period, parameters):
    p = parameters(period).gov.states.xx.tanf.income
    gross_earned = spm_unit("tanf_gross_earned_income", period)
    unearned = spm_unit("tanf_gross_unearned_income", period)

    # Step 1: Apply work expense deduction
    work_expense = min_(gross_earned * p.work_expense_rate, p.work_expense_max)
    after_work_expense = max_(gross_earned - work_expense, 0)

    # Step 2: Apply earnings disregard
    earnings_disregard = after_work_expense * p.disregard_rate
    countable_earned = max_(after_work_expense - earnings_disregard, 0)

    # Step 3: Add unearned (no deductions applied)
    return countable_earned + unearned
```

**With disregard percentage (simplified):**
```python
def formula(spm_unit, period, parameters):
    p = parameters(period).gov.states.xx.tanf.income
    gross_earned = spm_unit("tanf_gross_earned_income", period)
    unearned = spm_unit("tanf_gross_unearned_income", period)

    # Apply disregard to earned (keep 33% = disregard 67%)
    countable_earned = gross_earned * (1 - p.earned_disregard_rate)

    return max_(countable_earned, 0) + unearned
```

### When Unearned Income HAS Deductions

Some states DO have unearned income deductions (rare). Handle separately:

```python
def formula(spm_unit, period, parameters):
    gross_earned = spm_unit("tanf_gross_earned_income", period)
    gross_unearned = spm_unit("tanf_gross_unearned_income", period)
    earned_deductions = spm_unit("tanf_earned_income_deductions", period)
    unearned_deductions = spm_unit("tanf_unearned_income_deductions", period)

    # Apply each type of deduction to its respective income type
    countable_earned = max_(gross_earned - earned_deductions, 0)
    countable_unearned = max_(gross_unearned - unearned_deductions, 0)

    return countable_earned + countable_unearned
```

### Quick Reference

**Standard TANF pattern:**
```
Countable Income = max_(Earned - Earned Deductions, 0) + Unearned
```

**NOT:**
```
❌ max_(Earned + Unearned - Deductions, 0)
❌ max_(Earned - Deductions + Unearned, 0)  # Can go negative
```

---

## Federal/State Separation

### Federal Parameters
Location: `/parameters/gov/{agency}/`
- Base formulas and methodologies
- National standards
- Required elements

### State Parameters
Location: `/parameters/gov/states/{state}/`
- State-specific thresholds
- Implementation choices
- Scale factors

```yaml
# Federal: parameters/gov/hhs/fpg/base.yaml
first_person: 14_580

# State: parameters/gov/states/ca/scale_factor.yaml
fpg_multiplier: 2.0  # 200% of FPG
```

### State Income Tax Conformity to Federal Rules

**CRITICAL: State income taxes should reference federal income sources and limits, not redefine them**

Most state income taxes start with federal definitions and then make specific adjustments. When implementing state income tax:

**✅ CORRECT - Reference federal income sources:**
```python
class ms_agi(Variable):
    """Mississippi adjusted gross income"""
    value_type = float
    entity = TaxUnit
    definition_period = YEAR
    label = "Mississippi adjusted gross income"
    unit = USD

    def formula(tax_unit, period, parameters):
        # Start with federal AGI, which already includes
        # federal capital loss limits and other federal rules
        federal_agi = tax_unit("adjusted_gross_income", period)

        # Apply Mississippi-specific additions/subtractions
        ms_additions = tax_unit("ms_additions_to_agi", period)
        ms_subtractions = tax_unit("ms_subtractions_from_agi", period)

        return federal_agi + ms_additions - ms_subtractions
```

**❌ WRONG - Redefining income sources:**
```python
# DON'T create state-specific parameters like:
# parameters/gov/states/ms/tax/income/income_sources.yaml
# containing:
#   - capital_gains
#   - long_term_capital_gains
#   - short_term_capital_gains

# This bypasses federal limits like the $3,000 capital loss deduction limit
```

**Why this matters:**
- Federal income tax applies capital loss limits before reporting AGI
- State income taxes that start from federal AGI automatically inherit these limits
- Creating separate state income source parameters bypasses federal rules
- Results in incorrect calculations (e.g., unlimited capital loss deductions)

**Common state conformity patterns:**
1. **Full conformity** - State AGI = Federal AGI (rare)
2. **Rolling conformity** - State follows current federal rules
3. **Static conformity** - State follows federal rules as of a specific date
4. **Selective conformity** - State follows federal but with specific modifications

**Implementation approach:**
- Always start with federal income sources/AGI/taxable income as the base
- Use state parameters only for state-specific additions, subtractions, or modifications
- Reference federal variables: `adjusted_gross_income`, `taxable_income`, etc.
- Don't recreate federal income aggregation logic at the state level

**Example - Mississippi specifics:**
```python
class ms_additions_to_agi(Variable):
    """Mississippi additions to federal AGI"""
    # Add state-specific income items not in federal AGI
    adds = [
        "ms_state_bond_interest",
        "ms_other_additions"
    ]

class ms_subtractions_from_agi(Variable):
    """Mississippi subtractions from federal AGI"""
    # Subtract state-specific deductions
    adds = [
        "ms_retirement_income_exclusion",
        "ms_other_subtractions"
    ]
```

---

## Code Reuse Patterns

### Avoid Duplication - Create Intermediate Variables

**❌ ANTI-PATTERN: Copy-pasting calculations**
```python
# File 1: calculates income after deduction
def formula(household, period, parameters):
    gross = add(household, period, ["income"])
    deduction = p.deduction * household.nb_persons()
    return max_(gross - deduction, 0)

# File 2: DUPLICATES same calculation
def formula(household, period, parameters):
    gross = add(household, period, ["income"])  # Copy-pasted
    deduction = p.deduction * household.nb_persons()  # Copy-pasted
    after_deduction = max_(gross - deduction, 0)  # Copy-pasted
    return after_deduction < p.threshold
```

**✅ CORRECT: Reuse existing variables**
```python
# File 2: reuses calculation
def formula(household, period, parameters):
    countable_income = household("program_countable_income", period)
    return countable_income < p.threshold
```

**When to create intermediate variables:**
- Same calculation in 2+ places
- Logic exceeds 5 lines
- Reference implementations have similar variable

---

## TANF-Specific Patterns

### Study Reference Implementations First

**MANDATORY before implementing any TANF:**
- DC TANF: `/variables/gov/states/dc/dhs/tanf/`
- IL TANF: `/variables/gov/states/il/dhs/tanf/`
- TX TANF: `/variables/gov/states/tx/hhs/tanf/`

**Learn from them:**
1. Variable organization
2. Naming conventions
3. Code reuse patterns
4. When to use `adds` vs `formula`

### Standard TANF Structure
```
tanf/
├── eligibility/
│   ├── demographic_eligible.py
│   ├── income_eligible.py
│   └── eligible.py
├── income/
│   ├── earned/
│   ├── unearned/
│   └── countable_income.py
└── [state]_tanf.py
```

### Simplified TANF Rules

For simplified implementations:

**DON'T create state-specific versions of:**
- Demographic eligibility (use federal)
- Immigration eligibility (use federal)
- Income sources (use federal baseline)

```python
❌ DON'T CREATE:
ca_tanf_demographic_eligible_person.py
ca_tanf_gross_earned_income.py
parameters/.../income/sources/earned.yaml

✅ DO USE:
# Federal demographic eligibility
is_demographic_tanf_eligible
# Federal income aggregation
tanf_gross_earned_income
```

### Avoiding Unnecessary Wrapper Variables (CRITICAL)

**Golden Rule: Only create a state variable if you're adding state-specific logic to it!**

#### Understand WHY Variables Exist, Not Just WHAT

When studying reference implementations:
1. **Note which variables they have**
2. **READ THE CODE inside each variable**
3. **Ask: "Does this variable have state-specific logic?"**
4. **If it just returns federal baseline → DON'T copy it**

#### Variable Creation Decision Tree

Before creating ANY state-specific variable, ask:
1. Does federal baseline already calculate this?
2. Does my state do it DIFFERENTLY than federal?
3. Can I write the difference in 1+ lines of state-specific logic?
4. **Will this calculation be used in 2+ other variables?** (Code reuse exception)

**Decision:**
- If YES/NO/NO/NO → **DON'T create the variable**, use federal directly
- If YES/YES/YES/NO → **CREATE the variable** with state logic
- If YES/NO/NO/YES → **CREATE as intermediate variable** for code reuse (see exception below)

#### EXCEPTION: Code Reuse Justifies Intermediate Variables

**Even without state-specific logic, create a variable if the SAME calculation is used in multiple places.**

❌ **Bad - Duplicating calculation across variables:**
```python
# Variable 1 - Income eligibility
class mo_tanf_income_eligible(Variable):
    def formula(spm_unit, period, parameters):
        # Duplicated calculation
        gross = add(spm_unit, period, ["tanf_gross_earned_income", "tanf_gross_unearned_income"])
        return gross <= p.income_limit

# Variable 2 - Countable income
class mo_tanf_countable_income(Variable):
    def formula(spm_unit, period, parameters):
        # SAME calculation repeated!
        gross = add(spm_unit, period, ["tanf_gross_earned_income", "tanf_gross_unearned_income"])
        deductions = spm_unit("mo_tanf_deductions", period)
        return max_(gross - deductions, 0)

# Variable 3 - Need standard
class mo_tanf_need_standard(Variable):
    def formula(spm_unit, period, parameters):
        # SAME calculation AGAIN!
        gross = add(spm_unit, period, ["tanf_gross_earned_income", "tanf_gross_unearned_income"])
        return where(gross < p.threshold, p.high, p.low)
```

✅ **Good - Extract into reusable intermediate variable:**
```python
# Intermediate variable - used in multiple places
class mo_tanf_gross_income(Variable):
    adds = ["tanf_gross_earned_income", "tanf_gross_unearned_income"]

# Variable 1 - Reuses intermediate
class mo_tanf_income_eligible(Variable):
    def formula(spm_unit, period, parameters):
        gross = spm_unit("mo_tanf_gross_income", period)  # Reuse
        return gross <= p.income_limit

# Variable 2 - Reuses intermediate
class mo_tanf_countable_income(Variable):
    def formula(spm_unit, period, parameters):
        gross = spm_unit("mo_tanf_gross_income", period)  # Reuse
        deductions = spm_unit("mo_tanf_deductions", period)
        return max_(gross - deductions, 0)

# Variable 3 - Reuses intermediate
class mo_tanf_need_standard(Variable):
    def formula(spm_unit, period, parameters):
        gross = spm_unit("mo_tanf_gross_income", period)  # Reuse
        return where(gross < p.threshold, p.high, p.low)
```

**When to create intermediate variables for reuse:**
- ✅ Same calculation appears in 2+ variables
- ✅ Represents a meaningful concept (e.g., "gross income", "net resources")
- ✅ Simplifies maintenance (change once vs many places)
- ✅ Follows DRY (Don't Repeat Yourself) principle

**When NOT to create (still a wrapper):**
- ❌ Only used in ONE place
- ❌ Just passes through another variable unchanged
- ❌ Adds indirection without code reuse benefit

#### Red Flags for Unnecessary Wrapper Variables

```python
❌ INVALID - Pure wrapper, no state logic:
class in_tanf_assistance_unit_size(Variable):
    def formula(spm_unit, period):
        return spm_unit("spm_unit_size", period)  # Just returns federal

❌ INVALID - Aggregation without transformation:
class in_tanf_countable_unearned_income(Variable):
    def formula(tax_unit, period):
        return tax_unit.sum(person("tanf_gross_unearned_income", period))

❌ INVALID - Pass-through with no modification:
class in_tanf_gross_income(Variable):
    def formula(entity, period):
        return entity("tanf_gross_income", period)
```

#### Examples of VALID State Variables

```python
✅ VALID - Has state-specific disregard:
class in_tanf_countable_earned_income(Variable):
    def formula(spm_unit, period, parameters):
        p = parameters(period).gov.states.in.tanf.income
        earned = spm_unit("tanf_gross_earned_income", period)
        return earned * (1 - p.earned_income_disregard_rate)  # STATE LOGIC

✅ VALID - Uses state-specific limits:
class in_tanf_income_eligible(Variable):
    def formula(spm_unit, period, parameters):
        p = parameters(period).gov.states.in.tanf
        income = spm_unit("tanf_countable_income", period)
        size = spm_unit("spm_unit_size", period.this_year)
        limit = p.income_limit[min_(size, p.max_household_size)]  # STATE PARAMS
        return income <= limit

✅ VALID - IL has different counting rules:
class il_tanf_assistance_unit_size(Variable):
    adds = [
        "il_tanf_payment_eligible_child",  # STATE-SPECIFIC
        "il_tanf_payment_eligible_parent",  # STATE-SPECIFIC
    ]
```

#### State Variables to AVOID Creating

For TANF implementations:

**❌ DON'T create these (use federal directly):**
- `state_tanf_assistance_unit_size` (unless different counting rules like IL)
- `state_tanf_countable_unearned_income` (unless state has disregards)
- `state_tanf_gross_income` (just use federal baseline)
- Any variable that's just `return entity("federal_variable", period)`

**✅ DO create these (when state has unique rules):**
- `state_tanf_countable_earned_income` (if unique disregard %)
- `state_tanf_income_eligible` (state income limits)
- `state_tanf_maximum_benefit` (state payment standards)
- `state_tanf` (final benefit calculation)

### Demographic Eligibility Pattern

**Option 1: Use Federal (Simplified)**
```python
class ca_tanf_eligible(Variable):
    def formula(spm_unit, period, parameters):
        # Use federal variable
        has_eligible = spm_unit.any(
            spm_unit.members("is_demographic_tanf_eligible", period)
        )
        return has_eligible & income_eligible
```

**Option 2: State-Specific (Different thresholds)**
```python
class ca_tanf_demographic_eligible_person(Variable):
    def formula(person, period, parameters):
        p = parameters(period).gov.states.ca.tanf
        age = person("age", period.this_year)  # NOT monthly_age

        age_limit = where(
            person("is_full_time_student", period),
            p.age_threshold.student,
            p.age_threshold.minor_child
        )
        return age < age_limit
```

---

## Common Implementation Patterns

### Income Eligibility
```python
class program_income_eligible(Variable):
    value_type = bool
    entity = SPMUnit
    definition_period = MONTH

    def formula(spm_unit, period, parameters):
        p = parameters(period).gov.states.xx.program
        income = spm_unit("program_countable_income", period)
        size = spm_unit("spm_unit_size", period.this_year)

        # Get threshold from parameters
        threshold = p.income_limit[min_(size, p.max_household_size)]
        return income <= threshold
```

### Benefit Calculation
```python
class program_benefit(Variable):
    value_type = float
    entity = SPMUnit
    definition_period = MONTH
    unit = USD

    def formula(spm_unit, period, parameters):
        p = parameters(period).gov.states.xx.program
        eligible = spm_unit("program_eligible", period)

        # Calculate benefit amount
        base = p.benefit_schedule.base_amount
        adjustment = p.benefit_schedule.adjustment_rate
        size = spm_unit("spm_unit_size", period.this_year)

        amount = base + (size - 1) * adjustment
        return where(eligible, amount, 0)
```

### Using Scale Parameters
```python
def formula(entity, period, parameters):
    p = parameters(period).gov.states.az.program
    federal_p = parameters(period).gov.hhs.fpg

    # Federal base with state scale
    size = entity("household_size", period.this_year)
    fpg = federal_p.first_person + federal_p.additional * (size - 1)
    state_scale = p.income_limit_scale  # Often exists
    income_limit = fpg * state_scale
```

---

## Accessing Baseline Parameters in Reform Simulations

### When You Need Baseline vs Reform Comparison

Some variables need to compare values under current law (baseline) vs a proposed reform. This is common for:
- Variables calculating the **change** in a value due to a reform
- Fixed-cost employer variables (e.g., `employer_NI_fixed_employer_cost_change`)
- Any variable showing "difference from baseline"

### The Pattern for Accessing Baseline Parameters

**CRITICAL:** When a simulation has a baseline (i.e., it's a reform simulation), you must explicitly access baseline parameters:

```python
def formula(person, period, parameters):
    simulation = person.simulation

    # Check if this is a reform simulation with a baseline
    if simulation.baseline is not None:
        # Access baseline parameters through the baseline's tax benefit system
        baseline_parameters = simulation.baseline.tax_benefit_system.get_parameters_at_instant(period)
        baseline_value = baseline_parameters.gov.hmrc.national_insurance.some_rate
    else:
        # No baseline exists - use current parameters as baseline
        baseline_parameters = parameters(period)
        baseline_value = baseline_parameters.gov.hmrc.national_insurance.some_rate

    # Get reform (current) value
    reform_value = parameters(period).gov.hmrc.national_insurance.some_rate

    # Calculate difference
    return reform_value - baseline_value
```

### Common Mistake

**❌ WRONG - Using current parameters for baseline:**
```python
def formula(person, period, parameters):
    p = parameters(period)
    # This gets REFORM parameters, not baseline!
    baseline_rate = p.gov.hmrc.national_insurance.some_rate
    reform_rate = p.gov.hmrc.national_insurance.some_rate
    return reform_rate - baseline_rate  # Always returns 0!
```

**✅ CORRECT - Properly accessing baseline:**
```python
def formula(person, period, parameters):
    simulation = person.simulation

    if simulation.baseline is not None:
        baseline_p = simulation.baseline.tax_benefit_system.get_parameters_at_instant(period)
    else:
        baseline_p = parameters(period)

    baseline_rate = baseline_p.gov.hmrc.national_insurance.some_rate
    reform_rate = parameters(period).gov.hmrc.national_insurance.some_rate

    return reform_rate - baseline_rate
```

### When This Matters

This pattern is essential when:
1. The variable name contains "change", "difference", or "delta"
2. The variable compares policy scenarios
3. You're implementing reform impact analysis variables

Without this pattern, reform simulations will incorrectly show zero change because both "baseline" and "reform" values come from the same (reform) parameters.

---

## Variable Creation Checklist

Before creating any variable:
- [ ] Check if it already exists
- [ ] Use standard demographic variables (age, is_disabled)
- [ ] Reuse federal calculations where applicable
- [ ] Check for household_income before creating new
- [ ] Look for existing intermediate variables
- [ ] Study reference implementations

---

## Quality Standards

### Complete Implementation Requirements
- All values from parameters (no hard-coding)
- Complete formula logic
- Proper entity aggregation
- Correct period handling
- Meaningful variable names
- Proper metadata

### Anti-Patterns to Avoid
- Copy-pasting logic between files
- Hard-coding any numeric values
- Creating duplicate income variables
- State-specific versions of federal rules
- Placeholder TODOs in production code

---

## Parameter-to-Variable Mapping Requirements

### Every Parameter Must Have a Variable

**CRITICAL: Complete implementation means every parameter is used!**

When you create parameters, you MUST create corresponding variables:

| Parameter Type | Required Variable(s) |
|---------------|---------------------|
| resources/limit | `state_program_resources_eligible` |
| income/limit | `state_program_income_eligible` |
| payment_standard | `state_program_maximum_benefit` |
| income/disregard | `state_program_countable_earned_income` |
| categorical/requirements | `state_program_categorically_eligible` |

### Complete Eligibility Formula

The main eligibility variable MUST combine ALL checks:

```python
class state_program_eligible(Variable):
    def formula(spm_unit, period, parameters):
        income_eligible = spm_unit("state_program_income_eligible", period)
        resources_eligible = spm_unit("state_program_resources_eligible", period)  # DON'T FORGET!
        categorical = spm_unit("state_program_categorically_eligible", period)

        return income_eligible & resources_eligible & categorical
```

**Common Implementation Failures:**
- ❌ Created resource limit parameter but no resource_eligible variable
- ❌ Main eligible variable only checks income, ignores resources
- ❌ Parameters created but never referenced in any formula

---

## For Agents

When implementing variables:
1. **Study reference implementations** (DC, IL, TX TANF)
2. **Never hard-code values** - use parameters
3. **Map every parameter to a variable** - no orphaned parameters
4. **Complete ALL eligibility checks** - income AND resources AND categorical
5. **Reuse existing variables** - avoid duplication
6. **Use `adds` when possible** - cleaner than formula
7. **Create intermediate variables** for complex logic
8. **Follow metadata standards** exactly
9. **Complete implementation** or delete the file