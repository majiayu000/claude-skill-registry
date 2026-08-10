---
name: data-cleaning
description: Clean and preprocess datasets by handling missing values, removing duplicates, correcting types, resolving outliers, and enforcing validation schemas. Use when the user requests data cleaning or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Data Cleaning

This skill enables an AI agent to systematically clean and preprocess raw datasets into analysis-ready form. The agent handles missing values, duplicate records, data type mismatches, inconsistent formats, outlier treatment, and normalization. It can also enforce validation schemas to ensure ongoing data quality. The primary toolchain is pandas with support from pyjanitor and great_expectations for advanced validation.

## Workflow

1. **Ingest and profile the raw data.** Load the dataset and immediately generate a quality report: count nulls per column, identify duplicate rows, check data types against expected schema, and flag columns with mixed types. This profile drives every subsequent cleaning decision.

2. **Handle missing values.** Apply strategy per column based on data type and missingness pattern. For numeric columns with less than 5% missing, use median imputation. For categorical columns, use mode or a dedicated "Unknown" category. For columns missing more than 40%, flag them for potential removal and consult the user before dropping.

3. **Remove duplicates and resolve conflicts.** Identify exact duplicates and near-duplicates (e.g., rows differing only in whitespace or casing). For exact duplicates, keep the first occurrence. For near-duplicates, apply fuzzy matching with a configurable similarity threshold and merge conflicting values by recency or completeness.

4. **Correct data types and standardize formats.** Coerce columns to their intended types — parse date strings into datetime objects, convert numeric strings to floats, and normalize categorical values to a canonical form. Standardize formats such as phone numbers, postal codes, and currency representations.

5. **Detect and treat outliers.** Use the IQR method (1.5x) for symmetric distributions and z-scores for normally distributed data. Offer three treatment options: cap at boundary values (winsorization), replace with null for later imputation, or flag-only mode that annotates but preserves original values.

6. **Validate the cleaned output.** Run the cleaned dataset through validation rules — non-null constraints, range checks, uniqueness constraints, and referential integrity. Report any remaining violations and save the clean dataset alongside a cleaning log that documents every transformation applied.

## Supported Technologies

- **pandas** — core data manipulation and type coercion
- **pyjanitor** — method-chaining convenience for cleaning operations
- **great_expectations** — schema validation and data quality checks
- **fuzzywuzzy** — fuzzy string matching for near-duplicate detection
- **numpy** — numerical operations for outlier detection

## Usage

Provide the agent with the file path to the raw dataset and optionally a schema definition specifying expected column types, valid ranges, and uniqueness constraints. The agent will produce a cleaned file and a transformation log.

## Examples

### Example 1: Cleaning a messy CSV with pandas

```python
import pandas as pd
import numpy as np

# Load raw data
df = pd.read_csv("messy_orders.csv")
print(f"Raw shape: {df.shape}")  # (2340, 8)
print(df.isnull().sum())
# order_id         0
# customer_name   12
# email           45
# order_date      18
# amount          23
# status           0
# region          67
# discount         0

# 1. Fix data types — order_date has mixed formats
df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", dayfirst=False)
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

# 2. Handle missing values
df["customer_name"] = df["customer_name"].fillna("Unknown")
df["email"] = df["email"].fillna("missing@placeholder.com")
df["amount"] = df["amount"].fillna(df["amount"].median())
df["region"] = df["region"].fillna(df["region"].mode()[0])
df["order_date"] = df["order_date"].fillna(method="ffill")

# 3. Remove duplicates
before = len(df)
df = df.drop_duplicates(subset=["order_id"], keep="first")
print(f"Removed {before - len(df)} duplicate orders")  # Removed 34 duplicate orders

# 4. Standardize categorical values
df["status"] = df["status"].str.strip().str.lower().replace({
    "shipped": "shipped", "ship": "shipped",
    "cancelled": "cancelled", "canceled": "cancelled",
    "pending": "pending", "pend": "pending"
})
df["region"] = df["region"].str.strip().str.title()

# 5. Outlier treatment — cap amounts at IQR bounds
Q1 = df["amount"].quantile(0.25)
Q3 = df["amount"].quantile(0.75)
IQR = Q3 - Q1
lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
df["amount"] = df["amount"].clip(lower=lower, upper=upper)

print(f"Clean shape: {df.shape}")  # (2306, 8)
df.to_csv("clean_orders.csv", index=False)
```

### Example 2: Data validation pipeline with schema enforcement

```python
import great_expectations as gx

context = gx.get_context()

# Define a validation suite
suite = context.add_expectation_suite("orders_validation")

# Add expectations
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="order_id")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="amount", min_value=0.01, max_value=50000.00
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="status", value_set=["pending", "shipped", "delivered", "cancelled"]
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(column="order_id")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        column="email", regex=r"^[^@]+@[^@]+\.[^@]+$"
    )
)

# Run validation against cleaned data
results = context.run_validation(suite, batch=gx.read_csv("clean_orders.csv"))

print(f"Success: {results.success}")
print(f"Passed: {results.statistics['successful_expectations']}/{results.statistics['evaluated_expectations']}")
# Success: True
# Passed: 5/5
```

## Best Practices

- Always save a copy of the raw data before any transformations — cleaning should be reproducible, not destructive.
- Log every transformation with counts (e.g., "Filled 23 nulls in amount with median 312.45") to create an auditable cleaning trail.
- Prefer domain-informed imputation over mechanical defaults; consult the user when a column's missingness pattern is non-random (MNAR).
- Validate early and often — run schema checks after each cleaning phase, not just at the end.
- Treat cleaning as iterative: the first pass catches the obvious issues, but downstream analysis frequently surfaces new ones.
- Use `errors="coerce"` with `pd.to_numeric` and `pd.to_datetime` to surface conversion failures as NaNs rather than crashing.

## Edge Cases

- **Entirely empty columns.** If a column is 100% null, drop it automatically and log a warning rather than attempting imputation on zero information.
- **Duplicate column names.** Pandas silently allows duplicate column names. Detect them on load and rename with suffixes (`_1`, `_2`) before any operations.
- **Encoding issues.** If `read_csv` raises a `UnicodeDecodeError`, retry with `encoding="latin-1"` then `encoding="cp1252"` and log which encoding succeeded.
- **Date columns with multiple formats.** When a single column contains "2024-01-15", "01/15/2024", and "Jan 15, 2024", use `pd.to_datetime(col, format="mixed")` and verify the parsed results with spot checks.
- **Numeric columns stored as strings with currency symbols.** Strip `$`, `€`, commas, and whitespace before type coercion: `df["price"].str.replace(r"[$€,\s]", "", regex=True).astype(float)`.
