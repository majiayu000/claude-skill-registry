---
name: numpy-masked
description: Masked arrays for robust handling of missing or invalid data, ensuring they are excluded from statistical and mathematical computations. Triggers: masked array, numpy.ma, missing data, invalid values, hard mask.
---

## Overview
The `numpy.ma` module provides masked arrays, which couple a data array with a boolean mask. Masked elements are ignored in operations like `mean()`, `sum()`, and `log()`, making them ideal for datasets where certain entries should be excluded without deleting them and losing shape information.

## When to Use
- Handling sensor data with "no-data" values (e.g., -999).
- Performing statistics on arrays containing NaNs or Infs where you want the invalid values automatically excluded.
- Protecting specific data points from modification during processing using a "hard mask."
- Exporting data where missing values must be filled with a specific constant.

## Decision Tree
1. Do you need to keep the original array shape while ignoring certain values?
   - Use `ma.masked_array`.
2. Are you performing math on risky values (e.g., negative numbers in log)?
   - Use `ma.masked_invalid(arr)` or `ma.masked_less(arr, 0)`.
3. Want to extract only valid data for another tool?
   - Use the `.compressed()` method to get a 1D array of valid values.

## Workflows
1. **Calculating Stats on Tainted Data**
   - Create a masked array from raw data using `ma.masked_values(data, -999)`.
   - Perform a `.mean()` calculation.
   - Observe that the result only reflects valid, unmasked data points.

2. **Filling Missing Values for Export**
   - Identify a masked array with gaps.
   - Call `.filled(fill_value=0)` to create a standard ndarray.
   - Save the filled array to a CSV or binary file.

3. **Domain-Safe Vectorized Operations**
   - Use `ma.masked_invalid(arr)` to mask NaNs and Infs.
   - Apply a mathematical function (e.g., `ma.sqrt`).
   - Resulting array will have masks wherever the operation was invalid (e.g., square root of negative).

## Non-Obvious Insights
- **Hard Masking:** If a masked array has a "hard mask," assigning a value to a masked entry will silently fail; it remains masked. This is a safety feature for protecting outlier exclusions.
- **Assignment Masking:** Assigning the constant `ma.masked` to an array element automatically updates the internal mask to `True` for that position.
- **Compression Side-Effect:** Calling `.compressed()` returns a 1D array, which destroys the original dimensionality (e.g., a 2D masked array becomes 1D).

## Evidence
- "The package ensures that masked entries are not used in computations." [Source](https://numpy.org/doc/stable/reference/maskedarray.generic.html)
- "Unary and binary functions that have a validity domain (such as log or divide) return the masked constant whenever the input is masked or falls outside the validity domain." [Source](https://numpy.org/doc/stable/reference/maskedarray.generic.html)

## Scripts
- `scripts/numpy-masked_tool.py`: Routines for masked stats and domain-safe sqrt.
- `scripts/numpy-masked_tool.js`: Simulated boolean mask filtering.

## Dependencies
- `numpy` (Python)

## References
- [references/README.md](references/README.md)