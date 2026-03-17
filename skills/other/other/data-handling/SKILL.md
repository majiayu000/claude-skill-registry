---
name: data-handling
description: >
  Data handling best practices for R and Python data science analysis scripts. Use when writing
  data manipulation code, analysis pipelines, or .qmd scripts that process scientific/analytical
  data (e.g., filtering, joining, normalizing datasets). Do NOT load for general Python scripting,
  infrastructure code, or configuration management.
user-invocable: false
---

# Data Handling Best Practices

When writing data analysis code — in R or Python — follow these practices to ensure transparency, reproducibility, and catch errors early.

## 1. Organize Inputs at the Top

Group all data reads at the top of each script (or in dedicated setup/input chunks), with comments distinguishing external data from other scripts' outputs:

**R:**
```r
# --- Inputs (from other scripts) ---
mdata <- readRDS(here("outs/01_analysis/mdata.rds"))
modules <- read_tsv(here("outs/02_module_lists/modules.tsv"))

# --- Inputs (external data) ---
gene_names <- read_tsv(here("data/gene_naming/spongilla_gene_names_final.tsv"))
```

**Python:**
```python
# --- Inputs (from other scripts) ---
mdata = pd.read_parquet(PROJECT_ROOT / "outs/01_analysis/mdata.parquet")
modules = pd.read_csv(PROJECT_ROOT / "outs/02_module_lists/modules.tsv", sep="\t")

# --- Inputs (external data) ---
gene_names = pd.read_csv(PROJECT_ROOT / "data/gene_naming/spongilla_gene_names_final.tsv", sep="\t")
```

This makes dependencies self-documenting: reading the top of any script shows exactly what it needs and where those files come from. See the `script-organization` skill for full conventions.

## 2. Show Data at Key Steps

Include summaries whenever datasets are created or substantially altered.

**R:**
```r
# After loading data
data <- read_csv(here("data/raw_data.csv"))
cat("Loaded", nrow(data), "rows,", ncol(data), "columns\n")
glimpse(data)

# After major transformations
data_filtered <- data %>%
  filter(quality_score > 0.8)
cat("After quality filter:", nrow(data_filtered), "of", nrow(data), "rows retained\n")

# After joins
data_merged <- data %>%
  left_join(annotations, by = "gene_id")
cat("After annotation join:", nrow(data_merged), "rows,",
    sum(!is.na(data_merged$annotation)), "with annotations\n")
```

**Python:**
```python
# After loading data
data = pd.read_csv(PROJECT_ROOT / "data/raw_data.csv")
print(f"Loaded {len(data)} rows, {len(data.columns)} columns")
data.info()

# After major transformations
data_filtered = data.query("quality_score > 0.8")
print(f"After quality filter: {len(data_filtered)} of {len(data)} rows retained")

# After joins
data_merged = data.merge(annotations, on="gene_id", how="left")
print(f"After annotation join: {len(data_merged)} rows, "
      f"{data_merged['annotation'].notna().sum()} with annotations")
```

**When to show data:**
- After loading raw data
- After filtering or subsetting
- After joins (especially inner joins)
- After aggregation/summarization
- After normalization or transformation
- Before final output/plotting

## 3. Annotate Analytical Decisions

Interpret "analytical decisions" broadly. Any operation that transforms, scales, or interprets data should be annotated with the reasoning. Document the "why" directly in code comments or markdown.

**R:**
```r
# Normalize by library size using TMM (Robinson & Oshlack 2010)
# TMM chosen over RLE because of high proportion of zeros in sponge data
norm_factors <- calcNormFactors(dge, method = "TMM")

# Filter low-expression genes: require CPM > 1 in at least 3 samples
# Threshold based on smallest group size (n=3 per condition)
keep <- rowSums(cpm(dge) > 1) >= 3
dge <- dge[keep, ]
cat("Genes retained after expression filter:", sum(keep), "of", length(keep), "\n")
```

**Python:**
```python
# Z-score normalize per gene across samples
# Chosen over quantile normalization to preserve relative differences
from scipy import stats
data_z = data.apply(stats.zscore, axis=1)

# Filter low-abundance features: require > 0 in at least 3 samples
# Threshold based on smallest group size (n=3 per condition)
keep = (data > 0).sum(axis=1) >= 3
data_filtered = data.loc[keep]
print(f"Features retained: {keep.sum()} of {len(keep)}")
```

**What to annotate:**
- **Scaling and transformations** — log, z-score, ratios, pseudocounts
- **Normalization method** — which method and why it suits the data
- **Mathematical operations** — any formula applied to values
- **Filtering thresholds** — cutoffs and their rationale
- **Statistical model choices** — why this test/model
- **Significance cutoffs** — FDR, fold-change thresholds
- **Assumptions about the data** — what you're assuming to be true
- **Deviations from defaults** — non-standard parameters and why
- **Grouping/aggregation logic** — how replicates or samples are combined

## 4. Validate to Prevent Silent Data Loss

### Report row counts before and after joins

**R:**
```r
cat("Before join:", nrow(data), "rows\n")
data <- data %>% inner_join(other_data, by = "key")
cat("After join:", nrow(data), "rows\n")
```

**Python:**
```python
print(f"Before join: {len(data)} rows")
data = data.merge(other_data, on="key", how="inner")
print(f"After join: {len(data)} rows")
```

### Check for unmatched keys

**R:**
```r
unmatched <- data %>% anti_join(other_data, by = "key")
if (nrow(unmatched) > 0) {
  cat("WARNING:", nrow(unmatched), "rows will not match\n")
  cat("Unmatched keys:", head(unique(unmatched$key)), "...\n")
}
```

**Python:**
```python
unmatched = data[~data["key"].isin(other_data["key"])]
if len(unmatched) > 0:
    print(f"WARNING: {len(unmatched)} rows will not match")
    print(f"Unmatched keys: {unmatched['key'].unique()[:5]}...")
```

### Validate expected columns exist

**R:**
```r
required_cols <- c("id", "value", "category")
missing <- setdiff(required_cols, names(data))
if (length(missing) > 0) stop("Missing columns: ", paste(missing, collapse = ", "))
```

**Python:**
```python
required_cols = ["id", "value", "category"]
missing = set(required_cols) - set(data.columns)
if missing:
    raise ValueError(f"Missing columns: {missing}")
```

### Assert expected data characteristics

**R:**
```r
stopifnot("No data after filter" = nrow(data) > 0)
stopifnot("Unexpected NAs in key column" = !any(is.na(data$key)))
```

**Python:**
```python
assert len(data) > 0, "No data after filter"
assert data["key"].notna().all(), "Unexpected NAs in key column"
```

## 5. Hidden Sources of Data Loss

### R-specific
- `lm()`, `glm()`, `lmFit()` drop rows with NAs (complete case analysis)
- `cor()` with `use = "complete.obs"` excludes incomplete cases
- Many functions default to `na.action = na.omit`
- Factor levels dropped when subsetting
- `as.numeric()` on character introduces NAs

### Python-specific
- `pd.merge()` with `how="inner"` silently drops unmatched rows
- `df.dropna()` can remove more rows than expected if applied to wide dataframes
- `df.groupby()` excludes NA keys by default (use `dropna=False` to include)
- `df.astype(float)` on non-numeric strings raises errors (use `pd.to_numeric(errors="coerce")` — but this silently introduces NaN)
- `.value_counts()` excludes NaN by default (use `dropna=False`)
- Chained indexing (`df[condition]["col"] = val`) may fail silently — use `.loc[]`

### Both languages
- `mean()`, `sum()`, `sd()`/`std()` with NA removal (`na.rm=TRUE` / `skipna=True`) silently ignore NAs — report how many: `cat/print("NAs ignored:", sum(is.na(x)))`
- ggplot2/matplotlib removes rows with NAs or clips data outside axis limits
- Faceting/subplotting hides groups with no data

### Package-specific
- limma, DESeq2, edgeR have default filtering thresholds
- scikit-learn estimators silently handle NaN differently depending on the algorithm
- Always check documentation for implicit filtering

## 6. Quarto Document Patterns

### R

**For rendered output:** Put validation in chunks with `#| include: false` but keep summaries visible:

```r
#| label: validate-join
#| include: false
#| message: true

# Validation (hidden in output)
unmatched <- data %>% anti_join(other, by = "key")
if (nrow(unmatched) > 0) {
  message("WARNING: ", nrow(unmatched), " rows unmatched")
}
stopifnot(nrow(result) > 0)
```

```r
#| label: show-result

# Summary (visible in output)
cat("Final dataset:", nrow(result), "rows\n")
glimpse(result)
```

**Key pattern: `cat()` vs `message()`**
- `cat()` — verbose diagnostics, hidden with `include: false`
- `message()` — warnings that appear during rendering
- `print()`/`glimpse()` — data summaries, keep visible

### Python

```python
#| label: validate-join
#| include: false

# Validation (hidden in output)
unmatched = data[~data["key"].isin(other["key"])]
if len(unmatched) > 0:
    import warnings
    warnings.warn(f"{len(unmatched)} rows unmatched")
assert len(result) > 0, "No data after join"
```

```python
#| label: show-result

# Summary (visible in output)
print(f"Final dataset: {len(result)} rows")
result.info()
result.head()
```

**Key pattern: `print()` vs `warnings.warn()`**
- `print()` — diagnostics, hidden with `include: false` or kept visible
- `warnings.warn()` — warnings that surface in rendering output
- `df.info()` / `df.head()` / `df.describe()` — data summaries, keep visible

## Claude Code Behavior

### Surface Analysis Decisions — Never Resolve Ambiguities Silently

The user is a scientist who needs to understand and approve the analytical choices being made. **Do not silently resolve ambiguities or edge cases.**

**Always surface to the user before proceeding:**
- How unmatched, missing, or ambiguous data will be handled (e.g., catch-all defaults, NA treatment, edge cases that don't fit categories)
- Classification or labeling logic — show the rules AND any cases that don't cleanly match
- Filtering decisions — what gets included/excluded and why
- Any assumption about data structure that isn't explicitly documented
- Thresholds, cutoffs, or heuristics being applied

**Concretely:**
1. When categorizing data, flag cases that don't match known categories — label them as `"unmatched"` or `NA`, print them, and ask the user before assigning a default
2. When writing conditional logic (e.g., `case_when`, `if/elif/else`), show the user what falls into the catch-all/else case
3. When joining datasets, report unmatched rows on both sides
4. When a decision could reasonably go multiple ways, describe the options and ask

**Do NOT** assume the "obvious" answer is correct — what seems like a safe default may mask a real data issue. Never use a silent catch-all default that hides unmatched cases.

### Stop and Ask About Analytical Choices

Before making important analytical decisions, **stop and ask the user**. Explain the available options, trade-offs, and your recommendation. Interpret "important" broadly — when in doubt, ask.

**Always ask about:**
- **Normalization method** — TMM vs RLE vs quantile vs none; when multiple valid options exist
- **Background/reference sets** — which gene universe for GO/pathway analysis
- **Design matrix structure** — how to model experimental factors, interactions
- **Comparisons to run** — which contrasts for differential analysis
- **Filtering thresholds** — expression cutoffs, quality filters
- **Statistical tests** — parametric vs non-parametric, paired vs unpaired
- **Multiple testing correction** — FDR method, significance thresholds
- **Scaling/transformation** — log2, z-score, VSN; pseudocount values
- **Batch correction** — whether to apply, which method
- **Missing data handling** — imputation method, exclusion criteria
- **Clustering parameters** — distance metric, linkage method, number of clusters

**How to ask:**
1. Explain what decision needs to be made
2. List the main options with brief trade-offs
3. State your recommendation and why
4. Wait for user input before proceeding

### When Writing Code

1. **Include data summaries** at key transformation steps
2. **Annotate all decisions** with comments explaining the rationale
3. **Read validation output** — don't just check if command succeeded
4. **Alert the user** to warnings, unexpected counts, or suspicious patterns
5. **Summarize results** (e.g., "Join retained 450 of 500 rows, 50 unmatched")

**Do not silently proceed** if validation suggests problems or if an important analytical choice hasn't been discussed with the user.