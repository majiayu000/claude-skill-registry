---
name: component
description: Generate an Angular component with signals, OnPush, and host-based styling following Momentum CMS conventions. Use when creating new UI components in any library.
argument-hint: <library> <component-name>
---

# Generate Angular Component

Create an Angular component following Momentum CMS conventions.

## Arguments

- First argument: Library path (e.g., "admin", "ui", "admin/components")
- Second argument: Component name in kebab-case (e.g., "data-table", "field-renderer")

## Steps

1. Create component files in `libs/<library>/src/lib/<component>/`:
   - `<component>.ts` (component class)
   - `<component>.html` (template, if complex)
   - `<component>.spec.ts` (tests)

2. Use this template for the component:

```typescript
import { ChangeDetectionStrategy, Component, computed, input, output, signal, inject } from '@angular/core';

@Component({
  selector: 'mcms-<component-name>',
  host: { class: 'block' },
  template: `
    <!-- Template here -->
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class <PascalName>Component {
  // Signal inputs (use proper types, never `any`)
  readonly data = input.required<DataType>();

  // Optional inputs with defaults
  readonly disabled = input(false);

  // Signal outputs
  readonly valueChange = output<ValueType>();

  // Internal state
  private readonly _loading = signal(false);

  // Computed values
  readonly loading = this._loading.asReadonly();
  readonly hasData = computed(() => !!this.data());

  // Injected services
  private readonly http = inject(HttpClient);
}
```

3. Export from library's `index.ts`:

```typescript
export { <PascalName>Component } from './lib/<component>/<component>';
```

## Key Conventions

- **NO `standalone: true`** — default in Angular 21, redundant (ESLint enforced)
- **NO `any` types** — use proper interfaces (ESLint enforced)
- **NO `CommonModule` import** — unnecessary in Angular 21
- Always use `ChangeDetectionStrategy.OnPush`
- Use `input()` and `input.required()` for inputs
- Use `output()` for outputs
- Use `signal()` for internal state, `computed()` for derived values
- Use `inject()` for dependency injection
- Use `@for`/`@if`/`@switch` control flow
- Prefix selectors with `mcms-`

## UI Component Patterns

### No Wrapping Divs

Angular components create a host element. Style the host directly — do NOT add wrapper divs:

```typescript
@Component({
  selector: 'mcms-button',
  host: { class: 'inline-flex items-center gap-2' },
  template: `<ng-content />`,
})
```

NOT:

```typescript
// BAD: unnecessary wrapper div
template: `<div class="inline-flex items-center gap-2"><ng-content /></div>`,
```

### Class Configuration

Accept a `class` input for Tailwind customization via `hostClasses()` computed:

```typescript
@Component({
	selector: 'button[mcms-button]',
	host: { '[class]': 'hostClasses()' },
	template: `<ng-content />`,
	changeDetection: ChangeDetectionStrategy.OnPush,
})
export class McmsButtonComponent {
	readonly variant = input<'primary' | 'secondary'>('primary');
	readonly class = input('');

	readonly hostClasses = computed(
		() => `${baseClasses} ${variantClasses[this.variant()]} ${this.class()}`,
	);
}
```

### Theme Service

Use `McmsThemeService` for dark mode support:

```typescript
import { McmsThemeService } from '@momentumcms/admin';

@Component({...})
export class MyComponent {
  private readonly theme = inject(McmsThemeService);

  toggleDarkMode(): void {
    this.theme.toggleTheme();
  }

  readonly isDark = this.theme.isDark;           // computed signal
  readonly currentTheme = this.theme.theme;      // 'light' | 'dark' | 'system'
}
```

### App Tailwind Setup

Apps using the admin library must:

1. **tailwind.config.js** — Use the admin preset and include library sources:

```javascript
const adminPreset = require('../../libs/admin/tailwind.preset');

module.exports = {
	presets: [adminPreset],
	content: [
		join(__dirname, 'src/**/!(*.stories|*.spec).{ts,html}'),
		join(__dirname, '../../libs/admin/src/**/*.{ts,html}'),
		...createGlobPatternsForDependencies(__dirname),
	],
};
```

2. **styles.css** — Include CSS variables inline (Angular's esbuild can't resolve library CSS imports):

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
	:root {
		--mcms-background: 0 0% 100%;
		--mcms-foreground: 222 47% 11%;
		/* ... copy from libs/admin/src/styles/theme.css */
	}
	.dark {
		/* dark mode variables */
	}
}
```
