---
name: modern-jetpack-compose
description: >
  Guides writing, reviewing, and reasoning about modern Android UI code using
  Jetpack Compose. Covers best practices for state management, side effects,
  recomposition, navigation, Material 3 design, accessibility, and performance.
  Use when reading, writing, or reviewing any Jetpack Compose project.
license: MIT
metadata:
  author: Anh Vu <anhvt52@gmail.com>
  version: "1.0"
---

Review or generate Jetpack Compose code for correctness, modern API usage,
and adherence to Android best practices. Report only genuine issues — do not
nitpick style unless it contradicts a clear rule.

## Review / Generation Process

When reviewing existing code, follow these steps in order:

1. Check for deprecated or outdated APIs → `references/api.md`
2. Review composable structure and composition patterns → `references/composables.md`
3. Validate state management and data flow → `references/state.md`
4. Validate side-effect usage → `references/effects.md`
5. Check recomposition stability → `references/recomposition.md`
6. Validate navigation implementation → `references/navigation.md`
7. Check Material 3 / Expressive design compliance → `references/design.md`
8. Validate accessibility → `references/accessibility.md`
9. Check performance → `references/performance.md`
10. Quick Kotlin code review → `references/kotlin.md`
11. Final code hygiene check → `references/hygiene.md`

When **generating** new code, load the relevant reference files for the feature
being built before writing any code, so output is idiomatic from the start.

For partial reviews or targeted generation, load only the relevant reference files.


## Core Instructions

- Target Compose BOM 2024.x by default. Note where BOM 2025.x (Material Expressive)
  introduces new components or APIs.
- Use Material 3. Do not use Material 2 unless the project already uses it.
- Architecture: MVVM with unidirectional data flow (UDF). ViewModel + StateFlow
  for screen state. Compose UI observes state, emits events.
- Target Kotlin with modern language features (sealed interfaces, coroutines, Flow).
- Do not introduce third-party libraries without asking first.
- Each composable should live in its own file for non-trivial components.
- Organize by feature, not by technical layer (screens/home/, screens/settings/, etc.).


## Output Format

Organize findings by file. For each issue:

1. State the file and relevant line(s).
2. Name the rule being violated.
3. Show a brief before/after Kotlin snippet.

Skip files with no issues. End with a prioritized summary of the most impactful
changes to make first.

**Example output:**

### HomeScreen.kt

**Line 14: Use `collectAsStateWithLifecycle()` instead of `collectAsState()`.**

```kotlin
// Before
val uiState by viewModel.uiState.collectAsState()

// After
val uiState by viewModel.uiState.collectAsStateWithLifecycle()
```

**Line 42: Provide `key` in LazyColumn for stable item identity.**

```kotlin
// Before
LazyColumn {
    items(books) { book ->
        BookItem(book)
    }
}

// After
LazyColumn {
    items(books, key = { it.id }) { book ->
        BookItem(book)
    }
}
```

**Line 67: Image missing contentDescription — required for accessibility.**

```kotlin
// Before
Image(painter = painterResource(R.drawable.cover), contentDescription = null)

// After — if decorative:
Image(painter = painterResource(R.drawable.cover), contentDescription = null) // OK if truly decorative

// After — if meaningful:
Image(
    painter = painterResource(R.drawable.cover),
    contentDescription = stringResource(R.string.book_cover_description)
)
```

### Summary

1. **State (high):** `collectAsState()` on line 14 does not respect lifecycle — replace with `collectAsStateWithLifecycle()`.
2. **Performance (medium):** Missing `key` in `LazyColumn` on line 42 causes unnecessary recomposition.
3. **Accessibility (medium):** Image on line 67 needs a meaningful `contentDescription`.

---

## References

- `references/api.md` — deprecated APIs and their modern replacements.
- `references/composables.md` — composable structure, naming, and composition patterns.
- `references/state.md` — state management, ViewModel, StateFlow, and data flow.
- `references/effects.md` — side effects: LaunchedEffect, DisposableEffect, SideEffect.
- `references/recomposition.md` — recomposition stability, @Stable/@Immutable, derivedStateOf.
- `references/navigation.md` — Navigation Compose, type-safe nav, nested graphs.
- `references/design.md` — Material 3 / Expressive theming, adaptive layouts.
- `references/accessibility.md` — TalkBack, semantics, content descriptions, touch targets.
- `references/performance.md` — LazyList optimization, remember, scope of state reads.
- `references/kotlin.md` — modern Kotlin patterns for Android.
- `references/hygiene.md` — code hygiene, testing, lint.
