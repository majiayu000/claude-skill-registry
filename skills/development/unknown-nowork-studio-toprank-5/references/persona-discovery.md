# Persona Discovery — Meta Ads

Discovery procedure for `{data_dir}/meta/personas/{accountId}.json`. Used by `/meta-ads-audit` (creates the file) and conceptually informs creative direction in `/meta-ads`.

Personas on Meta are different from Search-engine personas. On Search, you discover personas from the **search terms** — the actual phrases people type. On Meta, you discover personas from **what creative resonates** — which angles, formats, and messaging convert. The data source is different, the framework is the same.

## Sources of evidence (in priority order)

1. **Top-performing ad creatives** — the angle, format, and messaging of ads with highest ROAS / lowest CPA. The persona is the cohort the ad spoke to successfully.
2. **Top-performing audiences** — which custom audiences and lookalike seeds convert best.
3. **Landing page content** — which pages convert best from Meta traffic; the person on the page when conversion happens.
4. **Demographic + placement breakdowns** — `getInsights` with `breakdowns=age,gender,publisher_platform`. Gives a coarse demographic skew.
5. **Customer email list / Shopify data** — if the user has it, real customer data > inferred from ads.

The agent should *triangulate* across at least 3 of these — a persona supported only by demographic skew is too weak.

## How many personas

2–3 is the right number for most accounts. More than 3 fragments creative production. One is usually too coarse — even single-product brands typically have a primary buyer and a gift-giver / influencer cohort.

## What goes in a persona

```json
{
  "name": "Skincare Switcher Sarah",
  "demographics": "Women 28–42, urban / suburban US, income $60k–$110k",
  "primary_goal": "Find a skincare routine that works for sensitive adult skin without the marketing nonsense",
  "pain_points": [
    "Tried 5+ brands, breakouts continue",
    "Distrusts overly-polished beauty marketing",
    "Wants ingredient transparency"
  ],
  "decision_trigger": "Founder-led explainer video where the founder talks about their own skin journey",
  "value": "AOV $68, repeat-purchase 2.4× per year (LTV ~$220)",
  "meta_creative_angles": [
    "UGC review with visible before/after",
    "Founder-led explainer (1 min)",
    "Ingredient deep-dive carousel"
  ],
  "visual_cues": [
    "Bathroom counter setting (relatable, not aspirational)",
    "Natural lighting",
    "Real-skin texture (not retouched)"
  ]
}
```

### Field-by-field

- **`name`** — memorable, mnemonic. "Skincare Switcher Sarah" beats "Persona 1".
- **`demographics`** — coarse; from the breakdown report and the audience definitions of best-performing ad sets.
- **`primary_goal`** — what they're trying to accomplish. Phrase as the customer would say it.
- **`pain_points`** — the frustrations the product solves. Pull from converting ad copy ("tired of breakouts that won't quit") and customer reviews if you have them.
- **`decision_trigger`** — what specifically tipped them into buying. On Meta, this is often a creative angle or social-proof signal.
- **`value`** — AOV + repeat behavior + estimated LTV. Tells you how much you can spend to acquire them.
- **`meta_creative_angles`** — concrete creative approaches that work for this persona (3–5).
- **`visual_cues`** — settings, lighting, casting that resonate. Distinct from `meta_creative_angles` — angles are message; cues are visual language.

## Process

1. **Pull the data already in memory.** Top-spending campaigns + ad sets, top-converting ads with creative summaries, demographic breakdowns, audience definitions of best-performing ad sets.

2. **Cluster.** Group ads with similar angles + demographic profiles. Look for distinct cohorts — e.g. "founder-led + ingredient-detail" wins on broad audience, "UGC + before-after" wins on lookalike-purchasers. Two distinct cohorts → two distinct personas.

3. **Validate against landing pages.** Pull the landing page copy via `WebFetch`. Does the page speak to the persona's pain points and decision trigger? If yes, the persona is grounded. If no, either the persona is wrong, the page is wrong, or there's a creative-to-page mismatch worth surfacing.

4. **Write the file.** Persist to `{data_dir}/meta/personas/{accountId}.json`:

```json
{
  "account_id": "1234567890",
  "saved_at": "2026-05-01T14:00:00Z",
  "personas": [
    { ... },
    { ... }
  ]
}
```

## Drop a persona if…

- You can't name 3+ distinct converting ad creatives that speak to it (no evidence)
- The demographic profile is identical to another persona (just rename and merge — they're the same cohort with different framing)
- The user reads it and says "no, that's not us" (user knowledge > inferred persona; respect it and update)

## Avoid these failure modes

- **Marketing-deck personas.** "Aspirational Andrea, age 35, lives in a coastal city, Pinterest-obsessed, drinks oat-milk lattes" sounds great in a deck and tells you nothing about how to make a Meta ad. Always pair every persona with concrete `meta_creative_angles` that have data behind them.
- **Persona inflation.** Having 5+ personas means you're slicing demographics, not finding distinct cohorts. The test: can you describe one ad creative each persona would respond to, and one ad creative they wouldn't? If not, they're the same persona.
- **Persona over-fitting.** A persona built on one converting ad set is fragile — when that ad set fatigues, the persona evaporates. Require 3+ converging signals (creative, audience, landing page).
- **Stereotyping.** Personas based on demographics alone (age + gender + income) are stereotypes. The behavioral signal — what they bought, what creative they responded to, what page they read — is what matters.

## Update cadence

Refresh personas when:

- A new product line launches (new persona may be entering the account)
- Quarterly during business-context refresh
- When a creative concept that worked stops working (the persona may have moved on or the cohort has converted-out)

Don't refresh continuously — personas are slower-moving than ad creative. Quarterly is appropriate.
