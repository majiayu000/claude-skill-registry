---
name: ucp-discount
description: Implement the UCP Discount extension — discount code application, validation, allocation tracking, and error handling. Use when adding promo code or discount logic to a UCP checkout.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# UCP Discount Extension

## Before writing code

**Fetch live spec**: Web-search `site:ucp.dev specification discount` and fetch the page for the exact discount schema, allocation model, and error codes.

## Conceptual Architecture

### Extension Relationship

Discount **extends** `dev.ucp.shopping.checkout`. Pruned if Checkout capability is absent.

### Key Concepts

- **Codes**: Array of discount code strings submitted by the buyer/agent.
- **Applied discounts**: Array of successfully applied discounts, each with:
  - `code`: The code that was applied
  - `title`: Display name
  - `amount`: Total discount amount (minor currency units)
  - `automatic`: Whether it was auto-applied (not from a code)
  - `method`: `"each"` (per-item) or `"across"` (spread across all applicable items)
  - `priority`: Order of application when multiple discounts interact
  - `allocations`: Array showing exactly how the discount is distributed across line items

### Allocation Invariant

**Sum of `allocations[].amount` MUST equal `applied_discount.amount`.** This ensures the discount is fully accounted for.

Each allocation has:
- `path`: JSONPath pointing to the line item (e.g., `$.line_items[0]`)
- `amount`: Portion of discount applied to that item

### Error Codes

UCP defines standard discount error codes:
- `discount_code_expired`
- `discount_code_invalid`
- `discount_code_already_applied`
- `discount_code_combination_disallowed`
- `discount_code_user_not_logged_in`
- `discount_code_user_ineligible`

These appear in the `messages` array with `type: "warning"` specifically when a discount code is rejected.

### Flow

1. Platform sends discount codes in the checkout update
2. Business validates codes, applies valid ones, returns errors for invalid ones
3. Applied discounts affect line item totals and session totals
4. Agent resolves discount errors (remove invalid code, inform user of ineligibility, etc.)

### Implementation Guidance

Fetch the exact schema from the live spec before implementing. Pay attention to how discounts interact with fulfillment costs and tax calculations — the spec defines the ordering.
