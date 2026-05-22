---
name: styling-patterns
# prettier-ignore
description: DaisyUI v5 design system. Use for backgrounds, borders, text sizes, opacity, semantic colors, and spacing.
---

# Styling Patterns

## Quick Start

```html
<!-- ✅ Correct: Proper background hierarchy -->
<div class="bg-base-200 p-6">
	<div class="card bg-base-100 p-4 shadow-md">
		<h2 class="mb-3 text-2xl font-bold">Section Title</h2>
		<p class="text-base">Main content text</p>
		<p class="text-sm opacity-60">Secondary metadata</p>
	</div>
</div>

<!-- ❌ Wrong: Same background as parent -->
<div class="bg-base-100">
	<div class="card bg-base-100">No visual separation</div>
</div>
```

## Core Principles

- **Background hierarchy**: base-200 (page) → base-100 (card) →
  base-200 (nested) - never same as parent
- **Borders**: Use `border-base-300` solid (no opacity)
- **Text sizes**: 3xl (h1) → 2xl (h2) → xl (h3) → base (body) → sm
  (metadata) → xs (hints)
- **Opacity**: ONLY 60/70/80, ONLY on metadata/descriptions (never
  titles/buttons/primary actions)
- **Shadows**: md (default) → lg (hover) → xl (important)
- **Semantic colors**: error/success should NOT have opacity
- **Test contrast**: Always verify on both light and dark themes

## Reference Files

- [styling-guide.md](references/styling-guide.md) - Complete design
  system with all rules and examples
