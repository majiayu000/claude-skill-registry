---
name: pension-calculation-validator
description: Validate LGPS (Local Government Pension Scheme) benefit calculations
  against LGPS Regulations 2013 to ensure accuracy, check early retirement reduction
  factors, verify Rule of 85 protections, and flag anomalies. Critical for ensuring
  correct member benefits.
---

---
name: pension-calculation-validator
description: Validate LGPS benefit calculations against regulations, check early retirement factors, verify rule of 85, flag calculation anomalies. Use when validating pension calculations, benefit statements, retirement quotes, transfer values. Keywords: calculation, benefit, LGPS, retirement, validate, rule of 85, early retirement, pension formula, accrual.
allowed-tools: Read, Bash, mcp__neo4j-psps__*, mcp__archon__rag_search_knowledge_base
model: claude-opus-4-5-20251101
context: fork
agent: general-purpose
---

# Pension Calculation Validator

## Purpose

Validate LGPS (Local Government Pension Scheme) benefit calculations against LGPS Regulations 2013 to ensure accuracy, check early retirement reduction factors, verify Rule of 85 protections, and flag anomalies. Critical for ensuring correct member benefits.

## When to Use

- Reviewing Annual Benefit Statements before issue
- Validating retirement quotes
- Checking transfer value calculations
- Auditing benefit calculations
- Investigating member queries about benefits
- Training administration staff
- Testing new calculation systems

## Calculation Types Supported

1. **Normal Retirement Pension** (age 65/State Pension Age)
2. **Early Retirement** (with reduction factors)
3. **Rule of 85 Protection** (transitional)
4. **Ill Health Retirement** (Tiers 1, 2, 3)
5. **Deferred Benefits** (with revaluation)
6. **Death Benefits** (death grants, survivor pensions)
7. **Transfer Values** (CETV)

## Validation Workflow

### Phase 1: Extract Calculation Details

**Step 1: Read calculation document/data**
```
# Input format examples:
# - Benefit statement PDF
# - Calculation spreadsheet
# - Retirement quote letter
# - Member data record

Read(file_path="[calculation-file]")
```

**Step 2: Extract key data points**

```markdown
## Member Data Extracted

### Personal Details
- Name: [Member name]
- Date of Birth: [DOB]
- NI Number: [NI number]
- Current Age: [Age]
- State Pension Age: [SPA]

### Employment
- Employment Start Date: [Date]
- Membership Start Date: [Date]
- Retirement Date (actual/assumed): [Date]
- Final Pensionable Pay: £[Amount]

### Service
- Total Membership: [Years and days]
- Final Salary Link Service: [Years and days] (if pre-2014)
- CARE Service: [Years and days] (post-2014)
- Part-time Service: [Details if applicable]

### Calculation Inputs
- Calculation Type: [Normal/Early/Ill Health/Deferred/Death]
- Calculation Date: [Date]
- Scheme Section: [Final Salary/CARE/Both]
- Rule of 85 Status: [Protected/Not Protected]
```

### Phase 2: Query Regulations

**Step 1: Get applicable regulations**

```
# Query PSPS database for calculation rules
mcp__neo4j-psps__read_neo4j_cypher(
  query="
    MATCH (r:Regulation)-[:GOVERNS]->(c:Calculation)
    WHERE c.type = $calcType
    RETURN r.reference, r.formula, r.effective_date, r.notes
  ",
  params={"calcType": "[calculation type]"}
)

# Search for calculation guidance
mcp__archon__rag_search_knowledge_base(
  query="LGPS [calculation type] formula regulation",
  match_count=5
)
```

**Step 2: Identify applicable formula**

```markdown
## Applicable Regulations

### Final Salary Benefits (pre-2014 service)
**Regulation**: LGPS Regulations 2013, Schedule 1
**Formula**: Pensionable service (years) / 60 × Final pensionable pay
**Lump Sum**: Automatic lump sum = Pension × 3

**Example**:
Service: 20 years
Final Pay: £30,000
Pension = 20/60 × £30,000 = £10,000 p.a.
Lump Sum = £10,000 × 3 = £30,000

### CARE Benefits (post-2014 service)
**Regulation**: LGPS Regulations 2013, Part 3
**Accrual Rate**: 1/49th
**Formula**: Sum of annual pension accounts (revalued)

**Example**:
Year 1: £30,000 × 1/49 = £612.24
Year 2: £30,600 × 1/49 = £624.49 (plus revaluation on Year 1)
Year 3: £31,212 × 1/49 = £636.98 (plus revaluation on Years 1 & 2)
etc.
```

### Phase 3: Perform Independent Calculation

**Step 1: Calculate expected benefit**

```markdown
## Independent Calculation

### Inputs
- Date of Birth: 15/05/1964
- State Pension Age: 66 (calculated from DOB)
- Membership: 1/04/2000 to 31/03/2024 = 24 years 0 days
- Final Pay: £35,000
- Retirement Age: 60 (early retirement)

### Final Salary Service (1/04/2000 to 31/03/2014)
Service: 14 years 0 days
Pension = 14/60 × £35,000 = £8,166.67 p.a.
Lump Sum = £8,166.67 × 3 = £24,500.00

### CARE Service (1/04/2014 to 31/03/2024)
[Calculate annual pension accounts with revaluation]
Year 1 (2014/15): £33,000 × 1/49 = £673.47
Year 2 (2015/16): £33,500 × 1/49 = £683.67 + revaluation
...
Year 10 (2023/24): £35,000 × 1/49 = £714.29 + revaluation
Total CARE Pension = £7,450.32 p.a. (after revaluation)

### Total Unreduced Pension
Final Salary: £8,166.67
CARE: £7,450.32
**Total: £15,616.99 p.a.**

### Early Retirement Reduction
Retirement at age 60, SPA is 66 = 6 years early
Reduction factor: Depends on year of early retirement
Using LGPS early retirement factors table:
6 years early = reduction of approximately 28%

Reduced pension: £15,616.99 × 0.72 = **£11,244.23 p.a.**

### Lump Sum
Final Salary automatic lump sum: £24,500.00
Plus any CARE commutation if taken
```

**Step 2: Check Rule of 85**

```markdown
## Rule of 85 Check

### Rule of 85 Definition
Member's age + scheme membership (both in whole years) ≥ 85
**AND** member born before 1/04/1960

### Protection Status
DOB: 15/05/1964
Born after 1/04/1960 → **NOT protected**

**If protected**, would check:
Age at retirement: 60
Membership: 24 years
60 + 24 = 84 (< 85, so reduction would still apply)

**Conclusion**: Early retirement reduction applies (no Rule of 85 protection)
```

### Phase 4: Compare Calculations

**Comparison table**:

```markdown
## Calculation Comparison

| Component | Provided Calc | Our Calc | Variance | Status |
|-----------|---------------|----------|----------|--------|
| Final Salary Service | 14 years | 14 years | 0 | ✓ |
| Final Salary Pension | £8,166.67 | £8,166.67 | £0.00 | ✓ |
| CARE Service | 10 years | 10 years | 0 | ✓ |
| CARE Pension (unreduced) | £7,398.15 | £7,450.32 | £52.17 | ⚠️ |
| Total Unreduced | £15,564.82 | £15,616.99 | £52.17 | ⚠️ |
| Early Retirement Factor | 0.72 | 0.72 | 0 | ✓ |
| **Final Pension** | **£11,206.67** | **£11,244.23** | **£37.56** | ⚠️ |
| Lump Sum | £24,500.00 | £24,500.00 | £0.00 | ✓ |

### Variance Analysis
**CARE Pension Variance: £52.17 (0.70%)**

Possible causes:
1. Different revaluation figures used
2. Rounding differences in annual calculations
3. Missing or incorrect salary data
4. Part-time service not accounted for

**Action**: Review CARE annual pension account records
**Materiality**: Low (< 1% variance)
**Recommendation**: Investigate but likely acceptable rounding
```

### Phase 5: Validation Checks

**Automated validation checks**:

```markdown
## Validation Checklist

### Data Quality Checks
- [ ] Date of birth matches member record
- [ ] NI number matches
- [ ] Membership dates continuous (no unexplained gaps)
- [ ] Final pay appears reasonable (not outlier)
- [ ] State Pension Age correctly calculated from DOB

### Formula Checks
- [ ] Correct accrual rate used (1/60 FS, 1/49 CARE)
- [ ] Revaluation applied to CARE accounts
- [ ] Early retirement factor applied correctly
- [ ] Lump sum calculated correctly (3× FS pension)

### Regulatory Checks
- [ ] Rule of 85 status assessed correctly
- [ ] Correct retirement age (not before 55)
- [ ] Ill health criteria met (if ill health retirement)
- [ ] Reduction factor from correct table/year

### Reasonableness Checks
- [ ] Pension not > 2/3 final pay (typical maximum)
- [ ] Total benefits not negative
- [ ] Reduction factor not > 50% (maximum early retirement)
- [ ] Similar to previous calculations for this member

### Edge Cases
- [ ] Part-time service pro-rated correctly
- [ ] Breaks in service handled
- [ ] Transfers in/out accounted for
- [ ] Additional voluntary contributions (AVCs) separate
- [ ] Multiple employments aggregated (if applicable)
```

### Phase 6: Flag Anomalies

**Common anomalies to flag**:

```markdown
## Anomaly Detection

### Red Flags 🔴 (Critical Errors)

**1. Wrong accrual rate**
- Calculation uses 1/80 instead of 1/60 for pre-2014
- **Impact**: Significant underpayment
- **Example**: £30k salary, 10 years = £3,750 (1/80) vs £5,000 (1/60)

**2. No early retirement reduction when required**
- Member under SPA but no reduction applied
- **Impact**: Significant overpayment
- **Example**: 5 years early = ~23% reduction missed

**3. Rule of 85 incorrectly applied**
- Protection granted when member not eligible
- **Impact**: Overpayment (reduction not applied when should be)

**4. Final pay incorrect**
- Using wrong pensionable pay definition
- Not using best of last 3 years (if applicable)
- **Impact**: Under/overpayment depending on error

**5. Service miscounted**
- Missing service periods
- Double-counting service
- **Impact**: Significant error in benefits

### Amber Flags 🟡 (Warnings)

**6. High revaluation variance**
- CARE revaluation differs significantly from expected
- **Impact**: Minor under/overpayment
- **Action**: Check revaluation rates used

**7. Part-time factors unclear**
- Part-time service adjustment not documented
- **Impact**: Potential error if not pro-rated
- **Action**: Verify part-time hours and factors

**8. Transfer values not shown**
- Member has transfer-in but not reflected
- **Impact**: Underpayment of benefits
- **Action**: Check transfer records

**9. Ill health enhancements unclear**
- Tier 1/2 ill health but enhancement not obvious
- **Impact**: Could be underpayment
- **Action**: Verify ill health tier and enhancement

### Green Flags ✓ (Acceptable)

**10. Minor rounding differences**
- Variance < £10 p.a. or < 0.1%
- **Impact**: Immaterial
- **Action**: Accept (rounding inherent in calcs)

**11. Different revaluation source**
- Using CPI vs different index
- **Impact**: Minor if recent
- **Action**: Document source used

**12. Recent salary changes**
- Final pay affected by recent promotion/increment
- **Impact**: None if correct pay used
- **Action**: Verify timing of change
```

### Phase 7: Generate Validation Report

**Report template**:

```markdown
# Pension Calculation Validation Report

**Member**: [Name]
**NI Number**: [NI]
**Calculation Type**: [Type]
**Validation Date**: [Date]
**Validator**: Claude Opus 4.5

## Executive Summary

**Overall Assessment**: [PASS / FAIL / PASS WITH MINOR ISSUES]

**Key Findings**:
- [Finding 1]
- [Finding 2]
- [Finding 3]

**Recommendation**: [Accept calculation / Request corrections / Escalate for review]

## Member Details

[From Phase 1]

## Regulatory Basis

[From Phase 2]

## Independent Calculation

[From Phase 3 - show full working]

## Comparison

[From Phase 4 - comparison table]

## Validation Checks

[From Phase 5 - checklist with results]

## Anomalies Identified

[From Phase 6 - list any red/amber/green flags]

### Critical Issues (Red 🔴)
[List any critical errors requiring correction]

### Warnings (Amber 🟡)
[List any warnings requiring investigation]

### Acceptable Variances (Green ✓)
[List any minor acceptable differences]

## Recommendations

### Immediate Actions Required
1. [Action if critical error found]
2. [Action if critical error found]

### Further Investigation
1. [Item to investigate if amber flag]
2. [Item to investigate if amber flag]

### Accept As-Is
[If validation passed, confirm acceptance]

## Supporting Evidence

### Regulations Referenced
- LGPS Regulations 2013, Regulation [X]
- Early Retirement Factors Table [Year]
- CPI Revaluation Rates [Period]

### Database Queries
- PSPS: [Node references]
- Archon RAG: [Page references]

## Calculations Detail

### Working Papers
[Attach detailed calc sheets if needed]

---

**Disclaimer**: This validation is based on publicly available LGPS regulations. Complex cases should be reviewed by the scheme actuary.

**Generated by**: Claude Opus 4.5 via Pension Calculation Validator
**Date**: [Timestamp]
```

## Calculation Formulas Quick Reference

### Final Salary (pre-2014)
```
Annual Pension = (Service in years / 60) × Final Pensionable Pay
Automatic Lump Sum = Annual Pension × 3
```

### CARE (post-2014)
```
Annual Pension Account = (Pensionable Pay in year / 49)
Revalued Amount = Previous amount × (1 + Revaluation rate)
Total CARE Pension = Sum of all revalued annual accounts
```

### Early Retirement Reduction
```
Years Early = SPA - Retirement Age
Reduction % = Look up in Early Retirement Factors table
Reduced Pension = Unreduced Pension × (1 - Reduction %)
```

### Rule of 85
```
Protected if: Born before 1/04/1960 AND
              (Age + Membership ≥ 85 at retirement)

If protected: No reduction if Rule of 85 met
If not protected: Standard early retirement reduction applies
```

### Ill Health Enhancements
```
Tier 1: Service enhanced to Normal Pension Age
Tier 2: Service enhanced by 25%
Tier 3: No enhancement (immediate payment only)
```

## Common Errors and How to Spot Them

**Error 1: Using 1/80 instead of 1/60**
```
Wrong: £30,000 × 10/80 = £3,750
Right: £30,000 × 10/60 = £5,000
Difference: £1,250 p.a. (33% error!)
```

**Error 2: Not applying early retirement reduction**
```
Member retires at 60, SPA 66
Wrong: Unreduced pension of £15,000
Right: Reduced by ~28% = £10,800
Difference: £4,200 p.a. overpayment!
```

**Error 3: Incorrect final pay**
```
Using current salary instead of average of best 3 consecutive years
Could be higher OR lower depending on salary history
Impact: Varies but can be significant
```

**Error 4: Missing CARE revaluation**
```
Wrong: Sum of nominal annual accounts
Right: Sum of revalued annual accounts
Impact: Underpayment (typically 10-20% over 10 years)
```

**Error 5: Rule of 85 misapplied**
```
Wrong: Granting protection to member born after 1/04/1960
Right: Check DOB before applying protection
Impact: Overpayment (reduction not applied when should be)
```

## Integration with Other Skills

- **lgps-scheme-amendment-analyzer**: Check if amendments affect calculations
- **regulatory-deadline-tracker**: Validate calculations before ABS deadline
- **pensions-research**: Look up complex regulation interpretations
- **cost-optimizer**: Always use Opus for calculations (high stakes)

## Quick Commands

```bash
# Calculate age from DOB
# DOB: 15/05/1964, Today: 10/01/2026
AGE=$(( ($(date +%Y) - 1964) - ($(date +%m%d) < 0515) ))
echo $AGE  # 61

# Calculate years of service
# Start: 01/04/2000, End: 31/03/2024
# Use online calculator or manual calculation

# Search for regulation
grep -i "regulation [0-9]+" calculation.txt
```

## Summary

This skill provides comprehensive pension calculation validation by:
- Performing independent calculations using LGPS regulations
- Comparing against provided calculations
- Identifying variances and anomalies
- Checking Rule of 85 protection
- Validating early retirement factors
- Flagging critical errors vs acceptable variances
- Generating detailed validation reports with recommendations

**Always use Opus model** for pension calculations due to financial complexity and member impact.

Ensures members receive correct benefits and protects scheme from overpayment errors.
