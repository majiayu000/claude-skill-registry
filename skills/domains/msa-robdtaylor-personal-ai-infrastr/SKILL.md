---
name: Msa
description: Conduct Gage R&R studies and validate measurement systems per AIAG MSA manual. Covers variable and attribute studies, acceptance criteria, and calculation methods. USE WHEN user says 'MSA', 'gage R&R', 'GR&R', 'measurement system', 'repeatability', 'reproducibility', 'attribute agreement', or 'ndc'. Integrates with ControlPlan, SPC, and AutomotiveManufacturing skills.
---

# Measurement System Analysis (MSA)

## When to Activate This Skill
- "Conduct gage R&R study"
- "Evaluate measurement system for [gage/characteristic]"
- "Calculate %GR&R"
- "Perform attribute agreement analysis"
- "What's the ndc for this gage?"
- "Is this measurement system acceptable?"
- "MSA requirements for [characteristic]"

## Purpose of MSA

MSA determines how much of the observed process variation is due to the measurement system rather than the actual process. Before making decisions based on measurement data, we must verify the measurement system is adequate.

### Why MSA Matters

**Without MSA:**
- "Good" parts may be rejected
- "Bad" parts may be accepted
- Process capability may be understated
- SPC decisions may be wrong
- Customer complaints may result

**With MSA:**
- Measurement confidence established
- Gage selection validated
- Training effectiveness verified
- Calibration adequacy confirmed

---

## Types of MSA Studies

### Variable MSA (Gage R&R)

For measurements that produce numerical data (dimensions, weight, temperature, etc.)

| Study Type | Purpose | Method |
|------------|---------|--------|
| Repeatability | Same operator, same gage, same part, multiple measurements | Single operator, 10+ measurements |
| Reproducibility | Different operators, same gage, same parts | Multiple operators measure same parts |
| Gage R&R | Combined repeatability and reproducibility | Standard study |
| Bias | Difference between measured and true value | Compare to master |
| Linearity | Bias across measurement range | Multiple references |
| Stability | Variation over time | Control chart on master |

### Attribute MSA

For measurements that produce pass/fail, good/bad, or categorical results

| Study Type | Purpose | Method |
|------------|---------|--------|
| Attribute Agreement | Operator consistency and accuracy | Multiple operators, multiple trials |
| Kappa | Agreement beyond chance | Statistical calculation |
| Effectiveness | Correct decisions vs. actual status | Reference evaluation |

---

## Variable Gage R&R Study

### Study Design (Standard AIAG)

| Parameter | Minimum | Preferred | Notes |
|-----------|---------|-----------|-------|
| Operators | 2 | 3 | Include typical operators |
| Parts | 5 | 10 | Represent process variation |
| Trials | 2 | 3 | Repeat measurements |
| Total readings | 20 | 30-90 | More = better discrimination |

### Study Execution

1. **Select parts** - Cover full range of process variation
2. **Number parts** - Hidden from operator view
3. **Randomize** - Operator doesn't know which part
4. **Measure** - Each operator measures all parts, multiple trials
5. **Record** - Document all measurements
6. **Analyze** - Calculate %GR&R, ndc

### Acceptance Criteria

| Metric | Acceptable | Marginal | Unacceptable |
|--------|------------|----------|--------------|
| %GR&R (vs Process) | <10% | 10-30% | >30% |
| %GR&R (vs Tolerance) | <10% | 10-30% | >30% |
| ndc (Number of Distinct Categories) | ≥5 | 3-4 | <3 |

### Interpretation

**%GR&R <10%:**
- Measurement system acceptable
- Can distinguish part-to-part variation
- Suitable for SPC

**%GR&R 10-30%:**
- May be acceptable for non-critical applications
- Requires customer approval for critical characteristics
- Consider improvement actions

**%GR&R >30%:**
- Measurement system not acceptable
- Must improve before use
- Consider: different gage, training, environment

**ndc (Number of Distinct Categories):**
- Represents how many groups the gage can distinguish
- ndc ≥5 required for variable data
- ndc <5 means gage acts more like attribute (good/bad only)

---

## Gage R&R Calculations

### ANOVA Method (Preferred)

Analysis of Variance separates total variation into:
- Part-to-part variation
- Operator variation
- Operator × Part interaction
- Repeatability (equipment)
- Reproducibility (operator)

### Range Method (X-bar/R)

Simpler calculation, widely used:

```
Repeatability (EV) = R̄ × K₁
Where: R̄ = average range across all operators
       K₁ = factor based on number of trials

Reproducibility (AV) = √[(X̄diff × K₂)² - (EV²/nr)]
Where: X̄diff = range of operator averages
       K₂ = factor based on number of operators
       n = number of parts
       r = number of trials

GR&R = √(EV² + AV²)

%GR&R = (GR&R / TV) × 100
Where: TV = Total Variation = √(GR&R² + PV²)
       PV = Part Variation

ndc = 1.41 × (PV / GR&R)
```

---

## Attribute Agreement Analysis

### When to Use

- Go/No-go gages
- Visual inspection
- Pass/fail tests
- Any categorical decision

### Study Design

| Parameter | Minimum | Preferred |
|-----------|---------|-----------|
| Appraisers | 2 | 3 |
| Samples | 20 | 30-50 |
| Trials | 2 | 3 |
| Sample mix | Include borderline | 50% good, 50% bad, include borderline |

### Key Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Within Appraiser Agreement | Self-consistency | ≥90% |
| Between Appraiser Agreement | Appraiser vs. Appraiser | ≥90% |
| Appraiser vs. Standard | Appraiser vs. Reference | ≥90% |
| Kappa | Agreement beyond chance | ≥0.75 |

### Kappa Interpretation

| Kappa Value | Interpretation |
|-------------|----------------|
| <0.20 | Poor agreement |
| 0.21-0.40 | Fair agreement |
| 0.41-0.60 | Moderate agreement |
| 0.61-0.80 | Substantial agreement |
| 0.81-1.00 | Almost perfect agreement |

---

## Other MSA Studies

### Bias Study

Measures systematic error (difference from true value)

**Method:**
1. Obtain reference standard (known true value)
2. Measure standard multiple times (≥10)
3. Calculate average of measurements
4. Bias = Average - Reference value

**Acceptance:** Bias ≈ 0 or within calibration tolerance

### Linearity Study

Measures bias across the measurement range

**Method:**
1. Select 5+ reference standards across range
2. Measure each standard multiple times
3. Plot bias vs. reference value
4. Fit regression line

**Acceptance:** Linearity (slope × Process Variation) <5%

### Stability Study

Measures variation over time

**Method:**
1. Select stable reference part/standard
2. Measure periodically (daily, weekly)
3. Plot on control chart
4. Monitor for trends or out-of-control

**Acceptance:** Stable control chart, no trends

---

## MSA Requirements by Application

### IATF 16949 Requirements (7.1.5.1.1)

- MSA required for all measurement systems in Control Plan
- Shall include study guidance and acceptance criteria
- Alternative methods may be used with customer approval

### Application Guidelines

| Characteristic | Required MSA | Criteria |
|----------------|--------------|----------|
| Critical (CC) | Gage R&R (variable) or Attribute Agreement | %GR&R <10% |
| Significant (SC) | Gage R&R (variable) or Attribute Agreement | %GR&R <30% |
| Standard | Gage R&R recommended | %GR&R <30% |
| SPC-monitored | Gage R&R required | ndc ≥5 |

---

## Common MSA Issues and Solutions

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| High repeatability | Gage resolution, condition | Better gage, calibrate, repair |
| High reproducibility | Training, technique | Standardize method, train |
| High interaction | Operator-dependent method | Simplify method, fixture |
| Poor ndc | Gage can't see variation | More sensitive gage |
| Low Kappa | Ambiguous criteria | Define clearer standards |
| Bias | Calibration, wear | Recalibrate, adjust |

---

## Output Format

When generating MSA content:

```markdown
# MSA Study Report

## Study Information
| Field | Value |
|-------|-------|
| **Study Type** | Gage R&R / Attribute Agreement |
| **Gage ID** | [ID] |
| **Gage Description** | [Type, range, resolution] |
| **Characteristic** | [What is measured] |
| **Specification** | [Tolerance] |
| **Study Date** | [Date] |
| **Conducted By** | [Name] |

## Study Parameters
| Parameter | Value |
|-----------|-------|
| Operators | [Number and names] |
| Parts | [Number] |
| Trials | [Number] |
| Total measurements | [Count] |

## Results
| Metric | Value | Acceptance | Status |
|--------|-------|------------|--------|
| %GR&R | [X]% | <10% / <30% | PASS/FAIL |
| ndc | [X] | ≥5 | PASS/FAIL |
| Repeatability | [X]% | - | - |
| Reproducibility | [X]% | - | - |

## Conclusion
[ACCEPTABLE / MARGINAL / UNACCEPTABLE]

## Actions (if required)
- [Action items]
```

---

## Integration with Related Skills

### ControlPlan
All gages in Control Plan require MSA:
- Variable gages: Gage R&R
- Attribute gages: Attribute agreement
- MSA status verified before production

**Load:** `read ~/.claude/skills/Controlplan/SKILL.md`

### SPC
SPC validity depends on MSA:
- ndc ≥5 required for variable SPC
- Measurement variation affects control limits
- Poor MSA = poor SPC decisions

**Load:** `read ~/.claude/skills/Spc/SKILL.md`

### AutomotiveManufacturing
MSA supports work instruction development:
- Measurement methods documented
- Gage identification required
- Operator training verified

**Load:** `read ~/.claude/skills/Automotivemanufacturing/SKILL.md`

---

## Supplementary Resources

For detailed guidance:
`read ~/.claude/skills/Msa/CLAUDE.md`

For study templates:
`ls ~/.claude/skills/Msa/templates/`

For acceptance criteria:
`read ~/.claude/skills/Msa/reference/acceptance-criteria.md`

For calculation formulas:
`read ~/.claude/skills/Msa/reference/calculation-formulas.md`
