---
name: data-structures
description: >-
  Reference for advanced data structure patterns used in competitive programming
  and technical interviews. Covers heaps, monotonic stacks, tries, segment trees,
  Fenwick trees, stack-based parsing, and ordered sets with Python templates,
  recognition signals, and edge case guidance.
user-invocable: false
disable-model-invocation: false
---

# Data Structure Patterns

This skill provides recognition signals, core ideas, Python templates, and pitfall guidance for seven advanced data structure patterns. Use it when a problem's constraints or access patterns suggest a specialized structure beyond basic arrays, hash maps, or linked lists. Each pattern section follows a consistent format: when to reach for it, how it works, a clean implementation template, and the mistakes that cost time in practice.

---

## Pattern Recognition Table

| Trigger Signals | Technique | Typical Complexity |
|---|---|---|
| "k-th largest/smallest", "top K", "merge K sorted" | Heap / Priority Queue | O(n log k) |
| "next greater/smaller element", "sliding window max/min" | Monotonic Stack / Queue | O(n) |
| "prefix matching", "autocomplete", "word search in grid" | Trie | O(L) per operation |
| "range query + point update", "range min/max/sum" | Segment Tree | O(log n) per query/update |
| "prefix sums with updates", "count of elements less than X" | Fenwick Tree (BIT) | O(log n) per query/update |
| "balanced parentheses", "evaluate expression", "nested structures" | Stack-Based Parsing | O(n) |
| "rank of element", "k-th smallest in dynamic set", "floor/ceiling" | Ordered Set (SortedList) | O(log n) per operation |

---

## Constraint-to-Technique Mapping

When the problem statement does not name a structure directly, use constraints to narrow the choice:

- **n <= 10^5 with repeated range queries** -- Segment Tree or Fenwick Tree. Prefer Fenwick when only prefix sums are needed; use Segment Tree for arbitrary range operations.
- **n <= 10^6 and "next greater" or "span" language** -- Monotonic Stack. Linear time is essential at this scale.
- **String dictionary with prefix lookups** -- Trie. Hash maps work for exact match but not prefix enumeration.
- **"Top K" or "k-th element" with streaming data** -- Heap. A size-k heap avoids sorting the full dataset.
- **Dynamic insertions + rank/order queries** -- SortedList. Python lacks a built-in balanced BST; sortedcontainers fills this gap.
- **Nested or recursive syntax (math expressions, HTML tags)** -- Stack-Based Parsing. The stack mirrors the nesting depth.

---

### Heap / Priority Queue

**Recognition Signals**
- "Find the k-th largest/smallest element"
- "Merge k sorted lists/arrays"
- "Continuously add elements and query the median or top-K"
- "Schedule tasks by priority"

**Core Idea**
A heap maintains partial order so that the min (or max) element is always accessible in O(1) with O(log n) insertion and extraction. For "top K" problems, maintain a min-heap of size k: every new element either replaces the root or is discarded, guaranteeing O(n log k) total work.

**Python Template**

```python
import heapq
from typing import List

def top_k_frequent(nums: List[int], k: int) -> List[int]:
    from collections import Counter
    freq = Counter(nums)
    # Min-heap of size k on frequency
    return heapq.nlargest(k, freq.keys(), key=freq.get)

def merge_k_sorted(lists: List[List[int]]) -> List[int]:
    result: list[int] = []
    heap: list[tuple[int, int, int]] = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        if elem_idx + 1 < len(lists[list_idx]):
            heapq.heappush(heap, (lists[list_idx][elem_idx + 1], list_idx, elem_idx + 1))
    return result
```

**Key Edge Cases**
- Empty input lists or sublists in merge-k scenarios
- All elements identical (heap still works, but deduplication may be needed)
- k equals n (heap degenerates; sorting may be simpler)
- Negative numbers with max-heap emulation (negate values for `heapq`)

**Common Mistakes**
- Forgetting that Python's `heapq` is a min-heap; for max-heap, negate values or use `heapq.nlargest`
- Not including a tiebreaker index in the heap tuple, causing crashes on uncomparable objects
- Using `heapify` then manually inserting without `heappush` (breaks the heap invariant)

---

### Monotonic Stack / Queue

**Recognition Signals**
- "Next greater element" or "next smaller element"
- "Sliding window maximum/minimum"
- "Largest rectangle in histogram"
- "Daily temperatures / stock span"

**Core Idea**
A monotonic stack maintains elements in strictly increasing or decreasing order. When a new element arrives, pop all elements that violate the monotonic property -- each popped element has found its "next greater" (or "next smaller"). Every element is pushed and popped at most once, yielding O(n) total. For sliding windows, a monotonic deque adds front-eviction to maintain the window boundary.

**Python Template**

```python
from collections import deque
from typing import List

def next_greater_element(nums: List[int]) -> List[int]:
    n = len(nums)
    result = [-1] * n
    stack: list[int] = []  # indices
    for i in range(n):
        while stack and nums[stack[-1]] < nums[i]:
            result[stack.pop()] = nums[i]
        stack.append(i)
    return result

def sliding_window_max(nums: List[int], k: int) -> List[int]:
    dq: deque[int] = deque()  # indices, front = max
    result: list[int] = []
    for i, val in enumerate(nums):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] <= val:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

**Key Edge Cases**
- Array with all equal elements (no element is "greater"; result is all -1)
- Single-element array (result is trivially -1)
- Circular array variant (iterate 2n elements using modular indexing)
- Window size k = 1 (output equals input)

**Common Mistakes**
- Storing values instead of indices on the stack (cannot determine window boundaries)
- Using the wrong comparison direction (< vs. <=) and getting a non-strictly monotonic stack
- Forgetting to handle the circular case by iterating `range(2 * n)`

---

### Trie

**Recognition Signals**
- "Find all words with a given prefix"
- "Word search in a 2D grid with a dictionary"
- "Autocomplete / typeahead suggestions"
- "Maximum XOR of two numbers in an array"

**Core Idea**
A trie stores strings character-by-character in a tree where each edge represents one character. Shared prefixes share nodes, making prefix lookups O(L) regardless of dictionary size. For XOR tries, store numbers bit-by-bit (MSB to LSB) and greedily choose the opposite bit at each level.

**Python Template**

```python
from typing import Optional

class TrieNode:
    __slots__ = ("children", "is_end", "count")
    def __init__(self) -> None:
        self.children: dict[str, "TrieNode"] = {}
        self.is_end: bool = False
        self.count: int = 0  # words passing through this node

class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.count += 1
        node.is_end = True

    def starts_with(self, prefix: str) -> int:
        """Return count of words with given prefix."""
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return 0
            node = node.children[ch]
        return node.count
```

**Key Edge Cases**
- Empty string insertion (root itself becomes an end node)
- Prefix that is also a complete word (must check `is_end` separately from prefix existence)
- Unicode or case-sensitive input (normalize before insertion)
- Deletion requires decrementing counts and pruning childless nodes

**Common Mistakes**
- Not distinguishing "prefix exists" from "exact word exists" (missing `is_end` check)
- Building a trie for exact-match-only problems where a hash set suffices
- Forgetting `__slots__` on trie nodes, leading to high memory usage on large dictionaries

---

### Segment Tree

**Recognition Signals**
- "Range sum/min/max query with point updates"
- "Count of elements in a range satisfying a condition"
- "Range update + range query" (lazy propagation)

**Core Idea**
A segment tree is a binary tree where each leaf represents one element and each internal node stores an aggregate (sum, min, max) of its children's range. Queries and updates both traverse O(log n) nodes. Lazy propagation defers range updates by tagging nodes, applying pending updates only when a child is accessed, keeping range updates at O(log n).

**Python Template**

```python
from typing import List

class SegmentTree:
    """Range sum query with point update."""
    def __init__(self, data: List[int]) -> None:
        self.n = len(data)
        self.tree = [0] * (2 * self.n)
        # Build leaves
        for i in range(self.n):
            self.tree[self.n + i] = data[i]
        # Build internal nodes
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def update(self, idx: int, val: int) -> None:
        idx += self.n
        self.tree[idx] = val
        while idx > 1:
            idx >>= 1
            self.tree[idx] = self.tree[2 * idx] + self.tree[2 * idx + 1]

    def query(self, left: int, right: int) -> int:
        """Sum of data[left:right] (half-open interval)."""
        res = 0
        left += self.n
        right += self.n
        while left < right:
            if left & 1:
                res += self.tree[left]
                left += 1
            if right & 1:
                right -= 1
                res += self.tree[right]
            left >>= 1
            right >>= 1
        return res
```

**Key Edge Cases**
- Single-element array (tree has two levels; queries are trivial)
- Query range equals the full array (should return root value)
- Index-0 vs. index-1 conventions (this template uses 0-indexed input)
- Overflow on large sums (use Python's arbitrary-precision integers or explicit modular arithmetic)

**Common Mistakes**
- Off-by-one in the query range (half-open `[left, right)` vs. closed `[left, right]`)
- Forgetting to propagate lazy values before accessing children in lazy segment trees
- Building with `2 * n` size but using 1-indexed logic (need `4 * n` for 1-indexed recursive style)

---

### Fenwick Tree (BIT)

**Recognition Signals**
- "Prefix sum queries with dynamic updates"
- "Count of elements less than X after insertions"
- "Inversion count in an array"
- "2D prefix sums with updates"

**Core Idea**
A Fenwick tree (Binary Indexed Tree) uses the binary representation of indices to partition prefix sums across O(log n) nodes. Each node at index `i` stores the sum of a range whose length equals the lowest set bit of `i`. Updates and prefix queries both run in O(log n). Fenwick trees use less memory and have smaller constants than segment trees but only support prefix-based queries natively. Range `[l, r]` is computed as `prefix(r) - prefix(l - 1)`.

**Python Template**

```python
from typing import List

class FenwickTree:
    def __init__(self, n: int) -> None:
        self.n = n
        self.tree = [0] * (n + 1)  # 1-indexed

    def update(self, i: int, delta: int) -> None:
        """Add delta to element at 1-indexed position i."""
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)

    def query(self, i: int) -> int:
        """Return prefix sum from index 1 to i (inclusive)."""
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

    def range_query(self, left: int, right: int) -> int:
        """Sum of elements in [left, right], 1-indexed."""
        return self.query(right) - self.query(left - 1)

    @classmethod
    def from_array(cls, data: List[int]) -> "FenwickTree":
        ft = cls(len(data))
        for i, val in enumerate(data, 1):
            ft.update(i, val)
        return ft
```

**Key Edge Cases**
- Zero-indexed input (convert to 1-indexed before calling update/query)
- Querying index 0 (should return 0, which the while loop handles naturally)
- Negative values in updates (Fenwick handles deltas, not absolute values)

**Common Mistakes**
- Using 0-indexed positions (index 0 causes an infinite loop in `update` because `0 & (-0) == 0`)
- Confusing "set value" with "add delta" (Fenwick stores cumulative deltas, not absolute values)
- Forgetting that `range_query(1, 0)` should return 0 (guard against inverted ranges)

---

### Stack-Based Parsing

**Recognition Signals**
- "Check if parentheses/brackets are balanced"
- "Evaluate arithmetic expression with operator precedence"
- "Decode nested encoded strings like `3[a2[c]]`"
- "Basic calculator with +, -, *, /, and parentheses"

**Core Idea**
A stack naturally mirrors nesting depth: push context when entering a deeper level (opening bracket, new sub-expression) and pop when leaving it (closing bracket, operator resolution). For expression evaluation, use two stacks (operands and operators) or convert to reverse Polish notation first. The stack preserves the outer context while you process the inner context; restoring is a simple pop.

**Python Template**

```python
from typing import List

def eval_expression(s: str) -> int:
    """Evaluate expression with +, -, and parentheses."""
    stack: list[tuple[int, int]] = []  # (result_before_paren, sign_before_paren)
    result = 0
    num = 0
    sign = 1
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch in "+-":
            result += sign * num
            num = 0
            sign = 1 if ch == "+" else -1
        elif ch == "(":
            stack.append((result, sign))
            result = 0
            sign = 1
        elif ch == ")":
            result += sign * num
            num = 0
            prev_result, prev_sign = stack.pop()
            result = prev_result + prev_sign * result
    result += sign * num
    return result

def is_balanced(s: str) -> bool:
    """Check if brackets are balanced."""
    pairs = {"(": ")", "[": "]", "{": "}"}
    stack: list[str] = []
    for ch in s:
        if ch in pairs:
            stack.append(pairs[ch])
        elif ch in pairs.values():
            if not stack or stack.pop() != ch:
                return False
    return len(stack) == 0
```

**Key Edge Cases**
- Empty string (should be considered balanced / evaluate to 0)
- Unary minus at the start of an expression (e.g., `-3 + 5`)
- Deeply nested structures that could overflow recursion (iterative stack avoids this)

**Common Mistakes**
- Not handling multi-digit numbers (accumulate digits before processing operators)
- Forgetting to process the last number after the loop ends (no trailing operator triggers it)
- Popping from an empty stack on mismatched closing brackets (check `len(stack)` first)

---

### Ordered Set (SortedList)

**Recognition Signals**
- "Find the k-th smallest element in a dynamic collection"
- "Count elements in a range [lo, hi] with insertions and deletions"
- "Floor/ceiling of a value in a dynamic set"
- "Sliding window median"

**Core Idea**
Python lacks a built-in balanced BST, but `sortedcontainers.SortedList` provides O(log n) insertion, deletion, and index-based access with excellent constant factors. It supports bisect for floor/ceiling, positional indexing for rank queries, and islice for range iteration. For contest environments without third-party imports, a Fenwick tree over a value-indexed array can simulate rank queries.

**Python Template**

```python
from sortedcontainers import SortedList
from typing import List, Optional

def sliding_window_median(nums: List[int], k: int) -> List[float]:
    sl = SortedList()
    result: list[float] = []
    for i, val in enumerate(nums):
        sl.add(val)
        if len(sl) > k:
            sl.remove(nums[i - k])
        if len(sl) == k:
            if k % 2 == 1:
                result.append(float(sl[k // 2]))
            else:
                result.append((sl[k // 2 - 1] + sl[k // 2]) / 2.0)
    return result

def floor_ceiling(sl: SortedList, val: int) -> tuple[Optional[int], Optional[int]]:
    """Return (floor, ceiling) of val in the sorted list."""
    idx = sl.bisect_right(val)
    floor = sl[idx - 1] if idx > 0 else None
    ceil_idx = sl.bisect_left(val)
    ceiling = sl[ceil_idx] if ceil_idx < len(sl) else None
    return floor, ceiling

def count_in_range(sl: SortedList, lo: int, hi: int) -> int:
    """Count elements in [lo, hi] inclusive."""
    return sl.bisect_right(hi) - sl.bisect_left(lo)
```

**Key Edge Cases**
- Duplicate values (SortedList allows duplicates; use `discard` to remove one occurrence, not all)
- Empty collection (bisect returns 0; floor/ceiling should return None)
- Value exactly equal to an existing element (floor and ceiling are both that element)
- Large n with frequent add/remove (handles 10^5-10^6 operations efficiently)

**Common Mistakes**
- Using `remove` on a value not in the list (raises ValueError; use `discard` for safe removal)
- Confusing `bisect_left` and `bisect_right` for floor/ceiling logic (left for ceiling, right for floor)
- Assuming SortedList is available everywhere (some contest judges lack `sortedcontainers`; have a BIT fallback)
