---
name: Android Jetpack Compose
description: Standards for Declarative UI, State Hoisting, and Performance
metadata:
  labels: [android, compose, ui]
  triggers:
    files: ['**/*.kt']
    keywords: ['@Composable', 'Modifier', 'Column', 'Row']
---

# Jetpack Compose Standards

## **Priority: P0**

## Implementation Guidelines

### State Hoisting

- **Pattern**: `Screen` (Stateful) -> `Content` (Stateless).
- **Events**: Pass lambda callbacks down (`onItemClick: (Id) -> Unit`).
- **Dependencies**: NEVER pass ViewModel to stateless composables.

### Performance

- **Recomposition**: Use `@Stable` / `@Immutable` on UI Models.
- **Lists**: Always use `key` in `LazyColumn` / `LazyRow`.
- **Modifiers**: Reuse Modifier instances or extract to variables if stable.

### Theming (Material 3)

- **Tokens**: Use `MaterialTheme.colorScheme` and `MaterialTheme.typography`.
- **Hardcoding**: `**No Hardcoded Colors**: Use Theme.`

## Anti-Patterns

- **Side Effects**: `**No SideEffects in Composition**: Use LaunchedEffect.`
- **ViewModel pass-through**: `**No VM deep pass**: Hoist state.`

## References

- [Patterns & Optimization](references/implementation.md)
