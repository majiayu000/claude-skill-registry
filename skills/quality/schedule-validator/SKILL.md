---
name: schedule-validator
description: Validate generated schedules for ACGME compliance, coverage gaps, and operational viability. Use when verifying schedule integrity before deployment or investigating schedule issues.
model_tier: opus
parallel_hints:
  can_parallel_with: [code-review, test-writer]
  must_serialize_with: [acgme-compliance, safe-schedule-generation]
  preferred_batch_size: 1
context_hints:
  max_file_context: 40
  compression_level: 1
  requires_git_context: false
  requires_db_context: true
escalation_triggers:
  - pattern: "uncoverable|impossible|infeasible"
    reason: "Infeasible schedule patterns need human intervention"
  - keyword: ["coverage gap", "minimum staffing"]
    reason: "Coverage gaps require operational decision"
---

# Schedule Validator Skill

Comprehensive validation of residency schedules for compliance, coverage, and operational feasibility.

## Two Truths: Prescriptive vs Descriptive

**CRITICAL CONTEXT: Understand which truth you're validating.**

| Truth Type | Tables | What It Represents |
|------------|--------|-------------------|
| **Prescriptive** | `rotation_templates`, `weekly_patterns` | What SHOULD happen (rules) |
| **Descriptive** | `half_day_assignments` | What DID happen (actual schedule) |

**Validation should check `half_day_assignments` (descriptive truth)** because that's what will actually be deployed. However, unexpected divergence from templates may indicate bugs.

### Alignment Check (NEW)

When prescriptive and descriptive diverge, verify it's intentional:

| Divergence | Expected Reason | Red Flag If Missing |
|------------|-----------------|---------------------|
| Template says `OFF`, assignment says `C` | `source='manual'` override | Missing manual source |
| Template says `LDNF`, assignment says `LEC` | Wednesday PM LEC rule | Missing preload |
| Template says `C`, assignment says `LV` | Absence preloaded | Missing absence record |

**If divergence exists without valid `source` explanation → investigate as potential bug.**

## When This Skill Activates

- After schedule generation completes
- Before finalizing a new schedule version
- When investigating schedule-related complaints
- During pre-deployment verification
- When checking impact of swaps or changes

## Validation Phases

### Phase 1: Structure Validation

**Check 1.1: Data Integrity**
- [ ] All assignments have required fields (resident, rotation, date)
- [ ] Dates are valid and within academic year
- [ ] No duplicate assignments for same resident/date
- [ ] All referenced residents/rotations exist

**Check 1.2: Coverage Completeness**
```
For each day/rotation:
1. Count assigned residents
2. Compare to minimum required
3. Flag under-coverage with shortfall count
```

**Check 1.3: Timeline Consistency**
- [ ] Rotations don't exceed maximum duration
- [ ] Transitions between rotations are valid
- [ ] No gaps in rotation coverage
- [ ] Block boundaries honored

### Phase 2: ACGME Compliance Validation

**Delegate to acgme-compliance skill for:**
- 80-hour rule verification
- 1-in-7 rule verification
- Supervision ratio validation
- Duty period limit checking

**Summarize findings:**
- Total violations found
- Total warnings found
- Resolution status (fixed/pending)

### Phase 3: Operational Feasibility

**Check 3.1: Staffing Reality**
```
For each rotation:
1. Verify requested faculty are actually available
2. Check for double-booking of faculty
3. Confirm skill matches (credentialed staff only)
```

**Check 3.2: Rotation Continuity**
```
For each resident:
1. No more than 2 consecutive same rotation
2. Adequate rotation variety
3. Educational requirements met
```

**Check 3.3: Coverage Stability**
```
For each critical rotation:
1. N-1 redundancy available?
2. Can single absence be absorbed?
3. Are backups cross-trained?
```

### Phase 4: Quality Metrics

**Metric 4.1: Distribution Fairness**
```
For each resident:
1. Count rotations assigned
2. Check against expected distribution
3. Identify overloaded/underloaded residents
```

**Metric 4.2: Work Load Balance**
```
For each week:
1. Calculate average hours per resident
2. Identify outlier weeks
3. Check for clustering
```

**Metric 4.3: Schedule Predictability**
```
1. Check weekly patterns consistent
2. Identify unexpected variations
3. Assess resident planning difficulty
```

## Validation Report Structure

```markdown
## Schedule Validation Report

**Schedule ID:** [ID]
**Period:** [Date Range]
**Overall Status:** [VALID / WARNINGS / INVALID]

### Validation Summary
- Data integrity: [PASS/FAIL]
- ACGME compliance: [PASS/FAIL/VIOLATIONS]
- Operational feasibility: [PASS/FAIL]
- Quality metrics: [PASS/FAIL]

### Issues Found

#### Critical Issues (Block Deployment)
1. [Issue description]
   - Affected: [Who/What]
   - Fix: [Required action]

#### Warnings (Operational Impact)
1. [Issue description]
   - Impact: [Consequence]
   - Resolution: [Recommended fix]

#### Recommendations (Optimization)
1. [Suggestion for improvement]

### Coverage Analysis
- Minimum staffing: [Numbers]
- Average coverage: [Numbers]
- Gap days: [If any]

### ACGME Summary
- 80-hour violations: [Count]
- 1-in-7 violations: [Count]
- Supervision violations: [Count]

### Success Criteria
- [ ] No data integrity errors
- [ ] ACGME fully compliant
- [ ] All rotations adequately covered
- [ ] No impossible coverage patterns
```

## Integration with Other Skills

### With acgme-compliance
- Calls acgme-compliance for detailed rule verification
- Summarizes findings for report
- Requests specific remediation if violations found

### With safe-schedule-generation
- Run after schedule generation
- Identify unfeasible schedules early
- Provide feedback for regeneration

### With swap-execution
- Validate proposed swap doesn't break schedule
- Check coverage remains adequate after swap

## Quick Validation Commands

```bash
# Full schedule validation
python -m app.scheduling.validator --schedule_id=current --full

# ACGME only
python -m app.scheduling.validator --schedule_id=current --acgme-only

# Coverage analysis only
python -m app.scheduling.validator --schedule_id=current --coverage-only

# Export validation report
python -m app.scheduling.validator --schedule_id=current --export=pdf
```

## Validation Checklist

- [ ] No duplicate assignments
- [ ] All dates valid and within academic year
- [ ] All residents referenced exist
- [ ] All rotations referenced exist
- [ ] Coverage gaps identified and counted
- [ ] ACGME compliance verified
- [ ] Staffing coverage adequate
- [ ] Rotation continuity acceptable
- [ ] Work load reasonably balanced
- [ ] Schedule is operable in practice
- [ ] **`source` column audit**: Verify preloads preserved, manual overrides have `source='manual'`
- [ ] **Prescriptive/descriptive alignment**: Unexpected divergence from templates explained by valid `source`

## Error Handling

**If validation fails catastrophically:**
1. Check if schedule data is corrupt
2. Verify database connection
3. Compare with previous known-good schedule
4. Request manual validation review

**If coverage gaps exist:**
1. Count shortage (how many needed)
2. Identify which dates/rotations affected
3. Suggest mitigation options
4. Decide: fix or accept operational risk

**If ACGME violations found:**
1. Document specific violations
2. Identify affected residents
3. Request acgme-compliance skill for remediation
4. Don't approve schedule without compliance

## References

- ACGME Common Program Requirements
- See PROMPT_LIBRARY.md for validation templates
- Schedule verification checklist in schedule-verification skill
