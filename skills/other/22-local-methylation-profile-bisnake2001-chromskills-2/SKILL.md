---
name: local-methylation-profile
description: This skill analyzes the local DNA methylation profiles around target genomic regions provide by user. Use this skill when you want to vasulize the average methylation profile around target regions (e.g. TSS, CTCF peak or other target regions).
---

# Local Methylation Profile Analysis

## Overview
- **Always prompt user** for which columns in the BED files are methylation fraction/percent. Never decide by yourself.
- Generat profile: Bin methylation around regions (±flank, fixed bin size), aggregate mean±SE.
- Visualize: Plot mean profile with ribbon and center line.

---

## Inputs & Outputs

### Inputs
```bash
methylation.bed
target_regions.bed
```

### Outputs
```bash
local_methyl_profile/
  stats/
    CpG_around_target.tsv
  plots/
    CpG_around_target.pdf
  temp/
    ... # other temp file generated
```

---

## Decision Tree

### Step 1: Preprocess input → 5-column BED (for methylKit), and 3-column BED (for target regions)
```bash
awk -F'\t' 'BEGIN {OFS="\t"} {print $1, $2, $3, $<i_methylation>}, $<i_coverage>}' methylation.bed # n is provide by user, *100 if is fraction 
awk -F'\t' 'BEGIN {OFS="\t"} {print $1, $2, $3}' target_regions.bed
```
---

### Step 2: Build methylation profiles around regions

Call:
- `mcp__methyl-tools__build_local_methylation_profile`

with:

 - `methyl_bed_path`: 5-column BED-like file from preprocess_methylation.
 - `regions_bed_path`: 3-column BED-like file from preprocess_regions.
 - `output_profile_tsv_path`: path for aggregated profile table (TSV).
 - `flank_size`: flank size in bp around region center (default 2000).
 - `bin_size`: bin size in bp (default 50).
 - `min_coverage`: minimum coverage threshold for CpGs (default 10).

---

### Step 3: Visualization
Call: 
- `mcp__methyl-tools__plot_profile`

with: 

- `profile_tsv_path`: TSV from build_methylation_profile.
- `output_plot_path`: output figure path (PNG/PDF; format inferred from extension).
- `title`: plot title (optional).

---

## Parameter Guidelines

| Context   | Flank | Bin  | Min cov |
|-----------|-------|------|---------|
| TF peaks  | ±2 kb | 50bp | 10x     |
| Promoters | ±1 kb | 50bp | 10x     |
| Enhancers | ±5 kb | 100bp| 5x      |
| Motifs    | ±0.5kb| 10–20| 10x     |

## Notes
- Snippets are *usage hints* and must be adapted to your paths and column indices.
