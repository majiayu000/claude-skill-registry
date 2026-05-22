---
name: react-code-smells
description: Principal-engineer-level React refactoring patterns for eliminating code smells. Covers prop drilling, state explosion, component composition, abstraction quality, coupling, hooks, rendering patterns, and testability. Use when refactoring existing React codebases, reviewing PRs for architectural issues, or identifying technical debt in React applications.
---

# Principal Engineering React Best Practices

Principal-engineer-level refactoring guide for React applications. Contains 42 rules across 8 categories, prioritized by impact from critical (state architecture, composition) to incremental (testability). Each rule includes code smell indicators, before/after examples, and safe transformation steps.

## When to Apply

Reference these guidelines when:
- Refactoring existing React codebases
- Reviewing PRs for architectural issues
- Identifying technical debt
- Planning large-scale refactoring efforts
- Deciding whether to extract, inline, or restructure components
- Improving testability of React code

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | State Architecture | CRITICAL | `state-` |
| 2 | Component Composition | CRITICAL | `comp-` |
| 3 | Abstraction Quality | HIGH | `abs-` |
| 4 | Coupling & Cohesion | HIGH | `couple-` |
| 5 | Hook Hygiene | MEDIUM-HIGH | `hook-` |
| 6 | Render Patterns | MEDIUM | `render-` |
| 7 | Side Effect Management | MEDIUM | `effect-` |
| 8 | Testability | LOW-MEDIUM | `test-` |

## Quick Reference

### 1. State Architecture (CRITICAL)

- [`state-prop-drilling-compound`](references/state-prop-drilling-compound.md) - Replace prop drilling with compound components
- [`state-prop-drilling-composition`](references/state-prop-drilling-composition.md) - Replace prop drilling with component composition
- [`state-derived-calculation`](references/state-derived-calculation.md) - Replace synchronized state with derived calculations
- [`state-machine-complex`](references/state-machine-complex.md) - Replace boolean explosion with state machines
- [`state-colocation`](references/state-colocation.md) - Colocate state with components that use it
- [`state-reducer-consolidation`](references/state-reducer-consolidation.md) - Consolidate related useState calls into useReducer
- [`state-context-selector`](references/state-context-selector.md) - Use context selectors to prevent cascade re-renders
- [`state-url-sync`](references/state-url-sync.md) - Move shareable state to URL parameters

### 2. Component Composition (CRITICAL)

- [`comp-render-props-extraction`](references/comp-render-props-extraction.md) - Extract shared logic with render props or hooks
- [`comp-slots-over-props`](references/comp-slots-over-props.md) - Use slots/children instead of configuration props
- [`comp-god-component-split`](references/comp-god-component-split.md) - Split god components by responsibility
- [`comp-controlled-uncontrolled`](references/comp-controlled-uncontrolled.md) - Choose controlled vs uncontrolled deliberately
- [`comp-headless-extraction`](references/comp-headless-extraction.md) - Extract headless components for reusable behavior
- [`comp-props-spreading`](references/comp-props-spreading.md) - Avoid untyped props spreading
- [`comp-polymorphic-as`](references/comp-polymorphic-as.md) - Use polymorphic 'as' prop for flexible elements
- [`comp-children-validation`](references/comp-children-validation.md) - Validate compound component children

### 3. Abstraction Quality (HIGH)

- [`abs-premature-abstraction`](references/abs-premature-abstraction.md) - Resist premature abstraction (Rule of Three)
- [`abs-over-configuration`](references/abs-over-configuration.md) - Prefer composition over configuration
- [`abs-extract-custom-hook`](references/abs-extract-custom-hook.md) - Extract custom hooks for reusable logic
- [`abs-inline-vs-extract`](references/abs-inline-vs-extract.md) - Know when to inline vs extract components
- [`abs-wrong-abstraction-fix`](references/abs-wrong-abstraction-fix.md) - Fix wrong abstractions by inlining first
- [`abs-utility-vs-domain`](references/abs-utility-vs-domain.md) - Separate utility hooks from domain hooks

### 4. Coupling & Cohesion (HIGH)

- [`couple-colocation-files`](references/couple-colocation-files.md) - Colocate related files by feature
- [`couple-dependency-injection`](references/couple-dependency-injection.md) - Use dependency injection for external services
- [`couple-interface-segregation`](references/couple-interface-segregation.md) - Apply interface segregation to props
- [`couple-circular-deps`](references/couple-circular-deps.md) - Break circular dependencies with inversion
- [`couple-stable-imports`](references/couple-stable-imports.md) - Import from stable public APIs only

### 5. Hook Hygiene (MEDIUM-HIGH)

- [`hook-dependency-stability`](references/hook-dependency-stability.md) - Ensure hook dependencies are stable
- [`hook-composition-over-size`](references/hook-composition-over-size.md) - Compose small hooks rather than one large hook
- [`hook-return-object-vs-tuple`](references/hook-return-object-vs-tuple.md) - Choose hook return type by use case
- [`hook-conditional-usage`](references/hook-conditional-usage.md) - Never call hooks conditionally
- [`hook-naming-conventions`](references/hook-naming-conventions.md) - Follow hook naming conventions

### 6. Render Patterns (MEDIUM)

- [`render-conditional-early-return`](references/render-conditional-early-return.md) - Use early returns for conditional rendering
- [`render-list-key-stability`](references/render-list-key-stability.md) - Use stable, unique keys for lists
- [`render-avoid-inline-objects`](references/render-avoid-inline-objects.md) - Avoid inline objects in JSX props
- [`render-fragment-cleanup`](references/render-fragment-cleanup.md) - Use fragments to avoid wrapper divs

### 7. Side Effect Management (MEDIUM)

- [`effect-to-event-handler`](references/effect-to-event-handler.md) - Move event responses from effects to handlers
- [`effect-cleanup-required`](references/effect-cleanup-required.md) - Always clean up effect side effects
- [`effect-single-responsibility`](references/effect-single-responsibility.md) - Separate unrelated effects
- [`effect-avoid-unnecessary`](references/effect-avoid-unnecessary.md) - Remove effects that aren't synchronization

### 8. Testability (LOW-MEDIUM)

- [`test-seam-creation`](references/test-seam-creation.md) - Create seams for testable components
- [`test-behavior-over-implementation`](references/test-behavior-over-implementation.md) - Test behavior, not implementation details
- [`test-extract-for-testability`](references/test-extract-for-testability.md) - Extract logic to hooks for testability
- [`test-mock-boundaries`](references/test-mock-boundaries.md) - Mock at boundaries, not internal details

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Related Skills

- For React 19 API best practices, see `react` skill
- For React core principles, see `react-principle-engineer` skill
- For form handling, see `react-hook-form` skill

## References

1. [react.dev](https://react.dev) - Official React documentation
2. [kentcdodds.com](https://kentcdodds.com) - Advanced React patterns
3. [patterns.dev](https://patterns.dev) - Design patterns in JavaScript
4. [testing-library.com](https://testing-library.com) - Testing best practices
