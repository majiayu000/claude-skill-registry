---
name: detailed-product-description
description: Writes a comprehensive, feature-by-feature product description with specs and benefits that can serve as a universal prompt for downstream content generation.
---

# Detailed Product Description

This skill produces a detailed product description covering features, benefits, specs, and usage steps.

## Input Variables
- [PRODUCT_INPUTS]: name, price, overview
- [PRODUCT_BIBLE]: features, specs, materials

## The Protocol
1. Summarize the product in 1–2 sentences.
2. Document specs precisely (dimensions, weight, materials, capacity, warranty).
3. List features with function and value.
4. Describe step-by-step usage.
5. Compile summary highlighting emotional outcomes and practical value.
6. Provide JSON handoff for reuse.

## Output Instructions
Render into `templates/detailed-product-description.md`. Be explicit and complete.



## Integration & Technical Specs

### API Specification
- **ID**: `detailed-product-description`
- **Path**: `skills/detailed-product-description/templates/detailed-product-description.md`
- **Context**: Part of *Product Detailing*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `detailed-product-description.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate detailed-product-description
```
