---
name: campaign-page-builder
description: The "Master Assembler" that maps copy, visuals, and video into the Kickstarter/Indiegogo HTML structure.
---

# Campaign Page Builder

This skill assembles all previous assets into the final campaign page layout.

## Input Variables
- [CAMPAIGN_COPY] (from campaign-page-copy)
- [VISUAL_ASSETS] (from visual-identity-core / logo-concept-architect)
- [VIDEO_SCRIPT] (from campaign-video-script)

## The Protocol
1.  **Section Mapping**: Define the order of the page sections (Standard High-Conversion Flow).
    - Header (Video + Hook)
    - Social Proof (Press logos)
    - Problem/Solution (The "Why")
    - Product Showcase (The "What" - GIFs/Images)
    - Technical Specs
    - Rewards/Pricing
    - Timeline & Team
    - Risks & FAQ
2.  **Asset Allocation**: Assign specific images/GIFs to each text block.
3.  **HTML Structure**: (Conceptual) Define the header tags (H1, H2) and image placement for the platform editor.

## Output Instructions
Render into `templates/campaign-page-layout.md`.


## Integration & Technical Specs

### API Specification
- **ID**: `campaign-page-builder`
- **Path**: `skills/campaign-page-builder/templates/campaign-page-layout.md`
- **Context**: Part of *Strategy & Management*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `campaign-page-layout.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate campaign-page-builder
```
