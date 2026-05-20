---
name: amazon-order-matcher
description: Scrape Amazon order history and match to Monarch Money transactions for auto-categorization. Uses browser automation to extract order details, then matches by amount and date to categorize uncategorized transactions.
---

# Amazon Order Matcher

Automatically categorize Amazon purchases in Monarch Money by matching against Amazon order history.

## How It Works

1. **Scrape Amazon Orders**: Browser automation (profile `openclaw`) extracts order history
2. **Match Transactions**: Matches by amount (exact match) with date tolerance (bank posts 1-3 days after order)
3. **Categorize**: Auto-assigns categories based on Amazon product descriptions
4. **Update Monarch**: Batch updates via Monarch CLI

## Quick Start

```bash
# Browser must be running with openclaw profile
browser action=start profile=openclaw

# Navigate to Amazon orders (login persisted in profile)
browser action=navigate targetUrl="https://www.amazon.com/your-orders/orders?timeFilter=year-2026"

# Extract orders via JavaScript evaluation (see scripts/extract_orders.js)
# Match to Monarch transactions (see scripts/match_and_categorize.py)
# Batch update (see scripts/batch_update.sh)
```

## Scripts

| Script | Purpose |
|--------|---------|
| `match_and_categorize.py` | Match Amazon orders to Monarch transactions, suggest categories |
| `batch_update.sh` | Apply category updates to Monarch |
| `quick_categorize.py` | Amount-based heuristics when order data unavailable |

## Category Mapping

| Product Type | Monarch Category | Category ID |
|--------------|------------------|-------------|
| Baby gates, locks, protectors | Baby formula | 225123032227674020 |
| Health supplements | Household | 162959461244237526 |
| Home appliances | Household | 162959461244237526 |
| Cables, tools, work equipment | Business expense | 178462006985127548 |
| Electronics, gadgets | Jeremy Spending Money | 162782301949818821 |
| Car accessories | Transportation | 162777981853398770 |
| Gifts | Gifts | 162777981853398756 |

## Data Files

- `data/amazon_orders_2026.json` - Scraped order data with dates, amounts, products
- Order data persists between sessions for re-matching

## Browser Session

Amazon login is persisted in the `openclaw` browser profile:
- No MFA needed on repeat visits
- Session survives browser restarts
- Target ID may change between sessions (get fresh via `browser action=tabs`)

## Cron Schedule

Weekly reconciliation runs Sunday 8pm ET:
- Scrapes new orders from Amazon
- Matches to uncategorized Monarch transactions
- Applies categories automatically
- Reports summary to Telegram

## Limitations

- Amount matching only (no order ID correlation with bank data)
- Multi-item orders may match incorrectly if total matches another order
- Refunds/returns need manual review
- Amazon Store Card transactions processed separately

## First-Time Setup

1. Start browser: `browser action=start profile=openclaw`
2. Navigate to Amazon and log in manually
3. Complete MFA verification
4. Login persists for future sessions
