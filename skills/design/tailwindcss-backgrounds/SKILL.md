---
name: tailwindcss-backgrounds
description: "Background utilities Tailwind CSS v4.1. Colors (bg-{color}, palette OKLCH P3), Gradients (bg-linear-*, bg-radial-*, bg-conic-* NEW), Images (bg-cover, bg-contain, bg-repeat), Blend modes."
user-invocable: false
---

# Tailwind CSS Backgrounds Skill

Complete reference for background utilities in Tailwind CSS v4.1, including colors, gradients, images, positioning, sizing, and blend modes.

## Background Colors

Use `bg-{color}` utilities to set background colors with the modernized OKLCH color palette.

```html
<!-- Basic colors -->
<div class="bg-red-500"></div>
<div class="bg-blue-600"></div>
<div class="bg-emerald-400"></div>

<!-- Opacity modifiers -->
<div class="bg-blue-500/50"></div>
<div class="bg-slate-900/75"></div>
```

### Color Palette (OKLCH P3)

The default Tailwind palette uses OKLCH color space for perceptually uniform colors across the wider P3 gamut:

- **Neutrals**: slate, gray, zinc, neutral, stone
- **Colors**: red, orange, amber, yellow, lime, green, emerald, teal, cyan, sky, blue, indigo, violet, purple, fuchsia, pink, rose

Each color has 11 shades: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950

## Linear Gradients

Create linear gradients using `bg-linear-*` utilities with direction and color stops.

```html
<!-- Directions -->
<div class="bg-linear-to-t from-blue-500 to-purple-500"></div>
<div class="bg-linear-to-r from-green-400 via-blue-500 to-purple-600"></div>
<div class="bg-linear-to-br from-yellow-200 to-red-600"></div>

<!-- Available directions -->
<!-- bg-linear-to-t, to-tr, to-r, to-br, to-b, to-bl, to-l, to-tl -->

<!-- Custom angles -->
<div class="bg-linear-45 from-slate-400 to-slate-600"></div>
<div class="bg-linear-180 from-indigo-500 to-pink-500"></div>
```

### Direction Utilities

- `bg-linear-to-t` - to top
- `bg-linear-to-tr` - to top right
- `bg-linear-to-r` - to right
- `bg-linear-to-br` - to bottom right
- `bg-linear-to-b` - to bottom
- `bg-linear-to-bl` - to bottom left
- `bg-linear-to-l` - to left
- `bg-linear-to-tl` - to top left
- `bg-linear-<angle>` - custom angle (e.g., `bg-linear-45`)

## Radial Gradients

Create radial gradients using `bg-radial-*` utilities.

```html
<div class="bg-radial from-yellow-400 to-slate-900"></div>
<div class="bg-radial from-purple-200 via-blue-400 to-slate-950"></div>
```

## Conic Gradients (NEW in v4.1)

Create conic gradients using `bg-conic-*` utilities, perfect for color wheels and circular patterns.

```html
<div class="bg-conic-0 from-red-500 to-red-500"></div>
<div class="bg-conic-45 from-blue-400 via-purple-500 to-pink-400"></div>
<div class="bg-conic-[from_45deg] from-slate-400 to-slate-600"></div>
```

## Gradient Color Stops

Control gradient color stops with `from-*`, `via-*`, and `to-*` utilities.

```html
<!-- Two colors -->
<div class="bg-linear-to-r from-blue-500 to-purple-500"></div>

<!-- Three colors -->
<div class="bg-linear-to-r from-green-400 via-blue-500 to-purple-600"></div>

<!-- Custom positions -->
<div class="bg-linear-to-r from-blue-500 from-0% to-purple-500 to-100%"></div>
```

## Background Images

Use `bg-[url(...)]` to apply custom background images.

```html
<div class="bg-[url(/img/mountains.jpg)]"></div>
<div class="bg-[url(data:image/svg+xml,...)]"></div>
```

## Background Size

Control how background images are sized.

```html
<!-- Predefined sizes -->
<div class="bg-cover"><!-- Fills container, may crop --></div>
<div class="bg-contain"><!-- Scales to fit, may show blank space --></div>

<!-- Custom sizes -->
<div class="bg-[size:10rem]"></div>
<div class="bg-[size:50%]"></div>
<div class="bg-[size:200px_100px]"></div>
```

## Background Position

Position the background image within its container.

```html
<!-- Predefined positions -->
<div class="bg-top-left"></div>
<div class="bg-top"></div>
<div class="bg-top-right"></div>
<div class="bg-left"></div>
<div class="bg-center"></div>
<div class="bg-right"></div>
<div class="bg-bottom-left"></div>
<div class="bg-bottom"></div>
<div class="bg-bottom-right"></div>

<!-- Custom positions -->
<div class="bg-[position:25%_75%]"></div>
```

## Background Repeat

Control how background images repeat.

```html
<!-- Repeat -->
<div class="bg-repeat"><!-- Tile in both directions --></div>
<div class="bg-repeat-x"><!-- Tile horizontally --></div>
<div class="bg-repeat-y"><!-- Tile vertically --></div>

<!-- No repeat -->
<div class="bg-no-repeat"><!-- Single image --></div>
```

## Background Blend Modes

Combine background colors with images using blend modes.

```html
<div class="bg-blue-500 bg-[url(...)] bg-blend-multiply"></div>
<div class="bg-slate-700 bg-[url(...)] bg-blend-overlay"></div>
<div class="bg-amber-400 bg-[url(...)] bg-blend-soft-light"></div>

<!-- Available blend modes -->
<!-- multiply, screen, overlay, darken, lighten, color-dodge,
     color-burn, hard-light, soft-light, difference, exclusion,
     hue, saturation, color, luminosity -->
```

## Complete Examples

### Color Background with Opacity

```html
<div class="bg-slate-900/50 px-6 py-8 rounded-lg">
  Content with translucent background
</div>
```

### Gradient Overlay on Image

```html
<div class="bg-[url(/img/hero.jpg)] bg-cover bg-center
           bg-linear-to-br from-black/40 to-transparent
           h-96 flex items-center justify-center">
  <h1 class="text-white text-4xl font-bold">Hero Title</h1>
</div>
```

### Gradient with Multiple Stops

```html
<div class="bg-linear-to-r
           from-emerald-500 from-0%
           via-blue-500 via-50%
           to-purple-600 to-100%
           h-20 rounded-lg"></div>
```

### Conic Gradient (Color Wheel)

```html
<div class="w-32 h-32 rounded-full
           bg-conic-0
           from-red-500 via-yellow-500 via-green-500 via-blue-500 via-purple-500 to-red-500"></div>
```

### Image with Blend Mode

```html
<div class="w-full h-80
           bg-blue-600
           bg-[url(/img/pattern.png)] bg-cover bg-center
           bg-blend-multiply
           rounded-lg"></div>
```

## Customization

Extend background utilities in your Tailwind config:

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  theme: {
    extend: {
      colors: {
        brand: {
          50: 'oklch(0.971 0.013 17.38)',
          500: 'oklch(0.637 0.237 25.331)',
          950: 'oklch(0.258 0.092 26.042)',
        },
      },
      backgroundImage: {
        gradient: 'url(\'/img/gradient.png\')',
      },
    },
  },
}
```

## Performance Tips

1. **Use color utilities** instead of hex values for better optimization
2. **Combine with `bg-no-repeat`** and sizing to prevent unwanted repetition
3. **Layer gradients** using multiple background utilities for complex effects
4. **Use opacity modifiers** (`/50`) instead of rgba for better tree-shaking
5. **Prefer conic/radial gradients** over images when possible for smaller file sizes
