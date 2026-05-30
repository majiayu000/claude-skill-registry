---
name: functional-screen-analysis
description: Analyze ENCODE functional genomics screens including CRISPR screens, MPRA (Massively Parallel Reporter Assays), and STARR-seq. Find screen data in ENCODE, process results, identify functional elements, and integrate with epigenomic annotations.
---

# Analyze ENCODE Functional Genomics Screens

## When to Use

- User wants to find or analyze CRISPR screen, MPRA, or STARR-seq data from ENCODE
- User asks about "functional screens", "CRISPR perturbation", "reporter assay", or "enhancer validation"
- User needs to identify functionally validated regulatory elements from screen results
- User wants to integrate screen results with epigenomic annotations (ChIP-seq, ATAC-seq peaks)
- Example queries: "find CRISPR screen data in ENCODE", "analyze MPRA results for enhancer activity", "which regulatory elements have functional validation?"

Discover and interpret functional validation data from CRISPR screens, MPRA (Massively Parallel Reporter Assays), and STARR-seq experiments in the ENCODE catalog. These assays directly test whether candidate regulatory elements have functional activity, complementing the correlative evidence from ChIP-seq, ATAC-seq, and Hi-C.

## Scientific Rationale

**The question**: "Which of the candidate regulatory elements identified by ENCODE actually have functional activity, and what genes do they regulate?"

The central challenge in regulatory genomics is that biochemical signatures (histone marks, chromatin accessibility, TF binding) are correlative — they identify *candidate* regulatory elements but cannot prove function. ENCODE Phase 4 addressed this gap by investing heavily in functional characterization: large-scale CRISPR perturbation screens, MPRA experiments testing thousands of candidate elements in parallel, and STARR-seq for genome-wide enhancer activity mapping.

### The Validation Gap

ENCODE catalogs 926,535 human candidate cis-regulatory elements (cCREs). But how many of these are truly functional?

- **CRISPR screens** (Gasperini et al. 2019): Of 5,920 candidate enhancers tested by CRISPRi, only ~12% showed significant effects on nearby gene expression
- **MPRA** (Inoue et al. 2017; Tewhey et al. 2016): Reporter assays confirm activity for 40-60% of predicted enhancers, depending on cell type and element class
- **STARR-seq** (Arnold et al. 2013): Genome-wide enhancer assays identify thousands of active elements, but episomal context differs from chromosomal

These functional assays provide the strongest evidence (short of genetic studies in humans) that a regulatory element has biological activity. ENCODE4 has scaled these approaches: the Functional Characterization Centers (Yao et al. 2024) performed 108 CRISPRi screens with >540,000 perturbations, targeting 3.27 million ENCODE SCREEN cCREs.

### Assay Comparison

| Assay | Tests | Context | Scale | Confidence | Key Limitation |
|-------|-------|---------|-------|-----------|----------------|
| CRISPR screen (CRISPRi/CRISPRa) | Endogenous perturbation | Native chromatin | 5,000–500,000 elements | Highest | Limited to cell lines; delivery constraints |
| MPRA | Reporter activity | Episomal (plasmid) | 10,000–100,000 variants | High for activity | Removed from chromatin context |
| STARR-seq | Self-transcription | Episomal (plasmid) | Genome-wide library | High for activity | Episomal; position effects |

### Literature Support

- **Gasperini et al. 2019** (Cell, ~800 citations): CRISPRi screen of 5,920 candidate enhancers with single-cell RNA-seq readout in K562 cells. Identified 664 enhancer-gene pairs. Established the "crisprQTL" framework linking perturbation effects to gene expression at single-cell resolution. [DOI](https://doi.org/10.1016/j.cell.2018.11.029)
- **Fulco et al. 2019** (Nature Genetics, ~1,200 citations): CRISPRi tiling screen combined with the Activity-By-Contact (ABC) model. Demonstrated that ABC predictions outperform distance-based enhancer-gene assignment. Quantitative relationship between enhancer activity, contact frequency, and gene regulation. [DOI](https://doi.org/10.1038/s41588-019-0538-0)
- **Shalem et al. 2014** (Science, ~5,500 citations): Genome-scale CRISPR-Cas9 knockout screening. The foundational paper for CRISPR loss-of-function screens. Established library design principles and analytical frameworks. [DOI](https://doi.org/10.1126/science.1247005)
- **Arnold et al. 2013** (Science, ~1,100 citations): STARR-seq — Self-Transcribing Active Regulatory Region sequencing. First genome-wide quantitative enhancer activity assay. Tests millions of fragments simultaneously in Drosophila; adapted to human. [DOI](https://doi.org/10.1126/science.1232542)
- **Inoue et al. 2017** (Genome Research, ~400 citations): MPRA for systematic variant effect prediction. Tested thousands of regulatory variants for allele-specific enhancer activity. Demonstrated that GWAS risk alleles frequently alter enhancer function. [DOI](https://doi.org/10.1101/gr.218032.116)
- **Li et al. 2014** (Genome Biology, ~2,800 citations): MAGeCK — Model-based Analysis of Genome-wide CRISPR-Cas9 Knockout. The standard computational tool for CRISPR screen analysis. Robust negative binomial model for guide RNA count data. [DOI](https://doi.org/10.1186/s13059-014-0554-4)
- **Gordon et al. 2020** (Nature Protocols, ~200 citations): MPRAflow — standardized computational pipeline for MPRA data analysis. Reproducible barcode counting, normalization, and activity scoring. [DOI](https://doi.org/10.1038/s41596-020-0339-z)
- **Tewhey et al. 2016** (Cell, ~600 citations): High-throughput identification of regulatory variants using MPRA. Tested >30,000 allelic pairs across 3,642 GWAS loci. Identified hundreds of variants with allele-specific regulatory activity. [DOI](https://doi.org/10.1016/j.cell.2016.09.027)
- **Nasser et al. 2021** (Nature, ~700 citations): ABC model for enhancer-gene prediction using ENCODE data. Linked 5,036 GWAS signals to 2,249 genes across 131 cell types. Validated predictions against CRISPRi perturbation data. [DOI](https://doi.org/10.1038/s41586-021-03446-x)
- **Klein et al. 2020** (Nature Genetics, ~350 citations): CRISPRi screen design principles for non-coding regulatory elements. Established that guide RNA positioning relative to regulatory element boundaries is critical. Quantified the "shadow" of CRISPRi repression (~1–2 kb). [DOI](https://doi.org/10.1038/s41588-020-0620-7)
- **Yao et al. 2024** (Nature Methods, ~26 citations): ENCODE4 Functional Characterization Centers — 108 CRISPRi screens, >540,000 perturbations across multiple cell types. Pre-designed sgRNA library targeting 3.27M ENCODE SCREEN cCREs. Establishes the largest functional characterization dataset for regulatory elements. [DOI](https://doi.org/10.1038/s41592-024-02216-7)
- **Lee et al. 2020** (Genome Biology, ~150 citations): STARRPeaker — peak caller designed specifically for STARR-seq data. Handles input library normalization and identifies significant enhancer peaks from STARR-seq enrichment. [DOI](https://doi.org/10.1186/s13059-020-02194-x)
- **Kim & Hart 2021** (Genome Medicine, ~200 citations): BAGEL2 — Bayesian Analysis of Gene Essentiality. Updated framework for identifying essential genes and functional elements from CRISPR screen data. [DOI](https://doi.org/10.1186/s13073-021-00898-0)

## Finding ENCODE Screen Data

### CRISPR Screens

```
encode_search_experiments(assay_title="CRISPR screen")
```

ENCODE contains CRISPRi (inhibition) and CRISPRa (activation) screens targeting regulatory elements:

| Screen Type | Mechanism | Effect on Target | Use Case |
|------------|-----------|-----------------|---------|
| CRISPRi (dCas9-KRAB) | Transcriptional repression | Silences enhancer/promoter | Loss-of-function; identifies required elements |
| CRISPRa (dCas9-VP64/p65) | Transcriptional activation | Activates latent elements | Gain-of-function; identifies sufficient elements |
| CRISPR knockout | Cas9 nuclease | Deletes element | Irreversible loss-of-function |

**Typical ENCODE CRISPR screen outputs**:
- Guide RNA quantifications (sgRNA counts per condition)
- Element quantifications (aggregated guide effects per target element)
- Differential expression results

```
# List available files for a CRISPR screen experiment
encode_list_files(
    experiment_accession="ENCSR...",
    file_format="tsv",
    assembly="GRCh38"
)
```

### MPRA Experiments

```
encode_search_experiments(assay_title="MPRA")
```

ENCODE MPRA experiments test candidate cis-regulatory elements for enhancer/promoter activity:

**Typical MPRA outputs**:
- Barcode count matrices (RNA and DNA)
- Activity scores per tested element
- Differential activity between alleles (for variant testing)

### STARR-seq Experiments

```
encode_search_experiments(assay_title="STARR-seq")
```

STARR-seq tests enhancer activity genome-wide using self-transcribing reporter constructs:

**Typical STARR-seq outputs**:
- Aligned reads (BAM)
- Signal tracks (bigWig) — enrichment over input
- Peak files (BED) — identified enhancer elements

### Combined Discovery

To find ALL functional characterization data for a tissue or cell type:

```
# All perturbation experiments
encode_search_experiments(perturbed=True, organ="...")

# Functional characterization in a specific cell line
encode_search_experiments(assay_title="CRISPR screen", biosample_term_name="K562")
encode_search_experiments(assay_title="MPRA", biosample_term_name="K562")
encode_search_experiments(assay_title="STARR-seq", biosample_term_name="K562")
```

## CRISPR Screen Analysis

### Data Types and File Formats

| Data Type | Format | Description |
|----------|--------|-------------|
| Guide RNA counts | TSV | Raw or normalized sgRNA counts per sample |
| Element quantifications | TSV | Aggregated effect sizes per target element |
| Differential expression | TSV | Genes with significant expression changes |

### Analytical Workflow

```
Step 1: Guide counts     → Quality filter low-representation guides
Step 2: Normalization     → Median ratio or total count normalization
Step 3: Statistical test  → MAGeCK, BAGEL2, or custom model
Step 4: Hit calling       → FDR correction, effect size thresholds
Step 5: Integration       → Overlay on ENCODE cCREs and epigenomic marks
```

### Key Analysis Tools

#### MAGeCK (Li et al. 2014)

The standard tool for CRISPR screen analysis:

```bash
# Count sgRNAs from FASTQ
mageck count -l library.tsv -n experiment \
    --sample-label "control,treatment" \
    --fastq control_R1.fastq.gz treatment_R1.fastq.gz

# Test for enrichment/depletion
mageck test -k experiment.count.txt \
    -t treatment -c control \
    -n results --remove-zero both
```

MAGeCK outputs:
- `results.gene_summary.txt` — Gene/element-level results (RRA and MLE)
- `results.sgrna_summary.txt` — Individual guide-level results
- Key columns: `neg|score`, `neg|fdr`, `pos|score`, `pos|fdr`

#### BAGEL2 (Kim & Hart 2021)

Bayesian framework for gene essentiality from CRISPR screens:

```bash
# Calculate Bayes Factors
BAGEL.py fc -i counts.txt -o foldchange.txt -c control_columns
BAGEL.py bf -i foldchange.txt -o bayes_factors.txt \
    -e essential_genes.txt -n nonessential_genes.txt
BAGEL.py pr -i bayes_factors.txt -o precision_recall.txt
```

### Quality Control Metrics

| QC Metric | Threshold | Description |
|----------|-----------|-------------|
| Guide representation | >200 reads/guide | Minimum coverage for statistical power |
| Replicate correlation | Pearson r > 0.7 | Between biological replicates |
| Positive control enrichment | p < 0.01 | Known essential genes/elements should score |
| Negative control depletion | ~50% at FDR 0.1 | Random non-targeting guides show no effect |
| Gini index | <0.3 | Measures guide count distribution evenness |
| Mapping rate | >70% | Reads mapping to library sequences |

### CRISPRi-Specific Considerations

- **Repression window**: CRISPRi silences a ~1–2 kb window around the guide target (Klein et al. 2020). Multiple guides within this window are not independent.
- **TSS proximity bias**: Elements near gene TSSs show stronger effects due to proximity to promoters. Control for distance-to-TSS in analysis.
- **Multiple guide averaging**: Require 2+ guides per element with concordant effects to call a hit.

### Integration with ENCODE Epigenomic Data

After identifying screen hits:

```
# Overlay CRISPRi hits on ENCODE cCREs
encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K27ac", biosample_term_name="K562")

# Check chromatin accessibility at hit locations
encode_search_experiments(assay_title="ATAC-seq", biosample_term_name="K562")

# Download peak files for intersection
encode_list_files(
    experiment_accession="ENCSR...",
    file_format="bed",
    output_type="IDR thresholded peaks",
    assembly="GRCh38",
    preferred_default=True
)
```

Intersection analysis:
```bash
# Intersect CRISPR hits with H3K27ac peaks
bedtools intersect -a crispr_hits.bed -b h3k27ac_peaks.bed -wa -wb > hits_in_enhancers.bed

# Calculate enrichment of hits in specific chromatin states
# Compare: (hits in enhancers / total hits) vs (all tested elements in enhancers / total tested)
```

## MPRA Analysis

### Data Types and File Formats

| Data Type | Format | Description |
|----------|--------|-------------|
| Barcode counts (DNA) | TSV | Input library representation |
| Barcode counts (RNA) | TSV | Transcriptional output |
| Activity scores | TSV | RNA/DNA ratio per element |

### Analytical Workflow

```
Step 1: Barcode counting   → Count barcodes in DNA and RNA libraries
Step 2: DNA normalization  → Normalize RNA counts by DNA representation
Step 3: Activity scoring   → Calculate RNA/DNA ratio per element
Step 4: Statistical test   → Compare to negative controls
Step 5: Allelic comparison → Test for allele-specific activity (if applicable)
```

### MPRAflow (Gordon et al. 2020)

Standardized computational pipeline:

```bash
# Run MPRAflow
nextflow run MPRAflow/MPRAflow.nf \
    --design design_file.txt \
    --fastq_insert insert_reads/ \
    --fastq_bc barcode_reads/ \
    --outdir results/
```

MPRAflow handles:
- Barcode-to-element association
- Count normalization
- Activity scoring with confidence intervals
- Allele-specific comparisons

### Activity Score Interpretation

The core MPRA measurement is the **activity ratio**:

```
Activity = log2(RNA_counts / DNA_counts)
```

| Activity Score | Interpretation |
|---------------|---------------|
| Activity >> 0 (e.g., >1.5) | Strong enhancer/promoter activity |
| Activity ~ 0 | No regulatory activity (or activity equal to minimal promoter) |
| Activity << 0 (e.g., <-1.0) | Potential silencer activity (reduces transcription) |

### Statistical Framework

- **Null distribution**: Negative control elements (scrambled sequences) define background
- **Test**: Compare each element's activity to the negative control distribution
- **Multiple testing**: Benjamini-Hochberg FDR across all tested elements
- **Effect size**: log2(activity ratio) relative to negative controls
- **Significance threshold**: FDR < 0.05 AND |log2FC| > 1.0 (typical, adjust per experiment)

### Integration with ENCODE Annotations

```python
# Correlate MPRA activity with ENCODE histone mark signals
# Elements with strong MPRA activity should show:
# - High H3K27ac signal (active enhancer mark)
# - Chromatin accessibility (ATAC-seq/DNase-seq signal)
# - TF binding (ChIP-seq signal at element)

# Elements with NO MPRA activity despite H3K27ac may be:
# - Context-dependent (active only in specific conditions)
# - False-positive biochemical marks
# - Silencer elements (negative activity in MPRA)
```

## STARR-seq Analysis

### Data Types and File Formats

| Data Type | Format | Description |
|----------|--------|-------------|
| Input library | BAM/FASTQ | Cloned genomic fragments |
| STARR-seq output | BAM/FASTQ | Self-transcribed fragments (enriched) |
| Signal tracks | bigWig | Enrichment over input |
| Peaks | BED | Identified enhancer elements |

### Analytical Workflow

```
Step 1: Alignment         → Map input and STARR-seq reads to genome
Step 2: Enrichment        → Calculate STARR-seq / input ratio
Step 3: Peak calling      → Identify enriched regions (enhancers)
Step 4: Quantification    → Measure enhancer strength per peak
Step 5: Integration       → Compare with ENCODE cCRE predictions
```

### STARRPeaker (Lee et al. 2020)

Purpose-built peak caller for STARR-seq data:

```bash
# Call peaks from STARR-seq
starrpeaker \
    --prefix output_prefix \
    --chromsize hg38.chrom.sizes \
    --bam input.bam starrseq.bam \
    --threshold 0.05
```

Alternatively, standard peak callers can be applied to the enrichment:
```bash
# Using MACS2 on STARR-seq enrichment
macs2 callpeak -t starrseq.bam -c input.bam \
    -f BAM -g hs --nomodel \
    -n starr_enhancers -q 0.05
```

### Comparison with ENCODE cCRE Predictions

| STARR-seq Result | ENCODE cCRE Status | Interpretation |
|-----------------|-------------------|---------------|
| Active in STARR-seq | dELS or pELS | Validated enhancer |
| Active in STARR-seq | PLS | Promoter with enhancer activity |
| Active in STARR-seq | Not in cCRE catalog | Novel enhancer (or context-dependent) |
| Inactive in STARR-seq | dELS or pELS | Possible false positive cCRE, or context-dependent |
| Inactive in STARR-seq | Not in cCRE catalog | Confirmed non-enhancer |

### STARR-seq Caveats

- **Episomal context**: STARR-seq tests elements outside their native chromatin. Elements requiring specific chromatin context may fail to score.
- **Position effects**: The reporter construct itself introduces bias (minimal promoter, polyA signal placement).
- **Quantitative, not binary**: STARR-seq enrichment is continuous. Use a statistical threshold (e.g., input-normalized enrichment > 2-fold, FDR < 0.05) rather than arbitrary cutoffs.
- **Species considerations**: STARR-seq was originally developed in Drosophila (Arnold et al. 2013). Human STARR-seq requires modifications (ori-free constructs) to reduce plasmid replication artifacts.

## Integrating Screens with Epigenomic Data

### Overlay on ChromHMM States

For each functionally validated element, determine its chromatin state:

```
# Retrieve ChromHMM annotations for the cell type
# (Pre-computed by Roadmap Epigenomics for 111 reference epigenomes)

# Enrichment analysis: are screen hits preferentially in specific chromatin states?
# Expected: hits enriched in active enhancer (Enh, EnhG) and active promoter (TssA) states
# Unexpected enrichment in quiescent or heterochromatin states suggests novel regulatory mechanisms
```

### Correlate with ENCODE cCRE Classes

| cCRE Class | Expected Screen Hit Rate | Rationale |
|-----------|------------------------|-----------|
| PLS (Promoter-like) | 30–50% | Promoters are consistently active |
| pELS (Proximal enhancer-like) | 15–25% | Proximity to promoters increases detection |
| dELS (Distal enhancer-like) | 5–15% | Distal enhancers are often cell-type-specific |
| CTCF-only | <5% | Insulators rarely show enhancer activity |
| No cCRE overlap | 1–3% | Novel elements or context-dependent activity |

### ABC Model Integration (Nasser et al. 2021)

The Activity-By-Contact model predicts enhancer-gene links using ENCODE data. Cross-reference screen hits:

```
# For each CRISPR hit:
# 1. Check if the hit is predicted by ABC to regulate the observed target gene
# 2. ABC-predicted enhancers that are also CRISPR-validated are highest confidence
# 3. CRISPR hits NOT predicted by ABC may act through mechanisms ABC does not model
```

### GWAS Variant Enrichment in Screen-Validated Elements

Screen-validated elements provide the strongest evidence for variant interpretation:

```
# Workflow:
# 1. Identify GWAS variants in LD (r2 > 0.8) from gwas-catalog skill
# 2. Intersect with functionally validated enhancers
# 3. Variants in CRISPR-validated enhancers are highest-priority causal candidates
# 4. Test for enrichment: are GWAS variants over-represented in screen hits?

bedtools intersect \
    -a gwas_variants_ld.bed \
    -b crispr_validated_enhancers.bed \
    -wa -wb > gwas_in_validated_enhancers.bed
```

## Experimental Design Considerations

### Library Complexity

| Screen Type | Minimum Library Size | Recommended Coverage |
|------------|---------------------|---------------------|
| CRISPR (gene-level) | 4–6 guides per gene | 500x per guide |
| CRISPR (element-tiling) | 1 guide per ~100bp | 200x per guide |
| MPRA | 10–20 barcodes per element | 100x per barcode |
| STARR-seq | Genome-wide fragmentation | 10x genome coverage |

### Control Element Selection

**Positive controls** (expected to score):
- Known essential genes (for knockout screens)
- Validated enhancers from VISTA or previous CRISPR studies
- Strong constitutive promoters (e.g., CMV, EF1a for MPRA)

**Negative controls** (expected to show no effect):
- Non-targeting sgRNAs (CRISPR) — 100–1,000 random guides
- Scrambled sequences (MPRA) — sequence-matched but shuffled
- Gene deserts (STARR-seq) — genomic regions far from genes

### Cell Type Matching

**Critical**: The functional screen must be performed in a cell type that is biologically relevant to the regulatory elements being tested. An enhancer active in hepatocytes may show no MPRA activity in HEK293 cells.

| ENCODE Screen Cell Types | Tissue Relevance |
|-------------------------|-----------------|
| K562 (CML) | Hematopoietic lineage, Tier 1 |
| HepG2 | Liver / hepatocyte |
| GM12878 | B-lymphocyte, Tier 1 |
| WTC-11 (iPSC-derived) | Multiple differentiated cell types |
| A549 | Lung epithelial |

When integrating screen data with ENCODE epigenomic data:
```
# Ensure cell type match
encode_search_experiments(assay_title="Histone ChIP-seq", target="H3K27ac", biosample_term_name="K562")
# Match the screen cell type exactly for meaningful correlation
```

### Power Analysis

| Elements Tested | Guides/Barcodes Per | Replicates | Expected Power (FDR<0.05, |FC|>1.5) |
|----------------|-------------------|-----------|--------------------------------------|
| 5,000 | 4 guides | 3 bio | ~80% for strong effects |
| 5,000 | 6 guides | 3 bio | ~90% for moderate effects |
| 50,000 | 2 guides | 2 bio | ~60% for strong effects only |

## Pitfalls & Edge Cases

- **CRISPR screen vs MPRA measure different things**: CRISPR screens test necessity (loss-of-function), while MPRA tests sufficiency (gain-of-function). An element can be MPRA-active but CRISPR-dispensable if redundant enhancers compensate.
- **MPRA context effects**: MPRA tests elements on episomal plasmids outside their native chromatin context. Elements that require specific chromatin states or 3D contacts may score negative in MPRA but be active in vivo.
- **STARR-seq input library bias**: STARR-seq results depend heavily on input library complexity. Low-complexity libraries produce false negatives. Always check input coverage before interpreting negative results.
- **Cell-type specificity of screens**: A CRISPR screen in K562 may miss enhancers active only in primary tissues. Screen results are specific to the cell type used — do not assume they generalize across tissues.
- **Effect size vs statistical significance**: In pooled CRISPR screens, large guide RNA libraries can produce statistically significant but biologically trivial effect sizes. Always set minimum effect size thresholds alongside p-value cutoffs.
- **Guide RNA efficiency confounds**: Poor guide RNA cutting efficiency creates false negatives in CRISPR screens. Use multiple guides per element and aggregate with MAGeCK or similar tools.

## Provenance Integration

Log all screen analysis operations:

```
encode_track_experiment(
    accession="ENCSR...",
    notes="CRISPR screen analysis for [cell type] regulatory elements"
)

encode_log_derived_file(
    file_path="/path/to/screen_results.tsv",
    source_accessions=["ENCSR...", "ENCFF..."],
    description="CRISPR screen hit list: [N] significant elements at FDR<0.05 from [total] tested in [cell type]",
    file_type="screen_results",
    tool_used="MAGeCK v0.5.9.5",
    parameters="mageck test -t treatment -c control --remove-zero both; FDR<0.05, |LFC|>0.5"
)

encode_log_derived_file(
    file_path="/path/to/screen_encode_integration.tsv",
    source_accessions=["ENCSR...(screen)", "ENCSR...(H3K27ac)", "ENCSR...(ATAC)"],
    description="Integration of [N] CRISPR hits with ENCODE cCREs and H3K27ac peaks in [cell type]. [X] hits overlap cCRE-ELS, [Y] overlap H3K27ac peaks",
    file_type="integrated_screen_annotation",
    tool_used="bedtools intersect + custom enrichment",
    parameters="GRCh38, bedtools v2.31.0, IDR thresholded peaks"
)
```

Link to relevant publications:
```
encode_link_reference(
    experiment_accession="ENCSR...",
    reference_type="pmid",
    reference_id="30612741",
    description="Gasperini et al. 2019 — CRISPRi screen methodology reference"
)
```

## Walkthrough: CRISPR Screen for Enhancer Regulators of Pluripotency in H1-hESC

**Goal**: Analyze a CRISPR interference (CRISPRi) screen targeting candidate enhancers to identify those required for pluripotency gene expression in H1-hESC cells.
**Context**: Functional genomics screens like CRISPRi directly test enhancer necessity, complementing observational epigenomic data.

### Step 1: Find CRISPR screen experiments in H1-hESC

```
encode_search_experiments(assay_title="CRISPR screen", biosample_term_name="H1", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 12,
  "results": [
    {"accession": "ENCSR000CRI", "assay_title": "CRISPR screen", "biosample_summary": "H1-hESC", "target": "enhancer screen"},
    {"accession": "ENCSR001SGR", "assay_title": "CRISPR screen", "biosample_summary": "H1-hESC", "target": "gene-level growth screen"}
  ]
}
```

**Interpretation**: 12 CRISPR screens in H1-hESC. Filter for enhancer-targeting screens (vs. gene-level knockouts).

### Step 2: Get experiment details

```
encode_get_experiment(accession="ENCSR000CRI")
```

Expected output:
```json
{
  "accession": "ENCSR000CRI",
  "assay_title": "CRISPR screen",
  "biosample_summary": "H1-hESC",
  "description": "CRISPRi screen targeting 10,000 candidate enhancers with NANOG-GFP readout",
  "replicates": 3,
  "status": "released",
  "lab": "/labs/jesse-engreitz/"
}
```

### Step 3: List screen result files

```
encode_list_files(accession="ENCSR000CRI", file_format="tsv", assembly="GRCh38")
```

Expected output:
```json
{
  "files": [
    {"accession": "ENCFF500SCR", "output_type": "element quantifications", "file_format": "tsv", "file_size_mb": 15.2},
    {"accession": "ENCFF501GDE", "output_type": "guide quantifications", "file_format": "tsv", "file_size_mb": 8.7}
  ]
}
```

**Interpretation**: "Element quantifications" contains per-enhancer effect sizes. "Guide quantifications" has per-guide data for QC.

### Step 4: Download and analyze screen results

```
encode_download_files(accessions=["ENCFF500SCR"], download_dir="/data/crispr_screen")
```

Analysis steps:
1. Filter for significant hits (adjusted p-value < 0.05, |log2FC| > 0.5)
2. Map guide coordinates to cCRE annotations
3. Categorize hits: promoter-proximal vs. distal enhancer
4. Rank by effect size to prioritize validation candidates

### Step 5: Cross-reference hits with epigenomic marks

Overlay significant enhancer hits with:
- H3K27ac ChIP-seq peaks → confirms active enhancer status
- ATAC-seq peaks → confirms accessible chromatin
- Hi-C loops → identifies enhancer-promoter contacts

**Interpretation**: Enhancers that are CRISPRi-sensitive AND marked by H3K27ac AND connected by chromatin loops represent high-confidence regulatory elements for pluripotency.

### Integration with downstream skills
- Feed hit enhancer coordinates into → **peak-annotation** for target gene assignment
- Overlay with → **histone-aggregation** marks to validate enhancer chromatin state
- Check enhancer variants via → **clinvar-annotation** for disease associations
- Use with → **regulatory-elements** to classify hits as promoter-proximal, enhancer, or insulator

## Code Examples

### 1. Survey available functional screens by assay type
```
encode_get_facets(assay_title="CRISPR screen", facet_field="biosample_ontology.term_name", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {
    "biosample_ontology.term_name": {"K562": 45, "H1": 12, "GM12878": 8, "HepG2": 6}
  }
}
```

### 2. Find MPRA experiments (complementary functional assay)
```
encode_search_experiments(assay_title="MPRA", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 28,
  "results": [
    {"accession": "ENCSR100MPR", "assay_title": "MPRA", "biosample_summary": "K562", "status": "released"}
  ]
}
```

### 3. Find STARR-seq experiments
```
encode_search_experiments(assay_title="STARR-seq", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 15,
  "results": [
    {"accession": "ENCSR200STR", "assay_title": "STARR-seq", "biosample_summary": "HepG2", "status": "released"}
  ]
}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Significant enhancer hits (BED) | **peak-annotation** | Assign target genes to validated enhancers |
| Screen effect sizes per element | **regulatory-elements** | Classify functional elements by regulatory category |
| Validated enhancer coordinates | **histone-aggregation** | Confirm H3K27ac/H3K4me1 marks at functional enhancers |
| CRISPRi-sensitive regions | **accessibility-aggregation** | Verify open chromatin at functional elements |
| Enhancer-gene pairs | **hic-aggregation** | Validate via chromatin loop support |
| Functional variant coordinates | **variant-annotation** | Annotate GWAS variants at validated enhancers |
| Screen results table | **visualization-workflow** | Generate volcano plots and Manhattan plots of screen hits |
| Validated regulatory elements | **disease-research** | Connect functional enhancers to disease mechanisms |

## Related Skills

- `regulatory-elements` — Characterizing the candidate regulatory elements that screens validate. Screens test cCRE predictions.
- `search-encode` — Finding CRISPR screen, MPRA, and STARR-seq experiments in the ENCODE catalog
- `variant-annotation` — Screen-validated elements provide the strongest evidence for GWAS variant interpretation
- `disease-research` — Functional screens identify disease-relevant regulatory elements for translational research
- `integrative-analysis` — Combining screen results with multi-omic ENCODE data layers
- `epigenome-profiling` — Building comprehensive epigenomic profiles to contextualize screen hits
- `quality-assessment` — Evaluating screen quality metrics (guide representation, replicate correlation, control enrichment)
- `gwas-catalog` — GWAS variants in screen-validated enhancers are highest-priority causal candidates
- `histone-aggregation` — Aggregated histone peaks provide the annotation layer for screen hit classification
- `accessibility-aggregation` — Chromatin accessibility at screen targets indicates guide delivery efficiency
- `data-provenance` — Document screen analysis parameters, tool versions, and thresholds for reproducibility
- `publication-trust` — Verify literature claims backing analytical decisions

## Presenting Results

When reporting functional screen analysis results, present:

- **Screen overview**: Assay type (CRISPRi/CRISPRa/MPRA/STARR-seq), cell type, number of elements tested, library complexity
- **Hit summary**: Number of significant hits at stated FDR threshold, effect size distribution
- **QC metrics**: Guide representation, replicate correlation, positive/negative control performance
- **cCRE overlap table**: How many hits overlap each ENCODE cCRE class (PLS, pELS, dELS, CTCF-only, none)
- **Chromatin state enrichment**: Are hits enriched in specific ChromHMM states?
- **Enhancer-gene links**: For CRISPR screens, which genes are regulated by validated enhancers?
- **Volcano plot guidance**: Plot -log10(FDR) vs. effect size (log2FC). Label top hits. Mark ENCODE cCRE-overlapping hits in a distinct color.
- **Manhattan-style visualization**: For genome-wide screens, plot effect sizes across chromosomes to show spatial distribution of hits.

Example summary:
```
CRISPR Screen Analysis: K562 CRISPRi (ENCSR...)
Elements tested:    5,920 candidate enhancers
Significant hits:   664 (11.2%) at FDR < 0.05
  - 423 overlap ENCODE cCRE-ELS (63.7% of hits)
  - 141 overlap cCRE-PLS (21.2% of hits)
  - 100 no cCRE overlap (15.1% — novel functional elements)
Median effect size:  22% reduction in target gene expression
Top hit:            ENCSR... element → MYC (62% reduction, FDR = 1.2e-15)
```

## For the request: "$ARGUMENTS"
