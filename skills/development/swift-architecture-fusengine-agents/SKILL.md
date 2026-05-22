---
name: swift-architecture
description: Design Swift app architecture with MVVM, Clean Architecture, dependency injection, and repository patterns. Use when structuring iOS/macOS projects, creating ViewModels, implementing DI, or organizing code layers.
user-invocable: false
---

# Swift Architecture Patterns

## Recommended: MVVM + Clean Architecture

```
App/
├── Features/
│   └── UserProfile/
│       ├── Views/ProfileView.swift
│       ├── ViewModels/ProfileViewModel.swift
│       └── Models/User.swift
├── Core/
│   ├── Network/NetworkService.swift
│   ├── Persistence/DataRepository.swift
│   └── DI/Container.swift
└── Shared/
    ├── Components/
    └── Extensions/
```

## ViewModel with @Observable (iOS 17+)

```swift
import Observation

@Observable
final class ProfileViewModel {
    // State
    var user: User?
    var isLoading = false
    var error: Error?

    // Dependencies
    private let repository: UserRepositoryProtocol

    init(repository: UserRepositoryProtocol = UserRepository()) {
        self.repository = repository
    }

    @MainActor
    func loadUser(id: String) async {
        isLoading = true
        defer { isLoading = false }

        do {
            user = try await repository.fetch(id: id)
        } catch {
            self.error = error
        }
    }
}
```

## Repository Pattern

```swift
protocol UserRepositoryProtocol: Sendable {
    func fetch(id: String) async throws -> User
    func save(_ user: User) async throws
}

final class UserRepository: UserRepositoryProtocol {
    private let api: APIClientProtocol
    private let cache: CacheProtocol

    init(api: APIClientProtocol, cache: CacheProtocol) {
        self.api = api
        self.cache = cache
    }

    func fetch(id: String) async throws -> User {
        if let cached: User = cache.get(key: id) { return cached }
        let user = try await api.get("/users/\(id)")
        cache.set(key: id, value: user)
        return user
    }
}
```

## Dependency Injection with Environment

```swift
// Define environment key
private struct APIClientKey: EnvironmentKey {
    static let defaultValue: APIClientProtocol = APIClient()
}

extension EnvironmentValues {
    var apiClient: APIClientProtocol {
        get { self[APIClientKey.self] }
        set { self[APIClientKey.self] = newValue }
    }
}

// Usage in App
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.apiClient, APIClient())
        }
    }
}
```

## Layer Responsibilities

| Layer | Contains | Depends On |
|-------|----------|------------|
| **Presentation** | View, ViewModel | Domain |
| **Domain** | Entity, UseCase, Protocol | Nothing |
| **Data** | Repository, DataSource, DTO | Domain |
