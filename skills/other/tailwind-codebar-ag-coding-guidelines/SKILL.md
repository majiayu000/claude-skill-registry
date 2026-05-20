---
name: tailwind
description: Tailwind CSS v4 styling conventions. Use when working with CSS, Tailwind utilities, or customizing the theme in Laravel projects.
---

**Name:** Tailwind CSS
**Description:** Tailwind CSS v4 styling conventions. Use when working with CSS, Tailwind utilities, or customizing the theme in Laravel projects.
**Compatible Agents:** general-purpose, frontend
**Tags:** resources/css/**/*.css, laravel, tailwind, css, vite, styling

## Rules

- **Tailwind CSS v4** utility classes only — no custom CSS classes
- Theme customization via `@theme` directive in `resources/css/app.css`
- Do not create custom `.css` class selectors — compose utilities in markup instead
- Vite is the build tool with `@tailwindcss/vite` plugin
- Entry point: `resources/css/app.css`
- Use `@source` directive to include Blade and Livewire paths for class scanning
- Use responsive prefixes (`sm:`, `md:`, `lg:`) for responsive design
- Use dark mode variant (`dark:`) when dark mode is supported
- Extract Blade components for complex repeated utility patterns — keep utility strings readable

## Examples

```css
/* resources/css/app.css — theme customization via @theme */
@import "tailwindcss";

@theme {
    --color-primary-500: #3b82f6;
    --color-accent-500: #8b5cf6;
    --font-sans: "Inter", system-ui, sans-serif;
}

@source "../views/**/*.blade.php";
@source "../../app/Livewire/**/*.php";
```

```blade
{{-- Compose utilities in markup — no custom CSS classes --}}
<div class="rounded-lg shadow-sm p-4 sm:p-6 lg:p-8 transition ease-in-out duration-150">
    <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100">Title</h2>
</div>
```

```blade
{{-- Extract complex patterns to components — avoid long utility strings in views --}}
<x-card class="p-4">
    {{ $slot }}
</x-card>
```

## Anti-Patterns

- Creating custom `.my-class { ... }` selectors in CSS files
- Using inline styles or `<style>` tags instead of Tailwind utilities
- Long, repeated utility strings in Blade views — extract to components
- Missing `@source` directives for Blade/Livewire paths (classes won't be scanned)
- Not using responsive prefixes when layout changes by viewport
- Hardcoding colors instead of using theme variables via `@theme`

## References

- [Tailwind CSS v4 Documentation](https://tailwindcss.com/docs)
- [Vite Plugin](https://tailwindcss.com/docs/installation/framework-guides/vite)
- Related: `Design/SKILL.md` — design system and component conventions
- Related: `Blade/SKILL.md` — Blade template structure
