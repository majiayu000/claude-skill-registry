---
name: campaign-video-script
description: Produces a high-conversion crowdfunding video script outline and copy with hook, problem, mechanism, proof, offer, CTA.
---

# Campaign Video Script

This skill scripts the campaign video with emotional narrative and logical proof aligned to platform best practices.

## Input Variables
- [BRAND_BIBLE]
- [PRODUCT_BIBLE]
- [PERSONA_DATA]

## The Protocol
1. Hook: promise, leading question, or problem statement.
2. Problem and Hero: empathic setup and founder authority.
3. Mechanism and Product Reveal.
4. How it works: step-by-step usage and science proof if applicable.
5. Feature highlights: 3–5 value-packed moments.
6. Social proof: testimonials or credible quotes.
7. Offer: perks, VIP discount, urgency.
8. CTA: clear next action.

## Output Instructions
Render the script into `templates/campaign-video-script.md` with timing notes and scene directions.



## Integration & Technical Specs

### API Specification
- **ID**: `campaign-video-script`
- **Path**: `skills/campaign-video-script/templates/campaign-video-script.md`
- **Context**: Part of *Campaign Messaging*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `campaign-video-script.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate campaign-video-script
```
