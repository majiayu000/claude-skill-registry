---
name: numpy-statistics
description: Standard and NaN-robust statistical functions for data analysis, histograms, and correlation matrices. Triggers: statistics, mean, nanmean, histogram, corrcoef, percentile, std.
---

## Overview
NumPy provides a suite of statistical functions for summarizing data. Key capabilities include calculating central tendencies, dispersion, and relationships between variables, with specific handling for missing values (NaNs).

## When to Use
- Summarizing experimental data (mean, median, standard deviation).
- Visualizing data distributions via histogram counts and binning.
- Identifying relationships between multiple variables using correlation matrices.
- Analyzing datasets with missing values where standard aggregations would fail.

## Decision Tree
1. Does your data contain `NaN`?
   - Yes: Use `nan` prefixed functions (e.g., `np.nanmean`).
   - No: Use standard functions (e.g., `np.mean`).
2. Creating a histogram?
   - Need normalized area? Set `density=True`.
   - Fixed bin widths? Provide an integer for `bins` or an array for custom edges.
3. Checking correlation?
   - Use `np.corrcoef`. Note: output may require clipping if float errors occur.

## Workflows
1. **Robust Mean Calculation**
   - Identify an array with potential missing values (NaNs).
   - Calculate the mean using `np.nanmean(arr)`.
   - Optionally use `np.nanstd(arr)` to find the standard deviation of the valid subset.

2. **Custom Histogram Creation**
   - Define a set of non-uniform bin edges `[0, 5, 10, 50, 100]`.
   - Pass the data and edges to `np.histogram(data, bins=edges)`.
   - Retrieve the counts and the validated edges for plotting.

3. **Inter-Variable Correlation Analysis**
   - Stack multiple data variables into a 2D array (rows as variables).
   - Execute `np.corrcoef(data)`.
   - Inspect the off-diagonal elements for Pearson correlation strengths.

## Non-Obvious Insights
- **NaN Sensitivity:** Standard statistical functions return `NaN` if even one element is missing; the `nan` versions are essential for real-world messy data.
- **Histogram Density:** The `density=True` flag ensures the integral over the histogram is 1, not that the sum of the counts is 1 (unless bin widths are 1).
- **Precision Clipping:** Correlation coefficients can occasionally drift outside `[-1, 1]` due to floating-point rounding; NumPy automatically mitigates this in `corrcoef` results.

## Evidence
- "nanmean... Compute the arithmetic mean along the specified axis, ignoring NaNs." [Source](https://numpy.org/doc/stable/reference/routines.statistics.html)
- "Note that the sum of the histogram values will not be equal to 1 unless bins of unity width are chosen; it is not a probability mass function." [Source](https://numpy.org/doc/stable/reference/generated/numpy.histogram.html)

## Scripts
- `scripts/numpy-statistics_tool.py`: Computes robust statistics and custom histograms.
- `scripts/numpy-statistics_tool.js`: Basic mean calculator.

## Dependencies
- `numpy` (Python)

## References
- [references/README.md](references/README.md)