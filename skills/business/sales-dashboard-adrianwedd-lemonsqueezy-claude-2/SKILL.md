---
name: sales-dashboard
description: Quick revenue overview and sales metrics. Shows today/week/month sales, recent orders, top products, and revenue trends. Use for daily business checks, launch tracking, or financial reporting. Triggers on "sales", "revenue", "how many orders", "dashboard", "sales report", or similar queries.
allowed-tools: Bash, Read
---

# Sales Dashboard Skill

**Purpose:** Fast revenue and sales metrics overview

## What This Skill Does

Fetches and displays key business metrics from Lemon Squeezy:
1. Revenue summary (today, 7 days, 30 days, all-time)
2. Order counts by status (paid, refunded, pending)
3. Recent orders (last 10)
4. Top-selling products/variants
5. Geographic breakdown (top countries)
6. Refund rate

## When to Use This Skill

**Common use cases:**
- Daily morning check: "How's the book doing?"
- Launch day tracking: "How many sales today?"
- Weekly review: "What's our revenue this week?"
- Product comparison: "Which edition sells best?"
- Financial planning: "Total revenue this month?"

## API Authentication

Uses `LEMON_SQUEEZY_API_KEY` environment variable.

## Usage Examples

**Example 1: Morning check**
```
User: How are sales today?
Assistant: [Uses sales-dashboard skill to show today's metrics]
```

**Example 2: Weekly review**
```
User: Give me a sales summary for the past week
Assistant: [Uses sales-dashboard with 7-day filter]
```

**Example 3: Product performance**
```
User: Which book edition is selling best?
Assistant: [Uses sales-dashboard to compare products]
```

## Implementation

### Step 1: Fetch Recent Orders

**Endpoint:** `GET https://api.lemonsqueezy.com/v1/orders`

**Query parameters:**
- `filter[store_id]` - Your store ID (required)
- `page[size]` - Number of orders (max 100)
- `sort` - Sort by created_at (newest first)
- `include` - Include order-items for product details

**Example request:**
```bash
curl "https://api.lemonsqueezy.com/v1/orders?filter[store_id]=YOUR_STORE_ID&page[size]=100&sort=-created_at&include=order-items" \
  -H "Accept: application/vnd.api+json" \
  -H "Authorization: Bearer $LEMON_SQUEEZY_API_KEY"
```

**Response:** Same as customer-lookup orders, but returns up to 100 most recent

### Step 2: Calculate Metrics

Process the orders data to calculate:

**Revenue by timeframe:**
```javascript
// Filter orders by created_at timestamp
const now = new Date();
const today = orders.filter(o => isToday(o.created_at) && o.status === 'paid');
const last7Days = orders.filter(o => isWithinDays(o.created_at, 7) && o.status === 'paid');
const last30Days = orders.filter(o => isWithinDays(o.created_at, 30) && o.status === 'paid');

// Sum totals (amounts are in cents)
const todayRevenue = today.reduce((sum, o) => sum + o.total, 0) / 100;
const weekRevenue = last7Days.reduce((sum, o) => sum + o.total, 0) / 100;
const monthRevenue = last30Days.reduce((sum, o) => sum + o.total, 0) / 100;
```

**Order counts:**
```javascript
const paidOrders = orders.filter(o => o.status === 'paid').length;
const refundedOrders = orders.filter(o => o.refunded === true).length;
const pendingOrders = orders.filter(o => o.status === 'pending').length;
```

**Top products:**
```javascript
// Group by product_name from first_order_item
const productCounts = {};
orders.forEach(order => {
  const product = order.first_order_item?.product_name || 'Unknown';
  productCounts[product] = (productCounts[product] || 0) + 1;
});

// Sort by count descending
const topProducts = Object.entries(productCounts)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 5);
```

**Geographic breakdown:**
```javascript
// Group by country
const countryCounts = {};
orders.forEach(order => {
  const country = order.country_formatted || order.country || 'Unknown';
  countryCounts[country] = (countryCounts[country] || 0) + 1;
});

// Sort by count
const topCountries = Object.entries(countryCounts)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 5);
```

**Refund rate:**
```javascript
const refundRate = paidOrders > 0
  ? ((refundedOrders / paidOrders) * 100).toFixed(1)
  : 0;
```

## Output Format

Present results in this dashboard structure:

```markdown
# 📊 Sales Dashboard

**Report Generated:** January 5, 2026 at 9:00 AM AEDT

---

## 💰 Revenue Summary

| Timeframe | Revenue | Orders | Avg Order |
|-----------|---------|--------|-----------|
| **Today** | $45.00 AUD | 3 | $15.00 |
| **Last 7 Days** | $180.00 AUD | 12 | $15.00 |
| **Last 30 Days** | $750.00 AUD | 50 | $15.00 |
| **All Time** | $1,234.00 AUD | 82 | $15.05 |

---

## 📈 Order Status Breakdown

- ✅ Paid: 82 orders
- 🔄 Pending: 0 orders
- 💸 Refunded: 1 order (1.2% refund rate)

---

## 🏆 Top Products (Last 30 Days)

1. **This Wasn't in the Brochure** - 48 sales ($720.00)
   - Standard tier: 30 sales
   - Supporter tier: 12 sales
   - Struggling tier: 6 sales
2. **Quick Maps PDF** - 234 downloads (free)

---

## 🌏 Top Countries (All Time)

1. 🇦🇺 Australia - 48 orders (58.5%)
2. 🇺🇸 United States - 18 orders (22.0%)
3. 🇬🇧 United Kingdom - 8 orders (9.8%)
4. 🇳🇿 New Zealand - 5 orders (6.1%)
5. 🇨🇦 Canada - 3 orders (3.6%)

---

## 🕐 Recent Orders (Last 10)

1. Order #12350 - $15.00 AUD - John D. (Sydney, AU) - 2 hours ago ✅
2. Order #12349 - $30.00 AUD - Sarah M. (Melbourne, AU) - 4 hours ago ✅
3. Order #12348 - $5.00 AUD - Mike T. (Perth, AU) - 6 hours ago ✅
4. Order #12347 - $15.00 AUD - Emma W. (Auckland, NZ) - 8 hours ago ✅
5. Order #12346 - $15.00 AUD - Alex P. (London, GB) - 10 hours ago ✅
6. Order #12345 - $30.00 AUD - Chris K. (Sydney, AU) - 12 hours ago ✅
7. Order #12344 - $15.00 AUD - Pat L. (Brisbane, AU) - 14 hours ago ✅
8. Order #12343 - $5.00 AUD - Jordan F. (Adelaide, AU) - 16 hours ago ✅
9. Order #12342 - $15.00 AUD - Taylor R. (Canberra, AU) - 18 hours ago ✅
10. Order #12341 - $30.00 AUD - Morgan S. (Hobart, AU) - 20 hours ago ✅

---

## 📊 Insights

- **Best day:** January 3 (8 orders, $120.00)
- **Average daily revenue (30d):** $25.00 AUD
- **Conversion rate (Quick Maps → Book):** ~20.5% (48/234)
- **Most popular tier:** Standard ($15) - 62.5% of paid orders
- **Peak hours:** 9am-11am and 7pm-9pm AEDT

---

## 🎯 Quick Actions

- [Create discount code](/create-discount-code) for launch promotion
- [Lookup customer](/customer-lookup) for support
- View full analytics: https://app.lemonsqueezy.com/dashboard
```

## Date/Time Filtering

**Calculate date ranges:**

```bash
# Today (ISO 8601 format)
TODAY_START=$(date -u +"%Y-%m-%dT00:00:00Z")

# 7 days ago
WEEK_START=$(date -u -d "7 days ago" +"%Y-%m-%dT00:00:00Z")

# 30 days ago
MONTH_START=$(date -u -d "30 days ago" +"%Y-%m-%dT00:00:00Z")

# Filter orders (do this client-side after fetching)
# Lemon Squeezy doesn't support date filtering in API yet
```

**Note:** Lemon Squeezy API doesn't have native date filters, so:
1. Fetch last 100-200 orders (adjust `page[size]`)
2. Filter by `created_at` timestamp client-side
3. For historical data, increase page size or paginate

## Performance Optimization

**Caching:**
- Cache results for 5-10 minutes (sales don't change instantly)
- Store in local file: `.cache/sales-dashboard-{timestamp}.json`
- Invalidate cache on manual refresh

**Pagination:**
```bash
# For stores with >100 orders, paginate:
curl "https://api.lemonsqueezy.com/v1/orders?filter[store_id]=STORE_ID&page[number]=1&page[size]=100" \
  -H "Authorization: Bearer $API_KEY"

# Response includes pagination links:
# "links": {
#   "first": "...",
#   "last": "...",
#   "next": "..."
# }
```

## Error Handling

**API rate limit (429):**
```markdown
⚠️ Rate limit exceeded. Please wait 60 seconds.

Lemon Squeezy allows 60 requests/minute.
```

**No orders found:**
```markdown
📭 No orders yet!

This is normal if:
- Store just launched
- Checkout not configured
- Testing in sandbox mode

Check: https://app.lemonsqueezy.com/orders
```

**Authentication error:**
```markdown
❌ Cannot access Lemon Squeezy API

Error: Unauthorized (401)

Verify LEMON_SQUEEZY_API_KEY is set correctly.
```

## Advanced Metrics

**For stores with subscriptions:**

```bash
# Fetch subscriptions
curl "https://api.lemonsqueezy.com/v1/subscriptions?filter[store_id]=STORE_ID" \
  -H "Authorization: Bearer $API_KEY"

# Calculate MRR (Monthly Recurring Revenue)
active_subscriptions = subscriptions.filter(s => s.status === 'active')
mrr = active_subscriptions.reduce((sum, s) => sum + s.mrr, 0) / 100
```

**For products with variants:**

```bash
# Group by variant_name
variant_sales = {}
orders.forEach(order => {
  const variant = order.first_order_item?.variant_name || 'Default'
  variant_sales[variant] = (variant_sales[variant] || 0) + 1
})
```

## Comparison Mode

**Compare timeframes:**
```markdown
## 📈 Week-over-Week Comparison

| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| Revenue | $180.00 | $150.00 | +20.0% 📈 |
| Orders | 12 | 10 | +20.0% 📈 |
| Avg Order | $15.00 | $15.00 | 0% → |
| Refunds | 0 | 1 | -100% 📉 |
```

## Export Options

**CSV export:**
```csv
Date,Orders,Revenue,Currency,Refunds
2026-01-05,3,45.00,AUD,0
2026-01-04,2,30.00,AUD,0
2026-01-03,8,120.00,AUD,0
```

**JSON export:**
```json
{
  "generated_at": "2026-01-05T09:00:00Z",
  "timeframe": "last_30_days",
  "summary": {
    "revenue": 750.00,
    "orders": 50,
    "refunds": 1
  }
}
```

## Testing

**Test with sample data:**
```bash
# Create test order in Lemon Squeezy dashboard
# Set mode to "Test" to avoid real charges
# Orders appear immediately in API
```

## Related Skills

- `/customer-lookup` - Deep dive into specific orders
- `/create-discount-code` - Create promotions based on performance
- `/revenue-report` - Generate monthly financial reports

## API Documentation

- Orders API: https://docs.lemonsqueezy.com/api/orders
- Store API: https://docs.lemonsqueezy.com/api/stores
- Subscriptions API: https://docs.lemonsqueezy.com/api/subscriptions
