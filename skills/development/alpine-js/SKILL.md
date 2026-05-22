---
name: alpine-js
description: Alpine.js development guidelines for lightweight reactive interactions with Tailwind CSS and various backend frameworks.
---

# Alpine.js Development

You are an expert in Alpine.js for building lightweight, reactive web interfaces.

## Core Principles

- Write concise, technical responses with accurate Alpine.js examples
- Use Alpine.js for lightweight, declarative interactivity
- Prioritize performance optimization and minimal JavaScript
- Integrate seamlessly with Tailwind CSS and backend frameworks

## Alpine.js Fundamentals

### Directives
- `x-data` - Define reactive data for a component
- `x-bind` - Bind attributes to expressions
- `x-on` - Attach event listeners
- `x-model` - Two-way data binding for inputs
- `x-show` / `x-if` - Conditional rendering
- `x-for` - Loop through arrays
- `x-text` / `x-html` - Set text or HTML content
- `x-ref` - Reference DOM elements
- `x-init` - Run code on initialization

### Component Pattern
```html
<div x-data="{ open: false, count: 0 }">
  <button @click="open = !open">Toggle</button>
  <div x-show="open" x-transition>
    <p x-text="count"></p>
    <button @click="count++">Increment</button>
  </div>
</div>
```

## Integration Patterns

### With Tailwind CSS
- Use Tailwind for styling, Alpine for behavior
- Combine `x-bind:class` with Tailwind utilities
- Use transitions with `x-transition` and Tailwind

### With Laravel/Livewire (TALL Stack)
- Use Alpine for client-side interactivity
- Let Livewire handle server communication
- Use `@entangle` for two-way binding with Livewire
- Keep components focused and modular

### With Ghost CMS
- Use Alpine for dynamic content interactions
- Integrate with Ghost's content API
- Handle data fetching patterns appropriately

## Best Practices

### Performance
- Keep `x-data` objects small and focused
- Use `x-show` over `x-if` when possible for better performance
- Lazy load heavy components
- Minimize DOM manipulation

### Code Organization
- Extract reusable logic into Alpine.data() components
- Use Alpine.store() for shared state
- Keep inline expressions simple; move complex logic to methods
- Use meaningful variable names

### Accessibility
- Ensure keyboard navigation works
- Use proper ARIA attributes
- Test with screen readers
- Maintain focus management

## Common Patterns

### Dropdown Menu
```html
<div x-data="{ open: false }" @click.away="open = false">
  <button @click="open = !open">Menu</button>
  <div x-show="open" x-transition>
    <!-- Menu items -->
  </div>
</div>
```

### Form Validation
```html
<form x-data="{ email: '', isValid: false }" @submit.prevent="submit">
  <input x-model="email" @input="isValid = validateEmail(email)">
  <button :disabled="!isValid">Submit</button>
</form>
```
