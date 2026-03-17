---
name: Android Navigation
description: Standards for Jetpack Navigation Compose (Type-safe)
metadata:
  labels: [android, navigation, compose]
  triggers:
    files: ['**/*NavHost.kt', '**/*Graph.kt']
    keywords: ['NavHost', 'navController', '@Serializable']
---

# Android Navigation Standards

## **Priority: P0**

## Implementation Guidelines

### Type-Safe Navigation

- **Library**: Navigation Compose 2.8.0+.
- **Routes**: Use `@Serializable` objects/classes instead of String routes.
- **Arguments**: No manual bundle parsing. Use `.toRoute<T>()`.

### Structure

- **Graphs**: Split large apps into nested navigation graphs (`navigation` extension functions).
- **Hoisting**: Hoist navigation events out of Screens. Composable screens should accept callbacks (`onNavigateToX`).

## Anti-Patterns

- **Hardcoded Strings**: `**No String Routes**: Use Typed Objects.`
- **Passing NavController**: `**No NavController in UI**: Hoist events.`

## References

- [Route Definitions](references/implementation.md)
