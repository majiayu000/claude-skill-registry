---
name: react-review
description: React and Next.js performance optimization guidelines from Vercel Engineering. Contains 45+ rules across 8 categories.
---

# Vercel React Best Practices

Quick reference for reviewing React code. For detailed rules with code examples, see [RULES.md](RULES.md).

## Rule Categories (by priority)

| Priority | Category | Impact |
|----------|----------|--------|
| 1 | Eliminating Waterfalls | CRITICAL |
| 2 | Bundle Size Optimization | CRITICAL |
| 3 | Server-Side Performance | HIGH |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH |
| 5 | Re-render Optimization | MEDIUM |
| 6 | Rendering Performance | MEDIUM |
| 7 | JavaScript Performance | LOW-MEDIUM |
| 8 | Advanced Patterns | LOW |

## Critical Rules Summary

### Eliminating Waterfalls
- `async-parallel` - Use `Promise.all()` for independent operations
- `async-defer-await` - Move await into branches where actually used
- `async-suspense-boundaries` - Use Suspense to stream content

### Bundle Size
- `bundle-barrel-imports` - Import directly, avoid barrel files
- `bundle-dynamic-imports` - Use `next/dynamic` for heavy components
- `bundle-defer-third-party` - Load analytics after hydration

### Re-render Optimization
- `rerender-memo` - Extract expensive work into memoized components
- `rerender-functional-setstate` - Use functional setState for stable callbacks
- `rerender-lazy-state-init` - Pass function to useState for expensive values

### Common Patterns
- `rendering-conditional-render` - Use ternary, not `&&` for conditionals with numbers
- Missing keys in list rendering
- Index as key for dynamic lists
