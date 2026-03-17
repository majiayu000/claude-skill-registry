---
name: C++ Ecosystem
description: This skill should be used when working with C++ projects, CMakeLists.txt, Ninja, clang-tidy, clang-format, GoogleTest, Catch2, or Modern C++ (C++11-23) language patterns. Provides comprehensive C++ ecosystem patterns and best practices.
---

# C++ Language

## Modern Features

**Move semantics** (C++11): Transfer ownership without copying.
```cpp
std::vector<int> v2 = std::move(v1); // v1 is now empty
```

**Smart pointers**: RAII-based automatic memory management.
- `unique_ptr` - Exclusive ownership, zero overhead
- `shared_ptr` - Shared ownership with reference counting
- `weak_ptr` - Non-owning observer of shared_ptr
```cpp
auto ptr = std::make_unique<MyClass>(args);
auto shared = std::make_shared<MyClass>(args);
```

**constexpr**: Compile-time computation (C++11 simple, C++14 loops, C++17 if constexpr, C++20 containers).

**auto and structured bindings** (C++17):
```cpp
auto [key, value] = pair;
```

**Lambdas**:
```cpp
auto add = [](int a, int b) { return a + b; };
auto capture_by_ref = [&x]() { x++; };
auto generic = [](auto a, auto b) { return a + b; }; // C++14
```

**Concepts** (C++20): Constraints on template parameters.
```cpp
template<typename T>
concept Addable = requires(T a, T b) { a + b; };
```

**Ranges** (C++20): Composable range operations.
```cpp
auto result = numbers | std::views::filter([](int n) { return n % 2 == 0; })
                      | std::views::transform([](int n) { return n * 2; });
```

**Modules** (C++20): Faster compilation, better encapsulation. Requires CMake 3.28+.

**Coroutines** (C++20): `co_yield`, `co_await`, `co_return`.

**Three-way comparison** (C++20): `auto operator<=>(const Point&) const = default;`

**Vocabulary types** (C++17): `std::optional`, `std::variant`, `std::any`.

## Concurrency
- `std::thread`, `std::async` for task-based parallelism
- `std::mutex`, `std::lock_guard`, `std::shared_mutex`
- `std::atomic` for lock-free operations
- `std::condition_variable` for synchronization
- Avoid: data races, deadlocks (use `std::scoped_lock` for multiple mutexes)

## Patterns
- **RAII**: Bind resource lifetime to object lifetime
- **Rule of Zero**: Prefer classes without special member functions (use smart pointers/containers)
- **Rule of Five**: If you define one of destructor/copy/move, define all five
- **PIMPL**: Hide implementation details, reduce compilation dependencies
- **CRTP**: Curiously Recurring Template Pattern for static polymorphism
- **Type Erasure**: Hide concrete types behind uniform interface

## Anti-patterns
- Raw pointer ownership - Use smart pointers
- Manual `new`/`delete` - Use `std::make_unique`/`std::make_shared`
- C-style casts - Use `static_cast`, `dynamic_cast`, etc.
- `using namespace std;` in headers - Use qualified names
- Throwing in destructors - Mark destructors `noexcept`

# CMake

## Project Structure
```
├── CMakeLists.txt
├── cmake/modules/
├── src/
├── include/project/
├── tests/
└── build/
```

## Modern CMake (3.0+)
```cmake
cmake_minimum_required(VERSION 3.20)
project(MyProject VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(mylib STATIC src/mylib.cpp)
target_include_directories(mylib PUBLIC include)
target_compile_features(mylib PUBLIC cxx_std_20)

add_executable(myapp src/main.cpp)
target_link_libraries(myapp PRIVATE mylib)
```

## Dependencies
```cmake
find_package(Threads REQUIRED)
find_package(GTest REQUIRED)
target_link_libraries(myapp PRIVATE Threads::Threads GTest::gtest)
```

## Compiler Options
```cmake
add_library(project_warnings INTERFACE)
target_compile_options(project_warnings INTERFACE
  $<$<CXX_COMPILER_ID:GNU,Clang>:
    -Wall -Wextra -Wpedantic -Werror -Wshadow -Wnon-virtual-dtor
    -Wconversion -Wsign-conversion -Wnull-dereference>)
```

## Commands
```bash
cmake -B build -G Ninja          # Configure
cmake --build build              # Build
cmake --build build --target test # Run tests
cmake --build build --config Release
```

# Toolchain

## Compilers
- **Clang**: `-std=c++20 -stdlib=libc++ -Wall -Wextra -Wpedantic -Werror`
- **GCC**: `-std=c++20 -Wall -Wextra -Wpedantic -Werror -fanalyzer`

## clang-tidy
```yaml
# .clang-tidy
Checks: >
  -*, bugprone-*, clang-analyzer-*, cppcoreguidelines-*,
  modernize-*, performance-*, readability-*,
  -modernize-use-trailing-return-type
WarningsAsErrors: '*'
```

## clang-format
```yaml
# .clang-format
BasedOnStyle: LLVM
IndentWidth: 4
ColumnLimit: 100
Standard: c++20
```

## Sanitizers
- **AddressSanitizer**: `-fsanitize=address -fno-omit-frame-pointer`
- **UndefinedBehaviorSanitizer**: `-fsanitize=undefined`
- **ThreadSanitizer**: `-fsanitize=thread` (cannot combine with ASan)
- **MemorySanitizer** (Clang only): `-fsanitize=memory`

# Testing

## GoogleTest
```cmake
enable_testing()
find_package(GTest REQUIRED)
add_executable(tests tests/test_main.cpp)
target_link_libraries(tests PRIVATE GTest::gtest GTest::gtest_main)
include(GoogleTest)
gtest_discover_tests(tests)
```
```cpp
TEST(MyTest, BasicAssertion) { EXPECT_EQ(1 + 1, 2); }
TEST_F(MyFixture, FixtureTest) { EXPECT_TRUE(true); }
```

## Catch2
```cmake
find_package(Catch2 3 REQUIRED)
target_link_libraries(tests PRIVATE Catch2::Catch2WithMain)
```
```cpp
TEST_CASE("Basic arithmetic", "[math]") {
    REQUIRE(1 + 1 == 2);
    SECTION("subtraction") { REQUIRE(2 - 1 == 1); }
}
```

# Context7 Integration
- C++ reference: `/websites/cppreference_com`
- CMake: `/Kitware/CMake`
- GoogleTest: `/google/googletest`
- Catch2: `/catchorg/Catch2`

# Best Practices
- Use smart pointers instead of raw pointers for ownership
- Enable `-Wall -Wextra -Werror` for all builds
- Run clang-tidy before committing
- Format with clang-format for consistent style
- Prefer const correctness throughout
- Use `noexcept` for move constructors and destructors
- Prefer `constexpr` for compile-time computation
- Use `std::string_view` for non-owning string references
- Prefer range-based for loops over index-based
- Use structured bindings for tuple/pair access
- Document public API with Doxygen comments
