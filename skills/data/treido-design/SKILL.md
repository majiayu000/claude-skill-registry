---
name: treido-design
description: Create UI specifications and review designs for Treido marketplace. Use when planning new UI features, reviewing existing designs for consistency, or when something "looks off" or "feels wrong" in the interface. Triggers include design reviews, mobile layout issues, spacing problems, visual hierarchy questions, or requests for UI specs before implementation.
deprecated: true
---

# Treido Design

> Deprecated (2026-01-29). Use `treido-orchestrator` Phase 2 planning; implement via `treido-impl-frontend`.

## Quick Start

1. Identify the surface (route, component, or flow)
2. Define the user goal and viewport priority (mobile-first)
3. Create a UI spec with layout, states, and acceptance criteria
4. Hand off to treido-frontend for implementation

## Design Philosophy

Treido follows a **clean marketplace aesthetic**:

- **Mobile-first**: Design for phones, enhance for desktop
- **Clear hierarchy**: One primary action per screen
- **Whitespace**: Generous spacing, avoid dense grids
- **Consistency**: Reuse existing patterns before inventing new ones
- **No decoration**: No gradients, glows, or animations

## UI Spec Template

When creating a spec, use this format:

```markdown
## Surface
- Route/component: `/products/[id]`
- Primary user goal: View product details and add to cart

## Layout (Mobile-First)

### Mobile (< 768px)
- Single column
- Image carousel: full width, 1:1 aspect
- Title + price: sticky bottom bar
- CTA: Full-width "Add to Cart" button

### Desktop (≥ 1024px)
- Two columns: image (60%) | details (40%)
- Image gallery: thumbnail strip below main
- CTA: Standard button width

## Component Map

| Component | Location | Notes |
|-----------|----------|-------|
| ImageCarousel | components/shared/ | Existing |
| ProductDetails | _components/ | Route-private |
| AddToCartButton | components/shared/ | Existing |
| PriceDisplay | components/shared/ | Existing |

## States

| State | UI |
|-------|-----|
| Loading | Skeleton: image placeholder + text lines |
| Empty | N/A (product always exists or 404) |
| Error | Error card with retry button |
| Success | Full product display |

## Accessibility

- Image carousel: keyboard navigable, alt text required
- Price: announced to screen readers
- Add to Cart: clear button label, loading state announced

## i18n Keys (if new copy needed)

```json
{
  "ProductPage": {
    "addToCart": { "en": "Add to Cart", "bg": "Добави в кошницата" },
    "outOfStock": { "en": "Out of Stock", "bg": "Няма наличност" }
  }
}
```

## Acceptance Criteria

- [ ] Mobile: single column, full-width CTA
- [ ] Desktop: two-column layout
- [ ] Loading state shows skeleton
- [ ] All text uses semantic tokens (no hardcoded colors)
- [ ] Passes `pnpm -s styles:gate`
```

## Design Constraints (Non-Negotiable)

### Tailwind v4 Only
- No gradients
- No arbitrary values (`[13px]`, `[#ff0000]`)
- No palette colors (`blue-500`, `red-600`)
- Use semantic tokens only (`bg-primary`, `text-foreground`)

### No New Animations
- Keep UX stable and fast
- Use existing transitions (hover states, focus rings)
- No page transitions, no skeleton shimmer, no loading spinners beyond existing

### Reuse Before Creating
```
Priority order:
1. Existing shadcn primitive (components/ui/)
2. Existing shared composite (components/shared/)
3. Adapt existing pattern
4. Create new (rare, needs justification)
```

## Common Patterns

### Mobile Navigation
- Bottom tab bar for primary nav
- Hamburger menu for secondary nav
- Back button in header for drill-down

### Card Layouts
- Mobile: single column, full-width cards
- Tablet: 2 columns
- Desktop: 3-4 columns with max-width container

### Form Patterns
- Labels above inputs (not floating)
- Error messages below input
- Submit button at bottom, full-width on mobile

### Modal/Sheet Usage
- **Mobile**: Bottom sheet (slides up)
- **Desktop**: Centered dialog or side panel

## Review Checklist

When reviewing existing UI:

- [ ] Mobile-first: works on 320px width?
- [ ] Touch targets: ≥44px tap areas?
- [ ] Hierarchy: one clear primary CTA?
- [ ] Spacing: uses standard tokens (p-4, gap-4)?
- [ ] Colors: semantic tokens only?
- [ ] Loading state: has skeleton or spinner?
- [ ] Error state: clear message + action?
- [ ] i18n: no hardcoded strings?

## Handoff to Implementation

After creating a spec:

```
Use treido-frontend to implement:
- Surface: [route/component]
- Files to create/modify: [list 1-3 files]
- Run verification: pnpm -s typecheck && pnpm -s lint && pnpm -s styles:gate
```

## References

**For component patterns:** See [references/patterns.md](references/patterns.md)
**For spacing/typography scale:** See [references/tokens.md](references/tokens.md)
