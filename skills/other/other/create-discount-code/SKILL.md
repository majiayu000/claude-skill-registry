---
name: create-discount-code
description: Create discount codes for promotions, launches, beta readers, or giveaways. Supports percentage/fixed discounts, usage limits, expiry dates, and product restrictions. Triggers on "create discount", "promo code", "coupon", "launch code", or similar queries.
allowed-tools: Bash, Read
---

# Create Discount Code Skill

**Purpose:** Fast discount code creation for marketing and promotions

## What This Skill Does

Creates discount codes in Lemon Squeezy with:
1. Code name (e.g., LAUNCH50, BETA2026)
2. Discount type (percentage or fixed amount)
3. Discount amount (e.g., 50% off or $5 off)
4. Usage limits (total redemptions, per-customer limit)
5. Expiry date (optional)
6. Product restrictions (all products or specific ones)

## When to Use This Skill

**Common use cases:**
- Launch promotions: "Create LAUNCH50 for 50% off"
- Beta reader rewards: "Create BETA100 for 100% off, limit 20"
- Podcast appearances: "Create PODCAST30 for 30% off"
- Social media giveaways: "Create GIVEAWAY for free access"
- Seasonal sales: "Create HOLIDAY25 for 25% off"
- Affiliate codes: "Create PARTNER20 for 20% off"

## API Authentication

Uses `LEMON_SQUEEZY_API_KEY` and `LEMON_SQUEEZY_STORE_ID` environment variables.

## Usage Examples

**Example 1: Launch promotion**
```
User: Create a 50% off code called LAUNCH50, limit 100 uses, expires in 7 days
Assistant: [Uses create-discount-code skill]
```

**Example 2: Beta reader reward**
```
User: Create BETA2026 for 100% off, limit to 20 people
Assistant: [Creates free code with redemption limit]
```

**Example 3: Podcast appearance**
```
User: I'm on a podcast next week. Create a 30% discount code
Assistant: [Creates PODCAST30 code, suggests expiry date]
```

## Implementation

### Create Discount Code API

**Endpoint:** `POST https://api.lemonsqueezy.com/v1/discounts`

**Required fields:**
- `store_id` - Your store ID
- `name` - Internal name (e.g., "Launch 50% Off")
- `code` - The actual code users type (e.g., "LAUNCH50")
- `amount` - Discount amount (percentage: 1-100, or cents for fixed)
- `amount_type` - "percent" or "fixed"

**Optional fields:**
- `duration` - "once", "repeating", or "forever"
- `duration_in_months` - How many months (for repeating)
- `starts_at` - When code becomes active (ISO 8601)
- `expires_at` - When code expires (ISO 8601)
- `max_redemptions` - Total usage limit (null = unlimited)
- `limit_redemptions_per_customer` - Per-customer limit
- `is_limited_to_products` - true/false
- `product_ids` - Array of product IDs (if limited)

**Example request (50% off, 7 days, 100 uses):**
```bash
curl -X POST "https://api.lemonsqueezy.com/v1/discounts" \
  -H "Accept: application/vnd.api+json" \
  -H "Content-Type: application/vnd.api+json" \
  -H "Authorization: Bearer $LEMON_SQUEEZY_API_KEY" \
  -d '{
    "data": {
      "type": "discounts",
      "attributes": {
        "store_id": YOUR_STORE_ID,
        "name": "Launch Week Promotion",
        "code": "LAUNCH50",
        "amount": 50,
        "amount_type": "percent",
        "duration": "once",
        "max_redemptions": 100,
        "expires_at": "2026-01-12T23:59:59Z"
      }
    }
  }'
```

**Example request (100% off, beta readers):**
```bash
curl -X POST "https://api.lemonsqueezy.com/v1/discounts" \
  -H "Accept: application/vnd.api+json" \
  -H "Content-Type: application/vnd.api+json" \
  -H "Authorization: Bearer $LEMON_SQUEEZY_API_KEY" \
  -d '{
    "data": {
      "type": "discounts",
      "attributes": {
        "store_id": YOUR_STORE_ID,
        "name": "Beta Reader Reward",
        "code": "BETA2026",
        "amount": 100,
        "amount_type": "percent",
        "duration": "once",
        "max_redemptions": 20
      }
    }
  }'
```

**Example request ($5 off, fixed amount):**
```bash
curl -X POST "https://api.lemonsqueezy.com/v1/discounts" \
  -H "Accept: application/vnd.api+json" \
  -H "Content-Type: application/vnd.api+json" \
  -H "Authorization: Bearer $LEMON_SQUEEZY_API_KEY" \
  -d '{
    "data": {
      "type": "discounts",
      "attributes": {
        "store_id": YOUR_STORE_ID,
        "name": "Five Dollar Discount",
        "code": "SAVE5",
        "amount": 500,
        "amount_type": "fixed",
        "duration": "once"
      }
    }
  }'
```

**Response structure:**
```json
{
  "data": {
    "type": "discounts",
    "id": "12345",
    "attributes": {
      "store_id": 12345,
      "name": "Launch Week Promotion",
      "code": "LAUNCH50",
      "amount": 50,
      "amount_type": "percent",
      "status": "published",
      "status_formatted": "Published",
      "duration": "once",
      "duration_in_months": null,
      "is_limited_redemptions": true,
      "max_redemptions": 100,
      "redemptions_count": 0,
      "is_limited_to_products": false,
      "starts_at": null,
      "expires_at": "2026-01-12T23:59:59.000000Z",
      "test_mode": false,
      "created_at": "2026-01-05T10:00:00.000000Z",
      "updated_at": "2026-01-05T10:00:00.000000Z"
    }
  }
}
```

## Discount Code Templates

### Template 1: Launch Promotion
```json
{
  "name": "Launch Week - 50% Off",
  "code": "LAUNCH50",
  "amount": 50,
  "amount_type": "percent",
  "duration": "once",
  "max_redemptions": 100,
  "expires_at": "+7 days"
}
```

**Use case:** Product launch, podcast appearance, press coverage

### Template 2: Beta Reader / Reviewer
```json
{
  "name": "Beta Reader Reward",
  "code": "BETA100",
  "amount": 100,
  "amount_type": "percent",
  "duration": "once",
  "max_redemptions": 20,
  "expires_at": null
}
```

**Use case:** Beta readers, reviewers, influencers
**Cost:** $0 (100% discount codes are free)

### Template 3: Early Bird
```json
{
  "name": "Early Bird Special",
  "code": "EARLYBIRD",
  "amount": 30,
  "amount_type": "percent",
  "duration": "once",
  "max_redemptions": 500,
  "expires_at": "+30 days"
}
```

**Use case:** Pre-launch list, early supporters

### Template 4: Seasonal Sale
```json
{
  "name": "End of Financial Year Sale",
  "code": "EOFY25",
  "amount": 25,
  "amount_type": "percent",
  "duration": "once",
  "max_redemptions": null,
  "starts_at": "2026-06-01T00:00:00Z",
  "expires_at": "2026-06-30T23:59:59Z"
}
```

**Use case:** Holiday sales, seasonal promotions

### Template 5: Affiliate / Partner
```json
{
  "name": "Partner Discount",
  "code": "PARTNER20",
  "amount": 20,
  "amount_type": "percent",
  "duration": "once",
  "max_redemptions": null,
  "expires_at": null
}
```

**Use case:** Ongoing affiliate codes (track with unique codes per partner)

### Template 6: First-Time Customer
```json
{
  "name": "Welcome Discount",
  "code": "WELCOME10",
  "amount": 10,
  "amount_type": "percent",
  "duration": "once",
  "limit_redemptions_per_customer": 1
}
```

**Use case:** Email capture, welcome series

### Template 7: Fixed Amount Off
```json
{
  "name": "Five Dollar Discount",
  "code": "SAVE5",
  "amount": 500,
  "amount_type": "fixed",
  "duration": "once"
}
```

**Note:** Amount is in cents (500 = $5.00)

## Output Format

After creating a discount code, present results like this:

```markdown
# ✅ Discount Code Created

## Code Details

**Code:** `LAUNCH50`
**Type:** 50% off
**Status:** Active ✅

## Usage

**Share this with customers:**
> Use code **LAUNCH50** at checkout for 50% off!
> Valid until January 12, 2026
> Limited to first 100 customers

**Checkout URL with code:**
https://your-store.lemonsqueezy.com/checkout/buy/PRODUCT_ID?checkout[discount_code]=LAUNCH50

## Limits

- **Max uses:** 100
- **Uses so far:** 0
- **Expires:** January 12, 2026 at 11:59 PM
- **Per-customer limit:** Unlimited

## Tracking

View redemptions: https://app.lemonsqueezy.com/discounts/12345

## Update/Delete

- Edit code: Use Lemon Squeezy dashboard
- Delete code: `DELETE /v1/discounts/12345`
- Disable code: Change status to "draft"

---

## 🎯 Marketing Copy (Ready to Use)

**Social media:**
```
🎉 Launch Week Special! Get 50% off with code LAUNCH50
Limited to first 100 customers. Ends Jan 12.
[Your checkout link]
```

**Email:**
```
Subject: [Launch Week] 50% Off Inside 🚀

Hi there,

To celebrate our launch, I'm offering 50% off to the first 100 customers.

Use code LAUNCH50 at checkout.

This offer expires January 12, so don't miss out!

[CTA Button: Get 50% Off]
```

**Podcast/Video mention:**
```
"If you want to grab a copy, I've created a special code for listeners:
LAUNCH50 - that's L-A-U-N-C-H-5-0 for 50% off.
It's good for the first 100 people and expires next week."
```
```

## Date/Time Helpers

**Common expiry patterns:**

```bash
# 7 days from now
expires_at=$(date -u -d "+7 days" +"%Y-%m-%dT23:59:59Z")

# End of month
expires_at=$(date -u -d "$(date +%Y-%m-01) +1 month -1 day" +"%Y-%m-%dT23:59:59Z")

# Specific date
expires_at="2026-06-30T23:59:59Z"

# No expiry
expires_at=null
```

**Common start dates:**

```bash
# Start immediately
starts_at=null

# Start tomorrow
starts_at=$(date -u -d "+1 day" +"%Y-%m-%dT00:00:00Z")

# Start specific date
starts_at="2026-06-01T00:00:00Z"
```

## Validation Rules

**Code format:**
- 2-256 characters
- Letters, numbers, hyphens, underscores
- Case-insensitive (LAUNCH50 = launch50)
- No spaces

**Amount limits:**
- Percentage: 1-100
- Fixed: Any positive integer (in cents)

**Redemption limits:**
- `null` = unlimited
- Must be positive integer

**Product restrictions:**
```json
{
  "is_limited_to_products": true,
  "product_ids": [123, 456]
}
```

## Error Handling

**Code already exists:**
```markdown
❌ Error: Code "LAUNCH50" already exists

Existing code details:
- Created: January 1, 2026
- Uses: 45/100
- Status: Active

Options:
1. Choose different code (e.g., LAUNCH50B)
2. Delete old code and recreate
3. Edit existing code in dashboard
```

**Invalid amount:**
```markdown
❌ Error: Invalid discount amount

For percentage: Must be 1-100
For fixed: Must be positive integer in cents (e.g., 500 = $5)

You provided: 150% (invalid)
Did you mean: 50% off?
```

**Store ID missing:**
```markdown
❌ Error: LEMON_SQUEEZY_STORE_ID not configured

Set in Cloudflare:
npx wrangler pages secret put LEMON_SQUEEZY_STORE_ID
```

## Security Considerations

**Don't create codes that:**
- Give >90% off publicly (reserve 100% for targeted use)
- Have no expiry and no limit (cost control)
- Are too generic (CODE, DISCOUNT, SALE)

**Do:**
- Set reasonable limits (100-500 uses)
- Use expiry dates for time-bound promos
- Track usage regularly
- Use unique codes per channel (track which works)

## Bulk Creation

**Create multiple codes at once:**

```bash
# Example: Create 10 unique affiliate codes
for i in {1..10}; do
  curl -X POST "https://api.lemonsqueezy.com/v1/discounts" \
    -H "Authorization: Bearer $API_KEY" \
    -d '{
      "data": {
        "type": "discounts",
        "attributes": {
          "store_id": STORE_ID,
          "name": "Affiliate Code '$i'",
          "code": "AFFILIATE'$i'",
          "amount": 20,
          "amount_type": "percent"
        }
      }
    }'
done
```

## Analytics Integration

**Track code performance:**

1. Create unique codes per channel:
   - PODCAST30 (podcast)
   - TWITTER30 (Twitter)
   - EMAIL30 (email list)

2. Compare redemptions:
```markdown
Channel Performance (30% off codes):
- PODCAST30: 45 uses
- TWITTER30: 23 uses
- EMAIL30: 67 uses

Winner: Email (67 conversions)
```

## Related Skills

- `/sales-dashboard` - See discount usage in revenue reports
- `/customer-lookup` - Check if customer used discount
- List all discounts: `GET /v1/discounts?filter[store_id]=STORE_ID`

## API Documentation

Full Lemon Squeezy Discounts API:
- Create: https://docs.lemonsqueezy.com/api/discounts#create-a-discount
- Update: https://docs.lemonsqueezy.com/api/discounts#update-a-discount
- Delete: https://docs.lemonsqueezy.com/api/discounts#delete-a-discount
- List: https://docs.lemonsqueezy.com/api/discounts#list-all-discounts

## Testing

**Test discount codes:**

1. Create code in test mode:
```json
{
  "test_mode": true,
  "code": "TEST50",
  "amount": 50,
  "amount_type": "percent"
}
```

2. Use in checkout with test card:
   - Card: 4242 4242 4242 4242
   - Expiry: Any future date
   - CVC: Any 3 digits

3. Verify discount applied correctly

4. Check redemption count increased
