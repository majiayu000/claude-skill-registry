---
name: cpp-dev-guidelines
description: C++ development guidelines for modern C++17/20 projects. Use when creating C++ classes, functions, headers, or working with CMake, templates, smart pointers, RAII, memory management, STL containers, multithreading, or C++ best practices. Covers project structure, modern C++ idioms, build systems, testing with GoogleTest/Catch2, and performance considerations.
---

# C++ Development Guidelines

## Purpose

Establish consistency and best practices for modern C++ development (C++17/20), covering memory safety, build systems, testing, and project organization.

## When to Use This Skill

Automatically activates when working on:
- Creating or modifying C++ files (`.cpp`, `.hpp`, `.h`, `.cc`)
- Writing classes, functions, or templates
- CMake configuration (`CMakeLists.txt`)
- Memory management and smart pointers
- Multithreading and concurrency
- Template metaprogramming
- Testing with GoogleTest or Catch2

---

## Quick Start

### New C++ Project Checklist

- [ ] **Project structure**: Separate include/src directories
- [ ] **CMakeLists.txt**: Modern CMake (3.14+)
- [ ] **Compiler flags**: Warnings enabled, sanitizers in debug
- [ ] **Smart pointers**: No raw `new`/`delete`
- [ ] **Tests**: GoogleTest or Catch2
- [ ] **Formatting**: clang-format config
- [ ] **Static analysis**: clang-tidy integration

### New Class Checklist

- [ ] Header guard or `#pragma once`
- [ ] Rule of 0/5 considered
- [ ] RAII for resources
- [ ] `const` correctness
- [ ] `noexcept` where appropriate
- [ ] Unit tests

---

## Project Structure

### Recommended Layout

```
project/
├── CMakeLists.txt              # Root CMake
├── cmake/
│   └── modules/                # Custom CMake modules
├── include/
│   └── myproject/
│       ├── core/
│       │   └── module.hpp
│       └── utils/
│           └── helpers.hpp
├── src/
│   ├── CMakeLists.txt
│   ├── core/
│   │   └── module.cpp
│   └── utils/
│       └── helpers.cpp
├── tests/
│   ├── CMakeLists.txt
│   ├── test_module.cpp
│   └── test_helpers.cpp
├── apps/                       # Executables
│   ├── CMakeLists.txt
│   └── main.cpp
├── third_party/                # External deps
├── .clang-format
├── .clang-tidy
└── README.md
```

### Header/Source Pairing

```
include/myproject/widget.hpp    # Public header
src/widget.cpp                  # Implementation
tests/test_widget.cpp           # Tests
```

---

## Core Principles (7 Key Rules)

### 1. RAII: Resource Acquisition Is Initialization

```cpp
// ❌ NEVER: Manual resource management
void bad() {
    int* ptr = new int(42);
    // ... if exception thrown, memory leaks
    delete ptr;
}

// ✅ ALWAYS: RAII with smart pointers
void good() {
    auto ptr = std::make_unique<int>(42);
    // Automatically cleaned up, even on exception
}
```

### 2. Prefer Smart Pointers

```cpp
// Ownership semantics
std::unique_ptr<Widget> owner;      // Exclusive ownership
std::shared_ptr<Widget> shared;     // Shared ownership
std::weak_ptr<Widget> observer;     // Non-owning observer

// ✅ Factory functions
auto widget = std::make_unique<Widget>(args...);
auto shared = std::make_shared<Widget>(args...);

// ❌ NEVER use raw new/delete for ownership
Widget* raw = new Widget();  // Who deletes this?
```

### 3. Use `const` Everywhere Possible

```cpp
class Widget {
public:
    // ✅ const member function - doesn't modify state
    [[nodiscard]] int getValue() const noexcept { return value_; }

    // ✅ const reference parameter - no copy, no modify
    void process(const std::string& input);

    // ✅ const return for non-trivial types
    [[nodiscard]] const std::vector<int>& getData() const;

private:
    int value_;
};

// ✅ const local variables
const auto result = calculate();
```

### 4. Follow the Rule of 0/5

```cpp
// ✅ Rule of 0: Let compiler generate everything
class SimpleClass {
    std::string name_;
    std::vector<int> data_;
    // No need to define copy/move/destructor
};

// ✅ Rule of 5: If you define one, define all
class ResourceOwner {
public:
    ResourceOwner();
    ~ResourceOwner();
    ResourceOwner(const ResourceOwner& other);
    ResourceOwner& operator=(const ResourceOwner& other);
    ResourceOwner(ResourceOwner&& other) noexcept;
    ResourceOwner& operator=(ResourceOwner&& other) noexcept;
};
```

### 5. Use `[[nodiscard]]` for Return Values That Shouldn't Be Ignored

```cpp
// ✅ Prevent ignoring important returns
[[nodiscard]] bool initialize();
[[nodiscard]] std::optional<Result> tryParse(std::string_view input);
[[nodiscard]] ErrorCode processData();

// Caller must use the return value
auto success = initialize();  // OK
initialize();                  // Compiler warning
```

### 6. Prefer `std::string_view` for Read-Only String Parameters

```cpp
// ❌ Creates copy for string literals
void process(const std::string& input);
process("hello");  // Allocates!

// ✅ No allocation, works with any string-like type
void process(std::string_view input);
process("hello");           // No allocation
process(std::string{"hi"}); // Works too
process(c_str);             // Works too
```

### 7. Use `auto` Judiciously

```cpp
// ✅ Good uses of auto
auto iter = container.begin();           // Iterator types
auto ptr = std::make_unique<Widget>();   // Factory returns
auto [key, value] = *map_iter;           // Structured bindings
auto lambda = [](int x) { return x*2; }; // Lambdas

// ❌ Avoid when type is unclear
auto x = getValue();  // What type is this?

// ✅ Be explicit when it aids readability
int count = getCount();
std::string name = getName();
```

---

## Modern CMake (3.14+)

### Root CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.14)
project(MyProject VERSION 1.0.0 LANGUAGES CXX)

# C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Compiler warnings
add_compile_options(
    -Wall -Wextra -Wpedantic
    -Werror  # Treat warnings as errors
    $<$<CONFIG:Debug>:-fsanitize=address,undefined>
)
add_link_options(
    $<$<CONFIG:Debug>:-fsanitize=address,undefined>
)

# Library
add_library(mylib
    src/module.cpp
    src/helpers.cpp
)
target_include_directories(mylib PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

# Executable
add_executable(myapp apps/main.cpp)
target_link_libraries(myapp PRIVATE mylib)

# Testing
enable_testing()
add_subdirectory(tests)
```

### Modern Target Properties

```cmake
# ✅ Modern CMake: target-based
target_include_directories(mylib PUBLIC include/)
target_link_libraries(mylib PUBLIC dependency)
target_compile_features(mylib PUBLIC cxx_std_17)

# ❌ Old CMake: directory-based (avoid)
include_directories(include/)
link_libraries(dependency)
```

---

## Common Patterns

### Optional Values

```cpp
#include <optional>

std::optional<User> findUser(int id) {
    if (auto it = users_.find(id); it != users_.end()) {
        return it->second;
    }
    return std::nullopt;
}

// Usage
if (auto user = findUser(42)) {
    std::cout << user->name << '\n';
}
```

### Error Handling with Expected (C++23) or Result Types

```cpp
// C++23: std::expected
std::expected<Value, Error> parse(std::string_view input);

// Pre-C++23: Custom Result type or exceptions
template<typename T, typename E>
class Result {
    std::variant<T, E> data_;
public:
    bool has_value() const;
    T& value();
    E& error();
};
```

### Span for Array Views (C++20)

```cpp
#include <span>

// ✅ Works with any contiguous container
void process(std::span<const int> data) {
    for (int x : data) { /* ... */ }
}

std::vector<int> vec{1, 2, 3};
std::array<int, 3> arr{1, 2, 3};
int c_arr[] = {1, 2, 3};

process(vec);    // All work
process(arr);
process(c_arr);
```

---

## Testing with GoogleTest

```cpp
#include <gtest/gtest.h>
#include "myproject/widget.hpp"

class WidgetTest : public ::testing::Test {
protected:
    void SetUp() override {
        widget_ = std::make_unique<Widget>();
    }

    std::unique_ptr<Widget> widget_;
};

TEST_F(WidgetTest, InitializesCorrectly) {
    EXPECT_EQ(widget_->getValue(), 0);
}

TEST_F(WidgetTest, SetValueUpdatesState) {
    widget_->setValue(42);
    ASSERT_EQ(widget_->getValue(), 42);
}

TEST(WidgetDeathTest, NullPointerCrashes) {
    Widget* null = nullptr;
    ASSERT_DEATH(null->getValue(), "");
}
```

---

## Anti-Patterns to Avoid

❌ Raw `new`/`delete` for ownership
❌ C-style casts (`(int)x`) - use `static_cast<int>(x)`
❌ `using namespace std;` in headers
❌ Non-const global variables
❌ Returning raw pointers for ownership
❌ Implicit conversions (use `explicit`)
❌ `#define` for constants (use `constexpr`)
❌ C-style arrays (use `std::array` or `std::vector`)

---

## Resource Files

### [style-guide.md](resources/style-guide.md)
Google C++ Style Guide + Apptronik rules, TODO comments, error handling

### [idioms.md](resources/idioms.md)
C++ idioms: RAII, PIMPL, CRTP, Copy-and-Swap, SFINAE, Type Erasure, NVI

<!-- ### [cmake-guide.md](resources/cmake-guide.md)
Modern CMake patterns, find_package, FetchContent

### [memory-management.md](resources/memory-management.md)
Smart pointers, custom deleters, memory arenas

### [templates.md](resources/templates.md)
Template patterns, SFINAE, concepts (C++20)

### [concurrency.md](resources/concurrency.md)
std::thread, mutexes, atomics, thread pools

### [testing-guide.md](resources/testing-guide.md)
GoogleTest, Catch2, mocking, benchmarks -->

---

## Related Skills

- **python-dev-guidelines** - Python development patterns
- **error-tracking** - Error handling patterns
- **skill-developer** - Creating and managing skills

---

**Skill Status**: INITIAL ✅
**Line Count**: < 500 ✅
**Progressive Disclosure**: Resource files for details ✅
