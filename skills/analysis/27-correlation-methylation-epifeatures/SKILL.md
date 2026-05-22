---
name: correlation-methylation-epiFeatures
description: This skill provides a complete pipeline for integrating CpG methylation data with chromatin features such as ATAC-seq signal, H3K27ac, H3K4me3, or other histone marks/TF signals.
---


# Integrative Analysis of DNA Methylation and Chromatin Features

## 1. Overview

Main steps include:
- Refer to the **Inputs & Outputs** section to check required inputs and set up the output directory structure.
- **Always prompt user** for genome assembly used.
- **Always prompt user** for which columns in the methylation BED files are methylation fraction/percent and coverage and strand.
- Load and preprocess CpG methylation data
- Tile methylation into fixed-size windows (e.g., 1kb) or in target regions.
- Import chromatin feature signal from bigWig files
- Build a unified region-level integration table
- Calculate correlations between every two features.
- Visualization

---

## 2. When to Use This Skill

Use this pipeline when you want to explore how DNA methylation relates to chromatin state, accessibility, or histone modifications. Suitable scenarios include:
- Assessing promoter/enhancer activation via methylation & ATAC/H3K27ac
- Integrating multi-omics datasets (ChIP-seq, ATAC-seq, WGBS)
- Evaluating epigenomic shifts across conditions, tissues, or celltypes

---

## 3. Inputs & Outputs

### Inputs

`<methylation_coverage>.bed`
`<epi_feature_1>.bw`
`<epi_feature_2>.bw`
`<target_regions>.bed` (optional)
`<genomic_annotation>.gtf` (optional)

### Outputs

```bash
corr_epi_methylation/
  stats/
    region_signal_table.tsv   # Unified table of methylation + chromatin signal
    correlation_table.tsv                 # Per-feature Spearman correlations
  plots/
    *.pdf                          # heatmap/scatterplot of the correlations
  temp/
```
---

## 4. Decision Tree

### STEP 1: Prepare the sample methylation data

```r
library(GenomicRanges)
library(methylKit)
meth_files <- list("sample1.cov", "sample2.cov")
sample_ids <- c("S1", "S2")

meth <- methRead(
  location = "sample.bed",
  sample.id = "S1",
  assembly = "hg38",  # provided by user
  treatment = 0,
  context = "CpG",
  pipeline = list(
    fraction = FALSE,  # percMeth is 0–100, fraction is 0-1, depend on inputs
    chr.col = 1,
    start.col = 2,
    end.col = 3,
    strand.col = 6,    # provided by user
    coverage.col = 10, # provided by user
    freqC.col = 11     # provided by user
  )
)
```

### STEP 3: Tile methylation into 1kb bins or count methylation in target regions

Option 1: no BED for target regions provided, calculate correlation in fix bin size

``` r
library(rtracklayer)
meth_tile <- tileMethylCounts(meth, win.size = 1000)
d <- getData(meth_tile)
mean_methylation <- d$numCs / (d$numCs + d$numTs)
regions <- as(meth_tile, "GRanges")
```

Option 2: Target regions provided, calculate correlation in target bins

``` r
library(rtracklayer)
bed_file <- "targets.bed"
targets <- import(bed_file, format = "BED")
meth_region <- regionCounts(meth, regions = targets)
d <- getData(meth_region)
mean_methylation <- d$numCs / (d$numCs + d$numTs)
regions     <- as(meth_region, "GRanges")  # similar to 'targets'
```

Option 3: calculate correlation in target genomic regions (e.g. promoter)
```r
library(TxDb.Hsapiens.UCSC.hg38.knownGene) # depend on the genomic assembly provide by user
library(rtracklayer)
txdb <- TxDb.Hsapiens.UCSC.hg38.knownGene
gene_gr <- genes(txdb)   # one GRanges per gene
regions <- promoters(gene_gr,  # prompt the user for the definition of promoter
                          upstream  = 2000,
                          downstream = 200)
regions <- keepStandardChromosomes(promoters_gr, pruning.mode = "coarse")

meth_region <- regionCounts(meth, regions = regions)
d <- getData(meth_region)
mean_methylation <- d$numCs / (d$numCs + d$numTs)
regions <- as(meth_region, "GRanges")  # similar to 'targets'
```

### Step 4: Build integrated region table

```r
bw_ATAC    <- "ATAC.bigWig"
bw_H3K27ac <- "H3K27ac.bigWig"
bw_H3K4me3 <- "H3K4me3.bigWig"
... # Other availabel genomic features

get_bw_mean <- function(bw_file, regions) {
  bw_list <- import(bw_file, which = regions, as = "NumericList")
  sapply(bw_list, function(x) mean(x, na.rm = TRUE))
}

ATAC_sig    <- get_bw_mean(bw_ATAC,    regions)
H3K27ac_sig <- get_bw_mean(bw_H3K27ac, regions)
H3K4me3_sig <- get_bw_mean(bw_H3K4me3, regions)

# Avoid adding the gene_id column when build the data frame here
df <- data.frame(
  seqnames = seqnames(regions),
  start = start(regions),
  end = end(regions),
  mean_methylation = mean_methylation,
  ATAC = ATAC_sig,
  H3K27ac = H3K27ac_sig,
  H3K4me3 = H3K4me3_sig
)

write.table(df, "region_signal_table.tsv", sep="\t",
            quote=FALSE, row.names=FALSE)
```


### STEP 6: Calculate correlations

```r
features_mat <- df[, c("mean_methylation", "ATAC", "H3K27ac", "H3K4me3")]
cor_mat <- cor(
  features_mat,
  use = "pairwise.complete.obs",
  method = "spearman"
)

write.table(
  cor_mat,
  "feature_correlation_tabel.tsv",
  sep = "\t",
  quote = FALSE,
  col.names = NA
)
```

### STEP 7: Visualization

```r
pdf("feature_correlation_heatmap.pdf", width = 4, height = 4)
pheatmap(
  cor_mat,
  cluster_rows = TRUE,
  cluster_cols = TRUE,
  display_numbers = TRUE,
  number_format = "%.2f",
  main = "Feature correlation"
)
dev.off()

# Scatter plots
pdf(file.path(output_dir, "plots", "methylation_epi_scatterplots.pdf"), width = 10, height = 5)
par(mfrow = c(1, 2))

# Methylation vs ATAC
plot(df_clean$mean_methylation, df_clean$ATAC,
     xlab = "Mean Methylation (%)", ylab = "ATAC-seq Signal",
     main = paste("Methylation vs ATAC-seq\nrho =", round(cor_mat["mean_methylation", "ATAC"], 3)),
     pch = 16, cex = 0.5, col = rgb(0, 0, 1, 0.3))
... # other methylation vs. feature pairs
dev.off()
```