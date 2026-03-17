---
name: responsive-design
description: Build responsive, device-optimized interfaces using mobile-first approach. Covers breakpoint strategies, fluid typography, container queries, viewport units, and device-specific optimizations for web, tablet, and mobile. Use for responsive layouts, adaptive design, and cross-device compatibility.
---

# Responsive Design

Create interfaces that work beautifully across all devices and screen sizes.

## Instructions

1. **Start mobile-first** - Write base styles for mobile, enhance for larger screens
2. **Use fluid layouts** - Prefer percentages and fr units over fixed pixels
3. **Set strategic breakpoints** - Break at content needs, not specific devices
4. **Test on real devices** - Emulators miss touch and performance nuances
5. **Optimize for touch** - Minimum 44x44px touch targets on mobile

## Breakpoint Strategy

### Tailwind Default Breakpoints

```css
/* Mobile first - base styles apply to all */
sm: 640px   /* Landscape phones, small tablets */
md: 768px   /* Tablets */
lg: 1024px  /* Desktops, laptops */
xl: 1280px  /* Large desktops */
2xl: 1536px /* Extra large screens */
```

### Content-Based Breakpoints

```tsx
// Break when content needs it, not at device widths
<div className="
  grid
  grid-cols-1                                    /* Stack on mobile */
  min-[500px]:grid-cols-2                        /* 2 cols when content fits */
  min-[800px]:grid-cols-3                        /* 3 cols for wider screens */
  min-[1200px]:grid-cols-4                       /* 4 cols for large screens */
  gap-4
">
```

## Layout Patterns

### Responsive Grid

```tsx
// Auto-fit grid - cards expand to fill space
<div className="grid grid-cols-[repeat(auto-fit,minmax(280px,1fr))] gap-6">
  {cards.map(card => <Card key={card.id} {...card} />)}
</div>

// Responsive sidebar layout
<div className="flex flex-col lg:flex-row min-h-screen">
  <aside className="
    w-full lg:w-64
    lg:sticky lg:top-0 lg:h-screen
    border-b lg:border-b-0 lg:border-r
  ">
    <Navigation />
  </aside>
  <main className="flex-1 p-4 lg:p-8">
    <Content />
  </main>
</div>
```

### Responsive Navigation

```tsx
function ResponsiveNav() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between h-16">
          <Logo />

          {/* Desktop nav */}
          <div className="hidden md:flex items-center space-x-4">
            <NavLink href="/home">Home</NavLink>
            <NavLink href="/about">About</NavLink>
            <NavLink href="/contact">Contact</NavLink>
          </div>

          {/* Mobile menu button */}
          <button
            className="md:hidden p-2"
            onClick={() => setIsOpen(!isOpen)}
            aria-expanded={isOpen}
            aria-label="Toggle navigation"
          >
            <MenuIcon />
          </button>
        </div>

        {/* Mobile nav */}
        {isOpen && (
          <div className="md:hidden py-4 space-y-2">
            <NavLink href="/home" block>Home</NavLink>
            <NavLink href="/about" block>About</NavLink>
            <NavLink href="/contact" block>Contact</NavLink>
          </div>
        )}
      </div>
    </nav>
  );
}
```

## Fluid Typography

### Clamp-Based Scaling

```css
/* Fluid font sizes that scale with viewport */
.fluid-heading {
  /* Min 24px, preferred 5vw, max 48px */
  font-size: clamp(1.5rem, 5vw, 3rem);
}

.fluid-body {
  /* Min 16px, preferred 1.5vw + 12px, max 20px */
  font-size: clamp(1rem, 1.5vw + 0.75rem, 1.25rem);
}
```

### Tailwind Fluid Typography

```tsx
// Responsive text that scales with breakpoints
<h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold">
  Responsive Heading
</h1>

<p className="text-base md:text-lg lg:text-xl">
  Body text that grows on larger screens
</p>
```

## Container Queries

### Modern Container-Based Layouts

```tsx
// Define container
<div className="@container">
  <div className="
    flex flex-col
    @md:flex-row     /* Row when container is 448px+ */
    @lg:gap-8        /* More gap when container is 512px+ */
  ">
    <img className="w-full @md:w-48" src="..." alt="..." />
    <div className="flex-1">
      <h3 className="text-lg @lg:text-xl">Title</h3>
      <p>Content adapts to container, not viewport</p>
    </div>
  </div>
</div>
```

```css
/* CSS Container Queries */
.card-container {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card {
    display: flex;
    gap: 1rem;
  }
}
```

## Viewport Units

```css
/* Viewport-relative sizing */
.full-height {
  height: 100vh;        /* 100% of viewport height */
  height: 100dvh;       /* Dynamic viewport (better for mobile) */
}

.half-width {
  width: 50vw;          /* 50% of viewport width */
}

/* Safe area for notched devices */
.safe-bottom {
  padding-bottom: env(safe-area-inset-bottom);
}
```

## Touch Optimization

### Touch Target Sizes

```tsx
// Minimum 44x44px touch targets (WCAG)
<button className="
  min-w-[44px] min-h-[44px]
  p-3
  flex items-center justify-center
">
  <Icon className="w-5 h-5" />
</button>

// Touch-friendly spacing
<nav className="flex flex-col">
  {links.map(link => (
    <a
      key={link.href}
      href={link.href}
      className="py-3 px-4 min-h-[44px] flex items-center"
    >
      {link.label}
    </a>
  ))}
</nav>
```

### Touch-Specific Styles

```tsx
// Disable hover effects on touch devices
<button className="
  bg-blue-600
  hover:bg-blue-700     /* Hover for mouse */
  active:bg-blue-800    /* Touch feedback */

  /* Tailwind touch variant */
  @media (hover: none) {
    &:hover { background: initial; }
  }
">
  Touch Me
</button>
```

## Image Optimization

### Responsive Images

```tsx
// Srcset for resolution switching
<img
  src="/image-800.jpg"
  srcSet="/image-400.jpg 400w, /image-800.jpg 800w, /image-1200.jpg 1200w"
  sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
  alt="Responsive image"
  className="w-full h-auto"
/>

// Picture element for art direction
<picture>
  <source media="(min-width: 1024px)" srcSet="/hero-desktop.jpg" />
  <source media="(min-width: 640px)" srcSet="/hero-tablet.jpg" />
  <img src="/hero-mobile.jpg" alt="Hero" className="w-full" />
</picture>
```

### Lazy Loading

```tsx
// Native lazy loading
<img
  src="/image.jpg"
  alt="..."
  loading="lazy"
  decoding="async"
/>

// Critical images should load eagerly
<img
  src="/hero.jpg"
  alt="Hero"
  loading="eager"
  fetchPriority="high"
/>
```

## Testing Checklist

### Device Testing
- [ ] iPhone SE (375px) - Smallest common phone
- [ ] iPhone 14 Pro (393px) - Current iPhone
- [ ] iPad (768px) - Tablet portrait
- [ ] iPad landscape (1024px) - Tablet landscape
- [ ] Desktop (1280px+) - Standard desktop
- [ ] Ultrawide (1920px+) - Large monitors

### Responsive Checks
- [ ] Content readable at all sizes
- [ ] No horizontal scroll on mobile
- [ ] Touch targets minimum 44x44px
- [ ] Text scales appropriately
- [ ] Images responsive and optimized
- [ ] Navigation accessible on mobile
- [ ] Forms usable on touch devices

## Best Practices

1. **Design for content, not devices** - Breakpoints where layout breaks
2. **Use relative units** - rem, em, %, vw instead of px
3. **Flexible images** - max-width: 100% by default
4. **Test zoom levels** - Support 200% zoom minimum
5. **Consider orientation** - Landscape vs portrait modes
6. **Optimize performance** - Mobile has slower networks

## When to Use

- Building any web application
- Creating marketing sites
- Developing web apps for mobile
- Designing component libraries
- Ensuring cross-device compatibility

## Notes

- Mobile traffic often exceeds 50% of web traffic
- Test on actual devices, not just browser emulators
- Consider Progressive Web App (PWA) for mobile
- Use device pixel ratio for high-DPI screens
