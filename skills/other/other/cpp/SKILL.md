---
name: cpp
description: C++ modern C++17/20/23 with STL, smart pointers, and performance optimization. Use for .cpp files.
---

# C++

Modern C++ development with smart pointers, RAII, and performance optimization.

## When to Use

- Working with `.cpp` or `.hpp` files
- Systems programming and embedded
- Game development with Unreal Engine
- Performance-critical applications

## Quick Start

```cpp
#include <memory>
#include <string>
#include <vector>

class User {
public:
    User(std::string name, std::string email)
        : name_(std::move(name)), email_(std::move(email)) {}

    const std::string& name() const { return name_; }
    const std::string& email() const { return email_; }

private:
    std::string name_;
    std::string email_;
};

auto user = std::make_unique<User>("John", "john@example.com");
```

## Core Concepts

### Smart Pointers

```cpp
// unique_ptr - exclusive ownership
auto user = std::make_unique<User>("John");

// shared_ptr - shared ownership
auto shared = std::make_shared<Resource>();
auto copy = shared;  // ref count increases

// weak_ptr - non-owning observer
std::weak_ptr<Resource> observer = shared;
if (auto locked = observer.lock()) {
    // safe to use
}

// Never use raw new/delete for ownership
```

### Move Semantics

```cpp
class Buffer {
public:
    Buffer(size_t size) : data_(new char[size]), size_(size) {}

    // Move constructor
    Buffer(Buffer&& other) noexcept
        : data_(other.data_), size_(other.size_) {
        other.data_ = nullptr;
        other.size_ = 0;
    }

    // Move assignment
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            data_ = other.data_;
            size_ = other.size_;
            other.data_ = nullptr;
            other.size_ = 0;
        }
        return *this;
    }

    ~Buffer() { delete[] data_; }

private:
    char* data_;
    size_t size_;
};
```

## Common Patterns

### Modern C++ Features

```cpp
// Structured bindings (C++17)
auto [name, age] = std::make_pair("John", 25);
for (const auto& [key, value] : map) { /* ... */ }

// std::optional (C++17)
std::optional<User> findUser(int id) {
    if (exists) return User{...};
    return std::nullopt;
}

// Concepts (C++20)
template<typename T>
concept Numeric = std::is_arithmetic_v<T>;

template<Numeric T>
T add(T a, T b) { return a + b; }

// Ranges (C++20)
auto result = numbers
    | std::views::filter([](int n) { return n % 2 == 0; })
    | std::views::transform([](int n) { return n * 2; });
```

### RAII Pattern

```cpp
class FileHandle {
public:
    explicit FileHandle(const char* path)
        : file_(std::fopen(path, "r")) {
        if (!file_) throw std::runtime_error("Cannot open file");
    }

    ~FileHandle() { if (file_) std::fclose(file_); }

    // Delete copy
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;

    // Allow move
    FileHandle(FileHandle&& other) noexcept : file_(other.file_) {
        other.file_ = nullptr;
    }

private:
    FILE* file_;
};
```

## Best Practices

**Do**:

- Use smart pointers for ownership
- Apply RAII for resource management
- Use `const` and `constexpr` liberally
- Prefer `std::string_view` for read-only strings

**Don't**:

- Use raw `new`/`delete` for ownership
- Return raw pointers from functions
- Use C-style casts (use `static_cast`)
- Ignore compiler warnings

## Troubleshooting

| Error              | Cause                           | Solution                       |
| ------------------ | ------------------------------- | ------------------------------ |
| Segmentation fault | Null pointer or buffer overflow | Use sanitizers, smart pointers |
| Memory leak        | Missing delete                  | Use RAII, smart pointers       |
| Undefined behavior | Dangling reference              | Ensure lifetime validity       |

## References

- [C++ Reference](https://en.cppreference.com/)
- [ISO C++ Guidelines](https://isocpp.github.io/CppCoreGuidelines/)
