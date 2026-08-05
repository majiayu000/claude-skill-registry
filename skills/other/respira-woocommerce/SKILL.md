---
name: respira-woocommerce
description: Use for WooCommerce operations on a WordPress site. Listing, reading, creating, updating, and duplicating products. Managing categories and tags. Reading orders and updating order status. Stock management. Sales reports. Storefront layout edits. Builder-aware throughout. Requires the Respira WooCommerce add-on (paid).
metadata:
  short-description: Builder-aware WooCommerce product, category, order, stock, and storefront management
  version: 1.2.0
  updated_at: 2026-05-17
  respira_min_version: 7.1.0
  requires_addon: respira-woocommerce-addon
---

# Respira WooCommerce

## What this skill covers

The Respira WooCommerce add-on (v2.1.0+) exposes 21 abilities through the WordPress Abilities API, plus a storefront layout surface for Elementor, Divi, Flatsome UX Builder, Bricks, and Gutenberg shop / product templates. The add-on is paid and license-gated; if the add-on isn't active, every Woo tool returns a clear `respira_webmcp_woo_unavailable` error and the user should be sent to `respira.press/addons/woocommerce`.

The 21 abilities namespace under `respira-woocommerce/*`:

- **Products**: get-products, get-product, create-product, update-product, duplicate-product.
- **Categories**: get-categories, get-category, create-category, update-category, delete-category.
- **Tags**: get-tags, get-tag, create-tag, update-tag, delete-tag.
- **Orders**: get-orders, get-order, update-order-status.
- **Stock**: get-stock-status, update-stock.
- **Reporting**: get-sales-report.

The storefront surface (under `/respira/v1/woocommerce/storefront/`) covers `analyze-shop`, `analyze-product`, `update-card-layout`, and `add-low-stock-badge`. These act on builder-managed product card templates rather than the WC core data.

## Common Mistakes

| Mistake | Correct approach |
|---|---|
| Using `respira_update_page` on a WooCommerce product page | Use the WooCommerce update-product ability for product data. Use `respira_find_element` plus `respira_update_element` for builder-managed visual content on the page. |
| Editing product price or stock directly in the page content | These are post meta fields. Use the update-product or update-stock abilities. |
| Running get-products without pagination on a large catalog | Always set `per_page` (max 100) and paginate. Large catalogs cause timeouts. |
| Applying a coupon via post meta | Coupons should go through the canonical WooCommerce coupon mutation (or the WC admin). Direct meta edits bypass WC validation. |
| Editing a builder-managed shop archive template via update_page | Use `respira_get_builder_info` to identify the template type first. The storefront tools cover product-card layout changes; visual edits go through `respira_update_element`. |
| Not checking whether WooCommerce is active before calling Woo tools | Confirm with `respira_get_site_context`. Woo tools return a structured error if the plugin is inactive or the add-on isn't licensed. |
| Forgetting that update-order-status only changes status | Updating the rest of the order (line items, totals, addresses) needs the WC admin or a dedicated tool. The ability is narrow on purpose. |

## Inputs

- Product ID, SKU, or search term.
- Category or tag slug or ID.
- Order ID or order status filter (pending, processing, on-hold, completed, cancelled, refunded, failed).
- Coupon code or coupon ID.
- The fields to read or update.

## Workflow

### Product operations

1. `respira_get_site_context`. Confirm WooCommerce active + add-on licensed.
2. `get-products`. Find the product by name, SKU, or filter. Set `per_page` and paginate.
3. `update-product`. Apply changes (price, stock, status, title, description, images).
4. For visual / builder content on the product page: `respira_get_builder_info` plus `respira_find_element` plus `respira_update_element`.

### Category and tag operations

1. `get-categories` or `get-tags`. Find the target by slug or name.
2. `create-`, `update-`, or `delete-`. Mutations gated by capability checks.
3. Reorder or reparent through `update-category` (parent + display order).

### Order operations

1. `get-orders` with a status filter.
2. `get-order` for a specific record.
3. `update-order-status` for status transitions. Anything more invasive needs the WC admin.

### Stock operations

1. `get-stock-status` for a snapshot.
2. `update-stock` for quantity or status mutations. The ability respects `manage_stock` per product.

### Storefront layout

1. `analyze-shop` or `analyze-product`. Returns the active builder and the editable card / template paths.
2. `update-card-layout` to mutate the product card structure.
3. `add-low-stock-badge` to insert the conditional badge widget.
4. Always snapshot the page first with `respira_create_page_duplicate`.

### Batch product updates

For updating multiple products (a price increase across a category):

1. `get-products` with the category filter. Collect target IDs.
2. `respira_batch_update`. Apply the same field change across all collected IDs in a single call.

## Rules

- Always check WooCommerce is active and the add-on is licensed before calling Woo tools.
- Never use `respira_update_page` on a product page to change price, stock, or product meta. Those are WC data fields.
- For product description: if the product page uses a builder, the visual description may live in the builder JSON. Use `respira_find_element` to locate it. The WC `description` field is the fallback (non-builder) description.
- `respira_batch_update` accepts a maximum of 100 items per call. Chunk larger operations.
- Never create or modify coupons without confirming the discount type with the user. A percent coupon applied as fixed_cart can cause significant revenue loss.
- Currency is per-site. Don't assume USD or EUR; read it from `respira_get_site_context`.

## Verification

After `update-product`:

1. Call `get-product` and confirm the changed fields match.
2. For price changes, verify both `regular_price` and `sale_price` are correct.
3. For stock changes, verify `stock_quantity` and `stock_status`.

After `update-order-status`:

1. Call `get-order` and confirm the status transition.
2. Note that WC emails fire automatically on certain transitions; tell the user.

After a batch update:

1. Sample 2-3 products from the batch and verify the changed field.
2. Report the total number of products updated and any that returned errors.

## Escalation

Stop and ask the user if:

- The product catalogue has more than 1,000 items and the request is "update all products". Confirm scope and batch strategy first.
- A coupon update would affect unlimited use or a site-wide discount. Confirm before applying.
- WooCommerce Subscriptions, Memberships, or Bookings are involved. These have their own data models. Check available tools before proceeding.
- The update would change a product's `status` from `publish` to `draft`. Confirm the user intends to unpublish.
- An order has been paid and shipped, and the request would modify it. WC stores immutable history on paid orders; ask before mutating.

## Example

Goal: update the regular price of "Merino Wool Tee" from €49 to €59.

```
1. respira_get_site_context        → WooCommerce 8.7 active, Woo add-on licensed ✓
2. get-products                    → search "Merino Wool Tee" → ID 2847
3. update-product                  → ID 2847, regular_price: "59"
4. get-product                     → ID 2847 → regular_price: "59.00" ✓
```
