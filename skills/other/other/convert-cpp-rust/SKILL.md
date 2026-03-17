---
name: convert-cpp-rust
description: Convert C++ code to idiomatic Rust. Use when migrating C++ projects to Rust, translating C++ patterns to idiomatic Rust, or refactoring C++ codebases. Extends meta-convert-dev with C++-to-Rust specific patterns, including FFI-based gradual migration.
---

# Convert C++ to Rust

Convert C++ code to idiomatic Rust. This skill extends `meta-convert-dev` with C++-to-Rust specific type mappings, idiom translations, and FFI strategies for gradual migration.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies, FFI patterns)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: C++ types → Rust types (RAII → ownership, smart pointers → Box/Rc/Arc)
- **Idiom translations**: C++ patterns → idiomatic Rust (templates → generics, virtual functions → traits)
- **Error handling**: C++ exceptions → Rust Result<T, E>
- **Memory/Ownership**: RAII/smart pointers → ownership/borrowing system
- **FFI Integration**: cxx crate for safe C++/Rust interop during migration
- **Template patterns**: C++ templates → Rust generics with trait bounds

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- C++ language fundamentals - see `lang-cpp-dev`
- Rust language fundamentals - see `lang-rust-dev`
- Reverse conversion (Rust → C++) - see `convert-rust-cpp` (if exists)
- Advanced C++ metaprogramming (SFINAE, CRTP) - complex patterns require case-by-case analysis

---

## Quick Reference

| C++ | Rust | Notes |
|----------|----------|-------|
| `std::string` | `String` | Owned, heap-allocated UTF-8 |
| `const char*` / `std::string_view` | `&str` | Borrowed string slice |
| `int` / `long` | `i32` / `i64` | Specify size explicitly |
| `unsigned int` | `u32` | Rust prefers explicit unsigned types |
| `float` / `double` | `f32` / `f64` | Direct mapping |
| `bool` | `bool` | Direct mapping |
| `std::vector<T>` | `Vec<T>` | Growable array |
| `std::array<T, N>` | `[T; N]` | Fixed-size array |
| `std::map<K, V>` | `HashMap<K, V>` / `BTreeMap<K, V>` | Unordered / ordered |
| `std::unique_ptr<T>` | `Box<T>` | Single ownership, heap allocation |
| `std::shared_ptr<T>` | `Rc<T>` / `Arc<T>` | Reference counting (single/multi-threaded) |
| `std::optional<T>` | `Option<T>` | Nullable type |
| `try/catch` | `Result<T, E>` + `?` | Type-safe error handling |
| `throw` | `Err(...)` or `panic!()` | Errors vs unrecoverable failures |
| `template<typename T>` | `<T>` with trait bounds | Generics with constraints |
| `class` / `struct` | `struct` + `impl` blocks | Separation of data and behavior |
| `virtual` functions | `trait` + `dyn Trait` | Dynamic dispatch via trait objects |
| `namespace` | `mod` | Module system |
| `nullptr` | `None` in `Option<T>` | Explicit nullability |

## When Converting Code

1. **Analyze source thoroughly** - Understand C++ object lifetimes, RAII patterns, and ownership semantics
2. **Map types first** - Create type equivalence table, especially smart pointers → Rust ownership
3. **Preserve semantics** - Maintain C++'s RAII cleanup guarantees in Rust's ownership system
4. **Adopt target idioms** - Don't write "C++ code in Rust syntax" (avoid unnecessary Rc/Arc)
5. **Handle edge cases** - nullptr checks, exception safety, move semantics, template instantiation
6. **Test equivalence** - Same inputs → same outputs, verify memory safety
7. **Consider FFI** - For large codebases, use cxx crate for gradual migration

---

## Type System Mapping

### Primitive Types

| C++ | Rust | Notes |
|----------|----------|-------|
| `bool` | `bool` | Direct mapping |
| `char` | `u8` | C++ char is 1 byte, not Unicode |
| `wchar_t` / `char16_t` / `char32_t` | `char` | Rust char is Unicode scalar value (4 bytes) |
| `int8_t` | `i8` | Guaranteed 8-bit signed |
| `int16_t` | `i16` | Guaranteed 16-bit signed |
| `int32_t` | `i32` | Guaranteed 32-bit signed |
| `int64_t` | `i64` | Guaranteed 64-bit signed |
| `uint8_t` | `u8` | Guaranteed 8-bit unsigned |
| `uint16_t` | `u16` | Guaranteed 16-bit unsigned |
| `uint32_t` | `u32` | Guaranteed 32-bit unsigned |
| `uint64_t` | `u64` | Guaranteed 64-bit unsigned |
| `size_t` | `usize` | Platform-dependent unsigned |
| `ptrdiff_t` | `isize` | Platform-dependent signed |
| `float` | `f32` | 32-bit floating point |
| `double` | `f64` | 64-bit floating point |
| `long double` | - | No direct equivalent; use external crate if needed |
| `void` | `()` | Unit type |

### String Types

| C++ | Rust | Notes |
|----------|----------|-------|
| `std::string` | `String` | Owned, heap-allocated, UTF-8 enforced |
| `const std::string&` | `&str` | Borrowed string slice for parameters |
| `std::string&&` | `String` | Move semantics → ownership transfer |
| `const char*` | `&str` / `*const u8` | Prefer &str; use raw pointer only for FFI |
| `char*` | `*mut u8` / `&mut [u8]` | Mutable buffer or raw pointer |
| `std::string_view` (C++17) | `&str` | Non-owning string reference |
| `std::u8string` (C++20) | `String` | Rust String is always UTF-8 |

### Collection Types

| C++ | Rust | Notes |
|----------|----------|-------|
| `std::vector<T>` | `Vec<T>` | Growable, owned array |
| `std::vector<T>&` | `&[T]` / `&mut [T]` | Borrowed slice for parameters |
| `std::array<T, N>` | `[T; N]` | Fixed-size array on stack |
| `std::deque<T>` | `VecDeque<T>` | Double-ended queue |
| `std::list<T>` | - | Use Vec<T> or VecDeque<T>; linked lists rare in Rust |
| `std::map<K, V>` | `BTreeMap<K, V>` | Ordered map, K must be Ord |
| `std::unordered_map<K, V>` | `HashMap<K, V>` | Hash table, K must be Hash + Eq |
| `std::set<T>` | `BTreeSet<T>` | Ordered set |
| `std::unordered_set<T>` | `HashSet<T>` | Hash set |
| `std::pair<T, U>` | `(T, U)` | Tuple |
| `std::tuple<T, U, V>` | `(T, U, V)` | Tuple |
| `std::span<T>` (C++20) | `&[T]` / `&mut [T]` | Non-owning view |

### Smart Pointer Types

| C++ | Rust | Notes |
|----------|----------|-------|
| `std::unique_ptr<T>` | `Box<T>` | Single ownership, heap allocation |
| `std::unique_ptr<T[]>` | `Vec<T>` | Owned dynamic array |
| `std::shared_ptr<T>` | `Rc<T>` | Reference counting (single-threaded) |
| `std::shared_ptr<T>` (thread-safe) | `Arc<T>` | Atomic reference counting (multi-threaded) |
| `std::weak_ptr<T>` | `Weak<T>` / `std::sync::Weak<T>` | Weak reference (Rc/Arc) |
| Raw pointer `T*` | `Box<T>` / `&T` / `&mut T` | Prefer owned/borrowed types; use raw only for FFI |
| `T* const` | `*const T` | Immutable raw pointer (unsafe) |
| `T*` (mutable) | `*mut T` | Mutable raw pointer (unsafe) |

### Optional and Variant Types

| C++ | Rust | Notes |
|----------|----------|-------|
| `std::optional<T>` (C++17) | `Option<T>` | Nullable type, compile-time safety |
| `T*` (nullable) | `Option<Box<T>>` | Heap-allocated nullable |
| `std::variant<T, U>` (C++17) | `enum` | Tagged union, type-safe variant |
| `std::any` (C++17) | - | Use generics or enums; avoid type erasure |
| `void*` | - | Use generics or trait objects; avoid in safe Rust |

### Function Types

| C++ | Rust | Notes |
|----------|----------|-------|
| `void (*)(int)` | `fn(i32)` | Function pointer |
| `std::function<int(int)>` | `Fn(i32) -> i32` | Closure trait (or FnMut, FnOnce) |
| Lambda `[](int x) { ... }` | `\|x\| { ... }` | Closure syntax |
| Lambda `[&](int x) { ... }` | `\|x\| { ... }` with captured refs | Borrow checker enforces safety |
| Lambda `[=](int x) { ... }` | `move \|x\| { ... }` | Move closure (takes ownership) |

### Composite Types

| C++ | Rust | Notes |
|----------|----------|-------|
| `struct { ... }` | `struct { ... }` | Similar syntax, fields private by default in Rust modules |
| `class { ... }` | `struct { ... }` + `impl` | Separate data (struct) from methods (impl) |
| `enum` | `enum` (fieldless) | C-like enum |
| `enum class` (C++11) | `enum` | Rust enums are always scoped |
| Tagged union (manual) | `enum` with variants | Rust enums are sum types |
| `union` | `union` (unsafe) | Avoid; use enums instead |
| Inheritance hierarchy | Composition + traits | Rust favors composition over inheritance |

---

## Idiom Translation

### Pattern 1: RAII and Resource Management

**C++:**
```cpp
class FileHandle {
private:
    FILE* file;

public:
    FileHandle(const char* path, const char* mode)
        : file(fopen(path, mode)) {
        if (!file) {
            throw std::runtime_error("Failed to open file");
        }
    }

    ~FileHandle() {
        if (file) {
            fclose(file);
        }
    }

    // Delete copy, allow move
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;
    FileHandle(FileHandle&& other) noexcept : file(other.file) {
        other.file = nullptr;
    }

    FILE* get() { return file; }
};

// Usage - automatic cleanup
void processFile(const char* filename) {
    FileHandle file(filename, "r");
    // Use file.get()
    // Automatically closed when function exits
}
```

**Rust:**
```rust
use std::fs::File;
use std::io::{self, Read};

struct FileHandle {
    file: File,
}

impl FileHandle {
    fn new(path: &str) -> io::Result<Self> {
        let file = File::open(path)?;
        Ok(FileHandle { file })
    }
}

// Drop trait provides automatic cleanup (like C++ destructor)
impl Drop for FileHandle {
    fn drop(&mut self) {
        // File::drop is called automatically - no manual close needed
        println!("FileHandle dropped");
    }
}

// Usage - automatic cleanup via Drop
fn process_file(filename: &str) -> io::Result<()> {
    let mut file = FileHandle::new(filename)?;
    // Use file
    Ok(())
    // Automatically dropped when function exits
}

// Or more idiomatically, use std::fs::File directly
fn process_file_idiomatic(filename: &str) -> io::Result<()> {
    let file = File::open(filename)?;
    // Use file
    Ok(())
    // File implements Drop, automatic cleanup
}
```

**Why this translation:**
- Rust's `Drop` trait is analogous to C++ destructors for RAII
- Constructors that can fail use `Result<T, E>` instead of exceptions
- Move semantics are default in Rust (no need for `std::move`)
- Ownership system eliminates need for manual delete copy constructors
- The `?` operator propagates errors ergonomically

### Pattern 2: Smart Pointers and Ownership

**C++:**
```cpp
#include <memory>
#include <vector>

class Node {
public:
    int value;
    std::shared_ptr<Node> next;

    Node(int v) : value(v), next(nullptr) {}
};

class LinkedList {
private:
    std::shared_ptr<Node> head;

public:
    void push(int value) {
        auto new_node = std::make_shared<Node>(value);
        new_node->next = head;
        head = new_node;
    }

    std::optional<int> pop() {
        if (!head) {
            return std::nullopt;
        }
        int value = head->value;
        head = head->next;
        return value;
    }
};
```

**Rust:**
```rust
// Avoid shared_ptr pattern in Rust when possible
// Prefer Box for single ownership
struct Node {
    value: i32,
    next: Option<Box<Node>>,
}

struct LinkedList {
    head: Option<Box<Node>>,
}

impl LinkedList {
    fn new() -> Self {
        LinkedList { head: None }
    }

    fn push(&mut self, value: i32) {
        let new_node = Box::new(Node {
            value,
            next: self.head.take(),  // Moves ownership
        });
        self.head = Some(new_node);
    }

    fn pop(&mut self) -> Option<i32> {
        self.head.take().map(|node| {
            self.head = node.next;
            node.value
        })
    }
}

// If shared ownership is truly needed (rare), use Rc
use std::rc::Rc;

struct SharedNode {
    value: i32,
    next: Option<Rc<SharedNode>>,
}

// Note: Rc creates immutable shared ownership
// For interior mutability, use Rc<RefCell<T>>
```

**Why this translation:**
- Rust prefers single ownership (`Box`) over shared ownership (`Rc`/`Arc`)
- `Option<Box<T>>` replaces nullable pointers
- `.take()` method moves ownership out of an Option, replacing with None
- Shared ownership (Rc/Arc) should be used sparingly in Rust
- Reference counting happens at compile-time via ownership tracking, not runtime

### Pattern 3: Templates vs Generics

**C++:**
```cpp
template<typename T>
class Container {
private:
    std::vector<T> data;

public:
    void add(const T& item) {
        data.push_back(item);
    }

    template<typename Predicate>
    std::vector<T> filter(Predicate pred) const {
        std::vector<T> result;
        for (const auto& item : data) {
            if (pred(item)) {
                result.push_back(item);
            }
        }
        return result;
    }

    size_t size() const { return data.size(); }
};

// Usage
Container<int> numbers;
numbers.add(1);
numbers.add(2);
auto evens = numbers.filter([](int x) { return x % 2 == 0; });
```

**Rust:**
```rust
struct Container<T> {
    data: Vec<T>,
}

impl<T> Container<T> {
    fn new() -> Self {
        Container { data: Vec::new() }
    }

    fn add(&mut self, item: T) {
        self.data.push(item);
    }

    fn size(&self) -> usize {
        self.data.len()
    }
}

// Conditional implementation for types that implement Clone
impl<T: Clone> Container<T> {
    fn filter<F>(&self, pred: F) -> Vec<T>
    where
        F: Fn(&T) -> bool,
    {
        self.data
            .iter()
            .filter(|item| pred(item))
            .cloned()
            .collect()
    }
}

// Usage
let mut numbers = Container::new();
numbers.add(1);
numbers.add(2);
let evens = numbers.filter(|x| x % 2 == 0);

// More idiomatic: use iterators directly
let numbers = vec![1, 2, 3, 4, 5];
let evens: Vec<_> = numbers.iter()
    .filter(|x| *x % 2 == 0)
    .copied()
    .collect();
```

**Why this translation:**
- Rust generics require explicit trait bounds (e.g., `T: Clone`)
- `where` clause provides cleaner syntax for complex bounds
- Rust's iterator pattern is more idiomatic than manual collection
- Generic functions use trait bounds instead of template parameter concepts
- No implicit constraints like C++ templates (explicit is better)

### Pattern 4: Inheritance vs Composition + Traits

**C++:**
```cpp
class Animal {
public:
    virtual void make_sound() const = 0;  // Pure virtual
    virtual ~Animal() = default;
};

class Dog : public Animal {
public:
    void make_sound() const override {
        std::cout << "Woof!\n";
    }
};

class Cat : public Animal {
public:
    void make_sound() const override {
        std::cout << "Meow!\n";
    }
};

void animal_sounds(const std::vector<std::unique_ptr<Animal>>& animals) {
    for (const auto& animal : animals) {
        animal->make_sound();
    }
}

int main() {
    std::vector<std::unique_ptr<Animal>> animals;
    animals.push_back(std::make_unique<Dog>());
    animals.push_back(std::make_unique<Cat>());
    animal_sounds(animals);
}
```

**Rust:**
```rust
// Define behavior with a trait (like C++ pure virtual interface)
trait Animal {
    fn make_sound(&self);
}

// Implement trait for concrete types
struct Dog;
impl Animal for Dog {
    fn make_sound(&self) {
        println!("Woof!");
    }
}

struct Cat;
impl Animal for Cat {
    fn make_sound(&self) {
        println!("Meow!");
    }
}

// Option 1: Dynamic dispatch with trait objects (like C++ virtual)
fn animal_sounds_dyn(animals: &[Box<dyn Animal>]) {
    for animal in animals {
        animal.make_sound();
    }
}

// Option 2: Static dispatch with generics (no runtime overhead)
fn animal_sounds_generic<A: Animal>(animals: &[A]) {
    for animal in animals {
        animal.make_sound();
    }
}

fn main() {
    // Dynamic dispatch (runtime polymorphism)
    let animals: Vec<Box<dyn Animal>> = vec![
        Box::new(Dog),
        Box::new(Cat),
    ];
    animal_sounds_dyn(&animals);

    // Static dispatch (compile-time polymorphism)
    let dogs = vec![Dog, Dog];
    animal_sounds_generic(&dogs);
}
```

**Why this translation:**
- Rust uses traits instead of inheritance for polymorphism
- `dyn Trait` provides runtime polymorphism (like C++ virtual functions)
- Generic bounds provide zero-cost compile-time polymorphism
- No inheritance hierarchy - composition and traits are preferred
- Trait objects require explicit `Box<dyn Trait>` or `&dyn Trait`

### Pattern 5: Exception Handling to Result Types

**C++:**
```cpp
#include <stdexcept>
#include <string>
#include <fstream>

class FileError : public std::runtime_error {
public:
    FileError(const std::string& msg) : std::runtime_error(msg) {}
};

std::string readFile(const std::string& path) {
    std::ifstream file(path);
    if (!file.is_open()) {
        throw FileError("Failed to open file: " + path);
    }

    std::string content;
    std::string line;
    while (std::getline(file, line)) {
        content += line + "\n";
    }

    if (file.bad()) {
        throw FileError("Error reading file: " + path);
    }

    return content;
}

void processFile(const std::string& path) {
    try {
        std::string content = readFile(path);
        // Process content
    } catch (const FileError& e) {
        std::cerr << "File error: " << e.what() << "\n";
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
    }
}
```

**Rust:**
```rust
use std::fs;
use std::io;
use std::path::Path;

// Custom error type
#[derive(Debug)]
enum FileError {
    Io(io::Error),
    InvalidContent(String),
}

impl From<io::Error> for FileError {
    fn from(err: io::Error) -> Self {
        FileError::Io(err)
    }
}

impl std::fmt::Display for FileError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            FileError::Io(e) => write!(f, "IO error: {}", e),
            FileError::InvalidContent(msg) => write!(f, "Invalid content: {}", msg),
        }
    }
}

impl std::error::Error for FileError {}

fn read_file(path: &Path) -> Result<String, FileError> {
    // ? operator propagates errors (like C++ exception unwinding)
    let content = fs::read_to_string(path)?;
    Ok(content)
}

fn process_file(path: &Path) {
    match read_file(path) {
        Ok(content) => {
            // Process content
            println!("Read {} bytes", content.len());
        }
        Err(FileError::Io(e)) => {
            eprintln!("File error: {}", e);
        }
        Err(FileError::InvalidContent(msg)) => {
            eprintln!("Invalid content: {}", msg);
        }
    }
}

// Or use the ? operator to propagate
fn process_file_propagate(path: &Path) -> Result<(), FileError> {
    let content = read_file(path)?;
    // Process content
    Ok(())
}
```

**Why this translation:**
- Rust uses `Result<T, E>` instead of exceptions for recoverable errors
- The `?` operator replaces `try/catch` for error propagation
- `From` trait enables automatic error conversion (like exception hierarchies)
- Pattern matching on Result is explicit and type-safe
- Unrecoverable errors use `panic!()` instead of exceptions

---

## Memory & Ownership Translation

### C++ RAII vs Rust Ownership

| C++ Pattern | Rust Equivalent | Key Difference |
|-------------|-----------------|----------------|
| Constructor acquires resource | Constructor returns `Result<T, E>` | Fallible construction explicit |
| Destructor releases resource | `Drop` trait | Automatic, deterministic cleanup |
| Copy constructor | `Clone` trait | Explicit, not automatic |
| Move constructor | Default move semantics | Moves are implicit, borrowing is explicit |
| `const T&` parameter | `&T` parameter | Borrow checker enforces lifetime |
| `T&&` parameter | `T` parameter | Takes ownership by default |
| `std::unique_ptr<T>` | `Box<T>` | Single ownership |
| `std::shared_ptr<T>` | `Rc<T>` / `Arc<T>` | Avoid when possible; prefer borrowing |

### Smart Pointer Translation Guide

```cpp
// C++: unique_ptr for single ownership
std::unique_ptr<Widget> widget = std::make_unique<Widget>();
use_widget(*widget);  // Dereference
auto moved = std::move(widget);  // Explicit move
```

```rust
// Rust: Box for single ownership
let widget = Box::new(Widget::new());
use_widget(&widget);  // Automatic deref via Deref trait
let moved = widget;  // Implicit move (widget no longer usable)
```

```cpp
// C++: shared_ptr for shared ownership
std::shared_ptr<Data> data = std::make_shared<Data>();
auto copy = data;  // Reference count increased
```

```rust
// Rust: Prefer borrowing over shared ownership
let data = Data::new();
use_data(&data);  // Borrow instead of clone
use_data_again(&data);  // Can borrow multiple times

// Only use Rc if truly needed (shared ownership)
use std::rc::Rc;
let data = Rc::new(Data::new());
let copy = Rc::clone(&data);  // Reference count increased
```

### Lifetime Annotations (No C++ Equivalent)

Rust's borrow checker requires explicit lifetime annotations when relationships aren't clear:

```rust
// Rust: Lifetime ensures returned reference is valid
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Struct containing references
struct Parser<'a> {
    source: &'a str,
    position: usize,
}

impl<'a> Parser<'a> {
    fn new(source: &'a str) -> Self {
        Parser { source, position: 0 }
    }

    fn current(&self) -> &'a str {
        &self.source[self.position..]
    }
}
```

C++ has no equivalent to lifetimes - the compiler doesn't track reference validity at compile time. Rust's lifetimes prevent dangling references that would compile in C++ but cause runtime errors.

---

## FFI & Interoperability (10th Pillar)

For large C++ codebases, gradual migration using FFI is often the best strategy. The `cxx` crate provides safe C++/Rust interop.

### Why FFI Matters for C++ → Rust

Instead of rewriting everything at once:
1. Convert performance-critical modules to Rust first
2. Keep stable C++ code as-is during transition
3. Test new Rust code against existing C++ test suite
4. Gradually replace C++ modules over time
5. Roll back easily if issues arise

### The cxx Crate

The `cxx` crate provides safe, zero-overhead C++ interop:

```toml
# Cargo.toml
[dependencies]
cxx = "1.0"

[build-dependencies]
cxx-build = "1.0"
```

### Basic FFI Example

**C++ side (src/cpp/widget.h):**
```cpp
#pragma once
#include <memory>
#include <string>

class Widget {
private:
    int value_;

public:
    Widget(int value);
    int get_value() const;
    void set_value(int value);
    std::string to_string() const;
};

std::unique_ptr<Widget> create_widget(int value);
```

**C++ implementation (src/cpp/widget.cpp):**
```cpp
#include "widget.h"
#include <sstream>

Widget::Widget(int value) : value_(value) {}

int Widget::get_value() const {
    return value_;
}

void Widget::set_value(int value) {
    value_ = value;
}

std::string Widget::to_string() const {
    std::ostringstream oss;
    oss << "Widget(" << value_ << ")";
    return oss.str();
}

std::unique_ptr<Widget> create_widget(int value) {
    return std::make_unique<Widget>(value);
}
```

**Rust FFI bridge (src/bridge.rs):**
```rust
#[cxx::bridge]
mod ffi {
    // Shared structs (visible to both C++ and Rust)
    struct Config {
        name: String,
        value: i32,
    }

    // C++ types and functions
    unsafe extern "C++" {
        include!("myproject/widget.h");

        // Opaque C++ type
        type Widget;

        // C++ functions
        fn create_widget(value: i32) -> UniquePtr<Widget>;
        fn get_value(self: &Widget) -> i32;
        fn set_value(self: Pin<&mut Widget>, value: i32);
        fn to_string(self: &Widget) -> String;
    }

    // Rust functions callable from C++
    extern "Rust" {
        fn process_widget(widget: &Widget) -> i32;
        fn create_config(name: String, value: i32) -> Config;
    }
}

// Implement Rust functions
fn process_widget(widget: &ffi::Widget) -> i32 {
    let current = widget.get_value();
    current * 2
}

fn create_config(name: String, value: i32) -> ffi::Config {
    ffi::Config { name, value }
}

// Use C++ from Rust
pub fn use_cpp_widget() {
    let widget = ffi::create_widget(42);
    println!("Widget: {}", widget.to_string());
    let doubled = process_widget(&widget);
    println!("Processed: {}", doubled);
}
```

**Build script (build.rs):**
```rust
fn main() {
    cxx_build::bridge("src/bridge.rs")
        .file("src/cpp/widget.cpp")
        .flag_if_supported("-std=c++17")
        .compile("myproject-cpp");

    println!("cargo:rerun-if-changed=src/bridge.rs");
    println!("cargo:rerun-if-changed=src/cpp/widget.h");
    println!("cargo:rerun-if-changed=src/cpp/widget.cpp");
}
```

### Data Type Marshalling

| C++ Type | cxx Bridge Type | Rust Type | Notes |
|----------|-----------------|-----------|-------|
| `int32_t` | `i32` | `i32` | Direct pass by value |
| `std::string` | `String` | `String` | Copied across boundary |
| `&std::string` | `&str` | `&str` | Zero-copy borrow |
| `std::unique_ptr<T>` | `UniquePtr<T>` | `UniquePtr<T>` | Ownership transfer |
| `std::shared_ptr<T>` | `SharedPtr<T>` | `SharedPtr<T>` | Reference counted |
| `&T` | `&T` | `&T` | Shared borrow |
| `&mut T` | `Pin<&mut T>` | `Pin<&mut T>` | Exclusive borrow |
| `std::vector<T>` | `Vec<T>` | `Vec<T>` | Copied across boundary |
| `&std::vector<T>` | `&CxxVector<T>` | `&CxxVector<T>` | Zero-copy view |

### Gradual Migration Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                  GRADUAL MIGRATION PHASES                    │
├─────────────────────────────────────────────────────────────┤
│  Phase 1: SETUP                                              │
│  • Add cxx to Cargo.toml                                     │
│  • Create FFI bridge module                                  │
│  • Set up build.rs to compile C++ code                       │
│  • Verify C++ and Rust can call each other                   │
├─────────────────────────────────────────────────────────────┤
│  Phase 2: IDENTIFY TARGET MODULES                            │
│  • Find performance bottlenecks (profile C++ code)           │
│  • Identify frequently-changing modules (benefit from Rust)  │
│  • Map dependencies between modules                          │
│  • Choose initial module with minimal dependencies           │
├─────────────────────────────────────────────────────────────┤
│  Phase 3: CONVERT FIRST MODULE                               │
│  • Translate C++ module to Rust                              │
│  • Expose Rust module via cxx bridge                         │
│  • Keep C++ interface unchanged (drop-in replacement)        │
│  • Test Rust implementation against C++ test suite           │
├─────────────────────────────────────────────────────────────┤
│  Phase 4: INTEGRATION                                        │
│  • Replace C++ module calls with Rust calls                  │
│  • Run full integration tests                                │
│  • Monitor for issues (memory leaks, performance)            │
│  • Rollback to C++ if needed                                 │
├─────────────────────────────────────────────────────────────┤
│  Phase 5: ITERATE                                            │
│  • Repeat for next module                                    │
│  • Gradually reduce C++ footprint                            │
│  • Eventually remove cxx bridge (all Rust)                   │
└─────────────────────────────────────────────────────────────┘
```

### FFI Best Practices

1. **Keep FFI boundary thin** - Convert types at the boundary, work with native types internally
2. **Avoid complex types** - Prefer simple types (integers, strings) over complex structs
3. **Handle errors explicitly** - C++ exceptions don't cross FFI boundary safely
4. **Test FFI thoroughly** - Memory bugs can occur at language boundaries
5. **Document ownership** - Be clear about who owns data (C++ or Rust)
6. **Measure overhead** - Profile FFI calls if performance-critical

### FFI Error Handling

```rust
#[cxx::bridge]
mod ffi {
    unsafe extern "C++" {
        include!("myproject/api.h");

        // C++ function that can throw
        fn risky_operation(value: i32) -> Result<String>;
    }
}

// Use from Rust
fn call_cpp() -> Result<(), Box<dyn std::error::Error>> {
    // cxx converts C++ exceptions to Rust Result
    let result = ffi::risky_operation(42)?;
    println!("Success: {}", result);
    Ok(())
}
```

**C++ side:**
```cpp
// C++ function that throws
std::string risky_operation(int32_t value) {
    if (value < 0) {
        throw std::runtime_error("Negative value not allowed");
    }
    return "Success";
}
```

---

## Common Pitfalls

### 1. Overusing Rc/Arc (Avoid C++ shared_ptr Mindset)

**Problem:** Translating every `shared_ptr` to `Rc`/`Arc`.

```rust
// Bad: Unnecessary shared ownership
use std::rc::Rc;

struct Node {
    value: i32,
    children: Vec<Rc<Node>>,  // Over-engineered
}
```

**Solution:** Prefer borrowing or single ownership:

```rust
// Good: Use Box for owned children
struct Node {
    value: i32,
    children: Vec<Box<Node>>,
}

// Or borrow when possible
fn process_nodes(nodes: &[Node]) {
    // Work with borrowed references
}
```

### 2. Fighting the Borrow Checker with Clones

**Problem:** Cloning everywhere to satisfy the borrow checker.

```rust
// Bad: Excessive cloning
fn process(data: &Vec<String>) -> Vec<String> {
    data.clone()  // Unnecessary full copy
        .into_iter()
        .filter(|s| s.len() > 5)
        .collect()
}
```

**Solution:** Use references properly:

```rust
// Good: Work with references
fn process(data: &[String]) -> Vec<&str> {
    data.iter()
        .filter(|s| s.len() > 5)
        .map(|s| s.as_str())
        .collect()
}

// Or if ownership is needed, be explicit
fn process_owned(data: Vec<String>) -> Vec<String> {
    data.into_iter()
        .filter(|s| s.len() > 5)
        .collect()
}
```

### 3. Null Pointer Mistakes

**Problem:** Treating `Option<T>` like nullable pointers without checking.

```rust
// Bad: Unwrapping without checking (panics at runtime)
fn get_value(opt: Option<i32>) -> i32 {
    opt.unwrap()  // Panics if None
}
```

**Solution:** Handle None explicitly:

```rust
// Good: Pattern matching
fn get_value(opt: Option<i32>) -> i32 {
    match opt {
        Some(v) => v,
        None => 0,  // Default value
    }
}

// Or use combinators
fn get_value(opt: Option<i32>) -> i32 {
    opt.unwrap_or(0)
}
```

### 4. Ignoring Lifetime Errors

**Problem:** Returning references that outlive their source.

```rust
// Bad: Compiler error - returning reference to local
fn create_string() -> &str {
    let s = String::from("hello");
    &s  // Error: s dropped at end of function
}
```

**Solution:** Return owned data or use proper lifetimes:

```rust
// Good: Return owned String
fn create_string() -> String {
    String::from("hello")
}

// Or if parameter-based:
fn first_word(s: &str) -> &str {
    s.split_whitespace().next().unwrap_or("")
}
```

### 5. Transliterating C++ Patterns

**Problem:** Writing "C++ code in Rust syntax" instead of idiomatic Rust.

```rust
// Bad: Transliterated C++ style
struct Container {
    data: Vec<i32>,
}

impl Container {
    fn get(&self, index: usize) -> Option<i32> {
        if index < self.data.len() {
            Some(self.data[index])
        } else {
            None
        }
    }
}
```

**Solution:** Use Rust idioms:

```rust
// Good: Idiomatic Rust
struct Container {
    data: Vec<i32>,
}

impl Container {
    fn get(&self, index: usize) -> Option<&i32> {
        self.data.get(index)  // Built-in method
    }
}

// Or even simpler - use Vec directly
fn get_item(data: &[i32], index: usize) -> Option<&i32> {
    data.get(index)
}
```

### 6. Manual Iterator Loops

**Problem:** Using C++-style loops instead of iterators.

```rust
// Bad: C++ style loop
let mut sum = 0;
for i in 0..numbers.len() {
    sum += numbers[i];
}
```

**Solution:** Use iterator methods:

```rust
// Good: Idiomatic iterator
let sum: i32 = numbers.iter().sum();

// Or for more complex operations
let sum: i32 = numbers.iter()
    .filter(|&&x| x > 0)
    .sum();
```

---

## Tooling

| Tool | Purpose | Notes |
|------|---------|-------|
| `cxx` crate | Safe C++/Rust FFI | Recommended for gradual migration |
| `bindgen` | Generate Rust FFI bindings from C++ headers | For C-compatible C++ APIs |
| `cbindgen` | Generate C/C++ headers from Rust | Expose Rust to C++ |
| `autocxx` | Automatically call C++ from Rust | Higher-level than cxx |
| `cpp` crate | Embed C++ directly in Rust | For quick experiments |
| `cargo expand` | Expand macros and generics | Understand template translation |
| `rust-analyzer` | IDE support | Catch lifetime/borrow errors early |
| `clippy` | Linter | Suggests idiomatic Rust patterns |

---

## Examples

### Example 1: Simple - String Processing

**Before (C++):**
```cpp
#include <string>
#include <algorithm>

std::string to_uppercase(const std::string& input) {
    std::string result = input;
    std::transform(result.begin(), result.end(), result.begin(),
                   [](unsigned char c) { return std::toupper(c); });
    return result;
}

int main() {
    std::string text = "hello world";
    std::string upper = to_uppercase(text);
    // text is still valid (copied)
}
```

**After (Rust):**
```rust
fn to_uppercase(input: &str) -> String {
    input.to_uppercase()
}

fn main() {
    let text = "hello world";
    let upper = to_uppercase(&text);
    // text is still valid (borrowed, not moved)
}
```

### Example 2: Medium - Optional Values and Error Handling

**Before (C++):**
```cpp
#include <optional>
#include <stdexcept>
#include <map>

class UserDatabase {
private:
    std::map<int, std::string> users;

public:
    void add_user(int id, const std::string& name) {
        if (users.count(id) > 0) {
            throw std::runtime_error("User already exists");
        }
        users[id] = name;
    }

    std::optional<std::string> get_user(int id) const {
        auto it = users.find(id);
        if (it != users.end()) {
            return it->second;
        }
        return std::nullopt;
    }

    bool remove_user(int id) {
        return users.erase(id) > 0;
    }
};

int main() {
    UserDatabase db;

    try {
        db.add_user(1, "Alice");
        auto user = db.get_user(1);
        if (user) {
            std::cout << "Found: " << *user << "\n";
        }
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
    }
}
```

**After (Rust):**
```rust
use std::collections::HashMap;

#[derive(Debug)]
enum DbError {
    UserExists,
}

struct UserDatabase {
    users: HashMap<i32, String>,
}

impl UserDatabase {
    fn new() -> Self {
        UserDatabase {
            users: HashMap::new(),
        }
    }

    fn add_user(&mut self, id: i32, name: String) -> Result<(), DbError> {
        if self.users.contains_key(&id) {
            return Err(DbError::UserExists);
        }
        self.users.insert(id, name);
        Ok(())
    }

    fn get_user(&self, id: i32) -> Option<&String> {
        self.users.get(&id)
    }

    fn remove_user(&mut self, id: i32) -> bool {
        self.users.remove(&id).is_some()
    }
}

fn main() {
    let mut db = UserDatabase::new();

    match db.add_user(1, String::from("Alice")) {
        Ok(()) => {
            if let Some(user) = db.get_user(1) {
                println!("Found: {}", user);
            }
        }
        Err(DbError::UserExists) => {
            eprintln!("Error: User already exists");
        }
    }
}
```

### Example 3: Complex - Polymorphism with Smart Pointers

**Before (C++):**
```cpp
#include <memory>
#include <vector>
#include <iostream>

class Shape {
public:
    virtual double area() const = 0;
    virtual void describe() const = 0;
    virtual ~Shape() = default;
};

class Circle : public Shape {
private:
    double radius;

public:
    Circle(double r) : radius(r) {}

    double area() const override {
        return 3.14159 * radius * radius;
    }

    void describe() const override {
        std::cout << "Circle with radius " << radius << "\n";
    }
};

class Rectangle : public Shape {
private:
    double width, height;

public:
    Rectangle(double w, double h) : width(w), height(h) {}

    double area() const override {
        return width * height;
    }

    void describe() const override {
        std::cout << "Rectangle " << width << "x" << height << "\n";
    }
};

class ShapeCollection {
private:
    std::vector<std::unique_ptr<Shape>> shapes;

public:
    void add_shape(std::unique_ptr<Shape> shape) {
        shapes.push_back(std::move(shape));
    }

    double total_area() const {
        double total = 0;
        for (const auto& shape : shapes) {
            total += shape->area();
        }
        return total;
    }

    void describe_all() const {
        for (const auto& shape : shapes) {
            shape->describe();
            std::cout << "  Area: " << shape->area() << "\n";
        }
    }
};

int main() {
    ShapeCollection collection;
    collection.add_shape(std::make_unique<Circle>(5.0));
    collection.add_shape(std::make_unique<Rectangle>(4.0, 6.0));

    collection.describe_all();
    std::cout << "Total area: " << collection.total_area() << "\n";
}
```

**After (Rust):**
```rust
// Define trait (like C++ abstract base class)
trait Shape {
    fn area(&self) -> f64;
    fn describe(&self) -> String;
}

// Concrete implementations
struct Circle {
    radius: f64,
}

impl Circle {
    fn new(radius: f64) -> Self {
        Circle { radius }
    }
}

impl Shape for Circle {
    fn area(&self) -> f64 {
        3.14159 * self.radius * self.radius
    }

    fn describe(&self) -> String {
        format!("Circle with radius {}", self.radius)
    }
}

struct Rectangle {
    width: f64,
    height: f64,
}

impl Rectangle {
    fn new(width: f64, height: f64) -> Self {
        Rectangle { width, height }
    }
}

impl Shape for Rectangle {
    fn area(&self) -> f64 {
        self.width * self.height
    }

    fn describe(&self) -> String {
        format!("Rectangle {}x{}", self.width, self.height)
    }
}

// Collection using trait objects (dynamic dispatch)
struct ShapeCollection {
    shapes: Vec<Box<dyn Shape>>,
}

impl ShapeCollection {
    fn new() -> Self {
        ShapeCollection { shapes: Vec::new() }
    }

    fn add_shape(&mut self, shape: Box<dyn Shape>) {
        self.shapes.push(shape);
    }

    fn total_area(&self) -> f64 {
        self.shapes.iter().map(|s| s.area()).sum()
    }

    fn describe_all(&self) {
        for shape in &self.shapes {
            println!("{}", shape.describe());
            println!("  Area: {}", shape.area());
        }
    }
}

fn main() {
    let mut collection = ShapeCollection::new();
    collection.add_shape(Box::new(Circle::new(5.0)));
    collection.add_shape(Box::new(Rectangle::new(4.0, 6.0)));

    collection.describe_all();
    println!("Total area: {}", collection.total_area());
}
```

---

## Limitations

This skill has limited coverage in some areas due to gaps in the foundation skills:

### Coverage Gaps

| Pillar | lang-cpp-dev | lang-rust-dev | Mitigation |
|--------|--------------|---------------|------------|
| Module System | ~ | ✓ | C++ namespaces → Rust modules documented via web research |
| Error Handling | ~ | ✓ | C++ exception patterns researched from cppreference.com |
| Serialization | ✗ | ✓ | Common C++ serialization libraries researched |
| FFI | ~ | ~ | Extended via meta-convert-dev FFI pillar and cxx crate docs |

### Known Limitations

1. **C++ Module System**: C++20 modules are new; this skill focuses on namespace translation
2. **Advanced Metaprogramming**: SFINAE, CRTP, and template metaprogramming require case-by-case analysis
3. **Coroutines**: C++20 coroutines have no direct Rust equivalent; use async/await patterns

### External Resources Used

| Resource | What It Provided | Reliability |
|----------|------------------|-------------|
| cxx crate docs | FFI patterns and examples | High (official) |
| cppreference.com | C++ exception model | High (community standard) |
| Rust Book | Ownership patterns | High (official) |

---

## See Also

- `meta-convert-dev` - Foundational patterns (APTV workflow, FFI pillar, testing strategies)
- `lang-cpp-dev` - C++ development patterns
- `lang-rust-dev` - Rust development patterns
- `convert-golang-rust` - Similar modern language → Rust conversion

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - Async, threads, channels across languages
- `patterns-serialization-dev` - JSON, validation, struct tags across languages
- `patterns-metaprogramming-dev` - Templates, macros, generics across languages
