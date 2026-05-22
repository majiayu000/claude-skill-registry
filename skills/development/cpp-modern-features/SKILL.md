---
name: cpp-modern-features
description: Use when working with modern C++ codebases requiring features from C++11 to C++23 including lambdas, move semantics, ranges, and concepts.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# C++ Modern Features

Master modern C++ features from C++11 through C++23, including lambdas, move
semantics, ranges, concepts, and compile-time evaluation. This skill enables
you to write efficient, expressive, and maintainable modern C++ code.

## C++11 Features

### Auto Type Deduction

The `auto` keyword enables automatic type inference, reducing verbosity and
improving maintainability:

```cpp
// Traditional
std::vector<int>::iterator it = vec.begin();
std::map<std::string, std::vector<int>>::const_iterator map_it = mymap.find("key");

// Modern C++11
auto it = vec.begin();
auto map_it = mymap.find("key");

// Auto with initialization
auto value = 42;              // int
auto pi = 3.14;              // double
auto name = std::string("Alice"); // std::string
auto lambda = [](int x) { return x * 2; }; // lambda type
```

### Range-Based For Loops

Simplified iteration over containers and arrays:

```cpp
std::vector<int> numbers = {1, 2, 3, 4, 5};

// Traditional loop
for (std::vector<int>::iterator it = numbers.begin(); it != numbers.end(); ++it) {
    std::cout << *it << " ";
}

// Range-based for (C++11)
for (int num : numbers) {
    std::cout << num << " ";
}

// With references to modify elements
for (int& num : numbers) {
    num *= 2;
}

// With const references for efficiency
for (const auto& str : string_vector) {
    process(str);
}
```

### Lambda Expressions

Anonymous functions with capture capabilities:

```cpp
// Basic lambda
auto add = [](int a, int b) { return a + b; };
int result = add(3, 4); // 7

// Lambda with captures
int multiplier = 10;
auto multiply = [multiplier](int x) { return x * multiplier; };

// Capture by reference
int counter = 0;
auto increment = [&counter]() { counter++; };

// Capture all by value
auto func1 = [=]() { return x + y + z; };

// Capture all by reference
auto func2 = [&]() { x++; y++; };

// Mixed captures
auto func3 = [&sum, multiplier](int x) { sum += x * multiplier; };

// Mutable lambda (can modify captured values)
auto mutable_func = [counter]() mutable { return counter++; };
```

### Smart Pointers

Automatic memory management with RAII:

```cpp
#include <memory>

// unique_ptr - exclusive ownership
std::unique_ptr<int> ptr1 = std::make_unique<int>(42);
std::unique_ptr<MyClass> obj = std::make_unique<MyClass>(arg1, arg2);

// shared_ptr - shared ownership with reference counting
std::shared_ptr<int> ptr2 = std::make_shared<int>(100);
std::shared_ptr<int> ptr3 = ptr2; // Reference count = 2

// weak_ptr - non-owning reference
std::weak_ptr<int> weak = ptr2;
if (auto locked = weak.lock()) {
    // Use locked pointer safely
    std::cout << *locked << std::endl;
}

// Custom deleter
auto deleter = [](FILE* fp) { fclose(fp); };
std::unique_ptr<FILE, decltype(deleter)> file(fopen("data.txt", "r"), deleter);
```

### Nullptr

Type-safe null pointer constant:

```cpp
// Old way (ambiguous)
void func(int x);
void func(char* ptr);
func(NULL); // Which overload? Depends on NULL definition

// Modern way (unambiguous)
func(nullptr); // Clearly calls func(char*)

// Smart pointer initialization
std::unique_ptr<int> ptr = nullptr;
if (ptr != nullptr) {
    // Use ptr
}
```

## C++14 Features

### Generic Lambdas

Lambdas with `auto` parameters:

```cpp
// Generic lambda (C++14)
auto generic_add = [](auto a, auto b) { return a + b; };

int sum1 = generic_add(3, 4);           // Works with int
double sum2 = generic_add(3.14, 2.71);  // Works with double
std::string concat = generic_add(std::string("Hello"), std::string(" World"));

// Multiple auto parameters
auto compare = [](auto a, auto b) { return a < b; };

// Use in algorithms
std::vector<int> vec = {5, 2, 8, 1, 9};
std::sort(vec.begin(), vec.end(), [](auto a, auto b) { return a > b; });
```

### Return Type Deduction

Automatic return type for functions:

```cpp
// C++14: auto return type deduction
auto multiply(int a, int b) {
    return a * b; // Return type deduced as int
}

auto get_vector() {
    return std::vector<int>{1, 2, 3}; // Deduced as std::vector<int>
}

// Multiple return statements must have same type
auto conditional(bool flag) {
    if (flag)
        return 42;    // int
    else
        return 100;   // int - OK
    // return 3.14;  // ERROR: different type
}
```

### Make Unique

Factory function for unique_ptr:

```cpp
// C++11 required manual construction
std::unique_ptr<MyClass> ptr1(new MyClass(arg1, arg2));

// C++14 provides std::make_unique
auto ptr2 = std::make_unique<MyClass>(arg1, arg2);

// Exception safety benefit
func(std::unique_ptr<int>(new int(1)), std::unique_ptr<int>(new int(2))); // Risky
func(std::make_unique<int>(1), std::make_unique<int>(2)); // Safe
```

## C++17 Features

### Structured Bindings

Decompose objects into individual variables:

```cpp
// Pairs and tuples
std::pair<int, std::string> get_data() {
    return {42, "Answer"};
}

auto [id, name] = get_data();
std::cout << id << ": " << name << std::endl;

// Maps
std::map<std::string, int> scores = {{"Alice", 95}, {"Bob", 87}};
for (const auto& [name, score] : scores) {
    std::cout << name << " scored " << score << std::endl;
}

// Arrays
int arr[3] = {1, 2, 3};
auto [a, b, c] = arr;

// Structs
struct Point { int x, y; };
Point p{10, 20};
auto [x, y] = p;
```

### If Constexpr

Compile-time conditional statements:

```cpp
template<typename T>
auto process(T value) {
    if constexpr (std::is_integral_v<T>) {
        return value * 2;
    } else if constexpr (std::is_floating_point_v<T>) {
        return value * 3.14;
    } else {
        return value;
    }
}

int result1 = process(10);      // Returns 20
double result2 = process(2.0);  // Returns 6.28
```

### Fold Expressions

Variadic template operations:

```cpp
// Sum all arguments
template<typename... Args>
auto sum(Args... args) {
    return (args + ...);
}

int total = sum(1, 2, 3, 4, 5); // 15

// Print all arguments
template<typename... Args>
void print(Args... args) {
    (std::cout << ... << args) << std::endl;
}

print("Value: ", 42, " ", 3.14); // Value: 42 3.14

// Logical operations
template<typename... Args>
bool all_true(Args... args) {
    return (... && args);
}

bool result = all_true(true, true, false); // false
```

### Std::optional

Type-safe optional values:

```cpp
#include <optional>

std::optional<int> find_value(const std::vector<int>& vec, int target) {
    auto it = std::find(vec.begin(), vec.end(), target);
    if (it != vec.end()) {
        return *it;
    }
    return std::nullopt;
}

// Usage
std::vector<int> numbers = {1, 2, 3, 4, 5};
if (auto result = find_value(numbers, 3)) {
    std::cout << "Found: " << *result << std::endl;
} else {
    std::cout << "Not found" << std::endl;
}

// Value_or for default
int value = find_value(numbers, 10).value_or(-1);
```

### Std::variant

Type-safe union:

```cpp
#include <variant>

std::variant<int, double, std::string> data;

data = 42;
data = 3.14;
data = std::string("Hello");

// Visit pattern
std::visit([](auto&& arg) {
    using T = std::decay_t<decltype(arg)>;
    if constexpr (std::is_same_v<T, int>) {
        std::cout << "int: " << arg << std::endl;
    } else if constexpr (std::is_same_v<T, double>) {
        std::cout << "double: " << arg << std::endl;
    } else {
        std::cout << "string: " << arg << std::endl;
    }
}, data);

// Get value
if (auto* str = std::get_if<std::string>(&data)) {
    std::cout << *str << std::endl;
}
```

## C++20 Features

### Concepts

Constrain template parameters:

```cpp
#include <concepts>

// Define a concept
template<typename T>
concept Numeric = std::is_arithmetic_v<T>;

// Use concept to constrain template
template<Numeric T>
T add(T a, T b) {
    return a + b;
}

// Concept with requires clause
template<typename T>
concept Hashable = requires(T a) {
    { std::hash<T>{}(a) } -> std::convertible_to<std::size_t>;
};

// Multiple constraints
template<typename T>
concept Sortable = std::copyable<T> && requires(T a, T b) {
    { a < b } -> std::convertible_to<bool>;
};

// Use in function
template<Sortable T>
void sort_data(std::vector<T>& vec) {
    std::sort(vec.begin(), vec.end());
}
```

### Ranges

Composable algorithms and views:

```cpp
#include <ranges>

std::vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

// Filter and transform using views
auto result = numbers
    | std::views::filter([](int n) { return n % 2 == 0; })
    | std::views::transform([](int n) { return n * n; });

for (int n : result) {
    std::cout << n << " "; // 4 16 36 64 100
}

// Take first N elements
auto first_five = numbers | std::views::take(5);

// Reverse view
auto reversed = numbers | std::views::reverse;

// Chaining multiple operations
auto complex_view = numbers
    | std::views::filter([](int n) { return n > 3; })
    | std::views::transform([](int n) { return n * 2; })
    | std::views::take(3);
```

### Coroutines

Cooperative multitasking:

```cpp
#include <coroutine>
#include <iostream>

// Simple generator
struct Generator {
    struct promise_type {
        int current_value;

        Generator get_return_object() {
            return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }

        std::suspend_always initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        std::suspend_always yield_value(int value) {
            current_value = value;
            return {};
        }

        void return_void() {}
        void unhandled_exception() {}
    };

    std::coroutine_handle<promise_type> handle;

    Generator(std::coroutine_handle<promise_type> h) : handle(h) {}
    ~Generator() { if (handle) handle.destroy(); }

    int value() { return handle.promise().current_value; }
    bool next() {
        handle.resume();
        return !handle.done();
    }
};

Generator counter(int start, int end) {
    for (int i = start; i < end; ++i) {
        co_yield i;
    }
}

// Usage
auto gen = counter(0, 5);
while (gen.next()) {
    std::cout << gen.value() << " ";
}
```

### Three-Way Comparison (Spaceship Operator)

Simplified comparison operators:

```cpp
#include <compare>

struct Point {
    int x, y;

    // Single operator generates all six comparison operators
    auto operator<=>(const Point& other) const = default;
};

Point p1{1, 2};
Point p2{1, 3};

bool eq = (p1 == p2);  // false
bool lt = (p1 < p2);   // true
bool gt = (p1 > p2);   // false

// Custom spaceship operator
struct Person {
    std::string name;
    int age;

    auto operator<=>(const Person& other) const {
        if (auto cmp = name <=> other.name; cmp != 0)
            return cmp;
        return age <=> other.age;
    }
};
```

## C++23 Features Preview

### Std::expected

Error handling without exceptions:

```cpp
#include <expected>

std::expected<int, std::string> divide(int a, int b) {
    if (b == 0) {
        return std::unexpected("Division by zero");
    }
    return a / b;
}

// Usage
auto result = divide(10, 2);
if (result) {
    std::cout << "Result: " << *result << std::endl;
} else {
    std::cout << "Error: " << result.error() << std::endl;
}

// Transform and error handling
auto transformed = divide(20, 4)
    .transform([](int x) { return x * 2; })
    .or_else([](auto error) {
        std::cout << "Error: " << error << std::endl;
        return std::expected<int, std::string>(0);
    });
```

### If with Initializer Enhancement

```cpp
// C++23: if with pattern matching improvements
std::map<int, std::string> map = {{1, "one"}, {2, "two"}};

if (auto [it, inserted] = map.insert({3, "three"}); inserted) {
    std::cout << "Inserted: " << it->second << std::endl;
}

// Enhanced static constexpr if
template<typename T>
void process(T value) {
    if constexpr (requires { value.size(); }) {
        std::cout << "Size: " << value.size() << std::endl;
    }
}
```

## Move Semantics

### Rvalue References

```cpp
class Buffer {
    char* data;
    size_t size;

public:
    // Constructor
    Buffer(size_t s) : size(s), data(new char[s]) {}

    // Copy constructor
    Buffer(const Buffer& other) : size(other.size), data(new char[size]) {
        std::copy(other.data, other.data + size, data);
    }

    // Move constructor
    Buffer(Buffer&& other) noexcept : size(other.size), data(other.data) {
        other.data = nullptr;
        other.size = 0;
    }

    // Copy assignment
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            delete[] data;
            size = other.size;
            data = new char[size];
            std::copy(other.data, other.data + size, data);
        }
        return *this;
    }

    // Move assignment
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data;
            data = other.data;
            size = other.size;
            other.data = nullptr;
            other.size = 0;
        }
        return *this;
    }

    ~Buffer() { delete[] data; }
};
```

### Std::move and Perfect Forwarding

```cpp
#include <utility>

// Using std::move
std::vector<int> vec1 = {1, 2, 3, 4, 5};
std::vector<int> vec2 = std::move(vec1); // vec1 is now empty

// Perfect forwarding
template<typename T>
void wrapper(T&& arg) {
    // Forward arg preserving its value category
    process(std::forward<T>(arg));
}

// Factory function with perfect forwarding
template<typename T, typename... Args>
std::unique_ptr<T> make_unique_custom(Args&&... args) {
    return std::unique_ptr<T>(new T(std::forward<Args>(args)...));
}

// Emplace methods use perfect forwarding
std::vector<std::pair<int, std::string>> vec;
vec.emplace_back(1, "one"); // Constructs in-place
```

## Lambda Advanced Features

### Recursive Lambdas

```cpp
// C++14 and later
auto fibonacci = [](int n) {
    auto impl = [](int n, auto& self) -> int {
        if (n <= 1) return n;
        return self(n-1, self) + self(n-2, self);
    };
    return impl(n, impl);
};

// C++23: Deducing this
auto fibonacci_cpp23 = [](this auto self, int n) -> int {
    if (n <= 1) return n;
    return self(n-1) + self(n-2);
};
```

### Init Captures (C++14)

```cpp
// Move-only types in captures
auto ptr = std::make_unique<int>(42);
auto lambda = [p = std::move(ptr)]() {
    std::cout << *p << std::endl;
};

// Initialize new variable in capture
auto lambda2 = [value = computeExpensiveValue()]() {
    return value * 2;
};

// Multiple init captures
auto lambda3 = [x = getValue(), y = getOtherValue()]() {
    return x + y;
};
```

## Compile-Time Evaluation

### Constexpr Functions

```cpp
// C++11 constexpr (limited)
constexpr int factorial_cpp11(int n) {
    return (n <= 1) ? 1 : n * factorial_cpp11(n - 1);
}

// C++14 constexpr (more powerful)
constexpr int factorial(int n) {
    int result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
}

constexpr int value = factorial(5); // Computed at compile time

// C++20 constexpr with std::vector
constexpr auto compute_primes(int max) {
    std::vector<int> primes;
    for (int i = 2; i < max; ++i) {
        bool is_prime = true;
        for (int p : primes) {
            if (i % p == 0) {
                is_prime = false;
                break;
            }
        }
        if (is_prime) primes.push_back(i);
    }
    return primes;
}
```

### Consteval (C++20)

Functions that must be evaluated at compile time:

```cpp
consteval int square(int n) {
    return n * n;
}

constexpr int value1 = square(5); // OK: compile-time
// int x = 5;
// int value2 = square(x); // ERROR: must be compile-time

// Consteval with constexpr
constexpr int maybe_compile_time(int n) {
    if (std::is_constant_evaluated()) {
        return n * n;
    } else {
        return n + n;
    }
}
```

## Best Practices

1. **Prefer auto for complex types**: Use `auto` to avoid verbose type
   declarations, especially with iterators and lambdas
2. **Use range-based for when possible**: Clearer intent and less error-prone
   than traditional loops
3. **Prefer lambdas for simple operations**: Especially in algorithm calls like
   `std::transform` and `std::for_each`
4. **Use smart pointers for ownership**: Prefer `unique_ptr` and `shared_ptr`
   over raw pointers for owned resources
5. **Embrace move semantics**: Implement move constructors/assignment for
   resource-owning types
6. **Use structured bindings**: Makes code more readable when working with
   pairs, tuples, and maps
7. **Prefer std::optional over special values**: Use `std::optional` instead of
   sentinel values like -1 or nullptr
8. **Use concepts to constrain templates (C++20)**: Makes template errors
   clearer and documents requirements
9. **Leverage ranges and views (C++20)**: More composable and efficient than
   traditional algorithms
10. **Use constexpr for compile-time computation**: Move computation to
    compile-time when possible for better performance

## Common Pitfalls

1. **Dangling references with auto**: `auto&` can create dangling references
   to temporaries
2. **Capturing by reference in lambdas**: Reference captures can outlive the
   captured variables
3. **Moving from const objects**: `std::move` on const objects doesn't
   actually move
4. **Default capturing [=] or [&]**: Can accidentally capture more than
   intended
5. **Forgetting to mark move operations noexcept**: Prevents some optimizations
   in containers
6. **Using std::move after using an object**: Moved-from objects are in valid
   but unspecified state
7. **Range-based for with temporaries**: Container temporaries destroyed before
   loop body
8. **Optional value access without checking**: Using `*` or `value()` without
   verifying `has_value()`
9. **Variant access without checking**: `std::get` throws if wrong type; use
   `get_if` or visitor
10. **Overusing auto**: Can hide important type information; use judiciously

## When to Use

Use this skill when:

- Working with modern C++ codebases (C++11 and later)
- Refactoring legacy code to use modern features
- Implementing resource management with RAII
- Writing generic code with templates and lambdas
- Optimizing performance with move semantics
- Implementing type-safe optional or variant types
- Working with ranges and functional-style algorithms
- Creating compile-time computed values
- Applying concepts to constrain templates
- Learning or teaching modern C++ practices

## Resources

- [C++ Reference - Lambda](https://en.cppreference.com/w/cpp/language/lambda)
- [C++ Reference - Auto](https://en.cppreference.com/w/cpp/language/auto)
- [C++ Reference - Range-based for](https://en.cppreference.com/w/cpp/language/range-for)
- [C++ Reference - Smart Pointers](https://en.cppreference.com/w/cpp/memory)
- [C++ Reference - Move Semantics](https://en.cppreference.com/w/cpp/language/move_constructor)
- [C++ Reference - Structured Bindings](https://en.cppreference.com/w/cpp/language/structured_binding)
- [C++ Reference - Optional](https://en.cppreference.com/w/cpp/utility/optional)
- [C++ Reference - Variant](https://en.cppreference.com/w/cpp/utility/variant)
- [C++ Reference - Concepts](https://en.cppreference.com/w/cpp/language/constraints)
- [C++ Reference - Ranges](https://en.cppreference.com/w/cpp/ranges)
- [C++ Reference - Coroutines](https://en.cppreference.com/w/cpp/language/coroutines)
- [C++ Reference - Constexpr](https://en.cppreference.com/w/cpp/language/constexpr)
