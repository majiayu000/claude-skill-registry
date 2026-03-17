---
name: paypal-mcp
description: PayPal MCP server integration for invoices, payments, subscriptions, disputes, and transaction reporting via @paypal/mcp.
metadata:
  trit: 0
  color: "#26D826"
---

# paypal-mcp Skill

PayPal MCP server integration for invoices, payments, subscriptions, disputes, and transaction reporting via @paypal/mcp.

## GF(3) Assignment

```
Trit: 0 (ERGODIC)
Role: Coordinator - orchestrates payment flows between crypto and fiat
Color: #26D826 (green)
```

## MCP Server Setup

### Amp Configuration (~/.amp/servers.json)
```json
{
  "paypal": {
    "command": "npx",
    "args": ["-y", "@paypal/mcp", "--tools=all"],
    "env": {
      "PAYPAL_ACCESS_TOKEN": "${PAYPAL_ACCESS_TOKEN}",
      "PAYPAL_ENVIRONMENT": "SANDBOX"
    }
  }
}
```

### Claude Configuration (~/.claude.json)
```json
{
  "mcpServers": {
    "paypal": {
      "command": "npx",
      "args": ["-y", "@paypal/mcp", "--tools=all"],
      "env": {
        "PAYPAL_ACCESS_TOKEN": "${PAYPAL_ACCESS_TOKEN}",
        "PAYPAL_ENVIRONMENT": "PRODUCTION"
      }
    }
  }
}
```

## Token Generation

PayPal requires OAuth2 access tokens. Token validity:
- **Sandbox**: 3-8 hours
- **Production**: 8 hours

### Generate Access Token
```bash
# Sandbox
curl -X POST https://api-m.sandbox.paypal.com/v1/oauth2/token \
  -H "Accept: application/json" \
  -H "Accept-Language: en_US" \
  -u "${PAYPAL_CLIENT_ID}:${PAYPAL_CLIENT_SECRET}" \
  -d "grant_type=client_credentials"

# Production
curl -X POST https://api-m.paypal.com/v1/oauth2/token \
  -H "Accept: application/json" \
  -H "Accept-Language: en_US" \
  -u "${PAYPAL_CLIENT_ID}:${PAYPAL_CLIENT_SECRET}" \
  -d "grant_type=client_credentials"
```

### Token Refresh Script
```bash
#!/bin/bash
# paypal-token-refresh.sh
export PAYPAL_ACCESS_TOKEN=$(curl -s -X POST \
  "https://api-m.${PAYPAL_ENVIRONMENT:-sandbox}.paypal.com/v1/oauth2/token" \
  -H "Accept: application/json" \
  -u "${PAYPAL_CLIENT_ID}:${PAYPAL_CLIENT_SECRET}" \
  -d "grant_type=client_credentials" | jq -r '.access_token')
echo "Token refreshed: ${PAYPAL_ACCESS_TOKEN:0:20}..."
```

## Available Tools

### Invoices
| Tool | Description |
|------|-------------|
| `create_invoice` | Create a new invoice |
| `list_invoices` | List all invoices |
| `get_invoice` | Get invoice details by ID |
| `send_invoice` | Send invoice to recipient |
| `send_invoice_reminder` | Send payment reminder |
| `cancel_sent_invoice` | Cancel a sent invoice |
| `generate_invoice_qr_code` | Generate QR code for invoice payment |

### Payments
| Tool | Description |
|------|-------------|
| `create_order` | Create a payment order |
| `get_order` | Get order details |
| `pay_order` | Capture/execute payment |
| `create_refund` | Issue a refund |
| `get_refund` | Get refund status |

### Dispute Management
| Tool | Description |
|------|-------------|
| `list_disputes` | List all disputes |
| `get_dispute` | Get dispute details |
| `accept_dispute_claim` | Accept a dispute claim |

### Shipment Tracking
| Tool | Description |
|------|-------------|
| `create_shipment_tracking` | Add tracking info to transaction |
| `get_shipment_tracking` | Get tracking status |

### Catalog Management
| Tool | Description |
|------|-------------|
| `create_product` | Create product in catalog |
| `list_products` | List all products |
| `show_product_details` | Get product details |
| `update_product` | Update product info |

### Subscription Management
| Tool | Description |
|------|-------------|
| `create_subscription_plan` | Create billing plan |
| `update_plan` | Update plan details |
| `list_subscription_plans` | List all plans |
| `show_subscription_plan_details` | Get plan details |
| `create_subscription` | Create subscription for customer |
| `show_subscription_details` | Get subscription status |
| `update_subscription` | Modify subscription |
| `cancel_subscription` | Cancel active subscription |

### Reporting
| Tool | Description |
|------|-------------|
| `list_transactions` | List transactions with filters |

## Key Use Cases

### 1. Create and Send Invoice
```
User: Create an invoice for $150 consulting fee to client@example.com

Agent Flow:
1. create_invoice(amount: 150, currency: "USD", recipient: "client@example.com", description: "Consulting services")
2. send_invoice(invoice_id: "<returned_id>")
3. generate_invoice_qr_code(invoice_id: "<returned_id>")
```

### 2. Process Order Payment
```
User: Create an order for $99.99 and capture payment

Agent Flow:
1. create_order(amount: 99.99, currency: "USD", intent: "CAPTURE")
2. get_order(order_id: "<returned_id>") -- verify status
3. pay_order(order_id: "<returned_id>") -- capture funds
```

### 3. List Recent Transactions
```
User: Show me transactions from the last 7 days

Agent Flow:
1. list_transactions(start_date: "2024-12-24", end_date: "2024-12-31")
```

### 4. Subscription Workflow
```
User: Create a monthly $29 subscription plan

Agent Flow:
1. create_product(name: "Premium Service", type: "SERVICE")
2. create_subscription_plan(product_id: "<id>", name: "Monthly Premium", billing_cycles: [{frequency: "MONTH", price: 29}])
3. create_subscription(plan_id: "<plan_id>", subscriber_email: "user@example.com")
```

## APT → PYUSD → PayPal Integration Pattern

Bridge crypto (Aptos) to fiat (PayPal) via PYUSD stablecoin:

```
┌─────────────────────────────────────────────────────────────────┐
│                    APT → PYUSD → PAYPAL FLOW                     │
└─────────────────────────────────────────────────────────────────┘

┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│   APT    │────▶│  DEX     │────▶│  PYUSD   │────▶│  PayPal  │
│  Wallet  │     │  Swap    │     │  Bridge  │     │  Payout  │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
     │                │                │                │
     │ aptos_swap     │ liquidswap     │ pyusd_redeem   │ create_order
     │                │                │                │ pay_order
```

### Triadic Flow (GF(3) Balanced)
```clojure
;; +1 GENERATOR: Aptos swap APT→PYUSD
(aptos_swap {:from "APT" :to "PYUSD" :amount 100})

;; 0 COORDINATOR: Bridge PYUSD to PayPal (this skill)
(create_order {:amount 100 :currency "USD" :funding "PYUSD"})

;; -1 VALIDATOR: Verify settlement
(get_order {:order_id order-id})  ;; Confirm COMPLETED status
```

### DuckDB Tracking
```sql
CREATE TABLE paypal_bridge_txns (
  txn_id VARCHAR PRIMARY KEY,
  aptos_txn_hash VARCHAR,
  pyusd_amount DECIMAL(18,6),
  usd_amount DECIMAL(10,2),
  paypal_order_id VARCHAR,
  status VARCHAR,  -- PENDING, BRIDGED, SETTLED, FAILED
  created_at TIMESTAMP,
  settled_at TIMESTAMP,
  gf3_trit INT CHECK (gf3_trit IN (-1, 0, 1))
);
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PAYPAL_ACCESS_TOKEN` | Yes | OAuth2 access token |
| `PAYPAL_ENVIRONMENT` | Yes | `SANDBOX` or `PRODUCTION` |
| `PAYPAL_CLIENT_ID` | For refresh | App client ID |
| `PAYPAL_CLIENT_SECRET` | For refresh | App client secret |

## Error Handling

Common PayPal API errors:
- `AUTHENTICATION_FAILURE` - Token expired, refresh required
- `INVALID_RESOURCE_ID` - Invoice/order not found
- `PERMISSION_DENIED` - Scope not authorized
- `RATE_LIMIT_REACHED` - Too many requests, backoff

## Triadic Skill Composition

PayPal-MCP as ERGODIC (0) coordinator in payment triads:

```
┌─────────────────────────────────────────────────────────────────┐
│  PAYMENT TRIAD                                                   │
├─────────────────────────────────────────────────────────────────┤
│  +1 GENERATOR   │  aptos-agent      │  Create crypto txn        │
│   0 COORDINATOR │  paypal-mcp       │  Bridge to fiat           │
│  -1 VALIDATOR   │  duckdb-ies       │  Verify settlement        │
├─────────────────────────────────────────────────────────────────┤
│  Σ trits = (+1) + (0) + (-1) = 0 ≡ 0 (mod 3) ✓                 │
└─────────────────────────────────────────────────────────────────┘
```

## See Also

- `aptos-agent` - Aptos blockchain interactions
- `aptos-trading` - DEX swaps for APT→PYUSD
- `duckdb-ies` - Transaction tracking and analytics
- `google-workspace` - Invoice delivery via Gmail

## References

- [PayPal MCP Server](https://github.com/paypal/mcp)
- [PayPal REST API Docs](https://developer.paypal.com/docs/api/overview/)
- [PYUSD Documentation](https://www.paypal.com/pyusd)
