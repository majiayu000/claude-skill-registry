---
name: histone-aggregation
description: Build comprehensive histone mark maps by aggregating narrowPeak data across multiple ENCODE experiments, donors, and labs. Use when the user wants to answer "where is this histone mark present in my tissue?" by combining peak calls from multiple studies into a union peak set with confidence annotations. Handles cross-lab batch effects, broad vs narrow marks, and ENCODE blocklist filtering.
---

# Aggregate Histone ChIP-seq Peaks Across Studies

## When to Use

- User wants to combine histone ChIP-seq peaks across multiple ENCODE experiments for a tissue or cell type
- User asks "where is H3K27ac in pancreas?" or "build a histone mark map for liver"
- User needs a union peak set from multiple donors, labs, or replicates
- User wants to create a consensus binding map from multiple ChIP-seq datasets
- Example queries: "aggregate all H3K4me3 peaks in brain", "combine histone marks across donors", "build enhancer map from H3K27ac data"

Build a comprehensive map of histone mark binding for a tissue/cell type by merging narrowPeak files from multiple ENCODE experiments into a union peak set.

## Scientific Rationale

**The question**: "Does my tissue have this histone mark, and at what genomic locations?"

This is a **detection/cataloging** question, not a differential one. Once a histone mark passes noise thresholds (ENCODE IDR, quality metrics), detection is binary — the mark is either bound or not. If detected in one donor but not another, that region is still a real binding site. Individual variation and technical differences (lab, depth, antibody lot) explain *absence*, not that *presence* is spurious.

**Therefore: we want the UNION of all detections, not a consensus.**

### Literature Support
- **ChIP-Atlas** (Oki et al. 2018, EMBO Reports, 597 citations): Integrated >70,000 public ChIP-seq datasets using union of all peak calls
- **ENCODE Phase 3** (Gorkin et al. 2020, Nature, 301 citations): Created unified chromatin state annotations by integrating all peaks across 1,128 ChIP-seq experiments
- **ENCODE Blacklist** (Amemiya et al. 2019, Scientific Reports, 1,372 citations): Defined the comprehensive set of problematic genomic regions to filter from all functional genomics analyses. Essential quality step. [DOI](https://doi.org/10.1038/s41598-019-45839-z)
- **Perna et al. 2024** (BMC Genomics): Found top 25% signalValue peaks most consistent across different processing pipelines — use as per-sample noise filter
- **ChIP-R** (Newell et al. 2020, 26 citations): Rank-product method for combining peaks from multiple replicates without BAMs, works directly on narrowPeak files
- **MSPC** (Jalili et al. 2021, BMC Bioinformatics): Rescues weak-but-real binding sites that IDR discards by exploiting replicates to lower calling thresholds — more sensitive alternative for union-based approaches
- **Hecht et al. 2023** (PLoS Comp Bio): Probability-of-Being-Signal (PBS) approach for cross-dataset comparison with differing read depths

## Step 1: Find All Available Experiments

Search for all histone ChIP-seq data for the target mark and tissue:

```
encode_search_experiments(
    assay_title="Histone ChIP-seq",
    target="H3K4me1",        # or H3K27ac, H3K4me3, H3K27me3, etc.
    organ="pancreas",         # user's tissue of interest
    biosample_type="tissue",  # or "cell line", "primary cell"
    limit=100
)
```

Present a summary table to the user showing:
- Number of experiments found
- Labs represented
- Number of unique donors/biosamples
- Any audit flags

Use `encode_get_facets` first if unsure what's available:
```
encode_get_facets(assay_title="Histone ChIP-seq", organ="pancreas")
```

## Step 2: Quality-Gate Each Experiment

For each experiment, check quality before including:

```
encode_get_experiment(accession="ENCSR...")
```

### Include if:
- Audit status: no ERROR flags (WARNING is acceptable)
- Has IDR thresholded peaks (passed replicate concordance)
- Sequencing depth meets ENCODE standards (10M+ for narrow marks, 20M+ for broad)

### Exclude if:
- ERROR audit flags
- Only pseudoreplicated peaks (no IDR = did not pass reproducibility)
- Known antibody issues (check audit details)

Track all included experiments:
```
encode_track_experiment(accession="ENCSR...")
```

## Step 3: Download IDR Thresholded NarrowPeak Files

For each passing experiment, get the peak files:

```
encode_list_files(
    experiment_accession="ENCSR...",
    file_format="bed",
    output_type="IDR thresholded peaks",
    assembly="GRCh38"
)
```

**File selection priority:**
1. **IDR thresholded peaks** (gold standard — passed replicate concordance)
2. **Optimal IDR peaks** (pooled replicates — most complete set)
3. **Replicated peaks** (alternative peak caller output)

Prefer `preferred_default=True` files when available.

Download all selected files:
```
encode_download_files(
    file_accessions=["ENCFF...", "ENCFF...", ...],
    download_dir="/path/to/data/narrowpeaks",
    organize_by="flat"
)
```

## Step 4: Per-Sample Noise Filtering

**IMPORTANT**: Filter BEFORE merging, not after.

### 4a. ENCODE Blocklist Filtering (Amemiya et al. 2019)
Remove artifact-prone regions (centromeres, telomeres, rDNA repeats, satellite repeats):
```bash
# Download ENCODE blocklist for GRCh38 from:
# https://github.com/Boyle-Lab/Blacklist/blob/master/lists/hg38-blacklist.v2.bed.gz
# For mm10: https://github.com/Boyle-Lab/Blacklist/blob/master/lists/mm10-blacklist.v2.bed.gz
bedtools intersect -a sample.narrowPeak -b hg38-blacklist.v2.bed -v > sample.filtered.narrowPeak
```

### 4b. SignalValue Filtering (Perna et al. 2024)
Filter each sample's peaks to retain those above the 25th percentile signalValue (column 7 in narrowPeak). The top 75% of peaks by signalValue are the most reliable across processing pipelines:
```bash
# Calculate the 25th percentile of the signalValue DISTRIBUTION for this sample
# (This is a true quantile, not 25% of the range)
TOTAL=$(wc -l < sample.filtered.narrowPeak)
LINE_25=$(echo "$TOTAL" | awk '{printf "%d", $1 * 0.25}')
THRESHOLD=$(sort -k7,7n sample.filtered.narrowPeak | awk -v line="$LINE_25" 'NR==line{print $7}')
awk -v t="$THRESHOLD" '$7 >= t' sample.filtered.narrowPeak > sample.qfiltered.narrowPeak
```

**Note**: This is a per-sample filter. Each experiment has different signal distributions. Do NOT apply a universal threshold across samples.

## Step 5: Union Merge Across Samples

### 5a. Handling Broad vs Narrow Marks

Different histone marks have different peak characteristics:

| Mark Class | Examples | Peak Type | Merge Gap (-d) |
|-----------|----------|-----------|----------------|
| Narrow/point | H3K4me3, H3K27ac, H3K4me1, H3K9ac | Sharp peaks | 0 (default, overlap only) |
| Broad/domain | H3K27me3, H3K9me3, H3K36me3 | Wide domains | 1000-5000bp |

### 5b. Label Peaks by Sample Before Merge

**CRITICAL**: To count unique SAMPLES (not overlapping peaks), tag each peak with its sample ID before concatenation:

```bash
# Tag each sample's peaks with a unique sample ID (column 4 = name field)
awk -v sid="sample1" 'BEGIN{OFS="\t"} {$4=sid; print}' sample1.qfiltered.narrowPeak > sample1.tagged.bed
awk -v sid="sample2" 'BEGIN{OFS="\t"} {$4=sid; print}' sample2.qfiltered.narrowPeak > sample2.tagged.bed
# ... repeat for all samples

# Concatenate all tagged peaks
cat sample*.tagged.bed > all_peaks.bed

# Sort by coordinate
bedtools sort -i all_peaks.bed > all_peaks.sorted.bed
```

### 5c. Union Merge Command

```bash
# Merge overlapping peaks, counting UNIQUE SAMPLES (not peaks)
# For NARROW marks (H3K4me3, H3K27ac, H3K4me1):
bedtools merge \
    -i all_peaks.sorted.bed \
    -c 4,7,9 \
    -o count_distinct,max,max \
    > union_peaks.bed
# Output columns: chr, start, end, n_unique_samples, max_signalValue, max_qValue

# For BROAD marks (H3K27me3, H3K9me3, H3K36me3):
bedtools merge \
    -i all_peaks.sorted.bed \
    -d 1000 \
    -c 4,7,9 \
    -o count_distinct,max,max \
    > union_peaks.bed
```

**Why count_distinct matters**: Without it, a sample with 3 overlapping peaks inflates the count to 3 instead of 1, making the confidence annotation wrong.

**Note on broad marks**: H3K27me3, H3K9me3, and H3K36me3 are typically called as **broadPeak** (not narrowPeak) in ENCODE. When downloading, check for `output_type="replicated peaks"` with `file_type="bed broadPeak"`. BroadPeak has the same first 9 columns as narrowPeak minus the summit column.

### 5d. Alternative: bedtools multiIntersect
If you want to know WHICH samples support each region:
```bash
bedtools multiIntersect \
    -i sample1.qfiltered.narrowPeak sample2.qfiltered.narrowPeak ... \
    -header \
    -names sample1 sample2 ... \
    > multi_intersect.bed
```

## Step 6: Confidence Annotation

Annotate each merged region by number of supporting samples. Given N total samples:

| Confidence | Criteria | Interpretation |
|-----------|----------|----------------|
| **High** | Detected in ≥50% of samples | Robust binding site, consistent across donors/labs |
| **Supported** | Detected in 2+ samples | Likely real, some individual/technical variation |
| **Novel/singleton** | Detected in 1 sample only | May be real but could be noise — keep but flag |

```bash
# Add confidence column (assuming N=6 total samples, column 4 = support count)
awk -v N=6 '{
    if ($4 >= N*0.5) conf="HIGH";
    else if ($4 >= 2) conf="SUPPORTED";
    else conf="SINGLETON";
    print $0"\t"conf"\t"$4"/"N
}' union_peaks.bed > union_peaks.annotated.bed
```

**CRITICAL**: Do NOT discard singletons. A peak detected in 1 of 6 donors is still a real binding event in that individual. The question is "can this mark bind here?" — and the answer is yes.

## Step 7: Log Provenance

Record the entire analysis chain:

```
encode_log_derived_file(
    file_path="/path/to/union_peaks.annotated.bed",
    source_accessions=["ENCSR...", "ENCSR...", ...],
    description="Union H3K4me1 peaks across N pancreas samples with confidence annotation",
    file_type="aggregated_peaks",
    tool_used="bedtools merge v2.31.0",
    parameters="blocklist filtered, signalValue >= 25th percentile per sample, bedtools merge -d 0 for narrow marks"
)
```

## Step 8: Summary Statistics

Report to the user:
- Total input experiments: N
- Experiments passing QC: M
- Total peaks before merge: X
- Union peaks after merge: Y
- High-confidence regions: Z (≥50% support)
- Supported regions: W (2+ support)
- Singleton regions: V (1 sample only)
- Genome coverage: bp covered / total genome

## Common Pitfalls

1. **Assembly mismatch**: ALL files must use the same assembly (GRCh38 or hg19). Use `encode_compare_experiments` to verify.

2. **Broad marks need gap tolerance**: H3K27me3 domains can span 10-100kb. Adjacent peaks from different samples should be merged with `-d 1000` or more.

3. **Don't use consensus for cataloging**: Requiring presence in N/M samples discards real biology. Consensus is for high-confidence subsets, not comprehensive catalogs.

4. **Filter noise per-sample, not post-merge**: SignalValue thresholds must be applied within each sample because signal distributions differ by library/sequencing depth.

5. **Antibody lot variation**: Even same-target experiments can have different peak profiles due to antibody batch effects. This is expected — it's why we use the union.

6. **Peak width variation across labs**: Different peak callers and parameters produce different peak widths. `bedtools merge` handles this naturally by collapsing overlaps.

7. **ChIP-R as alternative**: If the user wants a more statistical approach than simple union, recommend ChIP-R (rank-product method on narrowPeak files, no BAMs needed). But for the "is it bound anywhere?" question, union is more appropriate.

8. **Peak summits are lost after merge**: NarrowPeak column 10 encodes the peak summit position (offset from start). `bedtools merge` discards this. If downstream analysis requires summit positions (e.g., motif analysis), extract summits before merging and map back afterward.

9. **CUT&RUN/CUT&Tag data need a separate suspect list**: The ENCODE blacklist was designed for ChIP-seq. Nordin et al. 2023 (Genome Biology) showed CUT&RUN has its own problematic regions. If incorporating CUT&RUN/CUT&Tag data, apply both the ENCODE blacklist AND the CUT&RUN suspect list.

## Histone Mark Interpretation

For detailed biological meaning of each histone mark (writers, erasers, readers, contradictions, cancer-specific states), consult the comprehensive reference at `references/histone-marks-reference.md` (co-located in this skill's references directory). This catalog covers 21 individual marks, ChromHMM combinatorial states, functional categories, and 37 key papers.

Key mark-type considerations for aggregation:
- **Narrow marks** (H3K4me3, H3K27ac, H3K4me1, H3K9ac): Use narrowPeak files, standard merge
- **Broad marks** (H3K27me3, H3K9me3, H3K36me3): Use broadPeak files when available; narrowPeak underestimates domain size
- **Context-dependent marks** (H3K4me1): Meaning depends on co-occurring marks — H3K4me1+H3K27ac = active enhancer, H3K4me1+H3K27me3 = poised enhancer, H3K4me1 alone = primed enhancer (Creyghton et al. 2010, Rada-Iglesias et al. 2011)

## Walkthrough: Building a Consensus H3K27ac Map for Pancreatic Islets

**Goal**: Aggregate H3K27ac peaks from 5 ENCODE experiments into a union peak set for pancreatic islets.
**Context**: User wants to identify all genomic regions with active enhancer marks across multiple donors.

### Step 1: Find all H3K27ac experiments for pancreas

```
encode_search_experiments(
  assay_title="Histone ChIP-seq",
  organ="pancreas",
  target="H3K27ac"
)
```

Expected output:
```json
{
  "total": 5,
  "experiments": [
    {"accession": "ENCSR111PAN", "biosample_summary": "pancreas tissue male adult (44 years)"},
    {"accession": "ENCSR222PAN", "biosample_summary": "pancreas tissue female adult (51 years)"}
  ]
}
```

### Step 2: Download IDR-thresholded peaks for each experiment

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
  "files": [
    {"accession": "ENCFF100PK1", "output_type": "IDR thresholded peaks", "file_size_mb": 1.2},
    {"accession": "ENCFF200PK2", "output_type": "IDR thresholded peaks", "file_size_mb": 1.5}
  ]
}
```

### Step 3: Merge into union peak set with bedtools

```bash
cat *.bed | sort -k1,1 -k2,2n | bedtools merge -i - -c 4,5 -o count,mean > union_h3k27ac_pancreas.bed
```

**Interpretation**: Peaks present in ≥3 of 5 experiments are high-confidence tissue enhancers. Singleton peaks may reflect donor-specific or noise peaks.

## Code Examples

### 1. Search for histone peaks to aggregate

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
  "total": 8,
  "files": [{"accession": "ENCFF999LIV", "output_type": "IDR thresholded peaks", "assembly": "GRCh38"}]
}
```

## Integration

| This skill produces... | Feed into... | Using tool/skill |
|---|---|---|
| Union peak set (BED) | Peak annotation with genes | peak-annotation skill |
| Consensus enhancer map | Chromatin state classification | regulatory-elements skill |
| Multi-donor confidence scores | Quality filtering | quality-assessment skill |
| Tissue histone mark catalog | Cross-tissue comparison | compare-biosamples skill |
| Peak coordinates for motif analysis | TF motif enrichment | motif-analysis skill |

## Related Skills

- **accessibility-aggregation**: Same union approach for ATAC-seq/DNase-seq open chromatin peaks
- **methylation-aggregation**: Different approach (per-CpG averaging) for continuous methylation signal
- **hic-aggregation**: Union approach for BEDPE chromatin loops
- **regulatory-elements**: Use union peak sets from this skill to discover enhancers/promoters via combinatorial histone marks
- **epigenome-profiling**: Build chromatin state maps by integrating multiple histone marks
- **peak-annotation**: Annotate aggregated peaks with genomic features and nearest genes
- **visualization-workflow**: Visualize histone landscapes with genome browser tracks and heatmaps
- **batch-analysis**: Batch processing workflows for systematic histone aggregation across experiments
- **pipeline-chipseq**: Process raw ChIP-seq data through the full ENCODE-aligned pipeline
- **publication-trust**: Verify literature claims backing analytical decisions

## Presenting Results

- Present aggregated peaks as: chromosome | start | end | sample_count | max_signal. Show summary stats: total peaks, median peak width, samples contributing. Suggest: "Would you like to annotate these peaks with genomic features?"

## For the request: "$ARGUMENTS"
