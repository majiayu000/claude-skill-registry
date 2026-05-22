---
name: marketing-visual-design
description: Visual marketing asset creation for ads, social media, email, presentations, and brand collateral. Platform-specific dimensions, creative best practices, AI design tools, and conversion-focused visual hierarchy. Use when you need production-ready marketing visuals.
---

# Marketing Visual Design

Production-ready patterns for marketing visual asset creation.

**Scope**: Ad creatives, social media graphics, email visuals, presentation design, brand collateral. NOT product UI (use `software-ui-ux-design`).

**Primary specs & sources**: `data/sources.json` (official docs + curated best practices).

---

## Quick Start

1. Pick the asset type using the decision tree.
2. Capture requirements using `assets/` (brief, carousel, deck outline).
3. Produce a layout spec + copy variants + export plan (and a prompt pack if AI-generated).
4. Run QA gates (readability, brand, compliance, accessibility, specs) before handoff.

Use `software-ui-ux-design` for product UI, `marketing-cro` for experiment design, and `marketing-content-strategy` for messaging systems.

---

## Workflow

1. Confirm channel + placement (paid/organic, platform, static/video, ratio).
2. Ask intake questions (goal, audience, offer, proof, CTA, constraints, brand rules).
3. Select a creative direction (2-3 options) and lock the core message.
4. Build layout using the hierarchy rules (hook -> hero -> value -> CTA -> brand).
5. Create variants for testing (3-5); change one major variable per variant.
6. Run QA gates (specs, safe zones, readability, compliance, accessibility, export).
7. Handoff deliverables (final exports + editable source + copy + notes).

## Intake (Ask First)

- Objective: awareness, click, lead, purchase, retention
- Audience: who, what they care about, what they already know
- Offer: product, price/promo, risk reversal (trial/guarantee), deadline
- Proof: 1-2 strongest stats, testimonial, logo, rating, demo signal
- CTA: one action verb + destination (landing page, app store, form)
- Platform constraints: placement(s), ratio, file format, file size, duration
- Brand constraints: logo usage, fonts, colors, imagery rules, do/don’t list
- Compliance constraints: claims policy, regulated category, trademark usage, consent/model releases

## Decision Tree

```text
MARKETING VISUAL REQUEST
  |-- \"Ad creative\" -> references/ad-creative-specs.md
  |-- \"Social media graphic\" -> references/social-media-dimensions.md
  |-- \"Email banner\" -> references/email-visual-specs.md
  |-- \"Presentation/deck\" -> references/presentation-design.md
  |-- \"One-pager/collateral\" -> references/brand-collateral.md
  `-- \"AI-generated visual\" -> references/ai-design-tools.md
```

---

## Platform Dimensions Quick Reference

### Social Media (Static)

| Platform | Post | Story/Reel | Cover/Banner |
|----------|------|------------|--------------|
| **Instagram** | 1080x1080, 1080x1350 | 1080x1920 | N/A |
| **Facebook** | 1200x630, 1080x1080 | 1080x1920 | 820x312 |
| **LinkedIn** | 1200x1200, 1200x628 | N/A | 1584x396 |
| **TikTok** | 1080x1080 | 1080x1920 | N/A |
| **YouTube** | N/A | 1080x1920 (Shorts) | 2560x1440 |

### Ad Platforms

| Platform | Sizes | Safe Zone | Max File |
|----------|-------|-----------|----------|
| **Meta** | 1080x1080, 1080x1350 (4:5 best) | 14% from edges | 30MB/4GB |
| **Google Display** | 300x250, 728x90, 300x600 | N/A | 150KB |
| **YouTube Thumbnail** | 1280x720 | Right-bottom | 2MB |
| **TikTok Ads** | 1080x1920 | Top 130px, bottom 440px | 500MB |

For full specs and edge cases, use `references/`.

---

## Visual Hierarchy for Ads

| Element | Priority | Placement |
|---------|----------|-----------|
| **Hook/Headline** | 1 | Top 1/3 |
| **Hero Visual** | 2 | Center |
| **Value Prop** | 3 | Middle |
| **CTA** | 4 | Bottom 1/3 |
| **Logo** | 5 | Corner |

### Text Overlay Rules

| Platform | Max Text | Safe Zone |
|----------|----------|-----------|
| **Meta** | <20% recommended | 14% from edges |
| **TikTok** | Minimal | Top 130px, bottom 440px |
| **LinkedIn** | No strict limit | Headlines <2 lines |

---

## Variant Testing (Fast Defaults)

- Create 3-5 variants per concept: hook, hero visual, offer framing, CTA, proof.
- Keep one major variable per variant to attribute performance.
- Prioritize native-looking creative for social (UGC-style often wins) unless the brand requires polish.

### Carousel Structure

```text
SLIDE 1: Hook (problem or bold statement)
SLIDE 2-4: Solution/Benefits
SLIDE 5: Social proof
SLIDE 6: CTA with offer
```

### Video Structure (Hook-Retain-Convert)

| Section | Duration | Purpose |
|---------|----------|---------|
| **Hook** | 0-3s | Stop scroll |
| **Agitate** | 3-10s | Amplify pain |
| **Solution** | 10-20s | Product demo |
| **Proof** | 20-30s | Testimonials |
| **CTA** | 30-45s | Action |

---

## AI-Generated Visuals (Operational Notes)

- Use `references/ai-design-tools.md` for tool selection, prompt frameworks, and artifact avoidance.
- Prefer brand-safe workflows: licensed stock, first-party photography, or tools with clear commercial terms.
- Treat text-in-image as unreliable for exact typography; use AI for backgrounds/hero imagery, then typeset in design tools.

---

## QA Gates (Run Before Delivery)

- Specs: dimensions, aspect ratio, safe zones, duration (video), file size.
- Readability: passes thumbnail test, high contrast, minimal on-image text.
- Brand: correct logo, colors, fonts; consistent style across variants.
- Compliance: avoid prohibited claims, unlicensed trademarks, misleading before/after, missing disclosures.
- Accessibility: sufficient contrast, large-enough type, avoid text-only communication of meaning.
- Deliverables: export naming is consistent; editable source files included.

### File Formats

| Use Case | Format |
|----------|--------|
| Photos | JPEG |
| Transparency | PNG |
| Logos/icons | SVG |
| Animation | GIF/WebP |
| Print | PDF |
| Video | MP4 (H.264) |

---

## Resources

| Resource | Purpose |
|----------|---------|
| [references/ad-creative-specs.md](references/ad-creative-specs.md) | Full specs for Meta, Google, LinkedIn, TikTok |
| [references/social-media-dimensions.md](references/social-media-dimensions.md) | Complete platform dimensions |
| [references/presentation-design.md](references/presentation-design.md) | Investor deck, sales deck |
| [references/email-visual-specs.md](references/email-visual-specs.md) | Email design specs |
| [references/ai-design-tools.md](references/ai-design-tools.md) | AI prompting, workflows |
| [references/brand-collateral.md](references/brand-collateral.md) | One-pagers, case studies |
| [references/2026-creative-trends.md](references/2026-creative-trends.md) | UGC-style, sensory design, Meta algorithm |

## Templates

| Template | Purpose |
|----------|---------|
| [assets/ad-creative-brief.md](assets/ad-creative-brief.md) | Creative brief |
| [assets/social-carousel-template.md](assets/social-carousel-template.md) | Carousel structure |
| [assets/pitch-deck-outline.md](assets/pitch-deck-outline.md) | Investor deck |

## International Markets

This skill uses US/Western market defaults. For international visual design:

| Need | See Skill |
|------|-----------|
| Cultural color symbolism | [marketing-geo-localization](../marketing-geo-localization/SKILL.md) |
| Regional imagery guidelines | [marketing-geo-localization](../marketing-geo-localization/SKILL.md) |
| RTL design adaptations | [marketing-geo-localization](../marketing-geo-localization/SKILL.md) |
| Regional platform specs (WeChat, LINE) | [marketing-geo-localization](../marketing-geo-localization/SKILL.md) |

**Auto-triggers**: When your query mentions specific countries, cultural adaptation, or RTL design, both skills load automatically.

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| [marketing-cro](../marketing-cro/SKILL.md) | Landing page optimization |
| [marketing-content-strategy](../marketing-content-strategy/SKILL.md) | Brand messaging |
| [marketing-social-media](../marketing-social-media/SKILL.md) | Social strategy |
| [marketing-paid-advertising](../marketing-paid-advertising/SKILL.md) | Campaign strategy |
| [software-ui-ux-design](../software-ui-ux-design/SKILL.md) | Product UI (not marketing) |
