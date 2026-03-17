---
name: Performance
description: Optimization techniques including OnPush, @defer, and Image Optimization.
metadata:
  labels: [angular, performance, optimization, onpush]
  triggers:
    files: ['**/*.ts', '**/*.html']
    keywords: [ChangeDetectionStrategy.OnPush, @defer, NgOptimizedImage, runOutsideAngular]
---

# Performance

## **Priority: P1 (HIGH)**

## Principles

- **OnPush**: Always use `ChangeDetectionStrategy.OnPush`. Components should only update when Inputs change or Signals fire.
- **Deferrable Views**: Use `@defer` to lazy load heavy components/chunks below the fold.
- **Images**: Use `NgOptimizedImage` (`ngSrc`) for LCP optimization.

## Guidelines

- **Zoneless**: Prepare for Zoneless Angular by avoiding `Zone.runOutsideAngular` hacks. Use Signals.
- **TrackBy**: Always provide a tracking function in loops (`@for (item of items; track item.id)`).

## Anti-Patterns

- **Functions in Template**: `{{ calculate() }}` causes re-evaluation on every change detection cycle. Use `computed()` signals or pure pipes.
- **Heavy Constructors**: Keep constructors empty. Use `ngOnInit` or effects.

## References

- [Defer Usage](references/defer-usage.md)
