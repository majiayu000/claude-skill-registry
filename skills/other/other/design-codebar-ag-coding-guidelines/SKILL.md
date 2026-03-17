---
name: design
description: Component-first design system for Blade views. Use when creating UI components, designing responsive layouts, or implementing accessible interfaces.
---

**Name:** Design System
**Description:** Component-first design system for Blade views. Use when creating UI components, designing responsive layouts, or implementing accessible interfaces.
**Compatible Agents:** general-purpose, frontend
**Tags:** resources/views/**/*.blade.php, laravel, blade, design-system, components, responsive, accessibility

## Rules

- Every UI element MUST use a Blade component — no raw `<button>`, `<input>`, `<table>`, `<textarea>`, or styled `<div>` badges in page views
- Check the styleguide (`/styleguide`) for existing components before creating new ones
- Every new component MUST be added to `config/styleguide.php` and have a styleguide section
- Use anonymous components for presentation-only elements
- Accept `$attributes` and merge with defaults via `$attributes->merge(['class' => '...'])`
- Use named slots (`$header`, `$trigger`, `$content`) for composable layouts
- Props with `@props([...])` — always provide sensible defaults
- Mobile-first: base styles for 320px+, `sm:` for 640px+, `lg:` for 1024px+
- Tables must fall back to stacked cards on mobile
- All interactive elements: `min-h-[44px]` touch targets
- Use `<x-heading>` for typography — no raw `<h1>`-`<h6>` in page views
- Hover, focus, and disabled states on every interactive element
- `focus-visible` rings on all interactive elements
- ARIA labels for icon-only buttons
- Keyboard navigation support
- Screen-reader-only text (`sr-only`) where visual context is implicit

## Examples

```blade
{{-- Anonymous component with $attributes and @props --}}
@props([
    'variant' => 'primary',
    'size' => 'md',
])

<button
    {{ $attributes->merge(['class' => 'min-h-[44px] rounded-lg px-4 transition ease-in-out duration-150 focus-visible:ring-2 focus-visible:ring-accent-500']) }}
>
    {{ $slot }}
</button>
```

```blade
{{-- Composable layout with named slots --}}
<x-card>
    <x-slot:header>
        <x-heading level="2">{{ $title }}</x-heading>
    </x-slot:header>
    <x-slot:content>
        {{ $slot }}
    </x-slot:content>
</x-card>
```

```blade
{{-- Visual conventions: shadows, radius, color system --}}
<div class="rounded-lg shadow-sm p-6 transition ease-in-out duration-150">
    <span class="rounded-full bg-green-100 text-green-800 px-3 py-1">Active</span>
</div>
```

```blade
{{-- Icon-only button with ARIA label for screen readers --}}
<button type="button" aria-label="Close dialog" class="min-h-[44px] min-w-[44px] rounded-lg focus-visible:ring-2">
    <x-icon name="x" />
</button>
```

## Anti-Patterns

- Using raw HTML elements instead of Blade components in page views
- Creating new components without checking the styleguide first
- Forgetting to add new components to `config/styleguide.php`
- Interactive elements without `min-h-[44px]` touch targets
- Icon-only buttons without `aria-label` or `sr-only` alternative text
- Tables that do not fall back to stacked cards on mobile
- Missing `focus-visible` rings on interactive elements
- Using raw `<h1>`-`<h6>` instead of `<x-heading>`

## References

- [Laravel Blade Components](https://laravel.com/docs/blade#components)
- Related: `Blade/SKILL.md` — Blade template conventions
- Related: `Tailwind/SKILL.md` — Tailwind CSS styling conventions
