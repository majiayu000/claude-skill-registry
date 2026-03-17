---
name: C Ecosystem
description: This skill should be used when working with C projects, "C11", "C17", "C23", "Makefile", "gcc", "clang", "valgrind", "getopt", or C language patterns. Provides comprehensive Modern C (C11-C23) patterns, memory management, and CLI development best practices.
---

# C Language

## Standards Evolution

### C11 (ISO/IEC 9899:2011)
Major modernization with threading and type-generic features:
- `_Generic` - Type-generic selection for polymorphic macros
- `_Atomic` - Atomic types and operations for lock-free programming
- `_Thread_local` - Thread-local storage duration
- `_Static_assert` - Compile-time assertions
- `_Alignas/_Alignof` - Alignment specifier and query
- `_Noreturn` - Function that does not return
- Anonymous structs/unions

### C17 (ISO/IEC 9899:2018)
Bug fix release with no new features. `__STDC_VERSION__` = 201710L.

### C23 (ISO/IEC 9899:2024)
- `nullptr` - Null pointer constant with `nullptr_t` type
- `typeof` - Type inference operator
- `constexpr` - Compile-time constant objects
- `auto` - Type inference for variables
- Binary literals (`0b`), digit separators (`'`)
- Attributes: `[[nodiscard]]`, `[[maybe_unused]]`, `[[deprecated]]`, `[[fallthrough]]`, `[[noreturn]]`
- `bool`, `true`, `false` as keywords
- `#embed` for binary resource inclusion

## Type System

**Fixed-width integers** (`stdint.h`):
- `int8_t`, `int16_t`, `int32_t`, `int64_t` / unsigned variants
- `intptr_t`, `uintptr_t` - Pointer-sized integers
- `size_t` - Unsigned size type; `ptrdiff_t` - Signed pointer difference

**Type-generic selection** (C11):
```c
#define print_value(x) _Generic((x), \
    int: print_int, \
    double: print_double, \
    char *: print_string, \
    default: print_unknown)(x)
```

**Compound literals and designated initializers**:
```c
struct config cfg = { .name = "myapp", .timeout = 30, .verbose = true };
draw((struct point){.x = 10, .y = 20});
```

## Concurrency (C11)

**Atomics**:
```c
#include <stdatomic.h>
_Atomic int counter = 0;
atomic_fetch_add(&counter, 1);
```

**Thread-local storage**: `_Thread_local int errno_local;`

## Undefined Behavior to Avoid
- **Memory**: Null dereference, use-after-free, buffer overflow, double-free
- **Arithmetic**: Signed integer overflow, division by zero, shift beyond type width
- **Aliasing**: Strict aliasing violations, type punning without union
- **Sequence**: Modifying variable twice between sequence points

Use sanitizers (ASan, UBSan) during development to detect UB.

## Anti-patterns
- `void*` abuse - Use `_Generic` macros or code generation
- Magic numbers - Use named constants with `#define` or `enum`
- `strcpy`/`strcat`/`sprintf`/`gets` - Use `snprintf`, `fgets`
- `scanf` with unbounded `%s` - Use `%Ns` with explicit width
- Unchecked `malloc` - Always check for NULL
- Format string vuln (`printf(user_input)`) - Use `printf("%s", user_input)`

# Memory Management

## Allocation Patterns

**Basic allocation** - Always check return values:
```c
char *dst = malloc(len);
if (!dst) return NULL;
```

**Arena allocator** - Bulk allocation with single-point deallocation:
```c
typedef struct { char *base; size_t size, offset; } Arena;
void *arena_alloc(Arena *a, size_t bytes) {
    size_t aligned = (bytes + 7) & ~7;
    if (a->offset + aligned > a->size) return NULL;
    void *ptr = a->base + a->offset;
    a->offset += aligned;
    return ptr;
}
```
Use case: Parsing, compilers, request handling.

**Pool allocator** - Fixed-size object allocation with O(1) alloc/free.
Use case: Game entities, network connections, fixed-size records.

**Goto cleanup** - Resource cleanup with single exit point:
```c
int process_file(const char *path) {
    int result = -1;
    FILE *fp = NULL; char *buffer = NULL;
    fp = fopen(path, "r"); if (!fp) goto cleanup;
    buffer = malloc(SIZE); if (!buffer) goto cleanup;
    // ... process ...
    result = 0;
cleanup:
    free(buffer);
    if (fp) fclose(fp);
    return result;
}
```

# CLI Development

**getopt** - POSIX standard option parsing:
```c
while ((opt = getopt(argc, argv, "vo:h")) != -1) {
    switch (opt) {
    case 'v': verbose = 1; break;
    case 'o': output = optarg; break;
    case 'h': /* help */ return 0;
    default: return 1;
    }
}
// Remaining args: argv[optind] to argv[argc-1]
```

**getopt_long** - GNU extension for `--long-options`.

**Exit codes**: 0=success, 1=error, 2=usage error, 126=not executable, 127=not found, 128+N=signal N. See `<sysexits.h>` for EX_USAGE, EX_NOINPUT, etc.

**Signal handling**:
```c
static atomic_int running = 1;
static void handle_signal(int sig) { (void)sig; running = 0; }
// Use sigaction() instead of signal() for portability
```

**Error reporting**: Include program name, use `strerror(errno)` for system errors.

# Toolchain

## Compiler Flags
```bash
# GCC/Clang recommended
-std=c11 -Wall -Wextra -Wpedantic -Werror -Wshadow -Wconversion -Wstrict-prototypes
# GCC 10+ static analysis
-fanalyzer
```

## Sanitizers
- **AddressSanitizer**: `-fsanitize=address -fno-omit-frame-pointer`
- **UndefinedBehaviorSanitizer**: `-fsanitize=undefined`
- **ThreadSanitizer**: `-fsanitize=thread` (cannot combine with ASan)
- **MemorySanitizer** (Clang only): `-fsanitize=memory`

## Static Analysis
- **clang-tidy**: `clang-tidy src/*.c -- -std=c11`
- **cppcheck**: `cppcheck --enable=all --error-exitcode=1 src/`
- **valgrind**: `valgrind --leak-check=full --show-leak-kinds=all ./myapp`

## Testing
**Check** or **Unity** frameworks for unit testing.

# Build Systems

**Makefile** (simple):
```makefile
CC := gcc
CFLAGS := -std=c11 -Wall -Wextra -Wpedantic -g
SRCS := $(wildcard src/*.c)
OBJS := $(SRCS:.c=.o)
$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^ $(LDLIBS)
```

**CMake** and **Meson** for cross-platform builds. See cplusplus-ecosystem skill for detailed CMake patterns.

# Context7 Integration
- C reference: `/websites/cppreference_com`

# Best Practices
- Always check malloc/calloc/realloc return values
- Enable `-Wall -Wextra -Werror` for all builds
- Run with AddressSanitizer during development
- Use Valgrind before release
- Use fixed-width integer types from `stdint.h`
- Prefer `snprintf` over `sprintf`
- Use designated initializers for struct clarity
- Document ownership semantics in function comments
