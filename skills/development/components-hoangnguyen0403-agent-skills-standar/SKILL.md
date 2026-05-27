---
name: Components
description: Standards for Standalone Components, Signals inputs, and Control Flow.
metadata:
  labels: [angular, components, standalone, signals, control-flow]
  triggers:
    files: ['**/*.component.ts', '**/*.html']
    keywords: [angular component, standalone, input signal, output, @if, @for]
---

# Angular Components

## **Priority: P0 (CRITICAL)**

## Principles

- **Standalone**: `standalone: true`. Import dependencies directly in `imports` array.
- **Signal Inputs**: Use `input()` and `input.required()` instead of `@Input()`.
- **Signal Outputs**: Use `output()` (from v17.3+) instead of `@Output() EventEmitter`.
- **Control Flow**: Use `@if`, `@for`, `@switch` block syntax instead of `*ngIf`, `*ngFor`.
- **View Encapsulation**: Default `Emulated`. Use `None` carefully.

## Signals Integration

- Use `computed()` for derived state.
- Use `effect()` strictly for side effects (logging, manual DOM manipulation), NEVER for state propagation.

## Anti-Patterns

- **Complex Logic in Template**: Call a method or use a `computed` signal.
- **Direct DOM Access**: Avoid `ElementRef.nativeElement` modification. Use Directives or Renderer2.
- **Component Inheritance**: Prefer Composition (Directives, Services) over Class Inheritance.

## References

- [Standalone Pattern](references/standalone-pattern.md)
- [Control Flow](references/control-flow.md)
