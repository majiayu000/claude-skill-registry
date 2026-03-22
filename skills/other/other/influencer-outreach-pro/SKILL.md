---
name: influencer-outreach-pro
description: Writes personalized DM scripts and email pitches to influencers.
---

# Influencer Outreach Pro

This skill generates high-conversion outreach messages to recruit partners and influencers.

## Input Variables
- [PRODUCT_SUMMARY]
- [PERSONA_DATA] (Where they hang out)
- [OFFER_DETAILS] (What do they get? Free product? Commission?)

## The Protocol
1.  **Targeting Strategy**: Define the "Ideal Influencer Profile" (Micro vs. Macro, specific niches).
2.  **The "Value Hook"**: Determine what's in it for them. (Exclusive access, audience relevance, money).
3.  **Channel Adaptation**:
    - **Instagram DM**: Casual, short, emoji-friendly.
    - **TikTok DM**: Very short, trend-focused.
    - **Email Pitch**: Professional, structured, media kit attached.
4.  **Follow-up Sequence**: 3-step cadence (Initial -> Bump -> Final).

## Output Instructions
Render into `templates/influencer-outreach-scripts.md`.


## Integration & Technical Specs

### API Specification
- **ID**: `influencer-outreach-pro`
- **Path**: `skills/influencer-outreach-pro/templates/influencer-outreach-scripts.md`
- **Context**: Part of *Social & Community*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `influencer-outreach-scripts.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate influencer-outreach-pro
```
