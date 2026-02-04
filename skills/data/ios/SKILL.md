---
name: ios
description: Build, review, and refactor iOS mobile apps (Swift) using modern iOS patterns. Use for tasks like SwiftUI UI, navigation, state management, networking (URLSession), persistence (Core Data/SwiftData/Keychain), dependency injection, modularization (SPM), testing, performance, accessibility, and App Store release readiness.
---

# ios

Use this skill when working on iOS client (大前端 / 移动端) codebases.

## Defaults (unless repo dictates otherwise)

- Language: Swift
- UI: SwiftUI (if UIKit exists, follow existing architecture and integrate incrementally)
- Architecture: MVVM + unidirectional state where appropriate
- Concurrency: async/await, `Task`, `Actor` as needed
- Modularization: Swift Package Manager (SPM) if present

## Project structure (recommended)

- `App/`: application entry, app lifecycle, root navigation
- `Features/<Name>/`: feature modules (UI + ViewModel + domain models)
- `Core/`: shared utilities, design system, logging, networking primitives
- `Data/`: API clients, persistence implementations
- `Resources/`: assets, localization

## Workflow

1) Establish constraints
- iOS deployment target, supported devices, required permissions.
- SwiftUI vs UIKit and existing patterns (coordinator, reducers, etc.).

2) Define app flows
- Identify screens and navigation.
- Define `ViewState`/`Action` for each screen; keep states serializable and testable.

3) Networking
- Prefer `URLSession` + typed request/response models.
- Centralize auth headers, retries, and error mapping.
- Avoid leaking raw transport errors into UI; map to domain errors.

4) Persistence
- Choose one consistent approach: SwiftData/Core Data for structured data; UserDefaults for small prefs; Keychain for secrets/tokens.
- Add migration strategy notes if schema evolves.

5) UI & state
- Views should be mostly declarative; business logic lives in ViewModel.
- Make loading/error/empty states explicit.
- Use `@MainActor` for UI-facing state updates.

6) Performance & UX
- Minimize unnecessary view updates; use value types, `Equatable` states where helpful.
- Images: async loading/caching; list virtualization with `List` best practices.
- Accessibility: VoiceOver labels, Dynamic Type, sufficient contrast.

7) Quality gates
- Unit tests for ViewModels and domain logic.
- Snapshot/UI tests where valuable.
- Ensure release config (entitlements, signing, privacy strings) is correct.

## Output expectations when making changes

- Keep diffs localized; avoid broad refactors unless requested.
- Add/adjust tests when changing behavior.
- For new features: include navigation entry, state contract, and data wiring.

