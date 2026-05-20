---
name: cpp-guide
description: |
  C/C++ language guardrails, patterns, and best practices for AI-assisted development.
  Use when working with C/C++ files (.c, .cpp, .h, .hpp), CMakeLists.txt, or when the user mentions C/C++.
  Provides RAII patterns, smart pointer guidelines, move semantics,
  and testing standards specific to this project's coding standards.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: language
  language: cpp
  extensions: ".c,.cpp,.cc,.cxx,.h,.hpp,.hxx"
---

# C/C++ Guide

> Applies to: C++20, Systems Programming, Embedded, Game Engines, High-Performance Computing

## Core Principles

1. **RAII Everywhere**: Every resource (memory, files, locks, sockets) is owned by an object whose destructor releases it
2. **Zero Raw Ownership**: Never use `new`/`delete` directly; use smart pointers and containers for all heap allocation
3. **Value Semantics by Default**: Pass and return by value; rely on move semantics and copy elision for performance
4. **Compile-Time over Run-Time**: Use `constexpr`, `static_assert`, concepts, and templates to catch errors at compile time
5. **Warnings Are Errors**: Build with `-Wall -Wextra -Wpedantic -Werror`; every warning is a latent bug

## Guardrails

### Standard & Compiler

- Use C++20 as the minimum standard (`-std=c++20` / `CMAKE_CXX_STANDARD 20`)
- Compile with at least `-Wall -Wextra -Wpedantic`; treat warnings as errors (`-Werror`)
- Enable sanitizers in debug builds: `-fsanitize=address,undefined`
- Use `static_assert` to verify assumptions about types, sizes, and alignments
- Set `CMAKE_EXPORT_COMPILE_COMMANDS ON` for clang-tidy and IDE integration
- Pin compiler minimum version in CI (e.g., GCC 12+, Clang 15+, MSVC 19.34+)

### Code Style

- Run `clang-format` before every commit (no exceptions)
- Run `clang-tidy` with project checks before every commit
- `snake_case` for functions, variables, namespaces, file names
- `PascalCase` for types (classes, structs, enums, concepts, type aliases)
- `SCREAMING_SNAKE_CASE` for macros and compile-time constants
- Prefer `enum class` over plain `enum` (scoped, no implicit conversion)
- Header include order: own header, project headers, third-party, standard library
- Use `#pragma once` or traditional include guards consistently (pick one)
- No `using namespace std;` in headers (allowed in `.cpp` function scope only)

### Memory Management

- **Default to stack allocation**; heap allocate only when lifetime or size requires it
- `std::unique_ptr` for single ownership (default smart pointer)
- `std::shared_ptr` only when ownership is genuinely shared; document why
- Use `std::make_unique` and `std::make_shared` (exception-safe, single allocation)
- Containers (`std::vector`, `std::string`, `std::array`) manage their own memory
- Use `std::span` for non-owning views into contiguous memory
- Use `std::string_view` for non-owning string references (read-only, no allocation)

### Error Handling

- Use exceptions for truly exceptional conditions (constructor failure, precondition violations)
- Use `std::optional<T>` for values that may be absent (replaces sentinel values)
- Use `std::variant<T, Error>` or `std::expected<T, E>` (C++23) for result types
- Mark functions `noexcept` when they do not throw (enables move optimization)
- Always catch by `const` reference: `catch (const std::exception& e)`
- Never catch `...` without rethrowing or logging (swallowed errors are bugs)

### Concurrency

- Prefer `std::jthread` over `std::thread` (automatic join, stop token support)
- Protect shared mutable state with `std::mutex` and `std::scoped_lock`
- Use `std::atomic` for lock-free shared counters and flags
- Never hold a lock while calling a callback or virtual function (deadlock risk)
- All concurrent code must pass ThreadSanitizer (`-fsanitize=thread`)
- Prefer `std::latch`, `std::barrier`, `std::counting_semaphore` (C++20) for coordination

## Project Structure

```
myproject/
├── CMakeLists.txt              # Root: project(), options, add_subdirectory()
├── cmake/                      # Shared CMake modules (warnings, sanitizers)
├── src/
│   ├── CMakeLists.txt          # Library/executable targets
│   ├── main.cpp                # Entry point (thin: parse args, call run)
│   ├── app.cpp / app.hpp
│   └── domain/
│       └── user.cpp / user.hpp
├── include/myproject/          # Public headers (for libraries)
├── tests/
│   ├── CMakeLists.txt          # GoogleTest / Catch2 targets
│   └── test_user.cpp
├── benchmarks/
├── .clang-format
└── .clang-tidy
```

- `main.cpp` should be thin: parse arguments, build config, call into library code
- One class per header/source pair; test files mirror source structure
- Use `FetchContent` or `find_package` for dependencies

### CMakeLists.txt Essentials

```cmake
cmake_minimum_required(VERSION 3.20)
project(myproject VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_compile_options(-Wall -Wextra -Wpedantic -Werror)

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    add_compile_options(-fsanitize=address,undefined -fno-omit-frame-pointer)
    add_link_options(-fsanitize=address,undefined)
endif()

add_subdirectory(src)
add_subdirectory(tests)
```

## Key Patterns

### RAII Resource Wrapper

```cpp
class FileHandle {
public:
    explicit FileHandle(const std::filesystem::path& path)
        : handle_(std::fopen(path.c_str(), "r")) {
        if (!handle_) {
            throw std::runtime_error("Failed to open: " + path.string());
        }
    }
    ~FileHandle() { if (handle_) std::fclose(handle_); }

    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;
    FileHandle(FileHandle&& other) noexcept : handle_(std::exchange(other.handle_, nullptr)) {}
    FileHandle& operator=(FileHandle&& other) noexcept {
        if (this != &other) { if (handle_) std::fclose(handle_); handle_ = std::exchange(other.handle_, nullptr); }
        return *this;
    }

    FILE* get() const noexcept { return handle_; }
private:
    FILE* handle_;
};
```

### Smart Pointers

```cpp
// unique_ptr: default choice, single ownership
auto user = std::make_unique<User>("alice", "alice@example.com");
process_user(*user);  // pass by reference, not pointer

// shared_ptr: only when ownership is genuinely shared
auto config = std::make_shared<Config>(load_config("app.toml"));
auto worker1 = std::jthread([config] { serve(config); });
auto worker2 = std::jthread([config] { monitor(config); });

// weak_ptr: break reference cycles, optional observation
class TreeNode {
    std::vector<std::shared_ptr<TreeNode>> children_;
    std::weak_ptr<TreeNode> parent_;  // non-owning back-reference
};
```

### Move Semantics: Rule of Zero / Five

```cpp
// Rule of Zero: prefer this. Let members manage resources.
struct UserRecord {
    std::string name;
    std::string email;
    std::vector<std::string> roles;
    // No special member functions needed -- std::string and std::vector handle everything.
};

// Rule of Five: only when managing a raw resource manually.
// See references/patterns.md for full RAII wrapper examples.
// Key rules: move constructors/assignment MUST be noexcept;
// use std::exchange to leave moved-from objects in a valid state.
```

### std::optional and std::variant

```cpp
// std::optional: replaces sentinel values (-1, nullptr, "")
std::optional<User> find_user(std::string_view email) {
    auto it = users_.find(std::string(email));
    if (it == users_.end()) return std::nullopt;
    return it->second;
}

if (auto user = find_user("alice@example.com")) {
    std::println("Found: {}", user->name);
}

// std::variant: type-safe tagged union
using ParseResult = std::variant<int, double, std::string>;

std::visit(overloaded{
    [](int v)                { std::println("int: {}", v); },
    [](double v)             { std::println("double: {}", v); },
    [](const std::string& v) { std::println("string: {}", v); },
}, result);
```

### Concepts (C++20)

```cpp
template<typename T>
concept Hashable = requires(T a) {
    { std::hash<T>{}(a) } -> std::convertible_to<std::size_t>;
};

template<Hashable Key, typename Value>
class Cache {
public:
    void put(const Key& key, Value value) { store_[key] = std::move(value); }
    std::optional<Value> get(const Key& key) const {
        auto it = store_.find(key);
        return it != store_.end() ? std::optional(it->second) : std::nullopt;
    }
private:
    std::unordered_map<Key, Value> store_;
};
```

### constexpr Computation

```cpp
constexpr int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
static_assert(factorial(5) == 120);

consteval auto make_lookup_table() {
    std::array<int, 256> table{};
    for (int i = 0; i < 256; ++i) table[i] = (i * i) % 256;
    return table;
}
constexpr auto kLookup = make_lookup_table();
```

### Ranges (C++20)

```cpp
auto active_user_emails(const std::vector<User>& users) {
    return users
        | std::views::filter([](const User& u) { return u.is_active; })
        | std::views::transform(&User::email);
}

auto top_scores = scores
    | std::views::filter([](int s) { return s > 0; })
    | std::views::transform([](int s) { return s * 100 / max_score; })
    | std::views::take(10);
```

### Structured Bindings

```cpp
for (const auto& [key, value] : config_map) {
    std::println("{} = {}", key, value);
}

auto [min_it, max_it] = std::minmax_element(data.begin(), data.end());

auto [ok, msg, code] = process_request(req);
if (!ok) { log_error(msg, code); }
```

## Testing

### GoogleTest

```cpp
class UserServiceTest : public ::testing::Test {
protected:
    void SetUp() override {
        db_ = std::make_unique<InMemoryDatabase>();
        service_ = std::make_unique<UserService>(*db_);
    }
    std::unique_ptr<InMemoryDatabase> db_;
    std::unique_ptr<UserService> service_;
};

TEST_F(UserServiceTest, CreateUserSucceeds) {
    auto user = service_->create_user("alice", "alice@example.com");
    EXPECT_EQ(user.name, "alice");
    EXPECT_EQ(user.email, "alice@example.com");
    EXPECT_FALSE(user.id.empty());
}

TEST_F(UserServiceTest, DuplicateEmailThrows) {
    service_->create_user("alice", "alice@example.com");
    EXPECT_THROW(service_->create_user("bob", "alice@example.com"), DuplicateEmailError);
}
```

### Catch2

```cpp
TEST_CASE("Parser handles valid input", "[parser]") {
    Parser parser;
    SECTION("integer literals") {
        auto result = parser.parse("42");
        REQUIRE(result.has_value());
        CHECK(std::get<int>(*result) == 42);
    }
    SECTION("empty input returns nullopt") {
        CHECK_FALSE(parser.parse("").has_value());
    }
}
```

### Testing Standards

- Test names describe behavior: `TEST(OrderService, CancelledOrderCannotBeShipped)`
- Use `TEST_F` with fixtures for shared setup/teardown
- `EXPECT_*` for non-fatal assertions; `ASSERT_*` only when continuation is meaningless
- Coverage target: >80% for libraries, >60% for applications
- Mock external dependencies with interfaces and dependency injection
- Run tests under AddressSanitizer and UndefinedBehaviorSanitizer in CI

## Tooling

### Essential Commands

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Debug    # Configure
cmake --build build -j$(nproc)             # Build (parallel)
cmake --build build --target test          # Run tests (CTest)
clang-format -i src/**/*.cpp src/**/*.hpp  # Format
clang-tidy src/*.cpp -- -std=c++20         # Static analysis
gcovr --root . --html -o coverage.html     # Coverage report
```

### clang-format Configuration

```yaml
# .clang-format
BasedOnStyle: Google
IndentWidth: 4
ColumnLimit: 100
PointerAlignment: Left
SortIncludes: CaseInsensitive
```

### clang-tidy Configuration

```yaml
# .clang-tidy
Checks: >
  -*, bugprone-*, cert-*, cppcoreguidelines-*, misc-*,
  modernize-*, performance-*, readability-*,
  -modernize-use-trailing-return-type
WarningsAsErrors: '*'
HeaderFilterRegex: 'src/.*'
```

### Sanitizers Reference

| Sanitizer | Flag | Catches |
|-----------|------|---------|
| AddressSanitizer | `-fsanitize=address` | Buffer overflow, use-after-free, leaks |
| UndefinedBehaviorSanitizer | `-fsanitize=undefined` | Signed overflow, null deref, alignment |
| ThreadSanitizer | `-fsanitize=thread` | Data races, deadlocks |
| MemorySanitizer | `-fsanitize=memory` | Uninitialized reads (Clang only) |

- ASan + UBSan run together; TSan and MSan must run separately
- Always use `-fno-omit-frame-pointer` with sanitizers

## References

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- RAII wrappers, smart pointer patterns, thread-safe singleton

## External References

- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- [cppreference.com](https://en.cppreference.com/)
- [Compiler Explorer (Godbolt)](https://godbolt.org/)
- [GoogleTest Documentation](https://google.github.io/googletest/)
- [Catch2 Documentation](https://github.com/catchorg/Catch2/blob/devel/docs/Readme.md)
- [clang-tidy Checks](https://clang.llvm.org/extra/clang-tidy/checks/list.html)
- [CMake Best Practices](https://cmake.org/cmake/help/latest/guide/tutorial/index.html)
- [Abseil C++ Tips of the Week](https://abseil.io/tips/)
