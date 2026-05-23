---
name: COMPLIANCE_VALIDATION
description: ACGME & institutional rule checking with systematic audit workflows, historical analysis, and violation remediation. Use for compliance audits, violation investigation, and regulatory reporting.
---

# COMPLIANCE_VALIDATION Skill

Comprehensive ACGME compliance validation, historical analysis, and violation remediation for medical residency scheduling. This skill provides systematic audit workflows, trend analysis, and actionable remediation strategies.

## When This Skill Activates

- **Pre-deployment validation** - Before publishing any schedule
- **Regulatory audits** - Monthly/quarterly ACGME reporting
- **Violation investigation** - When compliance issues are detected
- **Historical analysis** - Trend analysis over multiple blocks
- **Remediation planning** - Fixing identified violations
- **Program review preparation** - Annual ACGME site visits
- **Post-swap validation** - After schedule swap execution

## Overview

This skill implements a three-phase compliance approach:

1. **AUDIT** - Systematic checking of current or historical schedules
2. **ANALYZE** - Pattern identification and trend analysis
3. **REMEDIATE** - Violation fixing with minimal disruption

Unlike the general `acgme-compliance` skill (which provides reference knowledge), this skill focuses on **systematic execution** of compliance workflows.

## Key Phases

### Phase 1: Audit
- Load schedule data from database
- Run all Tier 1/2 constraint validators
- Generate comprehensive violation report
- Classify violations by severity (CRITICAL, HIGH, MEDIUM, LOW)
- Identify affected personnel

### Phase 2: Analyze
- Aggregate violations across time periods
- Identify recurring patterns (same rule violated repeatedly)
- Calculate compliance metrics (% compliant blocks, violation rate)
- Generate trend charts (violations over time)
- Root cause analysis (why violations happen)

### Phase 3: Remediate
- Prioritize violations (Tier 1 ACGME first, then institutional)
- Generate remediation strategies for each violation
- Impact assessment (how fix affects other constraints)
- Execute fixes with transaction rollback support
- Verification (re-run validation after fix)

## Constraint Tiers

All constraints are classified into tiers for prioritization:

### Tier 1: ACGME Regulatory (CRITICAL)
**Must fix immediately - regulatory violations**
- 80-Hour Rule: Maximum 80 hours/week averaged over 4 weeks
- 1-in-7 Rule: One 24-hour period off every 7 days
- Supervision Ratios: PGY-specific faculty supervision
- Duty Period Limits: Maximum continuous duty hours
- Availability: No assignments during absences

### Tier 2: Institutional Hard Constraints (HIGH)
**Must fix before deployment - operational requirements**
- FMIT Coverage: Weekly faculty rotation
- Night Float Headcount: Exactly 1 resident
- NICU Friday Clinic: Required clinic day
- Post-Call Blocking: Required recovery time
- Credential Requirements: Slot-type invariants

### Tier 3: Soft Constraints (MEDIUM)
**Should fix if possible - preferences**
- Call spacing: Avoid back-to-back call weeks
- Weekend distribution: Fair distribution
- Clinic day preferences: PGY-specific clinic days

### Tier 4: Optimization Goals (LOW)
**Nice to have - quality improvements**
- Workload balance
- Continuity of care
- Learning opportunities

## Workflows

This skill provides specialized workflows in the `Workflows/` directory:

| Workflow | Purpose | When to Use |
|----------|---------|-------------|
| **audit-current-schedule.md** | Validate active schedule | Pre-deployment, monthly checks |
| **historical-compliance.md** | Analyze past schedules | Quarterly reporting, trend analysis |
| **violation-remediation.md** | Fix identified violations | After audit failures, post-swap |

## Key Files

### Core Validation Code
```
backend/app/services/constraints/acgme.py       - ACGME constraint validators
backend/app/validators/advanced_acgme.py        - Enhanced validators (24+4, NF limits)
backend/app/scheduling/constraints/acgme.py     - Constraint service integration
```

### Database Schema
```
backend/alembic/versions/003_add_acgme_audit_fields.py  - Audit trail schema
backend/app/models/assignment.py                        - Schedule assignments
backend/app/models/person.py                             - Faculty/resident data
backend/app/models/block.py                              - Time blocks
```

### Tests
```
backend/tests/validators/test_advanced_acgme.py         - Unit tests
backend/tests/integration/test_acgme_edge_cases.py      - Integration tests
backend/tests/performance/test_acgme_load.py            - Load testing
```

## Output Format

All compliance reports must follow this structure:

```
╔══════════════════════════════════════════════════════════════════╗
║  ACGME COMPLIANCE AUDIT REPORT                                   ║
║  Schedule: Block 10 (2026-03-12 to 2026-04-08)                  ║
║  Generated: 2025-12-26 15:30:00                                  ║
║  Validator: COMPLIANCE_VALIDATION Skill                          ║
╠══════════════════════════════════════════════════════════════════╣
║  OVERALL STATUS: [COMPLIANT / WARNING / VIOLATION]              ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  TIER 1: ACGME VIOLATIONS (Critical)                            ║
║  ────────────────────────────────────────────────────────────    ║
║  [List violations with person, date, specifics]                  ║
║                                                                  ║
║  TIER 2: INSTITUTIONAL VIOLATIONS (High)                        ║
║  ────────────────────────────────────────────────────────────    ║
║  [List violations]                                               ║
║                                                                  ║
║  TIER 3: SOFT CONSTRAINT WARNINGS (Medium)                      ║
║  ────────────────────────────────────────────────────────────    ║
║  [List warnings]                                                 ║
║                                                                  ║
║  SUMMARY METRICS                                                 ║
║  ────────────────────────────────────────────────────────────    ║
║  Total Violations: 3 (Tier 1: 2, Tier 2: 1)                     ║
║  Affected Personnel: 5 (3 residents, 2 faculty)                 ║
║  Compliance Rate: 94.2% (33/35 constraints passed)              ║
║                                                                  ║
║  RECOMMENDED ACTIONS                                             ║
║  ────────────────────────────────────────────────────────────    ║
║  1. [Specific remediation step]                                  ║
║  2. [Specific remediation step]                                  ║
║  3. [Specific remediation step]                                  ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

## Error Handling

### Database Connection Issues
```python
# Always use try-catch with rollback
try:
    db = SessionLocal()
    result = validate_schedule(db, schedule_id)
    db.commit()
except Exception as e:
    db.rollback()
    logger.error(f"Validation failed: {e}")
    raise
finally:
    db.close()
```

### Missing Data
If data is missing (no assignments, no residents), report clearly:
```
⚠️  VALIDATION INCOMPLETE: No assignments found for Block 10
   Possible causes:
   - Schedule not yet generated
   - Wrong date range
   - Database migration incomplete
```

### Constraint Failures
If a constraint validator fails (not just violations, but crashes):
```
❌ VALIDATOR ERROR: 80HourRule constraint failed to execute
   Error: Division by zero in _calculate_rolling_average()
   Action: Check that blocks exist in date range
```

## MCP Tool Integration

### Primary Tools
```
validate_acgme_compliance          - Run full ACGME validation
get_schedule                       - Retrieve schedule data
check_utilization_threshold_tool   - Verify 80% utilization
run_contingency_analysis          - N-1 coverage check
```

### Remediation Tools
```
execute_swap                       - Fix violations via swaps
get_swap_candidates               - Find compatible swap partners
validate_swap_compliance          - Ensure swap maintains compliance
```

## Escalation Matrix

| Violation Count | Severity | Action Required |
|----------------|----------|-----------------|
| 0 | GREEN | Deploy schedule |
| 1-2 Tier 3 | YELLOW | Fix within 7 days |
| 1-2 Tier 2 | ORANGE | Fix within 48 hours |
| Any Tier 1 | RED | Do not deploy, fix immediately |
| 3+ Tier 1 | BLACK | Escalate to Program Director |

## References

- See `Reference/acgme-rules-detailed.md` for complete ACGME citations
- See `Reference/compliance-glossary.md` for terminology definitions
- See `Workflows/` for step-by-step audit procedures

## Development Notes

**When adding new constraints:**
1. Add validator to `backend/app/services/constraints/acgme.py`
2. Register in `ACGMEConstraintValidator.constraints` list
3. Add unit test in `backend/tests/validators/`
4. Update this skill's reference documentation
5. Classify as Tier 1/2/3/4 for prioritization

**When fixing violations:**
1. Always create database backup first
2. Use transaction rollback if fix fails
3. Re-run validation after fix
4. Document fix in audit trail
5. Update historical compliance metrics
