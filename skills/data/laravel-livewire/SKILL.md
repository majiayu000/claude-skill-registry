---
name: laravel-livewire
description: Livewire 3 reactive components - wire:model, actions, events, Volt, Folio. Use when building reactive UI without JavaScript.
versions:
  laravel: "12.x"
  livewire: "3.x"
  php: "8.4"
user-invocable: true
references: references/components.md, references/wire-directives.md, references/lifecycle.md, references/forms-validation.md, references/events.md, references/alpine-integration.md, references/file-uploads.md, references/nesting.md, references/loading-states.md, references/navigation.md, references/testing.md, references/security.md, references/volt.md, references/folio.md, references/precognition.md, references/reverb.md, references/templates/BasicComponent.php.md, references/templates/FormComponent.php.md, references/templates/VoltComponent.blade.md, references/templates/DataTableComponent.php.md, references/templates/FileUploadComponent.php.md, references/templates/NestedComponents.php.md, references/templates/ComponentTest.php.md
related-skills: laravel-blade, laravel-testing, laravel-api
---

# Laravel Livewire

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Check existing Livewire components
2. **fuse-ai-pilot:research-expert** - Verify Livewire 3 patterns via Context7
3. **mcp__context7__query-docs** - Check specific Livewire features

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

| Feature | Description |
|---------|-------------|
| **Components** | Reactive PHP classes with Blade views |
| **wire:model** | Two-way data binding |
| **Actions** | Call PHP methods from frontend |
| **Events** | Component communication |
| **Volt** | Single-file components |
| **Folio** | File-based routing |

---

## Critical Rules

1. **Always use wire:key** in loops
2. **Use wire:model.blur** for validation, not .live everywhere
3. **Debounce search inputs** with .debounce.300ms
4. **#[Locked]** for sensitive IDs
5. **authorize()** in destructive actions
6. **protected methods** for internal logic

---

## Decision Guide

### Component Type

```
Component choice?
├── Complex logic → Class-based component
├── Simple page → Volt functional API
├── Medium complexity → Volt class-based
├── Quick embed → @volt inline
└── File-based route → Folio + Volt
```

### Data Binding

```
Binding type?
├── Form fields → wire:model.blur
├── Search input → wire:model.live.debounce.300ms
├── Checkbox/toggle → wire:model.live
├── Select → wire:model
└── No sync → Local Alpine x-data
```

---

## Reference Guide

### Core Concepts (WHY & Architecture)

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Components** | [components.md](references/components.md) | Creating components |
| **Wire Directives** | [wire-directives.md](references/wire-directives.md) | Data binding, events |
| **Lifecycle** | [lifecycle.md](references/lifecycle.md) | Hooks, mount, hydrate |
| **Forms** | [forms-validation.md](references/forms-validation.md) | Validation, form objects |
| **Events** | [events.md](references/events.md) | Dispatch, listen |
| **Alpine** | [alpine-integration.md](references/alpine-integration.md) | $wire, @entangle |
| **File Uploads** | [file-uploads.md](references/file-uploads.md) | Upload handling |
| **Nesting** | [nesting.md](references/nesting.md) | Parent-child |
| **Loading** | [loading-states.md](references/loading-states.md) | wire:loading, lazy |
| **Navigation** | [navigation.md](references/navigation.md) | SPA mode |
| **Testing** | [testing.md](references/testing.md) | Component tests |
| **Security** | [security.md](references/security.md) | Auth, rate limit |
| **Volt** | [volt.md](references/volt.md) | Single-file components |

### Advanced Features

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Folio** | [folio.md](references/folio.md) | File-based routing |
| **Precognition** | [precognition.md](references/precognition.md) | Live validation |
| **Reverb** | [reverb.md](references/reverb.md) | WebSockets |

### Templates (Complete Code)

| Template | When to Use |
|----------|-------------|
| [BasicComponent.php.md](references/templates/BasicComponent.php.md) | Standard component |
| [FormComponent.php.md](references/templates/FormComponent.php.md) | Form with validation |
| [VoltComponent.blade.md](references/templates/VoltComponent.blade.md) | Volt patterns |
| [DataTableComponent.php.md](references/templates/DataTableComponent.php.md) | Table with search/sort |
| [FileUploadComponent.php.md](references/templates/FileUploadComponent.php.md) | File uploads |
| [NestedComponents.php.md](references/templates/NestedComponents.php.md) | Parent-child |
| [ComponentTest.php.md](references/templates/ComponentTest.php.md) | Testing patterns |

---

## Quick Reference

### Basic Component

```php
class Counter extends Component
{
    public int $count = 0;

    public function increment(): void
    {
        $this->count++;
    }

    public function render()
    {
        return view('livewire.counter');
    }
}
```

### Volt Functional

```php
<?php
use function Livewire\Volt\{state};

state(['count' => 0]);

$increment = fn() => $this->count++;
?>

<button wire:click="increment">{{ $count }}</button>
```

### Wire Directives

```blade
<input wire:model.blur="email">
<input wire:model.live.debounce.300ms="search">
<button wire:click="save" wire:loading.attr="disabled">Save</button>
```

---

## Best Practices

### DO
- Use wire:key in @foreach loops
- Debounce search/filter inputs
- Use Form Objects for reusable logic
- Test with Livewire::test()
- #[Locked] for IDs, #[Computed] for derived data

### DON'T
- wire:model.live on every field
- Query in render() method
- Forget authorization in actions
- Skip wire:key in loops
- Store sensitive data in public properties
