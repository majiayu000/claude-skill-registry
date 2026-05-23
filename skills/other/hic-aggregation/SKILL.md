---
name: hic-aggregation
description: Build comprehensive chromatin contact maps by aggregating Hi-C loop calls (BEDPE) across multiple ENCODE experiments, donors, and labs. Use when the user wants to answer "what regions are in 3D contact in my tissue?" by creating a union catalog of chromatin loops. Handles resolution-aware anchor matching, cross-lab variation, and Hi-C-specific quality metrics.
---

# Aggregate Hi-C Chromatin Contacts Across Studies

## When to Use

- User wants to build a comprehensive catalog of chromatin loops from multiple Hi-C experiments
- User asks "what regions are in 3D contact in my tissue?" or "aggregate loop calls across donors"
- User needs a union catalog of BEDPE loops with resolution-aware anchor matching
- User wants to identify high-confidence loops supported by multiple experiments
- Example queries: "aggregate Hi-C loops for K562", "combine chromatin contacts across labs", "find consensus TAD boundaries in liver"

Build a comprehensive catalog of chromatin loops for a tissue/cell type by merging BEDPE loop calls from multiple ENCODE Hi-C experiments.

## Scientific Rationale

**The question**: "What regions are in 3D physical contact in my tissue?"

Like histone marks and accessibility, chromatin loops are a **detection question**. If a loop between Region A and Region B is detected in one donor but not another, the contact is still real — individual variation, sequencing depth, and computational resolution explain absence. We want the **union of all detected contacts**.

### Key Concepts

**Hi-C data** measures pairwise chromatin interactions genome-wide. After processing:
- **Contact matrix** (`.hic` file): Genome-wide interaction frequencies at multiple resolutions
- **Loop calls** (BEDPE): Statistically significant point interactions (loops) identified by algorithms like HICCUPS or Juicer
- **TAD boundaries**: Topologically associating domain boundaries
- **Compartments**: A/B compartment assignments

**BEDPE format** (Paired-End BED):
```
chr1  start1  end1  chr2  start2  end2  name  score  strand1  strand2
```
Each row represents a contact between two genomic anchor regions.

### Literature Support
- **Loop Catalog** (Reyna et al. 2025, Nucleic Acids Research): Created a union catalog of 4.19M unique loops across 1,089 Hi-C datasets. Demonstrated that union approach captures tissue-specific and constitutive loops. Used resolution-aware merging at 5kb, 10kb, and 25kb bins.
- **AQuA Tools** (Chakraborty et al. 2025): Toolkit for BEDPE intersection, union, and annotation. Handles paired-region arithmetic.
- **mariner** (Flores et al. 2024, Bioinformatics): R/Bioconductor package for BEDPE manipulation including merging loops across experiments with configurable anchor tolerance.
- **ENCODE Phase 3** (Gorkin et al. 2020, Nature, 301 citations): Integrated Hi-C data across tissues to define regulatory loops connecting enhancers to promoters.
- **ENCODE Blacklist** (Amemiya et al. 2019, Scientific Reports, 1,372 citations): Problematic genomic regions to filter from loop anchors. [DOI](https://doi.org/10.1038/s41598-019-45839-z)
- **Mustache** (Roayaei Ardakany et al. 2020, Genome Biology, 165 citations): Multi-scale loop caller that recovers more validated loops than HICCUPS. Different callers produce discordant loop sets.
- **Wolff et al. 2022** (GigaScience): Benchmark showing loop callers intersect by **~50% at most** — critical context for why union approach is necessary.

## Step 1: Find All Available Hi-C Data

```
encode_search_experiments(
    assay_title="Hi-C",
    organ="pancreas",           # user's tissue of interest
    biosample_type="tissue",
    limit=100
)
```

Present a summary to the user:
- Total Hi-C experiments
- Labs represented
- Unique donors/biosamples
- Resolution(s) available (check experiment metadata)

Use `encode_get_facets` to check availability:
```
encode_get_facets(assay_title="Hi-C", organ="pancreas")
```

**Note**: Hi-C data is computationally expensive to produce, so there are typically fewer experiments per tissue than ChIP-seq or ATAC-seq. Even 2-3 experiments can be valuable for union catalogs.

## Step 2: Quality-Gate Each Experiment

```
encode_get_experiment(accession="ENCSR...")
```

### Hi-C Quality Checks
- Audit status: no ERROR flags
- **Sequencing depth**: 400M+ valid read pairs for loop calling (ENCODE standard)
- **Cis/trans ratio**: >60% cis contacts expected (low cis suggests noisy library)
- **Hi-C-specific QC**: Library complexity, PCR duplicate rate
- Has loop calls (BEDPE output) — not all Hi-C experiments have called loops
- Resolution: at least 5-10kb resolution for loop detection

### Include if:
- Has BEDPE loop calls at consistent resolution
- Passes ENCODE audit (no ERROR flags)
- Adequate sequencing depth for loop resolution

### Exclude if:
- ERROR audit flags
- Only contact matrices without loop calls
- Very low sequencing depth (<200M valid pairs — insufficient for loop calling)

Track all included experiments:
```
encode_track_experiment(accession="ENCSR...")
```

## Step 3: Download Loop Call Files

For each experiment, get BEDPE loop calls:

```
# Search for loop/interaction files
encode_list_files(
    experiment_accession="ENCSR...",
    file_format="bedpe",
    assembly="GRCh38"
)

# Also check for BED-formatted loop files
encode_list_files(
    experiment_accession="ENCSR...",
    output_type="chromatin interactions",
    assembly="GRCh38"
)

# Or contact domains
encode_list_files(
    experiment_accession="ENCSR...",
    output_type="contact domains",
    assembly="GRCh38"
)
```

**File selection priority:**
1. **Chromatin interactions** (loop calls from HICCUPS or similar)
2. **Contact domains** (TADs — different analysis, handle separately)
3. **Replicated loops** (if available)

Prefer `preferred_default=True` files when available.

```
encode_download_files(
    file_accessions=["ENCFF...", ...],
    download_dir="/path/to/data/hic_loops",
    organize_by="flat"
)
```

## Step 4: Understanding Hi-C Resolution and Anchors

### Critical: Resolution-Aware Processing

Hi-C loop anchors are **binned regions**, not precise positions. The resolution determines anchor size:

| Resolution | Anchor Width | Best For | Typical Loop Count |
|-----------|-------------|---------|-------------------|
| 5 kb | 5,000 bp | Fine-scale promoter-enhancer loops | More loops |
| 10 kb | 10,000 bp | Standard analysis | Moderate |
| 25 kb | 25,000 bp | Large-scale domain contacts | Fewer loops |

**All loops being merged must be at the same resolution**, or anchors must be harmonized to a common resolution.

### Harmonizing Resolution
If experiments have loops called at different resolutions:
```bash
# Expand 5kb anchors to 10kb resolution
awk -v res=10000 'BEGIN{OFS="\t"} {
    # Bin anchor 1
    bin1_start = int($2/res) * res
    bin1_end = bin1_start + res
    # Bin anchor 2
    bin2_start = int($5/res) * res
    bin2_end = bin2_start + res
    print $1, bin1_start, bin1_end, $4, bin2_start, bin2_end, $7, $8, $9, $10
}' fine_res_loops.bedpe > harmonized_loops.bedpe
```

## Step 5: Per-Sample Filtering

### 5a. ENCODE Blocklist Filtering (Amemiya et al. 2019)
Remove loops with anchors in artifact-prone regions (download from https://github.com/Boyle-Lab/Blacklist/blob/master/lists/hg38-blacklist.v2.bed.gz):
```bash
# Filter loops where EITHER anchor overlaps a blocklist region
# First, extract anchor 1 and anchor 2 as separate BED files
awk 'BEGIN{OFS="\t"} {print $1,$2,$3,NR}' sample.bedpe > anchors1.bed
awk 'BEGIN{OFS="\t"} {print $4,$5,$6,NR}' sample.bedpe > anchors2.bed

# Find anchor rows NOT in blocklist
bedtools intersect -a anchors1.bed -b ENCODE_blocklist.bed -v | cut -f4 > clean_rows_1.txt
bedtools intersect -a anchors2.bed -b ENCODE_blocklist.bed -v | cut -f4 > clean_rows_2.txt

# Keep only rows where BOTH anchors pass
comm -12 <(sort clean_rows_1.txt) <(sort clean_rows_2.txt) > clean_rows.txt
awk 'NR==FNR{a[$1];next} FNR in a' clean_rows.txt sample.bedpe > sample.filtered.bedpe
```

### 5b. Score Filtering
Filter by interaction score/significance:
```bash
# If BEDPE has a score column (col 8), filter to significant interactions
# Keep top 75% by score (true distribution quantile, not range-based)
TOTAL=$(wc -l < sample.filtered.bedpe)
LINE_25=$(echo "$TOTAL" | awk '{printf "%d", $1 * 0.25}')
THRESHOLD=$(sort -k8,8n sample.filtered.bedpe | awk -v line="$LINE_25" 'NR==line{print $8}')
awk -v t="$THRESHOLD" '$8 >= t' sample.filtered.bedpe > sample.qfiltered.bedpe
```

### 5c. Remove Self-Ligation Artifacts
Loops where both anchors are very close are likely artifacts:
```bash
# Remove loops where anchors are on same chromosome and < 20kb apart
awk '{
    if ($1 != $4) print $0;  # inter-chromosomal: keep (rare but real)
    else if (($5 - $3) >= 20000) print $0;  # > 20kb apart: keep
}' sample.qfiltered.bedpe > sample.clean.bedpe
```

## Step 6: Union Merge of Loops

### The Paired-Region Matching Problem

Unlike peaks (single regions), loops are **pairs of regions**. Two loops match if **both anchors overlap**:

```
Loop 1:  [anchor1A]--------[anchor1B]
Loop 2:    [anchor2A]------[anchor2B]
```

These should merge if anchor1A overlaps anchor2A AND anchor1B overlaps anchor2B.

### Method A: bedtools pairToPair (Recommended for simple union)

```bash
# Concatenate all filtered loops
cat sample1.clean.bedpe sample2.clean.bedpe ... > all_loops.bedpe

# Sort by anchor 1 coordinates
sort -k1,1 -k2,2n -k4,4 -k5,5n all_loops.bedpe > all_loops.sorted.bedpe

# Use a custom merge approach:
# 1. Bin anchors to resolution, creating a loop ID
# 2. Group by loop ID
# 3. Count support

awk -v res=10000 'BEGIN{OFS="\t"} {
    # Create binned anchor coordinates as loop identifier
    a1_bin = $1 ":" int($2/res)*res
    a2_bin = $4 ":" int($5/res)*res
    # Canonical order (smaller coordinate first) to handle orientation
    if (a1_bin < a2_bin) loop_id = a1_bin "-" a2_bin
    else loop_id = a2_bin "-" a1_bin
    print loop_id, $0
}' all_loops.sorted.bedpe | \
sort -k1,1 | \
awk 'BEGIN{OFS="\t"} {
    if ($1 != prev_id) {
        if (NR > 1) print chr1, start1, end1, chr2, start2, end2, count, max_score
        prev_id = $1
        chr1=$2; start1=$3; end1=$4; chr2=$5; start2=$6; end2=$7
        count = 1; max_score = $9
    } else {
        count++
        if ($9 > max_score) max_score = $9
        # Expand anchors to encompass all overlapping calls
        if ($3 < start1) start1 = $3
        if ($4 > end1) end1 = $4
        if ($6 < start2) start2 = $6
        if ($7 > end2) end2 = $7
    }
} END {
    print chr1, start1, end1, chr2, start2, end2, count, max_score
}' > union_loops.bedpe
```

### Method B: Resolution-Binned Approach (Loop Catalog method)

Following the Loop Catalog (Reyna et al. 2025) approach:

```bash
# Bin all loop anchors to a fixed resolution
awk -v res=10000 'BEGIN{OFS="\t"} {
    a1_start = int($2/res) * res
    a1_end = a1_start + res
    a2_start = int($5/res) * res
    a2_end = a2_start + res
    # Canonical ordering
    if ($1 < $4 || ($1 == $4 && a1_start <= a2_start))
        print $1, a1_start, a1_end, $4, a2_start, a2_end
    else
        print $4, a2_start, a2_end, $1, a1_start, a1_end
}' all_loops.sorted.bedpe | \
sort -u | \
sort -k1,1 -k2,2n -k4,4 -k5,5n | \
uniq -c | \
awk 'BEGIN{OFS="\t"} {print $2,$3,$4,$5,$6,$7,$1}' > union_loops_binned.bedpe
# Columns: chr1, start1, end1, chr2, start2, end2, n_supporting_samples
```

### Method C: Using Specialized Tools

**mariner** (R/Bioconductor):
```r
library(mariner)
# Read BEDPE files as GInteractions
loops <- lapply(bedpe_files, read.table)
# Convert to GInteractions and merge
gi <- as_ginteractions(loops)
merged <- mergePairs(gi, radius = 10000)  # 10kb tolerance
```

**AQuA Tools** (Python):
```python
# BEDPE union with anchor overlap tolerance
aqua bedpe-union -i sample1.bedpe sample2.bedpe -o union.bedpe --slop 5000
```

## Step 7: Confidence Annotation

Given N total experiments:

| Confidence | Criteria | Interpretation |
|-----------|----------|----------------|
| **High** | Detected in >=50% of samples | Constitutive loop, present across individuals |
| **Supported** | Detected in 2+ samples | Likely real, some variation |
| **Singleton** | Detected in 1 sample only | May be individual-specific or depth-dependent |

```bash
awk -v N=4 '{
    if ($7 >= N*0.5) conf="HIGH";
    else if ($7 >= 2) conf="SUPPORTED";
    else conf="SINGLETON";
    print $0"\t"conf"\t"$7"/"N
}' union_loops_binned.bedpe > union_loops.annotated.bedpe
```

**Context for singletons**: Hi-C loop detection is very sensitive to sequencing depth. Many singletons may simply be under-powered in other samples rather than biologically absent. The Loop Catalog found that a union approach captures ~3x more loops than any individual experiment.

## Step 8: Separate Analysis for TADs and Compartments

**TAD boundaries** and **A/B compartments** require different aggregation than loops:

### TAD Boundaries
TAD boundaries are single genomic positions. Aggregate like narrow peaks:
```bash
# Extract TAD boundary BED from contact domain files
# Each boundary is a narrow region
cat tad_boundaries_sample*.bed | \
bedtools sort -i - | \
bedtools merge -i - -d 40000 -c 1 -o count > union_tad_boundaries.bed
# 40kb gap tolerance because TAD boundaries are resolution-dependent
```

### A/B Compartments
Compartment calls (eigenvector sign at each bin) should be aggregated by majority vote:
```bash
# For each resolution bin, assign A or B based on majority of samples
# This is more complex and typically done in R/Python
```

## Step 9: Log Provenance

```
encode_log_derived_file(
    file_path="/path/to/union_loops.annotated.bedpe",
    source_accessions=["ENCSR...", "ENCSR...", ...],
    description="Union chromatin loops across N pancreas Hi-C experiments",
    file_type="aggregated_loops",
    tool_used="bedtools + custom merge at 10kb resolution",
    parameters="blocklist filtered, score >= 25th pctl, self-ligation >= 20kb removed, 10kb resolution binning"
)
```

## Step 10: Summary Statistics

Report to the user:
- Total input experiments: N
- Experiments passing QC: M
- Resolution used: Xkb
- Total loops before merge: X
- Union loops after merge: Y
- High-confidence loops: Z (≥50% support)
- Supported loops: W (2+ support)
- Singleton loops: V (1 sample only)
- Distance distribution: median and range of loop sizes (anchor-to-anchor)
- Inter-chromosomal loops: count (expect very few)

## Pitfalls Specific to Hi-C Data

1. **Resolution mismatch**: Loop calls at 5kb vs 25kb resolution will have very different anchor sizes. Always harmonize to a common resolution before merging.

2. **Sequencing depth sensitivity**: Loop calling requires deep sequencing (400M+ valid pairs). Shallowly sequenced experiments will call far fewer loops — this is under-detection, not absence.

3. **Algorithm differences are LARGE**: Wolff et al. 2022 (GigaScience) found that HICCUPS, Mustache, Fit-Hi-C, and HiCExplorer loop callers **intersect by ~50% at most**. Mustache tends to recover more validated loops (Roayaei Ardakany et al. 2020). If mixing callers, note this in provenance — and this discordance is itself a reason to prefer the union approach.

4. **Orientation matters**: BEDPE anchors should be canonically ordered (anchor1 < anchor2 by genomic coordinate) before merging to avoid duplicate counting.

5. **Inter-chromosomal contacts**: These are rare but real. Handle separately — they cannot be distance-filtered.

6. **Distance distribution**: Most loops are 100kb-2Mb. Very short-range contacts (<20kb) are often noise from undigested chromatin. Very long-range (>10Mb) are rare.

7. **Do NOT mix assemblies**: All files must be GRCh38 or all hg19. Hi-C resolution binning makes liftOver of loops particularly error-prone.

8. **TADs vs loops**: These are different features. TADs are domains (regions), loops are point contacts (pairs). Do not mix them in the same union.

9. **Micro-C as complement**: Micro-C achieves higher resolution than Hi-C and can detect sub-TAD loops. Treat Micro-C loops as compatible with Hi-C loops in a union (Mustache works on both).

## Walkthrough: Building a Cross-Tissue Loop Catalog for the MYC Locus

**Goal**: Aggregate Hi-C chromatin loops across tissues to identify conserved and tissue-specific 3D contacts at the MYC gene locus.
**Context**: Cancer research — MYC is regulated by distal enhancers via chromatin looping.

### Step 1: Find Hi-C experiments across tissues

```
encode_search_experiments(assay_title="Hi-C", organism="Homo sapiens", limit=50)
```

Expected output:
```json
{
  "total": 89,
  "results": [
    {"accession": "ENCSR000AKA", "assay_title": "Hi-C", "biosample_summary": "GM12878", "status": "released"},
    {"accession": "ENCSR489OCU", "assay_title": "Hi-C", "biosample_summary": "K562", "status": "released"},
    {"accession": "ENCSR382RFU", "assay_title": "Hi-C", "biosample_summary": "liver", "status": "released"}
  ]
}
```

**Interpretation**: 89 Hi-C experiments available. Select 5–10 spanning diverse tissue types for cross-tissue comparison.

### Step 2: List loop files for each experiment

```
encode_list_files(accession="ENCSR000AKA", file_format="bedpe", assembly="GRCh38")
```

Expected output:
```json
{
  "files": [
    {"accession": "ENCFF001ABC", "output_type": "contact domains", "file_format": "bedpe", "file_size_mb": 2.4},
    {"accession": "ENCFF002DEF", "output_type": "chromatin interactions", "file_format": "bedpe", "file_size_mb": 1.8}
  ]
}
```

**Interpretation**: Use "chromatin interactions" files for loop aggregation. Contact domains are TADs, not loops.

### Step 3: Download loop files

```
encode_download_files(accessions=["ENCFF002DEF", "ENCFF003GHI", "ENCFF004JKL"], download_dir="/data/hic_loops")
```

Expected output:
```json
{
  "downloaded": 3,
  "total_size_mb": 5.6,
  "md5_verified": true,
  "files": ["/data/hic_loops/ENCFF002DEF.bedpe", "/data/hic_loops/ENCFF003GHI.bedpe", "/data/hic_loops/ENCFF004JKL.bedpe"]
}
```

### Step 4: Aggregate loops with resolution-aware anchor matching

Apply union merge across tissues:
- Expand loop anchors by ±resolution (e.g., ±5kb for 5kb resolution data)
- Merge overlapping anchors using bedtools pairToPair
- Assign tissue support counts to each union loop
- Filter: require ≥2 tissue support for conserved loops

### Step 5: Filter to MYC locus

```bash
# MYC locus: chr8:127,700,000-128,000,000
awk '$1=="chr8" && $2>=127700000 && $3<=128000000' union_loops.bedpe > myc_loops.bedpe
```

**Interpretation**: Loops anchored at the MYC promoter connecting to distal enhancers. Conserved loops (≥3 tissues) likely represent fundamental regulatory architecture; tissue-specific loops may drive context-dependent MYC activation.

### Integration with downstream skills
- Feed loop anchors into → **peak-annotation** for gene assignment at anchor regions
- Overlay with → **histone-aggregation** H3K27ac peaks to identify active enhancer-promoter loops
- Cross-reference loop-disrupting variants via → **variant-annotation**
- Visualize in → **ucsc-browser** as interaction tracks

## Code Examples

### 1. Survey available Hi-C data by tissue
```
encode_get_facets(assay_title="Hi-C", facet_field="organ", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {
    "organ": {"brain": 24, "heart": 12, "liver": 8, "lung": 6, "kidney": 4, "blood": 15}
  }
}
```

### 2. Get details for a specific Hi-C experiment
```
encode_get_experiment(accession="ENCSR000AKA")
```

Expected output:
```json
{
  "accession": "ENCSR000AKA",
  "assay_title": "Hi-C",
  "biosample_summary": "GM12878",
  "replicates": 2,
  "status": "released",
  "lab": "/labs/erez-lieberman-aiden/",
  "audit": {"WARNING": 1, "ERROR": 0}
}
```

### 3. Compare loop sets between two cell types
```
encode_compare_experiments(accession_1="ENCSR000AKA", accession_2="ENCSR489OCU")
```

Expected output:
```json
{
  "comparison": {
    "shared": {"assay": "Hi-C", "organism": "Homo sapiens", "assembly": "GRCh38"},
    "differences": {
      "biosample": ["GM12878", "K562"],
      "lab": ["/labs/erez-lieberman-aiden/", "/labs/erez-lieberman-aiden/"]
    }
  }
}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Union loop catalog (BEDPE) | **peak-annotation** | Assign genes to loop anchors |
| Conserved loop coordinates | **histone-aggregation** | Overlay H3K27ac at anchors to find active enhancer-promoter loops |
| Tissue-specific loops | **accessibility-aggregation** | Check if loop anchors overlap open chromatin |
| Loop anchor BED intervals | **variant-annotation** | Find GWAS/clinical variants disrupting loop anchors |
| Loop anchor coordinates | **liftover-coordinates** | Convert hg19 loops to GRCh38 |
| Aggregated loop statistics | **visualization-workflow** | Generate loop frequency heatmaps |
| Loop-gene assignments | **disease-research** | Connect loop disruptions to disease phenotypes |

## Related Skills

- **histone-aggregation**: Loop anchors often overlap with H3K27ac/H3K4me1 peaks — integrate with histone union sets to annotate loop function
- **accessibility-aggregation**: Loop anchors frequently coincide with accessible chromatin — validate loops by requiring anchor accessibility
- **regulatory-elements**: Use loops to connect distal enhancers (H3K27ac) to target promoters (H3K4me3)
- **epigenome-profiling**: Loops add 3D context to 1D chromatin state maps
- **pipeline-hic**: Process raw Hi-C data through the full ENCODE-aligned pipeline
- **batch-analysis**: Batch processing workflows for systematic Hi-C loop aggregation
- **publication-trust**: Verify literature claims backing analytical decisions

## Presenting Results

- Present aggregated loops as: chr | anchor1_start | anchor1_end | anchor2_start | anchor2_end | sample_count | resolution. Show loop statistics. Suggest: "Would you like to check if any GWAS variants overlap loop anchors?"

## For the request: "$ARGUMENTS"
