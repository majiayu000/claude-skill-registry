---
name: vertical-retail
description: Retail & e-commerce domain knowledge for SMB storefront products (storefront, inventory, pricing, cart-recovery). Codifies the vocabulary (SKU vs variant, reorder point, COGS/margin, ATS, AOV), the non-obvious rules (Shopify owns the storefront — don't fight it head-on; the wedge is multichannel inventory + reorder and cart recovery), the must-model entities (Product→Variants matrix, channel-aware InventoryLevel, ReorderRule, PricingRule, AbandonedCart), and what a naive build gets wrong (no variant model, single-channel inventory, reorder without lead-time/safety-stock). Applied by architect/pm during spec authoring so they aren't naive about retail; checked implicitly by pci-reviewer + cms-reviewer.
when_to_use: |
  Apply when architect or pm is speccing a retail / e-commerce product:
  - storefront / inventory / pricing / cart-recovery for an SMB seller
  - any catalog, checkout, stock-tracking, promotion, or abandoned-cart feature
  Do NOT apply to non-commerce verticals, or to heavy payments/tax work (defer those to pci-reviewer / billing).
effort: low
allowed-tools: Read, Write, Grep, Glob
paths:
  - "docs/architecture/**"
  - "docs/plans/**"
  - "docs/design/**"
---

# Retail & e-commerce — spec it like someone who's run a store

The SMB retail buyer already pays Shopify ($39–399/mo + 2.9%), BigCommerce, Wix, Ecwid, or
WooCommerce. They are not naive — so the spec can't be either. A storefront that "has products
and a cart" is table stakes; the value is in the parts those platforms do badly. Read this
before writing the catalog/inventory/pricing/cart sections of any retail ARCH or PLAN doc.

## 1. Domain vocabulary (use these exact words)

- **SKU vs variant** — a **variant** is one buyable configuration (Red / Large); its **SKU** is
  the unique code that variant ships and is counted under. A "product" is the parent; you stock,
  price, and sell *variants*, not products.
- **Multichannel / omnichannel** — selling across several channels (own storefront, Amazon,
  eBay, in-store POS, Instagram). *Omnichannel* additionally means one inventory pool behind all
  of them. Channel-awareness is the whole game for SMB inventory.
- **Reorder point** — stock level that triggers a purchase order = (avg daily demand × **lead
  time** in days) + **safety stock**. **Lead time** = supplier days from order to receipt.
  **Safety stock** = buffer for demand/lead-time variance. Reordering without all three is wrong.
- **COGS** (cost of goods sold) and **margin** = (price − COGS) / price. **Landed cost** = unit
  cost + freight + duties + handling; margin must use landed cost, not invoice cost.
- **ATS / available to sell** = on-hand − allocated (reserved by open orders) − safety stock.
  Customers buy against ATS, never raw on-hand.
- **Backorder vs preorder** — backorder = out of stock now, will refill (sell against incoming
  PO). Preorder = not released yet, future availability date. Different fulfillment promises.
- **Cart abandonment rate** = 1 − (completed checkouts / carts created); industry ~70%.
- **AOV** (average order value) and **conversion rate** = orders / sessions. The two levers
  pricing/promotions move.
- **Fulfillment** — pick/pack/ship. **Dropship** = supplier ships direct, seller never holds
  stock (so "stock" is the supplier's ATS feed, not yours).
- **MAP** (minimum advertised price) — supplier-imposed price floor; a pricing rule must respect
  it or the seller loses the brand.

## 2. Non-obvious domain rules

- **Shopify owns the storefront — don't fight it head-on.** A me-too checkout loses. The wedge is
  the platforms' *weak spots*: **multichannel inventory + reorder**, and **cart recovery**.
  Spec the storefront as competent-and-owned, and put the differentiation in the other three.
- **Variants explode combinatorially.** options (Size × Color × Material) multiply: 5×8×3 = 120
  variants per product. The data model, UI, and import flow must assume hundreds of variants per
  product, each with its own SKU / price / stock — not a flat product list.
- **Inventory must be channel-aware.** The same SKU is sold on storefront + Amazon + POS; stock
  must decrement across all and sync back, or you oversell. Single-channel inventory is the most
  common naive failure and the strongest wedge.
- **Pricing rules interact with floors.** A promotion or demand-based rule must clamp to a
  **margin floor** and **MAP**. A rule that can price below landed-cost margin is a bug, not a
  discount.

## 3. What a naive build gets wrong

- **Products without a variant model** — a flat `product { price, stock }` table. Breaks the
  instant the seller stocks two sizes. Variants are core, not an add-on.
- **Single-channel inventory** — stock that lives only in the storefront, no sync across Shopify /
  Amazon / POS. Guarantees overselling for any real SMB.
- **Reorder without lead-time / safety-stock** — "reorder when stock < 10" stocks out during the
  supplier lead time. Must use reorder-point math.
- **Cart recovery that ignores suppression / consent** — emailing/SMSing without consent, or after
  unsubscribe/purchase, is illegal (CAN-SPAM / TCPA / GDPR) and burns deliverability. Honor
  suppression + quiet hours.
- **Pricing that ignores the margin floor** — a promo engine that can sell below cost, or below MAP.

## 4. Must-model entities

| Entity | Key fields |
|---|---|
| **Product** | id, title, option axes (e.g. Size, Color) — the parent |
| **Variant** | product_id, option values (Red/L), **SKU**, price, COGS/landed cost — one per option combo |
| **InventoryLevel** | variant_id, **channel/location**, on_hand, allocated, safety_stock → derive ATS |
| **ReorderRule** | variant_id, reorder_point, reorder_qty, **lead_time_days**, supplier |
| **PricingRule** | scope (variant/collection), trigger (demand/margin/schedule), action, **margin_floor**, **MAP** |
| **AbandonedCart** | cart_id, customer, line items, value, abandoned_at, recovery state, consent/suppression |

The Variant *option matrix* and the channel-keyed InventoryLevel are the two that naive specs
collapse — keep them explicit.

## 5. Per-product notes (wedge + the one domain thing)

- **storefront** (content) — catalog, checkout, themes; a store the seller *owns*. Wedge: owned
  channel + SEO (it must rank — see [[local-seo]]). The one thing: the **Product→Variant** model
  and clean indexable URLs. Don't out-engineer Shopify's checkout; match it and move on.
- **inventory** (crud) — track stock across channels, auto-reorder before stockout. **This is the
  underserved-by-Shopify wedge.** The one thing: **channel-aware InventoryLevel + reorder-point
  math** (lead time + safety stock). Get this right and the product justifies itself.
- **pricing** (dashboard) — rules-based pricing + promotions reacting to demand/margin. Wedge:
  margin-aware automation SMBs do by hand. The one thing: every rule **clamps to margin floor +
  MAP**.
- **cart-recovery** (crm) — win back abandoned carts via timed email/SMS. Wedge: recovering the
  ~70% that abandon. The one thing: **consent + suppression + timing** — defer the messaging
  mechanics to [[lifecycle-messaging]].

## 6. Compliance (light — defer the heavy parts)

- **Sales tax nexus** — economic nexus thresholds vary by US state (post-Wayfair); the seller may
  owe tax in states they've never shipped to. Note it in the spec; defer the actual calc/filing to
  billing. Don't hand-roll tax.
- **Email / SMS consent** — cart recovery needs prior consent (CAN-SPAM / TCPA / GDPR), honored
  unsubscribe, and quiet-hours/suppression. Defer the delivery + consent machinery to
  [[lifecycle-messaging]]; the spec just states the requirement.
- **PCI** — checkout uses **Stripe-hosted** elements so card data never touches our servers
  (SAQ-A scope). State that intent; defer the scope proof to **pci-reviewer**.

## Output

When applied, contribute a **Retail domain** section to the ARCH/PLAN/DESIGN doc:

```
## Retail domain
- model: Product→Variant (option matrix, per-variant SKU/price/stock) · channel-aware InventoryLevel (ATS = on_hand − allocated − safety_stock)
- reorder: reorder_point = avg_demand × lead_time + safety_stock (not "< N")
- pricing: every rule clamps to margin_floor + MAP (margin on landed cost)
- cart-recovery: consent + suppression + timing → [[lifecycle-messaging]]
- wedge: multichannel inventory + reorder, cart recovery (don't fight Shopify's storefront/checkout)
- compliance: tax nexus → billing · consent → [[lifecycle-messaging]] · PCI Stripe-hosted (SAQ-A) → pci-reviewer
- migration: catalog/variant/stock import path → [[migration-ready-schema]]
```
