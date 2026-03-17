---
name: pre-mortem
description: |
  Before starting ANY significant task (feature build, refactor, integration,
  migration, or architectural change), first imagine the project has failed.
  Generate 3-5 specific failure scenarios, assess risk levels, identify
  mitigations, then adjust the implementation plan to address high-risk items
  FIRST. Do not start coding until the pre-mortem is acknowledged.
allowed-tools: |
  bash: find, grep, cat, head, ls, python
  file: read
---

# Pre-mortem

<purpose>
Elite engineers instinctively ask "how could this fail?" before writing code.
Claude does the opposite - jumps to implementation, discovers problems mid-way,
patches reactively. This skill encodes prospective hindsight: imagine failure,
then prevent it.
</purpose>

## Why This Works

Gary Klein's research on prospective hindsight shows teams who imagine failure
identify 30% more risks than teams who just "plan carefully." The mental shift
from "how do we succeed?" to "why did we fail?" unlocks different thinking.

## Instructions

<trigger>
Activate before ANY task involving:
- New feature implementation
- External service integration (payments, auth, APIs)
- Database migrations or schema changes
- Refactoring across multiple files
- Dependency upgrades
- Infrastructure changes
- Anything the user calls "significant" or "important"
</trigger>

### Step 1: Pause Before Implementing

Do NOT start writing code. First, run analysis:

```bash
python scripts/analyse_risk.py --task "<task description>" --path .
```

Or manually assess by examining:
- Files that will be touched
- External dependencies involved
- Data/state that could be corrupted
- User-facing impact if broken

### Step 2: Generate Failure Scenarios

Imagine it's 2 weeks later. The task failed. Ask: **"Why did it fail?"**

Generate 3-5 specific failure scenarios. For each:

| Component | Description |
|-----------|-------------|
| Scenario | Concrete failure description |
| Likelihood | HIGH / MEDIUM / LOW |
| Impact | What breaks if this happens |
| Detection | How would we know it failed |
| Mitigation | How to prevent or reduce risk |

<failure-categories>
Common failure patterns to consider:

**Integration failures:**
- Auth/credentials misconfigured
- Webhook signatures not validated
- Rate limits not handled
- Timeout/retry logic missing
- Test vs production environment confusion

**Data failures:**
- Migration corrupts existing data
- Missing null checks
- Race conditions on concurrent writes
- No rollback path
- Foreign key violations

**Logic failures:**
- Edge cases not handled
- Off-by-one errors in loops/pagination
- Timezone/locale assumptions
- Currency/precision errors
- State machine invalid transitions

**Operational failures:**
- No logging for debugging
- Secrets committed to repo
- No monitoring/alerting
- Deployment breaks rollback
- Missing feature flags
</failure-categories>

### Step 3: Present Pre-mortem

Format output as:

```
Pre-mortem Analysis: [Task Name]

If this fails in 2 weeks, it's probably because:

1. HIGH: [Scenario]
   Impact: [What breaks]
   Mitigation: [How to prevent]

2. HIGH: [Scenario]
   Impact: [What breaks]
   Mitigation: [How to prevent]

3. MED: [Scenario]
   Impact: [What breaks]
   Mitigation: [How to prevent]

4. MED: [Scenario]
   Impact: [What breaks]
   Mitigation: [How to prevent]

5. LOW: [Scenario]
   Impact: [What breaks]
   Mitigation: [How to prevent]

Adjusted Plan:
[Reordered implementation addressing HIGH risks first]

Proceed with this plan?
```

### Step 4: Adjust Implementation Order

Reorder the implementation plan to:
1. Address HIGH risk mitigations first
2. Build verification/detection early
3. Create rollback path before risky changes
4. Add logging before complex logic
5. Then proceed with main implementation

### Step 5: Get Acknowledgment

Do NOT proceed until user confirms. They may:
- Accept the plan
- Add risks you missed
- Deprioritise certain mitigations
- Ask for more detail on specific risks

## Risk Severity Guide

<severity>
**HIGH** - Must mitigate before proceeding:
- Data loss or corruption possible
- Security vulnerability
- Money/billing affected
- No rollback path
- Silent failure (looks fine, actually broken)

**MEDIUM** - Mitigate or explicitly accept risk:
- Poor user experience
- Performance degradation
- Technical debt accumulation
- Manual intervention needed if broken

**LOW** - Note but proceed:
- Cosmetic issues
- Minor inconvenience
- Easy to fix post-launch
- Caught by existing tests
</severity>

## NEVER

- Start significant tasks without pre-mortem
- Generate generic risks (be specific to THIS task)
- Skip high-risk mitigations to save time
- Assume "it probably won't happen"
- Proceed without user acknowledgment

## ALWAYS

- Be specific: "webhook signature validation" not "security issues"
- Include detection method for each risk
- Reorder plan based on risk findings
- Surface risks even if they're awkward
- Acknowledge when you're uncertain about a risk

## Examples

### Example 1: Payment Integration

User: "Add Stripe payment integration"

```
Pre-mortem Analysis: Stripe Payment Integration

If this fails in 2 weeks, it's probably because:

1. HIGH: Webhook signature validation wrong
   Impact: Payments process but our system never knows - orders stuck in limbo
   Detection: Customer complaints about "paid but not delivered"
   Mitigation: Test webhooks with Stripe CLI locally before writing business logic

2. HIGH: No idempotency keys
   Impact: Network retry causes duplicate charges
   Detection: Customer charged twice, refund requests
   Mitigation: Implement idempotency keys from the start, not retrofitted

3. HIGH: Test vs live key confusion
   Impact: Real charges in development, or test mode in production
   Detection: Angry customers or "payments not working" in prod
   Mitigation: Env validation on startup, assert key prefix matches environment

4. MED: Missing error states in UI
   Impact: User sees spinner forever, retries, double charge
   Detection: Support tickets, rage clicks in analytics
   Mitigation: Design loading/error/success states before API integration

5. MED: No payment logging
   Impact: Can't debug failed payments, refund disputes unwinnable
   Detection: "We have no record of this" situations
   Mitigation: Log every payment event with correlation ID

Adjusted Plan:
1. Set up Stripe CLI + webhook endpoint (test signature validation)
2. Implement idempotency key generation
3. Add environment validation (key prefix checks)
4. Build payment service with full logging
5. Create UI states (loading/error/success)
6. Then: actual payment flow implementation
7. End-to-end test with Stripe test cards

Proceed with this plan?
```

### Example 2: Database Migration

User: "Add soft delete to all models"

```
Pre-mortem Analysis: Soft Delete Migration

If this fails in 2 weeks, it's probably because:

1. HIGH: Existing queries return "deleted" records
   Impact: Users see deleted data, privacy/legal issues
   Detection: "Why is this showing up? I deleted it"
   Mitigation: Add default scope, audit ALL existing queries before migration

2. HIGH: Unique constraints now broken
   Impact: Can't recreate record with same email/username after soft delete
   Detection: "Email already exists" on new signup
   Mitigation: Make unique constraints exclude deleted records, or use different approach

3. HIGH: No rollback path
   Impact: If migration fails midway, data integrity unknown
   Detection: 500 errors, inconsistent state
   Mitigation: Test on production clone first, have restore procedure ready

4. MED: Cascade deletes still hard-delete related records
   Impact: Parent soft-deleted but children gone forever
   Detection: Missing related data after restore
   Mitigation: Audit all ON DELETE CASCADE, convert to soft delete

5. MED: Analytics/reporting now wrong
   Impact: Counts include deleted records, metrics inflated
   Detection: "Numbers don't match the UI"
   Mitigation: Update all aggregate queries to filter deleted

Adjusted Plan:
1. Audit all existing queries (grep for affected tables)
2. Audit unique constraints and cascades
3. Design soft delete schema (deleted_at column approach)
4. Create migration with rollback script
5. Test on staging with production data clone
6. Update queries one-by-one with tests
7. Then: deploy migration
8. Monitor for "deleted showing" errors

Proceed with this plan?
```

### Example 3: Minor Task (Pre-mortem Not Needed)

User: "Fix the typo in the error message"

```
This is a trivial change (single string edit). Pre-mortem not needed.

Proceeding directly.
```

<failed-attempts>
What DOESN'T work:

- **Generic risks**: "Security issues" is useless. "Webhook signature validation wrong" is actionable.
- **Skipping for "simple" tasks**: The "simple" migration that corrupts production data.
- **Listing risks without mitigations**: Identifying problems without solutions is just anxiety.
- **Not reordering the plan**: If you identify HIGH risks but still implement in original order, you've wasted the exercise.
- **Perfunctory pre-mortems**: Going through motions without real imagination. Ask "how would this ACTUALLY fail?"
- **Only technical risks**: Missing "team doesn't understand the change" or "deploy on Friday before vacation"
- **Assuming user will read carefully**: Present the most critical risks prominently, not buried in a list.
- **Pre-mortem paralysis**: 15 risks identified, nothing gets built. Focus on HIGH risks, accept some LOW risk.
</failed-attempts>
