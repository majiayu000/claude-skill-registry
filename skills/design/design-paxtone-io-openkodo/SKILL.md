---
name: design
description: >
  Premium frontend design skill that creates distinctive, accessible, production-grade interfaces with
  exceptional UX. Use when building UI components, pages, applications, or when styling/beautifying any
  web or mobile UI. Generates creative, polished code that balances best practices with distinctive
  aesthetics that surprise and delight. Supports design research via Dribbble, Behance, 21st.dev for
  inspiration. Enforces WCAG AAA accessibility, color psychology, and premium design feel. Includes
  Challenge Mode to validate user design choices against Design Bible principles.
---

# /kodo design

Premium frontend design skill for creating distinctive, accessible, production-grade interfaces.

## Philosophy

### The Jony Ive Approach

> "Reduce to the essential, then refine the essential."

Every design decision must pass through this filter:
1. **Is this element essential?** If not, remove it.
2. **Is this the simplest form?** If not, simplify it.
3. **Does this serve the user?** If not, reconsider it.

### Core Tenets

| Principle | Description |
|-----------|-------------|
| **Simplicity** | Remove until it breaks, then add back one thing |
| **Intentionality** | Every pixel has a purpose |
| **Consistency** | Same problem = same solution |
| **Hierarchy** | Guide the eye, don't compete for attention |
| **Restraint** | Elegance comes from what you leave out |

### Both/And, Not Either/Or

- Best practices AND creative distinction
- WCAG AAA accessibility AND visual delight
- Consistency AND memorable uniqueness
- Premium feel AND usability

This skill rejects the false choice between "generic but accessible" and "creative but inaccessible."
Every design should be both bulletproof AND beautiful.

---

## Challenge Mode

**CRITICAL**: This skill actively challenges user design choices against Design Bible principles.

### How Challenge Mode Works

When users propose or implement design choices, the plugin:

1. **Analyzes** the choice against Bible principles
2. **Identifies** any violations or concerns
3. **Challenges** the user with specific feedback
4. **Offers** Bible-recommended alternatives
5. **Requires explicit confirmation** to override

### Challenge Triggers

The plugin challenges when detecting:

| Violation | What's Detected | Bible Standard |
|-----------|-----------------|----------------|
| Pure colors | `#000000` or `#FFFFFF` used | Use `#F7F6F4` / `#1A1A1A` |
| Wrong ratio | Not 80/10/10 color distribution | 80% neutral, 10% brand, 10% feedback |
| High saturation | Colors at 100% saturation | Max 70-85% saturation |
| Low contrast | Below 7:1 for text | WCAG AAA (7:1) target |
| Bad sizing | Components off-scale | Bible component specs |
| Typography issues | Wrong hierarchy or line length | 45-75 char lines, defined scale |
| Animation problems | Decorative or long animations | Purposeful, 150-400ms max |
| Dark mode inversion | Colors inverted not parallel | Parallel design approach |

### Challenge Prompt Format

```
+======================================================================+
|  DESIGN BIBLE CHALLENGE                                              |
+======================================================================+
|  Issue: [Specific violation detected]                                |
|                                                                       |
|  Your choice: [What user selected]                                   |
|  Bible recommendation: [What the Bible suggests]                     |
|  Reason: [Why this matters for UX/accessibility]                     |
|                                                                       |
|  Options:                                                            |
|  1. Apply Bible recommendation                                       |
|  2. Modify my choice                                                 |
|  3. Override - I'm certain (requires confirmation)                   |
+======================================================================+
```

### User Override Protocol

To override a Bible recommendation, user must explicitly state:

> "I am definitive and sure I want to ignore plugin recommendations"

**Without this exact confirmation, proceed with Bible recommendation.**

Overrides are captured using `kodo reflect` for future reference.

---

## Commands

| Command | Purpose |
|---------|---------|
| `/kodo design [component/page]` | Design a specific component or page |
| `/kodo design-system` | Create or update project design foundation |
| `/kodo design-audit` | Audit existing UI for consistency, accessibility, UX |
| `/kodo design-theme [palette]` | Audit provided color theme for accessibility issues |
| `/kodo design-inspire [query]` | Research design inspiration before implementation |

---

## Workflow Overview

1. **Check context** -> Load existing design system from `.kodo/context/`
2. **Check/establish theme** -> Use existing theme or help user choose/create one
3. **Research (optional)** -> Find inspiration on Dribbble, Behance, 21st.dev
4. **Establish foundation** -> Define or verify design tokens, typography, colors
5. **Design with intention** -> Create distinctive yet accessible UI
6. **Capture learnings** -> `kodo reflect` to persist successful patterns

---

## Color Theme Workflow

**ALWAYS check for existing theme first:**

1. Look for theme in `.kodo/context/` for existing color definitions
2. Check `./docs/rules/design-system.md` if exists
3. If no theme exists, ASK the user:
   - "Do you have an existing color theme/palette you'd like to use?"
   - "Or should I use one of the predefined accessible palettes?"

**If user provides a theme:**
- Run `/kodo design-theme` automatically
- Analyze all colors for WCAG contrast compliance
- Check color blindness safety
- Report issues and recommend corrections
- Only proceed after user confirms corrected palette

---

## /kodo design-theme Workflow

When auditing a user-provided color theme:

### 1. Extract Colors
Parse all provided colors (hex, rgb, hsl, oklch)

### 2. Contrast Analysis
Test every text/background combination:

| Combination | Required Ratio | Status |
|-------------|----------------|--------|
| Primary on Background | 4.5:1 | PASS/FAIL |
| Text on Primary | 4.5:1 | PASS/FAIL |
| Secondary on Background | 4.5:1 | PASS/FAIL |
| Muted text on Background | 4.5:1 | PASS/FAIL |

### 3. Color Blindness Simulation
Test palette visibility for:
- Protanopia (red-green, ~1% of men)
- Deuteranopia (red-green, ~6% of men)
- Tritanopia (blue-yellow, rare)

### 4. Report Format

```markdown
## Theme Audit Report

### PASS Passing
- Primary/background: 5.2:1 (AA compliant)
- Text/background: 12.1:1 (AAA compliant)

### FAIL Failing
- Muted text/background: 2.8:1 (needs 4.5:1)
  **Recommendation**: Darken muted from oklch(65% ...) to oklch(55% ...)

- Warning/background: 2.1:1 (needs 3:1 for UI elements)
  **Recommendation**: Use oklch(60% 0.18 75) instead

### Warning: Color Blindness Concerns
- Primary and Error appear similar in deuteranopia
  **Recommendation**: Shift error hue from 25 to 15, or add icon indicators

### Corrected Palette
[Provide corrected values]
```

---

## /kodo design Workflow

### 1. Context Gathering

Before coding, understand:
- **Existing patterns**: Use `kodo query "ui components"` or `kodo query "design system"`
- **Feature context**: Check documentation for state requirements
- **Tech stack**: Identify frameworks and libraries in use

### 2. Aesthetic Direction

Commit to a BOLD direction. Choose from:

| Direction | Character | Best For |
|-----------|-----------|----------|
| **Refined Minimal** | Clean, spacious, precise | SaaS, productivity, B2B |
| **Warm Organic** | Soft edges, natural colors, flowing | Wellness, lifestyle, community |
| **Bold Editorial** | Strong typography, magazine-feel | Content, media, portfolios |
| **Luxury Premium** | Rich colors, elegant typography, subtle animations | High-end products, finance |
| **Playful Delightful** | Micro-animations, surprises, personality | Consumer apps, games, creative |
| **Technical Precision** | Data-dense, functional, efficient | Dashboards, dev tools, analytics |

**Key insight**: Elegance comes from executing the vision well, not from intensity.

### 3. Implementation Standards

**Typography:**
- Use distinctive fonts from project config
- Pair display font with body font intentionally
- Line height: 1.5x for body, tighter for headings
- 45-75 characters per line for optimal readability
- Minimum 14-16px body text

**Color (80/10/10 Rule - Non-negotiable):**
- **80% Neutrals**: Backgrounds, cards, containers, body text
- **10% Brand Accent**: Primary buttons, links, highlights
- **10% Feedback**: Success, warning, error, info states
- Use OKLCH color space for perceptually uniform colors
- **Never pure black/white**: Use `#F7F6F4` (light) / `#1A1A1A` (dark)
- **Saturation cap**: 70-85% max, never 100%
- WCAG AAA target (7:1 text contrast)
- Never rely on color alone - add icons, patterns, text

**Motion (Bible Timing Standards):**
- **Micro interactions**: 150-200ms (hovers, toggles, focus)
- **State changes**: 250-300ms (accordions, tabs, modals)
- **Page transitions**: 300-400ms (route changes)
- Every animation must serve UX, not decoration
- Use only `transform` and `opacity` (GPU-accelerated)
- **Always** respect `prefers-reduced-motion`

**Spacing:**
- Use consistent spacing scale (4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px)
- Generous whitespace > cramped layouts
- Visual grouping through proximity

**Accessibility (Non-negotiable - AAA Target):**
- **Contrast**: WCAG AAA (7:1) for text, 4.5:1 for large text, 3:1 for UI
- Focus states visible and styled (3:1 contrast minimum)
- Touch targets minimum 44x44px
- Keyboard navigation works completely
- Screen reader friendly (semantic HTML, ARIA when needed)
- Responsive at 200% zoom
- Always honor `prefers-reduced-motion`

### 4. Output Format

Generate code using modern tech stack:
- React 19+ components with TypeScript 5.7+
- Tailwind CSS 4+ with design tokens
- Framer Motion for animations
- shadcn/ui components when appropriate

---

## /kodo design-system Workflow

Create or update the design foundation in `./docs/rules/design-system.md`.

See `references/design-system-template.md` for the complete template.

---

## /kodo design-inspire Workflow

Research design inspiration before implementing:

1. **Use 21st.dev MCP** (if available):
   - Search for component inspiration
   - Find high-quality implementations
   - Get code snippets

2. **Web search** for:
   - Dribbble: `site:dribbble.com {query} ui design`
   - Behance: `site:behance.net {query} web design`
   - Awwwards: `site:awwwards.com {query}`

3. **Analyze and adapt**:
   - Note color palettes, typography choices
   - Identify layout patterns
   - Extract micro-interaction ideas
   - Document findings using `kodo curate`

**Never copy directly** - use as inspiration to create original work.

---

## /kodo design-audit Workflow

Audit existing UI for:

### Consistency Check
- Typography usage matches design system
- Colors within defined palette
- Spacing follows scale
- Components match patterns

### Accessibility Check
- Color contrast ratios
- Focus states present and visible
- Touch targets adequate (44x44px min)
- Semantic HTML structure
- Alt text on images

### UX Check
- Loading states defined
- Error states clear and helpful
- Empty states guide user action
- Form validation inline and clear
- Responsive behavior appropriate

---

## Responsive Breakpoints (Extended for 4K)

All designs MUST support these breakpoints:

| Breakpoint | Width | Target Devices |
|------------|-------|----------------|
| `sm` | 640px | Large phones |
| `md` | 768px | Tablets |
| `lg` | 1024px | Small laptops |
| `xl` | 1280px | Laptops |
| `2xl` | 1536px | Desktop monitors |
| `3xl` | 1920px | Full HD monitors |
| `4xl` | 2560px | QHD / 2K monitors |
| `5xl` | 3000px | 4K monitors |

### Tailwind Config Extension

```typescript
// tailwind.config.ts
export default {
  theme: {
    screens: {
      'sm': '640px',
      'md': '768px',
      'lg': '1024px',
      'xl': '1280px',
      '2xl': '1536px',
      '3xl': '1920px',
      '4xl': '2560px',
      '5xl': '3000px',
    },
  },
}
```

---

## Color Psychology Quick Reference

| Color | Evokes | Best For |
|-------|--------|----------|
| Blue | Trust, calm, professional | Finance, healthcare, B2B |
| Green | Growth, nature, success | Wellness, sustainability, confirmation |
| Purple | Luxury, creativity, wisdom | Premium, creative, spiritual |
| Orange | Energy, warmth, action | CTAs, alerts, playful brands |
| Red | Urgency, passion, importance | Sales, errors, bold statements |
| Yellow | Optimism, attention, caution | Highlights, warnings |
| Neutral | Sophistication, balance | Backgrounds, body text |
| Black | Luxury, power, elegance | Premium products, fashion |

---

## kodo Integration

Before designing, check existing patterns:
```bash
kodo query "ui components"
kodo query "color palette"
kodo query "typography"
```

After successful implementation:
```bash
kodo reflect  # Capture successful patterns as learnings
```

Add design decisions to context:
```bash
kodo curate "design-system" -c architecture
```

---

## Reference Files

- `references/design-bible-principles.md` - **Core Design Bible principles and Challenge Mode reference**
- `references/design-system-template.md` - Full design system documentation template
- `references/component-patterns.md` - Common UI patterns with accessibility
- `references/color-palettes.md` - Pre-built accessible color palettes (80/10/10 compliant)
- `references/accessibility-checklist.md` - WCAG AAA compliance checklist

---

## Quick Reference Card

```
COLOR:        80% neutral / 10% brand / 10% feedback
NEUTRALS:     #F7F6F4 (light) / #1A1A1A (dark)
SATURATION:   70-85% (never 100%)
CONTRAST:     7:1 AAA target

TYPOGRAPHY:   H1=44-56 / H2=28-32 / H3=20-24 / Body=16 / Small=14
LINE LENGTH:  45-75 characters

BUTTONS:      40-48px height / 8px radius / 16-24px padding
INPUTS:       40-48px height / 8px radius / 16px font
CARDS:        12-16px radius / 20-24px padding

ANIMATION:    Micro=150-200ms / State=250-300ms / Page=300-400ms
MOTION:       Always respect prefers-reduced-motion

DARK MODE:    Parallel design, not inversion
              Reduce saturation 10-20%
              Remove/reduce shadows

BREAKPOINTS:  sm=640 / md=768 / lg=1024 / xl=1280 / 2xl=1536
              3xl=1920 / 4xl=2560 / 5xl=3000
```
