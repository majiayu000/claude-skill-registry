---
name: product-positioning-summary
description: Generates a positioning summary using the CBBE framework (Salience, Performance, Imagery, Judgments, Feelings, Resonance) based on product, persona, and competitive context.
---

# Product Positioning Summary

This skill synthesizes market and product data to produce a clear, persuasive positioning narrative.

## Input Variables
- [PRODUCT_BIBLE]
- [PERSONA_DATA]
- [COMPETITOR_DATA]

## The Protocol
1. Salience: category, core problem, simple description.
2. Performance: points of parity, points of difference, value logic.
3. Imagery: associated brands, usage scenes, mode of use.
4. Judgments: positive beliefs, objections, credibility proof.
5. Feelings: target emotions, voice, tone.
6. Resonance: loyalty logic, mission, community connection.
7. Compile narrative and JSON handoff.

## Output Instructions
Render into `templates/product-positioning-summary.md`. Keep sections explicit for downstream use.



## Integration & Technical Specs

### API Specification
- **ID**: `product-positioning-summary`
- **Path**: `skills/product-positioning-summary/templates/product-positioning-summary.md`
- **Context**: Part of *Product Detailing*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `product-positioning-summary.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate product-positioning-summary
```
