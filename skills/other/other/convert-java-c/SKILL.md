---
name: convert-java-c
description: Convert Java code to idiomatic C. Use when migrating Java projects to C, translating Java patterns to idiomatic C, or refactoring Java codebases for performance, minimal runtime dependencies, and systems programming. Extends meta-convert-dev with Java-to-C specific patterns.
---

# Convert Java to C

Convert Java code to idiomatic C. This skill extends `meta-convert-dev` with Java-to-C specific type mappings, idiom translations, and tooling for transforming managed, object-oriented Java code into manual, procedural C.

## This Skill Extends

- `meta-convert-dev` - Foundational conversion patterns (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see the meta-skill first.

## This Skill Adds

- **Type mappings**: Java types → C types (managed → manual memory)
- **Idiom translations**: Java OOP patterns → C procedural/opaque pointer patterns
- **Error handling**: Exceptions → error codes + errno
- **Concurrency**: Java threads/synchronized → pthreads/mutexes
- **Memory/Ownership**: GC + automatic cleanup → malloc/free + manual management
- **Object-Oriented → Procedural**: Classes/interfaces → structs + function pointers

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- Java language fundamentals - see `lang-java-dev`
- C language fundamentals - see `lang-c-dev`
- Reverse conversion (C → Java) - see `convert-c-java`

---

## Quick Reference

| Java | C | Notes |
|------|---|-------|
| `int` | `int32_t` | Guaranteed 32-bit |
| `long` | `int64_t` | Guaranteed 64-bit |
| `byte` | `int8_t` | Signed 8-bit |
| `short` | `int16_t` | Signed 16-bit |
| `char` | `uint16_t` or `wchar_t` | Java char is UTF-16 |
| `float` | `float` | 32-bit IEEE 754 |
| `double` | `double` | 64-bit IEEE 754 |
| `boolean` | `bool` (C99+) or `int` | Use stdbool.h |
| `String` | `char*` or custom struct | Null-terminated or length-tracked |
| `ArrayList<T>` | `T*` + size/capacity | Manual dynamic array |
| `HashMap<K,V>` | Custom hash table | Use uthash or implement |
| `null` | `NULL` | Pointer null |
| `Object` | `void*` | Type-erased pointer |
| `interface` | `struct` with function pointers | Vtable pattern |
| `Exception` | `int` error code + `errno` | Manual error propagation |
| `synchronized` | `pthread_mutex_t` | Manual locking |
| `Thread` | `pthread_t` | POSIX threads |

## When Converting Code

1. **Analyze source thoroughly** before writing target
2. **Map types first** - create type equivalence table (Java primitives have exact C equivalents)
3. **Preserve semantics** over syntax similarity
4. **Plan memory management** - who owns what, when to free
5. **Adopt C idioms** - don't write "Java code in C syntax"
6. **Handle edge cases** - null, exceptions, array bounds
7. **Test equivalence** - same inputs → same outputs

---

## Type System Mapping

### Primitive Types

| Java | C | Notes |
|------|---|-------|
| `byte` | `int8_t` | Signed 8-bit (-128 to 127) |
| `short` | `int16_t` | Signed 16-bit (-32,768 to 32,767) |
| `int` | `int32_t` | Signed 32-bit |
| `long` | `int64_t` | Signed 64-bit |
| `char` | `uint16_t` or `wchar_t` | Java char is UTF-16 (2 bytes) |
| `float` | `float` | 32-bit IEEE 754 |
| `double` | `double` | 64-bit IEEE 754 |
| `boolean` | `bool` (C99+) or `int` | Use `#include <stdbool.h>` |
| `void` | `void` | No return value |

**Critical Note on char**: Java's `char` is a UTF-16 code unit (unsigned 16-bit). C's `char` is an ASCII character (8-bit). For Java String → C conversion, use UTF-8 `char*` or wide characters (`wchar_t*`).

### String Types

| Java | C | Notes |
|------|---|-------|
| `String` | `const char*` | Immutable, null-terminated |
| `String` | `char*` | Mutable, null-terminated |
| `StringBuilder` | `char*` + manual realloc | Dynamic buffer |
| `char[]` | `char*` or `uint16_t*` | Depends on encoding |

**String Encoding**: Java strings are UTF-16. C typically uses UTF-8. Convert using `iconv` or manual UTF-16 → UTF-8 conversion.

### Collection Types

| Java | C | Notes |
|------|---|-------|
| `ArrayList<T>` | `T*` + `size_t size, capacity` | Manual dynamic array |
| `LinkedList<T>` | `struct Node { T data; struct Node* next; }` | Manual linked list |
| `HashMap<K,V>` | `struct Entry { K key; V value; }*` + hash | Use uthash library or custom |
| `HashSet<T>` | `HashMap<T, bool>` or custom | Hash table with presence |
| `T[]` | `T*` + `size_t length` | Fixed-size or dynamic |
| `Queue<T>` | `T*` + head/tail pointers | Circular buffer or linked list |
| `Stack<T>` | `T*` + top pointer | Array-based stack |

### Object Types

| Java | C | Notes |
|------|---|-------|
| `class` | `struct` | Data + opaque pointer pattern |
| `interface` | `struct` with function pointers | Vtable pattern |
| `abstract class` | `struct` + function pointer vtable | Partial implementation |
| `enum` | `enum` or `#define` constants | C enums are just ints |
| `Object` | `void*` | Type-erased pointer (avoid) |
| `null` | `NULL` | Null pointer |

### Generic Types → Type Erasure or Macros

| Java | C | Notes |
|------|---|-------|
| `List<T>` | Separate type per `T` or `void*` | No generics; use macros or code generation |
| `<T extends Comparable>` | Function pointer for comparison | Pass comparator explicitly |
| `Map<K, V>` | Separate hash table per type | Or use `void*` with casting |

**Approach 1: Type-specific implementations**
```c
// int_list.h
typedef struct {
    int *data;
    size_t size;
    size_t capacity;
} IntList;

// string_list.h
typedef struct {
    char **data;
    size_t size;
    size_t capacity;
} StringList;
```

**Approach 2: Generic with void* (less type-safe)**
```c
typedef struct {
    void **data;
    size_t size;
    size_t capacity;
} GenericList;
```

**Approach 3: Macros (type-safe, compile-time)**
```c
#define DEFINE_LIST(T, PREFIX) \
typedef struct { \
    T *data; \
    size_t size, capacity; \
} PREFIX##List;
```

---

## Idiom Translation

### Pattern 1: Object Creation and Destruction

**Java:**
```java
// Constructor
public class User {
    private String name;
    private int age;

    public User(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // Destructor (finalize - rarely used)
    @Override
    protected void finalize() {
        // Cleanup
    }
}

// Usage
User user = new User("Alice", 30);
// GC handles cleanup automatically
```

**C:**
```c
// Opaque pointer pattern
typedef struct User User;

// Constructor
User* user_create(const char *name, int age) {
    User *user = malloc(sizeof(User));
    if (user == NULL) {
        return NULL;
    }
    user->name = strdup(name);  // Allocate copy
    user->age = age;
    return user;
}

// Destructor
void user_destroy(User *user) {
    if (user != NULL) {
        free(user->name);
        free(user);
    }
}

// Usage
User *user = user_create("Alice", 30);
if (user != NULL) {
    // Use user...
    user_destroy(user);
}
```

**Why this translation:**
- Java handles memory automatically with GC; C requires manual `malloc`/`free`
- Opaque pointers hide implementation details (similar to Java private fields)
- Constructor/destructor pattern mimics Java's object lifecycle
- Always check `malloc` return for NULL (Java throws OutOfMemoryError)

### Pattern 2: Null Handling

**Java:**
```java
// Nullable reference
String name = getUser(id);
if (name != null) {
    System.out.println(name.toUpperCase());
} else {
    System.out.println("Unknown");
}

// Optional (Java 8+)
Optional<String> nameOpt = Optional.ofNullable(getUser(id));
String upper = nameOpt.map(String::toUpperCase).orElse("Unknown");
```

**C:**
```c
// Null pointer check
char *name = get_user(id);
if (name != NULL) {
    // Create uppercase copy
    char upper[256];
    size_t i;
    for (i = 0; i < sizeof(upper) - 1 && name[i] != '\0'; i++) {
        upper[i] = toupper(name[i]);
    }
    upper[i] = '\0';
    printf("%s\n", upper);
} else {
    printf("Unknown\n");
}
free(name);

// Optional-like pattern (C11+)
typedef struct {
    bool present;
    char value[256];
} OptionalString;

OptionalString get_user_optional(int id) {
    OptionalString opt = {0};
    char *name = get_user(id);
    if (name != NULL) {
        opt.present = true;
        strncpy(opt.value, name, sizeof(opt.value) - 1);
        free(name);
    }
    return opt;
}
```

**Why this translation:**
- C has no built-in Optional type; must check NULL explicitly
- Manual memory management: know when to free returned pointers
- C strings are mutable; modifications require copying

### Pattern 3: Exception Handling → Error Codes

**Java:**
```java
public void processFile(String path) throws IOException {
    File file = new File(path);
    if (!file.exists()) {
        throw new FileNotFoundException(path);
    }

    try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
        String line = reader.readLine();
        // Process...
    } catch (IOException e) {
        throw new IOException("Failed to read " + path, e);
    }
}
```

**C:**
```c
#include <errno.h>

// Error codes
#define SUCCESS 0
#define ERR_FILE_NOT_FOUND -1
#define ERR_IO_ERROR -2

int process_file(const char *path) {
    // Check file exists
    if (access(path, F_OK) != 0) {
        errno = ENOENT;
        return ERR_FILE_NOT_FOUND;
    }

    FILE *file = fopen(path, "r");
    if (file == NULL) {
        // errno set by fopen
        return ERR_IO_ERROR;
    }

    char buffer[256];
    if (fgets(buffer, sizeof(buffer), file) == NULL) {
        fclose(file);
        return ERR_IO_ERROR;
    }

    // Process...

    fclose(file);
    return SUCCESS;
}

// Usage
int result = process_file("data.txt");
if (result != SUCCESS) {
    fprintf(stderr, "Error: %s (code %d)\n", strerror(errno), result);
}
```

**Why this translation:**
- C has no exceptions; use return codes and `errno`
- `errno` is a thread-local global for system error details
- Check every I/O operation return value
- Manual resource cleanup (no try-with-resources)

### Pattern 4: Interfaces → Function Pointer Vtables

**Java:**
```java
interface Drawable {
    void draw();
    int getWidth();
}

class Circle implements Drawable {
    private int radius;

    public Circle(int radius) {
        this.radius = radius;
    }

    @Override
    public void draw() {
        System.out.println("Drawing circle");
    }

    @Override
    public int getWidth() {
        return radius * 2;
    }
}
```

**C:**
```c
// Interface as vtable
typedef struct Drawable Drawable;

typedef struct {
    void (*draw)(Drawable *self);
    int (*get_width)(Drawable *self);
} DrawableVTable;

struct Drawable {
    const DrawableVTable *vtable;
    void *impl;  // Opaque implementation
};

// Circle implementation
typedef struct {
    int radius;
} Circle;

static void circle_draw(Drawable *self) {
    Circle *circle = (Circle *)self->impl;
    printf("Drawing circle with radius %d\n", circle->radius);
}

static int circle_get_width(Drawable *self) {
    Circle *circle = (Circle *)self->impl;
    return circle->radius * 2;
}

static const DrawableVTable circle_vtable = {
    .draw = circle_draw,
    .get_width = circle_get_width,
};

// Constructor
Drawable* circle_create(int radius) {
    Circle *circle = malloc(sizeof(Circle));
    if (circle == NULL) return NULL;

    circle->radius = radius;

    Drawable *drawable = malloc(sizeof(Drawable));
    if (drawable == NULL) {
        free(circle);
        return NULL;
    }

    drawable->vtable = &circle_vtable;
    drawable->impl = circle;
    return drawable;
}

// Usage
Drawable *obj = circle_create(10);
obj->vtable->draw(obj);           // Polymorphic call
int width = obj->vtable->get_width(obj);
```

**Why this translation:**
- C has no built-in polymorphism; simulate with function pointer tables (vtables)
- `void *impl` stores the concrete type (requires casting)
- Vtable stores function pointers for interface methods
- Manual vtable initialization (Java does this automatically)

### Pattern 5: ArrayList → Dynamic Array

**Java:**
```java
ArrayList<Integer> numbers = new ArrayList<>();
numbers.add(1);
numbers.add(2);
numbers.add(3);

for (int num : numbers) {
    System.out.println(num);
}

numbers.remove(1);  // Remove at index 1
```

**C:**
```c
typedef struct {
    int *data;
    size_t size;
    size_t capacity;
} IntList;

IntList* int_list_create(void) {
    IntList *list = malloc(sizeof(IntList));
    if (list == NULL) return NULL;

    list->data = malloc(10 * sizeof(int));  // Initial capacity
    if (list->data == NULL) {
        free(list);
        return NULL;
    }

    list->size = 0;
    list->capacity = 10;
    return list;
}

int int_list_add(IntList *list, int value) {
    if (list->size >= list->capacity) {
        // Resize (double capacity)
        size_t new_capacity = list->capacity * 2;
        int *new_data = realloc(list->data, new_capacity * sizeof(int));
        if (new_data == NULL) {
            return -1;  // Failed to resize
        }
        list->data = new_data;
        list->capacity = new_capacity;
    }

    list->data[list->size++] = value;
    return 0;
}

void int_list_remove_at(IntList *list, size_t index) {
    if (index >= list->size) return;

    // Shift elements left
    for (size_t i = index; i < list->size - 1; i++) {
        list->data[i] = list->data[i + 1];
    }
    list->size--;
}

void int_list_destroy(IntList *list) {
    if (list != NULL) {
        free(list->data);
        free(list);
    }
}

// Usage
IntList *numbers = int_list_create();
int_list_add(numbers, 1);
int_list_add(numbers, 2);
int_list_add(numbers, 3);

for (size_t i = 0; i < numbers->size; i++) {
    printf("%d\n", numbers->data[i]);
}

int_list_remove_at(numbers, 1);
int_list_destroy(numbers);
```

**Why this translation:**
- Java ArrayList auto-grows; C requires manual `realloc`
- Track both `size` (current elements) and `capacity` (allocated space)
- Manual bounds checking (Java throws IndexOutOfBoundsException)
- Explicit destroy function to free memory

### Pattern 6: HashMap → Custom Hash Table

**Java:**
```java
HashMap<String, Integer> ages = new HashMap<>();
ages.put("Alice", 30);
ages.put("Bob", 25);

Integer age = ages.get("Alice");
if (age != null) {
    System.out.println(age);
}

ages.remove("Bob");
```

**C:**
```c
// Using uthash library: https://troydhanson.github.io/uthash/
#include "uthash.h"

typedef struct {
    char *key;
    int value;
    UT_hash_handle hh;
} Entry;

Entry *ages = NULL;  // Hash table head

// Put
void put(const char *key, int value) {
    Entry *entry;
    HASH_FIND_STR(ages, key, entry);

    if (entry == NULL) {
        entry = malloc(sizeof(Entry));
        entry->key = strdup(key);
        entry->value = value;
        HASH_ADD_KEYPTR(hh, ages, entry->key, strlen(entry->key), entry);
    } else {
        entry->value = value;  // Update existing
    }
}

// Get
int get(const char *key, int *out_value) {
    Entry *entry;
    HASH_FIND_STR(ages, key, entry);

    if (entry != NULL) {
        *out_value = entry->value;
        return 1;  // Found
    }
    return 0;  // Not found
}

// Remove
void remove_key(const char *key) {
    Entry *entry;
    HASH_FIND_STR(ages, key, entry);

    if (entry != NULL) {
        HASH_DEL(ages, entry);
        free(entry->key);
        free(entry);
    }
}

// Cleanup
void destroy_all(void) {
    Entry *entry, *tmp;
    HASH_ITER(hh, ages, entry, tmp) {
        HASH_DEL(ages, entry);
        free(entry->key);
        free(entry);
    }
}

// Usage
put("Alice", 30);
put("Bob", 25);

int age;
if (get("Alice", &age)) {
    printf("%d\n", age);
}

remove_key("Bob");
destroy_all();
```

**Why this translation:**
- C has no built-in hash table; use libraries (uthash, glib) or implement manually
- Manual key copying (`strdup`) and freeing
- Return values indicate success/failure (no null to indicate missing)
- Iteration requires library-specific macros

### Pattern 7: Synchronized → Mutexes

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

**C:**
```c
#include <pthread.h>

typedef struct {
    int count;
    pthread_mutex_t mutex;
} Counter;

Counter* counter_create(void) {
    Counter *counter = malloc(sizeof(Counter));
    if (counter == NULL) return NULL;

    counter->count = 0;
    pthread_mutex_init(&counter->mutex, NULL);
    return counter;
}

void counter_increment(Counter *counter) {
    pthread_mutex_lock(&counter->mutex);
    counter->count++;
    pthread_mutex_unlock(&counter->mutex);
}

int counter_get(Counter *counter) {
    pthread_mutex_lock(&counter->mutex);
    int value = counter->count;
    pthread_mutex_unlock(&counter->mutex);
    return value;
}

void counter_destroy(Counter *counter) {
    if (counter != NULL) {
        pthread_mutex_destroy(&counter->mutex);
        free(counter);
    }
}
```

**Why this translation:**
- Java `synchronized` is automatic; C requires explicit lock/unlock
- Must remember to unlock (Java does this automatically even on exception)
- Consider using atomics (`atomic_int`) for simple counters (C11+)
- Initialize and destroy mutexes explicitly

### Pattern 8: Thread Creation

**Java:**
```java
Thread thread = new Thread(() -> {
    System.out.println("Running in thread");
});
thread.start();
thread.join();
```

**C:**
```c
#include <pthread.h>
#include <stdio.h>

void* thread_function(void *arg) {
    printf("Running in thread\n");
    return NULL;
}

int main(void) {
    pthread_t thread;

    if (pthread_create(&thread, NULL, thread_function, NULL) != 0) {
        perror("pthread_create");
        return 1;
    }

    if (pthread_join(thread, NULL) != 0) {
        perror("pthread_join");
        return 1;
    }

    return 0;
}
```

**Why this translation:**
- Java Thread wraps OS threads; C uses POSIX threads directly
- Function pointers instead of lambda/Runnable
- Manual error checking (Java throws exceptions)
- No automatic thread pooling (Java ExecutorService)

---

## Paradigm Translation

### Mental Model Shift: Object-Oriented → Procedural

| Java Concept | C Approach | Key Insight |
|--------------|------------|-------------|
| Class with state | `struct` + opaque pointer | Data separated from functions |
| Method | Function with `self` pointer | Explicit `this` as first parameter |
| Inheritance | Struct embedding + casting | Manual vtable for polymorphism |
| Interface | Function pointer table | Manual dispatch |
| Constructor | `create()` function | Explicit allocation with `malloc` |
| Destructor/finalize | `destroy()` function | Manual cleanup with `free` |
| `new` keyword | `malloc` + initialization | Manual memory allocation |
| GC | Manual `free` | Explicit deallocation |
| Access modifiers | Opaque pointers + header/impl split | Module-level visibility |

### Memory Management Mental Model

| Java Model | C Model | Conceptual Translation |
|------------|---------|------------------------|
| Automatic GC | Manual malloc/free | Ownership tracking is manual |
| References | Pointers | Explicit addresses |
| Array bounds checking | Manual checks or buffer overflow | No automatic safety |
| String immutability | Mutable char arrays | Manual copying for safety |
| No dangling references | Dangling pointers possible | Use-after-free bugs possible |

### Error Handling Mental Model

| Java Model | C Model | Conceptual Translation |
|------------|---------|------------------------|
| Exceptions | Error codes | No stack unwinding |
| try-catch | if (error) { handle } | Manual propagation |
| finally | goto cleanup pattern | Manual resource release |
| Checked exceptions | Function documentation | Compiler doesn't enforce |
| Stack traces | Manual logging | No automatic context |

---

## Error Handling

### Java Exception Model → C Error Codes

**Java Approach:**
- Exceptions for error conditions
- Stack unwinding for cleanup
- Checked vs unchecked exceptions
- Try-catch-finally blocks

**C Approach:**
- Return codes for error conditions
- Manual cleanup with goto or careful ordering
- `errno` for system call errors
- Explicit error checking at every call

**Pattern: Error Code + errno**

```c
// Error codes
typedef enum {
    SUCCESS = 0,
    ERR_NULL_POINTER = -1,
    ERR_OUT_OF_MEMORY = -2,
    ERR_FILE_NOT_FOUND = -3,
    ERR_IO_ERROR = -4,
} ErrorCode;

// Function with error handling
ErrorCode read_config(const char *path, Config **out) {
    if (path == NULL || out == NULL) {
        return ERR_NULL_POINTER;
    }

    FILE *file = fopen(path, "r");
    if (file == NULL) {
        errno = ENOENT;
        return ERR_FILE_NOT_FOUND;
    }

    Config *config = malloc(sizeof(Config));
    if (config == NULL) {
        fclose(file);
        return ERR_OUT_OF_MEMORY;
    }

    // Read data...
    if (fgets(config->buffer, sizeof(config->buffer), file) == NULL) {
        free(config);
        fclose(file);
        return ERR_IO_ERROR;
    }

    fclose(file);
    *out = config;
    return SUCCESS;
}

// Usage with goto cleanup pattern
ErrorCode process(void) {
    Config *config = NULL;
    Data *data = NULL;
    ErrorCode result = SUCCESS;

    result = read_config("app.conf", &config);
    if (result != SUCCESS) {
        goto cleanup;
    }

    data = malloc(sizeof(Data));
    if (data == NULL) {
        result = ERR_OUT_OF_MEMORY;
        goto cleanup;
    }

    // Process...

cleanup:
    free(data);
    free(config);
    return result;
}
```

---

## Concurrency Patterns

### Java Concurrency → POSIX Threads

**Java Model:**
- Thread class + Runnable interface
- `synchronized` keyword
- `wait()` / `notify()`
- ExecutorService thread pools
- CompletableFuture

**C Model:**
- pthread_t + function pointers
- pthread_mutex_t explicit locks
- pthread_cond_t condition variables
- Manual thread pool implementation
- No built-in async/await

**Pattern: Producer-Consumer with Condition Variables**

**Java:**
```java
class Queue {
    private LinkedList<Integer> items = new LinkedList<>();
    private final int MAX = 10;

    public synchronized void put(int item) throws InterruptedException {
        while (items.size() >= MAX) {
            wait();
        }
        items.add(item);
        notifyAll();
    }

    public synchronized int take() throws InterruptedException {
        while (items.isEmpty()) {
            wait();
        }
        int item = items.removeFirst();
        notifyAll();
        return item;
    }
}
```

**C:**
```c
#include <pthread.h>

#define MAX_QUEUE 10

typedef struct {
    int items[MAX_QUEUE];
    int head, tail, count;
    pthread_mutex_t mutex;
    pthread_cond_t not_full;
    pthread_cond_t not_empty;
} Queue;

Queue* queue_create(void) {
    Queue *q = malloc(sizeof(Queue));
    if (q == NULL) return NULL;

    q->head = q->tail = q->count = 0;
    pthread_mutex_init(&q->mutex, NULL);
    pthread_cond_init(&q->not_full, NULL);
    pthread_cond_init(&q->not_empty, NULL);
    return q;
}

void queue_put(Queue *q, int item) {
    pthread_mutex_lock(&q->mutex);

    while (q->count >= MAX_QUEUE) {
        pthread_cond_wait(&q->not_full, &q->mutex);
    }

    q->items[q->tail] = item;
    q->tail = (q->tail + 1) % MAX_QUEUE;
    q->count++;

    pthread_cond_signal(&q->not_empty);
    pthread_mutex_unlock(&q->mutex);
}

int queue_take(Queue *q) {
    pthread_mutex_lock(&q->mutex);

    while (q->count == 0) {
        pthread_cond_wait(&q->not_empty, &q->mutex);
    }

    int item = q->items[q->head];
    q->head = (q->head + 1) % MAX_QUEUE;
    q->count--;

    pthread_cond_signal(&q->not_full);
    pthread_mutex_unlock(&q->mutex);

    return item;
}

void queue_destroy(Queue *q) {
    if (q != NULL) {
        pthread_mutex_destroy(&q->mutex);
        pthread_cond_destroy(&q->not_full);
        pthread_cond_destroy(&q->not_empty);
        free(q);
    }
}
```

**Why this translation:**
- Java `wait()` / `notifyAll()` → `pthread_cond_wait()` / `pthread_cond_signal()`
- Java `synchronized` → explicit `pthread_mutex_lock/unlock`
- Manual mutex management (Java does it automatically)
- Condition variables require associated mutex

---

## Memory & Ownership

### Java GC → C Manual Memory Management

**Key Differences:**

| Aspect | Java | C |
|--------|------|---|
| Allocation | `new Object()` | `malloc(sizeof(Object))` |
| Deallocation | Automatic (GC) | Manual (`free()`) |
| Dangling references | Impossible | Possible (use-after-free) |
| Memory leaks | Possible (unreachable but referenced) | Possible (forgot to free) |
| Null checks | NullPointerException at runtime | Segmentation fault |
| Initialization | Guaranteed (default values) | Uninitialized (garbage) |

**Ownership Patterns in C:**

1. **Caller owns, callee borrows** (most common)
```c
void process_user(const User *user) {
    // user is borrowed, don't free
    printf("%s\n", user->name);
}

User *user = user_create("Alice", 30);
process_user(user);
user_destroy(user);  // Caller frees
```

2. **Callee owns, caller receives**
```c
char* create_greeting(const char *name) {
    char *greeting = malloc(100);
    snprintf(greeting, 100, "Hello, %s!", name);
    return greeting;  // Caller must free
}

char *msg = create_greeting("Alice");
printf("%s\n", msg);
free(msg);  // Caller frees
```

3. **Shared ownership (ref counting)**
```c
typedef struct {
    Data data;
    int ref_count;
} RefCounted;

RefCounted* ref_create(void) {
    RefCounted *r = malloc(sizeof(RefCounted));
    r->ref_count = 1;
    return r;
}

void ref_retain(RefCounted *r) {
    r->ref_count++;
}

void ref_release(RefCounted *r) {
    r->ref_count--;
    if (r->ref_count == 0) {
        free(r);
    }
}
```

---

## Common Pitfalls

1. **Forgetting to free memory**
   - **Issue**: Java GC handles cleanup; C requires manual `free()`
   - **Solution**: Every `malloc` should have a corresponding `free`; use goto cleanup pattern

2. **Null pointer dereference**
   - **Issue**: Java throws NullPointerException; C crashes with segfault
   - **Solution**: Check pointers before dereferencing: `if (ptr != NULL) { ... }`

3. **Buffer overflow**
   - **Issue**: Java arrays are bounds-checked; C arrays are not
   - **Solution**: Use `strncpy`, `snprintf`, track array sizes, validate indices

4. **Use-after-free**
   - **Issue**: Java GC prevents this; C allows accessing freed memory
   - **Solution**: Set pointers to NULL after freeing; use tools like valgrind

5. **String encoding mismatch**
   - **Issue**: Java strings are UTF-16; C strings are typically UTF-8 or ASCII
   - **Solution**: Convert encoding explicitly; use `iconv` library or manual conversion

6. **Integer overflow**
   - **Issue**: Java detects overflow (throws exception or wraps); C wraps silently
   - **Solution**: Use safe math libraries or check before operations

7. **Thread safety**
   - **Issue**: Java `synchronized` is implicit; C mutexes must be explicit
   - **Solution**: Document thread-safety requirements; use mutexes consistently

8. **Error handling**
   - **Issue**: Java exceptions propagate automatically; C error codes must be checked
   - **Solution**: Check every function return value; use goto for cleanup

9. **Missing initialization**
   - **Issue**: Java initializes fields to default values; C leaves memory uninitialized
   - **Solution**: Always initialize variables: `int x = 0;` or use `calloc` for zero-init

10. **Type safety**
    - **Issue**: Java has strong typing; C allows dangerous casts with `void*`
    - **Solution**: Minimize `void*` usage; use typed pointers; document ownership

---

## Tooling

| Tool | Purpose | Notes |
|------|---------|-------|
| GCC / Clang | C compiler | Use `-Wall -Wextra -Werror` for warnings |
| Valgrind | Memory leak detection | Detects leaks, use-after-free, uninitialized memory |
| AddressSanitizer | Memory error detection | Built into GCC/Clang with `-fsanitize=address` |
| gdb | Debugger | Debug segfaults and logic errors |
| uthash | Hash table library | Header-only hash table for C |
| cJSON | JSON parsing | Parse/generate JSON in C |
| Unity / CMocka | Unit testing | Testing frameworks for C |
| pthread | POSIX threads | Standard threading library |
| Make / CMake | Build system | Compile multi-file C projects |

---

## Examples

### Example 1: Simple - Data Class with Methods

**Before (Java):**
```java
public class Point {
    private int x;
    private int y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int getX() { return x; }
    public int getY() { return y; }

    public double distance(Point other) {
        int dx = this.x - other.x;
        int dy = this.y - other.y;
        return Math.sqrt(dx * dx + dy * dy);
    }
}
```

**After (C):**
```c
// point.h
#ifndef POINT_H
#define POINT_H

typedef struct {
    int x;
    int y;
} Point;

Point point_create(int x, int y);
int point_get_x(const Point *p);
int point_get_y(const Point *p);
double point_distance(const Point *p1, const Point *p2);

#endif

// point.c
#include "point.h"
#include <math.h>

Point point_create(int x, int y) {
    Point p = {x, y};
    return p;
}

int point_get_x(const Point *p) {
    return p->x;
}

int point_get_y(const Point *p) {
    return p->y;
}

double point_distance(const Point *p1, const Point *p2) {
    int dx = p1->x - p2->x;
    int dy = p1->y - p2->y;
    return sqrt(dx * dx + dy * dy);
}

// Usage
Point p1 = point_create(0, 0);
Point p2 = point_create(3, 4);
double dist = point_distance(&p1, &p2);  // 5.0
```

### Example 2: Medium - Error Handling with Resources

**Before (Java):**
```java
public String readFirstLine(String path) throws IOException {
    try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
        String line = reader.readLine();
        if (line == null) {
            throw new IOException("File is empty");
        }
        return line;
    }
}
```

**After (C):**
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#define SUCCESS 0
#define ERR_FILE_OPEN -1
#define ERR_FILE_EMPTY -2
#define ERR_OUT_OF_MEMORY -3

int read_first_line(const char *path, char **out_line) {
    if (path == NULL || out_line == NULL) {
        return ERR_FILE_OPEN;
    }

    FILE *file = fopen(path, "r");
    if (file == NULL) {
        return ERR_FILE_OPEN;
    }

    char buffer[256];
    if (fgets(buffer, sizeof(buffer), file) == NULL) {
        fclose(file);
        return ERR_FILE_EMPTY;
    }

    // Remove trailing newline
    size_t len = strlen(buffer);
    if (len > 0 && buffer[len - 1] == '\n') {
        buffer[len - 1] = '\0';
    }

    *out_line = strdup(buffer);
    if (*out_line == NULL) {
        fclose(file);
        return ERR_OUT_OF_MEMORY;
    }

    fclose(file);
    return SUCCESS;
}

// Usage
char *line = NULL;
int result = read_first_line("data.txt", &line);
if (result == SUCCESS) {
    printf("First line: %s\n", line);
    free(line);
} else {
    fprintf(stderr, "Error reading file: %d\n", result);
}
```

### Example 3: Complex - Thread-Safe Counter with Interface

**Before (Java):**
```java
interface Counter {
    void increment();
    int get();
}

class AtomicCounter implements Counter {
    private final AtomicInteger count = new AtomicInteger(0);

    @Override
    public void increment() {
        count.incrementAndGet();
    }

    @Override
    public int get() {
        return count.get();
    }
}

class SynchronizedCounter implements Counter {
    private int count = 0;

    @Override
    public synchronized void increment() {
        count++;
    }

    @Override
    public synchronized int get() {
        return count;
    }
}
```

**After (C):**
```c
// counter.h
#ifndef COUNTER_H
#define COUNTER_H

#include <pthread.h>
#include <stdatomic.h>

typedef struct Counter Counter;

typedef struct {
    void (*increment)(Counter *self);
    int (*get)(Counter *self);
    void (*destroy)(Counter *self);
} CounterVTable;

struct Counter {
    const CounterVTable *vtable;
    void *impl;
};

// Atomic counter
Counter* atomic_counter_create(void);

// Synchronized counter
Counter* synchronized_counter_create(void);

#endif

// counter.c
#include "counter.h"
#include <stdlib.h>

// Atomic implementation
typedef struct {
    atomic_int count;
} AtomicCounterImpl;

static void atomic_counter_increment(Counter *self) {
    AtomicCounterImpl *impl = (AtomicCounterImpl *)self->impl;
    atomic_fetch_add(&impl->count, 1);
}

static int atomic_counter_get(Counter *self) {
    AtomicCounterImpl *impl = (AtomicCounterImpl *)self->impl;
    return atomic_load(&impl->count);
}

static void atomic_counter_destroy_impl(Counter *self) {
    free(self->impl);
    free(self);
}

static const CounterVTable atomic_vtable = {
    .increment = atomic_counter_increment,
    .get = atomic_counter_get,
    .destroy = atomic_counter_destroy_impl,
};

Counter* atomic_counter_create(void) {
    AtomicCounterImpl *impl = malloc(sizeof(AtomicCounterImpl));
    if (impl == NULL) return NULL;

    atomic_init(&impl->count, 0);

    Counter *counter = malloc(sizeof(Counter));
    if (counter == NULL) {
        free(impl);
        return NULL;
    }

    counter->vtable = &atomic_vtable;
    counter->impl = impl;
    return counter;
}

// Synchronized implementation
typedef struct {
    int count;
    pthread_mutex_t mutex;
} SyncCounterImpl;

static void sync_counter_increment(Counter *self) {
    SyncCounterImpl *impl = (SyncCounterImpl *)self->impl;
    pthread_mutex_lock(&impl->mutex);
    impl->count++;
    pthread_mutex_unlock(&impl->mutex);
}

static int sync_counter_get(Counter *self) {
    SyncCounterImpl *impl = (SyncCounterImpl *)self->impl;
    pthread_mutex_lock(&impl->mutex);
    int value = impl->count;
    pthread_mutex_unlock(&impl->mutex);
    return value;
}

static void sync_counter_destroy_impl(Counter *self) {
    SyncCounterImpl *impl = (SyncCounterImpl *)self->impl;
    pthread_mutex_destroy(&impl->mutex);
    free(impl);
    free(self);
}

static const CounterVTable sync_vtable = {
    .increment = sync_counter_increment,
    .get = sync_counter_get,
    .destroy = sync_counter_destroy_impl,
};

Counter* synchronized_counter_create(void) {
    SyncCounterImpl *impl = malloc(sizeof(SyncCounterImpl));
    if (impl == NULL) return NULL;

    impl->count = 0;
    pthread_mutex_init(&impl->mutex, NULL);

    Counter *counter = malloc(sizeof(Counter));
    if (counter == NULL) {
        pthread_mutex_destroy(&impl->mutex);
        free(impl);
        return NULL;
    }

    counter->vtable = &sync_vtable;
    counter->impl = impl;
    return counter;
}

// Usage
Counter *counter = atomic_counter_create();
counter->vtable->increment(counter);
int count = counter->vtable->get(counter);
counter->vtable->destroy(counter);
```

---

## See Also

For more examples and patterns, see:
- `meta-convert-dev` - Foundational patterns with cross-language examples
- `convert-python-c` - Similar high-level to low-level conversion
- `lang-java-dev` - Java development patterns
- `lang-c-dev` - C development patterns

Cross-cutting pattern skills (for areas not fully covered by lang-*-dev):
- `patterns-concurrency-dev` - Threads, mutexes, atomics across languages
- `patterns-serialization-dev` - JSON, binary formats across languages
- `patterns-memory-eng` - Manual memory management patterns
