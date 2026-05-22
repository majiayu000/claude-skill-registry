---
name: verify-fix
description: "Mandatory incident fix verification with observables. Invoke after: applying production fixes, before declaring incidents resolved, when someone says 'I think that fixed it'. Requires log entries, metric changes, and database state confirmation."
---

# /verify-fix - Verify Incident Fix with Observables

**MANDATORY** verification step after any production incident fix.

## Philosophy

A fix is just a hypothesis until proven by metrics. "That should fix it" is not verification.

## When to Use

- After applying ANY fix to a production incident
- Before declaring an incident resolved
- When someone says "I think that fixed it"

## Verification Protocol

### 1. Define Observable Success Criteria

Before testing, explicitly state what we expect to see:

```
SUCCESS CRITERIA:
- [ ] Log entry: "[specific log message]"
- [ ] Metric change: [metric] goes from [X] to [Y]
- [ ] Database state: [field] = [expected value]
- [ ] API response: [endpoint] returns [expected response]
```

### 2. Trigger Test Event

```bash
# For webhook issues:
stripe events resend [event_id] --webhook-endpoint [endpoint_id]

# For API issues:
curl -X POST [endpoint] -d '[test payload]'

# For auth issues:
# Log in as test user, perform action
```

### 3. Observe Results

```bash
# Watch logs in real-time
vercel logs [app] --json | grep [pattern]

# Or for Convex:
npx convex logs --prod | grep [pattern]

# Check metrics
stripe events retrieve [event_id] | jq '.pending_webhooks'
```

### 4. Verify Database State

```bash
# Check the affected record
npx convex run --prod [query] '{"id": "[affected_id]"}'
```

### 5. Document Evidence

```
VERIFICATION EVIDENCE:
- Timestamp: [when]
- Test performed: [what we did]
- Log entry observed: [paste relevant log]
- Metric before: [value]
- Metric after: [value]
- Database state confirmed: [yes/no]

VERDICT: [VERIFIED / NOT VERIFIED]
```

## Red Flags (Fix NOT Verified)

- "The code looks right now"
- "The config is correct"
- "It should work"
- "Let's wait and see"
- No log entry observed
- Metrics unchanged
- Can't reproduce the original symptom

## Example: Webhook Fix Verification

```bash
# 1. Resend the failing event
stripe events resend evt_xxx --webhook-endpoint we_xxx

# 2. Watch logs (expect to see "Webhook received")
timeout 15 vercel logs app --json | grep webhook

# 3. Check delivery metric (expect decrease)
stripe events retrieve evt_xxx | jq '.pending_webhooks'
# Before: 4, After: 3 = DELIVERY SUCCEEDED

# 4. Check database state
npx convex run --prod users/queries:getUserByClerkId '{"clerkId": "user_xxx"}'
# Expect: subscriptionStatus = "active"

# VERDICT: VERIFIED - all 4 checks passed
```

## If Verification Fails

1. **Don't panic** - the fix hypothesis was wrong, that's okay
2. **Revert** if the fix made things worse
3. **Loop back** to observation phase (OODA-V)
4. **Question assumptions** - what did we miss?
