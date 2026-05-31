---
name: motif-analysis
description: "Guide for de novo and known motif enrichment analysis of ENCODE ChIP-seq and ATAC-seq peaks using HOMER and MEME Suite. Use when users need to discover TF binding motifs in peaks, validate ChIP-seq targets, or find co-binding partners. Trigger on: motif analysis, HOMER, MEME, de novo motif, motif enrichment, findMotifsGenome, AME, MEME-ChIP, known motif, TF binding motif, co-factor, motif discovery."
---

# Motif Analysis of ENCODE Peak Data

## When to Use

- User wants to discover transcription factor binding motifs in ChIP-seq or ATAC-seq peaks
- User asks about "motif enrichment", "HOMER", "MEME", or "de novo motif discovery"
- User needs to validate ChIP-seq targets by checking if the expected motif is enriched
- User wants to find co-binding partners or co-factor motifs in peak regions
- Example queries: "find motifs in my CTCF peaks", "run HOMER on ATAC-seq peaks", "what TFs co-bind with p300 in liver?"

Help the user perform de novo and known motif enrichment analysis on ENCODE ChIP-seq and ATAC-seq peaks. Motif analysis serves two critical purposes: (1) validating that ChIP-seq experiments pulled down the expected transcription factor, and (2) discovering co-regulatory partners that co-bind with the target factor. This skill covers the two major tool suites -- HOMER and MEME Suite -- from input preparation through result interpretation.

## Literature Foundation

| Reference | Journal | Key Contribution | DOI | Citations |
|-----------|---------|-----------------|-----|-----------|
| Heinz et al. (2010) | Molecular Cell | HOMER: Simple combinations of lineage-determining TFs prime cis-regulatory elements; introduced findMotifsGenome.pl for ChIP-seq motif analysis | [10.1016/j.molcel.2010.05.004](https://doi.org/10.1016/j.molcel.2010.05.004) | ~6,000 |
| Bailey et al. (2009) | Nucleic Acids Research | MEME Suite: comprehensive tools for motif discovery (MEME), enrichment (AME), scanning (FIMO), and spacing (SpaMo) | [10.1093/nar/gkp335](https://doi.org/10.1093/nar/gkp335) | ~2,500 |
| Bailey & Elkan (1994) | ISMB | Foundational MEME algorithm: expectation maximization for discovering ungapped motifs in biopolymers | PMID: 7584402 | ~4,000 |
| Machanick & Bailey (2011) | Bioinformatics | MEME-ChIP: all-in-one motif analysis pipeline optimized for large ChIP-seq datasets | [10.1093/bioinformatics/btr189](https://doi.org/10.1093/bioinformatics/btr189) | ~1,800 |
| Fornes et al. (2020) | Nucleic Acids Research | JASPAR 2020: curated, non-redundant TF binding profile database; standard reference for known motifs | [10.1093/nar/gkz1001](https://doi.org/10.1093/nar/gkz1001) | ~2,200 |
| Amemiya et al. (2019) | Scientific Reports | ENCODE Blacklist: regions producing artifact signal that can generate spurious motif hits | [10.1038/s41598-019-45839-z](https://doi.org/10.1038/s41598-019-45839-z) | ~1,372 |

## Prerequisites: Input Preparation

### Obtaining ENCODE Peaks

Search for and download ChIP-seq or ATAC-seq peaks:

```
encode_search_experiments(
    assay_title="TF ChIP-seq",
    target="CTCF",
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
    download_dir="/data/motif_analysis/"
)
```

### Preparing Sequences from Peaks

Motif analysis requires DNA sequences, not just genomic coordinates. Extract sequences centered on peak summits:

```bash
# For TF ChIP-seq: extract summit +/- 100bp (200bp window)
awk 'BEGIN{OFS="\t"} {summit=$2+$10; print $1, summit-100, summit+100, $4, $5}' \
    peaks.narrowPeak > summits_200bp.bed

# Remove blacklisted regions (Amemiya et al. 2019)
bedtools intersect -a summits_200bp.bed \
    -b hg38-blacklist.v2.bed -v > summits_clean.bed

# Extract FASTA sequences (requires genome FASTA)
bedtools getfasta -fi hg38.fa -bed summits_clean.bed -fo summits.fa

# For ATAC-seq: use full peak regions (typically 200-500bp)
bedtools getfasta -fi hg38.fa -bed atac_peaks_clean.bed -fo atac_peaks.fa
```

**Critical**: For TF ChIP-seq, always center on the summit (column 10 in narrowPeak format) and use a narrow window (150-250bp). Using the full peak region dilutes the motif signal because TF binding sites are concentrated at the summit. For histone ChIP-seq, use the full peak or a broader window because histone marks cover larger domains.

### Subsampling Large Peak Sets

For peak sets larger than 50,000, subsample the top peaks by signal strength:

```bash
# Sort by signalValue (column 7) descending, take top 10,000
sort -k7,7nr summits_clean.bed | head -10000 > top10k_summits.bed
bedtools getfasta -fi hg38.fa -bed top10k_summits.bed -fo top10k_summits.fa
```

This improves speed without sacrificing sensitivity, as the strongest peaks contain the most consistent motif instances.

## Part 1: HOMER findMotifsGenome

HOMER (Heinz et al. 2010) performs both de novo motif discovery and known motif enrichment in a single command. It is the most widely used tool for ChIP-seq motif analysis.

### 1a. Basic Usage

```bash
findMotifsGenome.pl peaks.bed hg38 homer_output/ \
    -size 200 \
    -mask \
    -p 8 \
    -preparsedDir /data/homer_preparsed/
```

**Key parameters**:

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `-size` | 200 (TF ChIP-seq) | Window around peak center; 200bp captures typical TF binding site + flanking context |
| `-size` | given (histone ChIP-seq) | Use actual peak boundaries for broad marks |
| `-mask` | always include | Mask repeat sequences to avoid spurious repeat-derived motifs |
| `-p` | 8 (or available cores) | Parallel threads for speed |
| `-preparsedDir` | reusable directory | Cache parsed genome for repeated runs |
| `-bg` | background.bed (optional) | Custom background regions; default uses matched GC regions from genome |
| `-mknown` | motifs.motif (optional) | Test specific known motifs in addition to default database |
| `-len` | 8,10,12 (default) | Motif lengths to search; default covers most TF motifs |

### 1b. Output Structure

HOMER produces a structured output directory:

```
homer_output/
    homerResults.html         # De novo motif results (interactive HTML)
    knownResults.html         # Known motif enrichment results
    homerResults/
        motif1.motif          # Position weight matrix for each de novo motif
        motif2.motif
        ...
    knownResults/
        known1.motif          # Matched known motif PWMs
        ...
    homerMotifs.all.motifs    # All de novo motifs in one file
    seq.autonorm.tsv          # Normalization statistics
```

### 1c. HOMER for ATAC-seq Peaks

ATAC-seq peaks represent accessible chromatin, not specific TF binding. Motif analysis on ATAC peaks reveals which TFs occupy accessible regions:

```bash
findMotifsGenome.pl atac_peaks.bed hg38 homer_atac_output/ \
    -size given \
    -mask \
    -p 8
```

Use `-size given` for ATAC-seq to analyze the full accessible region rather than a fixed window.

## Part 2: MEME-ChIP Suite

The MEME Suite (Bailey et al. 2009) provides a complementary approach with different algorithms and additional capabilities for motif spacing analysis and scanning.

### 2a. MEME-ChIP: All-in-One Pipeline

MEME-ChIP runs five tools sequentially: MEME (de novo discovery), DREME (short motif discovery), CentriMo (motif centrality), AME (known motif enrichment), and SpaMo (motif spacing).

```bash
meme-chip \
    -meme-maxw 30 \
    -meme-nmotifs 10 \
    -meme-minw 6 \
    -db JASPAR2024_CORE_vertebrates.meme \
    -o memechip_output/ \
    summits.fa
```

**Required input**: FASTA file of peak sequences (not BED coordinates -- MEME Suite works on sequences, not genomic intervals).

**Key parameters**:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `-meme-maxw` | 30 | Maximum motif width; 30 covers most TF motifs |
| `-meme-minw` | 6 | Minimum motif width |
| `-meme-nmotifs` | 10 | Number of de novo motifs to find |
| `-db` | JASPAR file | Known motif database for enrichment testing |
| `-o` | output directory | Results directory |
| `-meme-mod` | zoops (default) | Zero or one occurrence per sequence; appropriate for ChIP-seq |

### 2b. Individual MEME Suite Tools

**AME (Analysis of Motif Enrichment)**: Known motif enrichment testing, analogous to HOMER's known motif analysis:

```bash
ame --control --shuffle-- \
    --oc ame_output/ \
    summits.fa \
    JASPAR2024_CORE_vertebrates.meme
```

**FIMO (Find Individual Motif Occurrences)**: Scan sequences for individual instances of a specific motif:

```bash
fimo --oc fimo_output/ \
    --thresh 1e-4 \
    target_motif.meme \
    hg38.fa
```

**CentriMo (Central Motif Enrichment)**: Tests whether a motif is enriched at the center of peak sequences, which confirms direct binding (as opposed to indirect/co-factor binding):

```bash
centrimo --oc centrimo_output/ \
    summits.fa \
    JASPAR2024_CORE_vertebrates.meme
```

### 2c. Obtaining the JASPAR Database

The JASPAR database (Fornes et al. 2020) is the standard reference for known TF binding profiles:

```bash
# Download JASPAR 2024 core vertebrate motifs in MEME format
wget https://jaspar.elixir.no/download/data/2024/CORE/JASPAR2024_CORE_vertebrates_non-redundant_pfms_meme.txt \
    -O JASPAR2024_CORE_vertebrates.meme
```

For HOMER, the built-in motif database is used by default. To update:
```bash
perl /path/to/homer/configureHomer.pl -install hg38
```

## Part 3: Interpreting Results

### 3a. Validating ChIP-seq Target

The primary motif in a TF ChIP-seq experiment should match the antibody target. For example:

| ChIP Target | Expected Primary Motif | Consensus Sequence |
|-------------|----------------------|-------------------|
| CTCF | CTCF | CCGCGNGGNGGCAG |
| FOXA2 | Forkhead | TRTTTAC |
| PDX1 | Homeodomain | TAAT |
| NKX6.1 | NK-homeodomain | TTAATTG |
| TP53 | p53 | RRRCWWGYYY |

**If the expected motif is NOT the top hit**: This could indicate (a) antibody cross-reactivity, (b) indirect binding through a co-factor, (c) poor ChIP enrichment, or (d) a secondary binding mode. Check the experiment's ENCODE audit status and FRiP score before concluding the biology is unexpected.

### 3b. Discovering Co-Regulatory Partners

Secondary motifs reveal TFs that co-bind near the primary target. These co-factors are biologically significant:

- **Same-family members**: If FOXA2 ChIP shows FOXA1 and FOXA3 motifs, the antibody may recognize multiple family members, or family members bind adjacent sites
- **Lineage TFs**: Co-enrichment of lineage-determining TFs (e.g., GATA motifs in blood, HNF motifs in liver/pancreas) confirms tissue-specific binding
- **Architectural factors**: CTCF motifs in non-CTCF ChIP experiments often indicate binding near insulator elements
- **AP-1 motifs**: Frequently appear as secondary hits because AP-1 family members occupy many enhancers broadly

### 3c. CentriMo: Motif Centrality

CentriMo tests whether a motif is enriched at the center of peak sequences. This is a powerful validation:

| Centrality Pattern | Interpretation |
|-------------------|---------------|
| Strong central enrichment | Direct binding: the TF physically contacts this motif |
| Uniform distribution | Indirect binding: motif is nearby but not at the binding site |
| Depleted at center, enriched in flanks | Co-factor: binds adjacent to the primary factor |

### 3d. p-Value Interpretation

Both HOMER and MEME report p-values, but they are calculated differently:

- **HOMER**: Uses hypergeometric test comparing motif frequency in target peaks vs background sequences. Reports both p-value and percentage of target/background sequences containing the motif.
- **MEME**: Uses E-value (expected number of motifs with equal or better score found by chance). E-value < 0.05 is significant.
- **AME**: Uses Fisher's exact test by default. Adjusts for multiple testing.

**Multiple testing caveat**: When testing hundreds of known motifs, many will show nominal significance by chance. Focus on motifs with (a) low p-value AND (b) high enrichment fold change AND (c) biological plausibility.

## Complete Workflow

```
Step 1: Obtain ENCODE ChIP-seq/ATAC-seq peaks
    encode_search_experiments(assay_title="TF ChIP-seq", target="CTCF")
    encode_list_files(..., output_type="IDR thresholded peaks")
    encode_download_files(...)

Step 2: Prepare input sequences
    Extract summit +/- 100bp for TF ChIP-seq
    Remove blacklisted regions (Amemiya et al. 2019)
    Subsample to top 10,000 if needed
    Extract FASTA with bedtools getfasta

Step 3: Run HOMER
    findMotifsGenome.pl peaks.bed hg38 output/ -size 200 -mask -p 8

Step 4: Run MEME-ChIP
    meme-chip -meme-maxw 30 -db JASPAR2024.meme -o output/ summits.fa

Step 5: Interpret results
    Primary motif should match ChIP target (validation)
    Secondary motifs reveal co-factors
    CentriMo confirms direct vs indirect binding
    Compare HOMER and MEME results for concordance

Step 6: Document and track
    encode_log_derived_file(
        file_path="/data/motif_results/homerResults.html",
        source_accessions=["ENCSR..."],
        description="HOMER de novo + known motif analysis of CTCF peaks",
        tool_used="HOMER v4.11 findMotifsGenome.pl",
        parameters="-size 200 -mask -p 8"
    )
```

## Code Examples

### Complete HOMER Workflow

```bash
#!/bin/bash
# Full HOMER motif analysis for ENCODE TF ChIP-seq peaks

PEAKS="CTCF_idr_peaks.narrowPeak"
GENOME="hg38"
BLACKLIST="hg38-blacklist.v2.bed.gz"
OUTDIR="homer_CTCF"
THREADS=8

# Step 1: Filter blacklisted regions
bedtools intersect -a $PEAKS -b $BLACKLIST -v > peaks_clean.narrowPeak

# Step 2: Run HOMER (handles summit extraction internally with -size)
findMotifsGenome.pl peaks_clean.narrowPeak $GENOME $OUTDIR/ \
    -size 200 \
    -mask \
    -p $THREADS \
    -preparsedDir homer_preparsed/

echo "De novo results: $OUTDIR/homerResults.html"
echo "Known motif results: $OUTDIR/knownResults.html"
```

### Complete MEME-ChIP Workflow

```bash
#!/bin/bash
# Full MEME-ChIP motif analysis for ENCODE TF ChIP-seq peaks

PEAKS="CTCF_idr_peaks.narrowPeak"
GENOME_FA="hg38.fa"
BLACKLIST="hg38-blacklist.v2.bed.gz"
JASPAR="JASPAR2024_CORE_vertebrates.meme"
OUTDIR="memechip_CTCF"

# Step 1: Extract summit +/- 100bp
awk 'BEGIN{OFS="\t"} {s=$2+$10; if(s-100>=0) print $1,s-100,s+100,$4,$7}' \
    $PEAKS > summits_200bp.bed

# Step 2: Remove blacklisted regions
bedtools intersect -a summits_200bp.bed -b $BLACKLIST -v > summits_clean.bed

# Step 3: Subsample top 5000 by signal
sort -k5,5nr summits_clean.bed | head -5000 > top5k_summits.bed

# Step 4: Extract FASTA
bedtools getfasta -fi $GENOME_FA -bed top5k_summits.bed -fo top5k_summits.fa

# Step 5: Run MEME-ChIP
meme-chip \
    -meme-maxw 30 \
    -meme-nmotifs 10 \
    -meme-minw 6 \
    -db $JASPAR \
    -o $OUTDIR/ \
    top5k_summits.fa

echo "Results: $OUTDIR/index.html"
```

## Common Pitfalls

1. **Peak summit vs full peak region**: For TF ChIP-seq, always use summit-centered windows (150-250bp). Using the full peak region (often 300-1000bp) dilutes the motif signal because TF binding sites occupy only 6-20bp at the summit. For histone ChIP-seq or ATAC-seq, use the full peak region with `-size given` because the relevant sequence features are distributed across the region, not concentrated at a single point.

2. **Background model**: Both HOMER and MEME use background sequence models to calculate enrichment. HOMER generates GC-matched background from the genome by default, which is usually appropriate. For MEME-ChIP, the default shuffle-based background works well. However, if your peaks are strongly biased toward specific genomic features (e.g., all in CpG islands), consider providing a custom background set matched for genomic context to avoid false enrichment from GC bias.

3. **Repeat masking**: Always use repeat masking (`-mask` in HOMER, which uses the soft-masked genome). Without masking, repetitive elements dominate the de novo motif results. Alu elements, LINE elements, and simple repeats contain internal sequence patterns that HOMER and MEME will report as significant "motifs" that have no biological relevance to TF binding.

4. **Too many peaks overwhelm the analysis**: HOMER and MEME become slow and less specific with more than 50,000 sequences. More importantly, including weak peaks adds noise. Subsample to the top 5,000-10,000 peaks ranked by signal value or enrichment score. The strongest peaks have the most consistent motif instances and produce the clearest results. Quality over quantity.

5. **Missing JASPAR or outdated motif database**: MEME-ChIP requires an external motif database file for known motif enrichment. Without it, only de novo discovery runs. Download the current JASPAR core vertebrate set in MEME format from jaspar.elixir.no. HOMER ships with its own motif database, but it should be updated periodically with `configureHomer.pl`. Outdated databases may miss recently characterized TF motifs.

## Presenting Results

When reporting motif enrichment analysis results:

- **Enrichment table**: Present a table with columns: motif_name, p-value, % of target sequences with motif, % of background sequences with motif, fold_enrichment, and best_known_match (for de novo motifs)
- **Always report**: Tool and version (HOMER v4.x or MEME Suite v5.x), motif database used (JASPAR 2024 / HOMER default), number of input peaks, peak size used, and whether repeat masking was applied
- **De novo motifs**: For each de novo motif, report the E-value, number of sites, information content (bits), and the top match from the known motif database with its match p-value
- **Background model**: Specify the background used (HOMER: GC-matched genomic, MEME: shuffled sequences, or custom), as this directly affects enrichment significance
- **Context to provide**: Note the peak subsetting strategy (e.g., top 5,000 by signal) and whether results were consistent between HOMER and MEME when both were run
- **Next steps**: Suggest `jaspar-motifs` for targeted scanning of specific TF motifs at base-pair resolution, or `peak-annotation` to annotate motif-containing peaks with genomic features

## Walkthrough: Discovering Co-Binding TFs at Liver CTCF Sites

**Goal**: Find enriched motifs in CTCF ChIP-seq peaks from liver to identify co-binding partners.
**Context**: CTCF organizes chromatin loops; co-bound TFs may regulate liver-specific gene expression.

### Step 1: Find CTCF ChIP-seq peaks in liver

```
encode_search_files(
  assay_title="TF ChIP-seq",
  organ="liver",
  target="CTCF",
  file_format="bed",
  output_type="IDR thresholded peaks",
  assembly="GRCh38"
)
```

Expected output:
```json
{
  "total": 3,
  "files": [{"accession": "ENCFF345CTF", "output_type": "IDR thresholded peaks", "file_size_mb": 2.1}]
}
```

### Step 2: Download peaks for motif analysis

```
encode_download_files(
  accessions=["ENCFF345CTF"],
  download_dir="/data/motifs/liver_ctcf"
)
```

### Step 3: Run HOMER findMotifsGenome.pl
`findMotifsGenome.pl ENCFF345CTF.bed hg38 output_dir/ -size 200 -mask`

**Interpretation**: Expect CTCF motif as top hit (validation). Liver-specific co-binders (HNF4A, FOXA2) appearing in the known motif results suggest regulatory cooperation.

## Code Examples

### 1. Find ChIP-seq peaks for motif discovery

```
encode_search_files(
  assay_title="TF ChIP-seq",
  organ="pancreas",
  target="NKX2-2",
  file_format="bed",
  output_type="IDR thresholded peaks",
  assembly="GRCh38"
)
```

Expected output:
```json
{
  "total": 1,
  "files": [{"accession": "ENCFF789NKX", "output_type": "IDR thresholded peaks", "assembly": "GRCh38"}]
}
```

## Integration

| This skill produces... | Feed into... | Using tool/skill |
|---|---|---|
| Enriched motif lists (HOMER/MEME output) | TF identification | cross-reference -> Open Targets |
| De novo motifs (position weight matrices) | JASPAR comparison | jaspar-motifs skill |
| Co-binding TF predictions | Regulatory network | integrative-analysis skill |
| Motif locations (BED format) | Variant overlap | variant-annotation skill |
| Background-corrected enrichment scores | Publication tables | scientific-writing skill |

## Related Skills

- **regulatory-elements** -- Identify cis-regulatory elements that can be further characterized by motif content
- **epigenome-profiling** -- Comprehensive epigenomic profiles provide context for interpreting which TFs are active
- **histone-aggregation** -- Union peak sets from multiple histone experiments provide genomic context for motif results
- **accessibility-aggregation** -- Union ATAC/DNase peak sets define the accessible genome where TF binding occurs
- **peak-annotation** -- Annotate motif-containing peaks with genomic features and gene associations
- **visualization-workflow** -- Visualize motif enrichment at peaks using deepTools heatmaps centered on motif instances
- **publication-trust** -- Verify literature claims backing analytical decisions

## For the request: "$ARGUMENTS"
