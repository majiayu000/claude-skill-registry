---
name: kotlin-timber-logger
description: Add Timber logging statements to Kotlin Android files. Analyzes code logic to insert debug, info, warning, and error logs at function entry/exit, conditionals, try-catch blocks, and state changes. Only accepts Kotlin files (.kt). Use via /timber command.
---

# Kotlin Timber Logger

Add intelligent Timber logging to Kotlin Android files based on code analysis.

## Activation

Trigger via `/timber <file.kt>` slash command.

## Input Validation

**STRICT**: Only `.kt` files accepted
- Reject non-Kotlin files immediately
- Verify file exists before processing

## Log Levels

| Level | Method | Use Case |
|-------|--------|----------|
| Debug | `Timber.d()` | Function flow, state changes |
| Info | `Timber.i()` | Important milestones |
| Warning | `Timber.w()` | Potential issues |
| Error | `Timber.e()` | Caught exceptions |

## Logging Strategy

### Function Entry/Exit
```kotlin
fun processData(input: String): Result {
    Timber.d("processData() input.length=${input.length}")
    // ... logic ...
    Timber.d("processData() completed")
    return result
}
```

### Suspend Functions
```kotlin
suspend fun fetchData(): Data {
    Timber.d("fetchData() started")
    // ... async logic ...
    Timber.d("fetchData() completed")
    return data
}
```

### Conditionals (when/if)
```kotlin
when (state) {
    State.LOADING -> Timber.d("State: LOADING")
    State.SUCCESS -> Timber.d("State: SUCCESS, items=${data.size}")
    State.ERROR -> Timber.w("State: ERROR, msg=${error.message}")
}
```

### Try-Catch
```kotlin
try {
    val result = parseJson(json)
    Timber.d("JSON parsed successfully")
} catch (e: Exception) {
    Timber.e(e, "JSON parsing failed")
}
```

### StateFlow Updates
```kotlin
_uiState.update { current ->
    Timber.d("State update: loading=${current.loading} -> true")
    current.copy(loading = true)
}
```

## Safety Rules

**NEVER log:**
- Passwords, tokens, API keys
- PII (personal identifiable information)
- Full large objects (use `.size` or `.take(3)`)

**Avoid:**
- Logs inside tight loops (throttle or count only)
- High-frequency callbacks

## Process

1. Validate input is `.kt` file
2. Read file, check for `import timber.log.Timber`
3. Identify patterns: functions, try-catch, conditionals, state changes
4. Add import if missing
5. Insert appropriate log statements
6. Report changes made

## Output Format

```
Timber Logging Added: [filename.kt]

Added [N] logs:
- [X] Timber.d() debug
- [X] Timber.w() warning
- [X] Timber.e() error

Instrumented:
- functionName() - entry/exit
- handleError() - try-catch
- when block - state transitions

Import added: Yes/No
```
