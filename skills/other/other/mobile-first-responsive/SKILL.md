---
name: mobile-first-responsive
description: Mobile-first responsive design with Tailwind CSS v4. Use when building responsive layouts, configuring breakpoints, creating touch-friendly UIs, implementing dark mode, or optimizing for mobile devices. Covers grid/flexbox patterns, responsive typography, image optimization, and accessibility.
---

# Mobile-First Responsive Design

## Tailwind v4 Breakpoints (CSS-First Config)

Default breakpoints (mobile-first, min-width):

| Prefix | Width | Use Case |
|--------|-------|----------|
| (none) | 0px | Mobile base |
| `sm` | 640px (40rem) | Large phones |
| `md` | 768px (48rem) | Tablets |
| `lg` | 1024px (64rem) | Laptops |
| `xl` | 1280px (80rem) | Desktops |
| `2xl` | 1536px (96rem) | Large screens |

### Custom Breakpoints (v4 syntax)

```css
@import "tailwindcss";
@theme {
  --breakpoint-xs: 475px;
  --breakpoint-3xl: 1920px;
}
```

Override defaults:
```css
@theme {
  --breakpoint-*: initial;
  --breakpoint-mobile: 480px;
  --breakpoint-tablet: 768px;
  --breakpoint-desktop: 1024px;
}
```

### Max-Width Variants

```html
<!-- Hide on screens >= sm -->
<div class="max-sm:hidden">Mobile only</div>

<!-- Target range: md to lg only -->
<div class="md:max-lg:grid-cols-2">Tablet layout</div>
```

## Layout Patterns

### Responsive Grid

```html
<!-- 1 col mobile -> 2 col tablet -> 4 col desktop -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
  <div>Item</div>
</div>
```

### Flexbox Navigation

```html
<nav class="flex flex-col sm:flex-row sm:items-center gap-4">
  <a href="/" class="font-bold">Logo</a>
  <div class="flex flex-col sm:flex-row gap-2 sm:gap-4 sm:ml-auto">
    <a href="#">Link</a>
  </div>
</nav>
```

### Card Grid

```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
  <article class="p-4 rounded-lg bg-white dark:bg-gray-800 shadow">
    <img class="w-full aspect-video object-cover rounded"
         src="image.jpg" alt="" loading="lazy">
    <h3 class="mt-4 text-lg font-semibold">Title</h3>
    <p class="mt-2 text-gray-600 dark:text-gray-400">Description</p>
  </article>
</div>
```

## Touch-Friendly UI

### WCAG Target Sizes

- **Level AA (2.5.8)**: 24x24px minimum
- **Level AAA (2.5.5)**: 44x44px recommended
- **Spacing**: 8-12px between targets

```html
<!-- Touch-friendly button: min-h-11 = 44px -->
<button class="min-h-11 min-w-11 px-4 py-2 rounded-lg
               active:scale-95 touch-manipulation">
  Tap Me
</button>

<!-- Touch-friendly link list -->
<ul class="divide-y">
  <li>
    <a href="#" class="block py-3 px-4 min-h-11 flex items-center">
      Menu Item
    </a>
  </li>
</ul>
```

### Touch Utilities

```html
<!-- Prevent double-tap zoom, reduce touch delay -->
<button class="touch-manipulation">Fast tap</button>

<!-- Disable text selection on interactive elements -->
<div class="select-none">Draggable</div>
```

## Responsive Typography

### Using @tailwindcss/typography

```html
<article class="prose prose-sm md:prose-base lg:prose-lg dark:prose-invert">
  <h1>Heading</h1>
  <p>Content scales with viewport.</p>
</article>
```

### Fluid Typography with clamp()

```css
@theme {
  --font-size-fluid-sm: clamp(0.875rem, 0.8rem + 0.25vw, 1rem);
  --font-size-fluid-base: clamp(1rem, 0.9rem + 0.5vw, 1.25rem);
  --font-size-fluid-lg: clamp(1.25rem, 1rem + 1vw, 2rem);
  --font-size-fluid-xl: clamp(1.5rem, 1rem + 2vw, 3rem);
}
```

```html
<h1 class="text-fluid-xl font-bold">Responsive Heading</h1>
```

## Image Optimization

```html
<!-- Lazy loading with aspect ratio -->
<img src="image.jpg"
     alt="Description"
     loading="lazy"
     decoding="async"
     class="w-full aspect-video object-cover">

<!-- Responsive images with srcset -->
<img srcset="small.jpg 480w, medium.jpg 768w, large.jpg 1200w"
     sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
     src="medium.jpg"
     alt="Description"
     loading="lazy"
     class="w-full h-auto">

<!-- Background image placeholder pattern -->
<div class="relative bg-gray-200 dark:bg-gray-700">
  <img src="image.jpg"
       alt=""
       loading="lazy"
       class="w-full h-auto"
       onload="this.parentElement.classList.remove('bg-gray-200', 'dark:bg-gray-700')">
</div>
```

## Dark Mode

### System Preference (default)

```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
  Content adapts to OS setting
</div>
```

### Manual Toggle

```css
@import "tailwindcss";
@custom-variant dark (&:where(.dark, .dark *));
```

```html
<html class="dark">
  <body class="bg-white dark:bg-gray-900">
    <!-- dark: utilities active -->
  </body>
</html>
```

```javascript
// Toggle implementation
const toggle = () => {
  document.documentElement.classList.toggle('dark');
  localStorage.theme = document.documentElement.classList.contains('dark')
    ? 'dark' : 'light';
};

// On load: respect saved preference or system
document.documentElement.classList.toggle('dark',
  localStorage.theme === 'dark' ||
  (!('theme' in localStorage) &&
   matchMedia('(prefers-color-scheme: dark)').matches)
);
```

## Component Examples

See [references/components.md](references/components.md) for complete patterns:
- Responsive Navbar with mobile menu
- Card layouts
- Form inputs
- Modal dialogs

## Accessibility Checklist

See [references/a11y-checklist.md](references/a11y-checklist.md) for testing requirements.
