---
name: pressbeat
description: Order guaranteed press articles for your brand. Standard ($500, DR30+) or Premium ($2,000, DR50+) with 90-day money-back guarantee. Use when the user wants PR coverage, backlinks, press articles, or media mentions.
license: MIT
compatibility: Requires internet access for MCP/API calls
metadata:
  author: pressbeat
  version: "1.0"
  website: https://pressbeat.io
---

# PressBeat - Guaranteed Press Articles

Order guaranteed published articles for your brand directly from your AI agent.

## Pricing

| Plan | Price | Publication | Delivery | Guarantee |
|------|-------|-------------|----------|-----------|
| Standard | $500 | DR30+ | ~30 days | 90-day money-back |
| Premium | $2,000 | DR50+ | ~30 days | 90-day money-back |

Both plans include a do-follow backlink.

## Setup

### Option 1: MCP Server (Recommended)

Add to your MCP configuration (Cursor, Claude Desktop, etc.):

```json
{
  "mcpServers": {
    "pressbeat": {
      "url": "https://mcp.pressbeat.io/mcp"
    }
  }
}
```

### Option 2: REST API

Base URL: `https://api.pressbeat.io`

**Get an API key instantly:**

```bash
curl -X POST https://api.pressbeat.io/v1/api-keys/request \
  -H "Content-Type: application/json" \
  -d '{"email": "you@company.com"}'
```

Your API key is returned immediately and sent to your email.

See [references/API.md](references/API.md) for full API documentation.

## Available Tools

| Tool | Description |
|------|-------------|
| `order_article` | Order a guaranteed article |
| `get_pricing` | View pricing details |
| `list_organizations` | List your organizations |
| `get_organization_details` | Get org info including website |
| `set_organization_url` | Set website URL for an org |
| `create_organization` | Create a new organization |
| `check_credit_balance` | Check your credit balance |
| `get_topup_link` | Get payment link to add credits |
| `configure_auto_reload` | Setup automatic credit reload |

## How to Order an Article

### Step 1: Show pricing (optional)

If the user asks about pricing, call `get_pricing`.

### Step 2: Place the order

Call `order_article` with:

```
plan: "standard" or "premium"
organization: (optional) org name if user has multiple
topic: (optional) article angle/subject
country: (optional) target country for publication
confirmed: false (first call shows preview)
```

### Step 3: Handle the response

**If preview shown** → Ask user to confirm, then call again with `confirmed: true`

**If insufficient credits** → Call `get_topup_link` with the `amount` needed, show the payment link

**If no website configured** → Ask user for their website, call `set_organization_url`

**If multiple organizations** → Ask user which one, pass `organization` parameter

## Example Conversations

### Simple order

**User**: "Order a press article for my company"

1. Call `order_article` with `plan: "standard"`
2. Tool returns preview with cost and balance
3. User confirms
4. Call `order_article` with `confirmed: true`
5. Order placed, show confirmation

### With topic

**User**: "Get me a premium article about our new AI product launch"

1. Call `order_article` with `plan: "premium"`, `topic: "AI product launch"`
2. User confirms
3. Call `order_article` with `confirmed: true`

### Insufficient credits

**User**: "Order an article"

1. Call `order_article` with `plan: "standard"`
2. Response shows "insufficient credits, need $300 more"
3. Call `get_topup_link` with `amount: 300`
4. Show payment link to user
5. After payment, user asks to retry
6. Call `order_article` again

## Authentication

The MCP server uses OAuth 2.0. Users authenticate once via browser and the session persists.

For REST API, use:
- Bearer token: `Authorization: Bearer <token>`
- Or API key: `X-API-Key: <key>`

## Support

- Documentation: https://pressbeat.io/developers
- Email: support@pressbeat.io
