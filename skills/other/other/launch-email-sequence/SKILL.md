---
name: launch-email-sequence
description: Produces the full launch week email cadence (morning, evening, day 2 extension, reason #2, reason #1, week wrap) with precise CTAs and urgency framing.
---

# Launch Email Sequence

This skill structures the launch week communications to maximize early conversions, reinforce social proof, and maintain momentum.

## Input Variables
- [BRAND_BIBLE]
- [PRODUCT_BIBLE]
- [PERSONA_DATA]
- [PERKS]: VIP discount, limits, timing

## The Protocol
1. Launch Morning: VIP-first announcement with strongest CTA.
2. Launch Evening: Urgency and remaining slots.
3. Day 2: Extension notice and fairness rationale.
4. Day 3: Reason #2 with benefit proof.
5. Day 5: Reason #1 with press quotes.
6. Day 7: Week wrap with progress and benefits recap.
7. Provide JSON schedule and dynamic fields for variables.

## Output Instructions
Render into `templates/launch-email-sequence.md`. Include subject variants and button text for each email.



## Integration & Technical Specs

### API Specification
- **ID**: `launch-email-sequence`
- **Path**: `skills/launch-email-sequence/templates/launch-email-sequence.md`
- **Context**: Part of *Robust Email Strategy*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `launch-email-sequence.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate launch-email-sequence
```
