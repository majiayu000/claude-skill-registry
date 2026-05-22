---
name: policyengine-review-patterns
description: PolicyEngine code review patterns - validation checklist, common issues, review standards
---

# PolicyEngine Review Patterns

Comprehensive patterns for reviewing PolicyEngine implementations.

## Understanding WHY, Not Just WHAT

### Pattern Analysis Before Review

When reviewing implementations that reference other states:

**🔴 CRITICAL: Check WHY Variables Exist**

Before approving any state-specific variable, verify:
1. **Does it have state-specific logic?** - Read the formula
2. **Are state parameters used?** - Check for `parameters(period).gov.states.XX`
3. **Is there transformation beyond aggregation?** - Look for calculations
4. **Would removing it break functionality?** - Test dependencies

**Example Analysis:**
```python
# IL TANF has this variable:
class il_tanf_assistance_unit_size(Variable):
    adds = ["il_tanf_payment_eligible_child", "il_tanf_payment_eligible_parent"]
    # ✅ VALID: IL-specific eligibility rules

# But IN TANF shouldn't copy it blindly:
class in_tanf_assistance_unit_size(Variable):
    def formula(spm_unit, period):
        return spm_unit("spm_unit_size", period)
    # ❌ INVALID: No IN-specific logic, just wrapper
```

### Wrapper Variable Detection

**Red Flags - Variables that shouldn't exist:**
- Formula is just `return entity("federal_variable", period)`
- Aggregates federal baseline with no transformation
- No state parameters accessed
- Comment says "use federal" but creates variable anyway

**Action:** Request deletion of unnecessary wrapper variables

---

## Priority Review Checklist

### 🔴 CRITICAL - Automatic Failures

These issues will cause crashes or incorrect results:

#### 1. Vectorization Violations
```python
❌ FAILS:
if household("income") > 1000:  # Will crash with arrays
    return 500

✅ PASSES:
return where(household("income") > 1000, 500, 100)
```

#### 2. Hard-Coded Values
```python
❌ FAILS:
benefit = min_(income * 0.33, 500)  # Hard-coded 0.33 and 500

✅ PASSES:
benefit = min_(income * p.rate, p.maximum)
```

#### 3. Missing Parameter Sources
```yaml
❌ FAILS:
reference:
  - title: State website
    href: https://state.gov

✅ PASSES:
reference:
  - title: Idaho Admin Code 16.05.03.205(3)
    href: https://adminrules.idaho.gov/rules/current/16/160503.pdf#page=14
```

---

### 🟡 MAJOR - Must Fix

These affect accuracy or maintainability:

#### 4. Test Quality Issues
```yaml
❌ FAILS:
income: 50000  # No separator

✅ PASSES:
income: 50_000  # Proper formatting
```

#### 5. Calculation Accuracy
- Order of operations matches regulations
- Deductions applied in correct sequence
- Edge cases handled (negatives, zeros)

#### 6. Description Style
```yaml
❌ FAILS:
description: The amount of SNAP benefits  # Passive voice

✅ PASSES:
description: SNAP benefits  # Active voice
```

---

### 🟢 MINOR - Should Fix

These improve code quality:

#### 7. Code Organization
- One variable per file
- Proper use of `defined_for`
- Use of `adds` for simple sums

#### 8. Documentation
- Clear references to regulation sections
- Changelog entry present

---

## Common Issues Reference

### Documentation Issues

| Issue | Example | Fix |
|-------|---------|-----|
| No primary source | "See SNAP website" | Add USC/CFR citation |
| Wrong value | $198 vs $200 in source | Update parameter |
| Generic link | dol.gov | Link to specific regulation |
| Missing subsection | "7 CFR 273" | "7 CFR 273.9(d)(3)" |

### Code Issues

| Issue | Impact | Fix |
|-------|--------|-----|
| if-elif-else with data | Crashes microsim | Use where/select |
| Hard-coded values | Inflexible | Move to parameters |
| Missing defined_for | Inefficient | Add eligibility condition |
| Manual summing | Wrong pattern | Use adds attribute |

### Test Issues

| Issue | Example | Fix |
|-------|---------|-----|
| No separators | 100000 | 100_000 |
| No documentation | output: 500 | Add calculation comment |
| Wrong period | 2024-04 | Use 2024-01 or 2024 |
| Made-up variables | heating_expense | Use existing variables |

---

## Source Verification Process

### Step 1: Check Parameter Values

For each parameter file:
```python
✓ Value matches source document
✓ Source is primary (statute > regulation > website)
✓ URL links to exact section with page anchor
✓ Effective dates correct
```

### Step 2: Validate References

**Primary sources (preferred):**
- USC (United States Code)
- CFR (Code of Federal Regulations)
- State statutes
- State admin codes

**Secondary sources (acceptable):**
- Official policy manuals
- State plan documents

**Not acceptable alone:**
- Websites without specific sections
- Summaries or fact sheets
- News articles

---

## Code Quality Checks

### Vectorization Scan

Search for these patterns:
```python
# Red flags that indicate scalar logic:
"if household"
"if person"
"elif"
"else:"
"and " (should be &)
"or " (should be |)
"not " (should be ~)
```

### Hard-Coding Scan

Search for numeric literals:
```python
# Check for any number except:
# 0, 1, -1 (basic math)
# 12 (month conversion)
# Small indices (2, 3 for known structures)

# Flag anything like:
"0.5"
"100"
"0.33"
"65" (unless it's a standard age)
```

---

## Review Response Templates

### For Approval

```markdown
## PolicyEngine Review: APPROVED ✅

### Verification Summary
- ✅ All parameters trace to primary sources
- ✅ Code is properly vectorized
- ✅ Tests document calculations
- ✅ No hard-coded values

### Strengths
- Excellent USC/CFR citations
- Comprehensive test coverage
- Clear calculation logic

### Minor Suggestions (optional)
- Consider adding edge case for zero income
```

### For Changes Required

```markdown
## PolicyEngine Review: CHANGES REQUIRED ❌

### Critical Issues (Must Fix)

1. **Non-vectorized code** - lines 45-50
   ```python
   # Replace this:
   if income > threshold:
       benefit = high_amount

   # With this:
   benefit = where(income > threshold, high_amount, low_amount)
   ```

2. **Parameter value mismatch** - standard_deduction.yaml
   - Source shows $200, parameter has $198
   - Reference: 7 CFR 273.9(d)(1), page 5

### Major Issues (Should Fix)

3. **Missing primary source** - income_limit.yaml
   - Add statute/regulation citation
   - Current website link insufficient

Please address these issues and re-request review.
```

---

## Test Validation

### Check Test Structure

```yaml
# Verify proper format:
- name: Case 1, description.  # Numbered case with period
  period: 2024-01  # Valid period (2024-01 or 2024)
  input:
    people:
      person1:  # Generic names
        employment_income: 50_000  # Underscores
  output:
    # Calculation documented
    # Income: $50,000/year = $4,167/month
    program_benefit: 250
```

### Run Test Commands

```bash
# Unit tests
pytest policyengine_us/tests/policy/baseline/gov/

# Integration tests
policyengine-core test <path> -c policyengine_us

# Microsimulation
pytest policyengine_us/tests/microsimulation/
```

---

## Review Priorities by Context

### New Program Implementation
1. Parameter completeness
2. All documented scenarios tested
3. Eligibility paths covered
4. No hard-coded values

### Bug Fixes
1. Root cause addressed
2. No regression potential
3. Tests prevent recurrence
4. Vectorization maintained

### Refactoring
1. Functionality preserved
2. Tests still pass
3. Performance maintained
4. Code clarity improved

### Large-Scale Refactoring (Renaming)

**⚠️ CRITICAL: Variable/function renaming has high potential to break things**

When reviewing PRs that rename variables or functions across the codebase:

1. **Test Coverage Requirements**
   - All existing tests must pass
   - Run microsimulation tests if available
   - Consider running notebooks mentioned in repo docs
   - Check for implicit dependencies (string references, dynamic lookups)

2. **Common Breakage Points**
   - Variables referenced as strings (e.g., in reforms, API endpoints)
   - Dynamic variable lookups via `entity(variable_name, period)`
   - Parameter files that reference variable names
   - Documentation/examples that hardcode variable names
   - External tools/APIs that depend on variable naming

3. **Validation Strategy**
   ```bash
   # Basic validation
   pytest  # All unit tests

   # If notebooks exist, run them
   jupyter nbconvert --execute notebook.ipynb

   # Check for string references to renamed variables
   grep -r "old_variable_name" --include="*.py" --include="*.yaml"
   ```

4. **Approval Requirements**
   - Even if tests pass, require maintainer review
   - Look for usage in API/web app if variables are exposed
   - Check if any variables are part of the public interface

---

## Quick Review Checklist

**Parameters:**
- [ ] Values match sources
- [ ] References include subsections
- [ ] All metadata fields present
- [ ] Effective dates correct

**Variables:**
- [ ] Properly vectorized (no if-elif-else)
- [ ] No hard-coded values
- [ ] Uses existing variables
- [ ] Includes proper metadata

**Tests:**
- [ ] Proper period format
- [ ] Underscore separators
- [ ] Calculation comments
- [ ] Realistic scenarios

**Overall:**
- [ ] Changelog entry
- [ ] Code formatted
- [ ] Tests pass
- [ ] Documentation complete

---

## For Agents

When reviewing code:
1. **Check vectorization first** - crashes are worst
2. **Verify parameter sources** - accuracy critical
3. **Scan for hard-coding** - maintainability issue
4. **Validate test quality** - ensures correctness
5. **Run all tests** - catch integration issues
6. **Document issues clearly** - help fixes
7. **Provide fix examples** - speed resolution