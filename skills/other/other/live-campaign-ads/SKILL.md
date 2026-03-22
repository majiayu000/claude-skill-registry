---
name: live-campaign-ads
description: Generates live campaign ad headlines and bodies across urgency, discount, social proof, testimonial, and live-now motifs.
---

# Live Campaign Ads

This skill creates performance-focused ad copy variants tailored to crowdfunding stages.

## Input Variables
- [BRAND_BIBLE]
- [PRODUCT_BIBLE]
- [PERSONA_DATA]
- [CAMPAIGN_STATS]: funding %, backers, deadlines

## The Protocol
1. Create 5 headline families: Discount Offer, Live Now, Success Social Proof, Condensed Testimonial/PR, Ending Urgency.
2. For each family, produce 3 headline variants and 2 body variants.
3. Include dynamic tokens for funding %, deadline, perks.
4. Provide a CSV-friendly output and JSON block for ad ops.

## Output Instructions
Render into `templates/live-campaign-ads.md`. Keep lines short and punchy.



## Integration & Technical Specs

### API Specification
- **ID**: `live-campaign-ads`
- **Path**: `skills/live-campaign-ads/templates/live-campaign-ads.md`
- **Context**: Part of *Continual Interest*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `live-campaign-ads.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate live-campaign-ads
```
