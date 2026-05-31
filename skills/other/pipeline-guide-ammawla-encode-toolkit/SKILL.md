---
name: pipeline-guide
description: Access ENCODE uniform analysis pipelines, generate user-specific Nextflow/WDL pipelines, manage compute resources, and integrate with cloud platforms. Use when the user wants to understand ENCODE pipelines, run pipelines on their own data, generate custom Nextflow workflows from ENCODE pipeline code, check compute requirements (CPU/GPU/memory), run pipelines in background, or integrate with Google Cloud, AWS, or other cloud platforms. Also use when the user asks about ENCODE pipeline outputs, processing standards, software versions, or wants to replicate ENCODE processing. Covers local execution, HPC, and cloud deployment with resource-aware scheduling. Use this skill for ANY pipeline execution, workflow generation, or compute resource management task involving ENCODE data.
---

# ENCODE Pipeline Guide and Custom Workflow Generation

## When to Use

- User wants to understand ENCODE uniform analysis pipelines or run them on their own data
- User asks about "ENCODE pipeline", "Nextflow", "WDL", "processing standards", or "pipeline requirements"
- User needs to generate a custom Nextflow/WDL workflow based on ENCODE pipeline specifications
- User wants to know compute requirements (CPU, GPU, memory, storage) for running pipelines
- Example queries: "how do I run the ENCODE ChIP-seq pipeline?", "what are the compute requirements for Hi-C processing?", "generate a Nextflow pipeline for my ATAC-seq data"

Understand ENCODE pipelines, generate user-specific workflows in Nextflow/WDL, and manage compute resources for local, HPC, and cloud execution.

## ENCODE Uniform Analysis Pipelines

ENCODE uses standardized pipelines for each assay type, ensuring reproducibility across all datasets. All pipelines are:
- **Open source**: GitHub (github.com/ENCODE-DCC)
- **Containerized**: Docker and Singularity images
- **Written in WDL**: Workflow Description Language (Cromwell execution engine)
- **Portable**: Local, HPC (SLURM, SGE, PBS), or cloud (Google Cloud, AWS, Azure)

### Pipeline Repository Map

| Assay | GitHub Repository | Primary Tools | Container |
|-------|------------------|---------------|-----------|
| ChIP-seq | `ENCODE-DCC/chip-seq-pipeline2` | BWA, MACS2, IDR | `encodedcc/chip-seq-pipeline:v2.2.1` |
| ATAC-seq | `ENCODE-DCC/atac-seq-pipeline` | Bowtie2, MACS2, IDR | `encodedcc/atac-seq-pipeline:v2.2.0` |
| RNA-seq | `ENCODE-DCC/rna-seq-pipeline` | STAR, RSEM | `encodedcc/rna-seq-pipeline:v1.2.0` |
| DNase-seq | `ENCODE-DCC/dnase-seq-pipeline` | BWA, Hotspot2 | `encodedcc/dnase-seq-pipeline` |
| WGBS | `ENCODE-DCC/dna-me-pipeline` | Bismark/bwa-meth, MethylDackel | `encodedcc/dna-me-pipeline` |
| Hi-C | `ENCODE-DCC/hic-pipeline` | BWA, Juicer, HiCCUPS | `encodedcc/hic-pipeline` |
| scRNA-seq | `ENCODE-DCC/scrna-seq-pipeline` | STARsolo, Cellranger | — |
| scATAC-seq | `ENCODE-DCC/scatac-seq-pipeline` | Chromap, SnapATAC2 | — |
| CUT&RUN | `ENCODE-DCC/cutandrun-pipeline` | Bowtie2, SEACR/MACS2 | — |

## Literature Foundation

| Reference | Year | Relevance | Citations |
|-----------|------|-----------|-----------|
| Di Tommaso et al. "Nextflow enables reproducible computational workflows" | 2017 | Nextflow workflow manager | ~2,800 |
| Ewels et al. "The nf-core framework for community-curated bioinformatics pipelines" | 2020 | nf-core community pipelines | ~1,900 |
| Kurtzer et al. "Singularity: Scientific containers for mobility of compute" | 2017 | Singularity containers for HPC | ~2,500 |
| Merkel "Docker: lightweight Linux containers for consistent development and deployment" | 2014 | Docker containerization | ~3,000 |
| ENCODE Project Consortium "Expanded encyclopaedias of DNA elements" | 2020 | ENCODE Phase 3 standards | ~1,200 |
| Gruening et al. "Bioconda: sustainable and comprehensive software distribution" | 2018 | Bioconda packaging ecosystem | ~1,400 |

## Pipeline Output Types by Assay

### ChIP-seq Pipeline
| Output Type | Format | Description | Use For |
|------------|--------|-------------|---------|
| alignments | bam | Filtered, deduplicated | Reprocessing, visualization |
| signal of unique reads | bigWig | Unique read signal | Genome browser |
| fold change over control | bigWig | Normalized signal | Comparative visualization |
| IDR thresholded peaks | bed narrowPeak | Reproducible peaks | Peak analysis (gold standard) |
| pseudoreplicated peaks | bed narrowPeak | Single-replicate peaks | When only 1 replicate |
| optimal IDR peaks | bed narrowPeak | Pooled replicate peaks | Most complete peak set |

### ATAC-seq Pipeline
| Output Type | Format | Description | Use For |
|------------|--------|-------------|---------|
| alignments | bam | No-mito, deduplicated | Reprocessing |
| signal of unique reads | bigWig | Signal track | Genome browser |
| IDR thresholded peaks | bed narrowPeak | Reproducible peaks | Accessibility analysis |
| pseudoreplicated peaks | bed narrowPeak | Single-replicate | Backup peaks |

### RNA-seq Pipeline
| Output Type | Format | Description | Use For |
|------------|--------|-------------|---------|
| alignments | bam | STAR-aligned | Visualization, reprocessing |
| gene quantifications | tsv | Gene-level counts (RSEM) | Differential expression |
| transcript quantifications | tsv | Transcript-level counts | Isoform analysis |
| signal of unique reads | bigWig | Strand-specific signal | Genome browser |

### WGBS Pipeline
| Output Type | Format | Description | Use For |
|------------|--------|-------------|---------|
| alignments | bam | Bisulfite-converted | Reprocessing |
| methylation state at CpG | bed bedMethyl | Per-CpG levels | Methylation analysis |

### Hi-C Pipeline
| Output Type | Format | Description | Use For |
|------------|--------|-------------|---------|
| contact matrix | hic | Interaction frequencies | TAD/compartment calling |
| chromatin interactions | bedpe | Called loops | Loop analysis |

## Choosing the Right Output Files

### Decision Table
| Analysis Goal | File Type | Output Type | Priority |
|--------------|-----------|-------------|----------|
| Visualization | bigWig | fold change over control (ChIP) / signal of unique reads (others) | preferred_default=True |
| Peak overlap | bed narrowPeak | IDR thresholded peaks | Highest confidence |
| Quantitative | tsv / bed | gene quantifications / methylation state | Pipeline defaults |
| Custom processing | fastq | reads | When ENCODE pipeline doesn't match |

```
encode_list_files(experiment_accession="ENCSR...", preferred_default=True)
```

## Step 1: Assess User Compute Resources

Before generating any pipeline, check available resources:

### System Check Commands
```bash
# CPU cores
nproc                              # Linux
sysctl -n hw.ncpu                  # macOS

# Memory
free -h                            # Linux
sysctl -n hw.memsize | awk '{print $1/1024/1024/1024 " GB"}'  # macOS

# Disk space
df -h /path/to/data/

# GPU (if applicable)
nvidia-smi                         # NVIDIA GPU
# Note: Most ENCODE pipelines do NOT require GPU

# Docker availability
docker --version
docker info | grep "Total Memory"

# Singularity (for HPC)
singularity --version
```

### Minimum Resource Requirements by Pipeline

| Pipeline | Min CPU | Min RAM | Min Disk | GPU | Time Estimate (per sample) |
|----------|---------|---------|----------|-----|---------------------------|
| ChIP-seq | 4 cores | 16 GB | 50 GB | No | 2–4 hours |
| ATAC-seq | 4 cores | 16 GB | 50 GB | No | 2–4 hours |
| RNA-seq | 8 cores | 32 GB | 100 GB | No | 4–8 hours (index build) |
| WGBS | 8 cores | 48 GB | 200 GB | No | 12–24 hours |
| Hi-C | 8 cores | 64 GB | 200 GB | No | 8–16 hours |
| scRNA-seq | 8 cores | 64 GB | 100 GB | No | 4–8 hours |

### Resource Scaling
- **CPU**: Alignment steps are parallelizable; doubling cores approximately halves alignment time
- **RAM**: Genome index loading is the bottleneck; STAR requires ~32 GB for human genome
- **Disk**: FASTQ + BAM + intermediate files can exceed 100 GB per sample
- **Network**: ENCODE downloads at ~50–200 MB/s; plan for transfer time

## Step 2: Generate Custom Nextflow Workflows

When the user needs to run ENCODE-style processing, generate Nextflow workflows that mirror ENCODE pipeline logic.

### Why Nextflow Over WDL
- **Broader adoption**: Nextflow is used by nf-core, most HPC centers, and cloud platforms
- **Native container support**: Docker, Singularity, Podman
- **Cloud integration**: AWS Batch, Google Cloud Life Sciences, Azure Batch natively
- **Resource management**: Built-in CPU/memory/time limits per process
- **Resume capability**: Failed runs restart from last successful step

### Nextflow Pipeline Template

```nextflow
#!/usr/bin/env nextflow
nextflow.enable.dsl=2

// Pipeline parameters
params.reads         = null          // Input FASTQ path
params.genome        = 'GRCh38'     // Genome assembly
params.outdir        = './results'   // Output directory
params.max_cpus      = Runtime.runtime.availableProcessors()
params.max_memory    = '${available_memory} GB'
params.max_time      = '24.h'

// Resource limits (user-specific)
process {
    cpus   = { check_max( 4 * task.attempt, 'cpus' ) }
    memory = { check_max( 8.GB * task.attempt, 'memory' ) }
    time   = { check_max( 4.h * task.attempt, 'time' ) }

    errorStrategy = 'retry'
    maxRetries    = 2
}

// Example: ChIP-seq alignment process
process ALIGN_READS {
    tag "${sample_id}"
    cpus 4
    memory '16 GB'
    container 'encodedcc/chip-seq-pipeline:v2.2.1'

    input:
    tuple val(sample_id), path(reads)
    path genome_index

    output:
    tuple val(sample_id), path("*.bam"), emit: bam

    script:
    """
    bwa mem -t ${task.cpus} ${genome_index}/genome.fa ${reads} | \
        samtools sort -@ ${task.cpus} -o ${sample_id}.sorted.bam
    samtools index ${sample_id}.sorted.bam
    """
}
```

### Resource-Aware Configuration

Generate a `nextflow.config` based on user's system:

```nextflow
// Auto-detected from user system
params {
    max_cpus   = ${detected_cpus}
    max_memory = '${detected_memory} GB'
    max_time   = '72.h'
}

// Profile: local execution
profiles {
    local {
        process.executor = 'local'
        docker.enabled   = true
    }

    // Profile: SLURM HPC
    slurm {
        process.executor = 'slurm'
        process.queue    = 'normal'
        singularity.enabled = true
    }

    // Profile: Google Cloud
    gcloud {
        process.executor = 'google-lifesciences'
        google.region    = 'us-central1'
        google.project   = '${user_project}'
        workDir          = 'gs://${user_bucket}/work'
    }

    // Profile: AWS Batch
    awsbatch {
        process.executor = 'awsbatch'
        process.queue    = '${user_queue}'
        aws.region       = 'us-east-1'
        workDir          = 's3://${user_bucket}/work'
    }
}

// Resource checking function
def check_max(obj, type) {
    if (type == 'memory') {
        try { if (obj.compareTo(params.max_memory as nextflow.util.MemoryUnit) == 1) return params.max_memory as nextflow.util.MemoryUnit else return obj }
        catch (all) { return params.max_memory as nextflow.util.MemoryUnit }
    } else if (type == 'cpus') {
        try { return Math.min(obj, params.max_cpus as int) }
        catch (all) { return params.max_cpus as int }
    }
}
```

## Step 3: Cloud Integration

### Available Integrations (Official Marketplace)

For users who cannot run pipelines locally, offer cloud integration:

#### Google Cloud / Colab
- **Nextflow + Google Cloud Life Sciences**: Run full pipelines on Google Cloud
- **Google Colab**: For interactive analysis (R/Python notebooks)
  - Limited to 12 GB RAM (free tier) or 25 GB (Pro)
  - GPU available (useful for deep learning, not standard pipelines)
  - Best for: downstream analysis after pipeline completion

#### AWS
- **Nextflow + AWS Batch**: Run pipelines on AWS
- **AWS SageMaker**: For ML-based analysis
- Best for: Large-scale batch processing

#### Other Platforms
- **Terra (Broad Institute)**: WDL-native platform, ENCODE pipelines pre-installed
- **DNAnexus**: Cloud genomics platform with ENCODE pipeline apps
- **Galaxy**: Web-based, no coding required

### Cloud Cost Estimates
| Pipeline | Cloud Instance | Estimated Cost/Sample |
|----------|---------------|---------------------|
| ChIP-seq | n1-standard-8 (GCP) / m5.2xlarge (AWS) | $2–5 |
| ATAC-seq | n1-standard-8 / m5.2xlarge | $2–5 |
| RNA-seq | n1-standard-16 / m5.4xlarge | $5–10 |
| WGBS | n1-highmem-16 / r5.4xlarge | $10–25 |
| Hi-C | n1-highmem-16 / r5.4xlarge | $8–20 |

## Step 4: Background Execution

### Local Background Execution
```bash
# Run Nextflow in background with nohup
nohup nextflow run pipeline.nf \
    -profile local \
    --reads '/path/to/reads/*.fastq.gz' \
    --outdir results/ \
    -resume \
    -bg \
    > pipeline.log 2>&1 &

# Monitor progress
tail -f pipeline.log
nextflow log last
```

### Screen/tmux for Long Runs
```bash
# Create a persistent session
screen -S encode_pipeline
# or
tmux new -s encode_pipeline

# Run pipeline inside session
nextflow run pipeline.nf -profile local --reads '...' -resume

# Detach: Ctrl+A then D (screen) or Ctrl+B then D (tmux)
# Reattach later: screen -r encode_pipeline / tmux attach -t encode_pipeline
```

## Step 5: Extract ENCODE Pipeline Code Snippets

When the user needs specific processing steps (not full pipelines), extract the relevant code:

### Common Snippets

#### Alignment (ChIP-seq / ATAC-seq)
```bash
# ENCODE ChIP-seq alignment (from chip-seq-pipeline2)
bwa mem -t ${NCPUS} ${GENOME_INDEX} ${FASTQ_R1} ${FASTQ_R2} | \
    samtools view -@ ${NCPUS} -bS -q 30 -F 1804 - | \
    samtools sort -@ ${NCPUS} -o aligned.bam
samtools index aligned.bam

# Mark/remove duplicates
picard MarkDuplicates \
    INPUT=aligned.bam \
    OUTPUT=dedup.bam \
    METRICS_FILE=dup_metrics.txt \
    REMOVE_DUPLICATES=true
```

#### Peak Calling (MACS2)
```bash
# ENCODE standard peak calling
macs2 callpeak \
    -t treatment.bam \
    -c control.bam \
    -f BAMPE \
    -g hs \
    -n sample \
    --nomodel \
    --shift -75 \
    --extsize 150 \
    -B --SPMR \
    --keep-dup all \
    --call-summits \
    -q 0.05 \
    --outdir peaks/
```

#### IDR Analysis
```bash
# ENCODE IDR for replicate concordance
idr --samples rep1_peaks.narrowPeak rep2_peaks.narrowPeak \
    --input-file-type narrowPeak \
    --rank p.value \
    --output-file idr_peaks.narrowPeak \
    --plot \
    --idr-threshold 0.05
```

#### RNA-seq Quantification
```bash
# ENCODE RNA-seq (STAR + RSEM)
STAR --runThreadN ${NCPUS} \
    --genomeDir ${STAR_INDEX} \
    --readFilesIn ${FASTQ_R1} ${FASTQ_R2} \
    --readFilesCommand zcat \
    --outSAMtype BAM SortedByCoordinate \
    --quantMode TranscriptomeSAM \
    --outFilterMultimapNmax 20 \
    --alignSJoverhangMin 8 \
    --outFilterMismatchNmax 999 \
    --outFilterMismatchNoverReadLmax 0.04

rsem-calculate-expression \
    --bam --paired-end \
    -p ${NCPUS} \
    Aligned.toTranscriptome.out.bam \
    ${RSEM_INDEX} \
    rsem_output
```

#### Liftover (GRCh37 → GRCh38)
```bash
# Download chain file
wget https://hgdownload.soe.ucsc.edu/goldenPath/hg19/liftOver/hg19ToHg38.over.chain.gz

# Run liftover
liftOver input_hg19.bed hg19ToHg38.over.chain.gz output_hg38.bed unmapped.bed

# Log: liftOver version (Kent et al. 2002, Genome Research)
# Log: chain file source and date accessed
# Log: input count, output count, unmapped count
```

## Step 6: Language-Specific Integration

### R / Bioconductor
For users working in R, ENCODE data integrates with:
```r
# Key Bioconductor packages for ENCODE data
library(GenomicRanges)      # Genomic intervals
library(rtracklayer)        # Import BED/bigWig
library(DESeq2)             # Differential expression
library(DiffBind)           # Differential binding (ChIP-seq)
library(ChIPseeker)         # Peak annotation
library(chromVAR)           # Chromatin accessibility
library(BSgenome.Hsapiens.UCSC.hg38)  # Genome sequence
library(TxDb.Hsapiens.UCSC.hg38.knownGene)  # Gene models

# Import ENCODE peak file
peaks <- rtracklayer::import("ENCFF123ABC.bed", format="narrowPeak")

# Import ENCODE bigWig signal
signal <- rtracklayer::import("ENCFF456DEF.bigWig", format="bigWig")
```

Check package availability:
```r
# CRAN
available.packages(repos="https://cran.r-project.org")[,"Version"]

# Bioconductor
BiocManager::available()
BiocManager::version()
```

### Python
```python
# Key Python packages for ENCODE data
import pyBigWig          # Read bigWig files
import pybedtools        # BED operations
import pysam             # BAM file access
import scanpy as sc      # Single-cell analysis
import anndata           # AnnData format
import cooler            # Hi-C contact matrices
import pydeseq2          # Differential expression

# Import ENCODE peak file
import pandas as pd
peaks = pd.read_csv("ENCFF123ABC.bed", sep="\t", header=None,
                     names=["chr","start","end","name","score","strand",
                            "signalValue","pValue","qValue","peak"])
```

### Bash / Command Line
Core tools for ENCODE data processing:
```bash
# Essential tools and typical versions
bedtools --version    # v2.31.0 - genomic arithmetic
samtools --version    # 1.19 - BAM/CRAM operations
tabix                 # indexing BED/VCF
bigWigToBedGraph      # UCSC Kent tools
bedToBigBed           # UCSC Kent tools
macs2 --version       # 2.2.9.1 - peak calling
idr --version         # 2.0.4.2 - reproducibility
deeptools --version   # 3.5.4 - signal visualization
```

## Provenance Integration

When generating or running any pipeline, integrate with the data-provenance skill:

1. **Before execution**: Log all input files, tool versions, reference files
2. **During execution**: Capture stdout/stderr, resource usage
3. **After execution**: Log all output files with MD5 checksums, record runtime
4. **Script storage**: Save the generated pipeline script in `scripts/` directory

Every pipeline run should produce a provenance entry that enables methods writing.

## Pitfalls and Edge Cases

### Version Mismatches
- ENCODE has used multiple pipeline versions over the years
- Files from different pipeline versions may not be directly comparable
- Check the `analysis` field in file metadata for pipeline version
- When reprocessing, use the same pipeline version as ENCODE for comparability

### Container Requirements
- Docker requires root access (or rootless Docker)
- HPC systems typically use Singularity instead of Docker
- Singularity can pull Docker images: `singularity pull docker://encodedcc/chip-seq-pipeline:v2.2.1`

### Genome Index Files
- STAR genome index requires ~32 GB RAM to generate and ~30 GB disk
- BWA index is smaller (~8 GB for human genome)
- Pre-built indices are available from ENCODE or iGenomes
- Log the exact index version and source in provenance

### Cloud Costs
- Forgot to stop instances = runaway costs
- Use preemptible/spot instances for 60–80% cost savings (with retry logic)
- Set billing alerts before starting cloud runs

### Resume and Checkpointing
- Always use `-resume` flag with Nextflow to avoid re-running completed steps
- Cromwell provides similar call caching
- This is critical for long-running pipelines (WGBS, Hi-C)

## Child Pipeline Skills

For detailed, executable pipeline implementations, use these assay-specific child skills:

| Pipeline Skill | Assay | Aligner | Caller |
|---------------|-------|---------|--------|
| `pipeline-chipseq` | ChIP-seq | BWA-MEM | MACS2 + IDR |
| `pipeline-atacseq` | ATAC-seq | Bowtie2 | MACS2 (Tn5-adjusted) |
| `pipeline-rnaseq` | RNA-seq | STAR | RSEM + Kallisto |
| `pipeline-wgbs` | WGBS | Bismark | MethylDackel |
| `pipeline-hic` | Hi-C | BWA | Juicer + HiCCUPS |
| `pipeline-dnaseseq` | DNase-seq | BWA | Hotspot2 |
| `pipeline-cutandrun` | CUT&RUN | Bowtie2 | SEACR |

Each child includes: SKILL.md overview, 5 stage reference files, Nextflow DSL2 pipeline, Dockerfile, and cloud deployment configs (local/SLURM/GCP/AWS).

## Walkthrough: Selecting and Configuring the Right Pipeline for Your ENCODE Data

**Goal**: Guide a researcher from raw ENCODE FASTQ files through pipeline selection, configuration, and execution using the appropriate ENCODE uniform processing pipeline.
**Context**: ENCODE provides standardized pipelines for each assay type. This skill helps users select the right pipeline and configure it for their specific experiment.

### Step 1: Identify the experiment and assay type

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
  "status": "released",
  "pipeline": "Histone ChIP-seq (GRCh38)"
}
```

**Interpretation**: This is a Histone ChIP-seq experiment targeting H3K27ac. Use the **pipeline-chipseq** skill for processing.

### Step 2: Download raw FASTQ files

```
encode_list_files(accession="ENCSR000AKA", file_format="fastq", assembly="GRCh38")
```

Expected output:
```json
{
  "files": [
    {"accession": "ENCFF001FQ1", "output_type": "reads", "file_format": "fastq", "biological_replicates": [1], "paired_end": "1", "file_size_mb": 2400},
    {"accession": "ENCFF002FQ2", "output_type": "reads", "file_format": "fastq", "biological_replicates": [1], "paired_end": "2", "file_size_mb": 2500}
  ]
}
```

### Step 3: Select pipeline based on assay type

| ENCODE Assay | Pipeline Skill | Key Tool |
|---|---|---|
| Histone ChIP-seq | **pipeline-chipseq** | BWA-MEM + MACS2 + IDR |
| TF ChIP-seq | **pipeline-chipseq** | BWA-MEM + MACS2 + IDR |
| ATAC-seq | **pipeline-atacseq** | Bowtie2 + Tn5 shift + MACS2 |
| RNA-seq | **pipeline-rnaseq** | STAR 2-pass + RSEM |
| WGBS | **pipeline-wgbs** | Bismark + MethylDackel |
| Hi-C | **pipeline-hic** | BWA + pairtools + Juicer |
| DNase-seq | **pipeline-dnaseseq** | BWA + Hotspot2 |
| CUT&RUN/CUT&Tag | **pipeline-cutandrun** | Bowtie2 + SEACR |

### Step 4: Configure and run

For Histone ChIP-seq:
```bash
nextflow run pipeline-chipseq/main.nf \
  --fastq_r1 ENCFF001FQ1.fastq.gz \
  --fastq_r2 ENCFF002FQ2.fastq.gz \
  --genome GRCh38 \
  --target H3K27ac \
  --broad_peak false \
  -profile docker
```

### Step 5: Quality check the output

Use → **quality-assessment** skill to evaluate pipeline output against ENCODE standards:
- FRiP >= 1%
- NSC > 1.05
- RSC > 0.8

### Integration with downstream skills
- Raw data from → **download-encode** provides FASTQ input for all pipelines
- Pipeline output feeds into → **quality-assessment** for ENCODE-standard QC
- Processed peaks feed into → **peak-annotation**, **regulatory-elements**, **histone-aggregation**
- Each assay has a dedicated pipeline skill: pipeline-chipseq through pipeline-cutandrun

## Code Examples

### 1. Determine which pipeline to use
```
encode_get_experiment(accession="ENCSR000AKA")
```

Expected output:
```json
{
  "accession": "ENCSR000AKA",
  "assay_title": "Histone ChIP-seq",
  "pipeline": "Histone ChIP-seq (GRCh38)"
}
```

### 2. Find FASTQ files for pipeline input
```
encode_list_files(accession="ENCSR000AKA", file_format="fastq")
```

Expected output:
```json
{
  "files": [
    {"accession": "ENCFF001FQ1", "output_type": "reads", "paired_end": "1", "file_size_mb": 2400},
    {"accession": "ENCFF002FQ2", "output_type": "reads", "paired_end": "2", "file_size_mb": 2500}
  ]
}
```

### 3. Survey available data by assay type for pipeline selection
```
encode_get_facets(facet_field="assay_title", organism="Homo sapiens")
```

Expected output:
```json
{
  "facets": {
    "assay_title": {"Histone ChIP-seq": 2500, "TF ChIP-seq": 1800, "ATAC-seq": 450, "RNA-seq": 1200, "WGBS": 147}
  }
}
```

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Pipeline selection recommendation | **pipeline-chipseq** through **pipeline-cutandrun** | Route to correct assay-specific pipeline |
| FASTQ download commands | **download-encode** | Obtain raw data for pipeline input |
| Pipeline configuration | **bioinformatics-installer** | Install required pipeline dependencies |
| Pipeline output files | **quality-assessment** | Validate output against ENCODE QC standards |
| Processed peaks/signals | **peak-annotation** | Annotate pipeline output with gene assignments |
| Processed peaks | **regulatory-elements** | Classify pipeline output as enhancers/promoters/insulators |
| Pipeline run metadata | **data-provenance** | Log pipeline parameters and versions |
| Processed data | **visualization-workflow** | Generate QC and analysis visualizations |

## Related Skills

- `data-provenance` — Exact provenance logging for every operation
- `quality-assessment` — Evaluating pipeline output quality
- `download-encode` — Downloading ENCODE files for pipeline input
- `single-cell-encode` — Single-cell pipeline specifics
- `publication-trust` — Verify literature claims backing analytical decisions

## Presenting Results

When reporting pipeline recommendations:

- **Selected pipeline**: State the recommended pipeline (e.g., pipeline-chipseq, pipeline-atacseq) with a brief rationale based on the assay type and user's data
- **Resource estimates**: Present CPU, RAM, disk, and estimated runtime requirements in a table, compared against the user's available resources from system checks
- **Container availability**: Confirm whether Docker or Singularity is available and report the recommended container image with version tag
- **Execution profile**: Recommend the appropriate profile (local, slurm, gcp, aws) based on the user's compute environment
- **Cost estimate**: For cloud execution, provide per-sample cost estimates and recommend preemptible/spot instances where applicable
- **Genome index status**: Note whether pre-built genome indices are available or need to be generated, and estimate the index build time
- **Configuration summary**: Provide the recommended nextflow.config parameters tailored to the user's system
- **Next steps**: Direct the user to the specific child pipeline skill (e.g., "Use `pipeline-chipseq` to execute the pipeline with the parameters above")

## For the request: "$ARGUMENTS"
