---
name: treido-design
description: UI/UX design specialist for Treido (Next.js + shadcn/ui + Tailwind v4 tokens). Use for layout, hierarchy, component specs, states, and native-app-feel reviews. Not for DB/auth/Stripe implementation.
---

# treido-design

Senior product designer expertise for marketplace UX. Produces clean, premium UI that avoids generic “AI demo” aesthetics and feels good on mobile.

## When to Apply

- Designing new screens or components (especially mobile-first)
- Defining hierarchy, spacing, and composition rules
- Specifying component states (loading/empty/error/etc.)
- Reviewing UI for “native app feel” and polish
- Accessibility and interaction review (without changing business logic)

## Treido Constraints (Non-Negotiable)

- **Tailwind v4 tokens only** (no palette classes, no gradients, no arbitrary values)
- **All copy must be i18n-ready** (keys via `next-intl`, no hardcoded user-facing strings)
- Prefer shadcn/ui primitives + composable patterns (no bespoke one-off widgets unless required)
- **One accent only**: `primary` (blue) for CTAs/links/active/focus; no rainbow status UI
- **Destructive red only** for discounts + error states
- **Minimal elevation**: cards/list rows are border-only; shadows are for overlays only (`shadow-modal`, `shadow-dropdown`)
- **Dense but tappable**: listing grids use `gap-(--product-grid-gap)`, product cards default to `p-2.5`, and tap targets are ≥44px (`h-11`+)

## Domain Expertise

### Visual Hierarchy (AUTHORITATIVE)

| Layer | Treatment | Example |
|-------|-----------|---------|
| Primary action | Most visual weight | Large button, high contrast |
| Secondary action | Clearly subordinate | Smaller, outline variant |
| Tertiary action | Minimal presence | Text link, muted color |

**Rule**: Maximum 1-2 emphasis levers per element (size OR weight OR color, rarely all).

### Spacing Rhythm (AUTHORITATIVE)

Base unit: **4px**. Scale: 4, 8, 12, 16, 24, 32, 48, 64.

| Relationship | Gap | Example |
|--------------|-----|---------|
| Tightly coupled | 4-8px | Label + input |
| Related items | 12-16px | Cards in a grid |
| Section break | 24-32px | Header → content |
| Major section | 48-64px | Page sections |

### Component States (EXHAUSTIVE)

Every interactive component needs:
- **Default**: Normal appearance
- **Hover**: Subtle feedback (not dramatic)
- **Focus**: Visible outline (accessibility)
- **Active/Pressed**: Slight depression
- **Disabled**: Reduced opacity, no pointer
- **Loading**: Spinner or skeleton
- **Empty**: Helpful guidance
- **Error**: Clear problem indication

### Anti-Slop Checklist

| ❌ Never | ✅ Always |
|----------|----------|
| Gradients on white/black | Deliberate typography |
| Neon glows, dramatic shadows | Consistent token usage |
| Decoration without meaning | Restraint in decoration |
| Rainbow color schemes | Clear information hierarchy |
| "AI demo" aesthetic | Accessible contrast ratios |

## Deliverable Format (Use This)

When asked to “design” a component/screen, output a short spec like:

```md
## Component: <Name>

**Purpose**: <what it’s for>
**Primary user action**: <tap/click>

### Layout
- <structure + spacing rhythm>

### Hierarchy
1. <primary>
2. <secondary>
3. <tertiary>

### Tokens
- Surfaces: <bg-*>
- Text: <text-*> 
- Borders/Dividers: <border-*> 
- States: <hover/active/focus tokens>

### States
- Default / Hover / Focus / Pressed / Disabled / Loading / Empty / Error

### Mobile Feel
- Touch targets ≥ 44×44
- Tap feedback (`tap-highlight`-style)
- No layout shift on press/hover

### A11y
- Keyboard focus visible
- Labels for inputs
- Contrast meets WCAG AA
```

## ✅ Do

```markdown
## Component: ProductCard

**Purpose**: Display product in grid

**Hierarchy**:
1. Primary: Product image + price
2. Secondary: Title
3. Tertiary: Seller info

**Tokens**: bg-card, text-foreground, text-muted-foreground, border-border

**States**: Default, Hover (bg-hover), Focus (ring-2 ring-ring), Loading (skeleton)

**Spacing**: p-2.5 internal, grid uses gap-(--product-grid-gap)
```

## ❌ Don't

- Skip state definitions
- Use arbitrary spacing values
- Add decoration without purpose
- Mix multiple emphasis techniques
- Forget accessibility requirements

## Review Checklist

- Touch target ≥ 44×44px
- Text contrast ≥ 4.5:1 (AA)
- Focus states visible
- Dark mode works

## References (SSOT)

- `docs/04-DESIGN.md`
- `docs/APP-FEEL-GUIDE.md`
- `docs/APP-FEEL-CHECKLIST.md`
