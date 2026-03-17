---
name: Swift Ecosystem
description: This skill should be used when working with Swift projects, "Package.swift", "swift build/test/run", "swiftc", SwiftLint, SwiftFormat, or Swift language patterns. Provides comprehensive Swift ecosystem patterns and best practices for cross-platform CLI and library development.
version: 0.1.0
---

# Swift Language

## Type System

**Value vs Reference**:
- Structs/enums are value types (copied) - prefer for data models
- Classes are reference types (shared) - use when reference semantics or inheritance required
- Enums with associated values for algebraic data types

**Optionals**: Swift's nil-safety through `Optional` type.
```swift
if let value = optionalValue { use(value) }
guard let value = optionalValue else { return }
let value = optionalValue ?? defaultValue
let result = object?.property?.method()
```
Avoid force unwrap (`!`) - use safe unwrapping patterns.

**Protocols**: Define behavior contracts, prefer composition over inheritance.
```swift
protocol Identifiable { var id: String { get } }
protocol Timestamped { var createdAt: Date { get } }
struct User: Identifiable, Timestamped { ... }
```

**Generics**: Type parameters with constraints.
```swift
func process<T: Codable & Sendable>(_ item: T) -> Data { ... }
func compare<T>(_ a: T, _ b: T) -> Bool where T: Comparable { a < b }
```

**Noncopyable** (~Copyable, Swift 6+): Types with unique ownership.
```swift
struct UniqueResource: ~Copyable {
    consuming func release() { /* takes ownership */ }
}
```

## Error Handling

**Throwing functions**:
```swift
enum ParseError: Error { case invalidFormat, missingField(String) }
func parse(_ input: String) throws -> Config { ... }
do { let config = try parse(input) }
catch ParseError.invalidFormat { ... }
```

**Result type**: For async error handling or when throws is inconvenient.

**Typed throws** (Swift 6+): `func parse(_ input: String) throws(ParseError) -> Config`

## Concurrency (Swift 5.5+)

**async/await**:
```swift
func fetchData() async throws -> Data {
    let (data, _) = try await URLSession.shared.data(from: url)
    return data
}
```

**Actors**: Thread-safe mutable state.
```swift
actor Counter {
    private var value = 0
    func increment() { value += 1 }
    func getValue() -> Int { value }
}
```

**Sendable**: Mark types safe for concurrent access.

**Task groups**: Parallel execution with structured concurrency.
```swift
try await withThrowingTaskGroup(of: Result.self) { group in
    for item in items { group.addTask { try await process(item) } }
    return try await group.reduce(into: []) { $0.append($1) }
}
```

Rules: Use async/await over completion handlers, actors over locks, mark types Sendable when crossing concurrency boundaries.

## Memory Management

**Weak references**: Prevent retain cycles in closures/delegates.
```swift
service.fetch { [weak self] result in self?.handleResult(result) }
```

**Unowned**: Non-optional weak when lifetime is guaranteed.

## Common Patterns
- **Builder**: Fluent API for complex object construction
- **Result Builder** (`@resultBuilder`): DSL construction
- **Property Wrappers** (`@propertyWrapper`): Encapsulate property access patterns

## Anti-patterns
- Force unwrap (`!`) - Use safe unwrapping
- Force try (`try!`) - Use do-catch or propagate
- Classes for data - Use structs for value semantics
- `Any`/`AnyObject` abuse - Use generics or protocols
- Retain cycles - Use `[weak self]` or `[unowned self]`

# Swift Package Manager

## Project Structure
```
├── Package.swift
├── Sources/
│   ├── MyLibrary/
│   └── MyCLI/main.swift
├── Tests/MyLibraryTests/
└── Plugins/
```

## Package.swift
```swift
// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "MyPackage",
    products: [
        .library(name: "MyLibrary", targets: ["MyLibrary"]),
        .executable(name: "my-cli", targets: ["MyCLI"])
    ],
    dependencies: [
        .package(url: "https://github.com/apple/swift-argument-parser", from: "1.5.0"),
    ],
    targets: [
        .target(name: "MyLibrary"),
        .executableTarget(name: "MyCLI", dependencies: ["MyLibrary", .product(name: "ArgumentParser", package: "swift-argument-parser")]),
        .testTarget(name: "MyLibraryTests", dependencies: ["MyLibrary"])
    ]
)
```

## Commands
```bash
swift build                    # Compile
swift build -c release         # Release build
swift run                      # Build and run executable
swift test                     # Run all tests
swift test --filter MyTest     # Run specific test
swift package resolve          # Resolve dependencies
swift package update           # Update dependencies
swift package init --type library  # Create new package
```

# Toolchain

## SwiftLint
```yaml
# .swiftlint.yml
disabled_rules: [trailing_whitespace, line_length]
opt_in_rules: [empty_count, closure_spacing, force_unwrapping]
included: [Sources, Tests]
excluded: [.build, Packages]
line_length: { warning: 120, error: 200 }
```

## SwiftFormat (nicklockwood)
```
# .swiftformat
--swiftversion 6.0
--indent 4
--maxwidth 120
--self remove
--wraparguments before-first
```

## SourceKit-LSP
Bundled with Swift toolchain. Install Swift extension in VS Code for IDE integration.

## swift-testing (Swift 6+)
```swift
import Testing
@Test func addition() { #expect(1 + 1 == 2) }
@Test("Descriptive name") func subtraction() throws { #expect(try compute() > 0) }
@Test(arguments: [1, 2, 3]) func parameterized(value: Int) { #expect(value > 0) }
@Suite("Calculator") struct CalculatorTests { ... }
```

## swift-docc
```bash
swift package generate-documentation
```

# Context7 Integration
- Swift Language: `/swiftlang/swift`
- Argument Parser: `/apple/swift-argument-parser`
- Swift Log: `/apple/swift-log`
- SwiftFormat: `/nicklockwood/swiftformat`
- Vapor: `/vapor/vapor`
- Alamofire: `/alamofire/alamofire`

# Best Practices
- Use `swift build` for compilation; `swift test` for testing
- Run swiftlint before committing
- Format with swiftformat for consistent style
- Prefer value types (structs) over reference types (classes)
- Use async/await for asynchronous code
- Mark types as Sendable for concurrency safety
- Document public API with `///` doc comments
- Write tests alongside implementation
- Use Swift Testing framework for new test code
- Never use force unwrap (`!`) in library code
- Use guard for early exit patterns
