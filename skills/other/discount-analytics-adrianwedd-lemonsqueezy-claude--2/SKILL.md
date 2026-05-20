---
name: discount-analytics
description: Track promotional code performance and marketing attribution. Shows redemptions, revenue, conversion rates, and ROI by discount code. Identifies which marketing channels drive sales. Triggers on "discount analytics", "promo code performance", "which codes work", "marketing attribution", or similar queries.
allowed-tools: Bash, Read
---

# Discount Analytics Skill

**Purpose:** Marketing attribution and promo code ROI tracking

## What This Skill Does

Analyzes discount code performance through Lemon Squeezy API:
1. Fetch all discount codes
2. Calculate redemptions per code
3. Track revenue by code (gross vs. discounted)
4. Identify top-performing codes
5. Calculate conversion rates
6. ROI analysis by marketing channel
7. Identify underperforming codes

## When to Use This Skill

**Common use cases:**
- Post-launch review: "Which launch codes worked best?"
- Marketing attribution: "Did PODCAST30 drive more sales than EMAIL25?"
- ROI calculation: "Was LAUNCH50 worth the 50% discount?"
- Campaign planning: "What discount % gets best results?"
- Budget allocation: "Which channels should we invest more in?"
- Code cleanup: "Which codes are unused and can be deleted?"

## API Authentication

Uses `LEMON_SQUEEZY_API_KEY` environment variable (already set in Cloudflare).

## Usage Examples

**Example 1: All-time performance**
```
User: Show me discount code performance
Assistant: [Uses discount-analytics skill to fetch all codes and calculate metrics]
```

**Example 2: Specific code**
```
User: How many people used LAUNCH50?
Assistant: [Filters analytics for LAUNCH50 specifically]
```

**Example 3: Compare codes**
```
User: Which worked better: PODCAST30 or EMAIL30?
Assistant: [Compares redemptions, revenue, and conversion rates]
```

## Implementation

### Step 1: Fetch All Discount Codes

**Endpoint:** `GET https://api.lemonsqueezy.com/v1/discounts`

**Request:**
```bash
curl "https://api.lemonsqueezy.com/v1/discounts?filter[store_id]=YOUR_STORE_ID&page[size]=100" \
  -H "Accept: application/vnd.api+json" \
  -H "Authorization: Bearer $LEMON_SQUEEZY_API_KEY"
```

**Response structure:**
```json
{
  "data": [
    {
      "type": "discounts",
      "id": "1",
      "attributes": {
        "store_id": 264940,
        "name": "Launch Week - 50% Off",
        "code": "LAUNCH50",
        "amount": 50,
        "amount_type": "percent",
        "status": "published",
        "duration": "once",
        "max_redemptions": 100,
        "redemptions_count": 45,
        "is_limited_redemptions": true,
        "expires_at": "2026-01-12T23:59:59Z",
        "created_at": "2026-01-05T10:00:00Z"
      }
    },
    {
      "type": "discounts",
      "id": "2",
      "attributes": {
        "store_id": 264940,
        "name": "Podcast Appearance Code",
        "code": "PODCAST30",
        "amount": 30,
        "amount_type": "percent",
        "status": "published",
        "duration": "once",
        "max_redemptions": null,
        "redemptions_count": 23,
        "is_limited_redemptions": false,
        "expires_at": null,
        "created_at": "2026-01-07T10:00:00Z"
      }
    }
  ],
  "meta": {
    "page": {
      "currentPage": 1,
      "from": 1,
      "lastPage": 1,
      "perPage": 100,
      "to": 2,
      "total": 2
    }
  }
}
```

### Step 2: Fetch Orders with Discount Usage

**Endpoint:** `GET https://api.lemonsqueezy.com/v1/orders`

**Request:**
```bash
curl "https://api.lemonsqueezy.com/v1/orders?filter[store_id]=YOUR_STORE_ID&page[size]=100" \
  -H "Accept: application/vnd.api+json" \
  -H "Authorization: Bearer $LEMON_SQUEEZY_API_KEY"
```

**Filter orders that used discounts:**
```javascript
orders.filter(order => order.attributes.discount_total > 0)
```

**Extract discount code from order:**
```javascript
order.attributes.first_order_item.discount_code // "LAUNCH50"
```

### Step 3: Calculate Metrics

**Per-code metrics:**
```javascript
// For each discount code
const metrics = {
  code: "LAUNCH50",
  redemptions: 45,
  redemption_rate: "45%", // 45/100 max redemptions
  total_revenue: 337.50, // Sum of all orders with this code (after discount)
  gross_revenue: 675.00, // What revenue would have been without discount
  discount_amount: 337.50, // Total discount given
  average_order: 7.50, // total_revenue / redemptions
  status: "Active" | "Expired" | "Maxed Out",
  expires: "2026-01-12",
  created: "2026-01-05"
};
```

**Overall metrics:**
```javascript
const summary = {
  total_codes: 5,
  active_codes: 3,
  total_redemptions: 112,
  total_revenue_with_discounts: 892.00,
  total_discount_given: 445.00,
  average_discount_percent: 35,
  most_popular_code: "LAUNCH50"
};
```

### Step 4: Rank by Performance

**Sort by redemptions (popularity):**
```javascript
codes.sort((a, b) => b.redemptions_count - a.redemptions_count);
```

**Sort by revenue (value):**
```javascript
codes.sort((a, b) => b.total_revenue - a.total_revenue);
```

**Sort by conversion rate (efficiency):**
```javascript
codes.sort((a, b) => b.redemption_rate - a.redemption_rate);
```

## Output Format

```markdown
# 📊 Discount Code Analytics

**Report Generated:** January 6, 2026 at 10:00 AM AEDT
**Reporting Period:** All Time

---

## 💰 Summary

| Metric | Value |
|--------|-------|
| **Total Codes** | 5 active |
| **Total Redemptions** | 112 |
| **Revenue (with discounts)** | $892.00 AUD |
| **Revenue (without discounts)** | $1,337.00 AUD |
| **Total Discount Given** | $445.00 AUD |
| **Average Discount** | 33.3% |

---

## 🏆 Top Performing Codes

### 1. LAUNCH50 - Launch Week Promotion
- **Redemptions:** 45 / 100 (45% utilization)
- **Revenue Generated:** $337.50 AUD (after 50% discount)
- **Gross Revenue Impact:** $675.00 AUD
- **Discount Given:** $337.50 AUD
- **Average Order:** $7.50 AUD
- **Status:** ✅ Active (expires Jan 12)
- **ROI:** Strong - Drove 40% of all sales

### 2. PODCAST30 - Podcast Appearance
- **Redemptions:** 23 (unlimited)
- **Revenue Generated:** $241.50 AUD (after 30% discount)
- **Gross Revenue Impact:** $345.00 AUD
- **Discount Given:** $103.50 AUD
- **Average Order:** $10.50 AUD
- **Status:** ✅ Active (no expiry)
- **ROI:** Excellent - Best revenue per redemption

### 3. EMAIL25 - Email List
- **Redemptions:** 18 (unlimited)
- **Revenue Generated:** $202.50 AUD (after 25% discount)
- **Gross Revenue Impact:** $270.00 AUD
- **Discount Given:** $67.50 AUD
- **Average Order:** $11.25 AUD
- **Status:** ✅ Active (no expiry)
- **ROI:** Good - Consistent performance

### 4. BETA100 - Beta Readers
- **Redemptions:** 20 / 20 (100% utilization - MAXED OUT)
- **Revenue Generated:** $0.00 AUD (100% discount)
- **Gross Revenue Impact:** $300.00 AUD (value delivered)
- **Discount Given:** $300.00 AUD
- **Average Order:** $0.00 AUD
- **Status:** 🔴 Maxed Out
- **ROI:** N/A - Goodwill/marketing investment

### 5. MUSEPANTS - Special Giveaway
- **Redemptions:** 2 / 2 (100% utilization - MAXED OUT)
- **Revenue Generated:** $0.00 AUD (100% discount)
- **Gross Revenue Impact:** $30.00 AUD
- **Discount Given:** $30.00 AUD
- **Average Order:** $0.00 AUD
- **Status:** 🔴 Maxed Out (expires Jan 31)
- **ROI:** N/A - Special reward

### 6. FRIEND15 - Referral Program
- **Redemptions:** 4 (unlimited)
- **Revenue Generated:** $51.00 AUD (after 15% discount)
- **Gross Revenue Impact:** $60.00 AUD
- **Discount Given:** $9.00 AUD
- **Average Order:** $12.75 AUD
- **Status:** ✅ Active (no expiry)
- **ROI:** Low volume, high margin

---

## 📈 Performance Insights

### Best for Volume (Most Redemptions)
1. LAUNCH50 - 45 redemptions
2. PODCAST30 - 23 redemptions
3. BETA100 - 20 redemptions

### Best for Revenue (Highest Total Revenue)
1. LAUNCH50 - $337.50 AUD
2. PODCAST30 - $241.50 AUD
3. EMAIL25 - $202.50 AUD

### Best for Margin (Least Discount Given)
1. FRIEND15 - 15% average discount
2. EMAIL25 - 25% average discount
3. PODCAST30 - 30% average discount

### Highest Average Order Value
1. FRIEND15 - $12.75 per order
2. EMAIL25 - $11.25 per order
3. PODCAST30 - $10.50 per order

---

## 🎯 Marketing Attribution

**Channel Performance:**

| Channel | Code | Redemptions | Revenue | Avg Discount | ROI Grade |
|---------|------|-------------|---------|--------------|-----------|
| Launch Event | LAUNCH50 | 45 | $337.50 | 50% | A+ |
| Podcast | PODCAST30 | 23 | $241.50 | 30% | A |
| Email List | EMAIL25 | 18 | $202.50 | 25% | B+ |
| Referrals | FRIEND15 | 4 | $51.00 | 15% | C |

**Insights:**
- **Launch event** drove 40% of all sales (highest volume)
- **Podcast appearance** had best revenue per redemption ($10.50 avg)
- **Email list** most sustainable (lower discount, steady redemptions)
- **Referral program** low volume (needs promotion)

---

## 💡 Recommendations

### High Priority
1. **LAUNCH50 expiring soon** (Jan 12) - Consider extending or creating LAUNCH25 successor
2. **PODCAST30 performing well** - Book more podcast appearances
3. **BETA100 maxed out** - Create BETA2026 for new batch if needed

### Medium Priority
4. **EMAIL25 steady performer** - Promote more to email list
5. **FRIEND15 underutilized** - Promote referral program more actively

### Low Priority
6. **MUSEPANTS completed** - Archive (2/2 redemptions used)

---

## 🔍 Detailed Code Status

**Active Codes:** 4
- LAUNCH50 (expires Jan 12)
- PODCAST30 (no expiry)
- EMAIL25 (no expiry)
- FRIEND15 (no expiry)

**Maxed Out Codes:** 2
- BETA100 (20/20 used)
- MUSEPANTS (2/2 used)

**Expired Codes:** 0

---

## 📊 Time Series Analysis

**Redemptions Over Time:**

| Date Range | LAUNCH50 | PODCAST30 | EMAIL25 | Total |
|------------|----------|-----------|---------|-------|
| Jan 5-7 | 25 | 0 | 5 | 30 |
| Jan 8-10 | 15 | 12 | 8 | 35 |
| Jan 11-13 | 5 | 11 | 5 | 21 |

**Insights:**
- LAUNCH50 peaked early (launch day excitement)
- PODCAST30 steady post-launch (evergreen content)
- EMAIL25 consistent (recurring campaigns)

---

## 🎨 Campaign Planning

**What worked:**
- ✅ 50% discount drove high volume (45 redemptions)
- ✅ 30% discount had best revenue per redemption
- ✅ Podcast codes convert well (23 redemptions)
- ✅ Time-limited codes create urgency

**What didn't work:**
- ❌ Referral program underutilized (only 4 redemptions)
- ⚠️ 100% discount codes are generous but zero revenue

**Optimize next launch:**
1. Create tiered launch codes:
   - EARLYBIRD40 (first 50 customers)
   - LAUNCH30 (next 100 customers)
   - LAUNCH20 (extended run)
2. More podcast appearances (proven channel)
3. Promote referral program actively
4. Test lower discounts (20-25%) to improve margins

---

## 📉 Underperforming Codes

**Codes with <5 redemptions:**
- FRIEND15: 4 redemptions (needs promotion)

**Action items:**
1. Email existing customers about referral program
2. Add referral CTA to order confirmation
3. Create social media posts promoting FRIEND15
4. Consider increasing incentive (15% → 20%)
```

## Error Handling

**No discount codes found:**
```markdown
📭 No Discount Codes Found

**Possible reasons:**
- No codes created yet
- All codes expired/deleted
- API key lacks discount read permissions

**Next steps:**
1. Create first discount code: `/create-discount-code`
2. Verify API key has "Read discounts" permission
3. Check Lemon Squeezy dashboard: https://app.lemonsqueezy.com/discounts
```

**API Error:**
```markdown
❌ Cannot Fetch Discount Analytics

**API Error:** [Error message]

**Common causes:**
- API key lacks discount read permissions
- Network timeout
- Lemon Squeezy service issue

**Solutions:**
1. Verify API key has "Read discounts" scope
2. Retry in 1 minute
3. Check Lemon Squeezy status: https://status.lemonsqueezy.com
```

## Advanced Analytics

### Revenue Attribution Model

**Full attribution:**
```javascript
// Order used LAUNCH50 (50% off $15 = $7.50 paid)
{
  gross_revenue: 15.00, // What order would have been
  discount_amount: 7.50, // Amount discounted
  actual_revenue: 7.50, // What you received
  attribution: "LAUNCH50", // Marketing channel
  profit_margin: "50%", // Actual revenue / gross revenue
}
```

**Lifetime Value (LTV) tracking:**
```javascript
// Customer acquired via LAUNCH50, then purchased again at full price
{
  acquisition_code: "LAUNCH50",
  first_order: 7.50,
  repeat_orders: 15.00,
  total_ltv: 22.50,
  acquisition_cost: 7.50, // Discount given
  ltv_to_cac_ratio: 3.0, // Excellent (3:1)
}
```

### Cohort Analysis

**By acquisition channel:**
```markdown
| Code | Customers | Repeat Rate | Avg LTV | Best Channel? |
|------|-----------|-------------|---------|---------------|
| LAUNCH50 | 45 | 8% | $8.10 | No (low repeat) |
| EMAIL25 | 18 | 22% | $13.75 | Yes (high repeat) |
| PODCAST30 | 23 | 17% | $12.30 | Good |

**Insight:** EMAIL25 customers more loyal (lower discount → higher perceived value)
```

### A/B Test Results

**Test: 30% vs 50% discount**
```markdown
| Metric | 30% Discount | 50% Discount | Winner |
|--------|--------------|--------------|--------|
| Redemptions | 23 | 45 | 50% |
| Revenue | $241.50 | $337.50 | 50% |
| Margin | 70% | 50% | 30% |
| Avg Order | $10.50 | $7.50 | 30% |

**Conclusion:** 50% drives more volume, 30% drives better margins
**Recommendation:** Use 50% for launch, 30% for ongoing
```

## Automation Opportunities

**Auto-alerts:**
- Code reaching 80% of max redemptions → "LAUNCH50 almost full!"
- Code expiring in 48 hours → "LAUNCH50 expires soon, extend?"
- Code with 0 redemptions after 7 days → "PODCAST30 unused, promote?"
- High-performing code → "EMAIL25 converting well, increase budget?"

**Auto-optimization:**
- If code >90% redeemed → Auto-create successor code
- If code <5% redeemed after 1 week → Auto-suggest discount increase
- If code driving high repeat purchases → Auto-suggest similar codes

## Related Skills

- `/create-discount-code` - Create new codes based on analytics
- `/sales-dashboard` - Overall revenue metrics
- `/customer-lookup` - See which codes specific customers used

## API Documentation

**Lemon Squeezy Discounts API:**
- List discounts: https://docs.lemonsqueezy.com/api/discounts#list-all-discounts
- Get discount: https://docs.lemonsqueezy.com/api/discounts#retrieve-a-discount
- Discount usage: Calculated from orders API

## Export Options

**CSV export:**
```csv
Code,Redemptions,Max Redemptions,Revenue,Discount Given,Status,Expires
LAUNCH50,45,100,$337.50,$337.50,Active,2026-01-12
PODCAST30,23,,-,$241.50,$103.50,Active,-
EMAIL25,18,,-,$202.50,$67.50,Active,-
```

**JSON export:**
```json
{
  "generated_at": "2026-01-06T10:00:00Z",
  "summary": {
    "total_codes": 5,
    "total_redemptions": 112,
    "total_revenue": 892.00
  },
  "codes": [
    {
      "code": "LAUNCH50",
      "redemptions": 45,
      "revenue": 337.50,
      "status": "active"
    }
  ]
}
```

## Performance Benchmarks

**Industry standards (digital products):**
- Redemption rate: 3-8% (percentage of visitors who use code)
- Average discount: 20-30%
- Launch codes: 40-50% typical
- Ongoing codes: 15-25% typical
- 100% codes: Use sparingly (goodwill only)

**Your performance:**
- LAUNCH50: 45% redemption rate (excellent)
- PODCAST30: 30% discount, 23 redemptions (strong)
- EMAIL25: 25% discount, 18 redemptions (good)

**Recommendations:**
- You're in the optimal range
- LAUNCH50 drove urgency effectively
- 30% sweet spot for ongoing codes
- Consider testing 20% for higher margins
