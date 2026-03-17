---
name: aico-frontend-style-extraction
description: |
  Extract design tokens (colors, typography, spacing, effects) from reference website or screenshot to create project design system.

  UNIQUE VALUE: Creates standardized design-system.md file with all design tokens extracted systematically.

  Use this skill when:
  - User shares reference website URL and wants to extract its style
  - User provides screenshot or image and asks to "extract design", "extract style"
  - Running /frontend.init and need to create design system from reference
  - User asks to "create design system", "extract colors", "extract typography"
  - Need to establish consistent design tokens before starting frontend work

  Methods: URL (via Playwright MCP screenshot) or direct screenshot analysis
  Output: ALWAYS write to docs/reference/frontend/design-system.md
---

# Style Extraction

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## Process

1. **Get reference material**:
   - URL: Use Playwright MCP to take screenshot, then analyze
   - Screenshot: Analyze directly
   - Description: Generate tokens based on style keywords
2. **Extract systematically** using the checklist below
3. **Save output**: ALWAYS write to `docs/reference/frontend/design-system.md`

## Extraction Checklist

### Colors

- [ ] Background colors (page, card, section)
- [ ] Text colors (primary, secondary, muted)
- [ ] Accent/brand colors
- [ ] Border colors
- [ ] State colors (success, warning, error)

### Typography

- [ ] Font families (headings, body, mono)
- [ ] Font sizes (scale from xs to 4xl)
- [ ] Font weights (normal, medium, semibold, bold)
- [ ] Line heights

### Spacing & Layout

- [ ] Border radius values
- [ ] Container max-width
- [ ] Section padding
- [ ] Component spacing scale

### Effects

- [ ] Shadows (sm, md, lg)
- [ ] Borders & dividers
- [ ] Transitions

## Output Template

```markdown
# Design System

## Colors

### Brand

- Primary: #xxx
- Secondary: #xxx

### Text

- Primary: #xxx
- Secondary: #xxx
- Muted: #xxx

### Background

- Page: #xxx
- Card: #xxx

## Typography

### Font Family

- Headings: "Font Name", sans-serif
- Body: "Font Name", sans-serif

### Font Size

- sm: 0.875rem
- base: 1rem
- lg: 1.125rem
- xl: 1.25rem

## Spacing

### Border Radius

- sm: 0.125rem
- md: 0.375rem
- lg: 0.5rem

## Effects

### Shadow

- sm: 0 1px 2px rgba(0,0,0,0.05)
- md: 0 4px 6px rgba(0,0,0,0.1)
```

## Playwright MCP Usage

If user provides URL:

1. `browser_navigate` to URL
2. `browser_take_screenshot` (fullPage: true)
3. Analyze screenshot for design tokens

## Key Rules

- ALWAYS extract actual hex values from reference - don't guess
- MUST note shadows, borders, transitions
- ALWAYS save to `docs/reference/frontend/design-system.md`

## Common Mistakes

- ❌ Guess colors without checking → ✅ Extract actual hex values
- ❌ Skip subtle details → ✅ Note shadows, borders, transitions
- ❌ Ignore responsive differences → ✅ Document mobile vs desktop
