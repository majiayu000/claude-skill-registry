---
name: accessibility-aggregation
description: Build comprehensive chromatin accessibility maps by aggregating ATAC-seq and DNase-seq narrowPeak data across multiple ENCODE experiments, donors, and labs. Use when the user wants to answer "where is chromatin accessible in my tissue?" by combining peak calls into a union peak set. Handles cross-lab variation, ATAC vs DNase platform differences, and ENCODE blocklist filtering.
---

## When to Use

- User wants to combine ATAC-seq or DNase-seq peaks across multiple experiments for a tissue
- User asks "where is chromatin accessible in my tissue?" or "build an open chromatin map"
- User needs to merge accessibility data from different labs, donors, or platforms (ATAC vs DNase)
- User wants a comprehensive set of open chromatin regions for regulatory element discovery
- Example queries: "aggregate ATAC-seq peaks for pancreas", "combine DNase-seq across donors", "find all accessible regions in liver"

# Aggregate Chromatin Accessibility Peaks Across Studies

Build a comprehensive map of open chromatin for a tissue/cell type by merging ATAC-seq and/or DNase-seq narrowPeak files from multiple ENCODE experiments.

## Scientific Rationale

**The question**: "Where is chromatin accessible in my tissue?"

Like histone marks, chromatin accessibility is a **detection question**. An open chromatin region detected in one donor but not another is still a real accessible site — individual variation, sequencing depth, and technical factors explain absence. We want the **union of all detections**.

### ATAC-seq vs DNase-seq

Both measure open chromatin but with different biases:

| Property | ATAC-seq | DNase-seq |
|----------|----------|-----------|
| Method | Tn5 transposase insertion | DNase I hypersensitivity |
| Input required | ~50K cells | ~1M cells |
| Resolution | High | High |
| GC bias | Moderate (Tn5 preference) | Low |
| Mitochondrial reads | High (filter needed) | None |
| ENCODE availability | Newer experiments | Extensive historical catalog |
| Comparability | Generally comparable at open regions | |

### Literature Support
- **Corces et al. 2017** (Nature Methods, 733 citations): Established that ATAC-seq and DNase-seq identify largely overlapping accessible regions, with ATAC capturing ~75% of DNase sites. Both are valid for union maps.
- **ENCODE Blacklist** (Amemiya et al. 2019, Scientific Reports, 1,372 citations): Comprehensive set of problematic genomic regions to filter. Essential for all functional genomics analyses. [DOI](https://doi.org/10.1038/s41598-019-45839-z)
- **F-Seq2** (Zhao & Boyle 2020, NAR Genomics): Improved peak caller for DNase-seq and ATAC-seq with proper test statistics for IDR compatibility.
- **ENCODE Phase 3** (Gorkin et al. 2020, Nature, 301 citations): Integrated accessibility data with histone marks across tissues for chromatin state annotation.

**Recommendation**: If combining ATAC-seq and DNase-seq peaks, treat them as equivalent signal sources for accessibility. The union is appropriate because both detect the same biological signal (open chromatin) through different enzymatic mechanisms.

## Step 1: Find All Available Accessibility Data

```
# ATAC-seq
encode_search_experiments(
    assay_title="ATAC-seq",
    organ="pancreas",
    biosample_type="tissue",
    limit=100
)

# DNase-seq
encode_search_experiments(
    assay_title="DNase-seq",
    organ="pancreas",
    biosample_type="tissue",
    limit=100
)
```

Present a summary to the user:
- Total ATAC-seq experiments
- Total DNase-seq experiments
- Labs represented
- Whether to use one or both assay types

### Combining ATAC + DNase?
Ask the user:
- **Same assay only** (purest comparison, no cross-platform effects)
- **Both assays combined** (maximum coverage, slight platform variation)

For a comprehensive accessibility catalog, combining both is scientifically justified.

## Step 2: Quality-Gate Each Experiment

```
encode_get_experiment(accession="ENCSR...")
```

### ATAC-seq Quality Checks
- Audit status: no ERROR flags
- Has IDR thresholded peaks
- Low mitochondrial read fraction (ENCODE pipeline removes these)
- Good TSS enrichment score
- Nucleosome-free fragment enrichment visible

### DNase-seq Quality Checks
- Audit status: no ERROR flags
- Has Hotspot2 peaks or IDR thresholded peaks
- Adequate sequencing depth (20M+ mapped reads)
- Signal-to-noise ratio

Track all included experiments:
```
encode_track_experiment(accession="ENCSR...")
```

## Step 3: Download Peak Files

For each experiment:

```
# ATAC-seq — IDR thresholded peaks
encode_list_files(
    experiment_accession="ENCSR...",
    file_format="bed",
    output_type="IDR thresholded peaks",
    assembly="GRCh38"
)

# DNase-seq — may use different output types
encode_list_files(
    experiment_accession="ENCSR...",
    file_format="bed",
    output_type="peaks",
    assembly="GRCh38"
)
```

Prefer `preferred_default=True` files.

```
encode_download_files(
    file_accessions=["ENCFF...", ...],
    download_dir="/path/to/data/accessibility",
    organize_by="flat"
)
```

## Step 4: Per-Sample Noise Filtering

### 4a. ENCODE Blocklist Filtering (Amemiya et al. 2019)
```bash
# Download from: https://github.com/Boyle-Lab/Blacklist/blob/master/lists/hg38-blacklist.v2.bed.gz
bedtools intersect -a sample.narrowPeak -b hg38-blacklist.v2.bed -v > sample.filtered.narrowPeak
```

### 4b. SignalValue Filtering (Perna et al. 2024)
Same logic as histone aggregation — filter per-sample to top 75% by signalValue (column 7):
```bash
# Per-sample: remove bottom 25% by signalValue (true distribution quantile)
TOTAL=$(wc -l < sample.filtered.narrowPeak)
LINE_25=$(echo "$TOTAL" | awk '{printf "%d", $1 * 0.25}')
THRESHOLD=$(sort -k7,7n sample.filtered.narrowPeak | awk -v line="$LINE_25" 'NR==line{print $7}')
awk -v t="$THRESHOLD" '$7 >= t' sample.filtered.narrowPeak > sample.qfiltered.narrowPeak
```

### 4c. ATAC-specific: Remove Sub-nucleosomal Artifacts (optional)
For ATAC-seq, very narrow peaks (<50bp) can be Tn5 insertion artifacts:
```bash
awk '($3-$2) >= 50' sample.qfiltered.narrowPeak > sample.clean.narrowPeak
```

## Step 5: Union Merge

Accessibility peaks are **narrow/point-source** (like H3K4me3). Use default merge (overlap only, no gap tolerance).

**CRITICAL**: Tag peaks by sample before concatenation to count unique SAMPLES, not overlapping peaks:

```bash
# Tag each sample's peaks with a unique sample ID
awk -v sid="atac_s1" 'BEGIN{OFS="\t"} {$4=sid; print}' atac_sample1.qfiltered.narrowPeak > atac_s1.tagged.bed
awk -v sid="dnase_s1" 'BEGIN{OFS="\t"} {$4=sid; print}' dnase_sample1.qfiltered.narrowPeak > dnase_s1.tagged.bed
# ... repeat for all samples

# Concatenate all tagged peaks (ATAC + DNase combined or separate)
cat *.tagged.bed > all_accessibility.bed

# Sort
bedtools sort -i all_accessibility.bed > all_accessibility.sorted.bed

# Union merge — count UNIQUE SAMPLES (not peaks)
bedtools merge \
    -i all_accessibility.sorted.bed \
    -c 4,7,9 \
    -o count_distinct,max,max \
    > union_accessible_regions.bed
# Columns: chr, start, end, n_unique_samples, max_signalValue, max_qValue
```

### If Tracking Assay Source
To annotate whether peaks came from ATAC, DNase, or both:
```bash
# Add assay tag to each peak before concatenation
awk '{print $0"\tATAC"}' atac_peaks.bed > tagged.bed
awk '{print $0"\tDNase"}' dnase_peaks.bed >> tagged.bed

# After merge, use bedtools multiIntersect to track sources
bedtools multiIntersect \
    -i atac_sample1.bed atac_sample2.bed dnase_sample1.bed ... \
    -header \
    -names ATAC_1 ATAC_2 DNase_1 ... \
    > multi_intersect.bed
```

## Step 6: Confidence Annotation

Same logic as histone aggregation. Given N total samples:

| Confidence | Criteria | Interpretation |
|-----------|----------|----------------|
| **High** | ≥50% of samples | Constitutive accessible region |
| **Supported** | 2+ samples | Likely real, some variation |
| **Singleton** | 1 sample only | Keep — may be individual-specific or condition-specific |

```bash
awk -v N=8 '{
    if ($4 >= N*0.5) conf="HIGH";
    else if ($4 >= 2) conf="SUPPORTED";
    else conf="SINGLETON";
    print $0"\t"conf"\t"$4"/"N
}' union_accessible_regions.bed > union_accessible_regions.annotated.bed
```

## Step 7: Log Provenance

```
encode_log_derived_file(
    file_path="/path/to/union_accessible_regions.annotated.bed",
    source_accessions=["ENCSR...", "ENCSR...", ...],
    description="Union chromatin accessibility peaks (ATAC-seq + DNase-seq) across N pancreas samples",
    file_type="aggregated_accessibility",
    tool_used="bedtools merge v2.31.0",
    parameters="blocklist filtered, signalValue >= 25th pctl per sample, ATAC min width 50bp, bedtools merge -d 0"
)
```

## Step 8: Summary Statistics

Report to the user:
- Total input experiments: N (ATAC: X, DNase: Y)
- Experiments passing QC: M
- Total peaks before merge: X
- Union peaks after merge: Y
- High-confidence regions: Z (≥50% support)
- Supported regions: W (2+ support)
- Singleton regions: V (1 sample only)
- Genome coverage: bp covered / total genome
- Overlap between ATAC-only and DNase-only peaks (if both assays used)

## Pitfalls Specific to Accessibility Data

1. **ATAC mitochondrial reads**: ENCODE pipeline removes these, but verify in QC metrics. High mitochondrial fraction indicates poor nuclear chromatin enrichment.

2. **Tn5 sequence bias**: ATAC-seq Tn5 has mild sequence preference. For union maps this is acceptable — bias affects peak *intensity*, not *presence*.

3. **DNase hypersensitivity saturation**: Deeply sequenced DNase-seq detects more sites. Shallowly sequenced samples contribute fewer peaks but are not wrong — they just miss weaker sites.

4. **Promoter enrichment**: Both assays are enriched at promoters. When comparing accessibility across tissues, note that promoter accessibility is largely constitutive while enhancer accessibility is tissue-specific.

5. **Cell-type heterogeneity in tissue samples**: Bulk ATAC/DNase from tissue captures accessibility across ALL cell types. A peak may represent a minor cell population. This is correct for a tissue-level map but important to note.

6. **Do NOT mix assemblies**: All files must be GRCh38 or all hg19. Use `encode_compare_experiments` to verify.

7. **Peak summits lost after merge**: NarrowPeak column 10 (summit offset) is discarded by `bedtools merge`. If you need summits for motif analysis, extract them before merging and map back afterward.

8. **CUT&RUN/CUT&Tag accessibility data**: If ENCODE adds CUT&RUN-based accessibility data in the future, apply the CUT&RUN suspect list (Nordin et al. 2023, Genome Biology) in addition to the ENCODE blacklist.

## Walkthrough: Building a Pan-Donor Accessibility Map for Brain Cortex

**Goal**: Merge ATAC-seq peaks from 4 brain cortex experiments into a union accessibility map.
**Context**: User needs comprehensive open chromatin regions for regulatory element discovery.

### Step 1: Search for brain ATAC-seq experiments

```
encode_search_experiments(
  assay_title="ATAC-seq",
  organ="brain"
)
```

Expected output:
```json
{
  "total": 24,
  "experiments": [
    {"accession": "ENCSR001BRN", "biosample_summary": "brain cortex tissue male adult (53 years)"},
    {"accession": "ENCSR002BRN", "biosample_summary": "brain cortex tissue female adult (49 years)"}
  ]
}
```

### Step 2: Download narrowPeak files

```
encode_search_files(
  assay_title="ATAC-seq",
  organ="brain",
  file_format="bed",
  output_type="IDR thresholded peaks",
  assembly="GRCh38"
)
```

Expected output:
```json
{
  "total": 8,
  "files": [{"accession": "ENCFF001ATQ", "output_type": "IDR thresholded peaks", "assembly": "GRCh38"}]
}
```

### Step 3: Merge into union peak set

```bash
cat *.narrowPeak | sort -k1,1 -k2,2n | bedtools merge -i - -c 4,5 -o count,mean > union_atac_brain.bed
```

**Interpretation**: Union peaks represent all genomic positions where chromatin is accessible in brain cortex. Peaks found in all 4 donors are constitutive regulatory elements.

## Code Examples

### 1. Find accessibility data for aggregation

```
encode_get_facets(organ="pancreas", assay_title="ATAC-seq")
```

Expected output:
```json
{
  "facets": {"biosample_term_name": {"pancreas": 4, "pancreatic islet": 3}, "status": {"released": 6}}
}
```

## Integration

| This skill produces... | Feed into... | Using tool/skill |
|---|---|---|
| Union open chromatin map (BED) | Enhancer identification | regulatory-elements skill |
| Accessible regions for motif analysis | TF motif discovery | motif-analysis skill |
| Tissue accessibility catalog | Cross-tissue comparison | compare-biosamples skill |
| Open chromatin at variant sites | Variant functional annotation | variant-annotation skill |
| Accessible peak coordinates | Visualization signal anchors | visualization-workflow skill |

## Related Skills

- **histone-aggregation**: Same union approach for histone ChIP-seq narrowPeak data
- **methylation-aggregation**: Different approach (averaging) for continuous methylation signal; HMRs + accessibility peaks mark active regulatory elements
- **hic-aggregation**: Union approach for BEDPE chromatin loops; loops often anchor at accessible regions
- **regulatory-elements**: Use union accessibility maps to define active regulatory elements with histone mark combinations
- **motif-analysis**: Find enriched TF motifs in accessible regions using HOMER and MEME
- **pipeline-atacseq**: Process raw ATAC-seq data through the full ENCODE-aligned pipeline
- **batch-analysis**: Batch processing workflows for systematic accessibility aggregation
- **publication-trust**: Verify literature claims backing analytical decisions

## Presenting Results

- Present merged accessibility regions as: chr | start | end | assay_type | sample_count. Show ATAC vs DNase contribution. Suggest: "Would you like to run motif analysis on these accessible regions?"

## For the request: "$ARGUMENTS"
