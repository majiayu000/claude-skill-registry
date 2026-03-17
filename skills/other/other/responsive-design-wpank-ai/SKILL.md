---
name: responsive-design
model: standard
---

# Responsive Design

Modern responsive CSS patterns using container queries, fluid typography, CSS Grid, and mobile-first strategies.

## WHAT

Comprehensive responsive design techniques:
- Container queries for component-level responsiveness
- Fluid typography and spacing with `clamp()`
- CSS Grid and Flexbox layout patterns
- Mobile-first breakpoint strategies
- Responsive images and media
- Viewport units and dynamic sizing

## WHEN

- Building layouts that adapt across screen sizes
- Creating reusable components that respond to container size
- Implementing fluid typography scales
- Setting up responsive grid systems
- Handling mobile navigation patterns
- Optimizing images for different devices

## KEYWORDS

responsive, container query, media query, breakpoint, mobile-first, fluid typography, clamp, css grid, flexbox, viewport, adaptive, responsive images


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install responsive-design
```


---

## Breakpoint Scale (Mobile-First)

```css
/* Base: Mobile (< 640px) - no media query needed */

@media (min-width: 640px)  { /* sm: Large phones, small tablets */ }
@media (min-width: 768px)  { /* md: Tablets */ }
@media (min-width: 1024px) { /* lg: Laptops */ }
@media (min-width: 1280px) { /* xl: Desktops */ }
@media (min-width: 1536px) { /* 2xl: Large screens */ }
```

**Tailwind equivalents:** `sm:`, `md:`, `lg:`, `xl:`, `2xl:`

---

## Container Queries

Component-level responsiveness independent of viewport:

```css
/* Define containment context */
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Query the container, not viewport */
@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
  }
}

@container card (min-width: 600px) {
  .card-title {
    font-size: 1.5rem;
  }
}

/* Container query units */
.card-title {
  font-size: clamp(1rem, 5cqi, 2rem); /* 5% of container inline-size */
}
```

### Tailwind Container Queries

```tsx
function ResponsiveCard({ title, image, description }) {
  return (
    <div className="@container">
      <article className="flex flex-col @md:flex-row @md:gap-4">
        <img
          src={image}
          alt=""
          className="w-full @md:w-48 @lg:w-64 aspect-video @md:aspect-square object-cover"
        />
        <div className="p-4 @md:p-0">
          <h2 className="text-lg @md:text-xl @lg:text-2xl font-semibold">
            {title}
          </h2>
          <p className="mt-2 text-muted-foreground @md:line-clamp-3">
            {description}
          </p>
        </div>
      </article>
    </div>
  )
}
```

---

## Fluid Typography

### CSS Custom Properties Scale

```css
:root {
  --text-xs:  clamp(0.75rem,  0.7rem + 0.25vw, 0.875rem);
  --text-sm:  clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
  --text-base: clamp(1rem,    0.9rem + 0.5vw, 1.125rem);
  --text-lg:  clamp(1.125rem, 1rem + 0.625vw, 1.25rem);
  --text-xl:  clamp(1.25rem,  1rem + 1.25vw, 1.5rem);
  --text-2xl: clamp(1.5rem,   1.25rem + 1.25vw, 2rem);
  --text-3xl: clamp(1.875rem, 1.5rem + 1.875vw, 2.5rem);
  --text-4xl: clamp(2.25rem,  1.75rem + 2.5vw, 3.5rem);
}

h1 { font-size: var(--text-4xl); }
h2 { font-size: var(--text-3xl); }
h3 { font-size: var(--text-2xl); }
p  { font-size: var(--text-base); }
```

### Fluid Spacing Scale

```css
:root {
  --space-xs: clamp(0.25rem, 0.2rem + 0.25vw, 0.5rem);
  --space-sm: clamp(0.5rem,  0.4rem + 0.5vw, 0.75rem);
  --space-md: clamp(1rem,    0.8rem + 1vw, 1.5rem);
  --space-lg: clamp(1.5rem,  1.2rem + 1.5vw, 2.5rem);
  --space-xl: clamp(2rem,    1.5rem + 2.5vw, 4rem);
}
```

### Clamp Formula

```
clamp(MIN, PREFERRED, MAX)

MIN: Smallest allowed size
PREFERRED: Ideal fluid calculation (often uses vw)
MAX: Largest allowed size
```

---

## CSS Grid Responsive Layouts

### Auto-Fit Grid (Items Wrap)

```css
.grid-auto {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
  gap: 1.5rem;
}
```

### Named Grid Areas

```css
.page-layout {
  display: grid;
  grid-template-areas:
    "header"
    "main"
    "sidebar"
    "footer";
  gap: 1rem;
}

@media (min-width: 768px) {
  .page-layout {
    grid-template-columns: 1fr 300px;
    grid-template-areas:
      "header header"
      "main sidebar"
      "footer footer";
  }
}

@media (min-width: 1024px) {
  .page-layout {
    grid-template-columns: 250px 1fr 300px;
    grid-template-areas:
      "header header header"
      "nav main sidebar"
      "footer footer footer";
  }
}

.header  { grid-area: header; }
.main    { grid-area: main; }
.sidebar { grid-area: sidebar; }
.footer  { grid-area: footer; }
```

### Tailwind Grid

```tsx
function ProductGrid({ products }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 md:gap-6">
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  )
}
```

---

## Responsive Navigation

```tsx
function ResponsiveNav({ items }) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <nav className="relative">
      {/* Mobile toggle */}
      <button
        className="lg:hidden p-2"
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-controls="nav-menu"
      >
        <span className="sr-only">Toggle navigation</span>
        {isOpen ? <X /> : <Menu />}
      </button>

      {/* Navigation links */}
      <ul
        id="nav-menu"
        className={cn(
          // Mobile: dropdown
          "absolute top-full left-0 right-0 bg-background border-b",
          "flex flex-col",
          isOpen ? "flex" : "hidden",
          // Desktop: horizontal, always visible
          "lg:static lg:flex lg:flex-row lg:border-0"
        )}
      >
        {items.map(item => (
          <li key={item.href}>
            <a
              href={item.href}
              className="block px-4 py-3 lg:px-3 lg:py-2 hover:bg-muted lg:hover:bg-transparent"
            >
              {item.label}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  )
}
```

---

## Responsive Images

### Art Direction with Picture

```tsx
function ResponsiveHero() {
  return (
    <picture>
      {/* Different crops for different screens */}
      <source media="(min-width: 1024px)" srcSet="/hero-wide.webp" type="image/webp" />
      <source media="(min-width: 768px)" srcSet="/hero-medium.webp" type="image/webp" />
      <source srcSet="/hero-mobile.webp" type="image/webp" />
      
      <img
        src="/hero-mobile.jpg"
        alt="Hero description"
        className="w-full h-auto"
        loading="eager"
        fetchPriority="high"
      />
    </picture>
  )
}
```

### Resolution Switching with srcset

```tsx
function ProductImage({ product }) {
  return (
    <img
      src={product.image}
      srcSet={`
        ${product.image}?w=400 400w,
        ${product.image}?w=800 800w,
        ${product.image}?w=1200 1200w
      `}
      sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
      alt={product.name}
      className="w-full h-auto object-cover"
      loading="lazy"
    />
  )
}
```

---

## Responsive Tables

### Horizontal Scroll Pattern

```tsx
function ResponsiveTable({ data, columns }) {
  return (
    <div className="w-full overflow-x-auto">
      <table className="w-full min-w-[600px]">
        <thead>
          <tr>
            {columns.map(col => (
              <th key={col.key} className="text-left p-3">{col.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i} className="border-t">
              {columns.map(col => (
                <td key={col.key} className="p-3">{row[col.key]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
```

### Card Layout on Mobile

```tsx
function ResponsiveDataTable({ data, columns }) {
  return (
    <>
      {/* Desktop: table */}
      <table className="hidden md:table w-full">
        {/* standard table markup */}
      </table>

      {/* Mobile: cards */}
      <div className="md:hidden space-y-4">
        {data.map((row, i) => (
          <div key={i} className="border rounded-lg p-4 space-y-2">
            {columns.map(col => (
              <div key={col.key} className="flex justify-between">
                <span className="font-medium text-muted-foreground">{col.label}</span>
                <span>{row[col.key]}</span>
              </div>
            ))}
          </div>
        ))}
      </div>
    </>
  )
}
```

---

## Viewport Units

```css
/* Standard viewport units - problematic on mobile */
.full-height { height: 100vh; }

/* Dynamic viewport units (recommended) */
.full-height-dynamic { height: 100dvh; } /* Accounts for mobile browser UI */

/* Small viewport (minimum when UI shown) */
.min-full-height { min-height: 100svh; }

/* Large viewport (maximum when UI hidden) */
.max-full-height { max-height: 100lvh; }
```

---

## Best Practices

1. **Mobile-First**: Write base styles for mobile, enhance for larger screens
2. **Content Breakpoints**: Set breakpoints where content breaks, not device sizes
3. **Fluid Over Fixed**: Prefer `clamp()` and relative units over fixed `px`
4. **Container Queries**: Use for component-level responsiveness
5. **Touch Targets**: Minimum 44×44px tap targets on mobile
6. **Test Real Devices**: Simulators don't catch all issues
7. **Logical Properties**: Use `inline`/`block` for internationalization

---

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Horizontal scroll | Fixed widths | Use relative units, `max-width: 100%` |
| 100vh too tall on mobile | Address bar | Use `100dvh` or `100svh` |
| Tiny tap targets | Desktop design | Min 44px height/width on interactive elements |
| Images breaking layout | Missing constraints | Add `max-width: 100%; height: auto;` |
| Text too small | Fixed font size | Use fluid typography with `clamp()` |

---

## NEVER

- Use `px` for typography (use `rem`)
- Skip mobile testing on real devices
- Forget touch target sizing (44×44px minimum)
- Use `100vh` on mobile without fallback
- Nest too many media queries (flattens readability)
- Ignore content-based breakpoints in favor of device-specific ones
