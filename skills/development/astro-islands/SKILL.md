# Astro Islands Architecture Skill

## When to Use This Skill

Use this skill when:
- Adding interactive components to Astro pages
- Deciding between React, vanilla JS, or static HTML
- Troubleshooting hydration errors
- Optimizing JavaScript bundle size

## Core Principle

> **React is for composition and layout. Vanilla JS is for interactivity.**

In Astro, the best architecture ships minimal JavaScript:
- Use React/components for **SSR composition** (zero JS shipped)
- Use vanilla JS for **simple interactions** (theme toggle, mobile menu)
- Use `client:only` **sparingly** for complex widgets that truly need React state

## Astro Client Directives

| Directive | Server Renders? | Ships JS? | Use For |
|-----------|-----------------|-----------|---------|
| None | Yes | No | Static content, layouts |
| `client:load` | Yes | Yes | Hydrates immediately (avoid if possible) |
| `client:idle` | Yes | Yes | Hydrates when idle |
| `client:visible` | Yes | Yes | Hydrates when visible |
| `client:only="react"` | No | Yes | Complex widgets, no SSR |

## Architecture Patterns

### Pattern 1: Pure SSR (Recommended for most content)

```astro
---
// index.astro
import { HomePage } from '../components/HomePage';
const data = await fetchData();
---
<HomePage data={data} />  <!-- NO client directive = static HTML -->
```

**What you get:**
- React components render to static HTML at build time
- Zero JavaScript shipped
- Fully testable in isolation
- Fast page loads

### Pattern 2: Vanilla JS for Simple Interactivity

```astro
---
// Layout.astro
---
<button id="theme-toggle">Toggle Theme</button>

<script is:inline>
  document.getElementById('theme-toggle').addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
  });
</script>
```

**Use for:**
- Theme toggles (~20 lines)
- Mobile menu open/close (~15 lines)
- Simple form validation
- Scroll-triggered animations

**Benefits:**
- ~0.5kb vs ~5kb+ for React hydration
- No hydration bugs
- Works immediately (no waiting for React to load)

### Pattern 3: client:only for Complex Widgets (Last Resort)

```astro
---
// page.astro
import { PhotoGallery } from '../components/PhotoGallery';
---
<!-- Only when vanilla JS isn't sufficient -->
<PhotoGallery client:only="react" photos={photos} />
```

**Use for:**
- Complex state management
- Heavy user interaction (drag-drop, canvas)
- Third-party React libraries

**Trade-offs:**
- Ships React runtime (~5kb+)
- Renders empty until JS loads
- Cannot be nested inside SSR React

## Critical Constraint

### You CANNOT Nest Client Islands Inside SSR React

```astro
<!-- THIS DOES NOT WORK -->
<HomePage data={data} />  <!-- SSR React -->
<script>
  // Trying to mount React inside a div that HomePage rendered
  createRoot(document.getElementById('widget-root')).render(<Widget />);
</script>
```

**Error:** `@vitejs/plugin-react can't detect preamble`

**Why:** Astro's React integration doesn't support split-brain React:
- Part server-rendered
- Part client-mounted into server-rendered placeholders

**Solution:** Use vanilla JS for the interaction, or restructure so the interactive part is a sibling, not a child.

## Decision Tree

```
Need to render HTML?
├── Yes → Use React component (no directive)
│   └── Need interactivity?
│       ├── Simple (toggle, menu) → Vanilla JS script
│       └── Complex (gallery, forms) → Separate client:only component
└── No → Why are you here?
```

## Performance Comparison

| Approach | JS Shipped | Time to Interactive |
|----------|------------|---------------------|
| SSR React (no directive) | 0kb | Instant |
| SSR + Vanilla JS | ~0.5kb | Instant |
| SSR + client:load | ~5kb+ | After React loads |
| client:only | ~5kb+ | After React loads |

## Common Pitfalls

### DON'T: Use client:load on Layout Components
```astro
<!-- Bad: Ships React for static content -->
<Layout client:load>
  <Content />
</Layout>
```

### DON'T: Over-engineer Simple Interactions
```astro
<!-- Bad: React for a toggle -->
<ThemeToggle client:only="react" />

<!-- Good: Vanilla JS -->
<button id="theme-toggle">Toggle</button>
<script is:inline>/* 10 lines */</script>
```

### DON'T: Mix Astro Components Inside React
```tsx
// This DOES NOT WORK
export const Page = () => {
  return <AstroComponent />;  // Can't import .astro into .tsx
};
```

### DO: Keep React Containers Pure SSR
```tsx
// Good: No useState, no useEffect
export const HomePage: React.FC<Props> = ({ articles }) => {
  return (
    <>
      <Header />
      <ArticleGrid articles={articles} />
      <Footer />
    </>
  );
};
```

## Script Directive Reference

| Directive | Bundled? | Deferred? | Use For |
|-----------|----------|-----------|---------|
| `<script>` | Yes | Yes | Most scripts |
| `<script is:inline>` | No | No | Theme init (before paint), small scripts |

Use `is:inline` for:
- Theme initialization (must run before first paint)
- Tiny scripts where bundling overhead isn't worth it
- Scripts that need to run synchronously

## Testing Strategy

| What | Where | How |
|------|-------|-----|
| React components | Ladle/Storybook | Visual regression |
| Full page with interactions | Astro dev server | Playwright integration tests |
| Vanilla JS | Integration tests | Playwright |

You cannot test vanilla JS interactions in component isolation tools like Ladle - they need the full Astro page context.
