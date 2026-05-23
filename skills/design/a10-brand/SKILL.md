---
name: a10-brand
description: >
  Apply A10 Networks brand guidelines to any frontend output — React/JSX artifacts, HTML pages,
  dashboards, PDFs, infographics, charts, presentations, and documentation. Use this skill whenever
  creating or reviewing visual content for A10 Networks, Signal Horizon, Synapse, ThreatX Labs,
  The Crows, or any A10-related product. Also trigger when the user mentions A10 brand colors,
  Rubik font, square corners, or asks to make something "on-brand" for A10. This includes
  reviewing existing work against brand guidelines. If you are building any visual artifact and
  the context suggests it is for A10 Networks, use this skill even if the user doesn't explicitly
  ask for brand compliance.
---

# A10 Networks Brand Skill

This skill ensures every visual output for A10 Networks looks like it belongs to the same family —
whether it's a React dashboard, an HTML landing page, a PDF report, or a data visualization.

The goal is not robotic compliance with a checklist. The goal is to internalize the brand's
personality — **confident, bold, clean, engineered** — and express it naturally across every medium.

## Brand Spirit

A10's visual identity communicates: "We are serious engineers who build elegant solutions."

**The feeling**: Precision without coldness. Confidence without arrogance. Technical depth
presented with clarity. Think: the cockpit of a fighter jet — every element has purpose, nothing
is decorative for its own sake, but the overall effect is striking.

**Design principles**:
- **Bold, not busy** — Strong visual hierarchy. One focal point per section. Generous whitespace.
- **Diagonal energy** — A10's signature is the diagonal split (white/navy). Use clip-paths and
  angled dividers to create dynamism without chaos.
- **Sharp edges** — Square corners on EVERYTHING. Buttons, cards, inputs, images, badges. This is
  the single most recognizable A10 brand element. `border-radius: 0` is law.
- **Engineered typography** — Rubik Light (300) for headlines creates an elegant, modern feel.
  Headlines should feel lightweight and spacious, not heavy and shouty.
- **Purposeful color** — Blues dominate. Magenta punctuates. Accents inform. Every color choice
  should have a reason.

---

## Critical Rules (Non-Negotiable)

These are the rules that, if violated, make something instantly "not A10":

1. **Square corners everywhere** — `border-radius: 0` on buttons, cards, inputs, badges, images,
   modals, tooltips, everything. No exceptions. No "just a little rounding." Zero.

2. **Rubik font family** — Load from Google Fonts. Fallback to Calibri for Office contexts.
   ```html
   <link href="https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap" rel="stylesheet">
   ```

3. **Headline weight is Light (300)** — This is counterintuitive and the #1 mistake. H1-H4 use
   Rubik Light 300, NOT bold. Bold headlines are off-brand. Medium (500) for H5-H6 and buttons.

4. **On-brand colors only** — Use the brand palette. Off-brand colors are not forbidden but should
   be rare and justified. When in doubt, use A10 Blue `#0057B7`.

5. **Logo in approved colors only** — A10 Blue, Navy, White, or Black. Never magenta, never on
   accent backgrounds, never with effects.

6. **WCAG 2.1 AA contrast** — 4.5:1 minimum for text. No light-on-light or dark-on-dark.

---

## Color System

### Proportions (This Is the Key)

Think of color usage like a pyramid. The visual weight should roughly follow:

```
PRIMARY (dominant ~80% of all color)
├── Navy Blue    #001E62  — 35% — Dark backgrounds, headers, primary text on light
├── A10 Blue     #0057B7  — 25% — CTAs, links, primary brand moments
└── White        #FFFFFF  — 20% — Light backgrounds, text on dark

SECONDARY (supporting ~15%)
├── Sky Blue     #529EEC  — Dark-theme links, secondary accents, lighter chart elements
├── Magenta      #D62598  — THE dramatic accent. Badges, highlight CTAs, key moments. Sparingly.
└── Black        #000000  — Dark backgrounds, body text alternative

ACCENT (data & status only ~5%)
├── Purple       #440099  — Charts, illustrations
├── Cloud Blue   #5E8AB4  — Charts, alternative to gray
├── Orange       #E35205  — Warnings, emphasis, data viz
├── Green        #00B140  — Success states, positive KPIs
└── Red          #EF3340  — Error states, negative KPIs, danger
```

**Accent color rules**: Purple, Cloud Blue, Orange, Green, and Red are reserved for functional
use — data visualization series, status badges, KPI values, table cell highlights, alert states.
They should NOT be used for backgrounds, large UI areas, or decorative elements.

**Magenta rules**: Magenta is the "spice." Use it for one or two high-impact moments per page —
a primary CTA button, a featured badge, a key metric highlight. Never as a background color.
Never dominant. If you squint at the page and magenta is the first thing you see everywhere,
you've used too much.

### Full Palette Reference

For the complete palette with tints, shades, UI neutrals, hover states, and CSS custom properties,
read `references/color-system.md`.

---

## Typography

| Element | Size | Weight | Notes |
|---------|------|--------|-------|
| Eyebrow | 16px | Bold 700 | ALL-CAPS, letter-spacing: 0.1em. Only place for caps. |
| H1 | 48px / 3rem | Light 300 | |
| H2 | 32px / 2rem | Light 300 | |
| H3 | 28px / 1.75rem | Light 300 | |
| H4 | 24px / 1.5rem | Light 300 | |
| H5 | 20px / 1.25rem | Medium 500 | |
| H6 | 16px / 1rem | Medium 500 | |
| Body | 16px / 1rem | Regular 400 | Line-height: 24px |
| Small | 14px | Regular 400 | |
| Buttons | per size | Medium 500 | Title Case labels |
| Links | 16px | SemiBold 600 | |

**Rules**: Ragged-right alignment (never justified). No hyphenation. No ALL-CAPS except
eyebrows and small labels. Keep "A10 Networks" on the same line (use `white-space: nowrap`
on brand names).

---

## Themes

### When to Use Which

- **Light theme** — Corporate marketing, external-facing content, documentation, landing pages,
  white papers, blog posts
- **Dark theme** — Product UI, dashboards, security tools, demos, internal platform interfaces,
  anything for Signal Horizon / Synapse / ThreatX Labs / The Crows

If context doesn't make it obvious, **default to light for documents/marketing, dark for
product/technical UI.**

### Light Theme

| Layer | Color | Usage |
|-------|-------|-------|
| Base background | `#FFFFFF` | Page background |
| Section background | `#F0F4F8` | Alternating sections |
| Card background | `#DFE8F0` | Cards, subtle containers |
| Primary text | `#001E62` (Navy) | Headlines, body |
| Secondary text | `#404040` | Supporting text |
| Links | `#0057B7` → hover `#003EC8` | |
| Primary button | `#0057B7` → hover `#004189` | White text |
| Magenta button | `#D62598` → hover `#A01B72` | White text (use sparingly) |
| Outline button | 2px `#001E62` border → hover fill `#DFE8F0` | Navy text |

### Dark Theme

Signal Horizon uses a **charcoal/zinc-based dark mode** for better data contrast in dense
dashboard views. This is the approved product dark theme — not a brand violation.

| Layer | Color | Usage |
|-------|-------|-------|
| Hero/Header bg | `#001E62` (Navy) | Brand headers retain navy |
| Content bg | `#09090b` (Zinc 950) or `#000000` | Charcoal base for data contrast |
| Card bg | `#121212` (Deep Charcoal) or `#0A1A3A` (Navy variant) | |
| Surface subtle | `#18181b` (Zinc 900) | |
| Primary text | `#f4f4f5` (Zinc 100) | |
| Secondary text | `#a1a1aa` (Zinc 400) | |
| Links | `#529EEC` → hover `#7CBAFF` | |
| Primary button | `#529EEC` → hover `#7CBAFF` | White text |
| Outline button | 2px `#F0F4F8` border → hover fill `#003EC8` | White text |

**Note**: For marketing/corporate dark contexts, a navy-based palette (`#00174A`, `#0A1A3A`)
is also acceptable. The charcoal approach is preferred for product UIs with dense data.

---

## Buttons

**Shape**: Rectangular. `border-radius: 0`. Always. No exceptions. No slanted/angled edges.
**Labels**: Title Case ("Learn More" not "LEARN MORE" or "learn more").

| Size | Height | Font | Padding |
|------|--------|------|---------|
| Large (Primary) | 56px | Rubik Medium 500, 16px | 0 32px |
| Medium (Outlined) | 48px | Rubik Medium 500, 14px | 0 24px |
| Small (Secondary) | 40px | Rubik SemiBold 600, 12px | 0 20px |

---

## Charts & Data Visualization

Charts are a critical brand surface. Read `references/chart-standards.md` for the complete
chart component reference with gradient formulas, but here are the essentials:

**Series color priority** (use in this order):
1. A10 Blue `#0057B7` (primary series)
2. Sky Blue `#529EEC` (secondary series)
3. Green `#00B140` (success/positive)
4. Orange `#E35205` (warning/caution)
5. Red `#EF3340` (danger/error)
6. Magenta `#D62598` (accent, if needed)
7. Cloud Blue `#5E8AB4` (additional series)
8. Purple `#440099` (additional series)

**Chart rules**:
- Value labels on every bar/data point
- Dashed grid lines at opacity 0.3
- Rubik font throughout (Light 300 for chart titles, Regular 400 for labels)
- Subtitle with context below every chart title
- Hover states for interactivity
- Subtle gradients on bars (not flat fills) — vertical: lighten+30 top → darken-20 bottom
- No rounded corners on bars
- Dark theme default: cards on `#0A1A3A` background
- Left/top highlight edge on bars: `rgba(255,255,255,0.12)`
- Base opacity 0.9, hover opacity 1.0

The `assets/chart-reference.jsx` file contains production-ready React components for vertical
bar, horizontal bar, stacked horizontal, and grouped vertical charts. Use these as templates
when building chart components.

---

## Logos

Logo SVG assets are available in `assets/` for both light and dark themes:

| Product | Files | Usage |
|---------|-------|-------|
| **Apparatus** (app icon) | `apparatus-dark.svg`, `apparatus-light.svg` | Favicon, app icon, small mark |
| **Signal Horizon** | `signal-logo-{theme}.svg` | Logo mark only |
| | `signal-stacked-2line-{theme}.svg` | Stacked with product name |
| | `signal-horizontal-2line-tagline-{theme}.svg` | Horizontal with tagline |
| **Synapse** | `synapse-logo-{theme}.svg` | Logo mark only |
| | `synapse-lockup-stacked-{theme}.svg` | Stacked with product name |
| | `synapse-lockup-horizontal-tagline-{theme}.svg` | Horizontal with tagline |

**Logo rules**:
- Use `-dark` variants on dark/navy backgrounds, `-light` on white/light backgrounds
- Preferred placement: top-left. Acceptable: top-right, bottom-left. Avoid bottom-right.
- Clear space around logo = height of the white triangle inside the "A" in A10's mark
- Minimum size: 50px on screen
- Never distort, add shadows, rotate, recolor, or place on busy backgrounds
- When embedding SVGs inline, preserve viewBox and aspect ratio

---

## Layout Patterns

**Section alternation**: Cycle backgrounds — White → Light Gray `#F0F4F8` → Navy `#001E62` →
A10 Blue `#0057B7` — to create rhythm without borders.

**Diagonal split** (signature A10 treatment):
```css
.hero-diagonal::after {
  content: '';
  position: absolute;
  top: 0; right: 0;
  width: 50%; height: 100%;
  background: #FFFFFF;
  clip-path: polygon(20% 0, 100% 0, 100% 100%, 0 100%);
}
```

**Cards**: No borders, no rounded corners. Use subtle box-shadow:
- Light: `box-shadow: 0 2px 8px rgba(0, 30, 98, 0.1)`
- Dark: `box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3)`

**Spacing scale**: 4 / 8 / 16 / 24 / 32 / 48 / 64px

---

## Review Mode

When asked to review or audit existing work against A10 brand guidelines, perform a structured
pass through these categories. Report findings grouped by severity.

### Critical (Must Fix — instantly off-brand)
- [ ] Rounded corners anywhere (buttons, cards, inputs, images, badges)
- [ ] Wrong font (not Rubik, or Rubik not loaded)
- [ ] Bold headlines instead of Light 300
- [ ] Off-brand colors used prominently (not from palette, or accents used as primary)
- [ ] Logo in wrong colors or on wrong background
- [ ] Magenta used as background or dominant color
- [ ] Poor contrast (failing WCAG AA)

### Major (Should Fix — noticeably off)
- [ ] Wrong button heights or padding
- [ ] Missing or wrong hover states
- [ ] Incorrect font weights for element types
- [ ] Color proportions wrong (too much accent, not enough navy/blue)
- [ ] Charts without value labels or using flat fills
- [ ] Typography: justified text, ALL-CAPS body text, bold where light expected
- [ ] Missing Rubik font import (falling back to system fonts)
- [ ] Accent colors used for non-functional purposes (backgrounds, decorative)

### Minor (Polish — good to great)
- [ ] Inconsistent spacing (not using the 4/8/16/24/32/48/64 scale)
- [ ] Section backgrounds not alternating
- [ ] Icon sizing inconsistent
- [ ] Missing diagonal split opportunity on hero sections
- [ ] Links missing SemiBold weight or hover color change
- [ ] Charts missing subtitle context line
- [ ] Eyebrow text not using letter-spacing 0.1em

### Spirit Check (brand personality)
- [ ] Does it feel confident and clean, or cluttered and uncertain?
- [ ] Is there a clear visual hierarchy with one focal point per section?
- [ ] Is whitespace generous or cramped?
- [ ] Would this look at home next to a10networks.com?
- [ ] Is magenta used as a deliberate accent or scattered randomly?
- [ ] Do the blues dominate the color landscape as they should?

When reporting, lead with the most impactful issues. Provide specific fixes with exact hex codes,
font weights, and CSS properties. Don't just say "wrong color" — say "Header background is
`#2563EB` (Tailwind blue-600), should be `#0057B7` (A10 Blue)."

---

## Reference Files

For detailed specifications beyond what's in this file:

| File | When to Read |
|------|-------------|
| `references/color-system.md` | Need full tint/shade values, CSS custom properties, gradient specs |
| `references/typography.md` | Need complete type scale, kerning details, or Office/print specs |
| `references/chart-standards.md` | Building any chart or data visualization |
| `references/components.md` | Need button CSS, card patterns, alert styles, layout CSS |
| `references/review-checklist.md` | Performing a detailed brand audit with expanded criteria |

---

## CSS Quick-Start

For any new A10 artifact, start with this foundation:

```css
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap');

* { box-sizing: border-box; }
button, input, select, textarea, .card, .btn { border-radius: 0; }

:root {
  --a10-blue: #0057B7;
  --a10-navy: #001E62;
  --a10-white: #FFFFFF;
  --a10-sky: #529EEC;
  --a10-magenta: #D62598;
  --a10-black: #000000;
  --font: 'Rubik', 'Calibri', sans-serif;
}

body {
  font-family: var(--font);
  font-weight: 400;
  font-size: 16px;
  line-height: 1.5;
  color: var(--a10-navy);
}

h1, h2, h3, h4 { font-weight: 300; }
h5, h6 { font-weight: 500; }
```

## React Quick-Start

For JSX/React artifacts, apply the same principles. Use inline styles or a style object:

```jsx
const a10 = {
  blue: '#0057B7', navy: '#001E62', white: '#FFFFFF',
  sky: '#529EEC', magenta: '#D62598', black: '#000000',
  green: '#00B140', orange: '#E35205', red: '#EF3340',
  purple: '#440099', cloudBlue: '#5E8AB4',
  grayLight: '#F0F4F8', grayMedium: '#DFE8F0',
  grayDark: '#404040', grayMid: '#7F7F7F',
  cardDark: '#0A1A3A', navyDark: '#00174A',
  blueDark: '#004189', blueLight: '#7CBAFF',
  skyLight: '#BEDDFF', magentaDark: '#A01B72',
};

// Always include Rubik font link
// Always set border-radius: 0 on all interactive/container elements
// Always use fontWeight: 300 for h1-h4, 500 for h5-h6
```
