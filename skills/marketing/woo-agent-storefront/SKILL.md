---
name: woo-agent-storefront
description: Make a WooCommerce store discoverable and shoppable for AI assistants — set up product feeds in six formats, serve a store llms.txt, register with Google Merchant Center / OpenAI / Meta / Pinterest / TikTok, and hand out attributed cart links.
license: MIT
metadata:
  author: "Respira for WordPress"
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: commerce
---

# Woo Agent Storefront


## Description

Turn a WooCommerce store into an agent-ready storefront: always-fresh product feeds, a store llms.txt, program enrollment, and attributed cart links.

AI assistants recommend products to millions of shoppers, and they can only sell what they can read. This skill walks the whole path: configure and generate feeds in the formats the platforms actually ingest (Google Shopping XML, OpenAI/ChatGPT JSONL, Meta CSV, Pinterest CSV, TikTok CSV, generic CSV), validate them against each spec before registering anything, serve a store llms.txt at the site root, guide the merchant through each platform's enrollment (including the gated ones), and finish with signed cart links whose orders are attributed back to their agent source.

Requires the Respira WooCommerce Add-on v3.1+.

---

## Trigger Phrases

This skill activates when the user says any of the following:

- "make my store visible to chatgpt"
- "set up product feeds"
- "google shopping feed woocommerce"
- "agentic shopping for my store"
- "make my store agent-ready"
- "sell through ai assistants"
- "openai product feed"
- "submit products to google merchant center"
- "llms.txt for my store"
- "tiktok catalog feed" / "pinterest catalog feed" / "meta product feed"
- "cart links for ai agents"
- "agent storefront"

**Do NOT trigger for:** catalog content fixes without a discovery/feeds context (that is woo-catalog-perfection), general SEO requests, or stores without WooCommerce.

---

## Execution Workflow

### Step 1: Verify the surface

Call `respira_get_site_context` to confirm the connection, then `woocommerce_get_feed_status`. If the feed tools are missing, the store runs an add-on older than 3.1: stop and tell the user to update the Respira WooCommerce Add-on first.

### Step 2: Baseline the catalog

Run `woocommerce_validate_feed` for `google` (the strictest spec). Report the score and the failing checks in plain language. If the score is under 70, recommend running the **woo-catalog-perfection** skill first, and offer to continue anyway: platforms reject individual rows, not whole feeds.

### Step 3: Configure

Ask which surfaces matter (default: Google + OpenAI + generic CSV; offer Meta, Pinterest, TikTok). Then `woocommerce_configure_feed` with:

- `enabled_formats` per the answer
- `llms_txt: true` unless the site already serves one
- `cadence`: `daily` for most stores, `hourly` for stores with frequent price/stock changes (note: OpenAI recommends frequent refresh, which needs a real server cron, not wp-cron)
- `include_out_of_stock`: keep the default `true` (platforms prefer marked rows over vanishing rows)

Map categories with `woocommerce_set_feed_category_mapping` for the store's top-level product categories to Google's taxonomy. The tool lists unmapped terms; map the biggest ones first.

### Step 4: Generate and verify

`woocommerce_generate_feed`, then `woocommerce_get_feed_status` until every enabled format reports rows and a fresh timestamp. Fetch each public URL once and confirm it returns content (the pretty URL first, the /wp-json fallback if the host intercepts unknown paths). Confirm `/llms.txt` resolves at the site root. Surface any `cron_warning` from the status verbatim, with the fix (a real cron hitting wp-cron.php).

### Step 5: Register with each platform

Hand the user the exact feed URL for each platform with a short enrollment walkthrough:

- **Google Merchant Center**: Products → Data sources → Add product source → scheduled fetch with the `google.xml` URL. Bing Merchant Center accepts the same file.
- **OpenAI / ChatGPT**: apply for product discovery at chatgpt.com/merchants; the `openai.jsonl` URL is the feed they ingest. Instant Checkout is per-merchant approval; discovery is the open lane.
- **Meta Commerce Manager**: Catalog → Data sources → Data feed → scheduled fetch with the `meta.csv` URL.
- **Pinterest**: Business hub → Catalogs → Add data source with the `pinterest.csv` URL.
- **TikTok**: Seller Center → Products → Catalog upload with the `tiktok.csv` URL. TikTok requires a brand per product; the feed falls back to the store name where brand is missing, but real brands match better.

Do this as a checklist the merchant can complete asynchronously; none of these dashboards are reachable through MCP.

### Step 6: AI crawler access

Run `woocommerce_catalog_ai_readiness` and check the robots/AI-crawler section. If GPTBot, OAI-SearchBot, Google-Extended or PerplexityBot are blocked in robots.txt, tell the user exactly which line blocks which assistant and what removing it does. Do not edit robots.txt without explicit approval.

### Step 7: Attributed cart links

Demonstrate the loop end to end: create one cart link with `woocommerce_create_cart_link` (two real products, a source label like `chatgpt`), explain that the link fills the cart server-side and lands on the store's own checkout, and show where the numbers land with `woocommerce_agent_orders_report`. Checkout, payments and customer data stay on the store.

### Step 8: Report

Close with: enabled formats and their URLs, catalog score, categories mapped/unmapped, llms.txt status, the per-platform registration checklist with what is done vs pending, and the example cart link.

---

## Safety

- Feed generation is read-only over the catalog; it writes only its own option rows and feed files.
- Never edit robots.txt, prices, or products in this skill without explicit user approval; content fixes belong to woo-catalog-perfection.
- Feed URLs contain an unguessable token. Treat them like capability URLs: share with platforms, not in public posts.
