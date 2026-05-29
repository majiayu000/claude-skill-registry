---
name: numpy-memory
description: Deep dive into memory layout, including strides, C vs Fortran order, and zero-copy view generation via stride tricks. Triggers: strides, C-order, Fortran-order, memory locality, stride_tricks.
---

## Overview
NumPy memory management revolves around the concept of "strides." Strides define the number of bytes to skip in a flat 1D buffer to move to the next element in an N-dimensional space. Understanding this allows for zero-copy operations like transposition and complex sliding windows.

## When to Use
- Optimizing high-performance code for CPU cache locality.
- Creating overlapping sliding windows for signal processing without duplicating data.
- Interfacing with libraries that require specific memory orders (e.g., BLAS/Fortran).
- Manipulating array logic without incurring the cost of data copying.

## Decision Tree
1. Need to optimize for row-wise processing?
   - Use C-order (row-major). Smallest stride is on the last axis.
2. Interfacing with legacy Fortran or BLAS?
   - Use Fortran-order (column-major). Smallest stride is on the first axis.
3. Want to create a sliding window view?
   - Use `np.lib.stride_tricks.as_strided`. (Use with caution).

## Workflows
1. **Analyzing Memory Locality**
   - Check `arr.strides` and `arr.itemsize`.
   - Identify the axis with the smallest stride (fastest changing in memory).
   - Reorder loops or axes to ensure data access follows the smallest stride for cache efficiency.

2. **Zero-Copy Transposition**
   - Call `arr.T` or `arr.transpose()`.
   - Inspect the strides of the result.
   - Note that the underlying data buffer remains identical; only the stride metadata was swapped.

3. **Creating Sliding Windows without Copies**
   - Identify an array segment.
   - Use `np.lib.stride_tricks.as_strided` with a custom stride tuple to create overlapping windows.
   - Perform vectorized operations on the windowed view (warning: values may overlap).

## Non-Obvious Insights
- **Metadata Logic:** Changing an array's shape or transposing it often changes *only* the strides and shape metadata, leaving the data buffer untouched.
- **Cache Performance:** Iterating over an axis with a large stride is slow because elements are spaced far apart in memory, causing CPU cache misses.
- **Strides Modification:** Directly setting `arr.strides` is unsafe and discouraged; `as_strided` is the preferred, safer interface for advanced memory manipulation.

## Evidence
- "The strides of an array tell us how many bytes we have to skip in memory to move to the next position along a certain axis." [Source](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.strides.html)
- "The shape of the array can be changed very easily without changing anything in the data buffer or any data copying at all." [Source](https://numpy.org/doc/stable/dev/internals.html)

## Scripts
- `scripts/numpy-memory_tool.py`: Tools for stride analysis and zero-copy window creation.
- `scripts/numpy-memory_tool.js`: Simulated byte-offset calculator.

## Dependencies
- `numpy` (Python)

## References
- [references/README.md](references/README.md)