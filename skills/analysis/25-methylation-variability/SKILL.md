---
name: methylation-variability-analysis
description: This skill provides a complete and streamlined workflow for performing methylation variability and epigenetic heterogeneity analysis from whole-genome bisulfite sequencing (WGBS) data. It is designed for researchers who want to quantify CpG-level variability across biological samples or conditions, identify highly variable CpGs (HVCs), and explore epigenetic heterogeneity.
---

# SKILL: Methylation Variability & Heterogeneity Analysis

## Overview

Main steps include:

- Refer to the **Inputs & Outputs** section to check available inputs and design the output structure.
- **Always prompt user** for genome assembly used.
- **Always prompt user** for which columns in the BED files are methylation fraction/percent and coverage and strand.
- Building a multi-sample CpG methylation matrix from WGBS coverage files.
- Computing **between-sample variability** at CpG level (variance, MAD, CV).

---

## When to use this skill

Use this methylKit-based variability pipeline when you want to:

- Quantify **between-sample variability** at CpG level (e.g., across replicates, cell types, conditions).
- Identify **highly variable CpGs (HVCs)** as candidate epigenetically heterogeneous loci.
- Explore **epigenetic heterogeneity** between groups (e.g., GM12878 vs K562, disease vs control).

---

## Inputs & Outputs

### Inputs

`<sample1>.bed`
`<sample2>.bed`

### Outputs
```bash
methylation_variability/
  stats/
    top_variable_CpGs.tsv
    CpG_variability_stats.tsv
  plots/
    heatmap_top_variable_CpGs.pdf
    distribution_CpG_variance.pdf
    mean_vs_variance_scatter.pdf
  temp/
```

---

## Decision Tree

### Step 1: Prepare the sample meta data
```r
library(methylKit)
file.list <- list(
  "sample1.cov",
  "sample2.cov",
  "sample3.cov"
)

sample.id <- list("S1", "S2", "S3")
treatment <- c(0, 1, 1)  # e.g. 0 = control, 1 = treated

# Read methylation data
myobj <- methRead(
  location = file.list,
  sample.id = sample.id,
  assembly  = "hg38", # provided by user
  treatment = treatment,
  context   = "CpG",
  pipeline = list(
    fraction = FALSE,  # percMeth is 0–100, fraction is 0-1, depend on inputs
    chr.col = 1,
    start.col = 2,
    end.col = 3,
    strand.col = 6, # provided by user
    coverage.col = 10, # provided by user
    freqC.col = 11 # provided by user
  )
)

# Optional filtering: remove low / extremely high coverage CpGs
filtered.myobj <- filterByCoverage(
  myobj,
  lo.count = 10, lo.perc = NULL,
  hi.count = 99.9, hi.perc = TRUE
)

# Unite CpGs across samples (common CpG sites)
meth <- unite(filtered.myobj, destrand = TRUE)
```
### Step 2: Statistical analysis

```r
d <- getData(meth.united)
numCs.cols <- grep("numCs", colnames(d), value = TRUE)
cov.cols   <- grep("coverage", colnames(d), value = TRUE)
pmat01 <- d[, numCs.cols] / d[, cov.cols]
pmat01 <- as.matrix(data.frame(pmat01))

var.cpg <- rowVars(pmat01, na.rm = TRUE) # Variance across samples
mad.cpg <- rowMads(pmat01, na.rm = TRUE) # Median absolute deviation (MAD)

# Coefficient of variation (CV = sd / mean)
mean.cpg <- rowMeans(pmat01, na.rm = TRUE)
sd.cpg <- sqrt(var.cpg)
cv.cpg <- sd.cpg / (mean.cpg + 1e-6)  # add small constant to avoid division by zero

# Assemble statistics table
var.stats <- data.frame(
  chr = d$chr,
  start = d$start,
  end = d$end,
  mean = mean.cpg,
  variance = var.cpg,
  MAD = mad.cpg,
  CV = cv.cpg,
  stringsAsFactors = FALSE
)

var.stats <- var.stats[order(-var.stats$variance), ] # Sort by variance (descending)

# Save full table
write.table(
  var.stats,
  file = "CpG_variability_stats.tsv",
  sep = "	",
  quote = FALSE,
  row.names = FALSE
)
```

### Step 3: high variable CpG selection

```r
topN <- 1000
top.idx <- head(order(-var.cpg), topN)

pmat.top <- pmat01[top.idx, , drop = FALSE]

# Save top-variable CpGs table
write.table(
  var.stats[match(rownames(pmat.top), rownames(var.stats)), ],
  file = "top_variable_CpGs.tsv",
  sep = "	",
  quote = FALSE,
  row.names = FALSE
)
```

### Step 4: Visualization

```r
group.factor <- factor(ifelse(treatment == 0, "GM12878", "K562"))
ha <- HeatmapAnnotation(Group = group.factor)

Heatmap(
  pmat.top,
  name = "methylation",
  show_row_names = FALSE,
  show_column_names = TRUE,
  top_annotation = ha,
  cluster_rows = TRUE,
  cluster_columns = TRUE
)

# Distribution of the CpG variability
var.df <- data.frame(
  variance = var.cpg,
  log10_variance = log10(var.cpg + 1e-8)
)

ggplot(var.df, aes(x = log10_variance)) +
  geom_histogram(bins = 50) +
  theme_minimal() +
  labs(
    title = "CpG-wise methylation variance (log10 scale)",
    x = "log10(variance + 1e-8)",
    y = "Count of CpGs"
  )

# 3. Mean vs Variance scatter plot
ggplot(var.stats, aes(x = mean_methylation, y = variance)) +
    geom_hex(bins = 50) +
    scale_fill_viridis_c(trans = "log10") +
    theme_minimal() +
    labs(
      title = "Mean Methylation vs Variance",
      x = "Mean Methylation",
      y = "Variance",
      fill = "Count (log10)"
    ) +
    theme(
      plot.title = element_text(hjust = 0.5, size = 14, face = "bold")
    )
```
---

## Recommended Extensions

- You can change 'lo.count', 'hi.perc', and 'topN' depending on coverage and dataset size.
- If you want group-wise differential variability (e.g., GM12878 vs K562),
- you can apply variance/Bartlett/Levene tests per CpG using 'pmat01' and 'treatment'.
- Add region-level annotation (promoters, gene bodies, CpG islands) using `GenomicRanges` and TxDb annotations, then compute variability at region level by aggregating CpG variability.
- Implement differential variability tests between groups (e.g., variance comparison between GM12878 and K562).
- Combine this variability pipeline with DMR analysis from methylKit to simultaneously look at mean shifts and heterogeneity.
