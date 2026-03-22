---
name: community-manager-brain
description: Generates scripts for Discord/Facebook Group engagement and daily discussion prompts.
---

# Community Manager Brain

This skill keeps the community active and engaged during the campaign.

## Input Variables
- [BRAND_VOICE]
- [CAMPAIGN_STATUS] (Pre-launch, Live, Post-campaign)

## The Protocol
1.  **Platform Choice**: Discord (Real-time, heavy users) vs. Facebook Group (Asynchronous, older demo).
2.  **Engagement Cadence**:
    - **Welcome**: Automated welcome message for new joiners.
    - **Daily Discussion**: A "Question of the Day" to spark debate.
    - **Challenge**: A mini-contest (e.g., "Share your worst [Problem] story").
3.  **Moderation Guidelines**: How to handle FUD (Fear, Uncertainty, Doubt) or spam.

## Output Instructions
Render into `templates/community-engagement-plan.md`.


## Integration & Technical Specs

### API Specification
- **ID**: `community-manager-brain`
- **Path**: `skills/community-manager-brain/templates/community-engagement-plan.md`
- **Context**: Part of *Social & Community*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `community-engagement-plan.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate community-manager-brain
```
