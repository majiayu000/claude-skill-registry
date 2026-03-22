---
name: visual-identity-core
description: Defines the visual language of the brand, including color palette, typography, logo usage, and imagery guidelines.
---

# Visual Identity Core

This skill establishes the visual foundation of the brand, ensuring consistency across all assets.

## Input Variables
- [BRAND_NAME] (from brand-name-studio)
- [MDS] (Messaging & Direction Summary)
- [PERSONA_DATA] (Buyer Persona)
- [LOGO_CONCEPTS] (Optional: from logo-concept-architect)

## The Protocol
1.  **Visual Strategy**: Analyze the MDS and Persona to determine the visual mood (e.g., "Rugged & Reliable" vs. "Sleek & Modern").
2.  **Color Psychology**: Select a primary color, secondary color, and accent color. Explain the psychological impact of each.
3.  **Typography**: Choose a Header font (display), Body font (readability), and Accent font (personality).
4.  **Logo Guidelines**: specific rules for logo placement, clear space, and variations.
5.  **Imagery & Art Direction**: Define the style of photography (e.g., high contrast, candid, studio) and illustrations.
6.  **Graphic Elements**: Define shapes, textures, or patterns.

## Output Instructions
Render into `templates/visual-identity-guide.md`. Provide specific Hex codes for colors and font names/links (Google Fonts preferred).


## Integration & Technical Specs

### API Specification
- **ID**: `visual-identity-core`
- **Path**: `skills/visual-identity-core/templates/visual-identity-guide.md`
- **Context**: Part of *Brand Identity*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `visual-identity-guide.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate visual-identity-core
```
