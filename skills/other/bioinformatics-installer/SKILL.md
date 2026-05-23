---
name: bioinformatics-installer
description: "Install bioinformatics tools for ENCODE data analysis. Covers CLI tools (BWA, STAR, samtools, MACS2), R/Bioconductor packages (DESeq2, Seurat, ChIPseeker), Python packages (Scanpy, deeptools), and Nextflow pipeline infrastructure. Generates conda environments, R install scripts, and Python requirements. Use when the user needs to set up a bioinformatics workstation, install tools for a specific assay, create reproducible environments, or troubleshoot dependency issues. Trigger on: install tools, set up environment, conda create, bioinformatics setup, install R packages, install Bioconductor, install pipeline tools."
---

# Bioinformatics Installer for ENCODE Data Analysis

Install all bioinformatics tools needed for ENCODE data analysis, organized by assay type.
This skill provides ready-to-use conda environment definitions, R/Bioconductor install scripts,
Python package lists, and Nextflow pipeline infrastructure setup. Every environment is version-pinned
for reproducibility and tested against ENCODE uniform processing standards.

## When to Use

- User wants to install bioinformatics tools needed for ENCODE data analysis
- User asks about "install tools", "conda environment", "setup bioinformatics", or "install HOMER/MACS2/deeptools"
- User needs pre-configured conda environments for specific assay pipelines (ChIP-seq, ATAC-seq, RNA-seq, etc.)
- User wants to install R/Bioconductor packages (DESeq2, Seurat, ChIPseeker) or Python packages (Scanpy, pysam)
- Example queries: "install tools for ChIP-seq analysis", "set up a conda environment for ATAC-seq", "install deeptools and bedtools"

## Overview

ENCODE data analysis requires a broad ecosystem of tools spanning command-line aligners, peak
callers, signal processors, statistical analysis frameworks in R, Python visualization and
single-cell packages, and workflow engines. Setting up these tools correctly — with compatible
versions, proper channel priorities, and no dependency conflicts — is a significant barrier for
new users and a reproducibility concern for experienced analysts.

This skill solves that by providing:
- **7 assay-specific conda environments** with pinned tool versions matching ENCODE pipeline standards
- **R/Bioconductor install script** covering 50+ packages across 8 categories
- **Python install script** for single-cell, Hi-C, and genomics packages
- **Nextflow + container setup** for pipeline execution on local, HPC, and cloud platforms

All environments use the same channel priority (conda-forge > bioconda > defaults) and are tested
for cross-platform compatibility on Linux x86_64 and macOS (Intel + Apple Silicon where possible).

## Quick Start

Install a complete environment for any assay type with a single command:

```bash
# ChIP-seq (histone or TF)
conda env create -f skills/bioinformatics-installer/environments/chipseq-env.yml

# ATAC-seq
conda env create -f skills/bioinformatics-installer/environments/atacseq-env.yml

# RNA-seq
conda env create -f skills/bioinformatics-installer/environments/rnaseq-env.yml

# Hi-C
conda env create -f skills/bioinformatics-installer/environments/hic-env.yml

# Whole-Genome Bisulfite Sequencing (WGBS)
conda env create -f skills/bioinformatics-installer/environments/wgbs-env.yml

# DNase-seq
conda env create -f skills/bioinformatics-installer/environments/dnaseseq-env.yml

# CUT&RUN / CUT&Tag
conda env create -f skills/bioinformatics-installer/environments/cutandrun-env.yml
```

Using mamba for faster solves (recommended):

```bash
mamba env create -f skills/bioinformatics-installer/environments/chipseq-env.yml
```

Install R and Python packages:

```bash
# All R/Bioconductor packages
Rscript skills/bioinformatics-installer/scripts/install-r-packages.R --all

# All Python packages
bash skills/bioinformatics-installer/scripts/install-python-packages.sh --all

# Nextflow + Docker
bash skills/bioinformatics-installer/scripts/install-nextflow.sh --docker
```

## Per-Assay Environments

### ChIP-seq Environment (`encode-chipseq`)

For histone modification and transcription factor ChIP-seq processing following ENCODE
uniform pipeline standards (Landt et al. 2012, ENCODE Consortium 2020).

| Tool | Version | Purpose |
|------|---------|---------|
| BWA-MEM | 0.7.17 | Read alignment to reference genome (Li & Durbin 2009) |
| samtools | 1.19 | BAM manipulation, sorting, indexing, flagstat (Li et al. 2009) |
| MACS2 | 2.2.9.1 | Peak calling for narrow (TF) and broad (histone) marks (Zhang et al. 2008) |
| Picard | 3.1.1 | Duplicate marking and library complexity metrics (Broad Institute) |
| phantompeakqualtools | 1.2.2 | Strand cross-correlation (NSC/RSC) quality metrics (Kharchenko et al. 2008) |
| IDR | 2.0.3 | Irreproducible Discovery Rate for replicate consistency (Li et al. 2011) |
| deeptools | 3.5.5 | Signal normalization (bamCoverage), fingerprint, correlation (Ramirez et al. 2016) |
| bedtools | 2.31.0 | Interval operations, blacklist filtering (Quinlan & Hall 2010) |
| FastQC | 0.12.1 | Raw read quality assessment (Andrews 2010) |
| Trim Galore | 0.6.10 | Adapter and quality trimming via Cutadapt (Krueger 2012) |
| MultiQC | 1.21 | Aggregate QC report across all pipeline stages (Ewels et al. 2016) |
| bedGraphToBigWig | — | Convert bedGraph signal to bigWig for genome browser viewing (Kent et al. 2010) |

**Memory**: BWA index for GRCh38 requires ~5.5 GB RAM. Peak calling with MACS2 typically requires
4-8 GB. phantompeakqualtools loads full BAM into memory.

**Environment file**: `environments/chipseq-env.yml`

---

### ATAC-seq Environment (`encode-atacseq`)

For chromatin accessibility profiling via ATAC-seq following ENCODE standards
(Buenrostro et al. 2013, Corces et al. 2017).

| Tool | Version | Purpose |
|------|---------|---------|
| Bowtie2 | 2.5.3 | Alignment (preferred over BWA for ATAC-seq short fragments) (Langmead & Salzberg 2012) |
| MACS2 | 2.2.9.1 | Peak calling with --nomodel --shift -100 --extsize 200 for ATAC (Zhang et al. 2008) |
| samtools | 1.19 | BAM manipulation, mitochondrial read filtering |
| Picard | 3.1.1 | Duplicate marking, insert size metrics |
| deeptools | 3.5.5 | alignmentSieve (Tn5 offset), bamCoverage (signal tracks), plotFingerprint |
| bedtools | 2.31.0 | Blacklist filtering, interval operations |
| FastQC | 0.12.1 | Raw read quality and adapter content assessment |
| Trim Galore | 0.6.10 | Adapter trimming (Nextera adapters for ATAC-seq) |
| MultiQC | 1.21 | Aggregate QC reporting |

**Key ATAC-seq parameters**: Tn5 transposase introduces a +4/-5 bp offset that must be corrected.
Fragment size distribution should show nucleosomal ladder (sub-nucleosomal, mono-, di-, tri-).
TSS enrichment score should be >= 5 (GRCh38), >= 6 (hg19), or >= 10 (mm10) for high-quality data (ENCODE data standards).

**Environment file**: `environments/atacseq-env.yml`

---

### RNA-seq Environment (`encode-rnaseq`)

For gene expression quantification following ENCODE RNA-seq standards
(Conesa et al. 2016, ENCODE Consortium 2020).

| Tool | Version | Purpose |
|------|---------|---------|
| STAR | 2.7.11b | Splice-aware alignment with 2-pass mapping (Dobin et al. 2013) |
| RSEM | 1.3.3 | Gene/transcript quantification with expectation-maximization (Li & Dewey 2011) |
| Kallisto | 0.50.1 | Pseudoalignment-based transcript quantification (Bray et al. 2016) |
| Salmon | 1.10.3 | Quasi-mapping transcript quantification with GC bias correction (Patro et al. 2017) |
| featureCounts (subread) | 2.0.6 | Gene-level read counting for count-based DE methods (Liao et al. 2014) |
| samtools | 1.19 | BAM handling, flagstat, idxstats |
| FastQC | 0.12.1 | Read quality assessment |
| Trim Galore | 0.6.10 | Adapter and quality trimming |
| MultiQC | 1.21 | Aggregate QC report |
| RSeQC | 5.0.3 | RNA-seq-specific QC: gene body coverage, read distribution, inner distance (Wang et al. 2012) |

**Memory**: STAR genome generation requires 32+ GB RAM for human genome. STAR alignment requires
~30 GB RAM. Kallisto and Salmon are memory-efficient alternatives (~4 GB).

**Environment file**: `environments/rnaseq-env.yml`

---

### Hi-C Environment (`encode-hic`)

For chromatin conformation capture processing following ENCODE Hi-C standards
(Yardimci et al. 2019, Rao et al. 2014).

| Tool | Version | Purpose |
|------|---------|---------|
| BWA-MEM | 0.7.17 | Chimeric read alignment (each mate aligned independently) |
| pairtools | 1.0.3 | Parse, sort, deduplicate, filter contact pairs (Open2C) |
| cooler | 0.9.3 | Multi-resolution contact matrix storage and balancing (Abdennur & Mirny 2020) |
| Juicer | 2.20.00 | Contact matrix generation and HiCCUPS loop calling (Durand et al. 2016) |
| samtools | 1.19 | BAM handling for chimeric alignment parsing |
| bedtools | 2.31.0 | Restriction fragment and TAD boundary operations |
| FastQC | 0.12.1 | Read quality assessment |
| Trim Galore | 0.6.10 | Adapter trimming |
| MultiQC | 1.21 | Aggregate QC reporting |

**Key Hi-C parameters**: Cis/trans ratio > 60%, long-range cis contacts (> 20 kb) > 40%.
Resolution depends on sequencing depth: ~1 billion valid pairs for 5 kb resolution on human.

**Note**: Juicer requires Java 11+. Install via `conda install -c bioconda juicer_tools` or
download the `.jar` directly from the Aiden Lab GitHub.

**Environment file**: `environments/hic-env.yml`

---

### WGBS Environment (`encode-wgbs`)

For whole-genome bisulfite sequencing (DNA methylation) following ENCODE standards
(Foox et al. 2021, Schultz et al. 2015).

| Tool | Version | Purpose |
|------|---------|---------|
| Bismark | 0.24.2 | Bisulfite-aware alignment and methylation extraction (Krueger & Andrews 2011) |
| MethylDackel | 0.6.1 | Fast methylation extraction from bisulfite BAMs (Ryan 2023) |
| samtools | 1.19 | BAM manipulation, merge, index |
| bedtools | 2.31.0 | Interval operations for DMR analysis |
| FastQC | 0.12.1 | Read quality assessment (note: bisulfite libraries have biased base composition) |
| Trim Galore | 0.6.10 | Adapter trimming with --rrbs or default mode |
| MultiQC | 1.21 | Aggregate QC reporting with Bismark module |
| tabix | 1.19 | Index methylation BED files for random access |
| bgzip | 1.19 | Block-gzip compression for indexed access |

**Key WGBS parameters**: Bisulfite conversion rate ≥ 98% (check unmethylated spike-in lambda DNA).
CpG coverage >= 10x for reliable DMR calling. M-bias plots should be checked for end-repair artifacts.

**Environment file**: `environments/wgbs-env.yml`

---

### DNase-seq Environment (`encode-dnaseseq`)

For DNase I hypersensitive site mapping following ENCODE standards
(Thurman et al. 2012, ENCODE Consortium 2020).

| Tool | Version | Purpose |
|------|---------|---------|
| BWA-MEM | 0.7.17 | Read alignment to reference genome |
| Hotspot2 | 2.3.1 | DNase-seq hotspot detection (John et al. 2011) |
| HINT-ATAC | 0.13.2 | TF footprinting from DNase-seq data (Li et al. 2019) |
| F-Seq2 | 2.0.3 | Feature density estimation for peak calling (Boyle et al. 2008, Zhao et al. 2020) |
| samtools | 1.19 | BAM handling and filtering |
| bedtools | 2.31.0 | Interval operations, blacklist filtering |
| FastQC | 0.12.1 | Read quality assessment |
| Trim Galore | 0.6.10 | Adapter trimming |
| MultiQC | 1.21 | Aggregate QC reporting |

**Environment file**: `environments/dnaseseq-env.yml`

---

### CUT&RUN / CUT&Tag Environment (`encode-cutandrun`)

For antibody-targeted chromatin profiling via CUT&RUN (Skene & Henikoff 2017) and
CUT&Tag (Kaya-Okur et al. 2019).

| Tool | Version | Purpose |
|------|---------|---------|
| Bowtie2 | 2.5.3 | Alignment (recommended for shorter CUT&RUN/Tag fragments) |
| SEACR | 1.3 | Sparse Enrichment Analysis for CUT&RUN (Meers et al. 2019) |
| MACS2 | 2.2.9.1 | Alternative peak calling with adjusted parameters |
| samtools | 1.19 | BAM handling, spike-in alignment filtering |
| Picard | 3.1.1 | Duplicate marking (low duplication expected for CUT&RUN/Tag) |
| deeptools | 3.5.5 | Signal tracks, heatmaps, spike-in normalization |
| bedtools | 2.31.0 | Interval operations, suspect list filtering |
| FastQC | 0.12.1 | Read quality assessment |
| Trim Galore | 0.6.10 | Adapter trimming |
| MultiQC | 1.21 | Aggregate QC reporting |

**Key CUT&RUN/Tag notes**: These assays have inherently lower background than ChIP-seq. Do NOT
apply ChIP-seq quality thresholds — use CUT&RUN-specific metrics (Nordin et al. 2023). Apply
the CUT&RUN suspect list instead of the standard ENCODE blacklist. Spike-in normalization
(E. coli DNA for CUT&RUN, carry-over for CUT&Tag) is strongly recommended for quantitative
comparisons.

**Environment file**: `environments/cutandrun-env.yml`

## R/Bioconductor Packages

Install all R packages needed for ENCODE downstream analysis. The install script at
`scripts/install-r-packages.R` handles BiocManager setup, version locking, and
category-based installation.

### Core Genomic Infrastructure

These packages provide the foundation for all genomic data manipulation in R:

| Package | Purpose |
|---------|---------|
| GenomicRanges | Interval arithmetic on genomic coordinates (Lawrence et al. 2013) |
| GenomicFeatures | Gene model and transcript annotation handling |
| rtracklayer | Import/export BED, bigWig, GFF, narrowPeak, broadPeak |
| IRanges | Integer range operations (underlying GenomicRanges) |
| GenomeInfoDb | Chromosome naming conventions (UCSC vs Ensembl vs NCBI) |
| BiocGenerics | Common S4 generics across Bioconductor |
| S4Vectors | S4 class infrastructure for Bioconductor objects |
| AnnotationDbi | Unified interface to annotation databases |
| biomaRt | Ensembl BioMart query interface for gene annotation (Durinck et al. 2009) |

### Differential Analysis

| Package | Purpose |
|---------|---------|
| DESeq2 | Differential gene expression with shrinkage estimators (Love et al. 2014) |
| edgeR | Differential expression using empirical Bayes (Robinson et al. 2010) |
| limma | Linear models for microarray and RNA-seq data (Ritchie et al. 2015) |
| DiffBind | Differential binding analysis for ChIP-seq/ATAC-seq peaks (Stark & Brown 2011) |
| ChIPQC | ChIP-seq quality control in R (Carroll et al. 2014) |
| chromVAR | Chromatin accessibility variation across single cells (Schep et al. 2017) |

### Annotation and Pathway Analysis

| Package | Purpose |
|---------|---------|
| ChIPseeker | Peak annotation and visualization (Yu et al. 2015) |
| annotatr | Annotate genomic regions with CpG islands, genes, enhancers (Cavalcante & Sartor 2017) |
| clusterProfiler | Gene ontology and KEGG pathway enrichment (Yu et al. 2012) |
| org.Hs.eg.db | Human gene annotation database |
| org.Mm.eg.db | Mouse gene annotation database |
| TxDb.Hsapiens.UCSC.hg38.knownGene | Human transcript models (GRCh38) |
| TxDb.Mmusculus.UCSC.mm10.knownGene | Mouse transcript models (mm10) |

### Single-Cell Analysis

| Package | Purpose |
|---------|---------|
| Seurat | Comprehensive single-cell RNA-seq analysis (Hao et al. 2021) |
| Signac | Single-cell chromatin accessibility (ATAC-seq) analysis (Stuart et al. 2021) |
| SingleCellExperiment | Core Bioconductor container for single-cell data |
| scater | Single-cell QC, normalization, visualization (McCarthy et al. 2017) |
| scran | Single-cell normalization and feature selection (Lun et al. 2016) |

### Bulk-to-Single-Cell Deconvolution

| Package | Purpose |
|---------|---------|
| BayesPrism | Bayesian deconvolution with scRNA-seq reference (Chu et al. 2022) |
| InstaPrism | Fast approximation of BayesPrism for large datasets (Wang et al. 2024) |
| MuSiC_deconv | Multi-Subject Single Cell deconvolution (Wang et al. 2019) |
| DWLS | Dampened Weighted Least Squares deconvolution (Tsoucas et al. 2019) |
| BisqueRNA | Reference-based and marker-based deconvolution (Jew et al. 2020) |

### DNA Methylation Analysis

| Package | Purpose |
|---------|---------|
| DMRcate | Differentially methylated region detection (Peters et al. 2021) |
| bsseq | Bisulfite sequencing data handling and smoothing (Hansen et al. 2012) |
| methylKit | Methylation analysis from bisulfite sequencing (Akalin et al. 2012) |

### Visualization

| Package | Purpose |
|---------|---------|
| ComplexHeatmap | Publication-quality heatmaps with annotations (Gu et al. 2016) |
| EnhancedVolcano | Volcano plots for differential expression (Blighe et al. 2018) |
| Gviz | Genome browser-style track visualization (Hahne & Ivanek 2016) |
| ggplot2 | Grammar of graphics for all custom plots (Wickham 2016) |

### Statistics and Batch Correction

| Package | Purpose |
|---------|---------|
| sva (ComBat) | Surrogate variable analysis and batch correction (Leek et al. 2012) |
| WGCNA | Weighted Gene Co-expression Network Analysis (Langfelder & Horvath 2008) |
| ReactomePA | Reactome pathway analysis (Yu & He 2016) |

**Install script**: `scripts/install-r-packages.R`

```bash
# Install all categories
Rscript scripts/install-r-packages.R --all

# Install only specific categories
Rscript scripts/install-r-packages.R --chipseq      # DiffBind, ChIPQC, ChIPseeker
Rscript scripts/install-r-packages.R --rnaseq       # DESeq2, edgeR, limma
Rscript scripts/install-r-packages.R --singlecell   # Seurat, Signac, scater, scran
Rscript scripts/install-r-packages.R --methylation   # DMRcate, bsseq, methylKit
Rscript scripts/install-r-packages.R --deconvolution # BayesPrism, InstaPrism, MuSiC_deconv, DWLS, BisqueRNA
```

## Python Packages

Install Python packages for single-cell analysis, Hi-C processing, signal visualization,
and genomic data manipulation.

### Core Single-Cell Stack

| Package | Purpose |
|---------|---------|
| scanpy | Single-cell RNA-seq analysis framework (Wolf et al. 2018) |
| anndata | Annotated data matrix for single-cell (Virshup et al. 2021) |
| scvi-tools | Deep generative models for single-cell (Gayoso et al. 2022) |
| numpy | Numerical computing |
| pandas | Data manipulation and tabular operations |
| scipy | Scientific computing (sparse matrices, statistics) |
| matplotlib | Plotting foundation |
| seaborn | Statistical visualization |

### Genomics and Signal Processing

| Package | Purpose |
|---------|---------|
| deeptools | Signal tracks, heatmaps, correlation (also CLI; Ramirez et al. 2016) |
| pyBigWig | Read/write bigWig signal files (Ryan 2023) |
| pysam | Python interface to samtools/htslib (Li et al. 2009) |
| pybedtools | Python interface to bedtools (Dale et al. 2011) |

### Hi-C Analysis

| Package | Purpose |
|---------|---------|
| cooler | Multi-resolution contact matrices (Abdennur & Mirny 2020) |
| cooltools | Analysis toolkit for cooler data: TADs, compartments, insulation |
| hic-straw | Read .hic files from Juicer/Juicebox (Durand et al. 2016) |
| pyGenomeTracks | Genome browser visualization including Hi-C tracks |

### Single-Cell QC and Integration

| Package | Purpose |
|---------|---------|
| scrublet | Doublet detection for scRNA-seq (Wolock et al. 2019) |
| CellBender | Remove ambient RNA contamination (Fleming et al. 2023) |
| harmony-pytorch | Batch integration via Harmony in PyTorch (Korsunsky et al. 2019) |
| scanorama | Panoramic stitching of scRNA-seq datasets (Hie et al. 2019) |
| bbknn | Batch-balanced KNN graph construction (Polanski et al. 2020) |

**Install script**: `scripts/install-python-packages.sh`

```bash
# Install all Python packages
bash scripts/install-python-packages.sh --all

# Install only specific categories
bash scripts/install-python-packages.sh --singlecell  # scanpy, scvi-tools, harmony
bash scripts/install-python-packages.sh --hic          # cooler, cooltools, hic-straw
bash scripts/install-python-packages.sh --deeptools    # deeptools, pyBigWig, pysam
```

## Nextflow and Container Setup

ENCODE pipeline execution requires Nextflow DSL2 and a container runtime (Docker or Singularity).

### Nextflow Installation

```bash
# Install Nextflow (requires Java 11+)
curl -s https://get.nextflow.io | bash
mv nextflow /usr/local/bin/

# Verify
nextflow -version
```

### Docker (recommended for local/cloud)

```bash
# macOS
brew install --cask docker

# Linux (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Add current user to docker group (Linux)
sudo usermod -aG docker $USER
```

### Singularity (for HPC clusters)

```bash
# Most HPC clusters have Singularity pre-installed
# Check with: module load singularity && singularity version

# If not available, install via conda:
conda install -c conda-forge singularity
```

### Nextflow Configuration Profiles

The pipeline skills (pipeline-chipseq, pipeline-atacseq, etc.) include `nextflow.config` files
with profiles for local, SLURM, GCP, and AWS execution. Select the appropriate profile:

```bash
# Local with Docker
nextflow run main.nf -profile local

# HPC with Singularity
nextflow run main.nf -profile slurm

# Google Cloud
nextflow run main.nf -profile gcp

# AWS Batch
nextflow run main.nf -profile aws
```

**Install script**: `scripts/install-nextflow.sh`

## Motif Analysis Tools

For transcription factor binding motif discovery and scanning.

| Tool | Version | Type | Purpose |
|------|---------|------|---------|
| HOMER | 4.11 | CLI | De novo and known motif discovery, annotation (Heinz et al. 2010) |
| MEME Suite | 5.5.5 | CLI | MEME, DREME, STREME de novo discovery; FIMO scanning; AME enrichment (Bailey et al. 2015) |
| FIMO | 5.5.5 | CLI (part of MEME Suite) | Motif occurrence scanning across sequences |
| TFBSTools | R | R/Bioconductor | JASPAR motif handling, PFM/PWM conversion, motif scanning in R (Tan & Lenhard 2016) |

### HOMER Installation

```bash
# Download and configure HOMER
mkdir -p ~/software/homer
cd ~/software/homer
wget http://homer.ucsd.edu/homer/configureHomer.pl
perl configureHomer.pl -install homer
perl configureHomer.pl -install hg38   # Human genome
perl configureHomer.pl -install mm10   # Mouse genome

# Add to PATH
export PATH=$PATH:~/software/homer/bin
```

### MEME Suite Installation

```bash
# Via conda (recommended)
conda install -c bioconda meme

# Or from source
wget https://meme-suite.org/meme/meme-software/5.5.5/meme-5.5.5.tar.gz
tar xzf meme-5.5.5.tar.gz
cd meme-5.5.5
./configure --prefix=$HOME/software/meme --enable-build-libxml2 --enable-build-libxslt
make && make install
```

## Walkthrough: Setting Up a Complete ENCODE Analysis Environment

**Goal**: Install all bioinformatics tools needed to process ENCODE data, from raw FASTQ files through peak calling, annotation, and visualization, using Conda environments.
**Context**: ENCODE analysis requires dozens of specialized tools. This skill automates installation with pre-configured Conda environments for each pipeline stage.

### Step 1: Determine required tools by experiment type

```
encode_get_experiment(accession="ENCSR000AKA")
```

Expected output:
```json
{
  "accession": "ENCSR000AKA",
  "assay_title": "Histone ChIP-seq",
  "target": "H3K27ac"
}
```

**Interpretation**: Histone ChIP-seq requires: BWA-MEM (alignment), SAMtools (BAM processing), MACS2 (peak calling), IDR (reproducibility), bedtools (interval operations), deepTools (signal visualization).

### Step 2: Install the ChIP-seq Conda environment

```bash
# Using the pre-configured environment YAML
conda env create -f skills/bioinformatics-installer/scripts/chipseq-env.yml
conda activate encode-chipseq
```

The YAML includes:
```yaml
name: encode-chipseq
channels: [bioconda, conda-forge, defaults]
dependencies:
  - bwa=0.7.17
  - samtools=1.17
  - macs2=2.2.9.1
  - idr=2.0.3
  - bedtools=2.31.0
  - deeptools=3.5.4
  - picard=3.1.1
  - fastqc=0.12.1
  - multiqc=1.17
```

### Step 3: Install additional tools for downstream analysis

For peak annotation and motif analysis:
```bash
conda env create -f skills/bioinformatics-installer/scripts/annotation-env.yml
conda activate encode-annotation
# Includes: HOMER, GREAT, bedtools, R/Bioconductor (ChIPseeker, clusterProfiler)
```

### Step 4: Verify installation

```bash
# Quick verification of key tools
bwa 2>&1 | head -3
samtools --version | head -1
macs2 --version
bedtools --version
```

### Step 5: Download reference data for ENCODE analysis

```
encode_download_files(accessions=["ENCFF001ABC"], download_dir="/data/references")
```

Reference files needed:
- GRCh38 genome FASTA
- ENCODE blacklist v2 (Amemiya et al. 2019)
- Gene annotation GTF (GENCODE v36)

### Integration with downstream skills
- Installed tools are used by → **pipeline-chipseq** through **pipeline-cutandrun** for processing
- Reference data feeds into → **download-encode** for FASTQ retrieval
- Environment setup enables → **quality-assessment** tool execution
- Installed annotation tools support → **peak-annotation** and **motif-analysis**

## Code Examples

### 1. Find experiments to identify required tools

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
      "accession": "ENCSR799GHJ",
      "assay_title": "ATAC-seq",
      "biosample_summary": "pancreatic islet tissue male adult (44 years)",
      "status": "released"
    }
  ]
}
```

**Install decision**: ATAC-seq requires the `atacseq-env.yml` conda environment (Bowtie2 + MACS2 + deeptools + samtools + bedtools).

### 2. Get file info to understand format requirements

```
encode_get_file_info(accession="ENCFF001ABC")
```

Expected output:
```json
{
  "accession": "ENCFF001ABC",
  "file_format": "fastq",
  "file_size_mb": 4521.3,
  "read_length": 100,
  "paired_end": true,
  "platform": "Illumina NovaSeq 6000"
}
```

**Install decision**: Paired-end FASTQ needs Bowtie2 (not BWA for ATAC-seq), Picard for duplicate marking, and samtools for BAM processing.

## Pitfalls & Edge Cases

- **Conda solver conflicts**: Large conda environments with many packages can take hours to solve. Use mamba instead of conda for faster dependency resolution, or install in smaller focused environments.
- **R/Bioconductor version mismatch**: R packages from CRAN and Bioconductor must match the R version. Installing Bioconductor 3.18 packages with R 4.4 will fail silently or produce errors. Use BiocManager::install() to ensure version compatibility.
- **Python 2 vs Python 3**: Some legacy bioinformatics tools (MACS 1.x, old HOMER) require Python 2. Never install Python 2 tools in the same environment as Python 3 tools — use separate conda environments.
- **ARM Mac (M1/M2/M3) compatibility**: Many bioinformatics tools lack native ARM builds. Use `CONDA_SUBDIR=osx-64` or Rosetta 2 emulation for x86_64 packages. Some tools (samtools, BWA) have ARM-native builds.
- **Nextflow requires Java 11+**: Nextflow will not run on Java 8. Check `java -version` before running pipelines. Install with `curl -s https://get.nextflow.io | bash` for correct Java bundling.
- **Docker vs Singularity on HPC**: Most HPC clusters do not allow Docker (requires root). Use Singularity instead. Nextflow supports both via `-profile singularity` or `-profile docker`.

## Literature Foundation

| # | Reference | Key Contribution |
|---|-----------|-----------------|
| 1 | Li & Durbin 2009, Bioinformatics, DOI:10.1093/bioinformatics/btp324 (~30,000 cit) | BWA aligner |
| 2 | Langmead & Salzberg 2012, Nat Methods, DOI:10.1038/nmeth.1923 (~25,000 cit) | Bowtie2 aligner |
| 3 | Li et al. 2009, Bioinformatics, DOI:10.1093/bioinformatics/btp352 (~20,000 cit) | SAMtools/BAM format |
| 4 | Zhang et al. 2008, Genome Biol, DOI:10.1186/gb-2008-9-9-r137 (~7,000 cit) | MACS2 peak caller |
| 5 | Dobin et al. 2013, Bioinformatics, DOI:10.1093/bioinformatics/bts635 (~15,000 cit) | STAR RNA-seq aligner |
| 6 | Love et al. 2014, Genome Biol, DOI:10.1186/s13059-014-0550-8 (~30,000 cit) | DESeq2 |
| 7 | Ramirez et al. 2016, Nucleic Acids Res, DOI:10.1093/nar/gkw257 (~3,000 cit) | deeptools |
| 8 | Wolf et al. 2018, Genome Biol, DOI:10.1186/s13059-017-1382-0 (~5,000 cit) | Scanpy |
| 9 | Hao et al. 2021, Cell, DOI:10.1016/j.cell.2021.04.048 (~8,000 cit) | Seurat v4 |
| 10 | Quinlan & Hall 2010, Bioinformatics, DOI:10.1093/bioinformatics/btq033 (~10,000 cit) | bedtools |
| 11 | Ewels et al. 2016, Bioinformatics, DOI:10.1093/bioinformatics/btw354 (~3,000 cit) | MultiQC |
| 12 | Krueger & Andrews 2011, Bioinformatics, DOI:10.1093/bioinformatics/btr167 (~5,000 cit) | Bismark |
| 13 | Heinz et al. 2010, Molecular Cell, DOI:10.1016/j.molcel.2010.05.004 (~7,000 cit) | HOMER motif analysis |
| 14 | Bailey et al. 2015, Nucleic Acids Res, DOI:10.1093/nar/gkv416 (~3,000 cit) | MEME Suite |
| 15 | Meers et al. 2019, Epigenetics Chromatin, DOI:10.1186/s13072-019-0287-4 (~800 cit) | SEACR for CUT&RUN |
| 16 | Di Tommaso et al. 2017, Nat Biotechnol, DOI:10.1038/nbt.3820 (~2,500 cit) | Nextflow |
| 17 | Landt et al. 2012, Genome Res, DOI:10.1101/gr.136184.111 (~4,000 cit) | ENCODE ChIP-seq standards |
| 18 | ENCODE Consortium 2020, Nature, DOI:10.1038/s41586-020-2493-4 (~1,656 cit) | ENCODE Phase 3 |
| 19 | Amemiya et al. 2019, Sci Rep, DOI:10.1038/s41598-019-45839-z (~1,372 cit) | ENCODE Blacklist v2 |

## Integration

| This skill produces... | Feed into... | Purpose |
|---|---|---|
| Conda environments | **pipeline-chipseq** through **pipeline-cutandrun** | Provide tool dependencies for all pipeline stages |
| Installed reference data | **download-encode** | Reference genomes and annotations for alignment |
| Tool version inventory | **data-provenance** | Record exact tool versions for reproducibility |
| QC tool installations | **quality-assessment** | Enable FastQC, MultiQC, and ENCODE QC metric tools |
| Annotation tool setup | **peak-annotation** | HOMER, ChIPseeker for peak-to-gene assignment |
| Motif scanning tools | **jaspar-motifs** | MEME Suite for motif scanning against JASPAR |
| Visualization tools | **visualization-workflow** | deepTools, IGV, R/ggplot2 for data visualization |
| Liftover utilities | **liftover-coordinates** | UCSC liftOver binary for assembly conversion |

## Related Skills

- **pipeline-guide**: Parent skill for all pipeline execution; provides overview of available pipelines and tool selection guidance
- **pipeline-chipseq**: Uses the ChIP-seq conda environment tools for FASTQ-to-peaks processing
- **pipeline-atacseq**: Uses the ATAC-seq conda environment tools for accessibility analysis
- **pipeline-rnaseq**: Uses the RNA-seq conda environment for expression quantification
- **pipeline-wgbs**: Uses the WGBS conda environment for methylation analysis
- **pipeline-hic**: Uses the Hi-C conda environment for contact matrix generation
- **pipeline-dnaseseq**: Uses the DNase-seq conda environment for hotspot detection
- **pipeline-cutandrun**: Uses the CUT&RUN conda environment for CUT&RUN/CUT&Tag processing
- **quality-assessment**: Quality metrics require properly installed tools to compute
- **setup**: Initial ENCODE Toolkit server setup (MCP connection, not bioinformatics tools)
- **motif-analysis**: Requires HOMER and MEME Suite from this installer
- **visualization-workflow**: Uses deeptools, pyGenomeTracks, and R visualization packages from this installer
- **single-cell-encode**: Uses Seurat, Signac, Scanpy from this installer
- **publication-trust**: Assess scientific integrity of publications before relying on their methods or findings

## Presenting Results

- Present installed tools as a checklist table: tool | version | status (installed/failed/skipped). Group by assay environment. Suggest: "Would you like to verify the installation by running a quick test on sample ENCODE data?"
- If any installation fails, provide the exact error and a targeted fix. Common fixes: update conda, set channel priority, install system dependencies.

## For the request: "$ARGUMENTS"
