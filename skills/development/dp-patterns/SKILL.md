---
name: dp-patterns
description: Reference for dynamic programming patterns — recognition signals, constraint mapping, Python templates, edge cases, and common mistakes for 8 core DP techniques
user-invocable: false
disable-model-invocation: false
---

# Dynamic Programming Patterns

This reference covers eight foundational dynamic programming patterns commonly encountered in algorithmic problem solving. Each pattern includes recognition signals to identify when a problem maps to the technique, a working Python template, and specific edge cases and mistakes to watch for. Load this skill when solving optimization, counting, or subsequence problems that exhibit optimal substructure and overlapping subproblems.

## General DP Approach

Before selecting a specific pattern, apply this checklist:

1. **Identify the state**: What information do you need to uniquely describe a subproblem? (index, remaining capacity, bitmask of visited nodes)
2. **Define the recurrence**: How does the answer for the current state relate to answers for smaller states?
3. **Establish base cases**: What are the trivial subproblems with known answers?
4. **Determine iteration order**: Ensure every state is computed before it is needed (bottom-up) or use memoization (top-down)
5. **Optimize space**: If dp[i] depends only on dp[i-1] (or a small window), use rolling arrays instead of the full table

## Pattern Recognition Table

| Trigger Signals | Technique | Typical Complexity |
|---|---|---|
| "count the number of ways", "how many distinct paths" | Fibonacci / Climbing Stairs | O(N) time, O(1) space |
| "maximize value with weight limit", "partition into two equal subsets" | 0/1 Knapsack | O(N * W) time, O(W) space |
| "longest common subsequence", "minimum edit operations" | LCS / Edit Distance | O(N * M) time, O(min(N, M)) space |
| "longest increasing subsequence", "minimum number of envelopes" | LIS | O(N log N) time, O(N) space |
| "unique paths in grid", "minimum cost to reach bottom-right" | Grid DP | O(R * C) time, O(C) space |
| "maximum subarray sum", "best contiguous segment" | Kadane's Algorithm | O(N) time, O(1) space |
| "fewest coins to make amount", "ways to combine denominations" | Coin Change / Unbounded Knapsack | O(N * amount) time, O(amount) space |
| "visit all nodes exactly once", "assign N items optimally", N <= 20 | Bitmask DP | O(2^N * N) time, O(2^N) space |

## Constraint-to-Technique Mapping

Use input constraints to narrow the viable DP approach:

| Constraint Range | Viable Approaches |
|---|---|
| N <= 20 | Bitmask DP, brute-force with memoization |
| N <= 500 | O(N^3) DP (interval DP, Floyd-Warshall) |
| N <= 5,000 | O(N^2) DP (LIS quadratic, 2D tables) |
| N <= 100,000 | O(N log N) DP (LIS with binary search, segment tree optimization) |
| N <= 1,000,000 | O(N) DP (Fibonacci-style, Kadane, sliding window) |
| N * W <= 10^7 | Knapsack variants (0/1 or unbounded) |
| Grid R * C <= 10^6 | Standard grid DP with rolling array |

### Fibonacci / Climbing Stairs

**Recognition Signals**
- "How many ways to reach step N"
- "Count distinct ways to combine steps of size 1, 2, ..."
- "Decode ways" (how many ways to decode a digit string into letters)
- Recurrence follows f(n) = f(n-1) + f(n-2) or a generalized k-step variant

**Core Idea**
The answer at position N depends only on a fixed number of prior positions. Build the result iteratively from the base cases, keeping only the last k values in memory. This generalizes beyond two-step Fibonacci to any linear recurrence. When the recurrence has a fixed number of terms, space reduces to O(k) where k is the number of terms. For very large N (e.g., N > 10^18), matrix exponentiation can compute the result in O(k^3 log N).

**Python Template**
```python
def climb_stairs(n: int, steps: list[int] | None = None) -> int:
    """Count ways to reach step n using allowed step sizes."""
    if steps is None:
        steps = [1, 2]
    max_step = max(steps)
    # dp[i] = number of ways to reach step i
    dp: list[int] = [0] * (max_step + 1)
    dp[0] = 1  # base case: one way to stay at ground
    for i in range(1, n + 1):
        total = 0
        for s in steps:
            if i - s >= 0:
                total += dp[(i - s) % (max_step + 1)]
        dp[i % (max_step + 1)] = total
    return dp[n % (max_step + 1)]
```

**Key Edge Cases**
- n = 0: exactly 1 way (do nothing)
- n = 1 with only step size 2: 0 ways (unreachable)
- Large n with modular arithmetic required (typically mod 10^9 + 7)
- Negative step sizes are not valid; guard input

**Common Mistakes**
- Forgetting the base case dp[0] = 1 and getting all zeros
- Off-by-one in the loop range (should go up to n inclusive)
- Not applying modular arithmetic early, causing integer overflow in languages with fixed-width integers

### 0/1 Knapsack

**Recognition Signals**
- "Maximize total value without exceeding capacity W"
- "Can you partition the array into two subsets with equal sum"
- "Select a subset such that the sum equals target"
- Each item can be used at most once

**Core Idea**
For each item, decide to include or exclude it. Build a 1D DP array where dp[w] indicates the best achievable value (or a boolean for subset sum) using capacity w. Iterate items in the outer loop and capacity in reverse to ensure each item is used at most once. Common variants include subset sum (boolean dp), partition equal subset sum (check if total/2 is achievable), and target sum with +/- signs (offset the DP index by a constant).

**Python Template**
```python
def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:
    """Return maximum value achievable within capacity."""
    n = len(weights)
    dp: list[int] = [0] * (capacity + 1)
    for i in range(n):
        # Traverse capacity in reverse to avoid reusing item i
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[capacity]
```

**Key Edge Cases**
- All items heavier than capacity: answer is 0
- Capacity is 0: answer is 0 regardless of items
- Single item that exactly matches capacity
- Subset sum variant: dp is boolean, dp[0] = True

**Common Mistakes**
- Iterating capacity forward instead of reverse, which allows items to be picked multiple times (that is unbounded knapsack)
- Confusing 0/1 knapsack with unbounded knapsack when items are reusable
- Not handling the case where weights[i] > capacity (skip the inner loop for that item)

### Longest Common Subsequence (LCS)

**Recognition Signals**
- "Find the longest common subsequence of two strings"
- "Minimum number of insertions and deletions to transform A into B"
- "Edit distance between two strings"
- Two sequences compared element by element

**Core Idea**
Build a 2D table where dp[i][j] represents the LCS length of the first i characters of A and first j characters of B. If characters match, extend the diagonal; otherwise take the max of skipping from either side. Edit distance uses the same table structure with insertion, deletion, and substitution costs, where each operation adds 1 (or a weighted cost) and the goal switches from maximizing to minimizing. The "minimum deletions to make two strings equal" variant is directly: len(A) + len(B) - 2 * LCS(A, B).

**Python Template**
```python
def lcs(a: str, b: str) -> int:
    """Return length of the longest common subsequence."""
    m, n = len(a), len(b)
    # Use two rows to reduce space from O(m*n) to O(min(m,n))
    if m < n:
        a, b, m, n = b, a, n, m
    prev: list[int] = [0] * (n + 1)
    curr: list[int] = [0] * (n + 1)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev, curr = curr, [0] * (n + 1)
    return prev[n]
```

**Key Edge Cases**
- One or both strings empty: LCS is 0
- Strings are identical: LCS equals the full length
- No common characters at all: LCS is 0
- Very long strings (space optimization with rolling rows is critical)

**Common Mistakes**
- Mixing up 0-indexed and 1-indexed access between the string and the DP table
- Forgetting to reset the curr row between iterations when using rolling arrays
- Reconstructing the actual subsequence requires storing the full table or backtracking pointers, which the space-optimized version does not support

### Longest Increasing Subsequence (LIS)

**Recognition Signals**
- "Find the length of the longest strictly increasing subsequence"
- "Minimum number of envelopes that nest inside each other"
- "Longest chain of pairs"
- Ordering constraint on a single sequence

**Core Idea**
The O(N^2) approach builds dp[i] as the LIS ending at index i by checking all j < i where nums[j] < nums[i]. The O(N log N) approach (patience sorting) maintains a tails array where tails[k] is the smallest tail element of any increasing subsequence of length k+1. For each element, binary search for its position in tails to either extend or replace. To reconstruct the actual subsequence, maintain a parent pointer array alongside the tails.

**Python Template**
```python
import bisect

def lis_length(nums: list[int]) -> int:
    """Return length of longest strictly increasing subsequence. O(N log N)."""
    tails: list[int] = []
    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)  # extend the longest subsequence
        else:
            tails[pos] = num  # replace to keep smallest tail
    return len(tails)
```

**Key Edge Cases**
- Empty array: LIS is 0
- All elements equal: LIS is 1 (strictly increasing requires distinct values)
- Already sorted in increasing order: LIS equals array length
- Non-strictly increasing (allow equal): use bisect_right instead of bisect_left

**Common Mistakes**
- Using bisect_right for strictly increasing (gives non-decreasing subsequence instead)
- Assuming the tails array is the actual LIS (it is not; it only gives the correct length)
- Forgetting to handle the 2D variant (e.g., Russian doll envelopes) by sorting one dimension ascending and the second dimension descending before applying LIS on the second dimension
- Confusing "longest non-decreasing subsequence" with "longest strictly increasing subsequence" when duplicate values exist

### Grid DP

**Recognition Signals**
- "How many unique paths from top-left to bottom-right"
- "Minimum cost path in a grid moving only right or down"
- "Fill a matrix where each cell depends on its top and left neighbors"
- "Maximum cherries/gold you can collect traversing a grid" (multi-path grid DP)

**Core Idea**
Process cells row by row (or column by column). Each cell's value depends on its top neighbor and left neighbor. Use a single row array to reduce space: the current value at dp[c] is the "top" neighbor, and dp[c-1] is the "left" neighbor already updated in this row. For "unique paths" counting, the value is the sum of top and left; for "minimum path sum", take the min of top and left plus the current cell cost. Obstacles are handled by zeroing out blocked cells.

**Python Template**
```python
def min_path_sum(grid: list[list[int]]) -> int:
    """Return minimum path sum from top-left to bottom-right."""
    rows, cols = len(grid), len(grid[0])
    dp: list[int] = [0] * cols
    dp[0] = grid[0][0]
    # First row: can only come from the left
    for c in range(1, cols):
        dp[c] = dp[c - 1] + grid[0][c]
    # Remaining rows
    for r in range(1, rows):
        dp[0] += grid[r][0]  # first column: can only come from above
        for c in range(1, cols):
            dp[c] = min(dp[c], dp[c - 1]) + grid[r][c]
    return dp[cols - 1]
```

**Key Edge Cases**
- Single row or single column grid: path is forced, just sum all cells
- 1x1 grid: answer is the single cell value
- Grid with negative values: min-path logic still works, but "unique paths" counting is unaffected by values
- Obstacles (cells marked as blocked): set dp to infinity (min-path) or 0 (counting)

**Common Mistakes**
- Forgetting to initialize the first row and first column separately before the main loop
- Allowing diagonal movement when the problem only permits right and down
- Not handling the obstacle case (setting blocked cells to 0 or infinity depending on the variant)
- Modifying the input grid in place to save space without realizing the problem may need the original values later

### Kadane's Algorithm

**Recognition Signals**
- "Maximum sum of a contiguous subarray"
- "Best time to buy and sell stock" (single transaction variant)
- "Largest sum contiguous segment"
- "Maximum product subarray" (variant with sign tracking)
- "Circular subarray with maximum sum" (run Kadane twice: once normal, once inverted)

**Core Idea**
At each position, decide whether to extend the current subarray or start fresh. Track the running sum and reset it to the current element whenever extending would produce a smaller result. Maintain a global maximum across all positions. The "buy and sell stock" variant is Kadane's in disguise: compute the diff array of consecutive prices, then find the maximum subarray sum of the diffs.

**Python Template**
```python
def max_subarray_sum(nums: list[int]) -> int:
    """Return maximum sum of any contiguous subarray. Handles all-negative arrays."""
    if not nums:
        return 0
    current_sum = nums[0]
    best_sum = nums[0]
    for i in range(1, len(nums)):
        # Extend current subarray or start new one at nums[i]
        current_sum = max(nums[i], current_sum + nums[i])
        best_sum = max(best_sum, current_sum)
    return best_sum
```

**Key Edge Cases**
- All negative numbers: answer is the largest (least negative) single element
- Single element: answer is that element
- Array of all zeros: answer is 0
- Very large arrays where overflow matters (apply constraints)

**Common Mistakes**
- Initializing current_sum and best_sum to 0 instead of nums[0], which fails for all-negative arrays
- Returning 0 for all-negative arrays by incorrectly assuming subarray must have positive sum
- Not adapting for the "maximum product" variant, which requires tracking both the max and min running product due to sign flips
- For circular subarray max sum: forgetting to handle the case where all elements are negative (the inverted Kadane approach gives total_sum - min_subarray_sum, but if all are negative this wraps to 0, which is invalid since the subarray must be non-empty)

### Coin Change / Unbounded Knapsack

**Recognition Signals**
- "Fewest coins to make amount"
- "Number of ways to make change using denominations"
- "Each coin/item can be used unlimited times"
- "Minimum number of items to reach target sum"

**Core Idea**
Unlike 0/1 knapsack, items can be reused. Iterate capacity in the forward direction so each denomination contributes multiple times. For minimum coins, initialize dp with infinity and take the min. For counting combinations, accumulate sums. The critical distinction between counting combinations vs permutations lies in loop order: coins in the outer loop counts each set of coins once (combinations), while amount in the outer loop counts every ordering (permutations).

**Python Template**
```python
def coin_change_min(coins: list[int], amount: int) -> int:
    """Return fewest coins to make amount, or -1 if impossible."""
    dp: list[float] = [float("inf")] * (amount + 1)
    dp[0] = 0  # base case: 0 coins for amount 0
    for coin in coins:
        # Forward iteration allows reusing the same coin
        for a in range(coin, amount + 1):
            dp[a] = min(dp[a], dp[a - coin] + 1)
    return dp[amount] if dp[amount] != float("inf") else -1


def coin_change_ways(coins: list[int], amount: int) -> int:
    """Return number of distinct combinations to make amount."""
    dp: list[int] = [0] * (amount + 1)
    dp[0] = 1  # one way to make amount 0
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] += dp[a - coin]
    return dp[amount]
```

**Key Edge Cases**
- Amount is 0: min coins is 0, number of ways is 1
- No coins provided: impossible for any positive amount
- Single coin that does not divide the amount: impossible
- Counting permutations vs combinations: iterating coins in outer loop gives combinations; iterating amount in outer loop gives permutations

**Common Mistakes**
- Confusing combinations and permutations by swapping the loop order (coins-outer counts combinations, amount-outer counts permutations)
- Forgetting to return -1 when dp[amount] remains infinity
- Using reverse iteration (which gives 0/1 knapsack behavior instead of unbounded)

### Bitmask DP

**Recognition Signals**
- "Visit all N cities exactly once" (TSP)
- "Assign N tasks to N workers optimally"
- "Enumerate all subsets of a set"
- Constraint: N <= 20 (since 2^20 = ~10^6 is feasible)

**Core Idea**
Represent the set of visited/used elements as a bitmask integer. dp[mask] (or dp[mask][i]) stores the optimal value when the set of chosen elements is described by mask. Iterate over all 2^N masks and try adding each element not yet in the mask to transition to the next state. For subset enumeration without a "current position" dimension, use dp[mask] alone. When order matters (TSP), add a second dimension dp[mask][last] to track which element was visited last.

**Python Template**
```python
def tsp(dist: list[list[int]]) -> int:
    """Return minimum cost to visit all cities and return to start (TSP)."""
    n = len(dist)
    full_mask = (1 << n) - 1
    INF = float("inf")
    # dp[mask][i] = min cost to reach city i having visited cities in mask
    dp: list[list[float]] = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # start at city 0
    for mask in range(1, 1 << n):
        for u in range(n):
            if dp[mask][u] == INF:
                continue
            if not (mask >> u & 1):
                continue  # u not in current mask
            for v in range(n):
                if mask >> v & 1:
                    continue  # v already visited
                new_mask = mask | (1 << v)
                cost = dp[mask][u] + dist[u][v]
                if cost < dp[new_mask][v]:
                    dp[new_mask][v] = cost
    # Return to start city
    return int(min(dp[full_mask][i] + dist[i][0] for i in range(n)))
```

**Key Edge Cases**
- N = 1: only one city, cost is 0
- N = 0: no cities, trivially 0
- Asymmetric distances: dist[i][j] != dist[j][i] (common in directed TSP)
- Assignment problem variant: no return-to-start, just minimize total assignment cost

**Common Mistakes**
- Forgetting to check that the current city u is actually in the mask before expanding from it
- Not initializing the start state correctly (dp[1 << start][start] = 0)
- Using N > 20, which makes 2^N states exceed memory and time limits

## Top-Down vs Bottom-Up

Both approaches produce the same results but have different trade-offs:

| Aspect | Top-Down (Memoization) | Bottom-Up (Tabulation) |
|---|---|---|
| Implementation | Recursive with cache (functools.cache or dict) | Iterative with array |
| States computed | Only reachable states | All states in the table |
| Stack depth | Risk of RecursionError for large N (Python default limit: 1000) | No recursion; safe for any N |
| Space optimization | Harder to apply rolling arrays | Natural fit for rolling arrays |
| Debugging | Easier to trace individual subproblems | Easier to inspect the full table |

**When to prefer top-down**: The state space is sparse (many states are unreachable), or the recurrence is complex and hard to order iteratively.

**When to prefer bottom-up**: Space optimization is needed, the state space is dense, or recursion depth would exceed limits.

## Combining Patterns

Many problems require combining two or more patterns:

- **LIS on 2D points** (Russian doll envelopes): Sort by one dimension, apply LIS on the other
- **Grid DP + Bitmask**: Collect items in a grid where you must visit specific cells (small item count)
- **Knapsack + Fibonacci**: Count ways to fill a knapsack where item order matters (permutation variant)
- **LCS + Edit Distance**: Compute similarity scores between sequences using weighted operations
- **Kadane + Grid**: Maximum sum rectangle in a 2D matrix by fixing two rows and applying Kadane on column prefix sums
- **Coin Change + Counting**: Number of ways to make change with a maximum number of coins (bounded knapsack hybrid)

When a problem does not fit cleanly into one pattern, identify the state variables first, then check which pattern's recurrence most closely matches the transitions between states.

## Python-Specific Tips

**Memoization with functools.cache**
For top-down DP in Python 3.9+, use `@functools.cache` (or `@functools.lru_cache(maxsize=None)` for 3.8):

```python
import functools

@functools.cache
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

**Recursion limit**: Python's default recursion limit is 1000. For deep DP recursion, set `sys.setrecursionlimit(N + 100)` or convert to bottom-up.

**Integer size**: Python integers have arbitrary precision, so overflow is not a concern. However, modular arithmetic (% MOD) should still be applied at each step to keep numbers small and avoid slow big-integer operations.

**Array initialization**: Use `[0] * n` for 1D and `[[0] * cols for _ in range(rows)]` for 2D. Never use `[[0] * cols] * rows` as all rows will share the same reference.
