---
description: Complete Tailwind CSS utility classes reference - Layout, spacing, typography, colors, borders, effects
user-invocable: false
---

# Tailwind CSS Utility Classes

Complete reference for all Tailwind CSS utility classes organized by category.

## Layout Utilities

### Display

```html
<!-- Block, inline, flex, grid -->
<div class="block">Block</div>
<div class="inline">Inline</div>
<div class="flex">Flex</div>
<div class="grid">Grid</div>
<div class="hidden">Hidden</div>
```

**Docs:** `display.mdx`

### Flexbox

```html
<!-- Container -->
<div class="flex flex-row flex-wrap items-center justify-between gap-4">
  <!-- Items -->
  <div class="flex-1">Flex item</div>
  <div class="flex-shrink-0">Fixed</div>
</div>
```

**Docs:** `flex.mdx`, `flex-direction.mdx`, `flex-wrap.mdx`, `justify-content.mdx`, `align-items.mdx`, `gap.mdx`

### Grid

```html
<!-- Grid container -->
<div class="grid grid-cols-3 gap-4">
  <div>Item 1</div>
  <div class="col-span-2">Item 2 (spans 2 columns)</div>
</div>

<!-- Responsive grid -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
  <!-- Grid items -->
</div>
```

**Docs:** `grid-template-columns.mdx`, `grid-column.mdx`, `grid-row.mdx`, `gap.mdx`

### Position

```html
<div class="relative">
  <div class="absolute top-0 right-0">Absolute</div>
</div>
<div class="fixed bottom-4 right-4">Fixed</div>
<div class="sticky top-0">Sticky header</div>
```

**Docs:** `position.mdx`, `top-right-bottom-left.mdx`, `z-index.mdx`

## Spacing Utilities

### Padding

```html
<div class="p-4">All sides</div>
<div class="px-6 py-3">Horizontal & vertical</div>
<div class="pt-8 pr-4 pb-6 pl-2">Individual sides</div>
```

**Scale:** `0, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 56, 64`

**Docs:** `padding.mdx`

### Margin

```html
<div class="m-4">All sides</div>
<div class="mx-auto">Center horizontally</div>
<div class="-mt-4">Negative margin</div>
```

**Docs:** `margin.mdx`

### Gap

```html
<div class="flex gap-4">Flex gap</div>
<div class="grid gap-x-6 gap-y-4">Grid gap (x/y)</div>
```

**Docs:** `gap.mdx`

## Typography Utilities

### Font Family

```html
<p class="font-sans">Sans-serif</p>
<p class="font-serif">Serif</p>
<p class="font-mono">Monospace</p>
```

**Docs:** `font-family.mdx`

### Font Size

```html
<p class="text-xs">Extra small</p>
<p class="text-sm">Small</p>
<p class="text-base">Base</p>
<p class="text-lg">Large</p>
<p class="text-xl">Extra large</p>
<p class="text-2xl">2XL</p>
<p class="text-3xl">3XL</p>
```

**Docs:** `font-size.mdx`

### Font Weight

```html
<p class="font-thin">Thin (100)</p>
<p class="font-normal">Normal (400)</p>
<p class="font-semibold">Semibold (600)</p>
<p class="font-bold">Bold (700)</p>
```

**Docs:** `font-weight.mdx`

### Text Alignment

```html
<p class="text-left">Left</p>
<p class="text-center">Center</p>
<p class="text-right">Right</p>
<p class="text-justify">Justify</p>
```

**Docs:** `text-align.mdx`

### Line Height

```html
<p class="leading-tight">Tight (1.25)</p>
<p class="leading-normal">Normal (1.5)</p>
<p class="leading-relaxed">Relaxed (1.625)</p>
```

**Docs:** `line-height.mdx`

## Color Utilities

### Text Color

```html
<p class="text-black">Black</p>
<p class="text-gray-500">Gray 500</p>
<p class="text-blue-600">Blue 600</p>
<p class="text-red-500 dark:text-red-400">Red (dark mode)</p>
```

**Scale:** `50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950`

**Docs:** `color.mdx`, `colors.mdx`

### Background Color

```html
<div class="bg-white">White</div>
<div class="bg-gray-100">Gray 100</div>
<div class="bg-blue-500">Blue 500</div>
```

**Docs:** `background-color.mdx`

### Border Color

```html
<div class="border border-gray-300">Gray border</div>
<div class="border-2 border-blue-500">Blue border</div>
```

**Docs:** `border-color.mdx`

## Border Utilities

### Border Width

```html
<div class="border">Default (1px)</div>
<div class="border-2">2px all sides</div>
<div class="border-t-4">Top 4px</div>
<div class="border-x-2">Horizontal 2px</div>
```

**Docs:** `border-width.mdx`

### Border Radius

```html
<div class="rounded">Small (0.25rem)</div>
<div class="rounded-md">Medium (0.375rem)</div>
<div class="rounded-lg">Large (0.5rem)</div>
<div class="rounded-full">Full (9999px)</div>
<div class="rounded-t-lg">Top corners only</div>
```

**Docs:** `border-radius.mdx`

## Effect Utilities

### Shadow

```html
<div class="shadow">Default shadow</div>
<div class="shadow-md">Medium shadow</div>
<div class="shadow-lg">Large shadow</div>
<div class="shadow-xl">Extra large shadow</div>
```

**Docs:** `box-shadow.mdx`, `text-shadow.mdx`

### Opacity

```html
<div class="opacity-0">Invisible</div>
<div class="opacity-50">Half visible</div>
<div class="opacity-100">Fully visible</div>
```

**Docs:** `opacity.mdx`

### Filters

```html
<img class="blur-sm" src="..." />
<img class="brightness-75" src="..." />
<img class="contrast-125" src="..." />
<img class="grayscale" src="..." />
```

**Docs:** `filter-*.mdx` (blur, brightness, contrast, etc.)

## State Variants

### Hover

```html
<button class="bg-blue-500 hover:bg-blue-600">
  Hover me
</button>
```

### Focus

```html
<input class="border focus:border-blue-500 focus:ring-2 focus:ring-blue-200" />
```

### Active

```html
<button class="bg-blue-500 active:bg-blue-700">
  Click me
</button>
```

### Disabled

```html
<button class="bg-blue-500 disabled:bg-gray-300 disabled:cursor-not-allowed" disabled>
  Disabled
</button>
```

**Docs:** `hover-focus-and-other-states.mdx`

## Documentation Index

| Category | Files |
|----------|-------|
| Layout | `display.mdx`, `flex-*.mdx`, `grid-*.mdx`, `position.mdx` |
| Spacing | `padding.mdx`, `margin.mdx`, `gap.mdx` |
| Typography | `font-*.mdx`, `text-*.mdx`, `line-*.mdx` |
| Colors | `color.mdx`, `background-color.mdx`, `border-color.mdx` |
| Borders | `border-*.mdx`, `border-radius.mdx` |
| Effects | `box-shadow.mdx`, `opacity.mdx`, `filter-*.mdx` |
| States | `hover-focus-and-other-states.mdx` |
