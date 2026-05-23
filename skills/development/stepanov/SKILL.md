---
name: stepanov-generic-programming
description: Write C++ code following Alexander Stepanov's generic programming principles. Emphasizes algorithms over data structures, concepts as requirements, and mathematical rigor in interface design. Use when designing reusable algorithms or data structures that must work across types.
---

# Alexander Stepanov Style Guide

## Overview

Alexander Stepanov is the creator of the Standard Template Library (STL). His work transformed C++ from an OOP language into a generic programming powerhouse. The STL's design—algorithms operating on iterators over containers—is perhaps the most influential library design in programming history.

## Core Philosophy

> "Generic programming is about abstracting and classifying algorithms and data structures."

> "If you want to be a good programmer, you have to study algorithms, not languages."

Stepanov believes programming is applied mathematics. Good abstractions come from understanding the **algebraic structures** underlying computation.

## Design Principles

1. **Algorithms are Primary**: Design algorithms first, then figure out the minimal requirements on types.

2. **Concepts Define Requirements**: An algorithm's requirements on its types form a "concept"—a set of operations and properties.

3. **Iterators Abstract Position**: Iterators decouple algorithms from containers by abstracting "position in a sequence."

4. **Regular Types**: Types should behave like mathematical values—copyable, assignable, equality-comparable.

## Iterator Hierarchy

| Category | Operations | Example |
|----------|------------|---------|
| **Input** | `++`, `*`, `==` | `istream_iterator` |
| **Output** | `++`, `*` | `ostream_iterator` |
| **Forward** | Input + multi-pass | `forward_list::iterator` |
| **Bidirectional** | Forward + `--` | `list::iterator` |
| **Random Access** | Bidirectional + `[]`, `+`, `-` | `vector::iterator` |
| **Contiguous** (C++20) | Random Access + contiguous memory | `vector::iterator`, raw pointers |

## When Writing Code

### Always

- Define the minimal concept requirements for template parameters
- Separate algorithms from data structures via iterators
- Make types "regular" (copyable, assignable, comparable)
- Provide both iterator-pair and range overloads
- Document complexity guarantees

### Never

- Couple algorithms to specific container types
- Require more from types than the algorithm needs
- Ignore mathematical properties (associativity, commutativity)
- Break the expected semantics of standard operations

### Prefer

- Iterator pairs over container references (until ranges)
- Half-open ranges `[first, last)` over closed ranges
- Value semantics over reference semantics
- Composition of simple algorithms over monolithic ones

## Code Patterns

### Algorithm Design: Minimal Requirements

```cpp
// BAD: Requires specific container
template<typename T>
typename std::vector<T>::iterator 
find(std::vector<T>& v, const T& value);

// GOOD: Requires only InputIterator and EqualityComparable
template<typename InputIterator, typename T>
InputIterator find(InputIterator first, InputIterator last, const T& value) {
    while (first != last && !(*first == value)) {
        ++first;
    }
    return first;
}

// What does this algorithm ACTUALLY require?
// - InputIterator: ++, *, ==, copyable
// - T: EqualityComparable with *first
// Document these as the concept requirements
```

### Regular Types

```cpp
// A "regular" type behaves like an int: value semantics
class Point {
    double x_, y_;
public:
    // Default constructible (like int{} is 0)
    Point() : x_(0), y_(0) {}
    
    Point(double x, double y) : x_(x), y_(y) {}
    
    // Copyable (compiler-generated is fine)
    Point(const Point&) = default;
    Point& operator=(const Point&) = default;
    
    // Equality comparable
    friend bool operator==(const Point& a, const Point& b) {
        return a.x_ == b.x_ && a.y_ == b.y_;
    }
    friend bool operator!=(const Point& a, const Point& b) {
        return !(a == b);
    }
    
    // For ordered containers, provide total ordering
    friend bool operator<(const Point& a, const Point& b) {
        return std::tie(a.x_, a.y_) < std::tie(b.x_, b.y_);
    }
};

// Regular types can be used with all standard algorithms
std::vector<Point> points;
std::sort(points.begin(), points.end());
auto it = std::find(points.begin(), points.end(), Point{1.0, 2.0});
```

### Iterator Implementation

```cpp
template<typename T>
class LinkedList {
    struct Node {
        T value;
        Node* next;
    };
    Node* head_ = nullptr;
    
public:
    // Forward iterator (minimum for most algorithms)
    class iterator {
        Node* current_;
    public:
        // Iterator traits (required for algorithm compatibility)
        using iterator_category = std::forward_iterator_tag;
        using value_type = T;
        using difference_type = std::ptrdiff_t;
        using pointer = T*;
        using reference = T&;
        
        iterator(Node* n = nullptr) : current_(n) {}
        
        reference operator*() const { return current_->value; }
        pointer operator->() const { return &current_->value; }
        
        iterator& operator++() {
            current_ = current_->next;
            return *this;
        }
        
        iterator operator++(int) {
            iterator tmp = *this;
            ++(*this);
            return tmp;
        }
        
        friend bool operator==(const iterator& a, const iterator& b) {
            return a.current_ == b.current_;
        }
        friend bool operator!=(const iterator& a, const iterator& b) {
            return !(a == b);
        }
    };
    
    iterator begin() { return iterator(head_); }
    iterator end() { return iterator(nullptr); }
};
```

### Composing Algorithms

```cpp
// Stepanov's approach: build complex operations from simple ones

// rotate_copy = copy + rotate semantics
template<typename ForwardIt, typename OutputIt>
OutputIt rotate_copy(ForwardIt first, ForwardIt middle, ForwardIt last,
                     OutputIt d_first) {
    d_first = std::copy(middle, last, d_first);
    return std::copy(first, middle, d_first);
}

// partition_copy = partition semantics, preserves original
template<typename InputIt, typename OutputIt1, typename OutputIt2, typename Pred>
std::pair<OutputIt1, OutputIt2>
partition_copy(InputIt first, InputIt last,
               OutputIt1 d_first_true, OutputIt2 d_first_false,
               Pred pred) {
    while (first != last) {
        if (pred(*first)) {
            *d_first_true++ = *first;
        } else {
            *d_first_false++ = *first;
        }
        ++first;
    }
    return {d_first_true, d_first_false};
}
```

## Mental Model

Stepanov thinks like a mathematician:

1. **What is the abstract operation?** (e.g., "find the first element satisfying P")
2. **What are the minimal requirements?** (e.g., "forward traversal, predicate")
3. **What algebraic properties must hold?** (e.g., "predicate is consistent")
4. **What is the complexity?** (e.g., "O(n) comparisons")

## The STL Design Principles

1. **Containers own data**: `vector`, `list`, `map` manage memory
2. **Iterators abstract position**: Algorithms don't know about containers
3. **Algorithms implement operations**: Sorting, searching, transforming
4. **Function objects customize**: Predicates, comparators, transformers

This separation enables N algorithms + M containers = N×M combinations, not N×M implementations.

## Modern Evolution

- **C++20 Ranges**: Composable, lazy algorithm pipelines
- **Concepts**: Explicit constraint documentation and checking
- **Views**: Non-owning ranges for functional composition

```cpp
// Modern Stepanov-style code
auto result = numbers 
    | std::views::filter([](int n) { return n % 2 == 0; })
    | std::views::transform([](int n) { return n * n; })
    | std::views::take(10);
```

