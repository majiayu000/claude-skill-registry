---
name: acgme-compliance
description: ACGME regulatory compliance expertise for medical residency scheduling. Use when validating schedules, checking work hour limits, supervision ratios, or answering compliance questions. Integrates with MCP validation tools.
model_tier: opus
parallel_hints:
  can_parallel_with: [code-review, test-writer, constraint-preflight]
  must_serialize_with: [safe-schedule-generation, swap-execution]
  preferred_batch_size: 3
context_hints:
  max_file_context: 30
  compression_level: 1
  requires_git_context: false
  requires_db_context: true
escalation_triggers:
  - pattern: "violation"
    reason: "Compliance violations require human approval"
  - pattern: "exception"
    reason: "Policy exceptions need Program Director approval"
  - keyword: ["systemic", "recurring", "pattern"]
    reason: "Systemic issues require escalation"
---

# ACGME Compliance Skill

Expert knowledge of ACGME (Accreditation Council for Graduate Medical Education) requirements for residency program scheduling.

## When This Skill Activates

- Validating schedule compliance
- Checking resident work hours
- Verifying supervision ratios
- Answering ACGME-related questions
- Before finalizing any schedule changes
- When coverage gaps are detected

## Required MCP Tools (MUST USE)

**For ANY compliance validation, you MUST run:**

```python
# Step 1: Validate against ACGME rules
mcp__residency-scheduler__validate_schedule_tool(
    start_date="[start]",
    end_date="[end]",
    check_work_hours=True,
    check_supervision=True,
    check_rest_periods=True,
    check_consecutive_duty=True
)

# Step 2: Military compliance check (DRRS ratings)
mcp__residency-scheduler__check_mtf_compliance_tool(
    check_circuit_breaker=True,
    generate_sitrep=True
)

# Step 3: Query knowledge base for policy details
mcp__residency-scheduler__rag_search(
    query="ACGME [specific rule]",
    doc_type="acgme_rules"
)
```

These tools provide authoritative compliance data. Never rely on memory alone.

## Core ACGME Rules

### 1. 80-Hour Rule (Duty Hours)
**Requirement:** Maximum 80 hours per week, averaged over 4-week period

```
Weekly Hours ≤ 80 (averaged over rolling 4 weeks)
```

| Calculation | Formula |
|-------------|---------|
| 4-Week Average | `(Week1 + Week2 + Week3 + Week4) / 4` |
| Warning Threshold | > 75 hours/week |
| Violation | > 80 hours/week average |

**Common Violations:**
- Holiday coverage stacking
- Call schedule compression
- Inadequate post-call relief

### 2. 1-in-7 Rule (Days Off)
**Requirement:** One 24-hour period free from duty every 7 days

```
Must have ≥ 1 day completely off per 7-day period
```

| Status | Definition |
|--------|------------|
| Compliant | 24+ continuous hours off in 7-day window |
| At Risk | 6 consecutive duty days |
| Violation | 7+ consecutive duty days |

**Note:** Averaged over 4 weeks for some programs

### 3. Supervision Ratios
**Requirement:** Adequate faculty oversight based on training level

| Training Level | Max Residents per Faculty |
|----------------|---------------------------|
| PGY-1 (Intern) | 2:1 |
| PGY-2 | 4:1 |
| PGY-3+ | 4:1 |

**Critical Areas Requiring Direct Supervision:**
- Emergency procedures
- High-risk patient care
- Night float transitions

### 4. Duty Period Limits
| Scenario | Maximum Duration |
|----------|------------------|
| Standard shift | 24 hours |
| With strategic napping | 28 hours (rare exception) |
| Minimum time off between shifts | 8 hours |
| Extended (in-house call) | 24 + 4 hours transition |

### 5. Night Float Requirements
- Maximum 6 consecutive nights
- Adequate handoff time
- No other clinical duties during night float block

## MCP Tool Integration

### Primary Validation Tool
```
Tool: validate_acgme_compliance
Purpose: Full compliance check against all rules
Returns: violations[], warnings[], compliant_areas[]
```

### Supporting Tools
| Tool | Use Case |
|------|----------|
| `get_schedule` | Retrieve schedule data for analysis |
| `check_utilization_threshold_tool` | Verify 80% utilization limit |
| `run_contingency_analysis_resilience_tool` | Check N-1 coverage |

## Validation Workflow

### Phase 1: Data Gathering and Analysis

**Step 1.1: Collect Schedule Data**
```bash
# Use MCP tool to get current schedule
mcp call validate_acgme_compliance --schedule_id=current
```

Response includes:
- All assignments for specified period
- Work hours accumulated per resident
- Duty period configurations
- Supervision assignments

**Step 1.2: Extract Compliance Metrics**
For each resident:
- [ ] Cumulative hours this week/4-week average
- [ ] Days off in last 7 days
- [ ] Current supervision ratio in each rotation
- [ ] Consecutive duty days count
- [ ] Night float block duration

### Phase 2: Rule-by-Rule Analysis

**Step 2.1: 80-Hour Rule Analysis**
```
For each resident:
1. Calculate rolling 4-week average
   = (Week-4 + Week-3 + Week-2 + Week-1) / 4

2. Compare to threshold:
   - Compliant: < 80 hours/week average
   - Warning: 75-80 hours/week average
   - Violation: > 80 hours/week average

3. Identify problematic weeks:
   - Which week(s) exceed limit?
   - What assignments cause excess?
```

**Step 2.2: 1-in-7 Rule Analysis**
```
For each resident:
1. Look at each 7-day rolling window
2. Count continuous duty-free days
   - Need at least one 24-hour period off

3. Identify violations:
   - 7+ consecutive duty days = VIOLATION
   - 6 consecutive duty days = WARNING
   - Schedule relief needed by [DATE]
```

**Step 2.3: Supervision Ratio Analysis**
```
For each rotation with residents:
1. Count residents scheduled
2. Count faculty available on shift
3. Calculate ratio by training level
4. Compare to requirements:
   - PGY-1: Must be ≤ 2:1
   - PGY-2/3: Must be ≤ 4:1

4. Flag violations:
   - Specific shift/date
   - Gap count (how many too many)
   - Recommended faculty additions
```

**Step 2.4: Duty Period Analysis**
```
For each assignment:
1. Calculate duty period duration
2. Check for adequate rest after:
   - Post-24h call: minimum 8 hours off before next duty
   - Extended (28h): minimum 10 hours off

3. Flag violations with specific dates
```

### Phase 3: Issue Prioritization and Reporting

**Step 3.1: Categorize Findings**
| Severity | Criteria | Response Time |
|----------|----------|---|
| **VIOLATION** | Actual breach of rule | Immediate (today) |
| **WARNING** | Approaching threshold | 48 hours |
| **AT RISK** | Potential issue | Monitor, plan |
| **COMPLIANT** | Within all limits | Continue |

**Step 3.2: Prioritize Issues**
```
Ranking (highest to lowest priority):
1. Violations affecting resident health/safety
2. Systemic violations (recurring pattern)
3. Single-resident violations
4. Warning-level issues
5. At-risk scenarios
```

### Phase 4: Solution Development

**Step 4.1: Root Cause Analysis**
For each issue, identify:
- Underlying cause (staffing gap, schedule design, etc.)
- Whether it's systemic or isolated
- Historical context (has this happened before?)

**Step 4.2: Recommend Specific Fixes**
For violations, provide:
```
Issue: [Specific violation]
Affected: [Names and dates]
Root cause: [Why this happened]
Immediate fix: [Swap or reassignment specific to dates]
Long-term fix: [Schedule design change]
Impact assessment: [How fix affects other residents]
```

**Step 4.3: Validate Fix Doesn't Create New Issues**
After proposing fix:
- [ ] Verify fix resolves the violation
- [ ] Confirm it doesn't violate other rules
- [ ] Check supervision ratios remain compliant
- [ ] Verify affected residents don't now have 80-hour issues

## Escalation Triggers

**Escalate to Program Director when:**
1. Multiple simultaneous violations
2. Systemic pattern (same issue recurring)
3. Fix requires policy exception
4. Involves moonlighting hours
5. Resident health/safety concern

## Common Scenarios

### Scenario: Post-Call Scheduling
**Problem:** Resident scheduled for clinic after 24-hour call
**Rule:** Must have 8+ hours off after extended duty
**Fix:** Remove clinic assignment, ensure coverage

### Scenario: Holiday Coverage
**Problem:** Same residents covering multiple holidays
**Rule:** Fair distribution, 80-hour limit still applies
**Fix:** Rotate holiday assignments, check cumulative hours

### Scenario: Supervision Gap
**Problem:** Night shift with insufficient faculty
**Rule:** PGY-1s need 2:1 supervision
**Fix:** Add faculty coverage or redistribute residents

## Reporting Format

When reporting compliance status:

```
## ACGME Compliance Summary

**Overall Status:** [COMPLIANT / WARNING / VIOLATION]

### Violations (Immediate Action Required)
- [List specific violations with affected people/dates]

### Warnings (Action Within 48h)
- [List warnings approaching thresholds]

### Recommendations
1. [Specific actionable fix]
2. [Specific actionable fix]

### Affected Personnel
- [List names and specific issues]
```

## Integration with Other Skills

### With safe-schedule-generation
**Coordination:** ACGME compliance must be verified after each schedule generation
```
1. safe-schedule-generation creates schedule
2. acgme-compliance validates against all rules
3. If violations found, feedback to schedule generation
4. Repeat until compliant schedule produced
```

### With constraint-preflight
**Coordination:** Ensure constraints encode ACGME rules correctly
```
1. constraint-preflight validates constraint definitions
2. acgme-compliance tests constraints with real schedule data
3. Verify constraints actually prevent violations
```

### With swap-execution
**Coordination:** Verify swaps don't violate ACGME rules
```
1. swap-execution proposes swap
2. acgme-compliance pre-validates swap impact
3. Only execute if compliant
```

## Quick Reference Commands

### Validation Commands
```bash
# Full compliance check
python -m app.scheduling.acgme_validator --schedule_id=current --full-report

# Quick 80-hour check
python -m app.scheduling.acgme_validator --check-rule 80-hour --residents=all

# Specific resident check
python -m app.scheduling.acgme_validator --resident-id=PGY1-01 --period=4-weeks

# Export compliance report
python -m app.scheduling.acgme_validator --schedule_id=current --export=pdf
```

### Database Queries for Analysis
```python
# Get hours for resident this week
SELECT SUM(duration) FROM assignments
WHERE resident_id = 'PGY1-01'
AND assignment_date BETWEEN CURRENT_DATE - 7 AND CURRENT_DATE;

# Check consecutive duty days
SELECT DISTINCT(assignment_date) FROM assignments
WHERE resident_id = 'PGY1-01'
ORDER BY assignment_date DESC LIMIT 10;

# Supervision ratio check
SELECT rotation, COUNT(DISTINCT resident_id), COUNT(DISTINCT faculty_id)
FROM assignments
WHERE assignment_date = CURRENT_DATE
GROUP BY rotation;
```

## Validation Checklist

- [ ] 80-hour rule: All residents average ≤ 80 hours/week (4-week rolling)
- [ ] 1-in-7 rule: No resident has 7+ consecutive duty days
- [ ] Supervision ratios: PGY-1 at 2:1 or better, PGY-2/3 at 4:1 or better
- [ ] Duty periods: No shift exceeds 24 hours (28 max with strategic napping)
- [ ] Post-call rest: ≥ 8 hours off after 24-hour call before next duty
- [ ] Night float limits: ≤ 6 consecutive nights maximum
- [ ] Handoff times: Adequate time for shift handoff documented
- [ ] Time off: Residents able to use protected time
- [ ] No systemic issues: Not a recurring pattern of violations
- [ ] Documentation: Exceptions documented with Program Director approval

## Context Management

**Input Context Requirements:**
- Schedule data (assignments with dates, durations)
- Resident demographics (training level)
- Faculty assignments (supervision tracking)
- Any applicable exceptions or waivers

**Compression Strategy:**
- Keep: Violation summaries, specific issue details
- Remove: Intermediate calculation steps
- Summarize: Pass/fail results from large reports

**Required Context for Next Phase:**
- Identified violations (if any)
- Affected residents and dates
- Root causes identified
- Proposed fixes

## Common Patterns

### Pattern 1: Good - Explicit Rule Implementation
```python
# GOOD: Clear implementation of 80-hour rule
def check_80_hour_rule(resident_id: str) -> Tuple[bool, float]:
    """Check if resident exceeds 80-hour weekly average."""
    weeks = get_last_4_weeks(resident_id)
    hours_per_week = [sum_hours(week) for week in weeks]
    average = sum(hours_per_week) / len(hours_per_week)

    is_compliant = average <= 80.0
    return is_compliant, average
```

### Pattern 2: Problematic - Ambiguous Threshold
```python
# BAD: Unclear threshold and calculation
def check_hours(resident_id):
    hours = get_hours(resident_id)  # What period?
    if hours > 85:  # Why 85? Rule is 80
        return "violation"
```

### Pattern 3: Good - Supervision Ratio Clarity
```python
# GOOD: Clear calculation of supervision ratios
SUPERVISION_RATIOS = {
    "PGY1": 2,  # 2 residents per faculty
    "PGY2": 4,
    "PGY3": 4,
}

def verify_supervision(rotation: Rotation) -> bool:
    """Verify supervision ratios for rotation."""
    for level, max_ratio in SUPERVISION_RATIOS.items():
        residents = count_residents_by_level(rotation, level)
        faculty = count_faculty_in_rotation(rotation)
        actual_ratio = residents / faculty if faculty > 0 else 0

        if actual_ratio > max_ratio:
            log_violation(f"{level}: {actual_ratio}:1 exceeds {max_ratio}:1")
            return False
    return True
```

### Pattern 4: Problematic - Hardcoded Values Without Context
```python
# BAD: Magic numbers without explanation
if days_off < 1:  # Why 1? Context?
    flag_issue()
```

## Error Recovery

**If validation fails unexpectedly:**
1. Verify data source is correct (right schedule ID)
2. Check for data quality issues (missing assignments, invalid dates)
3. Confirm compliance logic matches current ACGME rules
4. If issue persists, escalate to human reviewer with error logs

**If fix implementation fails:**
1. Don't force invalid assignments
2. Report specific constraint that prevents fix
3. Suggest alternative solutions
4. Escalate if no valid solution exists

## Examples

### Example 1: 80-Hour Rule Violation Detection

**Context:** Schedule validation after holiday coverage assignments

**Input:**
```
Resident: PGY1-01
Period: December 20-31, 2025
Weekly hours: [78, 82, 79, 85]
```

**Process:**
1. Calculate 4-week rolling average: (78 + 82 + 79 + 85) / 4 = 81.0 hours/week
2. Compare to threshold: 81.0 > 80.0 → **VIOLATION**
3. Identify problematic week: Week 4 (85 hours) exceeds limit
4. Analyze assignments in Week 4:
   - 3x 24-hour call shifts = 72 hours
   - 2x clinic half-days = 8 hours
   - 1x conference = 5 hours
   - Total: 85 hours

**Output:**
```markdown
## ACGME Compliance Violation

**Severity:** VIOLATION
**Rule:** 80-Hour Weekly Limit
**Affected:** PGY1-01
**Period:** December 20-31, 2025
**Violation:** 81.0 hours/week average (exceeds 80.0)

**Root Cause:** Week 4 (Dec 24-31) has 85 hours due to holiday call stacking

**Immediate Fix:**
1. Remove one 24-hour call shift from Week 4
2. Assign call to PGY2-03 (currently at 72 hours average)
3. Result: PGY1-01 drops to 76.0 hours/week average (compliant)

**Long-term Fix:**
- Implement holiday coverage rotation to distribute load
- Add constraint: max 2 call shifts per week during holidays
```

### Example 2: Supervision Ratio Pre-Validation

**Context:** Night shift schedule validation before deployment

**Input:**
```
Rotation: Night Float Inpatient
Date: January 15, 2026
Residents scheduled: 6 (4 PGY-1, 2 PGY-2)
Faculty scheduled: 1
```

**Process:**
1. Calculate supervision ratios:
   - PGY-1: 4 residents / 1 faculty = 4:1 ratio
   - PGY-2: 2 residents / 1 faculty = 2:1 ratio
2. Compare to requirements:
   - PGY-1 required: ≤ 2:1, actual: 4:1 → **VIOLATION**
   - PGY-2 required: ≤ 4:1, actual: 2:1 → COMPLIANT
3. Calculate gap: Need 2 faculty total (4 PGY-1s ÷ 2 = 2), currently have 1
4. Identify solution: Add 1 more faculty to night shift

**Output:**
```markdown
## ACGME Supervision Violation

**Severity:** VIOLATION
**Rule:** PGY-1 Supervision Ratio (2:1 maximum)
**Date:** January 15, 2026
**Rotation:** Night Float Inpatient

**Current State:**
- 4 PGY-1 residents
- 1 faculty
- Ratio: 4:1 (exceeds 2:1 requirement)

**Required Action:**
- Add 1 additional faculty to night shift
- Suggested: FAC-04 (available, credentialed for night float)

**Verification:**
- Post-fix ratio: 4 PGY-1 / 2 faculty = 2:1 (compliant)
```

## Common Failure Modes

| Failure Mode | Symptom | Root Cause | Recovery Steps |
|--------------|---------|------------|----------------|
| **False Positive - "Violation" on Compliant Schedule** | Tool reports 80-hour violation when resident worked 78 hours | Calculation includes non-duty time (breaks, meals) | 1. Verify duty hour definition<br>2. Exclude breaks/meals from calculation<br>3. Re-run validation with corrected data |
| **Missing Consecutive Day Off** | Tool misses 1-in-7 violation | Algorithm only checks calendar days, not 24-hour periods | 1. Rewrite check to use 24-hour rolling windows<br>2. Account for shift boundaries (e.g., 11 PM - 11 PM) |
| **Supervision Ratio Miscalculation** | Faculty counted as "available" but on leave | Data source doesn't reflect real-time availability | 1. Cross-check with absence/leave calendar<br>2. Mark faculty as unavailable if on TDY/leave<br>3. Re-run supervision check |
| **Data Staleness** | Validation uses outdated schedule data | Cache not invalidated after swap | 1. Clear schedule cache<br>2. Re-fetch from database<br>3. Re-run validation |
| **Rule Misinterpretation** | Flagging night float as violation | Applying wrong duty period limits to night float | 1. Review ACGME night float exceptions<br>2. Update constraint to allow 6 consecutive nights<br>3. Document exception in validation logic |
| **Fix Creates New Violation** | Resolving 80-hour issue causes 1-in-7 violation | Insufficient validation of proposed fix | 1. Run full compliance check on proposed fix<br>2. Use iterative solver to find compliant solution<br>3. If no solution exists, escalate to Program Director |

## Integration with Other Skills

### With safe-schedule-generation
**Coordination:** ACGME compliance must be verified after each schedule generation
```
1. safe-schedule-generation creates schedule
2. acgme-compliance validates against all rules
3. If violations found, feedback to schedule generation
4. Repeat until compliant schedule produced
```

### With constraint-preflight
**Coordination:** Ensure constraints encode ACGME rules correctly
```
1. constraint-preflight validates constraint definitions
2. acgme-compliance tests constraints with real schedule data
3. Verify constraints actually prevent violations
```

### With swap-execution
**Coordination:** Verify swaps don't violate ACGME rules
```
1. swap-execution proposes swap
2. acgme-compliance pre-validates swap impact
3. Only execute if compliant
```

### With schedule-validator (MCP Tool)
**Tool Usage Pattern:**
```bash
# Get validation data
schedule_data=$(mcp call get_schedule --schedule_id=current)

# Run comprehensive ACGME check
violations=$(mcp call validate_acgme_compliance --data="$schedule_data")

# If violations found, generate remediation plan
if [ -n "$violations" ]; then
  # Use acgme-compliance skill to analyze and propose fixes
  # Then call swap_execution or schedule_generation to implement
fi
```

## Validation Checklist

After running ACGME compliance validation, verify:

- [ ] **80-hour rule:** All residents average ≤ 80 hours/week (4-week rolling)
- [ ] **1-in-7 rule:** No resident has 7+ consecutive duty days
- [ ] **Supervision ratios:** PGY-1 at 2:1 or better, PGY-2/3 at 4:1 or better
- [ ] **Duty periods:** No shift exceeds 24 hours (28 max with strategic napping)
- [ ] **Post-call rest:** ≥ 8 hours off after 24-hour call before next duty
- [ ] **Night float limits:** ≤ 6 consecutive nights maximum
- [ ] **Handoff times:** Adequate time for shift handoff documented
- [ ] **Time off:** Residents able to use protected time
- [ ] **No systemic issues:** Not a recurring pattern of violations
- [ ] **Documentation:** Exceptions documented with Program Director approval
- [ ] **Data freshness:** Validation used current schedule data (not cached)
- [ ] **Fix validation:** Proposed fixes don't create new violations

## References

- See `thresholds.md` for configurable warning levels
- See `exceptions.md` for documented exception procedures
- ACGME Common Program Requirements: https://www.acgme.org/
- See PROMPT_LIBRARY.md for detailed validation prompt templates
