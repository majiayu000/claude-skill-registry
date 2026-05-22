---
name: swift-guide
description: |
  Swift language guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Swift files (.swift), Package.swift, or when the user mentions Swift.
  Provides optionals handling, protocol-oriented patterns, concurrency with async/await,
  and testing standards specific to this project's coding standards.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: language
  language: swift
  extensions: ".swift"
---

# Swift Guide

> Applies to: Swift 5.9+, iOS/macOS/Server-Side, SPM, Concurrency

## Core Principles

1. **Value Semantics First**: Prefer structs over classes; use classes only when identity or inheritance is required
2. **Protocol-Oriented Design**: Compose behavior through protocols and extensions rather than class hierarchies
3. **Safe Optionals**: Unwrap explicitly with `guard let` or `if let`; force-unwrap (`!`) is forbidden outside tests
4. **Structured Concurrency**: Use async/await and task groups; avoid raw GCD queues for new code
5. **Compiler as Ally**: Enable strict concurrency checking; treat warnings as errors in CI

## Guardrails

### Version & Dependencies

- Use Swift 5.9+ with Swift Package Manager (Package.swift)
- Pin package versions with `.upToNextMinor(from:)` for libraries
- Run `swift package resolve` before committing after dependency changes
- Commit `Package.resolved` for applications; omit for libraries

### Code Style

- Run `swift format` or SwiftLint before every commit
- Follow [Swift API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/)
- `PascalCase` for types, protocols, enums | `camelCase` for functions, properties, variables
- Prefer trailing closure syntax for the last closure parameter
- Use `Self` instead of repeating the type name inside type definitions
- Mark classes `final` by default; remove `final` only when subclassing is designed for

### Optionals

- Use `guard let` for early exit when the unwrapped value is needed afterward
- Use `if let` for scoped unwrapping within a branch
- Use nil coalescing (`??`) for default values; optional chaining (`?.`) to traverse
- Never force-unwrap (`!`) outside of tests and `IBOutlet` declarations
- Use `compactMap` to filter nil from collections; `Optional.map`/`.flatMap` to transform

### Concurrency

- Use `async/await` for all asynchronous operations (no completion handlers in new code)
- Use `TaskGroup` / `ThrowingTaskGroup` for parallel fan-out
- Mark UI-bound code with `@MainActor`; avoid `DispatchQueue.main` in new code
- Use `actor` for mutable shared state; prefer actors over locks
- Conform types crossing isolation boundaries to `Sendable`
- Enable strict concurrency: `-strict-concurrency=complete`
- Always handle `Task.isCancelled` or `Task.checkCancellation()` in long-running work

### Protocols

- Define protocols where they are consumed, not where they are implemented
- Keep protocols focused: prefer multiple small protocols over one large one
- Use protocol extensions for default implementations of computed logic
- Use protocol composition (`SomeProtocol & AnotherProtocol`) for flexible constraints
- Prefer `some Protocol` (opaque types) over `any Protocol` when the concrete type is fixed

## Project Structure

```
MyProject/
├── Package.swift              # Manifest (targets, dependencies, platforms)
├── Package.resolved           # Locked versions (commit for apps)
├── Sources/
│   ├── MyProject/             # Main library target
│   │   ├── Models/
│   │   ├── Services/
│   │   ├── Protocols/
│   │   └── Extensions/        # TypeName+Capability.swift
│   └── MyProjectCLI/          # Executable target (thin entry point)
│       └── main.swift
├── Tests/
│   └── MyProjectTests/
└── README.md
```

- `main.swift` or `@main` struct should be thin: parse arguments, build dependencies, call library code
- Put all business logic in library targets (testable without running the binary)
- One primary type per file, file named after the type

## Key Patterns

### Optionals: guard let / if let

```swift
func processUser(id: String?) -> User {
    guard let id, !id.isEmpty else {
        return User.anonymous
    }
    guard let user = userCache[id] else {
        return fetchUser(id: id)
    }
    return user
}

func displayName(for user: User) -> String {
    if let nickname = user.nickname { return nickname }
    return "\(user.firstName) \(user.lastName)"
}
```

### Result Type for Typed Errors

```swift
enum NetworkError: Error, Sendable {
    case invalidURL(String)
    case serverError(statusCode: Int)
    case decodingFailed(underlying: Error)
}

func fetchData(from urlString: String) async -> Result<Data, NetworkError> {
    guard let url = URL(string: urlString) else { return .failure(.invalidURL(urlString)) }
    do {
        let (data, response) = try await URLSession.shared.data(from: url)
        guard let http = response as? HTTPURLResponse, (200..<300).contains(http.statusCode) else {
            return .failure(.serverError(statusCode: 0))
        }
        return .success(data)
    } catch {
        return .failure(.decodingFailed(underlying: error))
    }
}
```

### Protocol Extensions with Defaults

```swift
protocol Timestamped {
    var createdAt: Date { get }
    var updatedAt: Date { get }
}

extension Timestamped {
    var isRecent: Bool { updatedAt.timeIntervalSinceNow > -86_400 }
}

// Protocol composition for flexible constraints
func findRecent<T: Identifiable & Timestamped>(_ items: [T]) -> [T] {
    items.filter(\.isRecent)
}
```

### Actor for Shared Mutable State

```swift
actor CacheStore<Key: Hashable & Sendable, Value: Sendable> {
    private var storage: [Key: Value] = [:]
    private let maxSize: Int

    init(maxSize: Int = 1000) { self.maxSize = maxSize }

    func get(_ key: Key) -> Value? { storage[key] }

    func set(_ key: Key, value: Value) {
        if storage.count >= maxSize { storage.removeAll() }
        storage[key] = value
    }
}
```

### Async/Await with Task Groups

```swift
func fetchAllUsers(ids: [String]) async throws -> [User] {
    try await withThrowingTaskGroup(of: User.self) { group in
        for id in ids {
            group.addTask { try await self.fetchUser(id: id) }
        }
        var users: [User] = []
        for try await user in group { users.append(user) }
        return users
    }
}
```

### Sendable Conformance

```swift
// Value types: implicitly Sendable when all stored properties are Sendable
struct UserDTO: Sendable { let id: String; let name: String }

// Classes: must be final with immutable properties, or use @unchecked with a lock
final class AppConfig: Sendable { let apiBaseURL: URL; let maxRetries: Int
    init(apiBaseURL: URL, maxRetries: Int = 3) { self.apiBaseURL = apiBaseURL; self.maxRetries = maxRetries }
}
```

### Property Wrappers

```swift
@propertyWrapper
struct Clamped<Value: Comparable> {
    private var value: Value
    private let range: ClosedRange<Value>

    var wrappedValue: Value {
        get { value }
        set { value = min(max(newValue, range.lowerBound), range.upperBound) }
    }

    init(wrappedValue: Value, _ range: ClosedRange<Value>) {
        self.range = range
        self.value = min(max(wrappedValue, range.lowerBound), range.upperBound)
    }
}

struct AudioSettings {
    @Clamped(0...100) var volume: Int = 50
    @Clamped(0.5...2.0) var playbackSpeed: Double = 1.0
}
```

### Result Builders for DSLs

```swift
@resultBuilder
struct ArrayBuilder<Element> {
    static func buildBlock(_ components: [Element]...) -> [Element] { components.flatMap { $0 } }
    static func buildExpression(_ expression: Element) -> [Element] { [expression] }
    static func buildOptional(_ component: [Element]?) -> [Element] { component ?? [] }
    static func buildEither(first c: [Element]) -> [Element] { c }
    static func buildEither(second c: [Element]) -> [Element] { c }
}
```

## Testing

### XCTest with Async Support

```swift
import XCTest
@testable import MyProject

final class UserServiceTests: XCTestCase {
    private var sut: UserService!
    private var mockRepo: MockUserRepository!

    override func setUp() { super.setUp(); mockRepo = MockUserRepository(); sut = UserService(repository: mockRepo) }
    override func tearDown() { sut = nil; mockRepo = nil; super.tearDown() }

    func test_fetchUser_withValidID_returnsUser() async throws {
        mockRepo.stubbedUser = User(id: "1", name: "Alice")
        let user = try await sut.fetchUser(id: "1")
        XCTAssertEqual(user.name, "Alice")
    }

    func test_fetchUser_withInvalidID_throwsNotFound() async {
        mockRepo.stubbedError = .notFound
        do {
            _ = try await sut.fetchUser(id: "invalid")
            XCTFail("Expected notFound error")
        } catch let error as ServiceError {
            XCTAssertEqual(error, .notFound)
        } catch {
            XCTFail("Unexpected error: \(error)")
        }
    }
}
```

### Testing Standards

- Test names describe behavior: `func test_login_withExpiredToken_refreshesAutomatically()`
- Use `setUp()` / `tearDown()` for shared test fixtures
- Use protocol-based mocks injected via initializer (no singletons)
- Async tests use `async throws` directly (no XCTestExpectation for async/await code)
- Coverage target: >80% for business logic, >60% overall
- Test both success and failure paths for every public method

## Tooling

### Essential Commands

```bash
swift build                         # Build all targets
swift test                          # Run all tests
swift test --enable-code-coverage   # With coverage
swift package resolve               # Resolve dependencies
swift package update                # Update dependencies
swift format .                      # Format (swift-format)
swiftlint                           # Lint (SwiftLint)
swiftlint --fix                     # Auto-fix lint issues
```

### SwiftLint Key Rules

```yaml
# .swiftlint.yml -- enforce these as errors
force_cast: error
force_unwrapping: error
force_try: error
function_body_length:
  warning: 40
  error: 50
cyclomatic_complexity:
  warning: 8
  error: 10
```

### Package.swift Essentials

```swift
// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "MyProject",
    platforms: [.macOS(.v14), .iOS(.v17)],
    dependencies: [
        .package(url: "https://github.com/apple/swift-argument-parser", from: "1.3.0"),
        .package(url: "https://github.com/apple/swift-log", from: "1.5.0"),
    ],
    targets: [
        .target(name: "MyProject", dependencies: [
            .product(name: "Logging", package: "swift-log"),
        ], swiftSettings: [
            .enableExperimentalFeature("StrictConcurrency"),
        ]),
        .testTarget(name: "MyProjectTests", dependencies: ["MyProject"]),
    ]
)
```

## References

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Actor patterns, protocol composition, async sequences

## External References

- [The Swift Programming Language](https://docs.swift.org/swift-book/)
- [Swift API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/)
- [Swift Evolution Proposals](https://github.com/apple/swift-evolution)
- [Swift Package Manager Docs](https://www.swift.org/documentation/package-manager/)
- [SwiftLint](https://github.com/realm/SwiftLint)
- [swift-format](https://github.com/apple/swift-format)
- [Swift on Server](https://www.swift.org/server/)
