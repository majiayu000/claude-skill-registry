---
name: c
description: C programming with memory management, pointers, structs, and system-level development. Use for .c files.
---

# C

The foundational language for modern computing, operating systems, and embedded systems.

## When to Use

- Operating Systems / Drivers
- Embedded Systems
- High-performance computing
- Legacy codebases

## Quick Start

```c
#include <stdio.h>

int main() {
    printf("Hello, World!\n");
    return 0;
}
```

## Core Concepts

### Pointers

Variables that store memory addresses.

```c
int x = 10;
int *p = &x; // p holds address of x
printf("%d", *p); // Dereference p to get 10
```

### Memory Management

Manual allocation and deallocation.

```c
int *arr = (int*)malloc(10 * sizeof(int));
// use arr...
free(arr);
```

### Structs

User-defined data types.

## Best Practices

**Do**:

- Always initialized variables
- Check return values of `malloc`
- Guard against buffer overflows (use `snprintf` over `sprintf`)
- Use tools like Valgrind to check for leaks

**Don't**:

- Return pointers to local variables (stack memory)
- Use `gets()` (unsafe)

## References

- [C Reference](https://en.cppreference.com/w/c)
