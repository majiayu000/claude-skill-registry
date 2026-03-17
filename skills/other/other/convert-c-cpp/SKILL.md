---
name: convert-c-cpp
description: Convert C code to idiomatic C++. Use when migrating C projects to C++, translating C patterns to modern C++ idioms, or refactoring C codebases into C++. Extends meta-convert-dev with C-to-C++ specific patterns covering all 8 pillars (Module, Error, Concurrency, Metaprogramming, Zero/Default, Serialization, Build, Testing).
---

# Convert C to C++

Convert C code to idiomatic modern C++. This skill extends `meta-convert-dev` with C-to-C++ specific type mappings, idiom translations, and tooling guidance.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: C types → C++ types (primitives, structs, function pointers)
- **Idiom translations**: C patterns → idiomatic modern C++ (C++11/14/17/20)
- **Error handling**: Error codes → Exceptions, `std::optional`, `std::expected`
- **Memory management**: `malloc`/`free` → RAII, smart pointers
- **Module system**: Header guards → Namespaces, modules (C++20)
- **Metaprogramming**: Preprocessor macros → Templates, `constexpr`
- **Build systems**: Makefile → CMake
- **Testing**: Custom test frameworks → Google Test, Catch2

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- C language fundamentals - see `lang-c-dev`
- C++ language fundamentals - see `lang-cpp-dev`
- Reverse conversion (C++ → C) - see `convert-cpp-c`

---

## Quick Reference

| C | C++ | Notes |
|---|-----|-------|
| `int* ptr = malloc(n * sizeof(int))` | `std::vector<int> vec(n)` | RAII, no manual free |
| `struct Point p` | `Point p` | No `struct` keyword needed |
| `typedef struct { ... } Name;` | `struct Name { ... };` | Implicit typedef |
| `void* generic` | `template<typename T>` | Type-safe generics |
| `FILE* f = fopen(...)` | `std::ifstream f(...)` | RAII file handling |
| `enum { A, B, C }` | `enum class Status { A, B, C }` | Scoped enums |
| Error codes | `std::optional`, `std::expected`, exceptions | Modern error handling |
| Function pointers | `std::function`, lambdas | Type-safe callbacks |
| `NULL` | `nullptr` | Type-safe null pointer |
| `const char*` strings | `std::string`, `std::string_view` | Automatic memory mgmt |

## When Converting Code

1. **Analyze source thoroughly** - Identify memory ownership patterns in C code
2. **Map types first** - C primitives → C++ equivalents, structs → classes
3. **Replace manual memory management** - `malloc`/`free` → RAII, smart pointers
4. **Adopt C++ idioms** - Don't write "C code with `cout`"; use modern C++ patterns
5. **Use standard library** - Replace custom implementations with STL containers/algorithms
6. **Test incrementally** - Convert module by module, ensuring tests pass
7. **Enable compiler warnings** - Use `-Wall -Wextra -Wpedantic` to catch issues

---

## Type System Mapping

### Primitive Types

| C | C++ | Notes |
|---|-----|-------|
| `char`, `int`, `long` | Same | C++ inherits C primitive types |
| `unsigned int` | Same or `size_t` | Prefer `size_t` for sizes/indices |
| `int8_t`, `uint8_t` | Same (`<cstdint>`) | Exact-width integers |
| `NULL` | `nullptr` | Type-safe null pointer constant |
| `void*` | Avoid | Use templates or `std::any` instead |
| `bool` (C99) | `bool` | Native in C++, requires `<stdbool.h>` in C |

### Collection Types

| C | C++ | Notes |
|---|-----|-------|
| `int arr[10]` | `std::array<int, 10>` | Fixed-size, bounds-checked |
| `int* arr = malloc(...)` | `std::vector<int>` | Dynamic, RAII, automatic resize |
| Linked list (manual) | `std::list<T>`, `std::forward_list<T>` | Standard library |
| Hash table (manual) | `std::unordered_map<K, V>` | Efficient lookup |
| Binary tree (manual) | `std::map<K, V>`, `std::set<T>` | Ordered containers |

### Composite Types

| C | C++ | Notes |
|---|-----|-------|
| `struct Point { int x, y; };` | `struct Point { int x, y; };` | Same, but `struct` keyword optional for instances |
| `typedef struct { ... } Name;` | `struct Name { ... };` | Implicit typedef in C++ |
| `union Data { ... }` | `std::variant<...>` | Type-safe tagged union |
| `enum { A, B, C }` | `enum class Status { A, B, C }` | Scoped, strongly-typed |
| Tagged union (manual) | `std::variant<...>` | Type-safe alternative |

### Function Types

| C | C++ | Notes |
|---|-----|-------|
| `int (*func_ptr)(int, int)` | `std::function<int(int, int)>` | Type-erased, can hold lambdas |
| `typedef int (*Callback)(void*)` | `std::function<int(void*)>` | Modern function objects |
| `void qsort(void*, size_t, ...)` | `std::sort(begin, end, comparator)` | Type-safe, no void* |

---

## Idiom Translation

### Pattern 1: Memory Management (malloc/free → RAII)

**C:**
```c
#include <stdlib.h>

int* create_array(size_t n) {
    int* arr = malloc(n * sizeof(int));
    if (arr == NULL) {
        return NULL;
    }
    for (size_t i = 0; i < n; i++) {
        arr[i] = i * 2;
    }
    return arr;
}

void process() {
    int* data = create_array(100);
    if (data == NULL) {
        return;  // Error handling
    }

    // Use data...

    free(data);  // Manual cleanup
}
```

**C++:**
```cpp
#include <vector>

std::vector<int> create_array(size_t n) {
    std::vector<int> arr(n);
    for (size_t i = 0; i < n; i++) {
        arr[i] = i * 2;
    }
    return arr;  // Move semantics, no copy
}

void process() {
    auto data = create_array(100);
    // Use data...
    // Automatically freed when data goes out of scope
}
```

**Why this translation:**
- `std::vector` manages memory automatically (RAII)
- No risk of memory leaks or use-after-free
- Return by value is efficient with move semantics
- Bounds checking available with `.at(i)` instead of `[]`

### Pattern 2: Strings (char* → std::string)

**C:**
```c
#include <string.h>
#include <stdlib.h>

char* concat_strings(const char* a, const char* b) {
    size_t len_a = strlen(a);
    size_t len_b = strlen(b);
    char* result = malloc(len_a + len_b + 1);

    if (result == NULL) {
        return NULL;
    }

    strcpy(result, a);
    strcat(result, b);
    return result;
}

void example() {
    char* str = concat_strings("Hello", "World");
    if (str != NULL) {
        printf("%s\n", str);
        free(str);
    }
}
```

**C++:**
```cpp
#include <string>
#include <iostream>

std::string concat_strings(const std::string& a, const std::string& b) {
    return a + b;  // Operator overloading
}

// Or simply:
std::string concat_strings(const std::string& a, const std::string& b) {
    return a + b;
}

void example() {
    std::string str = concat_strings("Hello", "World");
    std::cout << str << '\n';
    // Automatic cleanup
}
```

**Why this translation:**
- `std::string` manages memory automatically
- No buffer overflow risks
- Rich API for string manipulation
- Concatenation via `operator+`
- Efficient move semantics for returns

### Pattern 3: Error Handling (Error Codes → Exceptions/Optional)

**C:**
```c
#define SUCCESS 0
#define ERROR_NULL_PTR -1
#define ERROR_NOT_FOUND -2

int find_user(int id, User* out_user) {
    if (out_user == NULL) {
        return ERROR_NULL_PTR;
    }

    User* user = lookup_user(id);
    if (user == NULL) {
        return ERROR_NOT_FOUND;
    }

    *out_user = *user;
    return SUCCESS;
}

// Usage
void example() {
    User user;
    int result = find_user(42, &user);
    if (result == SUCCESS) {
        // Use user
    } else if (result == ERROR_NOT_FOUND) {
        // Handle not found
    }
}
```

**C++ (with std::optional):**
```cpp
#include <optional>

std::optional<User> find_user(int id) {
    User* user = lookup_user(id);
    if (user == nullptr) {
        return std::nullopt;
    }
    return *user;
}

// Usage
void example() {
    if (auto user = find_user(42)) {
        // Use *user
    } else {
        // Handle not found
    }
}
```

**C++ (with exceptions):**
```cpp
#include <stdexcept>

User find_user(int id) {
    User* user = lookup_user(id);
    if (user == nullptr) {
        throw std::runtime_error("User not found");
    }
    return *user;
}

// Usage
void example() {
    try {
        User user = find_user(42);
        // Use user
    } catch (const std::runtime_error& e) {
        // Handle error
    }
}
```

**Why this translation:**
- `std::optional` avoids sentinel values and output parameters
- Exceptions separate happy path from error handling
- Clearer intent and less error-prone
- Modern C++23 will have `std::expected<T, E>` for richer error info

### Pattern 4: File I/O (FILE* → RAII streams)

**C:**
```c
#include <stdio.h>

int read_file(const char* filename, char** out_buffer, size_t* out_size) {
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        return -1;
    }

    fseek(file, 0, SEEK_END);
    long size = ftell(file);
    fseek(file, 0, SEEK_SET);

    char* buffer = malloc(size + 1);
    if (buffer == NULL) {
        fclose(file);
        return -1;
    }

    fread(buffer, 1, size, file);
    buffer[size] = '\0';
    fclose(file);

    *out_buffer = buffer;
    *out_size = size;
    return 0;
}
```

**C++:**
```cpp
#include <fstream>
#include <sstream>
#include <string>
#include <optional>

std::optional<std::string> read_file(const std::string& filename) {
    std::ifstream file(filename);
    if (!file) {
        return std::nullopt;
    }

    std::stringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
    // File automatically closed by destructor
}
```

**Why this translation:**
- `std::ifstream` uses RAII: automatically closes file
- No manual memory management for buffer
- Exception-safe: file closed even if exception thrown
- More concise and less error-prone

### Pattern 5: Structs → Classes with Methods

**C:**
```c
typedef struct {
    double x;
    double y;
} Point;

Point point_create(double x, double y) {
    Point p = {x, y};
    return p;
}

double point_distance(const Point* p1, const Point* p2) {
    double dx = p2->x - p1->x;
    double dy = p2->y - p1->y;
    return sqrt(dx*dx + dy*dy);
}

void point_print(const Point* p) {
    printf("Point(%.2f, %.2f)\n", p->x, p->y);
}
```

**C++:**
```cpp
#include <iostream>
#include <cmath>

struct Point {
    double x;
    double y;

    // Constructor
    Point(double x, double y) : x(x), y(y) {}

    // Member function
    double distance(const Point& other) const {
        double dx = other.x - x;
        double dy = other.y - y;
        return std::sqrt(dx*dx + dy*dy);
    }

    // Operator overload
    friend std::ostream& operator<<(std::ostream& os, const Point& p) {
        os << "Point(" << p.x << ", " << p.y << ")";
        return os;
    }
};

// Usage
Point p1(3.0, 4.0);
Point p2(0.0, 0.0);
std::cout << p1 << '\n';
std::cout << "Distance: " << p1.distance(p2) << '\n';
```

**Why this translation:**
- Methods are grouped with data (encapsulation)
- Constructors initialize members correctly
- Operator overloading for natural syntax
- Const correctness enforced by compiler

### Pattern 6: Function Pointers → Lambdas/std::function

**C:**
```c
typedef int (*Comparator)(const void*, const void*);

int int_compare(const void* a, const void* b) {
    int ia = *(const int*)a;
    int ib = *(const int*)b;
    return ia - ib;
}

void sort_array(int* arr, size_t n, Comparator cmp) {
    qsort(arr, n, sizeof(int), cmp);
}

// Usage
int data[] = {5, 2, 8, 1, 9};
sort_array(data, 5, int_compare);
```

**C++:**
```cpp
#include <algorithm>
#include <vector>

// Type-safe, no void*
void sort_array(std::vector<int>& arr, auto comparator) {
    std::sort(arr.begin(), arr.end(), comparator);
}

// Usage with lambda
std::vector<int> data = {5, 2, 8, 1, 9};
std::sort(data.begin(), data.end(), [](int a, int b) {
    return a < b;
});

// Or reverse sort
std::sort(data.begin(), data.end(), [](int a, int b) {
    return a > b;
});
```

**Why this translation:**
- Lambdas are type-safe (no `void*` casting)
- Can capture local variables
- Inline definition for simple comparisons
- `std::sort` is faster than `qsort` (inlined, type-specific)

### Pattern 7: Macros → Templates and constexpr

**C:**
```c
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define SQUARE(x) ((x) * (x))
#define ARRAY_SIZE(arr) (sizeof(arr) / sizeof((arr)[0]))

// Generic swap
#define SWAP(a, b, type) do { \
    type temp = (a); \
    (a) = (b); \
    (b) = temp; \
} while(0)
```

**C++:**
```cpp
// Type-safe templates
template<typename T>
constexpr T max(T a, T b) {
    return (a > b) ? a : b;
}

template<typename T>
constexpr T square(T x) {
    return x * x;
}

template<typename T, size_t N>
constexpr size_t array_size(T (&)[N]) {
    return N;
}

// Or use C++17 std::size
#include <iterator>
int arr[] = {1, 2, 3, 4, 5};
size_t size = std::size(arr);

// Swap with template
template<typename T>
void swap(T& a, T& b) {
    T temp = std::move(a);
    a = std::move(b);
    b = std::move(temp);
}

// Or just use std::swap
#include <utility>
std::swap(a, b);
```

**Why this translation:**
- Templates provide type safety
- `constexpr` enables compile-time evaluation
- Standard library provides `std::swap`, `std::max`, `std::min`
- Better error messages than macro errors
- Debugger-friendly (macros are invisible after preprocessing)

### Pattern 8: Enums → Scoped Enums

**C:**
```c
enum Color {
    COLOR_RED,
    COLOR_GREEN,
    COLOR_BLUE
};

enum Status {
    STATUS_OK,
    STATUS_ERROR
};

// Name conflicts possible
int color = COLOR_RED;
```

**C++:**
```cpp
enum class Color {
    Red,
    Green,
    Blue
};

enum class Status {
    Ok,
    Error
};

// No name conflicts, must scope
Color color = Color::Red;
Status status = Status::Ok;

// Stronger type safety
// Color c = Status::Ok;  // Error: type mismatch
```

**Why this translation:**
- `enum class` prevents name conflicts (scoped)
- No implicit conversion to int
- Stronger type safety
- Explicit scoping improves readability

---

## Error Handling Translation

### C Error Model → C++ Error Models

| C Pattern | C++ Pattern | When to Use |
|-----------|-------------|-------------|
| Return code (`int`) | `std::optional<T>` | Simple success/failure, no error details needed |
| Return code + errno | Exceptions | Rare errors, rich error context |
| Return code + output param | `std::expected<T, E>` (C++23) | Error details needed, exceptions undesirable |
| NULL return | `std::optional<T>` | May or may not find a value |

### Error Code → std::optional

**C:**
```c
#define SUCCESS 0
#define ERROR_NOT_FOUND -1

int get_config_value(const char* key, int* out_value) {
    if (key == NULL || out_value == NULL) {
        return -1;
    }

    // Lookup logic
    if (/* not found */) {
        return ERROR_NOT_FOUND;
    }

    *out_value = /* found value */;
    return SUCCESS;
}
```

**C++:**
```cpp
std::optional<int> get_config_value(const std::string& key) {
    // Lookup logic
    if (/* not found */) {
        return std::nullopt;
    }

    return /* found value */;
}

// Usage
if (auto value = get_config_value("timeout")) {
    std::cout << "Timeout: " << *value << '\n';
} else {
    std::cout << "Key not found\n";
}
```

### Error Code → Exceptions

**C:**
```c
int open_database(const char* path, Database** out_db) {
    if (path == NULL || out_db == NULL) {
        return ERROR_INVALID_ARG;
    }

    Database* db = malloc(sizeof(Database));
    if (db == NULL) {
        return ERROR_OUT_OF_MEMORY;
    }

    if (/* connection failed */) {
        free(db);
        return ERROR_CONNECTION_FAILED;
    }

    *out_db = db;
    return SUCCESS;
}

// Caller must check every error
int result = open_database(path, &db);
if (result != SUCCESS) {
    // Handle specific errors
}
```

**C++:**
```cpp
#include <stdexcept>
#include <memory>

class Database {
public:
    Database(const std::string& path) {
        if (/* connection failed */) {
            throw std::runtime_error("Failed to connect to database");
        }
        // Initialize
    }

    // RAII: destructor closes connection
    ~Database() {
        // Close connection
    }
};

// Usage - exceptions propagate automatically
try {
    Database db(path);
    // Use db
} catch (const std::runtime_error& e) {
    std::cerr << "Error: " << e.what() << '\n';
}
```

**Why this translation:**
- Exceptions separate error handling from main logic
- RAII ensures cleanup even if exception thrown
- Can't accidentally ignore errors (uncaught exception terminates)
- Error context preserved through exception object

---

## Memory Management Translation

### Manual Allocation → RAII and Smart Pointers

**C:**
```c
typedef struct {
    char* data;
    size_t size;
} Buffer;

Buffer* buffer_create(size_t size) {
    Buffer* buf = malloc(sizeof(Buffer));
    if (buf == NULL) {
        return NULL;
    }

    buf->data = malloc(size);
    if (buf->data == NULL) {
        free(buf);
        return NULL;
    }

    buf->size = size;
    return buf;
}

void buffer_destroy(Buffer* buf) {
    if (buf != NULL) {
        free(buf->data);
        free(buf);
    }
}

// Usage - easy to forget cleanup
Buffer* buf = buffer_create(1024);
// ... use buf ...
buffer_destroy(buf);  // Must remember to call
```

**C++ (RAII):**
```cpp
#include <vector>

class Buffer {
private:
    std::vector<char> data;

public:
    Buffer(size_t size) : data(size) {}

    // Rule of zero - compiler generates correct copy/move/destructor

    char& operator[](size_t i) { return data[i]; }
    size_t size() const { return data.size(); }
};

// Usage - automatic cleanup
{
    Buffer buf(1024);
    // ... use buf ...
}  // Automatically destroyed
```

**C++ (Smart Pointers for Heap Allocation):**
```cpp
#include <memory>

class LargeObject {
    // ... large data ...
};

// Unique ownership
auto obj = std::make_unique<LargeObject>();
// ... use obj ...
// Automatically deleted when obj goes out of scope

// Shared ownership
auto shared = std::make_shared<LargeObject>();
auto copy = shared;  // Reference count = 2
// Deleted when last shared_ptr is destroyed
```

**Why this translation:**
- No manual memory management needed
- Impossible to forget cleanup
- Exception-safe (cleanup happens even if exception thrown)
- Clear ownership semantics

---

## Concurrency Translation

### pthreads → std::thread and Synchronization Primitives

**C (pthreads):**
```c
#include <pthread.h>

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
int shared_counter = 0;

void* thread_function(void* arg) {
    for (int i = 0; i < 1000; i++) {
        pthread_mutex_lock(&mutex);
        shared_counter++;
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

int main() {
    pthread_t thread1, thread2;

    pthread_create(&thread1, NULL, thread_function, NULL);
    pthread_create(&thread2, NULL, thread_function, NULL);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    pthread_mutex_destroy(&mutex);

    printf("Counter: %d\n", shared_counter);
    return 0;
}
```

**C++:**
```cpp
#include <thread>
#include <mutex>
#include <iostream>

std::mutex mutex;
int shared_counter = 0;

void thread_function() {
    for (int i = 0; i < 1000; i++) {
        std::lock_guard<std::mutex> lock(mutex);  // RAII lock
        shared_counter++;
        // Automatically unlocked when lock goes out of scope
    }
}

int main() {
    std::thread thread1(thread_function);
    std::thread thread2(thread_function);

    thread1.join();
    thread2.join();

    std::cout << "Counter: " << shared_counter << '\n';
    return 0;
}
```

**Why this translation:**
- `std::lock_guard` provides RAII for mutex (can't forget to unlock)
- `std::thread` is type-safe (no `void*` casting)
- Cleaner syntax
- Exception-safe locking

---

## Build System Translation

### Makefile → CMake

**C (Makefile):**
```makefile
CC = gcc
CFLAGS = -Wall -Wextra -O2 -std=c11
LDFLAGS = -lm

SRCS = main.c utils.c
OBJS = $(SRCS:.c=.o)
TARGET = myapp

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(OBJS) -o $(TARGET) $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)
```

**C++ (CMake):**
```cmake
cmake_minimum_required(VERSION 3.20)
project(MyApp VERSION 1.0.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Create executable
add_executable(myapp
    src/main.cpp
    src/utils.cpp
)

# Include directories
target_include_directories(myapp PRIVATE include)

# Compiler flags
target_compile_options(myapp PRIVATE
    -Wall -Wextra -Wpedantic
)

# Link libraries
target_link_libraries(myapp PRIVATE
    # Add libraries here
)
```

**Build commands:**
```bash
# Configure
cmake -B build -S . -DCMAKE_BUILD_TYPE=Release

# Build
cmake --build build

# Clean
cmake --build build --target clean
```

**Why this translation:**
- CMake is cross-platform (Windows, Linux, macOS)
- Handles dependencies automatically
- Integrates with package managers (Conan, vcpkg)
- Better IDE support

---

## Testing Translation

### Custom Test Framework → Google Test

**C (Custom Framework):**
```c
#include <assert.h>
#include <stdio.h>

void test_addition() {
    assert(add(2, 3) == 5);
    assert(add(-1, 1) == 0);
    printf("test_addition passed\n");
}

void test_subtraction() {
    assert(subtract(5, 3) == 2);
    printf("test_subtraction passed\n");
}

int main() {
    test_addition();
    test_subtraction();
    printf("All tests passed\n");
    return 0;
}
```

**C++ (Google Test):**
```cpp
#include <gtest/gtest.h>
#include "math.hpp"

TEST(MathTest, Addition) {
    EXPECT_EQ(add(2, 3), 5);
    EXPECT_EQ(add(-1, 1), 0);
}

TEST(MathTest, Subtraction) {
    EXPECT_EQ(subtract(5, 3), 2);
}

// Fixture for common setup
class CalculatorTest : public ::testing::Test {
protected:
    void SetUp() override {
        calc = std::make_unique<Calculator>();
    }

    std::unique_ptr<Calculator> calc;
};

TEST_F(CalculatorTest, Operations) {
    calc->add(5);
    EXPECT_EQ(calc->result(), 5);
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
```

**Why this translation:**
- Rich assertion API
- Fixtures for setup/teardown
- Test discovery and filtering
- Better error messages
- Integration with CI/CD systems

---

## Serialization Translation

### Binary/JSON (C) → C++ Libraries

**C (cJSON):**
```c
#include <cJSON.h>

char* user_to_json(const User* user) {
    cJSON* root = cJSON_CreateObject();
    cJSON_AddStringToObject(root, "name", user->name);
    cJSON_AddNumberToObject(root, "age", user->age);

    char* json_str = cJSON_Print(root);
    cJSON_Delete(root);
    return json_str;
}

int user_from_json(User* user, const char* json_str) {
    cJSON* root = cJSON_Parse(json_str);
    if (root == NULL) {
        return -1;
    }

    cJSON* name = cJSON_GetObjectItem(root, "name");
    cJSON* age = cJSON_GetObjectItem(root, "age");

    if (!cJSON_IsString(name) || !cJSON_IsNumber(age)) {
        cJSON_Delete(root);
        return -1;
    }

    strncpy(user->name, name->valuestring, sizeof(user->name) - 1);
    user->age = age->valueint;

    cJSON_Delete(root);
    return 0;
}
```

**C++ (nlohmann/json):**
```cpp
#include <nlohmann/json.hpp>
using json = nlohmann::json;

struct User {
    std::string name;
    int age;
};

// Serialization
void to_json(json& j, const User& u) {
    j = json{{"name", u.name}, {"age", u.age}};
}

// Deserialization
void from_json(const json& j, User& u) {
    j.at("name").get_to(u.name);
    j.at("age").get_to(u.age);
}

// Usage
User user{"Alice", 30};
json j = user;  // Serialize
std::string json_str = j.dump();

// Deserialize
json j2 = json::parse(json_str);
User user2 = j2.get<User>();
```

**Why this translation:**
- Type-safe serialization/deserialization
- Automatic memory management
- Exception-based error handling
- Integration with modern C++ types

---

## Module System Translation

### Header Guards → Namespaces and C++20 Modules

**C (Header Guards):**
```c
// point.h
#ifndef POINT_H
#define POINT_H

typedef struct {
    double x;
    double y;
} Point;

Point point_create(double x, double y);
double point_distance(const Point* p1, const Point* p2);

#endif  // POINT_H
```

**C++ (Namespaces):**
```cpp
// point.hpp
#pragma once  // Modern alternative to include guards

namespace geometry {

class Point {
public:
    Point(double x, double y);
    double distance(const Point& other) const;

private:
    double x, y;
};

}  // namespace geometry
```

**C++20 (Modules):**
```cpp
// point.cppm
export module geometry;

export namespace geometry {

class Point {
public:
    Point(double x, double y);
    double distance(const Point& other) const;

private:
    double x, y;
};

}  // namespace geometry

// main.cpp
import geometry;

int main() {
    geometry::Point p1(3.0, 4.0);
    geometry::Point p2(0.0, 0.0);
    auto dist = p1.distance(p2);
}
```

**Why this translation:**
- Namespaces prevent name collisions
- Modules (C++20) eliminate header file re-parsing
- Faster compilation with modules
- Better encapsulation

---

## Common Pitfalls

### 1. Forgetting to Use `nullptr` Instead of `NULL`

**C:**
```c
int* ptr = NULL;
if (ptr == NULL) { /* ... */ }
```

**Wrong C++:**
```cpp
int* ptr = NULL;  // Don't use NULL
```

**Correct C++:**
```cpp
int* ptr = nullptr;  // Type-safe
if (ptr == nullptr) { /* ... */ }
```

**Why:** `nullptr` is type-safe and works correctly with overloading.

### 2. Not Using RAII for Resource Management

**Wrong:**
```cpp
void process() {
    int* data = new int[100];
    // ... use data ...
    delete[] data;  // Easy to forget or skip on early return
}
```

**Correct:**
```cpp
void process() {
    std::vector<int> data(100);
    // ... use data ...
    // Automatically cleaned up
}
```

### 3. Casting to `void*` When Templates Would Work

**Wrong:**
```cpp
void* generic_max(void* a, void* b, size_t size, int (*cmp)(const void*, const void*)) {
    return cmp(a, b) > 0 ? a : b;
}
```

**Correct:**
```cpp
template<typename T>
T max(T a, T b) {
    return (a > b) ? a : b;
}
```

### 4. Using C-Style Casts

**Wrong:**
```cpp
double d = 3.14;
int i = (int)d;  // C-style cast
```

**Correct:**
```cpp
double d = 3.14;
int i = static_cast<int>(d);  // Explicit and searchable
```

### 5. Manual Memory Management Instead of Smart Pointers

**Wrong:**
```cpp
Widget* widget = new Widget();
// ... use widget ...
delete widget;  // Might leak on exception
```

**Correct:**
```cpp
auto widget = std::make_unique<Widget>();
// ... use widget ...
// Automatically deleted
```

### 6. Using `char*` for Strings

**Wrong:**
```cpp
char* name = new char[50];
strcpy(name, "Alice");
// ... easy to cause buffer overflow ...
delete[] name;
```

**Correct:**
```cpp
std::string name = "Alice";
name += " Smith";  // Safe concatenation
// Automatic cleanup
```

### 7. Not Leveraging the Standard Library

**Wrong:**
```cpp
// Implement custom linked list, hash table, etc.
```

**Correct:**
```cpp
std::list<int> mylist;
std::unordered_map<std::string, int> mymap;
// Use tested, optimized implementations
```

### 8. Ignoring Const Correctness

**Wrong:**
```cpp
void print_point(Point* p) {  // Should be const
    std::cout << p->x << ", " << p->y << '\n';
}
```

**Correct:**
```cpp
void print_point(const Point& p) {  // Pass by const reference
    std::cout << p.x << ", " << p.y << '\n';
}
```

---

## Tooling

| Tool | Purpose | Notes |
|------|---------|-------|
| `c2rust` | Automated C → Rust translation | Not C++, but useful reference |
| `clang-tidy` | Static analysis, modernization | Checks for C-isms in C++ code |
| `cppcheck` | Static analysis | Finds bugs and style issues |
| `clang-format` | Code formatting | Enforces consistent style |
| `include-what-you-use` | Header hygiene | Ensures correct includes |
| CMake | Build system | Cross-platform builds |
| Conan / vcpkg | Package managers | Dependency management |

### Clang-Tidy Modernization Checks

```bash
# Run modernization checks
clang-tidy --checks='modernize-*' src/main.cpp -- -std=c++20

# Example checks:
# - modernize-use-nullptr (NULL → nullptr)
# - modernize-use-auto (explicit type → auto)
# - modernize-use-override (virtual → override)
# - modernize-make-unique (new → make_unique)
# - modernize-raw-string-literal (escape sequences → raw strings)
```

---

## Examples

### Example 1: Simple - Integer Array

**Before (C):**
```c
#include <stdlib.h>
#include <stdio.h>

int* create_sequence(int n) {
    int* arr = malloc(n * sizeof(int));
    if (arr == NULL) {
        return NULL;
    }

    for (int i = 0; i < n; i++) {
        arr[i] = i + 1;
    }

    return arr;
}

int main() {
    int* seq = create_sequence(10);
    if (seq == NULL) {
        fprintf(stderr, "Allocation failed\n");
        return 1;
    }

    for (int i = 0; i < 10; i++) {
        printf("%d ", seq[i]);
    }
    printf("\n");

    free(seq);
    return 0;
}
```

**After (C++):**
```cpp
#include <vector>
#include <iostream>

std::vector<int> create_sequence(int n) {
    std::vector<int> arr(n);

    for (int i = 0; i < n; i++) {
        arr[i] = i + 1;
    }

    return arr;  // Move semantics, efficient
}

int main() {
    auto seq = create_sequence(10);

    for (int value : seq) {
        std::cout << value << ' ';
    }
    std::cout << '\n';

    // Automatic cleanup
    return 0;
}
```

### Example 2: Medium - Linked List

**Before (C):**
```c
#include <stdlib.h>
#include <stdio.h>

typedef struct Node {
    int data;
    struct Node* next;
} Node;

typedef struct {
    Node* head;
} LinkedList;

void list_init(LinkedList* list) {
    list->head = NULL;
}

void list_push(LinkedList* list, int value) {
    Node* new_node = malloc(sizeof(Node));
    if (new_node == NULL) {
        return;
    }

    new_node->data = value;
    new_node->next = list->head;
    list->head = new_node;
}

void list_free(LinkedList* list) {
    Node* current = list->head;
    while (current != NULL) {
        Node* next = current->next;
        free(current);
        current = next;
    }
    list->head = NULL;
}

void list_print(const LinkedList* list) {
    Node* current = list->head;
    while (current != NULL) {
        printf("%d ", current->data);
        current = current->next;
    }
    printf("\n");
}

int main() {
    LinkedList list;
    list_init(&list);

    list_push(&list, 3);
    list_push(&list, 2);
    list_push(&list, 1);

    list_print(&list);
    list_free(&list);

    return 0;
}
```

**After (C++):**
```cpp
#include <list>
#include <iostream>

int main() {
    std::list<int> list;

    list.push_front(3);
    list.push_front(2);
    list.push_front(1);

    for (int value : list) {
        std::cout << value << ' ';
    }
    std::cout << '\n';

    // Automatic cleanup
    return 0;
}
```

### Example 3: Complex - Configuration Parser

**Before (C):**
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cJSON.h>

typedef struct {
    char* host;
    int port;
    int timeout;
} Config;

Config* config_create() {
    Config* cfg = malloc(sizeof(Config));
    if (cfg == NULL) {
        return NULL;
    }

    cfg->host = NULL;
    cfg->port = 8080;
    cfg->timeout = 30;

    return cfg;
}

void config_destroy(Config* cfg) {
    if (cfg != NULL) {
        free(cfg->host);
        free(cfg);
    }
}

int config_load(Config* cfg, const char* filename) {
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        return -1;
    }

    fseek(file, 0, SEEK_END);
    long size = ftell(file);
    fseek(file, 0, SEEK_SET);

    char* buffer = malloc(size + 1);
    if (buffer == NULL) {
        fclose(file);
        return -1;
    }

    fread(buffer, 1, size, file);
    buffer[size] = '\0';
    fclose(file);

    cJSON* root = cJSON_Parse(buffer);
    free(buffer);

    if (root == NULL) {
        return -1;
    }

    cJSON* host = cJSON_GetObjectItem(root, "host");
    if (cJSON_IsString(host)) {
        cfg->host = strdup(host->valuestring);
    }

    cJSON* port = cJSON_GetObjectItem(root, "port");
    if (cJSON_IsNumber(port)) {
        cfg->port = port->valueint;
    }

    cJSON* timeout = cJSON_GetObjectItem(root, "timeout");
    if (cJSON_IsNumber(timeout)) {
        cfg->timeout = timeout->valueint;
    }

    cJSON_Delete(root);
    return 0;
}

int main() {
    Config* cfg = config_create();
    if (cfg == NULL) {
        fprintf(stderr, "Failed to create config\n");
        return 1;
    }

    if (config_load(cfg, "config.json") != 0) {
        fprintf(stderr, "Failed to load config\n");
        config_destroy(cfg);
        return 1;
    }

    printf("Host: %s\n", cfg->host);
    printf("Port: %d\n", cfg->port);
    printf("Timeout: %d\n", cfg->timeout);

    config_destroy(cfg);
    return 0;
}
```

**After (C++):**
```cpp
#include <fstream>
#include <iostream>
#include <nlohmann/json.hpp>
#include <optional>
#include <string>

using json = nlohmann::json;

struct Config {
    std::string host = "localhost";
    int port = 8080;
    int timeout = 30;
};

// JSON serialization/deserialization
void from_json(const json& j, Config& cfg) {
    j.at("host").get_to(cfg.host);
    j.at("port").get_to(cfg.port);
    j.at("timeout").get_to(cfg.timeout);
}

std::optional<Config> load_config(const std::string& filename) {
    std::ifstream file(filename);
    if (!file) {
        return std::nullopt;
    }

    try {
        json j;
        file >> j;
        return j.get<Config>();
    } catch (const json::exception& e) {
        std::cerr << "JSON error: " << e.what() << '\n';
        return std::nullopt;
    }
}

int main() {
    if (auto cfg = load_config("config.json")) {
        std::cout << "Host: " << cfg->host << '\n';
        std::cout << "Port: " << cfg->port << '\n';
        std::cout << "Timeout: " << cfg->timeout << '\n';
    } else {
        std::cerr << "Failed to load config\n";
        return 1;
    }

    return 0;
}
```

**Key improvements:**
- RAII: file and JSON object automatically cleaned up
- `std::optional` for error handling (no output parameters)
- Exceptions handle JSON parsing errors
- Type-safe deserialization
- Default member initializers for Config
- No manual memory management

---

## Limitations

None. Both lang-c-dev and lang-cpp-dev have complete 8/8 pillar coverage, providing comprehensive guidance for all aspects of the conversion.

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `lang-c-dev` - C development patterns
- `lang-cpp-dev` - C++ development patterns
- `lang-cpp-patterns-dev` - Advanced C++ design patterns
- `lang-cpp-cmake-dev` - CMake build configuration
- `patterns-concurrency-dev` - Threads, async, synchronization
- `patterns-serialization-dev` - JSON, validation, data formats
- `patterns-metaprogramming-dev` - Templates, reflection, code generation
