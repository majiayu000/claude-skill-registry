---
name: search-and-optimization
description: >-
  Reference patterns for search, optimization, and greedy algorithms. Covers
  binary search (classic and on-answer), two pointers, sliding window, greedy
  strategies, prefix sums, merge intervals, and monotonic stack. Use when solving
  problems that involve searching sorted data, optimizing over constraints,
  processing subarrays/substrings, or reducing range queries.
user-invocable: false
disable-model-invocation: false
---

# Search and Optimization Patterns

This reference covers eight foundational search and optimization techniques that appear across competitive programming, coding interviews, and production algorithms. Each pattern includes recognition signals, a core idea summary, a Python template with type hints, key edge cases, and common mistakes.

---

## Pattern Recognition Table

| Trigger Signals | Technique | Typical Complexity |
|---|---|---|
| Sorted array, find target, O(log n) required | Binary Search | O(log n) |
| "Minimize the maximum", "find smallest feasible value" | Binary Search on Answer | O(n log S) where S = search space |
| Sorted array, find pair with target sum, in-place | Two Pointers | O(n) |
| Fixed/variable-length subarray, substring constraints | Sliding Window | O(n) |
| Local optimal leads to global optimal, exchange argument | Greedy | O(n log n) typical |
| Range sum queries, subarray sums, 2D region sums | Prefix Sums | O(n) build, O(1) query |
| Overlapping intervals, merge/insert, scheduling | Merge Intervals | O(n log n) |
| Next greater/smaller element, histogram areas | Monotonic Stack | O(n) |

---

## Constraint-to-Technique Mapping

When the problem does not immediately suggest a technique, use constraints as a guide:

- **n <= 10^5 and "find minimum/maximum feasible"** — Binary search on answer with a greedy or simulation check function.
- **Sorted input + pair/triplet finding** — Two pointers before considering hash maps. Saves space and often required by the problem.
- **Contiguous subarray/substring with a constraint** — Sliding window. If the constraint is a sum threshold, variable-size window. If fixed length k, fixed-size window.
- **Multiple range sum queries on static data** — Prefix sums. For 2D grids, build a 2D prefix sum matrix.
- **"Given a set of intervals"** — Sort by start (or end), then merge or sweep. Check if the problem is really interval scheduling (sort by end, greedy).
- **"For each element, find the next greater/smaller"** — Monotonic stack. Direction of traversal (left-to-right or right-to-left) depends on whether you need "next" or "previous".
- **Optimization under constraints with greedy proof** — Try exchange argument: if swapping any two elements in the solution cannot improve it, greedy works.

---

## Individual Patterns

### Binary Search

**Recognition Signals**
- Input array is sorted (or can be sorted without changing the answer).
- Problem asks for the position of a target or the insertion point.
- O(log n) time is expected or required.

**Core Idea**
Maintain a search interval `[lo, hi]` and halve it each step by comparing the midpoint against the target. The invariant is that the answer always lies within the current interval. Choose between `lo = mid + 1` and `hi = mid` (or `hi = mid - 1`) depending on whether you want the leftmost or rightmost match.

**Python Template**

```python
from bisect import bisect_left, bisect_right
from typing import List

def binary_search(nums: List[int], target: int) -> int:
    """Return index of target, or -1 if not found."""
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

def left_bound(nums: List[int], target: int) -> int:
    """Return index of first element >= target."""
    return bisect_left(nums, target)

def right_bound(nums: List[int], target: int) -> int:
    """Return index of first element > target."""
    return bisect_right(nums, target)
```

**Key Edge Cases**
- Empty array — return -1 or 0 depending on variant.
- All elements identical — left_bound and right_bound diverge.
- Target smaller than all elements or larger than all elements.
- Integer overflow in `lo + hi` — use `lo + (hi - lo) // 2`.

**Common Mistakes**
- Off-by-one: using `lo < hi` when the loop should be `lo <= hi` (or vice versa).
- Forgetting to handle the case where `bisect_left` returns `len(nums)`.
- Mutating the input array when the problem requires preserving order.

---

### Binary Search on Answer

**Recognition Signals**
- Problem asks to "minimize the maximum" or "maximize the minimum".
- The answer lies in a bounded numeric range and is monotonic (if X works, all values above/below also work).
- A feasibility check can be written in O(n) or O(n log n).

**Core Idea**
Instead of searching in the input array, binary search over the space of possible answers. Define a predicate `feasible(x) -> bool` that returns True if the answer x satisfies all constraints. The answer space is monotonic: once feasible becomes True, it stays True (or vice versa). Binary search finds the boundary.

**Python Template**

```python
from typing import Callable, List

def binary_search_on_answer(
    lo: int,
    hi: int,
    feasible: Callable[[int], bool],
) -> int:
    """Find the smallest value in [lo, hi] where feasible returns True."""
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

def can_split(nums: List[int], max_sum: int, k: int) -> bool:
    """Check if nums can be split into <= k subarrays each with sum <= max_sum."""
    count, current = 1, 0
    for x in nums:
        if x > max_sum:
            return False
        if current + x > max_sum:
            count += 1
            current = x
        else:
            current += x
    return count <= k
```

**Key Edge Cases**
- Single-element input where lo == hi immediately.
- The feasibility check must handle individual elements exceeding the candidate answer.
- Floating-point variant: use a fixed number of iterations (e.g., 100) instead of `lo < hi`.
- Off-by-one in bounds: `lo` should be the minimum possible answer, `hi` the maximum.

**Common Mistakes**
- Reversing the predicate direction (searching for max when predicate checks min feasibility).
- Setting initial bounds too tight and excluding the actual answer.
- Forgetting that maximizing the minimum requires flipping the search direction.

---

### Two Pointers

**Recognition Signals**
- Sorted array with a pair-sum or triplet-sum target.
- "Find two elements that satisfy a condition" with O(1) extra space.
- Removing duplicates in-place, or partitioning an array.
- Merging two sorted sequences.

**Core Idea**
Place one pointer at each end of a sorted array (opposite direction) or both at the start (same direction). Move pointers inward based on how the current state compares to the target. Each pointer moves at most n times, giving O(n) total. The technique exploits sorted order to prune the search space without nested loops.

**Python Template**

```python
from typing import List, Tuple, Optional

def two_sum_sorted(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """Find indices of two numbers in sorted array that sum to target."""
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s == target:
            return (lo, hi)
        elif s < target:
            lo += 1
        else:
            hi -= 1
    return None

def remove_duplicates(nums: List[int]) -> int:
    """Remove duplicates in-place from sorted array. Return new length."""
    if not nums:
        return 0
    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[read - 1]:
            nums[write] = nums[read]
            write += 1
    return write
```

**Key Edge Cases**
- Array with fewer than 2 elements.
- Multiple valid pairs — decide if you need the first, all, or any.
- Duplicate values that cause pointer movement to skip valid answers.
- Negative numbers affecting sum direction.

**Common Mistakes**
- Using two pointers on an unsorted array without sorting first.
- Not skipping duplicates when the problem asks for unique pairs.
- Returning indices from the sorted array when the problem wants original indices.

---

### Sliding Window

**Recognition Signals**
- "Maximum/minimum sum of subarray of size k" (fixed window).
- "Longest/shortest substring containing all characters of X" (variable window).
- Contiguous subarray or substring with a constraint on sum, count, or character frequency.
- O(n) expected and brute-force is O(n^2).

**Core Idea**
Maintain a window `[left, right]` over the array. Expand `right` to include more elements; shrink `left` when the window violates the constraint. Track the answer as the window slides. Fixed-size windows advance both pointers together. Variable-size windows expand until invalid, then contract until valid again.

**Python Template**

```python
from collections import Counter
from typing import List

def max_sum_subarray(nums: List[int], k: int) -> int:
    """Maximum sum of any contiguous subarray of size k."""
    n = len(nums)
    if n < k:
        return 0
    window_sum = sum(nums[:k])
    best = window_sum
    for i in range(k, n):
        window_sum += nums[i] - nums[i - k]
        best = max(best, window_sum)
    return best

def min_window_substring(s: str, t: str) -> str:
    """Shortest substring of s containing all characters of t."""
    need = Counter(t)
    missing = len(t)
    left = 0
    best_start, best_len = 0, len(s) + 1
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        while missing == 0:
            if right - left + 1 < best_len:
                best_start, best_len = left, right - left + 1
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    return s[best_start : best_start + best_len] if best_len <= len(s) else ""
```

**Key Edge Cases**
- Window size k equals the array length.
- Empty string t or s shorter than t in substring problems.
- All elements identical — window may never need to shrink.
- Negative numbers in sum-based windows (sliding window may not apply; consider prefix sums instead).

**Common Mistakes**
- Applying variable-size sliding window when the constraint is not monotonic (e.g., subarray with negative numbers).
- Off-by-one in window boundaries when computing length.
- Forgetting to update the frequency map when shrinking the window.

---

### Greedy

**Recognition Signals**
- Interval scheduling, activity selection, or job sequencing.
- "Maximum number of non-overlapping intervals".
- A locally optimal choice at each step provably leads to a global optimum.
- The problem has optimal substructure and the greedy choice property.

**Core Idea**
Make the locally optimal choice at each decision point without reconsidering previous choices. The key is proving correctness, typically via the exchange argument: assume an optimal solution differs from the greedy solution, then show you can swap one element to match the greedy choice without worsening the result. Sort the input by the criterion that enables the greedy choice.

**Python Template**

```python
from typing import List, Tuple

def activity_selection(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Select maximum non-overlapping intervals. Each interval is (start, end)."""
    intervals.sort(key=lambda x: x[1])
    selected: List[Tuple[int, int]] = []
    last_end = -1
    for start, end in intervals:
        if start >= last_end:
            selected.append((start, end))
            last_end = end
    return selected

def min_platforms(arrivals: List[int], departures: List[int]) -> int:
    """Minimum platforms needed so no train waits (sweep line variant)."""
    events: List[Tuple[int, int]] = []
    for a in arrivals:
        events.append((a, 1))
    for d in departures:
        events.append((d + 1, -1))
    events.sort()
    current = best = 0
    for _, delta in events:
        current += delta
        best = max(best, current)
    return best
```

**Key Edge Cases**
- Intervals that share an endpoint (closed vs. open interval semantics).
- All intervals overlap — answer is 1 for selection, n for platforms.
- Single interval input.
- Ties in the sorting criterion — secondary sort order matters.

**Common Mistakes**
- Sorting by start time when end time is needed (or vice versa).
- Assuming greedy works without proving the exchange argument.
- Not handling the edge case where `start == end` for zero-length intervals.

---

### Prefix Sums

**Recognition Signals**
- Multiple queries for the sum of a subarray or submatrix.
- "Number of subarrays with sum equal to k" (prefix sum + hash map).
- Range update queries on an array (difference array variant).
- O(1) per query required after preprocessing.

**Core Idea**
Build a prefix sum array where `prefix[i]` = sum of elements `[0..i-1]`. Any range sum `[l..r]` becomes `prefix[r+1] - prefix[l]` in O(1). For 2D, build a prefix sum matrix using inclusion-exclusion. Difference arrays are the inverse: store deltas, then reconstruct with a prefix sum after all updates.

**Python Template**

```python
from typing import List

def build_prefix(nums: List[int]) -> List[int]:
    """Build 1D prefix sum array. prefix[i] = sum(nums[0:i])."""
    prefix = [0] * (len(nums) + 1)
    for i, x in enumerate(nums):
        prefix[i + 1] = prefix[i] + x
    return prefix

def range_sum(prefix: List[int], l: int, r: int) -> int:
    """Sum of nums[l..r] inclusive using prefix array."""
    return prefix[r + 1] - prefix[l]

def subarray_sum_count(nums: List[int], k: int) -> int:
    """Count subarrays with sum exactly k."""
    from collections import defaultdict
    count = 0
    current = 0
    seen: dict[int, int] = defaultdict(int)
    seen[0] = 1
    for x in nums:
        current += x
        count += seen[current - k]
        seen[current] += 1
    return count
```

**Key Edge Cases**
- Empty array — prefix sum is `[0]`.
- Negative numbers — prefix sums are not monotonic, so binary search on prefix does not work.
- Subarray starting at index 0 — `prefix[0]` must be 0.
- Integer overflow on large inputs — use appropriate types.

**Common Mistakes**
- Off-by-one in prefix indexing: `prefix[r+1] - prefix[l]`, not `prefix[r] - prefix[l-1]` (unless 1-indexed).
- Forgetting to initialize `seen[0] = 1` in the hash map variant.
- Applying prefix sum binary search when values can be negative.

---

### Merge Intervals

**Recognition Signals**
- "Given a list of intervals, merge all overlapping intervals."
- Insert a new interval into a sorted non-overlapping list.
- "Minimum number of meeting rooms" (variant uses a sweep line or min-heap).
- Output is a reduced set of non-overlapping intervals.

**Core Idea**
Sort intervals by start time. Iterate through and merge the current interval with the last merged interval if they overlap (current start <= last end). Otherwise, start a new group. For insertion, find the overlap region, merge, and concatenate the non-overlapping parts. The sweep-line variant converts intervals into +1/-1 events for counting concurrent overlaps.

**Python Template**

```python
from typing import List, Tuple

def merge_intervals(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Merge all overlapping intervals. Each interval is (start, end)."""
    if not intervals:
        return []
    intervals.sort()
    merged: List[Tuple[int, int]] = [intervals[0]]
    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged

def insert_interval(
    intervals: List[Tuple[int, int]],
    new: Tuple[int, int],
) -> List[Tuple[int, int]]:
    """Insert new interval into sorted non-overlapping list and merge."""
    result: List[Tuple[int, int]] = []
    i, n = 0, len(intervals)
    while i < n and intervals[i][1] < new[0]:
        result.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= new[1]:
        new = (min(new[0], intervals[i][0]), max(new[1], intervals[i][1]))
        i += 1
    result.append(new)
    result.extend(intervals[i:])
    return result
```

**Key Edge Cases**
- Single interval — return as-is.
- All intervals overlap — result is one merged interval.
- Adjacent intervals `(1,3)` and `(3,5)` — overlapping if using `<=`, not if using `<`.
- Already sorted and non-overlapping input.

**Common Mistakes**
- Using `<` instead of `<=` for overlap check (depends on whether endpoints are inclusive).
- Forgetting to take `max(last_end, end)` when merging (the new interval might be contained).
- Sorting by end time when start time is needed for the merge algorithm.

---

### Monotonic Stack

**Recognition Signals**
- "Next greater element" or "next smaller element" for each position.
- "Largest rectangle in histogram" or "maximal rectangle in binary matrix".
- Stock span, daily temperatures, or trapping rain water.
- O(n) solution needed where brute force is O(n^2).

**Core Idea**
Maintain a stack that is always monotonically increasing or decreasing. When a new element violates the monotonic property, pop elements from the stack — each popped element has found its "next greater" (or "next smaller") in the current element. Every element is pushed and popped at most once, giving O(n) amortized time. The stack stores indices rather than values to enable distance calculations.

**Python Template**

```python
from typing import List

def next_greater_element(nums: List[int]) -> List[int]:
    """For each element, find the next greater element to its right. -1 if none."""
    n = len(nums)
    result = [-1] * n
    stack: List[int] = []  # indices, monotonically decreasing values
    for i in range(n):
        while stack and nums[stack[-1]] < nums[i]:
            result[stack.pop()] = nums[i]
        stack.append(i)
    return result

def largest_rectangle_histogram(heights: List[int]) -> int:
    """Largest rectangle area in a histogram."""
    stack: List[int] = []  # indices, monotonically increasing heights
    max_area = 0
    heights_ext = heights + [0]  # sentinel to flush remaining bars
    for i, h in enumerate(heights_ext):
        while stack and heights_ext[stack[-1]] > h:
            height = heights_ext[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    return max_area
```

**Key Edge Cases**
- All elements in strictly increasing order — stack never pops until a sentinel.
- All elements equal — every element's "next greater" is -1.
- Single element — result is -1 for next greater, or the element itself for histogram area.
- Circular array variant — iterate through `2 * n` indices using modulo.

**Common Mistakes**
- Storing values instead of indices on the stack (loses position information).
- Forgetting the sentinel value at the end to flush remaining stack elements.
- Confusing monotonically increasing vs. decreasing — increasing stack finds next smaller, decreasing finds next greater.
