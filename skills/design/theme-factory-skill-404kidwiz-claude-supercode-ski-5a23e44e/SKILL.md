---
name: theme-factory
description: Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-set themes with colors/fonts that you can apply to any artifact that has been creating, or can generate a new theme on-the-fly.
---

# Theme Factory

## Purpose
Provides a toolkit for applying consistent visual themes to various artifacts including presentations, documents, reports, and web pages. Offers pre-set themes and the ability to generate custom themes with coordinated colors, typography, and styling.

## When to Use
- Applying consistent branding to presentations or documents
- Styling HTML pages with professional color schemes
- Creating custom themes from brand guidelines
- Converting plain artifacts to themed versions
- Generating color palettes for new projects
- Ensuring accessibility in color choices
- Creating dark/light mode variations
- Styling reports and data visualizations

## Quick Start
**Invoke this skill when:**
- Applying consistent branding to presentations or documents
- Styling HTML pages with professional color schemes
- Creating custom themes from brand guidelines
- Converting plain artifacts to themed versions
- Generating color palettes for new projects

**Do NOT invoke when:**
- Designing UI components from scratch → use ui-designer
- Building complete web applications → use frontend-design
- Creating visual art or graphics → use canvas-design
- Applying Anthropic brand specifically → use brand-guidelines

## Decision Framework
```
Theming Need?
├── Corporate Branding → Use brand colors + approved fonts
├── Quick Professional → Apply pre-set theme
├── Custom Theme → Generate from primary color + style
├── Accessibility → Ensure WCAG contrast ratios
├── Dark Mode → Invert with adjusted colors
└── Print-Friendly → Optimize for paper output
```

## Core Workflows

### 1. Apply Pre-set Theme
1. Select target artifact (slides, doc, HTML)
2. Choose from available pre-set themes
3. Extract current content structure
4. Apply theme colors to headings, text, backgrounds
5. Set typography (fonts, sizes, weights)
6. Adjust spacing and layout to theme
7. Verify visual consistency

### 2. Generate Custom Theme
1. Gather brand inputs (primary color, logo, guidelines)
2. Generate complementary color palette
3. Select font pairing (heading + body)
4. Define spacing scale and component styles
5. Create theme configuration file
6. Apply to target artifact
7. Iterate based on feedback

### 3. Multi-Format Theme Application
1. Define theme as abstract tokens (colors, fonts, spacing)
2. Create format-specific implementations (CSS, PPTX styles, docx styles)
3. Apply appropriate implementation per artifact type
4. Ensure visual consistency across formats
5. Document theme usage guidelines

## Best Practices
- Start with accessible color contrast ratios (WCAG AA minimum)
- Limit color palette to 3-5 colors for cohesion
- Use consistent spacing scale (4px, 8px, 16px, etc.)
- Pair fonts intentionally (contrast or complement)
- Test themes on actual content, not lorem ipsum
- Provide light and dark mode variants when possible

## Anti-Patterns
- **Too many colors** → Limit to primary, secondary, accent + neutrals
- **Ignoring contrast** → Always verify accessibility ratios
- **Inconsistent spacing** → Use defined spacing scale
- **Random font pairing** → Choose fonts with intentional relationship
- **Theme without content** → Always test with real content
