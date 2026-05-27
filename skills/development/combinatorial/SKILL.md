---
name: combinatorial
description: |
    Use when solving problems involving permutations, combinations, backtracking, branch and bound, subset generation, and constraint satisfaction. Covers N-Queens, Sudoku solving, generating functions, and pruning strategies. Based on Knuth's TAOCP Vol. 4A.
    USE FOR: permutation and combination generation, backtracking algorithm design, constraint satisfaction problems, branch and bound optimization, subset enumeration, pruning strategy selection
    DO NOT USE FOR: graph traversal (use graph-algorithms), optimization with overlapping subproblems (use dynamic-programming)
license: MIT
metadata:
  displayName: "Combinatorial Algorithms"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "The Art of Computer Programming, Vol. 4A: Combinatorial Algorithms — Donald Knuth"
    url: "https://www-cs-faculty.stanford.edu/~knuth/taocp.html"
  - title: "Combinatorial Optimization — Wikipedia"
    url: "https://en.wikipedia.org/wiki/Combinatorial_optimization"
---

# Combinatorial Algorithms

## Overview
Combinatorial algorithms deal with counting, generating, and optimizing discrete structures -- permutations, combinations, subsets, partitions, and arrangements subject to constraints. Knuth devoted *The Art of Computer Programming, Volume 4A: Combinatorial Algorithms, Part 1* entirely to this topic, calling combinatorics "the mathematics of choice." This skill covers the core techniques for systematic enumeration, backtracking search, and constraint satisfaction.

## Fundamental Counting

### Permutations
An ordered arrangement of n elements. The number of permutations of n distinct elements is n! (n factorial).

- **All permutations of n elements**: n!
- **k-permutations of n elements** (ordered selection of k from n): n! / (n - k)!
- **Permutations with repetition**: n! / (n1! * n2! * ... * nk!) where ni is the count of each repeated element.

### Combinations
An unordered selection of k elements from n. The number of combinations is C(n, k) = n! / (k! * (n - k)!).

- **With repetition** (multiset coefficient): C(n + k - 1, k)

### Subsets
The power set of a set with n elements has 2^n subsets. Each element is either included or excluded.

## Backtracking

Backtracking is a systematic method for generating all (or some) possible configurations of a search space by incrementally building candidates and abandoning a candidate ("backtracking") as soon as it is determined that it cannot lead to a valid solution.

### Backtracking Template

```
BACKTRACK(state, choices):
    if state is a complete solution:
        process(state)
        return
    for each choice in choices:
        if is_valid(state, choice):       // pruning check
            apply(state, choice)
            BACKTRACK(state, remaining_choices)
            undo(state, choice)           // backtrack
```

**Key elements**:
1. **State**: The current partial solution being built.
2. **Choices**: The decisions available at each step.
3. **Constraints**: Rules that determine whether a partial solution is valid.
4. **Goal**: The condition that identifies a complete solution.

### Time Complexity
Backtracking explores a search tree. Without pruning, the worst case is O(b^d) where b is the branching factor and d is the depth. Effective pruning can dramatically reduce this in practice.

## Classic Backtracking Problems

### N-Queens
Place n queens on an n x n chessboard so that no two queens threaten each other (no shared row, column, or diagonal).

- **Approach**: Place queens one row at a time. For each row, try each column; prune if the column or either diagonal is already attacked.
- **State**: Positions of queens placed so far.
- **Pruning**: Track occupied columns and diagonals with sets or arrays.
- **Solutions**: 1 for n=1, 0 for n=2 and n=3, 2 for n=4, 10 for n=5, 92 for n=8.

### Sudoku Solving
Fill a 9x9 grid so that each row, column, and 3x3 box contains digits 1-9 exactly once.

- **Approach**: Find the next empty cell, try each digit 1-9, prune if the digit violates row/column/box constraints.
- **State**: The partially filled grid.
- **Pruning**: Check row, column, and box constraints before placing each digit. Advanced: propagate constraints (naked singles, hidden singles) to reduce the search space before branching.

### Subset Sum
Determine whether a subset of a given set sums to a target value.

- **Approach**: For each element, decide to include or exclude it. Prune branches where the running sum already exceeds the target (for positive numbers) or where the remaining elements cannot possibly reach the target.

## Branch and Bound

Branch and bound is an enhancement of backtracking for optimization problems. It maintains a bound (upper or lower, depending on minimization vs maximization) and prunes branches that cannot improve upon the best solution found so far.

### Framework

```
BRANCH_AND_BOUND(state):
    if state is a complete solution:
        update best_solution if state is better
        return
    if bound(state) cannot improve on best_solution:
        return  // prune
    for each choice in choices:
        apply(state, choice)
        BRANCH_AND_BOUND(state)
        undo(state, choice)
```

**Key elements**:
1. **Bounding function**: A fast estimate of the best possible solution achievable from the current state.
2. **Pruning**: Skip entire subtrees when the bound proves they cannot contain a better solution.

**Applications**: Traveling Salesman Problem, Integer Linear Programming, Job Scheduling, Knapsack (branch and bound variant).

## Subset Generation

### Iterative (Bitmask) Approach
Generate all 2^n subsets by iterating from 0 to 2^n - 1, where each bit indicates inclusion/exclusion.

```
GENERATE_SUBSETS(S):
    n = |S|
    for mask = 0 to 2^n - 1:
        subset = {S[i] for each bit i set in mask}
        process(subset)
```

### Recursive Approach
For each element, recursively generate subsets that include it and subsets that exclude it.

```
SUBSETS(S, index, current):
    if index == |S|:
        process(current)
        return
    SUBSETS(S, index + 1, current)              // exclude S[index]
    SUBSETS(S, index + 1, current + {S[index]}) // include S[index]
```

## Constraint Satisfaction Problems (CSP)

A CSP is defined by:
- **Variables**: The unknowns to be assigned values.
- **Domains**: The possible values for each variable.
- **Constraints**: Rules restricting which combinations of values are valid.

### Solving Strategies

| Strategy | Description |
|----------|-------------|
| **Backtracking search** | Assign variables one at a time, backtrack on constraint violation |
| **Forward checking** | After each assignment, remove inconsistent values from neighboring domains |
| **Arc consistency (AC-3)** | Propagate constraints to prune domains before and during search |
| **Variable ordering (MRV)** | Choose the variable with the Minimum Remaining Values (most constrained) first |
| **Value ordering (LCV)** | Try the Least Constraining Value first (preserves options for other variables) |

**Examples**: Sudoku, map coloring, scheduling, crossword puzzles, register allocation.

## Generating Functions (Conceptual)

Generating functions are a powerful mathematical tool from combinatorics that encode a sequence of numbers as coefficients of a formal power series. While primarily a theoretical tool, they provide closed-form solutions and identities for counting problems.

- **Ordinary generating function** (OGF): A(x) = sum of a_n * x^n. Used for combinations and selections.
- **Exponential generating function** (EGF): A(x) = sum of a_n * x^n / n!. Used for permutations and labeled structures.

**Practical insight**: Even without computing generating functions directly, understanding them helps recognize when a counting problem has a known closed-form solution or recurrence. Knuth uses generating functions extensively in TAOCP to derive exact formulas for combinatorial quantities.

**Example**: The generating function for the number of ways to make change for n cents using coins of denominations d1, d2, ..., dk is the product of 1/(1 - x^di) for each denomination. The coefficient of x^n gives the answer.

## Pruning Strategies

Effective pruning is what makes backtracking practical for large search spaces.

| Strategy | Description | Example |
|----------|-------------|---------|
| **Constraint propagation** | Reduce domains based on current assignments | Sudoku: eliminate placed digits from row/col/box |
| **Bound pruning** | Skip branches that cannot beat the current best | Branch and bound: skip if optimistic bound <= best |
| **Symmetry breaking** | Avoid exploring configurations that are equivalent by symmetry | N-Queens: fix the first queen to the left half |
| **Dominance pruning** | Skip states that are provably worse than another explored state | Knapsack: skip items with worse value-to-weight ratio |
| **Feasibility pruning** | Abandon states that cannot possibly lead to a valid solution | Subset sum: prune if remaining elements cannot reach target |
| **Ordering heuristics** | Process choices in an order likely to find solutions or prune early | MRV for CSPs, try larger values first for optimization |

## Complexity of Combinatorial Problems

| Problem | Brute Force | With Pruning / Optimization |
|---------|-------------|----------------------------|
| All permutations | O(n!) | O(n!) -- must enumerate all |
| All subsets | O(2^n) | O(2^n) -- must enumerate all |
| N-Queens (all solutions) | O(n!) | Significantly less with pruning |
| Sudoku | O(9^81) theoretical | Practical with constraint propagation |
| Subset Sum | O(2^n) | Pseudo-polynomial DP: O(n * target) |
| TSP (exact) | O(n!) | O(n^2 * 2^n) with DP (Held-Karp) |
| Graph Coloring | O(k^n) | NP-complete; effective with backtracking + pruning |

## Knuth's TAOCP Vol. 4A: Key Topics

| Section | Topic |
|---------|-------|
| 7.2.1 | Generating all n-tuples |
| 7.2.1.1 | Generating all permutations |
| 7.2.1.2 | Generating all combinations |
| 7.2.1.3 | Generating all partitions |
| 7.2.1.4 | Generating all set partitions |
| 7.2.1.5 | Generating all trees |
| 7.2.2 | Backtrack programming |
| 7.2.2.1 | Dancing links (Algorithm X) |

**Dancing Links (DLX)**: Knuth's Algorithm X with the "dancing links" technique is an efficient backtracking method for exact cover problems. It represents the constraint matrix as a doubly-linked list structure that allows O(1) removal and restoration of elements, making it highly efficient for problems like Sudoku, pentomino tiling, and N-Queens.

## Best Practices

- Always add pruning to backtracking -- even simple feasibility checks can reduce runtime by orders of magnitude.
- For optimization problems, consider branch and bound before exhaustive enumeration.
- Use constraint propagation (forward checking, arc consistency) for CSPs to reduce the effective search space.
- Choose variable and value ordering heuristics carefully -- MRV and LCV are strong general-purpose strategies.
- Consider whether the problem has symmetries that can be exploited to avoid redundant exploration.
- For problems with overlapping subproblems (e.g., subset sum, TSP), combine backtracking with dynamic programming.
- Reference Knuth's TAOCP Vol. 4A for the most rigorous and comprehensive treatment of combinatorial generation and backtracking, including Algorithm X and dancing links for exact cover problems.
