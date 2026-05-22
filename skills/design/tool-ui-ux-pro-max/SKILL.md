---
name: tool-ui-ux-pro-max
description: "Use when you need concrete UI/UX inputs (palette, typography, landing patterns, UX/a11y constraints) to drive design or review. Searchable UI/UX design intelligence (styles, palettes, typography, landing patterns, charts, UX/a11y guidelines + stack best practices) backed by CSV + a Python search script. Triggers: UIUX/uiux, UI/UX, UX design, UI design, design system, design spec, color palette, typography, layout, animation, accessibility/a11y, component styling. Actions: search, recommend, review, improve UI."
---

# Tool: UI/UX Pro Max (Searchable Design Intelligence)

This is a **lookup tool**, not a page generator.

Use it to quickly retrieve concrete inputs (palette tokens, typography pairings, UX constraints, stack-specific implementation notes) that can be synthesized into:
- `design-system.md`
- a UI refactor plan / acceptance criteria
- review checklists for “looks good but feels broken” issues

## Prerequisites

Ensure Python is available:

```bash
python3 --version || python --version
```

## Core command

Domain search:

```bash
python3 ~/.claude/skills/tool-ui-ux-pro-max/scripts/search.py "<query>" --domain <domain> [-n <max_results>]
```

Stack search:

```bash
python3 ~/.claude/skills/tool-ui-ux-pro-max/scripts/search.py "<query>" --stack <stack> [-n <max_results>]
```

Available stacks:
`html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`

## Recommended workflow

When asked to design / improve UI, do this:

1) Identify these inputs:
- **Product type**: SaaS / e-commerce / content / tool / dashboard / landing
- **Tone keywords**: minimal / premium / playful / warm / corporate / technical / bold
- **Industry**: healthcare / fintech / education / consumer / …
- **Stack**: React / Next.js / … (default to `html-tailwind` if unspecified)

2) Search domains (pick 1–3 results per domain, then synthesize):
1. `product` — product type → style direction
2. `style` — style details (color/shape/motion/complexity)
3. `typography` — heading/body pairing (includes Google Fonts + CSS import)
4. `color` — palette tokens (primary/secondary/CTA/background/text/border)
5. `landing` — landing structure (section order + CTA placement)
6. `chart` — chart recommendations (dashboards)
7. `ux` — UX + a11y rules and anti-patterns

3) Search by stack to ground decisions in implementation constraints:

```bash
python3 ~/.claude/skills/tool-ui-ux-pro-max/scripts/search.py "responsive layout" --stack nextjs
```

## Domain reference

| Domain | Use for | Example keywords |
|--------|---------|------------------|
| `product` | Style direction by product type | saas, ecommerce, portfolio, healthcare |
| `style` | UI style concepts & implementation hints | minimalism, brutalism, glassmorphism |
| `typography` | Font pairings + import instructions | elegant, playful, professional |
| `color` | Palette tokens (Hex) | saas, ecommerce, fintech |
| `landing` | Landing structure & CTA strategy | hero, testimonial, pricing |
| `chart` | Chart type selection | trend, comparison, funnel |
| `ux` | UX/a11y rules & anti-patterns | accessibility, animation, navigation |
| `prompt` | Prompt / technical keywords | (style name) |

## Example (beauty / wellness landing)

```bash
python3 ~/.claude/skills/tool-ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --domain product
python3 ~/.claude/skills/tool-ui-ux-pro-max/scripts/search.py "elegant minimal soft" --domain style
python3 ~/.claude/skills/tool-ui-ux-pro-max/scripts/search.py "elegant luxury" --domain typography
python3 ~/.claude/skills/tool-ui-ux-pro-max/scripts/search.py "beauty spa wellness" --domain color
python3 ~/.claude/skills/tool-ui-ux-pro-max/scripts/search.py "hero-centric social-proof" --domain landing
python3 ~/.claude/skills/tool-ui-ux-pro-max/scripts/search.py "accessibility" --domain ux
python3 ~/.claude/skills/tool-ui-ux-pro-max/scripts/search.py "animation" --domain ux
python3 ~/.claude/skills/tool-ui-ux-pro-max/scripts/search.py "responsive layout" --stack html-tailwind
```

Then: turn **palette + typography + motion constraints + component rules** into `design-system.md`, and convert the checklist below into acceptance criteria.

## Common professional UI rules (quick scan)

### Icons & visuals

| Rule | Do | Don’t |
|------|----|------|
| No emoji icons | Use a consistent SVG icon set (Heroicons/Lucide/Simple Icons) | Mix emoji/icons randomly |
| Stable hover states | Use color/opacity/shadow transitions | Use transforms that cause layout shift |
| Correct brand logos | Use official SVG sources | Guess logos or use inconsistent variants |
| Consistent sizing | Normalize icon sizing (e.g., 24×24) | Mix different viewBox/sizes |

### Interaction

| Rule | Do | Don’t |
|------|----|------|
| Pointer cursor | Add `cursor-pointer` to clickable surfaces | Leave clickable surfaces without affordance |
| Clear feedback | Change border/shadow/color on hover | Make hover states indistinguishable |
| Reasonable transitions | 150–300ms, consistent | Instant changes or sluggish >500ms |

### Layout

| Rule | Do | Don’t |
|------|----|------|
| Spacing from edges | Leave room for floating navs | Stick UI to viewport edges |
| Avoid hidden content | Account for fixed headers | Let content sit behind fixed bars |
| Consistent containers | Keep one container width system | Use multiple container widths randomly |

## Pre-delivery checklist (use as acceptance criteria)

### Visual quality
- [ ] No emoji used as UI icons
- [ ] Icons are from a consistent icon set
- [ ] Brand logos are correct (not guessed)
- [ ] Hover states do not cause layout shift
- [ ] Color usage follows a token system (avoid scattered raw hex values)

### Interaction
- [ ] All clickable surfaces have `cursor-pointer`
- [ ] Hover/focus states provide clear feedback
- [ ] Transitions are consistent (150–300ms)
- [ ] Keyboard focus is visible

### Layout & responsive
- [ ] Works at 320px / 768px / 1024px / 1440px
- [ ] No horizontal scroll on mobile
- [ ] Fixed elements do not cover content

### Accessibility (a11y)
- [ ] Images have alt text
- [ ] Form inputs have labels
- [ ] Color is not the only indicator
- [ ] Respects `prefers-reduced-motion`
