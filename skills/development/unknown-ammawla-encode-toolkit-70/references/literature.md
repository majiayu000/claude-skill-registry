# Pipeline Guide — Literature References

**Last updated:** 2026-03-07
**Purpose:** Reference catalog for the pipeline-guide skill — papers on workflow engines, containerization technologies, package management, community pipeline standards, and ENCODE pipeline specifications used for orchestrating and executing genomics analysis pipelines.

---

## Workflow Engines

### Di Tommaso et al. 2017 — Nextflow workflow framework

- **Citation:** Di Tommaso P, Chatzou M, Floden EW, Barja PP, Palumbo E, Notredame C. Nextflow enables reproducible computational workflows. *Nature Biotechnology*, 35(4), 316-319, 2017.
- **DOI:** [10.1038/nbt.3820](https://doi.org/10.1038/nbt.3820)
- **PMID:** 28398311
- **Citations:** ~2,000
- **Key findings:** Presented Nextflow, a reactive workflow framework that separates pipeline logic from execution environment, supporting Docker, Singularity, Conda, and native execution across local, HPC (SLURM, SGE, PBS), and cloud (AWS Batch, Google Life Sciences) platforms. Nextflow uses a dataflow programming model where processes communicate through asynchronous channels. All ENCODE toolkit pipeline skills (pipeline-chipseq, pipeline-atacseq, pipeline-rnaseq, pipeline-wgbs, pipeline-hic, pipeline-dnaseseq, pipeline-cutandrun) use Nextflow as their execution engine.

---

### Ewels et al. 2020 — nf-core community pipelines

- **Citation:** Ewels PA, Peltzer A, Fillinger S, Patel H, Alneberg J, Wilm A, Garcia MU, Di Tommaso P, Nahnsen S. The nf-core framework for community-curated bioinformatics pipelines. *Nature Biotechnology*, 38(3), 276-278, 2020.
- **DOI:** [10.1038/s41587-020-0439-x](https://doi.org/10.1038/s41587-020-0439-x)
- **PMID:** 32055031
- **Citations:** ~1,500
- **Key findings:** Described nf-core, a community framework for curated Nextflow pipelines with standardized structure, testing, documentation, and continuous integration. nf-core pipelines follow best practices including containerized software, test datasets, and parameter validation. The ENCODE toolkit pipeline skills adopt nf-core conventions for pipeline structure (main.nf, nextflow.config, Dockerfile) and serve as a model for how domain-specific pipelines should be organized and distributed.

---

### Vivian et al. 2017 — Toil workflow engine

- **Citation:** Vivian J, Rao AA, Nothaft FA, Ketchum C, Armstrong J, Novak A, Pfeil J, Narkizian J, Deran AD, Musselman-Brown A, Schmidt H, Amstutz P, Craft B, Goldman M, Rober K, Zhu J, Haussler D, Paten B. Toil enables reproducible, open source, big biomedical data analyses. *Nature Biotechnology*, 35(4), 314-316, 2017.
- **DOI:** [10.1038/nbt.3772](https://doi.org/10.1038/nbt.3772)
- **PMID:** 28398314
- **Citations:** ~400
- **Key findings:** Introduced Toil, a scalable, efficient workflow engine that supports CWL and WDL workflow languages and can run on multiple cloud platforms (AWS, Google Cloud, Azure) and HPC systems. Toil was used to process the TCGA dataset (over 20,000 samples) and supports ENCODE CWL pipeline specifications. As the original execution engine for many ENCODE pipelines, Toil provides an alternative to Nextflow for running ENCODE-standard analyses, particularly for CWL-based workflows.

---

## Containerization

### Kurtzer et al. 2017 — Singularity containers for HPC

- **Citation:** Kurtzer GM, Sochat V, Bauer MW. Singularity: scientific containers for mobility of compute. *PLoS ONE*, 12(5), e0177459, 2017.
- **DOI:** [10.1371/journal.pone.0177459](https://doi.org/10.1371/journal.pone.0177459)
- **PMID:** 28494014 | **PMC:** PMC5426675
- **Citations:** ~1,200
- **Key findings:** Described Singularity, a container system designed for HPC environments where Docker cannot run due to security restrictions (root privilege requirements). Singularity containers run as the user's own processes without requiring elevated privileges, making them compatible with shared computing clusters. The ENCODE toolkit pipeline skills support Singularity via the SLURM profile configuration, enabling pipeline execution on institutional HPC systems where Docker is not permitted.

---

### Merkel 2014 — Docker containerization

- **Citation:** Merkel D. Docker: lightweight Linux containers for consistent development and deployment. *Linux Journal*, 2014(239), 2, 2014.
- **Citations:** ~800
- **Key findings:** Provided the foundational description of Docker, the container platform that packages applications with their dependencies into portable, isolated environments. Docker containers ensure that software runs identically across different computing environments. All ENCODE toolkit pipeline skills include Dockerfiles specifying the exact tool versions, libraries, and dependencies needed for each pipeline stage, guaranteeing reproducibility from local development to cloud deployment.

---

## Package Management

### Grüning et al. 2018 — Bioconda package management

- **Citation:** Grüning B, Dale R, Sjodin A, Chapman BA, Rowe J, Tomkins-Tinch CH, Valieris R, Koester J, Bioconda Team. Bioconda: sustainable and comprehensive software distribution for the life sciences. *Nature Methods*, 15(7), 475-476, 2018.
- **DOI:** [10.1038/s41592-018-0046-7](https://doi.org/10.1038/s41592-018-0046-7)
- **PMID:** 29967506
- **Citations:** ~1,200
- **Key findings:** Introduced Bioconda, a channel for the Conda package manager providing over 3,000 bioinformatics packages with automatic container generation (BioContainers). Bioconda ensures reproducible installation of specific tool versions across platforms. ENCODE pipeline tools (BWA, MACS2, STAR, Bowtie2, Bismark, pairtools, SEACR, etc.) are distributed through Bioconda, and the toolkit's Nextflow configurations use Conda environments as a fallback when containers are not available.

---

## ENCODE Pipeline Standards

### ENCODE Project Consortium 2020 — ENCODE pipelines and standards

- **Citation:** ENCODE Project Consortium, Moore JE, Purcaro MJ, Pratt HE, Epstein CB, Shoresh N, Adrian J, Kawli T, Davis CA, Dobin A, et al. Expanded encyclopaedias of DNA elements in the human and mouse genomes. *Nature*, 583(7818), 699-710, 2020.
- **DOI:** [10.1038/s41586-020-2493-4](https://doi.org/10.1038/s41586-020-2493-4)
- **PMID:** 32728249 | **PMC:** PMC7410828
- **Citations:** ~2,000
- **Key findings:** Documented the standardized computational pipelines used to process all ENCODE Phase 3 data, including ChIP-seq, ATAC-seq, RNA-seq, WGBS, Hi-C, and DNase-seq pipelines with defined quality metrics for each assay. The pipelines specify exact software versions, reference genomes, and quality thresholds. The pipeline-guide skill maps these ENCODE-standard pipelines to their corresponding toolkit implementations, ensuring that users can reproduce ENCODE data processing with identical parameters.

---
