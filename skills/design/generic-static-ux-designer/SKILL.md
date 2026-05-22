---
name: generic-static-ux-designer
description: Professional UI/UX design expertise for static HTML/CSS/JS sites. Covers design thinking, user psychology, visual hierarchy, minimalist interaction patterns, accessibility, and performance-driven design. Use when designing features, improving UX, or conducting design reviews.
---

# Static Site UX Designer

Professional UX expertise for minimalist static sites.

**Extends:** [Generic UX Designer](../generic-ux-designer/SKILL.md) - Read base skill for design thinking process, user psychology, heuristic evaluation, and research methods.

## Minimalist Design Philosophy

### Less is More

Every element must earn its place:

- Does this add value for the user?
- Can I remove this and still communicate?
- Is this decoration or function?

### Content-to-Chrome Ratio

Maximize content, minimize interface:

```
BAD:  10% content, 90% navigation/chrome
GOOD: 80% content, 20% essential navigation
```

### Limited Palette = High Impact

- 2-3 colors maximum
- 1 accent color for actions
- Stark contrast over subtle gradients

## Performance-Constrained UX

### Every KB Matters

| Element              | Impact     |
| -------------------- | ---------- |
| Web font             | +50-100KB  |
| Hero image           | +200-500KB |
| Animation library    | +30-50KB   |
| JavaScript framework | +30-100KB  |

Ask: Does this UX improvement justify the weight?

### Speed is UX

- < 1s load time is expected
- < 100ms interaction response
- Users leave after 3s wait

## Static Page Flow Patterns

### Simple Navigation

```
Home → About → Contact → Back to Home
```

No infinite scroll, no SPA patterns. Clear page boundaries.

### Anchor Navigation

```html
<nav>
  <a href="#section1">Section 1</a>
  <a href="#section2">Section 2</a>
</nav>

<section id="section1">...</section>
<section id="section2">...</section>
```

## CSS-Only Interaction Patterns

### Accessible Disclosure

```html
<details>
  <summary>More info</summary>
  <p>Additional content here.</p>
</details>
```

### Hover States

```css
.card {
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
}
```

### No-JavaScript Fallbacks

Always work without JS:

- Navigation works with `<a>` tags
- Forms submit normally
- Content accessible without scripting

## Accessibility in Minimalism

### What Minimalism Allows

| Requirement      | Minimalist Solution      |
| ---------------- | ------------------------ |
| Focus indicators | Simple outline           |
| Skip links       | Clean text link          |
| Alt text         | Concise descriptions     |
| Contrast         | High contrast by default |

### Touch Targets

- 44x44px minimum
- 8px spacing between targets
- Larger is better on mobile

## Design Critique for Static Sites

### Questions to Ask

1. **Performance impact?**
   - How many KB does this add?
   - Is it worth the load time?

2. **Works without JS?**
   - Core function accessible?
   - Progressive enhancement?

3. **Adds clarity or noise?**
   - Does this help users?
   - Can it be simpler?

4. **Maintains aesthetic?**
   - Within color palette?
   - Consistent with existing?

### Red Flags

- Adding web fonts without strong reason
- Animation libraries for simple effects
- Complex navigation for few pages
- JavaScript where CSS suffices

## Static UX Checklist

- [ ] Core content visible without scrolling
- [ ] Navigation intuitive (< 5 items)
- [ ] Works without JavaScript
- [ ] Touch targets 44px minimum
- [ ] Color contrast 4.5:1+
- [ ] Page weight < 50KB (excl. images)

## See Also

- [Generic UX Designer](../generic-ux-designer/SKILL.md) - Design thinking, psychology
- [UX Principles](../_shared/UX_PRINCIPLES.md) - Research methods, heuristics
- [Design Patterns](../_shared/DESIGN_PATTERNS.md) - Visual patterns
