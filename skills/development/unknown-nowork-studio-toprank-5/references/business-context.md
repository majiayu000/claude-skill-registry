# Business Context — Crawl, Bootstrap, and Schema

The single source of truth for gathering business context for Meta Ads. Used by `/meta-ads-audit` to write `{data_dir}/meta/business-context.json`, and read by `/meta-ads` on every invocation.

If `{data_dir}/business-context.json` already exists from `/google-ads-audit`, **read it first as a starting point** — most fields (services, brand voice, differentiators, locations, seasonality, unit economics) are platform-agnostic. Then write a Meta-specific copy to `{data_dir}/meta/business-context.json` with overrides only where Meta-specific (creative inventory, custom audiences, Pixel health, funnel events).

## When to crawl

- First audit on a new account.
- Refresh when `audit_date` is > 90 days old.
- Refresh when the user reports a positioning change, new product line, or seasonal pivot.
- Always crawl on a full audit (Phase 4); crawl optionally on scoped audits if the file is fresh.

## What to crawl

In one parallel `WebFetch` batch:

1. **Homepage** — for value prop, hero copy, primary CTA, brand voice
2. **About page** (if exists) — for founder story, team size, year founded, location
3. **Top-spending ad's landing page** — message-match baseline; the page that's converting (or not)
4. **One additional landing page** if a different campaign points elsewhere (e.g. category vs. PDP for ecom)

For ecom specifically: also fetch the homepage and one PDP. The PDP tells you AOV-typical price point; the homepage tells you the brand promise.

Keep the crawl lean — 4 fetches in parallel is fast. Don't crawl the full site; you don't need it.

## Schema — fields and how to populate

### Identity

```json
{
  "business_name": "Brand Name",
  "industry": "ecommerce | saas | local_service | b2b_lead_gen | mobile_app | other",
  "website": "https://example.com",
  "account_id": "1234567890",
  "audit_date": "2026-05-01"
}
```

- `business_name` — from the Meta ad account name; cross-check against the homepage `<title>`.
- `industry` — pick from the enum; if the user doesn't fit cleanly, use `other` and add a `notes` line.

### Offering

```json
{
  "services": ["Premium skincare", "Subscription replenishment"],
  "differentiators": ["Founder-formulated", "Free shipping over $50", "60-day money-back"],
  "competitors": ["Competitor1", "Competitor2"],
  "locations": ["US", "CA"],
  "social_proof": ["10,000+ reviews", "Featured in Vogue", "Founder TEDx"],
  "offers_or_promotions": ["First-order 15% off", "Subscribe & save 20%"]
}
```

- Derive `services` from top-spending campaigns + landing page H1s.
- Derive `differentiators` from homepage value-prop sections; **always confirm with the user** (homepage copy lies more than any other source).
- `locations` are countries / regions where active ad sets target.
- `competitors` is almost always a user input — Meta data doesn't reveal them directly.

### Brand voice

```json
{
  "brand_voice": {
    "tone": "warm, plain-spoken, slightly cheeky",
    "words_to_use": ["clean", "real", "founder-led"],
    "words_to_avoid": ["cheap", "luxury", "ground-breaking"]
  }
}
```

Derive from top-performing ad copy (high link CTR + high CVR ads). If the user has a brand book, prefer it over inferred voice.

### Seasonality

```json
{
  "seasonality": {
    "peak_months": [11, 12],
    "slow_months": [1, 2, 7],
    "seasonal_hooks": ["Mother's Day gifting", "Black Friday bundle", "New Year reset"]
  }
}
```

For ecom, Q4 (Nov-Dec) is universal. Industry specifics: floral peaks Feb (Valentine's) + May (Mother's Day); fitness peaks January; school supplies peak July-Aug. Ask the user for unique-to-them spikes.

### Unit economics (essential — request if missing)

```json
{
  "unit_economics": {
    "aov_usd": 68.50,
    "profit_margin": 0.55,
    "ltv_usd": 220.00,
    "source": "user_provided"
  }
}
```

Without these, ROAS-aware scoring is impossible. **Always ask** if not in the file. `source` values:

- `user_provided` — user told us directly
- `inferred_from_template` — industry default (e.g. ecom apparel typical AOV $60, margin 55%) — flag as uncertain
- `derived_from_data` — computed from Shopify or Stripe data the user provided

Use `inferred_from_template` only as a temporary placeholder — never make a scaling recommendation without confirming.

### Landing pages

```json
{
  "landing_pages": {
    "https://example.com/skincare-bundle": {
      "h1": "The clean skincare bundle that actually works",
      "primary_cta": "Get the bundle — $48",
      "form_fields": 0,
      "notes": "Direct PDP; no email gate"
    }
  }
}
```

For each ad-traffic landing page, capture H1, primary CTA, form-field count (or "no form"), and any notes that affect message match. This is what `/meta-ads-audit` references when scoring creative-to-page coherence.

### Meta-specific extensions

```json
{
  "meta_funnel_events": {
    "top_of_funnel": "ViewContent",
    "mid_of_funnel": "AddToCart",
    "conversion": "Purchase"
  },
  "creative_inventory": {
    "concepts": ["UGC testimonial", "Founder explainer", "Product demo", "Lifestyle"],
    "formats": ["video_ugc", "video_studio", "static_lifestyle", "static_product"],
    "aspect_ratios": ["1:1", "4:5", "9:16"]
  },
  "custom_audiences": {
    "purchasers_180d": "audience_id_xxx",
    "abandoners_14d": "audience_id_yyy",
    "engagers_90d": "audience_id_zzz",
    "list_uploads": [
      { "name": "Email subscribers", "size": 28400, "uploaded": "2026-04-15" }
    ]
  },
  "pixel_health": {
    "pixel_id": "1234567890",
    "capi_enabled": true,
    "emq_score": 7.6,
    "last_event_at": "2026-04-30T19:45:00Z"
  }
}
```

These come from the audit data pulled in Phase 1 — fill them automatically. The user shouldn't need to provide pixel_health or custom_audiences manually; the API has them.

### Notes

```json
{
  "notes": "Founder-led brand, prefers UGC over polished studio work. Avoid the word 'natural' (FTC trouble in 2024). Q4 is 50% of annual revenue — protect Black Friday creative pipeline."
}
```

Free-form. Capture anything that doesn't fit elsewhere but a future audit needs to know.

## Crawl bootstrapping flow

1. **Read existing files in order:**
   - `{data_dir}/meta/business-context.json` (Meta-specific)
   - `{data_dir}/business-context.json` (Google Ads or shared)
   If either has content, use as starting point.

2. **Pull data-derivable fields** from the Phase 1 audit dataset (services from campaign names, locations from targeting, voice from top-CTR ads, pixel_health from API, etc.).

3. **Run the parallel WebFetch** for homepage + about + top-spending landing page + one additional. Merge findings.

4. **Ask the user (one short batch of questions)** for fields that data + crawl can't answer:
   - Differentiators — what makes you the choice over competitors?
   - Competitors — top 2–3 you compete with
   - Seasonality specifics — your spikes vs. industry typical
   - **AOV + profit margin** (essential — block on this before any scaling recommendation)
   - LTV (if subscription / repeat business)
   - Anything weird I should know? (ad policy issues, recent rebrand, audience pivot)

   Ask in one block, not iteratively — it's faster for the user.

5. **Write `{data_dir}/meta/business-context.json`** with `audit_date` set to today.

## What NOT to do

- **Don't invent competitors.** If you don't know, ask. Inventing them and using them in differentiation copy is worse than skipping it.
- **Don't infer unit economics from random web data.** Industry templates are explicit fallbacks; ad-hoc estimates from a homepage price are not.
- **Don't crawl 20 pages.** 4 is the sweet spot; more adds noise without information.
- **Don't write the file with empty `unit_economics`.** Either populate (even with `inferred_from_template`) or block on the user — but never ship it as `null` because downstream skills will break silently.
