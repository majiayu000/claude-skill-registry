---
name: swift-development
description: Provides core Swift 6+ language development capabilities, covering concurrency, macros, model design, and business logic. Use this skill when writing ViewModel, Service, or Repository layer code, defining data models, implementing algorithms, writing unit tests, or fixing concurrency warnings and data races.
---

# Swift 6 Development Skill

## Instructions

Follow this guide when working on non-UI Swift code, business logic, algorithms, or the data layer. Your goal is to write high-performance, thread-safe, and expressive Swift code.

## What This Skill Does

- **Concurrent Programming**: Write safe concurrent code using Actors, async/await, Task, and TaskGroup.
- **Type Safety**: Define Sendable types and use Typed Throws for precise error handling.
- **Testing**: Write modern unit tests using the Swift Testing framework.
- **Data Processing**: Write Codable models and encapsulate JSON parsing and network requests.
- **Macros**: Use or create macros to reduce boilerplate.

## When to Use This Skill

- When writing ViewModel, Service, or Repository layer code.
- When defining data models (structs, enums).
- When implementing algorithms or utility functions.
- When writing unit tests.
- When fixing concurrency warnings or data races.

## Examples

### Example 1: Defining a Safe Actor Service

```swift
/// A thread-safe user data service
actor UserService {
    private var cache: [String: User] = [:]
    
    // Use typed throws to specify the error type explicitly
    func fetchUser(id: String) async throws(NetworkError) -> User {
        if let cached = cache[id] {
            return cached
        }
        
        // Simulate network request
        let user = try await NetworkClient.shared.get("/users/\(id)", as: User.self)
        cache[id] = user
        return user
    }
}
```

### Example 2: Testing with Swift Testing

```swift
import Testing
@testable import MyApp

@Test("User parsing should succeed")
func userParsing() async throws {
    let json = """
    { "id": "1", "name": "Alice" }
    """.data(using: .utf8)!
    
    let user = try JSONDecoder().decode(User.self, from: json)
    
    #expect(user.name == "Alice")
    #expect(user.id == "1")
}
```

## Best Practices

- **Conform to Sendable**: Any type passed between concurrency domains must conform to the `Sendable` protocol.
- **Avoid Global Mutable State**: Avoid global variables unless protected by an Actor.
- **Implicitly Unwrapped Optionals**: Strictly forbidden (the force unwrap operator), except where unavoidable in initializers (very rare).
- **Use `let` over `var`**: Default to constants; use variables only when necessary.
- **Error Handling**: Prefer `throws` and `do-catch` over returning `Optional` or `Result` types (throws is more natural in async contexts).

## Notes

- Always pay attention to "Strict Concurrency Checking" compiler warnings.
- When handling closures across Actor boundaries, be mindful of `[weak self]` or `[unowned self]` (though usually not needed in `Task` unless breaking a reference cycle).
