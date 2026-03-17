---
name: cip-design
description: "Corporate Identity Program design with 50 deliverables, 20 styles, 20 industries. Generate CIP mockups with Gemini Nano Banana (Flash/Pro). Actions: design, create, generate brand identity. Deliverables: business card, letterhead, signage, vehicle, apparel, packaging. Styles: corporate, luxury, minimal, modern."
license: MIT
version: 1.0.0
dependencies:
  - ai-multimodal  # For Gemini Nano Banana image generation
---

# CIP Design - Corporate Identity Program Intelligence

Comprehensive Corporate Identity Program (CIP) design system with 50+ deliverables, 20 design styles, 20 industry guides. Search design guidelines and generate mockups using Gemini Nano Banana (Flash/Pro) models.

> **Note:** This skill uses `ai-multimodal` skill's Gemini integration for image generation with Nano Banana models (NOT Imagen).

## When to Apply

Activate when user requests:
- Corporate identity or brand identity design
- CIP/CI deliverable mockups (business cards, letterheads, signage, etc.)
- Brand application guidelines
- Vehicle branding, office signage, uniforms
- Complete brand identity packages

## Quick Reference

### 1. Generate CIP Brief (RECOMMENDED START)

```bash
python3 ~/.claude/skills/cip-design/scripts/search.py "tech startup" --cip-brief -b "BrandName"
```

Returns: Industry analysis, style recommendations, key deliverables.

### 2. Search Specific Domains

```bash
# Search deliverables
python3 ~/.claude/skills/cip-design/scripts/search.py "business card letterhead" --domain deliverable

# Search design styles
python3 ~/.claude/skills/cip-design/scripts/search.py "luxury premium elegant" --domain style

# Search industry guidelines
python3 ~/.claude/skills/cip-design/scripts/search.py "hospitality hotel" --domain industry

# Search mockup contexts
python3 ~/.claude/skills/cip-design/scripts/search.py "office reception" --domain mockup
```

### 3. Generate CIP Mockups with Gemini Nano Banana

**RECOMMENDED: Use --logo for accurate brand mockups**

```bash
# Generate with brand logo (RECOMMENDED - uses image editing)
python3 ~/.claude/skills/cip-design/scripts/generate.py --brand "TopGroup" --logo /path/to/logo.png --deliverable "business card" --industry "consulting"

# Generate full CIP set with logo
python3 ~/.claude/skills/cip-design/scripts/generate.py --brand "TopGroup" --logo /path/to/logo.png --industry "consulting" --set

# Use Pro model for higher quality / 4K text rendering
python3 ~/.claude/skills/cip-design/scripts/generate.py --brand "TopGroup" --logo logo.png --deliverable "business card" --model pro

# Custom deliverables with aspect ratio
python3 ~/.claude/skills/cip-design/scripts/generate.py --brand "GreenLeaf" --logo logo.png --industry "organic food" --deliverables "letterhead,packaging,vehicle" --ratio 16:9

# Without logo (AI generates its own interpretation)
python3 ~/.claude/skills/cip-design/scripts/generate.py --brand "TechFlow" --deliverable "business card" --no-logo-prompt
```

**Models:**
- `flash` (default): `gemini-2.5-flash-image` - Fast, cost-effective
- `pro`: `gemini-3-pro-image-preview` - Quality, 4K text rendering

**Image Editing Mode:**
When `--logo` is provided, uses Gemini's text-and-image-to-image capability to incorporate your ACTUAL logo into mockups. Without `--logo`, AI generates its own brand interpretation.

## Deliverable Categories

| Category | Items |
|----------|-------|
| Core Identity | Logo, Logo Variations |
| Stationery | Business Card, Letterhead, Envelope, Folder, Notebook, Pen |
| Security/Access | ID Badge, Lanyard, Access Card |
| Office Environment | Reception Signage, Wayfinding, Meeting Room Signs, Wall Graphics |
| Apparel | Polo Shirt, T-Shirt, Cap, Jacket, Apron |
| Promotional | Tote Bag, Gift Box, USB Drive, Water Bottle, Mug, Umbrella |
| Vehicle | Car Sedan, Van, Truck |
| Digital | Social Media, Email Signature, PowerPoint, Document Templates |
| Product | Packaging Box, Labels, Tags, Retail Display |
| Events | Trade Show Booth, Banner Stand, Table Cover, Backdrop |

## Design Styles Quick Guide

| Style | Colors | Best For |
|-------|--------|----------|
| Corporate Minimal | Navy, White, Blue | Finance, Legal, Consulting |
| Modern Tech | Purple, Cyan, Green | Tech, Startups, SaaS |
| Luxury Premium | Black, Gold, White | Fashion, Jewelry, Hotels |
| Warm Organic | Brown, Green, Cream | Food, Organic, Artisan |
| Bold Dynamic | Red, Orange, Black | Sports, Entertainment |

## Workflow Example

**User:** "Create a complete CIP for a luxury hotel called Grand Vista"

1. Generate CIP brief:
```bash
python3 ~/.claude/skills/cip-design/scripts/search.py "luxury hospitality hotel" --cip-brief -b "Grand Vista"
```

2. Generate key deliverables with logo (RECOMMENDED):
```bash
python3 ~/.claude/skills/cip-design/scripts/generate.py --brand "Grand Vista" --logo /path/to/grandvista-logo.png --industry "hospitality" --style "luxury premium" --set
```

3. Or without logo (AI generates interpretation):
```bash
python3 ~/.claude/skills/cip-design/scripts/generate.py --brand "Grand Vista" --industry "hospitality" --style "luxury premium" --set --no-logo-prompt
```

**Note:** If no logo exists, consider using the `logo-design` skill first to generate one.

### 4. Render HTML Presentation (Final Step)

Generate a professional HTML presentation from CIP mockups with detailed descriptions, concepts, and specifications.

```bash
# Generate HTML presentation from CIP images
python3 ~/.claude/skills/cip-design/scripts/render-html.py --brand "TopGroup" --industry "consulting" --images /path/to/cip-output

# Specify custom output path
python3 ~/.claude/skills/cip-design/scripts/render-html.py --brand "TopGroup" --industry "consulting" --images ./topgroup-cip --output presentation.html
```

**HTML Presentation Features:**
- Hero section with brand name, industry, style, and mood
- Individual deliverable cards with mockup images
- Detailed descriptions: concept, purpose, specifications
- Responsive design for desktop and mobile viewing
- Dark theme professional aesthetic
- Images embedded as base64 (single-file portable)

## References

- `references/deliverable-guide.md` - Detailed deliverable specifications
- `references/style-guide.md` - Design style descriptions
- `references/prompt-engineering.md` - AI generation prompts

## Setup

```bash
export GEMINI_API_KEY="your-key"  # Get from https://aistudio.google.com/apikey
pip install google-genai pillow
```

See `ai-multimodal` skill's `references/image-generation.md` for detailed Nano Banana documentation.
