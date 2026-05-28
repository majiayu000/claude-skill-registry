---
name: SWAP_EXECUTION
description: Execute resident-requested swaps with safety checks, audit trails, rollback capabilities, and escalation procedures. Use when processing swap requests, validating against constraints, or managing swap lifecycle including rollbacks.
---

# Swap Execution Skill

Production-ready swap execution with comprehensive safety checks, audit trails, and rollback capabilities.

## When This Skill Activates

- Processing incoming swap requests
- Validating swap compliance against Tier 1/2/3 constraints
- Executing validated swaps
- Rolling back problematic swaps
- Investigating swap failures or conflicts
- Escalating complex swap scenarios

## Overview

The swap execution system transforms resident/faculty schedule swap requests into safe, auditable database transactions. It operates in **5 distinct phases** with safety checks at each stage.

### The Five Phases

1. **Intake** - Parse and normalize the request
2. **Safety Checks** - Validate against constraints and conflicts
3. **Execution** - Update database with full audit trail
4. **Verification** - Confirm expected state
5. **Monitoring** - Track for 24h rollback window

## System Architecture

```
┌──────────────┐
│ Swap Request │ (Resident/Faculty initiates)
└──────┬───────┘
       │
       v
┌──────────────────────────────────────┐
│ PHASE 1: Request Intake              │
│ - Parse request JSON                 │
│ - Normalize dates/UUIDs              │
│ - Record requestor + timestamp       │
└──────┬───────────────────────────────┘
       │
       v
┌──────────────────────────────────────┐
│ PHASE 2: Safety Checks               │
│ - Constraint validation (3 tiers)   │
│ - Conflict detection                 │
│ - Resilience impact assessment       │
└──────┬───────────────────────────────┘
       │
       ├─[REJECT]─> Record reason + notify requestor
       │
       ├─[FLAG]───> Escalate to faculty for approval
       │
       v [PROCEED]
┌──────────────────────────────────────┐
│ PHASE 3: Execution                   │
│ - Create SwapRecord (EXECUTED)       │
│ - Update assignments                 │
│ - Update call cascade (Fri/Sat)      │
│ - Commit transaction                 │
└──────┬───────────────────────────────┘
       │
       v
┌──────────────────────────────────────┐
│ PHASE 4: Verification                │
│ - Confirm assignments updated        │
│ - Re-run constraint checks           │
│ - Notify affected parties            │
└──────┬───────────────────────────────┘
       │
       v
┌──────────────────────────────────────┐
│ PHASE 5: Monitoring                  │
│ - 24h rollback window active         │
│ - Watch for complaints/conflicts     │
│ - Auto-rollback on critical failures │
└──────────────────────────────────────┘
```

## Key Files

| File | Purpose |
|------|---------|
| `backend/app/models/swap.py` | SwapRecord, SwapStatus, SwapType models |
| `backend/app/services/swap_executor.py` | Core execution logic + rollback |
| `backend/app/services/swap_validation.py` | Pre-execution safety checks |
| `backend/app/services/swap_request_service.py` | Request intake + parsing |
| `backend/app/api/routes/swap.py` | API endpoints |
| `backend/tests/test_swap_executor.py` | Test coverage |

## Workflows

Each phase has a dedicated workflow document:

1. **[swap-request-intake.md](Workflows/swap-request-intake.md)** - Receive and parse swap requests
2. **[safety-checks.md](Workflows/safety-checks.md)** - Validate swap doesn't break rules
3. **[audit-trail.md](Workflows/audit-trail.md)** - Log all swap decisions
4. **[rollback-procedures.md](Workflows/rollback-procedures.md)** - Undo if something goes wrong

## Reference Documentation

- **[swap-failure-modes.md](Reference/swap-failure-modes.md)** - Common failure patterns with detection
- **[escalation-matrix.md](Reference/escalation-matrix.md)** - When to involve faculty/coordinator

## Output Format

When processing a swap request, always report in this format:

```markdown
## Swap Execution Report

**Request ID:** [UUID]
**Type:** [ONE_TO_ONE / ABSORB]
**Status:** [PENDING / EXECUTED / REJECTED / ROLLED_BACK]
**Requested By:** [Person Name/ID]
**Requested At:** [ISO timestamp]

### Parties
- **Source Faculty:** [Name] (ID: [UUID])
  - Week: [YYYY-MM-DD]
  - Current Hours: [X/80]
- **Target Faculty:** [Name] (ID: [UUID])
  - Week: [YYYY-MM-DD or null for ABSORB]
  - Current Hours: [Y/80]

### Safety Check Results
- **Tier 1 (Hard Constraints):** [PASS / FAIL]
  - 80-Hour Rule: [status]
  - 1-in-7 Rule: [status]
  - Supervision Ratios: [status]
- **Tier 2 (Soft Constraints):** [PASS / WARN]
  - Back-to-back conflicts: [details]
  - Coverage gaps: [details]
- **Tier 3 (Resilience):** [PASS / WARN]
  - Utilization impact: [before/after]
  - N-1 contingency: [status]

### Decision
- **Outcome:** [EXECUTED / REJECTED / ESCALATED]
- **Rationale:** [Explanation]
- **Executed At:** [timestamp if executed]
- **Swap ID:** [UUID if executed]

### Audit Trail
- Logged to: `swap_records` table
- Transaction ID: [DB transaction ID]
- Rollback eligible until: [timestamp + 24h]

### Next Steps
1. [Action item]
2. [Action item]
```

## Error Handling

### Validation Failures

Always provide **specific, actionable** error messages:

**Bad:**
```
"Swap failed validation"
```

**Good:**
```
"Swap rejected: Target faculty (Dr. Smith) has blocking absence
(TDY) from 2025-01-14 to 2025-01-18, overlapping with source
week 2025-01-15. Suggest alternative weeks: 2025-01-22, 2025-01-29."
```

### Execution Failures

On execution failure:
1. **Rollback database transaction** immediately
2. **Record failure reason** in audit log
3. **Notify requestor** with explanation
4. **Log for post-mortem** (don't leak sensitive data)

Example:
```python
try:
    # Execute swap
    result = executor.execute_swap(...)
except IntegrityError as e:
    logger.error(f"Swap {swap_id} failed: database integrity violation",
                 exc_info=True)
    return {
        "success": False,
        "error_code": "INTEGRITY_VIOLATION",
        "message": "Schedule conflict detected. Please refresh and try again."
    }
```

## Escalation Triggers

Automatically escalate to human when:

| Condition | Escalate To | Reason |
|-----------|------------|--------|
| Tier 2 constraint violation | Architect/Coordinator | Soft constraint override needed |
| Sensitive reason (fellowship interview) | Faculty/PD | Privacy + fairness |
| Multiple failed attempts (3+) | Coordinator | Possible scheduling issue |
| Resilience degradation > 10% | Architect | System health impact |
| Moonlighting conflict | Program Director | ACGME compliance risk |

See [escalation-matrix.md](Reference/escalation-matrix.md) for full decision tree.

## Common Scenarios

### Scenario 1: Simple One-to-One Swap (AUTO-APPROVED)

**Request:**
```json
{
  "source_faculty_id": "uuid-a",
  "source_week": "2025-02-03",
  "target_faculty_id": "uuid-b",
  "target_week": "2025-02-10",
  "swap_type": "one_to_one",
  "reason": "Conference attendance"
}
```

**Process:**
1. Intake: Normalize dates, validate UUIDs exist
2. Safety: All checks PASS
3. Execution: Update assignments, create SwapRecord
4. Verification: Confirm state
5. Monitoring: 24h rollback window starts

**Outcome:** AUTO-APPROVED, executed immediately

---

### Scenario 2: Absorb with Back-to-Back Conflict (REJECTED)

**Request:**
```json
{
  "source_faculty_id": "uuid-a",
  "source_week": "2025-02-03",
  "target_faculty_id": "uuid-b",
  "target_week": null,
  "swap_type": "absorb",
  "reason": "PTO"
}
```

**Safety Check Result:**
```
ERROR: Target faculty already has FMIT weeks 2025-01-27 and 2025-02-10.
Taking 2025-02-03 would create 3 consecutive weeks (burnout risk).
```

**Outcome:** REJECTED, suggest alternative faculty or weeks

---

### Scenario 3: Fellowship Interview (ESCALATED)

**Request:**
```json
{
  "source_faculty_id": "uuid-a",
  "source_week": "2025-03-17",
  "target_faculty_id": "uuid-b",
  "target_week": "2025-03-24",
  "swap_type": "one_to_one",
  "reason": "fellowship_interview"
}
```

**Safety Check Result:**
```
PASS (all constraints satisfied)
```

**Escalation Trigger:**
```
Reason code "fellowship_interview" requires PD approval
for fairness and confidentiality.
```

**Outcome:** ESCALATED to Program Director for approval

---

## Testing Checklist

Before deploying swap execution changes:

- [ ] Unit tests for `SwapExecutor` pass
- [ ] Unit tests for `SwapValidationService` pass
- [ ] Integration tests with actual DB pass
- [ ] Rollback window enforcement tested
- [ ] Constraint validation tested for all tiers
- [ ] Audit trail creation verified
- [ ] Notification delivery tested
- [ ] Escalation routing tested

```bash
# Run swap-specific tests
cd backend
pytest tests/test_swap_*.py -v

# Run integration tests
pytest tests/integration/test_swap_workflow.py -v
```

## Rollback Safety

**Critical:** Swaps can be rolled back within 24 hours.

- **Purpose:** Catch mistakes, resolve disputes, fix data errors
- **Window:** 24 hours from `executed_at` timestamp
- **Process:** See [rollback-procedures.md](Workflows/rollback-procedures.md)
- **Constraints:** Cannot rollback if outside window or if `status != EXECUTED`

```python
# Check if rollback eligible
executor = SwapExecutor(db)
can_rollback = executor.can_rollback(swap_id)

if can_rollback:
    result = executor.rollback_swap(
        swap_id=swap_id,
        reason="Resident reported schedule conflict",
        rolled_back_by_id=current_user_id
    )
```

## Performance Considerations

- **N+1 Query Prevention:** Use `selectinload()` for assignments
- **Batch Operations:** Group related updates in single transaction
- **Validation Caching:** Cache constraint results for repeated checks
- **Async Notifications:** Send emails/Slack messages asynchronously (Celery)

See `backend/app/services/swap_executor.py` for N+1 optimization examples.

## Security Considerations

- **Authorization:** Only requestor or admins can rollback
- **Audit Trail:** All actions logged with user ID + timestamp
- **Data Sanitization:** No PII in error messages
- **Rate Limiting:** Max 10 swap requests per user per day
- **Validation:** All inputs sanitized via Pydantic schemas

---

**For detailed phase documentation, see the Workflows/ directory.**
**For failure patterns and escalation rules, see the Reference/ directory.**
