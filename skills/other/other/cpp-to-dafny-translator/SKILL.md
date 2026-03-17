---
name: cpp-to-dafny-translator
description: Translate C/C++ programs to equivalent Dafny code while preserving semantics and ensuring verification. Use when users ask to convert, translate, or port C/C++ code to Dafny, or when they need to formally verify C/C++ algorithms using Dafny's verification capabilities. Handles functions, structs, pointers, arrays, memory management, and ensures the generated Dafny code is well-typed, executable, verifiable, and can successfully run.
---

# C/C++ to Dafny Translator

Translate C/C++ programs into equivalent, verifiable Dafny code while preserving program semantics and ensuring memory safety.

## Overview

This skill provides systematic guidance for translating C/C++ code to Dafny, handling memory management, pointer semantics, type conversions, and ensuring well-typed, verifiable output with appropriate specifications.

## Translation Workflow

```
C/C++ Input → Analyze Structure → Map Types & Memory → Translate → Add Specifications → Verify
    ├─ Identify types, pointers, memory patterns
    ├─ Map C/C++ constructs to Dafny equivalents
    ├─ Handle memory safety and ownership
    ├─ Add preconditions, postconditions, invariants
    └─ Validate executability and verification
```

## Core Translation Principles

### 1. Memory Safety First

Dafny enforces memory safety. Every translation must:
- Replace raw pointers with safe references or arrays
- Make memory bounds explicit
- Ensure no null pointer dereferences
- Handle dynamic memory with sequences or arrays

### 2. Preserve Semantics

The translated code must maintain the same computational behavior, preserve function contracts, keep algorithmic complexity, and handle all edge cases including error conditions.

### 3. Enable Verification

Generated Dafny code must include specifications (preconditions, postconditions, invariants), be verifiable by Dafny's verifier, compile and execute correctly, and follow Dafny idioms.

## Type Mapping Reference

### Basic Types

| C/C++ Type | Dafny Type | Notes |
|-----------|-----------|-------|
| `int`, `long` | `int` | Unbounded integers in Dafny |
| `unsigned int` | `nat` | Natural numbers (≥ 0) |
| `char` | `char` | Single character |
| `bool` | `bool` | Direct mapping |
| `float`, `double` | `real` | Exact rationals in Dafny |
| `void` | `()` | Unit type |
| `NULL` | Use `Option` or bounds checks | No null pointers |

### Composite Types

| C/C++ Type | Dafny Type | Notes |
|-----------|-----------|-------|
| `int arr[]` | `array<int>` | Fixed-size arrays |
| `int* ptr` | `array<int>` or `seq<int>` | Depends on usage |
| `struct` | `class` or `datatype` | Mutable vs immutable |
| `enum` | `datatype` | Algebraic data types |
| `union` | `datatype` with variants | Tagged unions |

For detailed mappings, see [references/type_mappings.md](references/type_mappings.md).

## Translation Patterns

### Functions

**Simple C function:**
```c
int add(int a, int b) {
    return a + b;
}
```

**Dafny:**
```dafny
function add(a: int, b: int): int
{
    a + b
}
```

**Function with side effects:**
```c
void increment(int* x) {
    (*x)++;
}
```

**Dafny (using method):**
```dafny
method increment(x: array<int>, index: nat)
    requires index < x.Length
    modifies x
    ensures x[index] == old(x[index]) + 1
{
    x[index] := x[index] + 1;
}
```

### Pointers and Arrays

**C array access:**
```c
int sum_array(int* arr, int n) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += arr[i];
    }
    return sum;
}
```

**Dafny:**
```dafny
method sumArray(arr: array<int>) returns (sum: int)
    ensures sum == arraySum(arr[..])
{
    sum := 0;
    var i := 0;
    while i < arr.Length
        invariant 0 <= i <= arr.Length
        invariant sum == arraySum(arr[..i])
    {
        sum := sum + arr[i];
        i := i + 1;
    }
}

function arraySum(s: seq<int>): int
{
    if |s| == 0 then 0 else s[0] + arraySum(s[1..])
}
```

### Structs and Classes

**C struct:**
```c
struct Point {
    int x;
    int y;
};

int distance_squared(struct Point* p) {
    return p->x * p->x + p->y * p->y;
}
```

**Dafny:**
```dafny
class Point {
    var x: int
    var y: int

    constructor(x0: int, y0: int)
        ensures x == x0 && y == y0
    {
        x := x0;
        y := y0;
    }
}

function distanceSquared(p: Point): int
    reads p
{
    p.x * p.x + p.y * p.y
}
```

### Control Flow

**If-else:**
```c
int max(int a, int b) {
    if (a > b) return a;
    else return b;
}
```

**Dafny:**
```dafny
function max(a: int, b: int): int
{
    if a > b then a else b
}
```

**Loops with invariants:**
```c
int factorial(int n) {
    int result = 1;
    for (int i = 1; i <= n; i++) {
        result *= i;
    }
    return result;
}
```

**Dafny:**
```dafny
method factorial(n: nat) returns (result: nat)
    ensures result == fact(n)
{
    result := 1;
    var i := 1;
    while i <= n
        invariant 1 <= i <= n + 1
        invariant result == fact(i - 1)
    {
        result := result * i;
        i := i + 1;
    }
}

function fact(n: nat): nat
{
    if n == 0 then 1 else n * fact(n - 1)
}
```

## Handling Common Challenges

### 1. Pointer Arithmetic

**Challenge:** C allows pointer arithmetic; Dafny doesn't.

**Solution:** Use array indices instead:
```c
// C
int* ptr = arr + 5;
*ptr = 10;
```

```dafny
// Dafny
arr[5] := 10;
```

### 2. Dynamic Memory Allocation

**Challenge:** C uses malloc/free; Dafny has automatic memory management.

**Solution:** Use arrays or sequences:
```c
// C
int* arr = (int*)malloc(n * sizeof(int));
// ... use arr ...
free(arr);
```

```dafny
// Dafny
var arr := new int[n];
// ... use arr ...
// No explicit free needed
```

### 3. Null Pointers

**Challenge:** C allows NULL; Dafny doesn't have null references.

**Solution:** Use Option types or ensure non-null:
```c
// C
int* find(int* arr, int n, int target) {
    for (int i = 0; i < n; i++) {
        if (arr[i] == target) return &arr[i];
    }
    return NULL;
}
```

```dafny
// Dafny
method find(arr: array<int>, target: int) returns (index: int)
    ensures index == -1 || (0 <= index < arr.Length && arr[index] == target)
{
    var i := 0;
    while i < arr.Length
        invariant 0 <= i <= arr.Length
    {
        if arr[i] == target {
            return i;
        }
        i := i + 1;
    }
    return -1;
}
```

### 4. Mutable vs Immutable

**Challenge:** C has mutable everything; Dafny distinguishes functions (pure) from methods (with side effects).

**Solution:**
- Use `function` for pure computations
- Use `method` for operations with side effects
- Add `reads` clauses for functions that read object fields
- Add `modifies` clauses for methods that modify state

### 5. Verification Annotations

**Challenge:** Dafny requires specifications for verification.

**Solution:** Add preconditions, postconditions, and loop invariants:
```dafny
method binarySearch(arr: array<int>, target: int) returns (index: int)
    requires forall i, j :: 0 <= i < j < arr.Length ==> arr[i] <= arr[j]  // sorted
    ensures index == -1 || (0 <= index < arr.Length && arr[index] == target)
{
    var low := 0;
    var high := arr.Length;
    while low < high
        invariant 0 <= low <= high <= arr.Length
        invariant forall i :: 0 <= i < low ==> arr[i] < target
        invariant forall i :: high <= i < arr.Length ==> arr[i] > target
    {
        var mid := (low + high) / 2;
        if arr[mid] < target {
            low := mid + 1;
        } else if arr[mid] > target {
            high := mid;
        } else {
            return mid;
        }
    }
    return -1;
}
```

## Translation Process

### Step 1: Analyze C/C++ Code

Identify all functions, structs, and global variables. Analyze pointer usage and memory patterns. Identify side effects and state modifications. Note any unsafe operations.

### Step 2: Plan Type and Memory Mappings

Map C/C++ types to Dafny types. Decide how to handle pointers (arrays, sequences, or references). Plan struct translations (class vs datatype). Identify what needs specifications.

### Step 3: Translate Constructs

Start with data structures (structs → classes/datatypes). Translate pure functions first. Convert functions with side effects to methods. Add memory safety checks. Include necessary specifications.

### Step 4: Add Verification Annotations

Add preconditions (`requires`). Add postconditions (`ensures`). Add loop invariants. Add frame conditions (`reads`, `modifies`). Add termination measures (`decreases`).

### Step 5: Verify and Test

Run Dafny verifier. Fix verification errors. Test with concrete examples. Ensure executability.

## Example Translation

**C code:**
```c
int is_sorted(int* arr, int n) {
    for (int i = 0; i < n - 1; i++) {
        if (arr[i] > arr[i + 1]) {
            return 0;
        }
    }
    return 1;
}

void bubble_sort(int* arr, int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}
```

**Dafny:**
```dafny
predicate isSorted(arr: array<int>)
    reads arr
{
    forall i, j :: 0 <= i < j < arr.Length ==> arr[i] <= arr[j]
}

method bubbleSort(arr: array<int>)
    modifies arr
    ensures isSorted(arr)
    ensures multiset(arr[..]) == multiset(old(arr[..]))
{
    var i := 0;
    while i < arr.Length - 1
        invariant 0 <= i <= arr.Length
        invariant forall k, l :: 0 <= k < i <= l < arr.Length ==> arr[k] <= arr[l]
        invariant multiset(arr[..]) == multiset(old(arr[..]))
    {
        var j := 0;
        while j < arr.Length - i - 1
            invariant 0 <= j <= arr.Length - i - 1
            invariant forall k :: 0 <= k < j ==> arr[k] <= arr[j]
            invariant multiset(arr[..]) == multiset(old(arr[..]))
        {
            if arr[j] > arr[j + 1] {
                arr[j], arr[j + 1] := arr[j + 1], arr[j];
            }
            j := j + 1;
        }
        i := i + 1;
    }
}
```

## Best Practices

1. **Start with Pure Functions**: Translate side-effect-free code first
2. **Add Specifications Incrementally**: Start with simple contracts, refine as needed
3. **Use Helper Functions**: Define pure functions to express properties
4. **Leverage Dafny's Verifier**: Let the verifier guide you to correct specifications
5. **Test Executability**: Use `Main` methods to test concrete examples
6. **Document Assumptions**: Note where C semantics differ from Dafny
7. **Handle Memory Explicitly**: Make all memory bounds and ownership clear

## Verification Checklist

Before finalizing translation:

- [ ] All types are correctly mapped
- [ ] Code compiles without errors
- [ ] Dafny verifier succeeds
- [ ] Preconditions capture all assumptions
- [ ] Postconditions specify all guarantees
- [ ] Loop invariants are sufficient for verification
- [ ] Memory safety is ensured (no out-of-bounds access)
- [ ] Termination is proven (decreases clauses if needed)
- [ ] Code is executable and produces correct results

## Additional Resources

For complex translations, refer to:
- [Type Mappings](references/type_mappings.md) - Comprehensive C/C++ to Dafny type guide
- [Memory Patterns](references/memory_patterns.md) - Handling pointers, arrays, and dynamic memory
- [Verification Guide](references/verification_guide.md) - Writing effective specifications
