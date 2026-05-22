---
name: tailwindcss-effects
description: "Effects utilities Tailwind CSS v4.1. Shadows (shadow-*, shadow-color, inset-shadow-* NEW), Opacity (opacity-*), Filters (blur, brightness, contrast, grayscale, sepia), Backdrop filters (backdrop-blur-*, backdrop-brightness-*), Masks (mask-* NEW)."
user-invocable: false
---

# Tailwind CSS v4.1 Effects

Effects utilities to add shadows, filters, masks and visual effects to elements.

## Box Shadow

### Shadows Standard

```html
<!-- Preset shadows -->
<div class="shadow-none">No shadow</div>
<div class="shadow-xs">Extra small shadow</div>
<div class="shadow-sm">Small shadow</div>
<div class="shadow">Base shadow</div>
<div class="shadow-md">Medium shadow</div>
<div class="shadow-lg">Large shadow</div>
<div class="shadow-xl">Extra large shadow</div>
<div class="shadow-2xl">2XL shadow</div>
```

### Shadow Color (v4.1 NEW)

```html
<!-- Custom shadow colors -->
<div class="shadow-sm shadow-red-500">Red tinted shadow</div>
<div class="shadow shadow-blue-400">Blue tinted shadow</div>
<div class="shadow-lg shadow-purple-500/50">Purple shadow with opacity</div>
```

### Inset Shadow (v4.1 NEW)

```html
<!-- Inner shadows -->
<div class="inset-shadow-sm">Inset small shadow</div>
<div class="inset-shadow">Inset base shadow</div>
<div class="inset-shadow-lg">Inset large shadow</div>
<div class="inset-shadow-lg inset-shadow-blue-500">Inset shadow with color</div>
```

### Arbitrary Shadow Values

```html
<div class="shadow-[0_4px_12px_rgba(0,0,0,0.3)]">Custom shadow</div>
<div class="shadow-[inset_0_1px_3px_0_rgba(0,0,0,0.1)]">Custom inset</div>
```

## Opacity

### Opacity Utilities

```html
<!-- Opacity scale 0-100% -->
<div class="opacity-0">Fully transparent</div>
<div class="opacity-25">25% opacity</div>
<div class="opacity-50">50% opacity</div>
<div class="opacity-75">75% opacity</div>
<div class="opacity-100">Fully opaque</div>
```

### Opacity with Colors

```html
<!-- Shorthand opacity in color values -->
<div class="bg-red-500/50">Red with 50% opacity</div>
<div class="text-blue-600/75">Text with 75% opacity</div>
<div class="border-gray-400/25">Border with 25% opacity</div>
<div class="shadow-lg shadow-black/30">Shadow with 30% opacity</div>
```

## Filters

### Blur

```html
<div class="blur-none">No blur</div>
<div class="blur-sm">Small blur (4px)</div>
<div class="blur">Base blur (12px)</div>
<div class="blur-md">Medium blur (16px)</div>
<div class="blur-lg">Large blur (24px)</div>
<div class="blur-xl">Extra large blur (40px)</div>
<div class="blur-2xl">2XL blur (64px)</div>

<!-- Arbitrary -->
<div class="blur-[8px]">Custom blur 8px</div>
```

### Brightness

```html
<div class="brightness-50">Darken to 50%</div>
<div class="brightness-75">Darken to 75%</div>
<div class="brightness-100">Normal (100%)</div>
<div class="brightness-125">Brighten to 125%</div>
<div class="brightness-150">Brighten to 150%</div>
<div class="brightness-200">Brighten to 200%</div>
```

### Contrast

```html
<div class="contrast-50">Reduce contrast 50%</div>
<div class="contrast-75">Reduce contrast 75%</div>
<div class="contrast-100">Normal contrast (100%)</div>
<div class="contrast-125">Increase contrast 125%</div>
<div class="contrast-150">Increase contrast 150%</div>
<div class="contrast-200">Increase contrast 200%</div>
```

### Grayscale

```html
<div class="grayscale-0">No grayscale</div>
<div class="grayscale">Full grayscale (100%)</div>

<!-- Arbitrary -->
<div class="grayscale-[50%]">50% grayscale</div>
```

### Sepia

```html
<div class="sepia-0">No sepia</div>
<div class="sepia">Full sepia (100%)</div>

<!-- Arbitrary -->
<div class="sepia-[75%]">75% sepia</div>
```

### Hue Rotate

```html
<div class="hue-rotate-0">No rotation</div>
<div class="hue-rotate-15">15 degree rotation</div>
<div class="hue-rotate-30">30 degree rotation</div>
<div class="hue-rotate-60">60 degree rotation</div>
<div class="hue-rotate-90">90 degree rotation</div>
<div class="hue-rotate-180">180 degree rotation</div>

<!-- Arbitrary -->
<div class="hue-rotate-[120deg]">Custom rotation</div>
```

### Invert

```html
<div class="invert-0">No invert</div>
<div class="invert">Full invert (100%)</div>

<!-- Arbitrary -->
<div class="invert-[50%]">50% invert</div>
```

### Saturate

```html
<div class="saturate-50">Desaturate to 50%</div>
<div class="saturate-100">Normal saturation (100%)</div>
<div class="saturate-150">Increase saturation 150%</div>
<div class="saturate-200">Increase saturation 200%</div>
```

## Backdrop Filters

Applies filters to the backdrop (element behind).

### Backdrop Blur

```html
<div class="backdrop-blur-none">No blur</div>
<div class="backdrop-blur-sm">Small blur (4px)</div>
<div class="backdrop-blur">Base blur (12px)</div>
<div class="backdrop-blur-md">Medium blur (16px)</div>
<div class="backdrop-blur-lg">Large blur (24px)</div>
<div class="backdrop-blur-xl">Extra large blur (40px)</div>
```

### Backdrop Brightness

```html
<div class="backdrop-brightness-50">Darken backdrop 50%</div>
<div class="backdrop-brightness-75">Darken backdrop 75%</div>
<div class="backdrop-brightness-100">Normal (100%)</div>
<div class="backdrop-brightness-125">Brighten backdrop 125%</div>
<div class="backdrop-brightness-150">Brighten backdrop 150%</div>
```

### Backdrop Contrast

```html
<div class="backdrop-contrast-50">Reduce backdrop contrast 50%</div>
<div class="backdrop-contrast-100">Normal (100%)</div>
<div class="backdrop-contrast-150">Increase backdrop contrast 150%</div>
```

### Backdrop Grayscale

```html
<div class="backdrop-grayscale-0">No grayscale</div>
<div class="backdrop-grayscale">Full grayscale (100%)</div>
```

### Backdrop Invert

```html
<div class="backdrop-invert-0">No invert</div>
<div class="backdrop-invert">Full invert (100%)</div>
```

### Backdrop Saturate

```html
<div class="backdrop-saturate-50">Desaturate backdrop 50%</div>
<div class="backdrop-saturate-100">Normal (100%)</div>
<div class="backdrop-saturate-150">Increase backdrop saturation 150%</div>
</div>
```

### Backdrop Sepia

```html
<div class="backdrop-sepia-0">No sepia</div>
<div class="backdrop-sepia">Full sepia (100%)</div>
```

## Mask (v4.1 NEW)

### Mask Image

```html
<!-- Preset masks -->
<div class="mask-none">No mask applied</div>
<div class="mask-linear">Linear gradient mask (top to bottom)</div>
<div class="mask-radial">Radial gradient mask (center)</div>

<!-- Custom mask image -->
<div class="mask-image-[url('/images/mask.svg')]">Custom mask</div>
```

### Mask Position

```html
<div class="mask-linear mask-position-center">Center mask</div>
<div class="mask-linear mask-position-top">Top mask</div>
<div class="mask-linear mask-position-bottom">Bottom mask</div>
<div class="mask-linear mask-position-left">Left mask</div>
<div class="mask-linear mask-position-right">Right mask</div>
```

### Mask Size

```html
<div class="mask-linear mask-size-contain">Contain mask</div>
<div class="mask-linear mask-size-cover">Cover mask</div>
<div class="mask-linear mask-size-auto">Auto mask size</div>

<!-- Arbitrary -->
<div class="mask-linear mask-size-[200%_100%]">Custom size</div>
```

### Mask Repeat

```html
<div class="mask-linear mask-repeat">Repeat mask</div>
<div class="mask-linear mask-repeat-x">Repeat horizontally</div>
<div class="mask-linear mask-repeat-y">Repeat vertically</div>
<div class="mask-linear mask-no-repeat">No repeat</div>
```

## Combined Effects

### Blur + Brightness

```html
<div class="blur-md brightness-75">
  Blurred and darkened
</div>
```

### Shadow + Opacity

```html
<div class="shadow-lg shadow-blue-500/50 opacity-90">
  Shadow with tint and opacity
</div>
```

### Backdrop Blur + Brightness

```html
<div class="backdrop-blur-md backdrop-brightness-90">
  Frosted glass effect
</div>
```

### Inset Shadow + Grayscale

```html
<div class="inset-shadow inset-shadow-black/20 grayscale-50">
  Pressed effect with grayscale
</div>
```

## Responsive Effects

```html
<!-- Mobile: small blur, Tablet: medium blur, Desktop: large blur -->
<div class="blur-sm md:blur-md lg:blur-lg">
  Responsive blur
</div>

<!-- Mobile: light opacity, Desktop: darker -->
<div class="opacity-75 md:opacity-50">
  Responsive opacity
</div>

<!-- Backdrop blur on medium+ screens -->
<div class="md:backdrop-blur-lg">
  Frosted glass on desktop
</div>
```

## Dark Mode

```html
<!-- Shadow color changes in dark mode -->
<div class="shadow-md shadow-black/25 dark:shadow-black/50">
  Darker shadow in dark mode
</div>

<!-- Opacity adjustments -->
<div class="opacity-70 dark:opacity-60">
  More visible in dark mode
</div>

<!-- Different blur in dark mode -->
<div class="blur-sm dark:blur-none">
  Less blur in dark mode
</div>
```

## Configuration (v4.1)

### CSS Theme Variables

```css
@import "tailwindcss";

@theme {
  --color-shadow: #000;
  --blur-custom: 20px;
}
```

### Custom Effects

```css
@utility glass-effect {
  @apply backdrop-blur-md backdrop-brightness-90 opacity-90;
}

@utility glow {
  box-shadow: 0 0 20px var(--color-cyan-500);
}
```

## Real-world Examples

### Modal with frosted backdrop
```html
<div class="fixed inset-0 backdrop-blur-sm backdrop-brightness-75">
  <!-- Modal content -->
</div>
```

### Card with elevated shadow
```html
<div class="rounded-lg bg-white p-6 shadow-lg shadow-blue-500/10">
  Card with subtle colored shadow
</div>
```

### Image with fade-out mask
```html
<div class="mask-linear mask-position-bottom">
  <img src="image.jpg" alt="Fading image" />
</div>
```

### Glassmorphism component
```html
<div class="backdrop-blur-md bg-white/30 rounded-lg border border-white/20">
  Glass effect container
</div>
```

## Browser Support

- **Shadows**: All modern browsers
- **Filters**: Chrome 18+, Firefox 35+, Safari 6+
- **Backdrop filters**: Chrome 76+, Safari 9+, Firefox 103+
- **Masks**: Chrome 1+, Safari 4+, Firefox 53+
- **Opacity**: All modern browsers

## Performance Tips

1. Use backdrop-blur sparingly - heavy performance impact
2. Prefer opacity for transparency over rgba colors
3. Use inset-shadow instead of multiple box-shadows for layering
4. Combine related effects in custom utilities to reduce class count
5. Test backdrop effects on low-end devices

## References

- [shadows.md](references/shadows.md) - Detailed shadow configuration
- [filters.md](references/filters.md) - Filter effects reference
- [opacity.md](references/opacity.md) - Opacity and transparency
