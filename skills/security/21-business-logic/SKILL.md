---
name: business-logic
description: Hunt business logic flaws — race conditions, workflow state bypass, parameter pollution affecting logic, coupon/discount abuse, refund logic, multi-step process bypass, integer overflow, negative quantities, double-spend. Use when looking for non-CVE bugs that require understanding the app's intended workflow.
metadata:
  type: skill
  phase: hunt
  vuln_class: business-logic
---

# Business Logic Flaws

> No scanner finds these. They pay the most.

## When to invoke

**Trigger phrases:**
- "race condition"
- "logic flaw"
- "workflow bypass"
- "double spend"
- "coupon abuse"
- "negative quantity"

## What is a business logic bug?

A flaw where the **technology is correct** but the **business intent is violated**:

- Coupon meant for one-time use is used 10 times
- Refund intended for the buyer is sent to the attacker
- Workflow meant to require admin approval can be skipped
- Rate limit per user can be bypassed via tenant switching
- Negative quantity yields negative price → free items + refund

## The 11 patterns

### Pattern 1: Race conditions (TOCTOU)

```
Time of check ≠ Time of use:
1. Check: "user has 1 coupon left" → true
2. Use:   "decrement coupon, apply discount"

If you fire 50 parallel requests at step 1+2:
- All 50 checks see "1 left" simultaneously
- All 50 uses apply the discount
- One coupon → 50 uses
```

**Apply to:**
- Coupon / promo code redemption
- Withdraw money / payout request
- File upload (each gets unique ID — collision possible)
- Friend request "accept" (creates relationship + grants permission)
- Vote (1 user, 1 vote)
- Like / favorite (intended 1-time per user)
- Account creation with same email
- Invitation acceptance
- 2FA verification (try wrong code in parallel)

### Pattern 2: Negative integers

```
{"quantity": -5, "price": 10}
→ total = -50
→ "refund" or "free + credit"
```

Test every numeric input:
- Quantities
- Amounts
- Discounts
- Pages (`page=-1`)
- Limits (`limit=-1`)
- Offsets

### Pattern 3: Float precision

```
0.1 + 0.2 = 0.30000000000000004 in IEEE-754
"price * quantity * 0.7" tax calc → rounding errors

# Try: price = 0.01, quantity = 100000 → total = 999.99 or 1000?
```

### Pattern 4: Integer overflow

```
{"amount": 9999999999999999999}  ← overflow signed int → negative
{"page": 2147483647 + 1}         ← INT_MAX + 1 = negative
```

### Pattern 5: Workflow skip (forced state transition)

```
Normal flow:
  cart → checkout → payment → confirmation → order_created

Bypass:
  cart → POST /api/order/create directly → order_created (skip payment)

OR:
  cart → checkout → cancel → confirmation     (skip payment by canceling mid-flow)
  cart → POST /confirmation with order_id from old order
```

### Pattern 6: Coupon / discount abuse

- Reuse single-use coupon by:
  - Race condition on apply
  - Logout/login cycle if reset per session
  - Different stripe/payment methods
  - Different cart variations
- Combine coupons that shouldn't combine
- Apply at the wrong stage of checkout
- Apply to wrong items
- Apply expired coupons (server didn't check `exp`)
- Apply admin/internal-only coupons (guessable codes)

### Pattern 7: Refund logic

- Request refund for someone else's order (IDOR)
- Refund + dispute → double refund
- Partial refund + cancel → full refund
- Refund to a different payment method (your card for victim's payment)

### Pattern 8: Tier / subscription manipulation

- Sign up free, then upgrade in a way that bypasses payment
- Cancel subscription but retain access
- Pro features available via direct API call ignoring subscription check

### Pattern 9: Rate limiting bypass

- Per-user rate limit bypassed by switching accounts (no per-IP limit)
- Per-IP bypassed via proxy/IPv6 randomization
- Per-tenant bypassed by signup of multiple tenants
- Bypass via aliasing in GraphQL (see `[[graphql]]`)
- Bypass via batching (one HTTP request, many operations)
- Bypass via case (some apps lowercase email but rate-limit by exact match)

### Pattern 10: Email change / "ownership reassignment"

- Change email on someone else's account (`[[idor-hunting]]`)
- "Transfer ownership" feature — does target user have to approve?
- Forced reassignment via accept-by-default

### Pattern 11: Mass assignment

```json
POST /api/user/update
{
  "name": "new name",
  "email": "new@x.com",
  "role": "admin",         ← shouldn't be settable
  "is_verified": true,
  "tenant_id": 1,          ← shouldn't be changeable
  "credits": 1000000,
  "stripe_customer_id": "cus_X"
}
```

Test every endpoint: throw a fuzzy field list at it.

## Step-by-Step Workflow

### 1. Walk the workflow as a normal user

Sign up, buy something, use a coupon, request a refund. Note **every state transition** and **what triggers it**.

### 2. Map state machine

Draw the flows. Identify:
- Required steps
- Optional steps
- Reversible steps
- Time-sensitive steps
- Single-use actions

### 3. Probe each step independently

For each transition `A → B`:
- Can you trigger B directly without A?
- Can you trigger A twice?
- Can you fork B from A in parallel (race)?
- Does the server check A's state when accepting B?

### 4. Race condition testing

Use **Burp Repeater + Send group in parallel** (Burp 2023+) or **Turbo Intruder**.

```python
# turbo_intruder example
def queueRequests(target, wordlists):
    engine = RequestEngine(
        endpoint=target.endpoint,
        concurrentConnections=30,
        requestsPerConnection=1,
        engine=Engine.THREADED
    )
    # Submit 30 identical coupon-apply requests in parallel
    for i in range(30):
        engine.queue(target.req)

def handleResponse(req, interesting):
    table.add(req)
```

Burp's "Send group in parallel" (last-byte sync) does this natively now.

### 5. Negative / overflow fuzzing

For every numeric parameter:
```
0, -1, -2147483648, 2147483647, 9999999999999999999, 0.0001, 1e10, NaN, Infinity, "1", "1.0", true, false, null, [], {}, "  "
```

### 6. Mass assignment fuzzing

Capture an update endpoint. Add common admin-only fields:
```json
{
  ...,
  "role": "admin",
  "isAdmin": true,
  "is_admin": true,
  "admin": true,
  "permissions": ["*", "admin"],
  "verified": true,
  "email_verified": true,
  "phone_verified": true,
  "tenant_id": "other-tenant",
  "stripe_customer_id": "cus_OTHER",
  "credit_balance": 999999,
  "subscription_tier": "enterprise",
  "is_internal": true,
  "is_staff": true,
  "groups": ["admins"]
}
```

If server silently accepts → mass assignment.

### 7. Coupon discovery & abuse

```bash
# Guess coupon codes
COUPONS=(
    SAVE10 SAVE20 SAVE50 SAVE100
    BLACKFRIDAY CYBERMONDAY HOLIDAY2026
    WELCOME WELCOME10 NEWUSER FIRSTBUY
    FREESHIP FREE
    ADMIN STAFF EMPLOYEE INTERNAL
    TEST DEBUG
    REFER100 REFERRAL
    {company-name}-launch
)

for code in "${COUPONS[@]}"; do
    curl -s -X POST "https://target.com/api/cart/apply-coupon" \
        -H "Content-Type: application/json" \
        -d "{\"code\":\"$code\"}"
done | grep -i 'applied\|success\|discount'
```

## Race condition tools

```bash
# turbo intruder (Burp extension) — for HTTP-based races
# nuclei race templates — for known patterns

# Hyper-parallel via http2 in Burp (last-byte sync)
# Send 100 requests with all bytes pre-sent except last bytes
# All servers respond near-simultaneously → race window

# h2c smuggling for races on HTTP/2 backends
```

## Output template

```markdown
## High: Race condition on coupon application — single-use coupon redeemed 30+ times

### Summary
The `/api/cart/apply-coupon` endpoint validates coupon-usage count before incrementing, allowing a Time-of-Check/Time-of-Use (TOCTOU) race. Sending 30 parallel requests with the same single-use coupon results in 30 successful applications, granting 30× the discount.

### Steps to reproduce
1. Log in as any user
2. Add an item to cart
3. Apply a coupon via UI to obtain a single-use code (e.g., "WELCOME20")
4. Capture the request:
   ```http
   POST /api/cart/apply-coupon HTTP/1.1
   Host: app.target.com
   Cookie: session=USER_SESSION
   Content-Type: application/json
   Content-Length: 30

   {"coupon": "WELCOME20"}
   ```
5. Send 30 of these requests in parallel using Burp Repeater "Send group in parallel" (last-byte sync)
6. Observe:
   - 27 out of 30 responses return `200 OK` with `"applied": true`
   - Cart total reduces by 27×20% (compounded)
   - Total comes out to negative — credited to account

### Impact
- Unlimited discount stacking → effective free orders + store credit
- For high-value items (e.g., $5,000 laptop), single attack yields $5,000+ in credit
- Affects all coupon types: percent-off, fixed-amount, freebie

### Suggested fix
- Use atomic DB operation (UPDATE coupons SET uses_count = uses_count + 1 WHERE uses_count < limit AND code = ?)
- OR use a distributed lock (Redis SETNX with TTL) keyed by coupon+user
- OR use a queue with single-threaded processing for redemptions
```

## Cross-references

- `[[idor-hunting]]` — IDOR + logic = often critical
- `[[ato-chains]]` — many ATOs are logic flaws
- `[[graphql]]` — GraphQL batching = built-in race
- `[[oauth-oidc]]` — auth flow races

## Common pitfalls

1. **Reporting "I clicked refund twice" without proving timing.** Use turbo intruder / parallel requests.
2. **Negative-quantity reports without final payment proof.** Show the actual money/refund movement.
3. **Workflow bypass without showing the "intended" workflow first.** Triage doesn't know your app.
4. **Mass assignment that doesn't actually privesc.** Verify the role change took effect on subsequent requests.
5. **"Coupon stacking" that's only client-side.** Server-side validation may catch it; verify server accepts.

## Severity guide

| Logic flaw | Typical bounty |
|---|---|
| Coupon abuse (full discount stacking) | High ($1k-5k) |
| Negative price / amount → refund | High ($1k-10k) depending on real-money impact |
| Race condition giving 2x of a single-use action | Medium-High ($500-3k) |
| Mass assignment → role privesc | Critical ($3k-15k) |
| Workflow bypass (skip payment) | Critical ($5k-30k) |
| Tier upgrade without payment | High-Critical ($2k-10k) |

## Pro tips

- **Sign up for the free tier.** Most logic bugs are in the upgrade / payment flow.
- **Use a real card with declines.** Some bugs only appear on failed payments.
- **Diff API responses across user roles.** Admin endpoints called by user with logic flaw.
- **Read disclosed reports for your target's competitors.** Same SaaS pattern → similar bugs.
- **Watch the "feature releases" page.** New features = new logic = new bugs.
