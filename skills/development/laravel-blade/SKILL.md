---
name: laravel-blade
description: Create Blade templates with components, slots, layouts, and directives. Use when building views, reusable components, or templating.
user-invocable: false
---

# Laravel Blade Templates

## Documentation

### Views & Templates
- [blade.md](docs/blade.md) - Blade templating
- [views.md](docs/views.md) - Views
- [localization.md](docs/localization.md) - Localization

### Frontend
- [frontend.md](docs/frontend.md) - Frontend scaffolding
- [vite.md](docs/vite.md) - Vite asset bundling

## Component Class

```php
<?php

declare(strict_types=1);

namespace App\View\Components;

final class Button extends Component
{
    public function __construct(
        public string $type = 'button',
        public string $variant = 'primary',
        public bool $disabled = false,
    ) {}

    public function variantClasses(): string
    {
        return match ($this->variant) {
            'primary' => 'bg-blue-500 text-white',
            'danger' => 'bg-red-500 text-white',
            default => 'bg-gray-200 text-gray-800',
        };
    }

    public function render(): View
    {
        return view('components.button');
    }
}
```

## Component View

```blade
<button
    type="{{ $type }}"
    {{ $disabled ? 'disabled' : '' }}
    {{ $attributes->merge(['class' => 'px-4 py-2 rounded ' . $variantClasses()]) }}
>
    {{ $slot }}
</button>
```

## Layout

```blade
{{-- resources/views/layouts/app.blade.php --}}
<!DOCTYPE html>
<html>
<head>
    <title>{{ $title ?? 'My App' }}</title>
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body>
    <x-navigation />
    <main>{{ $slot }}</main>
    <x-footer />
</body>
</html>
```

## Directives

```blade
@foreach($items as $item)
    {{ $loop->index }} - {{ $loop->first }} - {{ $loop->last }}
@endforeach

@auth
    Welcome, {{ auth()->user()->name }}
@endauth

@can('update', $post)
    <button>Edit</button>
@endcan
```
