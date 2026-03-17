---
name: refund-order
description: Process customer refunds quickly. Search by order number or email, view order details, and issue full/partial refunds with automatic customer notifications. Use for customer support, order issues, or goodwill refunds. Triggers on "refund", "issue refund", "process refund", "customer wants refund", or similar queries.
allowed-tools: Bash, Read
---

# Refund Order Skill

**Purpose:** Fast customer refund processing and support

## What This Skill Does

Processes refunds through the Lemon Squeezy API with:
1. Order lookup (by number or email)
2. Order verification (status, amount, refund eligibility)
3. Full or partial refund processing
4. Automatic customer notification
5. Refund confirmation and tracking

## When to Use This Skill

**Common use cases:**
- Customer emails: "I want a refund for order #12345"
- Wrong edition purchased: "Bought AU edition, need US edition"
- Technical issues: "Can't access download"
- Goodwill refund: Unhappy customer, issue refund for customer satisfaction
- Duplicate purchases: "Accidentally bought twice"
- Billing errors: "Charged wrong amount"

## API Authentication

Uses `LEMON_SQUEEZY_API_KEY` environment variable (already set in Cloudflare).

## Usage Examples

**Example 1: Refund by order number**
```
User: Customer wants refund for order #12345
Assistant: [Uses refund-order skill to process refund]
```

**Example 2: Refund by email**
```
User: Issue refund to customer@example.com
Assistant: [Looks up orders, confirms which to refund, processes]
```

**Example 3: Partial refund**
```
User: Give $5 refund to order #12345 (technical issue)
Assistant: [Processes partial refund]
```

## Implementation

### Step 1: Find Order

**By Order Number:**
```bash
curl "https://api.lemonsqueezy.com/v1/orders?filter[store_id]=YOUR_STORE_ID&filter[order_number]=12345" \
  -H "Accept: application/vnd.api+json" \
  -H "Authorization: Bearer $LEMON_SQUEEZY_API_KEY"
```

**By Email:**
```bash
curl "https://api.lemonsqueezy.com/v1/orders?filter[store_id]=YOUR_STORE_ID&filter[user_email]=customer@example.com" \
  -H "Accept: application/vnd.api+json" \
  -H "Authorization: Bearer $LEMON_SQUEEZY_API_KEY"
```

**Response structure:**
```json
{
  "data": [{
    "type": "orders",
    "id": "123456",
    "attributes": {
      "order_number": 12345,
      "user_name": "John Doe",
      "user_email": "customer@example.com",
      "status": "paid",
      "refunded": false,
      "total": 1500,
      "currency": "AUD",
      "created_at": "2026-01-01T12:00:00Z",
      "first_order_item": {
        "product_name": "This Wasn't in the Brochure"
      }
    }
  }]
}
```

### Step 2: Verify Refund Eligibility

**Check before refunding:**
- ✅ Status is "paid"
- ✅ Not already refunded
- ✅ Amount > 0
- ✅ Order exists

**Warning cases:**
```markdown
⚠️ Cannot refund:
- Order status "pending" (payment not completed)
- Order status "failed" (nothing to refund)
- Already refunded (check refunded_at field)
- Order older than 180 days (Stripe limitation - warn user)
```

### Step 3: Process Refund

**Endpoint:** `POST https://api.lemonsqueezy.com/v1/orders/{order_id}/refund`

**Full refund request:**
```bash
curl -X POST "https://api.lemonsqueezy.com/v1/orders/123456/refund" \
  -H "Accept: application/vnd.api+json" \
  -H "Content-Type: application/vnd.api+json" \
  -H "Authorization: Bearer $LEMON_SQUEEZY_API_KEY" \
  -d '{
    "data": {
      "type": "refunds",
      "attributes": {
        "amount": null
      }
    }
  }'
```

**Partial refund request:**
```bash
curl -X POST "https://api.lemonsqueezy.com/v1/orders/123456/refund" \
  -H "Accept: application/vnd.api+json" \
  -H "Content-Type: application/vnd.api+json" \
  -H "Authorization: Bearer $LEMON_SQUEEZY_API_KEY" \
  -d '{
    "data": {
      "type": "refunds",
      "attributes": {
        "amount": 500
      }
    }
  }'
```

**Note:** Amount is in cents (500 = $5.00). Use `null` for full refund.

**Response structure:**
```json
{
  "data": {
    "type": "refunds",
    "id": "789",
    "attributes": {
      "order_id": 123456,
      "amount": 1500,
      "amount_formatted": "$15.00",
      "created_at": "2026-01-06T10:00:00Z",
      "refunded_at": "2026-01-06T10:00:00Z"
    }
  }
}
```

### Step 4: Confirm with Customer

**Lemon Squeezy automatically:**
- Sends refund confirmation email to customer
- Updates order status to "refunded"
- Processes refund through Stripe (5-10 business days to customer)
- Deactivates license keys (if product uses licenses)

**You should:**
- Confirm refund processed successfully
- Tell customer when to expect refund (5-10 business days)
- Optionally: Send personal follow-up email

## Output Format

Present refund results in this structure:

```markdown
# ✅ Refund Processed Successfully

## Order Details
- **Order Number:** #12345
- **Customer:** John Doe (customer@example.com)
- **Original Amount:** $15.00 AUD
- **Product:** This Wasn't in the Brochure (Standard Edition)
- **Purchase Date:** January 1, 2026

## Refund Details
- **Refund Amount:** $15.00 AUD (100% refund)
- **Refund Date:** January 6, 2026
- **Refund ID:** 789
- **Status:** Processed ✅

## What Happens Next
1. ✅ Customer automatically notified via email
2. ✅ Refund processed through Stripe
3. ⏳ Customer will receive refund in 5-10 business days
4. ✅ Order status updated to "refunded"

## Customer Message Template

**Subject:** Refund Processed for Order #12345

Hi John,

Your refund has been processed successfully.

**Refund Details:**
- Amount: $15.00 AUD
- Order: #12345
- Timeframe: 5-10 business days to appear in your account

If you have any questions, just reply to this email.

Best regards,
Adrian Wedd
This Wasn't in the Brochure
```

## Error Handling

**Order not found:**
```markdown
❌ Order not found

**Search criteria:** Order #12345 or customer@example.com

**Possible reasons:**
- Order number typo (check with customer)
- Email typo (ask customer to check confirmation email)
- Order placed in different store
- Order still pending (payment not completed)

**Next steps:**
1. Ask customer to forward confirmation email
2. Check order number carefully (no spaces, correct digits)
3. Verify customer provided correct email address
```

**Already refunded:**
```markdown
⚠️ Order Already Refunded

**Order #12345** was refunded on January 5, 2026.

**Refund Details:**
- Amount: $15.00 AUD
- Refund Date: 2026-01-05
- Status: Completed

**Customer should:**
- Check bank statement (5-10 business days from refund date)
- Contact their bank if refund not received after 10 days
- Reply with bank statement if they claim no refund received
```

**Partial refund exceeds total:**
```markdown
❌ Invalid Refund Amount

**Order Total:** $15.00 AUD
**Requested Refund:** $20.00 AUD

Cannot refund more than order total.

**Options:**
1. Issue full refund ($15.00)
2. Issue partial refund (e.g., $10.00 for partial satisfaction)
```

**Pending order:**
```markdown
⚠️ Order Payment Pending

**Order #12345** has status "pending" (payment not yet completed).

**Cannot refund because:**
- No payment received yet
- Nothing to refund

**Options:**
1. Wait for payment to complete, then refund
2. Customer can cancel payment on their end
3. Contact Lemon Squeezy support if payment stuck
```

**API Error:**
```markdown
❌ Refund Failed

**API Error:** [Error message from Lemon Squeezy]

**Common causes:**
- API key lacks refund permissions
- Network timeout
- Lemon Squeezy service issue

**Next steps:**
1. Retry in 1 minute
2. Check API key has "Write refunds" permission
3. Process refund manually in Lemon Squeezy dashboard
4. Contact Lemon Squeezy support if persistent
```

## Refund Policy Guidance

**Recommended approach:**
- **No questions asked refunds:** First 30 days
- **Goodwill refunds:** Technical issues, customer dissatisfaction
- **Partial refunds:** Minor issues, keep customer happy
- **Educational refund:** "This wasn't what I expected" → full refund + recommend alternative resources

**Don't refund:**
- Customer already accessed all content and just wants money back after finishing book (abuse)
- Customer bought wrong edition → offer swap instead of refund
- Duplicate purchase → refund duplicate, keep one

## Refund Templates by Scenario

### Scenario 1: Wrong Edition Purchased
```markdown
**Action:** Offer edition swap (no refund needed)

Hi [Customer],

I see you purchased the AU edition but needed the US edition. No problem!

I've sent you access to the US edition. You now have both editions.

No refund needed - just use the US edition going forward.

Let me know if you have any questions!
```

### Scenario 2: Technical Issue (Can't Download)
```markdown
**Action:** Fix issue first, refund if can't resolve

Hi [Customer],

I see you're having trouble accessing your download. Let me help!

[Troubleshooting steps...]

If this doesn't work, I'll process a full refund immediately - just let me know.
```

### Scenario 3: "Not What I Expected"
```markdown
**Action:** Full refund + helpful redirect

Hi [Customer],

I'm sorry the book wasn't what you were looking for. I've processed a full refund of $15.00 AUD.

You'll see the refund in 5-10 business days.

If you're looking for [alternative resource], I recommend [suggestion].

Thanks for giving it a try!
```

### Scenario 4: Duplicate Purchase
```markdown
**Action:** Refund duplicate, keep one

Hi [Customer],

I see you accidentally purchased twice. I've refunded the duplicate order (#12346).

Your original order (#12345) is still active with full access.

Refund of $15.00 AUD will appear in 5-10 business days.
```

## Testing

**Test refund flow (TEST mode):**
1. Create test order using test card: 4242 4242 4242 4242
2. Wait for order to show "paid" status
3. Use skill to process refund
4. Verify refund email received
5. Check order status changed to "refunded"
6. Confirm refund appears in Lemon Squeezy dashboard

**Test card (Stripe):**
- Card: 4242 4242 4242 4242
- Expiry: Any future date
- CVC: Any 3 digits
- ZIP: Any 5 digits

## Related Skills

- `/customer-lookup` - Find customer before refunding
- `/order-lookup` - Verify order details
- `/resend-receipt` - If customer just needs access link (no refund needed)

## API Documentation

**Lemon Squeezy Refunds API:**
- Create refund: https://docs.lemonsqueezy.com/api/refunds#create-a-refund
- List refunds: https://docs.lemonsqueezy.com/api/refunds#list-all-refunds
- Get refund: https://docs.lemonsqueezy.com/api/refunds#retrieve-a-refund

## Important Notes

**Stripe Refund Timeline:**
- Refund processed instantly in Lemon Squeezy
- Stripe processes refund within 5-10 business days
- Customer sees "pending refund" in their bank
- Final credit appears after bank processing

**Fee Handling:**
- Lemon Squeezy fees NOT refunded (you lose ~3% + $0.50 per transaction)
- Example: $15 sale → You keep ~$14 after fees → Refund $15 → You're out $1
- Consider this when offering goodwill refunds

**Partial Refund Strategy:**
- Minor issue: 30-50% refund (keeps customer happy, limits loss)
- Major issue: 100% refund (goodwill, reputation protection)
- Very happy customer with tiny issue: Discount code for next purchase instead of refund

## Security Notes

**Never refund to different account:**
- Only refund to original payment method
- Cannot change refund destination
- Prevents fraud/money laundering

**Verify customer identity:**
- Ask for order number (proves they have confirmation email)
- Verify email matches order
- If suspicious, ask for last 4 digits of card used

## Automation Opportunities

**Auto-refund triggers (future enhancement):**
- Order created → Customer requests refund within 5 minutes → Likely duplicate/accident → Auto-refund
- Multiple failed download attempts → Technical issue → Offer instant refund
- Customer can't access content after 24 hours → Webhook failure → Auto-refund + manual delivery

**Metrics to track:**
- Refund rate (%) - Industry standard: 2-5% for digital products
- Time to refund (should be <1 hour during business hours)
- Refund reason categories (helps improve product/experience)
- Customer satisfaction after refund (follow-up survey)
