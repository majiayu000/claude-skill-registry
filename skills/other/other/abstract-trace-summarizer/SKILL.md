---
name: abstract-trace-summarizer
description: Performs abstract interpretation to produce summarized execution traces and high-level program behavior representations. Highlights key control flow paths, variable relationships, loop invariants, function summaries, and potential runtime states using abstract domains (intervals, signs, nullness, etc.). Use when analyzing program behavior, understanding execution paths, computing loop invariants, tracking variable ranges, detecting potential runtime errors, or generating program summaries without concrete execution.
---

# Abstract Trace Summarizer

## Overview

This skill performs abstract interpretation to analyze program behavior and produce summarized execution traces. It computes over-approximations of possible runtime states, tracks control flow paths, infers variable relationships, and generates high-level behavioral summaries without requiring concrete program execution.

## Core Workflow

### 1. Program Analysis Setup

**Initial Assessment:**
- Identify programming language and paradigm
- Determine analysis scope (function, module, program)
- Select appropriate abstract domains
- Identify analysis goals (safety, correctness, optimization)

**Abstract Domain Selection:**

Choose domains based on analysis needs:

**Numerical domains:**
- **Intervals**: Track value ranges `[min, max]`
- **Signs**: Track {negative, zero, positive, unknown}
- **Octagons**: Linear constraints `±x ±y ≤ c`
- **Polyhedra**: General linear constraints

**Non-numerical domains:**
- **Nullness**: Track {null, non-null, unknown} for pointers
- **Constant propagation**: Track known constant values
- **Type domains**: Track possible types
- **Parity**: Track {even, odd, unknown}

**Relational vs non-relational:**
- **Non-relational**: Track variables independently (faster, less precise)
- **Relational**: Track relationships between variables (slower, more precise)

### 2. Control Flow Analysis

**Build Control Flow Graph (CFG):**

Represent program structure:
```
Entry → Statement₁ → Statement₂ → ... → Exit
         ↓ (branch)
       Statement₃ → ...
```

**Identify key structures:**
- **Sequential**: Straight-line code
- **Conditional**: if-then-else branches
- **Loops**: while, for, do-while
- **Function calls**: Call/return edges
- **Exception handling**: try-catch-finally

**Path analysis:**
- **Path-sensitive**: Track separate states per path (more precise)
- **Path-insensitive**: Merge states at join points (more efficient)
- **Trace partitioning**: Hybrid approach based on key predicates

### 3. Abstract State Computation

**Transfer Functions:**

Model how statements affect abstract states:

**Assignment: `x = expr`**
```
1. Evaluate expr in current abstract state
2. Update abstract state for variable x
3. Propagate to successor states
```

**Conditional: `if (condition)`**
```
1. Evaluate condition in current abstract state
2. Refine state for true branch (assume condition holds)
3. Refine state for false branch (assume condition doesn't hold)
4. Analyze both branches separately
```

**Loop: `while (condition)`**
```
1. Compute fixpoint at loop head using widening
2. Analyze loop body with refined state
3. Optionally apply narrowing for precision
4. Extract loop invariant from fixpoint
```

**Function call: `y = f(x)`**
```
1. Look up or compute function summary
2. Apply preconditions to arguments
3. Update state with postconditions
4. Handle side effects
```

**Lattice Operations:**

**Join (∪)**: Merge states from different paths
```
Example: [1,5] ∪ [3,8] = [1,8]
Use: At control flow merge points
```

**Meet (∩)**: Refine state with constraints
```
Example: [1,10] ∩ [5,15] = [5,10]
Use: When adding constraints from conditions
```

**Widening (∇)**: Accelerate convergence for loops
```
Example: [0,n] ∇ [0,n+1] = [0,+∞]
Use: At loop heads to ensure termination
```

**Narrowing (△)**: Refine widened results
```
Example: [0,+∞] △ [0,100] = [0,100]
Use: After widening to improve precision
```

### 4. Variable Relationship Tracking

**Data Dependencies:**

Track how variables affect each other:
- **Def-use chains**: Where variables are defined and used
- **Use-def chains**: Which definitions reach each use
- **Dependency graph**: Variable dependency relationships

**Relational Constraints:**

For relational domains, track constraints:
```
Intervals: x ∈ [0,10], y ∈ [5,15]
Octagons: x - y ≤ 5, x + y ≤ 20
Polyhedra: 2x + 3y ≤ 30, x - y ≥ 0
```

**Equality Tracking:**
```
After x = y: track that x and y have equal values
After x = y + 1: track that x = y + 1
```

### 5. Loop Invariant Inference

**Fixpoint Computation:**

```
1. Initialize loop head state
2. Analyze loop body
3. Compute join of entry state and back-edge state
4. Apply widening if not converged
5. Repeat until fixpoint reached
6. Optionally apply narrowing
```

**Loop Invariant:**

Properties that hold at loop head:
```
Example: for i in range(n):
  Invariant: 0 ≤ i < n
```

**Loop Bounds:**

Estimate iteration counts:
- **Constant bounds**: `for i in range(10)` → 10 iterations
- **Symbolic bounds**: `for i in range(n)` → n iterations
- **Unbounded**: `while condition` → unknown iterations

**Loop Effects:**

Summarize loop behavior:
- Which variables are modified
- How values change per iteration
- Accumulated effects over all iterations

### 6. Function Summarization

**Compute Function Summaries:**

**Preconditions**: Required input states
```
Example: def divide(a, b)
  Precondition: b ≠ 0
```

**Postconditions**: Guaranteed output states
```
Example: def abs(x)
  Postcondition: result ≥ 0
```

**Side effects**: Modifications to global state
```
Example: def append(list, item)
  Side effect: list length increases by 1
```

**Frame conditions**: What remains unchanged
```
Example: def get_first(list)
  Frame: list is not modified
```

**Modular Analysis:**

Analyze functions separately:
1. Compute summary for each function
2. Reuse summaries at call sites
3. Handle recursion with fixpoint computation

### 7. Trace Summarization

**Generate High-Level Summary:**

**Execution paths:**
```
Path 1: Entry → L1 → L2 → L5 → Exit
  Condition: x > 0
  Result: returns positive value

Path 2: Entry → L1 → L3 → L4 → Exit
  Condition: x ≤ 0
  Result: returns zero or negative value
```

**Key control flow:**
```
- 3 conditional branches
- 2 loops (nested)
- 5 function calls
- 1 exception handler
```

**Variable states:**
```
Entry: x ∈ ℤ, y ∈ ℤ
Exit: result ∈ [0, +∞]
Invariant: x + y ≤ 100
```

**Potential runtime states:**
```
Normal termination: 85% of paths
Exception thrown: 15% of paths
Infinite loop: Not possible (proven)
```

## Output Format

Structure the abstract trace summary as follows:

```markdown
## Program Summary
- **Language**: [Programming language]
- **Scope**: [Function/Module/Program name]
- **Analysis Type**: [Abstract domain(s) used]

## Control Flow Structure
- **Total paths**: [Number of execution paths]
- **Loops**: [Number and nesting depth]
- **Conditionals**: [Number of branches]
- **Function calls**: [Number of calls]

## Abstract States

### Entry State
[Initial abstract state for variables]

### Key Program Points
**Location L1**: [Statement or label]
```
[Abstract state at this point]
```

**Location L2**: [Statement or label]
```
[Abstract state at this point]
```

### Exit State
[Final abstract state for variables]

## Variable Relationships
[Tracked relationships and constraints between variables]

## Loop Invariants
**Loop at L[X]**:
- **Invariant**: [Properties that hold at loop head]
- **Bound**: [Iteration count estimate]
- **Effect**: [How loop modifies state]

## Function Summaries
**Function [name]**:
- **Precondition**: [Required input conditions]
- **Postcondition**: [Guaranteed output conditions]
- **Side effects**: [Modifications to global state]
- **Complexity**: [Time/space complexity]

## Execution Paths

### Path 1: [Description]
**Condition**: [Path condition]
**Trace**: [Sequence of program points]
**Result**: [Final state or return value]

### Path 2: [Description]
**Condition**: [Path condition]
**Trace**: [Sequence of program points]
**Result**: [Final state or return value]

## Potential Runtime Behaviors
- **Normal termination**: [Conditions and states]
- **Exceptions**: [Possible exceptions and conditions]
- **Non-termination**: [Infinite loops or recursion]
- **Resource usage**: [Memory, time estimates]

## Safety Properties
- **Buffer safety**: [Array bounds checking results]
- **Null safety**: [Null pointer dereference analysis]
- **Type safety**: [Type correctness analysis]
- **Arithmetic safety**: [Overflow/underflow analysis]

## Recommendations
[Suggestions for improving code based on analysis]
```

## Analysis Techniques by Language

### Python
- **Type inference**: Track possible types for dynamic variables
- **Exception flow**: Model try-except-finally blocks
- **List operations**: Track list lengths and element types
- **Dictionary operations**: Track key-value relationships

### Java/C#
- **Null analysis**: Track nullness for object references
- **Type hierarchy**: Use class hierarchy for precision
- **Exception handling**: Model checked and unchecked exceptions
- **Concurrency**: Analyze thread interleavings and synchronization

### C/C++
- **Pointer analysis**: Track points-to relationships
- **Buffer bounds**: Analyze array and buffer accesses
- **Memory safety**: Detect use-after-free, double-free
- **Undefined behavior**: Identify potential UB

### JavaScript
- **Type coercion**: Model implicit type conversions
- **Prototype chain**: Track prototype relationships
- **Async operations**: Model promises and callbacks
- **Dynamic properties**: Track object property additions

## Common Analysis Patterns

### Pattern 1: Simple Loop Analysis

```python
# Code
for i in range(n):
    sum += arr[i]

# Analysis
Entry: sum = 0, i = ⊤, n ∈ [0,+∞]
Loop head: sum ∈ [0,+∞], i ∈ [0,n-1]
Loop invariant: 0 ≤ i < n, sum ≥ 0
Exit: sum ∈ [0,+∞], i = n
```

### Pattern 2: Conditional Branch Analysis

```python
# Code
if x > 0:
    result = x
else:
    result = -x

# Analysis
Entry: x ∈ ℤ
Branch 1 (x > 0): x ∈ [1,+∞], result = x ∈ [1,+∞]
Branch 2 (x ≤ 0): x ∈ [-∞,0], result = -x ∈ [0,+∞]
Join: result ∈ [0,+∞]
```

### Pattern 3: Null Safety Analysis

```java
// Code
if (obj != null) {
    return obj.getValue();
}
return -1;

// Analysis
Entry: obj ∈ {null, non-null, ⊤}
Branch 1 (obj != null): obj = non-null, access SAFE
Branch 2 (obj == null): obj = null, no dereference
Result: No null pointer dereference possible
```

### Pattern 4: Array Bounds Analysis

```python
# Code
for i in range(len(arr)):
    arr[i] = 0

# Analysis
Entry: arr has length L ∈ [0,+∞]
Loop: i ∈ [0, L-1]
Access: arr[i] where i ∈ [0, L-1] ⊆ [0, L-1]
Result: All accesses are safe
```

## Precision vs Performance Trade-offs

### High Precision (Slower)
- Path-sensitive analysis
- Relational domains (polyhedra, octagons)
- Context-sensitive function analysis
- Narrowing after widening

**Use when:**
- Proving critical safety properties
- Small code regions
- High assurance requirements

### Balanced Precision
- Trace partitioning
- Interval domain with some relations
- Summary-based function analysis
- Widening without narrowing

**Use when:**
- General program analysis
- Medium-sized programs
- Balance between precision and cost

### High Performance (Less Precise)
- Path-insensitive analysis
- Non-relational domains (intervals, signs)
- Context-insensitive function analysis
- Aggressive widening

**Use when:**
- Large codebases
- Quick feedback needed
- Scalability is priority

## Important Guidelines

### DO:
- ✅ Select appropriate abstract domains for the analysis goal
- ✅ Clearly document assumptions and approximations
- ✅ Explain loop invariants and their significance
- ✅ Highlight potential safety issues or runtime errors
- ✅ Provide concrete examples when explaining abstract states
- ✅ Show both over-approximation and under-approximation when relevant
- ✅ Explain fixpoint computation for loops
- ✅ Track variable relationships when using relational domains

### DON'T:
- ❌ Claim absolute certainty (abstract interpretation is approximate)
- ❌ Ignore infeasible paths without noting them
- ❌ Use overly complex domains when simpler ones suffice
- ❌ Forget to apply widening at loop heads (may not terminate)
- ❌ Present abstract states without explaining their meaning
- ❌ Ignore language-specific features (exceptions, concurrency)
- ❌ Overlook function summaries for modular analysis

## Resources

### references/abstract_interpretation.md
Comprehensive guide to abstract interpretation concepts including abstract domains, lattice operations, transfer functions, control flow analysis, variable relationship tracking, runtime state abstraction, trace summarization techniques, and precision vs performance trade-offs.

### references/examples.md
Complete examples of abstract trace summarization for various program patterns including simple loops, conditional branches, nested loops, pointer analysis, exception flow, recursive functions, concurrent programs, array bounds checking, string analysis, and state machines.
