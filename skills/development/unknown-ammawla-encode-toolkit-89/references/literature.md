# Bioinformatics Installer — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the bioinformatics-installer skill — papers on reproducible software environments, package management for bioinformatics, and the key tool ecosystem publications that define version requirements.

---

## Reproducible Environments

---

### Grüning et al. 2018 — Bioconda: sustainable bioinformatics software

- **Citation:** Grüning B, Dale R, Sjödin A, Chapman BA, Rowe J, Tomkins-Tinch CH, Valieris R, Köster J; Bioconda Team. Bioconda: sustainable and comprehensive software distribution for the life sciences. Nature Methods, 15(7):475-476, 2018.
- **DOI:** [10.1038/s41592-018-0046-7](https://doi.org/10.1038/s41592-018-0046-7)
- **PMID:** 29967506
- **Citations:** ~1,200
- **Key findings:** Introduced the Bioconda channel, a sustainable and community-driven distribution of bioinformatics software for the conda package manager. Provides >7,000 bioinformatics packages with dependency resolution, version pinning, and automated builds for Linux and macOS. Bioconda is the primary package source for all conda environments in this skill (channel priority: conda-forge > bioconda > defaults). The Bioconda model of community-maintained recipes ensures that tools are installable with consistent, tested dependency trees.

---

### Merkel 2014 — Docker: lightweight Linux containers

- **Citation:** Merkel D. Docker: lightweight Linux containers for consistent development and deployment. Linux Journal, 239(2), 2014.
- **Citations:** ~5,000
- **Key findings:** Docker containers provide OS-level virtualization ensuring that bioinformatics tools run identically regardless of the host system. The ENCODE consortium distributes official Docker images for each pipeline (encodedcc/*), and this skill's Nextflow setup guide configures Docker as the default container runtime. Docker is essential for ENCODE pipeline reproducibility because tool behavior can depend on system libraries, compiler versions, and kernel features.

---

### Kurtzer et al. 2017 — Singularity: containers for scientific computing

- **Citation:** Kurtzer GM, Sochat V, Bauer MW. Singularity: Scientific containers for mobility of compute. PLoS ONE, 12(5):e0177459, 2017.
- **DOI:** [10.1371/journal.pone.0177459](https://doi.org/10.1371/journal.pone.0177459)
- **PMID:** 28494014 | **PMC:** PMC5426675
- **Citations:** ~2,000
- **Key findings:** Introduced Singularity (now Apptainer), a container platform designed for HPC environments where Docker's root-level daemon model is not permitted. Singularity can convert Docker images and run them without root privileges, making it the standard container runtime on academic HPC clusters. This skill's install-nextflow.sh script detects the compute environment and configures either Docker (local/cloud) or Singularity (HPC/SLURM) accordingly.

---

### Di Tommaso et al. 2017 — Nextflow: scalable reproducible pipelines

- **Citation:** Di Tommaso P, Chatzou M, Floden EW, Barja PP, Palumbo E, Notredame C. Nextflow enables reproducible computational workflows. Nature Biotechnology, 35(4):316-319, 2017.
- **DOI:** [10.1038/nbt.3820](https://doi.org/10.1038/nbt.3820)
- **PMID:** 28398311
- **Citations:** ~2,500
- **Key findings:** Introduced Nextflow, a reactive workflow framework that enables writing complex pipelines with simple DSL syntax and running them across local, HPC, and cloud environments. Nextflow handles job scheduling, retry logic, caching (-resume), and container orchestration. The ENCODE Toolkit's 7 pipeline skills are all implemented as Nextflow DSL2 workflows, and this skill's install-nextflow.sh script installs Nextflow along with the appropriate container runtime.

---

### Ewels et al. 2020 — nf-core: community curated bioinformatics pipelines

- **Citation:** Ewels PA, Peltzer A, Fillinger S, Patel H, Alneberg J, Wilm A, Garcia MU, Di Tommaso P, Nahnsen S. The nf-core framework for community-curated bioinformatics pipelines. Nature Biotechnology, 38(3):276-278, 2020.
- **DOI:** [10.1038/s41587-020-0439-x](https://doi.org/10.1038/s41587-020-0439-x)
- **PMID:** 32055031
- **Citations:** ~1,500
- **Key findings:** Established nf-core as a community framework for curated Nextflow pipelines with standardized design patterns, CI testing, and documentation. nf-core pipelines (nf-core/chipseq, nf-core/atacseq, nf-core/rnaseq, nf-core/methylseq, nf-core/hic) represent an alternative implementation of the same processing steps defined in ENCODE pipelines. This skill provides environments compatible with both ENCODE-native and nf-core pipeline implementations.

---

## R/Bioconductor Ecosystem

---

### Huber et al. 2015 — Orchestrating high-throughput genomic analysis with Bioconductor

- **Citation:** Huber W, Carey VJ, Gentleman R, Anders S, Brainard M, Davis S, Dudoit S, Ellis B, Gatto L, Girke T, Gottardo R, Hahne F, Hansen KD, Irizarry RA, Lawrence M, Love MI, MacDonald J, Obenchain V, Oleś AK, Pagès H, Reyes A, Shannon P, Smyth GK, Tenenbaum D, Waldron L, Morgan M. Orchestrating high-throughput genomic analysis with Bioconductor. Nature Methods, 12(2):115-121, 2015.
- **DOI:** [10.1038/nmeth.3252](https://doi.org/10.1038/nmeth.3252)
- **PMID:** 25633503 | **PMC:** PMC4509590
- **Citations:** ~3,500
- **Key findings:** Established Bioconductor as the standard R package ecosystem for genomic data analysis. Bioconductor provides >2,000 packages organized around core data structures (GenomicRanges, SummarizedExperiment, SingleCellExperiment). This skill's install-r-packages.R script installs packages from 8 Bioconductor categories: differential expression (DESeq2, edgeR, limma), single-cell (Seurat, monocle3), ChIP-seq/ATAC-seq (ChIPseeker, DiffBind), genomic ranges (GenomicRanges, rtracklayer), annotation (biomaRt, clusterProfiler), visualization (ComplexHeatmap, EnhancedVolcano), deconvolution (BayesPrism, MuSiC), and methylation (DMRcate, bsseq).

---

## Python Scientific Ecosystem

---

### Wolf et al. 2018 — Scanpy: large-scale single-cell analysis

- **Citation:** Wolf FA, Angerer P, Theis FJ. SCANPY: large-scale single-cell gene expression data analysis. Genome Biology, 19:15, 2018.
- **DOI:** [10.1186/s13059-017-1382-0](https://doi.org/10.1186/s13059-017-1382-0)
- **PMID:** 29409532 | **PMC:** PMC5802054
- **Citations:** ~4,000
- **Key findings:** Introduced Scanpy, the dominant Python framework for single-cell analysis. Built on anndata for efficient data representation and providing preprocessing, clustering, trajectory inference, and visualization functions. This skill installs Scanpy and its ecosystem (anndata, scvi-tools, bbknn) via the Python install script for users processing ENCODE single-cell RNA-seq or ATAC-seq data.

---

## Key Tool Publications

The following publications establish the tools installed by this skill. See the individual pipeline skill literature.md files for detailed descriptions:

---

### Alignment Tools
- **BWA-MEM** (Li & Durbin 2009): DOI 10.1093/bioinformatics/btp324 — Used in ChIP-seq, DNase-seq, Hi-C pipelines
- **Bowtie2** (Langmead & Salzberg 2012): DOI 10.1038/nmeth.1923 — Used in ATAC-seq, CUT&RUN pipelines
- **STAR** (Dobin et al. 2013): DOI 10.1093/bioinformatics/bts635 — Used in RNA-seq pipeline
- **Bismark** (Krueger & Andrews 2011): DOI 10.1093/bioinformatics/btr167 — Used in WGBS pipeline

### Peak Callers
- **MACS2** (Zhang et al. 2008): DOI 10.1186/gb-2008-9-9-r137 — ChIP-seq, ATAC-seq
- **SEACR** (Meers et al. 2019): DOI 10.1186/s13072-019-0287-4 — CUT&RUN/CUT&Tag
- **Hotspot2** (John et al. 2011): DOI 10.1038/ng.759 — DNase-seq

### Quantification
- **RSEM** (Li & Dewey 2011): DOI 10.1186/1471-2105-12-323 — RNA-seq gene/transcript quantification
- **Kallisto** (Bray et al. 2016): DOI 10.1038/nbt.3519 — Fast pseudoalignment

### QC & Utilities
- **SAMtools** (Li et al. 2009): DOI 10.1093/bioinformatics/btp352 — Universal BAM operations
- **BEDTools** (Quinlan & Hall 2010): DOI 10.1093/bioinformatics/btq033 — Genomic arithmetic
- **deepTools** (Ramírez et al. 2016): DOI 10.1093/nar/gkw257 — Signal tracks, heatmaps
- **MultiQC** (Ewels et al. 2016): DOI 10.1093/bioinformatics/btw354 — QC report aggregation
- **FastQC** (Andrews 2010): URL https://www.bioinformatics.babraham.ac.uk/projects/fastqc/
- **Picard** (Broad Institute): URL https://broadinstitute.github.io/picard/

### Hi-C Specific
- **pairtools** (Open2C 2024): DOI 10.1371/journal.pcbi.1012164 — Pair-level processing
- **cooler** (Abdennur & Mirny 2020): DOI 10.1093/bioinformatics/btz540 — Contact matrix storage
- **Juicer tools** (Durand et al. 2016): DOI 10.1016/j.cels.2016.07.002 — .hic generation + HiCCUPS

### Methylation Specific
- **MethylDackel** (Ryan): URL https://github.com/dpryan79/MethylDackel — Methylation extraction
