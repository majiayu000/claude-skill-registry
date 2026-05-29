---
name: sampleinfo
description: The SampleInfo process is the pipeline entry point that reads sample metadata files, performs statistical analyses, and generates visualization reports.
---

# SampleInfo Process Configuration

## Purpose
The SampleInfo process is the pipeline entry point that reads sample metadata files, performs statistical analyses, and generates visualization reports.

## When to Use
- **Always required** as first process unless using `LoadingRNAFromSeurat`
- When you have sample metadata in CSV/TSV format
- When you need to generate statistical summaries and visualizations
- When you want to add or transform metadata columns before downstream analysis

**Note**: Mutually exclusive with `LoadingRNAFromSeurat`.

## Configuration Structure

```toml
[SampleInfo]
cache = true

[SampleInfo.in]
infile = "path/to/sample_info.txt"  # Required: yes (unless using LoadingRNAFromSeurat)

[SampleInfo.envs]
sep = "\t"                  # str - File separator
mutaters = {}                # dict - Column transformations using R expressions
save_mutated = false         # bool - Save mutated columns to output
exclude_cols = "TCRData,BCRData,RNAData"  # Columns hidden in report
defaults = { plot_type = "bar", more_formats = [], save_code = false }
stats = {}                   # dict - Statistical plot definitions
```

**Required input columns:** `Sample` (unique ID), `RNAData` (directory path)
**Optional columns:** `TCRData`, `BCRData`, additional metadata
**Data format:** CSV/TSV with header, RNA data must be `Read10X()`-compatible

### Environment Variables

**`sep` (string)**: Field separator - `"\t"`, `","`, `";"`, or any character

**`mutaters` (dict)**: R expressions for `dplyr::mutate()`. Keys are column names, values are R expressions.
- Example: `mutaters = { "AgeGroup" = "ifelse(Age > 60, 'Senior', 'Adult')" }`
- Special function `paired()` identifies paired samples: `paired(., 'PatientID', 'Timepoint', c('T1', 'T2'))`

**`save_mutated` (bool)**: Save mutated columns to output file. Factor columns lose level ordering when saved as text.

**`exclude_cols` (str/list)**: Comma-separated string or list of columns to exclude from report table.

**`defaults` (dict)**: Default plot parameters inherited by all plots:
```toml
[SampleInfo.envs.defaults]
plot_type = "bar"           # Plot type (see External References)
more_formats = []            # Additional formats: ["pdf", "svg"]
save_code = false            # Save R code and data
subset = null                # dplyr::filter expression
section = null               # Report section name
descr = null                 # Plot description
width = null, height = null, res = 100  # Plot dimensions
```

**`stats` (dict)**: Plot definitions. Keys are case names (titles), values inherit from `defaults`.

## External References

### Plotthis Functions

| plot_type | Function | Description |
|-----------|----------|-------------|
| `pie` | `PieChart()` | Pie chart |
| `bar` | `BarPlot()` | Bar plot |
| `box` | `BoxPlot()` | Box plot |
| `violin` | `ViolinPlot()` | Violin plot |
| `histogram` | `Histogram()` | Histogram |
| `density` | `DensityPlot()` | Density plot |
| `scatter` | `ScatterPlot()` | Scatter plot |
| `line` | `LinePlot()` | Line plot |
| `ridge` | `RidgePlot()` | Ridge plot |
| `heatmap` | `Heatmap()` | Heatmap |

**Full reference**: https://pwwang.github.io/plotthis/reference/

### Common Plot Parameters

```toml
x = "column_name", y = "column_name"  # Axis columns
split_by = "column_name", facet_by = "column_name"  # Split/facet
palette = "Paired", alpha = 1.0  # Color and transparency
title = "Plot Title", nrow = 2, ncol = 3  # Layout
legend.position = "right"  # Legend placement
```

### dplyr::filter() for `subset`

```toml
subset = "Sample == 'A'"
subset = "Age > 60"
subset = "Diagnosis %in% c('Colitis', 'Control')"
subset = "Sex == 'F' & Age > 50"
```

## Configuration Examples

### Minimal Configuration
```toml
[SampleInfo.in]
infile = "samples.txt"
```

### Basic Statistics
```toml
[SampleInfo.in]
infile = "sample_info.txt"

[SampleInfo.envs.stats."Samples_per_Diagnosis"]
plot_type = "bar"
x = "Sample"
split_by = "Diagnosis"
```

### Advanced Configuration
```toml
[SampleInfo.in]
infile = "metadata/samples.tsv"

[SampleInfo.envs]
save_mutated = true
mutaters = { "AgeGroup" = "ifelse(Age > 60, 'Senior', 'Adult')" }

[SampleInfo.envs.stats."N_Samples_per_Diagnosis"]
x = "Sample"
split_by = "Diagnosis"

[SampleInfo.envs.stats."Age_distribution"]
plot_type = "histogram"
x = "Age"
```

## Common Patterns

### Paired Sample Identification
```toml
[SampleInfo.envs]
mutaters = { "PairID" = "paired(., 'PatientID', 'Timepoint', c('T1', 'T2'))" }

[SampleInfo.envs.stats."Paired_Samples"]
x = "PairID"
subset = "!is.na(PairID)"
```

### Subset Analysis
```toml
[SampleInfo.envs.stats."Controls_Only"]
x = "Sample"
split_by = "Diagnosis"
subset = "Diagnosis == 'Control'"
```

## Dependencies

- **Upstream**: None (entry point process)
- **Downstream**: All pipeline processes depend on SampleInfo output
  - `SeuratPreparing`: Reads sample metadata
  - `ScRepLoading`: Uses TCRData/BCRData columns
  - All downstream: Use metadata columns for analysis

## Validation Rules

### Common Errors

1. **Missing input file**: Always specify `[SampleInfo.in.infile]`
2. **Invalid separator**: Match separator to file format (e.g., `sep = ","` for CSV)
3. **Missing required columns**: Ensure `Sample` and `RNAData` columns exist
4. **Factor level ordering**: Don't use `save_mutated` for factor columns - use `SeuratPreparing.envs.mutaters` instead

### Value Constraints

- `sep`: Single character string
- `mutaters`: Valid R expressions
- `stats` keys: Must be unique case names
- `devpars.res`: Positive integer (default: 100)

## Troubleshooting

- **Issue**: SampleInfo re-runs entire pipeline on parameter change
  **Solution**: Set `cache = "force"` at pipeline level and `[SampleInfo] cache = false`

- **Issue**: Factor levels appear in wrong order
  **Solution**: Use `SeuratPreparing.envs.mutaters` for factor columns

- **Issue**: Plots don't show expected data
  **Solution**: Check column names in `x`, `y`, `split_by` match input file exactly

- **Issue**: Paired sample function returns `NA` values
  **Solution**: Use `uniq = false` in `paired()` or adjust `idents` parameter

- **Issue**: Mutations not saved for downstream use
  **Solution**: Set `save_mutated = true`. For Seurat metadata, use `SeuratPreparing.envs.mutaters`

- **Issue**: Plot type not recognized
  **Solution**: Ensure `plot_type` is lowercase and maps to a plotthis function
