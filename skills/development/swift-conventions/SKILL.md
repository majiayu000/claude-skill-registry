---
name: swift-conventions
description: "Expert Swift decisions Claude doesn't instinctively make: struct vs class trade-offs, @MainActor placement, async/await vs Combine selection, memory management pitfalls, and iOS-specific anti-patterns. Use when writing Swift code for iOS/tvOS apps, reviewing Swift architecture decisions, or debugging memory/concurrency issues. Trigger keywords: Swift, iOS, tvOS, actor, async, Sendable, retain cycle, memory leak, struct, class, protocol, generic"
version: "3.0.0"
---

# Swift Conventions — Expert Decisions

Expert decision frameworks for Swift choices that require experience. Claude knows Swift syntax — this skill provides the judgment calls.

---

## Decision Trees

### Struct vs Class

```
Need shared mutable state across app?
├─ YES → Class (singleton pattern, session managers)
└─ NO
   └─ Need inheritance hierarchy?
      ├─ YES → Class (UIKit subclasses, NSObject interop)
      └─ NO
         └─ Data model or value type?
            ├─ YES → Struct (User, Configuration, Point)
            └─ NO → Consider what identity means
               ├─ Same instance matters → Class
               └─ Same values matters → Struct
```

**The non-obvious trade-off**: Structs with reference-type properties (arrays, classes inside) lose copy-on-write benefits. A `struct` containing `[UIImage]` copies the array reference, not images — mutations affect all "copies."

### async/await vs Combine vs Callbacks

```
Is this a one-shot operation? (fetch user, save file)
├─ YES → async/await (cleaner, better stack traces)
└─ NO → Is it a stream of values over time?
   ├─ YES
   │  └─ Need transformations/combining?
   │     ├─ Heavy transforms → Combine (map, filter, merge)
   │     └─ Simple iteration → AsyncStream
   └─ NO → Must support iOS 14?
      ├─ YES → Combine or callbacks
      └─ NO → async/await with continuation
```

**When Combine still wins**: Multiple publishers needing `combineLatest`, `merge`, or `debounce`. Converting this to pure async/await requires manual coordination that Combine handles elegantly.

### @MainActor Placement

```
Is every public method UI-related?
├─ YES → @MainActor on class/struct
└─ NO
   └─ Does it manage UI state? (@Published, bindings)
      ├─ YES → @MainActor on class, nonisolated for non-UI methods
      └─ NO
         └─ Only some methods touch UI?
            ├─ YES → @MainActor on specific methods
            └─ NO → No @MainActor needed
```

**Critical**: `@Published` properties MUST be updated on MainActor. SwiftUI observes on main thread — background updates cause undefined behavior, not just warnings.

### TaskGroup vs async let

```
Number of concurrent operations known at compile time?
├─ YES (2-5 fixed operations) → async let
│  Example: async let user = fetchUser()
│           async let posts = fetchPosts()
│
└─ NO (dynamic count, array of IDs) → TaskGroup
   Example: for id in userIds { group.addTask { ... } }
```

**async let gotcha**: All `async let` values MUST be awaited before scope ends. Forgetting to await silently cancels the task — no error, just missing data.

---

## NEVER Do

### Memory & Retain Cycles

**NEVER** capture `self` strongly in stored closures:
```swift
// ❌ Retain cycle — ViewModel never deallocates
class ViewModel {
    var onUpdate: (() -> Void)?

    func setup() {
        onUpdate = { self.refresh() } // self → onUpdate → self
    }
}

// ✅ Break with weak capture
onUpdate = { [weak self] in self?.refresh() }
```

**NEVER** use `unowned` unless you can PROVE the reference outlives the closure. When in doubt, use `weak`. The crash from dangling `unowned` is worse than the nil-check cost.

**NEVER** forget Timer invalidation:
```swift
// ❌ Timer retains target — object never deallocates
timer = Timer.scheduledTimer(target: self, selector: #selector(tick), ...)

// ✅ Block-based with weak capture + invalidate in deinit
timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { [weak self] _ in
    self?.tick()
}
deinit { timer?.invalidate() }
```

### Concurrency

**NEVER** access `@Published` from background:
```swift
// ❌ Undefined behavior — may work sometimes, crash others
Task.detached {
    viewModel.isLoading = false // Background thread!
}

// ✅ Explicit MainActor
Task { @MainActor in
    viewModel.isLoading = false
}
```

**NEVER** use `Task { }` for fire-and-forget without understanding cancellation:
```swift
// ❌ Task inherits actor context — may block UI
func buttonTapped() {
    Task { await heavyOperation() } // Runs on MainActor!
}

// ✅ Explicit detachment for background work
func buttonTapped() {
    Task.detached(priority: .userInitiated) {
        await heavyOperation()
    }
}
```

**NEVER** assume `Task.cancel()` stops execution immediately. Cancellation is cooperative — your code must check `Task.isCancelled` or use `try Task.checkCancellation()`.

### Optionals

**NEVER** force-unwrap in production code except:
1. `@IBOutlet` — set by Interface Builder
2. `URL(string: "https://known-valid.com")!` — compile-time known strings
3. `fatalError` paths where crash is correct behavior

**NEVER** use implicitly unwrapped optionals (`var user: User!`) for regular properties. Only valid for:
- `@IBOutlet` connections
- Two-phase initialization where value is set immediately after init

### Protocol Design

**NEVER** make protocols require `AnyObject` unless you need `weak` references:
```swift
// ❌ Unnecessarily restricts to classes
protocol DataProvider: AnyObject {
    func fetchData() -> Data
}

// ✅ Only require AnyObject for delegates that need weak reference
protocol ViewModelDelegate: AnyObject { // Needed for weak var delegate
    func viewModelDidUpdate()
}
```

**NEVER** add default implementations that change protocol semantics:
```swift
// ❌ Dangerous — conformers might not override
protocol Validator {
    func validate() -> Bool
}
extension Validator {
    func validate() -> Bool { true } // Silent "always valid"
}

// ✅ Make requirement obvious or use different name
extension Validator {
    func isAlwaysValid() -> Bool { true } // Clear this is a default
}
```

---

## iOS-Specific Patterns

### Dependency Injection in ViewModels

```swift
// ✅ Protocol-based for testability
protocol UserServiceProtocol {
    func fetchUser(id: String) async throws -> User
}

@MainActor
final class UserViewModel: ObservableObject {
    @Published private(set) var user: User?
    @Published private(set) var error: Error?

    private let userService: UserServiceProtocol

    init(userService: UserServiceProtocol = UserService()) {
        self.userService = userService
    }
}
```

**Why default parameter**: Production code uses real service, tests inject mock. No container framework needed for most apps.

### Property Wrapper Selection

| Wrapper | Use When | Memory Behavior |
|---------|----------|-----------------|
| `@State` | View-local primitive/value types | View-owned, recreated on parent rebuild |
| `@StateObject` | View creates and owns the ObservableObject | Created once, survives view rebuilds |
| `@ObservedObject` | View receives ObservableObject from parent | Not owned, may be recreated |
| `@EnvironmentObject` | Shared across view hierarchy | Must be injected by ancestor |
| `@Binding` | Two-way connection to parent's state | Reference to parent's storage |

**The StateObject vs ObservedObject trap**: Using `@ObservedObject` for a locally-created object causes recreation on every view update — losing all state.

### Error Handling Strategy

```swift
// Domain-specific errors with recovery info
enum UserError: LocalizedError {
    case notFound(userId: String)
    case unauthorized
    case networkFailure(underlying: Error)

    var errorDescription: String? {
        switch self {
        case .notFound(let id): return "User \(id) not found"
        case .unauthorized: return "Please log in again"
        case .networkFailure: return "Connection failed"
        }
    }

    var recoverySuggestion: String? {
        switch self {
        case .notFound: return "Check the user ID and try again"
        case .unauthorized: return "Your session expired"
        case .networkFailure: return "Check your internet connection"
        }
    }
}
```

---

## Performance Traps

### Copy-on-Write Gotchas

```swift
// ✅ COW works — array copied only on mutation
var a = [1, 2, 3]
var b = a        // No copy yet
b.append(4)      // Now b gets its own copy

// ❌ COW broken — class inside struct
struct Container {
    var items: NSMutableArray // Reference type!
}
var c1 = Container(items: NSMutableArray())
var c2 = c1      // Both point to same NSMutableArray
c2.items.add(1)  // Mutates c1.items too!
```

### Lazy vs Computed

```swift
// lazy: Computed ONCE, stored
lazy var dateFormatter: DateFormatter = {
    let f = DateFormatter()
    f.dateStyle = .medium
    return f
}()

// computed: Computed EVERY access
var formattedDate: String {
    dateFormatter.string(from: date) // Cheap, uses cached formatter
}
```

**Rule**: Expensive object creation → `lazy`. Simple derived values → computed.

### String Performance

```swift
// ❌ O(n) for each concatenation in loop
var result = ""
for item in items {
    result += item.description // Creates new String each time
}

// ✅ O(n) total
var result = ""
result.reserveCapacity(estimatedLength)
for item in items {
    result.append(item.description)
}

// ✅ Best for joining
let result = items.map(\.description).joined(separator: ", ")
```

---

## Quick Reference

### Access Control Decision

| Level | Use When |
|-------|----------|
| `private` | Implementation detail within declaration |
| `fileprivate` | Shared between types in same file (rare) |
| `internal` | Module-internal, app code default |
| `package` | Same package, different module (Swift 5.9+) |
| `public` | Framework API, readable outside module |
| `open` | Framework API, subclassable outside module |

**Default to most restrictive**. Start `private`, widen only when needed.

### Naming Quick Check

- Types: `PascalCase` nouns — `UserViewModel`, `NetworkError`
- Protocols: `PascalCase` — capability (`-able/-ible`) or description
- Functions: `camelCase` verbs — `fetchUser()`, `configure(with:)`
- Booleans: `is/has/should/can` prefix — `isLoading`, `hasContent`
- Factory methods: `make` prefix — `makeUserViewModel()`
