---
name: convert-java-cpp
description: Convert Java code to idiomatic C++. Use when migrating Java projects to C++, translating Java patterns to idiomatic C++, or refactoring Java codebases. Extends meta-convert-dev with Java-to-C++ specific patterns.
---

# Convert Java to C++

Convert Java code to idiomatic C++. This skill extends `meta-convert-dev` with Java-to-C++ specific type mappings, idiom translations, and tooling.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Java types → C++ types
- **Idiom translations**: Java patterns → idiomatic C++
- **Error handling**: Java exceptions → C++ exception handling and RAII
- **Memory management**: Java GC → C++ manual memory management and smart pointers
- **Concurrency**: Java threads → C++ threading and async patterns
- **Build systems**: Maven/Gradle → CMake/Make

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Java language fundamentals - see `lang-java-dev`
- C++ language fundamentals - see `lang-cpp-dev`
- Reverse conversion (C++ → Java) - see `convert-cpp-java`

---

## Quick Reference

| Java | C++ | Notes |
|------|-----|-------|
| `String` | `std::string` | Owned string |
| `int` | `int` / `int32_t` | 32-bit signed integer |
| `long` | `long` / `int64_t` | 64-bit signed integer |
| `double` | `double` | 64-bit float |
| `boolean` | `bool` | Boolean type |
| `Object` | `void*` / templates | Avoid void*, use templates |
| `List<T>` | `std::vector<T>` | Dynamic array |
| `Set<T>` | `std::set<T>` / `std::unordered_set<T>` | Ordered/unordered set |
| `Map<K, V>` | `std::map<K, V>` / `std::unordered_map<K, V>` | Ordered/unordered map |
| `Optional<T>` | `std::optional<T>` | Nullable value (C++17) |
| `Stream<T>` | Range views (C++20) / iterators | Lazy evaluation |
| `interface` | `class` (abstract) | Pure virtual functions |
| `class` | `class` / `struct` | Similar but different memory model |
| `package` | `namespace` | Code organization |
| `synchronized` | `std::mutex` + `std::lock_guard` | Thread safety |

## When Converting Code

1. **Analyze source thoroughly** before writing target
2. **Map types first** - create type equivalence table
3. **Preserve semantics** over syntax similarity
4. **Adopt C++ idioms** - don't write "Java code in C++ syntax"
5. **Handle memory explicitly** - GC → RAII and smart pointers
6. **Test equivalence** - same inputs → same outputs

---

## Type System Mapping

### Primitive Types

| Java | C++ | Notes |
|------|-----|-------|
| `byte` | `int8_t` / `char` | 8-bit signed |
| `short` | `int16_t` / `short` | 16-bit signed |
| `int` | `int` / `int32_t` | 32-bit signed |
| `long` | `long long` / `int64_t` | 64-bit signed |
| `float` | `float` | 32-bit floating point |
| `double` | `double` | 64-bit floating point |
| `char` | `char16_t` / `wchar_t` | 16-bit Unicode in Java, varies in C++ |
| `boolean` | `bool` | Boolean type |
| `void` | `void` | No return value |

### Collection Types

| Java | C++ | Notes |
|------|-----|-------|
| `ArrayList<T>` | `std::vector<T>` | Dynamic array, contiguous memory |
| `LinkedList<T>` | `std::list<T>` | Doubly-linked list |
| `HashSet<T>` | `std::unordered_set<T>` | Hash-based set, O(1) lookup |
| `TreeSet<T>` | `std::set<T>` | Sorted set, O(log n) lookup |
| `HashMap<K, V>` | `std::unordered_map<K, V>` | Hash-based map, O(1) lookup |
| `TreeMap<K, V>` | `std::map<K, V>` | Sorted map, O(log n) lookup |
| `Queue<T>` | `std::queue<T>` | FIFO queue |
| `Stack<T>` | `std::stack<T>` | LIFO stack |
| `Deque<T>` | `std::deque<T>` | Double-ended queue |
| `T[]` | `std::array<T, N>` / `std::vector<T>` | Fixed/dynamic array |

### Composite Types

| Java | C++ | Notes |
|------|-----|-------|
| `class` | `class` | Classes with constructors/destructors |
| `interface` | `class` with pure virtuals | Abstract base class |
| `abstract class` | `class` with virtuals | Base class with implementation |
| `enum` | `enum class` | Strongly-typed enum (C++11) |
| `@interface` (annotation) | Attributes (C++11) | Limited compared to Java |
| `record` (Java 14+) | `struct` | Immutable data class |
| `sealed class` (Java 17+) | `final` class | Restrict inheritance |

### Generic Type Mappings

| Java | C++ | Notes |
|------|-----|-------|
| `<T>` | `template<typename T>` | Generic type parameter |
| `<T extends Base>` | `template<typename T>` + `static_assert` | Type constraints |
| `<T extends A & B>` | Concepts (C++20) | Multiple constraints |
| `<? extends T>` | `const T&` / `T` | Upper bound wildcard |
| `<? super T>` | - | No direct equivalent |
| `List<?>` | Templates + type erasure | Complex pattern |

### Special Mappings

| Java | C++ | Notes |
|------|-----|-------|
| `Object` | `std::any` (C++17) / templates | Prefer templates |
| `null` | `nullptr` | Null pointer |
| `Optional<T>` | `std::optional<T>` (C++17) | Nullable value |
| `String` | `std::string` | UTF-8 string |
| `StringBuilder` | `std::ostringstream` / `std::string` | String building |
| `Comparable<T>` | `operator<` | Comparison operator |
| `Iterable<T>` | Iterator pattern | Range-for compatible |
| `Runnable` | `std::function<void()>` / lambda | Callable object |
| `Callable<T>` | `std::function<T()>` / lambda | Callable with return |

---

## Module System Translation

### Package → Namespace

**Java:**
```java
package com.example.myapp;

public class User {
    private String name;
    private int age;
}
```

**C++:**
```cpp
// user.hpp
#ifndef COM_EXAMPLE_MYAPP_USER_HPP
#define COM_EXAMPLE_MYAPP_USER_HPP

#include <string>

namespace com::example::myapp {

class User {
private:
    std::string name;
    int age;

public:
    User(const std::string& name, int age);
    // Getters/setters
};

}  // namespace com::example::myapp

#endif
```

**Why this translation:**
- Java packages map to C++ namespaces (use `::` separator in C++17+)
- Header guards (`#ifndef`) prevent multiple inclusion
- Declarations in `.hpp`, definitions in `.cpp`

### Import → Include

**Java:**
```java
import java.util.List;
import java.util.ArrayList;
import java.util.stream.*;
```

**C++:**
```cpp
#include <vector>
#include <algorithm>
#include <ranges>  // C++20
```

**Why this translation:**
- Java imports map to C++ includes
- C++ uses header files, not package-based imports
- Standard library in `<>`, local files in `""`

### Visibility Modifiers

| Java | C++ | Notes |
|------|-----|-------|
| `public` | `public:` | Accessible everywhere |
| `protected` | `protected:` | Accessible in class and subclasses |
| `private` | `private:` | Accessible only in class |
| `package-private` (default) | - | No direct equivalent, use unnamed namespace |

---

## Idiom Translation

### Pattern 1: Getter/Setter → Direct Access or Property

**Java:**
```java
public class User {
    private String name;
    private int age;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        if (age < 0) {
            throw new IllegalArgumentException("Age cannot be negative");
        }
        this.age = age;
    }
}
```

**C++:**
```cpp
class User {
private:
    std::string name;
    int age;

public:
    // Const getters
    const std::string& getName() const { return name; }
    int getAge() const { return age; }

    // Setters with validation
    void setName(const std::string& name) { this->name = name; }

    void setAge(int age) {
        if (age < 0) {
            throw std::invalid_argument("Age cannot be negative");
        }
        this->age = age;
    }
};
```

**Why this translation:**
- C++ uses `const` methods for getters (promise not to modify object)
- Return `const&` for large objects to avoid copying
- Throw standard exceptions (`std::invalid_argument`, etc.)

### Pattern 2: Null Handling → Optional/Smart Pointers

**Java:**
```java
public User findUser(String id) {
    for (User user : users) {
        if (user.getId().equals(id)) {
            return user;
        }
    }
    return null;
}

// Usage
User user = findUser("123");
if (user != null) {
    System.out.println(user.getName());
}
```

**C++:**
```cpp
std::optional<User> findUser(const std::string& id) {
    auto it = std::find_if(users.begin(), users.end(),
        [&id](const User& u) { return u.getId() == id; });

    if (it != users.end()) {
        return *it;
    }
    return std::nullopt;
}

// Usage
auto user = findUser("123");
if (user.has_value()) {
    std::cout << user->getName() << '\n';
}

// Or with value_or
auto name = findUser("123")
    .transform([](const User& u) { return u.getName(); })
    .value_or("Unknown");
```

**Why this translation:**
- `std::optional` makes null handling explicit (C++17)
- Safer than raw pointers for optional values
- Supports functional-style operations (`transform`, `value_or`)

### Pattern 3: Collection Operations → STL Algorithms/Ranges

**Java:**
```java
List<Integer> result = items.stream()
    .filter(x -> x % 2 == 0)
    .map(x -> x * 2)
    .collect(Collectors.toList());
```

**C++:**
```cpp
// Traditional STL algorithms
std::vector<int> result;
std::copy_if(items.begin(), items.end(), std::back_inserter(result),
    [](int x) { return x % 2 == 0; });
std::transform(result.begin(), result.end(), result.begin(),
    [](int x) { return x * 2; });

// Or with C++20 ranges (more similar to Java)
auto result = items
    | std::views::filter([](int x) { return x % 2 == 0; })
    | std::views::transform([](int x) { return x * 2; })
    | std::ranges::to<std::vector>();
```

**Why this translation:**
- C++20 ranges provide lazy evaluation like Java streams
- Traditional STL algorithms are more verbose but work in older C++
- Ranges compose better and are more readable

### Pattern 4: Try-with-Resources → RAII

**Java:**
```java
try (BufferedReader reader = new BufferedReader(new FileReader("file.txt"))) {
    String line = reader.readLine();
    // Use line
} catch (IOException e) {
    e.printStackTrace();
}
// reader is automatically closed
```

**C++:**
```cpp
// RAII - Resource Acquisition Is Initialization
#include <fstream>
#include <string>

try {
    std::ifstream file("file.txt");
    if (!file.is_open()) {
        throw std::runtime_error("Failed to open file");
    }

    std::string line;
    std::getline(file, line);
    // Use line
    // file is automatically closed when it goes out of scope
} catch (const std::exception& e) {
    std::cerr << e.what() << '\n';
}
```

**Why this translation:**
- C++ uses RAII pattern - resources cleaned up in destructors
- No need for explicit `close()` - automatic when object destroyed
- More general than Java's try-with-resources

### Pattern 5: Interfaces → Abstract Classes with Pure Virtuals

**Java:**
```java
public interface Drawable {
    void draw();

    default void render() {
        System.out.println("Rendering...");
        draw();
    }
}

public class Circle implements Drawable {
    @Override
    public void draw() {
        System.out.println("Drawing circle");
    }
}
```

**C++:**
```cpp
class Drawable {
public:
    // Pure virtual function (must be implemented)
    virtual void draw() = 0;

    // Virtual function with default implementation
    virtual void render() {
        std::cout << "Rendering...\n";
        draw();
    }

    // Virtual destructor (important!)
    virtual ~Drawable() = default;
};

class Circle : public Drawable {
public:
    void draw() override {
        std::cout << "Drawing circle\n";
    }
};
```

**Why this translation:**
- Pure virtual functions (`= 0`) = Java abstract methods
- Virtual functions with body = Java default methods
- **Always** provide virtual destructor for polymorphic classes
- Use `override` keyword for safety (C++11)

### Pattern 6: Inheritance → Composition (Preferred in C++)

**Java:**
```java
public class Stack<T> extends ArrayList<T> {
    public void push(T item) {
        add(item);
    }

    public T pop() {
        return remove(size() - 1);
    }
}
```

**C++:**
```cpp
// Prefer composition over inheritance
template<typename T>
class Stack {
private:
    std::vector<T> data;

public:
    void push(const T& item) {
        data.push_back(item);
    }

    T pop() {
        if (data.empty()) {
            throw std::runtime_error("Stack is empty");
        }
        T item = std::move(data.back());
        data.pop_back();
        return item;
    }

    bool empty() const {
        return data.empty();
    }

    size_t size() const {
        return data.size();
    }
};
```

**Why this translation:**
- Composition is more flexible than inheritance in C++
- Avoids exposing base class interface
- Better encapsulation and type safety

---

## Error Handling

### Exception Mapping

| Java Exception | C++ Exception | Notes |
|---------------|---------------|-------|
| `Exception` | `std::exception` | Base exception class |
| `RuntimeException` | `std::runtime_error` | Runtime errors |
| `IllegalArgumentException` | `std::invalid_argument` | Invalid argument |
| `IllegalStateException` | `std::logic_error` | Logic error |
| `NullPointerException` | `std::bad_optional_access` | Null access (or use optional) |
| `IndexOutOfBoundsException` | `std::out_of_range` | Array bounds |
| `IOException` | `std::ios_base::failure` | I/O error |
| `ArithmeticException` | `std::overflow_error` | Arithmetic error |

### Exception Handling Patterns

**Java:**
```java
public int divide(int a, int b) throws ArithmeticException {
    if (b == 0) {
        throw new ArithmeticException("Division by zero");
    }
    return a / b;
}

public void process() {
    try {
        int result = divide(10, 0);
    } catch (ArithmeticException e) {
        System.err.println("Error: " + e.getMessage());
    } finally {
        cleanup();
    }
}
```

**C++:**
```cpp
int divide(int a, int b) {
    if (b == 0) {
        throw std::invalid_argument("Division by zero");
    }
    return a / b;
}

void process() {
    try {
        int result = divide(10, 0);
    } catch (const std::invalid_argument& e) {
        std::cerr << "Error: " << e.what() << '\n';
    }
    // No finally - use RAII for cleanup
}

// RAII handles cleanup automatically
class Resource {
public:
    Resource() { /* acquire */ }
    ~Resource() { cleanup(); }  // Always called
};
```

**Why this translation:**
- C++ doesn't have `finally` - use RAII instead
- Catch by `const&` to avoid slicing
- Throw standard exceptions or custom types
- No checked exceptions in C++

### Custom Exceptions

**Java:**
```java
public class ValidationException extends Exception {
    public ValidationException(String message) {
        super(message);
    }
}
```

**C++:**
```cpp
class ValidationException : public std::exception {
private:
    std::string message;

public:
    explicit ValidationException(const std::string& msg) : message(msg) {}

    const char* what() const noexcept override {
        return message.c_str();
    }
};
```

---

## Memory Management

### Java GC → C++ Manual Memory

**Java (GC):**
```java
public class DataProcessor {
    private List<Data> cache = new ArrayList<>();

    public void addData(Data data) {
        cache.add(data);  // GC handles cleanup
    }
}
```

**C++ (RAII + Smart Pointers):**
```cpp
class DataProcessor {
private:
    std::vector<std::shared_ptr<Data>> cache;

public:
    void addData(std::shared_ptr<Data> data) {
        cache.push_back(data);
        // Automatically cleaned up when last shared_ptr is destroyed
    }

    // Or with unique ownership
    void addDataUnique(std::unique_ptr<Data> data) {
        cache.push_back(std::move(data));
    }
};
```

### Smart Pointer Decision Tree

```
Is the object optional/nullable?
├─ YES → std::optional<T> (if small) or std::unique_ptr<T> (if large/polymorphic)
└─ NO → Direct member (T) or reference (T&)

Does the object need shared ownership?
├─ YES → std::shared_ptr<T>
└─ NO → std::unique_ptr<T> or direct ownership

Is the object polymorphic (virtual functions)?
├─ YES → Must use pointers (raw, unique, or shared)
└─ NO → Can use direct value
```

### Memory Ownership Patterns

**Java (Shared References):**
```java
public class Cache {
    private Map<String, User> users = new HashMap<>();

    public User getUser(String id) {
        return users.get(id);  // Returns reference, GC handles lifetime
    }

    public void setUser(String id, User user) {
        users.put(id, user);  // Stores reference
    }
}
```

**C++ (Explicit Ownership):**
```cpp
class Cache {
private:
    std::unordered_map<std::string, std::shared_ptr<User>> users;

public:
    // Return shared pointer - shared ownership
    std::shared_ptr<User> getUser(const std::string& id) {
        auto it = users.find(id);
        if (it != users.end()) {
            return it->second;
        }
        return nullptr;
    }

    // Or return optional reference - no ownership transfer
    std::optional<std::reference_wrapper<const User>>
    getUserRef(const std::string& id) const {
        auto it = users.find(id);
        if (it != users.end()) {
            return *it->second;
        }
        return std::nullopt;
    }

    void setUser(const std::string& id, std::shared_ptr<User> user) {
        users[id] = user;
    }
};
```

**Why this translation:**
- C++ requires explicit ownership decisions
- Shared pointers for shared ownership (reference counting)
- References for borrowing without ownership transfer
- Unique pointers for exclusive ownership

---

## Concurrency Patterns

### Thread Creation

**Java:**
```java
Thread thread = new Thread(() -> {
    System.out.println("Running in thread");
});
thread.start();
thread.join();
```

**C++:**
```cpp
#include <thread>
#include <iostream>

std::thread thread([]() {
    std::cout << "Running in thread\n";
});
thread.join();
```

### Synchronized → Mutex

**Java:**
```java
public class Counter {
    private int count = 0;

    public synchronized void increment() {
        count++;
    }

    public synchronized int getCount() {
        return count;
    }
}
```

**C++:**
```cpp
#include <mutex>

class Counter {
private:
    int count = 0;
    mutable std::mutex mtx;

public:
    void increment() {
        std::lock_guard<std::mutex> lock(mtx);
        count++;
    }

    int getCount() const {
        std::lock_guard<std::mutex> lock(mtx);
        return count;
    }
};
```

**Why this translation:**
- `std::lock_guard` provides RAII locking (like Java synchronized)
- Automatically unlocks when scope ends
- Use `mutable` for mutex in const methods

### ExecutorService → std::async/thread pool

**Java:**
```java
ExecutorService executor = Executors.newFixedThreadPool(4);

Future<String> future = executor.submit(() -> {
    Thread.sleep(1000);
    return "Result";
});

String result = future.get();
executor.shutdown();
```

**C++:**
```cpp
#include <future>
#include <thread>
#include <chrono>

// Simple async
std::future<std::string> future = std::async(std::launch::async, []() {
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    return std::string("Result");
});

std::string result = future.get();

// For thread pools, use external library (e.g., Boost.Asio, Thread Pool)
```

### CompletableFuture → std::future/promise

**Java:**
```java
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    return fetchData();
});

future.thenApply(data -> parse(data))
      .thenAccept(result -> process(result))
      .exceptionally(ex -> handleError(ex));
```

**C++:**
```cpp
// C++ std::future is more limited
auto future = std::async(std::launch::async, []() {
    return fetchData();
});

try {
    auto data = future.get();
    auto result = parse(data);
    process(result);
} catch (const std::exception& ex) {
    handleError(ex);
}

// For chaining, use external library (e.g., folly::Future, boost::future)
```

---

## Metaprogramming

### Annotations → Attributes

**Java:**
```java
@Override
public String toString() {
    return "User";
}

@Deprecated
public void oldMethod() {
    // ...
}

@SuppressWarnings("unchecked")
public List getRawList() {
    // ...
}
```

**C++:**
```cpp
// C++11 attributes (limited compared to Java)
[[nodiscard]] int getValue() {
    return 42;
}

[[deprecated("Use newMethod instead")]]
void oldMethod() {
    // ...
}

[[maybe_unused]] void utilityFunction() {
    // ...
}

// C++20 attributes
[[likely]]
if (condition) {
    // Likely branch
}

[[unlikely]]
else {
    // Unlikely branch
}
```

**Why this translation:**
- C++ attributes are compiler hints, not runtime-accessible
- Much more limited than Java annotations
- No custom attributes like Java's annotation processing

### Reflection → Runtime Type Information (Limited)

**Java:**
```java
Class<?> clazz = obj.getClass();
Method[] methods = clazz.getDeclaredMethods();
for (Method method : methods) {
    System.out.println(method.getName());
}
```

**C++:**
```cpp
#include <typeinfo>

// Very limited reflection
const std::type_info& ti = typeid(obj);
std::cout << "Type: " << ti.name() << '\n';

// For more reflection, use external libraries:
// - Boost.PFR (Plain Old Data reflection)
// - rttr (Run-Time Type Reflection)
// - Meta Stuff (modern reflection library)
```

**Note:** C++ has minimal runtime reflection. Most "reflection" done at compile-time with templates.

### Generics → Templates

**Java:**
```java
public class Box<T> {
    private T value;

    public void set(T value) {
        this.value = value;
    }

    public T get() {
        return value;
    }
}

Box<String> box = new Box<>();
```

**C++:**
```cpp
template<typename T>
class Box {
private:
    T value;

public:
    void set(const T& value) {
        this->value = value;
    }

    const T& get() const {
        return value;
    }
};

Box<std::string> box;
```

**Why this translation:**
- C++ templates are more powerful (compile-time vs runtime)
- Templates fully instantiated at compile-time
- No type erasure in C++ (unlike Java)

---

## Serialization

### Jackson → Third-Party Libraries

**Java:**
```java
import com.fasterxml.jackson.databind.ObjectMapper;

public class User {
    @JsonProperty("user_id")
    private String id;
    private String name;

    @JsonIgnore
    private String password;
}

ObjectMapper mapper = new ObjectMapper();
String json = mapper.writeValueAsString(user);
User parsed = mapper.readValue(json, User.class);
```

**C++:**
```cpp
// Using nlohmann/json library
#include <nlohmann/json.hpp>

struct User {
    std::string id;
    std::string name;
    std::string password;  // Will handle separately
};

// Define serialization
void to_json(nlohmann::json& j, const User& u) {
    j = {
        {"user_id", u.id},
        {"name", u.name}
        // password omitted
    };
}

void from_json(const nlohmann::json& j, User& u) {
    j.at("user_id").get_to(u.id);
    j.at("name").get_to(u.name);
}

// Usage
nlohmann::json j = user;
std::string json_str = j.dump();

User parsed = j.get<User>();
```

**Popular C++ JSON libraries:**
- `nlohmann/json` - Modern, easy to use
- `RapidJSON` - Fast, SAX/DOM parsing
- `simdjson` - Extremely fast parsing
- `Boost.JSON` - Part of Boost

### Validation

**Java:**
```java
import jakarta.validation.constraints.*;

public class User {
    @NotNull
    @Size(min = 1, max = 100)
    private String name;

    @Email
    private String email;

    @Min(0)
    @Max(150)
    private int age;
}
```

**C++:**
```cpp
// Manual validation or use external library
class User {
private:
    std::string name;
    std::string email;
    int age;

public:
    User(std::string name, std::string email, int age) {
        if (name.empty() || name.length() > 100) {
            throw std::invalid_argument("Name must be 1-100 characters");
        }
        if (age < 0 || age > 150) {
            throw std::invalid_argument("Age must be 0-150");
        }
        // Email validation with regex
        std::regex email_regex(R"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})");
        if (!std::regex_match(email, email_regex)) {
            throw std::invalid_argument("Invalid email");
        }

        this->name = std::move(name);
        this->email = std::move(email);
        this->age = age;
    }
};
```

---

## Build System Translation

### Maven/Gradle → CMake

**Maven (pom.xml):**
```xml
<project>
    <groupId>com.example</groupId>
    <artifactId>myapp</artifactId>
    <version>1.0.0</version>

    <dependencies>
        <dependency>
            <groupId>com.google.guava</groupId>
            <artifactId>guava</artifactId>
            <version>32.0.0</version>
        </dependency>
    </dependencies>
</project>
```

**CMake (CMakeLists.txt):**
```cmake
cmake_minimum_required(VERSION 3.20)
project(myapp VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Dependencies
find_package(Boost REQUIRED)

add_executable(myapp
    src/main.cpp
    src/utils.cpp
)

target_include_directories(myapp PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(myapp PRIVATE
    Boost::boost
)

# Tests
enable_testing()
add_subdirectory(tests)
```

### Dependency Management

| Java | C++ | Notes |
|------|-----|-------|
| Maven Central | vcpkg / Conan / Hunter | Package managers |
| `pom.xml` | `CMakeLists.txt` | Build config |
| `.jar` files | `.a` / `.so` / `.dll` | Libraries |
| Modules (Java 9+) | Header files | Module system |

---

## Testing

### JUnit → Google Test / Catch2

**Java (JUnit):**
```java
import org.junit.jupiter.api.*;

class CalculatorTest {
    private Calculator calc;

    @BeforeEach
    void setUp() {
        calc = new Calculator();
    }

    @Test
    void shouldAddNumbers() {
        assertEquals(5, calc.add(2, 3));
    }

    @Test
    void shouldThrowOnDivideByZero() {
        assertThrows(ArithmeticException.class, () -> {
            calc.divide(10, 0);
        });
    }
}
```

**C++ (Google Test):**
```cpp
#include <gtest/gtest.h>
#include "calculator.hpp"

class CalculatorTest : public ::testing::Test {
protected:
    void SetUp() override {
        calc = std::make_unique<Calculator>();
    }

    std::unique_ptr<Calculator> calc;
};

TEST_F(CalculatorTest, ShouldAddNumbers) {
    EXPECT_EQ(5, calc->add(2, 3));
}

TEST_F(CalculatorTest, ShouldThrowOnDivideByZero) {
    EXPECT_THROW(calc->divide(10, 0), std::invalid_argument);
}
```

### Mockito → Google Mock

**Java (Mockito):**
```java
@Mock
private UserRepository repo;

@Test
void shouldFindUser() {
    when(repo.findById(1L)).thenReturn(Optional.of(user));

    User result = service.getUser(1L);

    verify(repo).findById(1L);
    assertEquals("Alice", result.getName());
}
```

**C++ (Google Mock):**
```cpp
class MockUserRepository : public UserRepository {
public:
    MOCK_METHOD(std::optional<User>, findById, (int64_t id), (override));
};

TEST(UserServiceTest, ShouldFindUser) {
    MockUserRepository repo;
    UserService service(repo);
    User expected{"Alice", 30};

    EXPECT_CALL(repo, findById(1))
        .WillOnce(::testing::Return(expected));

    auto result = service.getUser(1);
    EXPECT_EQ("Alice", result.getName());
}
```

---

## Common Pitfalls

### 1. Object Slicing

**Problem:**
```cpp
class Base {
public:
    virtual void print() { std::cout << "Base\n"; }
};

class Derived : public Base {
    int extra;
public:
    void print() override { std::cout << "Derived\n"; }
};

void process(Base obj) {  // Takes by value - SLICING!
    obj.print();  // Always prints "Base"
}

Derived d;
process(d);  // Derived object sliced to Base
```

**Fix:**
```cpp
void process(const Base& obj) {  // Take by reference
    obj.print();  // Polymorphic behavior
}
```

### 2. Forgetting Virtual Destructors

**Problem:**
```cpp
class Base {
public:
    ~Base() { /* cleanup */ }  // Not virtual!
};

class Derived : public Base {
    int* data;
public:
    ~Derived() { delete[] data; }  // Never called!
};

Base* ptr = new Derived();
delete ptr;  // Undefined behavior - Derived destructor not called
```

**Fix:**
```cpp
class Base {
public:
    virtual ~Base() { /* cleanup */ }  // Virtual destructor
};
```

### 3. Returning Dangling References

**Problem:**
```cpp
const std::string& getName() {
    std::string name = "temp";
    return name;  // Returns reference to destroyed object!
}
```

**Fix:**
```cpp
std::string getName() {
    return "temp";  // Return by value (move semantics)
}

// Or if truly returning member:
const std::string& getName() const {
    return memberName;  // OK - member outlives function
}
```

### 4. Iterator Invalidation

**Problem:**
```cpp
std::vector<int> vec = {1, 2, 3, 4, 5};
for (auto it = vec.begin(); it != vec.end(); ++it) {
    if (*it == 3) {
        vec.erase(it);  // it is now invalid!
    }
}
```

**Fix:**
```cpp
for (auto it = vec.begin(); it != vec.end();) {
    if (*it == 3) {
        it = vec.erase(it);  // erase returns next valid iterator
    } else {
        ++it;
    }
}

// Or use erase-remove idiom
vec.erase(std::remove(vec.begin(), vec.end(), 3), vec.end());
```

### 5. Copying Large Objects Unnecessarily

**Problem:**
```cpp
std::vector<int> getData() {
    std::vector<int> data(1000000);
    // fill data
    return data;  // Looks like copy but OK (NRVO)
}

void process(std::vector<int> data) {  // Copy!
    // Use data
}
```

**Fix:**
```cpp
// Return by value is OK (move semantics / NRVO)
std::vector<int> getData() {
    std::vector<int> data(1000000);
    return data;  // Moved or elided
}

// Take by const reference if not modifying
void process(const std::vector<int>& data) {
    // Use data
}

// Take by rvalue reference if consuming
void process(std::vector<int>&& data) {
    myData = std::move(data);
}
```

### 6. String Null-Termination Confusion

**Problem:**
```cpp
// Java strings are not null-terminated
// C++ std::string is, but C-style strings require care

char buffer[10];
std::string str = "0123456789";  // 10 chars
strcpy(buffer, str.c_str());  // Buffer overflow! Need 11 bytes for \0
```

**Fix:**
```cpp
char buffer[11];  // One extra for null terminator
std::strncpy(buffer, str.c_str(), sizeof(buffer) - 1);
buffer[sizeof(buffer) - 1] = '\0';  // Ensure null termination

// Or better: just use std::string
std::string buffer = str;
```

### 7. Unsigned Integer Underflow

**Problem:**
```cpp
// Java doesn't have unsigned types (except char)
// C++ does, and they can underflow

size_t count = 0;
count--;  // Underflows to SIZE_MAX (very large number)!

for (size_t i = vec.size() - 1; i >= 0; --i) {  // Infinite loop!
    // Process vec[i]
}
```

**Fix:**
```cpp
// Use signed for arithmetic that can go negative
int count = 0;
count--;  // -1

// Reverse iteration
for (size_t i = vec.size(); i-- > 0;) {
    // Process vec[i]
}

// Or use reverse iterators
for (auto it = vec.rbegin(); it != vec.rend(); ++it) {
    // Process *it
}
```

### 8. Const Correctness

**Problem:**
```cpp
// Java doesn't enforce const, C++ does

class Data {
    std::string value;
public:
    std::string getValue() {  // Not const!
        return value;
    }
};

void print(const Data& data) {
    std::cout << data.getValue();  // Error: calling non-const method on const object
}
```

**Fix:**
```cpp
class Data {
    std::string value;
public:
    const std::string& getValue() const {  // Const method
        return value;
    }
};
```

---

## Tooling

| Tool | Purpose | Notes |
|------|---------|-------|
| CMake | Build system | De facto standard |
| vcpkg | Package manager | Microsoft's package manager |
| Conan | Package manager | Decentralized, flexible |
| Google Test | Testing framework | Most popular |
| Catch2 | Testing framework | Header-only, BDD style |
| Google Mock | Mocking framework | Works with Google Test |
| Clang-Format | Code formatter | Based on LLVM |
| Clang-Tidy | Static analyzer | Catches common errors |
| Valgrind | Memory debugger | Detects leaks, errors |
| AddressSanitizer | Memory error detector | Part of Clang/GCC |
| Doxygen | Documentation | Javadoc equivalent |

---

## Examples

### Example 1: Simple - User Class

**Java:**
```java
public class User {
    private String name;
    private int age;

    public User(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }

    @Override
    public String toString() {
        return "User{name='" + name + "', age=" + age + "}";
    }
}
```

**C++:**
```cpp
#include <string>
#include <sstream>

class User {
private:
    std::string name;
    int age;

public:
    User(std::string name, int age)
        : name(std::move(name)), age(age) {}

    const std::string& getName() const {
        return name;
    }

    int getAge() const {
        return age;
    }

    std::string toString() const {
        std::ostringstream oss;
        oss << "User{name='" << name << "', age=" << age << "}";
        return oss.str();
    }
};
```

### Example 2: Medium - Repository Pattern

**Java:**
```java
public interface UserRepository {
    Optional<User> findById(Long id);
    List<User> findAll();
    void save(User user);
    void delete(Long id);
}

public class InMemoryUserRepository implements UserRepository {
    private Map<Long, User> users = new HashMap<>();

    @Override
    public Optional<User> findById(Long id) {
        return Optional.ofNullable(users.get(id));
    }

    @Override
    public List<User> findAll() {
        return new ArrayList<>(users.values());
    }

    @Override
    public void save(User user) {
        users.put(user.getId(), user);
    }

    @Override
    public void delete(Long id) {
        users.remove(id);
    }
}
```

**C++:**
```cpp
#include <unordered_map>
#include <vector>
#include <optional>
#include <memory>

class UserRepository {
public:
    virtual ~UserRepository() = default;

    virtual std::optional<User> findById(int64_t id) = 0;
    virtual std::vector<User> findAll() = 0;
    virtual void save(const User& user) = 0;
    virtual void remove(int64_t id) = 0;
};

class InMemoryUserRepository : public UserRepository {
private:
    std::unordered_map<int64_t, User> users;

public:
    std::optional<User> findById(int64_t id) override {
        auto it = users.find(id);
        if (it != users.end()) {
            return it->second;
        }
        return std::nullopt;
    }

    std::vector<User> findAll() override {
        std::vector<User> result;
        result.reserve(users.size());
        for (const auto& [_, user] : users) {
            result.push_back(user);
        }
        return result;
    }

    void save(const User& user) override {
        users[user.getId()] = user;
    }

    void remove(int64_t id) override {
        users.erase(id);
    }
};
```

### Example 3: Complex - Service with Dependencies

**Java:**
```java
public class UserService {
    private final UserRepository repository;
    private final EmailService emailService;
    private final Logger logger;

    public UserService(UserRepository repository,
                      EmailService emailService) {
        this.repository = repository;
        this.emailService = emailService;
        this.logger = LoggerFactory.getLogger(UserService.class);
    }

    public User createUser(String name, String email, int age) {
        logger.info("Creating user: {}", name);

        if (name == null || name.isEmpty()) {
            throw new IllegalArgumentException("Name cannot be empty");
        }

        if (age < 0 || age > 150) {
            throw new IllegalArgumentException("Invalid age: " + age);
        }

        User user = new User(name, email, age);
        repository.save(user);

        try {
            emailService.sendWelcomeEmail(user);
        } catch (EmailException e) {
            logger.warn("Failed to send welcome email", e);
        }

        return user;
    }

    public List<User> getActiveUsers() {
        return repository.findAll().stream()
            .filter(User::isActive)
            .sorted(Comparator.comparing(User::getName))
            .collect(Collectors.toList());
    }

    public Optional<User> updateUserAge(Long id, int newAge) {
        Optional<User> userOpt = repository.findById(id);

        if (userOpt.isPresent()) {
            User user = userOpt.get();
            user.setAge(newAge);
            repository.save(user);
            logger.info("Updated user {} age to {}", id, newAge);
        }

        return userOpt;
    }
}
```

**C++:**
```cpp
#include <memory>
#include <string>
#include <vector>
#include <optional>
#include <algorithm>
#include <spdlog/spdlog.h>  // Popular logging library

class UserService {
private:
    std::shared_ptr<UserRepository> repository;
    std::shared_ptr<EmailService> emailService;
    std::shared_ptr<spdlog::logger> logger;

public:
    UserService(std::shared_ptr<UserRepository> repository,
                std::shared_ptr<EmailService> emailService)
        : repository(std::move(repository))
        , emailService(std::move(emailService))
        , logger(spdlog::get("UserService")) {
        if (!logger) {
            logger = spdlog::stdout_color_mt("UserService");
        }
    }

    User createUser(const std::string& name, const std::string& email, int age) {
        logger->info("Creating user: {}", name);

        if (name.empty()) {
            throw std::invalid_argument("Name cannot be empty");
        }

        if (age < 0 || age > 150) {
            throw std::invalid_argument("Invalid age: " + std::to_string(age));
        }

        User user(name, email, age);
        repository->save(user);

        try {
            emailService->sendWelcomeEmail(user);
        } catch (const EmailException& e) {
            logger->warn("Failed to send welcome email: {}", e.what());
        }

        return user;
    }

    std::vector<User> getActiveUsers() {
        auto users = repository->findAll();

        // Filter active users
        std::vector<User> active;
        std::copy_if(users.begin(), users.end(), std::back_inserter(active),
            [](const User& u) { return u.isActive(); });

        // Sort by name
        std::sort(active.begin(), active.end(),
            [](const User& a, const User& b) {
                return a.getName() < b.getName();
            });

        return active;
    }

    // Or with C++20 ranges
    std::vector<User> getActiveUsersRanges() {
        auto users = repository->findAll();

        auto active = users
            | std::views::filter([](const User& u) { return u.isActive(); })
            | std::ranges::to<std::vector>();

        std::ranges::sort(active, {}, &User::getName);

        return active;
    }

    std::optional<User> updateUserAge(int64_t id, int newAge) {
        auto userOpt = repository->findById(id);

        if (userOpt.has_value()) {
            User& user = *userOpt;
            user.setAge(newAge);
            repository->save(user);
            logger->info("Updated user {} age to {}", id, newAge);
        }

        return userOpt;
    }
};
```

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `convert-golang-rust` - Similar systems language conversion patterns
- `lang-java-dev` - Java development patterns
- `lang-cpp-dev` - C++ development patterns

Cross-cutting pattern skills:
- `patterns-concurrency-dev` - Threading, mutexes, async patterns
- `patterns-serialization-dev` - JSON, data validation across languages
- `patterns-metaprogramming-dev` - Templates, generics, annotations
