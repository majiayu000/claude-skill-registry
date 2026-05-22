---
name: android
description: Build, review, and refactor Android mobile apps (Kotlin) using modern Android patterns. Use for tasks like setting up Gradle modules, Jetpack Compose UI, navigation, ViewModel/state management, networking (Retrofit/OkHttp), persistence (Room/DataStore), DI (Hilt/Koin), testing, performance, release builds, and Play Store readiness.
---

# android

Use this skill when working on Android client (大前端 / 移动端) codebases.

## Defaults (unless repo dictates otherwise)

- Language: Kotlin
- UI: Jetpack Compose (if legacy XML exists, follow existing structure)
- Architecture: MVVM + unidirectional data flow (UDF)
- Async: Kotlin Coroutines + Flow
- DI: Hilt if present; otherwise keep consistent with current

## Project structure (recommended)

- `app/`: application module (entry, navigation, composition root)
- `core/`: shared utilities and platform abstractions (optional)
- `data/`: API + persistence implementations
- `domain/`: use-cases, business models (pure Kotlin)
- `feature/<name>/`: feature modules or packages (UI + presentation)

## Workflow

1) Establish constraints
- Min/target SDK, build system, existing modules.
- Compose vs XML, single-module vs multi-module.

2) Define app flows
- Identify screens and navigation graph.
- Define state models per screen and their events/actions.

3) Data layer design
- API models vs domain models (mapping boundaries).
- Retrofit service interfaces + OkHttp interceptors (auth, logging).
- Caching strategy: memory vs disk (Room/DataStore).

4) UI & state
- Compose: keep Composables stateless where possible; state hoisted to ViewModel.
- ViewModel exposes `StateFlow<UiState>` and accepts events/intents.
- Handle loading/error/empty states explicitly.

5) Error handling
- Normalize errors (network, auth, validation) to domain-friendly types.
- Avoid leaking Retrofit/Room types into UI.

6) Performance & UX
- Avoid recomposition traps; use stable models and `remember`.
- Images: Coil; pagination for long lists; debounce inputs.
- Accessibility basics: content descriptions, large text support.

7) Quality gates
- Unit tests for domain and ViewModels.
- UI tests where meaningful (Compose testing).
- Lint/detekt/ktfmt if configured; keep build green.

## Output expectations when making changes

- Keep diffs localized; avoid broad refactors unless requested.
- Add/adjust tests when changing behavior.
- For new features: include navigation entry, UI state contract, and data wiring.

