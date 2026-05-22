---
name: thompson-elegant-systems
description: Write systems code in the style of Ken Thompson, co-creator of Unix, C, Go, UTF-8, and Plan 9. Emphasizes radical simplicity, elegant algorithms, and small composable tools. Use when designing systems that must endure.
---

# Ken Thompson Style Guide

## Overview

Ken Thompson co-created Unix, contributed to C, designed UTF-8, created Plan 9, and co-designed Go. He is a Turing Award winner whose work spans five decades of profound influence. His hallmark is finding the simplest possible solution that actually works.

## Core Philosophy

> "When in doubt, use brute force."

> "One of my most productive days was throwing away 1000 lines of code."

> "I think the major good idea in Unix was its clean and simple interface: open, close, read, and write."

Thompson believes complexity is the enemy. The best code is the code you don't write. The best abstraction is the one that disappears.

## Design Principles

1. **Radical Simplicity**: The simplest solution that works is the best.

2. **Small Sharp Tools**: Programs should do one thing excellently.

3. **Composition**: Combine simple tools to solve complex problems.

4. **Brute Force Works**: Don't be clever when simple is good enough.

## When Writing Code

### Always

- Question every line of code—is it necessary?
- Design for composition via simple interfaces
- Use text as the universal interface
- Throw away code that doesn't serve the goal
- Prototype with brute force, optimize only if needed
- Trust the tools you build

### Never

- Add features "just in case"
- Optimize before measuring
- Create complex abstractions for simple problems
- Fear starting over
- Conflate clever with good

### Prefer

- Simple linear algorithms over clever ones
- Text streams over binary formats
- Regular expressions for text processing
- Iteration over recursion when simpler
- Small programs over monolithic ones

## Code Patterns

### The Unix Filter Pattern

```c
// A perfect Unix filter: read stdin, transform, write stdout
#include <stdio.h>
#include <ctype.h>

// uppercase: convert input to uppercase
int main(void) {
    int c;
    while ((c = getchar()) != EOF) {
        putchar(toupper(c));
    }
    return 0;
}

// Usage: cat file.txt | uppercase | sort | uniq
// Composition through pipes
```

### Simple Interfaces

```c
// The Unix file interface: elegant simplicity
// Everything is open/close/read/write

int fd = open("file.txt", O_RDONLY);
char buf[4096];
ssize_t n;

while ((n = read(fd, buf, sizeof(buf))) > 0) {
    write(STDOUT_FILENO, buf, n);
}

close(fd);

// This same interface works for:
// - Files
// - Pipes
// - Sockets
// - Devices
// - /proc entries
```

### Brute Force First

```c
// Problem: find if a pattern exists in text
// Thompson's approach: just search

// Simple, obvious, correct
int contains(const char *text, const char *pattern) {
    while (*text) {
        const char *t = text;
        const char *p = pattern;
        while (*p && *t == *p) {
            t++;
            p++;
        }
        if (*p == '\0') return 1;
        text++;
    }
    return 0;
}

// Don't reach for KMP or Boyer-Moore until you've
// measured and proven you need them.
// For most inputs, brute force is fast enough.
```

### Minimal Data Structures

```c
// Arrays and structs solve most problems
// Don't reach for complexity

typedef struct {
    char *key;
    char *value;
} Entry;

typedef struct {
    Entry *entries;
    int count;
    int capacity;
} Table;

// Linear search is fine for small tables
char *table_get(Table *t, const char *key) {
    for (int i = 0; i < t->count; i++) {
        if (strcmp(t->entries[i].key, key) == 0) {
            return t->entries[i].value;
        }
    }
    return NULL;
}

// Only add hash table when profiling proves you need it
```

### UTF-8: Elegant Encoding

```c
// UTF-8: Thompson and Pike's masterpiece
// Self-synchronizing, ASCII-compatible, variable-width

// Decode one UTF-8 codepoint
int utf8_decode(const char *s, int *codepoint) {
    unsigned char c = s[0];
    
    if (c < 0x80) {
        *codepoint = c;
        return 1;
    }
    if ((c & 0xE0) == 0xC0) {
        *codepoint = (c & 0x1F) << 6 | (s[1] & 0x3F);
        return 2;
    }
    if ((c & 0xF0) == 0xE0) {
        *codepoint = (c & 0x0F) << 12 | (s[1] & 0x3F) << 6 | (s[2] & 0x3F);
        return 3;
    }
    if ((c & 0xF8) == 0xF0) {
        *codepoint = (c & 0x07) << 18 | (s[1] & 0x3F) << 12 | 
                     (s[2] & 0x3F) << 6 | (s[3] & 0x3F);
        return 4;
    }
    return -1;  // Invalid
}

// Simple rules, profound implications
```

### Go: Modern Thompson

```go
// Go reflects Thompson's philosophy for modern systems

// Simple concurrency: goroutines and channels
func pipeline() {
    naturals := make(chan int)
    squares := make(chan int)

    // Generator
    go func() {
        for x := 0; ; x++ {
            naturals <- x
        }
    }()

    // Squarer
    go func() {
        for x := range naturals {
            squares <- x * x
        }
    }()

    // Consumer
    for i := 0; i < 10; i++ {
        fmt.Println(<-squares)
    }
}

// No inheritance, no generics (initially), no exceptions
// Just structs, interfaces, goroutines, channels
// Radical simplicity
```

### Regular Expressions

```c
// Thompson's NFA regex algorithm: elegant and efficient

// Match: reports whether regexp matches text
// Simplified from Thompson's original
int match(const char *regexp, const char *text) {
    if (regexp[0] == '^')
        return matchhere(regexp + 1, text);
    
    do {  // must look even if string is empty
        if (matchhere(regexp, text))
            return 1;
    } while (*text++ != '\0');
    
    return 0;
}

int matchhere(const char *regexp, const char *text) {
    if (regexp[0] == '\0')
        return 1;
    if (regexp[1] == '*')
        return matchstar(regexp[0], regexp + 2, text);
    if (regexp[0] == '$' && regexp[1] == '\0')
        return *text == '\0';
    if (*text != '\0' && (regexp[0] == '.' || regexp[0] == *text))
        return matchhere(regexp + 1, text + 1);
    return 0;
}

// ~30 lines for a working regex engine
// That's Thompson elegance
```

## Mental Model

Thompson approaches problems by asking:

1. **What's the simplest thing that could work?** Start there
2. **Can I throw away code?** Less is more
3. **Does this compose?** Small pieces, loosely joined
4. **Is brute force good enough?** Usually yes
5. **Would I want to maintain this?** Simplicity endures

## Signature Thompson Moves

- Text streams as universal interface
- Brute force before cleverness
- Throwing away code
- Small programs that compose
- Regular expressions for text
- Clean, minimal interfaces
