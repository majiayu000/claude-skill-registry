---
name: applying-responsive-standards
description: Rules for mobile-first responsive design using Tailwind CSS. Use on every UI component to ensure cross-device compatibility.
---

# Responsive Design Standards

## When to use this skill
- Adding any new UI element or layout.
- Fixing layout bugs on mobile or tablet.

## Coding Style
- **Mobile First**: Write base styles for mobile, then use `md:`, `lg:`, `xl:` to upgrade for larger screens.
- **Stacking**: Use `flex-col` on mobile and `flex-row` on desktop (`md:flex-row`).
- **Grid**: Default to 1 column on mobile, 2 on tablet, and 3+ on desktop.

## Example
```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <!-- Tour Cards -->
</div>
```

## Instructions
- **Testing**: Frequently resize the browser or use DevTools device emulator.
- **Padding**: Increase horizontal padding on desktop (`px-4` vs `md:px-20`).
