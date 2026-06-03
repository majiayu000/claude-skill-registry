---
name: conversion-audit
description: "Audit a WordPress site for conversion-rate friction across six dimensions: above-the-fold clarity, CTA hierarchy, form length, social proof placement, page speed, and trust signals. Prioritized fixes with expected impact — recommendations, not redesigns."
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: audit
---

# Conversion Audit

**Version:** 1.0.0
**Updated:** 2026-05-24
**Category:** audit
**Status:** stable
**Requires:** Respira for WordPress plugin 7.1+ + MCP server

---

## Description

Audit a WordPress site for conversion-rate friction. Reads the landing pages, the homepage, the pricing page (if any), the contact page, and any pages that are linked from the main navigation. Identifies friction points across six dimensions: above-the-fold clarity, CTA hierarchy, form length, social proof placement, page speed (using existing Respira SpeedScan), and trust signals.

This is a CRO check, not a redesign. The output is a prioritized list of fixes the user can apply — each with a one-line "what to change" + "why" + "expected impact." No rewriting; recommendations only.

---

## What it audits (the six dimensions)

1. **Above-the-fold clarity.** Does the hero answer "what is this and why does it matter to me"? Within ~5 seconds, can a first-time visitor articulate the offer back? Common failures: jargon-heavy headline, image-first instead of message-first, no concrete value proposition.

2. **CTA hierarchy.** Is there one primary CTA per screen, or are there 4 competing buttons? Are CTAs visually distinguished from the secondary navigation? Is the CTA action clear ("Get a quote" vs "Submit")?

3. **Form length.** For forms found on the page: how many required fields? Common failures: asking for phone number when email would do, asking for company size for an MVP landing page, address before there's any commitment, 8+ fields when 3 would convert.

4. **Social proof placement.** Where are testimonials / customer logos / case-study links relative to the CTA? Common failure: social proof in the footer where nobody scrolls. Strong pattern: one testimonial above the fold, customer logos below the hero, full case study links by the pricing section.

5. **Page speed.** Pulls existing SpeedScan or runs `respira_analyze_pagespeed` if available. Slow pages don't convert. LCP > 2.5s, CLS > 0.1, FID > 100ms are conversion drags.

6. **Trust signals.** Does the page show: company name / logo, contact information, privacy policy link, secure checkout indicators (if commerce), real photos vs stock, named team / founder (vs faceless)?

---

## When to Use

- Quarterly CRO review
- Before launching a paid traffic campaign — don't drive paid clicks to a leaky page
- After a redesign — verify nothing important got dropped
- When conversion drops without an obvious cause
- For a new landing page review before publish

---

## Trigger Phrases

- "audit my conversion rate"
- "cro check"
- "find conversion leaks"
- "review my landing pages"
- "audit for conversion"
- "what's hurting my conversion"
- "conversion audit"

---

## Execution Workflow

### Step 1 — Confirm site + scope

Call `respira_get_active_site`. Ask the user: *"Audit a single page, the main flow (home + pricing + contact), or all top-nav pages?"* Default to "the main flow" if unclear.

### Step 2 — Identify pages to audit

- **Single page mode:** the user names the page.
- **Main flow mode:** homepage, `/pricing/` or `/plans/` if present, `/contact/` or `/get-in-touch/` if present, plus any page marked as a landing page (`page_template == 'landing'`).
- **Top-nav mode:** call `respira_list_menus` then `respira_list_menu_items` for the primary menu; audit each linked page.

For each page, call `respira_extract_builder_content(page_id)`.

### Step 3 — Run each audit dimension

For each page, walk the builder content and score each dimension. The scoring rubric:

**Above-the-fold clarity (0–3):**
- 3: clear value prop in headline, supporting sub-headline, primary CTA, visual that supports the message
- 2: headline + CTA but value prop unclear or visual fights the message
- 1: jargon-heavy or image-first, no concrete benefit
- 0: empty hero or missing CTA entirely

**CTA hierarchy (0–3):**
- 3: one primary CTA, visually distinct, action verb, repeated below the fold
- 2: primary CTA present but competing with 2+ other equally-prominent buttons
- 1: 3+ competing CTAs or generic verbs ("Submit", "Click here")
- 0: no clear CTA

**Form length (0–3, skip if no forms):**
- 3: 1–3 required fields, no asks beyond the minimum
- 2: 4–5 required fields with one optional
- 1: 6+ required fields OR asks for phone before commitment
- 0: 8+ fields or asks for sensitive data (DOB, SSN, address) without commitment

**Social proof placement (0–3):**
- 3: one testimonial / logo bar above the fold, more below the hero, named with photo + company
- 2: testimonials present but only below the fold or unnamed
- 1: footer-only social proof
- 0: none visible

**Page speed (0–3, from SpeedScan):**
- 3: LCP < 2.5s, CLS < 0.1, page weight < 2MB
- 2: one metric mildly off
- 1: two metrics off
- 0: LCP > 4s or CLS > 0.25 (conversion killer)

**Trust signals (0–3):**
- 3: named company, contact info visible, privacy link, real photos, named team
- 2: most present, one or two missing
- 1: faceless brand, stock photos, only generic contact
- 0: anonymous, no company info, no contact, no privacy

Page total: 0–18.

### Step 4 — Output the report

```markdown
## Conversion audit for {site_url}

Pages audited: {n_pages}

### Summary

| Page | Score | Top issue |
|---|---|---|
| / | 14 / 18 | CTA hierarchy: 3 competing primary CTAs in hero |
| /pricing/ | 11 / 18 | Form length: pricing form asks for 7 fields |
| /contact/ | 10 / 18 | Above-the-fold: no value prop, only "Get in touch" |
| ... | | |

### Prioritized fixes (highest impact first)

**1. {page_url} · CTA hierarchy**
- Current: 3 competing primary buttons in hero ("Get started", "See pricing", "Book a demo")
- Change to: one primary ("Get started"), demote others to secondary text links
- Why: competing CTAs split attention and drop CTR by ~30% in typical landing page tests

**2. {page_url} · Form length**
- Current: 7 required fields including phone + company size
- Change to: 3 required (name, email, what brings you here) + optional phone
- Why: every required field beyond 3 drops form completion by ~7%

**3. {page_url} · Above-the-fold clarity**
- Current: headline "Solutions for modern teams" — generic, no concrete offer
- Change to: headline that names what the user gets ("X for Y, in Z minutes" pattern)
- Why: visitors decide within ~5 seconds whether the page is for them; vague heroes lose them

(... continue for top 5–8 fixes ...)

### What's working

(Quick callouts of strong patterns the audit found, so the user knows what NOT to change.)

- {page}: above-the-fold clarity is strong — headline + sub + supporting visual all reinforce the offer.
- {page}: social proof placement is exemplary — named testimonial above the fold with photo and company.

### Speed signals (from SpeedScan)

| Page | LCP | CLS | Total weight |
|---|---|---|---|
| / | 2.1s ✓ | 0.08 ✓ | 1.8MB ✓ |
| /pricing/ | 3.4s ✗ | 0.15 ✗ | 3.2MB ✗ |
```

### Step 5 — Offer to act on a chosen fix

Ask: *"Want me to apply one of these now? I can duplicate the page (SafeEdit) and make the change for review."*

If yes, route to the appropriate edit flow (usually `respira_create_page_duplicate` + targeted `respira_update_element`).

---

## Hard rules

- **Recommendations, not redesigns.** This skill suggests changes; it does not apply them autonomously. Every applied change is a SafeEdit-protected duplicate, reviewed before promotion.
- **Score is directional, not gospel.** Use the score to prioritize, not as a verdict. A 14/18 page with a critical CTA bug is more urgent than a 10/18 page with diffuse issues.
- **Form audits use builder-native parsing.** If the form is a Gravity Forms shortcode, parse the GF form definition (not the rendered HTML). If WPForms, ditto. If Contact Form 7, ditto. Raw HTML parsing of form fields produces wrong field counts.
- **Speed signals come from SpeedScan if present, not from re-running a fresh audit.** Re-running is slow and costly. If the SpeedScan is more than 30 days old, note that and offer to refresh.
- **Trust signal checks include checking for the privacy / terms / contact pages existing.** Use `respira_list_pages` to verify, not just visually scan the page.

---

## Telemetry

Records: site URL hash, n_pages audited, score distribution, top issue categories detected, success/failure, total duration. No page content, no recommendations, no scores per page sent.

Endpoint: `POST https://www.respira.press/api/skills/track-usage`
