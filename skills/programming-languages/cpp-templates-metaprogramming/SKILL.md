---
name: cpp-templates-metaprogramming
description: Use when creating generic and type-safe C++ libraries with templates, SFINAE, concepts, and compile-time metaprogramming.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# C++ Templates and Metaprogramming

Master C++ templates, template metaprogramming, SFINAE, concepts, and
compile-time computation. This skill enables you to create generic, type-safe,
and highly efficient C++ libraries with compile-time guarantees.

## Function Templates

### Basic Function Templates

```cpp
// Simple function template
template<typename T>
T max(T a, T b) {
    return (a > b) ? a : b;
}

// Usage
int i = max(10, 20);           // T = int
double d = max(3.14, 2.71);    // T = double
// auto x = max(10, 3.14);     // ERROR: can't deduce T

// Multiple template parameters
template<typename T, typename U>
auto add(T a, U b) -> decltype(a + b) {
    return a + b;
}

auto result = add(5, 3.14);    // T = int, U = double, returns double

// C++14: simpler return type deduction
template<typename T, typename U>
auto multiply(T a, U b) {
    return a * b;
}
```

### Template Specialization

```cpp
// Primary template
template<typename T>
T absolute(T value) {
    return (value < 0) ? -value : value;
}

// Full specialization for const char*
template<>
const char* absolute<const char*>(const char* value) {
    return value; // Strings don't have absolute value
}

// Full specialization for std::string
template<>
std::string absolute<std::string>(std::string value) {
    return value;
}

// Usage
int a = absolute(-5);              // Uses primary template
const char* b = absolute("test");  // Uses const char* specialization
```

### Function Template Overloading

```cpp
// Overload 1: Generic template
template<typename T>
void print(T value) {
    std::cout << "Generic: " << value << std::endl;
}

// Overload 2: Pointer specialization
template<typename T>
void print(T* ptr) {
    std::cout << "Pointer: " << *ptr << std::endl;
}

// Overload 3: Non-template overload
void print(const char* str) {
    std::cout << "String: " << str << std::endl;
}

// Usage
int x = 42;
print(x);       // Overload 1
print(&x);      // Overload 2
print("hello"); // Overload 3 (exact match preferred)
```

## Class Templates

### Basic Class Templates

```cpp
// Simple class template
template<typename T>
class Container {
    T value;

public:
    Container(T v) : value(v) {}

    T get() const { return value; }
    void set(T v) { value = v; }
};

// Usage
Container<int> intContainer(42);
Container<std::string> strContainer("hello");

// Multiple template parameters
template<typename K, typename V>
class KeyValuePair {
    K key;
    V value;

public:
    KeyValuePair(K k, V v) : key(k), value(v) {}

    K getKey() const { return key; }
    V getValue() const { return value; }
};

KeyValuePair<std::string, int> pair("answer", 42);
```

### Template Member Functions

```cpp
template<typename T>
class Array {
    T* data;
    size_t size;

public:
    Array(size_t s) : size(s), data(new T[s]) {}
    ~Array() { delete[] data; }

    // Template member function
    template<typename Func>
    void forEach(Func func) {
        for (size_t i = 0; i < size; ++i) {
            func(data[i]);
        }
    }

    // Template conversion operator
    template<typename U>
    operator Array<U>() const {
        Array<U> result(size);
        for (size_t i = 0; i < size; ++i) {
            result.data[i] = static_cast<U>(data[i]);
        }
        return result;
    }
};

// Usage
Array<int> arr(5);
arr.forEach([](int& x) { x *= 2; });
```

### Class Template Specialization

```cpp
// Primary template
template<typename T>
class Storage {
    T data;

public:
    Storage(T d) : data(d) {}
    T get() const { return data; }
};

// Full specialization for pointers
template<typename T>
class Storage<T*> {
    T* data;

public:
    Storage(T* d) : data(d) {}
    T* get() const { return data; }
    T& operator*() { return *data; }
};

// Full specialization for bool (bit optimization)
template<>
class Storage<bool> {
    unsigned char data : 1;

public:
    Storage(bool d) : data(d) {}
    bool get() const { return data; }
};
```

### Partial Template Specialization

```cpp
// Primary template
template<typename T, typename U>
class Pair {
public:
    T first;
    U second;
    void info() { std::cout << "Generic pair" << std::endl; }
};

// Partial specialization: both types the same
template<typename T>
class Pair<T, T> {
public:
    T first;
    T second;
    void info() { std::cout << "Same type pair" << std::endl; }
};

// Partial specialization: second type is pointer
template<typename T, typename U>
class Pair<T, U*> {
public:
    T first;
    U* second;
    void info() { std::cout << "Second is pointer" << std::endl; }
};

// Usage
Pair<int, double> p1;    // Generic
Pair<int, int> p2;       // Same type
Pair<int, double*> p3;   // Second is pointer
```

## Template Parameters

### Type Parameters

```cpp
// Single type parameter
template<typename T>
class Vector {
    T* data;
};

// Multiple type parameters
template<typename T, typename Allocator>
class CustomVector {
    T* data;
    Allocator alloc;
};

// Default type parameters
template<typename T, typename Compare = std::less<T>>
class Set {
    Compare comp;
public:
    bool less(const T& a, const T& b) {
        return comp(a, b);
    }
};
```

### Non-Type Parameters

```cpp
// Integer non-type parameter
template<typename T, size_t N>
class Array {
    T data[N];

public:
    constexpr size_t size() const { return N; }

    T& operator[](size_t i) { return data[i]; }
    const T& operator[](size_t i) const { return data[i]; }
};

Array<int, 10> arr1;  // Array of 10 ints
Array<double, 5> arr2; // Array of 5 doubles

// Bool non-type parameter
template<typename T, bool IsSorted>
class Container {
public:
    void insert(T value) {
        if constexpr (IsSorted) {
            insert_sorted(value);
        } else {
            insert_unsorted(value);
        }
    }

private:
    void insert_sorted(T value) { /* ... */ }
    void insert_unsorted(T value) { /* ... */ }
};

// Pointer non-type parameter (C++17)
template<auto* Ptr>
class StaticWrapper {
public:
    auto& get() { return *Ptr; }
};
```

### Template Template Parameters

```cpp
// Template template parameter
template<typename T, template<typename> class Container>
class Stack {
    Container<T> data;

public:
    void push(const T& value) {
        data.push_back(value);
    }

    T pop() {
        T value = data.back();
        data.pop_back();
        return value;
    }
};

// Usage
Stack<int, std::vector> intStack;
Stack<double, std::deque> doubleStack;

// With multiple parameters
template<typename T,
         template<typename, typename> class Container,
         typename Allocator = std::allocator<T>>
class AdvancedStack {
    Container<T, Allocator> data;
};
```

## Variadic Templates

### Parameter Packs

```cpp
// Basic variadic template
template<typename... Args>
void print(Args... args) {
    (std::cout << ... << args) << std::endl; // C++17 fold expression
}

print(1, 2, 3, "hello", 3.14);

// Get pack size
template<typename... Args>
constexpr size_t count(Args... args) {
    return sizeof...(args);
}

size_t n = count(1, 2, 3, 4); // 4

// Recursive parameter pack processing (pre-C++17)
template<typename T>
void print_recursive(T value) {
    std::cout << value << std::endl;
}

template<typename T, typename... Args>
void print_recursive(T first, Args... rest) {
    std::cout << first << " ";
    print_recursive(rest...); // Recursive call
}
```

### Fold Expressions (C++17)

```cpp
// Unary right fold: (args op ...)
template<typename... Args>
auto sum(Args... args) {
    return (args + ...);
}

auto result = sum(1, 2, 3, 4, 5); // 15

// Unary left fold: (... op args)
template<typename... Args>
auto sum_left(Args... args) {
    return (... + args);
}

// Binary right fold: (args op ... op init)
template<typename... Args>
auto sum_with_init(Args... args) {
    return (args + ... + 0);
}

// Binary left fold: (init op ... op args)
template<typename... Args>
auto multiply_with_init(Args... args) {
    return (1 * ... * args);
}

// Logical fold expressions
template<typename... Args>
bool all_true(Args... args) {
    return (args && ...);
}

template<typename... Args>
bool any_true(Args... args) {
    return (args || ...);
}

// Comma fold for side effects
template<typename... Args>
void print_all(Args... args) {
    (std::cout << ... << args) << std::endl;
}
```

### Variadic Class Templates

```cpp
// Tuple-like class
template<typename... Types>
class Tuple;

// Base case: empty tuple
template<>
class Tuple<> {};

// Recursive case
template<typename Head, typename... Tail>
class Tuple<Head, Tail...> : private Tuple<Tail...> {
    Head value;

public:
    Tuple(Head h, Tail... t) : Tuple<Tail...>(t...), value(h) {}

    Head& head() { return value; }
    Tuple<Tail...>& tail() { return *this; }
};

// Usage
Tuple<int, double, std::string> t(42, 3.14, "hello");

// Variadic template with perfect forwarding
template<typename... Args>
auto make_unique_custom(Args&&... args) {
    return std::unique_ptr<T>(new T(std::forward<Args>(args)...));
}
```

## SFINAE (Substitution Failure Is Not An Error)

### Basic SFINAE

```cpp
// Enable if type has begin() method
template<typename T>
auto process(T container) -> decltype(container.begin(), void()) {
    std::cout << "Container with begin()" << std::endl;
}

// Enable if type is arithmetic
template<typename T>
auto process(T value)
    -> typename std::enable_if<std::is_arithmetic<T>::value>::type {
    std::cout << "Arithmetic type" << std::endl;
}

// Usage
std::vector<int> vec;
process(vec);    // First overload
process(42);     // Second overload
```

### Std::enable_if

```cpp
// Enable function for integral types only
template<typename T>
typename std::enable_if<std::is_integral<T>::value, T>::type
increment(T value) {
    return value + 1;
}

// C++14: cleaner syntax with enable_if_t
template<typename T>
std::enable_if_t<std::is_integral<T>::value, T>
decrement(T value) {
    return value - 1;
}

// As template parameter (C++14)
template<typename T, typename = std::enable_if_t<std::is_floating_point<T>::value>>
T half(T value) {
    return value / 2;
}

// Multiple enable_if conditions
template<typename T>
std::enable_if_t<std::is_pointer<T>::value &&
                 !std::is_const<std::remove_pointer_t<T>>::value, void>
modify(T ptr) {
    *ptr = {};
}
```

### Tag Dispatching

```cpp
// Implementation functions with tags
template<typename Iterator>
void advance_impl(Iterator& it, int n, std::random_access_iterator_tag) {
    it += n; // O(1) for random access
}

template<typename Iterator>
void advance_impl(Iterator& it, int n, std::input_iterator_tag) {
    while (n--) ++it; // O(n) for input iterators
}

// Dispatch function
template<typename Iterator>
void advance(Iterator& it, int n) {
    advance_impl(it, n,
        typename std::iterator_traits<Iterator>::iterator_category());
}
```

### If Constexpr (C++17)

```cpp
// Replaces many SFINAE use cases
template<typename T>
auto process(T value) {
    if constexpr (std::is_integral_v<T>) {
        return value * 2;
    } else if constexpr (std::is_floating_point_v<T>) {
        return value * 3.14;
    } else if constexpr (std::is_pointer_v<T>) {
        return *value;
    } else {
        return value;
    }
}

// Variadic template with if constexpr
template<typename T, typename... Args>
void print(T first, Args... rest) {
    std::cout << first;
    if constexpr (sizeof...(rest) > 0) {
        std::cout << ", ";
        print(rest...);
    } else {
        std::cout << std::endl;
    }
}
```

## Concepts (C++20)

### Defining Concepts

```cpp
#include <concepts>

// Simple concept
template<typename T>
concept Integral = std::is_integral_v<T>;

// Concept with requires expression
template<typename T>
concept Incrementable = requires(T x) {
    { ++x } -> std::same_as<T&>;
    { x++ } -> std::same_as<T>;
};

// Compound concept
template<typename T>
concept Number = std::is_arithmetic_v<T>;

template<typename T>
concept SignedNumber = Number<T> && std::is_signed_v<T>;

// Concept with multiple requirements
template<typename T>
concept Container = requires(T c) {
    typename T::value_type;
    typename T::iterator;
    { c.begin() } -> std::same_as<typename T::iterator>;
    { c.end() } -> std::same_as<typename T::iterator>;
    { c.size() } -> std::convertible_to<std::size_t>;
};
```

### Using Concepts

```cpp
// Constrain function template
template<Integral T>
T add(T a, T b) {
    return a + b;
}

// Requires clause
template<typename T>
    requires Integral<T>
T multiply(T a, T b) {
    return a * b;
}

// Abbreviated function template (C++20)
auto divide(Integral auto a, Integral auto b) {
    return a / b;
}

// Constrain class template
template<Container C>
class Processor {
    C container;
public:
    void process() {
        for (auto& item : container) {
            // Process item
        }
    }
};

// Multiple constraints
template<typename T>
    requires std::is_arithmetic_v<T> && std::is_signed_v<T>
T absolute(T value) {
    return value < 0 ? -value : value;
}
```

### Concept Specialization

```cpp
// Different implementations based on concepts
template<typename T>
void process(T value) {
    if constexpr (Integral<T>) {
        std::cout << "Processing integer: " << value << std::endl;
    } else if constexpr (std::floating_point<T>) {
        std::cout << "Processing float: " << value << std::endl;
    } else {
        std::cout << "Processing other: " << value << std::endl;
    }
}

// Concept-based overloading
void handle(Integral auto value) {
    std::cout << "Integral: " << value << std::endl;
}

void handle(std::floating_point auto value) {
    std::cout << "Float: " << value << std::endl;
}

void handle(Container auto container) {
    std::cout << "Container of size: " << container.size() << std::endl;
}
```

## Type Traits

### Standard Type Traits

```cpp
#include <type_traits>

// Type properties
static_assert(std::is_integral_v<int>);
static_assert(std::is_floating_point_v<double>);
static_assert(std::is_pointer_v<int*>);
static_assert(std::is_array_v<int[5]>);
static_assert(std::is_const_v<const int>);

// Type relationships
static_assert(std::is_same_v<int, int>);
static_assert(std::is_base_of_v<Base, Derived>);
static_assert(std::is_convertible_v<int, double>);

// Type modifications
using NoConst = std::remove_const_t<const int>;      // int
using NoRef = std::remove_reference_t<int&>;         // int
using NoPointer = std::remove_pointer_t<int*>;       // int
using AddConst = std::add_const_t<int>;              // const int
using AddPointer = std::add_pointer_t<int>;          // int*

// Conditional types
using Type = std::conditional_t<true, int, double>;  // int
```

### Custom Type Traits

```cpp
// Check if type has size() method
template<typename T, typename = void>
struct has_size : std::false_type {};

template<typename T>
struct has_size<T, std::void_t<decltype(std::declval<T>().size())>>
    : std::true_type {};

template<typename T>
inline constexpr bool has_size_v = has_size<T>::value;

// Usage
static_assert(has_size_v<std::vector<int>>);
static_assert(!has_size_v<int>);

// Check if type is iterable
template<typename T, typename = void>
struct is_iterable : std::false_type {};

template<typename T>
struct is_iterable<T, std::void_t<
    decltype(std::declval<T>().begin()),
    decltype(std::declval<T>().end())>>
    : std::true_type {};

template<typename T>
inline constexpr bool is_iterable_v = is_iterable<T>::value;
```

## Template Metaprogramming

### Compile-Time Computation

```cpp
// Factorial at compile time
template<int N>
struct Factorial {
    static constexpr int value = N * Factorial<N - 1>::value;
};

template<>
struct Factorial<0> {
    static constexpr int value = 1;
};

constexpr int fact5 = Factorial<5>::value; // 120

// Fibonacci at compile time
template<int N>
struct Fibonacci {
    static constexpr int value = Fibonacci<N - 1>::value + Fibonacci<N - 2>::value;
};

template<>
struct Fibonacci<0> {
    static constexpr int value = 0;
};

template<>
struct Fibonacci<1> {
    static constexpr int value = 1;
};

constexpr int fib10 = Fibonacci<10>::value; // 55
```

### Type Lists

```cpp
// Type list definition
template<typename... Types>
struct TypeList {};

// Get size of type list
template<typename List>
struct Length;

template<typename... Types>
struct Length<TypeList<Types...>> {
    static constexpr size_t value = sizeof...(Types);
};

// Get type at index
template<size_t Index, typename List>
struct At;

template<size_t Index, typename Head, typename... Tail>
struct At<Index, TypeList<Head, Tail...>>
    : At<Index - 1, TypeList<Tail...>> {};

template<typename Head, typename... Tail>
struct At<0, TypeList<Head, Tail...>> {
    using type = Head;
};

// Usage
using MyList = TypeList<int, double, char, std::string>;
static_assert(Length<MyList>::value == 4);
using SecondType = At<1, MyList>::type; // double
```

### CRTP (Curiously Recurring Template Pattern)

```cpp
// Static polymorphism via CRTP
template<typename Derived>
class Base {
public:
    void interface() {
        static_cast<Derived*>(this)->implementation();
    }

    void common_functionality() {
        std::cout << "Common code" << std::endl;
    }
};

class Derived1 : public Base<Derived1> {
public:
    void implementation() {
        std::cout << "Derived1 implementation" << std::endl;
    }
};

class Derived2 : public Base<Derived2> {
public:
    void implementation() {
        std::cout << "Derived2 implementation" << std::endl;
    }
};

// Usage
template<typename T>
void use(Base<T>& obj) {
    obj.interface(); // No virtual function overhead
}

Derived1 d1;
Derived2 d2;
use(d1); // Derived1 implementation
use(d2); // Derived2 implementation
```

### Expression Templates

```cpp
// Expression template for lazy evaluation
template<typename E>
class VecExpression {
public:
    double operator[](size_t i) const {
        return static_cast<const E&>(*this)[i];
    }

    size_t size() const {
        return static_cast<const E&>(*this).size();
    }
};

class Vec : public VecExpression<Vec> {
    std::vector<double> data;

public:
    Vec(size_t n) : data(n) {}

    double& operator[](size_t i) { return data[i]; }
    double operator[](size_t i) const { return data[i]; }
    size_t size() const { return data.size(); }

    template<typename E>
    Vec& operator=(const VecExpression<E>& expr) {
        for (size_t i = 0; i < size(); ++i) {
            data[i] = expr[i];
        }
        return *this;
    }
};

// Addition expression
template<typename E1, typename E2>
class VecSum : public VecExpression<VecSum<E1, E2>> {
    const E1& lhs;
    const E2& rhs;

public:
    VecSum(const E1& l, const E2& r) : lhs(l), rhs(r) {}

    double operator[](size_t i) const {
        return lhs[i] + rhs[i];
    }

    size_t size() const { return lhs.size(); }
};

// Operator overload
template<typename E1, typename E2>
VecSum<E1, E2> operator+(const VecExpression<E1>& lhs,
                          const VecExpression<E2>& rhs) {
    return VecSum<E1, E2>(static_cast<const E1&>(lhs),
                          static_cast<const E2&>(rhs));
}

// Usage: single loop evaluation
Vec v1(1000), v2(1000), v3(1000), v4(1000);
v4 = v1 + v2 + v3; // Efficient: no temporary vectors
```

## Constexpr and Consteval

### Constexpr Functions

```cpp
// Constexpr function (can be compile-time or runtime)
constexpr int square(int n) {
    return n * n;
}

constexpr int value1 = square(5);  // Compile-time
int x = 5;
int value2 = square(x);            // Runtime

// Constexpr with complex logic (C++14+)
constexpr int fibonacci(int n) {
    if (n <= 1) return n;

    int a = 0, b = 1;
    for (int i = 2; i <= n; ++i) {
        int temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

// Constexpr with std::array
constexpr auto make_array() {
    std::array<int, 5> arr{};
    for (size_t i = 0; i < arr.size(); ++i) {
        arr[i] = i * i;
    }
    return arr;
}

constexpr auto squares = make_array();
```

### Consteval Functions (C++20)

```cpp
// Must be evaluated at compile-time
consteval int cube(int n) {
    return n * n * n;
}

constexpr int value3 = cube(5);  // OK: compile-time
// int y = 5;
// int value4 = cube(y);         // ERROR: not compile-time

// is_constant_evaluated
constexpr int conditional_compute(int n) {
    if (std::is_constant_evaluated()) {
        // Compile-time path
        return n * n;
    } else {
        // Runtime path (might use hardware instructions)
        return n * n; // Could use intrinsics
    }
}
```

## Template Debugging

### Compile-Time Debugging

```cpp
// Print type at compile time (causes error with type info)
template<typename T>
struct DebugType;

// DebugType<decltype(value)> debug; // Error shows type

// Static assert for debugging
template<typename T>
void check_type(T value) {
    static_assert(std::is_integral_v<T>, "T must be integral");
    static_assert(sizeof(T) >= 4, "T must be at least 4 bytes");
}

// Concept for better error messages
template<typename T>
concept AtLeast4Bytes = sizeof(T) >= 4;

template<AtLeast4Bytes T>
void process(T value) {
    // If T doesn't satisfy concept, clear error message
}
```

### Template Error Reduction

```cpp
// Before C++20: cryptic errors
template<typename T>
void old_process(T value) {
    value.size(); // Error if T doesn't have size()
}

// C++20: Clear concept-based errors
template<typename T>
concept HasSize = requires(T t) {
    { t.size() } -> std::convertible_to<std::size_t>;
};

template<HasSize T>
void new_process(T value) {
    value.size(); // Clear error if T doesn't satisfy HasSize
}

// Static assert for early error
template<typename T>
void checked_process(T value) {
    static_assert(HasSize<T>, "T must have size() method");
    value.size();
}
```

## Best Practices

1. **Prefer concepts over SFINAE (C++20)**: Clearer error messages and more
   readable constraints
2. **Use type traits for type inspection**: Leverage std::is_same,
   std::is_integral, etc.
3. **Prefer constexpr over template metaprogramming**: More readable and debuggable
4. **Use if constexpr for conditional compilation**: Replaces many SFINAE use cases
5. **Avoid deep template recursion**: Can cause long compile times and errors
6. **Use abbreviated function templates carefully**: Can hide important type
   information
7. **Provide clear error messages**: Use static_assert or concepts to guide users
8. **Forward perfectly with std::forward**: Preserve value categories in
   template code
9. **Use variadic templates for flexible interfaces**: Better than overload sets
10. **Document template requirements**: Specify what operations types must
    support

## Common Pitfalls

1. **Two-phase lookup issues**: Name lookup behaves differently in templates
2. **Dependent name resolution**: Must use typename and template keywords correctly
3. **Template instantiation bloat**: Each instantiation creates new code
4. **Compile-time explosion**: Complex metaprogramming can cause long compiles
5. **Obscure error messages**: Template errors can be difficult to understand
6. **Missing typename keyword**: Required for dependent type names
7. **Missing template keyword**: Required for dependent template names
8. **Forgetting std::forward**: Breaks perfect forwarding
9. **Concept subsumption issues**: More specific concepts must subsume less specific
10. **Constexpr limitations**: Not all operations allowed in constexpr context

## When to Use

Use this skill when:

- Creating generic algorithms and data structures
- Building reusable library code
- Implementing compile-time computation
- Constraining template parameters with concepts
- Performing type introspection and manipulation
- Optimizing performance with zero-cost abstractions
- Creating domain-specific embedded languages (DSELs)
- Implementing static polymorphism with CRTP
- Building expression template libraries
- Teaching or learning advanced C++ techniques

## Resources

- [C++ Reference - Templates](https://en.cppreference.com/w/cpp/language/templates)
- [C++ Reference - SFINAE](https://en.cppreference.com/w/cpp/language/sfinae)
- [C++ Reference - Concepts](https://en.cppreference.com/w/cpp/language/constraints)
- [C++ Reference - Type Traits](https://en.cppreference.com/w/cpp/header/type_traits)
- [C++ Reference - Fold Expressions](https://en.cppreference.com/w/cpp/language/fold)
- [C++ Reference - Constexpr](https://en.cppreference.com/w/cpp/language/constexpr)
- [C++ Templates: The Complete Guide by Vandevoorde, Josuttis, Gregor](http://www.tmplbook.com/)
- [Modern C++ Design by Andrei Alexandrescu](https://erdani.com/index.php/books/modern-c-design/)
- [CppCon Talks on Template Metaprogramming](https://www.youtube.com/user/CppCon)
