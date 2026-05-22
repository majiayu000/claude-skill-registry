---
name: methylation-aggregation
description: Build comprehensive DNA methylation maps by aggregating WGBS (Whole Genome Bisulfite Sequencing) data across multiple ENCODE experiments, donors, and labs. Use when the user wants to answer "where is DNA methylated/unmethylated in my tissue?" by combining per-CpG methylation data into tissue-level methylation profiles. Handles coverage filtering, identifies hypomethylated regions (HMRs) and partially methylated domains (PMDs), and manages cross-lab variation.
---

# Aggregate DNA Methylation Data Across Studies

## When to Use

- User wants to build a tissue-level DNA methylation landscape from multiple WGBS experiments
- User asks "where is DNA methylated in brain?" or "find hypomethylated regions across donors"
- User needs to identify HMRs (hypomethylated regions), UMRs, or PMDs from aggregated WGBS data
- User wants per-CpG weighted methylation averages from multiple experiments
- Example queries: "aggregate WGBS data for liver", "build methylation map across donors", "find unmethylated CpG islands in pancreas"

Build a comprehensive methylation landscape for a tissue/cell type by merging WGBS bedMethyl files from multiple ENCODE experiments.

## Scientific Rationale

**The question**: "What is the DNA methylation state across the genome in my tissue?"

DNA methylation is **fundamentally different** from histone marks and accessibility:

| Property | Histone/Accessibility | DNA Methylation |
|----------|----------------------|-----------------|
| Signal type | Binary (bound/open or not) | Continuous (0-100% methylated) |
| Default state | Unmarked | ~70-80% methylated (CpG context) |
| Biology of interest | Where marks ARE present | Where methylation is ABSENT or REDUCED |
| Aggregation approach | Union of peak calls | Average/median of methylation levels per CpG |

**The key insight**: Unlike histone ChIP-seq where we want the union of all peaks, for methylation we want the **average methylation level per CpG site** across individuals. Methylation is a quantitative, continuous signal measured at every CpG dinucleotide.

**However**, for identifying regulatory regions, we focus on **hypomethylated regions (HMRs)** — stretches of low methylation that mark active regulatory elements. HMRs can be treated more like peaks for union-style aggregation.

### Literature Support
- **Roadmap Epigenomics** (Schultz et al. 2015, Nature, 2,900+ citations): Established that tissue-specific HMRs mark active regulatory elements; demonstrated per-CpG averaging across biological replicates as standard approach
- **DMRcate** (Peters et al. 2021, Nucleic Acids Research, 65 citations): Method for calling differentially methylated regions from multiple WGBS samples; uses kernel smoothing across CpG sites
- **ENCODE Phase 3** (Gorkin et al. 2020, Nature, 301 citations): Integrated methylation data with histone marks and accessibility to define chromatin states
- **ENCODE Blacklist** (Amemiya et al. 2019, Scientific Reports, 1,372 citations): Problematic genomic regions to filter. [DOI](https://doi.org/10.1038/s41598-019-45839-z)
- **Zhou et al. 2020** (Nature Genetics): Tissue-specific methylation patterns: ~80% of CpGs are constitutively methylated, ~10% constitutively unmethylated (CpG islands/promoters), ~10% tissue-variable
- **Liu et al. 2024** (Briefings in Bioinformatics): Cross-platform comparison (NovaSeq vs DNBSEQ) showing WGBS is gold standard; coverage depth critically affects accuracy; platform differences exist in GC-rich regions
- **Ortega-Recalde et al. 2021** (Methods in Molecular Biology): Demonstrated that even low-coverage WGBS can accurately estimate global methylation levels, with bootstrap methods to quantify uncertainty

### Two-Level Analysis

1. **Per-CpG level**: Average methylation at each CpG site across samples (quantitative map)
2. **Region level**: Identify HMRs, PMDs, and UMRs from the averaged profile (union of regulatory regions)

## Step 1: Find All Available WGBS Data

```
encode_search_experiments(
    assay_title="WGBS",
    organ="pancreas",           # user's tissue of interest
    biosample_type="tissue",
    limit=100
)
```

Present a summary to the user:
- Total WGBS experiments
- Labs represented
- Unique donors/biosamples
- Genome coverage per experiment

Use `encode_get_facets` to check availability:
```
encode_get_facets(assay_title="WGBS", organ="pancreas")
```

**Note**: WGBS is expensive to generate. Typical tissues have 2-5 experiments. Even 2 biological replicates are valuable for identifying consistent methylation patterns.

## Step 2: Quality-Gate Each Experiment

```
encode_get_experiment(accession="ENCSR...")
```

### WGBS Quality Checks
- Audit status: no ERROR flags
- **Bisulfite conversion rate**: >=98% (measured by lambda spike-in or non-CpG methylation)
- **Genome coverage**: >=10x mean CpG coverage for reliable per-site estimates
- **Mapping rate**: >=50% (bisulfite-converted reads are harder to map)
- **Duplication rate**: <30%
- Has `methylation state at CpG` output files (bedMethyl format)

### Include if:
- Bisulfite conversion >=98%
- Mean CpG coverage >=10x
- Has bedMethyl output files for GRCh38

### Exclude if:
- ERROR audit flags
- Conversion rate <98% (unconverted reads create false methylation calls)
- Very low coverage (<5x mean) — individual CpG estimates unreliable

Track all included experiments:
```
encode_track_experiment(accession="ENCSR...")
```

## Step 3: Download bedMethyl Files

For each experiment:

```
encode_list_files(
    experiment_accession="ENCSR...",
    output_type="methylation state at CpG",
    assembly="GRCh38"
)
```

**bedMethyl format** (ENCODE standard):
```
chr  start  end  name  score  strand  thickStart  thickEnd  color  coverage  percentMethylated
```
- Column 10: read coverage at this CpG
- Column 11: percent methylation (0-100)

Prefer `preferred_default=True` files:
```
encode_download_files(
    file_accessions=["ENCFF...", ...],
    download_dir="/path/to/data/methylation",
    organize_by="flat"
)
```

## Step 4: Per-Sample Quality Filtering

### 4a. Coverage Filtering (CRITICAL)
Low-coverage CpGs have unreliable methylation estimates. Filter per-sample:

```bash
# Keep only CpGs with >= 5x coverage (column 10)
# More stringent: >= 10x for quantitative analysis
awk '$10 >= 5' sample.bedMethyl > sample.covfiltered.bedMethyl
```

**Coverage thresholds by use case:**
| Threshold | Use Case | Typical CpGs Retained |
|-----------|----------|----------------------|
| >=3x | Exploratory / maximum retention | ~90% of CpGs |
| >=5x | Standard analysis | ~80% of CpGs |
| >=10x | High-confidence quantitative | ~60% of CpGs |

### 4b. ENCODE Blocklist Filtering (Amemiya et al. 2019)
```bash
# Download from: https://github.com/Boyle-Lab/Blacklist/blob/master/lists/hg38-blacklist.v2.bed.gz
bedtools intersect -a sample.covfiltered.bedMethyl -b hg38-blacklist.v2.bed -v > sample.filtered.bedMethyl
```

### 4c. Strand Merging (Optional but Recommended)
CpG methylation is typically symmetric (same on both strands). Merge strand-specific calls to increase per-CpG coverage. **Caveat**: Some ENCODE bedMethyl files may already be strand-merged — check if both strands are present before applying this step:
```bash
# Group CpGs by position (forward and reverse strand of same CpG)
# Sum coverage, calculate weighted average methylation
awk 'BEGIN{OFS="\t"} {
    # CpG position (use the C position as canonical)
    if ($6 == "+") pos = $2
    else pos = $2 - 1
    key = $1"\t"pos
    cov[key] += $10
    meth[key] += ($11/100) * $10
} END {
    for (k in cov) {
        split(k, a, "\t")
        avg_meth = (meth[k] / cov[k]) * 100
        print a[1], a[2], a[2]+2, "CpG", 0, ".", a[2], a[2]+2, "0,0,0", cov[k], avg_meth
    }
}' sample.filtered.bedMethyl | sort -k1,1 -k2,2n > sample.merged_strands.bedMethyl
```

## Step 5: Cross-Sample Aggregation (Per-CpG Averaging)

### 5a. Create a Unified CpG Matrix

```bash
# Step 1: Find CpGs covered in at least M of N samples
# Extract positions from each sample
for f in sample*.merged_strands.bedMethyl; do
    awk 'BEGIN{OFS="\t"} {print $1, $2, $3}' "$f"
done | sort -k1,1 -k2,2n | uniq -c | \
awk -v M=2 '$1 >= M {print $2, $3, $4}' OFS="\t" > shared_cpgs.bed

# Step 2: For each sample, extract methylation at shared CpGs
for f in sample*.merged_strands.bedMethyl; do
    bedtools intersect -a shared_cpgs.bed -b "$f" -wa -wb | \
    awk 'BEGIN{OFS="\t"} {print $1, $2, $3, $NF, $(NF-1)}' > "${f%.bedMethyl}.shared.txt"
    # Columns: chr, start, end, percentMeth, coverage
done
```

### 5b. Calculate Average Methylation Per CpG

**Weighted average** (recommended — accounts for coverage differences):
```bash
# Combine all samples, calculate coverage-weighted mean methylation per CpG
cat sample*.shared.txt | \
sort -k1,1 -k2,2n | \
awk 'BEGIN{OFS="\t"} {
    key = $1"\t"$2"\t"$3
    if (key != prev_key && NR > 1) {
        avg = total_weighted_meth / total_cov
        print prev_key, n_samples, total_cov, avg
        n_samples = 0; total_cov = 0; total_weighted_meth = 0
    }
    prev_key = key
    n_samples++
    total_cov += $5
    total_weighted_meth += ($4/100) * $5
} END {
    avg = total_weighted_meth / total_cov
    print prev_key, n_samples, total_cov, avg
}' > tissue_methylation_profile.bed
# Columns: chr, start, end, n_samples, total_coverage, mean_methylation_fraction
```

**Simple average** (alternative — equal weight per sample):
```bash
# Unweighted mean across samples
awk 'BEGIN{OFS="\t"} {
    key = $1"\t"$2"\t"$3
    meth[key] += $4
    n[key]++
} END {
    for (k in meth) {
        print k, n[k], meth[k]/n[k]
    }
}' <(cat sample*.shared.txt) | sort -k1,1 -k2,2n > tissue_methylation_simple.bed
```

### 5c. Calculate Methylation Variability
Track inter-individual variation to identify tissue-variable CpGs:
```bash
# Add standard deviation column
# (compute in R or Python for large datasets)
```

## Step 6: Identify Regulatory Methylation Features

### 6a. Hypomethylated Regions (HMRs)
HMRs mark active regulatory elements. Identify runs of low methylation. The 30% threshold is a commonly used cutoff (Schultz et al. 2015 used similar ranges), but **the optimal threshold depends on your tissue and question** — some studies use 20%, others 40%. Consider visualizing the methylation distribution first to identify a natural breakpoint:
```bash
# Find CpGs with average methylation < 30% (adjust threshold as needed)
awk '$6 < 0.30' tissue_methylation_profile.bed > hypo_cpgs.bed

# Merge adjacent hypomethylated CpGs into regions
# Require minimum 3 CpGs within 1kb of each other
bedtools merge -i hypo_cpgs.bed -d 1000 -c 1 -o count | \
awk '$4 >= 3' > tissue_HMRs.bed
# Columns: chr, start, end, n_hypomethylated_CpGs
```

### 6b. Unmethylated Regions (UMRs) — CpG Islands
Very low methylation (<10%) at CpG-dense regions:
```bash
awk '$6 < 0.10' tissue_methylation_profile.bed > unmeth_cpgs.bed
bedtools merge -i unmeth_cpgs.bed -d 500 -c 1 -o count | \
awk '$4 >= 5' > tissue_UMRs.bed
```

### 6c. Partially Methylated Domains (PMDs)
Large (>10kb) regions of intermediate methylation, often marking repressed regions:
```bash
# Find CpGs with methylation 30-70% (partially methylated)
awk '$6 >= 0.30 && $6 <= 0.70' tissue_methylation_profile.bed > partial_cpgs.bed

# Merge with large gap tolerance to find domains
bedtools merge -i partial_cpgs.bed -d 5000 -c 1 -o count | \
awk '$4 >= 20 && ($3-$2) >= 10000' > tissue_PMDs.bed
```

### 6d. Tissue-Specific Differentially Methylated Regions
If comparing to another tissue, use DMRcate or similar:
```r
# In R with DMRcate
library(DMRcate)
# Requires a methylation matrix (CpGs x samples with tissue labels)
# Identifies regions where methylation differs between tissues
```

## Step 7: Confidence Annotation

For HMRs/UMRs (region-level features), annotate by sample support:

| Confidence | Criteria | Interpretation |
|-----------|----------|----------------|
| **High** | Low methylation in >=50% of samples | Constitutive regulatory region |
| **Supported** | Low methylation in 2+ samples | Likely regulatory, some variation |
| **Variable** | High variance across samples | Cell-type heterogeneity or individual variation |

```bash
# Annotate HMRs with sample support
# Intersect each HMR with per-sample hypomethylated CpGs to count support
awk -v N=4 '{
    # Using n_samples from the aggregation
    if ($4 >= N*0.5) conf="HIGH";
    else if ($4 >= 2) conf="SUPPORTED";
    else conf="VARIABLE";
    print $0"\t"conf"\t"$4"/"N
}' tissue_HMRs.bed > tissue_HMRs.annotated.bed
```

For the per-CpG profile, annotate by coverage confidence:
```bash
awk -v N=4 '{
    if ($4 >= N) conf="ALL_SAMPLES";
    else if ($4 >= N*0.5) conf="MAJORITY";
    else conf="PARTIAL";
    print $0"\t"conf
}' tissue_methylation_profile.bed > tissue_methylation.annotated.bed
```

## Step 7b: Summary Statistics

Report to the user:
- Total input experiments: N
- Experiments passing QC: M (bisulfite conversion, coverage)
- Total CpGs per sample (before/after coverage filter)
- Shared CpGs across M+ samples: X
- Mean genome-wide methylation: Y%
- Number of HMRs: Z (with size distribution)
- Number of UMRs: W
- Number of PMDs: V (if applicable)
- High-confidence HMRs: how many in ≥50% of samples
- CpGs with high inter-individual variability

## Step 8: Integration with Other ENCODE Data

Methylation data is most powerful when integrated:

1. **HMRs + H3K27ac peaks** = Active enhancers (use histone-aggregation skill)
2. **HMRs + ATAC-seq peaks** = Open regulatory elements (use accessibility-aggregation skill)
3. **UMRs + H3K4me3 peaks** = Active promoters
4. **PMDs** = Often overlap H3K9me3 (heterochromatin)

```bash
# Example: Find HMRs that overlap H3K27ac peaks (active enhancers)
bedtools intersect -a tissue_HMRs.bed -b union_H3K27ac_peaks.bed -wa -u > active_enhancer_HMRs.bed
```

## Step 9: Log Provenance

```
encode_log_derived_file(
    file_path="/path/to/tissue_methylation.annotated.bed",
    source_accessions=["ENCSR...", "ENCSR...", ...],
    description="Aggregated per-CpG methylation profile across N pancreas WGBS experiments",
    file_type="aggregated_methylation",
    tool_used="bedtools + custom aggregation",
    parameters="coverage >= 5x per sample, shared CpGs in >= 2 samples, coverage-weighted mean, strand-merged"
)

encode_log_derived_file(
    file_path="/path/to/tissue_HMRs.annotated.bed",
    source_accessions=["ENCSR...", "ENCSR...", ...],
    description="Hypomethylated regions from aggregated pancreas methylation profile",
    file_type="aggregated_HMRs",
    tool_used="bedtools merge",
    parameters="mean methylation < 30%, >= 3 CpGs within 1kb, confidence annotated"
)
```

## Pitfalls Specific to Methylation Data

1. **Bisulfite conversion rate is critical**: Even 1% incomplete conversion creates false methylation at unmethylated CpGs. Always verify >=98% conversion. ENCODE reports this in QC metrics.

2. **Coverage drives accuracy**: A CpG with 3x coverage has wide confidence intervals (0-100% could easily be 0% or 30%). At 10x, estimates stabilize. At 30x, they are reliable. Always filter by coverage.

3. **Non-CpG methylation**: Present in some cell types (especially embryonic). ENCODE bedMethyl files typically report CpG context only. If non-CpG methylation is relevant, check experiment metadata.

4. **Strand asymmetry**: While CpG methylation is typically symmetric, it can be asymmetric at some sites. Strand merging loses this information. For most analyses, merging is appropriate.

5. **Cell-type heterogeneity**: Bulk WGBS from tissue captures methylation across ALL cell types. A CpG at 50% methylation could mean: (a) all cells are 50% methylated, or (b) half the cells are 0% and half are 100%. These are biologically different. Single-cell methylation data (if available) resolves this.

6. **CpG islands vs. open sea**: CpG-dense regions (islands) have very different methylation dynamics than CpG-sparse regions. Consider analyzing separately.

7. **Do NOT mix assemblies**: All files must be GRCh38 or all hg19. CpG positions are exact — even a 1bp offset from liftOver misaligns CpGs.

8. **X chromosome**: Males have one X (hemimethylation), females have two (one inactivated with different methylation). Handle sex chromosomes separately or filter them.

9. **Imprinted regions**: Some regions show ~50% methylation in all individuals due to genomic imprinting (one allele methylated, one not). These are normal, not noise.

10. **Do NOT use union logic for per-CpG methylation**: Unlike histone peaks where union is correct, methylation levels should be AVERAGED. Union logic only applies to the derived HMR/UMR/PMD regions.

11. **RRBS is NOT the same as WGBS**: Reduced Representation Bisulfite Sequencing (RRBS) covers only CpG-rich regions (~10% of CpGs). Do NOT mix RRBS and WGBS in per-CpG averaging — the CpG universe is different.

12. **Sequencing platform matters**: Liu et al. 2024 showed that NovaSeq and DNBSEQ-T7 give slightly different methylation estimates, especially in GC-rich regions. Note the platform in provenance if mixing experiments from different sequencers.

## Walkthrough: Cross-Tissue CpG Methylation Atlas for Imprinted Gene Regions

**Goal**: Aggregate whole-genome bisulfite sequencing (WGBS) data across tissues to identify tissue-invariant vs. tissue-specific methylation patterns at imprinted gene loci.
**Context**: Imprinted genes show parent-of-origin-specific methylation. Comparing across tissues reveals which imprinting control regions (ICRs) maintain methylation universally.

### Step 1: Find WGBS experiments across tissues

```
encode_search_experiments(assay_title="WGBS", organism="Homo sapiens", limit=50)
```

Expected output:
```json
{
  "total": 147,
  "results": [
    {"accession": "ENCSR765JPC", "assay_title": "WGBS", "biosample_summary": "liver", "status": "released"},
    {"accession": "ENCSR832HMR", "assay_title": "WGBS", "biosample_summary": "brain", "status": "released"},
    {"accession": "ENCSR091ENJ", "assay_title": "WGBS", "biosample_summary": "lung", "status": "released"}
  ]
}
```

**Interpretation**: 147 WGBS experiments available. Select tissues with ≥2 replicates for reliable per-CpG averaging.

### Step 2: List methylation bedGraph files

```
encode_list_files(accession="ENCSR765JPC", file_format="bed", output_type="methylation state at CpG", assembly="GRCh38")
```

Expected output:
```json
{
  "files": [
    {"accession": "ENCFF123BED", "output_type": "methylation state at CpG", "file_format": "bed bedMethyl", "file_size_mb": 245.0}
  ]
}
```

### Step 3: Download methylation files

```
encode_download_files(accessions=["ENCFF123BED", "ENCFF456MET", "ENCFF789CPG"], download_dir="/data/wgbs")
```

### Step 4: Per-CpG weighted averaging across replicates

For each tissue:
1. Merge replicates using weighted average: β = Σ(methylated reads) / Σ(total reads)
2. Filter CpGs with <10× combined coverage
3. Output: per-tissue methylation BED with columns: chr, start, end, β-value, coverage

### Step 5: Identify tissue-invariant ICRs

```bash
# H19/IGF2 ICR: chr11:2,016,000-2,022,000
bedtools intersect -a merged_methylation.bed -b imprinted_icrs.bed -wa -wb | \
  awk '{sum+=$4; n++} END {print sum/n}'
```

**Interpretation**: ICRs showing ~50% methylation across ALL tissues confirm maintained imprinting. Tissue-variable ICRs (range >20%) suggest tissue-specific imprinting loss.

### Integration with downstream skills
- Feed differentially methylated regions into → **peak-annotation** for nearest gene assignment
- Overlay with → **histone-aggregation** H3K4me3 to find promoter methylation–expression anticorrelation
- Cross-reference CpG variants via → **clinvar-annotation** for methylation-disrupting mutations
- Compare methylation at regulatory elements from → **regulatory-elements**

## Code Examples

### 1. Survey WGBS data availability by organ
```
encode_get_facets(assay_title="WGBS", facet_field="organ", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {
    "organ": {"brain": 32, "liver": 18, "heart": 12, "lung": 10, "blood": 8, "kidney": 6}
  }
}
```

### 2. Check experiment quality before aggregation
```
encode_get_experiment(accession="ENCSR765JPC")
```

Expected output:
```json
{
  "accession": "ENCSR765JPC",
  "assay_title": "WGBS",
  "biosample_summary": "liver",
  "replicates": 2,
  "status": "released",
  "audit": {"WARNING": 0, "ERROR": 0},
  "pipeline": "WGBS (GRCh38)"
}
```

### 3. Track aggregated experiments
```
encode_track_experiment(accession="ENCSR765JPC", notes="Liver WGBS for cross-tissue methylation atlas")
```

Expected output:
```json
{
  "status": "tracked",
  "accession": "ENCSR765JPC",
  "notes": "Liver WGBS for cross-tissue methylation atlas",
  "tracked_at": "2025-03-08T12:00:00Z"
}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Per-CpG β-value matrix | **regulatory-elements** | Identify methylation at cCREs and enhancers |
| Differentially methylated regions (DMRs) | **peak-annotation** | Assign DMRs to nearest genes |
| Tissue-specific hypomethylated regions | **histone-aggregation** | Correlate with H3K4me3 active promoter marks |
| Methylation at CpG islands | **variant-annotation** | Find variants disrupting CpG sites |
| HMR/UMR/PMD boundaries | **accessibility-aggregation** | Overlay open chromatin at unmethylated regions |
| Cross-tissue methylation atlas | **visualization-workflow** | Generate methylation heatmaps across tissues |
| CpG methylation at GWAS loci | **gwas-catalog** | Annotate trait-associated variants with methylation context |

## Related Skills

- **histone-aggregation**: HMRs + H3K27ac union peaks identify active enhancers; HMRs + H3K4me3 identify active promoters
- **accessibility-aggregation**: HMRs typically overlap open chromatin; concordance between HMRs and ATAC/DNase peaks validates both
- **hic-aggregation**: Hypomethylated enhancers often anchor chromatin loops to target genes
- **regulatory-elements**: Combine methylation with histone and accessibility data to classify regulatory element types
- **epigenome-profiling**: Methylation adds a critical layer to chromatin state annotation
- **pipeline-wgbs**: Process raw WGBS data through the full ENCODE-aligned pipeline
- **batch-analysis**: Batch processing workflows for systematic methylation aggregation
- **publication-trust**: Verify literature claims backing analytical decisions

## Presenting Results

- Present methylation summary as: total CpGs analyzed | mean coverage | methylation distribution (UMR/LMR/PMD). Show per-sample contribution. Suggest: "Would you like to correlate with histone marks?"

## For the request: "$ARGUMENTS"
