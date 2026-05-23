---
name: resend-receipt
description: Resend purchase confirmation emails with download links. Search by order number or email, verify order, and trigger receipt re-send. Solves "I lost my download link" support requests instantly. Triggers on "resend receipt", "send download link", "lost email", "can't find purchase", or similar queries.
allowed-tools: Bash, Read
---

# Resend Receipt Skill

**Purpose:** Instant customer support for lost download links

## What This Skill Does

Resends purchase confirmation emails through Lemon Squeezy API:
1. Order lookup (by number or email)
2. Order verification (paid, not refunded)
3. Receipt email re-send
4. Confirmation to support agent
5. Customer receives fresh download link

## When to Use This Skill

**Common use cases:**
- Customer emails: "I lost my download link"
- "Email went to spam, can you resend?"
- "Bought yesterday but never got confirmation"
- "Deleted email by accident"
- "Need to forward receipt to spouse"
- "Changed email address, need receipt at new address"

**This is the #1 customer support request for digital products.**

## API Authentication

Uses `LEMON_SQUEEZY_API_KEY` environment variable (already set in Cloudflare).

## Usage Examples

**Example 1: Resend by order number**
```
User: Customer lost download link for order #12345
Assistant: [Uses resend-receipt skill]
```

**Example 2: Resend by email**
```
User: Resend receipt to customer@example.com
Assistant: [Looks up order, resends receipt]
```

**Example 3: Multiple orders**
```
User: Customer says they never got confirmation for adrian@example.com
Assistant: [Finds all orders, asks which to resend, processes]
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

### Step 2: Verify Order Eligibility

**Can resend if:**
- ✅ Order status is "paid"
- ✅ Order not refunded
- ✅ Email address valid

**Cannot resend if:**
- ❌ Order status "pending" (no purchase completed)
- ❌ Order status "failed" (payment failed)
- ❌ Order refunded (customer no longer has access)

### Step 3: Resend Receipt

**Endpoint:** `POST https://api.lemonsqueezy.com/v1/orders/{order_id}/resend-receipt`

**Request:**
```bash
curl -X POST "https://api.lemonsqueezy.com/v1/orders/123456/resend-receipt" \
  -H "Accept: application/vnd.api+json" \
  -H "Content-Type: application/vnd.api+json" \
  -H "Authorization: Bearer $LEMON_SQUEEZY_API_KEY"
```

**Response:**
```json
{
  "data": {
    "type": "orders",
    "id": "123456",
    "attributes": {
      "order_number": 12345,
      "user_email": "customer@example.com",
      "receipt_sent": true,
      "receipt_sent_at": "2026-01-06T10:00:00Z"
    }
  }
}
```

**What the customer receives:**
- Email from: `noreply@lemonsqueezy.com` or your custom domain
- Subject: "Your receipt for This Wasn't in the Brochure"
- Contents:
  - Order summary
  - Download links
  - Receipt PDF
  - Support contact

## Output Format

```markdown
# ✅ Receipt Resent Successfully

## Order Details
- **Order Number:** #12345
- **Customer:** John Doe
- **Email:** customer@example.com
- **Product:** This Wasn't in the Brochure (Standard Edition)
- **Purchase Date:** January 1, 2026
- **Amount:** $15.00 AUD

## Receipt Delivery
- **Sent to:** customer@example.com
- **Sent at:** January 6, 2026 10:00 AM
- **Status:** Delivered ✅

## What the Customer Received
✅ Order confirmation email
✅ Download links for all purchased files
✅ PDF receipt
✅ Customer support contact

## Troubleshooting (If Customer Doesn't Receive)

**Tell customer to:**
1. Check spam/junk folder
2. Wait 5-10 minutes (email delivery delay)
3. Add `noreply@lemonsqueezy.com` to contacts
4. Check email spelling is correct: customer@example.com
5. Try different email if still not received

**If still not received after 30 minutes:**
- Email may be blocked by their provider
- Consider manual delivery via support email
- Check Lemon Squeezy email logs
```

## Error Handling

**Order not found:**
```markdown
❌ Order Not Found

**Search criteria:** Order #12345 or customer@example.com

**Possible reasons:**
- Order number typo
- Email typo (ask customer to check confirmation email they did receive)
- Order still pending (payment not completed)
- Order placed with different email

**Next steps:**
1. Ask customer to forward original confirmation email
2. Verify order number (no spaces, correct digits)
3. Ask if they used different email address
4. Check if payment is still pending
```

**Order pending:**
```markdown
⚠️ Order Payment Pending

**Order #12345** has status "pending" (payment not yet completed).

**Cannot resend receipt because:**
- Payment not confirmed yet
- No purchase completed
- No files to deliver

**Options:**
1. Wait for payment to complete (usually 5-30 minutes)
2. Customer should check if payment succeeded in their bank
3. If payment failed, customer needs to repurchase
```

**Order refunded:**
```markdown
⚠️ Order Refunded

**Order #12345** was refunded on January 5, 2026.

**Cannot resend receipt because:**
- Purchase was refunded
- Customer no longer has access
- Download links deactivated

**Options:**
1. Customer can repurchase if they want the book
2. Verify refund was intentional
3. If refund was error, process new purchase
```

**Email delivery failed:**
```markdown
❌ Email Delivery Failed

**Error:** Email bounced or rejected by customer's email provider

**Common causes:**
- Invalid email address
- Email provider blocking Lemon Squeezy
- Inbox full
- Email server down

**Solutions:**
1. Verify email address spelling
2. Try alternative email address
3. Manual delivery: Send download links directly via support email
4. Ask customer to whitelist `noreply@lemonsqueezy.com`
```

## Alternative Delivery Methods

**If email delivery fails repeatedly:**

### Option 1: Manual Email
```markdown
**Subject:** Your Download Links for Order #12345

Hi [Customer],

Your purchase of "This Wasn't in the Brochure" is confirmed!

**Order Details:**
- Order Number: #12345
- Amount Paid: $15.00 AUD
- Purchase Date: January 1, 2026

**Download Your Book:**
[Provide direct Cloudflare Pages link to authenticated download]

**Need Help?**
Reply to this email or visit: https://thiswasntinthebrochure.wtf/account

Best regards,
Adrian Wedd
```

### Option 2: Account Access
```markdown
Direct customer to account portal:
https://thiswasntinthebrochure.wtf/account

They can:
1. Enter order number
2. View all purchases
3. Download files
4. Access receipt
```

### Option 3: Magic Link (Future Enhancement)
```markdown
Generate one-time magic link:
https://thiswasntinthebrochure.wtf/access/[token]

- Valid for 24 hours
- No login required
- Direct file access
```

## Common Support Scenarios

### Scenario 1: "Email Went to Spam"
```markdown
**Action:** Resend + spam folder instructions

Hi [Customer],

I've resent your receipt to [email]. It should arrive in 5-10 minutes.

**Check your spam folder:**
1. Look for email from noreply@lemonsqueezy.com
2. Mark as "Not Spam"
3. Add sender to contacts

If still not there in 30 minutes, reply and I'll send the links directly.
```

### Scenario 2: "Never Got Confirmation"
```markdown
**Action:** Verify order exists, resend, troubleshoot

Hi [Customer],

I found your order #12345 from January 1. The receipt was originally sent to [email].

I've just resent it - should arrive in 5-10 minutes.

**Can't find it?**
- Check spam/junk folder
- Try searching your email for "Lemon Squeezy"
- Reply if still not received after 30 minutes

I'm here to help!
```

### Scenario 3: "Need to Forward to Spouse"
```markdown
**Action:** Resend to original email (they can forward)

Hi [Customer],

I've resent the receipt to [original email].

You can forward that email to your spouse - all the download links will work for them too.

Alternatively, they can access the files at:
https://thiswasntinthebrochure.wtf/account (using order #12345)
```

### Scenario 4: "Changed Email Address"
```markdown
**Action:** Cannot change email, provide workaround

Hi [Customer],

Unfortunately, I can't change the email address on the order (security policy).

**But here's what you can do:**

Option 1: Forward the email from your old address to your new one
Option 2: Access files at https://thiswasntinthebrochure.wtf/account (using order #12345)
Option 3: I can send you the download links directly to your new email

Which would you prefer?
```

## Bulk Resend Operations

**Scenario: "Never received confirmation" (multiple customers)**

If webhook failure caused multiple customers to miss receipts:

```bash
# Get all orders from specific date range
curl "https://api.lemonsqueezy.com/v1/orders?filter[store_id]=YOUR_STORE_ID&page[size]=100" \
  -H "Authorization: Bearer $API_KEY" | \
  # Filter by date, resend to all
  ...
```

**Use case:**
- Webhook downtime (Jan 1-5, 2026)
- Email provider issue
- System migration

**Process:**
1. Identify affected orders (date range, status "paid", receipt not sent)
2. Get approval from user before bulk operation
3. Resend in batches (10-20 at a time to avoid rate limits)
4. Log successes/failures
5. Follow up with any failures

## Testing

**Test receipt resend (TEST mode):**
1. Create test order: 4242 4242 4242 4242
2. Wait for order to show "paid"
3. Use skill to resend receipt
4. Check test email inbox
5. Verify download links work
6. Confirm receipt PDF correct

## Related Skills

- `/customer-lookup` - Find customer's orders
- `/order-lookup` - Verify order details before resending
- `/refund-order` - If customer wants refund instead of access

## API Documentation

**Lemon Squeezy Orders API:**
- Resend receipt: https://docs.lemonsqueezy.com/api/orders#resend-an-order-receipt
- List orders: https://docs.lemonsqueezy.com/api/orders#list-all-orders
- Get order: https://docs.lemonsqueezy.com/api/orders#retrieve-an-order

## Performance Metrics

**Track these to optimize support:**
- Time from request to receipt sent (target: <2 minutes)
- % of customers who receive email successfully (target: >98%)
- % of customers who need follow-up (target: <5%)
- % resolved with resend vs. manual delivery (target: >90% resend)

## Email Deliverability Tips

**Improve delivery rates:**
1. Use custom sending domain (not noreply@lemonsqueezy.com)
2. Set up SPF/DKIM/DMARC records
3. Monitor bounce rates
4. Remove invalid emails from list
5. Ask customers to whitelist sender

**Red flags (likely spam):**
- Free email providers (Gmail, Hotmail) with aggressive filters
- Corporate email with strict IT policies
- Temporary/disposable email addresses
- Typos in email address

## Automation Opportunities

**Auto-resend triggers (future):**
- Customer visits `/account` with order number → No previous email → Auto-resend
- Customer clicks "Resend Receipt" button → Self-service resend
- Failed webhook → Auto-resend after 1 hour
- Customer opens support ticket → Auto-suggest resend before human intervention

**Self-Service Portal:**
```
https://thiswasntinthebrochure.wtf/resend-receipt
- Enter order number
- Verify email
- Click "Resend"
- Instant delivery
```

## Security Considerations

**Verify customer identity:**
- Order number proves they received original email
- Email match confirms they're the buyer
- Don't resend to different email without verification

**Prevent abuse:**
- Rate limit: Max 3 resends per order per day
- Log all resend requests
- Flag suspicious patterns (multiple resends to different emails)

**Privacy:**
- Never reveal full email in logs (mask: cus****@example.com)
- Don't include payment details in resent email
- Use secure HTTPS links only
