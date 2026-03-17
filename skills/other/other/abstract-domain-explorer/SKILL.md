---
name: abstract-domain-explorer
description: Applies abstract interpretation using different abstract domains (intervals, octagons, polyhedra, sign, congruence) to statically analyze program variables and infer invariants, value ranges, and relationships. Use when analyzing program properties, inferring loop invariants, detecting potential errors, or understanding variable relationships through static analysis.
---

# Abstract Domain Explorer

## Overview

This skill applies abstract interpretation to statically analyze programs using various abstract domains. It infers invariants, value ranges, and relationships between variables without executing the code. Different domains offer different trade-offs between precision and efficiency.

## Analysis Workflow

Follow these steps to analyze programs with abstract domains:

### 1. Select Appropriate Domain(s)

**Choose based on analysis goals:**

**Interval Domain:**
- Use for: Range analysis, bounds checking, array indexing
- Precision: Low to medium
- Cost: Very efficient
- Example: Determine if x ∈ [0, 100]

**Sign Domain:**
- Use for: Sign analysis, division by zero detection
- Precision: Low
- Cost: Very efficient
- Example: Determine if x is positive, negative, or zero

**Congruence Domain:**
- Use for: Modular arithmetic, alignment analysis
- Precision: Medium (for specific patterns)
- Cost: Efficient
- Example: Determine if x ≡ 0 (mod 4)

**Octagon Domain:**
- Use for: Relational analysis, loop invariants with simple relationships
- Precision: Medium to high
- Cost: Moderate (O(n³) operations)
- Example: Infer x ≤ y + 5, x + y ≤ 10

**Polyhedra Domain:**
- Use for: Complex linear relationships, precise invariants
- Precision: High
- Cost: Expensive (exponential worst-case)
- Example: Infer 2x + 3y ≤ z + 10

**Reduced Product:**
- Use for: Combining strengths of multiple domains
- Precision: Higher than individual domains
- Cost: Sum of component costs
- Example: Intervals × Congruence for precise range with modular constraints

### 2. Initialize Abstract State

**Set initial values for program entry:**
- Constants: Exact values (e.g., x = 5 → x ∈ [5, 5])
- Inputs: Top element (e.g., user input → x ∈ [-∞, +∞])
- Uninitialized: Bottom element (unreachable)

**Example:**
```c
int x = 0;        // x ∈ [0, 0]
int y = input();  // y ∈ [-∞, +∞]
```

### 3. Apply Transfer Functions

**For each statement, compute abstract semantics:**

**Assignment (x = e):**
- Evaluate expression e in abstract domain
- Update abstract state for x

**Condition (assume c):**
- Refine abstract state based on condition
- Intersect with constraint

**Join (control flow merge):**
- Compute least upper bound of incoming states
- Used after if-else, at loop headers

**Example (Intervals):**
```c
x = y + 5;        // If y ∈ [a, b], then x ∈ [a+5, b+5]
assume(x > 10);   // If x ∈ [a, b], then x ∈ [max(a, 11), b]
```

### 4. Handle Loops with Widening

**For loops, apply widening to ensure termination:**

1. Compute first iteration
2. Compute second iteration
3. Apply widening operator (∇)
4. Check for convergence
5. Continue until fixpoint reached

**Example:**
```c
int x = 0;
while (x < 100) {
    x = x + 1;
}
```

- Iteration 0: x ∈ [0, 0]
- Iteration 1: x ∈ [0, 1]
- Widening: x ∈ [0, +∞]
- Refine with condition: x ∈ [0, 99] in loop
- Exit: x ∈ [100, 100]

### 5. Refine with Narrowing (Optional)

**Apply narrowing to improve precision:**
- Iterate a few more times (typically 1-3)
- Use narrowing operator (△)
- Refine over-approximations from widening

### 6. Extract Invariants

**Identify inferred properties:**
- Value ranges for each variable
- Relationships between variables
- Loop invariants
- Preconditions for safe operations

**Report format:**
- Variable: abstract value
- Invariants: logical formulas
- Safety properties: bounds checks, division by zero, etc.

## Analysis Examples

### Example 1: Range Analysis with Intervals

**Code:**
```c
int x = 0;
int y = 100;
while (x < 10) {
    x = x + 1;
    y = y - 1;
}
// What are the values of x and y here?
```

**Analysis (Interval Domain):**
- Entry: x ∈ [0, 0], y ∈ [100, 100]
- Loop iterations with widening:
  - Iter 0: x ∈ [0, 0], y ∈ [100, 100]
  - Iter 1: x ∈ [0, 1], y ∈ [99, 100]
  - Widening: x ∈ [0, +∞], y ∈ [-∞, 100]
  - Refine with x < 10: x ∈ [0, 9], y ∈ [-∞, 100]
- Narrowing: y ∈ [91, 100]
- Exit: x ∈ [10, 10], y ∈ [90, 90]

**Inferred Invariants:**
- Loop: x ∈ [0, 9], y ∈ [91, 100]
- Exit: x = 10, y = 90
- Implicit: x + y = 100 (not captured by intervals alone)

### Example 2: Relational Analysis with Octagons

**Code:**
```c
int x = 0;
int y = 0;
while (x < 10) {
    x = x + 1;
    y = y + 1;
}
```

**Analysis (Octagon Domain):**
- Entry: x = 0, y = 0, x - y = 0
- Loop iterations:
  - Maintains x - y = 0 throughout
  - x ∈ [0, 10], y ∈ [0, 10]
- Exit: x = 10, y = 10, x = y

**Inferred Invariants:**
- x = y (captured by octagon)
- x ∈ [0, 10], y ∈ [0, 10]

**Advantage over Intervals:**
Intervals would only infer x ∈ [0, 10], y ∈ [0, 10] but miss the relationship x = y.

### Example 3: Linear Relationships with Polyhedra

**Code:**
```c
int x = 0, y = 0, z = 0;
while (x < 10) {
    x = x + 1;
    y = y + 2;
    z = x + y;
}
```

**Analysis (Polyhedra Domain):**
- Entry: x = 0, y = 0, z = 0
- Loop iterations:
  - Infers: y = 2x, z = x + y, z = 3x
  - x ∈ [0, 10]
- Exit: x = 10, y = 20, z = 30

**Inferred Invariants:**
- y = 2x
- z = x + y
- z = 3x
- x ∈ [0, 10]

**Advantage over Octagons:**
Polyhedra can express y = 2x, which octagons cannot.

### Example 4: Modular Arithmetic with Congruence

**Code:**
```c
int sum = 0;
for (int i = 0; i < 100; i++) {
    sum = sum + 3;
}
```

**Analysis (Congruence Domain):**
- Entry: sum ≡ 0 (mod 3), i ≡ 0 (mod 1)
- Loop: sum ≡ 0 (mod 3) maintained
- Exit: sum ≡ 0 (mod 3)

**Analysis (Interval Domain):**
- Exit: sum ∈ [0, 300]

**Combined (Reduced Product):**
- sum ∈ [0, 300] and sum ≡ 0 (mod 3)
- Refined: sum ∈ {0, 3, 6, 9, ..., 297, 300}
- Exact: sum = 300

**Inferred Invariants:**
- sum is always divisible by 3
- sum ∈ [0, 300]

### Example 5: Division by Zero Detection with Sign

**Code:**
```c
int x = read_input();
int y = x * x;
int z = 100 / y;  // Safe?
```

**Analysis (Sign Domain):**
- x: ⊤ (unknown sign)
- y = x * x: ≥0 (non-negative)
- Problem: y could be 0 if x = 0
- Division 100 / y: **potential division by zero**

**Analysis (Interval Domain):**
- x: [-∞, +∞]
- y: [0, +∞]
- Problem: 0 ∈ [0, +∞]
- Division 100 / y: **potential division by zero**

**Inferred Property:**
- Unsafe: Division by zero possible when x = 0

### Example 6: Array Bounds Checking

**Code:**
```c
int arr[10];
int i = 0;
while (i < 10) {
    arr[i] = 0;  // Safe?
    i = i + 1;
}
```

**Analysis (Interval Domain):**
- Loop: i ∈ [0, 9]
- Array access: arr[i] where i ∈ [0, 9]
- Array bounds: [0, 9]
- **Safe:** i always within bounds

**Inferred Property:**
- No array bounds violation

### Example 7: Nested Loops with Octagons

**Code:**
```c
int i = 0, j = 0;
while (i < 10) {
    j = 0;
    while (j < i) {
        j = j + 1;
    }
    i = i + 1;
}
```

**Analysis (Octagon Domain):**
- Outer loop: i ∈ [0, 10]
- Inner loop: j ∈ [0, i], j ≤ i
- Exit: i = 10, j = 9, j ≤ i

**Inferred Invariants:**
- j ≤ i (relational invariant)
- i ∈ [0, 10]
- j ∈ [0, 9]

## Domain Comparison

| Domain | Precision | Cost | Relationships | Best For |
|--------|-----------|------|---------------|----------|
| Sign | Very Low | O(1) | None | Sign errors, division by zero |
| Interval | Low-Medium | O(1) | None | Range analysis, bounds checking |
| Congruence | Medium | O(1) | None | Modular patterns, alignment |
| Octagon | Medium-High | O(n³) | ±x ± y ≤ c | Simple relational invariants |
| Polyhedra | High | Exponential | Linear | Complex linear relationships |
| Reduced Product | Higher | Sum of components | Combined | Precise analysis with multiple aspects |

## Choosing the Right Domain

**Start with Intervals if:**
- You need range information
- Efficiency is critical
- No relationships needed

**Use Octagons if:**
- You need simple relationships (x ≤ y + c)
- Loop invariants involve variable pairs
- Moderate cost acceptable

**Use Polyhedra if:**
- Complex linear relationships needed
- Precision is critical
- Small programs or specific code sections
- Cost is acceptable

**Use Reduced Products if:**
- Multiple aspects needed (range + modular)
- Willing to pay combined cost
- Need precision from multiple domains

**Use Sign if:**
- Only sign information needed
- Very large programs
- Quick analysis required

**Use Congruence if:**
- Modular arithmetic patterns
- Alignment analysis
- Complement to intervals

## Constraints

**MUST:**
- Select appropriate domain(s) for analysis goals
- Apply transfer functions correctly
- Use widening for loops to ensure termination
- Report inferred invariants clearly
- Indicate precision limitations of chosen domain

**MUST NOT:**
- Claim exact values when domain gives approximations
- Ignore widening (may not terminate)
- Use expensive domains unnecessarily
- Report unsound results

## Resources

### references/abstract_domains.md
Comprehensive reference covering:
- Abstract interpretation fundamentals
- Detailed domain specifications (intervals, octagons, polyhedra, sign, congruence)
- Domain operations and transfer functions
- Widening and narrowing techniques
- Reduced product domains
- Fixpoint computation
- Complete analysis examples

