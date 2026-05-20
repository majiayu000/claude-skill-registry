---
name: lang-carbon-dev
description: Foundational Carbon patterns covering memory safety, modern syntax, C++ interop, and Carbon idioms. Use when writing Carbon code or migrating from C++. This is the entry point for Carbon development.
---

# Carbon Development Skill

## Overview

Carbon is an experimental successor language to C++, designed by Google to address modern development needs while maintaining seamless bidirectional interoperability with existing C++ codebases. Carbon aims to provide memory safety, modern syntax, and better developer ergonomics while allowing incremental migration from C++.

**Key Characteristics:**
- Memory safety with compile-time guarantees (following Rust's direction)
- Seamless C++ interoperability without runtime overhead
- Modern generics system with both checked and template generics
- Pattern matching for control flow
- Explicit, lightweight error handling
- Designed for large-scale adoption and migration

**Current Status (2025):**
- Experimental language under active development
- 0.1 milestone targeted for end of 2026 (ambitious goal)
- Major focus on C++ interop demo and memory safety design
- Built with Bazel, compiler evaluation phase

## Quick Reference

### Basic Syntax

```carbon
// Package declaration
package Sample api;

// Import statement
import Main;

// Function definition
fn Add(a: i32, b: i32) -> i32 {
    return a + b;
}

// Main entry point
fn Main() -> i32 {
    var result: i32 = Add(5, 10);
    Print("Result: {0}", result);
    return 0;
}
```

### Variable Declarations

```carbon
// Mutable variable
var x: i32 = 42;

// Immutable variable (const)
let y: i32 = 100;

// Type inference
var z: auto = 42;  // inferred as i32

// Uninitialized (must initialize before use)
var w: i32;
w = 50;
```

### Basic Types

```carbon
// Integer types
var a: i8 = 127;
var b: i16 = 32767;
var c: i32 = 2147483647;
var d: i64 = 9223372036854775807;

// Unsigned integers
var ua: u8 = 255;
var ub: u16 = 65535;
var uc: u32 = 4294967295;
var ud: u64 = 18446744073709551615;

// Floating point
var f: f32 = 3.14;
var g: f64 = 2.718281828;

// Boolean
var flag: bool = true;

// String
var message: String = "Hello, Carbon!";

// Type alias
alias MyInt = i32;
```

### Functions

```carbon
// Basic function
fn Greet(name: String) -> String {
    return "Hello, " + name;
}

// Multiple parameters
fn Calculate(x: i32, y: i32, operation: String) -> i32 {
    if (operation == "add") {
        return x + y;
    }
    return x - y;
}

// No return value (void)
fn PrintMessage(msg: String) {
    Print(msg);
}

// Early return
fn Divide(a: f64, b: f64) -> Optional(f64) {
    if (b == 0.0) {
        return Optional.None;
    }
    return Optional.Some(a / b);
}
```

### Control Flow

```carbon
// If-else
if (condition) {
    // do something
} else if (other_condition) {
    // do something else
} else {
    // default case
}

// While loop
var i: i32 = 0;
while (i < 10) {
    Print("{0}", i);
    i = i + 1;
}

// For loop
for (var j: i32 = 0; j < 10; j = j + 1) {
    Print("{0}", j);
}

// Break and continue
while (true) {
    if (should_exit) {
        break;
    }
    if (should_skip) {
        continue;
    }
    // normal iteration
}
```

### Pattern Matching

```carbon
// Match statement (replaces switch)
match (value) {
    case 0 => {
        Print("Zero");
    }
    case 1 => {
        Print("One");
    }
    case 2 | 3 | 4 => {
        Print("Two, three, or four");
    }
    default => {
        Print("Something else");
    }
}

// Match with patterns
fn Classify(x: i32) -> String {
    return match (x) {
        case 0 => "zero",
        case 1 => "one",
        case n if n < 0 => "negative",
        case n if n > 0 and n < 10 => "small positive",
        default => "large positive",
    };
}

// Destructuring in match
match (result) {
    case Optional.Some(value) => {
        Print("Got value: {0}", value);
    }
    case Optional.None => {
        Print("No value");
    }
}
```

## Core Concepts

### Memory Safety

Carbon's memory safety strategy follows Rust's direction, using the type system for compile-time guarantees without runtime overhead.

**Safety Categories:**

1. **Spatial Memory Safety:** Protects against out-of-bounds access
   - Array boundary checks
   - Invalid pointer dereferencing

2. **Temporal Memory Safety:** Protects against use-after-free
   - Heap use-after-free
   - Stack use-after-return

**Build Modes:**

```carbon
// Debug build: immediate runtime detection
var array: [i32; 5] = [1, 2, 3, 4, 5];
var index: i32 = 10;
// In debug mode: caught immediately
var value: i32 = array[index];

// Performance build: undefined behavior if violated
// Optimizer assumes no overflow/out-of-bounds
var x: i32 = 2147483647;
x = x + 1;  // UB in performance mode

// Hardened build: safe but potentially incorrect
// Overflow won't crash but may produce wrong result
// Or program will abort safely
```

**Uninitialized State Tracking:**

```carbon
// Carbon tracks initialization better than C++
var x: i32;
// Print(x);  // Error: use of uninitialized variable

x = 42;
Print(x);  // OK: initialized before use

// Conditional initialization
var y: i32;
if (condition) {
    y = 10;
} else {
    y = 20;
}
// OK: y is initialized in all paths
Print(y);
```

**Dynamic Bounds Checking:**

```carbon
// APIs designed for safety
fn SafeAccess(array: [i32], index: i32) -> Optional(i32) {
    if (index < 0 or index >= array.size()) {
        return Optional.None;
    }
    return Optional.Some(array[index]);
}

// Usage
match (SafeAccess(my_array, idx)) {
    case Optional.Some(value) => {
        Print("Value: {0}", value);
    }
    case Optional.None => {
        Print("Index out of bounds");
    }
}
```

### C++ Interoperability

Carbon's primary design goal is seamless, bidirectional interoperability with C++.

**Philosophy:**
- Zero runtime overhead for interop calls
- No custom bridge code for simple types/functions
- Call Carbon from C++ and vice versa
- Works even with non-Carbon-aware C++ toolchains
- Incremental migration support

**Calling C++ from Carbon:**

```carbon
// Import C++ header
import Cpp library "mylib.h";

fn UseCppFunction() {
    // Call C++ function directly
    var result: i32 = Cpp.MyCppFunction(42);

    // Use C++ class
    var obj: Cpp.MyCppClass = Cpp.MyCppClass();
    obj.Method();
}

// C++ types are accessible
fn ProcessVector(vec: Cpp.std.vector(i32)) {
    for (var i: i32 = 0; i < vec.size(); i = i + 1) {
        Print("{0}", vec[i]);
    }
}
```

**Calling Carbon from C++:**

```cpp
// C++ code
#include "carbon_module.h"

int main() {
    // Call Carbon function from C++
    int result = Carbon::MyFunction(10, 20);

    // Use Carbon class
    Carbon::MyClass obj;
    obj.DoSomething();

    return 0;
}
```

**Migration Strategy:**

```carbon
// Phase 1: Minimal migration
// Auto-migrate C++ to interop-focused Carbon dialect
// Maintains C++ semantics, minimal code changes

// Phase 2: Incremental refactoring
// Gradually adopt Carbon idioms
// Introduce memory safety features
// Modernize APIs and patterns

// Example: C++ -> Carbon migration
// C++ original:
// void processData(std::vector<int>& data) {
//     for (auto& item : data) {
//         item *= 2;
//     }
// }

// Phase 1: Direct migration
fn ProcessData(data: Cpp.std.vector(i32)*) {
    var i: i32 = 0;
    while (i < data->size()) {
        (*data)[i] = (*data)[i] * 2;
        i = i + 1;
    }
}

// Phase 2: Carbon idioms
fn ProcessData(data: [i32]*) {
    for (var i: i32 = 0; i < data.size(); i = i + 1) {
        data[i] = data[i] * 2;
    }
}
```

**Safety with Interop:**

```carbon
// Carbon code has safety guarantees
fn SafeCarbonFunction(x: i32) -> i32 {
    // Bounds checked, initialization verified
    var array: [i32; 5] = [1, 2, 3, 4, 5];
    return array[x % 5];  // Safe modulo operation
}

// C++ interop accepts higher risk
fn CallUnsafeCpp() {
    // C++ doesn't have same safety mechanisms
    // Carbon calling C++ accepts this risk
    unsafe {
        Cpp.LegacyFunction();
    }
}

// Mitigation strategies
fn SafeInterop(data: Cpp.std.vector(i32)) -> Optional(i32) {
    // Add runtime checks around C++ data
    if (data.empty()) {
        return Optional.None;
    }
    return Optional.Some(data[0]);
}
```

### Generics System

Carbon provides both checked generics and template generics for different use cases.

**Checked Generics:**

```carbon
// Basic generic function
fn GenericExample[T:! Type](x: T) -> T {
    return x;
}

// Usage with type inference
fn Main() -> i32 {
    var int_val: i32 = GenericExample(42);
    var str_val: String = GenericExample("hello");
    return 0;
}

// Generic with interface constraint
interface Comparable {
    fn Compare[self: Self](other: Self) -> i32;
}

fn Max[T:! Comparable](a: T, b: T) -> T {
    if (a.Compare(b) > 0) {
        return a;
    }
    return b;
}
```

**Interfaces:**

```carbon
// Define an interface
interface Vector {
    fn Add[self: Self](b: Self) -> Self;
    fn Scale[self: Self](v: f64) -> Self;
}

// Implement interface for a type
class Vec2 {
    var x: f64;
    var y: f64;
}

impl Vec2 as Vector {
    fn Add[self: Self](b: Self) -> Self {
        return Vec2{.x = self.x + b.x, .y = self.y + b.y};
    }

    fn Scale[self: Self](v: f64) -> Self {
        return Vec2{.x = self.x * v, .y = self.y * v};
    }
}

// Generic function using interface
fn Transform[T:! Vector](vec: T, factor: f64) -> T {
    return vec.Scale(factor);
}
```

**Template Generics:**

```carbon
// Template generic (C++ style)
// Not checked at definition, checked at instantiation
fn TemplateFunc[template T:! Type](x: T) -> T {
    // Can use any operations on T
    // Errors shown at instantiation site
    return x * 2 + 1;
}

// Useful for C++ interop
fn ProcessCppContainer[template T:! Type](container: T) {
    // Works with any C++ container-like type
    for (var i: i32 = 0; i < container.size(); i = i + 1) {
        Print("{0}", container[i]);
    }
}
```

**Advantages of Checked Generics:**

```carbon
// Checked generics catch errors at definition
fn BrokenGeneric[T:! Type](x: T) -> T {
    // Error: Type doesn't have '+' operator
    // return x + x;  // Caught immediately
}

// Fix: add constraint
interface Addable {
    fn Add[self: Self](other: Self) -> Self;
}

fn WorkingGeneric[T:! Addable](x: T) -> T {
    return x.Add(x);  // OK: constraint guarantees Add exists
}

// Better error messages
fn UseGeneric() {
    var s: String = "hello";
    // Error: String doesn't implement Addable
    // var result: String = WorkingGeneric(s);
    // Clear message about missing interface
}
```

**Generic Types:**

```carbon
// Generic class
class Container[T:! Type] {
    var data: [T];

    fn Add[self: Self*](item: T) {
        self->data.push_back(item);
    }

    fn Get[self: Self](index: i32) -> Optional(T) {
        if (index < 0 or index >= self.data.size()) {
            return Optional.None;
        }
        return Optional.Some(self.data[index]);
    }
}

// Usage
fn Main() -> i32 {
    var int_container: Container(i32) = Container(i32)();
    int_container.Add(10);
    int_container.Add(20);

    match (int_container.Get(0)) {
        case Optional.Some(value) => {
            Print("First: {0}", value);
        }
        case Optional.None => {
            Print("Empty");
        }
    }

    return 0;
}
```

### Type System

**Primitive Types:**

```carbon
// Sized integers (guaranteed size)
i8, i16, i32, i64      // Signed
u8, u16, u32, u64      // Unsigned

// Floating point
f32, f64

// Boolean
bool

// String
String

// Pointer types
T*                     // Mutable pointer
const T*               // Const pointer

// Array types
[T; N]                 // Fixed-size array
[T]                    // Dynamic array (slice)
```

**Type Aliases:**

```carbon
// Simple alias
alias IntPtr = i32*;
alias Callback = fn(i32) -> i32;

// Generic alias
alias Result[T:! Type, E:! Type] =
    variant { Ok(T), Err(E) };

// Usage
fn Divide(a: i32, b: i32) -> Result(i32, String) {
    if (b == 0) {
        return Result.Err("Division by zero");
    }
    return Result.Ok(a / b);
}
```

**Sum Types (Variants):**

```carbon
// Define a sum type
variant Option[T:! Type] {
    Some(T),
    None
}

// Usage
fn Find(array: [i32], target: i32) -> Option(i32) {
    for (var i: i32 = 0; i < array.size(); i = i + 1) {
        if (array[i] == target) {
            return Option.Some(i);
        }
    }
    return Option.None;
}

// Pattern matching on variants
fn UseOption(opt: Option(i32)) {
    match (opt) {
        case Option.Some(value) => {
            Print("Found: {0}", value);
        }
        case Option.None => {
            Print("Not found");
        }
    }
}
```

**Classes:**

```carbon
// Class definition
class Point {
    var x: f64;
    var y: f64;

    // Constructor
    fn Create(x_val: f64, y_val: f64) -> Self {
        return Point{.x = x_val, .y = y_val};
    }

    // Method
    fn Distance[self: Self](other: Self) -> f64 {
        var dx: f64 = self.x - other.x;
        var dy: f64 = self.y - other.y;
        return Math.Sqrt(dx * dx + dy * dy);
    }

    // Mutable method
    fn Move[self: Self*](dx: f64, dy: f64) {
        self->x = self->x + dx;
        self->y = self->y + dy;
    }
}

// Usage
fn Main() -> i32 {
    var p1: Point = Point.Create(0.0, 0.0);
    var p2: Point = Point.Create(3.0, 4.0);

    var dist: f64 = p1.Distance(p2);
    Print("Distance: {0}", dist);

    p1.Move(1.0, 1.0);

    return 0;
}
```

**Inheritance and Composition:**

```carbon
// Base class
class Shape {
    fn Area[self: Self] -> f64;
}

// Derived class
class Circle {
    var radius: f64;
    base: Shape;
}

impl Circle as Shape {
    fn Area[self: Self] -> f64 {
        return 3.14159 * self.radius * self.radius;
    }
}

// Composition
class Rectangle {
    var width: f64;
    var height: f64;
}

class ColoredRectangle {
    var rect: Rectangle;
    var color: String;

    fn Area[self: Self] -> f64 {
        return self.rect.width * self.rect.height;
    }
}
```

### Error Handling

Carbon uses explicit, statically-typed error handling without exceptions.

**Basic Error Handling:**

```carbon
// Return sum type for errors
variant Result[T:! Type, E:! Type] {
    Ok(T),
    Err(E)
}

// Function that can fail
fn ParseInt(s: String) -> Result(i32, String) {
    if (s.IsEmpty()) {
        return Result.Err("Empty string");
    }
    // ... parsing logic
    return Result.Ok(42);
}

// Handle errors
fn UseParseInt(input: String) {
    match (ParseInt(input)) {
        case Result.Ok(value) => {
            Print("Parsed: {0}", value);
        }
        case Result.Err(error) => {
            Print("Error: {0}", error);
        }
    }
}
```

**Optional Type:**

```carbon
// Built-in optional type
variant Optional[T:! Type] {
    Some(T),
    None
}

// Function returning optional
fn GetConfig(key: String) -> Optional(String) {
    if (ConfigExists(key)) {
        return Optional.Some(GetConfigValue(key));
    }
    return Optional.None;
}

// Unwrap with default
fn GetOrDefault(opt: Optional(i32), default: i32) -> i32 {
    return match (opt) {
        case Optional.Some(value) => value,
        case Optional.None => default,
    };
}
```

**Error Propagation:**

```carbon
// Error propagation operator (like Rust's ?)
// Expected in future Carbon versions
fn ProcessData() -> Result(i32, String) {
    var data: String = ReadFile("data.txt")?;
    var value: i32 = ParseInt(data)?;
    return Result.Ok(value * 2);
}

// Manual propagation (current approach)
fn ProcessDataManual() -> Result(i32, String) {
    var file_result: Result(String, String) = ReadFile("data.txt");
    match (file_result) {
        case Result.Err(e) => { return Result.Err(e); }
        case Result.Ok(data) => {
            var parse_result: Result(i32, String) = ParseInt(data);
            match (parse_result) {
                case Result.Err(e) => { return Result.Err(e); }
                case Result.Ok(value) => {
                    return Result.Ok(value * 2);
                }
            }
        }
    }
}
```

**Error Context:**

```carbon
// Enriching errors with context
variant Error {
    IoError(String),
    ParseError(String, i32),  // message, line number
    ValidationError(String)
}

fn ReadConfig(path: String) -> Result(Config, Error) {
    var content_result: Result(String, String) = ReadFile(path);
    var content: String = match (content_result) {
        case Result.Err(e) => {
            return Result.Err(Error.IoError(
                "Failed to read " + path + ": " + e
            ));
        }
        case Result.Ok(c) => c,
    };

    // Continue processing...
    return Result.Ok(config);
}
```

**No Exceptions:**

```carbon
// Carbon does NOT have exceptions
// No try-catch blocks
// No throw statements
// Errors are explicit in function signatures

// This forces explicit error handling
fn RiskyOperation() -> Result(i32, String) {
    // Must return Result, can't throw
    if (something_wrong) {
        return Result.Err("Something went wrong");
    }
    return Result.Ok(42);
}

// Caller must handle errors
fn Caller() {
    var result: Result(i32, String) = RiskyOperation();
    // Can't ignore the error - must handle it
    match (result) {
        case Result.Ok(value) => { /* use value */ }
        case Result.Err(e) => { /* handle error */ }
    }
}
```

### Build System

**Bazel-Based Build:**

```python
# BUILD file for Carbon project
load("@rules_carbon//carbon:defs.bzl", "carbon_library", "carbon_binary")

carbon_library(
    name = "mylib",
    srcs = ["mylib.carbon"],
    deps = [
        "//other:library",
    ],
)

carbon_binary(
    name = "myapp",
    srcs = ["main.carbon"],
    deps = [
        ":mylib",
    ],
)
```

**Compiler Usage:**

```bash
# Compile Carbon source
carbon compile main.carbon

# Verbose output
carbon -v compile main.carbon

# Specify output
carbon compile main.carbon -o output.o

# Check syntax only
carbon check main.carbon

# Run different compilation phases
carbon compile --phase=parse main.carbon
carbon compile --phase=check main.carbon
carbon compile --phase=lower main.carbon
```

**Project Structure:**

```
my_carbon_project/
├── BUILD                 # Bazel build file
├── WORKSPACE            # Bazel workspace
├── src/
│   ├── main.carbon      # Main entry point
│   ├── lib.carbon       # Library code
│   └── utils.carbon     # Utilities
├── tests/
│   ├── BUILD
│   └── test_lib.carbon  # Tests
└── api/
    └── public.carbon    # Public API
```

**Package System:**

```carbon
// Package declaration
package MyProject api;

// Import from same package
import .Utils;

// Import from other package
import OtherProject;

// Import specific symbols
import OtherProject.{Function, Type};

// Use imported code
fn Main() -> i32 {
    Utils.Helper();
    OtherProject.Function();
    return 0;
}
```

## Common Patterns

### Resource Management

```carbon
// RAII-style resource management
class File {
    var handle: FileHandle;

    fn Open(path: String) -> Result(Self, String) {
        var handle_result: Result(FileHandle, String) =
            OpenFileHandle(path);
        match (handle_result) {
            case Result.Err(e) => {
                return Result.Err(e);
            }
            case Result.Ok(h) => {
                return Result.Ok(File{.handle = h});
            }
        }
    }

    fn Read[self: Self*](buffer: [u8]*) -> Result(i32, String) {
        return ReadFromHandle(self->handle, buffer);
    }

    // Destructor
    destructor [self: Self*] {
        CloseFileHandle(self->handle);
    }
}

// Usage - automatic cleanup
fn ProcessFile(path: String) -> Result(i32, String) {
    var file_result: Result(File, String) = File.Open(path);
    match (file_result) {
        case Result.Err(e) => {
            return Result.Err(e);
        }
        case Result.Ok(file) => {
            var buffer: [u8; 1024] = [0; 1024];
            var read_result: Result(i32, String) =
                file.Read(&buffer);
            // file destroyed automatically here
            return read_result;
        }
    }
}
```

### Builder Pattern

```carbon
class ConfigBuilder {
    var host: Optional(String) = Optional.None;
    var port: Optional(i32) = Optional.None;
    var timeout: Optional(i32) = Optional.None;

    fn New() -> Self {
        return ConfigBuilder{};
    }

    fn SetHost[self: Self*](host: String) -> Self* {
        self->host = Optional.Some(host);
        return self;
    }

    fn SetPort[self: Self*](port: i32) -> Self* {
        self->port = Optional.Some(port);
        return self;
    }

    fn SetTimeout[self: Self*](timeout: i32) -> Self* {
        self->timeout = Optional.Some(timeout);
        return self;
    }

    fn Build[self: Self] -> Result(Config, String) {
        var h: String = match (self.host) {
            case Optional.Some(v) => v,
            case Optional.None => {
                return Result.Err("Host is required");
            }
        };

        var p: i32 = GetOrDefault(self.port, 8080);
        var t: i32 = GetOrDefault(self.timeout, 30);

        return Result.Ok(Config{
            .host = h,
            .port = p,
            .timeout = t
        });
    }
}

// Usage
fn CreateConfig() -> Result(Config, String) {
    var builder: ConfigBuilder = ConfigBuilder.New();
    return builder
        .SetHost("localhost")
        .SetPort(3000)
        .SetTimeout(60)
        .Build();
}
```

### Iterator Pattern

```carbon
interface Iterator {
    fn Next[self: Self*] -> Optional(i32);
}

class RangeIterator {
    var current: i32;
    var end: i32;
}

impl RangeIterator as Iterator {
    fn Next[self: Self*] -> Optional(i32) {
        if (self->current >= self->end) {
            return Optional.None;
        }
        var value: i32 = self->current;
        self->current = self->current + 1;
        return Optional.Some(value);
    }
}

fn Range(start: i32, end: i32) -> RangeIterator {
    return RangeIterator{.current = start, .end = end};
}

// Usage
fn Main() -> i32 {
    var iter: RangeIterator = Range(0, 10);
    while (true) {
        match (iter.Next()) {
            case Optional.Some(value) => {
                Print("{0}", value);
            }
            case Optional.None => {
                break;
            }
        }
    }
    return 0;
}
```

### Visitor Pattern

```carbon
// Define visitor interface
interface NodeVisitor {
    fn VisitNumber[self: Self*](value: i32);
    fn VisitString[self: Self*](value: String);
}

// Define visitable nodes
variant Node {
    Number(i32),
    String(String)
}

fn AcceptVisitor[V:! NodeVisitor](node: Node, visitor: V*) {
    match (node) {
        case Node.Number(value) => {
            visitor->VisitNumber(value);
        }
        case Node.String(value) => {
            visitor->VisitString(value);
        }
    }
}

// Implement concrete visitor
class PrintVisitor {}

impl PrintVisitor as NodeVisitor {
    fn VisitNumber[self: Self*](value: i32) {
        Print("Number: {0}", value);
    }

    fn VisitString[self: Self*](value: String) {
        Print("String: {0}", value);
    }
}

// Usage
fn Main() -> i32 {
    var nodes: [Node] = [
        Node.Number(42),
        Node.String("hello"),
        Node.Number(100)
    ];

    var visitor: PrintVisitor = PrintVisitor{};
    for (var i: i32 = 0; i < nodes.size(); i = i + 1) {
        AcceptVisitor(nodes[i], &visitor);
    }

    return 0;
}
```

### Factory Pattern

```carbon
interface Shape {
    fn Area[self: Self] -> f64;
    fn Perimeter[self: Self] -> f64;
}

class Circle {
    var radius: f64;
}

impl Circle as Shape {
    fn Area[self: Self] -> f64 {
        return 3.14159 * self.radius * self.radius;
    }

    fn Perimeter[self: Self] -> f64 {
        return 2.0 * 3.14159 * self.radius;
    }
}

class Rectangle {
    var width: f64;
    var height: f64;
}

impl Rectangle as Shape {
    fn Area[self: Self] -> f64 {
        return self.width * self.height;
    }

    fn Perimeter[self: Self] -> f64 {
        return 2.0 * (self.width + self.height);
    }
}

// Factory function
fn CreateShape(shape_type: String, params: [f64])
    -> Optional(variant {Circle, Rectangle})
{
    if (shape_type == "circle" and params.size() >= 1) {
        return Optional.Some(Circle{.radius = params[0]});
    } else if (shape_type == "rectangle" and params.size() >= 2) {
        return Optional.Some(Rectangle{
            .width = params[0],
            .height = params[1]
        });
    }
    return Optional.None;
}
```

## Migration from C++

### Common C++ to Carbon Translations

**Headers and Includes:**

```cpp
// C++
#include <vector>
#include <string>
#include "myheader.h"
```

```carbon
// Carbon
import Cpp library "vector";
import Cpp library "string";
import .MyModule;
```

**Class Definition:**

```cpp
// C++
class MyClass {
public:
    MyClass(int x, int y) : x_(x), y_(y) {}

    int getX() const { return x_; }
    void setX(int x) { x_ = x; }

    int compute() const {
        return x_ * y_;
    }

private:
    int x_;
    int y_;
};
```

```carbon
// Carbon
class MyClass {
    var x: i32;
    var y: i32;

    fn Create(x: i32, y: i32) -> Self {
        return MyClass{.x = x, .y = y};
    }

    fn GetX[self: Self] -> i32 {
        return self.x;
    }

    fn SetX[self: Self*](x: i32) {
        self->x = x;
    }

    fn Compute[self: Self] -> i32 {
        return self.x * self.y;
    }
}
```

**Templates to Generics:**

```cpp
// C++
template<typename T>
T max(T a, T b) {
    return (a > b) ? a : b;
}
```

```carbon
// Carbon - checked generic
interface Comparable {
    fn Compare[self: Self](other: Self) -> i32;
}

fn Max[T:! Comparable](a: T, b: T) -> T {
    if (a.Compare(b) > 0) {
        return a;
    }
    return b;
}

// Or template generic for C++ compatibility
fn MaxTemplate[template T:! Type](a: T, b: T) -> T {
    if (a > b) {
        return a;
    }
    return b;
}
```

**Smart Pointers:**

```cpp
// C++
std::unique_ptr<MyClass> obj =
    std::make_unique<MyClass>(10, 20);
std::shared_ptr<MyClass> shared =
    std::make_shared<MyClass>(10, 20);
```

```carbon
// Carbon - ownership via move semantics
var obj: MyClass = MyClass.Create(10, 20);
var moved_obj: MyClass = obj;  // Move ownership

// Reference counting (if needed)
var shared: Shared(MyClass) = Shared.New(MyClass.Create(10, 20));
```

**Exceptions to Results:**

```cpp
// C++
int divide(int a, int b) {
    if (b == 0) {
        throw std::runtime_error("Division by zero");
    }
    return a / b;
}

try {
    int result = divide(10, 0);
} catch (const std::exception& e) {
    std::cerr << "Error: " << e.what() << std::endl;
}
```

```carbon
// Carbon
fn Divide(a: i32, b: i32) -> Result(i32, String) {
    if (b == 0) {
        return Result.Err("Division by zero");
    }
    return Result.Ok(a / b);
}

match (Divide(10, 0)) {
    case Result.Ok(value) => {
        Print("Result: {0}", value);
    }
    case Result.Err(error) => {
        Print("Error: {0}", error);
    }
}
```

**Namespaces to Packages:**

```cpp
// C++
namespace MyNamespace {
namespace Utils {
    void helper() { }
}
}

MyNamespace::Utils::helper();
```

```carbon
// Carbon
package MyProject.Utils api;

fn Helper() { }

// Usage
import MyProject.Utils;
Utils.Helper();
```

### Migration Checklist

**Phase 1: Initial Setup**
- [ ] Set up Carbon toolchain and build system (Bazel)
- [ ] Identify C++ libraries to keep vs migrate
- [ ] Create interop layer for C++ dependencies
- [ ] Set up testing infrastructure

**Phase 2: Incremental Migration**
- [ ] Start with leaf modules (no dependencies)
- [ ] Migrate simple utility functions first
- [ ] Convert headers to Carbon packages
- [ ] Update build files to include Carbon sources
- [ ] Ensure tests pass with mixed C++/Carbon codebase

**Phase 3: Refactoring**
- [ ] Replace raw pointers with Carbon ownership
- [ ] Convert exceptions to Result types
- [ ] Adopt Carbon idioms (match, generics)
- [ ] Add memory safety features
- [ ] Improve error handling

**Phase 4: Optimization**
- [ ] Profile mixed codebase
- [ ] Identify performance bottlenecks
- [ ] Optimize hot paths
- [ ] Reduce C++ interop overhead where possible

## Carbon Idioms

### Prefer Match Over If-Else Chains

```carbon
// Less idiomatic
fn Classify(x: i32) -> String {
    if (x == 0) {
        return "zero";
    } else if (x > 0 and x < 10) {
        return "small";
    } else if (x >= 10) {
        return "large";
    } else {
        return "negative";
    }
}

// More idiomatic
fn Classify(x: i32) -> String {
    return match (x) {
        case 0 => "zero",
        case n if n > 0 and n < 10 => "small",
        case n if n >= 10 => "large",
        default => "negative",
    };
}
```

### Use Type System for Validation

```carbon
// Less idiomatic - runtime validation everywhere
fn ProcessAge(age: i32) {
    if (age < 0 or age > 150) {
        Print("Invalid age");
        return;
    }
    // use age
}

// More idiomatic - validated type
class Age {
    var value: i32;

    fn Create(v: i32) -> Result(Self, String) {
        if (v < 0 or v > 150) {
            return Result.Err("Invalid age");
        }
        return Result.Ok(Age{.value = v});
    }
}

fn ProcessAge(age: Age) {
    // age is guaranteed valid
    Print("Age: {0}", age.value);
}
```

### Make Invalid States Unrepresentable

```carbon
// Less idiomatic - multiple booleans
class Connection {
    var is_connected: bool;
    var is_authenticated: bool;
    var is_encrypted: bool;
    // Can be in invalid states!
}

// More idiomatic - state machine with variants
variant ConnectionState {
    Disconnected,
    Connected,
    Authenticated,
    Encrypted
}

class Connection {
    var state: ConnectionState;

    fn Connect[self: Self*] -> Result((), String) {
        match (self->state) {
            case ConnectionState.Disconnected => {
                self->state = ConnectionState.Connected;
                return Result.Ok(());
            }
            default => {
                return Result.Err("Already connected");
            }
        }
    }
}
```

### Prefer Immutability

```carbon
// Less idiomatic
fn ProcessData(data: [i32]*) {
    for (var i: i32 = 0; i < data->size(); i = i + 1) {
        data[i] = data[i] * 2;  // Mutation
    }
}

// More idiomatic
fn ProcessData(data: [i32]) -> [i32] {
    var result: [i32] = [];
    for (var i: i32 = 0; i < data.size(); i = i + 1) {
        result.push_back(data[i] * 2);
    }
    return result;
}
```

### Use Interfaces for Abstraction

```carbon
// Less idiomatic - concrete types everywhere
fn PrintCircle(c: Circle) {
    Print("Area: {0}", c.Area());
}

fn PrintRectangle(r: Rectangle) {
    Print("Area: {0}", r.Area());
}

// More idiomatic - interface abstraction
interface Shape {
    fn Area[self: Self] -> f64;
}

fn PrintShape[T:! Shape](s: T) {
    Print("Area: {0}", s.Area());
}
```

## Troubleshooting

### Compilation Errors

**Uninitialized Variable:**
```carbon
// Error
var x: i32;
Print(x);  // Error: use of uninitialized variable

// Fix
var x: i32 = 0;
Print(x);
```

**Type Mismatch:**
```carbon
// Error
var x: i32 = 42;
var y: f64 = x;  // Error: type mismatch

// Fix
var x: i32 = 42;
var y: f64 = Convert.ToF64(x);
```

**Missing Interface Implementation:**
```carbon
// Error
fn UseComparable[T:! Comparable](x: T) { }

class MyType { }

fn Main() -> i32 {
    var obj: MyType = MyType{};
    UseComparable(obj);  // Error: MyType doesn't implement Comparable
    return 0;
}

// Fix
impl MyType as Comparable {
    fn Compare[self: Self](other: Self) -> i32 {
        // Implementation
        return 0;
    }
}
```

### C++ Interop Issues

**Header Not Found:**
```carbon
// Error
import Cpp library "myheader.h";  // Error: file not found

// Fix - check include paths in BUILD file
carbon_library(
    name = "mylib",
    srcs = ["mylib.carbon"],
    copts = ["-I/path/to/headers"],
)
```

**Type Incompatibility:**
```carbon
// Error - C++ type not directly usable
fn UseCppVector(vec: Cpp.std.vector(i32)) {
    vec[0] = 42;  // Might fail
}

// Fix - use C++ API properly
fn UseCppVector(vec: Cpp.std.vector(i32)*) {
    vec->at(0) = 42;  // Use C++ methods
}
```

**Calling Convention Mismatch:**
```carbon
// Error - wrong calling convention for C++ function
fn CallCppFunction() {
    Cpp.MyFunction();  // Might fail if signature wrong
}

// Fix - match C++ signature exactly
import Cpp library "mylib.h";

fn CallCppFunction() {
    var result: i32 = Cpp.MyFunction(42, "hello");
}
```

### Build System Issues

**Missing Dependency:**
```python
# Error in BUILD file
carbon_binary(
    name = "myapp",
    srcs = ["main.carbon"],
    # Missing dependency
)

# Fix
carbon_binary(
    name = "myapp",
    srcs = ["main.carbon"],
    deps = [
        ":mylib",
        "//other:dependency",
    ],
)
```

**Circular Dependency:**
```python
# Error - circular deps
carbon_library(
    name = "a",
    srcs = ["a.carbon"],
    deps = [":b"],
)

carbon_library(
    name = "b",
    srcs = ["b.carbon"],
    deps = [":a"],  # Circular!
)

# Fix - refactor to break cycle
carbon_library(
    name = "common",
    srcs = ["common.carbon"],
)

carbon_library(
    name = "a",
    srcs = ["a.carbon"],
    deps = [":common"],
)

carbon_library(
    name = "b",
    srcs = ["b.carbon"],
    deps = [":common"],
)
```

### Memory Safety Issues

**Use After Move:**
```carbon
// Error
var x: MyClass = MyClass.Create();
var y: MyClass = x;  // x moved to y
x.Method();  // Error: use after move

// Fix - clone or use references
var x: MyClass = MyClass.Create();
var y: MyClass* = &x;  // Borrow, don't move
x.Method();  // OK
```

**Out of Bounds Access:**
```carbon
// Error in debug build
var array: [i32; 5] = [1, 2, 3, 4, 5];
var value: i32 = array[10];  // Panic in debug mode

// Fix - use safe access
fn SafeGet(array: [i32], index: i32) -> Optional(i32) {
    if (index >= 0 and index < array.size()) {
        return Optional.Some(array[index]);
    }
    return Optional.None;
}
```

### Generic Type Issues

**Constraint Not Satisfied:**
```carbon
// Error
fn RequiresComparable[T:! Comparable](x: T) { }

fn Main() -> i32 {
    var s: String = "hello";
    RequiresComparable(s);  // Error: String doesn't implement Comparable
    return 0;
}

// Fix - implement interface
impl String as Comparable {
    fn Compare[self: Self](other: Self) -> i32 {
        // Implementation
        return 0;
    }
}
```

**Type Inference Failure:**
```carbon
// Error - can't infer type
var x: auto = SomeGenericFunction();  // Ambiguous

// Fix - specify type explicitly
var x: i32 = SomeGenericFunction();
// Or provide type parameter
var x: auto = SomeGenericFunction[i32]();
```

## Best Practices

1. **Use checked generics by default**, template generics only for C++ interop
2. **Make error handling explicit** with Result/Optional types
3. **Prefer immutability** unless mutation is clearly needed
4. **Use pattern matching** instead of if-else chains
5. **Leverage the type system** to prevent invalid states
6. **Follow RAII principles** for resource management
7. **Start with C++ interop**, gradually refactor to Carbon idioms
8. **Test extensively** during migration from C++
9. **Use interfaces** to define contracts and enable polymorphism
10. **Document safety assumptions** especially around C++ interop

## Zero and Default Values

### Uninitialized Variables

```carbon
// Variables must be initialized before use
var x: i32;  // Declared but uninitialized
// Print(x);  // Error: use of uninitialized variable

x = 42;
Print(x);  // OK: now initialized

// Conditional initialization - all paths must initialize
var y: i32;
if (condition) {
    y = 10;
} else {
    y = 20;
}
Print(y);  // OK: initialized in all paths
```

### Default/Zero Values by Type

| Type | Zero Value | Initialization |
|------|------------|----------------|
| `i8, i16, i32, i64` | `0` | `var x: i32 = 0;` |
| `u8, u16, u32, u64` | `0` | `var x: u32 = 0;` |
| `f32, f64` | `0.0` | `var x: f64 = 0.0;` |
| `bool` | `false` | `var x: bool = false;` |
| `String` | `""` | `var x: String = "";` |
| Array | Empty | `var x: [i32] = [];` |
| Optional | `None` | `Optional.None` |
| Pointer | null (unsafe) | Use Optional instead |

### Struct/Class Initialization

```carbon
class Config {
    var host: String;
    var port: i32;
    var debug: bool;
}

// All fields must be initialized
var config: Config = Config{
    .host = "localhost",
    .port = 8080,
    .debug = false
};

// Factory function for defaults
class Config {
    fn Default() -> Self {
        return Config{
            .host = "localhost",
            .port = 8080,
            .debug = false
        };
    }
}

var config: Config = Config.Default();
```

### Optional for Nullable Values

```carbon
// Carbon discourages null pointers
// Use Optional instead
fn FindUser(id: i32) -> Optional(User) {
    if (UserExists(id)) {
        return Optional.Some(GetUser(id));
    }
    return Optional.None;
}

// Handle optionals
fn GetUsername(id: i32) -> String {
    match (FindUser(id)) {
        case Optional.Some(user) => {
            return user.name;
        }
        case Optional.None => {
            return "Unknown";
        }
    }
}

// Default value pattern
fn GetOrDefault[T:! Type](opt: Optional(T), default: T) -> T {
    return match (opt) {
        case Optional.Some(value) => value,
        case Optional.None => default,
    };
}
```

---

## Concurrency

Carbon's concurrency model is still under active design. The current focus is on memory safety and C++ interop before finalizing concurrency features.

### Current Status (2025)

```carbon
// Note: Concurrency syntax is subject to change
// This represents expected patterns based on design documents

// Thread safety through ownership
// Carbon aims to prevent data races at compile time
// Similar to Rust's Send/Sync traits

class ThreadSafeCounter {
    var count: i32;

    fn Increment[self: Self*] {
        // Atomic or synchronized access (design pending)
        self->count = self->count + 1;
    }
}
```

### Expected Concurrency Patterns

```carbon
// Async/await (expected in future versions)
async fn FetchData(url: String) -> Result(Data, Error) {
    var response: Response = await Http.Get(url);
    return response.Body();
}

// Structured concurrency (expected)
fn ProcessConcurrently(items: [Item]) -> [Result] {
    return parallel for (item in items) {
        ProcessItem(item)
    };
}
```

### C++ Interop for Concurrency

```carbon
// For now, use C++ threading via interop
import Cpp library "thread";
import Cpp library "mutex";

fn UseCppThreading() {
    var mutex: Cpp.std.mutex = Cpp.std.mutex();

    // Lock guard pattern
    var lock: Cpp.std.lock_guard(Cpp.std.mutex) =
        Cpp.std.lock_guard(&mutex);

    // Critical section
    DoWork();
}

// Dispatch to thread pool
fn RunInBackground(task: fn()) {
    var thread: Cpp.std.thread = Cpp.std.thread(task);
    thread.detach();
}
```

### Safety Philosophy

```carbon
// Carbon's concurrency will emphasize:
// 1. Compile-time data race prevention
// 2. Ownership-based thread safety
// 3. Explicit sharing markers
// 4. Integration with memory safety model

// Expected patterns:
// - Values are "thread-local" by default
// - Explicit markers for shared state
// - Channels for communication (like Go/Rust)
// - Actor model support (planned)
```

See `patterns-concurrency-dev` for cross-language concurrency patterns.

---

## Metaprogramming

Carbon provides compile-time metaprogramming through generics and template generics, but does NOT support runtime reflection.

### Checked Generics

```carbon
// Checked generics with interfaces
interface Printable {
    fn Print[self: Self]();
}

fn PrintAll[T:! Printable](items: [T]) {
    for (var i: i32 = 0; i < items.size(); i = i + 1) {
        items[i].Print();
    }
}

// Errors caught at definition site
fn BrokenGeneric[T:! Type](x: T) -> T {
    // Error: Type doesn't guarantee '+' operator
    // return x + x;
}
```

### Template Generics

```carbon
// Template generics (like C++ templates)
// Unchecked at definition, checked at instantiation
fn TemplateAdd[template T:! Type](a: T, b: T) -> T {
    return a + b;  // Works if T has + operator
}

// Usage - errors at call site if T doesn't support +
var result: i32 = TemplateAdd(5, 10);      // OK
// var bad: String = TemplateAdd("a", "b"); // Error at this line
```

### Compile-Time Constants

```carbon
// Compile-time values
let PI: f64 = 3.14159265358979;
let MAX_SIZE: i32 = 1024;

// Generic with compile-time value
class FixedArray[T:! Type, let N:! i32] {
    var data: [T; N];

    fn Size[self: Self]() -> i32 {
        return N;  // Compile-time constant
    }
}

var arr: FixedArray(i32, 10) = ...;
```

### Interface-Based Polymorphism

```carbon
// Define interface
interface Serializable {
    fn ToBytes[self: Self]() -> [u8];
    fn FromBytes(bytes: [u8]) -> Result(Self, String);
}

// Implement for type
class User {
    var name: String;
    var age: i32;
}

impl User as Serializable {
    fn ToBytes[self: Self]() -> [u8] {
        var result: [u8] = [];
        // Serialization logic
        return result;
    }

    fn FromBytes(bytes: [u8]) -> Result(Self, String) {
        // Deserialization logic
        return Result.Ok(User{.name = "Alice", .age = 30});
    }
}

// Generic function using interface
fn Clone[T:! Serializable](obj: T) -> Result(T, String) {
    var bytes: [u8] = obj.ToBytes();
    return T.FromBytes(bytes);
}
```

### No Runtime Reflection

```carbon
// Carbon does NOT support runtime reflection like Java/C#
// This is intentional for:
// 1. Performance (no RTTI overhead)
// 2. Safety (no dynamic type manipulation)
// 3. Predictability (all types known at compile time)

// Instead, use:
// 1. Generics for type-safe polymorphism
// 2. Interfaces for behavior abstraction
// 3. Variants for tagged unions
// 4. Pattern matching for type dispatch
```

See `patterns-metaprogramming-dev` for cross-language metaprogramming patterns.

---

## Serialization

Carbon does not yet have a standard serialization library. The expected patterns follow Carbon's type safety philosophy.

### Manual Serialization Pattern

```carbon
// Define serialization interface
interface Serializable {
    fn ToJson[self: Self]() -> String;
}

interface Deserializable {
    fn FromJson(json: String) -> Result(Self, String);
}

// Implement for type
class User {
    var name: String;
    var age: i32;
    var email: Optional(String);
}

impl User as Serializable {
    fn ToJson[self: Self]() -> String {
        var json: String = "{";
        json = json + "\"name\":\"" + self.name + "\",";
        json = json + "\"age\":" + ToString(self.age);
        match (self.email) {
            case Optional.Some(e) => {
                json = json + ",\"email\":\"" + e + "\"";
            }
            case Optional.None => {
                // Omit null fields
            }
        }
        json = json + "}";
        return json;
    }
}
```

### C++ Interop for JSON

```carbon
// Use C++ JSON libraries via interop
import Cpp library "nlohmann/json.hpp";

fn ParseJson(input: String) -> Result(Cpp.nlohmann.json, String) {
    // Use nlohmann::json via C++ interop
    var json: Cpp.nlohmann.json = Cpp.nlohmann.json.parse(input);
    return Result.Ok(json);
}

fn ToJsonString(data: Cpp.nlohmann.json) -> String {
    return data.dump();
}

// Convert to Carbon types
fn ParseUser(json: String) -> Result(User, String) {
    var parsed: Cpp.nlohmann.json = Cpp.nlohmann.json.parse(json);
    var user: User = User{
        .name = parsed["name"].get[String](),
        .age = parsed["age"].get[i32](),
        .email = Optional.None
    };
    if (parsed.contains("email")) {
        user.email = Optional.Some(parsed["email"].get[String]());
    }
    return Result.Ok(user);
}
```

### Validation Pattern

```carbon
// Validate after deserialization
class User {
    var name: String;
    var age: i32;

    fn Validate[self: Self]() -> Result((), String) {
        if (self.name.IsEmpty()) {
            return Result.Err("Name cannot be empty");
        }
        if (self.age < 0 or self.age > 150) {
            return Result.Err("Invalid age");
        }
        return Result.Ok(());
    }
}

fn ParseAndValidateUser(json: String) -> Result(User, String) {
    var user: User = ParseUser(json)?;
    user.Validate()?;
    return Result.Ok(user);
}
```

See `patterns-serialization-dev` for cross-language serialization patterns.

---

## Testing

Carbon uses Bazel for its build and test system. Testing patterns follow structured conventions.

### Basic Test Structure

```carbon
// test_mylib.carbon
package MyLib testing;

import MyLib;
import Testing;

fn TestAdd() {
    Testing.AssertEqual(MyLib.Add(2, 3), 5);
}

fn TestAddNegative() {
    Testing.AssertEqual(MyLib.Add(-1, 1), 0);
}

fn TestAddZero() {
    Testing.AssertEqual(MyLib.Add(0, 0), 0);
}
```

### Bazel Test Configuration

```python
# BUILD file
load("@rules_carbon//carbon:defs.bzl", "carbon_test")

carbon_test(
    name = "mylib_test",
    srcs = ["test_mylib.carbon"],
    deps = [
        ":mylib",
        "@carbon_testing//:testing",
    ],
)
```

### Assertion Patterns

```carbon
import Testing;

fn TestAssertions() {
    // Equality
    Testing.AssertEqual(actual, expected);
    Testing.AssertNotEqual(value1, value2);

    // Boolean
    Testing.AssertTrue(condition);
    Testing.AssertFalse(condition);

    // Optional
    Testing.AssertSome(optional);
    Testing.AssertNone(optional);

    // Result
    Testing.AssertOk(result);
    Testing.AssertErr(result);

    // Comparison
    Testing.AssertGreaterThan(5, 3);
    Testing.AssertLessThan(3, 5);
}
```

### Testing with Optional and Result

```carbon
fn TestOptionalHandling() {
    var result: Optional(i32) = FindValue(key);

    match (result) {
        case Optional.Some(value) => {
            Testing.AssertEqual(value, expectedValue);
        }
        case Optional.None => {
            Testing.Fail("Expected value but got None");
        }
    }
}

fn TestResultHandling() {
    var result: Result(User, String) = ParseUser(validJson);

    match (result) {
        case Result.Ok(user) => {
            Testing.AssertEqual(user.name, "Alice");
        }
        case Result.Err(error) => {
            Testing.Fail("Unexpected error: " + error);
        }
    }
}
```

### Test Organization

```
my_project/
├── src/
│   ├── BUILD
│   ├── lib.carbon
│   └── utils.carbon
└── tests/
    ├── BUILD
    ├── test_lib.carbon
    └── test_utils.carbon
```

### Mocking via Interfaces

```carbon
// Define interface for dependency
interface Database {
    fn Get[self: Self](key: String) -> Optional(String);
    fn Set[self: Self*](key: String, value: String);
}

// Production implementation
class RealDatabase {
    // Real database connection
}

impl RealDatabase as Database {
    fn Get[self: Self](key: String) -> Optional(String) {
        // Real implementation
    }
    fn Set[self: Self*](key: String, value: String) {
        // Real implementation
    }
}

// Test mock
class MockDatabase {
    var data: Map(String, String);
}

impl MockDatabase as Database {
    fn Get[self: Self](key: String) -> Optional(String) {
        return self.data.Get(key);
    }
    fn Set[self: Self*](key: String, value: String) {
        self.data.Set(key, value);
    }
}

// Test using mock
fn TestServiceWithMock() {
    var mock: MockDatabase = MockDatabase{.data = Map()};
    mock.Set("key", "value");

    var service: Service(MockDatabase) = Service(&mock);
    var result: String = service.Process("key");

    Testing.AssertEqual(result, "processed: value");
}
```

---

## Cross-Cutting Patterns

For cross-language comparison and translation patterns, see:

- `patterns-concurrency-dev` - Async patterns (when Carbon supports them)
- `patterns-serialization-dev` - JSON, validation patterns
- `patterns-metaprogramming-dev` - Generics, interface patterns

---

## Resources

### Official Documentation
- [Carbon Language Documentation](https://docs.carbon-lang.dev/)
- [Carbon Language GitHub](https://github.com/carbon-language/carbon-lang)
- [Carbon Roadmap](https://docs.carbon-lang.dev/docs/project/roadmap.html)
- [Carbon Safety Strategy](https://github.com/carbon-language/carbon-lang/blob/trunk/docs/project/principles/safety_strategy.md)

### Design Documents
- [Generics Overview](https://github.com/carbon-language/carbon-lang/blob/trunk/docs/design/generics/overview.md)
- [Generics Details](https://docs.carbon-lang.dev/docs/design/generics/details.html)
- [Interoperability Philosophy](https://github.com/carbon-language/carbon-lang/blob/trunk/docs/design/interoperability/philosophy_and_goals.md)
- [Error Handling Principles](https://github.com/carbon-language/carbon-lang/blob/trunk/docs/project/principles/error_handling.md)

### Community
- [Carbon Discussions](https://github.com/carbon-language/carbon-lang/discussions)
- [Weekly Updates](https://github.com/carbon-language/carbon-lang/discussions/6167)

---

**Note:** Carbon is experimental and under active development. The 0.1 milestone is targeted for late 2026. Syntax and features shown in this skill are based on current design proposals and may change. Always refer to the official documentation for the most up-to-date information.
