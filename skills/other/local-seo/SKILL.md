---
name: local-seo
description: Local-business SEO and structured-data framework for content-platform Product-Builder products that need to be found (storefronts, restaurant online-ordering, real-estate listings, service-business sites). Codifies schema.org structured data (LocalBusiness/Product/Menu/RealEstateListing), Core Web Vitals as a ranking input, local on-page signals (NAP consistency, Google Business Profile alignment), sitemap/robots/canonical hygiene, and listing syndication. Applied by senior-dev when building public pages and checked by cms-reviewer. cms-reviewer reviews SEO; this skill is how you BUILD it right the first time.
when_to_use: |
  Apply when building public, indexable pages for a local or commerce product:
  - storefront / online-ordering / listings / service-business landing pages
  - any page meant to rank in local or product search
  Do NOT apply to authenticated app surfaces or internal dashboards (noindex those).
effort: low
allowed-tools: Read, Write, Grep, Glob, WebFetch
paths:
  - "docs/architecture/**"
  - "docs/design/**"
  - "app/**"
  - "src/**"
---

# Local SEO — built to be found, not just reviewed

For a storefront, a restaurant, or a listing site, being discoverable IS the product. SEO
designed in is cheap; SEO retrofitted is a rebuild. Build these signals from the first page.

## 1. Structured data (schema.org) — the biggest local lever

Emit JSON-LD matching the entity, validated against Google's Rich Results requirements:

- **LocalBusiness** (+ the specific subtype: Restaurant, HomeAndConstructionBusiness,
  RealEstateAgent) — name, address (PostalAddress), geo, telephone, openingHours, priceRange,
  url, sameAs (social). This is the single highest-impact local SEO signal.
- **Product** + **Offer** (storefront) — name, image, price, availability, aggregateRating.
- **Menu** / **MenuItem** (restaurant online-ordering).
- **RealEstateListing** / **Residence** (listings) — price, address, floorSize, numberOfRooms.
- **BreadcrumbList** on every deep page; **FAQPage** where there's Q&A.

Validate every type with the Rich Results test before shipping; invalid JSON-LD earns nothing.

## 2. NAP consistency + Google Business Profile alignment

Name / Address / Phone must be **byte-identical** across the site, the LocalBusiness JSON-LD,
and the Google Business Profile. Inconsistent NAP fractures local ranking. State the canonical
NAP once and reuse it.

## 3. Core Web Vitals are a ranking input (not just perf)

LCP / INP / CLS feed search ranking for these pages. Coordinate with performance-engineer,
but the SEO-driven minimums: optimized responsive images (AVIF/WebP + srcset — see
`media-pipeline-engineer`), no layout shift on load (sized media), fast TTFB. A slow local
page loses to a fast competitor regardless of content.

## 4. Crawl + index hygiene

- **sitemap.xml** auto-generated from the catalog/listings, with `lastmod`; submitted.
- **robots.txt** allows indexable pages, blocks app/admin/checkout-internal.
- **Canonical** on every page (self or the preferred variant) — kills duplicate-content loss
  from filters/pagination/UTM.
- **noindex** authenticated + thin/internal pages explicitly.
- Clean, stable, keyword-relevant URLs (`/menu/margherita`, not `/p?id=8842`).

## 5. On-page + content signals

- One `<h1>` per page; descriptive `<title>` + meta description per page (templated from the
  entity, not duplicated site-wide).
- Descriptive `alt` text on every image (a11y AND image search).
- Internal linking between related entities (product↔category, listing↔neighborhood).
- Location pages for multi-location businesses (one indexable page per location, unique content).

## 6. Syndication (where the product distributes)

For listings/storefronts that syndicate (MLS/IDX, Google Shopping, marketplaces), the
canonical lives on **our** page; syndicated copies point back. Define the feed format +
update cadence (coordinate the source-of-truth with integrations-engineer).

## Output

When applied, contribute an **SEO** section to the architecture/design doc and a checklist
the senior-dev build satisfies:

```
## SEO
- schema.org types: <LocalBusiness subtype + Product/Menu/Listing> · JSON-LD validated
- canonical NAP: <name/address/phone> (identical in JSON-LD + GBP)
- CWV minimums: LCP/INP/CLS targets (with performance-engineer)
- crawl: sitemap.xml (lastmod) · robots.txt · canonical on all · noindex app/admin
- on-page: 1×h1, per-page title/meta, alt text, clean URLs
- syndication (if any): canonical = our page; feed = <format/cadence>
```
