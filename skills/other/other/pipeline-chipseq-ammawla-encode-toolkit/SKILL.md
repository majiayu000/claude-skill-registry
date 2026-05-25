---
name: pipeline-chipseq
description: "Execute ENCODE ChIP-seq processing pipeline from FASTQ to peaks and signal tracks. Child of pipeline-guide. Provides stage-by-stage Nextflow execution with Docker containers and cloud deployment. Use when users need to process ChIP-seq data following ENCODE standards, run peak calling with MACS2, perform IDR analysis, or generate signal tracks. Trigger on: ChIP-seq pipeline, run ChIP-seq, process ChIP-seq, MACS2 peak calling, IDR analysis, ChIP-seq FASTQ processing."
---

# ENCODE ChIP-seq Pipeline

## When to Use

- User wants to run a ChIP-seq processing pipeline from FASTQ to peaks and signal tracks
- User asks about "ChIP-seq pipeline", "MACS2", "peak calling", "BWA alignment for ChIP", or "IDR"
- User needs to process histone or TF ChIP-seq data following ENCODE standards
- Example queries: "process my ChIP-seq FASTQs", "run the ENCODE ChIP-seq pipeline", "call peaks from ChIP-seq with MACS2 and IDR"

Execute the ENCODE ChIP-seq processing pipeline from raw FASTQ files through peak calling,
IDR analysis, and signal track generation. This skill provides a complete Nextflow DSL2
implementation following ENCODE uniform analysis standards.

## Overview

The ENCODE ChIP-seq pipeline processes chromatin immunoprecipitation sequencing data through
a series of well-defined stages: quality control, adapter trimming, alignment to a reference
genome, filtering and deduplication, peak calling with MACS2, replicate consistency analysis
via IDR, and signal track generation. Each stage is parameterized according to ENCODE
standards and produces QC metrics for comprehensive quality assessment.

This pipeline handles both transcription factor (TF) ChIP-seq and histone modification
ChIP-seq, automatically selecting narrow or broad peak calling modes as appropriate.

## Key Literature

| Reference | Journal | Year | DOI | Relevance |
|-----------|---------|------|-----|-----------|
| Landt et al. "ChIP-seq guidelines and practices" | Genome Research | 2012 | 10.1101/gr.136184.111 | ENCODE ChIP-seq standards (~4,000 citations) |
| ENCODE Project Consortium "Expanded encyclopaedias" | Nature | 2020 | 10.1038/s41586-020-2493-4 | ENCODE Phase 3 standards |
| Zhang et al. "Model-based Analysis of ChIP-Seq (MACS)" | Genome Biology | 2008 | 10.1186/gb-2008-9-9-r137 | Peak caller (~7,000 citations) |
| Li et al. "Measuring reproducibility (IDR)" | Annals of Applied Statistics | 2011 | 10.1214/11-AOAS466 | Replicate consistency (~1,500 citations) |
| Amemiya et al. "ENCODE Blacklist" | Scientific Reports | 2019 | 10.1038/s41598-019-45839-z | Artifact regions (~1,372 citations) |
| Ramachandran et al. "phantompeakqualtools" | — | 2013 | — | NSC/RSC strand correlation metrics |

## Pipeline Stages

```
FASTQ ──> FastQC / Trim Galore ──> BWA-MEM ──> Samtools Filter ──> Picard MarkDup
  │                                                                       │
  │           ┌───────────────────────────────────────────────────────────┘
  │           v
  │     Blacklist Filter ──> MACS2 Peak Calling ──> IDR Analysis
  │                                │                     │
  │                                v                     v
  │                         Signal Tracks          QC Report (MultiQC)
  │                          (bigWig)
  v
 Raw QC Report
```

### Stage Summary

| Stage | Tool | Input | Output | Reference |
|-------|------|-------|--------|-----------|
| 1. QC & Trimming | FastQC, Trim Galore | Raw FASTQ | Trimmed FASTQ | references/01-qc-trimming.md |
| 2. Alignment | BWA-MEM | Trimmed FASTQ | Sorted BAM | references/02-alignment.md |
| 3. Filtering | Picard, Samtools, bedtools | Sorted BAM | Filtered BAM | references/03-filtering.md |
| 4. Peak Calling & IDR | MACS2, IDR | Filtered BAM | Peaks (narrowPeak/broadPeak) | references/04-analysis.md |
| 5. QC & Signal | deeptools, phantompeakqualtools | Filtered BAM, Peaks | bigWig, QC report | references/05-qc-metrics.md |

## Input Requirements

### Required Files
- **Treatment FASTQ**: ChIP sample reads (single-end or paired-end, gzipped)
- **Control FASTQ**: Input/IgG control reads (matching single-end or paired-end)
- **Reference genome**: BWA-indexed genome (GRCh38 for human, mm10 for mouse)

### Sample Sheet Format
```csv
sample_id,treatment_r1,treatment_r2,control_r1,control_r2,target,peak_type
SAMPLE1,chip_R1.fq.gz,chip_R2.fq.gz,input_R1.fq.gz,input_R2.fq.gz,H3K27ac,narrow
SAMPLE2,chip_R1.fq.gz,chip_R2.fq.gz,input_R1.fq.gz,input_R2.fq.gz,H3K27me3,broad
```

### Narrow vs Broad Peak Mode Decision

| Peak Type | Targets | MACS2 Mode |
|-----------|---------|------------|
| Narrow | H3K4me3, H3K4me1, H3K27ac, H3K9ac, all TFs, CTCF | `--qvalue 0.05` (default) |
| Broad | H3K27me3, H3K36me3, H3K9me3, H3K79me2 | `--broad --broad-cutoff 0.1` |

## QC Thresholds

These thresholds follow ENCODE standards established by Landt et al. 2012 and the
ENCODE DCC quality metrics documentation.

| Metric | Threshold | Category | Source |
|--------|-----------|----------|--------|
| Total sequenced reads | ≥20M (TF), ≥45M (histone) | Read depth | Landt 2012 |
| Mapping rate | >80% | Alignment | ENCODE |
| NRF (non-redundant fraction) | ≥0.8 | Library complexity | ENCODE |
| PBC1 (PCR bottleneck coeff 1) | ≥0.8 | Library complexity | ENCODE |
| PBC2 (PCR bottleneck coeff 2) | ≥3 | Library complexity | ENCODE |
| NSC (normalized strand coeff) | >1.05 | Enrichment | phantompeakqualtools |
| RSC (relative strand corr) | >0.8 | Enrichment | phantompeakqualtools |
| FRiP (fraction reads in peaks) | ≥1% | Peak quality | Landt 2012 |
| IDR optimal peaks | >20,000 (TF) | Reproducibility | ENCODE |
| Duplication rate | <30% | Library complexity | ENCODE |
| Mitochondrial fraction | <5% | Sample quality | ENCODE |

### Interpreting QC: Traffic Light System

| Color | Meaning | Action |
|-------|---------|--------|
| Green | All metrics pass | Proceed to analysis |
| Yellow | 1-2 metrics marginal | Review library prep, may be usable |
| Red | Multiple failures | Do not use; re-do experiment |

**Important**: No single metric is sufficient. Interpret QC collectively. A sample with
borderline NRF but excellent FRiP may still be usable.

## Execution

### Quick Start (Local Docker)
```bash
nextflow run scripts/main.nf \
  -profile local \
  --reads 'fastq/*_R{1,2}.fq.gz' \
  --control 'fastq/input_R{1,2}.fq.gz' \
  --genome GRCh38 \
  --peak_type narrow \
  --outdir results/
```

### SLURM HPC
```bash
nextflow run scripts/main.nf \
  -profile slurm \
  --reads 'fastq/*_R{1,2}.fq.gz' \
  --control 'fastq/input_R{1,2}.fq.gz' \
  --genome GRCh38 \
  --peak_type narrow \
  --outdir results/
```

### Google Cloud
```bash
nextflow run scripts/main.nf \
  -profile gcp \
  --reads 'gs://bucket/fastq/*_R{1,2}.fq.gz' \
  --control 'gs://bucket/fastq/input_R{1,2}.fq.gz' \
  --genome GRCh38 \
  --outdir 'gs://bucket/results/'
```

### AWS Batch
```bash
nextflow run scripts/main.nf \
  -profile aws \
  --reads 's3://bucket/fastq/*_R{1,2}.fq.gz' \
  --control 's3://bucket/fastq/input_R{1,2}.fq.gz' \
  --genome GRCh38 \
  --outdir 's3://bucket/results/'
```

## Cloud Cost Estimates

| Platform | Instance | Cost/Sample | Time/Sample | Notes |
|----------|----------|-------------|-------------|-------|
| GCP | n1-standard-8 | ~$2-5 | 2-4 hours | Preemptible recommended |
| AWS | m5.2xlarge | ~$2-5 | 2-4 hours | Spot instances recommended |
| Local | 8 cores, 32GB | $0 | 3-6 hours | Docker required |
| SLURM | 8 cores, 32GB | Varies | 2-4 hours | Singularity recommended |

## Output Directory Structure

```
results/
  fastqc/                   # Raw and trimmed QC reports
  trimmed/                  # Trimmed FASTQ files
  aligned/                  # Sorted BAM files
  filtered/                 # Filtered, deduplicated BAM
  peaks/
    narrow/                 # narrowPeak files (TF, active histone marks)
    broad/                  # broadPeak files (repressive marks)
    idr/                    # IDR-filtered reproducible peaks
  signal/
    fold_change/            # Fold change over control (bigWig)
    pvalue/                 # Signal p-value tracks (bigWig)
  qc/
    phantompeakqualtools/   # NSC/RSC strand correlation
    multiqc/                # Aggregated QC report
  logs/                     # Nextflow execution logs
```

## Common Pitfalls

### 1. Missing Input Control
ChIP-seq requires a matched input (or IgG) control for accurate peak calling.
Without it, MACS2 will call peaks against a uniform background model, leading to
high false positive rates. Always include a control sample from the same cell type
and batch.

### 2. Narrow vs Broad Peak Mode Mismatch
Using narrow peak calling for broad marks (H3K27me3, H3K36me3) fragments the signal
into many small peaks instead of capturing the broad domains. Use `--broad` for these
marks. Conversely, broad mode on TF ChIP-seq over-merges distinct binding sites.

### 3. Adapter Contamination
Short insert libraries may have significant adapter read-through. Always run Trim Galore
before alignment. Check FastQC adapter content plots: >5% adapter suggests a problem.

### 4. PCR Bottleneck
Low-input ChIP-seq libraries may have high duplication rates (>30%). This reduces the
effective read depth and inflates apparent signal. Monitor NRF and PBC metrics. If NRF
<0.8, consider re-doing library preparation with more input material.

### 5. Blacklist Region Artifacts
Repetitive and high-signal artifact regions inflate peak counts and FRiP. Always filter
against the ENCODE blacklist (Amemiya et al. 2019). The hg38-blacklist.v2.bed contains
~900 regions covering ~40 Mb that should be excluded from all analyses.

## Pipeline Scripts

| File | Description | Lines |
|------|-------------|-------|
| `scripts/main.nf` | Nextflow DSL2 pipeline | ~120 |
| `scripts/nextflow.config` | Execution profiles (local/slurm/gcp/aws) | ~60 |
| `scripts/Dockerfile` | Multi-stage Docker build with all tools | ~30 |

## ENCODE Data Integration

After running this pipeline on your own data, compare results with ENCODE:

```python
# Find matching ENCODE experiments
encode_search_experiments(
    assay_title="Histone ChIP-seq",
    target="H3K27ac",
    organ="pancreas",
    biosample_type="tissue"
)

# Download ENCODE peaks for comparison
encode_batch_download(
    download_dir="/data/encode_reference/",
    output_type="IDR thresholded peaks",
    target="H3K27ac",
    organ="pancreas",
    assembly="GRCh38"
)
```

## Pitfalls & Edge Cases

- **Input control is mandatory**: ChIP-seq without an input/IgG control produces unreliable peaks. MACS2 `-c` flag requires a matched control BAM. Never skip this — enrichment without background correction is meaningless.
- **Broad vs narrow peak mode**: H3K27me3, H3K36me3, H3K9me3 require `--broad` flag in MACS2. Using narrow mode on broad marks fragments them into thousands of small, biologically meaningless peaks.
- **Duplicate marking ≠ duplicate removal**: Mark duplicates with Picard but do NOT remove them before IDR. IDR needs duplicates to estimate signal reproducibility. Remove only after IDR filtering.
- **Cross-correlation QC can mislead**: NSC/RSC values depend on fragment length distribution. Deeply sequenced libraries can have high NSC but poor enrichment. Always check FRiP alongside NSC/RSC.
- **IDR requires biological replicates**: IDR is designed for true biological replicates, not technical replicates or pseudoreplicates. Using pseudoreplicates gives artificially high concordance and inflated peak counts.
- **Blacklist filtering order matters**: Apply ENCODE Blacklist v2 AFTER peak calling, not before alignment. Removing blacklist reads before alignment can distort fragment size estimation and normalization.

## Walkthrough: Processing ENCODE H3K27ac ChIP-seq from FASTQ to Peaks

**Goal**: Process raw H3K27ac ChIP-seq FASTQ files through the ENCODE uniform processing pipeline to generate IDR-thresholded peak calls and signal tracks.
**Context**: The ENCODE ChIP-seq pipeline standardizes processing with BWA-MEM alignment, MACS2 peak calling, and IDR reproducibility analysis.

### Step 1: Find the experiment and download FASTQs

```
encode_get_experiment(accession="ENCSR000AKA")
```

Expected output:
```json
{
  "accession": "ENCSR000AKA",
  "assay_title": "Histone ChIP-seq",
  "target": "H3K27ac",
  "biosample_summary": "GM12878",
  "replicates": 2,
  "status": "released"
}
```

### Step 2: List FASTQ files

```
encode_list_files(accession="ENCSR000AKA", file_format="fastq")
```

Expected output:
```json
{
  "files": [
    {"accession": "ENCFF001FQ1", "output_type": "reads", "paired_end": "1", "biological_replicates": [1], "file_size_mb": 2400},
    {"accession": "ENCFF002FQ2", "output_type": "reads", "paired_end": "2", "biological_replicates": [1], "file_size_mb": 2500},
    {"accession": "ENCFF003FQ3", "output_type": "reads", "paired_end": "1", "biological_replicates": [2], "file_size_mb": 2200},
    {"accession": "ENCFF004FQ4", "output_type": "reads", "paired_end": "2", "biological_replicates": [2], "file_size_mb": 2300}
  ]
}
```

**Interpretation**: 2 biological replicates, each paired-end. Both replicates are needed for IDR analysis.

### Step 3: Download FASTQs

```
encode_download_files(accessions=["ENCFF001FQ1", "ENCFF002FQ2", "ENCFF003FQ3", "ENCFF004FQ4"], download_dir="/data/chipseq/fastq")
```

### Step 4: Run the ChIP-seq pipeline

```bash
nextflow run pipeline-chipseq/main.nf \
  --fastq_r1 ENCFF001FQ1.fastq.gz,ENCFF003FQ3.fastq.gz \
  --fastq_r2 ENCFF002FQ2.fastq.gz,ENCFF004FQ4.fastq.gz \
  --genome GRCh38 \
  --target H3K27ac \
  --broad_peak false \
  --blacklist encode_blacklist_v2.bed \
  -profile docker
```

### Step 5: Validate output quality

Key QC metrics to check:
| Metric | Threshold | Purpose |
|---|---|---|
| FRiP | >= 1% | Fraction of reads in peaks |
| NSC | > 1.05 | Normalized strand coefficient |
| RSC | > 0.8 | Relative strand coefficient |
| NRF | >= 0.8 | Non-redundant fraction |

### Step 6: Log provenance

```
encode_log_derived_file(
  source_accessions=["ENCFF001FQ1", "ENCFF002FQ2", "ENCFF003FQ3", "ENCFF004FQ4"],
  derived_file="/data/chipseq/peaks/idr_peaks.narrowPeak",
  description="IDR-thresholded H3K27ac peaks from ENCODE pipeline",
  tool="ENCODE ChIP-seq pipeline v2.0 (BWA 0.7.17, MACS2 2.2.9.1, IDR 2.0.3)"
)
```

### Integration with downstream skills
- IDR peaks feed into -> **peak-annotation** for gene assignment
- Signal tracks (bigWig) feed into -> **visualization-workflow** for genome browser display
- Peak coordinates feed into -> **histone-aggregation** for cross-experiment union merge
- QC metrics evaluated by -> **quality-assessment** against ENCODE standards
- Pipeline provenance logged by -> **data-provenance**

## Code Examples

### 1. Find ChIP-seq data to process

```
encode_search_experiments(
  assay_title="Histone ChIP-seq",
  organ="liver",
  target="H3K4me3"
)
```

Expected output:
```json
{
  "total": 15,
  "experiments": [
    {
      "accession": "ENCSR456LIV",
      "target": "H3K4me3-human",
      "biosample_summary": "liver tissue male adult (54 years)",
      "status": "released"
    }
  ]
}
```

### 2. Download FASTQ files for pipeline input

```
encode_download_files(
  accessions=["ENCSR456LIV"],
  file_format="fastq",
  download_dir="/data/chipseq/liver_h3k4me3"
)
```

Expected output:
```json
{
  "downloaded": 4,
  "total_size_mb": 12450.5,
  "files": [
    {"accession": "ENCFF001REP1", "md5_verified": true, "paired_end": "1"},
    {"accession": "ENCFF002REP1", "md5_verified": true, "paired_end": "2"}
  ]
}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| IDR-thresholded peaks (narrowPeak) | **peak-annotation** | Assign peaks to nearest genes |
| IDR-thresholded peaks | **histone-aggregation** | Cross-experiment union merge for histone marks |
| Signal tracks (bigWig) | **visualization-workflow** | Genome browser visualization |
| Peak coordinates (BED) | **motif-analysis** | De novo motif discovery in peak regions |
| Filtered peaks | **regulatory-elements** | Classify as enhancers, promoters, insulators |
| QC metrics | **quality-assessment** | Validate against ENCODE ChIP-seq standards |
| Pipeline run logs | **data-provenance** | Record tool versions and parameters |
| Peak files | **variant-annotation** | Identify variants in ChIP-seq peaks |

## Related Skills

- **pipeline-guide** (parent): General pipeline selection and resource assessment
- **histone-aggregation**: Merge peaks across samples/replicates after peak calling
- **quality-assessment**: Deep-dive QC analysis beyond basic metrics
- **regulatory-elements**: Annotate peaks with regulatory element classifications
- **peak-annotation**: Annotate peaks with gene associations
- **compare-biosamples**: Compare ChIP-seq profiles across cell types
- **publication-trust**: Verify literature claims backing analytical decisions

## Presenting Results

When reporting ChIP-seq pipeline results:

- **Pipeline status**: Report completion status for each stage (QC, alignment, filtering, peak calling, IDR, signal generation) with pass/fail indicators
- **Key QC metrics**: Present FRiP (>=1%), NSC (>1.05), RSC (>0.8), NRF (>=0.8), duplication rate, and mapping rate in a summary table with ENCODE thresholds for comparison
- **Peak counts**: Report IDR optimal peak count, conservative peak count, and pseudoreplicated peak count. Note narrow vs broad mode used
- **Signal tracks**: Provide paths to fold-change-over-control bigWig and p-value bigWig files for genome browser visualization
- **Traffic light summary**: Use green/yellow/red to indicate overall sample quality based on collective QC assessment
- **Output paths**: List the key output directories (peaks/idr/, signal/fold_change/, qc/multiqc/)
- **Next steps**: Suggest `quality-assessment` for deeper QC evaluation, or `visualization-workflow` for genome browser session generation

## For the request: "$ARGUMENTS"
