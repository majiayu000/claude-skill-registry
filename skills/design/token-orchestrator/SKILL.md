---
name: token-orchestrator
description: Specialized logic for auditing components, detecting hardcoded values, and mapping them to the Northcote Curio design token set. Streamlines the transformation from generic CSS/Tailwind to localized, theme-aware tokens.
---

# Token Orchestrator Skill

**Role:** Automate token integration auditing and code generation for Phase 3

**Primary Use:** Audit any component, identify hardcoded values, map to tokens.json, generate transformation code

## Capabilities

- Component file parsing (TypeScript/React)
- Hardcoded value detection (colors, shapes, motion, spacing)
- Token mapping with confidence scoring
- Transformation code generation
- Compliance tracking

## Usage

Request: "Audit [component.tsx] using Token Orchestrator"

Output:

- Hardcoded values found
- Token mappings (with confidence)
- Before/after code
- Estimated implementation time

## Time Savings

- Manual audit: 15 minutes per component
- Token Orchestrator audit: 2 minutes per component
- 87% time reduction
