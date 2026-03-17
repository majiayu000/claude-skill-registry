---
name: swift-patterns
description: Use when creating Swift projects (iOS, macOS, CLI, frameworks), making memory management decisions, or working with Swift concurrency
---

# Swift Patterns

Tooling opinions, memory management, concurrency decisions, and non-linter-enforceable style rules.

## Style Guide

Source: Google Swift Style Guide + Swift API Design Guidelines. Only rules linters/formatters cannot enforce.

### Naming
- Treat acronyms as whole words: `loadHttpUrl` not `loadHTTPURL`
- Boolean names: `is`, `has`, `can`, `should` prefix
- Methods: imperative for side-effects (`sort()`), nouns for queries (`sorted()`)
- Mutating pairs: `sort()`/`sorted()`, `formUnion()`/`union()`
- Delegate patterns: `didFinish`, `willStart`, `shouldAllow` prefix
- File naming: `MyType+Protocol.swift` for extensions implementing protocols
- Error types: `Error` suffix (`NetworkError`, `ValidationError`)
- Avoid getters/setters: computed properties, not `getX()` methods

### Practices
- Force unwrap `!` requires safety comment explaining why nil is impossible
- `guard` over nested `if` for early exits
- Protocol naming: nouns (`Collection`) vs `-able`/`-ible`/`-ing` (`Equatable`, `Copying`)
- No `Any` without runtime check immediately after
- Error handling: throw custom error types, not `Optional` for recoverable failures
- Comments explain WHY, not WHAT
- Max function body ~40 lines

### SwiftLint Essential Rules (non-formatter)
```yaml
opt_in_rules:
  - explicit_init
  - explicit_type_interface
  - force_unwrapping
  - implicitly_unwrapped_optional
line_length: 120
function_body_length: 40
```

## Tooling Defaults

| Concern | Use | Why |
|---------|-----|-----|
| Package manager | SPM (Swift Package Manager) | Native, integrated, zero config |
| Linter | SwiftLint | De facto standard |
| Formatter | swift-format | Official Apple tool |
| Testing | XCTest or Swift Testing (5.9+) | Built-in, mature ecosystem |
| Dependencies | SPM only | Avoid CocoaPods/Carthage complexity |

### swift-format config
```json
{
  "version": 1,
  "lineLength": 120,
  "indentation": { "spaces": 2 },
  "respectsExistingLineBreaks": true
}
```

## Project Types

| Type | When | Structure |
|------|------|-----------|
| **iOS App** | iPhone/iPad apps | Xcode project + SPM for deps |
| **macOS App** | Desktop apps | Xcode project + AppKit/SwiftUI |
| **Framework** | Reusable libraries | SPM-only, no Xcode project |
| **CLI** | Command-line tools | SPM with executable target |
| **Multi-platform** | iOS + macOS + watchOS | Shared code in SPM package |

### Framework Package.swift
```swift
// swift-tools-version: 5.9
import PackageDescription

let package = Package(
  name: "MyLibrary",
  platforms: [.iOS(.v16), .macOS(.v13)],
  products: [
    .library(name: "MyLibrary", targets: ["MyLibrary"])
  ],
  dependencies: [],
  targets: [
    .target(name: "MyLibrary"),
    .testTarget(name: "MyLibraryTests", dependencies: ["MyLibrary"])
  ]
)
```

### Directory Structure
```
Sources/MyLibrary/
  MyLibrary.swift
  Models/
  Views/
  Utilities/
Tests/MyLibraryTests/
  MyLibraryTests.swift
Package.swift
.swiftlint.yml
```

## Memory Management (ARC)

### Weak vs Unowned Decision

| Use `weak` | Use `unowned` | Use strong |
|------------|---------------|------------|
| Optional relationship (may outlive) | Non-optional, guaranteed lifetime | Ownership responsibility |
| Parent-child with independent lifecycle | Child-parent where child can't outlive | Default case |
| Delegate patterns | Closure capturing guaranteed-alive context | Value types (struct, enum) |

**Rule**: Start with `weak`, switch to `unowned` only after profiling shows measurable overhead.

### Common Retain Cycles

#### Closures
```swift
// WRONG - self captured strongly
class ViewModel {
  var onUpdate: (() -> Void)?
  func setup() {
    onUpdate = {
      self.refresh()  // retain cycle
    }
  }
}

// RIGHT - weak self
class ViewModel {
  var onUpdate: (() -> Void)?
  func setup() {
    onUpdate = { [weak self] in
      self?.refresh()
    }
  }
}
```

#### Delegates
```swift
// WRONG
protocol ViewDelegate: AnyObject {}
class View {
  var delegate: ViewDelegate?  // should be weak
}

// RIGHT
class View {
  weak var delegate: ViewDelegate?
}
```

#### Two-way relationships
```swift
// WRONG
class Parent {
  var child: Child?
}
class Child {
  var parent: Parent?  // retain cycle
}

// RIGHT
class Parent {
  var child: Child?
}
class Child {
  weak var parent: Parent?
}
```

### Performance Note
`unowned` < `weak` overhead (no optional check), but profile first. Premature optimization causes crashes.

## Concurrency Patterns

### async/await vs GCD Decision

| Use async/await | Use GCD |
|-----------------|---------|
| Default for all new code | Legacy code integration |
| Structured concurrency needed | Fire-and-forget tasks |
| Error propagation matters | Very low-level control required |

**Rule**: Always prefer async/await unless integrating with legacy GCD code.

### @MainActor Usage

```swift
// Entire class
@MainActor
class ViewModel {
  var items: [Item] = []
  func update() { /* runs on main thread */ }
}

// Individual methods
class ViewModel {
  @MainActor
  func updateUI() { /* main thread */ }

  func fetchData() async { /* background */ }
}

// SwiftUI views (implicit @MainActor on body)
struct ContentView: View {
  var body: some View { /* always main thread */ }
}
```

### Actor Patterns

```swift
// Isolate mutable state
actor DataCache {
  private var cache: [String: Data] = [:]

  func get(_ key: String) -> Data? { cache[key] }
  func set(_ key: String, _ value: Data) { cache[key] = value }
}

// Usage
let cache = DataCache()
await cache.set("key", data)
let value = await cache.get("key")
```

### Task and TaskGroup

```swift
// Single task
Task {
  let data = await fetchData()
  await MainActor.run { updateUI(data) }
}

// Parallel tasks
await withThrowingTaskGroup(of: Data.self) { group in
  for url in urls {
    group.addTask { try await fetch(url) }
  }
  var results: [Data] = []
  for try await result in group {
    results.append(result)
  }
  return results
}
```

### AsyncStream for Event Streams

```swift
func locationUpdates() -> AsyncStream<Location> {
  AsyncStream { continuation in
    let manager = LocationManager()
    manager.onUpdate = { location in
      continuation.yield(location)
    }
    continuation.onTermination = { _ in
      manager.stop()
    }
    manager.start()
  }
}

// Usage
for await location in locationUpdates() {
  print(location)
}
```

### Task Cancellation

```swift
let task = Task {
  for i in 1...100 {
    try Task.checkCancellation()  // throws CancellationError
    await doWork(i)
  }
}

// Later
task.cancel()
```

## Common Gotchas

### Force unwraps crash at runtime
```swift
// WRONG - crashes if nil
let value = dict["key"]!

// RIGHT - handle nil case
guard let value = dict["key"] else { return }
```

### Implicitly unwrapped optionals
```swift
// WRONG - use rarely, mostly for IBOutlets
var name: String!

// RIGHT - use Optional
var name: String?
```

### Blocking main actor
```swift
// WRONG - freezes UI
@MainActor
func load() {
  let data = heavyComputation()  // blocks main thread
}

// RIGHT - offload work
@MainActor
func load() async {
  let data = await Task.detached {
    heavyComputation()
  }.value
}
```

### Actor reentrancy
```swift
actor Counter {
  var value = 0

  func increment() async {
    let old = value  // suspension point
    await Task.sleep(1_000_000_000)
    value = old + 1  // WRONG - value may have changed
  }
}

// RIGHT - atomic operation
actor Counter {
  var value = 0
  func increment() { value += 1 }
}
```

### Sendable violations
```swift
// WRONG - class not Sendable
class Data {}
Task {
  let data = Data()  // compiler error in strict concurrency
}

// RIGHT - use struct or mark @unchecked
struct Data: Sendable {}
```

### Task cancellation not automatic
```swift
// WRONG - continues even if task cancelled
Task {
  for i in 1...100 {
    await fetch(i)
  }
}

// RIGHT - check cancellation
Task {
  for i in 1...100 {
    try Task.checkCancellation()
    await fetch(i)
  }
}
```

### Weak self dance
```swift
// WRONG - crashes if self deallocated
closure { [weak self] in
  guard let self else { return }
  self.doWork()
  await self.asyncWork()  // self might be nil now
}

// RIGHT - recapture or use local
closure { [weak self] in
  guard let self else { return }
  doWork()
  Task { [weak self] in
    await self?.asyncWork()
  }
}
```

### Array/Dictionary copy-on-write
```swift
// Arrays are value types but COW optimized
var a = [1, 2, 3]
var b = a  // no copy yet
b.append(4)  // copy happens here
```

### Struct vs Class decision

| Use struct | Use class |
|------------|-----------|
| Value semantics needed | Reference semantics needed |
| Immutable data models | Lifecycle management (deinit) |
| No inheritance | Inheritance required |
| Small, simple types | Complex objects with identity |

### Protocol with associated type limitations
```swift
// Can't use as type directly
protocol Container {
  associatedtype Item
  func get() -> Item
}

// Need generics or type erasure
func process<C: Container>(_ container: C) { }
```

### Escaping closure retain cycles
```swift
// WRONG
class ViewModel {
  var completion: (() -> Void)?
  func start() {
    networkCall { [self] in  // captures self strongly
      self.completion?()
    }
  }
}

// RIGHT
class ViewModel {
  var completion: (() -> Void)?
  func start() {
    networkCall { [weak self] in
      self?.completion?()
    }
  }
}
```

## Testing Patterns

### XCTest
```swift
import XCTest
@testable import MyLibrary

final class MyTests: XCTestCase {
  func testExample() {
    let result = compute(5)
    XCTAssertEqual(result, 10)
  }

  func testAsync() async throws {
    let data = try await fetchData()
    XCTAssertNotNil(data)
  }
}
```

### Swift Testing (5.9+)
```swift
import Testing
@testable import MyLibrary

@Test func computation() {
  #expect(compute(5) == 10)
}

@Test func asyncOperation() async throws {
  let data = try await fetchData()
  #expect(data != nil)
}
```

### Dependency Injection for Testability
```swift
// Production
protocol NetworkService {
  func fetch() async throws -> Data
}

class ViewModel {
  private let network: NetworkService
  init(network: NetworkService) {
    self.network = network
  }
}

// Test
class MockNetwork: NetworkService {
  func fetch() async throws -> Data { Data() }
}

let vm = ViewModel(network: MockNetwork())
```

## Error Handling Patterns

### Result Type
```swift
func parse(_ input: String) -> Result<Int, ParseError> {
  guard let value = Int(input) else {
    return .failure(.invalidFormat)
  }
  return .success(value)
}

// Usage
switch parse("42") {
case .success(let value): print(value)
case .failure(let error): print(error)
}
```

### Custom Error Types
```swift
enum NetworkError: Error {
  case invalidURL
  case timeout
  case serverError(statusCode: Int)
}

func fetch() throws -> Data {
  throw NetworkError.timeout
}
```

### LocalizedError for User-Facing Messages
```swift
enum ValidationError: LocalizedError {
  case tooShort
  case invalidFormat

  var errorDescription: String? {
    switch self {
    case .tooShort: "Input is too short"
    case .invalidFormat: "Invalid format"
    }
  }
}
```

## Performance Tips

### Lazy Properties
```swift
class ViewModel {
  lazy var formatter: DateFormatter = {
    let f = DateFormatter()
    f.dateStyle = .long
    return f
  }()
}
```

### Copy-on-Write
```swift
// Arrays, dictionaries, sets use COW automatically
// Custom types:
struct MyCollection {
  private var storage: NSMutableArray

  mutating func append(_ item: Any) {
    if !isKnownUniquelyReferenced(&storage) {
      storage = storage.mutableCopy() as! NSMutableArray
    }
    storage.add(item)
  }
}
```

### @inline Hints
```swift
@inline(__always) func critical() { }
@inline(never) func debug() { }
```

### Profile with Instruments
- Time Profiler: CPU hotspots
- Allocations: memory usage
- Leaks: retain cycles
- System Trace: concurrency issues
