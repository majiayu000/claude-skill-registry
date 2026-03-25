---
name: acp-fulfillment
description: Implement ACP fulfillment options — shipping, digital delivery, in-store pickup, and local delivery. Use when building fulfillment selection, rate calculation, delivery window management, or tracking integration.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# ACP Fulfillment

## Before writing code

**Fetch live docs**:
1. Fetch `https://developers.openai.com/commerce/specs/checkout/` — fulfillment options are part of the checkout spec
2. Web-search `site:github.com agentic-commerce-protocol spec json-schema FulfillmentOption` for the schema
3. Web-search `site:github.com agentic-commerce-protocol rfcs orders fulfillment` for fulfillment in orders

## Conceptual Architecture

### Four Fulfillment Types

| Type | Use Case | Key Fields |
|------|----------|------------|
| **shipping** | Physical delivery to address | Carrier, tracking number/URL, delivery windows |
| **digital** | Downloads, licenses, access | Access URL, license key, expiration date |
| **pickup** | In-store or locker collection | Location, ready-by window, pickup-by deadline |
| **local_delivery** | Same-day/local service delivery | Service area, delivery window |

### How Fulfillment Works in Checkout

1. **Create session** — Merchant returns available `fulfillment_options[]` based on items and address
2. **Agent selects** — Agent (or buyer) picks a `fulfillment_option_id`
3. **Update session** — Agent sends the chosen `fulfillment_option_id` in an update
4. **Merchant recalculates** — Totals update to include fulfillment cost
5. **Post-purchase** — Merchant emits order updates with tracking and delivery details

### FulfillmentOption Object

Each option includes:
- `id` — Unique identifier for this option
- `type` — One of the four types above
- `title` — Display name (e.g., "Standard Shipping")
- `subtitle` — Additional info (e.g., "5-7 business days")
- `carrier` — Carrier name for shipping
- Delivery window (estimated dates/times)
- Pricing — Cost of this fulfillment option

### Delivery Windows

Time-based constraints:
- **Estimated delivery** — Date range for when buyer can expect delivery
- **Ready-by** (pickup) — When the order will be ready for collection
- **Pickup-by** (pickup) — Deadline to collect before order is returned
- **Delivery window** (local delivery) — Time slot for delivery

### Fulfillment in Orders

After checkout completion, fulfillment details appear in order webhook events:
- Tracking number and tracking URL
- Carrier name
- Shipment status updates
- Delivery confirmation

### Best Practices

- Return all available fulfillment options on session create (not just the cheapest)
- Compute fulfillment costs based on actual address (not estimates)
- Include realistic delivery windows — agents present these to buyers
- Update tracking information in real-time via order webhooks
- Support multiple fulfillment groups for split shipments
- Handle address validation before computing fulfillment options

Fetch the checkout spec and JSON schema for exact FulfillmentOption field names, types, and required fields before implementing.
