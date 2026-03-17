---
name: tailwindcss-sizing
description: "Sizing utilities Tailwind CSS v4.1. Width (w-*, w-screen, w-full, w-auto), Height (h-*, h-screen, h-full, h-dvh NEW), Min/Max (min-w-*, max-w-*, min-h-*, max-h-*), Aspect ratio (aspect-video, aspect-square)."
user-invocable: false
---

# Tailwind CSS Sizing Utilities

Comprehensive guide to sizing utilities in Tailwind CSS v4.1, including width, height, constraints, and aspect ratio controls.

## Width Utilities

### Basic Width Classes
- `w-0` - `w-96`: Fixed widths from 0 to 384px
- `w-full` - 100% width
- `w-screen` - 100% of viewport width
- `w-auto` - Auto width
- `w-min` - min-content
- `w-max` - max-content
- `w-fit` - fit-content

### Responsive Width
Apply different widths at different breakpoints:
```html
<div class="w-full md:w-1/2 lg:w-1/3">
  Responsive width
</div>
```

## Height Utilities

### Basic Height Classes
- `h-0` - `h-96`: Fixed heights from 0 to 384px
- `h-full` - 100% height
- `h-screen` - 100% of viewport height (100vh)
- `h-auto` - Auto height
- `h-min` - min-content
- `h-max` - max-content
- `h-fit` - fit-content
- `h-dvh` - Dynamic viewport height (NEW in v4.1)

### Dynamic Viewport Height (h-dvh)
The `h-dvh` utility uses the dynamic viewport height, which accounts for browser UI elements:
```html
<div class="h-dvh">
  Full dynamic viewport height
</div>
```

## Min/Max Width

### min-width
- `min-w-0` - min-width: 0
- `min-w-full` - min-width: 100%
- `min-w-min` - min-width: min-content
- `min-w-max` - min-width: max-content
- `min-w-fit` - min-width: fit-content

### max-width
- `max-w-none` - max-width: none
- `max-w-full` - max-width: 100%
- `max-w-screen-sm` - Based on breakpoints
- `max-w-screen-md`
- `max-w-screen-lg`
- `max-w-screen-xl`
- `max-w-screen-2xl`

## Min/Max Height

### min-height
- `min-h-0` - min-height: 0
- `min-h-full` - min-height: 100%
- `min-h-screen` - min-height: 100vh
- `min-h-min` - min-height: min-content
- `min-h-max` - min-height: max-content
- `min-h-fit` - min-height: fit-content

### max-height
- `max-h-none` - max-height: none
- `max-h-full` - max-height: 100%
- `max-h-screen` - max-height: 100vh
- `max-h-min` - max-height: min-content
- `max-h-max` - max-height: max-content
- `max-h-fit` - max-height: fit-content

## Aspect Ratio

### Common Aspect Ratios
- `aspect-auto` - auto
- `aspect-square` - 1 / 1
- `aspect-video` - 16 / 9

### Custom Aspect Ratios
```html
<!-- 3:2 ratio -->
<div class="aspect-[3/2]">
  Image container
</div>
```

## Common Patterns

### Full Screen Container
```html
<div class="w-screen h-dvh bg-white">
  Full screen content
</div>
```

### Constrained Container
```html
<div class="max-w-4xl mx-auto w-full px-4">
  Content with max width and padding
</div>
```

### Image Wrapper
```html
<div class="w-full h-auto">
  <img src="image.jpg" alt="description" class="w-full h-auto object-cover" />
</div>
```

### Video Container
```html
<div class="w-full aspect-video bg-black">
  <video src="video.mp4" class="w-full h-full"></video>
</div>
```

### Sidebar Layout
```html
<div class="flex min-h-screen">
  <aside class="w-64 h-screen overflow-auto">
    Sidebar
  </aside>
  <main class="flex-1">
    Content
  </main>
</div>
```

## References
- [Width Documentation](https://tailwindcss.com/docs/width)
- [Height Documentation](https://tailwindcss.com/docs/height)
- [Min-Width Documentation](https://tailwindcss.com/docs/min-width)
- [Max-Width Documentation](https://tailwindcss.com/docs/max-width)
- [Min-Height Documentation](https://tailwindcss.com/docs/min-height)
- [Max-Height Documentation](https://tailwindcss.com/docs/max-height)
- [Aspect Ratio Documentation](https://tailwindcss.com/docs/aspect-ratio)
