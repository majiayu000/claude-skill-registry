---
name: review-response-strategist
description: Generates on-brand responses to both 5-star and 1-star reviews to protect reputation.
---

# Review Response Strategist

This skill turns reviews into a marketing channel by demonstrating excellent customer service.

## Input Variables
- [REVIEW_TEXT]
- [STAR_RATING]
- [BRAND_VOICE]

## The Protocol
1.  **The 5-Star Strategy**: Reinforce the positive.
    - Thank them by name.
    - Reiterate the specific benefit they mentioned ("Glad you love the battery life!").
    - Call to action (Share with a friend).
2.  **The 1-Star Strategy (Damage Control)**:
    - **Empathize**: "I'm so sorry that happened."
    - **Own it**: No excuses.
    - **Move it offline**: "Please email me directly at [vip-email] so I can fix this."
3.  **The "Troll" Strategy**: How to handle obviously fake or malicious reviews (report vs. respond).

## Output Instructions
Render into `templates/review-response-playbook.md`.


## Integration & Technical Specs

### API Specification
- **ID**: `review-response-strategist`
- **Path**: `skills/review-response-strategist/templates/review-response-playbook.md`
- **Context**: Part of *Social & Community*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `review-response-playbook.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate review-response-strategist
```
