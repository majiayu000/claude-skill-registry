---
name: laravel-blade
description: Create Blade templates with components, slots, layouts, and directives. Use when building views, reusable components, or templating.
versions:
  laravel: "12.x"
  php: "8.4"
user-invocable: true
references: references/components.md, references/slots-attributes.md, references/layouts.md, references/directives.md, references/security.md, references/vite.md, references/advanced-directives.md, references/custom-directives.md, references/advanced-components.md, references/forms-validation.md, references/fragments.md, references/templates/ClassComponent.php.md, references/templates/AnonymousComponent.blade.md, references/templates/LayoutComponent.blade.md, references/templates/FormComponent.blade.md, references/templates/CardWithSlots.blade.md, references/templates/DynamicComponent.blade.md, references/templates/AdvancedDirectives.blade.md, references/templates/CustomDirectives.php.md, references/templates/AdvancedComponents.blade.md, references/templates/Fragments.blade.md
related-skills: laravel-livewire, laravel-i18n, fusecore
---

# Laravel Blade

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Check existing views, components structure
2. **fuse-ai-pilot:research-expert** - Verify latest Blade docs via Context7
3. **mcp__context7__query-docs** - Query specific patterns (components, slots)

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

Blade is Laravel's templating engine. It provides a clean syntax for PHP in views while compiling to pure PHP for performance.

| Component Type | When to Use |
|----------------|-------------|
| **Anonymous** | Simple UI, no logic needed |
| **Class-based** | Dependency injection, complex logic |
| **Layout** | Page structure, reusable shells |
| **Dynamic** | Runtime component selection |

---

## Critical Rules

1. **Always escape output** - Use `{{ }}` not `{!! !!}` unless absolutely necessary
2. **Use @props** - Declare expected props explicitly
3. **Merge attributes** - Allow class/attribute overrides with `$attributes->merge()`
4. **Prefer anonymous** - Use class components only when logic is needed
5. **Use named slots** - For complex layouts with multiple content areas
6. **CSRF in forms** - Always include `@csrf` in forms

---

## Decision Guide

### Component Type Selection

```
Need dependency injection?
├── YES → Class-based component
└── NO → Anonymous component
    │
    Need complex props logic?
    ├── YES → Class-based component
    └── NO → Anonymous component
```

### Layout Strategy

```
Simple page structure?
├── YES → Component layout (<x-layout>)
└── NO → Need fine-grained sections?
    ├── YES → @extends/@section
    └── NO → Component layout
```

---

## Key Concepts

| Concept | Description | Reference |
|---------|-------------|-----------|
| **@props** | Declare component properties | [components.md](references/components.md) |
| **$attributes** | Pass-through HTML attributes | [slots-attributes.md](references/slots-attributes.md) |
| **x-slot** | Named content areas | [slots-attributes.md](references/slots-attributes.md) |
| **@yield/@section** | Traditional layout inheritance | [layouts.md](references/layouts.md) |
| **$loop** | Loop iteration info | [directives.md](references/directives.md) |

---

## Reference Guide

### Concepts (WHY & Architecture)

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Components** | [components.md](references/components.md) | Class vs anonymous, namespacing |
| **Slots & Attributes** | [slots-attributes.md](references/slots-attributes.md) | Data flow, $attributes bag |
| **Layouts** | [layouts.md](references/layouts.md) | Page structure, inheritance |
| **Directives** | [directives.md](references/directives.md) | @if, @foreach, @auth, @can |
| **Security** | [security.md](references/security.md) | XSS, CSRF, escaping |
| **Vite** | [vite.md](references/vite.md) | Asset bundling |
| **Advanced Directives** | [advanced-directives.md](references/advanced-directives.md) | @once, @use, @inject, @switch, stacks |
| **Custom Directives** | [custom-directives.md](references/custom-directives.md) | Blade::if, Blade::directive |
| **Advanced Components** | [advanced-components.md](references/advanced-components.md) | @aware, shouldRender, index |
| **Forms & Validation** | [forms-validation.md](references/forms-validation.md) | @error, form helpers |
| **Fragments** | [fragments.md](references/fragments.md) | @fragment, HTMX integration |

### Templates (Complete Code)

| Template | When to Use |
|----------|-------------|
| [ClassComponent.php.md](references/templates/ClassComponent.php.md) | Component with logic/DI |
| [AnonymousComponent.blade.md](references/templates/AnonymousComponent.blade.md) | Simple reusable UI |
| [LayoutComponent.blade.md](references/templates/LayoutComponent.blade.md) | Page layout structure |
| [FormComponent.blade.md](references/templates/FormComponent.blade.md) | Form with validation |
| [CardWithSlots.blade.md](references/templates/CardWithSlots.blade.md) | Named slots pattern |
| [DynamicComponent.blade.md](references/templates/DynamicComponent.blade.md) | Runtime component |
| [AdvancedDirectives.blade.md](references/templates/AdvancedDirectives.blade.md) | @once, @use, @inject, @switch |
| [CustomDirectives.php.md](references/templates/CustomDirectives.php.md) | Create custom directives |
| [AdvancedComponents.blade.md](references/templates/AdvancedComponents.blade.md) | @aware, shouldRender, index |
| [Fragments.blade.md](references/templates/Fragments.blade.md) | HTMX partial updates |

---

## Quick Reference

### Anonymous Component

```blade
{{-- resources/views/components/alert.blade.php --}}
@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

### Class Component

```php
// app/View/Components/Alert.php
class Alert extends Component
{
    public function __construct(
        public string $type = 'info',
        public string $message = ''
    ) {}

    public function render(): View
    {
        return view('components.alert');
    }
}
```

### Named Slots

```blade
<x-card>
    <x-slot:header class="font-bold">
        Title
    </x-slot>

    Content goes here

    <x-slot:footer>
        Footer content
    </x-slot>
</x-card>
```

### Attribute Merging

```blade
@props(['disabled' => false])

<button {{ $attributes->merge([
    'type' => 'submit',
    'class' => 'btn btn-primary'
])->class(['opacity-50' => $disabled]) }}
    @disabled($disabled)
>
    {{ $slot }}
</button>
```

---

## Best Practices

### DO
- Use `@props` to document expected props
- Use `$attributes->merge()` for flexibility
- Prefer anonymous components for simple UI
- Use named slots for complex layouts
- Keep components focused and reusable

### DON'T
- Use `{!! !!}` without sanitization
- Forget `@csrf` in forms
- Put business logic in Blade templates
- Create deeply nested component hierarchies
- Hardcode classes (allow overrides)
