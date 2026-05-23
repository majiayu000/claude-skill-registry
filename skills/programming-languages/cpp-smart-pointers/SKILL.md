---
name: cpp-smart-pointers
description: Use when managing memory safely in C++ with smart pointers including unique_ptr, shared_ptr, weak_ptr, and RAII patterns.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# C++ Smart Pointers and RAII

Master C++ smart pointers and Resource Acquisition Is Initialization (RAII)
patterns for automatic, exception-safe resource management. This skill covers
unique_ptr, shared_ptr, weak_ptr, custom deleters, and best practices for
modern C++ memory management.

## RAII Principles

Resource Acquisition Is Initialization is a fundamental C++ idiom where
resource lifetime is tied to object lifetime.

### Core Concept

```cpp
// Bad: Manual resource management
void process_file_bad() {
    FILE* file = fopen("data.txt", "r");
    if (!file) return;

    // ... process file ...
    // If exception occurs, file never closed!

    fclose(file);
}

// Good: RAII with smart pointer
void process_file_good() {
    auto deleter = [](FILE* f) { if (f) fclose(f); };
    std::unique_ptr<FILE, decltype(deleter)> file(fopen("data.txt", "r"), deleter);

    if (!file) return;

    // ... process file ...
    // File automatically closed when unique_ptr destroyed
}

// Even better: Custom RAII wrapper
class FileHandle {
    FILE* file;
public:
    explicit FileHandle(const char* filename, const char* mode)
        : file(fopen(filename, mode)) {
        if (!file) throw std::runtime_error("Failed to open file");
    }

    ~FileHandle() {
        if (file) fclose(file);
    }

    // Delete copy operations
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;

    // Allow move operations
    FileHandle(FileHandle&& other) noexcept : file(other.file) {
        other.file = nullptr;
    }

    FileHandle& operator=(FileHandle&& other) noexcept {
        if (this != &other) {
            if (file) fclose(file);
            file = other.file;
            other.file = nullptr;
        }
        return *this;
    }

    FILE* get() const { return file; }
};
```

### RAII Benefits

```cpp
// Exception safety
void transaction() {
    std::lock_guard<std::mutex> lock(mutex); // RAII lock
    std::unique_ptr<Resource> resource = acquire_resource(); // RAII memory

    // If exception thrown, lock released and memory freed automatically
    risky_operation();
}

// Automatic cleanup in all paths
std::unique_ptr<int[]> create_buffer(size_t size) {
    auto buffer = std::make_unique<int[]>(size);

    if (size > max_size) {
        return nullptr; // buffer cleaned up
    }

    initialize(buffer.get(), size);
    return buffer; // ownership transferred
}
```

## Unique Ptr

`std::unique_ptr` provides exclusive ownership of dynamically allocated objects.

### Unique Ptr Basic Usage

```cpp
#include <memory>

// Creating unique_ptr
std::unique_ptr<int> ptr1(new int(42));
auto ptr2 = std::make_unique<int>(100); // Preferred (C++14)

// Array unique_ptr
std::unique_ptr<int[]> arr(new int[10]);
auto arr2 = std::make_unique<int[]>(10); // Preferred

// Custom types
class MyClass {
public:
    MyClass(int x, std::string s) : value(x), name(s) {}
    void print() const { std::cout << name << ": " << value << std::endl; }
private:
    int value;
    std::string name;
};

auto obj = std::make_unique<MyClass>(42, "Test");
obj->print();
```

### Ownership Transfer

```cpp
// Unique_ptr is move-only, not copyable
std::unique_ptr<int> ptr1 = std::make_unique<int>(42);

// std::unique_ptr<int> ptr2 = ptr1; // ERROR: copying deleted

// Move ownership
std::unique_ptr<int> ptr2 = std::move(ptr1);
// ptr1 is now nullptr, ptr2 owns the resource

// Function accepting ownership
void consume(std::unique_ptr<int> ptr) {
    std::cout << *ptr << std::endl;
    // ptr destroyed here, resource deleted
}

consume(std::move(ptr2)); // Transfer ownership to function

// Function returning ownership
std::unique_ptr<int> create() {
    auto ptr = std::make_unique<int>(100);
    return ptr; // Move semantics, no explicit std::move needed
}

auto result = create(); // Ownership transferred to result
```

### Custom Deleters

```cpp
// Function pointer deleter
void custom_delete(int* ptr) {
    std::cout << "Deleting: " << *ptr << std::endl;
    delete ptr;
}

std::unique_ptr<int, decltype(&custom_delete)> ptr(new int(42), custom_delete);

// Lambda deleter
auto deleter = [](int* ptr) {
    std::cout << "Lambda delete: " << *ptr << std::endl;
    delete ptr;
};

std::unique_ptr<int, decltype(deleter)> ptr2(new int(100), deleter);

// FILE* with custom deleter
auto file_deleter = [](FILE* f) {
    if (f) {
        std::cout << "Closing file" << std::endl;
        fclose(f);
    }
};

std::unique_ptr<FILE, decltype(file_deleter)> file(
    fopen("data.txt", "r"),
    file_deleter
);

// Socket with custom deleter
struct SocketDeleter {
    void operator()(int* socket) const {
        if (socket && *socket >= 0) {
            close(*socket);
            delete socket;
        }
    }
};

std::unique_ptr<int, SocketDeleter> socket(new int(create_socket()));
```

### Unique Ptr Operations

```cpp
std::unique_ptr<int> ptr = std::make_unique<int>(42);

// Access
int value = *ptr;         // Dereference
int* raw = ptr.get();     // Get raw pointer (doesn't transfer ownership)

// Check if owns object
if (ptr) {
    std::cout << "Owns resource" << std::endl;
}

// Release ownership (returns raw pointer, unique_ptr becomes nullptr)
int* released = ptr.release();
// Must manually delete released pointer
delete released;

// Reset (delete current object, optionally take ownership of new one)
ptr.reset();                    // Delete and become nullptr
ptr.reset(new int(100));        // Delete old, own new

// Swap
std::unique_ptr<int> ptr1 = std::make_unique<int>(1);
std::unique_ptr<int> ptr2 = std::make_unique<int>(2);
ptr1.swap(ptr2);
// or
std::swap(ptr1, ptr2);
```

## Shared Ptr

`std::shared_ptr` provides shared ownership with automatic reference counting.

### Shared Ptr Basic Usage

```cpp
#include <memory>

// Creating shared_ptr
std::shared_ptr<int> ptr1(new int(42));
auto ptr2 = std::make_shared<int>(100); // Preferred (more efficient)

// Shared ownership
auto ptr3 = ptr2; // Reference count = 2
auto ptr4 = ptr2; // Reference count = 3

std::cout << "Use count: " << ptr2.use_count() << std::endl; // 3

// Last shared_ptr destroyed deletes the object
{
    auto ptr5 = ptr2; // Reference count = 4
} // ptr5 destroyed, reference count = 3
```

### Make Shared

```cpp
// Prefer make_shared over new
auto ptr1 = std::make_shared<MyClass>(arg1, arg2);

// Why? Single allocation instead of two:
// new: allocates object + separate control block
// make_shared: single allocation for both

// Exception safety
func(std::shared_ptr<int>(new int(1)), std::shared_ptr<int>(new int(2))); // Risky
func(std::make_shared<int>(1), std::make_shared<int>(2)); // Safe

// Array support (C++17 and later may vary by implementation)
std::shared_ptr<int[]> arr(new int[10]);
// Note: make_shared for arrays added in C++20
```

### Shared Ptr Operations

```cpp
std::shared_ptr<int> ptr1 = std::make_shared<int>(42);
std::shared_ptr<int> ptr2 = ptr1;

// Access
int value = *ptr1;
int* raw = ptr1.get();

// Reference counting
std::cout << "Count: " << ptr1.use_count() << std::endl;
std::cout << "Unique: " << ptr1.unique() << std::endl; // true if count == 1

// Check if owns object
if (ptr1) {
    std::cout << "Owns resource" << std::endl;
}

// Reset
ptr1.reset();                    // Decrement ref count, become nullptr
ptr1.reset(new int(100));        // Decrement old ref count, own new object
ptr1 = nullptr;                  // Same as reset()

// Swap
ptr1.swap(ptr2);
std::swap(ptr1, ptr2);
```

### Aliasing Constructor

```cpp
struct Data {
    int x;
    int y;
};

auto data = std::make_shared<Data>();
data->x = 10;
data->y = 20;

// Create shared_ptr to member, but shares ownership of whole object
std::shared_ptr<int> x_ptr(data, &data->x);
std::shared_ptr<int> y_ptr(data, &data->y);

// data's reference count is 3
// When data, x_ptr, and y_ptr all destroyed, Data object deleted
```

## Weak Ptr

`std::weak_ptr` provides non-owning references to shared_ptr-managed objects.

### Weak Ptr Basic Usage

```cpp
std::shared_ptr<int> shared = std::make_shared<int>(42);
std::weak_ptr<int> weak = shared; // weak reference, doesn't increase ref count

std::cout << "Shared count: " << shared.use_count() << std::endl; // 1
std::cout << "Weak count: " << weak.use_count() << std::endl;     // 1

// Check if object still exists
if (!weak.expired()) {
    // Try to get shared_ptr
    if (auto locked = weak.lock()) {
        std::cout << "Value: " << *locked << std::endl;
        // locked is shared_ptr, safe to use
    }
}

// After shared destroyed
shared.reset();
if (weak.expired()) {
    std::cout << "Object no longer exists" << std::endl;
}
```

### Breaking Circular References

```cpp
// Problem: Circular reference causes memory leak
struct Node {
    std::shared_ptr<Node> next;
    ~Node() { std::cout << "Node destroyed" << std::endl; }
};

void memory_leak() {
    auto node1 = std::make_shared<Node>();
    auto node2 = std::make_shared<Node>();

    node1->next = node2;
    node2->next = node1; // Circular reference!

    // node1 and node2 go out of scope but objects never deleted
    // ref counts never reach zero
}

// Solution: Use weak_ptr for back references
struct NodeFixed {
    std::shared_ptr<NodeFixed> next;
    std::weak_ptr<NodeFixed> prev; // Break cycle with weak_ptr

    ~NodeFixed() { std::cout << "NodeFixed destroyed" << std::endl; }
};

void no_leak() {
    auto node1 = std::make_shared<NodeFixed>();
    auto node2 = std::make_shared<NodeFixed>();

    node1->next = node2;
    node2->prev = node1; // weak_ptr doesn't increase ref count

    // Objects properly deleted when shared_ptrs destroyed
}
```

### Observer Pattern

```cpp
class Subject;

class Observer {
    std::weak_ptr<Subject> subject;
public:
    void observe(std::shared_ptr<Subject> s) {
        subject = s;
    }

    void check() {
        if (auto s = subject.lock()) {
            std::cout << "Subject still exists" << std::endl;
            // Use s safely
        } else {
            std::cout << "Subject destroyed" << std::endl;
        }
    }
};

class Subject {
public:
    void do_something() {
        std::cout << "Subject doing something" << std::endl;
    }
};

// Usage
auto observer = std::make_shared<Observer>();
{
    auto subject = std::make_shared<Subject>();
    observer->observe(subject);
    observer->check(); // Subject exists
}
observer->check(); // Subject destroyed
```

### Cache Pattern

```cpp
class ResourceCache {
    std::unordered_map<std::string, std::weak_ptr<Resource>> cache;

public:
    std::shared_ptr<Resource> get(const std::string& key) {
        // Try to get from cache
        auto it = cache.find(key);
        if (it != cache.end()) {
            if (auto resource = it->second.lock()) {
                return resource; // Cache hit
            } else {
                cache.erase(it); // Expired entry
            }
        }

        // Cache miss: load resource
        auto resource = std::make_shared<Resource>(load_resource(key));
        cache[key] = resource; // Store weak reference
        return resource;
    }

    void cleanup() {
        // Remove expired entries
        for (auto it = cache.begin(); it != cache.end(); ) {
            if (it->second.expired()) {
                it = cache.erase(it);
            } else {
                ++it;
            }
        }
    }
};
```

## Custom Deleters and Allocators

### Advanced Deleter Patterns

```cpp
// Logging deleter
template<typename T>
struct LoggingDeleter {
    void operator()(T* ptr) const {
        std::cout << "Deleting object at " << ptr << std::endl;
        delete ptr;
    }
};

std::unique_ptr<int, LoggingDeleter<int>> ptr(new int(42));

// Array deleter for unique_ptr
template<typename T>
struct ArrayDeleter {
    void operator()(T* ptr) const {
        delete[] ptr;
    }
};

std::unique_ptr<int, ArrayDeleter<int>> arr(new int[10]);

// Conditional deleter
template<typename T>
class ConditionalDeleter {
    bool should_delete;
public:
    explicit ConditionalDeleter(bool del = true) : should_delete(del) {}

    void operator()(T* ptr) const {
        if (should_delete) {
            delete ptr;
        }
    }
};

// Resource pool deleter
template<typename T>
class PoolDeleter {
    std::shared_ptr<ResourcePool<T>> pool;
public:
    explicit PoolDeleter(std::shared_ptr<ResourcePool<T>> p) : pool(p) {}

    void operator()(T* ptr) const {
        pool->return_to_pool(ptr); // Return to pool instead of delete
    }
};
```

### Custom Allocators

```cpp
// Custom allocator for shared_ptr
template<typename T>
class TrackingAllocator {
public:
    using value_type = T;

    TrackingAllocator() = default;

    template<typename U>
    TrackingAllocator(const TrackingAllocator<U>&) {}

    T* allocate(std::size_t n) {
        std::cout << "Allocating " << n << " objects" << std::endl;
        return static_cast<T*>(::operator new(n * sizeof(T)));
    }

    void deallocate(T* ptr, std::size_t n) {
        std::cout << "Deallocating " << n << " objects" << std::endl;
        ::operator delete(ptr);
    }
};

// Usage with shared_ptr
auto ptr = std::allocate_shared<int>(TrackingAllocator<int>(), 42);
```

## Smart Pointer Conversions

### Safe Conversions

```cpp
// unique_ptr to shared_ptr (ownership transfer)
std::unique_ptr<int> unique = std::make_unique<int>(42);
std::shared_ptr<int> shared = std::move(unique); // unique is now nullptr

// shared_ptr to weak_ptr
std::weak_ptr<int> weak = shared;

// weak_ptr to shared_ptr (with null check)
if (auto locked = weak.lock()) {
    // Use locked shared_ptr
}

// Raw pointer to shared_ptr (dangerous - see pitfalls)
int* raw = new int(42);
// std::shared_ptr<int> shared(raw); // Dangerous!
```

### Downcasting with Smart Pointers

```cpp
class Base {
public:
    virtual ~Base() = default;
    virtual void foo() = 0;
};

class Derived : public Base {
public:
    void foo() override {}
    void bar() {}
};

// static_pointer_cast (like static_cast)
std::shared_ptr<Base> base = std::make_shared<Derived>();
std::shared_ptr<Derived> derived = std::static_pointer_cast<Derived>(base);

// dynamic_pointer_cast (like dynamic_cast, returns nullptr on failure)
std::shared_ptr<Base> base2 = std::make_shared<Derived>();
if (auto derived2 = std::dynamic_pointer_cast<Derived>(base2)) {
    derived2->bar(); // Safe to call Derived methods
}

// const_pointer_cast (like const_cast)
std::shared_ptr<const int> const_ptr = std::make_shared<const int>(42);
std::shared_ptr<int> mutable_ptr = std::const_pointer_cast<int>(const_ptr);
```

## Performance Considerations

### Memory Overhead

```cpp
// sizeof comparisons
sizeof(int*)                           // 8 bytes (64-bit)
sizeof(std::unique_ptr<int>)           // 8 bytes (same as raw pointer)
sizeof(std::shared_ptr<int>)           // 16 bytes (pointer + control block ptr)
sizeof(std::weak_ptr<int>)             // 16 bytes (same as shared_ptr)

// Control block overhead for shared_ptr
// Contains: reference count, weak count, deleter, allocator
// Size varies but typically 24-32 bytes

// make_shared vs new for shared_ptr
auto ptr1 = std::make_shared<int>(42);     // 1 allocation
std::shared_ptr<int> ptr2(new int(42));    // 2 allocations
```

### Performance Optimization

```cpp
// Prefer unique_ptr when possible
std::unique_ptr<Resource> create_resource() {
    return std::make_unique<Resource>();
}

// Convert to shared_ptr only if needed
auto unique = create_resource();
std::shared_ptr<Resource> shared = std::move(unique);

// Avoid unnecessary copies of shared_ptr
void process(const std::shared_ptr<Resource>& res) { // Pass by const ref
    // Use res, doesn't increase ref count
}

// Move when transferring ownership
std::shared_ptr<Resource> transfer(std::shared_ptr<Resource> res) {
    return res; // RVO or move
}

// Use weak_ptr for non-owning references
class Observer {
    std::weak_ptr<Subject> subject; // Doesn't increase ref count
};
```

## Exception Safety

### Strong Exception Guarantee

```cpp
class ExceptionSafe {
    std::unique_ptr<Resource1> res1;
    std::unique_ptr<Resource2> res2;

public:
    void update(int value) {
        // Create new resources
        auto new_res1 = std::make_unique<Resource1>(value);
        auto new_res2 = std::make_unique<Resource2>(value);

        // If exception thrown above, no changes made (strong guarantee)

        // Commit changes (noexcept operations)
        res1 = std::move(new_res1);
        res2 = std::move(new_res2);
    }
};
```

### RAII for Transactions

```cpp
class Transaction {
    std::unique_ptr<Connection> conn;
    bool committed = false;

public:
    explicit Transaction(std::unique_ptr<Connection> c)
        : conn(std::move(c)) {
        conn->begin_transaction();
    }

    ~Transaction() {
        if (!committed) {
            try {
                conn->rollback();
            } catch (...) {
                // Log error, don't throw from destructor
            }
        }
    }

    void commit() {
        conn->commit();
        committed = true;
    }
};

// Usage
void perform_transaction() {
    auto conn = std::make_unique<Connection>();
    Transaction txn(std::move(conn));

    // Do work
    // If exception thrown, transaction automatically rolled back

    txn.commit(); // Explicit commit on success
}
```

## Smart Pointers in Containers

### Vectors of Smart Pointers

```cpp
// Vector of unique_ptr
std::vector<std::unique_ptr<Widget>> widgets;

// Add elements (must move)
widgets.push_back(std::make_unique<Widget>(1));
widgets.push_back(std::make_unique<Widget>(2));

// Can't copy vector
// auto vec2 = widgets; // ERROR

// Can move vector
auto vec2 = std::move(widgets); // widgets now empty

// Iterate
for (const auto& widget : vec2) {
    widget->process();
}

// Remove element (automatically deleted)
vec2.erase(vec2.begin());

// Vector of shared_ptr
std::vector<std::shared_ptr<Widget>> shared_widgets;
shared_widgets.push_back(std::make_shared<Widget>(1));

// Can copy vector (increases ref counts)
auto shared_vec2 = shared_widgets;
```

### Maps with Smart Pointers

```cpp
// Map with unique_ptr values
std::map<std::string, std::unique_ptr<Resource>> resource_map;

// Insert
resource_map["key1"] = std::make_unique<Resource>(1);
resource_map.emplace("key2", std::make_unique<Resource>(2));

// Find and use
auto it = resource_map.find("key1");
if (it != resource_map.end()) {
    it->second->process();
}

// Extract ownership
auto extracted = std::move(resource_map["key1"]);
resource_map.erase("key1");

// Map with shared_ptr for shared ownership
std::map<std::string, std::shared_ptr<Resource>> shared_map;
shared_map["key"] = std::make_shared<Resource>(1);

// Multiple maps can share same resource
std::map<std::string, std::shared_ptr<Resource>> shared_map2;
shared_map2["key"] = shared_map["key"]; // Shares ownership
```

## Common Patterns

### Factory Pattern

```cpp
class Product {
public:
    virtual ~Product() = default;
    virtual void use() = 0;
};

class ConcreteProductA : public Product {
public:
    void use() override { std::cout << "Using A" << std::endl; }
};

class ConcreteProductB : public Product {
public:
    void use() override { std::cout << "Using B" << std::endl; }
};

class Factory {
public:
    static std::unique_ptr<Product> create(const std::string& type) {
        if (type == "A") {
            return std::make_unique<ConcreteProductA>();
        } else if (type == "B") {
            return std::make_unique<ConcreteProductB>();
        }
        return nullptr;
    }
};

// Usage
auto product = Factory::create("A");
if (product) {
    product->use();
}
```

### Pimpl Idiom

```cpp
// Widget.h
class Widget {
public:
    Widget();
    ~Widget();

    // Must declare but not define in header
    Widget(Widget&&) noexcept;
    Widget& operator=(Widget&&) noexcept;

    void do_something();

private:
    class Impl; // Forward declaration
    std::unique_ptr<Impl> pimpl;
};

// Widget.cpp
class Widget::Impl {
public:
    void do_something_impl() {
        // Implementation details hidden
    }

private:
    // Private members not in public header
    std::vector<int> data;
    std::string name;
};

Widget::Widget() : pimpl(std::make_unique<Impl>()) {}

// Define destructor in .cpp after Impl is complete
Widget::~Widget() = default;

Widget::Widget(Widget&&) noexcept = default;
Widget& Widget::operator=(Widget&&) noexcept = default;

void Widget::do_something() {
    pimpl->do_something_impl();
}
```

### Singleton Pattern

```cpp
class Singleton {
public:
    static Singleton& instance() {
        static Singleton instance; // Thread-safe in C++11
        return instance;
    }

    // Delete copy and move
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;
    Singleton(Singleton&&) = delete;
    Singleton& operator=(Singleton&&) = delete;

    void do_something() {
        std::cout << "Singleton method" << std::endl;
    }

private:
    Singleton() = default;
    ~Singleton() = default;
};

// Alternative: Smart pointer for explicit control
class ManagedSingleton {
public:
    static std::shared_ptr<ManagedSingleton> instance() {
        static auto inst = std::make_shared<ManagedSingleton>(PrivateTag{});
        return inst;
    }

private:
    struct PrivateTag {};
public:
    explicit ManagedSingleton(PrivateTag) {}
};
```

## Best Practices

1. **Prefer make_unique and make_shared**: More efficient and exception-safe
   than using new directly
2. **Use unique_ptr by default**: Only use shared_ptr when you actually need
   shared ownership
3. **Pass smart pointers by const reference**: Avoid unnecessary reference
   count changes with shared_ptr
4. **Use weak_ptr to break cycles**: Prevent memory leaks from circular
   shared_ptr references
5. **Return by value for ownership transfer**: Let move semantics handle
   efficient transfer
6. **Never create multiple shared_ptrs from same raw pointer**: Causes double
   deletion
7. **Custom deleters for non-memory resources**: Use for files, sockets,
   mutexes, etc.
8. **Mark move operations noexcept**: Enables optimizations in standard
   containers
9. **Use smart pointers in containers**: Allows containers of polymorphic
   objects
10. **Don't mix smart pointers with raw pointer ownership**: Choose one
    ownership model

## Common Pitfalls

1. **Creating shared_ptr from raw this pointer**: Use enable_shared_from_this
   instead
2. **Circular shared_ptr references**: Use weak_ptr for back references or
   parent pointers
3. **Creating multiple shared_ptrs from same raw pointer**: Causes double
   deletion
4. **Using get() to create new smart pointer**: Breaks ownership model
5. **Forgetting to use move with unique_ptr**: unique_ptr is not copyable
6. **Mixing smart pointers with manual delete**: Use one ownership model
   consistently
7. **Using shared_ptr when unique_ptr suffices**: Unnecessary overhead
8. **Not checking weak_ptr.lock() return value**: May return nullptr if object
   deleted
9. **Custom deleter issues**: Wrong deleter type or not handling nullptr
10. **Slicing with smart pointers**: Store base class pointers to preserve
    polymorphism

## When to Use

Use this skill when:

- Managing dynamically allocated memory in C++
- Implementing RAII patterns for resource management
- Working with polymorphic objects in containers
- Preventing memory leaks and dangling pointers
- Implementing exception-safe code
- Creating factory patterns or object hierarchies
- Managing shared resources with reference counting
- Breaking circular dependencies with weak references
- Wrapping C APIs with automatic cleanup
- Teaching or learning modern C++ memory management

## Resources

- [C++ Reference - unique_ptr](https://en.cppreference.com/w/cpp/memory/unique_ptr)
- [C++ Reference - shared_ptr](https://en.cppreference.com/w/cpp/memory/shared_ptr)
- [C++ Reference - weak_ptr](https://en.cppreference.com/w/cpp/memory/weak_ptr)
- [C++ Reference - make_unique](https://en.cppreference.com/w/cpp/memory/unique_ptr/make_unique)
- [C++ Reference - make_shared](https://en.cppreference.com/w/cpp/memory/shared_ptr/make_shared)
- [C++ Reference - enable_shared_from_this](https://en.cppreference.com/w/cpp/memory/enable_shared_from_this)
- [GotW #91: Smart Pointer Parameters](https://herbsutter.com/2013/06/05/gotw-91-solution-smart-pointer-parameters/)
- [Effective Modern C++ by Scott Meyers](https://www.oreilly.com/library/view/effective-modern-c/9781491908419/)
- [CppCoreGuidelines - Resource Management](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r-resource-management)
