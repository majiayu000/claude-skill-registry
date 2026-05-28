---
name: update-strategy-sequencer
description: Writes the "Campaign Updates" to keep excitement high during the "mid-campaign slump."
---

# Update Strategy Sequencer

This skill plans and scripts the critical updates sent to backers during the 30-day campaign.

## Input Variables
- [CAMPAIGN_DURATION] (Usually 30 days)
- [FUNDING_GOAL]

## The Protocol
1.  **The "Milestone" Updates**:
    - **Funded in X Hours**: The "Thank You" post.
    - **50% Funded**: (If slow) The "We need you" rally cry.
    - **Stretch Goals**: Unlocking new colors/features.
2.  **The "Mid-Campaign" Updates** (To fight the slump):
    - **Deep Dive**: Detailed look at one feature.
    - **Production Peek**: Behind-the-scenes at the factory.
    - **Founder Story**: Personal journey.
3.  **The "Final Countdown" Updates**:
    - **48 Hours Left**: Urgency.
    - **Final Hour**: "Last chance."

## Output Instructions
Render into `templates/campaign-updates.md`.


## Integration & Technical Specs

### API Specification
- **ID**: `update-strategy-sequencer`
- **Path**: `skills/update-strategy-sequencer/templates/campaign-updates.md`
- **Context**: Part of *Strategy & Management*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `campaign-updates.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate update-strategy-sequencer
```
