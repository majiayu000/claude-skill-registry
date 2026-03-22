---
name: campaign-page-copy
description: Generates full campaign page content structured for Kickstarter/Indiegogo using positioning, product, and voice assets.
---

# Campaign Page Copy

This skill composes the complete campaign page narrative and structure optimized for crowdfunding conversion.

## Input Variables
- [BRAND_BIBLE]
- [PRODUCT_BIBLE]
- [COMPETITOR_DATA]
- [PERSONA_DATA]

## The Protocol
1. Above-the-fold: qualifier, headline, subhead, trust anchors, hero image spec.
2. Old World: problem agitation and failed alternatives.
3. New World: mechanism reveal, feature stacking, technical deep dive, ecosystem.
4. Social Proof: media mentions, testimonials, endorsements, user count, UGC plan.
5. Risk Reversal: FAQ matrix, warranty, shipping clarity, privacy.
6. Final Offer: stack, price anchor, scarcity, final CTA, PS loop.
7. Structure sections for platform templates.

## Output Instructions
Render into `templates/campaign-page-copy.md`. Preserve section headers for easy page assembly.



## Integration & Technical Specs

### API Specification
- **ID**: `campaign-page-copy`
- **Path**: `skills/campaign-page-copy/templates/campaign-page-copy.md`
- **Context**: Part of *Crafting Compelling Copy*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `campaign-page-copy.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate campaign-page-copy
```
