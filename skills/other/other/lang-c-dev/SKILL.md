---
name: lang-c-dev
description: Foundational C programming patterns covering type system, memory management, pointers, arrays, preprocessor, compilation, concurrency (pthreads, mutexes, atomics), serialization (binary, JSON, struct packing), and testing (Unity, CMocka, Check). Complete 8/8 pillar coverage. Use when writing C code, understanding manual memory management, working with system-level programming, or needing guidance on which specialized C skill to use. This is the entry point for C development.
---

# C Fundamentals

Foundational C programming patterns and core language features. This skill serves as both a reference for common patterns and an index to specialized C skills.

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        C Skill Hierarchy                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                     ┌──────────────────┐                        │
│                     │   lang-c-dev     │ ◄── You are here       │
│                     │  (foundation)    │                        │
│                     └────────┬─────────┘                        │
│                              │                                  │
│     ┌────────────┬───────────┼───────────┬────────────┐        │
│     │            │           │           │            │        │
│     ▼            ▼           ▼           ▼            ▼        │
│ ┌────────┐ ┌──────────┐ ┌────────┐ ┌─────────┐ ┌──────────┐   │
│ │ memory │ │  posix   │ │library │ │ systems │ │ embedded │   │
│ │  -eng  │ │   -dev   │ │  -dev  │ │  -eng   │ │   -dev   │   │
│ └────────┘ └──────────┘ └────────┘ └─────────┘ └──────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**This skill covers:**
- Type system (primitives, structs, unions, enums)
- Pointers and memory management (malloc, free, addresses)
- Arrays and strings (null-terminated, manipulation)
- Preprocessor directives (#define, #include, macros)
- Header files and compilation process
- Concurrency (pthreads, mutexes, condition variables, atomics)
- Serialization (binary, JSON with cJSON, struct packing)
- Testing (Unity, CMocka, Check frameworks)
- Common idioms and safety patterns

**This skill does NOT cover (see specialized skills):**
- Advanced memory engineering → `lang-c-memory-eng`
- POSIX APIs and system calls → `lang-c-posix-dev`
- Library/package creation → `lang-c-library-dev`
- Systems programming patterns → `lang-c-systems-eng`
- Embedded programming → `lang-c-embedded-dev`

---

## Quick Reference

| Task | Pattern |
|------|---------|
| Declare variable | `type name = value;` |
| Declare pointer | `type *ptr;` |
| Allocate memory | `ptr = malloc(size * sizeof(type));` |
| Free memory | `free(ptr);` |
| Define macro | `#define NAME value` |
| Include header | `#include <stdio.h>` or `#include "header.h"` |
| Declare function | `return_type name(params);` |
| Define struct | `struct Name { type field; };` |
| Access member | `struct.field` or `ptr->field` |

---

## Skill Routing

Use this table to find the right specialized skill:

| When you need to... | Use this skill |
|---------------------|----------------|
| Understand memory safety, buffer overflows | `lang-c-memory-eng` |
| Work with POSIX APIs, file I/O, processes | `lang-c-posix-dev` |
| Create static/dynamic libraries | `lang-c-library-dev` |
| System-level programming, signals, IPC | `lang-c-systems-eng` |
| Embedded systems, bare-metal programming | `lang-c-embedded-dev` |

---

## Type System

### Primitive Types

```c
// Integer types
char c = 'A';              // 1 byte, -128 to 127
unsigned char uc = 255;    // 1 byte, 0 to 255
short s = -1000;           // 2 bytes (typically)
unsigned short us = 60000; // 2 bytes
int i = -100000;           // 4 bytes (typically)
unsigned int ui = 100000;  // 4 bytes
long l = -1000000L;        // 4 or 8 bytes
unsigned long ul = 1000000UL;
long long ll = -9223372036854775807LL;  // 8 bytes

// Floating-point types
float f = 3.14f;           // 4 bytes, ~7 decimal digits
double d = 3.141592653589793;  // 8 bytes, ~15 decimal digits
long double ld = 3.14159265358979323846L;  // 10-16 bytes

// Boolean (C99+)
#include <stdbool.h>
bool flag = true;          // Requires stdbool.h

// Size-specific types (C99+, stdint.h)
#include <stdint.h>
int8_t i8 = -128;          // Exactly 8 bits
uint8_t u8 = 255;          // Exactly 8 bits
int16_t i16 = -32768;      // Exactly 16 bits
uint16_t u16 = 65535;      // Exactly 16 bits
int32_t i32 = -2147483648; // Exactly 32 bits
uint32_t u32 = 4294967295U; // Exactly 32 bits
int64_t i64 = -9223372036854775807LL;  // Exactly 64 bits
uint64_t u64 = 18446744073709551615ULL; // Exactly 64 bits

// Pointer-sized integers
intptr_t iptr;             // Pointer-sized signed
uintptr_t uptr;            // Pointer-sized unsigned
size_t sz;                 // For sizes, unsigned
```

### Type Qualifiers

```c
// const: Value cannot be modified
const int max = 100;
const char *str = "Hello";  // Pointer to const char
char *const ptr = buf;      // Const pointer to char
const char *const cptr = "Fixed";  // Both const

// volatile: Value may change unexpectedly (hardware registers, signal handlers)
volatile int hardware_register;
volatile sig_atomic_t signal_flag;

// restrict (C99+): Pointer is only way to access object (optimization hint)
void copy(char *restrict dest, const char *restrict src, size_t n);
```

### Structs

```c
// Basic struct definition
struct Point {
    int x;
    int y;
};

// Creating instances
struct Point p1 = {10, 20};           // Designated order
struct Point p2 = {.y = 30, .x = 15}; // Designated initializers (C99+)

// Accessing members
p1.x = 5;
p1.y = 10;

// Typedef for convenience
typedef struct Point Point;
// Or combined:
typedef struct {
    int x;
    int y;
} Point;

// Now can use: Point p;
Point p3 = {1, 2};

// Nested structs
typedef struct {
    Point top_left;
    Point bottom_right;
} Rectangle;

// Struct with flexible array member (C99+)
typedef struct {
    size_t len;
    char data[];  // Must be last member
} String;

// Allocate with variable size
String *str = malloc(sizeof(String) + 100);
str->len = 100;
```

### Unions

```c
// Union: Members share same memory
union Data {
    int i;
    float f;
    char str[20];
};

// All members occupy same space; only one valid at a time
union Data d;
d.i = 10;        // Store integer
printf("%d\n", d.i);
d.f = 220.5f;    // Now integer is invalid
printf("%f\n", d.f);

// Common use: Tagged unions for type-safe variants
typedef enum { TYPE_INT, TYPE_FLOAT, TYPE_STRING } DataType;

typedef struct {
    DataType type;
    union {
        int i;
        float f;
        char *str;
    } value;
} Variant;

// Safe access
void print_variant(Variant *v) {
    switch (v->type) {
        case TYPE_INT:
            printf("%d\n", v->value.i);
            break;
        case TYPE_FLOAT:
            printf("%f\n", v->value.f);
            break;
        case TYPE_STRING:
            printf("%s\n", v->value.str);
            break;
    }
}
```

### Enums

```c
// Basic enum
enum Color {
    RED,     // 0
    GREEN,   // 1
    BLUE     // 2
};

// With explicit values
enum Status {
    OK = 0,
    ERROR = -1,
    PENDING = 1
};

// Typedef for convenience
typedef enum {
    MODE_READ = 0x01,
    MODE_WRITE = 0x02,
    MODE_EXECUTE = 0x04
} FileMode;

// Using enums
FileMode mode = MODE_READ | MODE_WRITE;  // Bitwise OR

// Enum as bit flags
if (mode & MODE_WRITE) {
    // Has write permission
}
```

---

## Pointers and Memory Management

### Pointer Basics

```c
int x = 10;
int *ptr = &x;   // ptr stores address of x

printf("%d\n", x);      // Value: 10
printf("%p\n", &x);     // Address of x
printf("%p\n", ptr);    // Address stored in ptr (same as &x)
printf("%d\n", *ptr);   // Dereference: value at address (10)

*ptr = 20;      // Modify x through pointer
printf("%d\n", x);  // x is now 20

// Pointer arithmetic
int arr[5] = {1, 2, 3, 4, 5};
int *p = arr;        // Points to first element
printf("%d\n", *p);      // 1
printf("%d\n", *(p+1));  // 2
printf("%d\n", *(p+2));  // 3

// NULL pointer
int *null_ptr = NULL;  // Points to nothing
if (null_ptr == NULL) {
    // Safe: check before dereferencing
}
```

### Dynamic Memory Allocation

```c
#include <stdlib.h>

// malloc: Allocate uninitialized memory
int *numbers = malloc(10 * sizeof(int));
if (numbers == NULL) {
    // Allocation failed
    perror("malloc");
    return -1;
}

// Use the memory
for (int i = 0; i < 10; i++) {
    numbers[i] = i * 2;
}

// Free when done
free(numbers);
numbers = NULL;  // Good practice: prevent use-after-free

// calloc: Allocate zero-initialized memory
int *zeros = calloc(10, sizeof(int));  // All elements = 0
free(zeros);

// realloc: Resize allocation
int *resized = realloc(numbers, 20 * sizeof(int));
if (resized == NULL) {
    // Realloc failed, original pointer still valid
    free(numbers);
    return -1;
}
numbers = resized;
free(numbers);

// Allocating structures
typedef struct {
    char name[50];
    int age;
} Person;

Person *person = malloc(sizeof(Person));
if (person == NULL) {
    return -1;
}
strcpy(person->name, "Alice");
person->age = 30;
free(person);
```

### Pointer Patterns

```c
// Double pointer (pointer to pointer)
void allocate_string(char **str) {
    *str = malloc(100);
}

char *buffer = NULL;
allocate_string(&buffer);
strcpy(buffer, "Hello");
free(buffer);

// Function pointers
int add(int a, int b) { return a + b; }
int subtract(int a, int b) { return a - b; }

int (*operation)(int, int);  // Declare function pointer
operation = add;
printf("%d\n", operation(5, 3));  // 8
operation = subtract;
printf("%d\n", operation(5, 3));  // 2

// Array of function pointers
typedef int (*BinaryOp)(int, int);
BinaryOp ops[] = {add, subtract};
printf("%d\n", ops[0](10, 5));  // 15
printf("%d\n", ops[1](10, 5));  // 5

// Const correctness
void read_data(const int *data, size_t n) {
    // data[0] = 10;  // Error: cannot modify
    printf("%d\n", data[0]);  // OK: can read
}

void write_data(int *data, size_t n) {
    data[0] = 10;  // OK: can modify
}
```

---

## Arrays and Strings

### Arrays

```c
// Fixed-size arrays
int numbers[5] = {1, 2, 3, 4, 5};
char chars[10] = {'a', 'b', 'c'};  // Rest initialized to 0

// Array size
size_t length = sizeof(numbers) / sizeof(numbers[0]);  // 5

// Multi-dimensional arrays
int matrix[3][4] = {
    {1, 2, 3, 4},
    {5, 6, 7, 8},
    {9, 10, 11, 12}
};

printf("%d\n", matrix[1][2]);  // 7

// Passing arrays to functions (decay to pointers)
void process(int arr[], size_t n) {
    // arr is actually int*
    for (size_t i = 0; i < n; i++) {
        arr[i] *= 2;
    }
}

int data[5] = {1, 2, 3, 4, 5};
process(data, 5);

// Dynamic arrays
size_t capacity = 10;
int *dynamic = malloc(capacity * sizeof(int));
// ... use dynamic array ...
free(dynamic);
```

### Strings (Null-Terminated Char Arrays)

```c
#include <string.h>

// String literals (stored in read-only memory)
const char *str1 = "Hello, World!";  // Pointer to literal

// Mutable string (array)
char str2[] = "Hello";  // {'H','e','l','l','o','\0'}
str2[0] = 'h';  // OK: modifiable

// String length
size_t len = strlen(str1);  // 13 (doesn't count '\0')

// String copy
char dest[50];
strcpy(dest, "Hello");       // Unsafe: no bounds check
strncpy(dest, "Hello", 49);  // Safer: limit length
dest[49] = '\0';             // Ensure null termination

// String concatenation
strcat(dest, " World");      // Unsafe
strncat(dest, " World", 49 - strlen(dest));  // Safer

// String comparison
if (strcmp(str1, str2) == 0) {
    // Strings equal
}
if (strncmp(str1, str2, 5) == 0) {
    // First 5 chars equal
}

// String search
char *pos = strchr(str1, 'W');   // Find first 'W'
if (pos != NULL) {
    printf("Found at index: %ld\n", pos - str1);
}

char *sub = strstr(str1, "World");  // Find substring
if (sub != NULL) {
    printf("Substring found\n");
}

// Safe string handling (C11+)
#ifdef __STDC_LIB_EXT1__
strcpy_s(dest, sizeof(dest), "Safe");
strcat_s(dest, sizeof(dest), " Copy");
#endif

// Manual string building
char buffer[100];
snprintf(buffer, sizeof(buffer), "Name: %s, Age: %d", "Alice", 30);
```

### String Manipulation Patterns

```c
// Tokenizing strings
char input[] = "apple,banana,cherry";
char *token = strtok(input, ",");
while (token != NULL) {
    printf("%s\n", token);
    token = strtok(NULL, ",");
}

// Converting strings to numbers
const char *num_str = "12345";
int num = atoi(num_str);           // ASCII to integer
long lnum = atol(num_str);         // ASCII to long
double dnum = atof("3.14159");     // ASCII to float

// Better conversion with error checking (C99+)
char *endptr;
long val = strtol(num_str, &endptr, 10);  // Base 10
if (endptr == num_str) {
    printf("No conversion performed\n");
} else if (*endptr != '\0') {
    printf("Partial conversion: stopped at '%s'\n", endptr);
}

// Formatting strings
char output[100];
int written = snprintf(output, sizeof(output),
                       "x=%d, y=%f, s=%s", 10, 3.14, "test");
if (written >= sizeof(output)) {
    printf("Output truncated\n");
}
```

---

## Preprocessor

### Include Directives

```c
// System headers (search system paths)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// User headers (search current directory first)
#include "myheader.h"
#include "utils/helper.h"
```

### Macros

```c
// Object-like macros
#define PI 3.14159
#define MAX_SIZE 1024
#define VERSION "1.0.0"

// Function-like macros
#define SQUARE(x) ((x) * (x))  // Parentheses important!
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define MIN(a, b) ((a) < (b) ? (a) : (b))

// Multi-line macros
#define SWAP(a, b, type) do { \
    type temp = (a); \
    (a) = (b); \
    (b) = temp; \
} while(0)

// Usage
int x = 5, y = 10;
SWAP(x, y, int);

// Stringification
#define STRINGIFY(x) #x
printf("%s\n", STRINGIFY(Hello));  // Prints: Hello

// Token pasting
#define CONCAT(a, b) a##b
int CONCAT(var, 123) = 42;  // Creates: int var123 = 42;

// Variadic macros (C99+)
#define LOG(fmt, ...) printf("[LOG] " fmt "\n", ##__VA_ARGS__)
LOG("Starting process");
LOG("Value: %d", 42);

// Common utility macros
#define ARRAY_SIZE(arr) (sizeof(arr) / sizeof((arr)[0]))
#define UNUSED(x) (void)(x)
#define likely(x)   __builtin_expect(!!(x), 1)   // GCC optimization hint
#define unlikely(x) __builtin_expect(!!(x), 0)
```

### Conditional Compilation

```c
// Platform-specific code
#ifdef _WIN32
    #include <windows.h>
    #define PATH_SEP '\\'
#elif defined(__linux__)
    #include <unistd.h>
    #define PATH_SEP '/'
#elif defined(__APPLE__)
    #include <TargetConditionals.h>
    #define PATH_SEP '/'
#else
    #error "Unsupported platform"
#endif

// Feature detection
#ifdef __STDC_VERSION__
    #if __STDC_VERSION__ >= 201112L
        // C11 or later
        #define HAS_C11 1
    #endif
#endif

// Debug builds
#ifdef NDEBUG
    #define debug_print(fmt, ...) ((void)0)
#else
    #define debug_print(fmt, ...) \
        fprintf(stderr, "[DEBUG] %s:%d: " fmt "\n", \
                __FILE__, __LINE__, ##__VA_ARGS__)
#endif

// Include guards (prevent multiple inclusion)
#ifndef MYHEADER_H
#define MYHEADER_H

// Header contents here

#endif  // MYHEADER_H

// Or use #pragma once (non-standard but widely supported)
#pragma once
```

### Predefined Macros

```c
printf("File: %s\n", __FILE__);      // Current file name
printf("Line: %d\n", __LINE__);      // Current line number
printf("Date: %s\n", __DATE__);      // Compilation date
printf("Time: %s\n", __TIME__);      // Compilation time
printf("Function: %s\n", __func__);  // Current function (C99+)

// Standard macros
#if defined(__STDC__)
    printf("Standard C\n");
#endif

#ifdef __STDC_VERSION__
    printf("C version: %ld\n", __STDC_VERSION__);
    // 199901L for C99
    // 201112L for C11
    // 201710L for C17/C18
#endif
```

---

## Header Files and Compilation

### Header File Structure

```c
// point.h
#ifndef POINT_H
#define POINT_H

// Type definitions
typedef struct {
    double x;
    double y;
} Point;

// Function declarations (prototypes)
Point point_create(double x, double y);
double point_distance(const Point *p1, const Point *p2);
void point_print(const Point *p);

// Inline functions (C99+)
static inline Point point_add(Point p1, Point p2) {
    return (Point){p1.x + p2.x, p1.y + p2.y};
}

#endif  // POINT_H
```

### Implementation File

```c
// point.c
#include "point.h"
#include <stdio.h>
#include <math.h>

Point point_create(double x, double y) {
    Point p = {x, y};
    return p;
}

double point_distance(const Point *p1, const Point *p2) {
    double dx = p2->x - p1->x;
    double dy = p2->y - p1->y;
    return sqrt(dx*dx + dy*dy);
}

void point_print(const Point *p) {
    printf("Point(%.2f, %.2f)\n", p->x, p->y);
}
```

### Compilation Process

```bash
# 1. Preprocessing: Expand macros, include headers
gcc -E main.c -o main.i

# 2. Compilation: Generate assembly
gcc -S main.c -o main.s

# 3. Assembly: Generate object code
gcc -c main.c -o main.o

# 4. Linking: Combine object files and libraries
gcc main.o point.o -o program -lm

# All in one step
gcc -Wall -Wextra -std=c11 -o program main.c point.c -lm

# Common flags
# -Wall -Wextra       Enable most warnings
# -Werror             Treat warnings as errors
# -std=c11            Use C11 standard
# -O2                 Optimization level 2
# -g                  Include debug symbols
# -D DEFINE_NAME=val  Define preprocessor macro
# -I /path/to/include Add include directory
# -L /path/to/libs    Add library directory
# -l library          Link with library
```

### Static vs Dynamic Linking

```bash
# Static library (.a)
# Create object files
gcc -c module1.c module2.c

# Create static library
ar rcs libmylib.a module1.o module2.o

# Link with static library
gcc main.c -L. -lmylib -o program

# Dynamic library (.so on Linux, .dylib on macOS, .dll on Windows)
# Create position-independent code
gcc -c -fPIC module1.c module2.c

# Create shared library
gcc -shared -o libmylib.so module1.o module2.o

# Link with dynamic library
gcc main.c -L. -lmylib -o program

# Run with dynamic library (if not in standard path)
LD_LIBRARY_PATH=. ./program
```

---

## Common Idioms and Patterns

### Error Handling

```c
// Return codes
#define SUCCESS 0
#define ERROR_NULL_POINTER -1
#define ERROR_OUT_OF_MEMORY -2
#define ERROR_INVALID_INPUT -3

int process_data(const char *input, char **output) {
    if (input == NULL || output == NULL) {
        return ERROR_NULL_POINTER;
    }

    *output = malloc(100);
    if (*output == NULL) {
        return ERROR_OUT_OF_MEMORY;
    }

    // Process data...

    return SUCCESS;
}

// Usage with goto for cleanup
int function(void) {
    char *buffer = NULL;
    FILE *file = NULL;
    int result = SUCCESS;

    buffer = malloc(1024);
    if (buffer == NULL) {
        result = ERROR_OUT_OF_MEMORY;
        goto cleanup;
    }

    file = fopen("data.txt", "r");
    if (file == NULL) {
        result = -1;
        goto cleanup;
    }

    // Process file...

cleanup:
    free(buffer);
    if (file != NULL) {
        fclose(file);
    }
    return result;
}
```

### Opaque Pointers (Information Hiding)

```c
// header.h
typedef struct Widget Widget;  // Forward declaration

Widget* widget_create(void);
void widget_destroy(Widget *w);
void widget_set_value(Widget *w, int value);
int widget_get_value(const Widget *w);

// implementation.c
struct Widget {  // Full definition hidden
    int value;
    char name[50];
    // Internal implementation details
};

Widget* widget_create(void) {
    Widget *w = malloc(sizeof(Widget));
    if (w != NULL) {
        w->value = 0;
        strcpy(w->name, "default");
    }
    return w;
}

void widget_destroy(Widget *w) {
    free(w);
}
```

### RAII-like Pattern with Cleanup Attribute (GCC/Clang)

```c
// GCC/Clang cleanup attribute
#define AUTO_FREE __attribute__((cleanup(cleanup_free)))

static inline void cleanup_free(void *p) {
    free(*(void**)p);
}

void example(void) {
    AUTO_FREE char *buffer = malloc(100);
    if (buffer == NULL) {
        return;  // No memory leak
    }

    // Use buffer...

    // Automatically freed when out of scope
}
```

### Generic Programming with Macros

```c
// Type-generic min/max (C11+)
#define min(a, b) _Generic((a), \
    int: min_int, \
    double: min_double, \
    default: min_int \
)(a, b)

static inline int min_int(int a, int b) {
    return a < b ? a : b;
}

static inline double min_double(double a, double b) {
    return a < b ? a : b;
}

// Simpler macro approach (works with any type)
#define MIN(a, b) ({ \
    __typeof__(a) _a = (a); \
    __typeof__(b) _b = (b); \
    _a < _b ? _a : _b; \
})
```

### Container_of Pattern (Linux Kernel Style)

```c
#define container_of(ptr, type, member) \
    ((type *)((char *)(ptr) - offsetof(type, member)))

typedef struct {
    int id;
    char name[50];
} Data;

typedef struct Node {
    struct Node *next;
    Data data;
} Node;

// Get Node from Data pointer
Data *data_ptr = &node->data;
Node *node_ptr = container_of(data_ptr, Node, data);
```

---

## Safety Patterns

### Buffer Overflow Prevention

```c
// BAD: Unsafe
char buffer[10];
strcpy(buffer, user_input);  // Buffer overflow if input > 9 chars

// GOOD: Safe with bounds checking
char buffer[10];
strncpy(buffer, user_input, sizeof(buffer) - 1);
buffer[sizeof(buffer) - 1] = '\0';  // Ensure null termination

// BETTER: Use safer functions (C11)
#ifdef __STDC_LIB_EXT1__
strcpy_s(buffer, sizeof(buffer), user_input);
#endif

// BEST: Dynamic allocation based on input size
size_t len = strlen(user_input) + 1;
char *buffer = malloc(len);
if (buffer != NULL) {
    strcpy(buffer, user_input);
    // ...
    free(buffer);
}
```

### NULL Pointer Checks

```c
// Always check after allocation
int *data = malloc(n * sizeof(int));
if (data == NULL) {
    fprintf(stderr, "Allocation failed\n");
    return -1;
}

// Check function parameters
void process(const int *data, size_t n) {
    if (data == NULL) {
        return;  // Or handle error
    }
    // Safe to use data
}

// Check before dereferencing
if (ptr != NULL && ptr->field > 0) {
    // Safe access
}
```

### Integer Overflow Prevention

```c
#include <stdint.h>
#include <limits.h>

// Check before multiplication
size_t safe_multiply(size_t a, size_t b) {
    if (a > 0 && b > SIZE_MAX / a) {
        return 0;  // Overflow would occur
    }
    return a * b;
}

// Check before addition
int safe_add(int a, int b) {
    if (a > 0 && b > INT_MAX - a) {
        return INT_MAX;  // Saturate
    }
    if (a < 0 && b < INT_MIN - a) {
        return INT_MIN;  // Saturate
    }
    return a + b;
}

// Use wider types for intermediate calculations
uint32_t a = 1000000;
uint32_t b = 1000000;
uint64_t result = (uint64_t)a * (uint64_t)b;
```

### Memory Leak Prevention

```c
// Pattern: Always pair malloc with free
void example(void) {
    char *buffer = malloc(100);
    if (buffer == NULL) {
        return;
    }

    // Use buffer...

    free(buffer);
}

// Pattern: Set pointer to NULL after free
free(ptr);
ptr = NULL;

// Pattern: Use goto for cleanup in complex functions
int complex_function(void) {
    void *res1 = NULL, *res2 = NULL, *res3 = NULL;
    int status = -1;

    res1 = malloc(100);
    if (res1 == NULL) goto cleanup;

    res2 = malloc(200);
    if (res2 == NULL) goto cleanup;

    res3 = malloc(300);
    if (res3 == NULL) goto cleanup;

    // Do work...
    status = 0;

cleanup:
    free(res3);
    free(res2);
    free(res1);
    return status;
}
```

---

## Troubleshooting

### Segmentation Fault

**Causes:**
- Dereferencing NULL pointer
- Dereferencing uninitialized pointer
- Writing beyond array bounds
- Use-after-free

**Debugging:**
```bash
# Compile with debug symbols
gcc -g program.c -o program

# Run with debugger
gdb ./program
(gdb) run
# When crash occurs:
(gdb) backtrace
(gdb) print variable_name

# Use valgrind for memory errors
valgrind --leak-check=full ./program
```

### Memory Leaks

```c
// LEAK: malloc without free
void leak_example(void) {
    char *buffer = malloc(100);
    // ... use buffer ...
    // Missing: free(buffer);
}

// LEAK: Losing pointer to allocated memory
void lose_pointer(void) {
    char *buffer = malloc(100);
    buffer = malloc(200);  // Lost first allocation!
    free(buffer);  // Only frees second allocation
}

// FIX: Track all allocations
void correct_version(void) {
    char *buffer = malloc(100);
    // ... use buffer ...
    free(buffer);
}
```

### Undefined Behavior

```c
// Uninitialized variable
int x;
printf("%d\n", x);  // UB: undefined value

// Fix: Initialize
int x = 0;

// Modifying string literal
char *str = "Hello";
str[0] = 'h';  // UB: segfault on many systems

// Fix: Use array
char str[] = "Hello";
str[0] = 'h';  // OK

// Signed integer overflow
int x = INT_MAX;
x++;  // UB

// Fix: Check before operation or use unsigned
if (x < INT_MAX) {
    x++;
}
```

### Compiler Warnings

```c
// Enable all warnings
gcc -Wall -Wextra -Wpedantic program.c

// Common warnings:
// - Unused variable: Remove or cast to void
// - Implicit declaration: Include proper header
// - Format string mismatch: Match printf format with type
// - Comparison between signed/unsigned: Cast appropriately
// - Missing return: Add return statement

// Example fixes:
void example(void) {
    int unused = 5;
    (void)unused;  // Suppress warning

    // Correct format specifiers
    size_t sz = 100;
    printf("%zu\n", sz);  // Use %zu for size_t

    int64_t big = 1000000LL;
    printf("%" PRId64 "\n", big);  // Use PRId64 from inttypes.h
}
```

---

## Concurrency

C has no built-in concurrency primitives in the standard. Most concurrent programming uses POSIX threads (pthreads) or platform-specific APIs.

### POSIX Threads (pthreads)

```c
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

// Thread function
void *thread_function(void *arg) {
    int *value = (int *)arg;
    printf("Thread received: %d\n", *value);

    // Return value
    int *result = malloc(sizeof(int));
    *result = *value * 2;
    return result;
}

int main(void) {
    pthread_t thread;
    int input = 42;

    // Create thread
    if (pthread_create(&thread, NULL, thread_function, &input) != 0) {
        perror("pthread_create");
        return 1;
    }

    // Wait for thread to finish
    void *result;
    if (pthread_join(thread, &result) != 0) {
        perror("pthread_join");
        return 1;
    }

    printf("Result: %d\n", *(int *)result);
    free(result);

    return 0;
}
```

### Mutexes (Mutual Exclusion)

```c
#include <pthread.h>

// Shared data protected by mutex
typedef struct {
    int counter;
    pthread_mutex_t mutex;
} SafeCounter;

void counter_init(SafeCounter *c) {
    c->counter = 0;
    pthread_mutex_init(&c->mutex, NULL);
}

void counter_increment(SafeCounter *c) {
    pthread_mutex_lock(&c->mutex);
    c->counter++;
    pthread_mutex_unlock(&c->mutex);
}

int counter_get(SafeCounter *c) {
    pthread_mutex_lock(&c->mutex);
    int value = c->counter;
    pthread_mutex_unlock(&c->mutex);
    return value;
}

void counter_destroy(SafeCounter *c) {
    pthread_mutex_destroy(&c->mutex);
}

// Usage
void *increment_thread(void *arg) {
    SafeCounter *counter = (SafeCounter *)arg;
    for (int i = 0; i < 1000; i++) {
        counter_increment(counter);
    }
    return NULL;
}
```

### Condition Variables

```c
#include <pthread.h>

typedef struct {
    int ready;
    pthread_mutex_t mutex;
    pthread_cond_t cond;
} Signal;

void signal_init(Signal *s) {
    s->ready = 0;
    pthread_mutex_init(&s->mutex, NULL);
    pthread_cond_init(&s->cond, NULL);
}

// Producer: signal when ready
void signal_notify(Signal *s) {
    pthread_mutex_lock(&s->mutex);
    s->ready = 1;
    pthread_cond_signal(&s->cond);  // Wake one waiter
    pthread_mutex_unlock(&s->mutex);
}

// Consumer: wait for signal
void signal_wait(Signal *s) {
    pthread_mutex_lock(&s->mutex);
    while (!s->ready) {
        pthread_cond_wait(&s->cond, &s->mutex);
    }
    pthread_mutex_unlock(&s->mutex);
}

void signal_destroy(Signal *s) {
    pthread_mutex_destroy(&s->mutex);
    pthread_cond_destroy(&s->cond);
}
```

### Atomic Operations (C11+)

```c
#include <stdatomic.h>
#include <pthread.h>

// Atomic counter (lock-free)
typedef struct {
    atomic_int counter;
} AtomicCounter;

void atomic_counter_init(AtomicCounter *c) {
    atomic_init(&c->counter, 0);
}

void atomic_counter_increment(AtomicCounter *c) {
    atomic_fetch_add(&c->counter, 1);
}

int atomic_counter_get(AtomicCounter *c) {
    return atomic_load(&c->counter);
}

// Compare and swap
_Bool atomic_compare_exchange_example(atomic_int *ptr, int expected, int desired) {
    return atomic_compare_exchange_strong(ptr, &expected, desired);
}

// Memory ordering
void atomic_with_ordering(void) {
    atomic_int x, y;

    // Sequential consistency (default)
    atomic_store(&x, 1);

    // Relaxed ordering (weakest)
    atomic_store_explicit(&y, 2, memory_order_relaxed);

    // Acquire-release ordering
    atomic_store_explicit(&x, 1, memory_order_release);
    atomic_load_explicit(&x, memory_order_acquire);
}
```

### Thread-Local Storage

```c
#include <pthread.h>
#include <stdio.h>

// Thread-local variable (C11+)
_Thread_local int thread_id = 0;

void *thread_func(void *arg) {
    thread_id = *(int *)arg;
    printf("Thread ID: %d\n", thread_id);
    return NULL;
}

// POSIX thread-specific data
pthread_key_t key;

void cleanup(void *data) {
    free(data);
}

void create_thread_data(void) {
    pthread_key_create(&key, cleanup);
}

void set_thread_data(int value) {
    int *data = malloc(sizeof(int));
    *data = value;
    pthread_setspecific(key, data);
}

int get_thread_data(void) {
    int *data = pthread_getspecific(key);
    return data ? *data : -1;
}
```

**See also:** `patterns-concurrency-dev` for cross-language concurrency patterns

---

## Serialization

C has no standard serialization framework. Data is typically serialized manually or using third-party libraries.

### Manual Binary Serialization

```c
#include <stdio.h>
#include <stdint.h>
#include <string.h>

typedef struct {
    uint32_t id;
    char name[50];
    float score;
} Record;

// Serialize to file (binary)
int serialize_record(const Record *record, const char *filename) {
    FILE *file = fopen(filename, "wb");
    if (file == NULL) {
        return -1;
    }

    size_t written = fwrite(record, sizeof(Record), 1, file);
    fclose(file);

    return written == 1 ? 0 : -1;
}

// Deserialize from file (binary)
int deserialize_record(Record *record, const char *filename) {
    FILE *file = fopen(filename, "rb");
    if (file == NULL) {
        return -1;
    }

    size_t read = fread(record, sizeof(Record), 1, file);
    fclose(file);

    return read == 1 ? 0 : -1;
}

// Network-safe serialization (handle endianness)
#include <arpa/inet.h>  // For htonl, ntohl

typedef struct {
    uint32_t id;
    uint32_t value;
} NetworkMessage;

void serialize_network(const NetworkMessage *msg, uint8_t *buffer) {
    uint32_t *ptr = (uint32_t *)buffer;
    ptr[0] = htonl(msg->id);      // Host to network byte order
    ptr[1] = htonl(msg->value);
}

void deserialize_network(NetworkMessage *msg, const uint8_t *buffer) {
    const uint32_t *ptr = (const uint32_t *)buffer;
    msg->id = ntohl(ptr[0]);      // Network to host byte order
    msg->value = ntohl(ptr[1]);
}
```

### JSON Serialization (cJSON Library)

```c
// cJSON: https://github.com/DaveGamble/cJSON
#include <cJSON.h>

typedef struct {
    char name[50];
    int age;
    char email[100];
} User;

// Serialize struct to JSON string
char *user_to_json(const User *user) {
    cJSON *root = cJSON_CreateObject();

    cJSON_AddStringToObject(root, "name", user->name);
    cJSON_AddNumberToObject(root, "age", user->age);
    cJSON_AddStringToObject(root, "email", user->email);

    char *json_str = cJSON_Print(root);  // Caller must free
    cJSON_Delete(root);

    return json_str;
}

// Deserialize JSON string to struct
int user_from_json(User *user, const char *json_str) {
    cJSON *root = cJSON_Parse(json_str);
    if (root == NULL) {
        return -1;
    }

    cJSON *name = cJSON_GetObjectItem(root, "name");
    cJSON *age = cJSON_GetObjectItem(root, "age");
    cJSON *email = cJSON_GetObjectItem(root, "email");

    if (!cJSON_IsString(name) || !cJSON_IsNumber(age) || !cJSON_IsString(email)) {
        cJSON_Delete(root);
        return -1;
    }

    strncpy(user->name, name->valuestring, sizeof(user->name) - 1);
    user->age = age->valueint;
    strncpy(user->email, email->valuestring, sizeof(user->email) - 1);

    cJSON_Delete(root);
    return 0;
}

// Usage
void json_example(void) {
    User user = {"Alice", 30, "alice@example.com"};

    // Serialize
    char *json = user_to_json(&user);
    printf("%s\n", json);

    // Deserialize
    User parsed;
    if (user_from_json(&parsed, json) == 0) {
        printf("Parsed: %s, %d, %s\n", parsed.name, parsed.age, parsed.email);
    }

    free(json);
}
```

### Struct Packing and Alignment

```c
#include <stddef.h>

// Default alignment (padding added)
struct Unpacked {
    char a;      // 1 byte
    // 3 bytes padding
    int b;       // 4 bytes
    char c;      // 1 byte
    // 3 bytes padding
};  // Total: 12 bytes

// Packed struct (no padding)
struct __attribute__((packed)) Packed {
    char a;      // 1 byte
    int b;       // 4 bytes
    char c;      // 1 byte
};  // Total: 6 bytes

// GCC/Clang: #pragma pack
#pragma pack(push, 1)
struct PackedPragma {
    char a;
    int b;
    char c;
};
#pragma pack(pop)

// Check alignment
void check_alignment(void) {
    printf("Unpacked size: %zu\n", sizeof(struct Unpacked));
    printf("Packed size: %zu\n", sizeof(struct Packed));

    // Get field offset
    printf("Offset of b: %zu\n", offsetof(struct Unpacked, b));
}

// Serialization with packed structs
int serialize_packed(const struct Packed *data, const char *filename) {
    FILE *file = fopen(filename, "wb");
    if (file == NULL) {
        return -1;
    }

    // Safe: no padding, predictable layout
    fwrite(data, sizeof(struct Packed), 1, file);
    fclose(file);
    return 0;
}
```

### Protocol Buffers / MessagePack (Third-Party)

```c
// Using protobuf-c: https://github.com/protobuf-c/protobuf-c
// Define .proto file, generate C code with protoc-c

// Example usage (generated code):
/*
Person person = PERSON__INIT;
person.name = "Alice";
person.id = 123;

// Serialize
size_t len = person__get_packed_size(&person);
uint8_t *buffer = malloc(len);
person__pack(&person, buffer);

// Deserialize
Person *parsed = person__unpack(NULL, len, buffer);
printf("Name: %s, ID: %d\n", parsed->name, parsed->id);
person__free_unpacked(parsed, NULL);
*/
```

**See also:** `patterns-serialization-dev` for cross-language serialization patterns

---

## Testing

C has no built-in test framework. Unit testing typically uses third-party frameworks like Unity, CMocka, or Check.

### Unity Framework

```c
// Unity: https://github.com/ThrowTheSwitch/Unity
#include "unity.h"

// Functions under test
int add(int a, int b) {
    return a + b;
}

int divide(int a, int b) {
    if (b == 0) return -1;  // Error code
    return a / b;
}

// Setup/teardown (called before/after each test)
void setUp(void) {
    // Initialize test fixtures
}

void tearDown(void) {
    // Clean up after test
}

// Test cases
void test_add_positive_numbers(void) {
    TEST_ASSERT_EQUAL_INT(5, add(2, 3));
    TEST_ASSERT_EQUAL_INT(10, add(7, 3));
}

void test_add_negative_numbers(void) {
    TEST_ASSERT_EQUAL_INT(-5, add(-2, -3));
    TEST_ASSERT_EQUAL_INT(0, add(-5, 5));
}

void test_divide_success(void) {
    TEST_ASSERT_EQUAL_INT(2, divide(6, 3));
    TEST_ASSERT_EQUAL_INT(-2, divide(-6, 3));
}

void test_divide_by_zero(void) {
    TEST_ASSERT_EQUAL_INT(-1, divide(10, 0));
}

// Main test runner
int main(void) {
    UNITY_BEGIN();

    RUN_TEST(test_add_positive_numbers);
    RUN_TEST(test_add_negative_numbers);
    RUN_TEST(test_divide_success);
    RUN_TEST(test_divide_by_zero);

    return UNITY_END();
}
```

### Common Unity Assertions

```c
// Integer assertions
TEST_ASSERT_EQUAL_INT(expected, actual);
TEST_ASSERT_NOT_EQUAL_INT(expected, actual);
TEST_ASSERT_GREATER_THAN_INT(threshold, actual);
TEST_ASSERT_LESS_THAN_INT(threshold, actual);
TEST_ASSERT_INT_WITHIN(delta, expected, actual);

// Floating point
TEST_ASSERT_EQUAL_FLOAT(expected, actual);
TEST_ASSERT_FLOAT_WITHIN(delta, expected, actual);

// Strings
TEST_ASSERT_EQUAL_STRING(expected, actual);
TEST_ASSERT_EQUAL_STRING_LEN(expected, actual, length);

// Memory
TEST_ASSERT_EQUAL_MEMORY(expected, actual, length);

// Pointers
TEST_ASSERT_NULL(pointer);
TEST_ASSERT_NOT_NULL(pointer);
TEST_ASSERT_EQUAL_PTR(expected, actual);

// Boolean
TEST_ASSERT_TRUE(condition);
TEST_ASSERT_FALSE(condition);

// Custom message
TEST_ASSERT_EQUAL_INT_MESSAGE(expected, actual, "Custom failure message");
```

### CMocka Framework

```c
// CMocka: https://cmocka.org/
#include <stdarg.h>
#include <stddef.h>
#include <setjmp.h>
#include <cmocka.h>

// Function to test
char *format_name(const char *first, const char *last) {
    if (first == NULL || last == NULL) {
        return NULL;
    }

    size_t len = strlen(first) + strlen(last) + 2;
    char *result = malloc(len);
    snprintf(result, len, "%s %s", first, last);
    return result;
}

// Test with setup/teardown
static int setup(void **state) {
    char *test_data = strdup("test");
    *state = test_data;
    return 0;
}

static int teardown(void **state) {
    free(*state);
    return 0;
}

// Test functions
static void test_format_name_success(void **state) {
    (void)state;  // Unused

    char *result = format_name("John", "Doe");
    assert_non_null(result);
    assert_string_equal(result, "John Doe");
    free(result);
}

static void test_format_name_null_input(void **state) {
    (void)state;

    char *result = format_name(NULL, "Doe");
    assert_null(result);

    result = format_name("John", NULL);
    assert_null(result);
}

// Test runner
int main(void) {
    const struct CMUnitTest tests[] = {
        cmocka_unit_test(test_format_name_success),
        cmocka_unit_test(test_format_name_null_input),
        cmocka_unit_test_setup_teardown(test_with_fixture, setup, teardown),
    };

    return cmocka_run_group_tests(tests, NULL, NULL);
}
```

### Mocking with CMocka

```c
// Mock a function
int __wrap_database_get_user(int id);  // Our mock
int __real_database_get_user(int id);  // Real function

int __wrap_database_get_user(int id) {
    check_expected(id);
    return (int)mock();
}

// Test using mock
static void test_with_mock(void **state) {
    (void)state;

    // Expect call with id=1, return 42
    expect_value(__wrap_database_get_user, id, 1);
    will_return(__wrap_database_get_user, 42);

    // Function under test calls database_get_user
    int result = process_user(1);
    assert_int_equal(result, 42);
}

// Compile with: -Wl,--wrap=database_get_user
```

### Check Framework

```c
// Check: https://libcheck.github.io/check/
#include <check.h>

START_TEST(test_add) {
    ck_assert_int_eq(add(2, 3), 5);
    ck_assert_int_eq(add(-1, 1), 0);
}
END_TEST

START_TEST(test_divide) {
    ck_assert_int_eq(divide(6, 3), 2);
    ck_assert_int_eq(divide(10, 0), -1);
}
END_TEST

Suite *create_suite(void) {
    Suite *s = suite_create("Math");

    TCase *tc_core = tcase_create("Core");
    tcase_add_test(tc_core, test_add);
    tcase_add_test(tc_core, test_divide);
    suite_add_tcase(s, tc_core);

    return s;
}

int main(void) {
    Suite *s = create_suite();
    SRunner *sr = srunner_create(s);

    srunner_run_all(sr, CK_NORMAL);
    int failed = srunner_ntests_failed(sr);
    srunner_free(sr);

    return (failed == 0) ? 0 : 1;
}
```

### Test Organization

```c
// test_math.c
#include "unity.h"
#include "math_functions.h"

void test_addition(void) {
    TEST_ASSERT_EQUAL_INT(5, add(2, 3));
}

void test_subtraction(void) {
    TEST_ASSERT_EQUAL_INT(2, subtract(5, 3));
}

// test_string.c
#include "unity.h"
#include "string_functions.h"

void test_concat(void) {
    char *result = concat("Hello", "World");
    TEST_ASSERT_EQUAL_STRING("HelloWorld", result);
    free(result);
}

// test_runner.c
#include "unity.h"

// External test declarations
extern void test_addition(void);
extern void test_subtraction(void);
extern void test_concat(void);

void setUp(void) {}
void tearDown(void) {}

int main(void) {
    UNITY_BEGIN();

    // Math tests
    RUN_TEST(test_addition);
    RUN_TEST(test_subtraction);

    // String tests
    RUN_TEST(test_concat);

    return UNITY_END();
}
```

### Coverage and Profiling

```bash
# Compile with coverage flags (GCC/Clang)
gcc -fprofile-arcs -ftest-coverage -o test_program test.c functions.c

# Run tests
./test_program

# Generate coverage report
gcov functions.c
lcov --capture --directory . --output-file coverage.info
genhtml coverage.info --output-directory coverage_html
```

---

## Cross-Cutting Patterns

For cross-language comparison and translation patterns, see:

- `patterns-concurrency-dev` - Threads, mutexes, atomics, channels
- `patterns-serialization-dev` - JSON, binary formats, endianness
- `patterns-metaprogramming-dev` - Macros, code generation

---

## References

- [C Programming Language (K&R Book)](https://en.wikipedia.org/wiki/The_C_Programming_Language)
- [C Standard Library Reference](https://en.cppreference.com/w/c)
- [GCC Documentation](https://gcc.gnu.org/onlinedocs/)
- [Clang Documentation](https://clang.llvm.org/docs/)
- Specialized skills: `lang-c-memory-eng`, `lang-c-posix-dev`, `lang-c-library-dev`, `lang-c-systems-eng`, `lang-c-embedded-dev`
