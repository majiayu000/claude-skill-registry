---
name: woo-pricing-promotions
description: "Use when the user says 'run a sale', 'discount this category', 'set up a coupon', 'reprice these products', 'end the sale', or asks what a discount would cost them. Plans the price change, shows it as a preview before anything moves, writes it with a snapshot, and can put it back."
license: MIT
metadata:
  author: "Respira for WordPress"
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: commerce
---

# Woo Pricing and Promotions

Runs a sale, a repricing, or a coupon on a live WooCommerce store, and treats the money as money. Every change is previewed before it happens, snapshotted when it does, and reversible afterwards.

## What this skill does

Pricing is the one place on a store where a plausible-looking mistake costs real money before anyone notices. A misplaced decimal is not a broken layout somebody reports; it is orders at the wrong price, and by the time it surfaces the orders exist. So the order of operations here is deliberate: understand the current prices, state the change in money rather than percentages, show it, then write it.

**Handles:**
- Category-wide or list-based repricing, by percentage, by fixed amount, or to a set value
- Scheduled sales with start and end dates, so the sale ends without anyone remembering to end it
- Coupons: fixed, percentage, free shipping, with usage limits and product or category restrictions
- Sale badges on the storefront
- Putting a price change back from the snapshot it wrote

## What this skill does NOT do

- **Decide the discount.** Depth is a margin decision. This skill will tell you what a discount costs against recent sales volume; it will not pick one.
- **Beat the guardrails.** A move over 50%, a discount deeper than 70%, or a price under 0.50 comes back blocked. That is the add-on refusing, and it is refusing on purpose. Say so plainly and ask, rather than resending with the override.
- **Touch tax, currency, or payment configuration.**
- **Reprice a variable product's parent and hope.** Variations carry their own prices; name them.

## Requirements

- WooCommerce with the Respira WooCommerce add-on, licensed
- The store's own reporting for volume, which `get-sales-report` reads

## Trigger Phrase

- "run a sale"

## Alternative Triggers

- "discount this category"
- "set up a coupon"
- "reprice these products"
- "end the sale"
- "what would 20% off cost me"

## Execution Workflow

### Phase 1: See the current state

Never reprice from memory of what a product costs.

1. `respira_woo_list-products-advanced` for the target set, or `get-product` for a named one. This also matters mechanically: reads are what the add-on records as provenance, and a write to something never read is annotated as unverified.
2. `get-sales-report` over a comparable recent window, so the discount has a volume to be measured against.
3. Note anything already on sale. Stacking a new sale on an existing one is the most common way a discount ends up twice as deep as intended.

### Phase 2: State it in money

Convert the ask into per-product numbers, and say them:

> 14 products in Outdoor. Regular prices 24.00 to 189.00. A 20% sale takes the range to 19.20 to 151.20. Against the last 30 days that is about 340 in discount at the same volume. Two of these are already on sale at 15%, so they would go to 32% off unless excluded.

Ask before writing. A percentage sounds smaller than the money it is.

### Phase 3: Preview

Run the write with `dry_run: true` first, every time. The response lists each product with its old and new prices and names anything the guardrails would block. Show that list. A preview is cheap and a repricing is not.

### Phase 4: Write

- `bulk-update-prices` for a repricing, or `schedule-sale` when it should end by itself
- `create-coupon` for a code, with `usage_limit` set unless the user says otherwise, because an uncapped code is a liability
- `add-sale-badge` if the storefront should show it

Snapshots are captured automatically. Report the snapshot ids.

### Phase 5: Confirm and hand back the undo

State what changed, in money, and how to reverse it: `revert-pricing` with the product and snapshot id. If the sale was scheduled, say the date it ends without anyone acting.

## Safety Model

- Preview before every write, no exceptions
- Snapshot before each price change, with a named path back
- Guardrails refuse outsized moves; treat a block as a question for the user, never as an obstacle to route around
- Coupons default to a usage limit
- Nothing here touches an existing order's price

## Honest Disclaimer

This skill changes live prices on a real store.

It cannot: judge whether a discount is good for the business, model demand, know your margins, or see a competitor's pricing. It will not decide depth for you.

It can: show what a change costs before it happens, apply it consistently across a set, schedule an end, and put it back.

## Tooling

`respira_woo_list-products-advanced`, `respira_woo_get-product`, `respira_woo_get-sales-report`, `respira_woo_bulk-update-prices`, `respira_woo_schedule-sale`, `respira_woo_revert-pricing`, `respira_woo_create-coupon`, `respira_woo_update-coupon`, `respira_woo_list-coupons`, `respira_woo_add-sale-badge`

## Telemetry

After run completion, fire-and-forget to `POST https://www.respira.press/api/skills/track-usage` with `skill_slug = woo-pricing-promotions`, site and version context, duration, products repriced, coupons created, blocks hit. Never block the user on telemetry.

## Related Skills

- Woo Catalog Perfection (fix the catalog the sale runs on)
- Woo Marketing Campaigns (tell people the sale exists)
- WooCommerce Health Check (state of the store before a promotion)

---

Built by Respira Team
https://respira.press/skills/woo-pricing-promotions
