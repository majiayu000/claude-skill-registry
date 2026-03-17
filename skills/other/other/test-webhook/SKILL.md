---
description: Simulate Paddle webhook events to test payment processing pipeline
handoffs:
  - label: Fix Webhook Handler
    agent: backend-engineer
    prompt: Fix the webhook handler issues identified in the test
    send: false
---

## User Input

```text
$ARGUMENTS
```

Options: `payment-success`, `chargeback`, `refund`, or custom payment_id

## Task

Send a mock Paddle webhook to the local/staging backend to test the full payment → AI → PDF → Email pipeline.

### Steps

1. **Parse Arguments**:
   - `payment-success` or empty: Test successful payment flow
   - `chargeback`: Test chargeback handling
   - `refund`: Test refund processing
   - Custom `pay_123`: Use specified payment_id

2. **Run Helper Script**:
   ```bash
   cd .claude/skills/test-webhook
   python test_webhook_helper.py --event [event_type] --payment-id [payment_id]
   ```

3. **The helper script will**:
   - Check if backend is running
   - Create test quiz data (for payment-success events)
   - Generate webhook payload with proper structure
   - Calculate HMAC-SHA256 signature
   - Send webhook request with headers
   - Monitor pipeline execution
   - Check database for results
   - Report summary

4. **Output will show**:
   - Webhook processing status
   - Pipeline execution times (AI, PDF, Blob, Email)
   - Database record verification
   - Total completion time
   - Any errors or issues

## Example Usage

```bash
/test-webhook                     # Test payment success flow
/test-webhook payment-success     # Same as above
/test-webhook chargeback          # Test chargeback handling
/test-webhook refund              # Test refund processing
/test-webhook pay_custom_123      # Use custom payment_id
```

## Exit Criteria

- Webhook request sent with valid signature
- Backend processes webhook successfully
- Full pipeline executes (AI → PDF → Blob → Email)
- Database records created correctly
- Completion time within 90s target

## Testing Scenarios

The helper script supports testing edge cases:
- `--missing-quiz`: Delete quiz before webhook (tests manual_resolution)
- `--duplicate`: Send same payment_id twice (tests idempotency)
- `--invalid-signature`: Send with wrong HMAC (tests validation)
- `--expired-timestamp`: Use old timestamp >5 min (tests timestamp validation)
