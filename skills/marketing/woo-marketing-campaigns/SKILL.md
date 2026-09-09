---
name: woo-marketing-campaigns
description: "Use when the user says 'plan a campaign', 'promote this product', 'write the copy for our sale', 'what should we push this month', or 'draft the launch for this collection'. Reads what the store actually sells, drafts the campaign around it, and stages every page and product change for approval."
license: MIT
metadata:
  author: "Respira for WordPress"
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: commerce
---

# Woo Marketing Campaigns

Plans and drafts a campaign for a WooCommerce store from what the store actually sells, rather than from what a model imagines a store like this sells.

## What this skill does

Most campaign copy for a store is written without looking at the store. It names products that were discontinued, promises stock that is not there, and picks a hero product that has sold four units all year. The fix is not better prose, it is reading the shop first.

So this reads sales, stock and catalogue quality before it writes a word, then drafts the campaign against real products at real prices with real availability, and stages every change rather than publishing it.

**Handles:**
- Choosing what to promote from sales data and stock, not from guesswork
- Campaign plan: the offer, the products, the dates, the pages that need to exist
- Landing page and category copy, written to a duplicate for approval
- Product descriptions and short descriptions for the promoted set
- The coupon or sale the campaign depends on, through Woo Pricing and Promotions
- A post-campaign read of what actually sold

## What this skill does NOT do

- **Send anything.** No email, no ads, no social posts. It drafts; a person sends.
- **Publish.** Copy lands on duplicates. Approval is a human step, always.
- **Invent stock or dates.** If a product has four units left, the campaign says so or picks something else.
- **Set the discount.** That is a margin decision, and it belongs to the owner. See Woo Pricing and Promotions.
- **Claim anything the store cannot support.** No "best", no "award-winning", no delivery promise the shipping settings do not back.

## Requirements

- WooCommerce with the Respira WooCommerce add-on, licensed
- Enough order history for `get-sales-report` to say something useful. On a store with almost no orders, say that plainly and plan from stock and margin instead of pretending the data speaks.

## Trigger Phrase

- "plan a campaign"

## Alternative Triggers

- "promote this product"
- "write the copy for our sale"
- "what should we push this month"
- "draft the launch for this collection"

## Execution Workflow

### Phase 1: Read the shop

1. `get-sales-report` over the last 30 and 90 days. What sells, what is seasonal, what has stalled.
2. `list-products-advanced` for stock and price on the candidates. A hero product that goes out of stock on day two is a campaign that ends on day two.
3. `find-low-stock` to rule those out early.
4. `analyze-catalog-quality` on the shortlist. A product with no image and a twelve-word description will not convert however good the campaign is, and fixing that comes first.

### Phase 2: Propose, do not assume

Come back with a plan and the reasoning, in the user's terms:

> Three candidates. The waxed jacket is your best seller in this window last year and has 40 in stock. The wool scarf has better margin but 6 left, so it works as an add-on rather than the hero. The boots sell well and have no photography, which is the thing to fix before promoting them.
>
> Suggested: jacket as hero, scarf as the add-on, boots held back until they have images.

Get agreement on the products and the offer before writing any copy.

### Phase 3: Fix what would waste the traffic

If the promoted products have catalogue gaps, fix those first with Woo Catalog Perfection. Driving traffic to a product with no image is spending attention on a page that cannot convert.

### Phase 4: Draft

- Landing or category copy through `respira_create_page_duplicate` and the builder tools, never onto the live page
- `update-product` for descriptions on the promoted set, staged
- The offer itself through Woo Pricing and Promotions, previewed with `dry_run` first

Every claim traces to something read in Phase 1. Prices come from the product, availability comes from stock, delivery claims come from the shipping settings or are not made.

### Phase 5: Hand over

List the drafts, their preview links, and what remains a human decision: approving the pages, sending whatever is being sent, and the date the offer ends.

### Phase 6: Afterwards

When the campaign has run, `get-sales-report` for the window and compare against the plan. Say what worked and what did not, including when the answer is that the campaign made no measurable difference.

## Safety Model

- Reads before writes, always
- Copy to duplicates; the live page is not touched
- Nothing is published or sent by this skill
- Price changes go through the previewed, snapshotted, guardrailed path
- Claims are traceable to store data, or they are not made

## Honest Disclaimer

This skill drafts a campaign from a store's own data.

It cannot: know your customers, your brand voice beyond what it can read, your margins, or your competition. It cannot send email or buy ads. It cannot tell you whether a campaign is a good idea.

It can: pick candidates from real sales and stock rather than plausibility, stop you promoting something that is nearly out of stock or has no photograph, draft copy that matches what you actually sell, and stage all of it for you to approve.

## Tooling

`respira_woo_get-sales-report`, `respira_woo_agent-orders-report`, `respira_woo_list-products-advanced`, `respira_woo_find-low-stock`, `respira_woo_analyze-catalog-quality`, `respira_woo_update-product`, `respira_woo_create-coupon`, `respira_woo_schedule-sale`, `respira_create_page_duplicate`, `respira_update_element`, `respira_get_snapshot`

## Telemetry

After run completion, fire-and-forget to `POST https://www.respira.press/api/skills/track-usage` with `skill_slug = woo-marketing-campaigns`, site and version context, duration, products promoted, drafts created. Never block the user on telemetry.

## Related Skills

- Woo Pricing and Promotions (the offer the campaign runs on)
- Woo Catalog Perfection (fix the products before promoting them)
- Brand Voice Synthesizer (write in the store's own voice)
- SEO & AEO Amplifier (make the campaign page findable)

---

Built by Respira Team
https://respira.press/skills/woo-marketing-campaigns
