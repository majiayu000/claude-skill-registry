---
name: pipeline-atacseq
description: "Execute ENCODE ATAC-seq processing pipeline from FASTQ to peaks and signal tracks. Child of pipeline-guide. Provides stage-by-stage Nextflow execution with Docker containers and cloud deployment. Handles Tn5 transposase offset correction, mitochondrial read removal, nucleosome-free fragment selection, and TSS enrichment scoring. Use when users need to process ATAC-seq data following ENCODE standards. Trigger on: ATAC-seq pipeline, run ATAC-seq, process ATAC-seq, chromatin accessibility, open chromatin, Tn5 shift, TSS enrichment."
---

# ENCODE ATAC-seq Pipeline

## When to Use

- User wants to run an ATAC-seq processing pipeline from FASTQ to peaks and signal tracks
- User asks about "ATAC-seq pipeline", "Tn5 shift", "chromatin accessibility pipeline", or "Bowtie2 for ATAC"
- User needs to process ATAC-seq data with proper Tn5 insertion site correction
- Example queries: "process my ATAC-seq FASTQs", "run ENCODE ATAC-seq pipeline", "call accessibility peaks from ATAC-seq"

Execute the ENCODE ATAC-seq processing pipeline from raw FASTQ files through Tn5 offset
correction, peak calling, IDR analysis, and signal track generation. This skill provides
a complete Nextflow DSL2 implementation following ENCODE uniform analysis standards.

## Overview

ATAC-seq (Assay for Transposase-Accessible Chromatin using sequencing) uses the Tn5
transposase to probe open chromatin regions. The ENCODE pipeline processes ATAC-seq data
through quality control, alignment with Bowtie2, Tn5 insertion site correction (+4/-5 bp
offset), mitochondrial read removal, nucleosome-free fragment selection, peak calling
with MACS2, and IDR-based replicate consistency analysis.

Key differences from ChIP-seq: Bowtie2 aligner (optimized for short fragments), Tn5
transposase shift correction, aggressive mitochondrial read filtering (can be 30-80%
of reads), nucleosomal fragment size distribution as a QC metric, and TSS enrichment
score as the primary quality indicator.

## Key Literature

| Reference | Journal | Year | DOI | Relevance |
|-----------|---------|------|-----|-----------|
| Buenrostro et al. "Transposition of native chromatin (ATAC-seq)" | Nature Methods | 2013 | 10.1038/nmeth.2688 | Original ATAC-seq method (~5,000 citations) |
| Corces et al. "An improved ATAC-seq protocol" | Nature Methods | 2017 | 10.1038/nmeth.4396 | Omni-ATAC improvements (~2,500 citations) |
| ENCODE Project Consortium "Expanded encyclopaedias" | Nature | 2020 | 10.1038/s41586-020-2493-4 | ENCODE Phase 3 standards |
| Amemiya et al. "ENCODE Blacklist" | Scientific Reports | 2019 | 10.1038/s41598-019-45839-z | Artifact regions (~1,372 citations) |
| Langmead & Salzberg "Fast gapped-read alignment with Bowtie 2" | Nature Methods | 2012 | 10.1038/nmeth.1923 | Aligner (~30,000 citations) |
| Yan et al. "From reads to insight: ATAC-seq analysis" | Genome Biology | 2020 | 10.1186/s13059-020-1929-3 | Analysis best practices |

## Pipeline Stages

```
FASTQ ──> FastQC / Trim Galore ──> Bowtie2 ──> Mito Removal + Tn5 Shift
  │                                                       │
  │           ┌──────────────────────────────────────────┘
  │           v
  │     Picard MarkDup ──> Blacklist Filter ──> Size Selection
  │                                                   │
  │                    ┌─────────────────┬────────────┘
  │                    v                 v
  │             NFR Fragments     Mono-Nucleosome
  │                    │
  │                    v
  │           MACS2 Peak Calling ──> IDR Analysis
  │                    │                    │
  │                    v                    v
  │             Signal Tracks         QC Report (MultiQC + ataqv)
  v
 Raw QC Report
```

### Stage Summary

| Stage | Tool | Input | Output | Reference |
|-------|------|-------|--------|-----------|
| 1. QC & Trimming | FastQC, Trim Galore | Raw FASTQ | Trimmed FASTQ | references/01-qc-trimming.md |
| 2. Alignment | Bowtie2 | Trimmed FASTQ | Sorted BAM | references/02-alignment.md |
| 3. Tn5 Shift & Filtering | Samtools, bedtools, Picard | Sorted BAM | Shifted, filtered BAM | references/03-tn5-filtering.md |
| 4. Peak Calling & IDR | MACS2, IDR | Filtered BAM | Peaks (narrowPeak) | references/04-peak-calling.md |
| 5. QC & Signal | deeptools, ataqv, MultiQC | Filtered BAM, Peaks | bigWig, QC report | references/05-qc-metrics.md |

## Input Requirements

### Required Files
- **ATAC-seq FASTQ**: Paired-end reads (strongly recommended; single-end supported)
- **Reference genome**: Bowtie2-indexed genome (GRCh38 for human, mm10 for mouse)

### Sample Sheet Format
```csv
sample_id,read1,read2,replicate
SAMPLE1_rep1,atac_R1.fq.gz,atac_R2.fq.gz,1
SAMPLE1_rep2,atac_R1.fq.gz,atac_R2.fq.gz,2
```

**No input control needed**: Unlike ChIP-seq, ATAC-seq does not require a separate
input or IgG control. MACS2 calls peaks against a local background model.

## Tn5 Transposase Offset Correction

The Tn5 transposase inserts sequencing adapters with a 9-bp duplication. To center
reads on the actual cut site:
- **Forward strand (+)**: shift +4 bp
- **Reverse strand (-)**: shift -5 bp

This correction is essential for accurate footprinting and motif analysis.

## Fragment Size Distribution

ATAC-seq produces a characteristic nucleosomal ladder pattern:

| Fragment Class | Size Range | Biological Meaning |
|---------------|------------|-------------------|
| Nucleosome-free (NFR) | <150 bp | Open chromatin / TF binding |
| Mono-nucleosome | 150-300 bp | Single nucleosome wrapping |
| Di-nucleosome | 300-500 bp | Two nucleosomes |
| Tri-nucleosome | 500-700 bp | Three nucleosomes |

For peak calling, use **nucleosome-free reads (<150 bp)** only.

## QC Thresholds

| Metric | Threshold | Category | Source |
|--------|-----------|----------|--------|
| Total sequenced reads | >=50M (recommended) | Read depth | ENCODE |
| Mapping rate | >80% | Alignment | ENCODE |
| Mitochondrial fraction | <20% (ideal <5%) | Sample quality | ENCODE |
| NRF (non-redundant fraction) | >=0.8 | Library complexity | ENCODE |
| PBC1 | >=0.8 | Library complexity | ENCODE |
| TSS enrichment score | >=5 | Signal quality | ENCODE standard |
| FRiP | >=0.3 | Peak quality | ENCODE |
| NFR fraction | >0.4 of fragments <150bp | Fragment distribution | Buenrostro 2013 |
| IDR optimal peaks | >50,000 | Reproducibility | ENCODE |

### TSS Enrichment Score

The TSS enrichment score measures the fold enrichment of ATAC-seq signal at
transcription start sites compared to flanking regions. It is the single most
informative QC metric for ATAC-seq:

| Score | Quality | Interpretation |
|-------|---------|---------------|
| >=7 | Excellent | High signal-to-noise |
| 5-7 | Good | Acceptable for most analyses |
| 3-5 | Marginal | Review other metrics carefully |
| <3 | Poor | Likely failed; consider re-doing |

## Execution

### Quick Start (Local Docker)
```bash
nextflow run scripts/main.nf \
  -profile local \
  --reads 'fastq/*_R{1,2}.fq.gz' \
  --genome GRCh38 \
  --outdir results/
```

### SLURM HPC
```bash
nextflow run scripts/main.nf \
  -profile slurm \
  --reads 'fastq/*_R{1,2}.fq.gz' \
  --genome GRCh38 \
  --outdir results/
```

### Google Cloud
```bash
nextflow run scripts/main.nf \
  -profile gcp \
  --reads 'gs://bucket/fastq/*_R{1,2}.fq.gz' \
  --genome GRCh38 \
  --outdir 'gs://bucket/results/'
```

### AWS Batch
```bash
nextflow run scripts/main.nf \
  -profile aws \
  --reads 's3://bucket/fastq/*_R{1,2}.fq.gz' \
  --genome GRCh38 \
  --outdir 's3://bucket/results/'
```

## Cloud Cost Estimates

| Platform | Instance | Cost/Sample | Time/Sample | Notes |
|----------|----------|-------------|-------------|-------|
| GCP | n1-standard-8 | ~$2-4 | 2-3 hours | Preemptible recommended |
| AWS | m5.2xlarge | ~$2-4 | 2-3 hours | Spot instances recommended |
| Local | 8 cores, 32GB | $0 | 3-5 hours | Docker required |
| SLURM | 8 cores, 32GB | Varies | 2-3 hours | Singularity recommended |

## Output Directory Structure

```
results/
  fastqc/                   # Raw and trimmed QC reports
  trimmed/                  # Trimmed FASTQ files
  aligned/                  # Sorted BAM files (pre-filtering)
  filtered/
    shifted/                # Tn5-corrected BAM files
    nfr/                    # Nucleosome-free fragments (<150 bp)
    mononuc/                # Mono-nucleosome fragments (150-300 bp)
  peaks/
    narrow/                 # MACS2 narrowPeak files
    idr/                    # IDR-filtered reproducible peaks
  signal/                   # bigWig signal tracks
  qc/
    tss_enrichment/         # TSS enrichment scores and plots
    fragment_size/          # Fragment size distribution plots
    ataqv/                  # Comprehensive ATAC-seq QC (ataqv)
    multiqc/                # Aggregated QC report
  logs/                     # Nextflow execution logs
```

## Common Pitfalls

### 1. High Mitochondrial Read Fraction
Mitochondrial DNA lacks chromatin and is highly accessible, often capturing 30-80%
of reads. This is the most common ATAC-seq quality issue. Filter chrM reads before
analysis. If >50% mito, consider optimizing the cell lysis step.

### 2. Missing Tn5 Shift Correction
Without the +4/-5 bp offset correction, cut-site positions are shifted by ~4.5 bp.
This matters for footprinting and motif analysis but has minimal effect on peak calling.
Always apply the shift for publication-quality results.

### 3. Using BWA Instead of Bowtie2
Bowtie2 handles the short fragments from ATAC-seq (especially NFR <150bp) better
than BWA-MEM. Use Bowtie2 with `--very-sensitive` for optimal ATAC-seq alignment.

### 4. Not Separating Nucleosomal Fractions
Peak calling on all fragments mixes nucleosome-free signal (TF binding) with
nucleosomal signal. Always size-select NFR (<150 bp) for peak calling.

### 5. Ignoring TSS Enrichment
TSS enrichment is the most informative single metric for ATAC-seq quality.
A score <5 indicates a failed experiment regardless of other metrics.

## Pipeline Scripts

| File | Description | Lines |
|------|-------------|-------|
| `scripts/main.nf` | Nextflow DSL2 pipeline | ~120 |
| `scripts/nextflow.config` | Execution profiles (local/slurm/gcp/aws) | ~60 |
| `scripts/Dockerfile` | Multi-stage Docker build with all tools | ~30 |

## ENCODE Data Integration

After running on your own data, compare with ENCODE reference:

```python
# Find matching ENCODE ATAC-seq experiments
encode_search_experiments(
    assay_title="ATAC-seq",
    organ="pancreas",
    biosample_type="tissue"
)

# Download ENCODE peaks for comparison
encode_batch_download(
    download_dir="/data/encode_reference/",
    output_type="IDR thresholded peaks",
    assay_title="ATAC-seq",
    organ="pancreas",
    assembly="GRCh38"
)
```

## Pitfalls & Edge Cases

- **Tn5 shift is critical**: ATAC-seq reads must be shifted +4/-5 bp to center on the Tn5 insertion site. Without this correction, footprinting analysis will be offset by ~5 bp and motif enrichment will be degraded.
- **Mitochondrial reads dominate**: Expect 30-80% mitochondrial reads in ATAC-seq. Filter chrM reads AFTER alignment, BEFORE peak calling. High mitoChRM (>80%) indicates dead/dying cells or poor nuclei isolation.
- **Fragment size distribution is diagnostic**: A nucleosomal ladder (sub-nucleosomal <150bp, mono-nucleosomal ~200bp, di-nucleosomal ~400bp) confirms successful transposition. Absence of the ladder suggests incomplete or failed transposition.
- **TSS enrichment threshold**: ENCODE requires TSS enrichment ≥5 (GRCh38), ≥6 (hg19), or ≥10 (mm10) for ATAC-seq (ENCODE data standards). Values below 4 indicate poor signal-to-noise. This is the single most informative QC metric for ATAC-seq.
- **Peak caller choice matters**: MACS2 with `--nomodel --shift -100 --extsize 200` is standard for ATAC-seq. Do NOT use the ChIP-seq default MACS2 settings — they assume sonicated fragment distributions.
- **Paired-end vs single-end**: ATAC-seq should always be paired-end to capture fragment sizes. Single-end ATAC-seq cannot distinguish nucleosome-free from nucleosomal fragments.

## Walkthrough: Processing ENCODE ATAC-seq from FASTQ to Accessible Chromatin Peaks

**Goal**: Process raw ATAC-seq FASTQ files through the ENCODE pipeline to generate nucleosome-free region peaks and signal tracks for chromatin accessibility analysis.
**Context**: ATAC-seq requires Tn5 transposase insertion site correction (+4/-5 bp shift) and nucleosomal fragment size filtering, handled by the ENCODE ATAC-seq pipeline.

### Step 1: Find ATAC-seq experiment

```
encode_get_experiment(accession="ENCSR637ENO")
```

Expected output:
```json
{
  "accession": "ENCSR637ENO",
  "assay_title": "ATAC-seq",
  "biosample_summary": "GM12878",
  "replicates": 2,
  "status": "released"
}
```

### Step 2: List FASTQ files

```
encode_list_files(accession="ENCSR637ENO", file_format="fastq")
```

Expected output:
```json
{
  "files": [
    {"accession": "ENCFF100ATQ", "output_type": "reads", "paired_end": "1", "biological_replicates": [1], "file_size_mb": 1800},
    {"accession": "ENCFF101ATQ", "output_type": "reads", "paired_end": "2", "biological_replicates": [1], "file_size_mb": 1900}
  ]
}
```

### Step 3: Run the ATAC-seq pipeline

```bash
nextflow run pipeline-atacseq/main.nf \
  --fastq_r1 ENCFF100ATQ.fastq.gz \
  --fastq_r2 ENCFF101ATQ.fastq.gz \
  --genome GRCh38 \
  --blacklist encode_blacklist_v2.bed \
  --mitochondrial_chr chrM \
  -profile docker
```

Key pipeline steps:
1. Adapter trimming (Trimmomatic/cutadapt)
2. Alignment (Bowtie2, very-sensitive mode)
3. Tn5 shift correction (+4/-5 bp)
4. Mitochondrial read removal
5. Nucleosome-free fragment selection (<150 bp)
6. Peak calling (MACS2, --nomodel --shift -75 --extsize 150)

### Step 4: Validate output quality

| Metric | Threshold | Purpose |
|---|---|---|
| TSS enrichment | >= 5 (GRCh38), >= 6 (hg19), >= 10 (mm10) | Signal enrichment at transcription start sites |
| Fragment size distribution | Nucleosomal ladder | ~200bp, ~400bp, ~600bp periodicity |
| Mitochondrial reads | < 20% | Excessive = failed library |
| FRiP | >= 0.2 | Fraction of reads in peaks |

### Step 5: Track and log provenance

```
encode_track_experiment(accession="ENCSR637ENO", notes="GM12878 ATAC-seq processed through ENCODE pipeline")
```

### Integration with downstream skills
- Accessible chromatin peaks feed into -> **accessibility-aggregation** for cross-experiment union merge
- Peak regions feed into -> **motif-analysis** for TF motif enrichment
- Signal tracks feed into -> **visualization-workflow** for browser display
- Peaks feed into -> **regulatory-elements** for cCRE classification
- QC metrics validated by -> **quality-assessment**

## Code Examples

### 1. Find ATAC-seq data for processing

```
encode_search_experiments(
  assay_title="ATAC-seq",
  organ="pancreas"
)
```

Expected output:
```json
{
  "total": 8,
  "experiments": [
    {
      "accession": "ENCSR789PAN",
      "assay_title": "ATAC-seq",
      "biosample_summary": "pancreas tissue male adult (44 years)",
      "status": "released"
    }
  ]
}
```

### 2. Check file details before download

```
encode_list_files(
  accession="ENCSR789PAN",
  file_format="fastq"
)
```

Expected output:
```json
{
  "total": 4,
  "files": [
    {
      "accession": "ENCFF100ATQ",
      "file_format": "fastq",
      "read_length": 50,
      "paired_end": "1",
      "file_size_mb": 3200.1
    }
  ]
}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Accessible chromatin peaks | **accessibility-aggregation** | Cross-experiment union merge |
| Peak regions (BED) | **motif-analysis** | TF motif enrichment in open chromatin |
| Signal tracks (bigWig) | **visualization-workflow** | Genome browser accessibility display |
| Nucleosome-free peaks | **regulatory-elements** | Classify accessible regions as enhancers/promoters |
| Peak coordinates | **variant-annotation** | Identify variants in accessible chromatin |
| TSS enrichment scores | **quality-assessment** | Validate against ENCODE ATAC-seq standards |
| Pipeline parameters | **data-provenance** | Record Tn5 shift, fragment filters, tool versions |
| Peak files | **jaspar-motifs** | Scan accessible regions for known TF motifs |

## Related Skills

- **pipeline-guide** (parent): General pipeline selection and resource assessment
- **accessibility-aggregation**: Merge ATAC-seq peaks across samples
- **quality-assessment**: Deep-dive QC analysis beyond basic metrics
- **regulatory-elements**: Annotate peaks with regulatory element classifications
- **compare-biosamples**: Compare accessibility profiles across cell types
- **pipeline-chipseq**: Sibling pipeline for ChIP-seq data
- **publication-trust**: Verify literature claims backing analytical decisions

## Presenting Results

When reporting ATAC-seq pipeline results:

- **TSS enrichment score**: Report the TSS enrichment score prominently -- this is the single most informative ATAC-seq QC metric. Include the quality tier (Excellent >=7, Good 5-7, Marginal 3-5, Poor <3)
- **Fragment size distribution**: Report NFR fraction (% fragments <150 bp) and confirm the characteristic nucleosomal ladder pattern (NFR, mono-, di-, tri-nucleosome peaks)
- **Peak counts**: Report IDR optimal peak count and total MACS2 peaks before IDR filtering
- **NFR/mono-nucleosome ratio**: Present the ratio of nucleosome-free to mono-nucleosomal fragments as a library quality indicator
- **Mitochondrial fraction**: Report % mitochondrial reads removed (ideal <5%, acceptable <20%)
- **Key QC metrics**: Present mapping rate, FRiP (>=0.3 for ATAC-seq), NRF, and duplication rate in a summary table
- **Output paths**: List key outputs (peaks/idr/, signal/, qc/tss_enrichment/, qc/fragment_size/)
- **Next steps**: Suggest `motif-analysis` for TF footprinting and de novo motif discovery, or `visualization-workflow` for genome browser session generation

## For the request: "$ARGUMENTS"
