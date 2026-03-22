---
name: brand-content-design
description: Use when user says "create presentation", "make slides", "make carousel", "LinkedIn carousel", "create HTML page", "make landing page", "build web page", "html design system", "design system", "setup brand", "brand init", "extract brand", "get outline", "color palette", "alternative colors", "infographic", "brand assets", "brand project". Use PROACTIVELY when user wants to create any visual content with consistent branding. MUST be invoked for branded content — routes to the correct command for presentations, carousels, infographics, and HTML pages.
version: 3.1.0
allowed-tools: Read, Glob, Grep, Write, Bash, AskUserQuestion, Skill
user-invocable: true
---

# Brand Content Design

Create branded visual content (presentations, LinkedIn carousels, HTML pages) with consistent brand identity.

## Trigger Phrases

- "create presentation" / "make slides"
- "create carousel" / "LinkedIn carousel"
- "create HTML page" / "make landing page" / "build web page"
- "html design system" / "design system"
- "setup brand" / "brand init" / "extract brand"
- "create template" / "new template"
- "get outline" / "outline for template" / "prepare content"
- "color palette" / "generate palette" / "alternative colors"
- NOT for: General design questions, non-branded content
- NOT for: Drupal conversion (use design-system-converter plugin instead)

## Project Detection

Before ANY operation, find the PROJECT_PATH using this search order:

1. **Current directory** - Check if `./brand-philosophy.md` exists
2. **Parent directory** - Check if `../brand-philosophy.md` exists
3. **Subdirectories** - Use `find . -maxdepth 2 -name "brand-philosophy.md"` to find nearby projects
4. **If multiple found** - Ask user which project to use
5. **If none found** - Direct user to run `/brand-init` first

**Once PROJECT_PATH is set**, the folder structure is:
```
{PROJECT_PATH}/
├── brand-philosophy.md          # Always exists
├── templates/
│   ├── presentations/
│   │   └── {template-name}/
│   │       ├── template.md
│   │       ├── canvas-philosophy.md
│   │       └── sample.pptx
│   ├── carousels/
│   │   └── {template-name}/
│   │       ├── template.md
│   │       ├── canvas-philosophy.md
│   │       └── sample.pdf
│   └── html/
│       └── {design-system-name}/
│           ├── canvas-philosophy.md
│           ├── design-system.md
│           └── components/      # Reusable HTML components
├── presentations/               # Output folder
├── carousels/                   # Output folder
├── html-pages/                  # Output folder (HTML pages)
└── assets/                      # Brand assets
```

**Finding templates:**
- Presentations: `find {PROJECT_PATH}/templates/presentations -name "template.md"`
- Carousels: `find {PROJECT_PATH}/templates/carousels -name "template.md"`

## Three-Layer System

Apply this layered approach when creating content:

1. **Layer 1 - Brand Philosophy** (`brand-philosophy.md` in project)
   - Load and apply visual DNA (colors, typography, imagery)
   - Load and apply verbal DNA (voice, tone, vocabulary)

2. **Layer 2 - Content Type Guide** (from plugin `references/`)
   - Read `references/presentations-guide.md` for presentations
   - Read `references/carousels-guide.md` for carousels

3. **Layer 3 - Template** (from project `templates/`)
   - Load template's `canvas-philosophy.md` for visual design rules
   - Follow template's structure for slide/card sequence

## Commands

Route user requests to the appropriate command:

| User Intent | Command |
|-------------|---------|
| Status, switch projects, or start | `/brand` |
| Initialize new project | `/brand-init` |
| Extract brand from sources | `/brand-extract` |
| Generate alternative color palettes | `/brand-palette` |
| Manage assets (logos, icons, fonts) | `/brand-assets` |
| Create presentation template | `/template-presentation` |
| Create carousel template | `/template-carousel` |
| Get outline template + AI prompt with slide/card definitions | `/outline` |
| Create presentation (guided) | `/presentation` |
| Create presentation (quick) | `/presentation-quick` |
| Create carousel (guided) | `/carousel` |
| Create carousel (quick) | `/carousel-quick` |
| Create HTML design system | `/design-html` |
| Create HTML page (guided) | `/html-page` |
| Create HTML page (quick) | `/html-page-quick` |
| Add new content type | `/content-type-new` |

## Underlying Skills

Use these skills during content generation:

| Skill | When to Use |
|-------|-------------|
| **visual-content** | Generate visual output from canvas philosophy (bundled) |
| **html-generator** | Generate HTML pages and components from design system (bundled) |
| **pptx** | Convert presentation PDFs to PowerPoint |
| **pdf** | Create multi-page carousel PDFs |

The `visual-content` skill is bundled with this plugin. For HTML-to-Drupal conversion, use the `design-system-converter` plugin.

## References

### Bundled (Plugin-Specific)
- `references/brand-philosophy-template.md` - Template for brand philosophy
- `references/template-structure.md` - Template for template.md files
- `references/canvas-philosophy-template.md` - Template for canvas philosophy
- `references/presentations-guide.md` - Presentation best practices
- `references/carousels-guide.md` - Carousel best practices
- `references/style-constraints.md` - 18 visual styles with enforcement blocks
- `references/color-palettes.md` - Color theory and palette types
- `references/output-specs.md` - Dimensions, formats, file sizes
- `references/bias-prevention.md` - Brand bias prevention checks
- `references/style-recommendation-engine.md` - Intelligent style selection by brand personality, purpose, audience
- `references/slide-composition-rules.md` - Per-slide-type focal points, layout modifiers, component frequency limits

### Online Dev-Guides (Design Systems)

For design system recognition and analysis methodology, use the dev-guides-navigator plugin:

Invoke `/dev-guides-navigator` with keywords like "design system recognition", "Bootstrap mapping", or "component analysis". The navigator handles caching and disambiguation — never fetch dev-guides URLs directly.
