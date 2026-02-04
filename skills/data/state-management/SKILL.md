---
name: iOS State Management
description: Standards for Combine, Observation, and Reactive Programming.
metadata:
  labels: [ios, state, combine, observation, reactive, observation-framework]
  triggers:
    files: ['**/*.swift']
    keywords: [Observable, @Published, PassthroughSubject, @Observable, @Namespace]
---

# iOS State Management Standards

## **Priority: P0**

## Implementation Guidelines

### Combine (Reactive)

- **Publishers**: Use `@Published` for state in ViewModels. Use `PassthroughSubject` for one-time events (Transitions/Alerts).
- **Memory Management**: Store subscriptions in a `Set<AnyCancellable>`. Ensure they are cleared on deinit.
- **Operators**: Use operators like `.debounce`, `.filter`, `.map`, and `.flatMap` to transform input stream.
- **Schedulers**: Always prefix UI property updates with `@MainActor` or use `.receive(on: DispatchQueue.main)`.

### Observation Framework (iOS 17+)

- **@Observable**: Use for modern, macro-based observation. Replace `ObservableObject` in SwiftUI apps.
- **Binding**: Use `$state` for two-way bindings in SwiftUI. No boilerplate `objectWillChange` calls.

### Best Practices

- **ViewState Unification**: Prefer a single `State` enum or struct (Unidirectional) for complex screens.
- **Avoid Over-Reactive**: Don't use Combine for simple local flags. Use standard `@State` or variables.

## Anti-Patterns

- **Subscription Leaks**: `**No uncleared subscriptions**: Always use .store(in: &cancellables).`
- **Main Thread Violation**: `**No UI updates on Background**: Use .receive(on: .main).`
- **Manual objectWillChange**: `**No manual notifications**: Use @Published or @Observable.`

## References

- [Combine & Observation Setup](references/implementation.md)
