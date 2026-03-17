---
name: ios-stack
description: Stack decisions for iOS apps (SwiftUI, offline-first, push notifications). Reference before scaffolding or architecture work.
---

## Locked decisions

| Layer         | Decision                                                  |
| ------------- | --------------------------------------------------------- |
| Distribution  | App Store (starting without developer program membership) |
| UI            | SwiftUI                                                   |
| Architecture  | MVVM with lightweight service layer                       |
| Concurrency   | Swift async/await                                         |
| Persistence   | SwiftData (offline-first)                                 |
| Networking    | URLSession (scaffolded for future use)                    |
| Push          | Stubbed until signing available                           |
| Dependencies  | Minimal; Swift Package Manager only if needed             |
| Environments  | local → non-prod → prod                                   |
| Quality gates | Strict (tests required, SwiftLint enforced)               |

## Project layout

```
MyApp/
  Features/               # Feature modules (View + ViewModel)
  UIComponents/           # Shared UI primitives
  Services/
    Persistence/          # PersistenceStore protocol + SwiftDataStore
    Notifications/        # Push handling (stubbed)
    Network/              # API client (scaffolded)
    Config/               # Environment configuration
  Infrastructure/         # Router, composition root
  Models/                 # SwiftData models
  Resources/              # Assets, strings
```

## Key patterns

### Environment switching

- `Environment.swift` with `.local`, `.nonProd`, `.prod` cases
- Resolved at build time via scheme + build configuration
- API base URLs, feature flags per environment

### Persistence boundary

- `PersistenceStore` protocol defines all data operations
- `SwiftDataStore` is the concrete implementation
- ViewModels never touch SwiftData directly

### Push notification stubbing

- `NotificationService` exists with full interface
- Permission requests return simulated success in local/non-prod
- Token registration logs locally until signing available
- Swap to real implementation when developer membership active

## Reference

For versions, Xcode setup, and implementation patterns, see `reference/ios-stack-reference.md`
