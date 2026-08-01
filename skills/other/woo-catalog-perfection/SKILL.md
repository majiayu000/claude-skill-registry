---
name: woo-catalog-perfection
description: Drive a WooCommerce catalog to an AI-readiness score of 90+ — an ordered fixlist loop that writes the missing images alt text, descriptions, brands, GTINs and category mappings, with a snapshot before every change.
license: MIT
metadata:
  author: "Respira for WordPress"
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: commerce
---

# Woo Catalog Perfection


## Description

Close the loop from "your catalog scores 43" to "your catalog scores 90+", product by product, with every change snapshotted.

AI shopping surfaces reject rows that are missing images, descriptions, brands or identifiers, and rank thin content last. This skill runs the Respira readiness fixlist as a work queue: score the catalog, fetch the ordered list of failing products with the exact tool that fixes each gap, apply the fixes in safe batches, and re-score until the target is reached. It writes real content, not filler: descriptions are drafted from the product's own attributes, categories and existing copy, and anything uncertain is queued for the merchant instead of invented.

Requires the Respira WooCommerce Add-on v3.1+.

---

## Trigger Phrases

This skill activates when the user says any of the following:

- "fix my catalog for ai"
- "improve my ai readiness score"
- "fix products failing the feed checks"
- "my products keep getting rejected by google"
- "catalog perfection"
- "fix missing gtins" / "fix missing brands" / "fix product descriptions"
- "get my catalog to 90"
- "clean up my product data"
- "feed disapprovals woocommerce"

**Do NOT trigger for:** feed setup and platform registration (that is woo-agent-storefront), pricing changes, or content work outside the catalog.

---

## Execution Workflow

### Step 1: Score and scope

`respira_get_site_context`, then `woocommerce_catalog_ai_readiness` for the baseline score and `woocommerce_readiness_fixlist` for the ordered work queue. Report: current score, how many products fail which checks, and the estimated pass count. Agree the target (default 90) and the batch size (default 10 products per pass, so every batch is reviewable).

### Step 2: Fix in priority order

The fixlist orders work by impact. Per product, apply only what the fixlist maps, using the tool it names:

1. **Missing GTIN** → `woocommerce_update_product` with `global_unique_id` when the user can supply real GTINs (ask; never fabricate a GTIN. If none exist, assign brand + SKU so identifier rules pass via brand+MPN).
2. **Missing brand** → `woocommerce_create_brand` / `woocommerce_update_product` brand assignment. Derive the brand from the product name or ask once for the house brand; apply consistently.
3. **Missing or thin description** → `woocommerce_update_product`. Draft 40-80 words from the product's own attributes, category and existing short description. No invented specs, no superlatives.
4. **Missing image alt text** → `woocommerce_set_image_alt`, descriptive and under 125 characters.
5. **Missing gallery** → `woocommerce_update_product` with `gallery_image_ids` only from existing media (`respira_list_media`); never hotlink.
6. **Unmapped categories** → `woocommerce_set_feed_category_mapping` to the closest Google taxonomy node.

Batch writes 10 at a time. Every write is snapshotted by the add-on automatically; state the snapshot coverage in the report.

### Step 3: Re-score and loop

After each batch, `woocommerce_validate_feed` (google) for the score delta. Continue until the target is hit, the fixlist is empty, or the remaining items need merchant input (real GTINs, product photos). Queue those explicitly instead of guessing.

### Step 4: Report

Close with: score before → after, products fixed per check type, what was written (with snapshot note: "every change is reversible for 90 days"), and the merchant-input queue (missing photos, GTINs to source). If feeds are enabled, remind that they rebuild automatically within minutes, so the fixes reach Google/ChatGPT on the next platform fetch.

---

## Safety

- Dry-run first on any bulk operation that supports it; show the preview before applying.
- Never fabricate GTINs, specs, materials, dimensions or certifications. Uncertain = ask or queue.
- Batches of 10 with a re-score between batches, so a bad pattern is caught after 10 products, not 500.
- Every write goes through the add-on's snapshot envelope; mention rollback in the final report.
