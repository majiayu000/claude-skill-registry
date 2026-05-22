---
name: peak-annotation
description: "Guide for annotating ENCODE peaks with genomic features using ChIPseeker and GREAT. Use when users need to assign peaks to genes, determine genomic feature distribution (promoter, intron, intergenic), or perform gene ontology enrichment of peak-associated genes. Trigger on: peak annotation, ChIPseeker, GREAT, peak to gene, genomic feature, promoter enrichment, gene ontology, peak distribution, TSS distance, nearest gene."
---

# Peak Annotation of ENCODE Data

## When to Use

- User wants to annotate genomic peaks with nearby genes, regulatory features, or functional categories
- User asks about "peak annotation", "ChIPseeker", "gene assignment", or "peak-to-gene mapping"
- User needs to classify peaks as promoter, enhancer, intronic, intergenic, etc.
- User wants to run GO/pathway enrichment on genes near their peaks
- Example queries: "annotate my H3K27ac peaks with nearby genes", "what genes are near these ATAC-seq peaks?", "run pathway analysis on peak-associated genes"

Help the user annotate ENCODE peak calls with genomic features and functional enrichment. Peak annotation bridges the gap between regulatory elements (peaks) and biological function (genes, pathways). This skill covers two complementary approaches: ChIPseeker for genomic feature annotation and visualization, and GREAT for functional enrichment analysis of non-coding regions.

## Literature Foundation

| Reference | Journal | Key Contribution | DOI | Citations |
|-----------|---------|-----------------|-----|-----------|
| Yu et al. (2015) | Bioinformatics | ChIPseeker: R/Bioconductor package for ChIP peak annotation, comparison, and visualization | [10.1093/bioinformatics/btv145](https://doi.org/10.1093/bioinformatics/btv145) | ~3,200 |
| McLean et al. (2010) | Nature Biotechnology | GREAT: Genomic Regions Enrichment of Annotations Tool; assigns biological meaning to cis-regulatory regions using basal+extension gene association | [10.1038/nbt.1630](https://doi.org/10.1038/nbt.1630) | ~2,800 |
| Zhu et al. (2010) | BMC Bioinformatics | ChIPpeakAnno: Bioconductor package for ChIP-seq/ChIP-chip annotation; pioneered peak-gene association | [10.1186/1471-2105-11-237](https://doi.org/10.1186/1471-2105-11-237) | ~1,200 |
| Tanigawa et al. (2022) | PLOS Computational Biology | rGREAT: R/Bioconductor interface to GREAT; enables programmatic enrichment analysis | [10.1371/journal.pcbi.1010378](https://doi.org/10.1371/journal.pcbi.1010378) | ~80 |
| Amemiya et al. (2019) | Scientific Reports | ENCODE Blacklist: artifact regions to exclude before annotation to avoid spurious gene associations | [10.1038/s41598-019-45839-z](https://doi.org/10.1038/s41598-019-45839-z) | ~1,372 |

## Prerequisites: Obtaining ENCODE Peaks

Search for and download peak files before annotation:

```
encode_search_experiments(
    assay_title="Histone ChIP-seq",
    target="H3K27ac",
    organ="pancreas",
    biosample_type="tissue"
)

encode_list_files(
    experiment_accession="ENCSR...",
    file_format="bed",
    output_type="IDR thresholded peaks",
    assembly="GRCh38",
    preferred_default=True
)

encode_download_files(
    file_accessions=["ENCFF..."],
    download_dir="/data/peak_annotation/"
)
```

**Pre-annotation filtering**: Always remove blacklisted regions before annotation:

```bash
bedtools intersect -a peaks.narrowPeak -b hg38-blacklist.v2.bed -v > peaks_clean.narrowPeak
```

## Part 1: ChIPseeker Annotation

ChIPseeker (Yu et al. 2015) annotates peaks with genomic features (promoter, UTR, exon, intron, intergenic) and provides publication-ready visualizations of the annotation distribution.

### 1a. Basic Annotation Workflow

```r
library(ChIPseeker)
library(TxDb.Hsapiens.UCSC.hg38.knownGene)
library(org.Hs.eg.db)
library(clusterProfiler)

# Load peak file
peaks <- readPeakFile("H3K27ac_peaks_clean.narrowPeak")

# Set transcript database (must match genome assembly)
txdb <- TxDb.Hsapiens.UCSC.hg38.knownGene

# Annotate peaks with genomic features
peakAnno <- annotatePeak(
    peaks,
    TxDb = txdb,
    annoDb = "org.Hs.eg.db",
    level = "gene",
    tssRegion = c(-3000, 3000)
)

# View annotation summary
peakAnno
```

### 1b. Understanding Annotation Categories

ChIPseeker classifies each peak into one genomic feature based on priority:

| Priority | Feature | Definition |
|----------|---------|------------|
| 1 | Promoter | Within TSS region (default: TSS +/- 3kb) |
| 2 | 5' UTR | Overlapping 5' untranslated region |
| 3 | 3' UTR | Overlapping 3' untranslated region |
| 4 | Exon | Overlapping exonic sequence |
| 5 | Intron | Within intronic sequence |
| 6 | Downstream | Within 3kb downstream of gene end |
| 7 | Distal Intergenic | Everything else (>3kb from any gene) |

Each peak receives exactly one annotation based on the highest-priority feature it overlaps.

**Promoter sub-categories**: ChIPseeker can further subdivide promoter peaks:

```r
peakAnno <- annotatePeak(
    peaks,
    TxDb = txdb,
    annoDb = "org.Hs.eg.db",
    level = "gene",
    tssRegion = c(-3000, 3000),
    # Subdivide promoter into bins
    genomicAnnotationPriority = c(
        "Promoter", "5UTR", "3UTR", "Exon", "Intron", "Downstream", "Intergenic"
    )
)
```

### 1c. Visualization Functions

ChIPseeker provides several publication-ready visualization functions:

**Genomic Feature Distribution Bar Plot**:
```r
plotAnnoBar(peakAnno) +
    theme_minimal(base_size = 14) +
    ggtitle("H3K27ac Genomic Feature Distribution")
ggsave("annotation_barplot.pdf", width = 10, height = 5)
```

**Genomic Feature Distribution Pie Chart**:
```r
plotAnnoPie(peakAnno)
```

**Distance to TSS Distribution**:
```r
plotDistToTSS(
    peakAnno,
    title = "H3K27ac Distance to Nearest TSS"
) + theme_minimal(base_size = 14)
ggsave("tss_distance.pdf", width = 8, height = 5)
```

**Peak Coverage Across Chromosomes**:
```r
covplot(peaks, weightCol = "V5") +
    ggtitle("H3K27ac Peak Coverage")
ggsave("chromosome_coverage.pdf", width = 12, height = 6)
```

**TSS-Centered Heatmap**:
```r
# Tag matrix around TSS
tagMatrix <- getTagMatrix(peaks, windows = promoter)
tagHeatmap(tagMatrix, xlim = c(-3000, 3000), color = "#FF8000")
```

### 1d. Extracting Annotated Gene Lists

```r
# Convert annotation to data frame
anno_df <- as.data.frame(peakAnno)

# Get genes associated with promoter peaks
promoter_genes <- anno_df[grepl("Promoter", anno_df$annotation), "SYMBOL"]
promoter_genes <- unique(promoter_genes[!is.na(promoter_genes)])

# Get all annotated genes (any feature overlap)
all_genes <- unique(anno_df$SYMBOL[!is.na(anno_df$SYMBOL)])

# Export for downstream analysis
write.csv(anno_df, "peak_annotations.csv", row.names = FALSE)
write.table(promoter_genes, "promoter_genes.txt",
            row.names = FALSE, col.names = FALSE, quote = FALSE)
```

### 1e. Gene Ontology Enrichment with clusterProfiler

After extracting gene lists, perform GO enrichment:

```r
# Convert gene symbols to Entrez IDs
gene_ids <- bitr(promoter_genes, fromType = "SYMBOL",
                 toType = "ENTREZID", OrgDb = org.Hs.eg.db)

# GO Biological Process enrichment
ego <- enrichGO(
    gene = gene_ids$ENTREZID,
    OrgDb = org.Hs.eg.db,
    ont = "BP",
    pAdjustMethod = "BH",
    pvalueCutoff = 0.05,
    qvalueCutoff = 0.05,
    readable = TRUE
)

# Visualize enrichment
dotplot(ego, showCategory = 20) +
    ggtitle("GO Biological Process Enrichment")
ggsave("go_enrichment.pdf", width = 10, height = 8)

# KEGG pathway enrichment
ekegg <- enrichKEGG(
    gene = gene_ids$ENTREZID,
    organism = "hsa",
    pvalueCutoff = 0.05
)
```

## Part 2: GREAT Enrichment

GREAT (McLean et al. 2010) assigns biological meaning to sets of non-coding genomic regions. Unlike ChIPseeker (which annotates individual peaks to nearest genes), GREAT uses a sophisticated gene association rule that accounts for gene density variation across the genome.

### 2a. GREAT Gene Association Rules

GREAT associates genomic regions to genes using a "basal plus extension" rule:

1. **Basal domain**: Each gene gets a default regulatory domain of 5kb upstream and 1kb downstream of the TSS
2. **Extension**: The basal domain extends up to 1Mb in both directions until it encounters another gene's basal domain
3. **Curated domains**: Known regulatory domains from the literature override the default rules

This approach is superior to simple nearest-gene assignment because it accounts for the fact that genes in gene-dense regions have smaller regulatory domains than genes in gene-poor regions.

### 2b. GREAT Web Interface

For quick analysis, use the GREAT web interface at http://great.stanford.edu/great/public/html/:

1. Upload BED file of peaks (hg38 assembly)
2. Select "Basal plus extension" association rule (default)
3. Select ontologies: GO, MSigDB Hallmark, Mouse Phenotype
4. Review enrichment tables and association plots

### 2c. rGREAT: Programmatic R Interface

For reproducible, scriptable analysis, use the rGREAT package (Tanigawa et al. 2022):

```r
library(rGREAT)

# Submit job to GREAT server
# For GREAT v4.0.4 with local computation:
peaks_gr <- import("H3K27ac_peaks_clean.narrowPeak")

great_job <- submitGreatJob(
    peaks_gr,
    species = "hg38",
    version = "4.0.4"
)

# Retrieve enrichment results
go_bp <- getEnrichmentTables(great_job, ontology = "GO Biological Process")
go_mf <- getEnrichmentTables(great_job, ontology = "GO Molecular Function")
msigdb <- getEnrichmentTables(great_job, ontology = "MSigDB Hallmark")

# View top results
head(go_bp[[1]], 20)

# Plot region-gene association statistics
plotRegionGeneAssociationGraphs(great_job)
```

### 2d. Local GREAT Analysis with rGREAT

For offline analysis without the GREAT server:

```r
library(rGREAT)

# Local GREAT analysis (no server required)
great_local <- great(
    peaks_gr,
    gene_sets = "msigdb:h",  # MSigDB Hallmark gene sets
    tss_source = "txdb:TxDb.Hsapiens.UCSC.hg38.knownGene",
    biomart_dataset = NULL
)

# Get enrichment table
enrichment <- getEnrichmentTable(great_local)
head(enrichment[order(enrichment$p_adjust), ], 20)
```

### 2e. GREAT vs ChIPseeker: When to Use Which

| Feature | ChIPseeker | GREAT |
|---------|-----------|-------|
| **Primary purpose** | Annotate individual peaks | Functional enrichment of peak sets |
| **Gene association** | Nearest gene or overlapping feature | Basal+extension rule (more sophisticated) |
| **Output** | Per-peak annotation + visualizations | Pathway/ontology enrichment |
| **Best for** | "Where are my peaks?" | "What do my peaks regulate?" |
| **Statistical test** | None (descriptive annotation) | Binomial + hypergeometric tests |
| **Handles distal peaks** | Assigns to "Distal Intergenic" | Associates with distant genes via extension rule |

Use ChIPseeker first to understand the genomic distribution of peaks, then GREAT to determine functional significance.

## Part 3: Comparing Peak Sets

### 3a. Venn Diagram of Peak Overlaps

```r
library(ChIPseeker)

# Load multiple peak sets
peaks_H3K27ac <- readPeakFile("H3K27ac_peaks.narrowPeak")
peaks_H3K4me3 <- readPeakFile("H3K4me3_peaks.narrowPeak")
peaks_ATAC <- readPeakFile("ATAC_peaks.narrowPeak")

peak_list <- list(
    H3K27ac = peaks_H3K27ac,
    H3K4me3 = peaks_H3K4me3,
    ATAC = peaks_ATAC
)

# Venn diagram of overlaps
vennplot(peak_list)
```

### 3b. Comparing Genomic Feature Distributions

Compare the annotation profiles of different peak sets:

```r
# Annotate each peak set
anno_H3K27ac <- annotatePeak(peaks_H3K27ac, TxDb = txdb, level = "gene")
anno_H3K4me3 <- annotatePeak(peaks_H3K4me3, TxDb = txdb, level = "gene")
anno_ATAC <- annotatePeak(peaks_ATAC, TxDb = txdb, level = "gene")

anno_list <- list(
    H3K27ac = anno_H3K27ac,
    H3K4me3 = anno_H3K4me3,
    ATAC = anno_ATAC
)

# Side-by-side annotation comparison
plotAnnoBar(anno_list) +
    theme_minimal(base_size = 14) +
    ggtitle("Genomic Feature Distribution Comparison")
ggsave("annotation_comparison.pdf", width = 12, height = 6)

# Compare distance to TSS
plotDistToTSS(anno_list) +
    theme_minimal(base_size = 14)
ggsave("tss_distance_comparison.pdf", width = 10, height = 6)
```

**Expected patterns**:
| Mark | Expected Distribution |
|------|----------------------|
| H3K4me3 | Predominantly promoter (60-80%) |
| H3K27ac | Mixed promoter (30-40%) and distal enhancer (40-50%) |
| H3K4me1 | Predominantly distal intergenic (enhancer, 50-70%) |
| ATAC-seq | Mixed: promoter + enhancer + other accessible sites |
| CTCF | Distributed across features; enriched at insulator elements |

### 3c. Differential Peak Annotation

For peaks that are condition-specific (e.g., gained or lost after treatment):

```r
# Annotate gained and lost peaks separately
gained_peaks <- readPeakFile("gained_peaks.bed")
lost_peaks <- readPeakFile("lost_peaks.bed")

anno_gained <- annotatePeak(gained_peaks, TxDb = txdb, level = "gene")
anno_lost <- annotatePeak(lost_peaks, TxDb = txdb, level = "gene")

# Compare annotations
plotAnnoBar(list(Gained = anno_gained, Lost = anno_lost)) +
    ggtitle("Genomic Features of Differential Peaks")

# Run GREAT on each set separately
great_gained <- submitGreatJob(gained_peaks, species = "hg38")
great_lost <- submitGreatJob(lost_peaks, species = "hg38")
```

## Full Workflow

```
Step 1: Download ENCODE peaks
    encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K27ac")
    encode_list_files(..., output_type="IDR thresholded peaks", assembly="GRCh38")
    encode_download_files(...)

Step 2: Pre-filter peaks
    Remove blacklisted regions (bedtools intersect -v)
    Optionally filter by signal threshold

Step 3: ChIPseeker annotation
    annotatePeak() for genomic feature classification
    plotAnnoBar(), plotDistToTSS(), covplot() for visualization
    Extract gene lists from annotations

Step 4: GREAT functional enrichment
    submitGreatJob() or local great() analysis
    Review GO, MSigDB, and phenotype enrichments
    Plot region-gene association statistics

Step 5: Compare conditions (if applicable)
    Annotate each peak set separately
    Compare annotation distributions
    Run GREAT on differential peak sets

Step 6: Document provenance
    encode_log_derived_file(
        file_path="/data/peak_annotations.csv",
        source_accessions=["ENCSR..."],
        description="ChIPseeker annotation of H3K27ac peaks in pancreatic islets",
        tool_used="ChIPseeker v1.34.0, TxDb.Hsapiens.UCSC.hg38.knownGene",
        parameters="tssRegion=c(-3000,3000), level=gene"
    )
```

## Common Pitfalls

1. **TSS database version mismatch**: The transcript database (TxDb) MUST match the genome assembly used for peak calling. For GRCh38/hg38 ENCODE data, use `TxDb.Hsapiens.UCSC.hg38.knownGene`. Using `hg19` TxDb with `hg38` peaks produces incorrect annotations because gene coordinates differ between assemblies. For mouse, use `TxDb.Mmusculus.UCSC.mm10.knownGene`. Always verify the assembly matches before running annotation.

2. **Promoter definition affects interpretation**: ChIPseeker defaults to TSS +/- 3kb as the "promoter" region. This is a generous definition that captures distal promoter elements. For a more conservative analysis, use `tssRegion = c(-1000, 1000)` (TSS +/- 1kb), which restricts promoter annotation to core promoter elements. The choice significantly affects what fraction of peaks are classified as "promoter" vs "distal intergenic" -- a 3kb window typically doubles the promoter fraction compared to 1kb. Report which definition you used.

3. **GREAT version matters**: GREAT v4 (current) and earlier versions use different gene association rules and ontology databases. Results from GREAT v3 and v4 are not directly comparable. Always specify the GREAT version in methods. When using rGREAT, set `version = "4.0.4"` explicitly to ensure reproducibility. The basal domain and extension distances differ between versions, which changes which genes are associated with each peak.

4. **Multiple peaks per gene vs gene-level summary**: ChIPseeker annotates each peak independently, so a single gene can appear multiple times (once for each associated peak). When converting to gene lists for enrichment analysis, deduplicate gene names. GREAT handles this differently by computing enrichment at the region level, accounting for the number of genomic regions associated with each gene. Be aware that these two approaches can produce different gene lists from the same peak set.

## Presenting Results

When reporting peak annotation results:

- **Genomic distribution**: Present the feature distribution as both a table and pie chart data: promoter (with TSS window definition used), 5' UTR, 3' UTR, exon, intron, downstream, and distal intergenic, with counts and percentages
- **Gene annotation table**: Include columns: peak_id, nearest_gene (symbol), distance_to_TSS (bp), genomic_feature, strand, and peak_score
- **Always report**: ChIPseeker version, TxDb used (e.g., TxDb.Hsapiens.UCSC.hg38.knownGene), promoter definition (e.g., TSS +/- 3kb vs +/- 1kb), genome assembly, and total peaks annotated
- **GREAT results**: If functional enrichment was run, report GREAT version, association rule (basal+extension), top enriched ontology terms with FDR-corrected p-values, and number of genomic regions associated
- **Context to provide**: Note that promoter definition strongly affects the promoter vs distal intergenic ratio, and that a single gene may appear multiple times if multiple peaks map to it
- **Next steps**: Suggest `motif-analysis` to discover TF motifs within annotated peak categories (e.g., promoter peaks vs enhancer peaks), or `regulatory-elements` for deeper enhancer/promoter characterization

## Walkthrough: Annotating Pancreas H3K27ac Peaks with Nearby Genes and Pathways

**Goal**: Annotate enhancer peaks with nearest genes and run pathway enrichment.
**Context**: User has H3K27ac peaks from pancreatic islets and wants to identify enriched biological processes.

### Step 1: Find H3K27ac peaks in pancreas

```
encode_search_files(
  assay_title="Histone ChIP-seq",
  organ="pancreas",
  target="H3K27ac",
  file_format="bed",
  output_type="IDR thresholded peaks",
  assembly="GRCh38"
)
```

Expected output:
```json
{
  "total": 5,
  "files": [{"accession": "ENCFF567PAN", "output_type": "IDR thresholded peaks", "file_size_mb": 1.8}]
}
```

### Step 2: Download and track the experiment

```
encode_download_files(
  accessions=["ENCFF567PAN"],
  download_dir="/data/peaks/pancreas_h3k27ac"
)
```

### Step 3: Run ChIPseeker annotation in R
```R
library(ChIPseeker)
peaks <- readPeakFile("ENCFF567PAN.bed")
peakAnno <- annotatePeak(peaks, TxDb=TxDb.Hsapiens.UCSC.hg38.knownGene)
# -> Distribution: Promoter (23%), Intron (38%), Intergenic (29%), Exon (10%)
```

### Step 4: Run GO enrichment on peak-associated genes
```R
library(clusterProfiler)
genes <- as.data.frame(peakAnno)$geneId
ego <- enrichGO(genes, OrgDb=org.Hs.eg.db, ont="BP")
# -> Top terms: "insulin secretion", "glucose homeostasis", "pancreas development"
```

**Interpretation**: Pancreas H3K27ac peaks are enriched near insulin secretion genes -- consistent with active enhancers driving islet-specific gene expression.

## Code Examples

### 1. Search for peaks to annotate

```
encode_search_files(
  assay_title="Histone ChIP-seq",
  organ="liver",
  target="H3K4me3",
  file_format="bed",
  output_type="IDR thresholded peaks",
  assembly="GRCh38"
)
```

Expected output:
```json
{
  "total": 4,
  "files": [{"accession": "ENCFF890LIV", "output_type": "IDR thresholded peaks", "assembly": "GRCh38", "file_size_mb": 0.9}]
}
```

## Integration

| This skill produces... | Feed into... | Using tool/skill |
|---|---|---|
| Gene-annotated peak list | Pathway enrichment analysis | integrative-analysis skill |
| Genomic feature distribution (pie chart) | Publication figures | scientific-writing -> figure legends |
| Peak-to-gene assignments | Expression correlation | gtex-expression skill |
| Promoter vs enhancer classification | Regulatory element catalog | regulatory-elements skill |
| Gene lists from peaks | Drug target search | cross-reference -> Open Targets |

## Related Skills

- **regulatory-elements** -- Identify candidate cis-regulatory elements before annotation; provides context for enhancer vs promoter classification
- **motif-analysis** -- Discover TF binding motifs within annotated peak categories (e.g., motifs in promoter-associated peaks vs enhancer peaks)
- **histone-aggregation** -- Union merge of histone peaks across experiments; annotate the aggregated peak set for comprehensive feature distribution
- **accessibility-aggregation** -- Union ATAC/DNase peaks; annotate accessible regions to understand the regulatory landscape
- **visualization-workflow** -- Create publication-quality plots of annotation results using deepTools, R, or genome browsers
- **publication-trust** -- Verify literature claims backing analytical decisions

## For the request: "$ARGUMENTS"
