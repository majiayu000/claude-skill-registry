---
name: acsl-annotation-assistant
description: Create ACSL (ANSI/ISO C Specification Language) formal annotations for C/C++ programs. Use this skill when working with formal verification, adding function contracts (requires/ensures), loop invariants, assertions, memory safety annotations, or any ACSL specifications. Supports Frama-C verification and generates comprehensive formal specifications for C/C++ code.
---

# ACSL Annotation Assistant

Generate comprehensive ACSL (ANSI/ISO C Specification Language) annotations for C/C++ programs to support formal verification with tools like Frama-C.

## Core Capabilities

### 1. Function Contracts

Add complete function specifications with preconditions and postconditions:

```c
/*@
  requires \valid(array + (0..n-1));
  requires n > 0;
  ensures \result >= 0 && \result < n;
  ensures \forall integer i; 0 <= i < n ==> array[\result] >= array[i];
  assigns \nothing;
*/
int find_max_index(int *array, int n);
```

### 2. Loop Annotations

Generate loop invariants, variants, and assigns clauses:

```c
/*@
  loop invariant 0 <= i <= n;
  loop invariant \forall integer k; 0 <= k < i ==> sum == \sum(0, k, array);
  loop assigns i, sum;
  loop variant n - i;
*/
for (i = 0; i < n; i++) {
    sum += array[i];
}
```

### 3. Memory Safety Specifications

Add pointer validity and separation annotations:

```c
/*@
  requires \valid(dest + (0..n-1));
  requires \valid_read(src + (0..n-1));
  requires \separated(dest + (0..n-1), src + (0..n-1));
  ensures \forall integer i; 0 <= i < n ==> dest[i] == \old(src[i]);
  assigns dest[0..n-1];
*/
void memcpy_safe(char *dest, const char *src, size_t n);
```

### 4. Assertions and Assumptions

Insert runtime and verification assertions:

```c
//@ assert 0 <= index && index < array_length;
//@ assume divisor != 0;
```

### 5. Axiomatic Definitions and Predicates

Define reusable logical predicates and axioms:

```c
/*@
  predicate sorted{L}(int *a, integer n) =
    \forall integer i, j; 0 <= i <= j < n ==> a[i] <= a[j];
*/

/*@
  axiomatic Sum {
    logic integer sum{L}(int *a, integer low, integer high);

    axiom sum_empty{L}:
      \forall int *a, integer i; sum(a, i, i) == 0;

    axiom sum_next{L}:
      \forall int *a, integer low, high;
        low < high ==> sum(a, low, high) == sum(a, low, high-1) + a[high-1];
  }
*/
```

## Annotation Workflow

### Step 1: Analyze the Function

Before annotating:
- Identify inputs, outputs, and side effects
- Determine memory access patterns
- Understand algorithmic properties (sorting, searching, etc.)
- Note any implicit assumptions

### Step 2: Add Function Contract

Start with the function-level specification:
1. **Preconditions** (`requires`): What must be true when function is called
2. **Postconditions** (`ensures`): What will be true when function returns
3. **Assigns clause**: What memory locations may be modified
4. **Behavioral specification**: Normal and exceptional behaviors if applicable

### Step 3: Annotate Loops

For each loop, specify:
1. **Loop invariant**: Properties that hold before and after each iteration
2. **Loop variant**: Decreasing measure proving termination
3. **Loop assigns**: Memory modified within the loop

### Step 4: Add Assertions

Insert intermediate assertions to:
- Document algorithmic properties
- Help verification tools
- Clarify complex logic

### Step 5: Define Helper Predicates

Create reusable logical definitions for:
- Common patterns (sorted arrays, valid ranges)
- Domain-specific properties
- Complex mathematical relationships

## Common ACSL Constructs

### Memory Validity
```c
\valid(ptr)                    // Single valid pointer
\valid(ptr + (low..high))      // Valid range
\valid_read(ptr)               // Read-only validity
\separated(ptr1, ptr2)         // No aliasing
```

### Quantifiers
```c
\forall type var; condition ==> property
\exists type var; condition && property
```

### Logic Functions
```c
\old(expr)                     // Value at function entry
\at(expr, Label)               // Value at specific point
\result                        // Function return value
\nothing                       // Empty set (for assigns)
```

### Integer Ranges
```c
\forall integer i; low <= i < high ==> array[i] >= 0
```

### Behaviors
```c
/*@
  behavior valid_input:
    assumes n > 0;
    requires \valid(array + (0..n-1));
    ensures \result >= 0;

  behavior invalid_input:
    assumes n <= 0;
    ensures \result == -1;

  complete behaviors;
  disjoint behaviors;
*/
```

## Verification Considerations

### For Frama-C WP Plugin

When generating annotations for WP verification:
- Use `assigns` clauses to specify frame conditions
- Prefer `\valid` over raw pointer checks
- Use `\separated` for pointer disjointness
- Add `loop assigns` for all loops
- Include `loop variant` for termination proofs

### Common Verification Patterns

**Array bounds safety:**
```c
/*@ requires 0 <= index < length;
    requires \valid(array + index);
*/
```

**Null pointer checks:**
```c
/*@ requires ptr != \null;
    requires \valid(ptr);
*/
```

**Overflow prevention:**
```c
/*@ requires INT_MIN <= a + b <= INT_MAX; */
```

## Output Format

Generate annotations in standard ACSL comment syntax:
- Multi-line contracts: `/*@ ... */`
- Single-line assertions: `//@ assertion`
- Place contracts immediately before function declarations
- Place loop annotations immediately before loop headers
- Include explanatory comments when annotations are complex

## Best Practices

1. **Start simple**: Begin with basic contracts, then refine
2. **Be precise**: Avoid over-specification or under-specification
3. **Document assumptions**: Make implicit assumptions explicit
4. **Use predicates**: Factor out common patterns
5. **Test incrementally**: Verify annotations with Frama-C as you go
6. **Include rationale**: Add comments explaining non-obvious specifications

## Example: Complete Annotated Function

```c
/*@
  predicate valid_array(int *a, integer n) =
    \valid(a + (0..n-1)) && n > 0;
*/

/*@
  requires valid_array(array, n);
  ensures \result >= 0 && \result < n;
  ensures \forall integer i; 0 <= i < n ==> array[\result] >= array[i];
  assigns \nothing;
*/
int find_max_index(int *array, int n) {
    int max_idx = 0;

    /*@
      loop invariant 0 <= i <= n;
      loop invariant 0 <= max_idx < n;
      loop invariant \forall integer k; 0 <= k < i ==>
                     array[max_idx] >= array[k];
      loop assigns i, max_idx;
      loop variant n - i;
    */
    for (int i = 1; i < n; i++) {
        if (array[i] > array[max_idx]) {
            max_idx = i;
        }
    }

    return max_idx;
}
```

## Resources

This skill includes reference materials for ACSL:

### references/

- `acsl_reference.md` - Comprehensive ACSL syntax reference
- `common_patterns.md` - Frequently used annotation patterns
- `frama_c_integration.md` - Tips for using with Frama-C

Load these references as needed for detailed syntax information or advanced patterns.
