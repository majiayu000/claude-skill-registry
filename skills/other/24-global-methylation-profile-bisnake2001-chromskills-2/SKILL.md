---  
name: global-methylation-profile 
description: This skill performs genome-wide DNA methylation profiling. It supports single-sample and multi-sample workflows to compute methylation density distributions, genomic feature distribution of the methylation profile, and sample-level clustering/PCA. Use it when you want to systematically characterize global methylation patterns from WGBS or similar per-CpG methylation call files.  
---

# Global DNA Methylation Profiling

## Overview

Main steps include:

- Refer to the **Inputs & Outputs** section to check available inputs and design the output structure.  
- **Always prompt user** for genome assembly used.
- **Always prompt user** for which columns are methylation fraction/percent and coverage and strand.
- Analyze the genomic feature distribution of methylations for each sample.
- Compute and visualize genome-wide methylation density distributions.
- For multi-sample datasets, prepare the matrix of methylation data.
- Perform PCA and hierarchical clustering to assess sample similarity based on global methylation.
- **Never use MCP tools in this skill**, use R scripts instead.
---

## When to use this skill

Use the **global-methylation-profiling** skill when you want to:

- Characterize **global DNA methylation status** of one or multiple samples (e.g. normal vs tumor, different cell types).  
- Compare broad methylation patterns across samples:  
  - Are some samples globally hypo-/hyper-methylated?  
  - Are certain chromosomes or genomic regions more strongly affected?  
- Explore genomic feature of your methylation dataset (e.g. promoter hypomethylation, gene body hypermethylation).  
- Perform **unsupervised clustering/PCA** to see if samples separate by condition based on genome-wide methylation patterns.

---

## Inputs & Outputs

### Inputs
`<sample.bed`

### Outputs

```bash
global_methylation_profile/
  stats/
    summary_statistics.tsv
    ...
  plots/
    sample1_genomic_feature_pie.pdf
    sample2_genomic_feature_pie.pdf
    ... # Other samples
    allSamples_methylation_density_overlay.pdf
    PCA_scatterplot.pdf
    sample_correlation_heatmap.pdf
    ...
  logs/
  temp/ # all the temp files
```

---

## Decision Tree

### Step 1: Prepare the sample meta data
```r
library(methylKit)
# Example input: Bismark coverage files (chr, start, end, numCs, numTs, strand)
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

### Step 2: Analyze Genomic Feature Distribution of CpGs

Annotate CpGs with genomic features (promoter, exon, intron, intergenic, etc.) with genomation and summarize where CpGs (or methylated CpGs) are located for each sample

```r
library(genomation)
library(TxDb.Hsapiens.UCSC.hg38.knownGene) # depend on user inputs
txdb <- TxDb.Hsapiens.UCSC.hg38.knownGene
# exons
exons <- unlist(exonsBy(txdb))
names(exons) <- NULL
mcols(exons)$type <- "exon"
# introns
introns <- unlist(intronsByTranscript(txdb))
names(introns) <- NULL
mcols(introns)$type <- "intron"
# promoters
promoters.gr <- promoters(txdb, upstream = 2000, downstream = 200)
names(promoters.gr) <- NULL
mcols(promoters.gr)$type <- "promoter"
# TSS（1bp）
TSSes <- promoters(txdb, upstream = 1, downstream = 1)
names(TSSes) <- NULL
mcols(TSSes)$type <- "TSS"
# 3'UTR
utr3 <- unlist(threeUTRsByTranscript(txdb))
names(utr3) <- NULL
mcols(utr3)$type <- "UTR3"
# 5'UTR
utr5 <- unlist(fiveUTRsByTranscript(txdb))
names(utr5) <- NULL
mcols(utr5)$type <- "UTR5"

gene.obj <- GRangesList(
  promoters = promoters.gr,
  exons     = exons,
  introns   = introns,
  TSSes     = TSSes
  UTR5      = utr5,
  UTR3      = utr3,
  ... # other features
)

for (i in seq_along(filtered.myobj)) {
  sample_id <- filtered.myobj[[i]]@sample.id
  cpg.gr <- as(filtered.myobj[[i]], "GRanges")
  ann.gene <- annotateWithGeneParts(cpg.gr, gene.obj)
  feature.summary <- getTargetAnnotationStats(ann.gene, percentage = TRUE)
  out_tab <- as.data.frame(feature.summary)
  write.table(
    out_tab,
    file      = file.path(plot_dir, paste0(sample_id, "_feature_annotation_stats.tsv")),
    sep       = "\t", quote = FALSE, row.names = FALSE
  )
  pdf(file.path(plot_dir, paste0(sample_id, "_genomic_feature_distribution.pdf")))
  plotTargetAnnotation(
    ann.gene,
    main = paste("Genomic feature distribution of CpGs -", sample_id)
  )
  dev.off()
}
```

Step 3: Compute & visualize genome-wide methylation density distributions

```r
# Convert to percent methylation matrix: rows = CpGs, cols = samples
meth.mat <- percMethylation(meth)  # values 0–100

df.long <- reshape2::melt(
  as.data.frame(meth.mat),
  variable.name = "Sample",
  value.name   = "Methylation"
)

ggplot(df.long, aes(x = Methylation, color = Sample)) +
  geom_density() +
  theme_bw() +
  xlab("Percent methylation") +
  ggtitle("Genome-wide methylation density across samples")
```

### Step 4: PCA & Hierarchical Clustering of Multi-sample Methylation

- Use CpG methylation profiles across samples to assess sample similarity and batch effects.

```r
# Meth matrix: rows = CpGs, cols = samples (0–100)
meth.mat <- percMethylation(meth)

# (Optional) Filter CpGs by variability
cpg.sd <- apply(meth.mat, 1, sd, na.rm = TRUE)
keep.var <- cpg.sd > 0
meth.var <- meth.mat[keep.var, ]
if (sum(keep.var) > 10000) {
  keep.idx <- order(cpg.sd[keep.var], decreasing = TRUE)[1:10000]
  meth.var <- meth.var[keep.idx, ]
}

# Z-score transformation (per CpG) – helps clustering
meth.scaled <- t(scale(t(meth.var)))  # rows scaled

pca <- prcomp(t(meth.scaled), center = FALSE, scale. = FALSE)
pca.df <- data.frame(
  Sample = colnames(meth.scaled),
  PC1 = pca$x[, 1],
  PC2 = pca$x[, 2],
  Treatment = factor(treatment, labels = c("Control", "Treatment"))
)

ggplot(pca.df, aes(x = PC1, y = PC2, color = Treatment, label = Sample)) +
  geom_point(size = 3) +
  geom_text(vjust = -1) +
  theme_bw() +
  ggtitle("PCA of global CpG methylation") +
  xlab(paste0("PC1 (", round(summary(pca)$importance[2, 1] * 100, 1), "%)")) +
  ylab(paste0("PC2 (", round(summary(pca)$importance[2, 2] * 100, 1), "%)"))

dist.samples <- dist(t(meth.scaled), method = "euclidean")
hc <- hclust(dist.samples, method = "complete")

plot(hc, main = "Hierarchical clustering of samples (methylation)",
     xlab = "", sub = "")

cor.samples <- cor(meth.var, use = "pairwise.complete.obs")

pheatmap(cor.samples,
         clustering_method = "complete",
         main = "Sample correlation based on CpG methylation")
```