---
name: ucp-fulfillment
description: Implement the UCP Fulfillment extension — shipping and pickup methods, destinations, fulfillment groups, selectable options, and estimated delivery. Use when adding shipping/pickup logic to a UCP checkout.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# UCP Fulfillment Extension

## Before writing code

**Fetch live spec**: Web-search `site:ucp.dev specification fulfillment` and fetch the page for the exact fulfillment schema, method types, group structure, and configuration options.

## Conceptual Architecture

### Extension Relationship

Fulfillment **extends** `dev.ucp.shopping.checkout`. It is pruned from negotiation if the Checkout capability is not in the intersection. Declared as `"extends": "dev.ucp.shopping.checkout"` in the schema.

### Key Concepts

- **Methods**: `shipping` or `pickup`. Each method is tied to specific line items via `line_item_ids`.
- **Destinations**: Where items go. For shipping: postal addresses. For pickup: retail locations.
- **Groups**: Business-generated packages/shipments. Each group belongs to a method and contains selectable options.
- **Options**: Individual fulfillment choices within a group (e.g., "Standard Shipping 5-7 days", "Express 1-2 days"). Each has a title, carrier, estimated delivery window, and cost totals.
- **Available Methods**: Alternative fulfillment methods the buyer can switch to, with `fulfillable_on` indicating availability (`"now"` or an ISO date).

### Configuration

The fulfillment extension has two configuration scopes:

**`platform_config`** (set by the platform, describes platform-level behavior):
- `supports_multi_group`: Whether the platform supports handling multiple fulfillment groups/shipments

**`merchant_config`** (set by the merchant/business, describes business-level behavior):
- `allows_multi_destination`: Whether multiple shipping addresses are supported (per method type)
- `allows_method_combinations`: Which method types can be combined (e.g., `[["shipping", "pickup"]]`)

### Flow

1. Platform creates checkout with line items
2. Business returns fulfillment methods with empty destinations and groups
3. Platform updates checkout with shipping address(es)
4. Business recalculates and returns fulfillment groups with selectable options
5. Platform selects an option per group (or lets user choose)
6. Business updates totals to include fulfillment costs
7. Checkout becomes `ready_for_complete`

### Implementation Guidance

Fetch the exact current schema from the live spec before implementing. The fulfillment data model has nested structures (methods → destinations → groups → options) that evolve across spec versions.

Also check the sample server at https://github.com/Universal-Commerce-Protocol/samples for reference fulfillment implementation.
