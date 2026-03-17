---
name: logo-design
description: "Logo design intelligence with 55 styles, 30 color palettes, 25 industries. Generate logos with Gemini Nano Banana model, search styles/colors/industries. Actions: design, create, generate logo. Industries: tech, healthcare, finance, food, fashion, fitness. Styles: minimalist, vintage, luxury, geometric, abstract, mascot, emblem. Features: AI prompt generation, design briefs, color psychology."
license: MIT
version: 1.0.0
---

# Logo Design - AI-Powered Logo Intelligence

Comprehensive logo design system with 55+ styles, 30 color palettes, 25 industry guides. Search design guidelines and generate logos using Gemini Nano Banana models.

## When to Apply

Activate when user requests:
- Logo design or creation
- Brand identity visual elements
- Logo style recommendations
- Color palette for logos
- Industry-specific logo guidance

## Quick Reference

Read [this official docs](https://ai.google.dev/gemini-api/docs/image-generation) for latest updates.

### 1. Generate Design Brief (RECOMMENDED START)

```bash
python3 ~/.claude/skills/logo-design/scripts/search.py "tech startup modern" --design-brief -p "BrandName"
```

Returns: Industry analysis, style recommendations, color palettes.

### 2. Search Specific Domains

```bash
# Search styles
python3 ~/.claude/skills/logo-design/scripts/search.py "minimalist clean modern" --domain style

# Search color palettes
python3 ~/.claude/skills/logo-design/scripts/search.py "tech professional trust" --domain color

# Search industry guidelines
python3 ~/.claude/skills/logo-design/scripts/search.py "healthcare medical" --domain industry
```

### 3. Generate Logo with Gemini Nano Banana model 

**ALWAYS** generate output logo images with white background.

```bash
python3 ~/.claude/skills/logo-design/scripts/generate.py --brand "TechFlow" --style minimalist --industry tech
python3 ~/.claude/skills/logo-design/scripts/generate.py --prompt "coffee shop vintage badge" --style vintage
```

Options: `--style` (minimalist, vintage, luxury, etc.), `--industry` (tech, healthcare, food, etc.)

**IMPORTANT:** When scripts failed, try to fix the scripts directly.

## Available Styles

| Category | Styles |
|----------|--------|
| General | Minimalist, Wordmark, Lettermark, Pictorial Mark, Abstract Mark, Mascot, Emblem, Combination Mark |
| Aesthetic | Vintage/Retro, Art Deco, Luxury, Playful, Corporate, Organic, Neon, Grunge, Watercolor |
| Modern | Gradient, Flat Design, 3D/Isometric, Geometric, Line Art, Duotone, Motion-Ready |
| Clever | Negative Space, Monoline, Split/Fragmented, Responsive/Adaptive |

## Color Psychology Quick Guide

| Color | Psychology | Best For |
|-------|------------|----------|
| Blue | Trust, stability, professional | Finance, tech, healthcare |
| Green | Growth, natural, sustainable | Eco, wellness, organic |
| Red | Energy, passion, urgency | Food, sports, entertainment |
| Gold | Luxury, premium, prestige | Fashion, jewelry, hotels |
| Purple | Creative, innovative, premium | Beauty, creative, tech |

## Industry Defaults

| Industry | Style | Colors | Typography |
|----------|-------|--------|------------|
| Tech | Minimalist, Abstract | Blues, purples, gradients | Geometric sans |
| Healthcare | Professional, Line Art | Blues, greens, teals | Clean sans |
| Finance | Corporate, Emblem | Navy, gold | Serif or clean sans |
| Food | Vintage Badge, Mascot | Warm reds, oranges | Friendly, script |
| Fashion | Wordmark, Luxury | Black, gold, white | Elegant serif |

## Workflow Example

**User:** "Create a logo for a sustainable coffee brand called GreenBean"

1. Generate design brief:
```bash
python3 ~/.claude/skills/logo-design/scripts/search.py "coffee organic eco sustainable" --design-brief -p "GreenBean"
```

2. Generate logo variations:
**ALWAYS** generate output logo images with white background.

```bash
python3 ~/.claude/skills/logo-design/scripts/generate.py --brand "GreenBean" --style vintage --industry eco
python3 ~/.claude/skills/logo-design/scripts/generate.py --brand "GreenBean" --style organic --industry food
```

1. **[FINAL STEP - REQUIRED]** Ask user about HTML preview:

After logo generation completes, **ALWAYS** use the `AskUserQuestion` tool to ask if the user wants to preview all generated logos in a single eye-catching HTML file.

**AskUserQuestion parameters:**
```json
{
  "questions": [{
    "question": "Would you like me to create an HTML preview page for all generated logos?",
    "header": "Preview",
    "options": [
      {
        "label": "Yes, create preview (Recommended)",
        "description": "Generate a beautiful HTML gallery matching brand colors, showing all logo variants with download links"
      },
      {
        "label": "No, skip preview",
        "description": "I'll review the files directly in the output folder"
      }
    ],
    "multiSelect": false
  }]
}
```

If user selects **Yes**, invoke /ui-ux-pro-max skill to create an HTML file in the output directory with:
- Brand-matching color scheme (extract from design brief or brand guidelines)
- Dark/light mode toggle
- Grid layout showcasing all logo variants
- Hover effects to enlarge logos
- Download buttons for each logo
- Responsive design for mobile viewing
- Brand name as page title

**IMPORTANT:** If there are multiple variants generated, lay them out side by side for better comparision.

## References

- `references/style-guide.md` - Detailed style descriptions and use cases
- `references/color-psychology.md` - Color meanings and combinations
- `references/industry-best-practices.md` - Industry-specific guidelines
- `references/prompt-engineering.md` - AI image generation prompts

## Setup

```bash
export GEMINI_API_KEY="your-key"  # Get from https://aistudio.google.com/apikey
pip install google-genai
```
