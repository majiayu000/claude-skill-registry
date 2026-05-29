---
name: bitrefill-website
description: "Browse and search Bitrefill's 1,500+ gift cards, top-ups, and eSIMs across 180+ countries. Filter by brand, category, or country — no credentials required."
compatibility: "No credentials or API access required. Instruction-only skill for navigating bitrefill.com."
metadata:
  author: bitrefill
  version: "1.2.1"
  homepage: "https://www.bitrefill.com"
---

# Bitrefill Website Skill

Use this skill when the user wants to **explore** Bitrefill (bitrefill.com): learn about products, search, compare, or understand pricing and availability. Bitrefill sells digital goods (gift cards, mobile top-ups, eSIMs) and offers Bitcoin/Lightning services. All products are delivered digitally.

> **Programmatic access & purchases:** For searching via API, buying products, managing orders, or any automated workflow, use the **bitrefill-cli** skill instead. This skill is browse-only — it helps users navigate and understand the website.

## When to Use This Skill

Activate when the user:
- Mentions **Bitrefill** or bitrefill.com
- Asks how to **search**, **find**, or **compare** products on Bitrefill
- Needs **information** (pricing, availability, country restrictions, denominations)
- Wants to understand what Bitrefill offers or how a product type works

**Redirect to bitrefill-cli** when the user wants to:
- **Buy** a product, make a purchase, or pay with crypto
- Use the Bitrefill **API** or **MCP endpoint** programmatically
- Manage **orders** or **invoices**
- Perform any **automated** or **CLI-based** workflow

If the request is vague (e.g. "I need a gift"), ask what type of product and for whom (country/interests).

## Quick Decision: What Does the User Want to Do?

```
User intent?
├─ Learn what Bitrefill offers / product types     → See "Product types at a glance" below; details in references/product-types.md
├─ Search or browse for a product                 → references/search-and-browse.md
└─ Get detailed info (price, country, how it works)→ references/search-and-browse.md
```

## Product Types at a Glance

| Product type | What it is | Main URL | Load details when needed |
|--------------|------------|----------|---------------------------|
| **Gift cards** | Digital gift cards (shopping, streaming, gaming, food, travel) | bitrefill.com/{country}/{lang}/gift-cards/ | references/product-types.md, references/supported-categories.md |
| **Mobile top-ups** | Prepaid airtime/data for a phone number (200+ countries) | bitrefill.com/refill/ | references/product-types.md |
| **eSIMs** | Travel data plans (data-only, QR activation, 190+ countries) | bitrefill.com/esim/all-destinations or bitrefill.com/{country}/{lang}/esims/ | references/product-types.md |
| **Bitcoin / Lightning** | Channel opening, liquidity, payment tools | bitrefill.com (relevant sections) | references/product-types.md (brief) |
| **Account & Auth** | Signup, login, password reset, referral program | bitrefill.com/signup, /login | references/account-and-auth.md |

**Critical:** Many products are **country- or region-specific**. Always confirm or infer the user's country (and, for top-ups, carrier) before recommending a product or flow.

- **Country in URL:** The first path segment is **country**, the second is **language** (e.g. `/us/en/gift-cards/`, `/mx/es/gift-cards/`). The country segment filters the **inventory shown** to gift cards usable in that country. To see a specific country's inventory, use that country in the URL.
- **Geolock:** Purchasability is enforced at **IP level**, not by the URL. If a product is not purchasable, it is due to the user's IP/location, not the country chosen in the URL.

## Task Flows (High Level)

### Browse or search

1. Identify **product type** (gift card / top-up / eSIM) and **country** (and carrier for top-ups if known).
2. For **quick discovery** of gift cards, send the user directly to search results: `https://www.bitrefill.com/{country}/{lang}/gift-cards/?q={query}` (e.g. `https://www.bitrefill.com/us/en/gift-cards/?q=amazon`) — no need to navigate from the home page.
3. For **eSIM discovery by destination**, send the user to **bitrefill.com/esim/all-destinations** to browse 190+ countries/regions.
4. Otherwise direct to the right section or use site search; help filter by category, brand, or amount.
5. For depth (categories, brands, denominations): **references/search-and-browse.md**, **references/supported-categories.md**.
6. **Category = path.** To list a category (or subcategory), use `/{country}/{lang}/gift-cards/{category-slug}/`.
7. **Subcategories:** Some categories have subcategories (e.g. travel → flights, train, bus). Same path pattern; slug = subcategory.
8. **Listings filters & sort:** Gift-card listings (all / category / subcategory) support query params: **filters** — `redemptionMethod` (online|instore), `minRating` (2–5), `minRewards` (1–10 cashback); **sort** — `s=2` (A–Z), `s=3` (recently added), `s=4` (cashback); default = popularity. See references/search-and-browse.md.

## Tips and Common Pitfalls

- **Country first:** Use the country in the URL to show the right inventory (cards usable in that country). Region-locked products (e.g. Amazon US vs UK) are the main source of errors — align product country with the user's.
- **Geolock vs URL:** Whether a product can be bought is determined by the user's IP (geolock), not by the country in the URL. The URL only controls which inventory is listed.
- **Refunds:** Digital goods are typically non-refundable once delivered; set expectations before purchase.

## Limitations

- **No scraping:** Cloudflare blocks automated access to www.bitrefill.com. Do not use firecrawl or direct scraping — requests return 403.
- **No API access:** This skill does not use the Bitrefill API or MCP endpoint. For programmatic access (search, buy, order management), use the **bitrefill-cli** skill.

## References

Load only when the agent needs more detail:

| Reference | Use when |
|-----------|----------|
| [product-types](references/product-types.md) | Explaining gift cards vs top-ups vs eSIMs, or how each works on the site |
| [search-and-browse](references/search-and-browse.md) | User wants to find or filter products |
| [supported-categories](references/supported-categories.md) | Listing categories or popular brands (gift cards, etc.) |
