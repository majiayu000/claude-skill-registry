---
name: c-cpp-to-lean4-translator
description: Translate C or C++ programs into equivalent Lean4 code, preserving program semantics and ensuring the generated code is well-typed, executable, and can run successfully. Use when the user asks to convert C/C++ code to Lean4, port C/C++ programs to Lean4, translate imperative code to functional Lean4, or create Lean4 versions of C/C++ algorithms.
---

# C/C++ to Lean4 Translator

## Overview

Transform C or C++ programs into equivalent Lean4 code that preserves the original semantics while leveraging Lean4's functional programming paradigm, strong type system, and proof capabilities.

## Translation Workflow

### Step 1: Analyze Input Code

Understand the C/C++ program structure and semantics:

1. **Identify program components:**
   - Functions and their signatures
   - Data structures (structs, classes, arrays)
   - Control flow patterns (loops, conditionals)
   - Memory management (allocation, pointers)
   - I/O operations
   - Dependencies and includes

2. **Understand semantics:**
   - What does the program compute?
   - What are the inputs and outputs?
   - Are there side effects?
   - What are the invariants and preconditions?

3. **Note translation challenges:**
   - Pointer arithmetic
   - Mutable state
   - Imperative loops
   - Manual memory management
   - Undefined behavior

### Step 2: Design Lean4 Structure

Plan the Lean4 equivalent before writing code:

1. **Choose appropriate types:**
   - `Int` for signed integers
   - `Nat` for unsigned integers and array indices
   - `Float` for floating-point numbers
   - `Array` for dynamic arrays
   - `List` for linked lists
   - Custom `structure` types for structs/classes

2. **Determine purity:**
   - Pure functions: return values directly
   - Side effects: use `IO` monad
   - Mutable state: use `IO.Ref` or `ST` monad

3. **Plan control flow translation:**
   - Loops → Recursive functions
   - Mutable variables → Function parameters
   - Early returns → Conditional expressions

4. **Handle memory:**
   - Stack allocation → Direct values
   - Heap allocation → Automatic memory management
   - Pointers → Direct values or references

### Step 3: Translate Code

Follow these translation principles:

#### Functions

**Pattern: Pure function**
```c
// C/C++
int add(int a, int b) {
    return a + b;
}
```

```lean
-- Lean4
def add (a b : Int) : Int :=
  a + b
```

**Pattern: Function with side effects**
```c
// C/C++
void printSum(int a, int b) {
    printf("%d\n", a + b);
}
```

```lean
-- Lean4
def printSum (a b : Int) : IO Unit :=
  IO.println (a + b)
```

#### Control Flow

**Pattern: If-else**
```c
// C/C++
int max(int a, int b) {
    if (a > b) return a;
    else return b;
}
```

```lean
-- Lean4
def max (a b : Int) : Int :=
  if a > b then a else b
```

**Pattern: For loop → Tail recursion**
```c
// C/C++
int sum(int n) {
    int result = 0;
    for (int i = 0; i < n; i++) {
        result += i;
    }
    return result;
}
```

```lean
-- Lean4
def sum (n : Nat) : Nat :=
  let rec loop (i acc : Nat) : Nat :=
    if i >= n then acc
    else loop (i + 1) (acc + i)
  loop 0 0
```

**Pattern: While loop → Recursion**
```c
// C/C++
int factorial(int n) {
    int result = 1;
    while (n > 1) {
        result *= n;
        n--;
    }
    return result;
}
```

```lean
-- Lean4
def factorial (n : Nat) : Nat :=
  let rec loop (n acc : Nat) : Nat :=
    if n <= 1 then acc
    else loop (n - 1) (acc * n)
  loop n 1
```

#### Data Structures

**Pattern: Struct**
```c
// C/C++
struct Point {
    int x;
    int y;
};
```

```lean
-- Lean4
structure Point where
  x : Int
  y : Int
  deriving Repr
```

**Pattern: Array**
```c
// C/C++
int arr[5] = {1, 2, 3, 4, 5};
```

```lean
-- Lean4
def arr : Array Int := #[1, 2, 3, 4, 5]
```

#### Pointers and References

**Key principle:** Lean4 doesn't have raw pointers. Translate based on usage:

- **Read-only pointers:** Pass by value
- **Output parameters:** Return values (use tuples for multiple returns)
- **Mutable references:** Use `IO.Ref` or return new values

```c
// C/C++ - Output parameter
void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}
```

```lean
-- Lean4 - Return tuple
def swap (a b : Int) : Int × Int :=
  (b, a)
```

### Step 4: Ensure Type Correctness

Lean4's type system is strict. Address common type issues:

1. **Integer types:**
   - Use `Nat` for non-negative values (array indices, counts)
   - Use `Int` for potentially negative values
   - Convert explicitly: `n.toNat`, `n.toInt`

2. **Array bounds:**
   - Lean4 requires proof of valid indices
   - Use safe accessors: `arr.get?`, `arr[i]?`
   - Or use `arr[i]!` with runtime check

3. **Division:**
   - Natural number division: `n / m` (rounds down)
   - Integer division: use `Int.div`
   - Handle division by zero explicitly

4. **Type annotations:**
   - Add explicit types when inference fails
   - Use `: Type` for clarity

### Step 5: Test and Verify

Ensure the translated code works correctly:

1. **Compile check:**
   ```bash
   lake build
   ```

2. **Create test cases:**
   ```lean
   #eval add 2 3        -- Should output 5
   #eval factorial 5    -- Should output 120
   ```

3. **Compare outputs:**
   - Run original C/C++ program
   - Run translated Lean4 program
   - Verify outputs match for same inputs

4. **Handle edge cases:**
   - Empty arrays
   - Zero values
   - Negative numbers
   - Boundary conditions

### Step 6: Optimize and Refine

Improve the translated code:

1. **Use Lean4 idioms:**
   - Replace manual recursion with `List.foldl`, `Array.foldl`
   - Use pattern matching instead of nested if-else
   - Leverage standard library functions

2. **Add documentation:**
   ```lean
   /-- Calculate the sum of first n natural numbers -/
   def sum (n : Nat) : Nat :=
     n * (n + 1) / 2
   ```

3. **Consider performance:**
   - Use tail recursion for loops
   - Prefer `Array` over `List` for random access
   - Use `@[inline]` for small functions

## Common Translation Patterns

For detailed patterns, see [translation_patterns.md](references/translation_patterns.md).

### Quick Reference

| C/C++ | Lean4 |
|-------|-------|
| `int x` | `def x : Int` |
| `unsigned int x` | `def x : Nat` |
| `float x` | `def x : Float` |
| `bool x` | `def x : Bool` |
| `char* str` | `def str : String` |
| `int arr[]` | `def arr : Array Int` |
| `struct S` | `structure S where` |
| `for (...)` | `let rec loop ...` |
| `while (...)` | `let rec loop ...` |
| `if (...) {...}` | `if ... then ... else ...` |
| `switch (...)` | `match ... with` |
| `return x` | `x` (last expression) |
| `void f()` | `def f : IO Unit` |
| `printf(...)` | `IO.println ...` |

## Examples

### Example 1: Simple Algorithm

**C/C++ Input:**
```c
int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}
```

**Lean4 Output:**
```lean
def gcd (a b : Nat) : Nat :=
  if b = 0 then a
  else gcd b (a % b)
```

### Example 2: Array Processing

**C/C++ Input:**
```c
int findMax(int arr[], int size) {
    int max = arr[0];
    for (int i = 1; i < size; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    return max;
}
```

**Lean4 Output:**
```lean
def findMax (arr : Array Int) : Option Int :=
  if arr.isEmpty then
    none
  else
    some (arr.foldl max arr[0]!)
```

### Example 3: Struct with Methods

**C/C++ Input:**
```cpp
struct Rectangle {
    int width;
    int height;

    int area() {
        return width * height;
    }

    int perimeter() {
        return 2 * (width + height);
    }
};
```

**Lean4 Output:**
```lean
structure Rectangle where
  width : Nat
  height : Nat
  deriving Repr

def Rectangle.area (r : Rectangle) : Nat :=
  r.width * r.height

def Rectangle.perimeter (r : Rectangle) : Nat :=
  2 * (r.width + r.height)
```

### Example 4: I/O Program

**C/C++ Input:**
```c
#include <stdio.h>

int main() {
    int n;
    printf("Enter a number: ");
    scanf("%d", &n);
    printf("Factorial: %d\n", factorial(n));
    return 0;
}
```

**Lean4 Output:**
```lean
def factorial (n : Nat) : Nat :=
  if n <= 1 then 1
  else n * factorial (n - 1)

def main : IO Unit := do
  IO.print "Enter a number: "
  let input ← IO.getStdIn >>= (·.getLine)
  match input.trim.toNat? with
  | some n =>
    IO.println s!"Factorial: {factorial n}"
  | none =>
    IO.println "Invalid input"
```

## Best Practices

1. **Start simple:** Translate basic functions first, then build up complexity
2. **Preserve semantics:** Ensure the Lean4 code computes the same results
3. **Use types wisely:** Leverage Lean4's type system for correctness
4. **Embrace immutability:** Prefer pure functions over mutable state
5. **Test thoroughly:** Verify outputs match for various inputs
6. **Document assumptions:** Note any semantic differences or limitations
7. **Leverage standard library:** Use built-in functions when available
8. **Handle errors gracefully:** Use `Option` or `Except` for error cases

## Limitations and Considerations

1. **Undefined behavior:** C/C++ undefined behavior must be handled explicitly in Lean4
2. **Performance:** Functional code may have different performance characteristics
3. **Concurrency:** C/C++ threading requires different approaches in Lean4
4. **Low-level operations:** Bit manipulation and pointer arithmetic need careful translation
5. **External libraries:** C/C++ library calls may not have direct Lean4 equivalents
6. **Macros:** C preprocessor macros need manual translation
7. **Templates:** C++ templates translate to Lean4 generics differently

## Resources

- **Translation patterns:** See [translation_patterns.md](references/translation_patterns.md) for comprehensive pattern catalog
- **Lean4 documentation:** https://lean-lang.org/documentation/
- **Lean4 standard library:** https://github.com/leanprover/lean4/tree/master/src/Init
