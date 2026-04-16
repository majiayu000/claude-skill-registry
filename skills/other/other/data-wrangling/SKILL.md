---
name: data-wrangling
description: Data cleaning, transformation, reshaping, joins, missing data handling, and tidy data principles. Covers the full pipeline from raw ingestion to analysis-ready datasets -- type coercion, deduplication, outlier detection, normalization, melting/pivoting, regex extraction, and reproducible transformation chains. Use when preparing, cleaning, or transforming data for analysis.
type: skill
category: data-science
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/data-science/data-wrangling/SKILL.md
superseded_by: null
---
# Data Wrangling

Data wrangling is the work that sits between raw data and analysis -- the unglamorous, indispensable practice of making data trustworthy. Estimates vary, but practitioners consistently report that 60-80% of analysis time is spent wrangling. This skill covers the principles and techniques of data cleaning, transformation, reshaping, and integration, grounded in Hadley Wickham's tidy data framework and extended to the realities of messy real-world datasets.

**Agent affinity:** tukey (EDA-driven cleaning), nightingale (routing wrangling tasks)

**Concept IDs:** data-data-sources, data-data-quality, data-sampling-bias

## The Wrangling Pipeline

| Stage | Goal | Key operations |
|---|---|---|
| 1. Ingestion | Get data into a working environment | Read CSV/JSON/Parquet/SQL, handle encodings, parse dates |
| 2. Profiling | Understand what you have | Shape, dtypes, nulls, distributions, cardinality |
| 3. Cleaning | Fix structural problems | Dedup, type coercion, standardize categories, fix encodings |
| 4. Missing data | Handle gaps | Detect patterns (MCAR/MAR/MNAR), impute or flag |
| 5. Transformation | Derive analysis-ready features | Normalize, bin, log-transform, create indicators |
| 6. Reshaping | Match the analysis structure | Melt, pivot, tidy form, denormalize |
| 7. Integration | Combine sources | Joins (inner/left/right/full/cross), concatenation, dedup post-join |
| 8. Validation | Confirm readiness | Schema checks, assertion tests, row-count reconciliation |

## Tidy Data Principles

Hadley Wickham (2014) formalized "tidy data" as three rules:

1. **Each variable forms a column.** A single column should contain values of exactly one variable.
2. **Each observation forms a row.** A single row should contain all values for exactly one observational unit.
3. **Each type of observational unit forms a table.** Mixing patient demographics and lab results in one table violates this rule.

Most messy datasets violate one or more of these rules in predictable ways:

| Violation | Example | Fix |
|---|---|---|
| Column headers are values, not variable names | Columns: `income_2020`, `income_2021`, `income_2022` | Melt to columns: `year`, `income` |
| Multiple variables stored in one column | `"M-25"` encodes both sex and age | Split into `sex` and `age` columns |
| Variables stored in both rows and columns | Pivot table with row headers as categories | Melt and re-pivot to tidy form |
| Multiple types in one table | Patient info mixed with visit records | Normalize into two related tables |
| One type spread across multiple tables | Monthly CSV files with identical schema | Concatenate with a `month` column |

Tidy data is not the only valid structure -- wide formats are sometimes more efficient for computation or display. But tidy form is the canonical starting point for analysis, and most tools (ggplot2, pandas groupby, SQL aggregation) assume it.

## Cleaning Techniques

### Type Coercion

Raw data arrives as strings. Coercion converts to the correct type:

- **Numeric:** Strip currency symbols, commas, whitespace. Handle locale-specific decimals (`,` vs `.`). Flag non-numeric values rather than silently converting to NaN.
- **Dates:** Parse with explicit format strings, never rely on automatic detection. Time zones matter -- store in UTC, display in local.
- **Categorical:** Standardize case, strip whitespace, map synonyms (`"USA"`, `"US"`, `"United States"` -> `"US"`). Use controlled vocabularies where possible.
- **Boolean:** Map common representations (`"yes"/"no"`, `"1"/"0"`, `"true"/"false"`, `"Y"/"N"`) to a single canonical form.

### Deduplication

Exact duplicates are trivial to detect. The hard cases are near-duplicates:

- **Record linkage:** When the same entity appears with slight variations (`"John Smith"` vs `"J. Smith"` vs `"SMITH, JOHN"`). Use fuzzy matching (Levenshtein distance, phonetic encoding) with a human-reviewed threshold.
- **Temporal duplicates:** The same event recorded at slightly different timestamps. Define a dedup window and keep the first/last/most-complete record.
- **Key discipline:** Always define what constitutes a unique observation before deduplication. A table of purchases has a different uniqueness key than a table of customers.

### Outlier Detection

Outliers are not errors -- they are values that warrant investigation:

- **Statistical:** Values beyond 1.5 * IQR (Tukey's fences), or beyond 3 standard deviations. These thresholds are guidelines, not laws.
- **Domain-based:** A human age of 150 is an error. A human age of 95 is unusual but valid. Domain knowledge trumps statistical rules.
- **Multivariate:** A value can be normal on each variable individually but extreme in combination (e.g., age 25 with 40 years of work experience). Mahalanobis distance or isolation forests detect these.

**Action on outliers:** Investigate first. If the value is a data entry error, correct it. If it is a measurement error, flag it. If it is a genuine extreme value, keep it and note its influence on summary statistics.

## Missing Data

### Missing Data Mechanisms

Rubin (1976) classified three mechanisms:

| Mechanism | Definition | Example | Implication |
|---|---|---|---|
| **MCAR** | Missingness is unrelated to any variable | Lab sample randomly dropped | Safe to drop or impute; no bias |
| **MAR** | Missingness depends on observed variables | High-income respondents skip income question less often | Imputation using observed predictors is valid |
| **MNAR** | Missingness depends on the missing value itself | People with depression less likely to report depression severity | No imputation is fully valid; requires sensitivity analysis |

### Handling Strategies

| Strategy | When to use | Trade-off |
|---|---|---|
| **Listwise deletion** | MCAR, small fraction missing (<5%) | Simple but loses observations |
| **Pairwise deletion** | MCAR, different analyses need different subsets | Keeps more data but correlation matrices may not be positive-definite |
| **Mean/median imputation** | Quick exploration only | Reduces variance, biases correlations toward zero |
| **Regression imputation** | MAR, continuous variables | Better than mean but inflates R-squared |
| **Multiple imputation** | MAR, formal inference | Gold standard; accounts for imputation uncertainty |
| **Indicator method** | Any mechanism, tree-based models | Add a binary "was_missing" column; let the model learn missingness patterns |
| **Domain-specific fill** | Known defaults | "No response" for surveys, 0 for counts that should exist |

## Joins and Integration

### Join Types

| Join | Keeps | Use when |
|---|---|---|
| **Inner** | Rows matching in both tables | You only want complete matches |
| **Left** | All rows from left, matching from right | Left table is the primary; right is enrichment |
| **Right** | All rows from right, matching from left | Symmetric to left join |
| **Full outer** | All rows from both | You need the complete picture of both sources |
| **Cross** | Every combination of left and right rows | Generating all pairs (e.g., all product-store combinations) |
| **Anti** | Left rows with NO match in right | Finding orphans or gaps |

### Join Hazards

- **Many-to-many joins:** Produce a Cartesian product of matching rows. Row count explodes. Always check cardinality before joining.
- **Key mismatches:** Different key formats (`"001"` vs `1`), trailing whitespace, case differences. Standardize keys before joining.
- **Null keys:** NULLs never match other NULLs in standard SQL joins. Decide how to handle null-keyed rows explicitly.
- **Post-join dedup:** Joins can introduce duplicates when key relationships are not 1:1. Validate row counts after every join.

## Transformation Techniques

### Normalization and Scaling

| Method | Formula | Use when |
|---|---|---|
| **Min-max** | (x - min) / (max - min) | Need values in [0, 1]; distribution shape preserved |
| **Z-score** | (x - mean) / std | Need zero-centered data; assumes roughly normal |
| **Robust scaling** | (x - median) / IQR | Outliers present; median/IQR resistant to extremes |
| **Log transform** | log(x + 1) | Right-skewed data; multiplicative relationships |

### Binning and Discretization

- **Equal-width:** Divide range into n bins of equal size. Simple but poor for skewed data.
- **Equal-frequency (quantile):** Each bin contains approximately the same number of observations. Better for skewed data.
- **Domain-driven:** Age groups (0-17, 18-34, 35-54, 55+), income brackets, clinical thresholds. Always preferred when domain knowledge exists.

### Feature Engineering

Feature engineering is the creative step where domain knowledge becomes computable:

- **Date decomposition:** Extract year, month, day-of-week, is-weekend, days-since-event.
- **Text extraction:** Regex for structured patterns (phone numbers, ZIP codes, email domains).
- **Interaction terms:** Product of two variables when their combination matters (e.g., age * income).
- **Aggregation:** Group-level statistics (customer's average order size, store's monthly variance).
- **Lag features:** Previous period's value for time series (yesterday's temperature, last month's sales).

## Reproducibility

A wrangling pipeline is only trustworthy if it is reproducible:

1. **Script everything.** No manual Excel edits. Every transformation is code.
2. **Version raw data.** Hash or checksum the input files. If the raw data changes, the pipeline should detect it.
3. **Document assumptions.** Why did you impute with median instead of mean? Why did you drop rows with more than 50% missing? Write it down.
4. **Test transformations.** Assert expected row counts, column types, value ranges, and null counts at each stage.
5. **Separate raw from derived.** Never overwrite raw data. Produce a new file or table at each stage.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Imputing before exploring | You do not know the missingness mechanism | Profile first, then choose strategy |
| Joining without checking cardinality | Many-to-many join silently explodes row count | Check key uniqueness before joining |
| Dropping outliers without investigation | Outliers may be the most important observations | Investigate, then decide |
| Mixing cleaning and analysis | Impossible to reproduce or audit | Separate wrangling script from analysis |
| Ignoring encoding issues | Garbled text, silent data loss | Specify encoding explicitly at ingestion |
| Normalizing before train/test split | Data leakage -- test set statistics influence training | Fit scaler on training data only |

## Cross-References

- **tukey agent:** Exploratory data analysis techniques that drive cleaning decisions. Primary agent for profiling and outlier investigation.
- **breiman agent:** Machine learning pipelines that consume wrangled data. Feature engineering feeds directly into model training.
- **fisher agent:** Experimental design that determines what data needs collecting and how.
- **statistical-modeling skill:** Regression and inference methods that require clean, properly typed data.
- **ethics-governance skill:** Privacy and consent considerations during data collection and integration.

## References

- Wickham, H. (2014). "Tidy Data." *Journal of Statistical Software*, 59(10), 1-23.
- Rubin, D. B. (1976). "Inference and Missing Data." *Biometrika*, 63(3), 581-592.
- Van Buuren, S. (2018). *Flexible Imputation of Missing Data*. 2nd edition. CRC Press.
- Dasu, T. & Johnson, T. (2003). *Exploratory Data Mining and Data Cleaning*. Wiley.
- Tukey, J. W. (1977). *Exploratory Data Analysis*. Addison-Wesley.
