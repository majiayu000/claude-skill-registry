---
name: Swift Protocol-Oriented Programming
description: Use when protocol-oriented programming in Swift including protocol extensions, default implementations, protocol composition, associated types, and designing flexible, reusable abstractions that favor composition over inheritance.
allowed-tools: []
---

# Swift Protocol-Oriented Programming

## Introduction

Protocol-oriented programming (POP) is Swift's paradigm for building flexible,
composable abstractions without the rigid hierarchies of class inheritance.
Protocols define interfaces that types can adopt, while protocol extensions
provide default implementations and capabilities to multiple types
simultaneously.

This approach offers the flexibility of composition, the performance of static
dispatch, and the ability to extend value types like structs and enums. POP is
foundational to Swift's standard library and enables powerful patterns for code
reuse, testing, and API design.

This skill covers protocol design, extensions, associated types, composition,
and practical patterns for building protocol-oriented architectures.

## Protocol Basics and Design

Protocols define contracts that types must fulfill, specifying required
properties, methods, and initializers without providing implementations.

```swift
// Basic protocol definition
protocol Drawable {
    var lineWidth: Double { get set }
    var color: String { get }

    func draw()
    mutating func resize(by factor: Double)
}

// Protocol adoption in struct
struct Circle: Drawable {
    var lineWidth: Double
    let color: String
    var radius: Double

    func draw() {
        print("Drawing circle with radius \(radius)")
    }

    mutating func resize(by factor: Double) {
        radius *= factor
    }
}

// Protocol adoption in class
class Rectangle: Drawable {
    var lineWidth: Double
    let color: String
    var width: Double
    var height: Double

    init(lineWidth: Double, color: String, width: Double, height: Double) {
        self.lineWidth = lineWidth
        self.color = color
        self.width = width
        self.height = height
    }

    func draw() {
        print("Drawing rectangle \(width)x\(height)")
    }

    func resize(by factor: Double) {
        width *= factor
        height *= factor
    }
}

// Using protocols as types
func render(shape: Drawable) {
    print("Rendering with \(shape.color) color")
    shape.draw()
}

let circle = Circle(lineWidth: 2.0, color: "red", radius: 5.0)
render(shape: circle)

// Protocol requirements for initializers
protocol Identifiable {
    var id: String { get }
    init(id: String)
}

struct User: Identifiable {
    let id: String
    let name: String

    init(id: String) {
        self.id = id
        self.name = "Unknown"
    }
}
```

Well-designed protocols are focused and cohesive, defining a single
responsibility rather than mixing unrelated requirements.

## Protocol Extensions

Protocol extensions provide default implementations to all adopting types,
enabling code reuse without inheritance and retroactive modeling of existing
types.

```swift
// Protocol with extension providing defaults
protocol Greetable {
    var name: String { get }
    func greet() -> String
    func formalGreet() -> String
}

extension Greetable {
    func greet() -> String {
        return "Hello, \(name)!"
    }

    func formalGreet() -> String {
        return "Good day, \(name)."
    }
}

// Type adopts protocol, gets defaults
struct Person: Greetable {
    let name: String
    // greet() and formalGreet() provided by extension
}

// Type can override defaults
struct Robot: Greetable {
    let name: String

    func greet() -> String {
        return "GREETINGS, \(name.uppercased())"
    }
}

// Conditional extensions
extension Collection where Element: Equatable {
    func allEqual() -> Bool {
        guard let first = first else { return true }
        return allSatisfy { $0 == first }
    }
}

let numbers = [5, 5, 5, 5]
print(numbers.allEqual()) // true

// Extending protocols with constraints
extension Drawable where Self: AnyObject {
    func drawWithRetain() {
        // Only available for class types
        draw()
    }
}

// Adding computed properties
extension Drawable {
    var description: String {
        return "Shape with \(color) color and \(lineWidth)pt line"
    }
}

// Protocol extension providing utilities
protocol JSONRepresentable {
    func toJSON() -> [String: Any]
}

extension JSONRepresentable {
    func toJSONString() -> String {
        let dict = toJSON()
        guard let data = try? JSONSerialization.data(
            withJSONObject: dict
        ),
              let string = String(data: data, encoding: .utf8) else {
            return "{}"
        }
        return string
    }
}
```

Protocol extensions enable retroactive modeling—adding protocol conformance to
types you don't own, including standard library types.

## Associated Types

Associated types create generic protocols, allowing conforming types to specify
concrete types that satisfy protocol requirements.

```swift
// Protocol with associated type
protocol Container {
    associatedtype Item

    var count: Int { get }
    mutating func append(_ item: Item)
    subscript(i: Int) -> Item { get }
}

// Concrete type specifies Item
struct IntStack: Container {
    typealias Item = Int // explicit, but can be inferred

    private var items: [Int] = []

    var count: Int {
        return items.count
    }

    mutating func append(_ item: Int) {
        items.append(item)
    }

    subscript(i: Int) -> Int {
        return items[i]
    }
}

// Generic type with associated type
struct Stack<Element>: Container {
    private var items: [Element] = []

    var count: Int {
        return items.count
    }

    mutating func append(_ item: Element) {
        items.append(item)
    }

    subscript(i: Int) -> Element {
        return items[i]
    }
}

// Using associated types in generic functions
func printAll<C: Container>(_ container: C) where C.Item == String {
    for i in 0..<container.count {
        print(container[i])
    }
}

// Associated type with constraints
protocol Graph {
    associatedtype Node: Hashable
    associatedtype Edge

    func neighbors(of node: Node) -> [Node]
    func edges(from node: Node) -> [Edge]
}

// Multiple associated types
protocol Transformable {
    associatedtype Input
    associatedtype Output

    func transform(_ input: Input) -> Output
}

struct StringToIntTransformer: Transformable {
    func transform(_ input: String) -> Int {
        return Int(input) ?? 0
    }
}

// Associated type with default
protocol Summable {
    associatedtype Result = Self

    func sum(with other: Self) -> Result
}

extension Int: Summable {
    func sum(with other: Int) -> Int {
        return self + other
    }
}
```

Associated types enable protocol-based generic programming, providing
flexibility while maintaining type safety and performance.

## Protocol Composition

Protocol composition combines multiple protocols into a single requirement,
enabling precise type constraints without creating protocol hierarchies.

```swift
// Individual protocols
protocol Named {
    var name: String { get }
}

protocol Aged {
    var age: Int { get }
}

protocol Addressable {
    var address: String { get }
}

// Function requiring multiple protocols
func displayInfo(for entity: Named & Aged) {
    print("\(entity.name) is \(entity.age) years old")
}

struct Employee: Named, Aged, Addressable {
    let name: String
    let age: Int
    let address: String
}

let employee = Employee(name: "Alice", age: 30, address: "123 Main St")
displayInfo(for: employee)

// Composition with classes
protocol Purchasable {
    var price: Double { get }
}

func processPurchase(item: AnyObject & Purchasable) {
    // Must be a class (AnyObject) and conform to Purchasable
    print("Processing purchase of $\(item.price)")
}

// Protocol composition in properties
class Store {
    var items: [Named & Purchasable] = []

    func addItem(_ item: Named & Purchasable) {
        items.append(item)
    }
}

// Composition with associated types
protocol Comparable2: Equatable {
    func isLessThan(_ other: Self) -> Bool
}

func sorted<T: Comparable2>(items: [T]) -> [T] {
    return items.sorted { $0.isLessThan($1) }
}

// Type alias for common compositions
typealias Person = Named & Aged & Addressable

func register(person: Person) {
    print("Registering \(person.name)")
}

// Composition in generic constraints
func merge<T>(_ a: T, _ b: T) -> [T] where T: Named & Aged {
    return [a, b].sorted { $0.age < $1.age }
}
```

Protocol composition creates precise constraints without the fragility of deep
inheritance hierarchies or the overhead of creating new protocols.

## Protocol Witnesses and Type Erasure

Type erasure hides concrete types behind protocol interfaces, enabling
heterogeneous collections and abstracting implementation details.

```swift
// Problem: protocols with associated types can't be used as types
protocol Producer {
    associatedtype Item
    func produce() -> Item
}

// Type-erased wrapper
struct AnyProducer<T>: Producer {
    typealias Item = T

    private let _produce: () -> T

    init<P: Producer>(_ producer: P) where P.Item == T {
        _produce = producer.produce
    }

    func produce() -> T {
        return _produce()
    }
}

// Concrete producers
struct IntProducer: Producer {
    func produce() -> Int {
        return 42
    }
}

struct StringProducer: Producer {
    func produce() -> String {
        return "Hello"
    }
}

// Heterogeneous array using type erasure
let producers: [Any] = [
    AnyProducer(IntProducer()),
    AnyProducer(StringProducer())
]

// Standard library type erasure: AnySequence
func makeSequence() -> AnySequence<Int> {
    let array = [1, 2, 3, 4, 5]
    return AnySequence(array)
}

// Combining type erasure with protocol composition
protocol DataSource {
    associatedtype Data
    func fetch() -> Data
}

struct AnyDataSource<T>: DataSource {
    typealias Data = T

    private let _fetch: () -> T

    init<DS: DataSource>(_ source: DS) where DS.Data == T {
        _fetch = source.fetch
    }

    func fetch() -> T {
        return _fetch()
    }
}

// Using existential types (Swift 5.7+)
protocol Animal {
    func makeSound() -> String
}

struct Dog: Animal {
    func makeSound() -> String { "Woof" }
}

struct Cat: Animal {
    func makeSound() -> String { "Meow" }
}

let animals: [any Animal] = [Dog(), Cat()]
```

Type erasure trades some type information for flexibility, enabling protocol
abstractions to work as concrete types in collections and properties.

## Protocol-Oriented Architecture Patterns

Protocol-oriented design supports testability, modularity, and clean
architecture through dependency injection and protocol-based abstractions.

```swift
// Dependency injection with protocols
protocol NetworkService {
    func fetch(url: URL) async throws -> Data
}

protocol DataStore {
    func save(_ data: Data, key: String) throws
    func load(key: String) throws -> Data
}

// Concrete implementations
struct URLSessionNetworkService: NetworkService {
    func fetch(url: URL) async throws -> Data {
        let (data, _) = try await URLSession.shared.data(from: url)
        return data
    }
}

struct UserDefaultsDataStore: DataStore {
    func save(_ data: Data, key: String) throws {
        UserDefaults.standard.set(data, forKey: key)
    }

    func load(key: String) throws -> Data {
        guard let data = UserDefaults.standard.data(forKey: key) else {
            throw DataStoreError.notFound
        }
        return data
    }
}

enum DataStoreError: Error {
    case notFound
}

// Business logic depends on protocols
class Repository {
    private let network: NetworkService
    private let store: DataStore

    init(network: NetworkService, store: DataStore) {
        self.network = network
        self.store = store
    }

    func fetchAndCache(url: URL, key: String) async throws {
        let data = try await network.fetch(url: url)
        try store.save(data, key: key)
    }
}

// Testing with mock implementations
struct MockNetworkService: NetworkService {
    let mockData: Data

    func fetch(url: URL) async throws -> Data {
        return mockData
    }
}

struct MockDataStore: DataStore {
    var storage: [String: Data] = [:]

    mutating func save(_ data: Data, key: String) throws {
        storage[key] = data
    }

    func load(key: String) throws -> Data {
        guard let data = storage[key] else {
            throw DataStoreError.notFound
        }
        return data
    }
}

// Strategy pattern with protocols
protocol SortStrategy {
    func sort<T: Comparable>(_ array: [T]) -> [T]
}

struct QuickSort: SortStrategy {
    func sort<T: Comparable>(_ array: [T]) -> [T] {
        guard array.count > 1 else { return array }
        // Quick sort implementation
        return array.sorted()
    }
}

struct BubbleSort: SortStrategy {
    func sort<T: Comparable>(_ array: [T]) -> [T] {
        // Bubble sort implementation
        return array.sorted()
    }
}

class Sorter {
    var strategy: SortStrategy

    init(strategy: SortStrategy) {
        self.strategy = strategy
    }

    func sort<T: Comparable>(_ array: [T]) -> [T] {
        return strategy.sort(array)
    }
}
```

Protocol-oriented architecture improves testability by allowing mock
implementations and supports flexibility by enabling runtime strategy changes.

## Best Practices

1. **Design small, focused protocols** with single responsibilities rather than
   large protocols mixing unrelated requirements

2. **Provide default implementations** in extensions to reduce boilerplate and
   allow selective customization by conforming types

3. **Prefer protocol composition over inheritance** to create precise
   constraints without fragile hierarchies

4. **Use associated types for generic protocols** when conforming types need to
   specify concrete types for requirements

5. **Apply protocol extensions conditionally** with where clauses to provide
   specialized behavior for constrained types

6. **Leverage value types with protocols** to gain composition benefits without
   reference semantics or inheritance limitations

7. **Create type-erased wrappers** for protocols with associated types when
   heterogeneous collections or abstraction is needed

8. **Design for testability** by depending on protocol abstractions rather than
   concrete types in business logic

9. **Use protocol witnesses for dependency injection** to decouple components
   and enable flexible configuration

10. **Document protocol semantics** clearly, including performance expectations
    and usage constraints beyond type signatures

## Common Pitfalls

1. **Creating overly broad protocols** that mix unrelated concerns leads to
   forced implementations and violation of interface segregation

2. **Forgetting mutating keyword** on protocol methods that modify value types
   causes compilation errors in struct implementations

3. **Protocol extension shadowing** where methods in extensions don't override
   implementations, using static dispatch instead

4. **Not constraining associated types** sufficiently allows conforming types to
   choose inappropriate concrete types

5. **Overusing type erasure** when simpler solutions exist adds complexity and
   obscures actual types unnecessarily

6. **Ignoring protocol vs class dispatch** differences leads to unexpected
   behavior when protocols use extensions and classes use inheritance

7. **Creating protocol hierarchies that mimic classes** defeats the purpose of
   protocol-oriented programming's compositional benefits

8. **Not providing default implementations** when most conforming types would
   use the same logic wastes opportunities for reuse

9. **Using protocols for everything** when concrete types suffice adds
   abstraction overhead without meaningful benefit

10. **Failing to test protocol conformance** thoroughly allows bugs in
    implementations that satisfy signatures but violate semantics

## When to Use This Skill

Use protocol-oriented programming when building Swift applications that require
flexibility, testability, and code reuse across value types and classes. This
applies to iOS, macOS, watchOS, tvOS, and server-side Swift development.

Apply protocols and extensions when designing frameworks, libraries, or modules
that need to support multiple implementations or allow clients to customize
behavior without subclassing.

Employ protocol composition when creating precise type constraints for functions
and properties, especially in generic code that needs to operate on types
satisfying multiple requirements.

Leverage associated types when building generic abstractions like collections,
transformers, or data sources where conforming types need to specify concrete
types.

Use protocol-based dependency injection in architectural patterns like MVVM,
VIPER, or Clean Architecture to improve testability and decouple components.

## Resources

- [Protocol-Oriented Programming WWDC Session](<https://developer.apple.com/videos/play/wwdc2015/408/>)
- [Swift Language Guide - Protocols](<https://docs.swift.org/swift-book/documentation/the-swift-programming-language/protocols/>)
- [Protocol Extensions Documentation](<https://docs.swift.org/swift-book/documentation/the-swift-programming-language/protocols/#Protocol-Extensions>)
- [Advanced Swift by Chris Eidhof](<https://www.objc.io/books/advanced-swift/>)
- [Swift Evolution Proposals](<https://github.com/apple/swift-evolution>)
