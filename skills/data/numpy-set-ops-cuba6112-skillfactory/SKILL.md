---
name: numpy-set-ops
description: Set-theoretic operations for finding unique elements, membership testing, and array intersections. Triggers: unique, isin, intersect1d, setdiff1d, union1d.
---

## Overview
NumPy provides vectorized set operations for 1D arrays and multidimensional subarrays. These tools allow for deduplication, membership testing, and finding differences/intersections between datasets.

## When to Use
- Deduplicating rows in a large feature matrix.
- Filtering a dataset to exclude a list of forbidden values.
- Synchronizing two datasets by finding their intersection.
- Compressing data by storing unique values and their index mappings.

## Decision Tree
1. Need to find non-duplicate elements?
   - Use `np.unique`.
2. Need to reconstruct the original array from unique values?
   - Set `return_inverse=True` in `np.unique`.
3. Checking if elements exist in another list?
   - Use `np.isin(data, target_list)`.

## Workflows
1. **Finding Unique Rows in a Dataset**
   - Create a 2D array.
   - Call `np.unique(arr, axis=0)`.
   - Inspect the result to see the deduplicated records.

2. **Reconstructing an Array from Sets**
   - Call `u, inv = np.unique(arr, return_inverse=True)`.
   - Store 'u' and 'inv' separately (useful for data compression).
   - Rebuild the original array using `u[inv]`.

3. **Filtering by Membership**
   - Define a 'forbidden' set of values.
   - Generate a boolean mask using `~np.isin(data, forbidden)`.
   - Filter the data: `clean_data = data[mask]`.

## Non-Obvious Insights
- **Flattening by Default:** Set operations work on flattened 1D versions of input arrays unless an `axis` is explicitly specified.
- **NaN Handling:** Like sorting, `unique` treats `NaN` as a value and sorts it to the end of the unique output.
- **Lexicographic Row Sort:** When `axis=0` is used in `unique`, the resulting unique rows are sorted lexicographically.

## Evidence
- "Returns the sorted unique elements of an array." [Source](https://numpy.org/doc/stable/reference/generated/numpy.unique.html)
- "isin(element, test_elements...)... broadcasting over element only." [Source](https://numpy.org/doc/stable/reference/routines.set.html)

## Scripts
- `scripts/numpy-set-ops_tool.py`: Routines for unique row detection and inverse reconstruction.
- `scripts/numpy-set-ops_tool.js`: Simulated set intersection logic.

## Dependencies
- `numpy` (Python)

## References
- [references/README.md](references/README.md)