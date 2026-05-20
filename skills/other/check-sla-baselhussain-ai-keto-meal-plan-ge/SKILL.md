---
description: Check manual resolution queue for SLA breaches and trigger auto-refunds
handoffs:
  - label: Resolve Manual Queue Item
    agent: backend-engineer
    prompt: Help resolve the manual queue item
    send: false
---

## User Input

```text
$ARGUMENTS
```

Options: `alert` (send alerts for breaches), empty (report only)

## Task

Check manual_resolution queue for SLA deadline breaches and optionally trigger auto-refunds.

### Steps

1. **Query Manual Resolution Queue**:
   ```bash
   cd backend
   python -c "
   from src.models.manual_resolution import ManualResolution
   from src.lib.database import SessionLocal
   from datetime import datetime

   db = SessionLocal()

   # Get all pending cases
   pending = db.query(ManualResolution).filter_by(status='pending').all()

   # Get SLA breaches
   breaches = db.query(ManualResolution).filter(
       ManualResolution.sla_deadline < datetime.utcnow(),
       ManualResolution.status == 'pending'
   ).all()

   print(f'Total Pending: {len(pending)}')
   print(f'SLA Breaches: {len(breaches)}')

   for breach in breaches:
       hours_past = (datetime.utcnow() - breach.sla_deadline).total_seconds() / 3600
       print(f'  - {breach.payment_id}: {hours_past:.1f}h past deadline')
       print(f'    Issue: {breach.issue_type}')
       print(f'    Created: {breach.created_at}')
   "
   ```

2. **Calculate Time to SLA Deadline** (for pending cases):
   ```python
   for case in pending:
       if case.sla_deadline > datetime.utcnow():
           hours_remaining = (case.sla_deadline - datetime.utcnow()).total_seconds() / 3600
           print(f'  - {case.payment_id}: {hours_remaining:.1f}h remaining')
       else:
           hours_past = (datetime.utcnow() - case.sla_deadline).total_seconds() / 3600
           print(f'  - {case.payment_id}: {hours_past:.1f}h PAST DEADLINE')
   ```

3. **Check Auto-Refund Eligibility** (FR-P-012):
   ```bash
   python -c "
   from src.services.paddle_refunds import check_refund_eligibility

   for breach in breaches:
       eligible = check_refund_eligibility(breach.payment_id)

       if eligible:
           print(f'✅ {breach.payment_id}: Eligible for auto-refund')
       else:
           print(f'⚠️ {breach.payment_id}: Manual method, route to manual queue')
   "
   ```

4. **Trigger Auto-Refunds** (if --alert flag):
   ```bash
   python -c "
   from src.services.sla_monitor import process_sla_breaches

   # This will:
   # 1. Check Paddle payment method compatibility
   # 2. Trigger refund for eligible cases (card, Apple Pay, Google Pay)
   # 3. Update manual_resolution status to 'sla_missed_refunded'
   # 4. Send email notification to customer
   # 5. Log high-priority Sentry alert

   results = process_sla_breaches()

   print(f'Auto-refunds triggered: {results["refunded"]}')
   print(f'Manual review required: {results["manual"]}')
   "
   ```

5. **Send Sentry Alerts** (for breaches):
   ```bash
   python -c "
   import sentry_sdk

   for breach in breaches:
       sentry_sdk.capture_message(
           f'SLA breach: {breach.payment_id}',
           level='error',
           extra={
               'payment_id': breach.payment_id,
               'issue_type': breach.issue_type,
               'hours_past_deadline': hours_past,
               'created_at': breach.created_at.isoformat()
           }
       )
   "
   ```

6. **Output Summary**:
   ```
   ✅ SLA Monitoring Report
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Timestamp: 2025-12-30 12:34:56 UTC

   Manual Resolution Queue:
   📊 Total Pending: 5 cases
   📊 SLA Breaches: 2 cases
   📊 Approaching SLA (<1h): 1 case

   Breaches:
   🔴 pay_abc123 (missing_quiz_data)
      - 2.3 hours past deadline
      - ✅ Auto-refund eligible
      - Status: Refund triggered

   🔴 pay_def456 (ai_generation_failed)
      - 1.7 hours past deadline
      - ⚠️ Bank transfer - manual review required
      - Status: Escalated to manual queue

   Approaching SLA:
   🟡 pay_ghi789 (email_delivery_failed)
      - 0.8 hours remaining
      - Retry scheduled in 15 minutes

   Actions Taken:
   ✅ 1 auto-refund triggered
   ✅ 1 escalated to manual review
   ✅ Sentry alerts sent
   ✅ Customer notifications sent

   Next Check: 15 minutes (automated cron job)
   ```

## Example Usage

```bash
/check-sla         # Report SLA status only
/check-sla alert   # Report + trigger auto-refunds
```

## Exit Criteria

- Manual resolution queue queried
- SLA deadlines calculated
- Breaches identified
- Auto-refunds triggered (if alert mode)
- Sentry alerts sent
- Customer notifications sent

## SLA Policy (FR-M-004, FR-P-012)

- **SLA Deadline**: 4 hours from manual_resolution creation
- **Auto-Refund**: Triggered automatically for compatible payment methods
- **Manual Methods**: Bank transfer, local payment methods route to manual review
- **Escalation**: High-priority Sentry alert + email to operations team
