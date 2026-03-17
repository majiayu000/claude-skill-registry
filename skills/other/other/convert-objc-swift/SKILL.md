---
name: convert-objc-swift
description: Convert Objective-C code to idiomatic Swift. Use when migrating Objective-C projects to Swift, translating Objective-C patterns to modern Swift, modernizing legacy codebases, or establishing gradual migration strategies with interop. Extends meta-convert-dev with Objective-C-to-Swift specific patterns including bridging and @objc attributes.
---

# Convert Objective-C to Swift

Convert Objective-C code to idiomatic Swift. This skill extends `meta-convert-dev` with Objective-C-to-Swift specific type mappings, idiom translations, interoperability patterns, and tooling for gradual migration.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Objective-C types → Swift types
- **Idiom translations**: Objective-C patterns → idiomatic Swift
- **Error handling**: NSError pattern → Swift throws/Result
- **Memory management**: Manual/ARC → Swift ARC with value semantics
- **FFI/Interop**: Bridging headers, @objc attributes, gradual migration strategies

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Objective-C language fundamentals - see `lang-objc-dev`
- Swift language fundamentals - see `lang-swift-dev`
- Reverse conversion (Swift → Objective-C) - see `convert-swift-objc`
- SwiftUI → UIKit migration - see platform-specific skills

---

## Quick Reference

| Objective-C | Swift | Notes |
|-------------|-------|-------|
| `NSString *` | `String` | Swift String is value type |
| `NSInteger` | `Int` | Platform-dependent signed integer |
| `BOOL` | `Bool` | Direct mapping |
| `NSArray *` | `[Any]` / `[Element]` | Generic array with type safety |
| `NSMutableArray *` | `[Element]` | Use `var` for mutability |
| `NSDictionary *` | `[String: Any]` / `[Key: Value]` | Generic dictionary |
| `id` | `Any` / `AnyObject` | Type-erased reference |
| `id<Protocol>` | `any Protocol` / `some Protocol` | Existential or opaque type |
| `nullable id` | `Optional<Any>` / `Any?` | Explicit optionality |
| `instancetype` | `Self` | Return type is class of receiver |
| `typedef void (^Block)()` | `() -> Void` | Closure type |
| `@property (weak)` | `weak var` | Weak reference |
| `@property (copy)` | `let` (for strings) | Immutable by default |
| `[obj method:param]` | `obj.method(param)` | Dot syntax |

## When Converting Code

1. **Analyze source thoroughly** - Understand memory management, protocols, categories
2. **Map types first** - Create comprehensive type equivalence table
3. **Preserve semantics** - Match behavior, not just syntax
4. **Adopt Swift idioms** - Don't write "Objective-C code in Swift syntax"
5. **Handle edge cases** - nil messaging, NSNull, dynamic typing
6. **Leverage type safety** - Replace `id` with specific types or generics
7. **Test equivalence** - Same inputs → same outputs

---

## Type System Mapping

### Primitive Types

| Objective-C | Swift | Notes |
|-------------|-------|-------|
| `BOOL` | `Bool` | Direct mapping (true/false vs YES/NO) |
| `NSInteger` | `Int` | Platform-dependent signed (32-bit or 64-bit) |
| `NSUInteger` | `UInt` | Platform-dependent unsigned |
| `int` | `Int32` | Explicit 32-bit signed |
| `unsigned int` | `UInt32` | Explicit 32-bit unsigned |
| `long` | `Int` (64-bit) / `Int32` (32-bit) | Platform-dependent |
| `long long` | `Int64` | Explicit 64-bit signed |
| `float` | `Float` | 32-bit floating point |
| `double` | `Double` | 64-bit floating point (default) |
| `CGFloat` | `CGFloat` | Platform-dependent float (bridged) |
| `char` | `CChar` / `Int8` | C char type |
| `unichar` | `UInt16` | Unicode character |
| `void` | `Void` / `()` | Unit type |
| `instancetype` | `Self` | Return type of current class |

### Foundation Types

| Objective-C | Swift | Notes |
|-------------|-------|-------|
| `NSString *` | `String` | Bridged; Swift String is value type |
| `NSMutableString *` | `String` (with `var`) | Swift strings mutable with var |
| `NSNumber *` | `NSNumber` / specific type | Bridge to Int, Double, Bool when possible |
| `NSArray *` | `[Any]` | Untyped array |
| `NSArray<Type *> *` | `[Type]` | Generic array with type safety |
| `NSMutableArray *` | `[Element]` (with `var`) | Mutable via var declaration |
| `NSDictionary *` | `[String: Any]` | Untyped dictionary |
| `NSDictionary<K, V> *` | `[K: V]` | Generic dictionary |
| `NSMutableDictionary *` | `[K: V]` (with `var`) | Mutable via var |
| `NSSet *` | `Set<AnyHashable>` | Untyped set |
| `NSSet<Type *> *` | `Set<Type>` | Generic set |
| `NSData *` | `Data` | Bridged value type |
| `NSDate *` | `Date` | Bridged value type |
| `NSURL *` | `URL` | Bridged value type |
| `NSError *` | `Error` / `NSError` | Conforming to Error protocol |

### Nullability and Optionals

| Objective-C | Swift | Notes |
|-------------|-------|-------|
| `id` | `Any?` | Implicitly optional in Objective-C |
| `nullable id` | `Any?` | Explicitly nullable |
| `nonnull id` | `Any` | Non-optional |
| `_Nullable` | `?` | Optional |
| `_Nonnull` | Non-optional | Default in Swift |
| `nil` | `nil` | Same keyword, different semantics |

### Blocks and Closures

| Objective-C | Swift | Notes |
|-------------|-------|-------|
| `void (^)(void)` | `() -> Void` | No parameters, no return |
| `NSInteger (^)(NSInteger)` | `(Int) -> Int` | Single parameter |
| `void (^)(NSString *, NSError *)` | `(String, Error) -> Void` | Multiple parameters |
| `typedef void (^Completion)()` | `typealias Completion = () -> Void` | Type alias |
| `@escaping` (implicit) | `@escaping` (explicit) | Escaping closures marked in Swift |

### Collection Types

| Objective-C | Swift | Notes |
|-------------|-------|-------|
| `NSArray<T *> *` | `[T]` | Generic array |
| `NSMutableArray<T *> *` | `var array: [T]` | Mutable array |
| `NSDictionary<K, V> *` | `[K: V]` | Generic dictionary |
| `NSMutableDictionary<K, V> *` | `var dict: [K: V]` | Mutable dictionary |
| `NSSet<T *> *` | `Set<T>` | Generic set |
| `NSMutableSet<T *> *` | `var set: Set<T>` | Mutable set |
| `NSOrderedSet<T *> *` | Custom (no direct equivalent) | Use array with uniqueness logic |

### Composite Types

| Objective-C | Swift | Notes |
|-------------|-------|-------|
| `@interface Class : Super` | `class Class: Super` | Class declaration |
| `@interface Class <Protocol>` | `class Class: Protocol` | Protocol adoption |
| `@interface Class ()` (extension) | `private extension Class` | Class extension |
| `@interface Class (Category)` | `extension Class` | Category → Extension |
| `@protocol Protocol` | `protocol Protocol` | Protocol definition |
| `@property Type *prop` | `var prop: Type` | Property |
| `@property (readonly)` | `let prop` | Immutable property |
| `@property (weak)` | `weak var` | Weak reference |
| `@property (copy)` | `let` / `var` | Copy semantic (Swift strings already copy) |
| `enum TypeName` | `enum TypeName` | Enumeration |
| `NS_ENUM(NSInteger, Name)` | `enum Name: Int` | Integer-backed enum |
| `NS_OPTIONS(NSUInteger, Name)` | `struct Name: OptionSet` | Option set |
| `typedef` | `typealias` | Type alias |
| `struct` | `struct` | Value type |

---

## Idiom Translation

### Pattern 1: Property Declaration and Access

**Objective-C:**
```objc
@interface Person : NSObject
@property (nonatomic, strong) NSString *name;
@property (nonatomic, assign) NSInteger age;
@property (nonatomic, weak) id<PersonDelegate> delegate;
@property (nonatomic, copy) NSString *bio;
@property (nonatomic, readonly) NSString *identifier;
@end

@implementation Person
@end

// Usage
Person *person = [[Person alloc] init];
person.name = @"Alice";
NSInteger age = person.age;
```

**Swift:**
```swift
class Person {
    var name: String
    var age: Int
    weak var delegate: (any PersonDelegate)?
    var bio: String  // Swift strings already have value semantics
    let identifier: String  // readonly → let

    init(name: String = "", age: Int = 0, identifier: String) {
        self.name = name
        self.age = age
        self.identifier = identifier
        self.bio = ""
    }
}

// Usage
let person = Person(identifier: UUID().uuidString)
person.name = "Alice"
let age = person.age
```

**Why this translation:**
- Swift properties don't need `@property` declaration
- Memory semantics: `strong` is default, `weak` explicit, `copy` unnecessary for value types
- Initialization required for all non-optional stored properties
- `let` for immutable, `var` for mutable

### Pattern 2: Method Declaration and Invocation

**Objective-C:**
```objc
@interface Calculator : NSObject
- (NSInteger)add:(NSInteger)a to:(NSInteger)b;
+ (instancetype)sharedCalculator;
- (void)performCalculation:(NSInteger)input
                completion:(void (^)(NSInteger result, NSError *error))completion;
@end

@implementation Calculator
- (NSInteger)add:(NSInteger)a to:(NSInteger)b {
    return a + b;
}

+ (instancetype)sharedCalculator {
    static Calculator *shared = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        shared = [[self alloc] init];
    });
    return shared;
}
@end

// Usage
Calculator *calc = [Calculator sharedCalculator];
NSInteger result = [calc add:5 to:10];
```

**Swift:**
```swift
class Calculator {
    func add(_ a: Int, to b: Int) -> Int {
        return a + b
    }

    static let shared = Calculator()

    func performCalculation(
        _ input: Int,
        completion: @escaping (Result<Int, Error>) -> Void
    ) {
        // Implementation
    }
}

// Usage
let calc = Calculator.shared
let result = calc.add(5, to: 10)
```

**Why this translation:**
- Swift methods use parameter labels naturally
- Singleton: `static let` is thread-safe and simpler than dispatch_once
- Completion handlers: prefer `Result<T, E>` over separate parameters
- `@escaping` must be explicit for closures that outlive function scope

### Pattern 3: Nullability and Optional Handling

**Objective-C:**
```objc
- (nullable NSString *)findUserName:(NSString *)userId {
    User *user = [self.users objectForKey:userId];
    return user ? user.name : nil;
}

// Usage
NSString *name = [self findUserName:@"123"];
if (name) {
    NSLog(@"Name: %@", name);
} else {
    NSLog(@"User not found");
}

// Nil messaging (safe)
NSString *upper = [name uppercaseString];  // Returns nil if name is nil
```

**Swift:**
```swift
func findUserName(_ userId: String) -> String? {
    guard let user = users[userId] else {
        return nil
    }
    return user.name
}

// Usage
if let name = findUserName("123") {
    print("Name: \(name)")
} else {
    print("User not found")
}

// Optional chaining
let upper = name?.uppercased()  // nil if name is nil

// Nil coalescing
let displayName = findUserName("123") ?? "Unknown"
```

**Why this translation:**
- Swift optionals are explicit and type-safe
- `if let` / `guard let` for safe unwrapping
- Optional chaining (`?.`) replaces Objective-C nil messaging
- Nil coalescing (`??`) provides defaults
- Force unwrap (`!`) should be rare and justified

### Pattern 4: Protocols and Delegation

**Objective-C:**
```objc
@protocol DataSourceDelegate <NSObject>
@required
- (NSInteger)numberOfItems;
@optional
- (void)didSelectItemAtIndex:(NSInteger)index;
@end

@interface DataSource : NSObject
@property (nonatomic, weak) id<DataSourceDelegate> delegate;
@end

@implementation DataSource
- (void)loadData {
    if ([self.delegate respondsToSelector:@selector(numberOfItems)]) {
        NSInteger count = [self.delegate numberOfItems];
    }

    if ([self.delegate respondsToSelector:@selector(didSelectItemAtIndex:)]) {
        [self.delegate didSelectItemAtIndex:0];
    }
}
@end
```

**Swift:**
```swift
protocol DataSourceDelegate: AnyObject {
    func numberOfItems() -> Int
    func didSelectItem(at index: Int)  // Optional methods not directly supported
}

// For optional protocol methods, use separate protocols or default implementations
extension DataSourceDelegate {
    func didSelectItem(at index: Int) {
        // Default implementation (makes it optional)
    }
}

class DataSource {
    weak var delegate: (any DataSourceDelegate)?

    func loadData() {
        guard let delegate = delegate else { return }

        let count = delegate.numberOfItems()
        delegate.didSelectItem(at: 0)  // Safe to call due to default implementation
    }
}
```

**Why this translation:**
- Swift protocols require `AnyObject` for class-only protocols (enables weak references)
- No `@required`/`@optional` - use protocol extensions for default implementations
- No runtime checks needed with type-safe protocols
- `any Protocol` for existential types (heterogeneous collections)

### Pattern 5: Enumerations

**Objective-C:**
```objc
typedef NS_ENUM(NSInteger, HTTPStatus) {
    HTTPStatusOK = 200,
    HTTPStatusNotFound = 404,
    HTTPStatusServerError = 500
};

typedef NS_OPTIONS(NSUInteger, FilePermissions) {
    FilePermissionsRead    = 1 << 0,
    FilePermissionsWrite   = 1 << 1,
    FilePermissionsExecute = 1 << 2
};

// Usage
HTTPStatus status = HTTPStatusOK;
FilePermissions perms = FilePermissionsRead | FilePermissionsWrite;
```

**Swift:**
```swift
enum HTTPStatus: Int {
    case ok = 200
    case notFound = 404
    case serverError = 500
}

struct FilePermissions: OptionSet {
    let rawValue: UInt

    static let read    = FilePermissions(rawValue: 1 << 0)
    static let write   = FilePermissions(rawValue: 1 << 1)
    static let execute = FilePermissions(rawValue: 1 << 2)
}

// Usage
let status = HTTPStatus.ok
let perms: FilePermissions = [.read, .write]

// Pattern matching
switch status {
case .ok:
    print("Success")
case .notFound:
    print("Not found")
case .serverError:
    print("Server error")
}
```

**Why this translation:**
- `NS_ENUM` → Swift `enum` with raw value
- `NS_OPTIONS` → `OptionSet` struct for bitwise options
- Swift enums are type-safe with pattern matching
- Array literal syntax for option sets

### Pattern 6: Error Handling

**Objective-C:**
```objc
- (BOOL)loadDataFromFile:(NSString *)path error:(NSError **)error {
    NSData *data = [NSData dataWithContentsOfFile:path options:0 error:error];
    if (!data) {
        return NO;
    }
    // Process data
    return YES;
}

// Creating custom errors
- (BOOL)validateUser:(User *)user error:(NSError **)error {
    if (user.name.length == 0) {
        if (error) {
            *error = [NSError errorWithDomain:@"com.example.validation"
                                         code:100
                                     userInfo:@{
                                         NSLocalizedDescriptionKey: @"Name is required"
                                     }];
        }
        return NO;
    }
    return YES;
}

// Usage
NSError *error = nil;
BOOL success = [self loadDataFromFile:@"data.txt" error:&error];
if (!success) {
    NSLog(@"Error: %@", error.localizedDescription);
}
```

**Swift:**
```swift
enum ValidationError: Error {
    case nameRequired
    case invalidFormat(String)
}

func loadData(from path: String) throws -> Data {
    return try Data(contentsOfFile: path)
}

func validateUser(_ user: User) throws {
    guard !user.name.isEmpty else {
        throw ValidationError.nameRequired
    }
}

// Usage with do-catch
do {
    let data = try loadData(from: "data.txt")
    // Process data
} catch {
    print("Error: \(error.localizedDescription)")
}

// Usage with try?
if let data = try? loadData(from: "data.txt") {
    // Process data
}

// Usage with Result
func loadDataResult(from path: String) -> Result<Data, Error> {
    Result { try Data(contentsOfFile: path) }
}
```

**Why this translation:**
- Swift uses exceptions (`throws`) instead of error pointers
- Custom error types conform to `Error` protocol (usually enums)
- `do-catch` for error handling
- `try?` for optional conversion
- `Result<T, E>` for explicit error values
- More type-safe and composable than NSError pattern

### Pattern 7: Categories → Extensions

**Objective-C:**
```objc
// NSString+Validation.h
@interface NSString (Validation)
- (BOOL)isValidEmail;
@end

// NSString+Validation.m
@implementation NSString (Validation)
- (BOOL)isValidEmail {
    NSString *pattern = @"[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}";
    NSPredicate *predicate = [NSPredicate predicateWithFormat:@"SELF MATCHES %@", pattern];
    return [predicate evaluateWithObject:self];
}
@end

// Usage
NSString *email = @"user@example.com";
if ([email isValidEmail]) {
    NSLog(@"Valid email");
}
```

**Swift:**
```swift
extension String {
    var isValidEmail: Bool {
        let pattern = "[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"
        let predicate = NSPredicate(format: "SELF MATCHES %@", pattern)
        return predicate.evaluate(with: self)
    }
}

// Usage
let email = "user@example.com"
if email.isValidEmail {
    print("Valid email")
}
```

**Why this translation:**
- Categories directly map to Swift extensions
- Prefer computed properties over methods when no parameters
- Extensions can add stored properties via associated objects (advanced)
- Swift extensions more powerful (can conform to protocols, add constraints)

### Pattern 8: Blocks → Closures

**Objective-C:**
```objc
typedef void (^CompletionBlock)(NSData *data, NSError *error);

@interface NetworkManager : NSObject
- (void)fetchDataWithCompletion:(CompletionBlock)completion;
@end

@implementation NetworkManager
- (void)fetchDataWithCompletion:(CompletionBlock)completion {
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        NSData *data = [self loadData];
        dispatch_async(dispatch_get_main_queue(), ^{
            if (completion) {
                completion(data, nil);
            }
        });
    });
}

// Avoiding retain cycles
- (void)setupCompletion {
    __weak typeof(self) weakSelf = self;
    self.completion = ^{
        __strong typeof(weakSelf) strongSelf = weakSelf;
        if (strongSelf) {
            [strongSelf doSomething];
        }
    };
}
@end
```

**Swift:**
```swift
typealias CompletionBlock = (Result<Data, Error>) -> Void

class NetworkManager {
    func fetchData(completion: @escaping CompletionBlock) {
        DispatchQueue.global().async {
            let data = self.loadData()
            DispatchQueue.main.async {
                completion(.success(data))
            }
        }
    }

    // Modern async/await (preferred)
    func fetchData() async throws -> Data {
        return try await withCheckedThrowingContinuation { continuation in
            fetchData { result in
                continuation.resume(with: result)
            }
        }
    }

    // Avoiding retain cycles
    var completion: (() -> Void)?

    func setupCompletion() {
        completion = { [weak self] in
            guard let self = self else { return }
            self.doSomething()
        }
    }
}
```

**Why this translation:**
- Closure types more concise than block types
- `@escaping` required for stored closures
- Prefer `Result<T, E>` over separate data/error parameters
- Swift async/await preferred over callbacks
- `[weak self]` / `guard let self` pattern cleaner than weak-strong dance

---

## FFI & Interoperability (10th Pillar)

Objective-C to Swift interoperability is exceptional, enabling **gradual migration** - the primary migration strategy for large codebases. You can mix Objective-C and Swift in the same project, calling code bidirectionally.

### Why FFI/Interop Matters for This Conversion

Unlike most language conversions, Objective-C → Swift supports:

1. **Incremental migration**: Convert one class at a time while maintaining a working app
2. **Bidirectional calling**: Swift can call Objective-C, Objective-C can call Swift
3. **Shared types**: Foundation types bridge automatically
4. **Same runtime**: Both use the Objective-C runtime on Apple platforms

### Gradual Migration Strategy

```
┌─────────────────────────────────────────────────────────────┐
│              OBJECTIVE-C → SWIFT MIGRATION                   │
├─────────────────────────────────────────────────────────────┤
│  Phase 1: SETUP                                              │
│  • Enable "Use Swift" in Xcode project                       │
│  • Create bridging header (auto-generated)                   │
│  • Import essential Objective-C headers                      │
├─────────────────────────────────────────────────────────────┤
│  Phase 2: IDENTIFY                                           │
│  • Start with leaf classes (fewest dependencies)             │
│  • Identify pure data models (easy to convert)               │
│  • Map protocols and categories                              │
├─────────────────────────────────────────────────────────────┤
│  Phase 3: CONVERT                                            │
│  • Convert one class at a time                               │
│  • Add @objc attribute to maintain Objective-C visibility    │
│  • Test after each conversion                                │
├─────────────────────────────────────────────────────────────┤
│  Phase 4: MODERNIZE                                          │
│  • Remove @objc where not needed                             │
│  • Adopt Swift-only features (optionals, value types)        │
│  • Refactor to protocol-oriented design                      │
├─────────────────────────────────────────────────────────────┤
│  Phase 5: COMPLETE                                           │
│  • Remove bridging header when all Objective-C gone          │
│  • Pure Swift codebase                                       │
└─────────────────────────────────────────────────────────────┘
```

### Bridging Header

When you add the first Swift file to an Objective-C project, Xcode creates a bridging header.

**ProjectName-Bridging-Header.h:**
```objc
// Import Objective-C headers to expose them to Swift
#import "MyObjectiveCClass.h"
#import "DataModel.h"
#import "NetworkManager.h"

// Framework imports
#import <SomeFramework/SomeFramework.h>
```

**Rules:**
- Import Objective-C headers here to use them in Swift
- No need to import in individual Swift files
- Only for app targets (frameworks use module maps)

### Using Objective-C from Swift

**Objective-C class:**
```objc
// Person.h
@interface Person : NSObject
@property (nonatomic, strong) NSString *name;
@property (nonatomic, assign) NSInteger age;
- (void)greet;
@end

// Person.m
@implementation Person
- (void)greet {
    NSLog(@"Hello, I'm %@", self.name);
}
@end
```

**Import in bridging header:**
```objc
// ProjectName-Bridging-Header.h
#import "Person.h"
```

**Use from Swift:**
```swift
// No import needed - bridging header makes it available
let person = Person()
person.name = "Alice"
person.age = 30
person.greet()
```

### Using Swift from Objective-C

**Swift class with @objc:**
```swift
// User.swift
@objc class User: NSObject {
    @objc var username: String
    @objc var email: String

    @objc init(username: String, email: String) {
        self.username = username
        self.email = email
        super.init()
    }

    @objc func validate() -> Bool {
        return !username.isEmpty && !email.isEmpty
    }
}
```

**Use from Objective-C:**
```objc
// Import generated header
#import "ProjectName-Swift.h"

// Use Swift class
User *user = [[User alloc] initWithUsername:@"alice" email:@"alice@example.com"];
BOOL isValid = [user validate];
```

**Key points:**
- `@objc` attribute exposes Swift declarations to Objective-C
- Swift class must inherit from NSObject (or @objc class)
- Xcode auto-generates `ProjectName-Swift.h` header
- Not all Swift features available in Objective-C (generics, protocols with associated types, etc.)

### @objc Attributes

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `@objc` | Expose to Objective-C runtime | `@objc func method()` |
| `@objc(name)` | Custom Objective-C name | `@objc(customName) func swiftName()` |
| `@objcMembers` | Expose all members of class | `@objcMembers class MyClass` |
| `@nonobjc` | Hide from Objective-C | `@nonobjc func swiftOnly()` |
| `@IBOutlet` | Interface Builder outlet | `@IBOutlet weak var label: UILabel!` |
| `@IBAction` | Interface Builder action | `@IBAction func buttonTapped()` |

### Type Bridging

Foundation types bridge automatically between Objective-C and Swift:

| Objective-C | Swift | Bridging |
|-------------|-------|----------|
| `NSString` | `String` | Automatic, toll-free |
| `NSArray` | `[Any]` | Automatic |
| `NSDictionary` | `[AnyHashable: Any]` | Automatic |
| `NSSet` | `Set<AnyHashable>` | Automatic |
| `NSNumber` | `Int`, `Double`, `Bool` | Automatic (context-dependent) |
| `NSData` | `Data` | Automatic |
| `NSDate` | `Date` | Automatic |
| `NSURL` | `URL` | Automatic |
| `NSError` | `Error` | Automatic (protocol conformance) |

**Bridging is free** - no performance cost for toll-free bridging.

### Protocol Bridging

**Objective-C protocol:**
```objc
@protocol Drawable <NSObject>
- (void)draw;
@optional
- (void)setColor:(UIColor *)color;
@end
```

**Use from Swift:**
```swift
// Conforms to Objective-C protocol
class Circle: NSObject, Drawable {
    func draw() {
        print("Drawing circle")
    }

    func setColor(_ color: UIColor) {
        // Optional method
    }
}
```

**Swift protocol exposed to Objective-C:**
```swift
@objc protocol Vehicle {
    @objc var speed: Double { get }
    @objc func accelerate()
    @objc optional func honk()  // Optional methods need @objc protocol
}
```

### Common Interop Patterns

#### Pattern: Mixed Inheritance

**Objective-C base class:**
```objc
@interface Animal : NSObject
@property (nonatomic, strong) NSString *name;
- (void)makeSound;
@end
```

**Swift subclass:**
```swift
class Dog: Animal {
    var breed: String = ""

    override func makeSound() {
        print("\(name ?? "") barks!")
    }

    func wagTail() {
        print("Wagging tail")
    }
}
```

#### Pattern: Category on Swift Class

You can add Objective-C categories to Swift classes:

**Swift class:**
```swift
@objc class Calculator: NSObject {
    @objc func add(_ a: Int, to b: Int) -> Int {
        return a + b
    }
}
```

**Objective-C category:**
```objc
@interface Calculator (Advanced)
- (NSInteger)multiply:(NSInteger)a by:(NSInteger)b;
@end

@implementation Calculator (Advanced)
- (NSInteger)multiply:(NSInteger)a by:(NSInteger)b {
    return a * b;
}
@end
```

#### Pattern: Selector and Dynamic Dispatch

**Objective-C dynamic behavior:**
```objc
SEL selector = @selector(greet);
if ([person respondsToSelector:selector]) {
    [person performSelector:selector];
}
```

**Swift equivalent:**
```swift
// Using @objc and Selector
@objc class Person: NSObject {
    @objc func greet() {
        print("Hello")
    }
}

let selector = #selector(Person.greet)
if person.responds(to: selector) {
    person.perform(selector)
}

// Modern Swift: prefer protocols and type safety
protocol Greeter {
    func greet()
}

if let greeter = person as? Greeter {
    greeter.greet()
}
```

### Interop Limitations

**Swift features NOT available in Objective-C:**

| Swift Feature | Workaround |
|---------------|------------|
| Generics | Use specific types or `id` |
| Protocols with associated types | Use type-erased wrappers |
| Tuples | Use structs or separate parameters |
| Enums with associated values | Use separate classes or `NS_ENUM` |
| Value types (struct) | Use classes (`NSObject` subclass) |
| Optionals (except via `_Nullable`) | Use nullable annotations |
| Protocol extensions | Expose via concrete class |

**Example: Type-erased wrapper for generic protocol:**
```swift
// Swift generic protocol (not @objc compatible)
protocol Container {
    associatedtype Element
    func add(_ element: Element)
}

// Type-erased wrapper for Objective-C
@objc class AnyContainer: NSObject {
    private let _add: (Any) -> Void

    init<C: Container>(_ container: C) {
        self._add = { element in
            if let typedElement = element as? C.Element {
                container.add(typedElement)
            }
        }
    }

    @objc func add(_ element: Any) {
        _add(element)
    }
}
```

### Build Configuration

**Mixed language targets:**

1. **Bridging header** (Objective-C → Swift):
   - Build Settings → "Objective-C Bridging Header"
   - Path: `ProjectName/ProjectName-Bridging-Header.h`

2. **Generated interface** (Swift → Objective-C):
   - Automatic: `ProjectName-Swift.h`
   - Import in Objective-C files

3. **Module name** (for Swift imports):
   - Build Settings → "Product Module Name"
   - Default: `ProjectName`

### Testing Mixed Code

```swift
// XCTest works with both languages
class MixedTests: XCTestCase {
    func testObjectiveCClass() {
        let person = Person()  // Objective-C class
        person.name = "Alice"
        XCTAssertEqual(person.name, "Alice")
    }

    func testSwiftClass() {
        let user = User(username: "bob", email: "bob@example.com")
        XCTAssertTrue(user.validate())
    }
}
```

**From Objective-C tests:**
```objc
@import XCTest;
#import "ProjectName-Swift.h"

@interface MixedTests : XCTestCase
@end

@implementation MixedTests
- (void)testSwiftClass {
    User *user = [[User alloc] initWithUsername:@"alice" email:@"alice@example.com"];
    XCTAssertTrue([user validate]);
}
@end
```

---

## Memory Management

### Objective-C ARC → Swift ARC

Both languages use Automatic Reference Counting, but Swift adds value semantics.

| Objective-C | Swift | Notes |
|-------------|-------|-------|
| `@property (strong)` | `var` (default) | Strong reference |
| `@property (weak)` | `weak var` | Weak reference |
| `@property (copy)` | `let` / `var` | Swift Strings/Arrays already have value semantics |
| `@property (assign)` | `var` (value types) | Primitive types |
| `__weak` | `weak` | Weak in closures |
| `__strong` | Default | Strong in closures |
| `__unsafe_unretained` | `unowned(unsafe)` | Rarely used |

### Reference Cycles

**Objective-C:**
```objc
@interface Parent : NSObject
@property (strong) Child *child;
@end

@interface Child : NSObject
@property (weak) Parent *parent;  // Weak to break cycle
@end

// Block cycle
__weak typeof(self) weakSelf = self;
self.completion = ^{
    __strong typeof(weakSelf) strongSelf = weakSelf;
    if (strongSelf) {
        [strongSelf doWork];
    }
};
```

**Swift:**
```swift
class Parent {
    var child: Child?
}

class Child {
    weak var parent: Parent?  // Weak to break cycle
}

// Closure cycle
completion = { [weak self] in
    guard let self = self else { return }
    self.doWork()
}

// Unowned (when you know reference always exists)
completion = { [unowned self] in
    self.doWork()  // Crashes if self is deallocated
}
```

### Value Semantics

**Objective-C (reference types):**
```objc
NSMutableArray *array1 = [NSMutableArray arrayWithObjects:@"A", @"B", nil];
NSMutableArray *array2 = array1;  // Same object
[array2 addObject:@"C"];
// array1 also contains "C"
```

**Swift (value types):**
```swift
var array1 = ["A", "B"]
var array2 = array1  // Copy on write
array2.append("C")
// array1 still ["A", "B"], array2 is ["A", "B", "C"]
```

**Why this matters:**
- Swift structs, enums, and standard types (String, Array, Dictionary) are value types
- Copy-on-write optimization prevents unnecessary copying
- Reference types (classes) still work like Objective-C
- Prefer value types in Swift for simpler, safer code

---

## Concurrency Patterns

### GCD → DispatchQueue

**Objective-C:**
```objc
dispatch_queue_t queue = dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0);
dispatch_async(queue, ^{
    NSData *data = [self heavyComputation];

    dispatch_async(dispatch_get_main_queue(), ^{
        [self updateUIWithData:data];
    });
});
```

**Swift (GCD):**
```swift
DispatchQueue.global().async {
    let data = self.heavyComputation()

    DispatchQueue.main.async {
        self.updateUI(with: data)
    }
}
```

**Swift (modern async/await):**
```swift
Task {
    let data = await heavyComputation()
    await MainActor.run {
        updateUI(with: data)
    }
}

// Async function
func heavyComputation() async -> Data {
    // Computation
    return data
}
```

### Completion Handlers → Async/Await

**Objective-C:**
```objc
- (void)fetchUserWithId:(NSString *)userId
             completion:(void (^)(User *user, NSError *error))completion {
    [self.network GET:@"/users" parameters:@{@"id": userId} success:^(id response) {
        User *user = [User fromJSON:response];
        completion(user, nil);
    } failure:^(NSError *error) {
        completion(nil, error);
    }];
}
```

**Swift (callback style):**
```swift
func fetchUser(
    id: String,
    completion: @escaping (Result<User, Error>) -> Void
) {
    network.get("/users", parameters: ["id": id]) { result in
        switch result {
        case .success(let data):
            let user = User(from: data)
            completion(.success(user))
        case .failure(let error):
            completion(.failure(error))
        }
    }
}
```

**Swift (async/await - preferred):**
```swift
func fetchUser(id: String) async throws -> User {
    let data = try await network.get("/users", parameters: ["id": id])
    return User(from: data)
}

// Usage
Task {
    do {
        let user = try await fetchUser(id: "123")
        print("Got user: \(user.name)")
    } catch {
        print("Error: \(error)")
    }
}
```

### Actors for Thread Safety

**Objective-C (manual synchronization):**
```objc
@interface BankAccount : NSObject
@property (atomic, assign) double balance;
@end

@implementation BankAccount
- (void)deposit:(double)amount {
    @synchronized(self) {
        self.balance += amount;
    }
}

- (BOOL)withdraw:(double)amount {
    @synchronized(self) {
        if (self.balance >= amount) {
            self.balance -= amount;
            return YES;
        }
        return NO;
    }
}
@end
```

**Swift (actor - automatic synchronization):**
```swift
actor BankAccount {
    private var balance: Double = 0

    func deposit(amount: Double) {
        balance += amount
    }

    func withdraw(amount: Double) -> Bool {
        guard balance >= amount else {
            return false
        }
        balance -= amount
        return true
    }
}

// Usage (automatically synchronized)
let account = BankAccount()
Task {
    await account.deposit(amount: 100)
    let success = await account.withdraw(amount: 50)
}
```

---

## Common Pitfalls

### 1. Force Unwrapping Optionals

**Problem:** Crashes when value is nil

**Objective-C:**
```objc
// Nil messaging is safe
NSString *name = [user name];  // Returns nil if user is nil
NSString *upper = [name uppercaseString];  // Returns nil if name is nil
```

**Swift (bad):**
```swift
let name = user!.name  // Crashes if user is nil
let upper = name!.uppercased()  // Crashes if name is nil
```

**Swift (good):**
```swift
guard let user = user else { return }
let name = user.name
let upper = name?.uppercased() ?? ""
```

### 2. Forgetting @objc for Interop

**Problem:** Swift declarations not visible to Objective-C

```swift
// Bad: Not visible to Objective-C
class MyClass {
    func myMethod() { }
}

// Good: Visible to Objective-C
@objc class MyClass: NSObject {
    @objc func myMethod() { }
}
```

### 3. Using id Instead of Specific Types

**Objective-C:**
```objc
- (id)fetchData {
    return @{@"key": @"value"};
}
```

**Swift (avoid):**
```swift
func fetchData() -> Any {
    return ["key": "value"]
}
```

**Swift (prefer):**
```swift
func fetchData() -> [String: String] {
    return ["key": "value"]
}
```

### 4. Ignoring Mutability Semantics

**Objective-C:**
```objc
NSArray *array = [NSArray arrayWithObjects:@"A", nil];
NSMutableArray *mutable = (NSMutableArray *)array;  // Dangerous cast
[mutable addObject:@"B"];  // Runtime error
```

**Swift:**
```swift
let array = ["A"]  // Immutable
// var mutable = array as! [String]  // No such thing as "mutable cast"

var mutable = array  // Copy
mutable.append("B")  // Safe, modifies copy
```

### 5. Not Handling nil in Collections

**Objective-C:**
```objc
NSArray *items = @[@"A", [NSNull null], @"C"];
NSString *second = items[1];  // NSNull object
// [second uppercaseString];  // Crashes - NSNull doesn't respond
```

**Swift:**
```swift
// Use optionals
let items: [String?] = ["A", nil, "C"]
let second = items[1]  // Optional<String>
let upper = second?.uppercased()  // Safe

// Or filter nils
let nonNilItems = items.compactMap { $0 }
```

### 6. Misunderstanding Property Attributes

**Objective-C:**
```objc
@property (copy) NSMutableString *title;  // Bad: copy makes it immutable
```

**Swift:**
```swift
// String already has value semantics
var title: String  // No need for "copy"

// For reference types that should be copied
var items: [Item] {
    didSet {
        // Array automatically copies on mutation
    }
}
```

### 7. Selector Typos

**Objective-C:**
```objc
[person performSelector:@selector(gret)];  // Typo: should be "greet"
// Runtime crash: unrecognized selector
```

**Swift:**
```swift
// Type-safe selector
#selector(Person.greet)  // Compiler error if method doesn't exist
```

### 8. Bridging Overhead

**Problem:** Unnecessary bridging between types

**Swift (inefficient):**
```swift
let nsString: NSString = "Hello"
let swiftString = nsString as String  // Bridge
let upper = swiftString.uppercased()
let nsUpper = upper as NSString  // Bridge again
```

**Swift (efficient):**
```swift
let string = "Hello"  // Swift String
let upper = string.uppercased()
// Use NSString only when required by API
```

---

## Tooling

| Tool | Purpose | Notes |
|------|---------|-------|
| Xcode migration assistant | Automated Swift conversion | Use as starting point, manual refinement needed |
| `swiftc` | Swift compiler | Compiles Swift code |
| Swift REPL | Interactive Swift | `swift` command in terminal |
| `swift-demangle` | Demangle Swift symbols | Debug symbol names |
| SwiftLint | Swift style linter | Enforce Swift conventions |
| Objective-C → Swift converter (Xcode) | Edit → Convert → To Modern Objective-C Syntax first | Improves conversion quality |

---

## Examples

### Example 1: Simple - Data Model

**Before (Objective-C):**
```objc
// User.h
@interface User : NSObject
@property (nonatomic, copy) NSString *username;
@property (nonatomic, copy) NSString *email;
@property (nonatomic, assign) NSInteger age;
- (instancetype)initWithUsername:(NSString *)username email:(NSString *)email age:(NSInteger)age;
@end

// User.m
@implementation User
- (instancetype)initWithUsername:(NSString *)username email:(NSString *)email age:(NSInteger)age {
    self = [super init];
    if (self) {
        _username = [username copy];
        _email = [email copy];
        _age = age;
    }
    return self;
}
@end
```

**After (Swift):**
```swift
struct User {
    let username: String
    let email: String
    let age: Int
}

// Auto-generated memberwise initializer:
// init(username: String, email: String, age: Int)

// Usage
let user = User(username: "alice", email: "alice@example.com", age: 30)
```

**Why this translation:**
- Swift `struct` is simpler for pure data
- No need for manual init - memberwise initializer is free
- Value semantics (copy) is default for structs
- `let` for immutable properties

### Example 2: Medium - Protocol and Delegation

**Before (Objective-C):**
```objc
// DataSource.h
@protocol DataSourceDelegate <NSObject>
@required
- (NSInteger)numberOfItems;
@optional
- (void)didSelectItemAtIndex:(NSInteger)index;
@end

@interface DataSource : NSObject
@property (nonatomic, weak) id<DataSourceDelegate> delegate;
- (void)loadData;
@end

// DataSource.m
@implementation DataSource
- (void)loadData {
    if ([self.delegate respondsToSelector:@selector(numberOfItems)]) {
        NSInteger count = [self.delegate numberOfItems];
        NSLog(@"Loading %ld items", (long)count);
    }

    if ([self.delegate respondsToSelector:@selector(didSelectItemAtIndex:)]) {
        [self.delegate didSelectItemAtIndex:0];
    }
}
@end

// ViewController.m
@interface ViewController () <DataSourceDelegate>
@end

@implementation ViewController
- (void)viewDidLoad {
    [super viewDidLoad];
    DataSource *dataSource = [[DataSource alloc] init];
    dataSource.delegate = self;
    [dataSource loadData];
}

- (NSInteger)numberOfItems {
    return 10;
}

- (void)didSelectItemAtIndex:(NSInteger)index {
    NSLog(@"Selected item at index %ld", (long)index);
}
@end
```

**After (Swift):**
```swift
protocol DataSourceDelegate: AnyObject {
    func numberOfItems() -> Int
    func didSelectItem(at index: Int)
}

// Default implementation makes method optional
extension DataSourceDelegate {
    func didSelectItem(at index: Int) {
        // Default: do nothing
    }
}

class DataSource {
    weak var delegate: (any DataSourceDelegate)?

    func loadData() {
        guard let delegate = delegate else { return }

        let count = delegate.numberOfItems()
        print("Loading \(count) items")

        delegate.didSelectItem(at: 0)
    }
}

class ViewController: UIViewController, DataSourceDelegate {
    override func viewDidLoad() {
        super.viewDidLoad()
        let dataSource = DataSource()
        dataSource.delegate = self
        dataSource.loadData()
    }

    func numberOfItems() -> Int {
        return 10
    }

    func didSelectItem(at index: Int) {
        print("Selected item at index \(index)")
    }
}
```

**Why this translation:**
- Protocol extension provides default implementation (replaces @optional)
- No runtime checks needed - type system ensures conformance
- `any DataSourceDelegate` for existential type
- More expressive parameter labels

### Example 3: Complex - Network Manager with Callbacks

**Before (Objective-C):**
```objc
// NetworkManager.h
typedef void (^NetworkCompletion)(id response, NSError *error);

@interface NetworkManager : NSObject
+ (instancetype)sharedManager;
- (void)GET:(NSString *)path
 parameters:(NSDictionary *)params
 completion:(NetworkCompletion)completion;
@end

// NetworkManager.m
@implementation NetworkManager

+ (instancetype)sharedManager {
    static NetworkManager *shared = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        shared = [[self alloc] init];
    });
    return shared;
}

- (void)GET:(NSString *)path
 parameters:(NSDictionary *)params
 completion:(NetworkCompletion)completion {

    NSURL *url = [NSURL URLWithString:path];
    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];

    NSURLSessionDataTask *task = [[NSURLSession sharedSession] dataTaskWithRequest:request
        completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
            if (error) {
                dispatch_async(dispatch_get_main_queue(), ^{
                    completion(nil, error);
                });
                return;
            }

            NSError *parseError = nil;
            id json = [NSJSONSerialization JSONObjectWithData:data options:0 error:&parseError];

            dispatch_async(dispatch_get_main_queue(), ^{
                if (parseError) {
                    completion(nil, parseError);
                } else {
                    completion(json, nil);
                }
            });
        }];

    [task resume];
}

@end

// Usage
[[NetworkManager sharedManager] GET:@"https://api.example.com/users"
                          parameters:@{@"page": @1}
                          completion:^(id response, NSError *error) {
    if (error) {
        NSLog(@"Error: %@", error.localizedDescription);
        return;
    }

    NSArray *users = response[@"users"];
    NSLog(@"Fetched %lu users", (unsigned long)users.count);
}];
```

**After (Swift - callback style):**
```swift
class NetworkManager {
    static let shared = NetworkManager()

    private init() {}

    func get(
        _ path: String,
        parameters: [String: Any] = [:],
        completion: @escaping (Result<Any, Error>) -> Void
    ) {
        guard let url = URL(string: path) else {
            completion(.failure(NetworkError.invalidURL))
            return
        }

        let task = URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                DispatchQueue.main.async {
                    completion(.failure(error))
                }
                return
            }

            guard let data = data else {
                DispatchQueue.main.async {
                    completion(.failure(NetworkError.noData))
                }
                return
            }

            do {
                let json = try JSONSerialization.jsonObject(with: data)
                DispatchQueue.main.async {
                    completion(.success(json))
                }
            } catch {
                DispatchQueue.main.async {
                    completion(.failure(error))
                }
            }
        }

        task.resume()
    }
}

enum NetworkError: Error {
    case invalidURL
    case noData
}

// Usage (callback style)
NetworkManager.shared.get("https://api.example.com/users", parameters: ["page": 1]) { result in
    switch result {
    case .success(let response):
        if let dict = response as? [String: Any],
           let users = dict["users"] as? [[String: Any]] {
            print("Fetched \(users.count) users")
        }
    case .failure(let error):
        print("Error: \(error.localizedDescription)")
    }
}
```

**After (Swift - modern async/await):**
```swift
class NetworkManager {
    static let shared = NetworkManager()

    private init() {}

    func get(_ path: String, parameters: [String: Any] = [:]) async throws -> Any {
        guard let url = URL(string: path) else {
            throw NetworkError.invalidURL
        }

        let (data, _) = try await URLSession.shared.data(from: url)
        return try JSONSerialization.jsonObject(with: data)
    }

    // Type-safe version with Codable
    func get<T: Decodable>(_ path: String, parameters: [String: Any] = [:]) async throws -> T {
        guard let url = URL(string: path) else {
            throw NetworkError.invalidURL
        }

        let (data, _) = try await URLSession.shared.data(from: url)
        return try JSONDecoder().decode(T.self, from: data)
    }
}

// Model
struct UsersResponse: Codable {
    let users: [User]
}

struct User: Codable {
    let id: Int
    let name: String
    let email: String
}

// Usage (async/await)
Task {
    do {
        let response: UsersResponse = try await NetworkManager.shared.get(
            "https://api.example.com/users",
            parameters: ["page": 1]
        )
        print("Fetched \(response.users.count) users")
    } catch {
        print("Error: \(error.localizedDescription)")
    }
}
```

**Why this translation:**
- Singleton: `static let` simpler than dispatch_once
- `Result<T, E>` more type-safe than separate parameters
- Modern Swift: async/await preferred over callbacks
- Codable provides type-safe JSON parsing
- Error handling: `throws` instead of error parameters
- Generic version with Codable removes need for casting

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `lang-objc-dev` - Objective-C development patterns
- `lang-swift-dev` - Swift development patterns

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - GCD, async/await, actors across languages
- `patterns-serialization-dev` - JSON, Codable, NSCoding across languages
- `patterns-metaprogramming-dev` - Runtime, reflection, property wrappers

Related conversion skills:
- `convert-swift-objc` - Reverse conversion (Swift → Objective-C)
