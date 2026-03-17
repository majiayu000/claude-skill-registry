---
name: customer-lookup
description: Search for customers by email or order number, view their purchase history, subscriptions, and license keys. Use for customer support, refund processing, or account verification. Triggers on "find customer", "lookup email", "check order", "customer support", or similar queries.
allowed-tools: Bash, Read
---

# Customer Lookup Skill

**Purpose:** Fast customer support and account verification

## What This Skill Does

Searches Lemon Squeezy for customer information using the API. Returns:
1. Customer details (name, email, purchase date)
2. All orders (with status, amount, products)
3. Active subscriptions (if any)
4. License keys (if applicable)
5. Recent activity timeline

## When to Use This Skill

**Common use cases:**
- User emails: "I can't access my book"
- Verify purchase before granting manual access
- Process refund requests
- Check subscription status
- Find order number for user
- Investigate payment issues

## API Authentication

The skill uses the `LEMON_SQUEEZY_API_KEY` environment variable (already set in Cloudflare).

To test locally, set in `.dev.vars`:
```
LEMON_SQUEEZY_API_KEY=your_api_key_here
```

## Usage Examples

**Example 1: Lookup by email**
```
User: Can you check if customer@example.com has purchased the book?
Assistant: [Uses customer-lookup skill]
```

**Example 2: Lookup by order number**
```
User: Customer says their order #12345 isn't working
Assistant: [Uses customer-lookup skill to find order details]
```

**Example 3: Before manual refund**
```
User: Customer wants a refund for order #67890
Assistant: [Uses customer-lookup to verify order exists and is paid]
```

## Implementation

### Step 1: Search Customers API

**Endpoint:** `GET https://api.lemonsqueezy.com/v1/customers`

**Query parameters:**
- `filter[email]` - Search by email
- `filter[store_id]` - Filter to your store only (important!)

**Example request:**
```bash
curl "https://api.lemonsqueezy.com/v1/customers?filter[email]=customer@example.com&filter[store_id]=YOUR_STORE_ID" \
  -H "Accept: application/vnd.api+json" \
  -H "Content-Type: application/vnd.api+json" \
  -H "Authorization: Bearer $LEMON_SQUEEZY_API_KEY"
```

**Response structure:**
```json
{
  "data": [
    {
      "type": "customers",
      "id": "123456",
      "attributes": {
        "store_id": 12345,
        "name": "John Doe",
        "email": "customer@example.com",
        "status": "active",
        "city": "Sydney",
        "region": "NSW",
        "country": "AU",
        "total_revenue_currency": 15,
        "mrr": 0,
        "status_formatted": "Active",
        "country_formatted": "Australia",
        "total_revenue_currency_formatted": "$15.00",
        "mrr_formatted": "$0.00",
        "created_at": "2026-01-01T12:00:00.000000Z",
        "updated_at": "2026-01-01T12:00:00.000000Z"
      }
    }
  ]
}
```

### Step 2: List Customer's Orders

**Endpoint:** `GET https://api.lemonsqueezy.com/v1/orders`

**Query parameters:**
- `filter[customer_id]` - Filter by customer ID from Step 1
- `filter[store_id]` - Your store ID
- `include=order-items` - Include product details

**Example request:**
```bash
curl "https://api.lemonsqueezy.com/v1/orders?filter[customer_id]=123456&filter[store_id]=YOUR_STORE_ID&include=order-items" \
  -H "Accept: application/vnd.api+json" \
  -H "Authorization: Bearer $LEMON_SQUEEZY_API_KEY"
```

**Response structure:**
```json
{
  "data": [
    {
      "type": "orders",
      "id": "1",
      "attributes": {
        "store_id": 12345,
        "customer_id": 123456,
        "identifier": "a1b2c3d4",
        "order_number": 12345,
        "user_name": "John Doe",
        "user_email": "customer@example.com",
        "currency": "AUD",
        "currency_rate": "1.00000000",
        "subtotal": 1500,
        "discount_total": 0,
        "tax": 0,
        "total": 1500,
        "subtotal_usd": 1000,
        "discount_total_usd": 0,
        "tax_usd": 0,
        "total_usd": 1000,
        "tax_name": "VAT",
        "tax_rate": "0.00",
        "status": "paid",
        "status_formatted": "Paid",
        "refunded": false,
        "refunded_at": null,
        "subtotal_formatted": "$15.00",
        "discount_total_formatted": "$0.00",
        "tax_formatted": "$0.00",
        "total_formatted": "$15.00",
        "first_order_item": {
          "id": 1,
          "order_id": 1,
          "product_id": 123,
          "variant_id": 456,
          "product_name": "This Wasn't in the Brochure",
          "variant_name": "Standard",
          "price": 1500
        },
        "created_at": "2026-01-01T12:00:00.000000Z",
        "updated_at": "2026-01-01T12:00:00.000000Z"
      }
    }
  ]
}
```

### Step 3: Check Subscriptions (if applicable)

**Endpoint:** `GET https://api.lemonsqueezy.com/v1/subscriptions`

**Query parameters:**
- `filter[customer_id]` - Customer ID
- `filter[store_id]` - Your store ID

### Step 4: Get License Keys (if product has licenses)

**Endpoint:** `GET https://api.lemonsqueezy.com/v1/license-keys`

**Query parameters:**
- `filter[order_id]` - Order ID from Step 2
- `filter[store_id]` - Your store ID

## Output Format

Present results in this structure:

```markdown
# Customer Lookup Results

## Customer Details
- Name: John Doe
- Email: customer@example.com
- Customer ID: 123456
- Status: Active
- Location: Sydney, NSW, Australia
- Total Spent: $15.00 AUD
- Customer Since: January 1, 2026

## Orders (1 total)

### Order #12345 - Paid ✅
- Date: January 1, 2026
- Amount: $15.00 AUD
- Status: Paid
- Product: This Wasn't in the Brochure (Standard)
- Order ID: a1b2c3d4
- Refunded: No

## Subscriptions
No active subscriptions

## License Keys
No license keys (product doesn't use licenses)

## Support Actions Available
- ✅ Grant manual access (if webhook failed)
- ✅ Issue refund
- ✅ Resend receipt email
- ✅ Update customer details
```

## Error Handling

**Customer not found:**
```markdown
❌ No customer found with email: customer@example.com

Possible reasons:
- Email typo (check spelling)
- Order placed with different email
- Order not yet processed
- Customer used different store

Ask customer to:
1. Check confirmation email for exact email used
2. Provide order number instead
3. Check spam folder for receipt
```

**Multiple customers (shouldn't happen with email filter):**
```markdown
⚠️ Multiple customers found. This shouldn't happen.

Please verify store_id filter is working correctly.
```

**API authentication error:**
```markdown
❌ API Error: Unauthorized

LEMON_SQUEEZY_API_KEY is invalid or expired.

Check: https://app.lemonsqueezy.com/settings/api
```

## Rate Limits

Lemon Squeezy API limits:
- 60 requests per minute per API key
- Includes all API calls across your account

If you hit rate limit (429 status):
- Wait 60 seconds
- Implement exponential backoff
- Cache results when possible

## Security Notes

**Never log or display:**
- Full API keys
- Customer payment details
- License keys in public channels

**Always verify:**
- Store ID matches YOUR_STORE_ID
- Request is for YOUR store (not cross-store lookup)

## Testing

Test with a known order:
```bash
# Your test order (replace with real values)
TEST_EMAIL="your-test@example.com"
TEST_ORDER="12345"
```

## Related Skills

- `/refund-order` - Issue refunds after lookup
- `/license-key-tool` - Manage licenses after finding customer
- `/sales-dashboard` - View all recent orders

## API Documentation

Full Lemon Squeezy API docs:
- Customers: https://docs.lemonsqueezy.com/api/customers
- Orders: https://docs.lemonsqueezy.com/api/orders
- Subscriptions: https://docs.lemonsqueezy.com/api/subscriptions
- License Keys: https://docs.lemonsqueezy.com/api/license-keys
