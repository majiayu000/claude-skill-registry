---
name: logo-concept-architect
description: Generates deep visual prompts for Midjourney/DALL-E to create logo vectors.
---

# Logo Concept Architect

This skill translates brand essence into precise AI image generation prompts for logo creation.

## Input Variables
- [BRAND_NAME]
- [MDS] (Messaging Direction Summary)
- [VISUAL_KEYWORDS] (from Visual Identity Strategy if available)

## The Protocol
1.  **Symbol Identification**: Brainstorm physical objects or abstract shapes that represent the brand values.
2.  **Style Definition**: Choose 5 distinct styles (e.g., Minimalist, Vintage, Abstract, Mascot, Lettermark).
3.  **Prompt Engineering**: Construct detailed prompts for Midjourney/DALL-E.
    - Include technical terms: "Vector", "Flat design", "Adobe Illustrator", "White background".
    - Exclude unwanted elements: "--no shading, realistic photo, complex details".
4.  **Color Integration**: Suggest prompts with and without brand colors (monochrome is better for shape validation).

## Output Instructions
Render into `templates/logo-prompts.md`. Provide 5 distinct concepts with corresponding prompts.


## Integration & Technical Specs

### API Specification
- **ID**: `logo-concept-architect`
- **Path**: `skills/logo-concept-architect/templates/logo-prompts.md`
- **Context**: Part of *Brand Identity*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `logo-prompts.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate logo-concept-architect
```
