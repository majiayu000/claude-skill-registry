---
name: numpy-string-ops
description: Vectorized string manipulation using the char module and modern string alternatives, including cleaning and search operations. Triggers: string operations, numpy.char, text cleaning, substring search.
---

## Overview
NumPy's `char` submodule provides vectorized versions of standard Python string operations. It allows for efficient processing of arrays containing `str_` or `bytes_` types, though it is being transitioned to a newer `strings` module in recent versions.

## When to Use
- Cleaning large text datasets (e.g., stripping whitespace, normalization).
- Performing batch substring searches across thousands of records.
- Concatenating columns of text data using broadcasting.
- Converting character casing for entire datasets simultaneously.

## Decision Tree
1. Starting new development?
   - Use `numpy.strings` if available; `numpy.char` is legacy.
2. Comparing strings with potential trailing spaces?
   - `numpy.char` comparison operators automatically strip whitespace.
3. Concatenating a constant prefix to an array of names?
   - Use `np.char.add(prefix, name_array)`.

## Workflows
1. **Batch String Concatenation**
   - Create two arrays of strings, A and B.
   - Use `np.char.add(A, B)` to join them element-wise.
   - Broadcasting applies if one array is a single string and the other is multidimensional.

2. **Cleaning Text Datasets**
   - Identify an array of messy text.
   - Apply `np.char.strip(arr)` to remove whitespace.
   - Use `np.char.lower(arr)` to normalize casing across the entire dataset.

3. **Finding Substrings in Arrays**
   - Use `np.char.find(text_array, 'target_word')`.
   - Identify elements with non-negative indices (where the word was found).
   - Filter the original array using boolean indexing based on the search result.

## Non-Obvious Insights
- **Legacy Status:** The `char` module is considered legacy; future-proof code should look towards the `numpy.strings` alternative.
- **Implicit Stripping:** Unlike standard Python `==`, `char` module comparison operators strip trailing whitespace before evaluating equality.
- **Vectorization Reality:** While these operations are vectorized, string manipulation is inherently less performant than numeric math because strings have variable lengths and require more complex memory management.

## Evidence
- "Unlike the standard numpy comparison operators, the ones in the char module strip trailing whitespace characters before performing the comparison." [Source](https://numpy.org/doc/stable/reference/routines.char.html)
- "The numpy.char module provides a set of vectorized string operations for arrays of type numpy.str_ or numpy.bytes_." [Source](https://numpy.org/doc/stable/reference/routines.char.html)

## Scripts
- `scripts/numpy-string-ops_tool.py`: Routines for batch text cleaning and search.
- `scripts/numpy-string-ops_tool.js`: Simulated string concatenation logic.

## Dependencies
- `numpy` (Python)

## References
- [references/README.md](references/README.md)