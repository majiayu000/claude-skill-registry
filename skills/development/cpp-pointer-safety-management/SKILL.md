---
name: cpp-pointer-safety-management
description: Comprehensive guidelines for safe pointer management in C/C++ code. Use when working with pointer variables, dynamic memory allocation, or any code involving pointer operations to prevent memory leaks, memory corruption, and dangling pointers.
---

# C/C++ Pointer Safety Management

## When to Use This Skill
Apply these guidelines when:
- Declaring or initializing pointer variables
- Allocating dynamic memory on the heap
- Passing pointers between functions
- Accessing memory through pointers
- Releasing or deallocating memory
- Refactoring legacy pointer-based code

## Declaration and Initialization

### Explicit Type Specification
- Always declare pointers with explicit types
- Use the "asterisk (*) rule" for clarity: place the asterisk next to the pointer name, not the type

### Immediate Initialization
- Initialize pointers immediately upon declaration
- Either assign valid memory address or set to NULL/nullptr
- Never leave pointers uninitialized

```cpp
// Good
int* pointer = nullptr;
int* pointer = new int(42);

// Bad
int* pointer;  // Uninitialized - dangerous!
```

## Memory Allocation and Usage

### Pre-Use Validation
- Always check pointer validity before dereferencing
- Perform boundary checks for array pointers
- Understand the data type the pointer references

### Clarity and Safety Techniques
- Use additional variables to improve code clarity
- Implement "dog tag fields" or explicit redundancy for validation
- Apply "memory parachute" techniques for critical operations

```cpp
// Validation before use
if (pointer != nullptr) {
    *pointer = value;
}

// Boundary checking
for (int i = 0; i < array_size && i < max_safe_size; i++) {
    array_ptr[i] = value;
}
```

## Memory Release and Cleanup

### Proper Deallocation
- Always free dynamically allocated memory
- Set pointers to NULL/nullptr after deletion to prevent dangling pointers
- Exercise caution when deleting nodes in linked structures

```cpp
delete pointer;
pointer = nullptr;  // Prevent dangling pointer
```

### Linked List Node Deletion
- Maintain list integrity during node removal
- Update adjacent node pointers before freeing memory
- Consider edge cases (head, tail, single node)

## Safe Alternatives

### Modern C++ Approaches
- Use smart pointers (`std::unique_ptr`, `std::shared_ptr`)
- Prefer C++ references over pointers when possible
- Leverage RAII (Resource Acquisition Is Initialization) patterns

### Encapsulation Techniques
- Use wrapper functions (e.g., SAFE_ routines) to isolate pointer operations
- Avoid pointer type casting when possible
- Implement custom memory managers for complex scenarios

```cpp
// Smart pointer example
std::unique_ptr<int> smart_ptr = std::make_unique<int>(42);
// Automatic cleanup when out of scope
```

## Common Pitfalls to Avoid

- Never dereference NULL or uninitialized pointers
- Avoid memory leaks by matching every allocation with deallocation
- Prevent double-free errors
- Eliminate dangling pointers
- Avoid buffer overruns in pointer arithmetic
- Minimize use of raw pointers in modern C++ code