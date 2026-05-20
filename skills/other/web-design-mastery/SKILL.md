---
name: web-design-mastery
description: "Production-grade web application UI design based on Refactoring UI principles. ALWAYS activate for: landing page, dashboard, auth screens, hero sections, card design, button design, form inputs, navigation, layouts, spacing decisions, typography hierarchy, color selection, shadows, depth, empty states, background decoration. Provides design workflow, visual hierarchy, spacing systems (4px grid), type scale, HSL color systems, shadow elevation, finishing touches. Turkish: sayfa tasarımı, UI/UX, frontend tasarım, web tasarım, güzel arayüz, modern tasarım, card tasarımı, buton stili, form tasarımı, renk paleti, tipografi. English: beautiful interface, sleek design, premium feel, visual hierarchy, whitespace, color palette, typography scale."
---

# Web Design Mastery

Production-grade UI design principles from Refactoring UI by Adam Wathan & Steve Schoger.

---

## Core Design Workflow

### 1. Start with a Feature, Not a Layout

- Design the actual piece of functionality first
- Don't start with navigation, sidebar, or shell
- Details come later—work in grayscale first
- Don't design too much—work in cycles

### 2. Establish Systems Before Designing

Define these systems up front to eliminate decision fatigue:

**Spacing Scale (px):**

| Token | Size | Use Case |
|-------|------|----------|
| 1 | 4 | Micro gaps |
| 2 | 8 | Tight, within components |
| 3 | 12 | Related elements |
| 4 | 16 | Section padding |
| 6 | 24 | Between sections |
| 8 | 32 | Major separation |
| 12 | 48 | Large gaps |
| 16 | 64 | Hero spacing |
| 24 | 96 | Maximum separation |

**Type Scale (px):**

| Size | Use Case |
|------|----------|
| 12 | Labels, meta, fine print |
| 14 | Body text, default |
| 16 | Emphasis, subheadings |
| 18 | Section headings |
| 20 | Card titles |
| 24 | Page section titles |
| 30 | Page headings |
| 36 | Hero subheading |
| 48 | Hero heading |
| 60-72 | Display text |

**Shadow Scale (5 levels):**

| Level | Use Case |
|-------|----------|
| 1 | Buttons, subtle lift |
| 2 | Cards, inputs |
| 3 | Dropdowns, popovers |
| 4 | Sticky elements |
| 5 | Modals, dialogs |

### 3. Build Hierarchy, Not Decoration

- **Primary**: Dark color (headlines, key actions)
- **Secondary**: Grey (supporting text, dates)
- **Tertiary**: Light grey (metadata, copyright)

Key principles:

- Size isn't everything—use weight and color
- Emphasize by de-emphasizing competing elements
- Labels are a last resort—combine with values
- Semantics are secondary to hierarchy

### 4. Apply Depth Meaningfully

- Light comes from above
- Shadows convey elevation (closer = more attention)
- Use two-part shadows for premium look
- Consider overlapping elements for layers

### 5. Finish with Polish

- Supercharge defaults (bullets → icons, style quotes)
- Add accent borders for visual interest
- Design empty states as first impressions
- Use fewer borders—prefer shadows or spacing

---

## Color System

**Categories needed:**

1. **Greys** (8-10 shades): Text, backgrounds, panels, borders
2. **Primary** (5-10 shades): Actions, active states, links
3. **Accents** (per semantic): Success, warning, error states

**Process for defining shades:**

1. Pick base color (500) that works as button background
2. Pick edges (100 for tinted bg, 900 for text)
3. Fill gaps: 700, 300 → 800, 600, 400, 200

**Key rules:**

- Use HSL for intuitive adjustments
- Increase saturation at lightness extremes
- Rotate hue toward bright (60°, 180°, 300°) for lighter
- Greys can be warm (yellow/orange tint) or cool (blue tint)
- Accessibility: 4.5:1 contrast for normal text, 3:1 for large

---

## Anti-Patterns

**NEVER do:**

- Grey text on colored backgrounds (hand-pick colors instead)
- Fill the whole screen when content needs less
- Use grids religiously (fixed widths often better)
- Ambiguous spacing (more space between groups than within)
- Relative sizing that doesn't scale
- Scale icons beyond intended size
- Rely on color alone for meaning

---

## Reference Files

For detailed guidance on specific topics:

| Topic | File | When to Read |
|-------|------|--------------|
| Visual hierarchy, labels, emphasis | [hierarchy.md](references/hierarchy.md) | Balancing element importance |
| Spacing, white space, layout grids | [spacing-layout.md](references/spacing-layout.md) | Layout decisions |
| Typography, fonts, line-height | [typography.md](references/typography.md) | Text styling |
| HSL, shades, accessibility | [color.md](references/color.md) | Color palette creation |
| Shadows, elevation, layers | [depth.md](references/depth.md) | Adding depth to UI |
| Borders, backgrounds, empty states | [finishing-touches.md](references/finishing-touches.md) | Polishing design |
