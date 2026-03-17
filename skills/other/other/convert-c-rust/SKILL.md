---
name: convert-c-rust
description: Convert C code to idiomatic Rust. Use when migrating C projects to Rust, translating C patterns to idiomatic Rust, or refactoring C codebases. Extends meta-convert-dev with C-to-Rust specific patterns covering manual memory management to ownership, pointer safety, type system enhancements, and modernization strategies.
---

# Convert C to Rust

Convert C code to idiomatic Rust. This skill extends `meta-convert-dev` with C-to-Rust specific type mappings, idiom translations, and tooling for migrating from manual memory management to Rust's ownership system.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: C types → Rust types with safety guarantees
- **Memory model**: Manual memory management → Ownership and borrowing
- **Pointer safety**: Raw pointers → References and smart pointers
- **Error handling**: Error codes → Result types
- **Module system**: Header files → Rust modules
- **Build system**: Makefiles/CMake → Cargo
- **Concurrency**: pthreads → std::thread and async
- **FFI patterns**: Interfacing between C and Rust during migration

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- C language fundamentals - see `lang-c-dev`
- Rust language fundamentals - see `lang-rust-dev`
- Reverse conversion (Rust → C) - see `convert-rust-c`
- Advanced C memory engineering - see `lang-c-memory-eng`
- Advanced Rust memory engineering - see `lang-rust-memory-eng`

---

## Quick Reference

| C | Rust | Notes |
|---|------|-------|
| `int` | `i32` | Signed 32-bit |
| `unsigned int` | `u32` | Unsigned 32-bit |
| `char` | `u8` / `char` | Byte vs Unicode scalar |
| `char*` | `*const u8` / `&str` / `String` | Raw / borrowed / owned |
| `void*` | `*mut c_void` / generics | Prefer generics |
| `struct` | `struct` | Similar syntax |
| `enum` | `enum` | Rust enums more powerful |
| `union` | `union` (unsafe) / `enum` | Prefer tagged enum |
| `NULL` | `Option<T>` / `null()` | Type-safe nullability |
| `malloc/free` | `Box::new` / `Vec` / auto-drop | RAII |
| `FILE*` | `std::fs::File` | Safe file handling |
| `errno` | `Result<T, E>` | Explicit error handling |
| `pthread_t` | `std::thread` / `tokio` | Safe concurrency |
| `#define` | `const` / macros | Type-safe constants |
| `#include` | `use` / `mod` | Module system |

## When Converting Code

1. **Analyze source thoroughly** - Understand memory management patterns
2. **Map types first** - Create type equivalence table
3. **Identify ownership** - Determine who owns each allocation
4. **Translate pointers** - Convert to references or smart pointers
5. **Handle errors explicitly** - Replace error codes with Result
6. **Preserve semantics** - Same behavior, safer implementation
7. **Test equivalence** - Same inputs → same outputs

---

## Type System Mapping

### Primitive Types

| C Type | Size (typical) | Rust Type | Size | Notes |
|--------|---------------|-----------|------|-------|
| `char` | 1 byte | `i8` | 1 byte | Signed byte |
| `unsigned char` | 1 byte | `u8` | 1 byte | Unsigned byte |
| `short` | 2 bytes | `i16` | 2 bytes | Signed 16-bit |
| `unsigned short` | 2 bytes | `u16` | 2 bytes | Unsigned 16-bit |
| `int` | 4 bytes | `i32` | 4 bytes | Signed 32-bit (default) |
| `unsigned int` | 4 bytes | `u32` | 4 bytes | Unsigned 32-bit |
| `long` | 4/8 bytes | `i64` / `isize` | 8 bytes / ptr-sized | Platform-dependent in C |
| `unsigned long` | 4/8 bytes | `u64` / `usize` | 8 bytes / ptr-sized | Platform-dependent in C |
| `long long` | 8 bytes | `i64` | 8 bytes | Signed 64-bit |
| `float` | 4 bytes | `f32` | 4 bytes | 32-bit floating point |
| `double` | 8 bytes | `f64` | 8 bytes | 64-bit floating point (default) |
| `_Bool` / `bool` | 1 byte | `bool` | 1 byte | Boolean (C99+) |
| `size_t` | ptr-sized | `usize` | ptr-sized | Sizes and indices |
| `ptrdiff_t` | ptr-sized | `isize` | ptr-sized | Pointer arithmetic |
| `intptr_t` | ptr-sized | `isize` | ptr-sized | Pointer-sized integer |
| `uintptr_t` | ptr-sized | `usize` | ptr-sized | Unsigned pointer-sized |
| `void` | - | `()` | 0 bytes | Unit type |

**Fixed-width types (C99+ stdint.h → Rust):**

| C (stdint.h) | Rust | Notes |
|--------------|------|-------|
| `int8_t` | `i8` | Exactly 8 bits signed |
| `uint8_t` | `u8` | Exactly 8 bits unsigned |
| `int16_t` | `i16` | Exactly 16 bits signed |
| `uint16_t` | `u16` | Exactly 16 bits unsigned |
| `int32_t` | `i32` | Exactly 32 bits signed |
| `uint32_t` | `u32` | Exactly 32 bits unsigned |
| `int64_t` | `i64` | Exactly 64 bits signed |
| `uint64_t` | `u64` | Exactly 64 bits unsigned |

### Pointer Types

| C Pattern | Rust Pattern | When to Use |
|-----------|--------------|-------------|
| `const T*` | `&T` | Immutable borrow (read-only access) |
| `T*` | `&mut T` | Mutable borrow (exclusive access) |
| `T*` | `Box<T>` | Owned heap allocation |
| `T*` | `*const T` | Raw pointer (unsafe, FFI) |
| `T*` | `*mut T` | Mutable raw pointer (unsafe, FFI) |
| `T**` | `&mut &T` / `Box<Box<T>>` | Pointer to pointer |
| `void*` | `*mut c_void` / `T: ?Sized` | Type-erased pointer / generics |
| `NULL` | `None` | `Option<&T>` or `Option<Box<T>>` |
| Array pointer `T*` | `&[T]` / `&mut [T]` | Slice (borrowed array) |
| Array pointer `T*` | `Vec<T>` | Owned dynamic array |

### Structure and Union Types

| C | Rust | Notes |
|---|------|-------|
| `struct Point { int x; int y; }` | `struct Point { x: i32, y: i32 }` | Similar syntax |
| `typedef struct { ... } Name;` | `struct Name { ... }` | No typedef needed |
| `union Data { ... }` | `union Data { ... }` (unsafe) | Requires unsafe to access |
| Tagged union | `enum Data { Int(i32), Float(f64) }` | Safer alternative |
| `struct` with padding | `#[repr(C)]` attribute | Match C layout for FFI |
| `struct` bit fields | Manual bit manipulation | No direct equivalent |
| Flexible array member | `Vec<T>` or manual allocation | Safer alternatives |

### Enum Types

**C:**
```c
enum Color {
    RED,      // 0
    GREEN,    // 1
    BLUE      // 2
};

enum Status {
    OK = 0,
    ERROR = -1,
    PENDING = 1
};
```

**Rust:**
```rust
// C-like enum
#[repr(i32)]  // Use C representation
enum Color {
    Red = 0,
    Green = 1,
    Blue = 2,
}

// Rust idiomatic enum with data
enum Status {
    Ok,
    Error(String),  // Can carry data
    Pending { progress: f64 },
}
```

**Why this translation:**
- Rust enums can carry associated data (algebraic data types)
- Use `#[repr(C)]` or `#[repr(i32)]` for C compatibility
- Rust enums are type-safe and cannot be used as raw integers without explicit conversion

### Function Pointers

| C | Rust | Notes |
|---|------|-------|
| `int (*fn)(int, int)` | `fn(i32, i32) -> i32` | Function pointer |
| `int (*fn)(int, int)` | `Fn(i32, i32) -> i32` | Trait object (can capture) |
| `void (*callback)(void*)` | `Box<dyn Fn(*mut c_void)>` | Callback with state |
| Function pointer array | `[fn(); N]` / `Vec<fn()>` | Array of function pointers |

---

## Memory Management Translation

### Manual Allocation → Ownership

**C: Manual Memory Management**
```c
#include <stdlib.h>
#include <string.h>

// Allocate and initialize
char *create_string(const char *s) {
    char *result = malloc(strlen(s) + 1);
    if (result == NULL) {
        return NULL;
    }
    strcpy(result, s);
    return result;
}

// Caller must free
int main(void) {
    char *str = create_string("Hello");
    if (str == NULL) {
        return 1;
    }
    printf("%s\n", str);
    free(str);  // Manual cleanup
    return 0;
}
```

**Rust: Automatic Memory Management**
```rust
// Return owned String
fn create_string(s: &str) -> String {
    s.to_string()  // Allocates and returns ownership
}

fn main() {
    let s = create_string("Hello");
    println!("{}", s);
    // s automatically dropped at end of scope
}
```

**Why this translation:**
- Rust's ownership system ensures memory is freed exactly once
- No explicit `free()` needed - Drop trait handles cleanup
- Impossible to return dangling pointers
- Compiler enforces memory safety at compile time

### malloc/calloc/realloc → Rust Allocation

| C Pattern | Rust Pattern | Notes |
|-----------|--------------|-------|
| `malloc(size)` | `Box::new(value)` | Single heap allocation |
| `malloc(n * sizeof(T))` | `Vec::with_capacity(n)` | Array allocation |
| `calloc(n, sizeof(T))` | `vec![0; n]` | Zero-initialized array |
| `realloc(ptr, new_size)` | `vec.resize(new_len, default)` | Resize allocation |
| `free(ptr)` | Automatic | Drop trait |
| `ptr = NULL` after free | Not needed | Move semantics prevent use-after-free |

**C: Array Allocation**
```c
int *numbers = malloc(10 * sizeof(int));
if (numbers == NULL) {
    return -1;
}

// Use array
for (int i = 0; i < 10; i++) {
    numbers[i] = i * 2;
}

// Resize
int *resized = realloc(numbers, 20 * sizeof(int));
if (resized == NULL) {
    free(numbers);
    return -1;
}
numbers = resized;

free(numbers);
```

**Rust: Vec Allocation**
```rust
let mut numbers = Vec::with_capacity(10);

// Use array
for i in 0..10 {
    numbers.push(i * 2);
}

// Resize
numbers.resize(20, 0);

// Automatic cleanup when numbers goes out of scope
```

### Pointer Patterns → References and Smart Pointers

**Pattern 1: Passing by Pointer**

**C:**
```c
void modify(int *value) {
    *value += 10;
}

int x = 5;
modify(&x);  // x is now 15
```

**Rust:**
```rust
fn modify(value: &mut i32) {
    *value += 10;
}

let mut x = 5;
modify(&mut x);  // x is now 15
```

**Pattern 2: Optional Pointers (NULL)**

**C:**
```c
int *find_value(int key) {
    if (key_exists) {
        return &value;
    }
    return NULL;
}

int *result = find_value(42);
if (result != NULL) {
    printf("%d\n", *result);
}
```

**Rust:**
```rust
fn find_value(key: i32) -> Option<&i32> {
    if key_exists {
        Some(&value)
    } else {
        None
    }
}

if let Some(result) = find_value(42) {
    println!("{}", result);
}
```

**Pattern 3: Shared Ownership**

**C:**
```c
// Reference counting (manual)
typedef struct {
    int ref_count;
    int value;
} RefCounted;

RefCounted *acquire(RefCounted *ptr) {
    ptr->ref_count++;
    return ptr;
}

void release(RefCounted *ptr) {
    if (--ptr->ref_count == 0) {
        free(ptr);
    }
}
```

**Rust:**
```rust
use std::rc::Rc;

let value = Rc::new(42);
let shared = Rc::clone(&value);  // Increment ref count
// Both `value` and `shared` point to same data
// Automatically freed when last Rc is dropped
```

**Thread-safe version:**
```rust
use std::sync::Arc;

let value = Arc::new(42);
let shared = Arc::clone(&value);  // Thread-safe reference counting
```

### Lifetime and Borrowing

**C: Dangling Pointer**
```c
int *get_pointer(void) {
    int x = 42;
    return &x;  // UNDEFINED BEHAVIOR: x is on stack
}
```

**Rust: Compile Error**
```rust
fn get_pointer() -> &i32 {
    let x = 42;
    &x  // ERROR: x does not live long enough
}
```

**Fix: Return Owned Value**
```rust
fn get_value() -> i32 {
    let x = 42;
    x  // Move ownership to caller
}

// Or heap allocate
fn get_box() -> Box<i32> {
    Box::new(42)
}
```

**C: Struct with Pointer**
```c
typedef struct {
    char *name;  // Who owns this?
    int age;
} Person;

// Lifetime unclear - does Person own the name?
```

**Rust: Explicit Lifetime**
```rust
// Borrowed reference (doesn't own)
struct Person<'a> {
    name: &'a str,
    age: i32,
}

// Or owned (owns the name)
struct PersonOwned {
    name: String,
    age: i32,
}
```

---

## Module System Translation

### Header Files → Rust Modules

**C: Header/Implementation Split**
```c
// point.h
#ifndef POINT_H
#define POINT_H

typedef struct {
    double x;
    double y;
} Point;

Point point_create(double x, double y);
double point_distance(const Point *p1, const Point *p2);

#endif
```

```c
// point.c
#include "point.h"
#include <math.h>

Point point_create(double x, double y) {
    Point p = {x, y};
    return p;
}

double point_distance(const Point *p1, const Point *p2) {
    double dx = p2->x - p1->x;
    double dy = p2->y - p1->y;
    return sqrt(dx*dx + dy*dy);
}
```

**Rust: Single File Module**
```rust
// point.rs
pub struct Point {
    pub x: f64,
    pub y: f64,
}

impl Point {
    pub fn new(x: f64, y: f64) -> Self {
        Point { x, y }
    }

    pub fn distance(&self, other: &Point) -> f64 {
        let dx = other.x - self.x;
        let dy = other.y - self.y;
        (dx*dx + dy*dy).sqrt()
    }
}
```

### Include Guards → Module System

| C Pattern | Rust Pattern | Why |
|-----------|--------------|-----|
| `#ifndef` / `#define` / `#endif` | Not needed | Module system prevents double inclusion |
| `#pragma once` | Not needed | Same reason |
| `#include "header.h"` | `use crate::module;` | Explicit imports |
| `#include <stdlib.h>` | `use std::collections::HashMap;` | Standard library imports |
| Forward declarations | Not needed | Compiler resolves order |

### Visibility

| C Pattern | Rust Pattern | Notes |
|-----------|--------------|-------|
| `static int x;` (file-local) | `static X: i32` (private by default) | Module-private |
| Public function | `pub fn name()` | Explicitly public |
| Public struct | `pub struct Name` | Explicitly public |
| Private helper | `fn helper()` (no `pub`) | Private by default |
| Opaque type | `pub struct Handle { _private: () }` | Hidden internals |

---

## Error Handling Translation

### Error Codes → Result Types

**C: Error Code Pattern**
```c
#define SUCCESS 0
#define ERROR_NULL_POINTER -1
#define ERROR_OUT_OF_MEMORY -2
#define ERROR_INVALID_INPUT -3

int parse_number(const char *input, int *output) {
    if (input == NULL || output == NULL) {
        return ERROR_NULL_POINTER;
    }

    char *endptr;
    long val = strtol(input, &endptr, 10);

    if (endptr == input) {
        return ERROR_INVALID_INPUT;
    }

    *output = (int)val;
    return SUCCESS;
}

// Usage
int value;
int result = parse_number("42", &value);
if (result != SUCCESS) {
    fprintf(stderr, "Error: %d\n", result);
    return result;
}
```

**Rust: Result Type**
```rust
#[derive(Debug)]
enum ParseError {
    InvalidInput,
    OutOfRange,
}

fn parse_number(input: &str) -> Result<i32, ParseError> {
    input.parse::<i32>()
        .map_err(|_| ParseError::InvalidInput)
}

// Usage
match parse_number("42") {
    Ok(value) => println!("Parsed: {}", value),
    Err(e) => eprintln!("Error: {:?}", e),
}

// Or with ? operator
fn process() -> Result<(), ParseError> {
    let value = parse_number("42")?;  // Propagates error
    println!("Value: {}", value);
    Ok(())
}
```

**Why this translation:**
- Result type is explicit in function signature
- Compiler enforces error handling (cannot ignore Result)
- `?` operator provides concise error propagation
- Type system prevents mixing error types

### errno → Result

**C: errno Pattern**
```c
#include <stdio.h>
#include <errno.h>
#include <string.h>

FILE *open_file(const char *path) {
    FILE *file = fopen(path, "r");
    if (file == NULL) {
        fprintf(stderr, "Error opening file: %s\n", strerror(errno));
        return NULL;
    }
    return file;
}
```

**Rust: Result with std::io::Error**
```rust
use std::fs::File;
use std::io;

fn open_file(path: &str) -> io::Result<File> {
    File::open(path)
}

// Usage
match open_file("data.txt") {
    Ok(file) => { /* use file */ },
    Err(e) => eprintln!("Error opening file: {}", e),
}
```

### goto cleanup → RAII

**C: goto for Cleanup**
```c
int process_file(const char *path) {
    FILE *file = NULL;
    char *buffer = NULL;
    int result = -1;

    file = fopen(path, "r");
    if (file == NULL) {
        goto cleanup;
    }

    buffer = malloc(1024);
    if (buffer == NULL) {
        goto cleanup;
    }

    // Process file...
    result = 0;

cleanup:
    free(buffer);
    if (file != NULL) {
        fclose(file);
    }
    return result;
}
```

**Rust: Automatic Cleanup with Drop**
```rust
use std::fs::File;
use std::io::{self, Read};

fn process_file(path: &str) -> io::Result<()> {
    let mut file = File::open(path)?;
    let mut buffer = String::new();

    file.read_to_string(&mut buffer)?;

    // Process buffer...

    Ok(())
    // file and buffer automatically cleaned up
}
```

**Why this translation:**
- Drop trait ensures cleanup even on early return
- No need for explicit cleanup labels
- Exception-safe (cleanup happens even if panic occurs)

---

## Concurrency Translation

### pthreads → std::thread

**C: pthread Creation**
```c
#include <pthread.h>
#include <stdio.h>

void *thread_function(void *arg) {
    int value = *(int *)arg;
    printf("Thread received: %d\n", value);
    return NULL;
}

int main(void) {
    pthread_t thread;
    int input = 42;

    pthread_create(&thread, NULL, thread_function, &input);
    pthread_join(thread, NULL);

    return 0;
}
```

**Rust: std::thread**
```rust
use std::thread;

fn main() {
    let input = 42;

    let handle = thread::spawn(move || {
        println!("Thread received: {}", input);
    });

    handle.join().unwrap();
}
```

**Why this translation:**
- Rust's type system prevents data races at compile time
- `move` closure transfers ownership to thread
- Cannot accidentally share non-thread-safe data

### Mutexes

**C: pthread_mutex**
```c
#include <pthread.h>

typedef struct {
    int counter;
    pthread_mutex_t mutex;
} SafeCounter;

void counter_init(SafeCounter *c) {
    c->counter = 0;
    pthread_mutex_init(&c->mutex, NULL);
}

void counter_increment(SafeCounter *c) {
    pthread_mutex_lock(&c->mutex);
    c->counter++;
    pthread_mutex_unlock(&c->mutex);
}

void counter_destroy(SafeCounter *c) {
    pthread_mutex_destroy(&c->mutex);
}
```

**Rust: std::sync::Mutex**
```rust
use std::sync::{Arc, Mutex};

struct SafeCounter {
    counter: Arc<Mutex<i32>>,
}

impl SafeCounter {
    fn new() -> Self {
        SafeCounter {
            counter: Arc::new(Mutex::new(0)),
        }
    }

    fn increment(&self) {
        let mut count = self.counter.lock().unwrap();
        *count += 1;
        // Lock automatically released when `count` goes out of scope
    }

    fn get(&self) -> i32 {
        *self.counter.lock().unwrap()
    }
}
```

**Why this translation:**
- Lock guard (RAII) ensures mutex is always unlocked
- Cannot access data without holding lock (compile-time guarantee)
- Arc provides thread-safe reference counting

### Atomics

**C: C11 Atomics**
```c
#include <stdatomic.h>

atomic_int counter = ATOMIC_VAR_INIT(0);

void increment(void) {
    atomic_fetch_add(&counter, 1);
}

int get_value(void) {
    return atomic_load(&counter);
}
```

**Rust: std::sync::atomic**
```rust
use std::sync::atomic::{AtomicI32, Ordering};

static COUNTER: AtomicI32 = AtomicI32::new(0);

fn increment() {
    COUNTER.fetch_add(1, Ordering::SeqCst);
}

fn get_value() -> i32 {
    COUNTER.load(Ordering::SeqCst)
}
```

**Memory Ordering Comparison:**

| C11 | Rust | Description |
|-----|------|-------------|
| `memory_order_relaxed` | `Ordering::Relaxed` | No synchronization |
| `memory_order_acquire` | `Ordering::Acquire` | Load barrier |
| `memory_order_release` | `Ordering::Release` | Store barrier |
| `memory_order_acq_rel` | `Ordering::AcqRel` | Both barriers |
| `memory_order_seq_cst` | `Ordering::SeqCst` | Sequential consistency (default) |

---

## Serialization Translation

### Binary Serialization

**C: struct write/read**
```c
#include <stdio.h>

typedef struct {
    uint32_t id;
    char name[50];
    float score;
} Record;

int serialize(const Record *record, const char *filename) {
    FILE *file = fopen(filename, "wb");
    if (file == NULL) return -1;

    size_t written = fwrite(record, sizeof(Record), 1, file);
    fclose(file);

    return written == 1 ? 0 : -1;
}

int deserialize(Record *record, const char *filename) {
    FILE *file = fopen(filename, "rb");
    if (file == NULL) return -1;

    size_t read = fread(record, sizeof(Record), 1, file);
    fclose(file);

    return read == 1 ? 0 : -1;
}
```

**Rust: bincode / serde**
```rust
use serde::{Serialize, Deserialize};
use std::fs::File;
use std::io::{self, Write, Read};

#[derive(Serialize, Deserialize)]
struct Record {
    id: u32,
    name: String,  // Dynamic size
    score: f32,
}

fn serialize(record: &Record, filename: &str) -> io::Result<()> {
    let encoded = bincode::serialize(record).unwrap();
    let mut file = File::create(filename)?;
    file.write_all(&encoded)?;
    Ok(())
}

fn deserialize(filename: &str) -> io::Result<Record> {
    let mut file = File::open(filename)?;
    let mut buffer = Vec::new();
    file.read_to_end(&mut buffer)?;
    let record = bincode::deserialize(&buffer).unwrap();
    Ok(record)
}
```

### JSON Serialization

**C: cJSON Library**
```c
#include <cJSON.h>

typedef struct {
    char name[50];
    int age;
} User;

char *user_to_json(const User *user) {
    cJSON *root = cJSON_CreateObject();
    cJSON_AddStringToObject(root, "name", user->name);
    cJSON_AddNumberToObject(root, "age", user->age);

    char *json = cJSON_Print(root);
    cJSON_Delete(root);
    return json;  // Caller must free
}
```

**Rust: serde_json**
```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
struct User {
    name: String,
    age: i32,
}

fn user_to_json(user: &User) -> String {
    serde_json::to_string(user).unwrap()
}

fn user_from_json(json: &str) -> Result<User, serde_json::Error> {
    serde_json::from_str(json)
}
```

---

## Build System Translation

### Makefiles → Cargo

**C: Makefile**
```makefile
CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -O2
LDFLAGS = -lm

SRCS = main.c utils.c parser.c
OBJS = $(SRCS:.c=.o)
TARGET = myapp

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(OBJS) -o $(TARGET) $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

.PHONY: all clean
```

**Rust: Cargo.toml**
```toml
[package]
name = "myapp"
version = "0.1.0"
edition = "2021"

[dependencies]
# No math library needed - built-in

[profile.release]
opt-level = 2
```

**Build commands:**
```bash
# C
make
make clean

# Rust
cargo build
cargo build --release
cargo clean
```

### CMake → Cargo

**C: CMakeLists.txt**
```cmake
cmake_minimum_required(VERSION 3.10)
project(MyApp C)

set(CMAKE_C_STANDARD 11)

add_executable(myapp
    src/main.c
    src/utils.c
    src/parser.c
)

target_link_libraries(myapp m)
```

**Rust: Project Structure**
```
myapp/
├── Cargo.toml
└── src/
    ├── main.rs
    ├── utils.rs
    └── parser.rs
```

---

## Testing Translation

### Unity/CMocka → Rust Tests

**C: Unity Framework**
```c
#include "unity.h"

int add(int a, int b) {
    return a + b;
}

void test_add_positive(void) {
    TEST_ASSERT_EQUAL_INT(5, add(2, 3));
}

void test_add_negative(void) {
    TEST_ASSERT_EQUAL_INT(0, add(-1, 1));
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_add_positive);
    RUN_TEST(test_add_negative);
    return UNITY_END();
}
```

**Rust: Built-in Tests**
```rust
fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_positive() {
        assert_eq!(add(2, 3), 5);
    }

    #[test]
    fn test_add_negative() {
        assert_eq!(add(-1, 1), 0);
    }
}
```

**Run tests:**
```bash
# C (with Unity)
gcc test.c unity.c -o test && ./test

# Rust
cargo test
```

---

## Metaprogramming Translation

### Preprocessor Macros → Rust Macros

**C: Object-like Macros**
```c
#define PI 3.14159
#define MAX_SIZE 1024
#define VERSION "1.0.0"
```

**Rust: Constants**
```rust
const PI: f64 = 3.14159;
const MAX_SIZE: usize = 1024;
const VERSION: &str = "1.0.0";
```

**C: Function-like Macros**
```c
#define SQUARE(x) ((x) * (x))
#define MAX(a, b) ((a) > (b) ? (a) : (b))

int result = SQUARE(5);  // 25
```

**Rust: Macros or Inline Functions**
```rust
// Macro (compile-time)
macro_rules! square {
    ($x:expr) => { $x * $x };
}

// Inline function (preferred for simple cases)
#[inline]
fn max<T: Ord>(a: T, b: T) -> T {
    if a > b { a } else { b }
}

let result = square!(5);  // 25
let result = max(10, 20); // 20
```

**C: Multi-line Macros**
```c
#define SWAP(a, b, type) do { \
    type temp = (a); \
    (a) = (b); \
    (b) = temp; \
} while(0)
```

**Rust: Macro**
```rust
macro_rules! swap {
    ($a:expr, $b:expr) => {
        {
            let temp = $a;
            $a = $b;
            $b = temp;
        }
    };
}

// Or use std::mem::swap
use std::mem;
mem::swap(&mut a, &mut b);
```

**C: Conditional Compilation**
```c
#ifdef DEBUG
    #define LOG(msg) printf("DEBUG: %s\n", msg)
#else
    #define LOG(msg) ((void)0)
#endif
```

**Rust: Conditional Compilation**
```rust
#[cfg(debug_assertions)]
macro_rules! log {
    ($msg:expr) => { println!("DEBUG: {}", $msg) };
}

#[cfg(not(debug_assertions))]
macro_rules! log {
    ($msg:expr) => {};
}

// Or use cfg! macro
if cfg!(debug_assertions) {
    println!("DEBUG: {}", msg);
}
```

---

## Common Idioms

### Pattern 1: String Handling

**C: Null-Terminated Strings**
```c
#include <string.h>
#include <stdlib.h>

char *concat(const char *s1, const char *s2) {
    size_t len = strlen(s1) + strlen(s2) + 1;
    char *result = malloc(len);
    if (result == NULL) return NULL;

    strcpy(result, s1);
    strcat(result, s2);
    return result;  // Caller must free
}
```

**Rust: String/&str**
```rust
fn concat(s1: &str, s2: &str) -> String {
    format!("{}{}", s1, s2)
    // Or: s1.to_string() + s2
    // Or: [s1, s2].concat()
}

// No manual memory management needed
```

### Pattern 2: Array Manipulation

**C: Manual Bounds Checking**
```c
int find_max(const int *arr, size_t len) {
    if (len == 0) {
        return -1;  // Error indicator
    }

    int max = arr[0];
    for (size_t i = 1; i < len; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    return max;
}
```

**Rust: Iterators**
```rust
fn find_max(arr: &[i32]) -> Option<i32> {
    arr.iter().max().copied()
}

// Or with pattern matching
fn find_max_explicit(arr: &[i32]) -> Option<i32> {
    match arr.first() {
        None => None,
        Some(&first) => {
            let max = arr.iter().fold(first, |max, &x| max.max(x));
            Some(max)
        }
    }
}
```

### Pattern 3: Callback Functions

**C: Callback with void* Context**
```c
typedef void (*callback_t)(int value, void *context);

void process_array(const int *arr, size_t len, callback_t cb, void *ctx) {
    for (size_t i = 0; i < len; i++) {
        cb(arr[i], ctx);
    }
}

void print_cb(int value, void *ctx) {
    const char *prefix = (const char *)ctx;
    printf("%s%d\n", prefix, value);
}

// Usage
process_array(arr, len, print_cb, "Value: ");
```

**Rust: Closures**
```rust
fn process_array<F>(arr: &[i32], mut cb: F)
where
    F: FnMut(i32),
{
    for &value in arr {
        cb(value);
    }
}

// Usage
let prefix = "Value: ";
process_array(&arr, |value| {
    println!("{}{}", prefix, value);
});
```

---

## Common Pitfalls

### 1. Use-After-Free

**C: Dangling Pointer**
```c
int *ptr = malloc(sizeof(int));
*ptr = 42;
free(ptr);
printf("%d\n", *ptr);  // UNDEFINED BEHAVIOR
```

**Rust: Compile Error**
```rust
let ptr = Box::new(42);
drop(ptr);  // Explicit drop
// println!("{}", *ptr);  // ERROR: use of moved value
```

**Why this matters:**
- Rust ownership system prevents use-after-free at compile time
- Cannot access value after it has been moved or dropped

### 2. Double-Free

**C: Double Free**
```c
char *str = malloc(100);
free(str);
free(str);  // UNDEFINED BEHAVIOR
```

**Rust: Impossible**
```rust
let s = Box::new(String::from("hello"));
drop(s);
// drop(s);  // ERROR: use of moved value
```

### 3. Buffer Overflow

**C: No Bounds Checking**
```c
int arr[10];
arr[15] = 42;  // UNDEFINED BEHAVIOR
```

**Rust: Panic or Compile Error**
```rust
let mut arr = [0; 10];
// arr[15] = 42;  // PANIC at runtime (in debug mode)

// Better: use safe access
if let Some(elem) = arr.get_mut(15) {
    *elem = 42;
} else {
    println!("Index out of bounds");
}
```

### 4. NULL Pointer Dereference

**C: NULL Check Required**
```c
int *ptr = get_value();
if (ptr == NULL) {
    return -1;
}
*ptr = 10;  // Safe only if check above
```

**Rust: Type-Safe Nullability**
```rust
let ptr: Option<Box<i32>> = get_value();
match ptr {
    Some(mut p) => *p = 10,
    None => return Err("NULL pointer"),
}

// Or with ? operator
let mut p = get_value()?;
*p = 10;
```

### 5. Integer Overflow

**C: Undefined Behavior**
```c
int x = INT_MAX;
x++;  // UNDEFINED BEHAVIOR
```

**Rust: Panic (Debug) or Wrap (Release)**
```rust
let x = i32::MAX;
// let y = x + 1;  // PANIC in debug mode

// Explicit behavior
let y = x.wrapping_add(1);  // Wrap around
let y = x.checked_add(1);   // Returns Option<i32>
let y = x.saturating_add(1); // Saturate at MAX
```

---

## Tooling

### c2rust

Automated C to Rust translation tool (produces unsafe Rust as starting point):

```bash
# Install
cargo install c2rust

# Translate C code
c2rust transpile compile_commands.json

# Produces .rs files with unsafe Rust code
# Manual cleanup needed to make code idiomatic
```

**Output characteristics:**
- Generates unsafe Rust that matches C behavior
- Preserves C-style pointer usage (raw pointers)
- Good starting point but requires manual refactoring
- Use as scaffolding, not final code

### Incremental Migration with FFI

**Strategy:** Gradually replace C modules with Rust while maintaining C API:

**C header (legacy):**
```c
// api.h
int process_data(const char *input, char *output, size_t output_len);
```

**Rust implementation:**
```rust
use std::ffi::{CStr, CString};
use std::os::raw::c_char;

#[no_mangle]
pub extern "C" fn process_data(
    input: *const c_char,
    output: *mut c_char,
    output_len: usize,
) -> i32 {
    // Convert C string to Rust
    let input = unsafe {
        assert!(!input.is_null());
        CStr::from_ptr(input)
    };

    let input_str = match input.to_str() {
        Ok(s) => s,
        Err(_) => return -1,
    };

    // Pure Rust logic
    let result = process(input_str);

    // Convert back to C string
    let result_cstring = CString::new(result).unwrap();
    let bytes = result_cstring.as_bytes_with_nul();

    if bytes.len() > output_len {
        return -2;  // Buffer too small
    }

    unsafe {
        std::ptr::copy_nonoverlapping(
            bytes.as_ptr(),
            output as *mut u8,
            bytes.len(),
        );
    }

    0  // Success
}

fn process(input: &str) -> String {
    // Safe, idiomatic Rust code
    input.to_uppercase()
}
```

### Build Integration

**Cargo with C Dependencies:**
```toml
[build-dependencies]
cc = "1.0"
```

**build.rs:**
```rust
fn main() {
    cc::Build::new()
        .file("src/legacy/utils.c")
        .compile("utils");
}
```

---

## Migration Strategies

### Strategy 1: Clean Slate (Full Rewrite)

**When to use:**
- Small to medium codebase
- Well-defined requirements
- Time to rewrite from scratch
- Want to modernize architecture

**Approach:**
1. Understand C codebase behavior
2. Design Rust architecture
3. Implement in idiomatic Rust
4. Test against C version (golden tests)

### Strategy 2: Incremental (FFI Boundary)

**When to use:**
- Large codebase
- Need continuous operation
- Limited resources
- Risk-averse

**Approach:**
1. Identify module boundaries
2. Create FFI wrappers for C modules
3. Rewrite one module at a time in Rust
4. Expose Rust module with C-compatible FFI
5. Gradually replace C modules

### Strategy 3: c2rust Then Refactor

**When to use:**
- Very large codebase
- Complex pointer logic
- Need mechanical translation first

**Approach:**
1. Run c2rust on codebase
2. Get compiling unsafe Rust
3. Write comprehensive tests
4. Incrementally refactor to safe Rust
5. Replace raw pointers with references
6. Replace manual memory management with RAII

---

## Examples

### Example 1: Simple - Linked List Node

**Before (C):**
```c
struct Node {
    int value;
    struct Node *next;
};

struct Node *create_node(int value) {
    struct Node *node = malloc(sizeof(struct Node));
    if (node == NULL) {
        return NULL;
    }
    node->value = value;
    node->next = NULL;
    return node;
}

void free_list(struct Node *head) {
    while (head != NULL) {
        struct Node *next = head->next;
        free(head);
        head = next;
    }
}
```

**After (Rust):**
```rust
struct Node {
    value: i32,
    next: Option<Box<Node>>,
}

impl Node {
    fn new(value: i32) -> Box<Node> {
        Box::new(Node {
            value,
            next: None,
        })
    }
}

// Automatic cleanup via Drop trait
// No manual free_list needed
```

### Example 2: Medium - String Buffer

**Before (C):**
```c
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *data;
    size_t len;
    size_t capacity;
} StringBuffer;

StringBuffer *strbuf_create(size_t capacity) {
    StringBuffer *buf = malloc(sizeof(StringBuffer));
    if (buf == NULL) return NULL;

    buf->data = malloc(capacity);
    if (buf->data == NULL) {
        free(buf);
        return NULL;
    }

    buf->data[0] = '\0';
    buf->len = 0;
    buf->capacity = capacity;
    return buf;
}

int strbuf_append(StringBuffer *buf, const char *str) {
    size_t str_len = strlen(str);
    if (buf->len + str_len + 1 > buf->capacity) {
        size_t new_cap = buf->capacity * 2;
        char *new_data = realloc(buf->data, new_cap);
        if (new_data == NULL) return -1;

        buf->data = new_data;
        buf->capacity = new_cap;
    }

    strcpy(buf->data + buf->len, str);
    buf->len += str_len;
    return 0;
}

void strbuf_destroy(StringBuffer *buf) {
    free(buf->data);
    free(buf);
}
```

**After (Rust):**
```rust
struct StringBuffer {
    data: String,
}

impl StringBuffer {
    fn new() -> Self {
        StringBuffer {
            data: String::new(),
        }
    }

    fn with_capacity(capacity: usize) -> Self {
        StringBuffer {
            data: String::with_capacity(capacity),
        }
    }

    fn append(&mut self, s: &str) {
        self.data.push_str(s);
        // Automatic reallocation if needed
    }

    fn as_str(&self) -> &str {
        &self.data
    }
}

// Automatic cleanup via Drop trait

// Or just use String directly:
let mut s = String::new();
s.push_str("Hello");
s.push_str(" World");
```

### Example 3: Complex - Thread-Safe Queue

**Before (C):**
```c
#include <pthread.h>
#include <stdlib.h>

typedef struct Node {
    void *data;
    struct Node *next;
} Node;

typedef struct {
    Node *head;
    Node *tail;
    pthread_mutex_t mutex;
    pthread_cond_t cond;
} Queue;

Queue *queue_create(void) {
    Queue *q = malloc(sizeof(Queue));
    if (q == NULL) return NULL;

    q->head = q->tail = NULL;
    pthread_mutex_init(&q->mutex, NULL);
    pthread_cond_init(&q->cond, NULL);
    return q;
}

int queue_push(Queue *q, void *data) {
    Node *node = malloc(sizeof(Node));
    if (node == NULL) return -1;

    node->data = data;
    node->next = NULL;

    pthread_mutex_lock(&q->mutex);

    if (q->tail == NULL) {
        q->head = q->tail = node;
    } else {
        q->tail->next = node;
        q->tail = node;
    }

    pthread_cond_signal(&q->cond);
    pthread_mutex_unlock(&q->mutex);

    return 0;
}

void *queue_pop(Queue *q) {
    pthread_mutex_lock(&q->mutex);

    while (q->head == NULL) {
        pthread_cond_wait(&q->cond, &q->mutex);
    }

    Node *node = q->head;
    void *data = node->data;

    q->head = node->next;
    if (q->head == NULL) {
        q->tail = NULL;
    }

    pthread_mutex_unlock(&q->mutex);

    free(node);
    return data;
}

void queue_destroy(Queue *q) {
    pthread_mutex_destroy(&q->mutex);
    pthread_cond_destroy(&q->cond);
    // ... free remaining nodes ...
    free(q);
}
```

**After (Rust):**
```rust
use std::sync::{Arc, Mutex, Condvar};
use std::collections::VecDeque;

struct Queue<T> {
    data: Arc<(Mutex<VecDeque<T>>, Condvar)>,
}

impl<T> Queue<T> {
    fn new() -> Self {
        Queue {
            data: Arc::new((Mutex::new(VecDeque::new()), Condvar::new())),
        }
    }

    fn push(&self, item: T) {
        let (lock, cvar) = &*self.data;
        let mut queue = lock.lock().unwrap();
        queue.push_back(item);
        cvar.notify_one();
    }

    fn pop(&self) -> T {
        let (lock, cvar) = &*self.data;
        let mut queue = lock.lock().unwrap();

        while queue.is_empty() {
            queue = cvar.wait(queue).unwrap();
        }

        queue.pop_front().unwrap()
    }
}

impl<T> Clone for Queue<T> {
    fn clone(&self) -> Self {
        Queue {
            data: Arc::clone(&self.data),
        }
    }
}

// Automatic cleanup via Drop trait
// Type-safe: cannot push/pop wrong types
// Send + Sync: compiler verifies thread safety
```

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `convert-typescript-rust` - High-level to Rust conversion patterns
- `convert-golang-rust` - GC to ownership conversion patterns
- `lang-c-dev` - C development patterns
- `lang-rust-dev` - Rust development patterns

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - Thread safety patterns
- `patterns-serialization-dev` - Data serialization patterns
- `patterns-metaprogramming-dev` - Macro patterns
