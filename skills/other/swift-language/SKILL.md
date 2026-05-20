---
name: swift-language
description: "Apply modern Swift language patterns and idioms for non-concurrency, non-SwiftUI code. Covers if/switch expressions (Swift 5.9+), typed throws (Swift 6+), result builders, property wrappers, opaque and existential types (some vs any), guard patterns, Never type, Regex builders (Swift 5.7+), Codable best practices (CodingKeys, custom decoding, nested containers), modern collection APIs (count(where:), contains(where:), replacing()), FormatStyle (.formatted() on dates, numbers, measurements), and string interpolation patterns. Use when writing core Swift code involving generics, protocols, enums, closures, or modern language features."
---

# Swift Language Patterns

Core Swift language features and modern syntax patterns targeting Swift 5.9+
through Swift 6. Covers language constructs, type system features, Codable,
string and collection APIs, and formatting. For concurrency (actors, async/await,
Sendable), see the `swift-concurrency` skill. For SwiftUI views and state
management, see `swiftui-patterns`.

## Contents

- [If/Switch Expressions](#ifswitch-expressions)
- [Typed Throws](#typed-throws)
- [Result Builders](#result-builders)
- [Property Wrappers](#property-wrappers)
- [Opaque and Existential Types](#opaque-and-existential-types)
- [Guard Patterns](#guard-patterns)
- [Never Type](#never-type)
- [Regex Builders](#regex-builders)
- [Codable Best Practices](#codable-best-practices)
- [Modern Collection APIs](#modern-collection-apis)
- [FormatStyle](#formatstyle)
- [String Interpolation](#string-interpolation)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## If/Switch Expressions

Swift 5.9+ allows `if` and `switch` as expressions that return values. Use them
to assign, return, or initialize directly.

```swift
// Assign from if expression
let icon = if isComplete { "checkmark.circle.fill" } else { "circle" }

// Assign from switch expression
let label = switch status {
case .draft: "Draft"
case .published: "Published"
case .archived: "Archived"
}

// Works in return position
func color(for priority: Priority) -> Color {
    switch priority {
    case .high: .red
    case .medium: .orange
    case .low: .green
    }
}
```

**Rules:**
- Every branch must produce a value of the same type.
- Multi-statement branches are not allowed -- each branch is a single expression.
- Wrap in parentheses when used as a function argument to avoid ambiguity.

## Typed Throws

Swift 6+ allows specifying the error type a function throws.

```swift
enum ValidationError: Error {
    case tooShort, invalidCharacters, alreadyTaken
}

func validate(username: String) throws(ValidationError) -> String {
    guard username.count >= 3 else { throw .tooShort }
    guard username.allSatisfy(\.isLetterOrDigit) else { throw .invalidCharacters }
    return username.lowercased()
}

// Caller gets typed error -- no cast needed
do {
    let name = try validate(username: input)
} catch {
    // error is ValidationError, not any Error
    switch error {
    case .tooShort: print("Too short")
    case .invalidCharacters: print("Invalid characters")
    case .alreadyTaken: print("Taken")
    }
}
```

**Rules:**
- Use `throws(SomeError)` only when callers benefit from exhaustive error
  handling. For mixed error sources, use untyped `throws`.
- `throws(Never)` marks a function that syntactically throws but never actually
  does -- useful in generic contexts.
- Typed throws propagate: a function calling `throws(A)` and `throws(B)` must
  itself throw a type that covers both (or use untyped `throws`).

## Result Builders

`@resultBuilder` enables DSL-style syntax. SwiftUI's `@ViewBuilder` is the most
common example, but you can create custom builders for any domain.

```swift
@resultBuilder
struct ArrayBuilder<Element> {
    static func buildBlock(_ components: [Element]...) -> [Element] {
        components.flatMap { $0 }
    }
    static func buildExpression(_ expression: Element) -> [Element] { [expression] }
    static func buildOptional(_ component: [Element]?) -> [Element] { component ?? [] }
    static func buildEither(first component: [Element]) -> [Element] { component }
    static func buildEither(second component: [Element]) -> [Element] { component }
    static func buildArray(_ components: [[Element]]) -> [Element] { components.flatMap { $0 } }
}

func makeItems(@ArrayBuilder<String> content: () -> [String]) -> [String] { content() }

let items = makeItems {
    "Always included"
    if showExtra { "Conditional" }
    for name in names { name.uppercased() }
}
```

**Builder methods:** `buildBlock` (combine statements), `buildExpression` (single value), `buildOptional` (`if` without `else`), `buildEither` (`if/else`), `buildArray` (`for..in`), `buildFinalResult` (optional post-processing).

## Property Wrappers

Custom `@propertyWrapper` types encapsulate storage and access patterns.

```swift
@propertyWrapper
struct Clamped<Value: Comparable> {
    private var value: Value
    let range: ClosedRange<Value>

    var wrappedValue: Value {
        get { value }
        set { value = min(max(newValue, range.lowerBound), range.upperBound) }
    }

    var projectedValue: ClosedRange<Value> { range }

    init(wrappedValue: Value, _ range: ClosedRange<Value>) {
        self.range = range
        self.value = min(max(wrappedValue, range.lowerBound), range.upperBound)
    }
}

// Usage
struct Volume {
    @Clamped(0...100) var level: Int = 50
}

var v = Volume()
v.level = 150   // clamped to 100
print(v.$level) // projected value: 0...100
```

**Design rules:**
- `wrappedValue` is the primary getter/setter.
- `projectedValue` (accessed via `$property`) provides metadata or bindings.
- Property wrappers can be composed: `@A @B var x` applies outer wrapper first.
- Do not use property wrappers when a simple computed property suffices.

## Opaque and Existential Types

### `some Protocol` (Opaque Type)

The caller does not know the concrete type, but the compiler does. The
underlying type is fixed for a given scope.

```swift
func makeCollection() -> some Collection<Int> {
    [1, 2, 3]  // Always returns Array<Int> -- compiler knows the concrete type
}
```

Use `some` for:
- Return types when you want to hide implementation but preserve type identity.
- Parameter types (Swift 5.9+): `func process(_ items: some Collection<Int>)` --
  equivalent to a generic `<C: Collection<Int>>`.

### `any Protocol` (Existential Type)

An existential box that can hold any conforming type at runtime. Has overhead
from dynamic dispatch and heap allocation.

```swift
func process(items: [any StringProtocol]) {
    for item in items {
        print(item.uppercased())
    }
}
```

### When to choose

| Use `some` | Use `any` |
|---|---|
| Return type hiding concrete type | Heterogeneous collections |
| Function parameters (replaces simple generics) | Dynamic type erasure needed |
| Better performance (static dispatch) | Protocol has `Self` or associated type requirements you need to erase |

**Rule of thumb:** Default to `some`. Use `any` only when you need a
heterogeneous collection or runtime type flexibility.

## Guard Patterns

`guard` enforces preconditions and enables early exit. It keeps the happy path
left-aligned and reduces nesting.

```swift
func processOrder(_ order: Order?) throws -> Receipt {
    // Unwrap optionals
    guard let order else { throw OrderError.missing }

    // Validate conditions
    guard order.items.isEmpty == false else { throw OrderError.empty }
    guard order.total > 0 else { throw OrderError.invalidTotal }

    // Boolean checks
    guard order.isPaid else { throw OrderError.unpaid }

    // Pattern matching
    guard case .confirmed(let date) = order.status else {
        throw OrderError.notConfirmed
    }

    return Receipt(order: order, confirmedAt: date)
}
```

**Best practices:**
- Use `guard` for preconditions, `if` for branching logic.
- Combine related guards: `guard let a, let b else { return }`.
- The `else` block must exit scope: `return`, `throw`, `continue`, `break`, or
  `fatalError()`.
- Use shorthand unwrap: `guard let value else { ... }` (Swift 5.7+).

## Never Type

`Never` indicates a function that never returns. It conforms to all protocols
since Swift 5.5+ (bottom type).

```swift
// Function that terminates the program
func crashWithDiagnostics(_ message: String) -> Never {
    let diagnostics = gatherDiagnostics()
    logger.critical("\(message): \(diagnostics)")
    fatalError(message)
}

// Useful in generic contexts
enum Result<Success, Failure: Error> {
    case success(Success)
    case failure(Failure)
}
// Result<String, Never> -- a result that can never fail
// Result<Never, Error>  -- a result that can never succeed

// Exhaustive switch: no default needed since Never has no cases
func handle(_ result: Result<String, Never>) {
    switch result {
    case .success(let value): print(value)
    // No .failure case needed -- compiler knows it's impossible
    }
}
```

## Regex Builders

Swift 5.7+ Regex builder DSL provides compile-time checked, readable patterns.

```swift
import RegexBuilder

// Parse "2024-03-15" into components
let dateRegex = Regex {
    Capture { /\d{4}/ }; "-"; Capture { /\d{2}/ }; "-"; Capture { /\d{2}/ }
}

if let match = "2024-03-15".firstMatch(of: dateRegex) {
    let (_, year, month, day) = match.output
}

// TryCapture with transform
let priceRegex = Regex {
    "$"
    TryCapture { OneOrMore(.digit); "."; Repeat(.digit, count: 2) }
        transform: { Decimal(string: String($0)) }
}
```

**When to use builder vs. literal:**
- Builder: complex patterns, reusable components, strong typing on captures.
- Literal (`/pattern/`): simple patterns, familiarity with regex syntax.
- Both can be mixed: embed `/.../` literals inside builder blocks.

## Codable Best Practices

### Custom CodingKeys

Rename keys without writing a custom decoder:

```swift
struct User: Codable {
    let id: Int
    let displayName: String
    let avatarURL: URL

    enum CodingKeys: String, CodingKey {
        case id
        case displayName = "display_name"
        case avatarURL = "avatar_url"
    }
}
```

### Custom Decoding

Handle mismatched types, defaults, and transformations:

```swift
struct Item: Decodable {
    let name: String
    let quantity: Int
    let isActive: Bool

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        name = try container.decode(String.self, forKey: .name)
        quantity = try container.decodeIfPresent(Int.self, forKey: .quantity) ?? 0
        if let boolValue = try? container.decode(Bool.self, forKey: .isActive) {
            isActive = boolValue
        } else {
            isActive = (try container.decode(String.self, forKey: .isActive)).lowercased() == "true"
        }
    }
    enum CodingKeys: String, CodingKey { case name, quantity; case isActive = "is_active" }
}
```

### Nested Containers

Flatten nested JSON into a flat Swift struct:

```swift
// JSON: { "id": 1, "metadata": { "created_at": "...", "tags": [...] } }
struct Record: Decodable {
    let id: Int
    let createdAt: String
    let tags: [String]

    enum CodingKeys: String, CodingKey {
        case id, metadata
    }

    enum MetadataKeys: String, CodingKey {
        case createdAt = "created_at"
        case tags
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        id = try container.decode(Int.self, forKey: .id)
        let metadata = try container.nestedContainer(
            keyedBy: MetadataKeys.self, forKey: .metadata)
        createdAt = try metadata.decode(String.self, forKey: .createdAt)
        tags = try metadata.decode([String].self, forKey: .tags)
    }
}
```

See `references/swift-patterns-extended.md` for additional Codable patterns
(enums with associated values, date strategies, unkeyed containers).

## Modern Collection APIs

Prefer these modern APIs over manual loops:

```swift
let numbers = [1, 2, 3, 4, 5, 6, 7, 8]

// count(where:) -- Swift 5.0+, use instead of .filter { }.count
let evenCount = numbers.count(where: { $0.isMultiple(of: 2) })

// contains(where:) -- short-circuits on first match
let hasNegative = numbers.contains(where: { $0 < 0 })

// first(where:) / last(where:)
let firstEven = numbers.first(where: { $0.isMultiple(of: 2) })

// String replacing() -- Swift 5.7+, returns new string
let cleaned = rawText.replacing(/\s+/, with: " ")
let snakeCase = name.replacing("_", with: " ")

// compactMap -- unwrap optionals from a transform
let ids = strings.compactMap { Int($0) }

// flatMap -- flatten nested collections
let allTags = articles.flatMap(\.tags)

// Dictionary(grouping:by:)
let byCategory = Dictionary(grouping: items, by: \.category)

// reduce(into:) -- efficient accumulation
let freq = words.reduce(into: [:]) { counts, word in
    counts[word, default: 0] += 1
}
```

## FormatStyle

Use `.formatted()` instead of `DateFormatter`/`NumberFormatter`. It is
type-safe, localized, and concise.

```swift
// Dates
let now = Date.now
now.formatted()                                       // "3/15/2024, 2:30 PM"
now.formatted(date: .abbreviated, time: .shortened)   // "Mar 15, 2024, 2:30 PM"
now.formatted(.dateTime.year().month().day())          // "Mar 15, 2024"
now.formatted(.relative(presentation: .named))        // "yesterday"

// Numbers
let price = 42.5
price.formatted(.currency(code: "USD"))               // "$42.50"
price.formatted(.percent)                             // "4,250%"
(1_000_000).formatted(.number.notation(.compactName)) // "1M"

// Measurements
let distance = Measurement(value: 5, unit: UnitLength.kilometers)
distance.formatted(.measurement(width: .abbreviated)) // "5 km"

// Duration (Swift 5.7+)
let duration = Duration.seconds(3661)
duration.formatted(.time(pattern: .hourMinuteSecond)) // "1:01:01"

// Byte counts
Int64(1_500_000).formatted(.byteCount(style: .file)) // "1.5 MB"

// Lists
["Alice", "Bob", "Carol"].formatted(.list(type: .and)) // "Alice, Bob, and Carol"
```

**Parsing:** `FormatStyle` also supports parsing:
```swift
let value = try Decimal("$42.50", format: .currency(code: "USD"))
let date = try Date("Mar 15, 2024", strategy: .dateTime.month().day().year())
```

## String Interpolation

Extend `DefaultStringInterpolation` for domain-specific formatting. Use `"""` for multi-line strings (indentation is relative to the closing `"""`). See `references/swift-patterns-extended.md` for custom interpolation examples.

## Common Mistakes

1. **Using `any` when `some` works.** Default to `some` for return types and
   parameters. `any` has runtime overhead and loses type information.
2. **Manual loops instead of collection APIs.** Use `count(where:)`,
   `contains(where:)`, `compactMap`, `flatMap` instead of manual iteration.
3. **`DateFormatter` instead of FormatStyle.** `.formatted()` is simpler,
   type-safe, and handles localization automatically.
4. **Force-unwrapping Codable decodes.** Use `decodeIfPresent` with defaults
   for optional or missing keys.
5. **Nested if-let chains.** Use `guard let` for preconditions to keep the
   happy path at the top level.
6. **String regex for simple operations.** Use `.replacing()` and
   `.contains()` before reaching for Regex.
7. **Ignoring typed throws.** When a function has a single, clear error type,
   typed throws give callers exhaustive switch without casting.
8. **Overusing property wrappers.** A computed property is simpler when there
   is no reuse or projected value needed.
9. **Building collections with `var` + `append` in a loop.** Prefer `map`,
   `filter`, `compactMap`, or `reduce(into:)`.
10. **Not using if/switch expressions.** When assigning from a condition, use
    an expression instead of declaring `var` and mutating it.

## Review Checklist

- [ ] `some` used over `any` where possible
- [ ] `guard` used for preconditions, not nested `if let`
- [ ] Collection APIs used instead of manual loops
- [ ] `.formatted()` used instead of `DateFormatter`/`NumberFormatter`
- [ ] Codable types use `CodingKeys` for API key mapping
- [ ] `decodeIfPresent` with defaults for optional JSON fields
- [ ] if/switch expressions used for simple conditional assignment
- [ ] Property wrappers have clear reuse justification
- [ ] Regex builder used for complex patterns (literal OK for simple ones)
- [ ] String interpolation is clean -- no unnecessary `String(describing:)`
- [ ] Typed throws used when callers benefit from exhaustive error handling
- [ ] `Never` used appropriately in generic contexts

## References

- Extended patterns and Codable examples: `references/swift-patterns-extended.md`
