---
name: Kotlin Language Patterns
description: idiomatic Kotlin 1.9+ standards (Null Safety, Expressions, Extensions).
metadata:
  labels: [kotlin, language, idioms, null-safety]
  triggers:
    files: ['**/*.kt', '**/*.kts']
    keywords: [val, var, null, extension, data class, sealed, when]
---

# Kotlin Language Patterns

## **Priority: P0 (CRITICAL)**

Modern, idiomatic Kotlin standards for safety and conciseness.

## Implementation Guidelines

- **Immutability**: Use `val` by default. Only use `var` if mutation is required locally.
- **Null Safety**: Use `?` for nullable types. Use safe call `?.` and Elvis `?:` over `!!`.
- **Expressions**: Prefer expression bodies `fun foo() = ...` for one-liners. Use `if` and `try` as expressions.
- **Classes**: Use `data class` for DTOs. Use `sealed interface/class` for state hierarchies (Result, UIState).
- **Extension Functions**: Prefer extensions over utility classes (`StringUtil`). Keep them private/internal if specific to a module.
- **Named Arguments**: Use named arguments for clarity, especially with booleans or multiple params of same type.
- **String Templates**: Use `"$var"` over concatenation. Use `"""` for multiline strings (SQL/JSON).

## Anti-Patterns

- **Not-null Assertion (`!!`)**: `**No !!**: Never use in production code; use safe calls or requireNotNull.`
- **Java-isms**: `**No get/set prefixes**: Use properties. Prefer top-level functions over companion object statics.`
- **Lateinit Abuse**: `**Avoid lateinit var**: Prefer nullable types or lazy delegates.`
- **Empty Catch**: `**No Silenced Errors**: Never swallow exceptions without logging or handling.`

## Code

```kotlin
// Sealed Class + When Expression
sealed interface UiState {
    data object Loading : UiState
    data class Success(val data: List<String>) : UiState
    data class Error(val message: String) : UiState
}

fun render(state: UiState) = when (state) {
    UiState.Loading -> showLoading()
    is UiState.Success -> showData(state.data)
    is UiState.Error -> logError(state.message) // Smart cast
}

// Extension Function
private fun String.toSlug(): String = this.lowercase().replace(" ", "-")
```

## Related Topics

best-practices | coroutines | android
