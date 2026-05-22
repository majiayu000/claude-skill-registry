---
name: integrative-analysis
description: Plan and execute integrative analysis combining multiple ENCODE experiments for cross-dataset or multi-omic workflows. Use when the user wants to combine experiments, perform cross-dataset comparison, multi-omic integration, peak overlap analysis, differential binding, signal correlation, chromatin state segmentation, enhancer-gene linkage, or any analysis that requires merging or comparing data from two or more ENCODE experiments. Covers same-assay cross-sample, multi-omic same-sample, cross-organism, and perturbation integration designs. Guides compatibility checks, batch effect detection, normalization, integration strategy selection, and provenance documentation.
---

# Integrative Analysis of ENCODE Data

## When to Use

- User wants to combine multiple ENCODE experiments for cross-dataset analysis
- User asks about "integrating", "combining", or "comparing" experiments
- User wants to overlay histone marks with accessibility or expression data
- User needs to plan a multi-omic analysis using ENCODE data
- User asks about peak overlap, differential binding, or signal correlation
- User wants to perform ChromHMM segmentation using ENCODE histone data

Help the user combine multiple ENCODE experiments for cross-dataset or multi-omic analysis. This skill covers the full integration workflow: from defining the question and selecting compatible experiments, through choosing the right integration strategy and tools, to validating results and documenting provenance.

## Literature Foundation

| Reference | Journal | Key Contribution | DOI | Citations |
|-----------|---------|-----------------|-----|-----------|
| ENCODE Phase 3 (2020) | Nature | Registry of 926,535 candidate cis-regulatory elements; integrative analysis framework across 5,992 experiments | [10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4) | ~1,656 |
| Gorkin et al. (2020) | Nature | Integrative analysis of 3,158 mouse epigenomes; cross-tissue chromatin state annotation | [10.1038/s41586-020-2093-3](https://doi.org/10.1038/s41586-020-2093-3) | ~301 |
| Ernst & Kellis (2012) | Nature Methods | ChromHMM: chromatin state discovery from combinatorial histone mark patterns | [10.1038/nmeth.1906](https://doi.org/10.1038/nmeth.1906) | ~2,294 |
| Nasser et al. (2021) | Nature | Activity-by-Contact (ABC) model for enhancer-gene linkage; outperforms proximity assignment | [10.1038/s41586-021-03446-x](https://doi.org/10.1038/s41586-021-03446-x) | ~468 |
| Quinlan & Hall (2010) | Bioinformatics | BEDTools: genome arithmetic for interval comparisons, intersections, and merges | [10.1093/bioinformatics/btq033](https://doi.org/10.1093/bioinformatics/btq033) | ~10,000 |
| Ramirez et al. (2016) | Nucleic Acids Res | deepTools: signal normalization, correlation, and visualization for multi-sample genomic data | [10.1093/nar/gkw257](https://doi.org/10.1093/nar/gkw257) | ~3,000 |
| Love et al. (2014) | Genome Biology | DESeq2: differential analysis of count data with shrinkage estimation | [10.1186/s13059-014-0550-8](https://doi.org/10.1186/s13059-014-0550-8) | ~40,000 |
| Ross-Innes et al. (2012) | Nature | DiffBind: differential binding analysis of ChIP-seq peak data across conditions | [10.1038/nature10730](https://doi.org/10.1038/nature10730) | ~1,200 |
| Leek et al. (2010) | Nature Rev Genetics | Tackling batch effects: PCA-based detection, SVA/ComBat correction, experimental design | [10.1038/nrg2825](https://doi.org/10.1038/nrg2825) | ~1,200 |

## Step 1: Define the Integration Question

Clarify with the user which type of integration they need. There are four fundamental designs:

| Integration Design | Example | Key Challenge |
|-------------------|---------|---------------|
| **Same assay, cross-sample** | H3K27ac ChIP-seq across 5 tissues | Batch effects between labs/donors |
| **Multi-omic, same sample** | ATAC-seq + RNA-seq + ChIP-seq in K562 | Matching file types and normalization |
| **Cross-organism** | Human vs mouse liver chromatin | Ortholog mapping, synteny conservation |
| **Perturbation / condition** | Before vs after treatment | Need matched replicates per condition |

Each design has different requirements for compatibility, normalization, and statistical framework. Establish the design before searching for data.

**Questions to ask the user**:
- What biological question are you trying to answer?
- Are you comparing across samples (differential) or combining across samples (cataloging)?
- How many conditions/tissues/time points?
- Do you need statistical testing or descriptive overlap?

## Step 2: Find Compatible Experiments

### 2a. Explore Data Availability

Start with `encode_get_facets` to understand what data exists before committing to a design:

```
encode_get_facets(
    assay_title="Histone ChIP-seq",
    organ="pancreas"
)
```

This returns counts by target, biosample, lab, and other facets. Use it to verify that the intended comparison has sufficient data on both sides.

### 2b. Search for Candidate Experiments

Search for experiments matching each arm of the integration:

```
encode_search_experiments(
    assay_title="Histone ChIP-seq",
    target="H3K27ac",
    organ="pancreas",
    biosample_type="tissue",
    limit=100
)
```

For multi-omic designs, search each assay layer separately:

```
# Accessibility layer
encode_search_experiments(assay_title="ATAC-seq", organ="pancreas", limit=50)

# Expression layer
encode_search_experiments(assay_title="total RNA-seq", organ="pancreas", limit=50)

# Histone layer
encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K27ac", organ="pancreas", limit=50)
```

Present a summary table to the user showing experiments found per arm, number of replicates, labs represented, and any audit flags.

## Step 3: Check Pairwise Compatibility

Track candidate experiments and then check compatibility:

```
encode_track_experiment(accession="ENCSR...")
encode_track_experiment(accession="ENCSR...")

encode_compare_experiments(
    accession1="ENCSR...",
    accession2="ENCSR..."
)
```

The compatibility check evaluates:

| Dimension | Compatible | Requires Action | Incompatible |
|-----------|-----------|-----------------|-------------|
| **Organism** | Same species | Cross-species with ortholog mapping | N/A (always addressable) |
| **Assembly** | Same build (GRCh38) | Different builds (need liftOver) | Mixed within analysis without lifting |
| **Assay** | Same assay | Different assays (expected in multi-omic) | N/A |
| **Biosample** | Same term name | Different biosamples (expected in cross-sample) | Unexpected mismatch |
| **Lab** | Same lab | Different labs (flag for batch effects) | N/A |
| **Pipeline** | Same version | Different versions (flag, may need reprocessing) | Fundamentally different pipelines |
| **Replicates** | 2+ biological | 1 replicate (limited statistical power) | 0 replicates (unusable) |

**Critical rule**: ALL experiments in an integration MUST share the same genome assembly. Never mix GRCh38 and hg19 coordinates without explicit liftOver.

## Step 4: Select Matched Files

For each experiment, retrieve files using `encode_list_files`:

```
encode_list_files(
    experiment_accession="ENCSR...",
    file_format="bed",
    output_type="IDR thresholded peaks",
    assembly="GRCh38",
    preferred_default=True
)
```

### File Matching Rules

All files entering the same integration MUST be matched on:

1. **Same assembly** (GRCh38 for human, mm10 for mouse)
2. **Same output type** (e.g., all "IDR thresholded peaks" or all "fold change over control")
3. **Same file format** (all narrowPeak, all bigWig, all TSV)
4. **Same pipeline version** when possible (check ENCODE pipeline annotations)

### File Type Compatibility Matrix

Not all file types can be directly integrated. This matrix shows which combinations are valid:

| File Type A | File Type B | Integration Method | Valid? |
|------------|------------|-------------------|--------|
| narrowPeak | narrowPeak | BEDTools intersect/merge | Yes |
| narrowPeak | broadPeak | BEDTools intersect (with caveats) | Yes, but peak resolution differs |
| narrowPeak | bigWig | Signal extraction at peak locations | Yes |
| bigWig | bigWig | deepTools multiBigwigSummary | Yes |
| bigWig | narrowPeak | Signal quantification within peaks | Yes |
| gene quant TSV | gene quant TSV | DESeq2 count matrix | Yes |
| gene quant TSV | narrowPeak | Gene-centric: peaks near expressed genes | Yes (indirect) |
| contact matrix | narrowPeak | Loops anchored at peaks | Yes (resolution-dependent) |
| narrowPeak | gene quant TSV | Enhancer-gene linkage (ABC model) | Yes (requires Hi-C) |

**Cannot directly combine**:
- Raw FASTQ with processed peaks (different processing stages)
- BAM from different aligners without re-alignment
- Peaks from different assemblies without liftOver

## Step 5: Assess and Control Batch Effects

Batch effects are the most common source of false findings in integrative analysis. Following Leek et al. (2010), batch effects arise from lab, date, sequencing platform, library prep, and processing differences.

### 5a. Detection

**PCA of signal values**: Compute a sample-by-region signal matrix (e.g., read counts in consensus peak regions) and perform PCA. If the first principal components separate by lab or processing date rather than biology, batch effects are present.

```bash
# Using deepTools (Ramirez et al. 2016):
multiBigwigSummary bins \
    -b sample1.bigWig sample2.bigWig sample3.bigWig ... \
    --labels Lab1_Rep1 Lab1_Rep2 Lab2_Rep1 Lab2_Rep2 \
    -o signal_matrix.npz

plotPCA -in signal_matrix.npz \
    --plotFile pca_samples.pdf \
    --labels Lab1_Rep1 Lab1_Rep2 Lab2_Rep1 Lab2_Rep2
```

**Lab-correlated clustering**: In the PCA or hierarchical clustering, check whether samples group by lab/date/platform instead of by biological condition. If PC1 or PC2 correlates with a known technical variable (Pearson r > 0.5), batch correction is needed.

### 5b. Mitigation

| Method | Tool | When to Use |
|--------|------|-------------|
| **ComBat** | sva R package | Known batch variable, >=2 samples per batch |
| **SVA** | sva R package | Unknown confounders, exploratory |
| **limma removeBatchEffect** | limma R package | For visualization only (not for DE testing) |
| **Matched design** | Experimental design | Best approach: match conditions within each batch |

### 5c. When NOT to Correct

- **Small sample sizes** (< 3 per condition per batch): correction can remove real signal
- **Confounded design**: if batch and condition are perfectly correlated (all treated from lab A, all control from lab B), batch correction removes the biological signal. This design cannot be rescued computationally.
- **Single-sample batches**: ComBat requires >=2 samples per batch to estimate batch parameters
- **When batch is biology**: e.g., comparing tissues from different labs is expected to cluster by tissue AND lab

### 5d. Best Practice

Always report whether batch effects were detected and what (if anything) was done about them. If correction was applied, show PCA before and after correction. If correction was not applied, explain why (e.g., no batch structure detected, or design is confounded).

## Step 6: Choose Integration Strategy

This is the core decision point. The strategy depends on the data types being combined and the question being asked.

### Integration Strategy Table

| Integration Type | Data Sources | Tool/Method | Key Considerations |
|-----------------|-------------|-------------|-------------------|
| **Peak overlap** | ChIP + ChIP, or ChIP + ATAC | BEDTools intersect (Quinlan & Hall 2010) | Filter blacklist regions first; use IDR peaks; report overlap fraction both ways |
| **Signal correlation** | bigWig + bigWig | deepTools multiBigwigSummary + plotCorrelation (Ramirez et al. 2016) | All samples must use the same normalization (e.g., fold change over control); bin size affects resolution |
| **Differential binding** | ChIP-seq peaks across conditions | DiffBind (Ross-Innes et al. 2012) | Need >=2 biological replicates per condition; use consensus peak set; includes normalization |
| **Differential expression** | RNA-seq counts across conditions | DESeq2 (Love et al. 2014) | Need >=3 replicates per condition for statistical power; use raw counts, NOT TPM/FPKM |
| **Chromatin state** | 5+ histone marks from same biosample | ChromHMM (Ernst & Kellis 2012) | Requires core 5-mark panel minimum; binarized signal input; 200bp bins standard |
| **Enhancer-gene linkage** | ATAC/H3K27ac + RNA-seq + Hi-C | ABC model (Nasser et al. 2021) | Needs accessibility + expression + contact data; outperforms nearest-gene by ~2x |
| **Multi-omic overlay** | Mixed assays at same locus | Genome browser + deepTools heatmap | Visual validation essential; no single statistical test covers all combinations |

### Choosing the Right Strategy

```
IF comparing same assay across conditions:
    IF peak data → DiffBind (differential binding)
    IF count data → DESeq2 (differential expression)
    IF signal data → deepTools correlation + visualization

IF combining different assays on same sample:
    IF 5+ histone marks → ChromHMM (chromatin states)
    IF peaks + signal → BEDTools intersect + signal quantification
    IF peaks + expression + contacts → ABC model (enhancer-gene)

IF cataloging across many samples (union):
    → See histone-aggregation or accessibility-aggregation skills
```

## Step 7: Execute Integration

### 7a. Peak Overlap (BEDTools)

Compare peak sets from two experiments:

```bash
# Remove blacklisted regions first (Amemiya et al. 2019)
bedtools intersect -a peaks_A.narrowPeak -b hg38-blacklist.v2.bed -v > peaks_A.clean.bed
bedtools intersect -a peaks_B.narrowPeak -b hg38-blacklist.v2.bed -v > peaks_B.clean.bed

# Find overlapping peaks (minimum 1bp overlap)
bedtools intersect -a peaks_A.clean.bed -b peaks_B.clean.bed -wa -u > overlap_A_in_B.bed

# Report overlap statistics both directions
# A in B: what fraction of A peaks overlap B?
# B in A: what fraction of B peaks overlap A?
bedtools intersect -a peaks_A.clean.bed -b peaks_B.clean.bed -wa -u | wc -l  # A in B count
bedtools intersect -a peaks_B.clean.bed -b peaks_A.clean.bed -wa -u | wc -l  # B in A count
```

For multi-sample overlap, use `bedtools multiIntersect`:
```bash
bedtools multiIntersect \
    -i sample1.bed sample2.bed sample3.bed \
    -header \
    -names tissue1 tissue2 tissue3 \
    > multi_overlap.bed
```

### 7b. Signal Correlation (deepTools)

Compare signal tracks across experiments:

```bash
# Build signal matrix across genome bins
multiBigwigSummary bins \
    -b condA_rep1.bigWig condA_rep2.bigWig condB_rep1.bigWig condB_rep2.bigWig \
    --labels CondA_R1 CondA_R2 CondB_R1 CondB_R2 \
    --binSize 10000 \
    -o results.npz

# Pearson correlation heatmap
plotCorrelation -in results.npz \
    --corMethod pearson \
    --whatToPlot heatmap \
    --plotFile correlation_heatmap.pdf

# PCA for sample clustering
plotPCA -in results.npz \
    --plotFile pca.pdf
```

**Normalization requirement**: All bigWig files must use the same normalization. ENCODE provides "fold change over control" bigWigs, which are already input-normalized. Do NOT mix "signal of unique reads" (raw pileup) with "fold change over control" (normalized).

### 7c. Differential Binding (DiffBind)

```r
# R code for DiffBind analysis (Ross-Innes et al. 2012)
library(DiffBind)

# Create sample sheet
samples <- data.frame(
    SampleID = c("CondA_R1", "CondA_R2", "CondB_R1", "CondB_R2"),
    Condition = c("A", "A", "B", "B"),
    Replicate = c(1, 2, 1, 2),
    bamReads = c("condA_r1.bam", "condA_r2.bam", "condB_r1.bam", "condB_r2.bam"),
    Peaks = c("condA_r1.narrowPeak", "condA_r2.narrowPeak", "condB_r1.narrowPeak", "condB_r2.narrowPeak")
)

dba <- dba(sampleSheet = samples)
dba <- dba.count(dba)
dba <- dba.contrast(dba, categories = DBA_CONDITION)
dba <- dba.analyze(dba, method = DBA_DESEQ2)
results <- dba.report(dba, th = 0.05)
```

**Requirements**: >=2 biological replicates per condition (>=3 preferred). BAM files needed for counting reads in peaks.

### 7d. Differential Expression (DESeq2)

```r
# R code for DESeq2 analysis (Love et al. 2014)
library(DESeq2)

# Use RAW counts from ENCODE gene quantification TSV (not TPM)
countData <- read.table("count_matrix.tsv", header=TRUE, row.names=1)
colData <- data.frame(condition = factor(c("A", "A", "A", "B", "B", "B")))

dds <- DESeqDataSetFromMatrix(countData, colData, design = ~ condition)
dds <- DESeq(dds)
results <- results(dds, contrast = c("condition", "B", "A"), alpha = 0.05)
```

**Critical**: DESeq2 requires raw counts. ENCODE gene quantification files provide both TPM and expected counts. Use the raw/expected count column, never TPM or FPKM, as DESeq2 performs its own normalization internally.

### 7e. Chromatin State Segmentation (ChromHMM)

Requires the core 5-mark histone panel from the same biosample:
- H3K4me3 (active promoter)
- H3K27ac (active enhancer/promoter)
- H3K4me1 (enhancer priming)
- H3K27me3 (polycomb repression)
- H3K36me3 (transcription)

```bash
# Binarize signal data (200bp bins)
java -jar ChromHMM.jar BinarizeBed chromsizes.txt input_dir cell_mark_table.txt output_dir

# Learn model (15 or 18 states)
java -jar ChromHMM.jar LearnModel binarized_dir output_dir 15 GRCh38
```

See Ernst & Kellis (2012) for parameter selection and state interpretation.

### 7f. Enhancer-Gene Linkage (ABC Model)

The ABC model (Nasser et al. 2021) predicts enhancer-gene connections by multiplying enhancer Activity (H3K27ac signal) by Contact frequency (Hi-C):

**Required inputs**:
- ATAC-seq or DNase-seq peaks (accessibility)
- H3K27ac ChIP-seq signal (activity)
- Hi-C contact matrix (3D contact)
- Gene expression (RNA-seq TPM)

**Advantages over nearest-gene**: Nearest-gene assignment fails for >40% of enhancers. The ABC model correctly handles cases where enhancers skip the nearest gene to regulate a more distal target.

## Step 8: Validate Integration Results

Validation is essential. No integration result should be trusted without cross-validation.

### 8a. Known Biology Checks

- **Housekeeping genes**: Active promoter marks (H3K4me3, H3K27ac) should be present at GAPDH, ACTB, and other constitutively expressed genes across all tissues
- **Tissue-specific genes**: Tissue-specific marks should appear at known tissue markers (e.g., INS at beta cell enhancers, ALB at liver enhancers)
- **Blacklist regions**: No results should overlap ENCODE blacklist regions (Amemiya et al. 2019)

### 8b. Replicate Consistency

- In differential analyses, biological replicates within a condition should cluster together
- Pearson or Spearman correlation between replicates should be r > 0.8 for ChIP-seq signal
- If replicates do not correlate, the integration is unreliable

### 8c. Cross-Validation with Independent Data

- Compare differential peaks to published data for the same comparison
- Check overlap with ENCODE cCRE registry (candidate cis-regulatory elements)
- Validate enhancer-gene predictions against expression data (predicted target genes should be expressed)

### 8d. Quantitative Metrics

| Validation | Method | Acceptable Threshold |
|-----------|--------|---------------------|
| Replicate correlation | Pearson r on signal matrix | r > 0.8 |
| Peak overlap reciprocity | Jaccard index | Depends on comparison (same assay: >0.3; different assays: >0.05) |
| Differential FDR | Benjamini-Hochberg | FDR < 0.05 for discovery; < 0.01 for high-confidence |
| ChromHMM state coherence | Known promoters in "Active TSS" state | > 80% |
| ABC prediction accuracy | Validated enhancer-gene pairs | AUC > 0.7 |

## Step 9: Document Integration with Provenance

Every output of the integration must be logged for reproducibility.

### 9a. Log Each Derived File

```
encode_log_derived_file(
    file_path="/path/to/overlap_results.bed",
    source_accessions=["ENCSR...", "ENCSR..."],
    description="Peak overlap between H3K27ac (pancreas) and ATAC-seq (pancreas), blacklist-filtered",
    file_type="peak_overlap",
    tool_used="bedtools intersect v2.31.0",
    parameters="bedtools intersect -a H3K27ac.bed -b ATAC.bed -wa -u; blacklist v2 pre-filtered"
)
```

### 9b. Record the Full Integration Design

Document:
1. All experiments included (accessions) and why they were selected
2. All experiments excluded and why
3. Quality metrics for each experiment
4. Batch effects detected and correction applied (or justification for no correction)
5. Integration strategy chosen and rationale
6. Tool versions for every step
7. Validation results

### 9c. Track and Verify Provenance Chain

```
encode_get_provenance(file_path="/path/to/overlap_results.bed")
```

## Normalization Requirements

Different data types require different normalization. Using the wrong normalization invalidates the integration.

| Data Type | Normalization for Visualization | Normalization for Statistical Testing | ENCODE File to Use |
|-----------|-------------------------------|--------------------------------------|-------------------|
| ChIP-seq signal | Fold change over input control | Raw counts in peak regions (DiffBind handles internally) | "fold change over control" bigWig |
| ATAC-seq signal | RPM or CPM | Raw counts (DESeq2 handles internally) | "signal of unique reads" or "fold change over control" bigWig |
| RNA-seq expression | TPM for cross-gene comparison | Raw expected counts for DESeq2 | "gene quantifications" TSV |
| Hi-C contacts | KR or ICE normalized | Raw contact matrices for statistical comparison | "contact matrix" HiC |
| DNA methylation | Beta values (0-1) | M-values (log2(beta/(1-beta))) for statistical testing | WGBS bed files |

**Common mistakes**:
- Using TPM in DESeq2 (violates negative binomial assumption)
- Comparing RPM-normalized signal across experiments with different library sizes (RPM does not account for composition bias)
- Mixing "signal of unique reads" with "fold change over control" bigWigs

## Common Pitfalls

1. **Assembly mismatch**: All files must use the same genome assembly. GRCh38 and hg19 coordinates are NOT interchangeable. Use `encode_compare_experiments` to verify before starting. LiftOver is acceptable but introduces edge effects at assembly-discordant regions.

2. **Peak caller differences**: IDR thresholded peaks, MACS2 peaks, and SPP peaks have different properties (number, width, signal distribution). Mixing peak types across conditions introduces systematic bias. Always use the same output type across all experiments in a comparison.

3. **Normalization inconsistency**: Signal tracks must be normalized comparably. ENCODE "fold change over control" bigWigs are input-normalized and can be compared directly. "Signal of unique reads" bigWigs are NOT comparable across experiments with different sequencing depths without additional normalization.

4. **Antibody lot variation**: Even same-target ChIP-seq experiments can show different peak profiles due to antibody batch effects. Different labs may use antibodies from different vendors or lots. This does not invalidate integration but should be documented. Expect 70-90% peak overlap between experiments using different antibody lots.

5. **Cell type heterogeneity**: Bulk experiments from complex tissues (e.g., brain, pancreas) contain mixed cell type signals. A "tissue-specific enhancer" may actually be specific to a minority cell type within the tissue. Where possible, use cell type-sorted or single-cell data for integrative analysis.

6. **Saturation and depth differences**: Experiments with higher sequencing depth detect more peaks. Comparing a 50M-read experiment to a 10M-read experiment produces asymmetric overlap: most 10M peaks will overlap 50M peaks, but many 50M peaks will be unique. Report overlap fractions in both directions.

7. **Circular reasoning**: Do not use the same data to both discover and validate a finding. For example, if you identify enhancers using H3K27ac peaks and then "validate" them by checking H3K27ac signal at those locations, you have validated nothing. Use an independent data layer (e.g., ATAC-seq, expression) for validation.

8. **Pipeline version differences**: ENCODE has updated its uniform processing pipelines over time. Experiments processed with different pipeline versions may have systematic differences in peak calls, signal normalization, or quality filtering. Check pipeline version annotations in experiment metadata.

## Walkthrough: Multi-Mark Integrative Analysis of Brain Regulatory Elements

**Goal**: Combine multiple histone marks, accessibility, and expression data from ENCODE to define chromatin states and identify active regulatory elements in brain tissue.
**Context**: Individual marks provide partial views. Integrative analysis (e.g., ChromHMM) combines them into a complete chromatin state map.

### Step 1: Collect all available marks for brain

```
encode_get_facets(facet_field="target.label", organ="brain", assay_title="Histone ChIP-seq", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {"target.label": {"H3K27ac": 24, "H3K4me3": 20, "H3K27me3": 18, "H3K4me1": 15, "H3K36me3": 12, "H3K9me3": 8}}
}
```

### Step 2: Search for matching experiments from the same biosample

```
encode_search_experiments(assay_title="Histone ChIP-seq", biosample_term_name="GM12878", organism="Homo sapiens", limit=20)
```

### Step 3: Download peak files for all marks

```
encode_download_files(accessions=["ENCFF001AC", "ENCFF002K4", "ENCFF003K27", "ENCFF004K4M1"], download_dir="/data/integrative")
```

### Step 4: Run ChromHMM for chromatin state segmentation

```bash
# Learn 15-state model
ChromHMM.sh LearnModel -p 8 input_marks/ output_model/ 15 GRCh38
```

**Interpretation**: ChromHMM produces 15 chromatin states: active TSS, active enhancer, poised enhancer, heterochromatin, etc. Map states to biological functions using the emission probabilities.

### Integration with downstream skills
- Multi-mark data from → **epigenome-profiling** provides the input mark collection
- Chromatin states feed into → **regulatory-elements** for element classification
- State-annotated regions feed into → **peak-annotation** for gene assignment
- ChromHMM output feeds into → **visualization-workflow** for genome-wide state display

## Code Examples

### 1. Find all histone marks for a biosample
```
encode_get_facets(facet_field="target.label", assay_title="Histone ChIP-seq", biosample_term_name="GM12878", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {"target.label": {"H3K27ac": 3, "H3K4me3": 3, "H3K27me3": 2, "H3K4me1": 2, "H3K36me3": 2}}
}
```

### 2. Download signal tracks for ChromHMM input
```
encode_search_files(file_format="bigWig", output_type="fold change over control", biosample_term_name="GM12878", assembly="GRCh38")
```

Expected output:
```json
{
  "total": 15,
  "results": [
    {"accession": "ENCFF100BW", "file_format": "bigWig", "target": "H3K27ac", "file_size_mb": 45}
  ]
}
```

### 3. Track experiments used for integrative analysis
```
encode_track_experiment(accession="ENCSR000AKA", notes="GM12878 H3K27ac for ChromHMM integrative analysis")
```

Expected output:
```json
{"status": "tracked", "accession": "ENCSR000AKA", "notes": "GM12878 H3K27ac for ChromHMM integrative analysis"}
```

## Related Skills

- **compare-biosamples** -- Systematic comparison of data availability across tissues and cell types; use to plan cross-sample integration designs
- **epigenome-profiling** -- Build comprehensive epigenomic profiles by assembling histone marks, accessibility, and expression for a single biosample
- **multi-omics-integration** -- Deep multi-omic regulatory landscape construction (enhancer discovery, ChromHMM, TF networks); more specialized than this general integration skill
- **histone-aggregation** -- Union merge of histone ChIP-seq peaks across studies; use as input layer for integrative analysis
- **accessibility-aggregation** -- Union merge of ATAC-seq/DNase-seq peaks across studies; use as input layer for integrative analysis
- **data-provenance** -- Detailed provenance tracking and methods writing; use to document the full integration chain for publication
- **ucsc-browser** -- Retrieve ENCODE tracks from UCSC for integration with locally-derived data
- **ensembl-annotation** -- Ensembl Regulatory Build annotations complement ENCODE cCRE data for cross-resource integration
- **geo-connector** -- Find complementary non-ENCODE datasets in GEO for expanded integrative analysis
- **publication-trust** -- Verify literature claims backing analytical decisions

## Presenting Results

- Present integration results as: analysis type | key finding | supporting evidence | confidence. Show overlap statistics for multi-assay intersections. Suggest: "Would you like to visualize these overlaps?"

## For the request: "$ARGUMENTS"
