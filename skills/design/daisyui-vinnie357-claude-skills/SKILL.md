---
name: daisyui
description: Guide for daisyUI component library with Tailwind CSS. Use when building UI components, implementing themes, or creating responsive designs with daisyUI.
---

# daisyUI Component Library

Use this skill when building user interfaces with daisyUI and Tailwind CSS, implementing UI components, or configuring themes.

## When to Use This Skill

Activate when:
- Building UI components with daisyUI
- Choosing appropriate daisyUI components for design needs
- Implementing responsive layouts with daisyUI
- Configuring or customizing themes
- Converting designs to daisyUI components
- Troubleshooting daisyUI component styling

## What is daisyUI?

daisyUI is a Tailwind CSS component library providing:

- **Semantic component classes** - High-level abstractions of Tailwind utilities
- **33+ built-in themes** - Light, dark, and creative theme variants
- **Framework-agnostic** - Works with any HTML/CSS project
- **Utility-first compatible** - Combine components with Tailwind utilities

## Installation

Add daisyUI to your project:

```bash
npm install -D daisyui@latest
```

Configure `tailwind.config.js`:

```javascript
module.exports = {
  plugins: [require("daisyui")],
}
```

For detailed installation options and CDN usage, see `references/installation.md`.

## Component Categories

daisyUI provides components across these categories:

- **Actions**: Buttons, dropdowns, modals, swap
- **Data Display**: Cards, badges, tables, carousels, stats
- **Data Input**: Input, textarea, select, checkbox, radio, toggle
- **Navigation**: Navbar, menu, tabs, breadcrumbs, pagination
- **Feedback**: Alert, progress, loading, toast, tooltip
- **Layout**: Drawer, footer, hero, stack, divider

For component-specific guidance, consult the appropriate reference file.

## Quick Usage

### Basic Button

```html
<button class="btn">Button</button>
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-accent">Accent</button>
```

### Card Component

```html
<div class="card w-96 bg-base-100 shadow-xl">
  <figure><img src="image.jpg" alt="Image" /></figure>
  <div class="card-body">
    <h2 class="card-title">Card Title</h2>
    <p>Card description text</p>
    <div class="card-actions justify-end">
      <button class="btn btn-primary">Action</button>
    </div>
  </div>
</div>
```

### Modal

```html
<button class="btn" onclick="my_modal.showModal()">Open Modal</button>

<dialog id="my_modal" class="modal">
  <div class="modal-box">
    <h3 class="font-bold text-lg">Modal Title</h3>
    <p class="py-4">Modal content here</p>
    <div class="modal-action">
      <form method="dialog">
        <button class="btn">Close</button>
      </form>
    </div>
  </div>
</dialog>
```

## Theming

### Using Built-in Themes

Set theme via HTML attribute:

```html
<html data-theme="cupcake">
```

Available themes: light, dark, cupcake, bumblebee, emerald, corporate, synthwave, retro, cyberpunk, valentine, halloween, garden, forest, aqua, lofi, pastel, fantasy, wireframe, black, luxury, dracula, cmyk, autumn, business, acid, lemonade, night, coffee, winter, dim, nord, sunset

### Theme Switching

```html
<select class="select" data-choose-theme>
  <option value="light">Light</option>
  <option value="dark">Dark</option>
  <option value="cupcake">Cupcake</option>
</select>
```

For advanced theming and customization, see `references/theming.md`.

## Responsive Design

daisyUI components work with Tailwind's responsive prefixes:

```html
<button class="btn btn-sm md:btn-md lg:btn-lg">
  Responsive Button
</button>

<div class="card w-full md:w-96">
  <!-- Responsive card -->
</div>
```

## When to Consult References

- **Installation details**: Read `references/installation.md`
- **Complete component list**: Read `references/components.md`
- **Theming and customization**: Read `references/theming.md`
- **Layout patterns**: Read `references/layouts.md`
- **Form components**: Read `references/forms.md`
- **Common patterns**: Read `references/patterns.md`

## Combining with Tailwind Utilities

daisyUI semantic classes combine with Tailwind utilities:

```html
<!-- daisyUI component + Tailwind utilities -->
<button class="btn btn-primary shadow-lg hover:shadow-xl transition-all">
  Enhanced Button
</button>

<div class="card bg-base-100 border-2 border-primary rounded-lg p-4">
  <!-- Card with custom styling -->
</div>
```

## Key Principles

- **Semantic over utility**: Use component classes for common patterns
- **Utility for customization**: Apply Tailwind utilities for unique styling
- **Theme-aware**: Components adapt to theme colors automatically
- **Accessible**: Components follow accessibility best practices
- **Composable**: Combine components to build complex UIs

## Pro Tips

- Use `btn-{size}` modifiers: `btn-xs`, `btn-sm`, `btn-md`, `btn-lg`
- Add `btn-outline` for outlined button variants
- Use `badge` component for status indicators
- Combine `modal` with `modal-backdrop` for better UX
- Use `drawer` for mobile navigation patterns
- Leverage `stats` component for dashboard metrics
- Use `loading` class on buttons for async operations
