---
name: ui-design-system
description: Use when creating or maintaining UI design systems, design tokens, component documentation, responsive calculations, quality checks, or design-dev handoff materials.
---

# UI Design System Toolkit

Professional toolkit for creating and maintaining scalable design systems.

## Core Capabilities
- Design token generation (colors, typography, spacing)
- Component system architecture
- Responsive design calculations
- Accessibility compliance
- Developer handoff documentation

## Key Scripts

### design_token_generator.py
Generates complete design system tokens from brand colors.

**Usage**: `python scripts/design_token_generator.py [brand_color] [style] [format]`
- Styles: modern, classic, playful
- Formats: json, css, scss

**Features**:
- Complete color palette generation
- Modular typography scale
- 8pt spacing grid system
- Shadow and animation tokens
- Responsive breakpoints
- Multiple export formats

## Verification

Before reporting completion, validate generated tokens or handoff artifacts against the requested brand color, output format, accessibility constraints, and the target implementation surface. For script usage, run the command with representative input and inspect the emitted JSON/CSS/SCSS for valid syntax and preserved brand values.
