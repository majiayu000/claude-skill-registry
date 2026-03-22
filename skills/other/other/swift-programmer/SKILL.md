---
name: swift-programmer
description: Swift-specific idioms, tooling, and philosophy. Use when working with Swift code. Emphasizes protocol-oriented programming, value semantics, strict concurrency (Swift 6+), and compile-time safety guarantees.
---

# Swift Programming

<skill_scope skill="swift-programmer">
**Related skills:**
- `software-engineer` — Core design principles and system architecture
- `macos-programmer` — macOS-specific patterns when building Mac apps
- `test-driven-development` — Testing philosophy and practices
- `functional-programmer` — Functional paradigm principles (Swift supports FP)

This skill covers Swift-specific idioms, tooling, and philosophy. It emphasizes protocol-oriented programming, value semantics, strict concurrency (Swift 6+), and compile-time safety guarantees.
</skill_scope>

## Core Philosophy

<philosophy>
**Swift 6 fundamental shift**: From memory safety to **compile-time data-race safety**. Think in **isolation domains, not threads**.

**Version targeting**: Use the latest Swift version available. For internal apps, don't support older versions. For open-source libraries, support N-1 or N-2 versions maximum.

**Prefer**: Protocol composition over inheritance, value semantics over reference semantics, static dispatch over dynamic dispatch.
</philosophy>

## Swift 6 Concurrency: Critical Concepts and Gotchas

<concurrency_fundamentals>
**Mental model shift**: Think in **isolation domains**, not threads. Each domain (task, actor, global actor) executes serially with exclusive access to its state. Every piece of mutable state belongs to exactly one isolation domain at any time.

**Suspension points at `await`**: Task yields thread, executor may schedule different task, upon resumption may execute on **different thread** but always maintains **same isolation domain**. This separation of logical execution (isolation) from physical execution (threads) is critical.

**Structured concurrency**: Task hierarchies with automatic cancellation propagation. Use `TaskGroup` for parallel work with bounded lifetime. Avoid detached tasks except in exceptional circumstances.

**Swift 6.2 Approachable Concurrency**[^approachable-concurrency]: Code is single-threaded by default until you explicitly introduce parallelism with `@concurrent` attribute. Async functions stay on the calling actor unless explicitly offloaded. This eliminates most data-race errors for naturally sequential code.
</concurrency_fundamentals>

### Actor Re-entrancy (Most Common Bug)

<actor_reentrancy>
**The Problem**: Actor state can change at ANY `await` because other tasks can run on the actor while suspended.

```swift
actor BankAccount {
    var balance: Double = 0

    func withdraw(_ amount: Double) async throws {
        guard balance >= amount else { throw InsufficientFunds() }
        // ⚠️ DANGER: Another task can run here
        await processWithdrawal(amount)
        balance -= amount  // May violate guard above!
    }

    // ✅ Better: synchronous transaction
    func withdrawSync(_ amount: Double) throws {
        guard balance >= amount else { throw InsufficientFunds() }
        balance -= amount  // Atomic, no re-entrancy
    }
}
```

**Real-world example**:
```swift
actor OrderProcessor {
    var pendingOrders: [Order] = []

    func processNextOrder() async {
        guard !pendingOrders.isEmpty else { return }
        let order = pendingOrders[0]

        // ⚠️ DANGER: pendingOrders could change here
        await performExpensiveProcessing(order)

        // Crash if another task removed the order!
        pendingOrders.removeFirst()
    }

    // ✅ Fix: Check state after suspension
    func processNextOrderSafe() async {
        guard !pendingOrders.isEmpty else { return }
        let order = pendingOrders[0]

        await performExpensiveProcessing(order)

        // Re-check after suspension
        if let index = pendingOrders.firstIndex(where: { $0.id == order.id }) {
            pendingOrders.remove(at: index)
        }
    }
}
```

**Pattern**: Keep actor methods synchronous when possible. Compose with async wrappers. For async methods, re-validate state after every `await`.
</actor_reentrancy>

### @MainActor: Critical Misunderstandings

<mainactor_details>
**Guarantee 1**: `@MainActor` ONLY guarantees main thread execution for:
- **Async functions** (always)
- **Sync functions called from `@MainActor` context**

**Guarantee 2**: Sync `@MainActor` functions called from non-isolated contexts CAN run on background threads in Swift 5 mode. **Swift 6 mode catches this at compile time.**

**Example of the danger**:
```swift
@MainActor
class ViewModel {
    var state: Int = 0

    func updateState() {  // Sync method
        state += 1
        updateUI()  // Assumes main thread
    }
}

// Calling from background thread (Swift 5 mode):
Task.detached {
    let vm = await ViewModel()
    // ⚠️ This CAN run on background thread!
    await vm.updateState()  // Race condition possible
}
```

**Swift 6.2 Isolated Conformances**:
```swift
protocol Exportable {
    func export()
}

// This conformance is tied to @MainActor
extension ViewModel: @MainActor Exportable {
    func export() {
        // Can safely use main-actor state
        print(state)
    }
}

// Compiler prevents non-main-actor usage
nonisolated func process(_ item: any Exportable) {
    item.export()  // ❌ Error: Cannot use @MainActor conformance
}

@MainActor func process(_ item: any Exportable) {
    item.export()  // ✅ OK: We're on main actor
}
```

**Opt-out with `nonisolated`**:
```swift
@MainActor class ViewModel {
    var title: String = ""

    nonisolated func heavyComputation() async -> Data {
        // Runs on global concurrent pool
        return await performExpensiveWork()
    }

    // ❌ Cannot access main-actor state from nonisolated
    nonisolated func broken() {
        print(title)  // Error: main-actor property access
    }
}
```

**Swift 6.2 Default Main Actor Mode**: Enable `-default-isolation MainActor` build flag to infer `@MainActor` on all types by default. Opt out specific functions with `@concurrent` or `nonisolated`.
</mainactor_details>

### Decision Framework: Actors vs @MainActor vs Classes

<isolation_decision>
| Use Case | Type | Why |
|----------|------|-----|
| UI updates, SwiftUI state | `@MainActor class` | Must run on main thread |
| SwiftUI observable objects | `@MainActor class` with `@Observable` | Required for SwiftUI reactivity |
| Shared mutable state (non-UI) | `actor` | Custom serialization domain |
| Parallel workers, background tasks | `actor` | Serialize access to worker state |
| No mutable shared state | `class` or `struct` | No isolation needed |
| Explicitly parallel work | `@concurrent func` | Offload to background pool |
| Global singletons (UI) | `@MainActor class` with `static let` | Ensure singleton thread-safe |
| Global singletons (non-UI) | `actor` with `static let` | Serialize singleton access |
| ❌ SwiftUI data models | **Never `actor`** | Forces UI updates off main thread → crashes |
| ❌ SwiftUI view state | **Never plain `class`** | Use `@MainActor class` + `@Observable` |

**Anti-pattern**: Using custom actors for SwiftUI observable objects causes race conditions between UI thread and actor's executor. Always use `@MainActor` for UI-related state.
</isolation_decision>

### Sendable Protocol: Deep Dive

<sendable_deep>
**Sendable types** (safe to share across isolation domains):
1. **Value types** where all stored properties are Sendable
2. **Final classes** with only immutable (`let`) Sendable properties
3. **Actors** (implicitly Sendable—state is isolated)
4. **Functions** marked `@Sendable`
5. **@Sendable closures** (cannot capture non-Sendable or mutable values)

**Compiler inference**: Non-public types get Sendable inferred if they meet requirements. Public types require explicit conformance.

**`@unchecked Sendable`** for manually synchronized types:
```swift
import Synchronization

final class ThreadSafeCache: @unchecked Sendable {
    private let cache = Mutex<[String: Data]>([:])

    func get(_ key: String) -> Data? {
        cache.withLock { $0[key] }
    }

    func set(_ key: String, _ value: Data) {
        cache.withLock { $0[key] = value }
    }
}
```

**Common Sendable violations**:
```swift
// ❌ Non-final class can't be Sendable (inheritance issues)
class Config: Sendable {  // Error
    let value: String = ""
}

// ✅ Make it final
final class Config: Sendable {
    let value: String = ""
}

// ❌ Mutable property on Sendable
final class Counter: Sendable {  // Error
    var count: Int = 0
}

// ✅ Use actor instead
actor Counter {
    var count: Int = 0
}

// ❌ Non-Sendable property
final class ViewModel: Sendable {  // Error
    let cache: NSCache<NSString, NSData>  // NSCache not Sendable
}

// ✅ Use @unchecked if you know it's safe
final class ViewModel: @unchecked Sendable {
    let cache: NSCache<NSString, NSData>
    // Document why this is safe
}
```

**@Sendable closures**:
```swift
func processAsync(_ handler: @Sendable @escaping () -> Void) {
    Task {
        handler()
    }
}

// ❌ Capturing mutable variable
var count = 0
processAsync {
    count += 1  // Error: capture of 'count' in @Sendable closure
}

// ✅ Capture immutable copy
var count = 0
count += 1
processAsync { [count] in
    print(count)  // OK: captured by value
}

// ❌ Capturing non-Sendable type
class NotSendable { }
let obj = NotSendable()
processAsync {
    obj.doSomething()  // Error: capture non-Sendable in @Sendable
}

// ✅ Make type Sendable or use nonisolated(unsafe)
nonisolated(unsafe) let obj = NotSendable()
processAsync {
    obj.doSomething()  // OK but unsafe - you ensure safety
}
```
</sendable_deep>

### Region-Based Isolation & Transfer Semantics

<region_isolation>
**SE-0414 Region-based Isolation**[^se-0414]: Allows safe transfer of non-Sendable values when ownership is provably transferred.

**SE-0430 `sending` Keyword**[^se-0430]: Explicitly marks parameters/returns as transferring ownership across isolation boundaries.

```swift
class NonSendable {
    var data: String = ""
}

actor DataProcessor {
    // `consuming` means ownership is transferred IN
    func process(_ item: consuming NonSendable) {
        // Safe: item transferred into actor's region
        item.data = "processed"
    }

    // `sending` means ownership is transferred OUT
    func create() -> sending NonSendable {
        let item = NonSendable()
        item.data = "created"
        return item  // Transferred to caller
    }
}

func use() async {
    let item = NonSendable()
    await processor.process(item)
    // item no longer accessible - ownership transferred
    // print(item.data)  // Error: use after transfer

    let newItem = await processor.create()
    // newItem is now owned by this isolation domain
    print(newItem.data)  // OK
}
```

**Use when**: Passing large non-Sendable objects between actors without copying, implementing ownership transfer semantics, avoiding Sendable conformance for complex types.

**See local docs**: `/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/share/doc/swift/diagnostics/sending-risks-data-race.md`
</region_isolation>

### @concurrent Attribute (Swift 6.2)

<concurrent_attribute>
**Purpose**[^se-0461]: Explicitly offload async work to background thread pool, freeing up the calling actor.

**Before `@concurrent`** (Swift 6.0-6.1):
```swift
@MainActor
class ViewModel {
    func loadData() async {
        // This runs on main actor, blocking UI
        let data = await performExpensiveWork()
        self.data = data
    }
}
```

**With `@concurrent`** (Swift 6.2):
```swift
class ImageProcessor {
    // Always runs on concurrent thread pool
    @concurrent
    static func processImage(_ data: Data) async -> Image {
        // Expensive work runs in parallel
        return performExpensiveProcessing(data)
    }
}

@MainActor
class ViewModel {
    func loadData() async {
        // Work offloaded to background
        let processed = await ImageProcessor.processImage(rawData)
        // Back on main actor for this line
        self.data = processed
    }
}
```

**When to use**:
- CPU-intensive work that shouldn't block actors
- Image/video processing
- Heavy computations
- Large data parsing

**When NOT to use**:
- I/O operations (already async, won't block actor)
- Simple calculations
- Code that must maintain actor isolation

**See local docs**: `/Applications/Xcode.app/Contents/PlugIns/IDEIntelligenceChat.framework/Versions/A/Resources/AdditionalDocumentation/Swift-Concurrency-Updates.md`
</concurrent_attribute>

### Swift 6 Migration: Common Errors and Fixes

<migration_errors>
**Error 1**: "Stored property 'X' of 'Sendable'-conforming class is mutable"
```swift
// ❌ Problem
final class Config: Sendable {
    var timeout: TimeInterval = 30
}

// ✅ Fix 1: Make immutable
final class Config: Sendable {
    let timeout: TimeInterval
}

// ✅ Fix 2: Use actor
actor Config {
    var timeout: TimeInterval = 30
}
```

**Error 2**: "Capture of 'X' with non-Sendable type in @Sendable closure"
```swift
class ViewModel {
    func process() {
        Task {
            self.update()  // ❌ Error: non-Sendable capture
        }
    }
}

// ✅ Fix 1: Make type Sendable
@MainActor
final class ViewModel {
    func process() {
        Task { @MainActor in
            self.update()  // OK: isolated to main actor
        }
    }
}

// ✅ Fix 2: Use weak capture
class ViewModel {
    func process() {
        Task { [weak self] in
            await self?.update()
        }
    }
}
```

**Error 3**: "Call to main actor-isolated instance method 'X' in synchronous nonisolated context"
```swift
@MainActor
class ViewModel {
    func update() { }
}

func caller(vm: ViewModel) {
    vm.update()  // ❌ Error: sync call to main-actor method
}

// ✅ Fix 1: Make caller async
func caller(vm: ViewModel) async {
    await vm.update()
}

// ✅ Fix 2: Isolate caller to main actor
@MainActor
func caller(vm: ViewModel) {
    vm.update()  // OK: both on main actor
}
```

**Error 4**: "Static property 'shared' is not concurrency-safe"
```swift
class Singleton {
    static let shared = Singleton()  // ❌ Error
}

// ✅ Fix 1: Isolate to main actor
@MainActor
class Singleton {
    static let shared = Singleton()
}

// ✅ Fix 2: Use actor
actor Singleton {
    static let shared = Singleton()
}

// ✅ Fix 3: Make Sendable
final class Singleton: Sendable {
    static let shared = Singleton()
    // Must have no mutable state
}
```

**Use `@preconcurrency import`** for unmigrated dependencies:
```swift
@preconcurrency import ThirdPartySDK

// Suppresses Sendable warnings from ThirdPartySDK
```

**See local docs**: All files in `/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/share/doc/swift/diagnostics/`
</migration_errors>

## Protocol-Oriented Programming

<protocol_oriented>
**Core principle**: "Don't start with a class, start with a protocol."[^abrahams-pop]

**When to use protocols**:
- Multiple types share behavior WITHOUT shared state
- Value types need to participate
- Multiple conformance needed (Swift = single inheritance for classes)
- Retroactive conformance to types you don't own

**When to use classes**:
- Need stored property inheritance
- Need to call `super` implementations
- Working with UIKit/AppKit (forced)
- Identity matters more than equality

**Protocol extensions = mixins**: Default implementations enable code reuse without inheritance.

**Anti-pattern from OOP**: Treating protocols as "interfaces" with no default implementations. This recreates OOP hierarchy problems.

**Dispatch gotcha**: Extension methods without protocol requirement = static dispatch (compile-time type). With requirement = dynamic dispatch.
</protocol_oriented>

## Value vs Reference Types

<value_vs_reference>
**Apple's guidance**: "Prefer structs over classes unless you need reference semantics."[^value-semantics]

**Decision tree**:
```
Need identity semantics (object lifetime matters)? → class
Need shared mutable state? → class (careful!)
Need stored property inheritance? → class
Everything else → struct
```

**Performance myth**: "Classes are faster because pointers."
**Reality**: Value types often faster—stack allocation, no ref-counting, passed in registers when small.

**Best practice**: Avoid value types with inner references—violates value semantics and adds ref-counting overhead.
</value_vs_reference>

## Error Handling

<error_handling>
| Mechanism | Use When |
|-----------|----------|
| `throws` | Recoverable errors with context |
| `Result<T, E>` | Async callbacks, deferred handling |
| `Optional` | Simple absence, no error details needed |

**Swift 6 typed throws**:
```swift
enum FileError: Error { case notFound, permissionDenied }

func loadFile(_ path: String) throws(FileError) -> Data {
    guard fileExists(path) else { throw .notFound }
    return try Data(contentsOf: URL(fileURLWithPath: path))
}
// Caller: error is FileError, not 'any Error'
```
</error_handling>

## Tooling (Mandatory)

<tooling>
**SwiftLint + SwiftFormat**: Mandatory in CI/CD. Fail builds on violations.
- SwiftLint: Code smells, complexity, naming, architecture
- SwiftFormat: ALL formatting (indentation, spacing, wrapping)

**Swift Package Manager**: Three-layer architecture (Core ← Domain ← Features). Unidirectional dependencies.

**Testing**: Prefer Swift Testing for new unit tests (native async, `#expect` macro, parameterized tests). XCTest required for UI/performance tests.

**Documentation**: DocC mandatory for all public APIs. Use `​``Symbol``​` links. Document complexity when not O(1).

**Configuration files**: See local .swiftlint.yml and .swiftformat in projects for standard configs.
</tooling>

## Common Mistakes from Other Languages

<common_mistakes>
**From Java/C#**: Using classes for everything → **Use structs by default**

**From Python/JavaScript**: Using `Any` extensively → **Leverage generics and protocols**

**From C/C++**: Using `UnsafePointer` unnecessarily → **Let ARC work, use weak/unowned for cycles**

**From Rust**: Over-applying ownership patterns → **Trust Swift's ARC + copy-on-write**

**From Objective-C**: Using `NSString`, `NSArray`, `NSDictionary` → **Use Swift native types**

**From any OOP**: Creating deep inheritance hierarchies → **Use protocol composition**
</common_mistakes>

## Memory Management Gotchas

<memory_gotchas>
**Retain cycles**: Parent ↔ child, closures capturing self, delegate patterns

**Closure capture lists**:
```swift
{ [weak self] in
    guard let self else { return }
    // Use self
}
```

**Weak vs Unowned**:
- `weak`: Optional, auto-nil when deallocated (safe)
- `unowned`: Non-optional, NOT auto-nil (crashes if accessed after dealloc)

**Rule**: Prefer `weak` unless lifetime relationship is absolutely certain.
</memory_gotchas>

## API Design Core Principles

<api_design>
**Apple's three pillars**[^api-guidelines]:
1. **Clarity at point of use** (most important)
2. **Clarity over brevity**
3. **Document every declaration**

**Naming**:
- No side-effects → noun phrases: `x.distance(to: y)`
- With side-effects → imperative verbs: `x.sort()`
- Mutating/non-mutating pairs: `sort()`/`sorted()`, `append(_:)`/`appending(_:)`
- Factory methods start with "make": `makeIterator()`

**Access control**: Default to `private`, use `internal` for module-wide, `public`/`open` only for framework APIs.

**Source**: https://www.swift.org/documentation/api-design-guidelines/
</api_design>

## Swift 6.2 New Features

<swift_6_2>
**InlineArray**[^se-0453]: Fixed-size arrays with stack allocation, no heap, no ref-counting. Use for performance-critical fixed-size collections.

**Span**[^se-0447]: Safe contiguous memory access without unsafe pointers. Compile-time lifetime checking prevents use-after-free.

**Isolated conformances**: Protocol conformances can be tied to specific actors (e.g., `@MainActor Exportable`).

**@concurrent attribute**: Explicitly offload async work to background thread pool.

**Default main actor mode**: Opt-in `-default-isolation MainActor` for mostly-single-threaded apps.
</swift_6_2>

## Respecting Third-Party Codebases

<third_party>
When contributing to open-source Swift:
- Respect existing style (even if wrong)
- Don't introduce modern features to older-version projects
- Follow CONTRIBUTING.md precisely
- Match formatting exactly
- Keep PRs focused

**You're a guest—respect house rules.**
</third_party>

## Local Documentation Resources

<local_docs>
**Xcode ships with LLM-optimized Swift documentation:**

**Swift Diagnostic Docs** (compiler errors):
- Path: `/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/share/doc/swift/diagnostics/`
- Files: `sendable-closure-captures.md`, `actor-isolated-call.md`, 30+ others
- Use when: Encountering specific Swift 6 concurrency errors

**LLM-Optimized Framework Guides**:
- Path: `/Applications/Xcode.app/Contents/PlugIns/IDEIntelligenceChat.framework/Versions/A/Resources/AdditionalDocumentation/`
- Files: `Swift-Concurrency-Updates.md`, `Swift-InlineArray-Span.md`, framework integration guides
- Use when: Learning Swift 6.2 features, modern patterns

**The Swift Programming Language Book**:
- Online: https://docs.swift.org/swift-book/
- Source (Markdown): https://github.com/swiftlang/swift-book/tree/main/TSPL.docc
- Use when: Need authoritative language reference
</local_docs>

## Authoritative Resources

<resources>
**Official Documentation (readable)**:
- Swift.org: https://www.swift.org/
- Swift Evolution: https://www.swift.org/swift-evolution/
- API Guidelines: https://www.swift.org/documentation/api-design-guidelines/
- Swift Book (Markdown): https://github.com/swiftlang/swift-book/tree/main/TSPL.docc
- DocC: https://www.swift.org/documentation/docc/
- Apple Developer Docs: https://developer.apple.com/documentation/

**Tooling**:
- SwiftLint: https://github.com/realm/SwiftLint
- SwiftFormat: https://github.com/nicklockwood/SwiftFormat
- Swift Testing: https://github.com/apple/swift-testing

**Style Guides**:
- Google: https://google.github.io/swift/
- Kodeco: https://github.com/kodecocodes/swift-style-guide
</resources>

## Sources

<sources>
[^abrahams-pop]: Dave Abrahams. 2015. Protocol-Oriented Programming in Swift (Session 408). WWDC 2015. https://developer.apple.com/videos/play/wwdc2015/408/

[^api-guidelines]: Apple Inc. Swift API Design Guidelines. https://www.swift.org/documentation/api-design-guidelines/

[^value-semantics]: Apple Inc. Choosing Between Structures and Classes. Swift Documentation. https://developer.apple.com/documentation/swift/choosing-between-structures-and-classes

[^approachable-concurrency]: Swift Project. 2025. Approachable Concurrency Vision Document. Swift Evolution. https://github.com/swiftlang/swift-evolution/blob/main/visions/approachable-concurrency.md

[^se-0414]: Michael Gottesman, et al. 2024. SE-0414: Region-based Isolation. Swift Evolution. https://github.com/swiftlang/swift-evolution/blob/main/proposals/0414-region-based-isolation.md

[^se-0430]: Michael Gottesman, et al. 2024. SE-0430: `sending` parameter and result values. Swift Evolution. https://github.com/swiftlang/swift-evolution/blob/main/proposals/0430-transferring-parameters-and-results.md

[^se-0447]: Guillaume Lessard, et al. 2024. SE-0447: Span: Safe Access to Contiguous Storage. Swift Evolution. https://github.com/swiftlang/swift-evolution/blob/main/proposals/0447-span-access-shared-contiguous-storage.md

[^se-0453]: Alejandro Alonso, et al. 2025. SE-0453: Vector (InlineArray). Swift Evolution. https://github.com/swiftlang/swift-evolution/blob/main/proposals/0453-vector.md

[^se-0461]: Holly Borla, et al. 2025. SE-0461: Run nonisolated async functions on the caller's actor by default. Swift Evolution. https://github.com/swiftlang/swift-evolution/blob/main/proposals/0461-async-function-isolation.md

[^tspl]: Apple Inc. and Swift Project Authors. 2014–2025. The Swift Programming Language. https://docs.swift.org/swift-book/
</sources>
