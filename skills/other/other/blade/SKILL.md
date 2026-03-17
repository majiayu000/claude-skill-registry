---
name: blade
description: Laravel Blade template conventions covering components, output escaping, security, structure, and formatting.
---

**Name:** Blade Templates
**Description:** Laravel Blade template conventions covering components, output escaping, security, structure, and formatting.
**Compatible Agents:** general-purpose, frontend
**Tags:** resources/views/**/*.blade.php, laravel, php, frontend, blade, template, html

## Rules

- Use Blade components (`<x-component>`) for reusable UI pieces
- Prefer anonymous components for simple, presentation-only elements
- Use class-based components when logic is needed
- Use `{{ }}` for escaped output (default) — never output raw user input unescaped
- Use `{!! !!}` only when the content is explicitly safe (e.g., pre-sanitized HTML)
- No inline `<style>` tags in Blade files
- No inline `<script>` tags in Blade files — use Livewire or Alpine.js via Blade directives
- Keep all user-facing text in English
- Indent Blade directives consistently (4 spaces)
- Use short attribute syntax where supported: `@class`, `@style`

## Examples

```blade
{{-- Escaped output — always use {{ }} for user data --}}
<h1>{{ $user->name }}</h1>
<p>{{ $post->excerpt }}</p>

{{-- Raw output — only for pre-sanitized content --}}
{!! $article->sanitizedBody !!}

{{-- Anonymous component --}}
<x-card>
    <x-slot:title>{{ $invoice->title }}</x-slot:title>
    <p>{{ $invoice->amount }}</p>
</x-card>
```

```blade
{{-- @class directive for conditional classes --}}
<div @class(['p-4 rounded', 'bg-green-100' => $active, 'bg-red-100' => $error])>
    {{ $message }}
</div>

{{-- @style directive for conditional styles --}}
<div @style(['color: green' => $success, 'color: red' => $failure])>
    {{ $text }}
</div>
```

```blade
{{-- Alpine.js via directive — no inline script tags --}}
<div x-data="{ open: false }">
    <button @click="open = !open">Toggle</button>
    <div x-show="open">Content</div>
</div>
```

## Anti-Patterns

- Using `{!! $user->input !!}` for user-provided data — XSS vulnerability
- Adding `<style>` or `<script>` tags directly in Blade files
- Putting complex PHP logic directly in Blade templates (use components or Livewire)
- Using inconsistent indentation for `@if`, `@foreach`, `@while` blocks
- Hardcoding non-English text directly in Blade (use translation helpers for user-facing strings)

## References

- [Laravel Blade Templates](https://laravel.com/docs/blade)
- [Alpine.js](https://alpinejs.dev/)
- Related: `Livewire/SKILL.md` — interactive UI in Blade templates
- Related: `Design/SKILL.md` — component-first design system
