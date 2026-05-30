---
name: pipeline-rnaseq
description: "Execute ENCODE RNA-seq pipeline from FASTQ to gene quantification and signal tracks. Child of pipeline-guide. Provides Nextflow execution with Docker and cloud deployment. Use when processing RNA-seq data with STAR alignment, RSEM/Kallisto quantification, or generating expression matrices. Trigger on: RNA-seq pipeline, gene expression, STAR alignment, RSEM quantification, transcript quantification, TPM, FPKM, RNA processing, run RNA-seq."
---

# ENCODE RNA-seq Pipeline

## When to Use

- User wants to run an RNA-seq processing pipeline from FASTQ to gene quantification
- User asks about "RNA-seq pipeline", "STAR alignment", "RSEM", "gene expression quantification", or "Kallisto"
- User needs to process bulk RNA-seq data with ENCODE-standard 2-pass STAR alignment
- Example queries: "process my RNA-seq FASTQs", "quantify gene expression from RNA-seq", "run STAR and RSEM on my data"

Execute the ENCODE RNA-seq processing pipeline from raw FASTQ files through splice-aware
alignment, gene/transcript quantification, and strand-specific signal track generation.
This skill provides a complete Nextflow DSL2 implementation following ENCODE uniform
analysis standards.

## Overview

RNA-seq measures transcriptome-wide gene expression by sequencing cDNA derived from
cellular RNA. The ENCODE pipeline processes RNA-seq data through quality control,
splice-aware alignment with STAR (2-pass mode), gene and transcript quantification
with RSEM, optional fast pseudoalignment with Kallisto, and generation of strand-specific
signal tracks as bigWig files.

Key design decisions: STAR 2-pass mode for maximum splice junction sensitivity, RSEM
for accurate gene/transcript/isoform quantification including multi-mapped reads,
stranded library protocol (dUTP/rf-stranded) as the ENCODE standard, and paired-end
sequencing with a minimum of 30 million uniquely mapped reads per replicate.

## Key Literature

| Reference | Journal | Year | DOI | Relevance |
|-----------|---------|------|-----|-----------|
| Dobin et al. "STAR: ultrafast universal RNA-seq aligner" | Bioinformatics | 2013 | 10.1093/bioinformatics/bts635 | Splice-aware aligner (~12,000 citations) |
| Li & Dewey "RSEM: accurate transcript quantification from RNA-Seq data" | BMC Bioinformatics | 2011 | 10.1186/1471-2105-12-323 | Gene/transcript quantification (~6,000 citations) |
| Bray et al. "Near-optimal probabilistic RNA-seq quantification" | Nature Biotechnology | 2016 | 10.1038/nbt.3519 | Fast pseudoalignment (~4,000 citations) |
| Wang et al. "RSeQC: quality control of RNA-seq experiments" | Bioinformatics | 2012 | 10.1093/bioinformatics/bts356 | RNA-seq QC suite (~3,500 citations) |
| ENCODE Project Consortium "Expanded encyclopaedias" | Nature | 2020 | 10.1038/s41586-020-2493-4 | ENCODE Phase 3 standards |
| Frankish et al. "GENCODE 2021" | Nucleic Acids Research | 2021 | 10.1093/nar/gkaa1087 | Gene annotation reference |

## Pipeline Stages

```
FASTQ ──> FastQC / Trim Galore ──> STAR (2-pass) ──> Genome BAM + Transcriptome BAM
  |                                                        |              |
  |                  ┌─────────────────────────────────────┘              |
  |                  v                                                    v
  |         Signal Track Generation                              RSEM Quantification
  |          (strand-specific bigWig)                        (gene + transcript + isoform)
  |                  |                                                    |
  |                  v                                                    v
  |          Plus strand bigWig                                genes.results (TPM/FPKM)
  |          Minus strand bigWig                               isoforms.results
  |                                                                       |
  |         ┌───────────────────────────────────────────────────────────┘
  |         v
  |   Kallisto (optional fast pseudoalignment)
  |         |
  |         v
  └──> RSeQC + MultiQC ──> Aggregated QC Report
```

### Stage Summary

| Stage | Tool | Input | Output | Reference |
|-------|------|-------|--------|-----------|
| 1. QC & Trimming | FastQC, Trim Galore | Raw FASTQ | Trimmed FASTQ | references/01-qc-trimming.md |
| 2. Alignment | STAR (2-pass) | Trimmed FASTQ | Genome BAM + Transcriptome BAM | references/02-star-alignment.md |
| 3. Quantification | RSEM, Kallisto | Transcriptome BAM / FASTQ | Gene/transcript counts, TPM, FPKM | references/03-quantification.md |
| 4. Signal Tracks | bedGraphToBigWig | STAR bedGraph | Strand-specific bigWig | references/04-signal-tracks.md |
| 5. QC Metrics | RSeQC, MultiQC | BAM, counts | Strandedness, coverage, saturation | references/05-qc-metrics.md |

## Input Requirements

### Required Files
- **RNA-seq FASTQ**: Paired-end reads (ENCODE standard; single-end supported)
- **Reference genome**: STAR-indexed genome with gene annotation (GRCh38 + GENCODE for human)
- **Gene annotation**: GENCODE GTF (v38+ for human, vM27+ for mouse)

### Sample Sheet Format
```csv
sample_id,read1,read2,replicate,strandedness
SAMPLE1_rep1,rna_R1.fq.gz,rna_R2.fq.gz,1,reverse
SAMPLE1_rep2,rna_R1.fq.gz,rna_R2.fq.gz,2,reverse
```

**Strandedness**: ENCODE uses dUTP-based stranded libraries. The resulting reads are
`reverse` stranded (read 2 matches the sense strand). If unknown, the pipeline will
auto-detect strandedness using RSeQC `infer_experiment.py`.

## Library Strandedness

| Protocol | Strandedness | RSEM flag | Kallisto flag | Common Usage |
|----------|-------------|-----------|---------------|-------------|
| dUTP (ENCODE standard) | Reverse | `--strandedness reverse` | `--rf-stranded` | Most ENCODE RNA-seq |
| SMARTer / SMART-Seq2 | Unstranded | `--strandedness none` | (default) | Single-cell, low-input |
| Illumina TruSeq Stranded | Reverse | `--strandedness reverse` | `--rf-stranded` | Standard bulk RNA-seq |
| Directional ligation | Forward | `--strandedness forward` | `--fr-stranded` | Some legacy protocols |

## QC Thresholds

| Metric | Threshold | Category | Source |
|--------|-----------|----------|--------|
| Total sequenced reads | >=30M PE reads | Read depth | ENCODE |
| Uniquely mapped reads | >=70% of total | Alignment | ENCODE |
| Multi-mapped reads | <10% | Alignment | ENCODE |
| rRNA rate | <10% | Sample quality | ENCODE |
| Strandedness agreement | >90% | Library prep | RSeQC |
| Exonic rate | >60% | Mapping quality | RSeQC |
| Gene body coverage | Relatively uniform (5'/3' bias <1.5) | RNA integrity | RSeQC |
| Duplication rate | <60% | Library complexity | Picard |
| Detected genes (TPM>1) | >12,000 (human) | Sensitivity | ENCODE |
| Saturation | Approaching plateau at sequencing depth | Depth sufficiency | RSeQC |

### Read Depth Guidelines

| Application | Minimum Reads (PE) | Recommended | Notes |
|-------------|-------------------|-------------|-------|
| Gene-level expression | 20M | 30M | ENCODE minimum |
| Transcript-level expression | 40M | 60M | Isoform resolution requires more depth |
| Differential expression | 20M per sample | 30M per sample | 3+ biological replicates per condition |
| Novel junction discovery | 60M | 100M+ | STAR 2-pass mode benefits from depth |
| Fusion detection | 50M | 80M+ | Chimeric reads are rare |

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
| GCP | n1-highmem-8 | ~$3-6 | 2-4 hours | STAR index loading dominates; preemptible recommended |
| AWS | r5.2xlarge | ~$3-6 | 2-4 hours | r-series for STAR memory; spot recommended |
| Local | 8 cores, 32GB | $0 | 3-6 hours | Docker required; STAR needs 32GB+ RAM |
| SLURM | 8 cores, 32GB | Varies | 2-4 hours | Singularity recommended |

**Memory note**: STAR genome index loading requires ~32GB RAM for human. Machines with
<32GB will fail at the alignment step. Use `--limitGenomeGenerateRAM` to cap index size
for constrained environments, but this reduces mapping sensitivity.

## Output Directory Structure

```
results/
  fastqc/                   # Raw and trimmed QC reports
  trimmed/                  # Trimmed FASTQ files
  star/
    genome_bam/             # Genome-aligned BAM files
    transcriptome_bam/      # Transcriptome BAM files (for RSEM)
    logs/                   # STAR alignment logs (Log.final.out)
    junctions/              # Splice junction files (SJ.out.tab)
  rsem/
    genes/                  # genes.results (gene_id, TPM, FPKM, expected_count)
    isoforms/               # isoforms.results (transcript_id, TPM, FPKM)
  kallisto/                 # Kallisto quantification output (optional)
    abundance.tsv           # transcript TPMs and counts
  signal/
    plus/                   # Plus-strand bigWig signal tracks
    minus/                  # Minus-strand bigWig signal tracks
  qc/
    rseqc/                  # RSeQC output (strandedness, coverage, distribution)
    multiqc/                # Aggregated QC report
  logs/                     # Nextflow execution logs
```

## Common Pitfalls

### 1. Insufficient Memory for STAR
STAR loads the entire genome index into shared memory (~32GB for human). This is the most
common failure mode. Always allocate at least 32GB RAM for the alignment step. On shared
HPC systems, check memory limits per job.

### 2. Wrong Strandedness Setting
Using incorrect strandedness results in near-zero gene counts. If you see uniformly low
counts, check strandedness with `infer_experiment.py` from RSeQC. ENCODE dUTP libraries
are `reverse` stranded.

### 3. Using FPKM for Cross-Sample Comparison
FPKM values are not comparable across samples because they depend on total library
composition. Use TPM (comparable across samples) or raw counts with DESeq2/edgeR
normalization for differential expression.

### 4. Ignoring Multi-Mapped Reads
RSEM uses an expectation-maximization algorithm to probabilistically assign multi-mapped
reads. This is critical for gene families and repetitive elements. Do not pre-filter
multi-mappers before RSEM quantification.

### 5. Skipping rRNA Assessment
High rRNA contamination (>10%) indicates failed rRNA depletion. This reduces effective
sequencing depth and inflates apparent duplication rates. Always check rRNA rate before
downstream analysis.

### 6. Not Using 2-Pass Mode for Novel Junctions
STAR 1-pass mode only uses annotated splice junctions. 2-pass mode first discovers novel
junctions then re-maps, critical for non-model organisms or samples with extensive
alternative splicing.

## Pipeline Scripts

| File | Description | Lines |
|------|-------------|-------|
| `scripts/main.nf` | Nextflow DSL2 pipeline | ~130 |
| `scripts/nextflow.config` | Execution profiles (local/slurm/gcp/aws) | ~60 |
| `scripts/Dockerfile` | Docker build with STAR, RSEM, Kallisto, RSeQC | ~35 |

## ENCODE Data Integration

After running on your own data, compare with ENCODE reference:

```python
# Find matching ENCODE RNA-seq experiments
encode_search_experiments(
    assay_title="total RNA-seq",
    organ="pancreas",
    biosample_type="tissue"
)

# Download ENCODE gene quantifications for comparison
encode_batch_download(
    download_dir="/data/encode_reference/",
    output_type="gene quantifications",
    assay_title="total RNA-seq",
    organ="pancreas",
    assembly="GRCh38"
)

# Download ENCODE signal tracks for browser visualization
encode_search_files(
    file_format="bigWig",
    assay_title="total RNA-seq",
    organ="pancreas",
    output_type="signal of unique reads"
)
```

## Pitfalls & Edge Cases

- **Strandedness must match library prep**: STAR requires correct `--outSAMstrandField` and RSEM needs `--strandedness`. Using wrong strand settings can halve gene counts or assign reads to antisense genes.
- **rRNA contamination**: rRNA >10% wastes sequencing depth. Ribosomal depletion libraries should have <5%. Poly-A selection libraries should have <1%. Check with FastQC or Picard CollectRnaSeqMetrics.
- **STAR 2-pass mode is required**: The first pass discovers novel splice junctions; the second pass uses them. Single-pass STAR misses tissue-specific or rare splicing events, reducing sensitivity for differential exon usage.
- **Gene-level vs transcript-level quantification**: RSEM provides transcript-level estimates but gene-level aggregation is more robust for differential expression. Transcript-level analysis requires many more replicates (≥6).
- **TPM normalization is not for cross-sample comparison**: TPM normalizes within a sample but is NOT appropriate for comparing expression across conditions. Use DESeq2 size factors or TMM normalization for differential expression.
- **Batch effects in multi-lab data**: RNA-seq is highly sensitive to library prep method, sequencer, and lab. Always check for batch effects with PCA before combining datasets from different sources.

## Walkthrough: Processing ENCODE RNA-seq from FASTQ to Gene Quantification

**Goal**: Process raw RNA-seq FASTQ files through the ENCODE pipeline to generate gene expression quantifications (TPM/FPKM) and signal tracks.
**Context**: The ENCODE RNA-seq pipeline uses STAR 2-pass alignment and RSEM quantification, producing both gene-level and transcript-level expression estimates.

### Step 1: Find RNA-seq experiment

```
encode_get_experiment(accession="ENCSR000CPR")
```

Expected output:
```json
{
  "accession": "ENCSR000CPR",
  "assay_title": "RNA-seq",
  "biosample_summary": "K562",
  "replicates": 2,
  "status": "released"
}
```

### Step 2: List FASTQ files

```
encode_list_files(accession="ENCSR000CPR", file_format="fastq")
```

Expected output:
```json
{
  "files": [
    {"accession": "ENCFF200RN1", "output_type": "reads", "paired_end": "1", "biological_replicates": [1], "file_size_mb": 3200},
    {"accession": "ENCFF201RN2", "output_type": "reads", "paired_end": "2", "biological_replicates": [1], "file_size_mb": 3300}
  ]
}
```

### Step 3: Run the RNA-seq pipeline

```bash
nextflow run pipeline-rnaseq/main.nf \
  --fastq_r1 ENCFF200RN1.fastq.gz \
  --fastq_r2 ENCFF201RN2.fastq.gz \
  --genome GRCh38 \
  --annotation gencode.v36.annotation.gtf \
  --strandedness reverse \
  -profile docker
```

Key pipeline steps:
1. Quality trimming (fastp)
2. STAR 2-pass alignment (splice-aware)
3. RSEM gene quantification (TPM, FPKM, expected counts)
4. Kallisto transcript quantification (optional)
5. Signal track generation (bigWig)
6. QC metrics (RSeQC, MultiQC)

### Step 4: Validate output quality

| Metric | Threshold | Purpose |
|---|---|---|
| Mapping rate | >= 70% | Alignment success |
| rRNA rate | < 10% | rRNA depletion efficiency |
| Replicate correlation | >= 0.9 | Biological consistency |
| Exonic rate | > 60% | Expected for mRNA-seq |

### Step 5: Use expression data with ENCODE epigenomic data

Compare gene expression with enhancer marks:
```
encode_search_experiments(assay_title="Histone ChIP-seq", biosample_term_name="K562", target="H3K27ac", organism="Homo sapiens")
```

**Interpretation**: Genes with high TPM AND nearby H3K27ac peaks have validated enhancer-gene connections. Low expression despite nearby enhancer marks suggests poised or tissue-specific regulation.

### Integration with downstream skills
- Gene quantifications feed into -> **peak-annotation** for expression-validated peak targets
- Expression data connects to -> **gtex-expression** for tissue comparison
- Processed data feeds into -> **compare-biosamples** for differential expression analysis
- Pipeline provenance logged by -> **data-provenance**

## Code Examples

### 1. Find RNA-seq experiments for a tissue

```
encode_search_experiments(assay_title="total RNA-seq", organ="liver", organism="Homo sapiens")
```

Expected output:
```json
{
  "total": 35,
  "results": [
    {"accession": "ENCSR300RNA", "assay_title": "RNA-seq", "biosample_summary": "liver", "status": "released"}
  ]
}
```

### 2. Check for existing gene quantifications

```
encode_list_files(accession="ENCSR300RNA", file_format="tsv", output_type="gene quantifications", assembly="GRCh38")
```

Expected output:
```json
{
  "files": [
    {"accession": "ENCFF400GEQ", "output_type": "gene quantifications", "file_format": "tsv", "file_size_mb": 5.2}
  ]
}
```

### 3. Download expression data

```
encode_download_files(accessions=["ENCFF400GEQ"], download_dir="/data/rnaseq/quantification")
```

Expected output:
```json
{
  "downloaded": 1,
  "md5_verified": true,
  "files": ["/data/rnaseq/quantification/ENCFF400GEQ.tsv"]
}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Gene expression (TPM/FPKM) | **peak-annotation** | Validate enhancer targets with expression data |
| Expression matrix | **gtex-expression** | Compare cell-line vs. tissue expression |
| Differential expression results | **compare-biosamples** | Identify tissue-specific gene regulation |
| Signal tracks (bigWig) | **visualization-workflow** | Display expression signal in genome browser |
| Expression quantifications | **disease-research** | Connect gene expression to disease phenotypes |
| Pipeline run parameters | **data-provenance** | Record STAR/RSEM versions and settings |
| QC metrics | **quality-assessment** | Validate against ENCODE RNA-seq standards |

## Related Skills

- **pipeline-guide** (parent): General pipeline selection and resource assessment
- **quality-assessment**: Deep-dive QC analysis beyond basic metrics
- **integrative-analysis**: Combine RNA-seq with ChIP-seq/ATAC-seq for regulatory inference
- **compare-biosamples**: Compare expression profiles across cell types
- **single-cell-encode**: For scRNA-seq data processing (different pipeline)
- **pipeline-chipseq**: Sibling pipeline for ChIP-seq data
- **pipeline-atacseq**: Sibling pipeline for ATAC-seq data
- **publication-trust**: Verify literature claims backing analytical decisions

## Presenting Results

When reporting RNA-seq pipeline results:

- **Mapping rate**: Report STAR uniquely mapped rate (>70% expected), multi-mapped rate (<10%), and unmapped rate from Log.final.out
- **Gene/transcript counts**: Report number of detected genes (TPM>1, expect >12,000 for human) and detected transcripts
- **rRNA rate**: Report rRNA contamination percentage (<10% expected). Flag if rRNA depletion appears to have failed
- **Quantification paths**: Provide paths to RSEM genes.results (TPM, FPKM, expected_count) and Kallisto abundance.tsv files
- **Strandedness**: Confirm the detected strandedness from RSeQC infer_experiment.py matches the expected library protocol
- **Key QC metrics**: Present exonic rate (>60%), gene body coverage uniformity, duplication rate, and saturation curve status in a summary table
- **Signal tracks**: Provide paths to strand-specific bigWig files (plus/ and minus/)
- **Next steps**: Suggest `integrative-analysis` to combine RNA-seq with ChIP-seq/ATAC-seq for regulatory inference, or `compare-biosamples` for cross-tissue expression comparison

## For the request: "$ARGUMENTS"
