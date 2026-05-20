---
name: packaging-experience-designer
description: Designs the box structure, copy on the box, and "surprise" elements for a memorable unboxing.
---

# Packaging Experience Designer

This skill architects the physical unboxing experience, turning a delivery into a brand event.

## Input Variables
- [PRODUCT_BIBLE] (Dimensions, components)
- [BRAND_BIBLE] (Voice, Tone, Visuals)

## The Protocol
1.  **Structural Design**: Determine the best box style (e.g., Magnetic rigid box, Tuck-top mailer) based on product protection and premium feel.
2.  **Exterior Aesthetics**: Design the "First Glance" appeal.
    - Top: Logo placement.
    - Sides: Value props or slogans.
    - Bottom: Necessary legal/barcode info.
3.  **The Reveal (Unboxing Flow)**:
    - What is the first thing they see? (Product or Welcome Card?)
    - How are components arranged?
4.  **Copywriting**: Write "micro-copy" for flaps, interior walls, or inserts (e.g., "Hello, Beautiful").
5.  **Surprise & Delight**: Suggest hidden elements (stickers, QR codes, easter eggs).
6.  **Material Specs**: Define paper quality (GSM), finish (Matte/Gloss/Soft-touch), and eco-friendliness.

## Output Instructions
Render into `templates/packaging-design-brief.md`.


## Integration & Technical Specs

### API Specification
- **ID**: `packaging-experience-designer`
- **Path**: `skills/packaging-experience-designer/templates/packaging-design-brief.md`
- **Context**: Part of *Product Experience*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `packaging-design-brief.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate packaging-experience-designer
```
