---
name: tailwindcss-spacing
description: "Spacing utilities Tailwind CSS v4.1. Margin (m-*, mx-*, my-*, mt-*, mr-*, mb-*, ml-*, -m-* negative, m-auto), Padding (p-*, px-*, py-*, pt-*, pr-*, pb-*, pl-*), Space between (space-x-*, space-y-*)."
user-invocable: false
---

# Tailwind CSS Spacing Utilities

Complete reference for Tailwind CSS v4.1 spacing utilities: margin, padding, and space-between.

## Quick Reference

### Margin Classes
- **m-{size}**: All sides margin
- **mx-{size}**: Horizontal (left + right)
- **my-{size}**: Vertical (top + bottom)
- **mt-{size}**: Top margin
- **mr-{size}**: Right margin
- **mb-{size}**: Bottom margin
- **ml-{size}**: Left margin
- **-m-{size}**: Negative margin
- **m-auto**: Auto margin (centering)

### Padding Classes
- **p-{size}**: All sides padding
- **px-{size}**: Horizontal (left + right)
- **py-{size}**: Vertical (top + bottom)
- **pt-{size}**: Top padding
- **pr-{size}**: Right padding
- **pb-{size}**: Bottom padding
- **pl-{size}**: Left padding

### Space Between Children
- **space-x-{size}**: Horizontal spacing between flex/grid children
- **space-y-{size}**: Vertical spacing between flex/grid children

## Spacing Scale

Tailwind CSS v4.1 uses a configurable spacing scale where `--spacing` is the base unit (default: 0.25rem/4px).

| Class | Value |
|-------|-------|
| 0 | 0 |
| px | 1px |
| 0.5 | calc(var(--spacing) * 2) = 0.5rem |
| 1 | calc(var(--spacing) * 4) = 1rem |
| 2 | calc(var(--spacing) * 8) = 2rem |
| 3 | calc(var(--spacing) * 12) = 3rem |
| 4 | calc(var(--spacing) * 16) = 4rem |
| 6 | calc(var(--spacing) * 24) = 6rem |
| 8 | calc(var(--spacing) * 32) = 8rem |
| 12 | calc(var(--spacing) * 48) = 12rem |
| 16 | calc(var(--spacing) * 64) = 16rem |

## Common Patterns

### Centered Container
```html
<div class="mx-auto">Centered content</div>
```

### Card with Padding
```html
<div class="p-6 bg-white rounded-lg shadow">Card content</div>
```

### Flex Items with Spacing
```html
<div class="flex space-x-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

### Stack with Vertical Spacing
```html
<div class="space-y-4">
  <p>Paragraph 1</p>
  <p>Paragraph 2</p>
  <p>Paragraph 3</p>
</div>
```

See detailed references:
- [Margin utilities →](./references/margin.md)
- [Padding utilities →](./references/padding.md)
