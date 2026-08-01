---
name: python-pandas-best-practices
description: '---name: pandas-best-practices'
---

---name: pandas-best-practices
description: Standards for efficient, readable, and performant data manipulation using Python's Pandas library.
license: MIT
metadata:
  author: AI Group
  version: "1.0.0"
  category: Software_Engineering
compatibility:
  - system: Python 3.9+
  - system: Pandas 2.0+
allowed-tools:
  - read_file
  - replace
  - write_file

keywords:
  - python-pandas-best-practices
  - automation
  - biomedical
measurable_outcome: execute task with >95% success rate.
---"

# Pandas Best Practices

This skill provides guidelines for working with tabular data in Python. It focuses on vectorization, memory management, and method chaining to write "Modern Pandas" code.

## When to Use This Skill

*   **Data Cleaning**: Preprocessing clinical or genomic datasets.
*   **Analysis**: Performing aggregations, merges, or statistical summaries.
*   **Performance**: Optimizing slow-running scripts that process large CSVs/DataFrames.

## Core Capabilities

1.  **Vectorization**: Replacing `for` loops with vectorized array operations.
2.  **Method Chaining**: Writing readable, fluent data transformation pipelines.
3.  **Memory Optimization**: Using appropriate dtypes (Categoricals, Nullable Ints) to reduce RAM usage.
4.  **Modern Indexing**: Using `.loc` and `.iloc` correctly; avoiding `SettingWithCopyWarning`.

## Workflow

1.  **Inspect Data**: Check `df.info()` and `df.head()`.
2.  **Define Pipeline**: Plan transformations (filter -> group -> aggregate).
3.  **Implement Chain**: Write the logic as a chain of methods.
4.  **Optimize**: Check for loops or `apply` calls that can be vectorized.

## Example Usage

**User**: "Calculate the mean age by patient group, but exclude patients with missing IDs."

**Agent Action**:
1.  Reads `references/rules.md`.
2.  Generates:
    ```python
    result = (
        df
        .dropna(subset=['patient_id'])
        .groupby('patient_group')['age']
        .mean()
        .reset_index()
    )
    ```
