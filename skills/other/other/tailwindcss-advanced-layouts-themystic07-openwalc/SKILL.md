---
name: tailwindcss-advanced-layouts
description: Tailwind CSS advanced layout techniques including CSS Grid and Flexbox patterns
---

# Tailwind CSS Advanced Layout Techniques

## CSS Grid Mastery

### Complex Grid Layouts

```html
<!-- Holy Grail Layout -->
<div class="grid min-h-screen grid-rows-[auto_1fr_auto]">
  <header class="bg-white shadow">Header</header>
  <div class="grid grid-cols-[250px_1fr_300px]">
    <aside class="bg-gray-50 p-4">Sidebar</aside>
    <main class="p-6">Main Content</main>
    <aside class="bg-gray-50 p-4">Right Sidebar</aside>
  </div>
  <footer class="bg-gray-800 text-white">Footer</footer>
</div>

<!-- Responsive Holy Grail -->
<div class="grid min-h-screen grid-rows-[auto_1fr_auto]">
  <header>Header</header>
  <div class="grid grid-cols-1 md:grid-cols-[250px_1fr] lg:grid-cols-[250px_1fr_300px]">
    <aside class="order-2 md:order-1">Sidebar</aside>
    <main class="order-1 md:order-2">Main</main>
    <aside class="order-3 hidden lg:block">Right</aside>
  </div>
  <footer>Footer</footer>
</div>
```

### Grid Template Areas

```css
@utility grid-areas-dashboard {
  grid-template-areas:
    "header header header"
    "nav main aside"
    "nav footer footer";
}

@utility area-header { grid-area: header; }
@utility area-nav { grid-area: nav; }
@utility area-main { grid-area: main; }
@utility area-aside { grid-area: aside; }
@utility area-footer { grid-area: footer; }
```

```html
<div class="grid grid-areas-dashboard grid-cols-[200px_1fr_250px] grid-rows-[60px_1fr_40px] min-h-screen">
  <header class="area-header bg-white shadow">Header</header>
  <nav class="area-nav bg-gray-100">Navigation</nav>
  <main class="area-main p-6">Main Content</main>
  <aside class="area-aside bg-gray-50 p-4">Sidebar</aside>
  <footer class="area-footer bg-gray-800 text-white">Footer</footer>
</div>
```

### Auto-Fill and Auto-Fit Grids

```html
<!-- Auto-fill: Creates as many tracks as fit, even empty ones -->
<div class="grid grid-cols-[repeat(auto-fill,minmax(250px,1fr))] gap-6">
  <div class="bg-white rounded-lg shadow p-4">Card 1</div>
  <div class="bg-white rounded-lg shadow p-4">Card 2</div>
  <div class="bg-white rounded-lg shadow p-4">Card 3</div>
</div>

<!-- Auto-fit: Collapses empty tracks -->
<div class="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-6">
  <!-- Cards stretch to fill available space -->
</div>

<!-- With arbitrary values -->
<div class="grid grid-cols-[repeat(auto-fill,minmax(min(100%,300px),1fr))] gap-4">
  <!-- Handles edge case where container is smaller than minmax min -->
</div>
```

### Subgrid

```css
/* Enable subgrid in v4 */
@utility subgrid-cols {
  grid-template-columns: subgrid;
}

@utility subgrid-rows {
  grid-template-rows: subgrid;
}
```

```html
<div class="grid grid-cols-4 gap-4">
  <!-- Span 2 columns but align children to parent grid -->
  <div class="col-span-2 grid subgrid-cols gap-4">
    <div>Aligned to parent column 1</div>
    <div>Aligned to parent column 2</div>
  </div>
</div>
```

## Advanced Flexbox Patterns

### Space Distribution

```html
<!-- Equal spacing with first/last at edges -->
<div class="flex justify-between">
  <div>First</div>
  <div>Second</div>
  <div>Third</div>
</div>

<!-- Equal spacing everywhere including edges -->
<div class="flex justify-around">
  <div>Item</div>
  <div>Item</div>
  <div>Item</div>
</div>

<!-- Double space between items vs edges -->
<div class="flex justify-evenly">
  <div>Item</div>
  <div>Item</div>
  <div>Item</div>
</div>
```

### Flexible Item Sizing

```html
<!-- Items share space equally -->
<div class="flex">
  <div class="flex-1">1/3</div>
  <div class="flex-1">1/3</div>
  <div class="flex-1">1/3</div>
</div>

<!-- First item takes 2x space -->
<div class="flex">
  <div class="flex-[2]">2/4</div>
  <div class="flex-1">1/4</div>
  <div class="flex-1">1/4</div>
</div>

<!-- Fixed + flexible -->
<div class="flex">
  <div class="w-64 shrink-0">Fixed 256px</div>
  <div class="flex-1 min-w-0">Flexible (can shrink)</div>
</div>

<!-- Prevent shrinking with text overflow -->
<div class="flex min-w-0">
  <div class="shrink-0">Icon</div>
  <div class="min-w-0 truncate">Very long text that should truncate</div>
</div>
```

### Masonry-Like with Flexbox

```html
<!-- Column-based masonry -->
<div class="flex flex-col flex-wrap h-[800px] gap-4">
  <div class="w-[calc(33.333%-1rem)] h-48">Item 1</div>
  <div class="w-[calc(33.333%-1rem)] h-64">Item 2</div>
  <div class="w-[calc(33.333%-1rem)] h-32">Item 3</div>
  <!-- Items flow vertically then wrap to next column -->
</div>
```

## Container Queries

### Basic Container Queries

```css
@plugin "@tailwindcss/container-queries";
```

```html
<!-- Define container -->
<div class="@container">
  <!-- Respond to container width -->
  <div class="flex flex-col @md:flex-row @lg:grid @lg:grid-cols-3 gap-4">
    <div>Item 1</div>
    <div>Item 2</div>
    <div>Item 3</div>
  </div>
</div>
```

### Named Containers

```html
<!-- Multiple named containers -->
<div class="@container/sidebar">
  <nav class="@[200px]/sidebar:flex-col @[300px]/sidebar:flex-row">
    Navigation
  </nav>
</div>

<div class="@container/main">
  <article class="@[600px]/main:prose-lg @[900px]/main:prose-xl">
    Content
  </article>
</div>
```

### Container Query Units

```html
<!-- Size relative to container -->
<div class="@container">
  <h1 class="text-[5cqw]">Scales with container width</h1>
  <p class="text-[3cqi]">Scales with container inline size</p>
</div>
```

## Position and Layering

### Sticky Positioning

```html
<!-- Sticky header -->
<header class="sticky top-0 z-50 bg-white/80 backdrop-blur-sm border-b">
  Navigation
</header>

<!-- Sticky sidebar -->
<aside class="sticky top-20 h-[calc(100vh-5rem)] overflow-auto">
  Sidebar content
</aside>

<!-- Sticky table header -->
<div class="overflow-auto max-h-96">
  <table>
    <thead class="sticky top-0 bg-white shadow">
      <tr>
        <th class="sticky left-0 bg-white z-10">Corner cell</th>
        <th>Column 2</th>
      </tr>
    </thead>
    <tbody>...</tbody>
  </table>
</div>
```

### Fixed Elements

```html
<!-- Fixed bottom navigation (mobile) -->
<nav class="fixed bottom-0 inset-x-0 z-50 bg-white border-t md:hidden">
  <div class="flex justify-around py-2">
    <a href="#">Home</a>
    <a href="#">Search</a>
    <a href="#">Profile</a>
  </div>
</nav>

<!-- Fixed action button -->
<button class="fixed bottom-6 right-6 z-40 rounded-full bg-brand-500 p-4 shadow-lg">
  <PlusIcon />
</button>
```

### Z-Index Management

```css
@theme {
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-fixed: 300;
  --z-modal-backdrop: 400;
  --z-modal: 500;
  --z-popover: 600;
  --z-tooltip: 700;
  --z-toast: 800;
}

@utility z-dropdown { z-index: var(--z-dropdown); }
@utility z-sticky { z-index: var(--z-sticky); }
@utility z-fixed { z-index: var(--z-fixed); }
@utility z-modal-backdrop { z-index: var(--z-modal-backdrop); }
@utility z-modal { z-index: var(--z-modal); }
@utility z-popover { z-index: var(--z-popover); }
@utility z-tooltip { z-index: var(--z-tooltip); }
@utility z-toast { z-index: var(--z-toast); }
```

## Overflow and Scrolling

### Custom Scrollbars

```css
@utility scrollbar-thin {
  scrollbar-width: thin;
}

@utility scrollbar-none {
  scrollbar-width: none;
  -ms-overflow-style: none;
}

@utility scrollbar-none::-webkit-scrollbar {
  display: none;
}

/* Custom scrollbar styling */
@utility scrollbar-custom {
  scrollbar-color: oklch(0.7 0 0) oklch(0.95 0 0);
}

@utility scrollbar-custom::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

@utility scrollbar-custom::-webkit-scrollbar-track {
  background: oklch(0.95 0 0);
  border-radius: 4px;
}

@utility scrollbar-custom::-webkit-scrollbar-thumb {
  background: oklch(0.7 0 0);
  border-radius: 4px;
}

@utility scrollbar-custom::-webkit-scrollbar-thumb:hover {
  background: oklch(0.5 0 0);
}
```

### Scroll Snap

```html
<!-- Horizontal carousel -->
<div class="flex snap-x snap-mandatory overflow-x-auto gap-4 pb-4">
  <div class="snap-start shrink-0 w-80">Card 1</div>
  <div class="snap-start shrink-0 w-80">Card 2</div>
  <div class="snap-start shrink-0 w-80">Card 3</div>
</div>

<!-- Full-page sections -->
<div class="h-screen snap-y snap-mandatory overflow-y-auto">
  <section class="h-screen snap-start">Section 1</section>
  <section class="h-screen snap-start">Section 2</section>
  <section class="h-screen snap-start">Section 3</section>
</div>

<!-- Snap with padding -->
<div class="snap-x scroll-pl-6 overflow-x-auto">
  <div class="snap-start">...</div>
</div>
```

### Scroll Margin for Anchors

```html
<!-- Offset for fixed header -->
<section id="about" class="scroll-mt-20">
  <!-- Content appears below fixed header when linked -->
</section>
```

## Aspect Ratio and Object Fit

### Responsive Aspect Ratios

```html
<!-- Fixed aspect ratio container -->
<div class="aspect-video bg-gray-100">
  <video class="h-full w-full object-cover">...</video>
</div>

<div class="aspect-square rounded-full overflow-hidden">
  <img src="avatar.jpg" class="h-full w-full object-cover" />
</div>

<!-- Custom aspect ratio -->
<div class="aspect-[4/3]">4:3 content</div>
<div class="aspect-[21/9]">Ultra-wide content</div>
```

### Object Positioning

```html
<!-- Focus on specific part of image -->
<div class="h-64 overflow-hidden">
  <img
    src="portrait.jpg"
    class="h-full w-full object-cover object-top"
  />
</div>

<!-- Arbitrary object position -->
<img class="object-cover object-[25%_75%]" src="..." />
```

## Advanced Spacing

### Logical Properties

```html
<!-- Works for LTR and RTL -->
<div class="ps-4 pe-6 ms-auto">
  Padding and margin that respect text direction
</div>

<!-- Block direction (vertical in horizontal writing modes) -->
<div class="pbs-4 pbe-6 mbs-auto">
  Block-direction spacing
</div>
```

### Space Between with Dividers

```html
<!-- Dividers between items -->
<ul class="divide-y divide-gray-200">
  <li class="py-4">Item 1</li>
  <li class="py-4">Item 2</li>
  <li class="py-4">Item 3</li>
</ul>

<!-- Horizontal dividers -->
<div class="flex divide-x divide-gray-200">
  <div class="px-4">Section 1</div>
  <div class="px-4">Section 2</div>
  <div class="px-4">Section 3</div>
</div>
```

### Negative Margins for Bleeds

```html
<!-- Full-bleed image in padded container -->
<article class="px-6">
  <p>Padded content</p>
  <img src="hero.jpg" class="-mx-6 w-[calc(100%+3rem)]" />
  <p>More padded content</p>
</article>

<!-- Pull quote that breaks out -->
<div class="max-w-prose mx-auto px-4">
  <p>Normal content...</p>
  <blockquote class="-mx-8 md:-mx-16 px-8 md:px-16 py-8 bg-gray-100">
    Featured quote that extends beyond content width
  </blockquote>
</div>
```

## Multi-Column Layout

### Text Columns

```html
<!-- Responsive columns -->
<div class="columns-1 sm:columns-2 lg:columns-3 gap-8">
  <p>Content flows across columns...</p>
</div>

<!-- Fixed-width columns -->
<div class="columns-[300px] gap-6">
  <p>Creates as many 300px columns as fit</p>
</div>

<!-- Prevent breaks inside elements -->
<div class="columns-2">
  <div class="break-inside-avoid mb-4">
    Card that stays together
  </div>
</div>
```

## Responsive Patterns

### Container Queries + Media Queries

```html
<div class="@container">
  <div class="
    /* Container query for component-level responsiveness */
    @md:flex @md:gap-4

    /* Media query for page-level responsiveness */
    lg:grid lg:grid-cols-2
  ">
    Content
  </div>
</div>
```

### Breakpoint-Based Visibility

```html
<!-- Show different content per breakpoint -->
<nav>
  <!-- Mobile menu button -->
  <button class="md:hidden">Menu</button>

  <!-- Desktop navigation -->
  <ul class="hidden md:flex gap-4">
    <li>Home</li>
    <li>About</li>
    <li>Contact</li>
  </ul>
</nav>
```

### Fluid Sizing with Clamp

```html
<!-- Fluid padding -->
<section class="py-[clamp(2rem,5vw,6rem)] px-[clamp(1rem,3vw,4rem)]">
  Content with responsive padding
</section>

<!-- Fluid max-width -->
<div class="mx-auto w-full max-w-[clamp(300px,90vw,1200px)]">
  Responsive container
</div>
```

## Print Styles

```html
<!-- Hide elements when printing -->
<nav class="print:hidden">Navigation</nav>

<!-- Show only when printing -->
<div class="hidden print:block">Print-only content</div>

<!-- Print-specific styles -->
<article class="print:text-black print:bg-white">
  <h1 class="text-2xl print:text-xl">Heading</h1>
  <a href="..." class="text-blue-500 print:text-black print:underline">
    Link (shows as text when printed)
  </a>
</article>

<!-- Prevent page breaks -->
<div class="print:break-inside-avoid">
  Keep this content together on one page
</div>

<!-- Force page break -->
<div class="print:break-before-page">
  Start on new page
</div>
```

## Best Practices

### 1. Use Modern Layout Methods

```html
<!-- Prefer Grid for 2D layouts -->
<div class="grid grid-cols-3 gap-4">

<!-- Prefer Flexbox for 1D layouts -->
<div class="flex items-center gap-2">
```

### 2. Handle Edge Cases

```html
<!-- Prevent flex item from overflowing -->
<div class="flex min-w-0">
  <div class="min-w-0 truncate">Long text</div>
</div>

<!-- Prevent grid blowout -->
<div class="grid grid-cols-1 min-w-0">
  <div class="overflow-hidden">Content that might overflow</div>
</div>
```

### 3. Use Semantic Sizing

```html
<!-- Prefer max-w-prose for reading content -->
<article class="max-w-prose mx-auto">

<!-- Use container for page sections -->
<div class="container mx-auto px-4">
```

### 4. Test All Breakpoints

Create systematic tests for all responsive layouts to ensure they work at every breakpoint.
