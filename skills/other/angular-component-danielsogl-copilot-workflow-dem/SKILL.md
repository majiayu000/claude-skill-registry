---
name: angular-component
description: Use when creating new Angular components, directives, or pipes. Triggers on requests to "create component", "add component", "new component", "build a component", or modify existing component patterns.
---

# Angular Component Creation Guide

Create Angular v20+ standalone components following project patterns.

## Component Structure

Every component must:

1. Be standalone (default in Angular v20+, do NOT set `standalone: true`)
2. Use `ChangeDetectionStrategy.OnPush`
3. Use `inject()` function for DI (not constructor injection)
4. Use signal-based inputs with `input()` and outputs with `output()`
5. Use modern control flow: `@if`, `@for`, `@switch` (NOT `*ngIf`, `*ngFor`)
6. Be placed in its own subfolder within the appropriate type folder

## File Location (DDD Structure)

```
src/app/
  <domain>/           # e.g., tasks, user
    feature/          # Feature/container components
      <component-name>/
        <component-name>.ts
        <component-name>.html
        <component-name>.scss
        <component-name>.spec.ts
    ui/               # Presentational components
      <component-name>/
        ...
```

## Component Template

```typescript
import {
  ChangeDetectionStrategy,
  Component,
  computed,
  inject,
  input,
  output,
  signal,
} from "@angular/core";

@Component({
  selector: "app-example",
  templateUrl: "./example.html",
  styleUrl: "./example.scss",
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [
    // Import only required standalone components, directives, pipes
    // Do NOT import CommonModule or RouterModule
  ],
})
export class Example {
  // Dependency Injection using inject()
  private readonly someService = inject(SomeService);

  // Signal-based inputs
  readonly data = input.required<DataType>();
  readonly disabled = input(false);

  // Two-way binding with model()
  readonly value = model(0);

  // Signal-based outputs
  readonly valueChange = output<number>();
  readonly submitted = output<void>();

  // Local signal state
  private readonly loading = signal(false);

  // Computed/derived state
  readonly displayText = computed(() =>
    this.loading() ? "Loading..." : `Value: ${this.value()}`,
  );

  // Methods
  submit(): void {
    this.submitted.emit();
  }
}
```

## Template Patterns

```html
<!-- Modern control flow (REQUIRED) -->
@if (loading()) {
<app-spinner />
} @else {
<div class="content">
  @for (item of items(); track item.id) {
  <app-item [data]="item" (click)="selectItem(item)" />
  } @empty {
  <p>No items found</p>
  }
</div>
} @switch (status()) { @case ('pending') {
<span>Pending</span>
} @case ('complete') {
<span>Complete</span>
} @default {
<span>Unknown</span>
} }

<!-- Use class bindings, not ngClass -->
<div [class.active]="isActive()" [class.disabled]="disabled()">
  <!-- Use style bindings, not ngStyle -->
  <div [style.color]="textColor()"></div>
</div>
```

## Input Transformations

```typescript
import { booleanAttribute, numberAttribute } from '@angular/core';

// Boolean transformation
readonly disabled = input(false, { transform: booleanAttribute });

// Number transformation
readonly count = input(0, { transform: numberAttribute });
```

## Host Configuration

```typescript
@Component({
  selector: 'app-example',
  host: {
    // Host bindings
    '[class.is-active]': 'isActive()',
    '[attr.aria-label]': 'ariaLabel()',

    // Host listeners
    '(click)': 'onClick($event)',
    '(keydown.enter)': 'onEnter()',

    // Static properties
    'role': 'button',
  },
})
```

## Deferred Loading

```html
@defer (on viewport) {
<app-heavy-component />
} @placeholder {
<div>Loading placeholder...</div>
} @loading (minimum 200ms) {
<app-spinner />
} @error {
<p>Failed to load</p>
}
```

## Checklist

- [ ] Component in own subfolder within feature/ or ui/
- [ ] Using `ChangeDetectionStrategy.OnPush`
- [ ] Using `inject()` for dependencies
- [ ] Using signal-based `input()` and `output()`
- [ ] Using modern control flow (`@if`, `@for`, `@switch`)
- [ ] No CommonModule or RouterModule imports
- [ ] Template and styles in separate files
- [ ] Selector uses `app-` prefix with kebab-case
