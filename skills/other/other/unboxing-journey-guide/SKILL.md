---
name: unboxing-journey-guide
description: Writes the "Welcome Card" inside the box and the QR code landing page copy.
---

# Unboxing Journey Guide

This skill ensures the customer's first physical interaction with the product builds loyalty.

## Input Variables
- [BRAND_VOICE]
- [SUPPORT_URL]

## The Protocol
1.  **The Welcome Card**:
    - **Front**: A strong brand statement or "Thank You."
    - **Back**: Simple "Get Started" steps and a QR code.
2.  **The QR Landing Page**:
    - **Video**: "How to set up your [Product]."
    - **Community Join**: Link to the Facebook Group/Discord.
    - **Upsell**: (Optional) "Get 10% off accessories."
3.  **The "Review Ask"**: Strategy for asking for a review *after* they have had a "Win."

## Output Instructions
Render into `templates/unboxing-experience.md`.


## Integration & Technical Specs

### API Specification
- **ID**: `unboxing-journey-guide`
- **Path**: `skills/unboxing-journey-guide/templates/unboxing-experience.md`
- **Context**: Part of *Product Experience*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `unboxing-experience.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate unboxing-journey-guide
```
