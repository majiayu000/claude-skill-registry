---
name: numpy-sorting
description: NumPy sorting provides efficient tools for ordering data. Beyond basic
  sorting, it includes partitioning for top-k selection and vectorized binary search
  for finding insertion points in sorted data.
---

---
name: numpy-sorting
description: Sorting and searching algorithms including O(n) partitioning, binary search, and hierarchical multi-key sorting. Triggers: sort, argsort, partition, searchsorted, lexsort, nan sort order.
---

## Overview
NumPy sorting provides efficient tools for ordering data. Beyond basic sorting, it includes partitioning for top-k selection and vectorized binary search for finding insertion points in sorted data.

## When to Use
- Finding the top $k$ largest or smallest elements without a full sort ($O(N)$).
- Ordering data based on multiple criteria (e.g., sort by Date, then by Price).
- Mapping data into bins or ranges using binary search.
- Handling datasets containing NaNs where sorting order is sensitive.

## Decision Tree
1. Need the indices of the sorted order (not the values)?
   - Use `np.argsort`.
2. Only need the $k$ smallest elements?
   - Use `np.partition(arr, k)`. Elements to the left of index $k$ are smaller.
3. Finding where to insert a value to keep order?
   - Use `np.searchsorted(sorted_arr, value)`.

## Workflows
1. **Efficiently Finding the Smallest K Elements**
   - Identify an unsorted array.
   - Call `np.partition(arr, kth=k)`.
   - Select the first k elements: `result[:k]`.

2. **Vectorized Lookup in Sorted Ranges**
   - Ensure the target array 'A' is sorted.
   - Pass a list of values 'V' to `np.searchsorted(A, V)`.
   - Use the returned indices to map values to specific bins or ranges.

3. **Indirect Multi-Key Sort**
   - Define primary and secondary key arrays.
   - Use `np.lexsort((secondary, primary))` to get the index array.
   - Apply the indices to the data to achieve the desired hierarchical sort order.

## Non-Obvious Insights
- **NaN Position:** `np.nan` is treated as larger than `np.inf` and is always sorted to the end of the array.
- **Partition Performance:** Partitioning along the last axis is significantly faster and uses less memory than partitioning along any other axis.
- **Lexsort Order:** `lexsort` takes keys in reverse order of importance; the *last* key in the sequence is the *primary* sort key.

## Evidence
- "In the output array, all elements smaller than the k-th element are located to the left of this element and all equal or greater are located to its right." [Source](https://numpy.org/doc/stable/reference/generated/numpy.partition.html)
- "Binary search is used to find the required insertion points." [Source](https://numpy.org/doc/stable/reference/generated/numpy.searchsorted.html)

## Scripts
- `scripts/numpy-sorting_tool.py`: Implements top-k selection and hierarchical lexsort.
- `scripts/numpy-sorting_tool.js`: Basic sort simulation.

## Dependencies
- `numpy` (Python)

## References
- [references/README.md](references/README.md)