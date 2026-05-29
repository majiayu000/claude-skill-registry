---
name: swap-analyzer
description: Analyze swap compatibility and safety. Use when evaluating proposed schedule swaps to ensure they maintain ACGME compliance and operational coverage.
model_tier: opus
parallel_hints:
  can_parallel_with: [code-review, test-writer]
  must_serialize_with: [acgme-compliance, safe-schedule-generation]
  preferred_batch_size: 2
context_hints:
  max_file_context: 20
  compression_level: 1
  requires_git_context: false
  requires_db_context: true
escalation_triggers:
  - pattern: "incompatible|infeasible"
    reason: "Incompatible swaps require human decision"
  - keyword: ["violation", "coverage gap"]
    reason: "Swaps creating violations need escalation"
---

# Swap Analyzer Skill

Comprehensive analysis of schedule swap compatibility and impact assessment.

## When This Skill Activates

- Faculty requests schedule swap
- Evaluating swap feasibility
- Checking swap impact before execution
- Investigating swap-related issues
- Pre-validating swap proposals

## Swap Analysis Framework

### Phase 1: Swap Type Classification

**Identify Swap Pattern:**
```
Swap types:
1. One-to-one swap
   - Resident A's rotation swapped with Resident B
   - Most common, usually feasible

2. Absorb swap
   - Resident A gives shift to Resident B
   - Requires accepting extra load

3. Multi-party swap
   - Chain involving 3+ residents
   - Complex validation needed

4. Faculty/coverage swap
   - Change faculty assignments
   - Affects supervision ratios
```

### Phase 2: Feasibility Analysis

**Step 2.1: Rotation Compatibility**
```
For proposed swap:
1. Is rotation type switchable?
   - Can A work B's rotation?
   - Required credentials?
   - Skill match?

2. Are residents trained for rotations?
   - Check rotation requirements
   - Verify prerequisite training
   - Confirm no conflicts
```

**Step 2.2: ACGME Compliance Check**
```
For each resident involved:
1. 80-hour rule impact
   - Would swap cause violation?
   - Check weeks affected
   - Estimate new hours

2. 1-in-7 rule impact
   - Would swap violate days off rule?
   - Check consecutive duty days after swap

3. Supervision impact
   - Ratio still compliant?
   - Adequate supervision in each rotation?
```

**Step 2.3: Coverage Impact**
```
1. Original coverage
   - Who covers each shift?
   - Is there redundancy?

2. After swap coverage
   - Any coverage gaps created?
   - Minimum staffing maintained?
   - Critical rotations still covered?

3. Backup availability
   - Can gaps be filled?
   - Backup cost/impact?
```

### Phase 3: Impact Assessment

**Step 3.1: Quantify Changes**
```
For each resident:
1. Hours change
   - Current: X hours
   - After swap: Y hours
   - Difference: ±Z hours

2. Rotation change
   - Current: [Rotation A]
   - After swap: [Rotation B]
   - Type change: Clinical/Admin/Procedure/etc

3. Work load impact
   - Fair? Too much? Too light?
```

**Step 3.2: Risk Assessment**
```
Risk factors:
1. Compliance risk: [LOW/MEDIUM/HIGH]
2. Coverage risk: [LOW/MEDIUM/HIGH]
3. Fairness risk: [LOW/MEDIUM/HIGH]
4. Overall risk: [SAFE / PROCEED WITH CAUTION / UNSAFE]
```

### Phase 4: Recommendation

**Step 4.1: Generate Recommendation**
```
Possible outcomes:
1. APPROVED
   - Swap is safe and compliant
   - No issues identified

2. APPROVED WITH CONDITIONS
   - Swap approved if conditions met
   - List specific conditions

3. BLOCKED
   - Swap creates violations
   - Explain specific issues

4. NEEDS MODIFICATION
   - Swap feasible with adjustments
   - Suggest alternative dates/residents
```

## Swap Analysis Report

```markdown
## Swap Feasibility Report

**Swap Type:** [TYPE]
**Requested By:** [NAME]
**Date Requested:** [DATE]

### Proposed Swap
- Resident A: [Current] → [Proposed]
- Resident B: [Current] → [Proposed]
- Dates: [START] to [END]

### Feasibility Analysis

#### Rotation Compatibility
- [x] Rotation A can be done by Resident B
- [x] Resident B has required credentials
- [x] No prerequisite issues

#### ACGME Compliance
- 80-hour impact: [A: ±Z hours, B: ±Z hours]
- 1-in-7 impact: [Compliant/Violation detail]
- Supervision impact: [Compliant/Violation detail]

#### Coverage Impact
- Gaps created: [None/List gaps]
- Coverage maintained: [YES/NO]
- Backup available: [YES/NO]

### Recommendation

**APPROVED** / **BLOCKED** / **CONDITIONAL**

Reasoning: [Explanation]

### Conditions (if applicable)
1. [Condition 1]
2. [Condition 2]

### Alternative Suggestions
1. [Alternative 1]
2. [Alternative 2]
```

## Common Swap Scenarios

### Scenario 1: One-to-One Procedural Swap
**Request:** Swap inpatient block for clinic block
**Analysis:**
- Rotation compatibility: Check
- Skill match: Check
- Hours impact: Usually minor
- Coverage: Usually safe
**Typical outcome:** APPROVED

### Scenario 2: Holiday Coverage Request
**Request:** Swap holiday duties
**Analysis:**
- Often stacks hours dangerously
- Check 4-week rolling average impact
- Verify 80-hour rule not violated
**Typical outcome:** CONDITIONAL or BLOCKED

### Scenario 3: Night Float Swap
**Request:** Swap night float blocks
**Analysis:**
- Coverage critical
- 6-night limit impact
- Supervision in night float important
**Typical outcome:** Varies widely

### Scenario 4: Last-Minute Absence Coverage
**Request:** Absorb shift due to emergency
**Analysis:**
- Fair distribution check
- Fatigue/safety concern
- Must not exceed 80-hour rule
**Typical outcome:** Usually BLOCKED unless fairness maintained

## Integration with swap-execution

After analysis:
1. If APPROVED: Pass to swap-execution for implementation
2. If BLOCKED: Deny swap with explanation
3. If CONDITIONAL: Send conditions to requester
4. If NEEDS MODIFICATION: Propose alternatives

## Quick Analysis Commands

```bash
# Analyze proposed swap
python -m app.swaps.analyzer --resident1=A --resident2=B --dates=START-END

# Check impact on 80-hour rule
python -m app.swaps.analyzer --resident1=A --rule=80-hour --dates=START-END

# Simulate swap to see hours impact
python -m app.swaps.analyzer --resident1=A --simulate --dates=START-END
```

## Validation Checklist

- [ ] Swap type identified correctly
- [ ] Rotation compatibility verified
- [ ] ACGME rules checked
- [ ] Coverage impact assessed
- [ ] Risk level determined
- [ ] Recommendation clear and justified
- [ ] Conditions (if any) specific and measurable
- [ ] Alternative suggestions provided if BLOCKED

## Error Handling

**If swap analysis fails:**
1. Check if schedule data is valid
2. Verify swap parameters are correct
3. Confirm residents/dates exist
4. Escalate if data is inconsistent

**If result is ambiguous:**
1. Re-run with more specific parameters
2. Check for data quality issues
3. Request human review

## References

- Swap management procedures in swap-management skill
- ACGME rules in acgme-compliance skill
- Swap execution in swap-execution skill

