---
name: sorting-searching
description: |
    Use when implementing or selecting sorting and searching algorithms. Covers comparison sorts (Quicksort, Mergesort, Heapsort, Insertion sort, Timsort), linear sorts (Counting, Radix, Bucket), and searching techniques (binary search, interpolation search, two pointers, sliding window). Based on Knuth's TAOCP Vol. 3.
    USE FOR: sorting algorithm selection, searching algorithm selection, understanding sort stability, complexity comparison of sorting methods, binary search variations, two-pointer and sliding window techniques
    DO NOT USE FOR: graph traversal (use graph-algorithms), dynamic programming (use dynamic-programming)
license: MIT
metadata:
  displayName: "Sorting & Searching Algorithms"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "The Art of Computer Programming, Vol. 3: Sorting and Searching — Donald Knuth"
    url: "https://www-cs-faculty.stanford.edu/~knuth/taocp.html"
  - title: "Sorting Algorithm — Wikipedia"
    url: "https://en.wikipedia.org/wiki/Sorting_algorithm"
---

# Sorting & Searching Algorithms

## Overview
Sorting and searching are among the most fundamental operations in computer science. Knuth dedicated the entirety of *The Art of Computer Programming, Volume 3: Sorting and Searching* to these topics, reflecting their importance and depth. This skill covers the major algorithms in both categories, their complexities, and guidance on when to use each.

## Sorting Algorithms

### Comparison Sorts

Comparison-based sorts determine order by comparing pairs of elements. The theoretical lower bound for comparison sorting is O(n log n).

#### Quicksort
- **Strategy**: Divide and conquer. Pick a pivot, partition the array so elements less than the pivot come before it and elements greater come after, then recurse.
- **Time**: O(n log n) average, O(n^2) worst case (poor pivot choice)
- **Space**: O(log n) stack space (in-place partitioning)
- **Stable**: No
- **Best for**: General-purpose sorting; fastest in practice for most data distributions due to excellent cache behavior.

```
QUICKSORT(A, lo, hi):
    if lo < hi:
        p = PARTITION(A, lo, hi)
        QUICKSORT(A, lo, p - 1)
        QUICKSORT(A, p + 1, hi)

PARTITION(A, lo, hi):
    pivot = A[hi]
    i = lo - 1
    for j = lo to hi - 1:
        if A[j] <= pivot:
            i = i + 1
            swap A[i] and A[j]
    swap A[i + 1] and A[hi]
    return i + 1
```

#### Mergesort
- **Strategy**: Divide and conquer. Split the array in half, recursively sort each half, then merge the two sorted halves.
- **Time**: O(n log n) in all cases
- **Space**: O(n) auxiliary
- **Stable**: Yes
- **Best for**: When stability is required, linked lists, external sorting (large files that do not fit in memory).

```
MERGESORT(A, lo, hi):
    if lo < hi:
        mid = (lo + hi) / 2
        MERGESORT(A, lo, mid)
        MERGESORT(A, mid + 1, hi)
        MERGE(A, lo, mid, hi)

MERGE(A, lo, mid, hi):
    create temporary arrays L = A[lo..mid], R = A[mid+1..hi]
    i = 0, j = 0, k = lo
    while i < |L| and j < |R|:
        if L[i] <= R[j]:
            A[k] = L[i]; i++
        else:
            A[k] = R[j]; j++
        k++
    copy remaining elements of L or R into A
```

#### Heapsort
- **Strategy**: Build a max-heap from the array, then repeatedly extract the maximum to build the sorted result.
- **Time**: O(n log n) in all cases
- **Space**: O(1) (in-place)
- **Stable**: No
- **Best for**: When guaranteed O(n log n) is needed without extra memory. Not cache-friendly, so often slower than Quicksort in practice.

#### Insertion Sort
- **Strategy**: Build the sorted array one element at a time by inserting each element into its correct position among the already-sorted elements.
- **Time**: O(n) best case (nearly sorted), O(n^2) worst/average case
- **Space**: O(1) (in-place)
- **Stable**: Yes
- **Best for**: Small arrays, nearly sorted data, online sorting (data arrives one element at a time). Often used as the base case in hybrid sorts.

#### Timsort
- **Strategy**: Hybrid of Mergesort and Insertion sort. Identifies natural runs (already sorted subsequences), extends them with insertion sort, then merges runs using an optimized merge procedure.
- **Time**: O(n) best case (already sorted), O(n log n) worst case
- **Space**: O(n) auxiliary
- **Stable**: Yes
- **Best for**: Real-world data that often contains partially sorted subsequences. Default sort in Python and Java.

### Linear Sorts

These sorts exploit constraints on the input (bounded range, integer keys) to beat the O(n log n) comparison lower bound.

#### Counting Sort
- **Strategy**: Count occurrences of each value, then compute positions from cumulative counts.
- **Time**: O(n + k) where k is the range of input values
- **Space**: O(n + k)
- **Stable**: Yes
- **Best for**: Small integer ranges (e.g., sorting grades 0-100, characters).

#### Radix Sort
- **Strategy**: Sort by each digit/character position from least significant to most significant, using a stable sub-sort (typically counting sort) at each position.
- **Time**: O(d * (n + k)) where d is the number of digits and k is the radix
- **Space**: O(n + k)
- **Stable**: Yes
- **Best for**: Fixed-length integers or strings with bounded alphabet.

#### Bucket Sort
- **Strategy**: Distribute elements into buckets based on value range, sort each bucket individually, then concatenate.
- **Time**: O(n + k) average when input is uniformly distributed; O(n^2) worst case
- **Space**: O(n + k)
- **Stable**: Depends on bucket sort
- **Best for**: Uniformly distributed floating-point numbers in a known range.

### Sorting Complexity Comparison

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Quicksort | O(n log n) | O(n log n) | O(n^2) | O(log n) | No |
| Mergesort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Heapsort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Insertion Sort | O(n) | O(n^2) | O(n^2) | O(1) | Yes |
| Timsort | O(n) | O(n log n) | O(n log n) | O(n) | Yes |
| Counting Sort | O(n + k) | O(n + k) | O(n + k) | O(n + k) | Yes |
| Radix Sort | O(d(n + k)) | O(d(n + k)) | O(d(n + k)) | O(n + k) | Yes |
| Bucket Sort | O(n + k) | O(n + k) | O(n^2) | O(n + k) | Varies |

### When to Use Which Sort

| Situation | Recommended Sort |
|-----------|-----------------|
| General purpose, in-memory | Quicksort (or language default, often Timsort) |
| Stability required | Mergesort or Timsort |
| Guaranteed O(n log n), no extra space | Heapsort |
| Small arrays (n < 20) | Insertion Sort |
| Nearly sorted data | Insertion Sort or Timsort |
| Integer keys with small range | Counting Sort |
| Fixed-length integer/string keys | Radix Sort |
| Uniformly distributed floating-point data | Bucket Sort |
| External sorting (data on disk) | External Mergesort |
| Linked list sorting | Mergesort |

## Searching Algorithms

### Binary Search
- **Precondition**: Array must be sorted.
- **Strategy**: Repeatedly halve the search space by comparing the target to the middle element.
- **Time**: O(log n)
- **Space**: O(1) iterative, O(log n) recursive

```
BINARY_SEARCH(A, target):
    lo = 0, hi = len(A) - 1
    while lo <= hi:
        mid = lo + (hi - lo) / 2
        if A[mid] == target:
            return mid
        else if A[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1  // not found
```

**Variations**: Lower bound (first occurrence), upper bound (last occurrence), search on answer (binary search the solution space).

### Interpolation Search
- **Precondition**: Array must be sorted and values uniformly distributed.
- **Strategy**: Estimate the position of the target based on its value relative to the min and max of the current range.
- **Time**: O(log log n) average for uniformly distributed data, O(n) worst case
- **Best for**: Large, uniformly distributed sorted datasets.

### Two Pointers Technique
- **Strategy**: Use two pointers (indices) that move through the data structure, typically from opposite ends or at different speeds.
- **Time**: Typically O(n)
- **Common applications**: Pair sum in sorted array, removing duplicates, partitioning, palindrome check, merging sorted arrays.

### Sliding Window Technique
- **Strategy**: Maintain a window (contiguous subarray) that slides through the array, expanding or shrinking to satisfy a condition.
- **Time**: Typically O(n)
- **Common applications**: Maximum/minimum subarray of size k, longest substring without repeating characters, smallest subarray with sum >= target.

### Searching Complexity Comparison

| Algorithm | Average | Worst | Precondition |
|-----------|---------|-------|--------------|
| Linear Search | O(n) | O(n) | None |
| Binary Search | O(log n) | O(log n) | Sorted |
| Interpolation Search | O(log log n) | O(n) | Sorted, uniform distribution |
| Hash Lookup | O(1) | O(n) | Hash table built |
| Two Pointers | O(n) | O(n) | Often sorted |
| Sliding Window | O(n) | O(n) | Contiguous subarray problems |

## Stability in Sorting

A sort is **stable** if elements with equal keys retain their original relative order after sorting. Stability matters when:
- Sorting by multiple keys (sort by secondary key first, then by primary key with a stable sort).
- Preserving meaningful insertion order.
- Composing sorts for multi-level ordering.

## Best Practices

- Use your language's built-in sort (typically Timsort or Introsort) unless you have a specific reason not to -- they are highly optimized.
- For searching in a sorted collection, always prefer binary search over linear search.
- Consider the two pointers technique before reaching for nested loops on sorted data.
- The sliding window technique converts many O(n^2) brute-force subarray problems into O(n).
- When data has bounded integer keys, consider counting or radix sort for linear-time performance.
- Reference Knuth's TAOCP Vol. 3 for rigorous analysis of any sorting or searching method.
