---
name: ritchie-c-mastery
description: Write systems code in the style of Dennis Ritchie, co-creator of Unix and creator of C. Emphasizes clean abstraction, portable systems code, and the art of language design. Use when writing C or designing system interfaces.
---

# Dennis Ritchie Style Guide

## Overview

Dennis Ritchie created the C programming language and co-created Unix with Ken Thompson. C became the lingua franca of systems programming, and Unix's design principles shaped all modern operating systems. Ritchie's work exemplifies how good abstraction enables both portability and performance.

## Core Philosophy

> "Unix is basically a simple operating system, but you have to be a genius to understand the simplicity."

> "C is quirky, flawed, and an enormous success."

> "UNIX is very simple, it just needs a genius to understand its simplicity."

Ritchie believed in creating abstractions that map closely to the machine while remaining portable across different hardware.

## Design Principles

1. **Abstraction with Transparency**: Hide details but don't hide the cost.

2. **Portability**: Write for the abstract machine, not specific hardware.

3. **Trust the Programmer**: C gives you power; use it responsibly.

4. **Minimal Language, Maximal Library**: Keep the language small.

## When Writing Code

### Always

- Write portable C using standard constructs
- Keep functions short and focused
- Use meaningful names that convey purpose
- Handle errors explicitly
- Understand what the compiler generates
- Document interfaces, not implementations

### Never

- Rely on undefined behavior
- Assume type sizes (use stdint.h)
- Ignore compiler warnings
- Cast unnecessarily
- Use magic numbers

### Prefer

- `size_t` for sizes and counts
- `stdint.h` types for fixed-width needs
- `const` for read-only data
- Stack allocation over heap when possible
- Static functions for internal linkage

## Code Patterns

### The K&R Style

```c
// Classic Ritchie/Kernighan style

#include <stdio.h>
#include <string.h>

// Functions are short and focused
int strlen_safe(const char *s)
{
    int n;
    
    for (n = 0; *s != '\0'; s++)
        n++;
    return n;
}

// Compact but clear
void reverse(char *s)
{
    int c, i, j;
    
    for (i = 0, j = strlen(s) - 1; i < j; i++, j--) {
        c = s[i];
        s[i] = s[j];
        s[j] = c;
    }
}

// Main is simple
int main(void)
{
    char buf[100];
    
    while (fgets(buf, sizeof(buf), stdin) != NULL) {
        buf[strcspn(buf, "\n")] = '\0';  // Remove newline
        reverse(buf);
        printf("%s\n", buf);
    }
    return 0;
}
```

### Pointer Idioms

```c
// Pointers are addresses—embrace them

// Copy string: pointer version (Ritchie preferred)
void strcpy_ptr(char *dst, const char *src)
{
    while ((*dst++ = *src++) != '\0')
        ;
}

// Traverse array with pointer
void process_array(int *arr, size_t n)
{
    int *end = arr + n;
    
    for (int *p = arr; p < end; p++) {
        process(*p);
    }
}

// Pointer to pointer for modification
int alloc_buffer(char **buf, size_t size)
{
    *buf = malloc(size);
    return *buf != NULL ? 0 : -1;
}
```

### Error Handling

```c
// C style: return values indicate errors
// Ritchie Unix convention: 0 = success, -1 = error, errno set

#include <errno.h>

int read_file(const char *path, char *buf, size_t size)
{
    FILE *fp;
    size_t n;
    
    fp = fopen(path, "r");
    if (fp == NULL) {
        return -1;  // errno is set by fopen
    }
    
    n = fread(buf, 1, size - 1, fp);
    if (ferror(fp)) {
        fclose(fp);
        return -1;
    }
    
    buf[n] = '\0';
    fclose(fp);
    return 0;
}

// Usage:
if (read_file("config.txt", buf, sizeof(buf)) < 0) {
    perror("read_file");
    exit(1);
}
```

### Struct Design

```c
// Structs should be minimal and purposeful

typedef struct node {
    struct node *next;
    char *data;
} Node;

typedef struct list {
    Node *head;
    Node *tail;
    size_t count;
} List;

// Operations on structs
void list_init(List *l)
{
    l->head = NULL;
    l->tail = NULL;
    l->count = 0;
}

int list_push(List *l, const char *data)
{
    Node *n = malloc(sizeof(*n));
    if (n == NULL)
        return -1;
    
    n->data = strdup(data);
    n->next = l->head;
    l->head = n;
    if (l->tail == NULL)
        l->tail = n;
    l->count++;
    return 0;
}
```

### Header File Design

```c
// mylib.h - public interface only

#ifndef MYLIB_H
#define MYLIB_H

#include <stddef.h>

// Opaque type - implementation hidden
typedef struct context Context;

// Public API
Context *context_create(void);
void     context_destroy(Context *ctx);
int      context_process(Context *ctx, const char *input);
char    *context_result(Context *ctx);

#endif


// mylib.c - implementation

#include "mylib.h"
#include <stdlib.h>
#include <string.h>

struct context {
    char *buffer;
    size_t size;
    // Internal details hidden from users
};

Context *context_create(void)
{
    Context *ctx = malloc(sizeof(*ctx));
    if (ctx == NULL)
        return NULL;
    
    ctx->buffer = NULL;
    ctx->size = 0;
    return ctx;
}

// ... implementation continues
```

### The Unix API Style

```c
// Unix system calls: elegant, minimal

// Open returns fd or -1
int fd = open("file.txt", O_RDONLY);
if (fd < 0) {
    perror("open");
    exit(1);
}

// Read returns bytes read, 0 on EOF, -1 on error
char buf[4096];
ssize_t n;

while ((n = read(fd, buf, sizeof(buf))) > 0) {
    if (write(STDOUT_FILENO, buf, n) != n) {
        perror("write");
        exit(1);
    }
}

if (n < 0) {
    perror("read");
    exit(1);
}

close(fd);
```

### Portability

```c
#include <stdint.h>  // Fixed-width types
#include <limits.h>  // System limits

// Use fixed-width when you need exact sizes
uint32_t crc32(const uint8_t *data, size_t len);

// Use size_t for sizes
void process(const void *data, size_t size);

// Check limits, don't assume
#if CHAR_BIT != 8
#error "This code requires 8-bit bytes"
#endif

// Endianness handling
uint32_t read_be32(const uint8_t *p)
{
    return ((uint32_t)p[0] << 24) |
           ((uint32_t)p[1] << 16) |
           ((uint32_t)p[2] << 8)  |
           ((uint32_t)p[3]);
}
```

## Mental Model

Ritchie approaches systems programming by asking:

1. **What is the abstraction?** Define clean interfaces
2. **What is the cost?** Abstractions should be transparent
3. **Is this portable?** Avoid machine-specific assumptions
4. **Is the interface minimal?** Small interfaces are easier to implement
5. **What can go wrong?** Handle errors explicitly

## Signature Ritchie Moves

- Pointer arithmetic for efficiency
- Return values for error indication
- Opaque types for encapsulation
- Minimal header interfaces
- Standard library reliance
- Portable type usage
